# Section 08: Auto-Complete & Help

## Overview

The CLI provides shell auto-completion for bash, zsh, and fish shells. Help output is organized hierarchically with command descriptions, argument details, and usage examples. The --help flag shows context-sensitive help at any level of the command tree.

## Architecture

```
Help System
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

$ voiceagent --help
Usage: voiceagent [options] [command]

CLI for managing Voice Agent resources.

Options:
  -V, --version              Show version number
  -h, --help                 Show help

Commands:
  agents           Manage AI voice agents
  calls            Manage calls
  campaigns        Manage outbound campaigns
  config           Manage CLI configuration

$ voiceagent agents --help
Usage: voiceagent agents [options] [command]

Manage AI voice agents.

Commands:
  list             List all agents
  get <id>         Get agent details
  create           Create a new agent
  update <id>      Update agent configuration
  delete <id>      Delete an agent
  deploy <id>      Deploy agent to production

$ voiceagent agents create --help
Usage: voiceagent agents create [options]

Create a new agent.

Options:
  --name <name>          Agent name
  --voice-provider <p>   Voice provider (elevenlabs, azure, google, amazon)
  --voice-id <id>        Voice ID
  --model-provider <p>   Model provider (openai, anthropic, google)
  --model <model>        Model name
  --file <path>          JSON/YAML file with agent configuration
  -h, --help             Display help

Auto-Complete:
  $ voiceagent agents [TAB][TAB]
  list    get    create    update    delete    deploy

  $ voiceagent agents create --voice-provider [TAB][TAB]
  elevenlabs    azure    google    amazon

  $ voiceagent agents create --model-provider [TAB][TAB]
  openai    anthropic    google
```

## Design Decisions

- **Commander.js Built-in Help**: Auto-generates help from command definitions
- **Shell Completion via commander**: `commander` package provides completion generation
- **Help Topics**: Extended help available via `voiceagent help <topic>` for detailed guides
- **Usage Examples**: Every command includes practical examples in help text

## Implementation Approach

```typescript
import { Command } from 'commander';

// Help configuration
const program = new Command();

program
  .name('voiceagent')
  .description('CLI for managing Voice Agent resources.')
  .version('1.0.0')
  .helpOption('-h, --help', 'Display help')
  .addHelpText('after', `
Examples:
  $ voiceagent agents list --status active
  $ voiceagent agents create --name "Support Bot" --file config.json
  $ voiceagent agents deploy ag_123
  $ voiceagent calls list --limit 50

Documentation: https://docs.voiceagent.com/cli
Report issues: https://github.com/voiceagent/cli/issues
  `);

// Command-specific help text
const agentsCommand = new Command('agents')
  .description('Manage AI voice agents')
  .addHelpText('after', `
Examples:
  List all agents:            voiceagent agents list
  Get agent details:          voiceagent agents get <id>
  Create agent interactively: voiceagent agents create
  Create from config file:    voiceagent agents create --file agent.json
  Delete agent:               voiceagent agents delete <id> --force
  Deploy to production:       voiceagent agents deploy <id>
  `);

// Shell auto-completion setup
function setupCompletion(program: Command): void {
  // Generate completion script
  program.command('completion')
    .description('Generate shell completion script')
    .argument('[shell]', 'Shell type (bash|zsh|fish)')
    .action((shell?: string) => {
      const shellType = shell || detectShell();

      switch (shellType) {
        case 'bash':
          console.log(`# Add this to your ~/.bashrc or ~/.bash_profile
eval "$(voiceagent completion bash)"
`);
          console.log(generateBashCompletion(program));
          break;
        case 'zsh':
          console.log(`# Add this to your ~/.zshrc
eval "$(voiceagent completion zsh)"
`);
          console.log(generateZshCompletion(program));
          break;
        case 'fish':
          console.log(`# Add this to ~/.config/fish/config.fish
voiceagent completion fish | source
`);
          console.log(generateFishCompletion(program));
          break;
      }
    });
}

function detectShell(): string {
  const shell = process.env.SHELL || '';
  if (shell.includes('zsh')) return 'zsh';
  if (shell.includes('fish')) return 'fish';
  return 'bash';
}

// Generate bash completion
function generateBashCompletion(program: Command): string {
  const commands = program.commands.map(cmd => cmd.name());
  const options = program.options.map(opt => opt.long || opt.short);

  return `_voiceagent_completions() {
    local cur prev words cword
    _init_completion || return

    if [[ $cword -eq 1 ]]; then
      COMPREPLY=($(compgen -W "${commands.join(' ')}" -- "$cur"))
      return
    fi

    case "\${words[1]}" in
      agents)
        COMPREPLY=($(compgen -W "list get create update delete deploy" -- "$cur"))
        ;;
      calls)
        COMPREPLY=($(compgen -W "list get monitor transfer" -- "$cur"))
        ;;
      config)
        COMPREPLY=($(compgen -W "set get list profile" -- "$cur"))
        ;;
    esac
  } &&
  complete -F _voiceagent_completions voiceagent`;
}

// Extended help topics
const helpTopics: Record<string, string> = {
  'authentication': `
Authentication Help
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

The CLI supports the following authentication methods:
  1. API Key (recommended):  --api-key <key> or VOICE_AGENT_API_KEY
  2. Config file:            Set via 'voiceagent config set api_key <key>'
  3. Interactive:            Prompts when no key is found

Create an API key: https://dashboard.voiceagent.com/settings/api-keys
  `,
  'output-format': `
Output Format Help
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  --output table    Tabular display (default for terminals)
  --output json     JSON format (default for CI/pipe)
  --output yaml     YAML format

Use '--no-color' to disable colored output.
  `,
};

program.command('help')
  .argument('[topic]', 'Help topic')
  .action((topic?: string) => {
    if (topic && helpTopics[topic]) {
      console.log(helpTopics[topic]);
    } else if (topic) {
      console.log(`Unknown help topic: ${topic}`);
      console.log('Available topics:', Object.keys(helpTopics).join(', '));
    } else {
      program.help();
    }
  });
```

## Integration Points

- **Shell Integration**: Users source completion script in their shell config
- **Homebrew**: Homebrew installation includes automatic completion setup
- **CI/CD**: Help available in CI for debugging — `voiceagent --help` always works
- **Man Pages**: Generate man page from help text for Linux package distribution

## Production Considerations

- **Completion Performance**: Completion scripts must be fast — avoid API calls during tab completion
- **Update Notification**: Check for CLI updates asynchronously, non-blocking
- **Help Text Maintenance**: Keep help text in sync with command definitions
- **Internationalization**: Help text can be localized by loading language files

## Open-Source Tools

- **Commander.js**: Built-in help generation and completion support
- **chalk**: Help text formatting with color highlighting
