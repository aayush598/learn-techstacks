# Section 04: Workato Integration

## Overview

The Workato integration enables enterprise users to connect the voice agent platform with Workato's enterprise automation platform, which is designed for complex, high-volume integrations with governance, role-based access control, and enterprise security compliance. Workato recipes (their term for automations) can combine voice agent triggers and actions with SaaS applications, on-premise systems, and custom APIs, all through Workato's low-code recipe designer.

Workato's platform is tailored for enterprise use cases requiring audit trails, connection management, error handling with human-in-the-loop approval gates, and on-premise agent connectivity. The integration exposes the voice agent platform's capabilities through Workato's SDK, which generates a connector package that can be published to Workato's marketplace. The connector supports Workato's features: custom actions, triggers, lookup tables, recipe lifecycle management, and recipe-level error handling.

## Architecture

```
                 Workato Integration

   Workato Platform ←→ Workato Connector ←→ Voice Agent API
                            |
   +----------------------------------------------------------+
   |              Workato Connector Components                |
   |                                                          |
   |  +------------------+  +-------------------+            |
   |  | Connection       |  | Custom Actions    |            |
   |  | • OAuth2         |  | • Create call     |            |
   |  | • API Key        |  | • Send message    |            |
   |  | • Connection     |  | • Update contact  |            |
   |  |   validation     |  | • Get analytics   |            |
   |  +------------------+  +-------------------+            |
   |  +------------------+  +-------------------+            |
   |  | Triggers         |  | Lookup Tables     |             |
   |  | • Polling        |  | • Agent list      |            |
   |  | • Webhook        |  | • Campaign list   |            |
   |  | • Scheduled      |  | • Template list   |            |
   |  +------------------+  +-------------------+            |
   |  +------------------+  +-------------------+            |
   |  | Object Defs      |  | Recipe Actions    |             |
   |  | • Call object    |  | • Picklist        |            |
   |  | • Contact object |  | • Input schema    |            |
   |  | • Message object |  | • Output schema   |            |
   |  +------------------+  +-------------------+            |
   +----------------------------------------------------------+
```

## Design Decisions

- **Workato SDK-based connector over custom API integration:** Workato's SDK (Ruby-based) generates a connector gem that implements Workato's connector interface: connection definition, test, actions, triggers, and object definitions. The SDK handles authentication, pagination, rate limiting, and error mapping. Using the SDK ensures the connector follows Workato's best practices and can be deployed to Workato's marketplace. Trade-off: SDK requires Ruby development expertise and testing within Workato's connector test harness but provides first-class support for all Workato features.

- **Polling triggers with configurable interval over webhooks for enterprise compliance:** Workato supports both polling and webhook triggers. For enterprise compliance requirements (audit trails, guaranteed delivery, firewall restrictions), polling triggers with configurable intervals (5, 15, 30, 60 minutes) are preferred. The connector implements polling that tracks a cursor (last processed event ID or timestamp) and only fetches new events since the last poll. Workato's built-in deduplication prevents duplicate recipe executions. Trade-off: polling introduces latency (up to the configured polling interval) but works reliably through enterprise firewalls and provides audit trails.

- **Batch operations for enterprise scalability over single-record processing:** Enterprise recipes often process thousands of records. The connector implements batch actions (Create Multiple Contacts, Send Bulk Messages) alongside single-record actions. Batch actions accept arrays of records and process them through the platform's bulk API endpoints. Workato's recipe engine supports iterators to split batches back into individual records if needed. Trade-off: batch operations require implementing bulk API endpoints but reduce API calls by orders of magnitude for large datasets.

## Implementation Approach

```
# Workato connector definition (Ruby SDK)
{
  title: 'Voice Agent Platform',
  description: 'Enterprise automation connector for Voice Agent Platform',
  key: 'voice_agent',

  connection: {
    fields: [
      {
        name: 'subdomain',
        label: 'Account Subdomain',
        optional: false,
        hint: 'Your voice agent account subdomain (e.g., "mycompany" from mycompany.voiceagent.com)',
      },
      {
        name: 'api_key',
        label: 'API Key',
        type: 'password',
        optional: false,
        hint: 'Generate an API key from Settings > API Keys',
      },
    ],

    authorization: {
      type: 'custom_auth',
      apply: lambda do |connection|
        headers('X-API-Key': connection['api_key'], 'Content-Type': 'application/json')
        base_uri("https://#{connection['subdomain']}.api.voiceagent.com/v1")
      end,
    },

    test: lambda do |connection|
      get('/health')
    end,
  },

  object_definitions: {
    call: {
      fields: lambda do |_connection, _config_fields|
        [
          { name: 'id', type: :string, label: 'Call ID', control_type: 'text' },
          { name: 'call_sid', type: :string, label: 'Call SID', control_type: 'text' },
          { name: 'duration', type: :integer, label: 'Duration (seconds)' },
          { name: 'status', type: :string, label: 'Status', control_type: 'select', pick_list: 'call_statuses' },
          { name: 'customer_phone', type: :string, label: 'Customer Phone', control_type: 'phone' },
          { name: 'agent_id', type: :string, label: 'Agent ID' },
          { name: 'completed_at', type: :date_time, label: 'Completed At' },
          { name: 'recording_url', type: :string, label: 'Recording URL', control_type: 'url' },
          { name: 'transcription', type: :string, label: 'Transcription', control_type: 'text' },
        ]
      end,
    },
  },

  actions: {
    send_sms: {
      title: 'Send SMS',
      subtitle: 'Send an SMS message',
      help: 'Sends an SMS message to a phone number through the voice agent platform.',
      input_fields: lambda do |_object_definitions|
        [
          { name: 'to', type: :string, label: 'To', control_type: 'phone', optional: false },
          { name: 'message', type: :string, label: 'Message', control_type: 'text', optional: false },
          { name: 'from_number', type: :string, label: 'From Number', control_type: 'phone', optional: true,
            hint: 'Leave empty to use default account number' },
        ]
      end,
      output_fields: lambda do |_object_definitions|
        [
          { name: 'id', type: :string, label: 'Message ID' },
          { name: 'status', type: :string, label: 'Status' },
          { name: 'to', type: :string, label: 'To' },
          { name: 'sent_at', type: :date_time, label: 'Sent At' },
        ]
      end,
      execute: lambda do |_connection, input, _input_schema, _output_schema|
        response = post('/messages', {
          to: input['to'],
          text: input['message'],
          from: input['from_number'],
          channel: 'sms',
        })
        response
      end,
    },

    get_call_analytics: {
      title: 'Get Call Analytics',
      subtitle: 'Retrieve call analytics for a date range',
      input_fields: lambda do |_object_definitions|
        [
          { name: 'start_date', type: :date, label: 'Start Date', optional: false },
          { name: 'end_date', type: :date, label: 'End Date', optional: false },
          { name: 'granularity', type: :string, label: 'Granularity',
            control_type: 'select', pick_list: 'analytics_granularity', optional: true },
        ]
      end,
      output_fields: lambda do |_object_definitions|
        [
          { name: 'total_calls', type: :integer, label: 'Total Calls' },
          { name: 'answered_calls', type: :integer, label: 'Answered Calls' },
          { name: 'avg_duration', type: :number, label: 'Avg Duration (s)' },
          { name: 'total_duration', type: :integer, label: 'Total Duration (s)' },
        ]
      end,
      execute: lambda do |_connection, input, _input_schema, _output_schema|
        get('/analytics/calls', {
          start_date: input['start_date'],
          end_date: input['end_date'],
          granularity: input['granularity'] || 'day',
        })
      end,
    },
  },

  triggers: {
    new_calls_poll: {
      title: 'New Calls (Polling)',
      subtitle: 'Triggers on new completed calls',
      poll: lambda do |_connection, _input, closure|
        page_size = 100
        offset = closure['offset'] || 0

        response = get('/calls', {
          status: 'completed',
          per_page: page_size,
          offset: offset,
          sort: 'completed_at_desc',
        })

        next_closure = if response.length == page_size
          { offset: offset + page_size, 'has_more': true }
        else
          { offset: 0, 'has_more': false }
        end

        [response, next_closure, nil]
      end,
      dedup: lambda do |call|
        call['id']
      end,
      output_fields: lambda do |_object_definitions|
        [
          { name: 'id', type: :string, label: 'Call ID' },
          { name: 'call_sid', type: :string, label: 'Call SID' },
          { name: 'duration', type: :integer, label: 'Duration(s)' },
          { name: 'customer_phone', type: :string, label: 'Customer Phone' },
          { name: 'completed_at', type: :date_time, label: 'Completed At' },
        ]
      end,
    },
  },

  pick_lists: {
    call_statuses: lambda do |_connection|
      [
        ['Completed', 'completed'],
        ['Failed', 'failed'],
        ['Busy', 'busy'],
        ['No Answer', 'no_answer'],
        ['Canceled', 'canceled'],
      ]
    end,
    analytics_granularity: lambda do |_connection|
      [
        ['Hour', 'hour'],
        ['Day', 'day'],
        ['Week', 'week'],
        ['Month', 'month'],
      ]
    end,
  },
}
```

## Open-Source Tools

| Tool | License | Purpose |
|------|---------|---------|
| Workato SDK (MIT) | Ruby | Connector development |
| RSpec (MIT) | Ruby | Connector testing framework |

## Production Considerations

**Scaling:** Workato enterprise customers may run recipes that process thousands of events per hour. Ensure the platform's API can handle batch operations efficiently. Workato has a configurable rate limit per connection — coordinate with the customer to set appropriate limits. Workato recipes can be paused and resumed — the connector should handle graceful resume (resume from last processed cursor) without data duplication.

**Security:** Workato enterprise features include Connection Approval (admins approve connections before use) and Recipe Governance (approval gates before recipe deployment). The connector should support field-level encryption tags for sensitive data (phone numbers). Workato stores credentials encrypted and the platform should minimize the permission scope of API keys used with Workato.

**Monitoring:** Workato provides recipe execution logs and error notifications natively. The platform should track Workato-originated API calls separately for usage analytics. Monitor API response times for Workato requests — Workato has a 60-second timeout for action execution and 300 seconds for batch operations. Alert on unusual error patterns from Workato connections (indicates connector issues or API changes).
