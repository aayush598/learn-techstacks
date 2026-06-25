
---

# High-Level Design (Q101–Q250)

## Q101: Design URL Shortener (TinyURL)

**Answer:**

**Requirements:**
- **Functional:** Generate short alias for long URL, redirect to original URL, optional custom alias, TTL, analytics
- **Non-functional:** Highly available, low latency redirects, scalable to billions of URLs

**High-level architecture:**

```
[Client] → [Load Balancer] → [Web Servers]
                                  ↓
                         [Cache (Redis)]
                              ↓
                      [Database (SQL/NoSQL)]
                              ↓
                    [Analytics Service (Kafka + HDFS)]
```

**Key design decisions:**

1. **Key Generation:**
   - **Base62 encoding:** 62^7 = ~3.5T combinations
   - **Approach A (Unique ID + encode):** Use a distributed unique ID generator (Snowflake, Redis INCR) and encode to base62
   - **Approach B (Random):** Generate random 7-char string, check collision (rare at 3.5T space)

2. **Storage:** Two tables:
   - `url_mapping(short_key PK, long_url, created_at, expires_at, user_id)`
   - `click_events(id PK, short_key FK, timestamp, user_agent, ip, referrer)`

3. **Caching:** Cache `short_key → long_url` in Redis. Use LRU eviction. TTL based on access patterns.

4. **Redirection:** HTTP 301 (permanent redirect — cached by browser, fewer hits to server) vs 302 (temporary — allows analytics). Recommendation: 301 for production, 302 for A/B testing.

5. **Scale:**
   - **Read:** 100K QPS → Cache handles 99%, DB handles 1%
   - **Write:** 1000 QPS → DB handles directly, async analytics
   - DB sharding by `short_key` hash for writes, replicas for reads

**API Design:**
```
POST /shorten
  Request: { "url": "https://...", "custom_alias": "myalias", "ttl_days": 30 }
  Response: { "short_url": "https://short.url/abc1234" }

GET /{short_key}
  Response: HTTP 301 → long URL
```

**Estimation:**
- 1B URLs, 10K new/s, 100K redirects/s
- Storage: 1B × 500 bytes = 500GB
- Cache: 20% most accessed URLs ≈ 200M entries × 200 bytes = 40GB RAM

---

## Q102: Design WhatsApp / Messenger

**Answer:**

**Requirements:**
- **Functional:** One-on-one chat, group chat, last seen, read receipts, media sharing, voice/video calls
- **Non-functional:** Low latency (<100ms), high availability, end-to-end encryption, offline delivery

**Architecture:**

```
Client A ←→ WebSocket/HTTP Long Polling → [Load Balancer] → [Chat Service]
                                                                  ↓
                                                         [Message Queue (Kafka)]
                                                                  ↓
                                                         [Delivery Workers]
                                                                  ↓
                                                    [Notification Service (Push)]
                                                                  ↓
                                                         [Database (Cassandra)]
```

**Detailed Design:**

1. **Connection Management:**
   - **WebSocket:** Persistent TCP connection for real-time bidirectional communication
   - **Connection Manager:** Maintains mapping `userId → WebSocket connection`. If on multiple devices, `userId → List<WebSocket>`
   - If WebSocket fails, fallback to **Long Polling**

2. **Message Flow:**
   - Alice sends message → Chat Service → Kafka (persistence + ordering) → Delivery Worker
   - Delivery Worker: If Bob is online (WebSocket open), push message directly
   - If Bob is offline, store message in DB + send push notification via FCM/APNs
   - Message stored with `(sender_id, receiver_id, timestamp, content, status)`

3. **Message Ordering and ID:**
   - Each message gets a globally unique ID from Snowflake (timestamp-based)
   - Messages are ordered by `(sender_id, receiver_id, timestamp)` or by server-assigned sequence number within conversation

4. **Last Seen & Read Receipts:**
   - Client sends periodic heartbeats to update `last_seen` in Redis
   - Read receipts: When Bob opens the chat, client sends `{ conversation_id, last_read_message_id }`
   - Server updates `last_read_message_id` for the conversation

5. **Group Chat:**
   - Fan-out approach: For groups < 100, store message once per group, members pull on join
   - For groups > 100, each member gets their own copy (write-amplified but read-efficient)
   - Hybrid: Small groups = single copy + pull; Large groups = fan-out writes

6. **End-to-End Encryption (E2EE):**
   - Signal Protocol for each conversation
   - Each message has a unique encryption key
   - Server never sees plaintext content

7. **Media Sharing:**
   - Upload to CDN/Blob Store (S3)
   - Generate thumbnail (compressed version)
   - Send thumbnail URL in message, full image fetched lazily
   - Use pre-signed URLs with TTL for security

8. **Scalability:**
   - **Chat Service:** Stateless, horizontally scalable
   - **Database:** Cassandra for message storage (write-optimized, time-series data)
   - **Cache:** Redis for `userId → connection` mapping, session data
   - **CDN:** For media files to reduce latency

**Estimation:**
- 2B users, 100M daily active
- 50 messages/user/day = 5B messages/day ≈ 58K messages/sec
- Storage: 365 days × 5B messages × 1KB = 1.8PB/year

---

## Q103: Design Twitter / Feed System

**Answer:**

**Requirements:**
- **Functional:** Post tweet, follow/unfollow, news feed (timeline), like/retweet/reply, trending topics
- **Non-functional:** Low latency feed loading, high write throughput (thousands of tweets/sec), eventual consistency acceptable

**Architecture:**

```
[Client] → [Load Balancer] → [API Gateway]
                                    ↓
                      ┌────────────┴────────────┐
               [Tweet Service]          [Feed Service]
                      ↓                         ↓
              [Timeline Cache]          [Fanout Workers]
                      ↓                         ↓
              [Tweet DB (Cassandra)]    [Feed Cache (Redis)]
                      ↓
              [Search Service (Elasticsearch)]
                      ↓
              [Trending Topics (Spark Streaming)]
```

**Core Design: Feed Generation**

**Approach A: Pull-based (Fanout on Read)**
- On feed load, query all followees' recent tweets, merge and sort
- **Pro:** Minimal write amplification, fresh tweets always
- **Con:** Slow for users with many followees (need to query 1000+ users)

**Approach B: Push-based (Fanout on Write)**
- When a celebrity tweets, push to all followers' timelines
- **Pro:** Feed load = O(1) cache read
- **Con:** Write amplification for celebrities with millions of followers

**Hybrid Approach (Recommended):**
- **Regular users (< 10K followers):** Push-based. Pre-compute feeds on tweet creation
- **Celebrities (> 10K followers):** Pull-based. Followers merge celebrity tweets into their feed on load
- This avoids the "thundering herd" problem when a celebrity tweets

**Tweet Creation Flow:**
1. Tweet Service receives tweet, writes to Tweet DB (Cassandra)
2. Tweet Service publishes event to "NewTweet" Kafka topic
3. Fanout Worker consumes:
   - Look up follower list from Social Graph Service (Redis)
   - For regular users: push tweet ID to each follower's timeline cache (Redis sorted set, score = timestamp)
   - For celebrities: add tweet ID to celebrity's tweet list in Redis

**Feed Loading Flow:**
1. Client requests feed (page 1, last 20 tweets)
2. Feed Service loads from timeline cache (Redis sorted set: `user:{userId}:timeline`)
3. For each tweet ID, fetch tweet content from Tweet Cache (Redis)
4. Add celebrity tweets (not yet pushed) — fetch from each celebrity's tweet list
5. Merge and sort all tweets by timestamp
6. Return top 20, along with cursor for pagination

**Database Schema (Cassandra):**
```sql
CREATE TABLE tweets (
    user_id text,
    tweet_id timeuuid,
    content text,
    media_urls list<text>,
    like_count counter,
    retweet_count counter,
    PRIMARY KEY (user_id, tweet_id)
) WITH CLUSTERING ORDER BY (tweet_id DESC);

CREATE TABLE timeline (
    user_id text,
    tweet_id timeuuid,
    author_id text,
    timestamp bigint,
    PRIMARY KEY (user_id, tweet_id)
) WITH CLUSTERING ORDER BY (tweet_id DESC);
```

**Search:**
- Elasticsearch for full-text tweet search
- Inverted index on tweet content, user mentions, hashtags

**Trending Topics:**
- Spark Streaming consumes tweet stream
- Sliding window count of hashtags (e.g., last 1 hour, 24 hours)
- Trending = most frequent hashtags, penalized for long-term popularity (use velocity not just volume)

**Estimation:**
- 500M tweets/day = 5,800 tweets/sec (peak ~15K/sec)
- 300M DAU, each reads 200 tweets/day = 60B feed reads/day
- Feed read is cached Redis ZSET with tweet IDs only

---

## Q104: Design Uber / Ride-sharing

**Answer:**

**Requirements:**
- **Functional:** Request ride, find nearby drivers, match rider with driver, real-time tracking, fare calculation
- **Non-functional:** Low latency match (< 5s), high availability, location privacy, scalability to millions

**Architecture:**

```
[Rider App] ←→ WebSocket/SSE → [Load Balancer] → [API Gateway]
                                                         ↓
[Driver Location Service (Redis Geo)] ← [Ride Service]
                         ↓
                  [Dispatch Service]
                         ↓
                  [Matching Engine]
                         ↓
                  [Kafka]
                         ↓
                  [Surge Pricing Service]
                         ↓
                  [Database (PostgreSQL + Cassandra)]
```

**Core Design: Driver Location Management**

**Problem:** Millions of drivers sending location updates every 3-5 seconds. Need to query "drivers within 5km" in < 50ms.

**Solution — Redis Geo:**
- Redis GEOADD stores driver locations: `GEOADD drivers:city {longitude} {latitude} {driver_id}`
- GEORADIUS queries: `GEORADIUS drivers:city {lng} {lat} 5 km`
- Geo-hashing on client side to reduce updates: Only send if location changed > 100m
- **Grid segmentation:** Divide city into grid cells (1km × 1km). Driver updates sent to cell topic

**Matching Flow:**
1. Rider requests ride → Ride Service
2. Query Redis Geo for nearby drivers (radius = 5km, expand if none found)
3. **Matching strategies:**
   - **Nearest driver:** Simple but may not be optimal
   - **ETA-based:** Calculate estimated time of arrival for top-5 drivers, pick fastest
   - **Batched matching:** Wait 2 seconds (or fill a batch of 10 riders) and solve assignment problem optimally (Hungarian algorithm / linear programming)
4. Send ride request to selected driver(s) via WebSocket
5. Driver accepts → ride confirmed, all other drivers notified to cancel

**Sending ride request to drivers:**
- Push to top-N nearest drivers' WebSockets
- First driver to accept gets the ride
- If no driver accepts within 15 seconds, expand radius

**Geospatial Indexing Options:**
- **Redis Geo:** Simple, fast, but in-memory — all data must fit in RAM
- **GeoHash:** Encode lat/lng into base32 string. Query prefix = bounding box
- **QuadTree / Google S2:** More precise, used by Uber for geofencing

**Surge Pricing:**
- Monitor `driver_availability / rider_demand` ratio in each grid cell
- If ratio < threshold (e.g., 1.5 drivers per rider), apply surge multiplier
- Formula: `surge = base_rate * max(1, (demand / supply) * elasticity_factor)`
- Notify riders of surge before confirming

**Ride Lifecycle:**
```
REQUESTED → DRIVER_ACCEPTED → ARRIVING → IN_PROGRESS → COMPLETED → PAID
                ↓ CANCELLED (ride timeout)         → CANCELLED
```

**Data Storage:**
- **Ride events:** Cassandra (time-series: ride_id, timestamp, status, location)
- **Driver location:** Redis (ephemeral, TTL = 60 seconds)
- **User/Driver profiles:** PostgreSQL
- **Trip history:** Data warehouse (Hive/BigQuery)

**Fare Calculation:**
```
distance_fare = distance_km * per_km_rate
time_fare = duration_min * per_min_rate
base_fare = base_rate
total = (base_fare + distance_fare + time_fare) * surge_multiplier
```

**Estimation:**
- 15M trips/day, 1M concurrent drivers
- Location updates: 1M × (1/5 Hz) = 200K writes/sec
- Ride matches: 15M/day = 175 matches/sec peak

---

## Q105: Design YouTube / Netflix (Video Streaming)

**Answer:**

**Requirements:**
- **Functional:** Upload video, transcode to multiple qualities, stream video, search, recommendations
- **Non-functional:** Low latency streaming, high availability, adaptive bitrate (ABR), CDN distribution

**Architecture:**

```
[Upload] → [Load Balancer] → [Upload Service] → [Blob Store (S3)]
                                                      ↓
                                              [Video Processing Pipeline]
                                                      ↓
                                    ┌─────────────────┴─────────────────┐
                              [Transcoder]                        [Thumbnail Generator]
                                    ↓                                     ↓
                              [CDN (Edge Servers)]                [CDN]
                                    ↓
[Client (ABR)] ← [Streaming Service] ← [CDN]
                                    ↓
                              [Metadata DB (PostgreSQL)]
                                    ↓
                              [Search (Elasticsearch)]
                                    ↓
                              [Recommendation Engine]
```

**Core Design: Video Upload & Processing**

1. **Upload:**
   - Client uploads video to Upload Service (chunked upload for large files)
   - Upload Service saves raw video to Blob Store (S3/Google Cloud Storage)
   - Metadata (title, description, tags) saved to Metadata DB
   - Video processing job published to Kafka

2. **Video Transcoding:**
   **Why transcode?** Different devices need different resolutions/bitrates. ABR (Adaptive Bitrate Streaming) requires multiple renditions.
   - **Resolutions:** 360p, 480p, 720p, 1080p, 4K
   - **Codecs:** H.264 (widest compatibility), VP9 (better compression), AV1 (best but slow)
   - **Process:**
     1. Split video into **segments** (2-10 seconds each)
     2. Transcode each segment to all target resolutions
     3. Generate **Manifest file** (.m3u8 for HLS, .mpd for DASH)
     4. Upload segments + manifest to CDN

3. **ABR (Adaptive Bitrate Streaming):**
   - Client downloads manifest file listing all renditions
   - Client's ABR algorithm monitors: buffer level, download speed, device capabilities
   - Switches between qualities seamlessly at segment boundaries
   - **BBA (Buffer-Based Algorithm):** If buffer > 30 seconds, request higher quality; if < 5 seconds, lower quality
   - **Throughput-based:** Average download speed of last N segments → predict best quality

4. **CDN Caching:**
   - Video segments cached at CDN edge servers (closest to user)
   - **Cache hit:** 90%+ for popular videos → served from edge
   - **Cache miss:** CDN fetches from origin server, caches for subsequent requests
   - Popular videos are proactively pushed to CDN edges

5. **Recommendation Engine:**
   - **Collaborative Filtering:** Users who watched X also watched Y
   - **Content-based:** Similar tags, categories, descriptions
   - **Deep Learning:** Neural network embeddings for user and video vectors
   - Two-stage: Candidate generation (hundreds) → Ranking (dozens) → Re-ranking (diversity)

6. **Live Streaming:**
   - Ingest RTMP stream → Transcoding pipeline (real-time, low latency)
   - **HLS Latency:** Standard HLS has 20-30s delay. LL-HLS (Low-Latency HLS) reduces to 2-5s
   - **WebRTC:** Sub-second latency for interactive streaming (used by Twitch alternatives)

**Storage Estimation:**
- 500 hours of video uploaded per minute
- 1 minute of raw video = 500MB (uncompressed) → 30MB (compressed H.264)
- Total storage per minute: 500 × 30MB = 15GB/min
- Total per year: 15GB × 60 × 24 × 365 = ~8PB/year

**Bandwidth:**
- 1B hours watched/day
- Average bitrate: 5 Mbps
- Bandwidth: 1B × 3600 × 5 Mbps / 8 = 2.25 exabits/day ≈ 28 TB/s

---

## Q106: Design Instagram / Photo Sharing

**Answer:**

**Requirements:**
- **Functional:** Upload photo/video, filters, follow/unfollow, feed, like/comment, stories, explore
- **Non-functional:** Low latency feed, high write throughput for photos, availability > storage consistency

**Architecture:**

```
[Client] → [Load Balancer] → [API Gateway]
                                    ↓
                     ┌──────────────┴──────────────┐
              [Photo Service]               [Feed Service]
                     ↓                              ↓
              [Image Processor]            [Fanout Workers]
                     ↓                              ↓
              [CDN (CloudFront)]           [Feed Cache (Redis)]
                     ↓
              [Metadata DB (Cassandra)]
                     ↓
              [Social Graph (TiDB/Neo4j)]
```

**Core Design: Photo Upload**

1. Client uploads photo → Upload Service
2. Service generates photo ID (Snowflake)
3. Original image saved to S3/Blob Store
4. Image Processor (async via Kafka) performs:
   - **Thumbnail generation:** 150×150 for feed
   - **Resizing:** 640×640, 1080×1080
   - **Filters:** Apply selected filter server-side or client-side
5. All resized versions uploaded to CDN
6. Metadata saved: `(photo_id, user_id, caption, location, timestamp, CDN_urls)`

**Feed Generation:**
- Same hybrid push/pull as Twitter (Q103)
- Regular users (< 10K followers): push photo ID to followers' feed cache
- Celebrities: followers pull from celebrity's feed on load

**Stories (Ephemeral Content):**
- Stories expire in 24 hours
- Stored with TTL in Redis / Cassandra (TTL column)
- Each user's stories stored as list: `user:{userId}:stories`
- Feed generation: merge stories from followed users (sorted by recency)
- Seen-status tracked per user-story pair

**Explore Page (Discovery):**
- **Content-based:** Extract image embeddings using CNN (ResNet, EfficientNet)
- **Similarity search:** Use ANN (Approximate Nearest Neighbor) index — FAISS, Annoy
- **User interest:** Track what user likes/saves, recommend similar content
- **Trending:** Cluster popular photos by content similarity

**Photo Storage Estimation:**
- 100M photos/day, avg 2MB per photo (compressed)
- Storage: 200 TB/day, 73 PB/year (before replication)
- CDN reduces origin load by 95%

**Database:**
- **Photo metadata:** Cassandra (partition by user_id, cluster by timestamp)
- **Social graph (follows):** Cassandra wide-row `follower_id → Set<followee_id>` or Neo4j
- **Feed cache:** Redis sorted sets per user

---

## Q107: Design Dropbox / Google Drive

**Answer:**

**Requirements:**
- **Functional:** Upload/download files, sync across devices, file sharing, versioning, folder organization
- **Non-functional:** High consistency (files must be correct), conflict resolution, offline support, delta sync

**Architecture:**

```
[Client App] ←→ [API Gateway] ←→ [Metadata Service]
                                         ↓
                                  [Block Store (S3)]
                                         ↓
                                  [Delta Sync Service]
                                         ↓
                                  [Notification Service (WebSocket)]
                                         ↓
                                  [Database (PostgreSQL + Cassandra)]
```

**Core Design: File Sync**

**Key insight:** Don't sync entire files — sync **blocks** (chunks). Each file is split into fixed-size blocks (e.g., 4MB). Each block has a content hash (SHA-256).

**Upload Flow:**
1. Client computes block hashes for each block in the file
2. Client sends block hashes to Sync Service
3. Sync Service checks which blocks already exist in Block Store (dedup)
4. Client uploads only **new blocks**
5. After upload, Sync Service records file metadata: `(file_id, version, block_list, user_id, parent_folder)`
6. Changes propagated to linked devices via Notification Service

**Download Flow:**
1. Client requests file → Metadata Service returns block list
2. Client downloads each block (parallel, from CDN/Block Store)
3. Client reconstructs file from blocks
4. Client verifies integrity (SHA-256 hash match)

**Delta Sync:**
- For small changes (e.g., editing a text file), uploading the entire file is wasteful
- **rsync-like algorithm:** Client and server exchange checksums of blocks, only changed blocks transmitted
- **Binary diff:** For files within same version family, compute binary diff and send only differences

**Conflict Resolution:**
- **Last writer wins:** Simplest, but may lose data
- **Versioning:** Keep both versions as separate conflict copies
- **CRDT (Conflict-free Replicated Data Type):** For collaborative editing (Google Docs style), merge conflicts automatically at data structure level
- Dropbox: Creates "conflicted copy" files

**Offline Support:**
- Client maintains local SQLite database of file metadata and block cache
- Changes queued locally, synced when online
- **Sync status:** Green (synced), Yellow (syncing), Red (conflict), Blue (offline edits pending)

**Versioning:**
- Each file version stored as a snapshot of block list
- Space-efficient: only changed blocks stored for new versions
- Version retention: unlimited (paid) or 30 days (free), with ability to restore any version

**File Sharing:**
- Shares stored as `(file_id, shared_by, shared_with, permission, expiry)`
- Links: generate token with TTL, embed in URL
- Permission levels: view, comment, edit

**Storage Deduplication:**
- Block-level: Same block across files/users stored once (if same file shared)
- Saves 30-50% storage for popular files

**Database Schema (PostgreSQL for metadata):**
```sql
CREATE TABLE files (
    file_id UUID PRIMARY KEY,
    user_id UUID,
    name TEXT,
    parent_folder_id UUID REFERENCES folders,
    is_directory BOOLEAN,
    size BIGINT,
    mime_type TEXT,
    version INT,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

CREATE TABLE file_blocks (
    file_id UUID,
    version INT,
    block_index INT,
    block_hash TEXT,
    PRIMARY KEY (file_id, version, block_index)
);

CREATE TABLE blocks (
    block_hash TEXT PRIMARY KEY,
    ref_count INT,
    size INT,
    storage_path TEXT
);
```

**Estimation:**
- 500M users, 2GB average storage per user = 1EB total storage
- 100M daily active syncing = 10K file updates/sec peak
- Dedup ratio: ~40%, actual storage ~600PB

---

## Q108: Design E-commerce (Amazon)

**Answer:**

**Requirements:**
- **Functional:** Product catalog, product search, cart, checkout, payment, order tracking, seller portal, reviews
- **Non-functional:** High availability (99.99%), consistency for payments (ACID), scalability for flash sales

**Architecture:**

```
[Client] → [CDN] → [Load Balancer] → [API Gateway]
                                            ↓
                   ┌──────────────────────┴──────────────────────┐
            [Product Service]    [Cart Service]    [Order Service]
                   ↓                    ↓                    ↓
            [Product Index]       [Cart Cache]         [Order DB]
            (Elasticsearch)       (Redis)              (PostgreSQL)
                   ↓                                       ↓
            [Catalog DB]                              [Payment Service]
            (MySQL Sharded)                                ↓
                                                      [Fraud Detection]
                                                           ↓
                                                      [Kafka]
                                                           ↓
                   ┌───────────────────────────────────────┴──────┐
            [Inventory Service]                      [Shipping Service]
                   ↓                                       ↓
            [Inventory DB]                             [Logistics Provider API]
```

**Core Design Components:**

### Product Catalog
- **Challenges:** 350M+ products, complex facets (brand, size, color, price range), real-time inventory
- **Database:** Sharded MySQL by product_id hash
- **Search:** Elasticsearch — inverted index on product attributes
- **Caching:** Product pages cached in Redis (CDN for static HTML). Invalidated when price/stock changes

### Cart Service
- **Stateless** from user perspective — cart stored on server (not local storage)
- **Storage:** Redis with TTL (`cart:{userId}` hash, keys = product_id, values = quantity)
- **Merge on login:** Merge guest cart with saved cart from previous session

### Order Processing
```
Checkout → Validate Cart → Reserve Inventory → Process Payment → Create Order → Send Confirmation
```

- **Step 1: Reserve Inventory:** Optimistic locking on inventory count
```sql
UPDATE inventory SET reserved = reserved + 1 WHERE product_id = ? AND stock - reserved >= 1;
```
- **Step 2: Payment:** Idempotent payment (order_id as idempotency key)
- **Step 3: Order created** with status PENDING → CONFIRMED → SHIPPED → DELIVERED
- All steps orchestrated via Saga pattern (compensating actions for failures)

### Payment Service
- **Multiple gateways:** Stripe, PayPal, Razorpay — abstracted via Adapter pattern
- **PCI DSS compliance:** Never store raw card numbers
- **Idempotency:** Each payment request has `idempotency_key = order_id`, gateway ensures exactly-once
- **Failure handling:** Retry with exponential backoff, dead-letter queue for manual review

### Inventory Management
- **Synchronous reservation** (during checkout, hold for 15 minutes)
- **Asynchronous stock update** (when order placed, decrement actual stock)
- **Sharding:** By product_id or warehouse_id
- **Read replicas** for catalog browsing, primary for writes during checkout

### Flash Sale / High Traffic Patterns
1. **Throttle at API Gateway:** Rate limit per user (1 request/5 seconds)
2. **Queue checkout requests:** Kafka/Redis queue, workers process at capacity
3. **Pre-reduce inventory:** For limited drops, pre-reserve stock for confirmed users
4. **Circuit breaker:** If payment service lags, gracefully degrade (show "high traffic")

### Caching Strategy
| Layer | Cache | TTL | Invalidation |
|-------|-------|-----|-------------|
| Product page | CDN (HTML) | 1 hour | Webhook on price/stock change |
| Product details | Redis | 5 min | Cache-aside with writes |
| Cart | Redis | 7 days | Writes go directly to cache |
| User sessions | Redis | 30 min | Session expiry |
| Search results | Elasticsearch query cache | 1 min | Index updates |

### Scaling for Peak (Prime Day)
- Horizontal scaling of all stateless services
- Database read replicas (10× normal)
- Auto-scaling groups with pre-warmed instances
- Chaos engineering: GameDay simulations

---

## Q109: Design Web Crawler

**Answer:**

**Requirements:**
- **Functional:** Crawl web pages starting from seed URLs, extract content, detect duplicate content, respect robots.txt, schedule re-crawls
- **Non-functional:** Crawl billions of pages, polite crawling (don't DDoS), fault-tolerant

**Architecture:**

```
[Seed URLs] → [URL Frontier (Priority Queue)]
                     ↓
              [Crawl Worker Pool]
                     ↓
              [Downloader] → [Internet]
                     ↓
              [Content Parser]
                     ↓
         ┌───────────┴───────────┐
    [Deduplication]          [Link Extractor]
         ↓                         ↓
    [Content Store]          [URL Filter]
         ↓                         ↓
    [Blob Store]             [URL Frontier]
                                   ↓
                           [URL Seen Check (Bloom Filter)]
```

**Core Components:**

### 1. URL Frontier
- **Manages URLs to crawl** with politeness settings
- **Priority queue:** News articles > Blog posts > Regular pages
- **Politeness delay:** Don't hit same domain more than once per X seconds
- **Back-queue per domain:** Each domain has its own queue to enforce politeness
- **Freshness:** URLs that change frequently get re-crawled sooner

### 2. DNS Resolution
- **Caching:** DNS results cached to reduce latency
- **Batch resolution:** Resolve multiple URLs for the same domain at once

### 3. Downloader
- HTTP client with customizable headers, timeout, retry
- **Robots.txt cache:** Parse and cache `robots.txt` per domain, respect `Disallow` rules
- **JavaScript rendering (optional):** Headless browser (Chrome Puppeteer) for SPAs

### 4. Deduplication — Content Fingerprinting
- **Simhash:** Generate fingerprint of document content
- **Near-duplicate detection:** Cosine similarity or Simhash Hamming distance < threshold
- **URL dedup:** Bloom filter for URLs already seen (space-efficient, allows false positives for "already crawled")

### 5. URL Normalization & Filtering
- Normalize: lowercase, remove fragments, sort query params
- Filter: Exclude file types (.pdf, .jpg, .mp4), spam domains, blacklisted URLs

### 6. Storage
- **Raw content:** Blob store (S3/HDFS), keyed by document hash
- **Metadata:** URL, crawl timestamp, content-type, links count, HTTP status
- **Index:** Elasticsearch for full-text search

### 7. Crawl Policy
- **BFS:** Simple, but doesn't prioritize important pages
- **Politeness:** Configurable delay between requests to same domain
- **Respect `Crawl-Delay`** in robots.txt
- **Sitemaps:** Parse XML sitemaps for high-value pages

### Scaling & Performance
| Metric | Value |
|--------|-------|
| Pages/day | 1B+ |
| Crawlers | 10K machines |
| Per crawler throughput | 100 pages/sec |
| Bandwidth | 10 Gbps per crawler |

### Politeness Queue
```
Time-wheel: Each domain added with next allowed crawl time
Poller: Check time-wheel every second, move ready domains to frontier
```

---

## Q110: Design Rate Limiter

**Answer:**

**Requirements:**
- **Functional:** Limit requests per user/IP/API key within time window, configurable rules, different limits per tier
- **Non-functional:** Low latency (< 1ms added), distributed, accurate, high availability

**Architecture:**

```
[Client] → [API Gateway] → [Rate Limiter Middleware]
                                   ↓
                      ┌────────────┴────────────┐
                   [Redis Cluster]         [Local Cache]
                   (distributed)           (in-memory, for burst)
```

**Algorithms (detailed in Q39):**

### Token Bucket (Recommended for most use cases)
```java
class DistributedTokenBucket {
    private final Redis redis;

    boolean allowRequest(String key, int capacity, int refillRate) {
        String luaScript = """
            local key = KEYS[1]
            local now = tonumber(ARGV[1])
            local capacity = tonumber(ARGV[2])
            local refillRate = tonumber(ARGV[3])

            local bucket = redis.call('hgetall', key)
            local lastRefill = 0
            local currentTokens = capacity

            if #bucket > 0 then
                lastRefill = tonumber(bucket[2])
                currentTokens = tonumber(bucket[4])
            end

            local elapsed = math.max(0, now - lastRefill)
            currentTokens = math.min(capacity, currentTokens + elapsed * refillRate)

            if currentTokens >= 1 then
                currentTokens = currentTokens - 1
                redis.call('hmset', key, 'lastRefill', now, 'tokens', currentTokens)
                return 1
            else
                return 0
            end
        """;
        return redis.eval(luaScript, key, System.currentTimeMillis(), capacity, refillRate);
    }
}
```

### Optimization: Local Cache + Redis
- **Local cache:** Use in-memory token bucket with short TTL (e.g., 1 second). Handles 90% of requests without Redis round trip
- **Redis:** Synchronize counters across instances. Eventual consensus — slight over- or under-count is acceptable
- **Lua scripts** ensure atomicity

### Response Headers
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 45
X-RateLimit-Reset: 1620000000
```

**Handling Exceeded Limits:**
```json
HTTP 429 Too Many Requests
{
  "error": "rate_limit_exceeded",
  "message": "API rate limit exceeded. Retry after 30 seconds.",
  "retry_after": 30
}
```

**Distributed Considerations:**
- **Clock skew:** Use Redis time (avoid server clock dependency)
- **Race condition:** Redis Lua scripts provide atomicity
- **Fail open:** If Redis is down, fall back to local rate limiting (slightly inaccurate but keeps service up)

---

## Q111: Design Notification System

**Answer:**

**Requirements:**
- **Functional:** Send notifications via email, SMS, push, in-app. Template-based. Priority levels. User preferences.
- **Non-functional:** High throughput (1M+/min), reliable delivery, ordering per user

**Architecture:**

```
[Service A] → [Notification API] → [Kafka (Event Bus)]
                                         ↓
                                  [Notification Workers]
                                         ↓
                     ┌─────────────────┴─────────────────┐
              [Render Service]                    [Preference Filter]
                     ↓                                     ↓
              [Template Engine]                    [User Preferences DB]
                     ↓
              [Channel-specific Senders]
              (Email/SMS/Push/InApp)
                     ↓
              [Delivery Providers]
              (SES, Twilio, FCM)
                     ↓
              [Analytics & Tracking]
```

**Detailed Flow:**

1. **Producer:** Any service publishes `NotificationEvent` to Kafka:
```json
{
  "event_id": "uuid",
  "user_id": "123",
  "template_id": "order_confirmation",
  "channels": ["email", "push"],
  "params": { "order_id": "456", "total": "$50" },
  "priority": "HIGH"
}
```

2. **Notification Workers** consume events:
   - **Preference Filter:** Check user's opt-in preferences (e.g., user disabled push at night)
   - **Rate Limit Check:** Don't send > 5 notifications per hour per user
   - **Deduplication:** Same event_id skipped if already processed

3. **Render Service:**
   - Load template: `"Hello {{name}}, your order {{order_id}} is confirmed for {{total}}"`
   - Inject parameters, render HTML/plaintext

4. **Channel Senders:**
   - **Email:** SES/SendGrid, SMTP pool, batch sends
   - **SMS:** Twilio/AWS SNS, 160-char limit
   - **Push:** FCM (Android), APNs (iOS). 4KB payload limit
   - **In-App:** WebSocket push to open connections

5. **Retry & Dead Letter:**
   - Failed deliveries retried: 1min, 5min, 30min, 2hr, 6hr
   - After max retries → Dead Letter Queue (DLQ)
   - Track delivery status: `PENDING → SENT → DELIVERED → READ → FAILED`

6. **Analytics:** Open rates, click-through rates, A/B testing

### Database Schema
```sql
CREATE TABLE notifications (
    event_id UUID PRIMARY KEY,
    user_id UUID,
    template_id TEXT,
    status TEXT,
    channels TEXT[],
    priority TEXT,
    created_at TIMESTAMP,
    sent_at TIMESTAMP,
    delivered_at TIMESTAMP
);

CREATE TABLE notification_templates (
    template_id TEXT PRIMARY KEY,
    subject_template TEXT,
    body_template TEXT,
    channel TEXT
);
```

---

## Q112: Design News Feed System

(Same as Q103 — Feed System)

## Q113: Design Search Autocomplete (Trie-based)

**Answer:**

**Requirements:**
- **Functional:** Return top-N completions for prefix, real-time, support for new queries, personalization
- **Non-functional:** < 50ms latency, handle 50K QPS, support 500M queries/day

**Architecture:**

```
[Client] → [CDN] → [Load Balancer] → [API Gateway]
                                            ↓
                                   [Query Service]
                                            ↓
                                   [Trie Cache (Redis)]
                                            ↓
                                   [Trie Store (DynamoDB/SSD)]
                                            ↓
                              [Offline Aggregator (MapReduce/Spark)]
```

**Core Data Structure: Trie**

```java
class TrieNode {
    Map<Character, TrieNode> children = new HashMap<>();
    Map<String, Integer> topQueries;  // Pre-computed top-5 for this prefix
    int frequency;
    boolean isEnd;
}
```

**Building the Trie (Offline):**
1. Aggregate search queries from logs (past 30 days)
2. MapReduce: `map(query → 1)`, `reduce(query → count)`
3. Build trie: For each query, insert into trie, update frequency at each node
4. At each node, maintain top-K queries (by frequency) that match this prefix
5. Serialize and store trie in key-value store (DynamoDB) or memory-mapped file

**Processing a Query:**
1. Client sends `GET /autocomplete?q=app&top=5`
2. Query Service looks up in Trie Cache:
   - Traverse trie: a → p → p
   - At node for "app", return pre-computed top-5 completions
3. If not in cache, fetch from Trie Store (DynamoDB), populate cache

**Optimizations:**
- **Pre-compute at each node:** Store top-5 completions to avoid traversal
- **Trie compression (Radix Tree / Patricia Trie):** Merge single-child nodes to reduce memory
- **Cache headers:** `Cache-Control: public, max-age=60` for CDN caching
- **Stale-while-revalidate:** Serve stale results while fetching fresh ones

**Updating the Trie (Online):**
- **Background batch:** Rebuild trie every 24 hours from query logs
- **Real-time trending:** Monitor query velocity (queries in last hour > 10× normal), add to trie with elevated priority

**Personalization (Advanced):**
- On autocomplete request, inject user's recent searches at position 1-2
- Different trie for different user segments (language, region)

**Distributed Trie:**
- **Sharding by prefix:** `a-f → Shard 1`, `g-l → Shard 2`, etc.
- Each shard holds subtrie for its prefix range
- Query goes to exactly one shard (based on prefix's first character)

**Storage Estimation:**
- 500M unique queries, avg 30 chars = 15GB raw
- Trie storage (compressed): ~5-10GB in memory
- Redis cache: most popular 10M prefixes, ~2GB RAM

---

## Q114: Design API Rate Limiter

(Same as Q110)

## Q115: Design Google Maps (Navigation)

**Answer:**

**Requirements:**
- **Functional:** Map rendering, directions/pathfinding, real-time traffic, place search, geocoding, ETA
- **Non-functional:** 99.9% availability, sub-second routing, global coverage, 100M+ daily active users

**Architecture:**

```
[Client] → [CDN (Map Tiles)] → [Load Balancer] → [API Gateway]
                                                        ↓
                          ┌────────────────────────────┴────────────┐
                   [Routing Service]                     [Geocoding Service]
                          ↓                                        ↓
                   [Graph DB (OSM)]               [Place Index (Elasticsearch)]
                          ↓
                   [Traffic Service]
                          ↓
                   [Real-time Data (Kafka)]
                          ↓
                   [Map Tile Renderer]
```

**Core Design Components:**

### 1. Map Tiles
- **Tile pyramid:** Level 0 = 1 tile (whole world), Level 20 = 2^40 tiles (~1 trillion)
- **Vector tiles (modern):** Binary format (.mvt, .pbf) — smaller, render on client. Protobuf encoding.
- **Raster tiles (legacy):** PNG/JPEG images — larger, no client rendering.
- **CDN caching:** Tiles cached at edge with max-age headers. Pre-fetch popular tiles.

### 2. Routing / Pathfinding

**Graph Structure:**
- Nodes = intersections, Edges = road segments
- Each edge has: distance, speed_limit, traversal_time, road_type, turn_restrictions

**A* Search Algorithm:**
```java
List<Node> findPath(Node start, Node end) {
    PriorityQueue<Node> open = new PriorityQueue<>(
        Comparator.comparingDouble(n -> n.g + heuristic(n, end)));
    Map<Node, Node> cameFrom = new HashMap<>();
    Map<Node, Double> gScore = new HashMap<>();
    gScore.put(start, 0.0);
    open.add(start);

    while (!open.isEmpty()) {
        Node current = open.poll();
        if (current == end) return reconstructPath(cameFrom, current);
        for (Edge edge : current.edges) {
            double tentativeG = gScore.get(current) + edge.cost;
            if (tentativeG < gScore.getOrDefault(edge.to, Double.MAX_VALUE)) {
                cameFrom.put(edge.to, current);
                gScore.put(edge.to, tentativeG);
                open.add(edge.to);
            }
        }
    }
    return null;
}
```

**Optimizations for real-time:**
- **Graph hierarchy:** Pre-compute fastest paths between highway junctions. Highway-level chaining reduces search space by 90%.
- **Contraction Hierarchies (CH):** Pre-process graph to add "shortcut" edges. Bi-directional Dijkstra. Used by OSRM, GraphHopper.
- **Partitioning:** Divide world into regions. Pre-compute distances between region borders.

### 3. Real-time Traffic
- **Data sources:** GPS probes from users (anonymized), road sensors, incident reports
- **Congestion model:** For each road segment, compute current speed as percentile of probe speeds
- **Traffic on edges:** `current_travel_time = base_time * (free_flow_speed / current_speed)`
- **Update frequency:** Every 2-5 minutes for major roads, 15 min for minor roads

### 4. Geocoding (Address → Coordinates)
- Trie-based search on normalized address string
- **Reverse geocoding** (Coordinates → Address): R-tree / QuadTree for spatial lookup
- **Place search:** Elasticsearch with geo-distance scoring

### 5. ETA Prediction
- Base time from routing (sum of segment traversal times)
- Adjustments: Traffic multiplier, turn delays, stop signs/traffic lights, historical patterns
- Model: Gradient Boosting (XGBoost/LightGBM) on features: time_of_day, day_of_week, weather, events

### 6. Offline Maps
- Download map tiles for region (vector tiles)
- Routing graph subset for offline navigation (A* on device)

**Database:**
- **OpenStreetMap data:** PostGIS (PostgreSQL with spatial extension)
- **Graph:** Memory-mapped files for routing engine
- **Traffic:** Google Bigtable / Cassandra (time-series per road segment)

**Estimation:**
- 100M daily route requests
- 1B+ waypoints (nodes in OSM)
- 20TB compressed map data globally (vector tiles)

---

## Q116: Design Uber Backend

(Same as Q104)

## Q117: Design Ticketmaster / BookMyShow

**Answer:**

**Requirements:**
- **Functional:** Browse events, select seats, book tickets, payment, reservation hold
- **Non-functional:** High consistency (no double booking), handle 10K+ concurrent bookings for popular events, high availability

**Architecture:**

```
[Client] → [CDN] → [Load Balancer] → [API Gateway]
                                            ↓
                    ┌───────────────────────┴───────────────────────┐
             [Event Service]         [Booking Service]         [Payment Service]
                    ↓                       ↓                        ↓
             [Event DB]            [Seat Lock Manager]         [Payment Gateway]
             (PostgreSQL)          (Redis w/ Lua)
                    ↓
             [Search (Elasticsearch)]
```

**Core Design: Seat Locking & Booking**

**Challenge:** Popular shows sell 10K+ tickets in seconds. Need to prevent double booking.

**Solution — Two-Phase Booking:**
```
Phase 1: Reserve  (5 min timeout)
Phase 2: Confirm   (after payment)
```

### Seat Lock Manager (Redis-based)
```java
class SeatLockManager {
    private Redis redis;
    private static final int LOCK_TIMEOUT_MS = 5 * 60 * 1000;

    boolean acquireLocks(String showId, List<String> seatIds, String userId) {
        String luaScript = """
            local showId = KEYS[1]
            local userId = ARGV[1]
            local timeout = tonumber(ARGV[2])

            for i = 3, #ARGV do
                local seatId = ARGV[i]
                local lockKey = showId .. ':seat:' .. seatId
                local lockedBy = redis.call('get', lockKey)
                if lockedBy and lockedBy ~= userId then
                    return 0  -- Already locked
                end
            end
            for i = 3, #ARGV do
                local seatId = ARGV[i]
                local lockKey = showId .. ':seat:' .. seatId
                redis.call('setex', lockKey, timeout / 1000, userId)
            end
            return 1
        """;
        return redis.eval(luaScript, showId, userId, LOCK_TIMEOUT_MS, seatIds);
    }
}
```

### Booking Flow
1. User selects seats → calls `POST /book/hold`
2. Booking Service calls Seat Lock Manager to acquire locks
3. If success → create `Booking` record with status `PENDING`, start 5-min timer
4. If fail → return specific seats already locked
5. User completes payment → `POST /book/confirm`
6. Payment processed → status changed to `CONFIRMED`, locks become permanent
7. If payment fails or timeout → release locks, cancel booking

### Queue System for High Demand
- **Request queue:** Bookings go into a queue (Kafka/Redis list)
- **Worker pool:** Process N bookings per second
- **Position in queue:** Return `{ position: 42, estimated_wait_seconds: 15 }`

### Database Schema
```sql
CREATE TABLE events (
    event_id UUID PRIMARY KEY,
    name TEXT,
    venue_id UUID,
    datetime TIMESTAMP
);

CREATE TABLE venue_seats (
    venue_id UUID,
    section TEXT,
    row TEXT,
    seat_number INT,
    seat_type TEXT,
    price DECIMAL,
    PRIMARY KEY (venue_id, section, row, seat_number)
);

CREATE TABLE show_seats (
    show_id UUID,
    section TEXT,
    row TEXT,
    seat_number INT,
    status TEXT,
    locked_by TEXT,
    locked_until TIMESTAMP,
    version INT,
    PRIMARY KEY (show_id, section, row, seat_number)
);
```

**Caching:**
- Event details: Redis cache with 1-hour TTL
- Seat map: Redis hash, invalidated on write
- Available seat count: Redis counter, updated atomically

---

## Q118: Design Hotel Booking

(Same as Q66 with added HLD considerations — essentially similar to Ticketmaster with rooms instead of seats)

## Q119: Design Distributed Messaging Queue (Kafka-like)

**Answer:**

**Requirements:**
- **Functional:** Publish messages to topics, consume with consumer groups, message persistence, ordering within partition, replay
- **Non-functional:** High throughput (millions of messages/sec), fault-tolerant, durable (persist to disk), horizontal scalability

**Architecture:**

```
[Producers] → [Broker Cluster]
                    ↓
             [Partitions (Leader/Follower)]
                    ↓
              [Kafka Topic]
                    ↓
             [Consumer Groups]
                    ↓
              [Consumers]
```

**Core Design Concepts:**

### 1. Topic and Partition
- Topic is a logical stream of messages
- Each topic is split into **partitions** (ordered, immutable sequence of messages)
- Each partition is a **commit log** — sequential writes, indexed by offset
- Messages with same key go to same partition (guarantee order within partition)
- Partition is the unit of parallelism: #consumers in a group ≤ #partitions

### 2. Brokers and Replication
- Each partition has one **leader** and multiple **followers** (ISR — In-Sync Replicas)
- Producers write to partition leader
- Followers replicate from leader
- When leader fails, a follower from ISR becomes leader
- Replication factor = 3 (tolerates 2 broker failures)

### 3. Message Persistence
- Messages written to **page cache** (OS-level) and flushed to disk
- Sequential disk I/O (append-only log) — very fast (600 MB/s)
- Each message stored with: offset, key, value, timestamp, headers
- Retained for configurable time (e.g., 7 days) or size limit

### 4. Producer
- `acks=0`: Fire-and-forget (fast, may lose data)
- `acks=1`: Leader acknowledges (leader received, may lose if leader fails before replication)
- `acks=all`/`-1`: All ISR replicas acknowledge (strongest durability)
- **Idempotent producer:** `enable.idempotence=true` prevents duplicates

### 5. Consumer
- Consumer tracks **offset** (position in partition) — stored in `__consumer_offsets` topic
- `auto.offset.reset=earliest`: Start from oldest message
- `auto.offset.reset=latest`: Start from newest (skip previous)
- **At-least-once:** Process then commit offset (may reprocess if crash between processing and commit)
- **Exactly-once:** Transactional API — produce-consume in a transaction
- **Rebalancing:** When consumer joins/leaves group, partitions reassigned

### 6. Key Optimization Features
- **Zero-copy:** Messages sent from disk to network without copying to application memory (`sendfile()` syscall)
- **Batching:** Producers batch messages (default: 16KB/10ms), consumers fetch in batches (default: 1MB/500ms)
- **Compression:** gzip, snappy, lz4, zstd — compress batches for network/disk efficiency
- **Log compaction:** Keep only latest value for each key (useful for state stores)

### 7. ZooKeeper / KRaft
- ZooKeeper manages: broker metadata, leader election, cluster membership
- **KRaft (Kafka 2.8+, production in 3.x):** Removes ZooKeeper dependency, uses Raft consensus internally

### API (Simplified)
```java
// Producer
producer.send(new ProducerRecord<>("orders", orderId, orderJson));

// Consumer
consumer.subscribe("orders");
while (true) {
    ConsumerRecords<String, String> records = consumer.poll(100);
    for (ConsumerRecord<String, String> record : records) {
        process(record.value());
    }
    consumer.commitSync();
}
```

### Estimation
- LinkedIn (origin): 1 trillion messages/day, 1 PB/day throughput
- Typical: 1M messages/sec per cluster
- Latency: P99 < 10ms (acks=1)

---

## Q120: Design Distributed Cache (Redis-like)

**Answer:**

**Requirements:**
- **Functional:** Key-value store with TTL, data structures (string, hash, list, set, sorted set), eviction policies
- **Non-functional:** < 1ms latency, 100K+ QPS per node, high availability, horizontal scaling

**Architecture:**

```
[Client] → [Client-side Partitioning/Proxy] → [Redis Cluster]
                                                    ↓
                    ┌─────────────────────────────────┴──────────────────┐
             [Master Node 1]               [Master Node 2]         [Master Node N]
                    ↓                                ↓                       ↓
             [Replica 1.1]                [Replica 2.1]           [Replica N.1]
             [Replica 1.2]                [Replica 2.2]           [Replica N.2]
```

**Core Design:**

### 1. Data Sharding (Redis Cluster)
- 16384 hash slots in total
- Key → CRC16(key) % 16384 → slot → node
- Nodes are assigned slot ranges (e.g., Node1: 0-5460, Node2: 5461-10922, Node3: 10923-16383)
- Adding/removing nodes: Slot migration between nodes (online rebalancing)

### 2. Replication & High Availability
- Each master has 1+ replicas (async replication)
- Replica sync: Full RDB dump + incremental command propagation
- **Sentinel** (standalone mode): Monitors masters, auto-failover if master is down
- **Cluster mode:** Automatic failover, slot migration

### 3. Persistence Options
- **RDB (snapshot):** Periodic point-in-time snapshots. Fast restart. May lose data between snapshots.
- **AOF (Append-Only File):** Every write command logged. Durable (fsync every sec or every write). Slower restart.
- **Hybrid (Redis 7+):** RDB + incremental AOF for fast restart + durability.

### 4. Eviction Policies (Q85)
| Policy | Description |
|--------|-------------|
| `noeviction` | Returns error when memory limit reached |
| `allkeys-lru` | Evict least recently used keys |
| `allkeys-lfu` | Evict least frequently used keys |
| `volatile-lru` | Evict LRU among keys with TTL set |
| `volatile-ttl` | Evict key with shortest TTL |
| `allkeys-random` | Evict random key |

### 5. Network Model
- **Single-threaded** event loop (epoll/kqueue)
- All commands executed sequentially (no race conditions within one instance)
- **Benchmark:** 100K-1M QPS per node (depending on command complexity)

### 6. Optimizations
- **Pipelining:** Send multiple commands without waiting for responses (batch)
- **Connection pooling:** Reuse TCP connections
- **Local cache + Redis (Multi-layer):** Caffeine/Cache2k on client side reduces Redis load
- **Read from replicas:** Scale reads (risk of stale data due to async replication)

### 7. Distributed Cache Considerations
- **Hotkey problem:** A single key (e.g., trending video) gets 100K QPS → overwhelms one node
  - Solution: Local cache for hot keys, replicate key to multiple nodes (scatter-gather)
- **Thundering herd:** Many clients try to compute same missing cache entry simultaneously
  - Solution: Lock (SET NX) around cache recomputation, first writer does the work
- **Cache breakdown:** Sudden failure of cache node → DB overwhelmed
  - Solution: Connection pools, circuit breakers, local fallback

### Estimation
- 10-node cluster: 1M+ QPS, sub-millisecond latency
- Memory: 64GB per node → 640GB total cache

---

## Q121: Design Distributed Key-Value Store

**Answer:**

**Requirements:**
- **Functional:** Get/put/delete by key, range queries, ACID transactions, TTL
- **Non-functional:** High availability, partition tolerance, scalability, low latency (single-digit ms for p99)

**Architecture (DynamoDB-like):**

```
[Client] → [Request Router] → [Coordinator Nodes]
                                    ↓
                          [Partition Layer (Consistent Hashing)]
                                    ↓
                    ┌───────────────────┴───────────────────┐
              [Storage Node 1]                    [Storage Node N]
                    ↓                                       ↓
              [RocksDB/LSM]                          [RocksDB/LSM]
                    ↓                                       ↓
              [Replication]                          [Replication]
```

**Core Design:**

### 1. Partitioning (Consistent Hashing)
- Key → hash → virtual node on consistent hash ring
- Each physical node handles multiple virtual nodes
- **Advantage:** Adding/removing nodes requires only moving data for immediate neighbors

### 2. Replication — Quorum-based
```
R = read quorum size
W = write quorum size
N = replication factor

Strong consistency: W + R > N
Example: N=3, W=2, R=2 → guarantees at least 1 overlapping node
```

- **Tunable consistency:** Per-request `get(key, consistency=QUORUM)` or `get(key, consistency=ONE)`
- **Read repair:** On read, if a replica has stale data, update it
- **Hinted handoff:** If a replica is down, another node temporarily stores the write, delivers when replica recovers
- **Merkle trees:** Compare replicas for anti-entropy (detect inconsistencies), fetch missing data

### 3. Storage Engine (LSM Tree — LevelDB/RocksDB)
```
MemTable (in-memory sorted tree)
    ↓ (flush when full)
SSTable (Sorted String Table) — immutable, sorted key-value pairs
    ↓
Compaction: merge SSTables, remove tombstones, keep latest values
```

- **Write:** Append to WAL (write-ahead log) → insert into MemTable → batch flush to SSTable
- **Read:** Check MemTable → Bloom filter per SSTable → binary search in SSTable

### 4. Membership & Failure Detection (Gossip Protocol)
- Each node maintains cluster membership list
- Gossip: Periodically send membership info to a random node
- Every node knows about every other node within seconds
- Failure detection: Suspect node if missed N heartbeats, confirm with others before marking dead

### Read Path
```
Client request → Coordinator → All replicas of partition contacted
Wait for R responses → Return latest version
If inconsistencies → Read repair background task
```

### Write Path
```
Client request → Coordinator → Write to WAL → Insert MemTable
Wait for W acknowledgements → Return success
Background: flush MemTable to SSTable → compaction
```

---

## Q122: Design Distributed File System

**Answer:**

**Requirements:**
- **Functional:** Store files, directory hierarchy, read/write by path, append-only writes, replication
- **Non-functional:** Fault tolerance, high throughput (hundreds of GB/s), petabyte scale

**Architecture (Google GFS / HDFS-like):**

```
[Client] ←→ [Master/NameNode]
                ↓
         [Metadata Store (RAM + Edit Log)]
                ↓
    ┌───────────┴───────────┐
[Chunk Server 1]   [Chunk Server N]
    ↓                       ↓
[Local Disk]          [Local Disk]
```

**Core Design:**

### 1. Master (NameNode)
- Single coordinator (but with Standby for HA)
- Stores **metadata only**: file → list of chunks, chunk → list of chunk servers
- Everything in memory + edit log (write-ahead log on disk)
- **Lease management:** Coordinates writes to avoid conflicts

### 2. Chunks
- Files split into **fixed-size chunks** (e.g., 64MB for GFS, 128MB for HDFS)
- Each chunk is stored on 3 chunk servers (replication factor = 3)
- Each chunk has a unique **chunk handle** (64-bit ID)

### 3. Read
```
1. Client asks Master: "read file X, offset Y"
2. Master returns: chunk handle, list of chunk servers (e.g., CS1, CS2, CS3)
3. Client selects nearest chunk server
4. Client sends: read(chunk_handle, byte_range) to chunk server
5. Chunk server returns data
```

### 4. Write — Append Operation
```
1. Client asks Master for chunk lease
2. Master grants lease to one chunk server (primary)
3. Client sends data to all chunk servers (pipeline: CS1 → CS2 → CS3)
4. All acknowledge receipt
5. Client sends write command to primary
6. Primary orders writes, assigns sequence numbers
7. Primary writes to local chunk + sends to secondaries
8. All acknowledge → success
```

### 5. Fault Tolerance
- **Master HA:** Active/Standby with shared edit log (Quorum Journal Manager or ZooKeeper)
- **Chunk replication:** 3 replicas on different racks
- **Heartbeat:** Chunk servers send heartbeats to master every 3 seconds
- **Re-replication:** If replica count drops below target, master schedules new copies

### 6. Data Integrity
- **Checksums per 64KB block** within each chunk
- On read, chunk server verifies checksum
- On mismatch, report to master, read from another replica

### 7. Snapshots
- Copy-on-write: When file is snapshotted, master creates new metadata entry pointing to same chunks

### Performance Characteristics
| Metric | Value |
|--------|-------|
| Chunk size | 128 MB |
| Read throughput | ~100 MB/s per chunk server |
| Aggregate read | 10k disks × 100 MB/s = 1 TB/s |
| Write throughput | ~50 MB/s per chunk server |
| Metadata | 10M files × 640 bytes = 6.4 GB RAM |

---

## Q123: Design Distributed Job Scheduler

**Answer:**

**Requirements:**
- **Functional:** Schedule jobs (one-time, recurring CRON), trigger based on events, dependency resolution, retry, monitoring
- **Non-functional:** High availability, exactly-once execution, handle millions of jobs, fault-tolerant

**Architecture:**

```
[REST API] → [Scheduler Service]
                    ↓
             [Job Store (PostgreSQL)]
                    ↓
             [Dispatcher Workers]
                    ↓
     ┌──────────────┴──────────────┐
[Task Executors]            [Trigger Service]
                                    ↓
                             [Event Bus (Kafka)]
```

**Core Design:**

### 1. Data Model
```sql
CREATE TABLE jobs (
    job_id UUID PRIMARY KEY,
    name TEXT,
    type TEXT,  -- ONETIME, CRON, EVENT
    schedule TEXT,  -- CRON expression or null
    status TEXT,  -- ACTIVE, PAUSED, COMPLETED
    handler TEXT,
    payload JSONB,
    max_retries INT DEFAULT 3,
    retry_delay_seconds INT DEFAULT 60,
    timeout_seconds INT DEFAULT 300,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

CREATE TABLE job_executions (
    execution_id UUID PRIMARY KEY,
    job_id UUID REFERENCES jobs,
    status TEXT,  -- SCHEDULED, RUNNING, SUCCEEDED, FAILED
    scheduled_at TIMESTAMP,
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    result JSONB,
    error TEXT,
    worker_id TEXT
);
```

### 2. Scheduler — Leader Election
- Multiple scheduler instances, only one leader (via ZooKeeper / database lock)
- Leader scans for jobs ready to execute:
```sql
SELECT * FROM job_executions
WHERE status = 'SCHEDULED'
  AND scheduled_at <= NOW()
  AND (locked_by IS NULL OR locked_at < NOW() - INTERVAL '5 minutes')
LIMIT 100;
```

### 3. Partitioning
- Jobs partitioned by `job_id % N` (consistent hashing for resizing)
- Each scheduler instance responsible for its partition

### 4. CRON Scheduling
- CRON expressions parsed to `next_run_at`
- Recurring jobs create `job_execution` records when triggered

### 5. Retry & Backoff
```
Failed → retry_delay → SCHEDULED
After max_retries → status = FAILED (permanent)
```
- Retry with exponential backoff: `delay = base * 2^attempt + random_jitter`
- Dead letter queue: Jobs that failed permanently

### 6. Exactly-Once Execution
- Idempotent job handlers (use execution_id as idempotency key)
- Database-backed locking prevents double-dispatch
- Atomic status transition: `UPDATE ... WHERE status = 'SCHEDULED'`

---

## Q124: Design Real-time Gaming Leaderboard

**Answer:**

**Requirements:**
- **Functional:** Submit score, get leaderboard (top 100), get user rank, real-time updates, tie-breaking by timestamp
- **Non-functional:** < 10ms read/write, handle 100K+ writes/sec, global scale

**Architecture:**

```
[Game Client] → [Game Server] → [Score Ingestion API]
                                       ↓
                                [Kafka / Queue]
                                       ↓
                                [Leaderboard Worker]
                                       ↓
                            ┌──────────┴──────────┐
                      [Redis Sorted Set]    [Database (for persistence)]
```

**Core Design: Leaderboard with Redis Sorted Sets**

```java
class LeaderboardService {
    private static final String LEADERBOARD_KEY = "game:leaderboard";

    void submitScore(String userId, int score) {
        // For tie-breaking by time: score = actualScore * 10^12 + (MAX_TIMESTAMP - now)
        long compositeScore = ((long) score << 20) | (MAX_TIMESTAMP - System.currentTimeMillis());
        redis.zadd(LEADERBOARD_KEY, compositeScore, userId);
    }

    List<LeaderboardEntry> getTopN(int n) {
        return redis.zrevrangeWithScores(LEADERBOARD_KEY, 0, n - 1)
            .stream()
            .map(t -> new LeaderboardEntry(t.getValue(), t.getScore()))
            .collect(toList());
    }

    long getUserRank(String userId) {
        Long rank = redis.zrevrank(LEADERBOARD_KEY, userId);
        return rank == null ? -1 : rank + 1;
    }
}
```

### Tie-breaking Strategy
- **Primary key:** Score (higher is better)
- **Secondary key:** Timestamp (earlier submission wins ties)
- Encoding: `composite_score = (score << 20) | (MAX_TIMESTAMP - timestamp)`

### Daily/Weekly/Monthly Leaderboards
```java
String getLeaderboardKey(String period) {
    String suffix = switch (period) {
        case "daily" -> LocalDate.now().toString();
        case "weekly" -> LocalDate.now().with(DayOfWeek.MONDAY).toString();
        case "monthly" -> YearMonth.now().toString();
        case "alltime" -> "alltime";
    };
    return "leaderboard:" + suffix;
}
```

### Persistence & Recovery
- Redis sorted set is primary data store (high performance)
- **Snapshot to DB** periodically (every minute): `ZRANGE + ZSCORES` → batch write to PostgreSQL
- On Redis restart, restore from DB snapshot

### Scaling Strategy
| Approach | Description | Pros | Cons |
|----------|-------------|------|------|
| Single Redis | All scores in one sorted set | Simple, atomic | Memory bound |
| Redis Cluster | Shard by user_id hash | Scalable | Cross-shard queries expensive |
| Tiered | Top 1000 (exact) + percentile buckets | Reduces memory | Complex |

### Handling High Write Volume (100K+/sec)
1. **Batched writes:** Game servers buffer scores, batch submit every 100ms
2. **Aggregation window:** Within a 1-second window, only keep highest score per user
3. **Pipelining:** Redis pipeline for batch ZADD operations

---

## Q125: Design Recommendation System

**Answer:**

**Requirements:**
- **Functional:** Recommend items (products, videos, posts) to users based on history, personalization, real-time
- **Non-functional:** < 100ms latency, handle 10M+ users, update recommendations as user interacts

**Architecture:**

```
[User Activity Logs] → [Kafka/Event Bus]
                             ↓
                   [Offline Pipeline (Spark)]
                             ↓
              ┌────────────────┴────────────────┐
         [Candidate Generation]          [Feature Engineering]
              ↓                                ↓
         [Candidate Pool]               [Feature Store]
              ↓                                ↓
         [Ranking Model]                      ↓
              ↓                                ↓
         [Re-ranking]                         ↓
              ↓                                ↓
         [Recommendation API] ←───────────────┘
              ↓
         [Cache (Redis)]
```

**Core Approach: Two-stage Recommendation**

### Stage 1: Candidate Generation (Recall)
Goal: From millions of items, narrow to hundreds of candidates.

**Strategies:**
1. **Collaborative Filtering:**
   - User-based: Find similar users, recommend what they liked
   - Item-based: "Users who liked this also liked..."
   - Matrix Factorization (SVD, ALS): Decompose user-item interaction matrix into latent factors

2. **Content-based:**
   - Extract item features (category, tags, embedding)
   - Recommend items similar to what user liked before
   - Cosine similarity between item vectors

3. **Popularity/Context:**
   - Trending in user's region
   - New releases (time-decayed popularity)

4. **Embedding-based (Deep Learning):**
   - Two-tower model: User tower + Item tower
   - Learn embeddings in same vector space
   - ANN (Approximate Nearest Neighbor) search for fast retrieval (FAISS, ScaNN, HNSW)

### Stage 2: Ranking
Goal: Score hundreds of candidates, pick top-N (usually 10-50).

**Model:**
- **Features:** User features (history, demographics), Item features (category, popularity), Context features (time, device), Cross features (user×item interaction count)
- **Model types:**
  - Logistic Regression (simple, interpretable)
  - Gradient Boosted Trees (XGBoost, LightGBM)
  - Deep Neural Network (Wide & Deep, DCN)

### Stage 3: Re-ranking
- **Diversity:** MMR (Maximum Marginal Relevance): `score = λ * relevance - (1-λ) * max_similarity_to_already_selected`
- **Business rules:** Remove already-purchased items, enforce freshness, promote sponsored content

### Online Serving
```java
class RecommendationService {
    List<Recommendation> getRecommendations(User user, int n) {
        String cacheKey = "recs:" + user.id;
        List<Recommendation> cached = cache.get(cacheKey);
        if (cached != null) return cached;

        List<Item> candidates = candidateGen.getCandidates(user);
        List<ScoredItem> scored = rankingModel.score(user, candidates);
        List<Recommendation> recs = reRank(scored, n);

        cache.put(cacheKey, recs, Duration.ofMinutes(5));
        return recs;
    }
}
```

---

## Q126: Design Chat System (WhatsApp)

(Same as Q102)

## Q127: Design Collaborative Document Editing (Google Docs)

**Answer:**

**Requirements:**
- **Functional:** Real-time multi-user editing, cursor presence, comments, version history, offline editing
- **Non-functional:** < 200ms latency for local edits, conflict-free collaboration, reliable

**Architecture:**

```
[User A] ←→ WebSocket → [Load Balancer] → [Document Service]
[User B] ←→ WebSocket                        ↓
                                         [CRDT/Automerge/OT Engine]
                                                ↓
                                         [Document Store (PostgreSQL)]
                                                ↓
                                         [Snapshot Store (S3)]
```

**Core Design: Conflict Resolution**

### Approach 1: Operational Transformation (OT)
**Used by: Google Docs, Etherpad**

**Concept:** Each edit is an **operation** (e.g., `insert(pos, chars)`, `delete(start, end)`). When operations from different users conflict, transform one operation against the other.

**Example:**
- User A: `insert(3, "AB")` ("abc" → "abABc")
- User B at same time: `insert(3, "XY")` ("abc" → "abXYc")
- Server receives A first: state = "abABc"
- Server receives B: transform B's operation against A's operation
- Transformed B: `insert(5, "XY")` (because A added 2 chars at position 3)
- Result: "abABXYc" (consistent for both)

### Approach 2: CRDT (Conflict-free Replicated Data Types)
**Used by: Automerge, Yjs, Liveblocks**

**Concept:** Each character has a unique ID. Edits are idempotent and commutative — no transformation needed.

**Why CRDT is winning:**
- No central server required for conflict resolution
- Works offline (merge when online)
- Easier to reason about than OT

### Cursor Presence
- Each user broadcasts their cursor position (character offset)
- Broadcast at most 10 times/second
- Color-coded cursors per user

### Document Storage
- **Snapshot + Operations log:**
  - Store full document snapshot periodically (every 50 operations or 5 minutes)
  - Store all operations since last snapshot
  - On load: apply snapshot + replay operations since snapshot

---

## Q128: Design CDN

**Answer:**

**Requirements:**
- **Functional:** Cache static/dynamic content at edge locations, reduce origin load, fast content delivery
- **Non-functional:** Low latency (P99 < 50ms for cache hit), high availability (99.99%), global coverage

**Architecture:**

```
[Origin Server] ←→ [CDN Control Plane]
                        ↓
[Edge Server PoP 1]  [Edge Server PoP 2]  ... [Edge Server PoP N]
      ↓                       ↓                      ↓
[End Users]             [End Users]             [End Users]
```

**Core Design:**

### 1. Point of Presence (PoP)
- A PoP is a data center with caching servers in a geographic region
- Major CDNs (Akamai, CloudFront, Cloudflare) have 100-400+ PoPs

### 2. Caching Strategy
- **Forward proxy:** CDN requests content from origin on behalf of client
- **Reverse proxy:** Origin pushes content to CDN proactively

**Cache layers:**
1. **L1 (Edge cache):** In PoP. Fast (in-RAM or SSD). Small capacity.
2. **L2 (Regional cache):** Larger, in SSD/HDD.
3. **Origin:** Full dataset.

**Cache decision:**
- `Cache-Control: public, max-age=86400` → cache for 1 day
- `Cache-Control: private` → don't cache
- `Cache-Control: no-store` → bypass

### 3. Cache Eviction
- **LRU, LFU, Hybrid, TTL-based**
- **Stale-while-revalidate:** Serve stale content while fetching fresh in background

### 4. Content Routing
- **DNS-based:** GeoDNS returns IP of nearest PoP
- **Anycast:** Same IP from all PoPs. BGP routes user to nearest PoP

### 5. Dynamic Content Acceleration
- **TCP optimizations:** Fast connection setup, keep-alive, multiplexing
- **Route optimization:** CDN measures latency between PoPs, chooses fastest path to origin

### 6. Invalidation
- **Explicit:** `POST /purge { paths: ["/images/*"] }`
- **TTL-based:** Automatic expiry
- **Versioned URLs:** `/static/js/app.v2.js` → never needs invalidation

### Performance Impact
| Metric | Without CDN | With CDN |
|--------|-------------|----------|
| Latency (US→Tokyo) | 150ms | 10ms |
| Cache hit ratio | N/A | 80-95% |
| Origin load reduction | N/A | 10-20× |

---

## Q129: Design Payment System

**Answer:**

**Requirements:**
- **Functional:** Process payments (cards, wallets, UPI), refunds, idempotency, reconciliation, fraud detection
- **Non-functional:** > 99.99% uptime, strong consistency for balance, 2-phase commit across services

**Architecture:**

```
[Client] → [Payment API] → [Payment Service]
                                ↓
                          [Fraud Detection]
                                ↓
                          [Payment Orchestrator]
                                ↓
            ┌───────────────────┼───────────────────┐
     [Card Gateway]       [Wallet Service]     [UPI Service]
```

**Core Flow — Payment:**
```
1. Client → POST /payments { order_id, amount, source }
2. Payment Service creates Payment with status PENDING
3. Fraud Check (async): ML model scores transaction
4. If fraud score < threshold → proceed
5. Payment Orchestrator: Authorization (reserve amount on card)
6. Capture: Debit the card, finalize payment
   status = CAPTURED
7. Post-payment: Update order status, send receipt, update balances
```

### Idempotency
- Every payment request has `idempotency_key` (e.g., `order_id + user_id`)
- Payment Service checks if key already processed → return existing result

### Double Payment Prevention
- **Two-phase reservation:** Authorize (lock) → Capture (charge)
- **Idempotency key** prevents duplicate submissions
- **Atomic operations:** `UPDATE balance SET amount = amount - ? WHERE user_id = ? AND amount >= ?`

### Payment States
```
PENDING → AUTHORIZED → CAPTURED → SETTLED
                ↓           ↓
           DECLINED     FAILED
                ↓
           REFUNDED / PARTIALLY_REFUNDED
```

### Security
- **PCI DSS compliance:** Never store raw card numbers (use tokenization)
- **Tokenization:** Replace card number with token
- **3D Secure (SCA):** Redirect to bank for authentication
- **Encryption:** TLS in transit, AES-256 at rest

### Accounting (Double-Entry Ledger)
```sql
CREATE TABLE ledger_entries (
    entry_id UUID PRIMARY KEY,
    account_id TEXT,  -- 'revenue', 'merchant_123', 'gateway_fees'
    amount BIGINT,    -- in cents
    type TEXT,        -- DEBIT / CREDIT
    payment_id UUID,
    created_at TIMESTAMP
);
```

---

## Q130: Design Content Delivery Network

(Same as Q128)

## Q131–Q150: Additional HLD Topics

### Q131: Design a Distributed Queue (SQS-like)

**Answer:**
- Queues are sharded across storage nodes (each shard = ordered log)
- **Visibility timeout:** Message is invisible for N seconds after read; if not deleted, reappears
- **Dead letter queue:** Messages that fail processing N times go to DLQ
- **Throughput:** Scale by adding shards

### Q132: Design a Webhook System

**Answer:**
- Register webhook URL per event type
- On event → HTTP POST to URL with HMAC-signed payload
- Retry with exponential backoff: 1min, 5min, 30min, 2hr, 6hr, 12hr, 24hr
- Dead letter after max retries
- Rate limit per target (e.g., 100 req/s)

### Q133: Design a Feature Flag System

**Answer:**
- Admin creates flag with targeting rules (user segment, percentage rollout)
- SDK caches flags locally (30s refresh)
- Evaluation: `isEnabled(flag, userContext)` checks rules
- CDN for flag config distribution
- Kill switch: Every 5s poll for critical flags

### Q134: Design a Log Aggregation System

**Answer:**
- Logs collected via Filebeat/Fluentd → Kafka → Logstash → Elasticsearch → Kibana
- Alternative: Vector → Kafka → ClickHouse → Grafana
- Hot tier (SSD, 7 days), Warm (HDD, 30 days), Cold (S3, 1 year)
- Schema-on-read for semi-structured logs

### Q135: Design a Distributed Configuration System

**Answer:**
- Centralized config store (etcd, ZooKeeper)
- Watchers: Clients get notified on config changes
- Versioning, rollback, hierarchical keys
- `db/host`, `db/port`, `cache/ttl`

### Q136: Design a Search Engine (Elasticsearch-like)

**Answer:**
- **Inverted index:** `term → [docId, frequency, position]`
- **Scoring:** BM25 algorithm
- **Sharding:** Index split into shards, query scatters to all shards, results merge
- **Near real-time:** Writes are visible after refresh interval (1s default)

### Q137: Design a Video Conferencing System (Zoom-like)

**Answer:**
- **SFU (Selective Forwarding Unit):** Server forwards selected video streams to each participant
- Client sends 1 stream, receives N-1 streams
- **Simulcast:** Send 3 resolution streams, SFU selects appropriate one
- WebRTC for transport, ICE for NAT traversal, DTLS-SRTP for encryption
- Adaptive bitrate based on network conditions

### Q138: Design a Time-Series Database

**Answer:**
- **Compression:** Delta-of-delta encoding for timestamps, XOR for floats (Gorilla compression)
- **Downsampling:** Pre-compute aggregates at 1min → 1hour → 1day granularities
- **Retention:** Drop data older than N days
- **Index:** Inverted index on tags/labels
- Examples: InfluxDB, Prometheus, TimescaleDB

### Q139: Design a Graph Database (Neo4j-like)

**Answer:**
- Nodes and Edges with properties
- **Index-free adjacency:** Each node stores pointers to its edges
- Traversal: Follow edges from node to connected nodes
- Query: `MATCH (u:User)-[:FOLLOWS]->(f) RETURN f`

### Q140: Design a Distributed Locking Service

**Answer:**
- **Redis Redlock:** `SET key value NX PX 30000`
- **ZooKeeper:** Ephemeral sequential znodes, lowest sequence holds lock
- **etcd:** Lease-based locking
- Redlock caution: Asynchronous replication can cause split-brain

### Q141: Design a Distributed Tracing System (Jaeger/Zipkin)

**Answer:**
- **Trace:** End-to-end request identified by `trace_id`
- **Span:** Unit of work, has `span_id`, `parent_span_id`, `operation_name`, duration, tags
- **Propagation:** `trace_id` and `span_id` in HTTP headers (`X-B3-TraceId`)
- **Sampling:** Head-based (1% of requests) or tail-based (all slow requests)

### Q142: Design a Data Pipeline / ETL System

**Answer:**
- **CDC (Change Data Capture):** Debezium captures DB binlog changes → Kafka
- **Stream processing:** Flink/Spark for transformations
- **Batch (ELT):** Load raw data → transform in warehouse (dbt)
- **DLQ:** Failed records for manual reprocessing

### Q143: Design a Service Mesh (Istio-like)

**Answer:**
- **Sidecar proxy (Envoy):** Intercepts all service-to-service traffic
- **Control Plane:** Manages proxy config, certificates (mTLS), traffic routing
- **Benefits:** Retry, circuit breaking, load balancing, tracing, mTLS — all without code changes
- Traffic splitting for canary deployments

### Q144: Design a Serverless Platform (AWS Lambda-like)

**Answer:**
- Function code stored in S3, containers created on invocation
- **Cold start:** 100-1000ms for first invocation (download code → create container → run)
- **Warm start:** Sub-ms overhead (reuse existing container)
- Scaling: Create new containers up to account concurrency limit
- **Provisioned concurrency:** Keep N containers warm

### Q145: Design a Cloud Storage System (S3-like)

**Answer:**
- Flat namespace: `bucket/key` addressing
- Key → partition via hash
- **Strong consistency (S3 since 2020):** Read-after-write via metadata quorum
- **Erasure coding:** 10+4 scheme, tolerates 4 failures with 1.4× overhead (vs 3× replication)
- Multi-part upload for large files

### Q146: Design a BI / Analytics Dashboard

**Answer:**
- OLAP cube: Pre-compute aggregates by dimensions (time, user, product, region)
- Columnar storage for efficient compression and scan
- Real-time: Kafka → Flink → ClickHouse
- Historical: Batch ETL → Data warehouse

### Q147: Design a Distributed Unique ID Generator

(Same as Q98 — Snowflake)

### Q148: Design a Rate Limiting Proxy (API Gateway Rate Limiter)

(Same as Q110)

### Q149: Design a Subscription Management System

**Answer:**
- Plans with billing cycles (monthly/yearly)
- Trial periods, upgrades/downgrades with proration
- **Dunning:** Retry failed payments, escalate, suspend
- Invoicing, payment history

### Q150: Design a Shipping / Logistics System

**Answer:**
- Warehouse inventory management
- Pick-pack-ship workflow
- Carrier integration (FedEx/UPS) via APIs
- Real-time tracking updates
- Rate calculation and address validation

---

## Q151–Q250: Quick HLD Topics

**Q151: Design a Payment Wallet** — Prepaid/postpaid balance per user. Transaction history. Add money (CC/DC/NEFT). Send money (P2P). Ledger entries (double-entry). Fraud detection. Idempotency.

**Q152: Design a Food Delivery System (Zomato/Swiggy)** — Restaurant catalog, menu search, cart/checkout, order tracking, real-time delivery partner location, ETA prediction. Similar to Uber Eats.

**Q153: Design a Social Network (Facebook)** — User profiles, friend graph (bidirectional), feed (see Q103), messenger (see Q102), groups, pages, notifications.

**Q154: Design a Blogging Platform (Medium)** — Write/read articles, rich text editor, tags, claps (like), follow, recommendation engine.

**Q155: Design a Video Streaming Platform (Twitch)** — Live streaming: RTMP ingest, transcoding, HLS packaging, chat (WebSocket), notifications. VOD: record streams, catalog.

**Q156: Design a Music Streaming Service (Spotify)** — Catalog (millions of songs), search, playlists, audio streaming (adaptive bitrate for music — Opus codec), recommendations, offline downloads.

**Q157: Design a Classifieds Platform (Craigslist)** — Post ads, search with filters, categories, images, contact via email relay, anti-spam, moderation.

**Q158: Design a Payment Gateway (Stripe)** — Merchants → Payments → Card networks. Tokenization, webhooks, dashboard, fraud rules, subscription management, dispute handling.

**Q159: Design a Survey/Forms Platform (Typeform)** — Form builder (drag-drop), responses storage, analytics, conditional logic, embeddable forms, webhook on submission.

**Q160: Design a Calendar / Scheduling System (Calendly)** — Users set availability → share booking link → invitee picks slot → event created. Calendar integration (Google Calendar, Outlook). Reminders (email, SMS). Timezone handling.

**Q161: Design an Email Delivery Service (SendGrid)** — SMTP relay, email API, template engine, bounce handling, spam complaints, analytics (open, click), suppression list.

**Q162: Design a Push Notification System** — Device registration, FCM/APNs integration, delivery tracking, batching, throttling.

**Q163: Design an A/B Testing Platform** — Create experiment (variants, traffic split). SDK assigns user to variant. Metrics collection. Statistical analysis (p-value, confidence intervals). Decision: rollout winning variant.

**Q164: Design a User Authentication System (Auth0-like)** — OAuth 2.0 / OIDC, SSO (SAML/OIDC), MFA, passwordless, user directory, brute force protection, session management.

**Q165: Design a Document Management System** — Upload, versioning, folder hierarchy, full-text search, permissions (view/edit/comment), audit trail, document preview.

**Q166: Design a Coupon / Promo Engine** — Create coupon (code, discount type, valid dates, usage limits, conditions). Validate coupon at checkout. Track usage. Prevent abuse.

**Q167: Design a Kanban / Project Management Board (Jira-like)** — Boards, columns, cards, drag-drop, real-time updates (WebSocket), assignees, labels, sprint planning.

**Q168: Design a Notification Preferences System** — Users set which notifications they want (email/SMS/push), quiet hours, digest frequency. Preference DB per user.

**Q169: Design a Real-time Chat Support System (Intercom-like)** — Customer ↔ Agent chat. Routing: assign to available agent. Canned responses. Chat history. Co-browsing.

**Q170: Design a Review / Rating System** — Users rate items (1-5 stars), write reviews. Aggregated rating. Sort by helpfulness. Verified purchase badge. Abuse detection.

**Q171: Design a Inventory Reservation System** — During checkout, reserve inventory for N minutes. Release on timeout. Prevent overselling.

**Q172: Design a Credit Scoring System** — Compute credit score based on transaction history, repayment behavior, demographics. ML model + rule engine.

**Q173: Design a Fraud Detection Pipeline** — Real-time scoring (ML model on transaction features). Rule engine (velocity checks, geolocation anomalies). Batch backtesting.

**Q174: Design a Referral System** — Generate referral link/code. Track sign-ups from referrals. Reward both parties after criteria met. Prevent abuse (fraud detection).

**Q175: Design a Multi-tenant SaaS System** — Tenant isolation (DB per tenant, schema per tenant, or shared). Tenant provisioning. Billing per tenant. Custom domains.

**Q176: Design a Rate-limiting Proxy (Envoy-like)** — L7 proxy intercepts requests → rate limiter → forward/block. Configurable rules per route/header. Redis backend.

**Q177: Design a Search Suggestions System** — See Q113 (Autocomplete). Also include: trending searches, recent searches, personalization.

**Q178: Design a Content Moderation System** — Automated (ML: image NSFW detection, text toxicity) + human reviewers. Queue for human review. Appeal process.

**Q179: Design a Metrics Collection System (Prometheus-like)** — Pull-based: scrape metrics from targets at intervals. Time-series DB. PromQL query language. Alerting rules.

**Q180: Design an API Gateway (Kong/AWS API Gateway)** — Single entry point for microservices. Routing, authentication, rate limiting, caching, request/response transformation, monitoring.

**Q181: Design a Code Review System (GitHub-like)** — Pull request workflow: diff view, inline comments, review approval, merge checks (CI status), merge strategies.

**Q182: Design a Container Orchestration System (Kubernetes-light)** — Pod scheduling, service discovery, health checks, rolling updates, secrets management, persistent volumes.

**Q183: Design a CI/CD Pipeline** — Source → Build → Test → Deploy. Artifact repository. Pipeline as code. Parallel stages. Rollback capability.

**Q184: Design a Backup and Restore System** — Snapshot DB/files → compress → encrypt → store in S3/Glacier. Incremental backups. Point-in-time recovery. Retention policy.

**Q185: Design a Data Warehouse (Snowflake-like)** — Columnar storage, virtual warehouses (compute clusters), separation of storage and compute, zero-copy cloning, time travel.

**Q186: Design a Stream Processing System (Flink-like)** — Event time processing, watermarks, state management, checkpoints for fault tolerance, exactly-once semantics.

**Q187: Design a Geospatial Query System** — QuadTree, GeoHash, R-tree. Find nearby points: compute hash → query prefix match. Used by Uber, Maps.

**Q188: Design a Shopping Feed Personalization** — Ranking: boost items from favorite categories, recently viewed, similar to past purchases. Real-time signal: add to cart.

**Q189: Design a Cache Warming System** — Pre-populate cache before expected traffic (e.g., before sale event). Identify popular content from logs. Push to CDN/Redis.

**Q190: Design a Dark Launch / Canary Release System** — Route small % of traffic to new version. Monitor errors/latency. Gradual increase. Auto-rollback on degradation.

**Q191: Design a Customer Support Ticketing System** — Create ticket (email/chat/phone). Assign to agent. Priority queue. SLA tracking. Knowledge base integration.

**Q192: Design an Inventory Forecasting System** — Predict future demand based on historical sales, seasonality, trends. ML model (ARIMA, Prophet, LSTM).

**Q193: Design a Dynamic Pricing Engine** — Adjust prices based on demand/supply (surge pricing), competitor prices, user segments, time. ML optimization.

**Q194: Design a Multi-currency Wallet** — Balances in multiple currencies. Currency conversion (FX rates). Exchange with spread. Settlement.

**Q195: Design a Product Recommendation Carousel** — See Q125. For each page view, recommend N items. Real-time: update based on current page context.

**Q196: Design a Reverse Image Search System** — Extract image embedding (CNN). ANN index (FAISS) for similarity search. Used for: find similar products, plagiarized images.

**Q197: Design a Real-time Anomaly Detection System** — Streaming metrics → detect outliers (statistical: 3σ, MAD; ML: Isolation Forest). Alert on anomaly.

**Q198: Design a Customer Data Platform (CDP)** — Unify customer data from multiple sources. Identity resolution (same user across devices). Profile store. Segmentation.

**Q199: Design a Edge Computing Platform** — Run code at edge locations (CDN). Lambda@Edge, Cloudflare Workers. Low-latency processing close to users.

**Q200: Design a Voting / Polling System with Results** — Create poll, real-time result updates (WebSocket), prevent duplicate voting (user auth + rate limit), result accuracy.

**Q201–Q250: High-Level Design Quick References**

**Q201: Design a Hotel Booking System (High-Level)** — Search by location/dates, room inventory (sharded by hotel_id), pricing engine, reservation with hold timeout, payment, cancellation policy.

**Q202: Design a Flight Booking System** — Search flights (join routes × dates), fare classes (bucket allocation), PNR generation, seat selection, ancillary services.

**Q203: Design a Learning Management System** — Courses, lessons, progress tracking, quizzes, certificates. Video streaming (see Q105). Discussion forums.

**Q204: Design a Gaming Matchmaking System** — Players → ranked queue → match (similar skill). ELO/Glicko rating system. Party support. Region-based.

**Q205: Design a Real-time Translation System** — Audio/Text input → ML translation model → output in target language. WebSocket for real-time streaming.

**Q206: Design a Face Recognition System** — Detect face → extract embedding → match against known faces (ANN index). Liveness detection. Use cases: authentication, tagging.

**Q207: Design a Voice Assistant (Alexa-like)** — Wake word detection → ASR (speech-to-text) → NLU (intent parsing) → Action execution → TTS (text-to-speech).

**Q208: Design a Smart Home Hub** — Device management (WiFi/Zigbee), user automations (if-then rules), remote access via cloud, voice control integration.

**Q209: Design a Digital Wallet (PayPal/Venmo)** — Balance management, P2P transfers, request money, split bills, transaction feed, fraud detection, compliance.

**Q210: Design a Food Ordering Platform** — Restaurant menu, cart, checkout (with delivery address), order tracking, real-time driver tracking, rating.

**Q211: Design a Online Test / Proctoring System** — Questions → timer → submit. Proctoring: camera + screen recording + AI for suspicious behavior.

**Q212: Design a Cloud IDE (GitHub Codespaces)** — Container workspace, terminal, file explorer, VS Code in browser, git integration, collaboration.

**Q213: Design a Digital Signage System** — Create playlists → schedule display → push content to screens. Remote management. Analytics (plays, engagement).

**Q214: Design a Document Signing / E-Signature System** — Upload document → place signature fields → send to signers → track status → audit trail.

**Q215: Design a Content Management System (CMS)** — Create/edit pages (WYSIWYG), media library, versioning, publish workflow, permissions, CDN for static content.

**Q216: Design a User Session Management System** — Create session on login, validate on request, expire on logout/timeout. Redis session store. Token rotation.

**Q217: Design a Fraud Detection for Payments** — ML model scores each transaction. Features: amount, velocity, geolocation, device fingerprint, user history. Rule engine + model.

**Q218: Design a Shipping Rate Calculator** — Address validation → lookup carrier rates (FedEx/UPS API) → apply discounts → return rates. Caching for frequent routes.

**Q219: Design a Team Collaboration Platform (Slack-like)** — Channels, messaging (see Q102), file sharing, search, integrations (webhooks, bots), threads.

**Q220: Design a Inventory Search with Filters** — Elasticsearch with product attributes. Faceted search: brand, size, color, price range, rating. Real-time inventory counts.

**Q221: Design a Customer Review System** — Write review, upload photos, rate. Moderation (auto + manual). Verified purchase badge. Helpful votes. Sort by relevance/date.

**Q222: Design a Coupon Distribution System** — Generate codes, batch send (email/SMS), track redemption, limit per user. Anti-hoarding measures.

**Q223: Design a Real-time Collaboration Whiteboard** — Canvas with shapes/text. CRDT for conflict resolution. WebSocket for real-time sync. Cursor presence.

**Q224: Design a Push Notification Orchestrator** — Manage push campaigns. Segment users. Schedule sends. Throttle to avoid spam. Track delivery/open. A/B test copy.

**Q225: Design a Social Media Analytics Dashboard** — Track followers, engagement (likes, comments, shares), reach, impressions. Scheduled reports. Export CSV.

**Q226: Design a Package Tracking System** — Scan at each checkpoint → update tracking status. Customer notification on status change. Estimated delivery date.

**Q227: Design a Course Recommendation System** — Based on user's completed courses, skills, career goals. Collaborative filtering + content-based.

**Q228: Design a QR Code Generation System** — Encode data (URL, text, vCard) → generate QR code image → store/serve. Dynamic QR: redirect URL can be changed.

**Q229: Design a Barcode / Label Printing System** — Generate label (UPC, EAN, SKU) → send to printer. Integration with inventory systems. Batch printing.

**Q230: Design a Multi-vendor Marketplace (Etsy/Amazon)** — Vendor onboarding, product listing, order routing (to correct vendor), commission calculation, vendor dashboard.

**Q231: Design an Email List Management System** — Import contacts, segment lists, send campaigns (Mailchimp-like), track opens/clicks, unsubscribe management.

**Q232: Design a Image CDN / Optimization Service** — Accept image upload → resize/crop/compress on-the-fly → serve via CDN. URL-based transformations: `/image.jpg?w=200&h=200`.

**Q233: Design a Product Feed Aggregator** — Collect product data from multiple sources → normalize → index → serve via API. Used by shopping comparison sites.

**Q234: Design a Tax Calculation System** — Calculate tax for orders based on: product tax category, customer location (state/country), business rules. Avalara/TaxJar integration.

**Q235: Design a Voucher / Gift Card System** — Issue gift card (with code + balance). Redeem at checkout. Check balance. Partial redemption. Expiry.

**Q236: Design a Subscription Box Service** — Recurring shipments. Customize box contents. Skip/cancel/pause. Billing on schedule. Inventory planning.

**Q237: Design a Real-time Stock Ticker** — Stream stock prices via WebSocket. Market data feed → Kafka → WebSocket server → clients. Historical data store.

**Q238: Design a Weather Data Service** — Collect data from sensors/satellites → process (forecast models) → store → serve via API. Geospatial queries.

**Q239: Design a Sports Live Score System** — Ingest scores from data providers → broadcast via WebSocket to clients. Match state management. Historical stats.

**Q240: Design a Fitness Tracking App (Strava-like)** — Record GPS activity (run/cycle), display route map, calculate stats (distance, pace, elevation), leaderboards, social feed.

**Q241: Design a Photo Editing / Filter App (VSCO-like)** — Apply filters, adjust parameters (brightness, contrast), save/share. ML filters (style transfer). Performance: GPU processing.

**Q242: Design a News Aggregator (Google News-like)** — Crawl news sources (see Q109), categorize (NLP), rank by freshness/relevance, personalize feed, breaking news alerts.

**Q243: Design a Forum / Discussion Platform** — Categories, topics, posts, nested comments. Moderation tools. Search. User reputation (karma). Vote system.

**Q244: Design a Bookmarking / Save System** — Users save items (products, articles, videos). Organize in collections. Search bookmarks. Share collections.

**Q245: Design a Virtual Event Platform (Zoom + Expo)** — Live streaming (see Q143), breakout rooms, virtual booths, networking, attendee analytics.

**Q246: Design a Resources / Asset Library** — Upload images, icons, fonts, templates. Organize by tags/categories. Search. Version history. Team permissions.

**Q247: Design a Customer Journey / Funnel Analytics** — Track user events → group into sessions → visualize funnel (signup → activate → purchase). Attribution modeling.

**Q248: Design a Contract Management System** — Create contract → e-sign → store → track renewals. Auto-reminders. Clause library. Audit trail.

**Q249: Design a Patent / Intellectual Property Search** — Full-text search with synonyms, classifications (IPC/CPC). Prior art search. Citation tracking.

**Q250: Design a Knowledge Graph (Google Knowledge Graph)** — Entities (people, places, things) with relationships. Data from multiple sources. Semantic search. SPARQL query.
