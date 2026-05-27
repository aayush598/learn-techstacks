# Section 05: Contact Segmentation & Tagging

## Overview

Contact segmentation enables targeted campaign execution by grouping contacts based on shared attributes, behaviors, or custom criteria. Instead of sending the same campaign to an entire contact list, segments allow precise targeting — for example, "high-value customers in California who haven't been contacted in 30 days." Tags provide a lighter-weight, more flexible categorization system that can be applied, removed, and searched dynamically.

The segmentation engine evaluates contact attributes against segment criteria at query time (dynamic segments) or at assignment time (static segments). Dynamic segments are evaluated each time a campaign fetches contacts, ensuring that contacts are always up-to-date with their current attributes. Static segments capture a snapshot of contacts at a point in time, useful for fixed campaign lists. Tags are simpler labels that can be applied manually, via API, or through automated rules.

## Architecture

```
+----------+    +----------+    +----------+    +----------+    +----------+
| Audio    |--->| WebSocket|--->| Jitter   |--->| PLC      |--->| Player   |
| Producer |    | (WSS)    |    | Buffer   |    | (Packet  |    | (smooth  |
| (100ms   |    | (binary) |    | (adaptive|    |  Loss    |    |  output) |
|  chunks) |    |          |    |  60-200) |    |  Conceal)|    +----------+
+----------+    +----------+    +----------+    +----------+
```


## Design Decisions

- **Provider Abstraction**: All STT providers implement a common interface. Enables seamless failover (Deepgram -> Whisper -> Web Speech API) without code changes.
- **VAD Gating**: Reduces STT costs by 40-60% by not billing silence. VAD miss rate must be <1%.
- **Audio Normalization**: 16kHz mono PCM via Kaiser-window resampling ensures consistent quality across diverse input codecs.
## Implementation Approach

```
class SegmentEngine {
  async evaluateSegment(segmentId, tenantContext) {
    const segment = await prisma.segment.findUnique({
      where: { id: segmentId }
    });

    if (segment.type === 'static') {
      return this.getStaticSegmentContacts(segmentId);
    }

    return this.queryDynamicSegment(segment.criteria, tenantContext);
  }

  async queryDynamicSegment(criteria, tenantContext) {
    const conditions = this.buildConditions(criteria);
    
    // Build optimized SQL/Prisma query
    const contacts = await prisma.contact.findMany({
      where: {
        tenant_id: tenantContext.tenantId,
        AND: [
          ...conditions.attributeConditions,
          this.buildTagConditions(criteria.tags),
          this.buildHistoryConditions(criteria.callHistory),
          this.buildComputedConditions(criteria.computed)
        ]
      },
      include: {
        tags: criteria.includeTags || false
      },
      take: criteria.limit || 10000,
      orderBy: this.buildSortOrder(criteria.sortBy)
    });

    return contacts;
  }

  buildConditions(criteria) {
    const conditions = [];
    
    if (criteria.filters) {
      for (const filter of criteria.filters) {
        switch (filter.operator) {
          case 'equals':
            conditions.push({ [filter.field]: filter.value });
            break;
          case 'greater_than':
            conditions.push({ [filter.field]: { gt: filter.value } });
            break;
          case 'in':
            conditions.push({ [filter.field]: { in: filter.values } });
            break;
          case 'contains':
            conditions.push({ [filter.field]: { contains: filter.value, mode: 'insensitive' } });
            break;
          case 'last_contacted_before':
            conditions.push({
              lastContactedAt: { lt: this.subtractDays(filter.days) }
            });
            break;
        }
      }
    }

    return { attributeConditions: conditions };
  }
}

class TagManager {
  async applyTags(contactId, tags, tenantContext) {
    // Bulk tag application with dedup
    const existingTags = await prisma.tag.findMany({
      where: {
        tenant_id: tenantContext.tenantId,
        name: { in: tags }
      }
    });

    const existingNames = new Set(existingTags.map(t => t.name));
    const newTags = tags
      .filter(t => !existingNames.has(t))
      .map(name => ({ name, tenant_id: tenantContext.tenantId }));

    // Create new tags and associate with contact
    await prisma.$transaction(async (tx) => {
      const created = await tx.tag.createMany({ data: newTags, skipDuplicates: true });
      const allTags = existingTags.concat(created);
      
      await tx.contactTag.createMany({
        data: allTags.map(t => ({
          contact_id: contactId,
          tag_id: t.id
        })),
        skipDuplicates: true
      });
    });
  }

  async getContactsByTag(tagName, tenantContext) {
    return prisma.contact.findMany({
      where: {
        tenant_id: tenantContext.tenantId,
        tags: { some: { tag: { name: tagName } } }
      }
    });
  }
}
```

## Integration Points

- **Campaign Engine (Ch 01):** Campaigns reference segments for contact selection
- **Contact Import (sec-01, sec-02):** Auto-tagging rules fire during import
- **Call Outcome Processing (Ch 04):** Dispositions can automatically add/remove tags
- **DNC Service (Ch 07):** DNC list membership is a special system tag
- **Analytics (Ch 09):** Segment performance comparison and tag analytics
- **CRM Integration (Part 10, Ch 02):** CRM segments can be synced to campaign segments

## Open-Source Tools

- **ws** (MIT): WebSocket
- **MediaRecorder API**: Recording
- **Opus** (BSD): Audio codec
## Production Considerations

- Dynamic segment queries on large contact databases (millions) require careful index design
- Cache segment evaluation results with a TTL (e.g., 5 minutes) for frequently accessed segments
- Segment refresh for static segments should be scheduled during off-peak hours
- Tag management UI should include tag usage analytics and unused tag cleanup
- Implement tag autocomplete in the UI to prevent typo-based tag proliferation
- Set maximum tag limits per contact (e.g., 50 tags) to prevent performance degradation
- Segment criteria validation is important — circular or contradictory criteria should be detected
- Segment preview feature showing contact count and sample members validates criteria before saving
- Consider materialized views for complex dynamic segments that are queried frequently
- Export segment membership for external analysis tools with privacy safeguards
