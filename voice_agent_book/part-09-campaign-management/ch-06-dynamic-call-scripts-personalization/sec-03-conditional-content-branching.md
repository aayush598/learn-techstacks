# Section 03: Conditional Content & Branching

## Overview

Conditional content and branching enable scripts to adapt dynamically to each contact's situation, the call's progression, and real-time inputs from the AI agent. Instead of a linear script, the template engine evaluates conditions — based on contact data, campaign context, or agent-detected intents — and selects the appropriate script path. This creates a conversational flow that feels natural and responsive rather than robotic and predetermined.

Branching supports multiple patterns: if/else blocks based on contact attributes (existing vs. new customer), intent-based routing (interested vs. not interested), state machine progression (greeting → qualification → offer → closing), and dynamic content injection (different offers based on customer segment). The system also supports recursive branching where a branch contains further conditions, creating a complete decision tree.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│              Conditional Content & Branching                 │
├─────────────────────────────────────────────────────────────┤
│  Script Decision Tree:                                      │
│                                                             │
│  ┌────────────────────────────────────────┐                │
│  │  Opening                               │                │
│  └────────────┬───────────────────────────┘                │
│               │                                            │
│               ▼                                            │
│  ┌──────────────────────────────┐                          │
│  │ Is Existing Customer?       │                          │
│  └──────┬──────────────┬───────┘                          │
│         │ Yes          │ No                               │
│         ▼              ▼                                   │
│  ┌────────────┐  ┌──────────────────┐                     │
│  │ "Welcome   │  │ "We have a       │                     │
│  │  back!"    │  │  special offer"  │                     │
│  └──────┬─────┘  └────────┬─────────┘                     │
│         │                 │                                │
│         ▼                 ▼                                │
│  ┌──────────────────────────────┐                          │
│  │ How are you today?           │                          │
│  └────────────┬─────────────────┘                          │
│               │                                            │
│               ▼                                            │
│  ┌──────────────────────────────┐                          │
│  │ Agent detects intent        │                          │
│  └──────┬──────────┬───────────┘                          │
│         │          │                                      │
│  ┌──────▼───┐  ┌───▼───────┐                              │
│  │ Interested│  │ Not       │                              │
│  │          │  │ Interested│                              │
│  └──────┬───┘  └───┬───────┘                              │
│         │          │                                      │
│  ┌──────▼───┐  ┌───▼───────┐                              │
│  │ Present  │  │ Thank &   │                              │
│  │ Offer    │  │ Close     │                              │
│  └──────────┘  └───────────┘                              │
└─────────────────────────────────────────────────────────────┘
```

## Design Decisions

- **Pre-computed vs. runtime branching:** Pre-computed branches (based on contact data known before the call) are evaluated at template render time. Runtime branches (based on agent-detected intents) are evaluated during the call. Trade-off: pre-computed is faster, runtime is more adaptive.

- **Intent-based routing as first-class primitive:** The template engine provides an `{{#intent}}` helper that lets the AI agent route based on detected intent during the conversation. This is more natural than if/else based on survey-style questions. Trade-off: intent detection dependency vs. conversational flow.

- **State machine integration:** Complex scripts can define states (greeting, qualification, offer, closing) with transitions triggered by agent-detected events. The template engine tracks the current state. Trade-off: state machine complexity vs. structured script flow.

- **Fallback paths for uncertainty:** Every branch must have a default/fallback path for when conditions cannot be evaluated or intents are unclear. This prevents the script from reaching a dead end. Trade-off: fallback path overhead vs. script completeness.

## Implementation Approach

```
class BranchingEngine {
  constructor(templateEngine, intentDetector) {
    this.template = templateEngine;
    this.intentDetector = intentDetector;
  }

  async evaluateBranch(node, context) {
    switch (node.type) {
      case 'if':
        return this.evaluateConditional(node, context);
      case 'intent':
        return this.evaluateIntentRouting(node, context);
      case 'state_machine':
        return this.evaluateStateMachine(node, context);
      case 'slot':
        return this.evaluateSlot(node, context);
      default:
        return this.template.render(node.children, context);
    }
  }

  async evaluateConditional(node, context) {
    const condition = await this.evaluateCondition(node.expression, context);
    
    if (condition) {
      return this.template.render(node.trueBranch, context);
    } else if (node.falseBranch) {
      return this.template.render(node.falseBranch, context);
    }
    return '';
  }

  async evaluateIntentRouting(node, context) {
    // Listen for the agent's detected intent
    const intent = await this.intentDetector.waitForIntent(
      context.callSid,
      node.intents,
      node.timeout || 15000
    );

    if (intent && node.routes[intent]) {
      return this.template.render(node.routes[intent].children, {
        ...context,
        detectedIntent: intent,
        intentConfidence: intent.confidence
      });
    }

    // Fallback path
    return node.routes['_fallback'] 
      ? this.template.render(node.routes._fallback.children, context)
      : '';
  }

  async evaluateStateMachine(node, context) {
    const stateMachine = node.states;
    let currentState = context.currentState || node.initialState;

    const output = [];
    let maxTransitions = 10; // Prevent infinite loops

    while (currentState && maxTransitions > 0) {
      const state = stateMachine[currentState];
      
      // Render state content
      const rendered = this.template.render(state.content, {
        ...context,
        currentState
      });
      output.push(rendered);

      // Check for transitions
      const transition = await this.evaluateTransitions(
        state.transitions, 
        context
      );

      if (transition) {
        currentState = transition.target;
        // Store in context for next evaluation
        context.currentState = currentState;
      } else {
        currentState = null; // End state machine
      }

      maxTransitions--;
    }

    return output.join('\n');
  }

  async evaluateTransitions(transitions, context) {
    if (!transitions || transitions.length === 0) return null;

    for (const transition of transitions) {
      switch (transition.type) {
        case 'auto':
          return transition; // Automatic transition
        case 'intent':
          const intent = await this.intentDetector.checkIntent(
            context.callSid,
            transition.intent,
            1000 // Quick check, don't wait
          );
          if (intent) return transition;
          break;
        case 'condition':
          const matched = await this.evaluateCondition(
            transition.expression, 
            context
          );
          if (matched) return transition;
          break;
      }
    }

    return null;
  }

  async evaluateCondition(expression, context) {
    switch (expression.type) {
      case 'variable':
        return !!this.resolveVariableAtBranch(expression.path, context);
      case 'comparison':
        const { left, operator, right } = expression;
        const leftVal = this.resolveVariableAtBranch(left, context);
        const rightVal = right.startsWith('{{') 
          ? this.resolveVariableAtBranch(right.slice(2, -2), context)
          : right;
        return this.compareValues(leftVal, operator, rightVal);
      case 'and':
        return (await this.evaluateCondition(expression.left, context)) &&
               (await this.evaluateCondition(expression.right, context));
      case 'or':
        return (await this.evaluateCondition(expression.left, context)) ||
               (await this.evaluateCondition(expression.right, context));
      case 'not':
        return !(await this.evaluateCondition(expression.expression, context));
      case 'function':
        return this.evaluateFunction(expression.name, expression.args, context);
    }
  }

  // Slot filling — ask a question and use the answer as a variable
  async evaluateSlot(node, context) {
    const slotName = node.slotName;
    const question = this.template.render(node.question, context);
    
    // The agent will ask the question and capture the response
    const answer = await this.intentDetector.captureSlot(
      context.callSid,
      slotName,
      question,
      node.validation,
      node.retryCount || 2
    );

    // Make the answer available to subsequent template rendering
    context.slots = { ...context.slots, [slotName]: answer };

    if (answer.filled) {
      return this.template.render(node.successBranch, context);
    } else {
      return this.template.render(node.fallbackBranch, context);
    }
  }
}
```

## Integration Points

- **Template Engine (sec-01):** Branching directives are parsed as part of the template AST
- **Intent Detector (Part 06):** Receives real-time intents from AI agent for routing
- **Slot Filler (Part 06):** Captures structured data from natural conversation
- **AI Agent Runtime (Part 06):** Executes the script including branching decisions
- **Campaign Analytics (Ch 09):** Tracks branch selection rates and path effectiveness
- **A/B Testing (Ch 10):** Compares different branching strategies

## Open-Source Tools

- **json-rules-engine:** Lightweight rules engine for complex conditional logic
- **XState / Robot:** State machine libraries that can model script flows
- **NLP.js / Rasa:** Intent detection for runtime branching
- **Lodash.get:** Safe nested property access for condition evaluation
- **Zod:** Validation schema for slot values

## Production Considerations

- Runtime branching adds latency while waiting for intent detection — set reasonable timeouts (5-15 seconds)
- State machine loops must be bounded — max transition count prevents infinite loops from poorly defined state machines
- Slot validation should include retry logic with clear failure messaging — "I'm sorry, I didn't catch that"
- Branch evaluation should be logged for debugging and optimization — which branches are taken most/least often?
- Pre-compute as many branches as possible before the call to reduce runtime latency
- Intent detection accuracy directly impacts branching quality — monitor intent confusion rates
- Fallback paths prevent dead ends but should be monitored — high fallback usage indicates script or intent issues
- A/B test different branching structures — a 3-deep tree may convert better than a 2-deep one
- Provide a visual branching tree editor for non-technical campaign managers
- Test all branch paths during QA — hidden conditional logic is a common source of script errors
