# Section 01: CLI Architecture

## Overview

The Voice Agent CLI uses Commander.js for command parsing and middleware pipeline for cross-cutting concerns. The architecture follows a layered pattern: command definition → argument parsing → middleware pipeline → handler execution → output formatting. The CLI supports both interactive and non-interactive modes for CI/CD integration.

## Architecture

```
CLI Architecture Layers
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[User Input] → [Commander.js] → [Middleware Pipeline] → [Handler] → [Output]
                    │                    │                   │
              ┌─────┴──────┐     ┌───────┴───────┐    ┌─────┴──────┐
              │ Command    │     │ 1. Auth       │    │ Table      │
              │ Tree       │     │ 2. Config     │    │ JSON       │
              │            │     │ 3. Rate Limit │    │ YAML       │
              │ agents     │     │ 4. Logging    │    │ Color      │
              │   list     │     │ 5. Telemetry  │    │            │
              │   create   │     └───────────────┘    └────────────┘
              │   deploy   │
              │ calls      │
              │ config     │
              └────────────┘

Middleware Pipeline:
  [Input] → [Auth Check] → [Config Load] → [Rate Limit] → [Logging] → [Handler]
                │               │              │              │
           Check API key   Load .voiceagentrc  Respect     Log command
           or prompt       from ~/.config      throttle    execution

Plugin System:
  interface Plugin {
    name: string;
    hook: 'pre' | 'post';
    execute(context: CommandContext): Promise<void>;
  }

  Examples:
    - telemetry plugin: sends anonymous usage data
    - update plugin: checks for CLI updates
    - completion plugin: generates shell completions
```

## Design Decisions

- **Commander.js Over oclif**: Lighter weight, simpler API, better for smaller CLI tools
- **Middleware Pipeline**: Cross-cutting concerns (auth, config, logging) handled once per command
- **Plugin System**: Extensible without modifying core CLI code
- **Async First**: All handlers support async/await for API calls

## Implementation Approach

```typescript
// Main CLI entry point
#!/usr/bin/env node
import { Command } from 'commander';
import { AuthMiddleware } from './middleware/auth';
import { ConfigMiddleware } from './middleware/config';
import { LoggingMiddleware } from './middleware/logging';
import { agentsCommand } from './commands/agents';
import { callsCommand } from './commands/calls';
import { campaignsCommand } from './commands/campaigns';
import { configCommand } from './commands/config';
import { Pipeline } from './pipeline';

const program = new Command();

program
  .name('voiceagent')
  .description('CLI for managing Voice Agent resources')
  .version('1.0.0')
  .option('--api-key <key>', 'API key (overrides config)')
  .option('--environment <env>', 'Environment (production|sandbox)')
  .option('--output <format>', 'Output format (table|json|yaml)', 'table')
  .option('--no-color', 'Disable colorized output');

// Register middleware
const pipeline = new Pipeline();
pipeline.use(new AuthMiddleware());
pipeline.use(new ConfigMiddleware());
pipeline.use(new LoggingMiddleware());

// Register commands
program.addCommand(agentsCommand(pipeline));
program.addCommand(callsCommand(pipeline));
program.addCommand(campaignsCommand(pipeline));
program.addCommand(configCommand(pipeline));

// Global error handler
program.hook('postAction', (command, actionResult) => {
  if (actionResult instanceof Error) {
    console.error(`Error: ${actionResult.message}`);
    process.exit(1);
  }
});

program.parse(process.argv);

// Middleware pipeline
interface CommandContext {
  command: string;
  args: Record<string, unknown>;
  options: Record<string, unknown>;
  config: Record<string, unknown>;
  apiKey: string;
  environment: string;
  output: string;
  color: boolean;
}

interface Middleware {
  name: string;
  execute(context: CommandContext): Promise<CommandContext>;
}

class Pipeline {
  private middlewares: Middleware[] = [];

  use(middleware: Middleware): void {
    this.middlewares.push(middleware);
  }

  async run(context: CommandContext): Promise<CommandContext> {
    let ctx = context;
    for (const middleware of this.middlewares) {
      ctx = await middleware.execute(ctx);
    }
    return ctx;
  }
}

// Authentication middleware
class AuthMiddleware implements Middleware {
  name = 'auth';

  async execute(context: CommandContext): Promise<CommandContext> {
    const apiKey = context.options.apiKey as string
      || context.config.apiKey
      || process.env.VOICE_AGENT_API_KEY;

    if (!apiKey) {
      const { input } = await import('@inquirer/prompts');
      const key = await input({ message: 'Enter your API key:' });
      context.apiKey = key;
    } else {
      context.apiKey = apiKey;
    }

    return context;
  }
}
```

## Integration Points

- **Config File**: `~/.config/voiceagent/.voiceagentrc` for persistent settings
- **Shell Completion**: Auto-complete for bash/zsh/fish
- **CI/CD**: Non-interactive mode with `--api-key` and `--output json` flags

## Production Considerations

- **Update Notifications**: Check for CLI updates on background
- **Telemetry**: Anonymous usage data (commands used, errors) with opt-out
- **Error Formatting**: Consistent error output — red text, error code, suggestion
- **Progress Indicators**: Spinners for long-running operations

## Open-Source Tools

- **Commander.js**: Command-line interface framework
- **@inquirer/prompts**: Interactive prompts for CLI input
- **chalk**: Terminal string coloring
- **ora**: Terminal spinners for async operations
