# REST API Interview Questions and Answers - Part 2

## Q1: How does the HTTP `Expect: 100-continue` header work in REST APIs, and when should you use it?
**A:** The Expect: 100-continue header allows a client to ask the server whether it should send the request body before actually sending it. The client sends headers only; if the server responds with 100 Continue, the client sends the body. If the server responds with 417 Expectation Failed or 4xx, the client avoids sending the body. Use cases: (1) uploading large files where you want to check authentication/authorization before transferring data, (2) avoiding wasted bandwidth when the server will reject the request. Not all servers support it; proxies may mishandle it. Modern APIs rarely use this; instead, use a two-step upload (create upload session, then upload data).

**Code:**
```python
import gc

class Parent:
    def __init__(self):
        self.other = MyClass()

class MyClass:
    def __init__(self):
        self.obj = None

a = Parent()
b = MyClass()
a.other = b          # a -> b
b.obj = a            # b -> a  (circular reference)
del a, b
print("collected:", gc.collect())   # cyclic GC detects and frees
```

## Q2: How do you design a REST API that supports long-polling vs WebSocket upgrade via the `Upgrade` header?
**A:** Two approaches: (1) Long-polling: client sends a GET request; the server holds the connection open until new data is available or timeout occurs, then responds. The client immediately sends another request. This is simpler but has higher overhead. (2) WebSocket upgrade: client sends GET with `Upgrade: websocket` and `Connection: Upgrade` headers. Server responds with 101 Switching Protocols. The connection is then upgraded to a WebSocket for bidirectional communication. Use the `Sec-WebSocket-Key` and `Sec-WebSocket-Accept` headers for the handshake. Design decision: long-polling for infrequent updates, WebSocket for real-time bidirectional communication.

**Code:**
```python
def func_decorator(f):
    def wrapper(*args, **kwargs):
        return f(*args, **kwargs) * 2
    return wrapper

@func_decorator
def add(a, b):
    return a + b

def class_decorator(cls):
    cls.extras = ["added"]
    return cls

@class_decorator
class Widget:
    pass

print(add(2, 3))          # 10 - function behavior modified
print(Widget.extras)      # ['added'] - class enhanced
```

## Q3: How do you implement a REST API that handles `Idempotency-Key` for at-most-once semantics on POST endpoints?
**A:** Idempotency key implementation: (1) Client generates a unique UUID and sends it in the `Idempotency-Key` header, (2) Server checks if a response for this key exists (in cache/DB), (3) If yes: return the cached response (same status code and body), (4) If no: process the request, store the key + response, return the response, (5) Cache expiration: keys should expire after a reasonable period (e.g., 24 hours), (6) Response storage: include status code, body, and headers, (7) Concurrent requests with same key: use a database-level lock or optimistic concurrency to ensure only one processes, (8) Error handling: return 400 if key is missing for mutation endpoints.

**Code:**
```python
class Point:
    __slots__ = ("x", "y")        # define the fixed attribute set
    def __init__(self, x, y):
        self.x, self.y = x, y

p = Point(1, 2)
print(p.x, p.y)
print(hasattr(p, "__dict__"))     # False
# p.z = 3  -> AttributeError: no slot for z
```

## Q4: How does HTTP `Strict-Transport-Security` (HSTS) interact with REST API clients that are not browsers?
**A:** HSTS is a response header (`Strict-Transport-Security: max-age=31536000; includeSubDomains`) that tells browsers to only connect via HTTPS for the specified duration. For non-browser API clients (curl, mobile apps, server-to-server): (1) HSTS is typically ignored — these clients do not have an HSTS preload list, (2) The header does not enforce HTTPS; it's a hint only for user agents that support it, (3) API clients should implement their own HTTPS enforcement, (4) For sensitive APIs, require HTTPS at the server level (redirect HTTP to HTTPS) regardless of HSTS, (5) HSTS preloading is for domains, not API endpoints.

**Code:**
```python
class Positive:
    def __init__(self):
        self.ages = {}
    def __get__(self, obj, objtype=None):
        return self.ages[id(obj)]
    def __set__(self, obj, value):
        if value < 0:
            raise ValueError("age must be >= 0")
        self.ages[id(obj)] = value

class Person:
    age = Positive()       # descriptor defined on the class

alice = Person()
alice.age = 30             # routed through __set__
print(alice.age)           # routed through __get__
```

## Q5: How do you design REST API error responses that support both human-readable and machine-readable error codes?
**A:** Structured error format: (1) `error.code`: machine-readable string like `RATE_LIMIT_EXCEEDED`, `VALIDATION_ERROR`, `INSUFFICIENT_FUNDS`, (2) `error.message`: human-readable description, (3) `error.details`: array of per-field errors with `field`, `reason`, `message`, (4) `error.request_id`: correlation ID for debugging, (5) `error.docs_url`: link to documentation for the error type, (6) `error.status`: the HTTP status code for easier client handling. Example: `{ "error": { "code": "INVALID_PARAMETER", "message": "The email parameter is invalid", "details": [{ "field": "email", "reason": "format", "message": "Must be a valid email address" }], "request_id": "abc-123", "docs_url": "https://api.example.com/errors/INVALID_PARAMETER" } }`.

**Code:**
```python
import copy

class Shallow:
    pass

inner = [1, 2]
orig = {"data": inner}

shallow = copy.copy(orig)
deep = copy.deepcopy(orig)

shallow["data"].append(3)     # shallow copy shares inner object
print(orig["data"])           # [1, 2, 3]  - mutated!
print(deep["data"])           # [1, 2]     - independent
```

## Q6: How do you design a REST API that supports partial responses (sparse fieldsets) using the `fields` query parameter?
**A:** Sparse fieldsets allow clients to specify which fields to include in the response. Pattern: `GET /users/123?fields=id,name,email`. Implementation: (1) Server parses the `fields` parameter, (2) Only returns the requested fields in the response, (3) If `fields` is omitted, return the full default representation, (4) Handle nested fields: `?fields=id,name,address(city,zip)`, (5) Benefits: reduced bandwidth, faster serialization, (6) Challenges: caching complexity (different field combinations create different responses), (7) JSON:API standard formalizes this with `fields[TYPE]` parameter. Always validate requested fields against the schema.

**Code:**
```python
import asyncio

async def one():
    await asyncio.sleep(0.1)
    return 1

async def main():
    # the event loop schedules these coroutines on a single thread
    results = await asyncio.gather(one(), one())
    print(results)

asyncio.run(main())    # [1, 1]
```

## Q7: How do you handle REST API versioning via the `Accept` header (content negotiation)?
**A:** Content negotiation versioning: (1) Client sends `Accept: application/vnd.company.v2+json`, (2) Server parses the vendor media type to extract the version, (3) Server routes to the appropriate handler or transforms the response, (4) Default: if no version specified, use the latest stable version (or return 400), (5) The `vnd.` prefix indicates vendor-specific media types. Benefits: (a) URL remains clean (no /v1/ prefix), (b) version is part of content negotiation, (c) different representations of same resource can coexist. Drawbacks: (a) harder to test from browser, (b) caching proxies may not handle vendor MIME types well, (c) requires client cooperation.

**Code:**
```python
class Resource:
    def __enter__(self):               # acquire / enter the with block
        print("acquired")
        return self
    def __exit__(self, exc_type, exc, tb):   # called on exit, error or not
        print("released")
        return False                   # False: exceptions propagate

with Resource() as r:
    print("using", r)
```

## Q8: How do you design a REST API for file uploads that supports resumable uploads?
**A:** Resumable upload protocol: (1) POST `/uploads` creates an upload session, returns `upload_id` and a URL like `/uploads/{upload_id}`, (2) Client uploads chunks using PUT/PATCH with `Content-Range` header: `bytes 0-999/5000`, (3) Server responds with `Range: bytes=0-999` (or `308 Resume Incomplete`) indicating received bytes, (4) Client resumes from last received byte, (5) On completion, server responds with 201 Created and the final resource URL, (6) Use TTL for abandoned uploads, (7) Store upload state in a database or file system, (8) Consider using TUS protocol (open standard for resumable uploads). Benefits: fault-tolerant uploads, handles network interruptions.

**Code:**
```python
class A: pass
class B(A): pass
class C(A): pass
class D(B, C): pass          # diamond

print([c.__name__ for c in D.__mro__])
# ['D', 'B', 'C', 'A', 'object'] - C3 linearization, each class once
```

## Q9: How does the `Vary` header affect API caching, and what are common pitfalls?
**A:** The `Vary` header tells caches that the response may vary based on one or more request headers. Example: `Vary: Accept, Authorization`. Common values: (1) `Accept` — response differs by content type, (2) `Authorization` — response differs per user, (3) `Accept-Encoding` — response differs by compression, (4) `Origin` — CORS responses vary by origin. Pitfalls: (1) `Vary: *` disables caching entirely (too aggressive), (2) Missing `Vary: Authorization` can cause one user's authenticated response to be served to another user (security issue), (3) Overusing `Vary` fragments the cache (different cache entries for each header combination), (4) CDNs and proxies may not handle `Vary` consistently, (5) `Vary: Accept-Encoding` is automatically added by some proxies.

**Code:**
```python
import functools

@functools.lru_cache(maxsize=3)
def expensive(n):
    print("computing", n)
    return n * n

print(expensive(4))    # computing 4 -> 16
print(expensive(4))    # cached -> 16, no recompute
print(expensive.cache_info())

# args must be hashable, function must be deterministic
```

## Q10: How do you implement a REST API that supports both `application/json` and `application/x-protobuf` for the same endpoint?
**A:** Multi-format support: (1) Server inspects the `Accept` header to determine response format, (2) Client sends `Content-Type` header to indicate request format, (3) Server has serializers/deserializers for both formats, (4) If `Accept: application/x-protobuf`, the server serializes the response as protobuf, (5) If `Accept: application/json`, the server serializes as JSON, (6) If the client sends protobuf, the server deserializes accordingly, (7) Benefits: protobuf is faster and smaller (binary), JSON is debuggable, (8) Challenges: maintaining two serialization layers, ensuring consistent validation, (9) Use a single internal representation and pluggable serializers, (10) Default to JSON if no acceptable format is specified.

**Code:**
```python
import threading
from concurrent.futures import ProcessPoolExecutor

def cpu_task(n):
    return sum(range(n))

# threads: share memory, GIL-bound -> best for I/O-bound
threads = [threading.Thread(target=cpu_task, args=(1000,)) for _ in range(2)]
for t in threads: t.start()
for t in threads: t.join()

# processes: separate memory + GIL, true CPU parallelism
with ProcessPoolExecutor(max_workers=2) as ex:
    print(list(ex.map(cpu_task, [100, 200])))
```

## Q11: How do you handle REST API pagination with `Link` headers (RFC 5988)?
**A:** Link header pagination: (1) Include a `Link` header in responses with rel values: `Link: <https://api.example.com/users?page=2>; rel="next", <https://api.example.com/users?page=1>; rel="prev", <https://api.example.com/users?page=10>; rel="last", <https://api.example.com/users?page=1>; rel="first"`, (2) The client follows the `rel="next"` URL to get the next page, (3) No `next` link means the last page, (4) Benefits: follows REST principles (links are part of the resource state), no custom pagination schema, (5) Combined with cursor-based pagination: `Link: <https://api.example.com/users?cursor=abc>; rel="next"`, (6) Always include `total` or similar metadata for clients that need to know total count, (7) The Link header is standardized and cache-friendly.

**Code:**
```python
class A:
    def whoami(self):
        return "A"

class B:
    def whoami(self):
        return "B"

class C(A, B):          # MRO decides which whoami() wins
    pass

print(C().whoami())     # A - first in MRO
print([k.__name__ for k in C.__mro__])
```

## Q12: How do you implement a REST API that supports both synchronous and asynchronous processing patterns?
**A:** Dual-mode API: (1) Client sends a request with a `Prefer: respond-async` header (RFC 7240), (2) If the server can process synchronously (fast operation), it responds normally (200/201), (3) If the server chooses async (slow operation), it responds with 202 Accepted and a `Location` header pointing to a status endpoint, (4) The status endpoint (`/operations/{id}`) returns 200 OK with status: pending/running/completed/failed and a `percentComplete` field, (5) When complete, the status endpoint returns 303 See Other redirecting to the result, (6) Alternative: always use async for mutations (POST/PUT/PATCH/DELETE) to make all write operations uniform, (7) The `Prefer` header lets the client express preference without changing the endpoint URL.

**Code:**
```python
import sys
print("GIL prevents true multithreading in CPython for CPU-bound code")
import threading, time

def busy():
    t = time.time()
    while time.time() - t < 0.2:
        pass

start = time.time()
ts = [threading.Thread(target=busy) for _ in range(2)]
[t.start() for t in ts]
[t.join() for t in ts]
print(f"{time.time() - start:.2f}s (serialized by the GIL)")
```

## Q13: How does the `Prefer` header (RFC 7240) enable API clients to express processing preferences?
**A:** The Prefer header allows clients to specify preferences: (1) `Prefer: return=minimal` — return 204 No Content instead of the full resource, (2) `Prefer: return=representation` — return the full resource in the response, (3) `Prefer: respond-async` — process asynchronously, (4) `Prefer: wait=N` — wait up to N seconds for a synchronous response before switching to async, (5) `Prefer: handling=lenient` — lenient validation, (6) `Prefer: handling=strict` — strict validation. The server responds with `Preference-Applied: return=minimal` to indicate which preference was honored. Not all clients or servers support Prefer; always provide a reasonable default behavior.

**Code:**
```python
class Task:
    counter = 0                      # class state

    def __init__(self, name):
        self.name = name             # instance state
        Task.counter += 1

    def instance_method(self):       # self -> instance state
        return f"task {self.name}"

    @classmethod
    def total(cls):                  # cls -> class state
        return cls.counter

    @staticmethod
    def info():                      # neither, plain function on the class
        return "tasks collection"

t1, t2 = Task("a"), Task("b")
print(t1.instance_method())
print(Task.total())       # 2
print(Task.info())
```

## Q14: How do you implement REST API soft-delete with a `deleted_at` timestamp and automatic cleanup?
**A:** Soft-delete pattern: (1) Add `deleted_at` timestamp (nullable) to resources, (2) DELETE sets `deleted_at = now()` instead of deleting, (3) GET/DELETE queries filter with `WHERE deleted_at IS NULL`, (4) GET `?include_deleted=true` or GET `/users/123?deleted=true` for admin recovery, (5) POST `/users/123/restore` sets `deleted_at = NULL`, (6) Background job permanently deletes records where `deleted_at < now() - 30 days`, (7) Unique indexes: use partial indexes `WHERE deleted_at IS NULL` to allow unique constraints on active records while allowing duplicate soft-deleted names, (8) Cascade soft-deletes to related resources.

**Code:**
```python
class immutable_list(tuple):
    def __new__(cls, items):         # __new__ creates & returns instance
        return super().__new__(cls, items)
    # __init__ would also be called after __new__

class Normal:
    def __init__(self, x):           # regular initializer
        self.x = x

print(immutable_list([1, 2]))
print(Normal(5).x)
```

## Q15: How do you design a REST API for a geo-distributed system with data residency requirements?
**A:** Geo-distributed API design: (1) Region-aware endpoints: `https://eu.api.example.com` and `https://us.api.example.com`, (2) Data residency: requests to EU endpoint store data only in EU, (3) Global request routing: DNS-based (GeoDNS) or anycast routing, (4) `Content-Location` header indicates where the resource was created, (5) Cross-region replication: async replication with conflict resolution (last-writer-wins or CRDTs), (6) `Location` header: `Location: https://eu.api.example.com/users/123`, (7) GDPR compliance: right to erasure API endpoint that purges data from all regions, (8) Monitoring: per-region latency and error rate dashboards.

**Code:**
```python
import sys
print(sys.path)                # where import looks
import math                    # triggers finder -> loader sequence
print(math.__spec__)
```

## Q16: How do you implement a REST API that supports batch operations with atomicity guarantees?
**A:** Batch API design: (1) POST `/batch` accepts an array of requests: `{ "requests": [{ "method": "POST", "path": "/users", "body": {...} }, { "method": "PATCH", "path": "/users/1", "body": {...} }] }`, (2) `atomic: true` parameter ensures all-or-nothing execution (requires transaction support), (3) `atomic: false` processes independently and returns per-item status, (4) Response: `{ "results": [{ "status": 201, "headers": {...}, "body": {...} }, { "status": 200, ... }] }`, (5) Use 200 OK for the batch itself (even if individual operations fail), (6) Maximum batch size (e.g., 100 operations), (7) Each operation can reference previous results using `$ref: 0.body.id`.

**Code:**
```python
from abc import ABC, abstractmethod

class Animal(ABC):
    @abstractmethod
    def sound(self):
        ...
    def legs(self):                 # concrete method is fine on an ABC
        return 4

class Dog(Animal):
    def sound(self):
        return "woof"

print(Dog().sound(), Dog().legs())
# Dog must implement sound() or it can't be instantiated
```

## Q17: How do you implement REST API request tracing with correlation IDs across microservices?
**A:** Distributed tracing: (1) Client generates a `X-Request-Id` or `X-Correlation-Id` header (UUID), (2) The first service that receives the request passes this header to all downstream calls, (3) Each service records: request ID, service name, span ID, parent span ID, start time, duration, (4) Logs include the trace ID: `{"trace_id": "abc123", "service": "auth", "latency": 45}`, (5) Tracing headers: `X-Request-Id` (end-to-end), `X-B3-TraceId` (Zipkin), `X-B3-SpanId`, (6) The API response includes the request ID so clients can reference it in support tickets, (7) Centralized tracing UI (Jaeger, Zipkin) for visualization, (8) Always propagate tracing context even on error responses.

**Code:**
```python
class Money:
    def __init__(self, amount):
        self.amount = amount
    def __repr__(self):      # unambiguous, for debugging
        return f"Money({self.amount})"
    def __str__(self):       # user-friendly, for print()
        return f"${self.amount}"
    def __format__(self, spec):    # used by f-string / format()
        return str(self)

m = Money(5)
print(repr(m))     # Money(5)
print(str(m))      # $5
print(f"{m}")      # $5
```

## Q18: How do you design a REST API that prevents mass assignment vulnerabilities?
**A:** Mass assignment prevention: (1) Whitelist approach: define which fields can be set via API per endpoint/operation, (2) Use a write schema (PATCH/POST) separate from the read schema (GET), (3) Never directly pass request body to ORM models, (4) Implement a `writable` annotation or DTO (Data Transfer Object) layer, (5) For PATCH, use JSON Patch (RFC 6902) which explicitly lists fields to modify, (6) Validate each field individually before assignment, (7) Reject unknown fields by default (configurable via a `strict` mode flag), (8) Audit log all field changes for sensitive fields. Example: creating a user should not allow setting `is_admin=true` unless explicitly permitted.

**Code:**
```python
import struct

data = struct.pack("3i", 1, 2, 3)     # buffer protocol underneath
mv = memoryview(data)                 # zero-copy view into the bytes
print(mv.nbytes, mv.tolist())
print(struct.unpack("3i", mv))        # (1, 2, 3)
```

## Q19: How does HTTP `Content-Disposition` header work for file downloads, and what security considerations exist?
**A:** Content-Disposition controls how the browser handles the response: (1) `inline` — display in browser if possible (PDF, images), (2) `attachment; filename="report.pdf"` — force download with specified filename. Security: (1) Sanitize filenames to prevent path traversal (`../../etc/passwd`), (2) Remove control characters and null bytes from filenames, (3) Set `X-Content-Type-Options: nosniff` to prevent MIME sniffing, (4) Validate the file extension matches the content type, (5) Always set `Content-Type` explicitly, (6) For user-uploaded files served to other users, consider serving from a separate domain or using `Content-Disposition: attachment` to prevent XSS via HTML files.

**Code:**
```python
class RangeN:
    def __init__(self, n):
        self.n = n
        self.i = 0
    def __iter__(self):          # must return an iterator
        return self
    def __next__(self):          # returns next item, or raises StopIteration
        if self.i >= self.n:
            raise StopIteration
        self.i += 1
        return self.i

print(list(RangeN(3)))           # [1, 2, 3]
```

## Q20: How do you design a REST API that supports both optimistic and pessimistic locking?
**A:** Locking strategies: (1) Optimistic: use `If-Match` header with ETag — `PUT /users/123 If-Match: "abc123"`. If the ETag doesn't match, return 412 Precondition Failed. (2) Pessimistic: POST `/users/123/lock` acquires an exclusive lock (returns a lock token), DELETE `/users/123/lock` releases it. Specify lock duration/timeout. (3) Use `Lock-Token` header with `If-Match: (<lock-token>)` for WebDAV-style locking. (4) Optimistic locking is preferred for most APIs (no lock management overhead), (5) Pessimistic locking for long-running operations (editing a document for minutes). (6) Always include the current ETag in GET responses so clients can use it for subsequent mutations.

**Code:**
```python
try:
    raise ValueError("original")
except ValueError:
    raise                            # bare raise: re-raise current exception

# raise e  (raise a chosen instance) and  raise ... from ...  (chain)
try:
    try:
        1 / 0
    except ZeroDivisionError as e:
        raise ValueError("wrapped") from e
except ValueError as exc:
    print("cause:", type(exc.__cause__).__name__)
```

## Q21: How do you implement cursor-based pagination with composite cursors for sorting by multiple fields?
**A:** Composite cursor: (1) Encode sort values into the cursor: base64 encode `{"created_at": "2024-01-01T00:00:00Z", "id": "abc123"}`, (2) SQL: `WHERE (created_at < $1) OR (created_at = $1 AND id < $2) ORDER BY created_at DESC, id DESC LIMIT 20`, (3) The cursor points to the last item of the previous page, (4) Benefits: stable pagination even when new items are inserted, efficient on large datasets, (5) Send cursor in query: `?cursor=eyJjcmVhdGVkX2F0IjogIjIwMjQtMDEtMDFUMDA6MDA6MDBaIiwgImlkIjogImFiYzEyMyJ9`, (6) Include a `has_more` boolean in the response so clients know when to stop.

**Code:**
```python
class Base:
    def __init__(self):
        print("Base")
        super().__init__()

class Mixin:
    def __init__(self):
        print("Mixin")
        super().__init__()

class Both(Base, Mixin):
    def __init__(self):
        super().__init__()       # follows the MRO cooperatively

Both()    # prints Mixin then Base
```

## Q22: How does the `If-None-Match` header interact with `Cache-Control: no-cache` differently in REST APIs?
**A:** `Cache-Control: no-cache` means the cached response must be revalidated with the server before use (not "do not cache"). `If-None-Match` is the revalidation mechanism: (1) Client caches the response with ETag, (2) On next request, client sends `If-None-Match: "etag-value"`, (3) If the resource hasn't changed, server returns 304 Not Modified (empty body), (4) The client uses its cached response. With `no-cache` but no ETag: the client must re-fetch the full response every time (wasteful). For efficient caching, ALWAYS include ETag with `no-cache`. For truly dynamic data, use `Cache-Control: no-store` (never cache) or short `max-age` with ETag.

**Code:**
```python
from enum import Enum, auto, unique

@unique                    # rejects duplicate values
class Color(Enum):
    RED = 1
    GREEN = auto()         # auto() assigns 2

print(Color.RED.name, Color.RED.value)
print(Color.GREEN.value)   # 2
for c in Color:
    print(c)
```

## Q23: How do you design a REST API that handles idempotent retries for payment processing?
**A:** Payment idempotency: (1) Client generates a unique `Idempotency-Key` (UUID) for each payment attempt, (2) Server checks if the key was already processed — if yes, return the original response (including the same status code), (3) If the original request was still processing and a retry arrives, the server should wait for the original to complete (not start a duplicate), (4) Use a database lock on the idempotency key: `INSERT INTO idempotency_keys (key, response) VALUES ($1, NULL) ON CONFLICT DO NOTHING RETURNING *`, (5) If the INSERT succeeds, this is the first attempt — proceed with payment, (6) If the INSERT fails (duplicate key), this is a retry — fetch and return the stored response, (7) Store responses with a TTL (e.g., 24 hours), (8) Never allow a retry to change the result: 200 with "already charged" is different from the original 201 "charge created".

**Code:**
```python
import threading, time

def work():
    time.sleep(0.1)      # I/O-bound: GIL released, threads overlap

start = time.time()
for i in range(4):
    threading.Thread(target=work).start()
# main thread still runs while others sleep
# for CPU-bound loops the GIL would serialize them
print("main thread continues while I/O-bound threads run")
```

## Q24: How do you implement REST API rate limiting with token bucket vs sliding window algorithms?
**A:** Rate limiting algorithms: (1) Token bucket: a bucket with N tokens refills at rate R tokens/second. Each request consumes a token. If the bucket is empty, the request is denied. Burst-friendly, allows short traffic spikes up to bucket size. (2) Sliding window log: track timestamps of requests in the current window. Count how many falls within the window. More accurate but more memory. (3) Sliding window counter: approximate sliding window using the previous window's count + current window's partial count. Memory-efficient and accurate enough. (4) Implementation: use Redis for distributed rate limiting. (5) Response headers: `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset`, `Retry-After`. (6) For 429 Too Many Requests: include `Retry-After` in seconds.

**Code:**
```python
import cProfile, pstats, io

def inner():
    return sum(range(1000))

def outer():
    return inner() * 2

prof = cProfile.Profile()
prof.enable()
outer()
prof.disable()
# sort by cumulative time and print stats
buf = io.StringIO()
pstats.Stats(prof, stream=buf).sort_stats("cumulative").print_stats()
print(buf.getvalue()[:400])
```

## Q25: How do you design a REST API for search with faceted navigation?
**A:** Faceted search API: (1) GET `/products?q=shoes&category=men&sort=price_asc&page=1` for basic search, (2) Response includes products array and facets object: `{ "facets": { "brand": { "Nike": 42, "Adidas": 35 }, "size": { "10": 15, "11": 12 }, "price_range": { "0-50": 100, "51-100": 50 } } }`, (3) Facets returned depend on the current query and filters, (4) Each facet value should be a clickable URL that adds/removes the filter, (5) Use `POST /search` for complex queries (JSON body with nested filters), (6) Powering: Elasticsearch or Algolia for full-text + faceted search, (7) Cache: cache common search results with short TTL.

**Code:**
```python
from dataclasses import dataclass

@dataclass
class Invoice:
    amount: int
    tax_rate: float = 0.2
    tax_total: float = 0.0

    def __post_init__(self):       # runs after the generated __init__
        self.tax_total = self.amount * self.tax_rate

inv = Invoice(100)
print(inv.tax_total)    # 20.0
```

## Q26: How do you implement REST API field-level security where certain fields are only visible to authorized users?
**A:** Field-level security: (1) Define field permissions: `{ "email": ["admin", "self"], "ssn": ["admin"], "name": ["*"] }`, (2) In the serializer/interceptor, check the user's role and identity against the field's required permissions, (3) For list endpoints: return the resource without restricted fields (or with masked values), (4) For detail endpoints: same logic, optionally include `?include_sensitive=true` for authorized users, (5) Return a consistent schema, just with null/empty values for unauthorized fields, (6) Never return partial schemas (different fields for different users), (7) Audit: log when sensitive fields are accessed, (8) Performance: avoid per-field checks in hot paths; cache permissions per role.

**Code:**
```python
import sys

a = "hello"          # identifier-like literal -> may be interned
b = "hello"
print(a is b)        # True (CPython interns literals)

c = "".join(["he", "llo"])   # dynamically built -> not interned
d = "hello"
print(c is d)        # typically False

key = sys.intern("shared")
print(sys.intern("shared") is key)    # True - explicitly interned
```

## Q27: How do you implement REST API webhook delivery with retry, deduplication, and signature verification?
**A:** Webhook system: (1) Payload: POST to registered URL with JSON body containing event type, resource ID, timestamp, (2) Signature: HMAC-SHA256 of the payload with a shared secret, sent in `X-Signature-256` header, (3) Delivery: immediate attempt, then retry with exponential backoff (1min, 5min, 30min, 2hr, 6hr, 24hr — max 6 attempts), (4) Deduplication: include `X-Event-Id` (UUID), receiver should deduplicate by this ID, (5) Dead letter: after max retries, log the failure and store for manual inspection, (6) Rate limiting: don't overwhelm receivers, max N webhooks per second, (7) IP allowlisting: suggest receivers allowlist webhook sender IPs, (8) Testing: provide a test endpoint or UI to send sample webhooks.

**Code:**
```python
class Proxy:
    def __getattribute__(self, name):       # ALL attribute reads
        if name.startswith("_"):
            raise AttributeError("blocked")
        return super().__getattribute__(name)

    def __getattr__(self, name):            # only when attribute is missing
        return f"no {name}"

p = Proxy()
print(p.public)     # raises AttributeError within __getattribute__
print(getattr(p, "whatever", "fallback"))
```

## Q28: How do you design a REST API that handles timezone-aware date/time inputs and outputs?
**A:** Timezone handling: (1) Always store and transmit timestamps in UTC (ISO 8601: `2024-01-15T14:30:00Z`), (2) Accept timezone offset in input: `2024-01-15T14:30:00+05:30`, convert to UTC for storage, (3) Return timestamps in UTC: `"created_at": "2024-01-15T09:00:00Z"`, (4) Optionally, allow clients to specify timezone via `X-Timezone: America/New_York` header, (5) The server converts UTC to the requested timezone in responses, (6) For date-only fields (birthday, start_date), use `2024-01-15` without timezone, (7) Document the expected format: always ISO 8601, always UTC, (8) Never use non-standard formats like MM/DD/YYYY.

**Code:**
```python
import asyncio

def gen():
    yield 1          # generator: produces values with state
    yield 2

async def coro():
    await asyncio.sleep(0)   # coroutine: awaits, runs on event loop
    return "done"

g = gen()
print(next(g), next(g))
print(asyncio.run(coro()))   # done
```

## Q29: How do you implement REST API bulk reads using the `Prefer` header with `return=representation` for efficiency?
**A:** Bulk reads: (1) POST `/users/bulk` with `{ "ids": [1, 2, 3, ...] }` (up to 1000 IDs), (2) The response is a map: `{ "results": { "1": {...}, "2": {...}, "3": {...} } }`, (3) Missing IDs are omitted from the result, (4) Benefits: one round trip instead of N, consistent snapshot (if using transaction), (5) Alternative: GET `/users?ids=1,2,3` with a custom media type, (6) For very large datasets, use cursor-based pagination with the collection endpoint, (7) Cache: bulk reads should be cacheable (ETag on the response), (8) Rate limit: count bulk reads as N requests for rate limiting purposes.

**Code:**
```python
class Singleton:
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

a = Singleton()
b = Singleton()
print(a is b)      # True - one instance only
```

## Q30: How do you design a REST API for a notification system that supports email, SMS, and push notifications?
**A:** Notification API: (1) POST `/notifications` with `{ "type": "order_confirmed", "channels": ["email", "push"], "recipients": ["user_123"], "data": { "order_id": "ORD-456" } }`, (2) Each notification type has a template (stored server-side), (3) The request is queued for async processing, (4) Response: 202 Accepted with `Location: /notifications/{id}`, (5) GET `/notifications/{id}` returns status: pending/sent/failed and per-channel status, (6) Preferences: GET/PUT `/users/{id}/notification_preferences` controls which notification types each user receives, (7) Rate limiting: per-user, per-channel, (8) Unsubscribe: include `List-Unsubscribe` header in email notifications.

**Code:**
```python
# my_script.py
def main():
    print("running")

if __name__ == "__main__":   # direct execution (not import)
    main()
else:
    print("imported as", __name__)
```

## Q31: How do you implement REST API sorting with configurable sort direction per field?
**A:** Multi-field sorting: (1) Query parameter: `?sort=name:asc,created_at:desc`, (2) Parse into sort directives: `[{field: "name", dir: "asc"}, {field: "created_at", dir: "desc"}]`, (3) Whitelist sortable fields to prevent database errors or injection, (4) Default sort: if unspecified, use a sensible default (e.g., `created_at:desc`), (5) Security: never allow sorting by unindexed fields (performance issue), (6) Return sort information in the response for client confirmation, (7) For cursor-based pagination, the sort order must be consistent across pages, (8) Documentation: clearly list which fields support sorting and the direction syntax.

**Code:**
```python
import pickletools
import pickle

class Data:
    def __init__(self, x):
        self.x = x
    def __reduce__(self):          # controls how pickling reconstructs
        return (Data, (self.x,))

d = Data(42)
payload = pickle.dumps(d)          # could be a malicious stream
print(pickle.loads(payload).x)     # unpickling can run arbitrary code
pl = pickletools.optimize(payload)
print(len(pl) <= len(payload))     # True - optimized bytes
```

## Q32: How does the `X-Frame-Options` header protect REST API endpoints that serve embedded content?
**A:** X-Frame-Options prevents clickjacking attacks by controlling whether a page can be embedded in a frame/iframe. Values: (1) `DENY` — cannot be embedded in any frame, (2) `SAMEORIGIN` — can be embedded only on the same origin, (3) `ALLOW-FROM https://example.com` — deprecated, use `Content-Security-Policy: frame-ancestors` instead. For REST APIs: (1) API responses that return JSON rarely need this (JSON is not rendered as HTML), (2) But if your API serves HTML (API docs, error pages, file upload previews), set `DENY`, (3) For embedding API documentation UIs (Swagger UI), use `SAMEORIGIN`, (4) Modern alternative: `Content-Security-Policy: frame-ancestors 'self' https://trusted.com`.

**Code:**
```python
import weakref

class Heavy:
    def __init__(self, name):
        self.name = name

obj = Heavy("cache-1")
ref = weakref.ref(obj)
print(ref() is obj)     # True

del obj
print(ref())            # None - object was collected
```

## Q33: How do you design a REST API that supports server-sent events (SSE) for real-time updates?
**A:** SSE API design: (1) GET `/events` with `Accept: text/event-stream`, (2) Server responds with `Content-Type: text/event-stream` and keeps the connection open, (3) Event format: `data: {"type": "order_updated", "order_id": 123}

`, (4) Include `id:` field for Last-Event-Id reconnection, (5) Client reconnection: client sends `Last-Event-Id: 42` to resume from the last received event, (6) Heartbeat: server sends `: heartbeat` comments every 30s to keep the connection alive, (7) Filtering: `GET /events?types=order_updated,order_created` to subscribe to specific event types, (8) Authentication: use query parameter token or cookie (SSE cannot set custom headers).

**Code:**
```python
import threading

lock = threading.Lock()
counter = 0

def inc():
    global counter
    with lock:                # context manager makes it deadlock-safe
        counter += 1

ts = [threading.Thread(target=inc) for _ in range(10)]
for t in ts: t.start()
for t in ts: t.join()
print(counter)                # 10 - protected increment
```

## Q34: How do you implement REST API fuzzy search with typo tolerance using Levenshtein distance?
**A:** Fuzzy search: (1) Query: `GET /products?q=shoo&fuzzy=true`, (2) Server applies Levenshtein distance or Damerau-Levenshtein to find terms within N edits of the query, (3) For Elasticsearch: use `fuzziness: AUTO` parameter, (4) For PostgreSQL: use `pg_trgm` extension with `similarity()` function, (5) For in-memory: use BK-tree or SymSpell for efficient fuzzy matching, (6) Response includes the corrected term suggestion: `{ "did_you_mean": "shoes", "results": [...] }`, (7) Performance: fuzzy search is computationally expensive — use dedicated search engines for production, (8) Autocomplete: use prefix-based search for typeahead, which is faster than full fuzzy matching.

**Code:**
```python
from typing import List, Dict, Optional, Union, Any

Vector = List[float]                 # alias
Config = Dict[str, Union[int, str]]  # composed types

def norm(v: Vector) -> Optional[float]:
    return sum(x * x for x in v) ** 0.5 if v else None

print(norm([3.0, 4.0]))   # 5.0
print(norm([]))           # None
```

## Q35: How do you design a REST API for a versioned file storage system?
**A:** File storage API: (1) POST `/files` uploads a file, returns file ID and metadata, (2) GET `/files/{id}` downloads the latest version, (3) GET `/files/{id}?version=2` downloads a specific version, (4) PUT `/files/{id}` uploads a new version, (5) GET `/files/{id}/versions` lists all versions, (6) DELETE `/files/{id}/versions/2` deletes a specific version, (7) Metadata: include ETag (file hash), Content-Type, Content-Length, last-modified, (8) Range requests: support `Range: bytes=0-1023` for partial downloads, (9) Deduplication: detect duplicate uploads via hash and return existing file URL, (10) Limits: max file size, max versions per file, retention policy.

**Code:**
```python
# module a.py
def use():
    from module_b import helper   # lazy import, only when called
    return helper()

# keeps module load order from failing on circular dependency
```

## Q36: How do you implement REST API rate limiting with a sliding window counter in Redis?
**A:** Sliding window counter in Redis: (1) Use a sorted set with timestamps as scores: `ZADD rate_limiter:user:123 <timestamp> <request_id>`, (2) Remove old entries: `ZREMRANGEBYSCORE rate_limiter:user:123 0 <window_start>`, (3) Count: `ZCARD rate_limiter:user:123`, (4) If count > limit, reject with 429, (5) Window: typical 60 seconds for per-minute rate limits, (6) Accuracy: the sorted set approach is exact (no approximation), (7) Memory: each request stores one entry — set an expiration on the key: `EXPIRE rate_limiter:user:123 120` (clean up after 2x window), (8) Alternative: use INCR with sliding window by maintaining two counters (current minute and previous minute).

**Code:**
```python
import copy

class Box:
    def __init__(self, items):
        self.items = items
    def __copy__(self):                      # custom shallow copy
        return Box(self.items)
    def __deepcopy__(self, memo):            # custom deep copy
        return Box(copy.deepcopy(self.items, memo))

b = Box([1, 2, [3]])
c = copy.deepcopy(b)
c.items[2].append(4)
print(b.items)    # [1, 2, [3]] unchanged
print(c.items)    # [1, 2, [3, 4]]
```

## Q37: How do you design a REST API for a loyalty/rewards points system that prevents abuse?
**A:** Rewards API: (1) POST `/transactions` records point earn/burn with idempotency key, (2) GET `/users/{id}/balance` returns current points and expiration schedule, (3) GET `/users/{id}/transactions` lists point history with pagination, (4) Fraud prevention: daily accrual limits, velocity checks (max X points per hour), (5) Point expiration: return points with expiration dates, expire via scheduled job, (6) Audit trail: all point changes are logged with reason, source, and admin who approved (if manual), (7) Rollback: POST `/transactions/{id}/reverse` reverses a transaction with reason, (8) Consistency: use transactions for balance updates to prevent race conditions.

**Code:**
```python
class Plugin:
    registry = []

    def __init_subclass__(cls, **kwargs):   # runs for every subclass
        super().__init_subclass__(**kwargs)
        cls.registry.append(cls.__name__)

class A(Plugin): pass
class B(Plugin): pass

print(Plugin.registry)     # ['A', 'B']
```

## Q38: How does the `Access-Control-Expose-Headers` header affect CORS for REST APIs?
**A:** `Access-Control-Expose-Headers` tells the browser which response headers the client JavaScript can access. By default, only simple response headers are exposed (Cache-Control, Content-Language, Content-Type, Expires, Last-Modified, Pragma). For custom headers: (1) If your API sends `X-RateLimit-Remaining`, `X-Request-Id`, or other custom headers, they must be listed in `Access-Control-Expose-Headers`, (2) Example: `Access-Control-Expose-Headers: X-Request-Id, X-RateLimit-Remaining, X-RateLimit-Reset`, (3) Without this header, `fetch()` and `XMLHttpRequest` cannot read these headers via `getResponseHeader()`, (4) The header applies to both simple and preflight responses, (5) Wildcard (`*`) can expose all headers, but not for credentialed requests.

**Code:**
```python
class Temp:
    def __del__(self):
        print("finalizing")     # might never be called if cycles exist

obj = Temp()
del obj                        # prints "finalizing" (usually)
```

## Q39: How do you implement REST API sub-resource filtering with complex nested conditions?
**A:** Complex filtering: (1) JSON-encoded filter: `GET /orders?filter={"status":"shipped","total":{"$gt":100}}`, (2) RSQL/FIQL syntax: `GET /orders?filter=status==shipped;total=gt=100`, (3) OData query: `GET /orders?$filter=status eq 'shipped' and total gt 100`, (4) Benefits of RSQL: URL-safe, supports AND (`;`), OR (`,`), comparison operators (`==`, `=gt=`, `=lt=`, `=ge=`, `=le=`, `=in=`), (5) Nesting: `filter=user/name==john` for related resources, (6) Security: validate filter fields against a whitelist, limit filter depth, (7) Performance: ensure filtered fields are indexed, add max query complexity limits.

**Code:**
```python
from collections import namedtuple
from dataclasses import dataclass

Point = namedtuple("Point", ["x", "y"])     # immutable, tuple-subclass

@dataclass
class PointDC:
    x: int
    y: int

p = Point(1, 2)
q = PointDC(1, 2)
print(p.x, p)       # namedtuple fields
print(q == PointDC(1, 2))   # dataclass auto __eq__
```

## Q40: How do you design a REST API for a booking system that handles double-booking prevention?
**A:** Booking API: (1) Availability: GET `/slots?date=2024-01-15&resource_id=123` returns available time slots, (2) Hold: POST `/holds` creates a temporary hold on a slot (expires in 15 minutes), returns hold token, (3) Book: POST `/bookings` with hold token confirms the booking, (4) Optimistic concurrency: PUT `/bookings/{id} If-Match: "etag"` prevents conflicting updates, (5) Pessimistic locking: GET `/slots/{id}/lock` for administrative overrides, (6) Expiration: background job expires unconfirmed holds, (7) Conflict response: 409 Conflict with details about the conflicting booking, (8) Waitlist: POST `/waitlist` with resource and date range, (9) Overbooking: optional configurable overbooking ratio for high-demand resources.

**Code:**
```python
import asyncio

async def task(v):
    await asyncio.sleep(0.05)
    return v

async def main():
    # gather: returns results in input order, propagates first error
    results = await asyncio.gather(task(1), task(2))
    print(results)            # [1, 2]

    # wait: lower-level, returns (done, pending)
    done, pending = await asyncio.wait(
        [task(3), task(4)],
        timeout=1,
        return_when=asyncio.FIRST_COMPLETED,
    )
    print(len(done), [d.result() for d in done])

asyncio.run(main())
```

## Q41: How do you implement REST API compression with different algorithms (gzip, brotli, zstd)?
**A:** Content negotiation for compression: (1) Client sends `Accept-Encoding: gzip, br, zstd`, (2) Server selects the best algorithm supported by both, (3) Preference order: zstd > br > gzip (by compression ratio), (4) Server compresses the response body and sets `Content-Encoding: zstd`, (5) The `Vary: Accept-Encoding` header ensures caches differentiate compressed vs uncompressed versions, (6) Minimum size threshold: don't compress responses smaller than 1KB (wasteful), (7) Server-sent events (SSE): compression works well for long-lived streams, (8) Brotli generally offers the best compression ratio for JSON (15-20% better than gzip), (9) zstd offers similar compression to brotli with faster decompression, (10) CPU cost: compression adds server CPU usage; consider pre-compressing static responses.

**Code:**
```python
from __future__ import annotations   # must be near the top

def add(a: int, b: int) -> int:
    return a + b

print(add(1, 2))
print(add.__annotations__)   # {'a': 'int', 'b': 'int', 'return': 'int'}
```

## Q42: How do you design a REST API that supports multiple data formats including CSV and Excel export?
**A:** Multiple export formats: (1) Content negotiation via `Accept` header: `Accept: text/csv` or `Accept: application/vnd.openxmlformats-officedocument.spreadsheetml.sheet`, (2) Query parameter: `GET /users/export?format=csv`, (3) Server uses a strategy pattern to choose the serializer, (4) CSV: streams rows line by line, low memory usage, (5) Excel: uses a library (OpenXML, Apache POI), more memory, (6) For large exports: use async processing (202 Accepted), generate file, provide download link, (7) Streaming: use `Transfer-Encoding: chunked` for large datasets, (8) Pagination in export: export all pages in one file, (9) Column selection: `?fields=id,name,email&format=csv`.

**Code:**
```python
import asyncio

def gen():
    for i in range(3):
        yield i                # generator: lazy sync sequence

async def coro():
    await asyncio.sleep(0)     # coroutine: async, awaited
    return "done"

print(list(gen()))             # [0, 1, 2]
print(asyncio.run(coro()))     # done
```

## Q43: How do you implement REST API conditional request for batch operations using `If-Match`?
**A:** Conditional batch: (1) POST `/batch` with `If-Match: "batch-etag"` — the batch only executes if the collection's ETag matches, (2) The ETag represents the current state of all resources in the batch, (3) If resources changed since the client last fetched the collection, the ETag won't match, and the batch is rejected with 412 Precondition Failed, (4) The client must re-fetch the collection and reconcile, (5) Use case: reordering a list of items — prevent concurrent reorder conflicts, (6) Implementation: maintain a version number for the collection, increment on any mutation, (7) For batch operations on the same resource, use per-resource ETags.

**Code:**
```python
import functools

@functools.lru_cache(maxsize=None)
def expensive(x):
    print(f"computing {x}")
    return x * x

print(expensive(3))    # computing 3 -> 9
print(expensive(3))    # 9 (cached)
print(expensive.cache_info())
```

## Q44: How do you design a REST API that supports both JSON and XML responses with proper content negotiation?
**A:** Dual format support: (1) Client sends `Accept: application/json` or `Accept: application/xml`, (2) Server inspects `Accept` header and serializes accordingly, (3) Quality values: `Accept: application/json;q=0.9, application/xml;q=0.5` prioritizes JSON, (4) If client doesn't specify: default to JSON (modern standard), (5) The `Content-Type` response header reflects the actual format returned, (6) Serialization: use Jackson/JAXB (Java), serde (Rust), or json/xml modules in your framework, (7) XML namespaces: for enterprise APIs, define XML namespaces for versioning, (8) Error responses should also respect the Accept header, (9) Testing: test both formats for every endpoint, (10) XML is mostly legacy; consider deprecating XML support if traffic is minimal.

**Code:**
```python
from contextlib import contextmanager, closing, suppress, nullcontext

@contextmanager
def block():
    print("enter")
    try:
        yield
    finally:
        print("exit")

with block():            # contextmanager-decorated generator
    pass

class C:
    def close(self):
        print("closed")
with closing(C()):
    pass                 # close() always called

with suppress(ValueError):
    raise ValueError()   # swallowed

with nullcontext() as n:   # no-op context manager (default arg value)
    print("no-op works")
```

## Q45: How do you implement REST API event sourcing where the API itself records all state changes as events?
**A:** Event-sourced API: (1) Every mutation (POST/PUT/PATCH/DELETE) creates an event stored in an event store, (2) GET endpoints read from materialized views (projections) built from events, (3) GET `/users/123/events` returns the full event history: `[{ "event": "user_created", "timestamp": "...", "data": {...} }, { "event": "email_changed", "timestamp": "...", "data": {...} }]`, (4) POST `/events` can directly append events (admin/import use cases), (5) Rebuilding projections: POST `/admin/rebuild-projections` replays all events, (6) Immutability: events are never deleted or updated, only new events are appended, (7) Versioning: events have a version number, (8) Snapshots: periodically create snapshots to avoid replaying all events from the beginning.

**Code:**
```python
from multiprocessing import Process, Manager, Value, Queue

def worker(shared_value, shared_list, q):
    shared_value.value += 1
    shared_list.append("item")
    q.put("done")

if __name__ == "__main__":
    v = Value("i", 0)                 # shared ctypes value
    with Manager() as manager:
        shared_list = manager.list()  # shared Python list (proxy)
        q = Queue()
        procs = [Process(target=worker, args=(v, shared_list, q))
                 for _ in range(2)]
        for p in procs: p.start()
        for p in procs: p.join()
        print(v.value, list(shared_list), q.get(), q.get())
```

## Q46: How does the `Access-Control-Allow-Credentials` header impact CORS for APIs that use cookies for authentication?
**A:** Access-Control-Allow-Credentials: true is required when the API uses cookies for authentication (rather than Authorization header). Implications: (1) The client must set `credentials: 'include'` in fetch/XHR, (2) The server must respond with `Access-Control-Allow-Credentials: true`, (3) When credentials is true, `Access-Control-Allow-Origin` cannot be `*` — it must be an explicit origin, (4) `Access-Control-Allow-Headers` cannot use `*` either, (5) Vary: Origin header must be set to handle different origins, (6) Security: only set this if you actually need cookie-based auth, (7) Preflight requests are required for cross-origin credentialed requests with non-simple methods.

**Code:**
```python
class UppercaseNamespace(dict):
    def __setitem__(self, key, value):
        super().__setitem__(key.upper(), value)

class Meta(type):
    @classmethod
    def __prepare__(cls, name, bases, **kw):
        return UppercaseNamespace()       # custom class-body namespace

class Widget(metaclass=Meta):
    size = 10          # stored as 'SIZE' in the namespace

print(Widget.SIZE)     # 10
```

## Q47: How do you implement REST API pagination with total count estimation for large datasets?
**A:** Estimated total count: (1) For large datasets (millions+), exact COUNT(*) is expensive (full table scan), (2) Use database statistics: `EXPLAIN SELECT * FROM users` gives an estimated row count from the query planner, (3) Cache the count: count once, cache with TTL, (4) Approximate count: `SELECT reltuples FROM pg_class WHERE relname = 'users'` (PostgreSQL), (5) Return `total: "estimated"` or `total: null` and `total_type: "exact" | "estimated"`, (6) If exact is needed: use counting in the database with an index-only scan, (7) For cursor-based pagination, total count is not needed; just include `has_more: true/false`, (8) Always document how total is calculated.

**Code:**
```python
from functools import partial

def power(base, exponent):
    return base ** exponent

square = partial(power, exponent=2)   # fix exponent -> new callable
cube = partial(power, exponent=3)

print(square(5))    # 25
print(cube(2))      # 8
print(cube.keywords, cube.args)
```

## Q48: How do you design a REST API for a real-time collaboration feature (like Google Docs)?
**A:** Collaboration API: (1) WebSocket upgrade for real-time editing, (2) Operational Transform (OT) or CRDT for conflict resolution, (3) Initial load: GET `/documents/{id}` returns full document + version vector, (4) Changes: client sends op: `{ "op": "insert", "pos": 5, "text": "hello", "version": 42 }`, (5) Server applies, broadcasts to other connected clients, (6) Cursor awareness: broadcast cursor positions (no persistence), (7) Presence: users online, (8) Persistence: periodic snapshot + change log for crash recovery, (9) Auth: WebSocket authentication via token in query string, (10) Scalability: use Redis pub/sub for cross-server broadcasting.

**Code:**
```python
from typing import Generic, TypeVar

T = TypeVar("T")

class Box(Generic[T]):          # __class_getitem__ lets you write Box[int]
    def __getitem__(self, key):     # instance subscription: box[0]
        return f"get {key}"

print(Box[int])                # Box[int] (generic alias via class_getitem)
b = Box[int]()
print(b[0])                    # get 0 (instance __getitem__)
```

## Q49: How do you implement REST API data export with GDPR right to portability?
**A:** GDPR data export: (1) POST `/users/{id}/export` triggers a GDPR data export, (2) Response: 202 Accepted with `Location: /exports/{id}`, (3) GET `/exports/{id}` returns status, (4) When complete: download URL (signed, short-lived), (5) Format: JSON or CSV, machine-readable, structured, (6) Data included: profile, settings, activity history, content created, (7) Excluded: internal logs, analytics data not linked to user, (8) Timeframe: must be provided within 30 days (GDPR requirement), (9) Size: for large exports, generate asynchronously and email download link, (10) Cleanup: delete export files after 7 days.

**Code:**
```python
import struct

raw = bytes([1, 2, 3])

# struct packs/unpacks binary per format strings
packed = struct.pack(">2H", 300, 500)   # big-endian unsigned shorts
a, b = struct.unpack(">2H", packed)
print(a, b)                        # 300 500

ba = bytearray(raw)
ba[0] = 9
mv = memoryview(ba)                # zero-copy access
print(mv[0], bytes(raw))
```

## Q50: How do you design a REST API for an e-commerce shopping cart that handles concurrent modifications?
**A:** Cart API: (1) GET `/cart` returns cart items with ETag, (2) PUT `/cart` replaces the entire cart (idempotent), used with If-Match for concurrency, (3) PATCH `/cart` adds/removes items using JSON Patch, (4) POST `/cart/items` adds a single item (simpler for clients), (5) Concurrency: last-write-wins for carts is common (risk: lost updates), (6) Better: use ETag + If-Match for PUT, reject stale modifications with 412, (7) Price validation: re-validate prices on checkout (prices may have changed), (8) Stock check: on add-to-cart, validate stock availability, (9) Expiration: remove items from cart if stock runs out, (10) Saved cart: POST `/carts/{id}/save` for wishlist functionality.

**Code:**
```python
# util.py
__all__ = ["public_fn", "VISIBLE"]    # controls `from util import *`

def public_fn():
    return "public"

def _private_fn():
    return "private"

VISIBLE = True

from util import *     # in another module, only __all__ names come in
```

## Q51: How do you implement REST API request validation that returns all validation errors at once (not fail-fast)?
**A:** Comprehensive validation: (1) Validate all fields before returning errors (not fail on first error), (2) Collect errors in a list: `{ "errors": [{ "field": "email", "code": "INVALID_FORMAT" }, { "field": "age", "code": "MIN_VALUE", "constraint": 18 }] }`, (3) Use a validation library that supports collecting multiple errors (JSR 380 Bean Validation, Pydantic, Joi), (4) Validate nested objects recursively, (5) Validate query parameters, path parameters, and body, (6) Return 422 Unprocessable Entity for validation errors, (7) Include a summary: `"error_count": 5`, (8) For security: don't reveal internal schema details in errors (e.g., database field names), (9) Performance: validate at the API gateway or middleware layer, before reaching business logic.

**Code:**
```python
def classify(value):
    match value:
        case 0:                     # literal pattern
            return "zero"
        case [x, y]:                # sequence pattern
            return f"pair {x},{y}"
        case {"name": n}:           # mapping pattern
            return f"named {n}"
        case int() as i if i > 0:   # class pattern + guard
            return "positive int"
        case _:                     # wildcard
            return "something else"

print(classify(0))
print(classify([1, 2]))
print(classify({"name": "Ada"}))
print(classify(5))
```

## Q52: How do you design a REST API for a multi-currency payment system?
**A:** Multi-currency API: (1) All amounts are integers (smallest currency unit: cents, paise, etc.), (2) Include `currency` field as ISO 4217 code (USD, EUR, JPY), (3) Exchange rates: GET `/rates?from=USD&to=EUR` returns current rate, (4) Conversion: POST `/conversions` with `{ "amount": 1000, "from": "USD", "to": "EUR" }`, (5) Rounding: specify rounding rules per currency (JPY has no decimal, BHD has 3 decimals), (6) Display: include both `amount` (cents) and `amount_display` (with decimal point: "10.00"), (7) Multi-currency cart: prices stored in base currency, displayed in user's preferred currency, (8) Idempotency: critical for payment operations, (9) Smallest unit: clearly document that all amounts are in the smallest currency unit.

**Code:**
```python
class Point:
    __match_args__ = ("x", "y")     # enables positional class patterns
    def __init__(self, x, y):
        self.x, self.y = x, y

def where(pt):
    match pt:
        case Point(0, 0):
            return "origin"
        case Point(x, y):
            return f"({x}, {y})"

print(where(Point(0, 0)))     # origin
print(where(Point(1, 2)))     # (1, 2)
```

## Q53: How do you implement REST API IP allowlisting and geo-blocking?
**A:** IP-based access control: (1) Allowlist: maintain a list of allowed IPs/CIDR ranges, (2) Denylist: block known malicious IPs, (3) Geo-blocking: use GeoIP database to determine request origin, block/allowed countries, (4) Implementation: middleware at the API gateway level (not in application code), (5) For cloud: use security groups (AWS), Cloud Armor (GCP), or API Gateway IP whitelist, (6) For self-hosted: NGINX `allow/deny` directives or iptables, (7) Response: 403 Forbidden for blocked IPs, (8) Consider CDN: client IP may be the CDN's IP; use `X-Forwarded-For` header correctly, (9) Dynamic changes: allowlist changes should propagate quickly (API for updates), (10) Audit: log all blocked requests for security analysis.

**Code:**
```python
data = [1, 2, 3, 4, 5]

if (n := len(data)) > 3:          # assigns n, avoids calling len twice
    print(f"length {n}")

total = (t := sum(data))          # also useful in while loops:
print(t)                          # while (line := f.readline()): ...
```

## Q54: How do you design a REST API for a notification preference center (opt-in/opt-out)?
**A:** Notification preferences: (1) GET `/users/{id}/notification_preferences` returns current preferences, (2) PUT/PATCH updates preferences partially, (3) Schema: `{ "email": { "order_confirmed": true, "marketing": false }, "sms": { "order_confirmed": true }, "push": { "all": false } }`, (4) Global opt-out: `{ "email": { "enabled": false } }` disables all email, (5) Unsubscribe links: include `[{ "type": "email", "url": "https://api.example.com/unsubscribe?token=..." }]` in preference response for easy unsubscribe, (6) Default preferences: set during registration (all essential, no marketing), (7) Validation: check that notification types exist, (8) Consent tracking: log when and how preferences changed, (9) Rate limiting: don't send more than X emails per day per user.

**Code:**
```python
# pyproject.toml
# [build-system]
# requires = ["setuptools>=68"]
# build-backend = "setuptools.build_meta"
# [project]
# name = "mypkg"
# dependencies = ["requests>=2.31"]

# modern packaging config replaced setup.py/setup.cfg/requirements.txt
```

## Q55: How do you implement REST API content negotiation for language localization (i18n)?
**A:** Language localization: (1) Accept-Language header: `Accept-Language: fr-CA, fr;q=0.9, en;q=0.8`, (2) Server parses quality values and selects the best matching locale, (3) Response: `Content-Language: fr-CA`, (4) Translated content: error messages, field labels, datetime formats, (5) For data (user-generated content), language is part of the resource: GET `/articles/123?language=en`, (6) Resource-level language: `Accept-Language` can select between available translations, (7) Fallback: if requested language is not available, fall back to default (en), (8) Locale-aware sorting: use collation for proper sorting in different languages, (9) Testing: test with different Accept-Language values to verify fallback behavior.

**Code:**
```python
import numpy as np   # (illustrative; numpy exposes the buffer protocol)

buf = bytearray(b"abcdef")
mv = memoryview(buf)         # zero-copy view
mv[0] = ord("X")             # writes straight into buf
print(buf)                   # bytearray(b'Xbcdef')
slice32 = memoryview(buf).cast("i")   # reinterpret without copying
print(slice32.tolist())
```

## Q56: How do you design a REST API for a subscription billing system with proration?
**A:** Subscription billing API: (1) Plans: GET `/plans` lists available plans with prices, (2) Subscribe: POST `/subscriptions` with `{ "plan_id": "pro", "interval": "month" }`, (3) Proration: PATCH `/subscriptions/{id}` with `{ "plan_id": "enterprise" }` — server calculates prorated credit/due, (4) Proration response: `{ "credit": 500, "charge": 2000, "next_billing_date": "2024-02-15" }`, (5) Invoice: GET `/invoices/{id}` provides line items for proration, (6) Coupons: POST `/subscriptions/{id}/coupons` with coupon code, (7) Cancellation: DELETE `/subscriptions/{id}` at period end (with immediate option), (8) Webhook: notify on `subscription.updated`, `payment.failed`, (9) Dunning: automatic retry on failed payment with escalation.

**Code:**
```python
class Normal:
    pass

class Slotted:
    __slots__ = ("x",)

n, s = Normal(), Slotted()
print(hasattr(n, "__dict__"))    # True - dynamic attribute storage
print(hasattr(s, "__dict__"))    # False - fixed slots instead
# s.y = 1  -> AttributeError
```

## Q57: How do you implement REST API audit logging with before/after snapshots?
**A:** Audit logging: (1) Middleware intercepts all mutating requests (POST, PUT, PATCH, DELETE), (2) Before mutation: capture resource state (before snapshot), (3) After mutation: capture new state (after snapshot), (4) Log entry: `{ "actor": "user_123", "action": "update", "resource": "order", "resource_id": "ORD-456", "before": {...}, "after": {...}, "timestamp": "...", "ip": "1.2.3.4", "request_id": "req-789" }`, (5) Sensitive field masking: never log passwords, tokens, or PII in before/after, (6) Storage: dedicated audit log database or log aggregation system, (7) Retention: 1-7 years depending on compliance, (8) Query: search by actor, resource, action, time range, (9) Immutable: audit logs should be append-only, (10) Performance: async write to avoid impacting API response time.

**Code:**
```python
import logging
import sys

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)

logger = logging.getLogger("app")
logger.info("started with %s", "workers=4")   # lazy formatting
logger.warning("disk low: %d%%", 5)
```

## Q58: How do you design a REST API that supports idempotent key rotation?
**A:** Idempotency key rotation: (1) Keys have a TTL (e.g., 24 hours after first use), (2) Clients should generate a new key for each unique operation, (3) After a successful response, the key can be reused after the TTL expires, (4) For payment operations: keys should be unique per payment attempt, (5) If the client needs to retry with a different key (key lost), they must cancel the previous operation first, (6) Key collision: return 409 Conflict if the same key is used for a different operation, (7) Key format: UUIDv4 or server-generated pre-approval tokens, (8) Key storage: encrypted or hashed for security, (9) Key cleanup: background job removes expired keys.

**Code:**
```python
import threading

# C extensions can release the GIL around heavy loops;
# this lets other threads run concurrently:
import numpy as np

arr = np.arange(10_000_000)
# numpy releases the GIL during arr.sum() -> threads can run in parallel
print(arr.sum() % 1000)

# pure-Python CPU loops hold the GIL, so they serialize
```

## Q59: How do you implement REST API data seeding for integration tests?
**A:** Test data seeding: (1) POST `/testing/setup` with `{ "users": [...], "orders": [...] }` creates test data in one call, (2) DELETE `/testing/teardown` removes all test data, (3) `X-Testing: true` header indicates test mode (enables/disables side effects like emails), (4) Factories: GET `/testing/factories/users` returns a template with random valid data, (5) Snapshot: POST `/testing/snapshots` captures current state, POST `/testing/restore/{snapshot_id}` restores, (6) Isolation: each test run gets a unique namespace or database, (7) Rate limiting: testing endpoints should bypass rate limits but require special auth, (8) Documentation: clearly mark testing endpoints and disable in production.

**Code:**
```python
import tracemalloc

tracemalloc.start()
big = [bytearray(1000) for _ in range(100)]
current, peak = tracemalloc.get_traced_memory()
print(f"current={current/1024:.0f}KB peak={peak/1024:.0f}KB")

snapshot = tracemalloc.take_snapshot()
for stat in snapshot.statistics("lineno")[:5]:
    print(stat)
```

## Q60: How do you design a REST API for a file conversion service (e.g., PDF to DOCX)?
**A:** File conversion API: (1) POST `/conversions` with file upload and target format: `{ "format": "docx" }` returns conversion ID, (2) GET `/conversions/{id}` returns status (pending, processing, completed, failed) and progress percentage, (3) When completed, GET `/conversions/{id}/download` returns the converted file, (4) Supported formats: GET `/conversions/formats` lists supported input/output pairs, (5) Options: `?quality=high&page_range=1-5` for PDF-specific conversions, (6) Webhook: POST callback URL receives conversion result, (7) Limits: max file size, max pages, conversions per day, (8) Cleanup: delete source and converted files after TTL (24 hours), (9) Processing: async with worker queue.

**Code:**
```python
import asyncio

async def inner():
    await asyncio.sleep(0)
    return 42

async def main():
    # await calls __await__() on the awaitable internally
    result = await inner()
    print(result)

asyncio.run(main())
```

## Q61: How does the `Sec-Fetch-*` metadata header suite help REST APIs detect CSRF and XSSI attacks?
**A:** Sec-Fetch headers (Fetch Metadata Request Headers) provide context about the request's origin: (1) `Sec-Fetch-Site: cross-site` vs `same-origin` vs `same-site` vs `none`, (2) `Sec-Fetch-Mode: navigate` vs `same-origin` vs `cors` vs `no-cors`, (3) `Sec-Fetch-Dest: document` vs `empty` vs `script` vs `image`, (4) `Sec-Fetch-User: ?1` (user initiated navigation), (5) Server-side validation: reject requests where Sec-Fetch-Site is cross-site and Sec-Fetch-Mode is navigate (CSRF), (6) Reject requests where Sec-Fetch-Dest is script for JSON endpoints (XSSI), (7) Support: all modern browsers send these headers; servers can enforce policies, (8) Fallback: if headers are absent (HTTP clients, old browsers), apply standard CSRF protections.

**Code:**
```python
import subprocess

res = subprocess.run(["echo", "hello"], capture_output=True, text=True)
print(res.stdout)              # hello
print(res.returncode)          # 0

p = subprocess.Popen(["grep", "py"],
                     stdout=subprocess.PIPE,
                     text=True)
out, err = p.communicate()
print(out)
```

## Q62: How do you implement REST API data masking for sensitive fields in responses?
**A:** Data masking: (1) Email: `j***@example.com`, (2) Phone: `+1 (***) ***-1234`, (3) SSN: `***-**-1234`, (4) Credit card: `****-****-****-1234`, (5) Implementation: annotation-driven (`@Masked(type=EMAIL)`) or middleware that masks based on field patterns, (6) Unmasked access: for authorized roles (admin, support), return the full value, (7) Audit: log when masked fields are accessed in full, (8) Consistency: mask consistently across all endpoints (list and detail), (9) Search: allow searching by masked values? (e.g., last 4 digits of phone), (10) Response: return masked values always unless explicit role allows unmasked access.

**Code:**
```python
name = "Ada"
print(f"Hi {name}")              # works fine

# Pre-3.12 limits: no backslashes inside {} ...
nl = "\n"
print(f"a{nl}b")                  # workaround: assign to a variable

# ... and use str.format() or %-style for dynamic templates:
tpl = "name={name} age={age}"
print(tpl.format(name="Ada", age=36))
```

## Q63: How do you design a REST API for a discussion forum with threading and moderation?
**A:** Forum API: (1) Threads: GET/POST/PUT/DELETE `/threads`, (2) Posts: GET/POST/PUT/DELETE `/threads/{id}/posts`, (3) Nesting: each post has `parent_id` for threading, (4) Pagination: nested replies paginated separately from top-level, (5) Moderation: POST `/posts/{id}/report`, POST `/posts/{id}/moderate` (delete, hide, warn), (6) Voting: POST `/posts/{id}/vote` with `{ "direction": "up" | "down" }`, (7) Pinning: PATCH `/threads/{id}` with `{ "pinned": true }`, (8) Locking: PATCH `/threads/{id}` with `{ "locked": true }` prevents new replies, (9) Spam detection: check content against spam patterns, rate-limit posting, (10) Notifications: POST `/subscriptions` to follow thread.

**Code:**
```python
class MyDict(dict):
    def __missing__(self, key):       # hooks dict[key] when key absent
        return f"default for {key}"

d = MyDict(a=1)
print(d["a"])          # 1
print(d["nope"])       # default for nope
```

## Q64: How do you implement REST API pagination with `Prefer: count=exact` for optional total count?
**A:** Optional total count: (1) Client sends `Prefer: count=exact` to request an exact total count, (2) Default response (without header) uses estimated count or omits total, (3) Server responds with `Preference-Applied: count=exact` and includes the total count, (4) This avoids expensive COUNT(*) queries for clients that don't need the total, (5) For paginated lists: always include `has_more: bool` (cheap to check with LIMIT + 1), (6) The exact count can be expensive for large tables — add a timeout or fall back to estimate, (7) Rate limit: requests with `Prefer: count=exact` may count as more expensive requests, (8) Cache: cache exact counts with TTL.

**Code:**
```python
class BaseModel:
    cache = {}

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.cache[cls.__name__] = cls

class User(BaseModel): pass
class Order(BaseModel): pass

print(BaseModel.cache)   # {'User': ..., 'Order': ...} auto-registered
```

## Q65: How do you design a REST API for a social media feed with algorithmic ranking?
**A:** Feed API: (1) GET `/feed` returns personalized feed based on user's preferences/following, (2) `?limit=20&cursor=...` for cursor-based pagination, (3) Ranking: server-side algorithm (recency, relevance, engagement), (4) Filtering: `?content_types=post,article,video`, (5) Interactions: POST `/feed/items/{id}/like`, POST `/feed/items/{id}/share`, (6) Hide: POST `/feed/items/{id}/hide` removes from feed, (7) Report: POST `/feed/items/{id}/report`, (8) Refresh: GET `/feed?refresh=true` returns fresh content maintaining read state, (9) Polling: GET `/feed/poll?since=<timestamp>` for incremental updates, (10) Performance: pre-compute feeds for active users, cache heavily.

**Code:**
```python
import asyncio

def gen():
    yield from range(3)          # yield from: delegate to subgenerator

async def coro():
    await asyncio.sleep(0)       # await: suspend until awaitable done
    return "ok"

print(list(gen()))               # [0, 1, 2]
print(asyncio.run(coro()))       # ok
```

## Q66: How do you implement REST API graceful degradation (circuit breaker pattern)?
**A:** Graceful degradation: (1) Downstream service fails: return cached response if available, (2) Circuit breaker states: closed (normal), open (failing, reject immediately), half-open (test recovery), (3) Degraded response: include `X-Degraded: true` header and `{ "degraded": true, "data": [...] }` in body, (4) Partial data: if one service fails, return data from other services with degradation indicator, (5) Stale data: serve cached data with `Warning: 299 api.example.com "Stale data"` header, (6) Fallback: provide simplified responses when full data is unavailable, (7) Monitoring: track degradation rate, (8) API contract: document which endpoints can degrade and what the degraded response looks like.

**Code:**
```python
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

def task(i):
    time.sleep(0.1)
    return i * i

with ThreadPoolExecutor(max_workers=4) as pool:
    futs = [pool.submit(task, i) for i in range(4)]
    for f in as_completed(futs):     # yields futures as they finish
        print(f.result())
```

## Q67: How do you design a REST API for a video streaming platform?
**A:** Video streaming API: (1) Upload: POST `/videos` with multipart upload or resumable upload, (2) Transcoding: POST `/videos/{id}/transcode` with quality presets, (3) Manifest: GET `/videos/{id}/manifest` returns HLS/DASH manifest URL, (4) Streaming: GET `/videos/{id}/stream` redirects to CDN, (5) Thumbnails: GET `/videos/{id}/thumbnails?time=30s`, (6) Metadata: title, description, tags, categories, (7) Playlists: POST `/playlists` with video IDs ordered, (8) Analytics: POST `/analytics/plays` with play event (client-side beacon), (9) DRM: POST `/licenses` for Widevine/PlayReady license, (10) Adaptive bitrate: manifest lists multiple quality levels; client switches automatically.

**Code:**
```python
import asyncio

async def agen():
    for i in range(3):
        await asyncio.sleep(0)   # allowed inside async generator
        yield i

async def main():
    async for x in agen():       # async for: iterate over async iterable
        print(x)

    async with fetch() as s:     # async with: async context manager
        print(s)

asyncio.run(main())
```

## Q68: How do you implement REST API webhook security using signature verification and replay protection?
**A:** Webhook security: (1) Signature: HMAC-SHA256 of the raw request body using a shared secret, sent in `X-Signature-256` header, (2) Timestamp: include `X-Event-Timestamp` in header, (3) Replay protection: receiver checks timestamp deviation (within 5 minutes), (4) Nonce: include `X-Event-Id` (UUID), receiver deduplicates by this ID, (5) Verification: `expected_sig = hmac.new(secret, timestamp + '.' + body, hashlib.sha256).hexdigest()`, (6) Key rotation: support multiple keys by including key ID in the header, (7) HTTPS only: webhooks should only be delivered to HTTPS endpoints, (8) IP allowlisting: suggest receivers allowlist webhook sender IPs, (9) Retry: exponential backoff for delivery failures.

**Code:**
```python
class ListNamespace(dict):
    pass

class Meta(type):
    @classmethod
    def __prepare__(cls, name, bases, **kw):
        return ListNamespace()    # namespace dict used during class body

class Widget(metaclass=Meta):
    a = 1
    b = a + 1        # class body runs against the prepared namespace

print(Widget.a, Widget.b)   # 1 2
```

## Q69: How do you design a REST API that supports both flat and nested resource creation in a single request?
**A:** Compound document creation: (1) POST `/orders` with nested resources: `{ "customer": { "name": "John", "email": "john@example.com" }, "items": [{ "product_id": 1, "quantity": 2 }], "shipping_address": { "street": "123 Main St", ... } }`, (2) Server creates all resources atomically (in a transaction), (3) Response includes all created resources with their IDs, (4) Server resolves relationships (e.g., links order to customer), (5) Validation: validate all nested resources, return all errors, (6) Limits: max nesting depth (3 levels), max items per request (100), (7) Atomicity: either all resources are created or none, (8) idempotency: idempotency key applies to the entire compound operation, (9) JSON:API supports compound documents with `include` and `relationships`.

**Code:**
```python
class Value:
    def __init__(self, n):
        self.n = n
    def __eq__(self, other):                # == compares VALUE
        return isinstance(other, Value) and self.n == other.n
    def __hash__(self):                     # consistent with __eq__
        return hash(self.n)

a, b = Value(5), Value(5)
print(a == b)     # True - value equality
print(a is b)     # False - different identity
```

## Q70: How do you implement REST API requests that preload related resources (eager loading)?
**A:** Eager loading: (1) `GET /orders?include=customer,items.product` returns orders with customer and product details embedded, (2) Server resolves includes and embeds them in the response, (3) Format: `{ "data": [...], "included": { "customer": {...}, "product": {...} } }` (JSON:API style), or embedded directly within each resource, (4) Nested includes: `include=customer.addresses`, (5) Limits: max include depth, max included resources per request, (6) Performance: use database eager loading (JOINs or batch loading) to avoid N+1 queries, (7) Caching: vary cache key by include parameter, (8) Sparse fieldsets: combine with `fields[customer]=id,name` to limit included fields.

**Code:**
```python
import pickle

class Rebuildable:
    def __init__(self, names):
        self.names = names
    def __reduce__(self):             # controls (de)serialization
        return (Rebuildable, (self.names,))

obj = Rebuildable(["a"])
print(pickle.loads(pickle.dumps(obj)).names)   # ['a']
# __reduce_ex__(protocol) preferred when customizing per protocol
```

## Q71: How does the HTTP `Forwarded` header work for REST APIs behind proxies?
**A:** The Forwarded header (RFC 7239) standardizes how proxies forward client information. Format: `Forwarded: for=192.0.2.60; proto=https; by=203.0.113.43; host=api.example.com`. Components: (1) `for`: the original client IP, (2) `proto`: the original protocol (http/https), (3) `by`: the proxy that forwarded the request, (4) `host`: the original Host header value. Legacy alternatives: `X-Forwarded-For`, `X-Forwarded-Proto`, `X-Forwarded-Host`. Server should: (1) Trust the last proxy in the chain (not the first), (2) Validate that the proxy is trusted (IP allowlist), (3) Use the forwarded values for rate limiting, geo-IP, and logging.

**Code:**
```python
class Meta(type):
    def __instancecheck__(cls, instance):
        return hasattr(instance, "quack")   # structural, not real subclass
    def __subclasscheck__(cls, subclass):
        return hasattr(subclass, "moo")

class Duck(metaclass=Meta): pass

class Mallard:
    def quack(self): pass

class Cow: pass
print(isinstance(Mallard(), Duck))   # True - has quack
print(isinstance(Cow(), Duck))       # False
```

## Q72: How do you design a REST API for a product inventory system with real-time stock updates?
**A:** Inventory API: (1) GET `/products/{id}/inventory` returns current stock level and warehouse locations, (2) Stock reservation: POST `/reservations` reserves stock for a pending order (TTL: 15 minutes), (3) Stock deduction: POST `/inventory/deductions` on order confirmation, (4) Restock: POST `/inventory/receipts` for incoming stock, (5) Real-time: WebSocket or SSE for stock level changes, (6) Low stock alerts: GET `/inventory/alerts?threshold=10`, (7) Multi-warehouse: include `warehouse_id` in inventory operations, (8) Hold calculation: `available = on_hand - reserved - quality_hold`, (9) Concurrency: use optimistic locking for stock updates (prevent overselling), (10) Auditing: full inventory transaction log.

**Code:**
```python
text = "café"                # Python 3 str stores unicode directly
encoded = text.encode("utf-8")    # str -> bytes
print(encoded)                    # b'caf\xc3\xa9'
print(encoded.decode("utf-8"))    # bytes -> str
print("spam".encode("ascii"))     # pure ASCII round-trips fine
```

## Q73: How do you implement REST API content-addressable storage (immutable resources keyed by hash)?
**A:** Content-addressable API: (1) POST `/contents` with binary data, server returns `{ "hash": "sha256-abc123..." }`, (2) GET `/contents/{hash}` retrieves the content, (3) If the same content is uploaded again, the same hash is returned (deduplication), (4) Immutable: content cannot be updated or deleted (append-only), (5) Metadata: PUT `/contents/{hash}/metadata` with content type, description, (6) References: other resources reference content by hash: `{ "avatar_hash": "sha256-abc123" }`, (7) GC: background job removes content not referenced by any resource, (8) Benefits: deduplication, cache-friendly (hash never changes), integrity verification, (9) Use cases: file storage, package registries, artifact repositories.

**Code:**
```python
from typing import Generic, TypeVar

T = TypeVar("T")

class Registry(Generic[T]):       # Generic supplies __class_getitem__
    pass

r = Registry[int]                # Registry[int] works
print(r)
# list[int] on built-ins (Python 3.9+) also uses __class_getitem__:type
```

## Q74: How do you design a REST API for a real-time leaderboard?
**A:** Leaderboard API: (1) GET `/leaderboards/daily?date=2024-01-15&limit=100` returns top players with rank, score, and player info, (2) GET `/leaderboards/daily/players/{id}` returns a player's rank and surrounding players, (3) Score update: POST `/scores` with `{ "player_id": "abc", "score": 1500, "game_id": "xyz" }`, (4) Real-time: WebSocket for live score updates, (5) Ranking types: daily, weekly, all-time, friends-only, (6) Ties: tie-breaking rule (earliest to reach score wins), (7) Performance: use Redis sorted sets for real-time leaderboards, (8) Persistence: periodic snapshot to database, (9) Caching: cache top 100 with short TTL.

**Code:**
```python
import sys

def trace(frame, event, arg):
    if event == "call":
        print("calling", frame.f_code.co_name)
    return trace

def add(a, b):
    return a + b

sys.settrace(trace)       # trace per-line / per-call
add(1, 2)
sys.settrace(None)        # stop tracing
```

## Q75: How do you implement REST API self-descriptive error responses with error documentation URLs?
**A:** Self-descriptive errors: (1) Each error code maps to a documentation URL, (2) Response: `{ "error": { "code": "INVALID_PARAMETER", "message": "Invalid email format", "docs_url": "https://docs.api.example.com/errors/INVALID_PARAMETER", "request_id": "req-abc" } }`, (3) The docs URL explains the error, common causes, and how to fix it, (4) For validation errors: include which field is invalid and the constraint, (5) For rate limiting: include rate limit headers and docs on best practices, (6) For server errors: include the request ID for support reference, (7) Stability: error codes are part of the API contract and should not change without a new version, (8) i18n: the message can be localized, but the code remains the same.

**Code:**
```python
from contextlib import contextmanager

@contextmanager
def managed():
    print("setup")             # __enter__
    try:
        yield "resource"       # yielded once; caller binds via `as`
    finally:
        print("teardown")      # __exit__

with managed() as r:
    print(r)
```

## Q76: How do you design a REST API for a geocoding / reverse geocoding service?
**A:** Geocoding API: (1) Forward: GET `/geocode?q=1600+Amphitheatre+Parkway,+Mountain+View,+CA`, (2) Reverse: GET `/reverse?lat=37.422&lng=-122.084`, (3) Response: `{ "results": [{ "formatted_address": "...", "lat": 37.422, "lng": -122.084, "components": { "street_number": "1600", "route": "Amphitheatre Pkwy", "locality": "Mountain View", "admin_area": "CA", "country": "US", "postal_code": "94043" }, "bbox": {...} }] }`, (4) Autocomplete: GET `/autocomplete?q=1600+Amphi` for typeahead, (5) Batch: POST `/geocode/batch` with up to 100 addresses, (6) Rate limit: strict limits (geocoding is expensive), (7) Cache: cache geocoding results aggressively, (8) Attribution: many providers require attribution in the response.

**Code:**
```python
from typing import Protocol, runtime_checkable
from abc import ABC, abstractmethod

@runtime_checkable
class Drawable(Protocol):        # structural: anything with draw() is a Drawable
    def draw(self): ...

class Circle:                    # no inheritance needed
    def draw(self): pass

@runtime_checkable
class Quackable(Protocol):
    def quack(self): ...

print(isinstance(Circle(), Drawable))   # True

class Animal(ABC):               # nominal: explicit subclassing required
    @abstractmethod
    def move(self): ...
```

## Q77: How do you implement REST API performance budget enforcement via response headers?
**A:** Performance budget: (1) Server measures response time and includes `X-Response-Time: 45ms`, (2) Optionally include `X-Performance-Budget: { "actual": 45, "budget": 100, "status": "pass" }`, (3) If response exceeds the budget, return `X-Performance-Budget: { "status": "fail", "warning": "Response time exceeded 100ms budget" }`, (4) The budget is per-endpoint and configurable, (5) For bulk/list endpoints: budget scales with result count, (6) For degraded performance: return 200 with the response but include a warning, (7) Monitoring: track budget violations over time, (8) Alerting: notify team if budget is consistently exceeded.

**Code:**
```python
import asyncio

async def produce():
    for i in range(3):
        await asyncio.sleep(0)     # async op between yields
        yield i * 10

async def main():
    # async generator: async def + yield, iterated with async for
    async for item in produce():
        print(item)

asyncio.run(main())
```

## Q78: How do you design a REST API that supports resource locking for collaborative editing?
**A:** Collaborative locking: (1) Lock acquisition: POST `/resources/{id}/lock` with `{ "ttl": 300 }` returns lock token, (2) Lock renewal: PUT `/resources/{id}/lock/{token}` refreshes the TTL, (3) Lock release: DELETE `/resources/{id}/lock/{token}`, (4) Lock check: GET `/resources/{id}/lock` returns current lock holder (or 404 if unlocked), (5) Mutations with lock: PATCH `/resources/{id}` with `If: <lock-token>` header, (6) Timeout: locks auto-release after TTL (heartbeat required), (7) Force release: POST `/resources/{id}/lock/force` (admin only), (8) Lock waiting: POST `/resources/{id}/lock?wait=true` blocks until lock is available, (9) WebSocket: lock state changes broadcast via WebSocket, (10) Conflict: if no lock, use optimistic concurrency with ETag.

**Code:**
```python
import functools

def traced(func):
    @functools.wraps(func)         # copies func onto wrapper AND sets __wrapped__
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

@traced
def hello():
    return "hi"

print(hello())
print(hello.__wrapped__)           # the original function is reachable
print(hello.__wrapped__())
```

## Q79: How do you implement REST API schema evolution with backward-compatible changes?
**A:** Backward-compatible changes: (1) Adding new fields: always safe (clients ignore unknown fields), (2) Adding new endpoints: always safe, (3) Adding optional query parameters: safe, (4) Making required fields optional: safe, (5) Widening types: int32 to int64, string length limit increase, (6) Deprecation: mark fields as deprecated in docs but keep them working, (7) Removing fields: add `deprecated: true` and `x-deprecation-date` in OpenAPI spec, keep the field for at least one major version cycle, (8) Renaming fields: add the new field alongside the old one, remove the old after migration, (9) Changing enum values: add new values, never remove, (10) Response format: never change existing field types, response structure, or status codes.

**Code:**
```python
from operator import attrgetter, itemgetter
import functools

class Person:
    def __init__(self, name, age):
        self.name, self.age = name, age
    def __repr__(self):
        return f"{self.name}({self.age})"

people = [Person("bob", 30), Person("ada", 25)]

print(sorted(people, key=attrgetter("age")))     # key function
print(sorted(people, key=lambda p: p.name))      # lambdas work too

# cmp_to_key adapts an old-style comparator
print(sorted([3, 1, 2], key=functools.cmp_to_key(lambda a, b: b - a)))
```

## Q80: How do you design a REST API for a referral/affiliate tracking system?
**A:** Referral API: (1) GET `/referrals/codes` returns user's referral codes, (2) POST `/referrals/codes` generates a new code for a campaign, (3) GET `/referrals/leaderboard` top referrers, (4) GET `/referrals/conversions` lists referred users and rewards, (5) Attribution: last-touch or first-touch model, (6) Cookie tracking: referral link sets a cookie with referrer ID and campaign, (7) Conversion: POST `/referrals/conversions` with `{ "referred_user_id": 456, "referral_code": "ABC123" }`, (8) Reward: POST `/referrals/rewards` grants referral bonus, (9) Fraud detection: IP check, device fingerprint, conversion velocity limits, (10) Payout: GET `/referrals/payouts` for balance and withdrawal history.

**Code:**
```python
import pickle

class Session:
    def __getstate__(self):              # what to pickle away
        return self.__dict__             # default: instance dict

    def __setstate__(self, state):       # restore after unpickling
        self.__dict__.update(state)

s = Session()
s.user = "ada"
restored = pickle.loads(pickle.dumps(s))
print(restored.user)   # ada
```

## Q81: How does the `Timing-Allow-Origin` header affect performance measurement of REST APIs?
**A:** Timing-Allow-Origin enables cross-origin performance measurement. Without this header, browser-side JavaScript cannot access timing data (Resource Timing API) for API calls to different origins. (1) The server sets `Timing-Allow-Origin: https://myapp.com` or `*`, (2) This exposes resource timing metrics (DNS lookup, TCP handshake, TLS negotiation, response time), (3) Without this header, `performance.getEntriesByType('resource')` reports 0 for all timing metrics on cross-origin requests, (4) Use for: monitoring real user monitoring (RUM) performance from the browser, (5) Security: restrict to specific origins rather than using wildcard, (6) Combine with `Access-Control-Expose-Headers: Timing-Allow-Origin`.

**Code:**
```python
# constructor injection (the idiomatic Python approach)
class Engine:
    def start(self):
        return "engine started"

class Car:
    def __init__(self, engine):   # dependency passed in, not hard-coded
        self.engine = engine
    def drive(self):
        return self.engine.start()

car = Car(Engine())
print(car.drive())
```

## Q82: How do you implement REST API differential updates using JSON Merge Patch (RFC 7396)?
**A:** JSON Merge Patch: (1) PATCH `/users/123` with `Content-Type: application/merge-patch+json`, (2) Body: `{ "name": "New Name", "email": null }` — sets name, removes email, (3) Semantics: null means remove the field, absent fields are unchanged, (4) Differences from JSON Patch (RFC 6902): merge patch is simpler (just the diff), but cannot express complex operations (like array insert at index), (5) Response: 200 OK with the full updated resource, (6) Idempotency: JSON Merge Patch is not inherently idempotent (two patches may produce different results), (7) Use JSON Merge Patch for simple partial updates, JSON Patch for complex transformations (arrays, deep nesting).

**Code:**
```python
import gc

class Node:
    def __init__(self):
        self.peer = None

a, b = Node(), Node()
a.peer = b
b.peer = a          # cycle; both define no __del__ -> fine for GC

del a, b
print(gc.collect())  # 3.4+ can collect cycles that include __del__
```

## Q83: How do you design a REST API for a voucher/discount code system?
**A:** Voucher API: (1) CRUD: GET/POST/PUT/DELETE `/vouchers` for voucher codes, (2) Validation: POST `/vouchers/validate` with `{ "code": "SAVE20", "cart_total": 10000, "items": [...] }`, (3) Response: `{ "valid": true, "discount": { "type": "percentage", "value": 20, "max_discount": 5000 }, "description": "20% off up to $50" }`, (4) Usage: POST `/vouchers/redeem` applies to order (with idempotency), (5) Constraints: minimum order value, first-time customer, specific products, date range, usage limit, (6) Stacking: can this voucher be combined with others?, (7) Generation: POST `/vouchers/generate` with `{ "count": 100, "prefix": "SUMMER", "expires_at": "..." }`, (8) Analytics: GET `/vouchers/analytics` for redemption rate, revenue impact.

**Code:**
```python
import asyncio

async def background():
    await asyncio.sleep(0.1)
    return "done"

async def main():
    # create_task: schedule a coroutine on the current loop
    t = asyncio.create_task(background())
    # ensure_future: accepts task/future/coroutine and wraps as needed
    fut = asyncio.ensure_future(background())
    await asyncio.gather(t, fut)

asyncio.run(main())
```

## Q84: How do you implement REST API request deduplication based on request body content?
**A:** Content-based deduplication: (1) Server hashes the request body (SHA-256) and uses it as a deduplication key, (2) Combined with endpoint path and authentication context, (3) If the same hash is seen within a time window (e.g., 5 seconds), return the cached response, (4) This handles duplicate POST requests without requiring the client to send an idempotency key, (5) Risks: (a) two different requests with the same body are treated as duplicate (false positive), (b) body must be buffered to compute hash (memory overhead for large payloads), (6) Usually safer to use explicit Idempotency-Key header instead, (7) Use content-based dedup only for specific endpoints where identical requests are truly duplicate (e.g., analytics events, logging).

**Code:**
```python
import sys

def hook(exc_type, exc, tb):
    print("uncaught:", exc_type.__name__, exc)
    sys.exit(1)

sys.excepthook = hook
raise ValueError("boom")     # instead of default traceback, hook runs
```

## Q85: How do you design a REST API for a real-time search autocomplete/suggest?
**A:** Autocomplete API: (1) GET `/suggest?q=sho&limit=5` returns completions: `["shoes", "shorts", "shopping cart"]`, (2) Prefix matching: returns terms starting with the query, (3) Frequency ranking: most popular/most relevant first, (4) Personalization: include user's past searches in suggestions, (5) Categories: `GET /suggest?q=sho&type=product,category`, (6) Each suggestion: `{ "text": "shoes", "type": "product", "category": "Footwear" }`, (7) Performance: responses in <50ms, use in-memory trie or Elasticsearch suggest, (8) Cache: cache common prefixes, (9) Rate limit: higher limits for autocomplete (many keystrokes), (10) Debouncing: client-side debounce (300ms) before calling API.

**Code:**
```python
from dataclasses import dataclass

@dataclass(frozen=True)          # generates __setattr__ that raises
class Point:
    x: int
    y: int

p = Point(1, 2)
print(p)
# p.x = 3   -> FrozenInstanceError
```

## Q86: How do you implement REST API rate limiting with a distributed counter using Redis?
**A:** Distributed rate limiting with Redis: (1) Sliding window sorted set: `ZADD rate:user:123 <timestamp> <request_id>`, `ZREMRANGEBYSCORE rate:user:123 0 <window_start>`, `ZCARD rate:user:123`, (2) Fixed window counter: `INCR rate:user:123:<window>`, `EXPIRE rate:user:123:<window> 60`, (3) Token bucket: `local key = KEYS[1]; local tokens = redis.call('get', key); if (tokens == false) then redis.call('set', key, burst-1); return 1; elseif (tonumber(tokens) > 0) then redis.call('decr', key); return 1; else return 0; end`, (4) Cluster mode: use Redis Cluster with hash tags so rate limiter keys for the same user are on the same node, (5) Fallback: if Redis is down, allow the request (fail open) or deny (fail closed), (6) Lua scripting for atomic operations, (7) Per-endpoint and per-user rate limits.

**Code:**
```python
class Seq:
    def __init__(self, n):
        self.n = n
    def __iter__(self):                 # forward: used by iter()/for
        return iter(range(self.n))
    def __reversed__(self):             # backward: used by reversed()
        return iter(range(self.n - 1, -1, -1))

s = Seq(3)
print(list(s))              # [0, 1, 2]
print(list(reversed(s)))    # [2, 1, 0]
```

## Q87: How do you design a REST API for a consent management platform (CMP) for GDPR/CCPA compliance?
**A:** Consent API: (1) POST `/consents` records user consent: `{ "user_id": 123, "purposes": { "analytics": true, "marketing": false, "functional": true }, "timestamp": "..." }`, (2) GET `/consents/{user_id}` returns current consent settings, (3) GET `/consents/{user_id}/history` returns consent change log, (4) GET `/consents/proof/{id}` returns cryptographic proof of consent (signed timestamp), (5) Withdraw consent: POST `/consents/{user_id}/withdraw` with specific purposes, (6) Data deletion: POST `/users/{id}/forget` implements right to erasure, (7) Data portability: GET `/users/{id}/export` for data portability download, (8) Access: GET `/users/{id}/personal_data` returns all personal data stored, (9) Third-party consent: GET `/consents/third_party` shows which third parties have access.

**Code:**
```python
nums = [1, 2, 3, 4]

doubled = list(map(lambda x: x * 2, nums))      # map
evens = list(filter(lambda x: x % 2 == 0, nums))  # filter
print(doubled, evens)

# equivalent list comprehension (usually preferred in Python)
doubled2 = [x * 2 for x in nums]
evens2 = [x for x in nums if x % 2 == 0]
print(doubled2, evens2)
```

## Q88: How do you implement REST API long-running operation tracking with progress reporting?
**A:** Operation tracking: (1) POST `/operations` starts a long-running process, returns 202 with `Location: /operations/{id}`, (2) GET `/operations/{id}` returns status: `{ "status": "running", "progress": 45, "message": "Processing batch 45/100", "started_at": "...", "estimated_completion": "..." }`, (3) Statuses: queued, running, completing, completed, failed, cancelled, (4) Cancellation: POST `/operations/{id}/cancel` requests cancellation (best-effort), (5) Retry: POST `/operations/{id}/retry` re-runs, (6) Result: on completion, GET `/operations/{id}/result` returns the output, (7) Error: on failure, GET `/operations/{id}/error` returns error details, (8) Cleanup: DELETE `/operations/{id}` removes operation metadata, (9) Webhook: operation status changes callback to registered URL, (10) Expiration: operations expire after 7 days.

**Code:**
```python
from typing import Literal

def set_mode(mode: Literal["fast", "safe"]) -> str:
    return f"mode={mode}"

print(set_mode("fast"))     # ok for mypy (Literal value)
print(set_mode("safe"))
# set_mode("unknown") would be a type error
```

## Q89: How do you design a REST API for a product recommendation engine?
**A:** Recommendation API: (1) GET `/recommendations?user_id=123&context=homepage` returns personalized recommendations, (2) GET `/recommendations/{product_id}/similar` returns similar products, (3) GET `/recommendations/trending?category=electronics&period=7d` returns trending products, (4) GET `/recommendations/personalized?user_id=123&limit=20` for tailored results, (5) Feedback: POST `/recommendations/feedback` with `{ "product_id": 456, "action": "click" | "purchase" | "dismiss" }` to improve algorithm, (6) A/B testing: `X-Recommendation-Variant: A` header indicates which algorithm version served the result, (7) Diversity: ensure recommendations are not all from the same category, (8) Freshness: new products get a boost.

**Code:**
```python
from pprint import pprint

data = {"nested": {"a": [1, 2, 3], "b": {"x": True}}, "list": [1, "two"]}
pprint(data, sort_dicts=True)   # pretty-print nested structures
```

## Q90: How do you implement REST API observability with structured logging and span attributes?
**A:** API observability: (1) Structured logging: JSON format with `timestamp`, `level`, `message`, `service`, `endpoint`, `method`, `status_code`, `latency_ms`, `trace_id`, `user_id`, (2) Tracing: OpenTelemetry spans for each request with attributes: `http.method`, `http.route`, `http.status_code`, (3) Request lifecycle: create span on request, add child spans for DB queries, external calls, (4) Metrics: Prometheus histograms for latency (p50, p95, p99), counters for requests by status code, (5) Log correlation: include `trace_id` in all logs for correlation, (6) Error tracking: capture stack traces and request context, (7) Health endpoint: GET `/health` returns status of all dependencies, (8) Ready endpoint: GET `/ready` returns true when the service can accept traffic.

**Code:**
```python
# plugins/plugin_a.py          <- separate module files
#   def run(): return "A"
# plugins/plugin_b.py
#   def run(): return "B"

import importlib

for name in ("plugin_a", "plugin_b"):
    mod = importlib.import_module(f"plugins.{name}")  # dynamic import
    print(name, "->", mod.run())
```

## Q91: How do you design a REST API for a cryptocurrency wallet?
**A:** Crypto wallet API: (1) Generate wallet: POST `/wallets` returns address and encrypted private key, (2) Balance: GET `/wallets/{address}/balance` returns balance for all tokens, (3) Transaction: POST `/transactions` with `{ "to": "...", "amount": "0.1", "token": "ETH", "gas_limit": 21000 }`, (4) Transaction status: GET `/transactions/{hash}`, (5) History: GET `/wallets/{address}/transactions` with pagination, (6) Fees: GET `/gas/estimates` for current gas prices, (7) Webhook: POST `/webhooks` for transaction confirmation notifications, (8) Rate limiting: strict limits to prevent abuse, (9) Security: API keys with withdrawal permissions, address allowlisting, transaction limits, (10) Multi-sig: POST `/transactions/multisig` requires multiple signatures.

**Code:**
```python
class A:
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        print("A sees subclass", cls.__name__)

class B:
    def __init_subclass__(cls, **kwargs):
        B.flag = True
        super().__init_subclass__(**kwargs)

class C(A, B): pass          # cooperates via super(), both hooks run
print(getattr(B, "flag", False))
```

## Q92: How do you implement REST API server-side request forgery (SSRF) protection when proxying user-provided URLs?
**A:** SSRF protection: (1) Block private IP ranges: 10.x.x.x, 172.16-31.x.x, 192.168.x.x, 127.x.x.x, 169.254.x.x, (2) Block metadata IPs: 169.254.169.254 (cloud metadata), (3) URL validation: validate scheme (only http/https), parse hostname to IP before connecting, (4) DNS rebinding protection: resolve hostname, connect, then verify IP matches resolved address, (5) Allowlist domains instead of URLs if possible, (6) Use a dedicated proxy with IP restrictions for external requests, (7) Timeout: short timeout for external requests (5s), (8) Response size limit: limit response body size, (9) Disable redirect following or validate redirect targets, (10) Network segmentation: run proxy in a separate network segment with no access to internal services.

**Code:**
```python
import os
import pathlib

os.makedirs("demo_dir/sub", exist_ok=True)
print(os.path.isdir("demo_dir/sub"))        # True
print(os.path.join("demo_dir", "file.txt"))
print(pathlib.Path("demo_dir").exists())    # object-oriented alternative
```

## Q93: How do you design a REST API for a print-on-demand service?
**A:** Print-on-demand API: (1) Products: CRUD `/products` with sizes, colors, materials, (2) Design upload: POST `/designs` with SVG/PNG, returns preview URL, (3) Product + design: POST `/products/{id}/variants` with `{ "design_id": 123, "size": "XL", "color": "black" }`, (4) Order: POST `/orders` with cart items and shipping address, (5) Mockup: POST `/mockups` generates product preview images (async), (6) Pricing: GET `/pricing` with size, color, quantity for estimated cost, (7) Tracking: POST `/orders/{id}/tracking` updates shipping status, (8) Webhooks: `order.placed`, `order.shipped`, `order.delivered`, (9) Fulfillment: POST `/orders/{id}/fulfill` triggers print partner API.

**Code:**
```python
import functools
import logging

logging.basicConfig(level=logging.INFO)

def log_calls(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logging.info("calling %s", func.__name__)
        result = func(*args, **kwargs)
        logging.info("%s returned %r", func.__name__, result)
        return result
    return wrapper

@log_calls
def add(a, b):
    return a + b

print(add(2, 3))
```

## Q94: How do you implement REST API rate limiting with cost-based (not count-based) limits?
**A:** Cost-based rate limiting: (1) Assign a cost to each endpoint based on server processing: GET /users = 1 point, POST /search = 5 points, POST /export = 50 points, (2) Rate limit is a budget per time window (e.g., 1000 points per minute), (3) Each request deducts its cost from the budget, (4) If budget is exhausted, return 429, (5) Benefits: heavy operations are limited more strictly, fair across different usage patterns, (6) Implementation: `REDIS_INCRBY rate:user:123:points <cost>`, check if total exceeds limit, (7) Reset: budget resets per time window, (8) Documentation: publish cost table per endpoint.

**Code:**
```python
from typing import Final

MAX_WORKERS: Final = 8     # type checker flags reassignment

class Service:
    pass

@final
class Immutable:
    pass

print(MAX_WORKERS)
```

## Q95: How do you design a REST API for a real-time chat system?
**A:** Chat API: (1) Conversations: GET/POST `/conversations`, (2) Messages: GET/POST `/conversations/{id}/messages`, (3) Pagination: cursor-based (by message ID or timestamp), (4) Real-time: WebSocket for live messages and typing indicators, (5) Message types: text, image, file, system (user joined, left), (6) Read receipts: POST `/conversations/{id}/read` with `{ "last_read_message_id": 456 }`, (7) Typing: WebSocket event `typing:{conversation_id}:{user_id}`, (8) Reactions: POST `/messages/{id}/reactions` with emoji, (9) Editing: PUT `/messages/{id}` (within time limit), (10) Deletion: DELETE `/messages/{id}` (soft delete, keeps placeholder), (11) Push notifications: push to offline users via FCM/APNS.

**Code:**
```python
b = b"abc"          # immutable bytes
ba = bytearray(b)   # mutable bytearray
ba[0] = ord("X")    # in-place mutation
ba.append(100)      # extend
print(ba, bytes(ba))
```

## Q96: How do you implement REST API API key management with scoped permissions?
**A:** API key management: (1) Create key: POST `/api-keys` with `{ "label": "CI/CD pipeline", "scopes": ["read:users", "write:orders"], "expires_at": "2025-01-01" }`, (2) List keys: GET `/api-keys` returns key metadata (not the full key), (3) Revoke: DELETE `/api-keys/{id}` immediately invalidates, (4) Rotation: POST `/api-keys/{id}/rotate` generates a new key value (old key is invalidated), (5) Scopes: granular permissions, follow the format `resource:action`, (6) Rate limits: separate rate limits per API key, (7) IP binding: restrict key to specific IPs/CIDR ranges, (8) Usage: GET `/api-keys/{id}/usage` returns request counts, last used, (9) Never return the full key value in list responses; only show prefix + masked portion.

**Code:**
```python
import pkgutil
import os

# packages carry __path__: list of dirs searched for submodules
print("num? ", hasattr(os, "__path__"))          # os module: False
pkg_path = pkgutil.get_loader("xml").get_filename(source)  # package: has __path__
print(xml.__path__ if False else "xml is a package with __path__")
```

## Q97: How do you design a REST API for a digital asset management (DAM) system?
**A:** DAM API: (1) Upload: POST `/assets` with multipart upload, returns asset ID, (2) Metadata: PUT `/assets/{id}` updates title, description, tags, categories, (3) Search: GET `/assets?q=landscape&tags=photo&sort=created_at:desc`, (4) Transforms: POST `/assets/{id}/transforms` with `{ "type": "resize", "width": 800, "height": 600 }`, (5) Collections: POST `/collections` with asset IDs for grouping, (6) Versioning: GET `/assets/{id}/versions` for version history, (7) Rights management: PUT `/assets/{id}/rights` with license, usage terms, expiry, (8) Download: GET `/assets/{id}/download` with optional transform parameters, (9) Preview: GET `/assets/{id}/preview` for thumbnail/watermarked preview, (10) Bulk operations: POST `/assets/bulk` for batch tag, move, delete.

**Code:**
```python
from datetime import datetime, timezone, timedelta
from zoneinfo import ZoneInfo

now_utc = datetime.now(timezone.utc)
print(now_utc)                                          # aware UTC

ny = now_utc.astimezone(ZoneInfo("America/New_York"))   # IANA tz
print(ny)

fixed = timezone(timedelta(hours=5, minutes=30))
print(now_utc.astimezone(fixed))     # custom fixed offset
```

## Q98: How do you implement REST API graceful request body size limits with proper error responses?
**A:** Body size limits: (1) Set `Content-Length` check middleware (e.g., 10MB default, 100MB for file uploads), (2) If body exceeds limit, return 413 Payload Too Large before reading the body, (3) Response: `{ "error": { "code": "PAYLOAD_TOO_LARGE", "message": "Request body exceeds 10MB limit", "max_size": 10485760 } }`, (4) Include `Retry-After` header if temporary limit due to server load, (5) For chunked transfer (no Content-Length): read up to limit, close connection if exceeded, (6) Per-endpoint limits: allow larger limits on specific endpoints via configuration, (7) Stream large uploads to disk/temp before processing, (8) Respond quickly before reading the entire body (check Content-Length header), (9) Document body size limits in OpenAPI spec.

**Code:**
```python
import sys

print("math loaded before import:", "math" in sys.modules)
import math
print("after import:", "math" in sys.modules)   # True - cached
del sys.modules["math"]                          # force reload next import
```

## Q99: How do you design a REST API for a feature flag/toggle management system?
**A:** Feature flag API: (1) CRUD: GET/POST/PUT/DELETE `/flags`, (2) Flag schema: `{ "key": "new_checkout", "enabled": true, "rules": [{ "type": "percentage", "value": 50 }, { "type": "user_id", "values": ["123", "456"] }, { "type": "custom", "expression": "user.tier == 'beta'" }] }`, (3) Evaluation: POST `/flags/{key}/evaluate` with `{ "user": { "id": "123", "tier": "beta" } }` returns `{ "enabled": true, "reason": "user.tier match" }`, (4) Bulk evaluation: POST `/flags/evaluate` returns all enabled flags for context, (5) Targeting: percentage rollout, user/group targeting, custom rules, (6) SDK: GET `/flags/sdk/{sdk_key}` optimized for SDK polling, (7) Audit: GET `/flags/{key}/history` for change log, (8) Schedule: PUT `/flags/{key}` with `{ "scheduled_at": "2024-01-15T00:00:00Z", "changes": { "enabled": true } }`.

**Code:**
```python
import asyncio

async def main():
    await asyncio.sleep(1)
    return 7

# asyncio.run:  creates a new event loop, runs to completion, closes it
result = asyncio.run(main())
print(result)   # 7
# cannot be called from inside a running loop
```

## Q100: How do you implement REST API content negotiation for protocol buffers (protobuf) vs JSON?
**A:** Protobuf content negotiation: (1) Client sends `Accept: application/x-protobuf` or `Content-Type: application/x-protobuf`, (2) Server serializes/deserializes using protobuf binary format, (3) gRPC-web compatibility: `Accept: application/grpc-web+proto`, (4) The API must document the .proto schema and message definitions, (5) The same endpoint serves both JSON and protobuf based on Accept header, (6) Advantages: smaller payload (up to 10x smaller), faster serialization/deserialization, typed schemas, (7) Challenges: not human-readable (debugging requires tools), schema evolution requires coordinating proto updates, (8) For TypeScript/JavaScript clients: use protobuf.js or ts-proto to generate client code, (9) The `Content-Type` response header indicates which format was used, (10) Typically used for internal service-to-service APIs where performance matters.

**Code:**
```python
class Animal: pass
class Dog(Animal): pass
class Cat(Animal): pass

# __subclasses__ returns IMMEDIATE (not deep) subclasses
print(Animal.__subclasses__())     # [<class Dog>, <class Cat>]
```

