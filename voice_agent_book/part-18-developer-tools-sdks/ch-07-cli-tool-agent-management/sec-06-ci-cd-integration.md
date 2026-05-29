# Section 06: CI/CD Integration

## Overview

The CLI supports non-interactive mode for CI/CD pipelines. Exit codes signal success/failure, JSON output enables programmatic parsing, and environment variables configure authentication. The CLI can be installed in GitHub Actions, GitLab CI, Jenkins, and other CI systems.

## Architecture

```
CI/CD Integration Patterns
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

GitHub Actions Workflow:
  name: Deploy Voice Agent
  on:
    push:
      branches: [main]

  jobs:
    deploy:
      runs-on: ubuntu-latest
      steps:
        - uses: actions/checkout@v4
        - uses: actions/setup-node@v4
        - run: npm install -g @voiceagent/cli
        - run: |
            voiceagent agents deploy ag_123 \
              --api-key ${{ secrets.VOICE_AGENT_API_KEY }} \
              --environment production \
              --output json
        - run: |
            voiceagent campaigns start cmp_456 \
              --api-key ${{ secrets.VOICE_AGENT_API_KEY }} \
              --output json

Exit Codes:
  0: Success
  1: General error (invalid args, API error)
  2: Authentication error
  3: Configuration error
  4: Rate limited (retry suggested)

Non-Interactive Detection:
  if (!process.stdout.isTTY) {
    // Disable all interactive prompts
    // Default all confirmations to --force behavior
    // Output JSON by default
  }

Environment Variables:
  VOICE_AGENT_API_KEY      → API Key
  VOICE_AGENT_ENV          → Environment
  VOICE_AGENT_OUTPUT       → Output format
  CI                       → Auto-detect CI environment
```

## Design Decisions

- **Exit Code Convention**: Standard Unix exit codes with specific meanings for common failures
- **Auto-Detect CI**: When `CI=true` or stdout is not a TTY, disable interactive mode
- **JSON Default in CI**: When stdout is not a TTY, default output format is JSON
- **Secrets via Environment**: API keys passed via environment variables, not command-line arguments

## Implementation Approach

```typescript
// CI detection
function isCI(): boolean {
  return process.env.CI === 'true'
    || process.env.GITHUB_ACTIONS === 'true'
    || process.env.GITLAB_CI === 'true'
    || process.env.JENKINS_URL !== undefined
    || !process.stdout.isTTY;
}

// CI-adaptive configuration
function getCIOptions(): Record<string, unknown> {
  if (!isCI()) {
    return {};
  }

  return {
    output: 'json',
    force: true,
    'no-color': !process.stdout.isTTY,
  };
}

// Exit code handler
const ExitCodes = {
  SUCCESS: 0,
  ERROR: 1,
  AUTH_ERROR: 2,
  CONFIG_ERROR: 3,
  RATE_LIMITED: 4,
} as const;

// Command wrapper with exit code handling
async function runCommand(fn: () => Promise<void>): Promise<void> {
  try {
    await fn();
    process.exit(ExitCodes.SUCCESS);
  } catch (error) {
    if (error instanceof AuthenticationError) {
      console.error('Authentication failed. Check your API key.');
      process.exit(ExitCodes.AUTH_ERROR);
    }

    if (error instanceof RateLimitError) {
      console.error('Rate limited. Retry after', error.retryAfter, 'seconds.');
      process.exit(ExitCodes.RATE_LIMITED);
    }

    console.error(`Error: ${(error as Error).message}`);
    process.exit(ExitCodes.ERROR);
  }
}

// GitHub Actions integration
class GitHubActionsIntegration {
  setOutput(name: string, value: string): void {
    if (process.env.GITHUB_OUTPUT) {
      // Modern GitHub Actions
      fs.appendFileSync(
        process.env.GITHUB_OUTPUT,
        `${name}=${value}\n`,
      );
    } else {
      // Legacy GitHub Actions
      console.log(`::set-output name=${name}::${value}`);
    }
  }

  setFailed(message: string): void {
    console.log(`::error::${message}`);
    process.exit(ExitCodes.ERROR);
  }

  startGroup(name: string): void {
    console.log(`::group::${name}`);
  }

  endGroup(): void {
    console.log('::endgroup::');
  }
}

// CI-optimized commands
async function handleDeployForCI(ctx: CommandContext, agentId: string): Promise<void> {
  const client = createClient(ctx);

  if (isCI()) {
    const github = new GitHubActionsIntegration();
    github.startGroup('Deploying Agent');

    const spinner = ora('Deploying...').start();
    const result = await client.agents.deploy(agentId);
    spinner.succeed('Deployed');

    github.setOutput('deployment_id', result.deploymentId);
    github.setOutput('status', result.status);

    // Print machine-readable output
    console.log(JSON.stringify(result));
    github.endGroup();
  } else {
    // Interactive deploy with confirmation
    const confirmed = await confirm({
      message: `Deploy agent ${agentId} to production?`,
      default: false,
    });

    if (confirmed) {
      const spinner = ora('Deploying...').start();
      const result = await client.agents.deploy(agentId);
      spinner.succeed('Deployed');
      printOutput(result, ctx);
    }
  }
}
```

## Integration Points

- **GitHub Actions**: Native CI integration with output variables and annotations
- **GitLab CI**: Compatible with GitLab CI/CD environment variables
- **Docker**: CLI available as Docker image for containerized pipelines
- **npm/PyPI**: Install CLI via npm (`@voiceagent/cli`) or pip (`voiceagent-cli`)

## Production Considerations

- **Idempotent CI Runs**: All CLI commands are idempotent for safe retries in CI
- **Secret Masking**: CI platform masks API keys in logs automatically
- **Caching**: CLI caches responses for repeated calls in same pipeline
- **Parallel Safety**: Concurrent CLI calls use different API keys per job

## Open-Source Tools

- **CI Environment Detection**: Built-in detection for GitHub Actions, GitLab CI, Jenkins
- **@actions/core**: GitHub Actions toolkit for output and annotations
