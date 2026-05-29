# Section 02: Command Structure Design

## Overview

CLI commands follow a tree structure with nested subcommands, arguments, flags, and options. Commands are organized by resource (agents, calls, campaigns) with consistent naming across subcommands (list, get, create, update, delete, deploy).

## Architecture

```
Command Tree
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

$ voiceagent <command> [subcommand] [arguments] [options]

Commands:
  agents          Manage AI voice agents
    list          List all agents                           [flags: --status, --limit, --cursor]
    get <id>      Get agent details
    create        Create a new agent (interactive or JSON)
    update <id>   Update agent configuration                [flags: --file, --set]
    delete <id>   Delete an agent
    deploy <id>   Deploy agent to production                [flags: --version, --rollback]

  calls           Manage calls
    list          List call history                         [flags: --agent, --status, --from, --to]
    get <id>      Get call details
    monitor       Real-time call monitoring                 [flags: --filter]
    transfer <id> Transfer a call                           [flags: --target, --priority]

  campaigns       Manage outbound campaigns
    list          List campaigns
    create        Create campaign
    start <id>    Start campaign execution
    pause <id>    Pause campaign
    resume <id>   Resume paused campaign
    stats <id>    Get campaign statistics

  config          Manage CLI configuration
    set <key> <value>   Set configuration value
    get <key>           Get configuration value
    list                List all config
    profile             Manage profiles
      create <name>     Create new profile
      use <name>        Switch profile
      list              List profiles

Global Flags:
  --api-key <key>       API key (overrides config)
  --environment <env>   Environment (production|sandbox)
  --output <format>     Output format (table|json|yaml)
  --no-color           Disable colors
  --help, -h           Show help
  --version, -v         Show version
```

## Design Decisions

- **Nested Subcommands**: `agents list`, `agents get <id>` — predictable and scoped
- **Positional Arguments**: Resource IDs as positional arguments; filters as flags
- **Consistent Order**: `command subcommand [args] [flags]` — standardized across all commands
- **Interactive Default**: `create` without `--file` flag opens interactive prompts

## Implementation Approach

```typescript
import { Command } from 'commander';

// Agent command definitions
export function agentsCommand(pipeline: Pipeline): Command {
  const agents = new Command('agents')
    .description('Manage AI voice agents');

  agents
    .command('list')
    .description('List all agents')
    .option('--status <status>', 'Filter by status (active|paused|draft)')
    .option('--limit <number>', 'Maximum results', '20')
    .option('--cursor <cursor>', 'Pagination cursor')
    .action(async (options) => {
      const ctx = await pipeline.run({
        command: 'agents list',
        args: {},
        options,
      });
      await handleListAgents(ctx);
    });

  agents
    .command('get')
    .description('Get agent details')
    .argument('<id>', 'Agent ID')
    .action(async (id, options) => {
      const ctx = await pipeline.run({
        command: 'agents get',
        args: { id },
        options,
      });
      await handleGetAgent(ctx, id);
    });

  agents
    .command('create')
    .description('Create a new agent')
    .option('--file <path>', 'JSON/YAML file with agent config')
    .option('--name <name>', 'Agent name')
    .option('--voice-provider <provider>', 'Voice provider')
    .option('--voice-id <id>', 'Voice ID')
    .option('--model-provider <provider>', 'AI model provider')
    .option('--model <model>', 'Model name')
    .action(async (options) => {
      const ctx = await pipeline.run({
        command: 'agents create',
        args: {},
        options,
      });
      await handleCreateAgent(ctx, options);
    });

  agents
    .command('update')
    .description('Update agent configuration')
    .argument('<id>', 'Agent ID')
    .option('--file <path>', 'JSON/YAML file with agent config')
    .option('--set <key=value...>', 'Set individual config values')
    .action(async (id, options) => {
      const ctx = await pipeline.run({
        command: 'agents update',
        args: { id },
        options,
      });
      await handleUpdateAgent(ctx, id, options);
    });

  agents
    .command('delete')
    .description('Delete an agent')
    .argument('<id>', 'Agent ID')
    .option('--force', 'Skip confirmation prompt')
    .action(async (id, options) => {
      const ctx = await pipeline.run({
        command: 'agents delete',
        args: { id },
        options,
      });
      await handleDeleteAgent(ctx, id, options);
    });

  agents
    .command('deploy')
    .description('Deploy agent to production')
    .argument('<id>', 'Agent ID')
    .option('--version <tag>', 'Version tag for deployment')
    .option('--rollback', 'Rollback to previous version')
    .action(async (id, options) => {
      const ctx = await pipeline.run({
        command: 'agents deploy',
        args: { id },
        options,
      });
      await handleDeployAgent(ctx, id, options);
    });

  return agents;
}
```

## Integration Points

- **SDK Integration**: Command handlers use the TypeScript SDK for API calls
- **Config System**: Global options merge with config file values
- **Help Generation**: Commander.js auto-generates --help output from descriptions

## Production Considerations

- **Argument Validation**: Validate argument formats (ID prefixes, UUIDs) before API calls
- **Sensitive Data**: Never log API keys or secrets in command output
- **Large Output**: Paginate long lists automatically; prompt to continue
- **Cancellation**: Handle Ctrl+C gracefully — clean up any in-progress operations

## Open-Source Tools

- **Commander.js**: Command parsing with nested subcommands
- **yargs**: Alternative CLI framework for comparison
