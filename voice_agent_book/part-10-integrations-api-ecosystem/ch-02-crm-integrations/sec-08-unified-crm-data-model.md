# Section 08: Unified CRM Data Model

## Overview

The unified CRM data model provides a system-agnostic abstraction over the diverse data models of different CRM platforms. The model defines canonical types for entities that all CRM integrations share — Contact (Person), Account (Organization), Lead, Opportunity (Deal), Activity (Call, Task, Meeting), and Note. Each canonical type has a minimal set of required fields and an extensible set of optional fields. CRM adapters map between the canonical model and the CRM-specific model, enabling the platform to work with any CRM through a consistent interface.

The unified model addresses several challenges: different CRMs use different terminology (Deal vs. Opportunity vs. Potential), different field structures (HubSpot uses flat properties while Salesforce uses compound types), different required fields (Pipedrive requires a deal title, Salesforce doesn't), and different association models (Salesforce uses lookup relationships, HubSpot uses association labels). The model also handles cross-entity relationships — a Contact belongs to an Account, a Deal is associated with a Contact and Account, Activities are linked to one or more entities.

## Architecture

```
                    Unified CRM Data Model

   +----------------------------------------------------------+
   |                 Canonical Domain Model                    |
   |                                                          |
   |  +-------------+  +-------------+  +-------------+       |
   |  | Contact     |  | Account     |  | Lead        |       |
   |  | • id        |  | • id        |  | • id        |       |
   |  | • firstName |  | • name      |  | • firstName |       |
   |  | • lastName  |  | • industry  |  | • lastName  |       |
   |  | • email     |  | • phone     |  | • email     |       |
   |  | • phone     |  | • website   |  | • company   |       |
   |  | • customFlds|  | • customFlds|  | • source    |       |
   |  +-------------+  +-------------+  +-------------+       |
   |        |                |                |                |
   |        +--------+-------+--------+------+                |
   |                 |                |                        |
   |        +--------v-------+  +-----v--------+               |
   |        | Deal           |  | Activity     |               |
   |        | • id           |  | • id         |               |
   |        | • title        |  | • type       |               |
   |        | • stage        |  | • subject    |               |
   |        | • value        |  | • startTime  |               |
   |        | • contactIds[] |  | • endTime    |               |
   |        | • accountId    |  | • contactId  |               |
   |        | • customFields |  | • dealId     |               |
   |        +----------------+  | • callData   |               |
   |                             +--------------+               |
   +----------------------------------------------------------+
              |              |              |
              v              v              v
   +----------------------------------------------------------+
   |              CRM Adapter Mapping Layer                    |
   |                                                          |
   |  +----------------+  +----------------+                  |
   |  | Salesforce     |  | HubSpot        |  | Zoho | Pipedrive |
   |  | Mapping        |  | Mapping        |  | ...  |  ...  |
   |  +----------------+  +----------------+                 |
   +----------------------------------------------------------+
```

## Design Decisions

- **Minimal canonical model with extensible custom fields:** The canonical model defines only the fields that are common across all CRM platforms (name, email, phone for contacts; name, industry for accounts; title, value, stage for deals). CRM-specific fields (Salesforce record types, HubSpot lead status) are stored in a custom fields map with string keys. This keeps the model simple while supporting any CRM field. Trade-off: custom fields lack type safety and require runtime validation against CRM schemas.

- **Entity relationships as arrays of IDs with type qualifiers:** Relationships between entities are expressed as arrays of `{type, id}` pairs rather than specific foreign key fields. A Deal has `relatedEntities: [{type: 'contact', id: '123'}, {type: 'account', id: '456'}]`. This flexible approach handles diverse CRM relationship models without model changes. Trade-off: relationship queries require joining through a mapping table, adding query complexity.

- **Versioned schema evolution with backward compatibility:** The canonical model is versioned (v1, v2). New fields are added in new versions without removing old fields. Adapters declare which model version they support. The platform can evolve the model without breaking existing integrations. Trade-off: versioning adds complexity to adapter development and testing.

## Implementation Approach

```
// Canonical domain types

interface CanonicalContact {
  externalId?: string;
  integrationId?: string;
  firstName: string;
  lastName: string;
  email?: string;
  phone?: string;
  mobile?: string;
  title?: string;
  accountId?: string;
  customFields: Record<string, any>;
  metadata: {
    createdAt?: number;
    updatedAt?: number;
    source?: string;
  };
}

interface CanonicalAccount {
  externalId?: string;
  name: string;
  industry?: string;
  phone?: string;
  website?: string;
  customFields: Record<string, any>;
}

interface CanonicalDeal {
  externalId?: string;
  title: string;
  value: number;
  currency: string;
  stage: string;
  pipeline?: string;
  contactIds: string[];
  accountId?: string;
  expectedCloseDate?: number;
  customFields: Record<string, any>;
}

interface CanonicalActivity {
  externalId?: string;
  type: 'call' | 'meeting' | 'task' | 'email' | 'note';
  subject: string;
  description?: string;
  startTime: number;
  endTime: number;
  duration?: number;
  contactId?: string;
  dealId?: string;
  status: 'planned' | 'completed' | 'cancelled';
  callData?: { direction: string; disposition: string; recordingUrl?: string };
  metadata: Record<string, any>;
}

// Model mapper interface
interface CRMModelMapper {
  contact: {
    toCanonical(crmData: any): CanonicalContact;
    fromCanonical(contact: CanonicalContact): any;
  };
  account: {
    toCanonical(crmData: any): CanonicalAccount;
    fromCanonical(account: CanonicalAccount): any;
  };
  deal: {
    toCanonical(crmData: any): CanonicalDeal;
    fromCanonical(deal: CanonicalDeal): any;
  };
  activity: {
    toCanonical(crmData: any): CanonicalActivity;
    fromCanonical(activity: CanonicalActivity): any;
  };
}

class UnifiedModelService {
  async translateToCanonical(crmType: string, crmData: any, mapper: CRMModelMapper): Promise<any> {
    switch (crmType) {
      case 'contact': return mapper.contact.toCanonical(crmData);
      case 'account': return mapper.account.toCanonical(crmData);
      case 'deal': return mapper.deal.toCanonical(crmData);
      case 'activity': return mapper.activity.toCanonical(crmData);
    }
  }
}
```

## Open-Source Tools

| Tool | License | Purpose |
|------|---------|---------|
| **Zod** (MIT) | Validation | Canonical model validation |
| **TypeScript** (Apache 2.0) | Language | Type-safe model definitions |
| **jsonata** (MIT) | Transformation | Model transformation |

## Production Considerations

**Scaling:** The unified model adds serialization/deserialization overhead to every CRM operation. Pre-compile mappers for each adapter to minimize per-call transformation cost. Cache canonical model instances in request-scoped memory to avoid redundant transformations within the same request.

**Security:** The canonical model must not propagate sensitive data unintentionally. When mapping from CRM to canonical, filter out fields that are not part of the canonical schema. When mapping from canonical to CRM, only include fields that the integration is authorized to write. Implement field-level allowlists per integration.

**Monitoring:** Track model transformation success rate, average transformation time, custom field coverage (% of expected fields successfully mapped), and schema validation failure rate. Alert on high transformation failure rates that may indicate model mismatch between canonical and CRM schema versions.
