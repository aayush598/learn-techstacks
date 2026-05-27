# Section 01: Zapier Integration

## Overview

The Zapier integration enables voice agent platform events and actions to be exposed through Zapier's automation platform, allowing users to create Zaps that connect voice agent triggers and actions with thousands of other applications without writing code. The integration publishes platform capabilities as Zapier Triggers (e.g., "New Call Completed", "New Payment Received") and Actions (e.g., "Create Contact", "Send SMS", "Update Customer Record"), which users can combine in multi-step workflows.

The integration is built using Zapier's Integration Platform (CLI + JavaScript SDK), which provides a structured framework for defining authentication, triggers, actions, search endpoints, and testing. The Zapier adapter runs as a separate service that translates between Zapier's platform protocol and the voice agent's internal APIs. It handles OAuth2 authentication flow, webhook subscription management for triggers, and action execution through the platform's unified API.

## Architecture

```
                  Zapier Integration

   Zapier Platform ←→ Zapier Adapter ←→ Voice Agent API
                        |
   +----------------------------------------------------------+
   |              Zapier Adapter Components                   |
   |                                                          |
   |  +------------------+  +-------------------+            |
   |  | Authentication   |  | Trigger Defs      |            |
   |  | • OAuth2 flow    |  | • Call completed  |            |
   |  | • API Key auth   |  | • Payment received|            |
   |  | • Session refresh|  | • Customer created|            |
   |  +------------------+  +-------------------+            |
   |  +------------------+  +-------------------+            |
   |  | Action Defs      |  | Search/Find Defs  |             |
   |  | • Send SMS       |  | • Find customer   |            |
   |  | • Create contact |  | • Lookup order    |            |
   |  | • Update CRM     |  | • Check inventory |            |
   |  +------------------+  +-------------------+            |
   |  +------------------+  +-------------------+            |
   |  | Webhook Sub Mgmt |  | Input/Output      |            |
   |  | • Subscribe      |  | Schema            |             |
   |  | • Unsubscribe    |  | • Dynamic fields  |            |
   |  | • Renewal        |  | • Custom types    |            |
   |  +------------------+  +-------------------+            |
   +----------------------------------------------------------+
```

## Design Decisions

- **REST-hooks pattern for triggers over polling:** Zapier's REST-hooks (webhook-based triggers) provide real-time event delivery to Zaps. When a trigger fires, the platform sends an HTTP POST to Zapier's hook URL with the event payload. This is more responsive than polling (which has 5-15 minute latency) and reduces API calls. The adapter manages webhook subscriptions — creating them when a user enables a Zap, refreshing them before expiry (30-day Zapier hook TTL), and cleaning up on deactivation. Trade-off: REST-hooks require the platform to maintain a webhook receiver and manage subscription lifecycle but provide sub-second trigger latency.

- **Dynamic field schemas for action inputs over static forms:** Zapier actions use dynamic field schemas that adapt to the user's account configuration. For example, the "Create Contact" action dynamically fetches custom field definitions from the platform so users can map Zapier input fields to platform custom fields. This provides a better UX than static forms that hard-code a fixed set of fields. Trade-off: dynamic fields require fetching schema data during Zap editor interaction, adding latency to the editor experience but ensuring the right fields are available.

- **Zapier CLI platform over visual builder for version-controlled deployment:** The integration is developed using the Zapier CLI, which generates a bundled JavaScript application deployed to Zapier's platform. This approach enables version control, automated testing, CI/CD integration, and collaboration through code reviews. The visual builder is used for prototyping and documentation but the production integration is CLI-managed. Trade-off: CLI-based development requires Node.js expertise and local development setup but provides professional deployment and testing capabilities.

## Implementation Approach

```
// Zapier integration definition (app definition)
const App = {
  version: require('./package.json').version,
  platformVersion: require('zapier-platform-core').version,

  authentication: {
    type: 'oauth2',
    oauth2Config: {
      authorizeUrl: {
        url: 'https://api.voiceagent.com/oauth/authorize',
        params: {
          client_id: '{{process.env.CLIENT_ID}}',
          state: '{{bundle.inputData.state}}',
          redirect_uri: '{{bundle.inputData.redirect_uri}}',
          response_type: 'code',
        },
      },
      getAccessToken: {
        url: 'https://api.voiceagent.com/oauth/token',
        method: 'POST',
        params: {
          code: '{{bundle.inputData.code}}',
          client_id: '{{process.env.CLIENT_ID}}',
          client_secret: '{{process.env.CLIENT_SECRET}}',
          grant_type: 'authorization_code',
          redirect_uri: '{{bundle.inputData.redirect_uri}}',
        },
      },
      refreshAccessToken: {
        url: 'https://api.voiceagent.com/oauth/token',
        method: 'POST',
        params: {
          refresh_token: '{{bundle.authData.refresh_token}}',
          client_id: '{{process.env.CLIENT_ID}}',
          client_secret: '{{process.env.CLIENT_SECRET}}',
          grant_type: 'refresh_token',
        },
      },
      autoRefresh: true,
    },
  },

  triggers: {
    new_call_completed: {
      key: 'new_call_completed',
      noun: 'Call',
      display: {
        label: 'New Call Completed',
        description: 'Triggers when a voice call completes.',
      },
      operation: {
        inputFields: [
          { key: 'status', type: 'string', helpText: 'Filter by call status', required: false, choices: ['completed', 'failed', 'busy', 'no-answer', 'canceled'] },
          { key: 'min_duration', type: 'integer', helpText: 'Minimum call duration in seconds', required: false },
        ],
        performSubscribe: async (z, bundle) => {
          const response = await z.request({
            url: 'https://api.voiceagent.com/v1/webhooks',
            method: 'POST',
            body: {
              url: bundle.targetUrl,
              eventTypes: ['call.completed'],
              filters: bundle.inputData,
              version: '1.0.0',
            },
          });
          return { id: response.data.id, url: bundle.targetUrl };
        },
        performUnsubscribe: async (z, bundle) => {
          await z.request({
            url: `https://api.voiceagent.com/v1/webhooks/${bundle.subscribeData.id}`,
            method: 'DELETE',
          });
        },
        perform: async (z, bundle) => {
          // Zapier sends the webhook payload directly as the result
          return [bundle.cleanedRequest];
        },
        sample: {
          id: 'evt_123',
          callSid: 'CA123456',
          duration: 120,
          status: 'completed',
          customerPhone: '+14155551234',
          agentId: 'ag_001',
          completedAt: '2026-05-27T12:00:00Z',
        },
        outputFields: [
          { key: 'id', label: 'Event ID', type: 'string' },
          { key: 'callSid', label: 'Call SID', type: 'string' },
          { key: 'duration', label: 'Duration (seconds)', type: 'integer' },
          { key: 'status', label: 'Call Status', type: 'string' },
          { key: 'customerPhone', label: 'Customer Phone', type: 'string' },
        ],
      },
    },
  },

  creates: {
    send_sms: {
      key: 'send_sms',
      noun: 'SMS',
      display: {
        label: 'Send SMS',
        description: 'Sends an SMS message to a phone number.',
      },
      operation: {
        inputFields: [
          { key: 'to', label: 'To Phone Number', type: 'string', required: true, helpText: 'E.164 format (+14155551234)' },
          { key: 'message', label: 'Message', type: 'text', required: true, helpText: 'SMS message content' },
        ],
        perform: async (z, bundle) => {
          const response = await z.request({
            url: 'https://api.voiceagent.com/v1/messages',
            method: 'POST',
            body: {
              to: bundle.inputData.to,
              text: bundle.inputData.message,
              type: 'sms',
            },
          });
          return response.data;
        },
        sample: {
          id: 'msg_001',
          to: '+14155551234',
          status: 'sent',
          createdAt: '2026-05-27T12:00:00Z',
        },
      },
    },
  },

  searches: {
    find_customer: {
      key: 'find_customer',
      noun: 'Customer',
      display: {
        label: 'Find Customer',
        description: 'Finds a customer by phone number or email.',
      },
      operation: {
        inputFields: [
          { key: 'phone', type: 'string', required: false, helpText: 'Search by phone number' },
          { key: 'email', type: 'string', required: false, helpText: 'Search by email address' },
        ],
        perform: async (z, bundle) => {
          const params = new URLSearchParams();
          if (bundle.inputData.phone) params.set('phone', bundle.inputData.phone);
          if (bundle.inputData.email) params.set('email', bundle.inputData.email);
          const response = await z.request({
            url: `https://api.voiceagent.com/v1/customers?${params.toString()}`,
            method: 'GET',
          });
          return response.data;
        },
      },
    },
  },
};

module.exports = {
  app: App,
};
```

## Open-Source Tools

| Tool | License | Purpose |
|------|---------|---------|
| Zapier CLI (MIT) | Node.js | Integration development |
| Zapier Platform Core (MIT) | Node.js | Runtime SDK |
| Zapier Testing (MIT) | Node.js | Automated integration tests |

## Production Considerations

**Scaling:** Zapier triggers via REST-hooks pass through the platform's existing webhook infrastructure. Ensure the webhook delivery engine can handle Zapier's traffic — Zapier may re-subscribe hooks and cause burst events during hook renewal. Zapier action execution must be fast (Zapier has a 30-second timeout for action execution). Cache authentication tokens and frequently accessed data. Monitor the number of active Zapier subscriptions and their webhook delivery health.

**Security:** The Zapier OAuth2 flow redirects users to the platform's authorization page where they grant specific permissions (scopes). Define minimal OAuth scopes for Zapier operations. The Zapier integration's client secret must be stored securely and rotated regularly. Never expose full API responses containing sensitive data — filter outputs to include only fields exposed in the Zapier action/trigger output definitions.

**Monitoring:** Track the number of active Zapier connections, webhook subscription events per second, action execution count and latency, authentication success/failure rates, and error types. Alert on high Zapier action failure rates, authentication failures (possible OAuth token expiry issue), and unusual subscription patterns. Monitor Zapier platform API deprecation notices and plan updates accordingly.
