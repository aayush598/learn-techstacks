# Section 03: Contact Deduplication Strategies

## Overview

Contact deduplication prevents the same person from appearing multiple times in a contact list, which would result in duplicate calls, wasted telephony costs, and poor customer experience. Deduplication must handle exact matches (same phone number) and fuzzy matches (same person with slightly different data) across multiple dimensions — phone number, email, name, and custom field combinations.

The deduplication engine supports configurable matching rules per campaign or tenant. Some use cases require strict phone-only dedup, while others need multi-field matching with confidence thresholds. The system must also handle deduplication within a single import (internal dedup) and against existing contacts in the campaign or tenant (cross-reference dedup). Merge resolution strategies determine what happens when duplicates are found — skip, replace, or merge fields.

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
class DeduplicationEngine {
  constructor(config) {
    this.strategies = {
      phone: new PhoneMatchStrategy(config.phoneWeight),
      email: new EmailMatchStrategy(config.emailWeight),
      name: new FuzzyNameStrategy(config.nameWeight, config.nameThreshold),
      custom: new CustomFieldStrategy(config.customFields, config.customWeight)
    };
    this.threshold = config.matchThreshold; // 0.0 - 1.0
    this.mergeStrategy = config.mergeStrategy; // 'skip' | 'replace' | 'merge'
  }

  async findDuplicates(contact, existingContacts) {
    const candidates = [];

    for (const existing of existingContacts) {
      let totalScore = 0;
      let totalWeight = 0;

      for (const [name, strategy] of Object.entries(this.strategies)) {
        const { score, weight } = await strategy.match(contact, existing);
        totalScore += score * weight;
        totalWeight += weight;
      }

      const normalizedScore = totalWeight > 0 ? totalScore / totalWeight : 0;
      
      if (normalizedScore >= this.threshold) {
        candidates.push({
          existingContact: existing,
          matchScore: normalizedScore,
          matchedOn: this.getMatchedDimensions(contact, existing)
        });
      }
    }

    // Return best match
    return candidates.sort((a, b) => b.matchScore - a.matchScore)[0] || null;
  }

  async resolve(contact, duplicate) {
    switch (this.mergeStrategy) {
      case 'skip':
        return duplicate.existingContact;
      case 'replace':
        return { ...contact, id: duplicate.existingContact.id };
      case 'merge':
        return this.fieldLevelMerge(contact, duplicate.existingContact);
      default:
        return contact;
    }
  }
}

class FuzzyNameStrategy {
  match(contactA, contactB) {
    const nameA = `${contactA.firstName} ${contactA.lastName}`.toLowerCase();
    const nameB = `${contactB.firstName} ${contactB.lastName}`.toLowerCase();
    
    // Soundex comparison
    const soundexMatch = this.soundex(nameA) === this.soundex(nameB);
    // Levenshtein distance for typo tolerance
    const distance = this.levenshtein(nameA, nameB);
    const normalizedDistance = 1 - (distance / Math.max(nameA.length, nameB.length));
    
    const score = soundexMatch ? Math.max(0.7, normalizedDistance) : normalizedDistance;
    return { score, weight: this.weight };
  }

  soundex(s) {
    // Standard Soundex algorithm implementation
    return s.charAt(0) + s.slice(1).replace(/[aeiouyhw]/g, '').substring(0, 3);
  }

  levenshtein(a, b) {
    // Standard Levenshtein distance
    const matrix = Array.from({ length: a.length + 1 }, (_, i) => [i]);
    // ... full implementation truncated for brevity
  }
}
```

## Integration Points

- **Contact Import Pipeline (sec-01):** Dedup runs as a step within the import pipeline
- **API Import (sec-02):** Bulk API imports can enable/disable dedup via options
- **Contact Service:** Dedup result determines insert vs. update behavior
- **Campaign Service:** Dedup scope (per-campaign vs. per-tenant) is defined by campaign config
- **Analytics (Ch 09):** Dedup rate and duplicate detection metrics

## Open-Source Tools

- **ws** (MIT): WebSocket
- **MediaRecorder API**: Recording
- **Opus** (BSD): Audio codec
## Production Considerations

- Dedup performance degrades quadratically with list size — O(n²) for naive pairwise comparison
- Use blocking (indexing by phone area code or first letter of name) to reduce comparison space
- For lists >100K contacts, use database-level dedup with indexes rather than in-memory comparison
- Dedup threshold tuning is critical — too low catches duplicates but may merge unrelated contacts; too high misses duplicates
- Audit dedup decisions by logging the match score, matched dimensions, and resolution action
- Provide a dedup preview UI where users can see potential duplicates before committing merges
- Consider time-based dedup — contacts imported more than 30 days apart may be kept as separate entries
- Cross-tenant dedup is generally not performed for privacy and data isolation reasons
- Implement a manual merge tool for edge cases where automated dedup is uncertain
- Track dedup effectiveness metrics — duplicate call rate, merge accuracy, manual override rate
