# Section 07: Retry Priority Queuing

## Overview

When a campaign has thousands of contacts scheduled for retry, the order in which they are called matters significantly. Retry priority queuing ensures that the most important and most likely-to-answer contacts are called first, maximizing campaign effectiveness within available resource constraints. Without priority queuing, retries would be processed in FIFO order, which may not align with business priorities.

The priority system assigns each retry job a dynamic priority score based on contact value, predicted answer probability, retry attempt number, elapsed time since last attempt, and campaign-specific business rules. The retry queue is maintained as a sorted set, with the dialer always pulling the highest-priority contact next. Priority scores are recalculated periodically as conditions change — a contact's priority may increase as they wait longer or decrease if their calling window is about to close.

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
class RetryPriorityQueue {
  constructor(redis, config) {
    this.redis = redis;
    this.config = config;
    this.queueKey = 'retry:priority';
    this.recalculationInterval = 300000; // 5 minutes
  }

  async addToQueue(contact, campaign, attempt) {
    const member = `${contact.id}:${campaign.id}:${attempt.number}`;
    const score = await this.calculatePriority(contact, campaign, attempt);

    await this.redis.zadd(this.queueKey, score.toString(), member);
    
    return { member, score };
  }

  async popHighestPriority() {
    // Get the highest priority item
    const result = await this.redis.zrevrange(this.queueKey, 0, 0, 'WITHSCORES');
    if (result.length === 0) return null;

    const [member, score] = result;
    await this.redis.zrem(this.queueKey, member);

    const [contactId, campaignId, attemptNum] = member.split(':');
    return {
      contactId,
      campaignId,
      attemptNumber: parseInt(attemptNum),
      priorityScore: parseFloat(score)
    };
  }

  async calculatePriority(contact, campaign, attempt) {
    const factors = {
      contactValue: await this.getContactValueScore(contact),
      answerProb: await this.predictAnswerProbability(contact),
      waitTimeDecay: this.calculateWaitTimeDecay(attempt.lastAttemptAt),
      attemptsRemaining: this.calculateAttemptsRemaining(
        attempt.number, campaign.maxAttempts
      ),
      windowUrgency: await this.calculateWindowUrgency(contact, campaign)
    };

    // Composite score: weighted sum normalized to 0-1
    let score = 0;
    for (const [factor, value] of Object.entries(factors)) {
      const weight = this.config.factorWeights[factor] || 0;
      score += value * weight;
    }

    // Apply starvation prevention floor
    const hoursWaiting = this.hoursSince(attempt.lastAttemptAt);
    const floor = Math.min(0.8, hoursWaiting * 0.01); // Increases 0.01 per hour
    score = Math.max(score, floor);

    return Math.min(1.0, Math.max(0.0, score));
  }

  async recalculateAllPriorities() {
    // Get all items in queue
    const items = await this.redis.zrange(this.queueKey, 0, -1);
    
    const pipeline = this.redis.pipeline();
    
    for (const member of items) {
      const [contactId, campaignId, attemptNum] = member.split(':');
      
      // Fetch fresh data and recalculate
      const contact = await this.getContact(contactId);
      const campaign = await this.getCampaign(campaignId);
      const attempt = await this.getAttempt(contactId, campaignId, parseInt(attemptNum));
      
      const newScore = await this.calculatePriority(contact, campaign, attempt);
      pipeline.zadd(this.queueKey, newScore.toString(), member);
    }

    await pipeline.exec();
  }

  async removeFromQueue(contactId, campaignId) {
    // Remove all queue entries for this contact + campaign
    const pattern = `${contactId}:${campaignId}:*`;
    const cursor = '0';
    let membersToRemove = [];

    do {
      const [nextCursor, members] = await this.redis.sscan(
        this.queueKey, cursor, 'MATCH', pattern
      );
      membersToRemove = membersToRemove.concat(members);
      cursor = nextCursor;
    } while (cursor !== '0');

    if (membersToRemove.length > 0) {
      await this.redis.zrem(this.queueKey, ...membersToRemove);
    }
  }

  calculateWaitTimeDecay(lastAttemptAt) {
    if (!lastAttemptAt) return 0.5;
    const hours = this.hoursSince(lastAttemptAt);
    // Sigmoid-like decay: priority increases with wait time
    return 1 / (1 + Math.exp(-0.1 * (hours - 12)));
  }

  calculateAttemptsRemaining(attemptNumber, maxAttempts) {
    const remaining = maxAttempts - attemptNumber;
    const ratio = remaining / maxAttempts;
    // Higher priority for contacts with more remaining attempts
    return ratio;
  }

  async calculateWindowUrgency(contact, campaign) {
    // How close is the calling window to closing?
    const windowEnd = await this.getWindowEnd(contact, campaign);
    if (!windowEnd) return 0.5;
    
    const minutesLeft = (windowEnd.getTime() - Date.now()) / 60000;
    if (minutesLeft <= 0) return 0; // Window already closed
    if (minutesLeft <= 15) return 0.9; // Urgent
    if (minutesLeft <= 60) return 0.7;
    return 0.3;
  }
}
```

## Integration Points

- **Retry Scheduler:** Adds contacts to the priority queue after each failed attempt
- **Dialing Engine (Ch 01):** Pulls highest-priority contact for dialing
- **Smart Retry (sec-03):** Answer probability prediction feeds priority calculation
- **Contact Scoring:** Contact value score from CRM/lead scoring system
- **Calling Window Enforcer (Ch 03):** Window urgency calculation
- **Analytics (Ch 09):** Queue depth, average wait time, priority distribution monitoring

## Open-Source Tools

- **ws** (MIT): WebSocket
- **MediaRecorder API**: Recording
- **Opus** (BSD): Audio codec
## Production Considerations

- Redis sorted sets are in-memory — ensure the queue fits in memory (1M entries ≈ 100MB)
- Priority recalculation is CPU-intensive — run on a schedule rather than on every access
- Starvation prevention floor must be carefully calibrated — too high defeats prioritization, too low allows starvation
- Queue consistency between Redis and database — if Redis is lost, rebuild the queue from pending retry records
- Consider priority tiers (high, medium, low) instead of continuous scores for simpler management
- Test queue behavior under load — 100K items with concurrent producers and consumers
- Monitor queue wait time distribution — if high-value contacts consistently wait longer than low-value, priority weights need adjustment
- Remove contacts from the queue when they are exhausted or opt-out (don't waste queue space)
- Provide queue visualization in the UI — "Next 10 contacts to be called" with priority scores
- Redis persistence (RDB/AOF) should be configured to minimize queue data loss risk
