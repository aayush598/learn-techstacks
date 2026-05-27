# Section 02: Simulated Call Flow Design

## Overview

Call flow design defines the conversation graph that simulations follow. Each flow represents a complete interaction scenario, from greeting to resolution. Flow designs are created by conversation designers and product managers, then translated into machine-readable definitions for the simulation engine.

A call flow consists of states (conversation waypoints), transitions (intent-driven movement between states), expected responses (what the agent should say), and success criteria (how we know the flow completed correctly). Flows range from simple linear paths to complex multi-branch scenarios with conditionals.

## Design Decisions

- **React Flow over Custom**: Battle-tested node/edge rendering. Saves 6+ months custom development.
- **Local-First State**: Zustand + debounced saves (2s). Instant UI response without waiting for API.
- **Function-as-Edge**: Edges carry conditions and transforms. Flow evaluates conditions at each step.
## Implementation Approach

```yaml
# Example: Technical Support Flow
name: technical-support-flow
version: 1.2
description: Handles technical support inquiries

variables:
  customer_name: string
  issue_type: enum(login, billing, performance)

states:
  greeting:
    entry: "Hello, thank you for calling support. How can I help you?"
    transitions:
      report_issue: identify_issue
      billing_question: billing_flow
      goodbye: end_call

  identify_issue:
    entry: "I'm sorry to hear you're having trouble. Can you describe the issue?"
    on_entry_action: set_context(phase: troubleshooting)
    transitions:
      login_issue: verify_account
      performance_issue: run_diagnostics
      unclear: clarify_issue

  verify_account:
    entry: "Let me look up your account. Could you provide your email?"
    on_entry_action: request_account_info
    transitions:
      provide_email: check_account
      no_account: offer_creation

  check_account:
    action: verify_account_exists(variables.email)
    transitions:
      account_found: resolve_login_issue
      account_not_found: offer_creation

  resolve_login_issue:
    entry: "I found your account. Let me help you with the login."
    action: initiate_password_reset(variables.email)
    transitions:
      resolved: closing
      need_clarification: clarify_issue

  closing:
    entry: "Is there anything else I can help you with?"
    transitions:
      no: end_call
      yes: identify_issue

  end_call:
    entry: "Thank you for calling. Have a great day!"
    type: terminal

success_criteria:
  - path_ends_in: [end_call]
  - required_intents: [report_issue, provide_email]
  - max_turns: 10
  - required_entities: [customer_email]
```

## Integration Points

- **Simulation Engine**: Flow definitions consumed by the simulation engine
- **Conversation Designer**: Visual editor generates flow YAML
- **Testing**: Flows validated against test criteria
- **Analytics**: Flow completion rates tracked
- **Versioning**: Flow versions tracked alongside agent versions

## Open-Source Tools

- **React Flow** (MIT): Node-based UI
- **Zustand** (MIT): State management
- **Immer** (MIT): Immutable updates
## Production Considerations

- **Flow Complexity**: Overly complex flows are hard to test; keep states manageable
- **Flow Maintenance**: Flows need updating as product evolves; flag outdated flows
- **Test Coverage**: Ensure every state and transition is tested
- **Error Recovery**: Test that agents gracefully handle unexpected inputs
- **Performance Review**: Flow execution time affects user experience; optimize bottlenecks
