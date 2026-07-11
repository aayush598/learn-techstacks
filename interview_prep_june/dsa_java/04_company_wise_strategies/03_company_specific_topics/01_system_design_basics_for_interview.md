# System Design Basics for DSA Interviews

## LRU Cache

**Problem**: Design a cache with O(1) get and put, evicting least recently used.

**Solution**: HashMap + DoublyLinkedList
```
get(key): if exists, move node to front, return value
put(key, value): if exists update + move to front
                 else add to front, if full evict from back
```

**Data structures**: `HashMap<Integer, Node>`, `Node {key, value, prev, next}`, dummy head/tail

## TinyURL

**Problem**: Design a URL shortener that generates short aliases.

**Approaches**:
1. **Hash + base62**: MD5/SHA → first 6-7 chars → base62 encode (collision handling)
2. **Counter + base62**: Distributed counter → base62 encode
3. **Pre-generated keys**: Pre-generate unique IDs

**Storage**: Database (key → longURL), cache (Redis) for hot URLs

## Autocomplete System

**Problem**: Return top K sentences for a given prefix.

**Solution**: Trie + Heap
- Each node in trie stores top K hot sentences from that prefix
- On input: traverse trie, return precomputed top K
- On selection: update frequencies

**Optimizations**: Precompute top K at each node, update lazily or with MapReduce offline

## Top K System (Heavy Hitters)

**Problem**: Find top K frequent items in a stream.

**Solutions**:
1. **HashMap + Heap**: Exact, O(n log k) — needs all items
2. **Count-Min Sketch**: Probabilistic, approximate counts with sub-linear space
3. **Lossy Counting**: Deterministic approximation with bounded error

## Rate Limiter

**Problem**: Limit requests per user/IP in a time window.

**Algorithms**:
1. **Token Bucket**: Tokens refill at constant rate, each request consumes one
2. **Sliding Window Log**: Store timestamp of each request, count in window
3. **Sliding Window Counter**: Count in current + prev window, weighted average
4. **Fixed Window Counter**: Count reset at window boundary (simple but bursty)

## Key-Value Store

**CAP Theorem**: Pick 2 of Consistency, Availability, Partition Tolerance

**Consistent Hashing**: Distribute keys across nodes, minimal reshuffling on node add/remove
- Hash both keys and nodes to ring
- Each key assigned to nearest clockwise node
- Virtual nodes for better distribution

## Pub-Sub System

**Components**: Publisher, Subscriber, Topic, Message Queue

**Flow**: Publisher sends to topic → broker stores → delivers to all subscribers

**Variants**: At-most-once, at-least-once, exactly-once delivery
