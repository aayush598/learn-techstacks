# Section 08: Unified Helpdesk Adapter

## Overview

The unified helpdesk adapter provides a consistent interface across multiple helpdesk platforms (Zendesk, Freshdesk, Intercom, ServiceNow) behind a single abstraction. This enables the voice platform to work with any helpdesk system through the same API, simplifying the integration code and enabling multi-helpdesk workflows where a single call might interact with tickets in multiple helpdesk instances.

The unified adapter defines a common set of operations that all helpdesk adapters must implement: ticket CRUD (create, read, update), comment/conversation management, contact lookup/creation, status management, and webhook registration. Each helpdesk-specific adapter implements these operations using its platform's API semantics. The unified adapter also handles cross-cutting concerns like authentication, rate limiting, error mapping (standardizing error codes across platforms), and capability discovery (which operations does this specific helpdesk instance support?).

## Architecture

```
                    Unified Helpdesk Adapter

   +----------------------------------------------------------+
   |           Unified Helpdesk Interface                      |
   |                                                          |
   |  createTicket() | addComment() | getTicket()            |
   |  updateStatus() | findContact()| registerWebhook()      |
   +----------------------------------------------------------+
              |              |              |
              v              v              v
   +------------------+  +------------------+  +------------------+
   | Zendesk Adapter  |  | Freshdesk        |  | Intercom         |
   |                  |  | Adapter          |  | Adapter          |
   +------------------+  +------------------+  +------------------+
   +------------------+  +------------------+
   | ServiceNow       |  | [Future Helpdesk]|
   | Adapter          |  | Adapter          |
   +------------------+  +------------------+
              |              |              |
              v              v              v
   +----------------------------------------------------------+
   |           Cross-Cutting Services                         |
   |                                                          |
   |  Authentication | Rate Limiting | Error Mapping          |
   |  Caching        | Retry Logic   | Observability          |
   +----------------------------------------------------------+
```

## Design Decisions

- **Interface-driven adapter design with capability flags:** Each adapter implements a common interface but can declare capabilities (supportsSLA, supportsCustomFields, supportsAttachments, supportsThreading). The platform queries capabilities at runtime to determine which features are available for a given integration. This gracefully handles platforms with different feature sets. Trade-off: capability flags must be maintained as platforms add or remove features.

- **Standardized domain model with platform-specific mapping:** The unified adapter defines a canonical ticket model (ID, subject, description, status, priority, requester, createdAt, updatedAt, tags, customFields). Each platform adapter maps between this canonical model and its system-specific model. The mapping is defined as a configuration (field mapping table) rather than code, enabling customization per helpdesk instance. Trade-off: the canonical model may not capture all platform-specific fields without resorting to custom fields maps.

- **Plugin-based adapter loading with runtime registration:** Adapters are loaded dynamically at startup through a plugin registry. New helpdesk adapters can be added by creating a new adapter class and registering it — no core code changes needed. Adapters can be enabled/disabled per tenant without restart. Trade-off: dynamic loading requires careful version management to prevent compatibility issues.

## Implementation Approach

```
// Unified helpdesk interface
interface HelpdeskAdapter {
  readonly platform: string;
  readonly capabilities: HelpdeskCapabilities;

  initialize(config: HelpdeskConfig): Promise<void>;
  healthCheck(): Promise<HealthStatus>;

  // Ticket operations
  createTicket(ticket: TicketInput): Promise<AdapterResponse<TicketResult>>;
  getTicket(ticketId: string): Promise<AdapterResponse<TicketResult>>;
  updateTicket(ticketId: string, update: Partial<TicketInput>): Promise<AdapterResponse<void>>;

  // Comment operations
  addComment(ticketId: string, comment: CommentInput): Promise<AdapterResponse<void>>;
  getComments(ticketId: string): Promise<AdapterResponse<CommentResult[]>>;

  // Contact operations
  findContact(query: string): Promise<AdapterResponse<ContactResult | null>>;
  createOrUpdateContact(contact: ContactInput): Promise<AdapterResponse<ContactResult>>;

  // Webhook operations
  registerWebhook(config: WebhookConfig): Promise<AdapterResponse<{ id: string }>>;
  unregisterWebhook(webhookId: string): Promise<AdapterResponse<void>>;
  verifyWebhook(payload: any, signature: string): boolean;
}

// Canonical domain types
interface TicketInput {
  subject: string;
  description: string;
  requesterEmail: string;
  requesterName?: string;
  priority: 'low' | 'medium' | 'high' | 'urgent';
  type?: string;
  tags?: string[];
  customFields?: Record<string, any>;
  attachments?: { url: string; filename: string }[];
}

interface TicketResult {
  id: string;
  displayId: string;
  subject: string;
  status: string;
  priority: string;
  requesterEmail: string;
  createdAt: number;
  updatedAt: number;
  tags: string[];
  customFields: Record<string, any>;
}

interface HelpdeskCapabilities {
  ticketTypes: boolean;       // Supports ticket type categorization
  customFields: boolean;      // Supports custom fields on tickets
  attachments: boolean;       // Supports file attachments
  slaManagement: boolean;     // Supports SLA policies
  threading: boolean;         // Supports ticket threading
  satisfactionRatings: boolean; // Supports CSAT surveys
}

class UnifiedHelpdeskFactory {
  private adapters = new Map<string, HelpdeskAdapter>();

  register(type: string, adapter: HelpdeskAdapter) {
    this.adapters.set(type, adapter);
  }

  getAdapter(integrationConfig: HelpdeskConfig): HelpdeskAdapter {
    const adapter = this.adapters.get(integrationConfig.type);
    if (!adapter) throw new Error(`Unsupported helpdesk type: ${integrationConfig.type}`);
    return adapter;
  }

  async createAndInitialize(integrationConfig: HelpdeskConfig): Promise<HelpdeskAdapter> {
    const adapter = this.getAdapter(integrationConfig);
    await adapter.initialize(integrationConfig);
    return adapter;
  }
}

// Implementation pattern for each helpdesk
class GenericHelpdeskAdapter extends BaseAdapter implements HelpdeskAdapter {
  platform: string;
  capabilities: HelpdeskCapabilities;

  async createTicket(ticket: TicketInput): Promise<AdapterResponse<TicketResult>> {
    // Platform-specific implementation
    throw new Error('Not implemented');
  }

  async getTicket(ticketId: string): Promise<AdapterResponse<TicketResult>> {
    throw new Error('Not implemented');
  }
}
```

## Open-Source Tools

| Tool | License | Purpose |
|------|---------|---------|
| **TypeScript** (Apache 2.0) | Language | Interface definitions |
| **Zod** (MIT) | Validation | Canonical model validation |
| **Axios** (MIT) | HTTP client | API communication |

## Production Considerations

**Scaling:** The unified adapter adds one additional abstraction layer per API call. Profile adapter overhead to ensure it's under 5ms per call. Cache adapter instances by integration configuration (same config → same adapter instance). For multi-instance deployments, adapter state (connections, tokens) must be shareable across instances.

**Security:** Adapter implementations must not leak platform-specific details through the unified interface. Error messages should be sanitized to remove internal implementation details. Capability declarations should not reveal platform-specific configuration details.

**Monitoring:** Track adapter distribution (% of tenants using each helpdesk type), per-operation latency across adapters, capability utilization (which features are used), and adapter-specific error rates. Alert on adapter unavailability (health check failures) and capability mismatch (requested operation not supported by adapter).
