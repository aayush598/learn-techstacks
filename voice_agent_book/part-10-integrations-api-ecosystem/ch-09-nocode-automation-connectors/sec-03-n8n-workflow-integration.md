# Section 03: n8n Workflow Integration

## Overview

The n8n workflow integration enables self-hosted and cloud-based n8n instances to connect with the voice agent platform through n8n's extensible node system. n8n is an open-source, fair-code workflow automation tool that gives users full control over their data — workflows run on the user's own infrastructure, data never leaves their control, and they can customize every aspect of the integration.

The integration is packaged as an n8n community node (npm package) that adds a "Voice Agent" node to n8n's node library. The node supports multiple operations categorized as triggers (webhook-based event reception via n8n's webhook listener), operations (CRUD actions on platform resources), and resource lookups. The integration leverages n8n's built-in features: credential management for secure API key storage, binary data handling for audio file processing, and n8n's execution context for workflow state management.

## Architecture

```
               n8n Workflow Integration

   n8n Instance ←→ n8n Node ←→ Voice Agent API
                        |
   +----------------------------------------------------------+
   |              n8n Node Architecture                       |
   |                                                          |
   |  +------------------+  +-------------------+            |
   |  | Credential       |  | Node Class        |            |
   |  | • API Key        |  | • Properties      |            |
   |  | • OAuth2         |  | • Execute method  |            |
   |  | • Credential test|  | • Resource list   |            |
   |  +------------------+  +-------------------+            |
   |  +------------------+  +-------------------+            |
   |  | Operations       |  | Resources         |             |
   |  | • Call           |  | • Calls           |            |
   |  | • Message        |  | • Messages        |            |
   |  | • Contact        |  | • Contacts        |            |
   |  | • Analytics      |  | • Analytics       |            |
   |  | • Webhook        |  | • Recordings      |            |
   |  +------------------+  +-------------------+            |
   +----------------------------------------------------------+
```

## Design Decisions

- **n8n node as npm package over built-in node contribution:** The integration is distributed as a community node via npm, not contributed to n8n's core node library. This allows independent versioning, agile releases, and avoids the n8n core contribution process (which requires review and alignment with n8n's release cycle). Users install the package with `npm install @voiceagent/n8n-nodes-voiceagent` and register it in their n8n instance. Trade-off: community nodes require manual installation by users but enable faster iteration independent of n8n's release cadence.

- **Resource-based node design over operation-per-node:** Instead of creating separate nodes for each operation (Send SMS node, Get Call node), the integration uses a single "Voice Agent" node with a resource selector and operation selector. Users first select a resource (Call, Message, Contact, Analytics, Recording) and then an operation (Get, List, Create, Delete). This reduces node library clutter and follows n8n's recommended pattern for API integrations. Trade-off: a single node with multiple resources/operations has a more complex UI than separate nodes but provides a more organized and scalable integration pattern.

- **Webhook trigger via n8n's built-in webhook listener over platform push:** n8n's trigger mode leverages its built-in "Webhook" node or the node's own trigger capability. When configured as a trigger, the node registers a webhook endpoint on the n8n instance (or via n8n's external webhook URL) and the platform pushes events to that URL. The node handles webhook signature verification, JSON parsing, and output formatting. n8n's webhook system handles retry and deduplication. Trade-off: using n8n's webhook infrastructure means the node delegates retry/dedup to n8n (less control) but simplifies the node implementation and aligns with n8n's architecture.

## Implementation Approach

```
// n8n community node definition (TypeScript)
import { IExecuteFunctions, ITriggerFunctions, INodeType, INodeTypeDescription, NodeOperation, NodeConnectionType } from 'n8n-workflow';

export class VoiceAgent implements INodeType {
  description: INodeTypeDescription = {
    displayName: 'Voice Agent',
    name: 'voiceAgent',
    icon: 'file:voiceagent.svg',
    group: ['transform'],
    version: 1,
    subtitle: '={{$parameter["resource"] + ": " + $parameter["operation"]}}',
    description: 'Interact with Voice Agent Platform API',
    defaults: { name: 'Voice Agent' },
    inputs: [NodeConnectionType.Main],
    outputs: [NodeConnectionType.Main],
    credentials: [{ name: 'voiceAgentApi', required: true }],
    requestDefaults: {
      baseURL: 'https://api.voiceagent.com/v1',
      headers: { 'Content-Type': 'application/json' },
    },

    properties: [
      {
        displayName: 'Resource',
        name: 'resource',
        type: 'options',
        noDataExpression: true,
        options: [
          { name: 'Call', value: 'call' },
          { name: 'Message', value: 'message' },
          { name: 'Contact', value: 'contact' },
          { name: 'Analytics', value: 'analytics' },
          { name: 'Recording', value: 'recording' },
          { name: 'Webhook', value: 'webhook' },
        ],
        default: 'call',
      },

      // Call operations
      {
        displayName: 'Operation',
        name: 'operation',
        type: 'options',
        noDataExpression: true,
        displayOptions: { show: { resource: ['call'] } },
        options: [
          { name: 'Get Call', value: 'get', description: 'Get call details by SID', action: 'Get a call' },
          { name: 'List Calls', value: 'list', description: 'List calls with filters', action: 'List calls' },
          { name: 'Delete Call', value: 'delete', description: 'Delete call recording', action: 'Delete a call' },
        ],
        default: 'get',
      },

      // Message operations
      {
        displayName: 'Operation',
        name: 'operation',
        type: 'options',
        noDataExpression: true,
        displayOptions: { show: { resource: ['message'] } },
        options: [
          { name: 'Send SMS', value: 'sendSms', description: 'Send an SMS message', action: 'Send an SMS' },
          { name: 'Send WhatsApp', value: 'sendWhatsApp', description: 'Send a WhatsApp message', action: 'Send a WhatsApp message' },
          { name: 'Get Message Status', value: 'getStatus', description: 'Check message delivery status', action: 'Get a message status' },
        ],
        default: 'sendSms',
      },

      // Call ID parameter
      {
        displayName: 'Call SID',
        name: 'callSid',
        type: 'string',
        required: true,
        displayOptions: { show: { resource: ['call'], operation: ['get', 'delete'] } },
        default: '',
      },

      // SMS parameters
      {
        displayName: 'To',
        name: 'to',
        type: 'string',
        required: true,
        displayOptions: { show: { resource: ['message'], operation: ['sendSms', 'sendWhatsApp'] } },
        default: '',
        placeholder: '+14155551234',
      },
      {
        displayName: 'Message',
        name: 'text',
        type: 'string',
        typeOptions: { rows: 4 },
        required: true,
        displayOptions: { show: { resource: ['message'], operation: ['sendSms', 'sendWhatsApp'] } },
        default: '',
      },
    ],
  };

  async execute(this: IExecuteFunctions): Promise<INodeExecutionData[][]> {
    const items = this.getInputData();
    const resource = this.getNodeParameter('resource', 0) as string;
    const operation = this.getNodeParameter('operation', 0) as string;
    const credentials = await this.getCredentials('voiceAgentApi');

    const results = [];

    for (let i = 0; i < items.length; i++) {
      try {
        let response;

        if (resource === 'call' && operation === 'get') {
          const callSid = this.getNodeParameter('callSid', i) as string;
          response = await this.helpers.request({
            method: 'GET',
            url: `/calls/${callSid}`,
            headers: { 'Authorization': `Bearer ${credentials.apiKey}` },
          });
        } else if (resource === 'message' && operation === 'sendSms') {
          const to = this.getNodeParameter('to', i) as string;
          const text = this.getNodeParameter('text', i) as string;
          response = await this.helpers.request({
            method: 'POST',
            url: '/messages',
            headers: { 'Authorization': `Bearer ${credentials.apiKey}` },
            body: { to, text, channel: 'sms' },
          });
        }

        results.push({ json: response });
      } catch (error) {
        if (this.continueOnFail()) {
          results.push({ json: { error: error.message } });
        } else {
          throw error;
        }
      }
    }

    return [results];
  }
}

// Credential definition
export class VoiceAgentApi implements ICredentialType {
  name = 'voiceAgentApi';
  displayName = 'Voice Agent API';
  properties: ICredentialNodeProperties[] = [
    {
      displayName: 'API Key',
      name: 'apiKey',
      type: 'string',
      typeOptions: { password: true },
      default: '',
    },
    {
      displayName: 'Environment',
      name: 'environment',
      type: 'options',
      options: [
        { name: 'Production', value: 'https://api.voiceagent.com/v1' },
        { name: 'Sandbox', value: 'https://sandbox.api.voiceagent.com/v1' },
      ],
      default: 'https://api.voiceagent.com/v1',
    },
  ];

  async test(credential: ICredentialData): Promise<ICredentialTestResult> {
    try {
      const { apiKey, environment } = credential;
      await axios.get(`${environment}/health`, {
        headers: { Authorization: `Bearer ${apiKey}` },
      });
      return { status: 'OK', message: 'Connection successful' };
    } catch (error) {
      return { status: 'Error', message: error.message };
    }
  }
}
```

## Open-Source Tools

| Tool | License | Purpose |
|------|---------|---------|
| n8n Workflow (Sustainable Use License) | Server | Workflow automation |
| n8n Node Dev Toolkit (MIT) | Node.js | Node development + testing |
| n8n CLI (MIT) | Node.js | Build and packaging |

## Production Considerations

**Scaling:** n8n is self-hosted by users — the platform has no control over n8n infrastructure. Ensure API responses are fast (n8n has a configurable timeout, default 120 seconds). For high-volume event triggers, users should configure n8n's concurrency settings to avoid backlogs. The webhook endpoint must be publicly accessible for n8n's trigger mode — document required firewall settings and TLS configuration for users.

**Security:** n8n instances can be self-hosted — users have full access to their data. The platform should minimize data exposure by implementing field-level API responses (users only get fields they have permissions for). API keys should be scoped and revocable. Document security best practices for n8n deployment (HTTPS enforcement, rate limiting, access control). n8n's credential encryption should be used (users encrypt their API key with n8n's encryption key).

**Monitoring:** Since n8n is self-hosted, the platform has no visibility into workflow execution. Provide API usage metrics and rate limit headers so users can monitor their consumption. Track overall API usage from n8n connections and alert on unusual patterns. Maintain a changelog for the n8n node and use semantic versioning to communicate breaking changes. Monitor npm download statistics for the community node to track adoption.
