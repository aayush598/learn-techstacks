# Section 05: Output Formatting

## Overview

The CLI supports multiple output formats: table (default for humans), JSON (for programmatic consumption), and YAML (for configuration export). Output is colorized by default with syntax highlighting. Custom formatters can be registered for resource-specific display.

## Architecture

```
Output Format Selection
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

$ voiceagent agents list --output table
┌─────────┬──────────────────────┬────────┬──────────────────────────────┐
│ ID      │ Name                 │ Status │ Created                      │
├─────────┼──────────────────────┼────────┼──────────────────────────────┤
│ ag_abc  │ Customer Support Bot │ active │ 2025-06-01T10:00:00.000Z    │
│ ag_def  │ Sales Assistant      │ draft  │ 2025-05-28T14:30:00.000Z    │
│ ag_ghi  │ Survey Agent         │ paused │ 2025-05-15T08:00:00.000Z    │
└─────────┴──────────────────────┴────────┴──────────────────────────────┘

$ voiceagent agents list --output json
{
  "data": [
    { "id": "ag_abc", "name": "Customer Support Bot", "status": "active", ... },
    { "id": "ag_def", "name": "Sales Assistant", "status": "draft", ... }
  ],
  "pagination": { "cursor": null, "has_more": false }
}

$ voiceagent agents get ag_abc --output yaml
id: ag_abc
name: Customer Support Bot
status: active
voice:
  provider: elevenlabs
  voiceId: "21m00Tcm4TlvDq8ikWAM"
  speed: 1.0
model:
  provider: openai
  model: gpt-4o
  temperature: 0.7
  maxTokens: 4096
createdAt: "2025-06-01T10:00:00.000Z"

Color Key:
  - Green: success, active status
  - Yellow: warning, paused status
  - Red: error, failed status
  - Blue: IDs and metadata
  - Gray: timestamps
```

## Design Decisions

- **Default to Table**: Human-readable tables for interactive use
- **JSON for Automation**: Machine-parsable output for CI/CD and scripting
- **YAML for Config Export**: Editable YAML output that can be fed back into `create --file`
- **Color Coding**: Consistent color scheme — green=good, yellow=warning, red=error

## Implementation Approach

```typescript
import { table } from 'table';
import chalk from 'chalk';
import yaml from 'yaml';
import { Writable } from 'node:stream';

// Output format types
type OutputFormat = 'table' | 'json' | 'yaml';

// Abstract formatter
interface Formatter<T> {
  format(data: T, context: OutputContext): string;
}

interface OutputContext {
  format: OutputFormat;
  color: boolean;
}

// Table formatter for agents
class AgentTableFormatter implements Formatter<Agent | Agent[]> {
  format(data: Agent | Agent[], context: OutputContext): string {
    const agents = Array.isArray(data) ? data : [data];

    const header = ['ID', 'Name', 'Status', 'Created'];
    const rows = agents.map(agent => [
      context.color ? chalk.blue(agent.id) : agent.id,
      agent.name,
      this.formatStatus(agent.status, context.color),
      context.color ? chalk.gray(new Date(agent.createdAt).toLocaleString()) : agent.createdAt,
    ]);

    return table([header, ...rows], {
      border: {
        topBody: '─', topJoin: '┬', topLeft: '┌', topRight: '┐',
        bottomBody: '─', bottomJoin: '┴', bottomLeft: '└', bottomRight: '┘',
        bodyLeft: '│', bodyRight: '│', bodyJoin: '│',
        joinBody: '─', joinLeft: '├', joinRight: '┤', joinJoin: '┼',
      },
    });
  }

  private formatStatus(status: string, color: boolean): string {
    if (!color) return status;

    switch (status) {
      case 'active': return chalk.green(status);
      case 'paused': return chalk.yellow(status);
      case 'draft': return chalk.gray(status);
      case 'archived': return chalk.red(status);
      default: return status;
    }
  }
}

// JSON formatter
class JsonFormatter implements Formatter<unknown> {
  format(data: unknown, context: OutputContext): string {
    return JSON.stringify(data, null, 2);
  }
}

// YAML formatter
class YamlFormatter implements Formatter<unknown> {
  format(data: unknown, context: OutputContext): string {
    return yaml.stringify(data, { indent: 2 });
  }
}

// Output formatter registry
class OutputFormatter {
  private formatters: Map<string, Formatter<unknown>> = new Map();

  constructor() {
    this.formatters.set('json', new JsonFormatter());
    this.formatters.set('yaml', new YamlFormatter());
  }

  register<T>(type: string, formatter: Formatter<T>): void {
    this.formatters.set(type, formatter as Formatter<unknown>);
  }

  format<T>(data: T, context: OutputContext): string {
    const formatter = this.formatters.get(context.format);

    if (!formatter) {
      // Default to JSON for unknown formats
      return new JsonFormatter().format(data, context);
    }

    return formatter.format(data, context);
  }
}

// Print output function
function printOutput(data: unknown, ctx: CommandContext): void {
  const formatter = new OutputFormatter();

  // Register resource-specific formatters
  formatter.register('agent', new AgentTableFormatter());

  // Determine type key for custom formatter
  const typeKey = Array.isArray(data) ? data[0]?.constructor?.name : (data as Record<string, unknown>)?.id?.slice(0, 2);

  const context: OutputContext = {
    format: ctx.options.output as OutputFormat || 'table',
    color: ctx.options.color !== false,
  };

  const output = formatter.format(data, context);
  console.log(output);
}

// Pagination helper
function printPaginated<T>(result: ListResponse<T>, ctx: CommandContext): void {
  printOutput(result.data, ctx);

  if (result.pagination.hasMore) {
    console.log(chalk.gray(`\nMore results available. Use --cursor ${result.pagination.cursor} to view next page.`));
  }
}
```

## Integration Points

- **Resource Formatters**: Register custom formatters per resource type for optimized display
- **Pagination Display**: Show cursor hint when results are paginated
- **Error Formatting**: Errors always formatted consistently regardless of output mode

## Production Considerations

- **Output Truncation**: Wide tables auto-wrap or truncate based on terminal width
- **Streaming Output**: For large lists, stream JSON output as NDJSON (newline-delimited JSON)
- **Color Detection**: Auto-detect TTY color support; honor NO_COLOR environment variable
- **Internationalization**: Date and number formatting respects locale settings

## Open-Source Tools

- **table**: Terminal table formatting with Unicode borders
- **chalk**: Terminal string coloring
- **yaml**: YAML serialization
