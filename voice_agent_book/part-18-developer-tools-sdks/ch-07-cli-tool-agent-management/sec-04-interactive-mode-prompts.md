# Section 04: Interactive Mode & Prompts

## Overview

The CLI provides rich interactive mode using Inquirer.js prompts. Interactive mode is the default for commands like `create` that require complex input. Auto-complete suggests valid values for provider names, model names, and other enum-like fields. Confirmation dialogs prevent accidental destructive operations.

## Architecture

```
Interactive Prompt Flow
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

$ voiceagent agents create
? Agent Name: Customer Support Bot
? Description: Handles customer refund requests
? Voice Provider: (Use arrow keys)
❯ elevenlabs
  azure
  google
  amazon
? Voice ID: 21m00Tcm4TlvDq8ikWAM
? Voice Speed: 1.0
? Model Provider: openai
? Model: gpt-4o
? Temperature: 0.7
? Max Tokens: 4096
? Greeting: Hello, thank you for calling. How can I help?
? Timezone: UTC

Confirm creation:
  Name: Customer Support Bot
  Voice: elevenlabs / 21m00Tcm4TlvDq8ikWAM
  Model: openai / gpt-4o

? Proceed? (Y/n) Yes

✓ Agent created: ag_abc123

Non-Interactive Mode:
  $ voiceagent agents create --file agent-config.json
  → Skips all prompts, creates agent from file

  $ voiceagent agents delete ag_123 --force
  → Skips confirmation prompt
```

## Design Decisions

- **Interactive by Default**: Commands with no flags enter interactive mode for guided input
- **Auto-Complete**: Suggest valid values for enum fields; fetch options from API for dynamic fields
- **Confirmation for Destructive Actions**: Delete, deploy, transfer require explicit confirmation
- **Progress Indicators**: Spinners for API calls; progress bars for batch operations

## Implementation Approach

```typescript
import { input, select, confirm, password, checkbox } from '@inquirer/prompts';
import ora from 'ora';

// Interactive agent creation
async function interactiveCreateAgent(ctx: CommandContext): Promise<CreateAgentRequest> {
  const name = await input({
    message: 'Agent Name:',
    validate: (value) => value.length > 0 ? true : 'Name is required',
  });

  const description = await input({
    message: 'Description:',
    default: '',
  });

  const voiceProvider = await select({
    message: 'Voice Provider:',
    choices: [
      { name: 'ElevenLabs', value: 'elevenlabs' },
      { name: 'Azure', value: 'azure' },
      { name: 'Google', value: 'google' },
      { name: 'Amazon', value: 'amazon' },
    ],
  });

  const voiceId = await input({
    message: 'Voice ID:',
    validate: (value) => value.length > 0 ? true : 'Voice ID is required',
  });

  const speed = await input({
    message: 'Voice Speed:',
    default: '1.0',
    validate: (value) => {
      const num = parseFloat(value);
      return num >= 0.5 && num <= 2.0 ? true : 'Must be between 0.5 and 2.0';
    },
  });

  const modelProvider = await select({
    message: 'Model Provider:',
    choices: [
      { name: 'OpenAI', value: 'openai' },
      { name: 'Anthropic', value: 'anthropic' },
      { name: 'Google', value: 'google' },
    ],
  });

  const model = await input({
    message: 'Model:',
    default: modelProvider === 'openai' ? 'gpt-4o' : 'claude-3-opus-20240229',
  });

  const temperature = await input({
    message: 'Temperature:',
    default: '0.7',
  });

  const maxTokens = await input({
    message: 'Max Tokens:',
    default: '4096',
  });

  const greeting = await input({
    message: 'Greeting:',
    default: '',
  });

  const request: CreateAgentRequest = {
    name,
    description: description || undefined,
    voice: {
      provider: voiceProvider as VoiceProvider,
      voiceId,
      speed: parseFloat(speed),
    },
    model: {
      provider: modelProvider as ModelProvider,
      model,
      temperature: parseFloat(temperature),
      maxTokens: parseInt(maxTokens),
    },
    greeting: greeting || undefined,
  };

  // Confirmation
  console.log('\nConfirm creation:');
  console.log(`  Name: ${request.name}`);
  console.log(`  Voice: ${request.voice.provider} / ${request.voice.voiceId}`);
  console.log(`  Model: ${request.model.provider} / ${request.model.model}\n`);

  const confirmed = await confirm({ message: 'Proceed?', default: true });

  if (!confirmed) {
    console.log('Cancelled.');
    process.exit(0);
  }

  return request;
}

// Handler with progress indicator
async function handleCreateAgent(ctx: CommandContext, options: Record<string, unknown>): Promise<void> {
  let request: CreateAgentRequest;

  if (options.file) {
    // Read from file
    const filePath = options.file as string;
    const content = await fs.promises.readFile(filePath, 'utf-8');
    request = JSON.parse(content);
  } else {
    // Interactive mode
    request = await interactiveCreateAgent(ctx);
  }

  const spinner = ora('Creating agent...').start();

  try {
    const client = createClient(ctx);
    const agent = await client.agents.create(request);
    spinner.succeed(`Agent created: ${agent.id}`);
    printOutput(agent, ctx);
  } catch (error) {
    spinner.fail('Failed to create agent');
    throw error;
  }
}

// Auto-complete for dynamic values
async function promptAgentSelection(client: VoiceAgent, message: string): Promise<string> {
  const agents = await client.agents.list({ limit: 100 });

  const { select } = await import('@inquirer/prompts');

  const choice = await select({
    message,
    choices: agents.data.map(a => ({
      name: `${a.name} (${a.id})`,
      value: a.id,
    })),
    // Searchable
    pageSize: 10,
  });

  return choice;
}

// Confirmation for destructive actions
async function confirmDestructive(
  message: string,
  ctx: CommandContext,
): Promise<boolean> {
  if (ctx.options.force) {
    return true;
  }

  return confirm({
    message,
    default: false,
  });
}
```

## Integration Points

- **Inquirer.js**: Rich interactive prompts with validation and auto-complete
- **Ora**: Terminal spinners for async operations
- **CLI Handler**: Interactive mode automatically selected when no input flags provided

## Production Considerations

- **Non-Interactive Detection**: Skip prompts when stdout is not a TTY (pipelines, CI)
- **Input Validation**: All prompts validate input before proceeding
- **Sensitive Input**: Use password-style prompt for API keys (masked input)
- **Default Values**: Sensible defaults reduce keystrokes for common cases

## Open-Source Tools

- **@inquirer/prompts**: Interactive CLI prompts
- **ora**: Elegant terminal spinners
- **chalk**: Terminal string styling for colorful output
