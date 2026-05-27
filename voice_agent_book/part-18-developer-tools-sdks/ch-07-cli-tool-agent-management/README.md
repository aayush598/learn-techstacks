# Chapter 07: CLI Tool for Agent Management

> **Part:** 18 - Developer Tools, SDKs & API Layer

---

## Sections

| # | Section | Description |
|---|---------|-------------|
| 01 | [CLI Architecture](sec-01-cli-architecture.md) | Commander.js / oclif, command tree, middleware pipeline, plugin system |
| 02 | [Command Structure Design](sec-02-command-structure-design.md) | Nested commands, argument parsing, flags and options, subcommand organization |
| 03 | [Auth & Configuration Storage](sec-03-auth-configuration-storage.md) | API key storage, config file (.voiceagentrc), profile management, secure keyring integration |
| 04 | [Interactive Mode & Prompts](sec-04-interactive-mode-prompts.md) | Interactive prompts (Inquirer), auto-complete, confirmation dialogs, progress indicators |
| 05 | [Output Formatting](sec-05-output-formatting.md) | Table output, JSON output, YAML output, custom formatters, colorized output |
| 06 | [CI/CD Integration](sec-06-ci-cd-integration.md) | Non-interactive mode, exit codes, JSON output for CI, GitHub Actions integration |
| 07 | [CLI Testing & Distribution](sec-07-cli-testing-distribution.md) | Snapshot testing, mock API server, executable packaging, npm/PyPI distribution |
| 08 | [Auto-Complete & Help](sec-08-auto-complete-help.md) | Shell auto-completion, man pages, --help output, help topics, usage examples |

---

## CLI Command Tree

```
$ voiceagent --help

Commands:
  agents          Manage AI voice agents
    list          List all agents
    create        Create a new agent
    get           Get agent details
    update        Update agent configuration
    delete        Delete an agent
    deploy        Deploy agent to production
    test          Test agent in sandbox

  calls           Manage calls
    list          List call history
    get           Get call details
    monitor       Real-time call monitoring

  campaigns       Manage outbound campaigns
    list          List campaigns
    create        Create campaign
    start         Start campaign
    pause         Pause campaign

  config          Manage CLI configuration
    set           Set configuration value
    get           Get configuration value
    profile       Manage profiles

  --help, -h      Show help
  --version, -v   Show version
```

---

## Learning Objectives

- Design CLI architecture with Commander.js/oclif
- Implement nested command structure with argument parsing
- Build auth and configuration storage with profiles
- Create interactive mode with prompts and auto-complete
- Implement multiple output formats (table, JSON, YAML)
- Support CI/CD integration with non-interactive mode
- Test CLI with snapshot testing and mock servers
- Implement shell auto-completion and help system
