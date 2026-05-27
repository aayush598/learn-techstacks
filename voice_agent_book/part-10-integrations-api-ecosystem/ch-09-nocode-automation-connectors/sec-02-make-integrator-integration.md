# Section 02: Make (Integromat) Integration

## Overview

The Make (formerly Integromat) integration exposes the voice agent platform's capabilities through Make's visual automation platform, allowing users to build complex multi-step scenarios that connect voice events with hundreds of apps. Make's unique strength is its visual scenario builder with sophisticated data transformation capabilities (aggregators, iterators, routers, data stores) that enable complex automation logic beyond simple trigger-action patterns.

The integration package includes Make modules for triggers (webhook-based event reception), actions (platform API operations such as sending messages, managing contacts, and retrieving analytics), and searches (looking up platform data from within scenarios). Modules are deployed to Make's app marketplace and are maintained through Make's developer SDK. The integration supports Make's advanced features like webhook re-signing, data structure negotiation, and real-time scenario monitoring.

## Architecture

```
                  Make (Integromat) Integration

   Make Platform ←→ Make Adapter ←→ Voice Agent API
                        |
   +----------------------------------------------------------+
   |              Make Adapter Components                     |
   |                                                          |
   |  +------------------+  +-------------------+            |
   |  | Module Registry  |  | Triggers          |            |
   |  | • Triggers       |  | • Watch calls     |            |
   |  | • Actions        |  | • Watch payments  |            |
   |  | • Searches       |  | • Watch customers |            |
   |  +------------------+  +-------------------+            |
   |  +------------------+  +-------------------+            |
   |  | Actions          |  | Data Structures    |            |
   |  | • Send message   |  | • Input schemas   |            |
   |  | • Create contact |  | • Output schemas  |            |
   |  | • Get analytics  |  | • Mappable fields |            |
   |  +------------------+  +-------------------+            |
   |  +------------------+  +-------------------+            |
   |  | Webhook Mgmt     |  | Auth              |             |
   |  | • Instant trigger|  | • API Key         |            |
   |  | • Data delivery  |  | • OAuth2          |            |
   |  | • Re-signing     |  | • Scope mgmt      |            |
   |  +------------------+  +-------------------+            |
   +----------------------------------------------------------+
```

## Design Decisions

- **Instant triggers via webhooks over polling triggers:** Make supports "instant" triggers that receive real-time data via webhooks, similar to Zapier's REST-hooks. When a user adds a "Watch Calls" module to a scenario, Make registers a webhook URL with the platform. The platform pushes events to this URL as they occur. Make's scenario engine receives the webhook payload and starts the scenario execution. Trade-off: instant triggers have lower latency and better UX than polling (which adds 5-15 minute delays) but require webhook subscription management.

- **Data structure negotiation for dynamic input schemas:** Make's module interface allows dynamic input field negotiation — when a user selects an action, the platform returns the available input fields and their types dynamically. For example, selecting "Create Contact" returns fields like name, email, phone, and custom fields specific to the user's account. This is implemented through Make's `input` property that calls a platform API to fetch field definitions. Trade-off: dynamic negotiation adds an API call during module configuration but ensures users see the exact fields available in their account.

- **Aggregator support for batch operations:** Make's unique aggregator modules allow batching multiple events into a single platform API call. For example, collecting incoming call events over 1 minute and sending a single batch SMS digest. The integration provides aggregator-compatible endpoints that accept arrays of payloads. This enables efficient bulk operations that would otherwise require multiple API calls. Trade-off: aggregator support requires implementing batch API endpoints but enables powerful patterns like daily summaries and bulk updates.

## Implementation Approach

```
// Make app definition (JSON/YAML config for Make's developer platform)
{
  "name": "Voice Agent Platform",
  "version": "1.0.0",
  "description": "Connect your voice agent platform with Make scenarios",
  "platform": ["voiceagent.com"],

  "authentication": {
    "type": "apiKey",
    "apiKey": {
      "header": "X-API-Key",
      "in": "header"
    }
  },

  "modules": [
    {
      "name": "Watch Calls",
      "type": "trigger",
      "interface": "instant",
      "webhook": {
        "url": "https://api.voiceagent.com/v1/webhooks",
        "method": "POST",
        "headers": {
          "Content-Type": "application/json"
        },
        "body": {
          "eventTypes": ["call.completed"],
          "url": "{{webhookUrl}}"
        },
        "response": {
          "mappable": {
            "id": "{{id}}",
            "callSid": "{{callSid}}",
            "duration": "{{duration}}",
            "status": "{{status}}",
            "customerPhone": "{{customerPhone}}",
            "agentId": "{{agentId}}"
          }
        }
      }
    },
    {
      "name": "Send Message",
      "type": "action",
      "interface": "regular",
      "input": {
        "url": "https://api.voiceagent.com/v1/messages/send",
        "method": "POST",
        "body": {
          "to": "{{parameters.to}}",
          "text": "{{parameters.text}}",
          "channel": "{{parameters.channel}}"
        }
      },
      "parameters": {
        "to": {
          "type": "text",
          "label": "Recipient Phone Number",
          "required": true,
          "help": "E.164 format, e.g., +14155551234"
        },
        "text": {
          "type": "text",
          "label": "Message Content",
          "required": true
        },
        "channel": {
          "type": "select",
          "label": "Channel",
          "options": [
            {"label": "SMS", "value": "sms"},
            {"label": "WhatsApp", "value": "whatsapp"},
            {"label": "Voice", "value": "voice"}
          ],
          "default": "sms"
        }
      }
    },
    {
      "name": "Get Analytics",
      "type": "action",
      "interface": "regular",
      "input": {
        "url": "https://api.voiceagent.com/v1/analytics/calls",
        "method": "GET",
        "params": {
          "startDate": "{{parameters.startDate}}",
          "endDate": "{{parameters.endDate}}",
          "granularity": "{{parameters.granularity}}"
        }
      },
      "parameters": {
        "startDate": {
          "type": "date",
          "label": "Start Date",
          "required": true
        },
        "endDate": {
          "type": "date",
          "label": "End Date",
          "required": true
        },
        "granularity": {
          "type": "select",
          "label": "Granularity",
          "options": [
            {"label": "Hour", "value": "hour"},
            {"label": "Day", "value": "day"},
            {"label": "Week", "value": "week"},
            {"label": "Month", "value": "month"}
          ],
          "default": "day"
        }
      }
    },
    {
      "name": "Search Customers",
      "type": "search",
      "interface": "regular",
      "input": {
        "url": "https://api.voiceagent.com/v1/customers/search",
        "method": "POST",
        "body": {
          "query": "{{parameters.query}}",
          "field": "{{parameters.field}}"
        }
      },
      "parameters": {
        "query": {
          "type": "text",
          "label": "Search Query",
          "required": true
        },
        "field": {
          "type": "select",
          "label": "Search Field",
          "options": [
            {"label": "Phone Number", "value": "phone"},
            {"label": "Email", "value": "email"},
            {"label": "Name", "value": "name"},
            {"label": "Customer ID", "value": "id"}
          ],
          "default": "phone"
        }
      }
    }
  ],

  "baseUrl": "https://api.voiceagent.com/v1",
  "webhookResponse": {
    "status": 200,
    "body": "OK"
  }
}
```

## Open-Source Tools

| Tool | License | Purpose |
|------|---------|---------|
| Make SDK (MIT) | Node.js | Module development |
| Make CLI (MIT) | Node.js | Local testing + deployment |

## Production Considerations

**Scaling:** Make scenarios can trigger at high frequency during event bursts. The webhook endpoint for Make must be reliable and fast — response within 2 seconds (Make's webhook timeout). If processing takes longer, acknowledge the webhook immediately and process asynchronously. Make has a 40-second execution timeout for action modules — ensure API operations complete within this window. For longer operations, use Make's "continue" pattern (return a URL for the scenario to poll for completion).

**Security:** API key-based authentication is the most common for Make integrations. Keys should be scoped per user/token with configurable permissions. Make stores the API key and sends it with every request — ensure keys can be revoked without affecting other platform functionality. Implement rate limiting on the Make adapter to prevent runaway scenarios from consuming excessive API quota.

**Monitoring:** Track Make module execution counts, average execution time per module, error rates by module type, and webhook registration churn. Monitor for Make-specific error patterns: "Data structure mismatch" (input schema changed), "Module timeout" (API too slow), "Rate limit exceeded" (too many scenario runs). Alert on sustained error rates > 5% and monitor the Make platform changelog for breaking API changes.
