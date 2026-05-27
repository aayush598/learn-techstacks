# Section 02: Adapter Pattern Implementation

## Overview

The adapter pattern implementation provides the concrete mechanics for how each external system adapter is structured, how it handles API-specific concerns (authentication, request formation, response parsing, error mapping), and how it integrates with the broader integration framework. Each adapter encapsulates all knowledge about a specific external API behind a clean interface, allowing the rest of the platform to interact with external systems through a uniform abstraction.

The adapter implementation follows a layered structure: a base layer (handles HTTP communication, authentication token management, request/response logging), a transformation layer (maps between platform domain objects and API-specific formats), and a business logic layer (implements integration-specific workflows like contact sync or ticket creation). The base layer is shared across all adapters. The transformation and business logic layers are adapter-specific. Each adapter also implements a health check method and a capability discovery method that lets the framework know what operations the adapter supports.

## Architecture

```
                  Adapter Pattern Structure

   Core Platform ←→ Adapter Interface ←→ Specific Adapter ←→ External API
                        |
   +------------------------------------------------------------+
   |                Adapter Implementation Layers               |
   |                                                            |
   |  +------------------------------------------------------+  |
   |  |  Capability Layer                                     |  |
   |  |  - Describes what operations this adapter supports    |  |
   |  |  - Enables runtime capability discovery                |  |
   |  +------------------------------------------------------+  |
   |  +------------------------------------------------------+  |
   |  |  Business Logic Layer (Adapter-specific)              |  |
   |  |  - Workflow implementations (sync, lookup, create)    |  |
   |  |  - Multi-step API orchestration                       |  |
   |  |  - Data enrichment and validation                     |  |
   |  +------------------------------------------------------+  |
   |  +------------------------------------------------------+  |
   |  |  Transformation Layer (Adapter-specific)              |  |
   |  |  - Domain-to-API mapping functions                    |  |
   |  |  - API-to-domain mapping functions                     |  |
   |  |  - Field-level transformations                        |  |
   |  +------------------------------------------------------+  |
   |  +------------------------------------------------------+  |
   |  |  Base Layer (Shared)                                  |  |
   |  |  - HTTP client with connection pooling                |  |
   |  |  - Authentication token management                    |  |
   |  |  - Retry and timeout handling                         |  |
   |  |  - Request/response logging                           |  |
   |  +------------------------------------------------------+  |
   +------------------------------------------------------------+
```

## Design Decisions

- **Capability-based adapter discovery over static configuration:** Adapters declare their capabilities (supported operations, data types, authentication methods) through a capability interface. The framework introspects adapters at registration to discover available functionality without hard-coded capability lists. A CRM adapter declares "contact_sync", "activity_log", "lead_create" while an e-commerce adapter declares "order_lookup", "inventory_check", "return_create". Trade-off: capability discovery requires runtime reflection or convention-based naming but eliminates configuration drift.

- **Schema-defined transformations with auto-generated mapping code:** Transformations between domain objects and API-specific formats are defined as JSON Schema mappings. The framework auto-generates transformation functions from these schemas, reducing manual mapping code by 80%. Mappings include field renames, type coercions, default values, and computed fields. Trade-off: schema-driven mapping adds complexity for edge cases (nested objects, conditional mappings) but dramatically reduces boilerplate.

- **Versioned adapters with backward compatibility guarantees:** Adapter implementations are versioned. When an external API changes, a new adapter version is created while the old version continues to serve existing configurations. The framework routes requests to the appropriate adapter version based on the tenant's integration configuration. Trade-off: maintaining multiple adapter versions increases maintenance burden but prevents breaking changes from forcing tenant migrations.

## Implementation Approach

```
interface AdapterCapability {
  operations: ('read' | 'write' | 'search' | 'webhook' | 'sync')[];
  entities: string[];         // Supported domain entities
  authMethods: ('oauth2' | 'api_key' | 'basic' | 'mtls')[];
  rateLimits: { maxRequests: number; windowMs: number };
  dataFormat: 'rest' | 'graphql' | 'soap' | 'grpc';
}

interface ContactData {
  externalId?: string;
  firstName: string;
  lastName: string;
  email?: string;
  phone?: string;
  customFields: Record<string, any>;
}

abstract class CRMMAdapter extends BaseAdapter {
  abstract createContact(contact: ContactData): Promise<AdapterResponse<{ id: string }>>;
  abstract updateContact(id: string, contact: Partial<ContactData>): Promise<AdapterResponse<void>>;
  abstract searchContacts(query: string): Promise<AdapterResponse<ContactData[]>>;
  abstract logActivity(contactId: string, activity: ActivityData): Promise<AdapterResponse<void>>;
}

class SalesforceAdapter extends CRMMAdapter {
  private soapClient: SOAPClient;
  private restClient: AxiosInstance;

  async createContact(contact: ContactData): Promise<AdapterResponse<{ id: string }>> {
    const sfContact = this.transformToSalesforceContact(contact);
    const response = await this.restClient.post('/services/data/v58.0/sobjects/Contact', sfContact);
    return { success: true, data: { id: response.data.id } };
  }

  async searchContacts(query: string): Promise<AdapterResponse<ContactData[]>> {
    const soql = `SELECT Id, FirstName, LastName, Email, Phone FROM Contact WHERE Name LIKE '%${query}%'`;
    const response = await this.restClient.get('/services/data/v58.0/query', { params: { q: soql } });
    return {
      success: true,
      data: response.data.records.map(r => this.transformFromSalesforceContact(r))
    };
  }

  private transformToSalesforceContact(contact: ContactData) {
    return {
      FirstName: contact.firstName,
      LastName: contact.lastName,
      Email: contact.email,
      Phone: contact.phone,
      ...contact.customFields
    };
  }
}
```

## Open-Source Tools

| Tool | License | Purpose |
|------|---------|---------|
| **Axios** (MIT) | HTTP client | REST API communication |
| **SOAP** (MIT) | Node.js | SOAP API communication |
| **Zod** (MIT) | Validation | Response schema validation |
| **jsonata** (MIT) | Transformation | JSON transformation/ mapping |

## Production Considerations

**Scaling:** Adapter instances are pooled per integration configuration. Pool size is configurable (default 5-10 connections per adapter). Connection reuse is critical for performance — the HTTP client should maintain persistent connections with keep-alive. Adapter response caching at the framework level reduces load on external APIs and improves response times for repeated queries (same contact looked up multiple times).

**Security:** API keys and OAuth tokens are encrypted at rest and decrypted only in memory for the duration of the request. Adapters should never log sensitive data (tokens, PII). Support credential rotation through the adapter lifecycle — expired tokens trigger automatic re-authentication. Rate limits must be enforced at the per-tenant, per-adapter level to prevent one tenant from consuming another's quota.

**Monitoring:** Track adapter-specific metrics per operation: request count, success rate, latency percentiles, error distribution (timeout, auth failure, rate limit, server error). Monitor credential expiry and alert when tokens are approaching expiration. Track adapter version distribution across tenants to plan deprecations.
