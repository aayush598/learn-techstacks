# REST API Interview Questions and Answers

## Q1: What is REST?
**A:** REST (Representational State Transfer) is an architectural style for designing networked applications. It uses a stateless, client-server communication protocol (typically HTTP) and treats server data as resources that can be created, read, updated, or deleted using standard HTTP methods.

**Code:**
```python
print("Hello, world!")  # high-level, readable, general-purpose
```

## Q2: What are the constraints of REST architecture?
**A:** REST has six constraints: (1) Uniform Interface, (2) Stateless, (3) Cacheable, (4) Client-Server, (5) Layered System, and (6) Code on Demand (optional). An API that satisfies all constraints is considered "RESTful."

**Code:**
```python
x = 5
x = "now a string"          # dynamic typing
print(x.upper(), len(x))    # batteries included (stdlib)
```

## Q3: What is a resource in REST?
**A:** A resource is any identifiable entity or object in a REST API, accessed via a URI. Examples: /users/123, /orders, /products/abc. Resources are abstractions — they can represent database rows, files, or computed data.

**Code:**
```python
lst = [1, 2]
lst.append(3)          # list is mutable
tup = (1, 2)           # tuple is immutable
print(lst, tup)
d = {tup: "tuple key"}   # tuples are hashable -> dict keys
```

## Q4: What is the uniform interface constraint in REST?
**A:** The uniform interface separates clients from servers by standardizing the way resources are identified (URIs), manipulated (HTTP methods), described (representations like JSON/XML), and self-described (HATEOAS). It simplifies the architecture and enables independent evolution.

**Code:**
```python
def calculate_total(items):   # snake_case function
    total = 0               # 4-space indentation
    for item in items:
        total += item
    return total

print(calculate_total([1, 2, 3, 4]))
```

## Q5: What is statelessness in REST?
**A:** Statelessness means each request from a client to the server must contain all information needed to understand and process the request. The server does not store any client session context. Session state is kept entirely on the client. This improves scalability and visibility.

**Code:**
```python
def logger(func):
    def wrapper(*args, **kwargs):
        print(f"calling {func.__name__}")
        return func(*args, **kwargs)
    return wrapper

@logger
def add(a, b):
    return a + b

add(2, 3)
```

## Q6: What are the main HTTP methods used in REST APIs?
**A:** GET (retrieve a resource), POST (create a resource), PUT (replace a resource entirely), PATCH (partially update a resource), DELETE (remove a resource), HEAD (same as GET but only returns headers), OPTIONS (returns supported methods for a resource).

**Code:**
```python
import threading, time

def work():
    time.sleep(1)              # I/O-bound: GIL released, thread can run

t1 = threading.Thread(target=work)   # GIL lets one thread run bytecode at a time
t2 = threading.Thread(target=work)
t1.start(); t2.start(); t1.join(); t2.join()
print("done")
```

## Q7: What is the difference between PUT and POST?
**A:** PUT is idempotent and typically updates/replaces a resource at a specific URI (client determines the URI). POST creates a new resource (server determines the URI) and is not idempotent. PUT can also create if the resource does not exist at the specified URI.

**Code:**
```python
import copy

original = [[1, 2], [3, 4]]
shallow = copy.copy(original)
deep = copy.deepcopy(original)

shallow[0].append(99)     # shallow: inner object is shared
print(original)           # [[1, 2, 99], [3, 4]]
print(deep)               # [[1, 2], [3, 4]] unaffected
```

## Q8: What is the difference between PUT and PATCH?
**A:** PUT replaces the entire resource with the request body. PATCH applies a partial update — only the fields specified in the request body are modified. PATCH is more bandwidth-efficient for small updates.

**Code:**
```python
import sys
x = []
print(sys.getrefcount(x) - 1)   # references to x
del x                           # refcount reaches 0 -> deallocated

import gc
gc.collect()                    # handles circular references
```

## Q9: What is idempotence in REST?
**A:** An operation is idempotent if making the same request multiple times produces the same result as making it once. GET, PUT, DELETE, HEAD, OPTIONS are idempotent. POST is NOT idempotent (multiple POST requests create multiple resources). PATCH is not necessarily idempotent.

**Code:**
```python
def intro(*args, **kwargs):
    print("args:", args)
    print("kwargs:", kwargs)

intro(1, 2, name="Alice", age=30)
# args: (1, 2)   kwargs: {'name': 'Alice', 'age': 30}
```

## Q10: What is the difference between safe and idempotent methods?
**A:** Safe methods (GET, HEAD, OPTIONS) do not change server state — they are read-only. Idempotent methods (PUT, DELETE) may change state, but repeated identical requests have the same effect as a single request. All safe methods are idempotent, but not vice versa.

**Code:**
```python
squares = [x**2 for x in range(10) if x % 2 == 0]
print(squares)   # [0, 4, 16, 36, 64]
```

## Q11: What is the correct HTTP status code for a successful GET request?
**A:** 200 OK. For a successful POST that creates a resource: 201 Created. For a successful DELETE: 204 No Content. For a successful PUT/PATCH: 200 OK or 204 No Content.

**Code:**
```python
add = lambda x, y: x + y          # anonymous single-expression function
print(add(2, 3))

words = ["banana", "apple", "cherry"]
print(sorted(words, key=lambda w: len(w)))   # uses lambda as key
```

## Q12: What is the difference between 200 OK and 201 Created?
**A:** 200 OK indicates the request succeeded and the response contains the representation of the resource. 201 Created specifically indicates a resource was created as a result of a POST or PUT request and typically includes a Location header with the URI of the new resource.

**Code:**
```python
try:
    result = 10 / 0
except ZeroDivisionError as e:
    print("caught:", e)
else:
    print("no error")
finally:
    print("always runs")
```

## Q13: What does a 204 No Content response mean?
**A:** 204 No Content indicates the server successfully processed the request but there is no content to return in the response body. It is commonly used for DELETE operations or PUT/PATCH operations that do not return the updated resource.

**Code:**
```python
a = [1, 2, 3]
b = [1, 2, 3]

print(a == b)   # True  - value equality
print(a is b)   # False - different objects
print(256 is 256)  # True - small ints are interned
```

## Q14: What is the meaning of 3xx status codes?
**A:** 3xx status codes indicate redirection. 301 Moved Permanently (resource has a new permanent URI), 302 Found (temporary redirect), 304 Not Modified (cached version is still valid, used with conditional GETs), 307 Temporary Redirect, 308 Permanent Redirect.

**Code:**
```python
with open("demo.txt", "w") as f:   # __enter__ opens, __exit__ closes
    f.write("hello")
# f is automatically closed, even if an exception occurs
```

## Q15: What is the difference between 401 Unauthorized and 403 Forbidden?
**A:** 401 Unauthorized means the client is not authenticated (no valid credentials). 403 Forbidden means the client is authenticated but does not have permission to access the resource. They are often confused — 401 is about authentication; 403 is about authorization.

**Code:**
```python
def countdown(n):
    while n > 0:
        yield n            # generator: lazy sequence
        n -= 1

print(list(countdown(3)))              # [3, 2, 1]
print(sum(x**2 for x in range(5)))     # generator expression: 30
```

## Q16: What does a 404 Not Found status code indicate?
**A:** 404 indicates the server cannot find the requested resource. This could mean the resource does not exist or the URI is invalid. It should not expose whether the resource exists but access is denied (use 403 for that).

**Code:**
```python
class Point:
    def __init__(self, x, y):
        self.x, self.y = x, y
    def __repr__(self):                     # unambiguous, dev-facing
        return f"Point({self.x}, {self.y})"
    def __str__(self):                      # readable, user-facing
        return f"({self.x}, {self.y})"

p = Point(1, 2)
print(str(p))    # (1, 2)
print(repr(p))   # Point(1, 2)
```

## Q17: What is the meaning of 422 Unprocessable Entity?
**A:** 422 Unprocessable Entity indicates the server understands the request's content type and syntax but cannot process the request body due to semantic errors (e.g., validation failures, missing required fields, invalid data formats).

**Code:**
```python
class A: pass
class B(A): pass
class C(A): pass
class D(B, C): pass

print([c.__name__ for c in D.__mro__])
# ['D', 'B', 'C', 'A', 'object']
```

## Q18: What is the difference between 500 Internal Server Error and 502 Bad Gateway?
**A:** 500 indicates a generic server-side error. 502 indicates the server (acting as a gateway/proxy) received an invalid response from an upstream server. 500 is the server's own fault; 502 indicates a dependency failure.

**Code:**
```python
import math                      # module: a .py file
from math import sqrt           # import a name directly

print(math.pi)                  # qualify via module
print(sqrt(16))                 # already in this namespace
```

## Q19: What is the difference between 503 Service Unavailable and 504 Gateway Timeout?
**A:** 503 means the server is temporarily overloaded or under maintenance. 504 means the server (gateway/proxy) did not receive a timely response from an upstream server. 503 suggests retry later; 504 suggests an upstream issue.

**Code:**
```python
def greet(name: str, age: int = 0) -> str:   # type hints
    return f"{name} ({age})"

print(greet("Ada", 36))
print(greet.__annotations__)
```

## Q20: What are common REST API endpoint naming conventions?
**A:** Use nouns (not verbs) for resources: /users, /articles, /orders. Use plural names for collections. Use lowercase with hyphens for multi-word names (/order-items). Nest related resources (/users/123/orders). Use query parameters for filtering/sorting.

**Code:**
```python
class Demo:
    cls_data = 0

    def instance_method(self):          # takes self, instance state
        return f"instance {self}"

    @classmethod
    def class_method(cls):              # takes cls, class state
        cls.cls_data += 1
        return cls.cls_data

    @staticmethod
    def static_method():                # no self / cls
        return "static"

d = Demo()
print(d.instance_method())
print(Demo.class_method(), Demo.class_method())
print(Demo.static_method())
```

## Q21: How do you design REST API endpoints for CRUD operations?
**A:** Collection: GET /users (list), POST /users (create). Single resource: GET /users/{id} (read), PUT /users/{id} (replace), PATCH /users/{id} (partial update), DELETE /users/{id} (delete). Use sub-resources for relationships: /users/{id}/orders.

**Code:**
```python
class Point:
    __slots__ = ("x", "y")          # fixed attribute set
    def __init__(self, x, y):
        self.x, self.y = x, y

p = Point(1, 2)
print(p.x, p.y)
print(hasattr(p, "__dict__"))       # False -> memory saved
```

## Q22: How do you handle filtering, sorting, and pagination in REST APIs?
**A:** Use query parameters: ?status=active (filtering), ?sort=-created_at (sorting, minus for descending), ?page=2&limit=20 or ?offset=20&limit=20 (pagination). Return pagination metadata in the response (total, page, limit, next, previous URLs).

**Code:**
```python
class Meta(type):
    def __new__(mcs, name, bases, ns):
        ns["created_by"] = "metaclass"
        return super().__new__(mcs, name, bases, ns)

class Widget(metaclass=Meta):
    pass

print(Widget.created_by)   # metaclass intercepted class creation
```

## Q23: What is cursor-based pagination vs offset-based pagination?
**A:** Offset-based uses ?page=2&limit=20 — simple but inefficient for large offsets (skipping rows). Cursor-based uses ?cursor=abc123 — uses a unique, sequential value (often id or created_at) and is efficient regardless of dataset size. Cursor-based is recommended for real-time data.

**Code:**
```python
import threading

def worker(name):
    print(f"{name} running")

threads = [threading.Thread(target=worker, args=(f"T{i}",)) for i in range(3)]
for t in threads: t.start()
for t in threads: t.join()
```

## Q24: How do you handle API versioning?
**A:** Common approaches: (1) URI versioning (/v1/users, /v2/users), (2) Header versioning (Accept: application/vnd.company.v1+json), (3) Query parameter versioning (?version=1). URI versioning is most common. Content negotiation (header-based) is more RESTful.

**Code:**
```python
import threading
from multiprocessing import Process

def job():
    total = sum(range(1000))
    print(f"computed {total}")

# threads: one process, shared memory, GIL-limited
t = threading.Thread(target=job); t.start(); t.join()

# processes: own memory + GIL, true parallelism
p = Process(target=job); p.start(); p.join()

# Use ProcessPoolExecutor for CPU-bound work in parallel:
from concurrent.futures import ProcessPoolExecutor
if __name__ == "__main__":
    with ProcessPoolExecutor(2) as ex:
        print(list(ex.map(lambda x: x * x, [1, 2, 3, 4])))
```

## Q25: What is HATEOAS?
**A:** HATEOAS (Hypermedia As The Engine Of Application State) is a REST constraint where the API response includes links to related actions and resources. Clients navigate the API dynamically through these links, reducing the need for out-of-band documentation.

**Code:**
```python
import asyncio

async def fetch(i):
    await asyncio.sleep(0.1)          # non-blocking wait
    return f"result-{i}"

async def main():
    results = await asyncio.gather(fetch(1), fetch(2))
    print(results)

asyncio.run(main())   # ['result-1', 'result-2']
```

## Q26: What is content negotiation in REST?
**A:** Content negotiation allows the client and server to agree on the format of the response. The client sets the Accept header (e.g., Accept: application/json) and the server responds with the appropriate format. The Content-Type header indicates the actual format of the response body.

**Code:**
```python
import asyncio

async def inner():
    return "value"

async def outer_await():
    v = await inner()        # await: awaits an awaitable
    return v

print(asyncio.run(outer_await()))   # value

def gen():
    yield from range(3)      # yield from: delegate to a subgenerator

print(list(gen()))   # [0, 1, 2]
```

## Q27: What are common content types used in REST APIs?
**A:** application/json (most common), application/xml (legacy), text/plain, text/html, multipart/form-data (file uploads), application/octet-stream (binary data), application/x-www-form-urlencoded (form data), application/pdf (specific file type).

**Code:**
```python
class Point:
    def __new__(cls, x, y):          # creates the instance (called first)
        print("__new__")
        return super().__new__(cls)
    def __init__(self, x, y):        # initializes it (after __new__)
        print("__init__")
        self.x, self.y = x, y

p = Point(1, 2)
# __new__
# __init__
```

## Q28: What is the difference between application/json and application/x-www-form-urlencoded?
**A:** application/json sends data as a JSON string, supporting nested objects and arrays. application/x-www-form-urlencoded encodes data as key-value pairs (like query parameters). JSON is preferred for complex data; form encoding is simpler for basic forms.

**Code:**
```python
class Person:
    def __init__(self, name):
        self._name = name
    @property
    def name(self):                 # getter: accessed like attribute
        return self._name
    @name.setter
    def name(self, value):          # setter with validation
        if not value:
            raise ValueError("empty name")
        self._name = value

p = Person("Ada")
p.name = "Grace"
print(p.name)
```

## Q29: How do you handle errors in a REST API?
**A:** Return appropriate HTTP status codes (4xx for client errors, 5xx for server errors) with a consistent error response body. Include a unique error ID for debugging. Structure: { "error": { "code": "VALIDATION_ERROR", "message": "Email is required", "details": [...] } }.

**Code:**
```python
from typing import get_type_hints

mutable = [1, 2]          # list
immutable = (1, 2)        # tuple
mapping = {"a": 1}        # dict
myset = {1, 2, 3}         # set
frozen = frozenset({1})   # frozenset
print(type(mutable), type(immutable), type(mapping), type(myset), type(frozen))
```

## Q30: What should an error response body contain?
**A:** Best practice: error code (machine-readable), message (human-readable), details/validation errors, request ID/correlation ID, and timestamp. The structure should be consistent across all endpoints. Include a documentation URL for common errors.

**Code:**
```python
lst = [1, 2, 3, 4]

lst.reverse()                # in-place
print(lst)

print(list(reversed([1, 2, 3])))   # iterator
print([1, 2, 3][::-1])            # reversed copy
```

## Q31: How do you handle validation errors in REST APIs?
**A:** Return 400 Bad Request or 422 Unprocessable Entity with a structured response listing each validation failure: { "errors": [ { "field": "email", "message": "Invalid email format" } ] }. Validate both query parameters and request body.

**Code:**
```python
lst = [1, 2, 3, 2]
lst.remove(2)       # removes first occurrence of value 2
print(lst)          # [1, 3, 2]

del lst[1]          # deletes by index
popped = lst.pop()  # removes & returns last item
print(lst, popped)
```

## Q32: What is rate limiting in REST APIs?
**A:** Rate limiting controls how many requests a client can make within a time window. It protects the API from abuse. Responses include headers: X-RateLimit-Limit (max requests), X-RateLimit-Remaining (remaining requests), X-RateLimit-Reset (when limit resets). 429 Too Many Requests on limit exceeded.

**Code:**
```python
import gc

class Ref:
    pass

a, b = Ref(), Ref()
a.other = b
b.other = a            # circular reference - refcounting can't free these
del a, b

print(gc.collect())    # cyclic collector reclaims them
```

## Q33: What is the 429 Too Many Requests status code?
**A:** 429 indicates the client has exceeded the rate limit. The response should include a Retry-After header indicating how long to wait before retrying. The server may also return rate limit metadata in the response body.

**Code:**
```python
values = [1, 2, 3, 4, 5]
if (n := len(values)) > 3:          # walrus: assign within expression
    print(f"list has {n} items")
```

## Q34: How do you implement authentication in REST APIs?
**A:** Common methods: (1) API Keys (simple, in header or query param), (2) Basic Auth (username:password base64-encoded), (3) Bearer Token (JWT or opaque token in Authorization header), (4) OAuth 2.0 (delegated authorization), (5) Session-based (cookies, less common for APIs).

**Code:**
```python
d1, d2 = {"a": 1}, {"b": 2}

merged = d1 | d2              # Python 3.9+
print(merged)                 # {'a': 1, 'b': 2}

also = {**d1, **d2}          # older versions
print(also)
```

## Q35: What is JWT (JSON Web Token)?
**A:** JWT is a compact, self-contained token format for transmitting claims between parties. It consists of three base64-encoded parts (header, payload, signature) separated by dots. JWTs are commonly used for API authentication — the server verifies the signature and extracts user claims.

**Code:**
```python
class Calc:
    def add(self, a, b):
        return a + b

def fake_add(self, a, b):
    return "mocked"

Calc.add = fake_add            # monkey patch at runtime
print(Calc().add(1, 2))        # mocked
```

## Q36: What is the difference between JWT and opaque tokens?
**A:** JWT is self-contained — it carries user claims and metadata, so the server does not need a database lookup to authenticate. Opaque tokens are random strings that require server-side lookup (e.g., database or cache) to retrieve associated user data. JWT is faster but harder to revoke.

**Code:**
```python
class Circle:
    pi = 3.14159

    def _init(self):
        pass

    @classmethod
    def with_diameter(cls, d):      # cls instead of self
        return cls(d / 2)

    @staticmethod
    def how_beautiful():            # no self, no cls
        return "very"

    @property
    def radius(self):               # accessed like an attribute
        return getattr(self, "_r", 0)

c = Circle.with_diameter(4)
print(Circle.how_beautiful(), c.radius)
```

## Q37: How do you handle token refresh in REST APIs?
**A:** Use a two-token system: access token (short-lived, e.g., 15 minutes) and refresh token (long-lived, e.g., 7 days). When the access token expires, the client sends the refresh token to a /auth/refresh endpoint to get a new access token. Refresh tokens can be revoked.

**Code:**
```python
import sys
print(sys.path[0])               # script dir / current dir
# plus PYTHONPATH, stdlib dirs, and .pth paths - all in sys.path
```

## Q38: What is OAuth 2.0?
**A:** OAuth 2.0 is an authorization framework that enables third-party applications to obtain limited access to a user's resources without sharing credentials. It defines grant types (authorization code, client credentials, implicit, password) and roles (resource owner, client, authorization server, resource server).

**Code:**
```python
import os
# python -m venv /path/to/venv   -> creates isolated interpreter
print(os.popen("python -m venv /tmp/demo_venv").read())
print(os.path.isdir("/tmp/demo_venv/bin"))   # activation script dir
```

## Q39: What is the difference between OAuth 2.0 and OpenID Connect?
**A:** OAuth 2.0 is for authorization (granting access to resources). OpenID Connect (OIDC) is an authentication layer built on top of OAuth 2.0, adding an ID token (JWT) that contains user identity information. OIDC answers "who is the user?"; OAuth 2.0 answers "what can the app access?"

**Code:**
```python
import subprocess, sys
# pip install requests, pip freeze > requirements.txt
result = subprocess.run([sys.executable, "-m", "pip", "--version"],
                        capture_output=True, text=True)
print(result.stdout)
```

## Q40: What is the Authorization header format?
**A:** The format is Authorization: <type> <credentials>. Common types: Bearer <token> (JWT or opaque token), Basic <base64-encoded-credentials>, Digest <digest-value>, APIKey <api-key>.

**Code:**
```python
# requirements.txt  ->  pip install -r requirements.txt (deployment pins)
#    requests==2.32.0
#
# setup.py  ->  pip install . (package metadata & deps for distribution)

print("pip install -r requirements.txt")
print("pip install .")
```

## Q41: How do you implement CORS in a REST API?
**A:** CORS (Cross-Origin Resource Sharing) is implemented via server response headers. The key header is Access-Control-Allow-Origin (specifies allowed origins). Other headers: Access-Control-Allow-Methods, Access-Control-Allow-Headers, Access-Control-Max-Age, Access-Control-Allow-Credentials.

**Code:**
```python
class Vec:
    def __init__(self, x):
        self.x = x
    def __len__(self):          # supports len(v)
        return 1
    def __str__(self):          # supports str(v) / print(v)
        return f"Vec({self.x})"
    def __add__(self, other):   # supports v + other
        return Vec(self.x + other.x)

v = Vec(3) + Vec(4)
print(len(v), v)
```

## Q42: What is a preflight request in CORS?
**A:** For requests with non-simple methods (PUT, DELETE, PATCH) or custom headers, browsers send a preflight OPTIONS request before the actual request. The server must respond with CORS headers. The client then sends the actual request only if the preflight succeeds.

**Code:**
```python
class Money:
    def __init__(self, amount):
        self.amount = amount
    def __eq__(self, other):                    # needed for dict/set use
        return isinstance(other, Money) and self.amount == other.amount
    def __hash__(self):                         # same hash for equal objects
        return hash(self.amount)

wallet = {Money(5), Money(5)}
print(len(wallet))      # 1 - equal objects hash alike
```

## Q43: What is a simple request in CORS?
**A:** A simple request uses GET, HEAD, or POST with Content-Type of application/x-www-form-urlencoded, multipart/form-data, or text/plain. Simple requests do not trigger a preflight — the browser sends the request directly and checks CORS headers on the response.

**Code:**
```python
class Proxy:
    def __getattr__(self, name):      # only when normal lookup fails
        return f"fallback for {name}"

    def __getattribute__(self, name):  # called for every access
        return super().__getattribute__(name)

p = Proxy()
print(p.anything)      # fallback for anything
```

## Q44: How do you handle file uploads in REST APIs?
**A:** Use multipart/form-data content type with POST or PUT. The request body is divided into parts, each with its own Content-Type and headers. The server parses the multipart stream to extract files and form fields. Binary files can also be sent directly as the request body with appropriate Content-Type.

**Code:**
```python
import functools

@functools.lru_cache(maxsize=128)
def fib(n):
    return n if n < 2 else fib(n - 1) + fib(n - 2)

print(fib(30))                   # 832040, cached fast
print(fib.cache_info())
```

## Q45: What is idempotency key?
**A:** An idempotency key is a unique identifier (usually a UUID) sent by the client in the Idempotency-Key header. The server stores the result of the first request with that key and returns the same response for duplicate requests. It prevents duplicate processing (e.g., double charging a credit card).

**Code:**
```python
# pkg/__init__.py  -> makes pkg a package, runs on import
# pkg/__main__.py   -> allows:  python -m pkg
print("python -m pkg  executes pkg/__main__.py")
```

## Q46: How do you implement idempotency for POST requests?
**A:** The client generates a unique idempotency key (UUID) and sends it in the Idempotency-Key header. The server checks if it has processed this key before. If yes, it returns the cached response. If no, it processes the request and caches the response keyed by the idempotency key.

**Code:**
```python
import unittest

def add(a, b):
    return a + b

class TestAdd(unittest.TestCase):
    def test_add(self):
        self.assertEqual(add(2, 3), 5)
        self.assertGreater(add(1, 1), 1)

if __name__ == "__main__":
    unittest.main(argv=[""], exit=False)
```

## Q47: What is the difference between REST and SOAP?
**A:** REST is an architectural style using HTTP and JSON/XML, is stateless, and has a uniform interface. SOAP is a protocol using XML, supports stateful operations, has built-in error handling, and supports WS-Security. REST is simpler and more lightweight; SOAP is more rigid but offers enterprise-grade security.

**Code:**
```python
from unittest.mock import Mock, patch

mock = Mock()
mock.fetch.return_value = {"id": 1}
print(mock.fetch())          # {'id': 1}
mock.fetch.assert_called_once()

func = lambda: "real"
with patch("__main__.func", return_value="stubbed"):
    print(func())            # stubbed
```

## Q48: What is the difference between REST and GraphQL?
**A:** REST exposes multiple endpoints returning fixed data structures. GraphQL exposes a single endpoint where clients query exactly the data they need. REST over-fetches/under-fetches; GraphQL solves this. REST uses HTTP caching naturally; GraphQL requires custom caching.

**Code:**
```python
import unittest

# pytest style
def test_add():
    assert 1 + 1 == 2

# unittest style
class TestAdd(unittest.TestCase):
    def test_add(self):
        self.assertEqual(1 + 1, 2)

unittest.main(argv=[""], exit=False)
```

## Q49: What is the difference between REST and gRPC?
**A:** REST uses HTTP/1.1 or HTTP/2 with text-based JSON. gRPC uses HTTP/2 with Protocol Buffers (binary, smaller, faster). gRPC supports streaming (server, client, bidirectional). REST is more universally understood; gRPC is faster for service-to-service communication.

**Code:**
```python
class Managed:
    def __enter__(self):            # acquire resource
        print("enter")
        return self
    def __exit__(self, exc_type, exc, tb):   # release, called even on errors
        print("exit")
        return False                # False -> don't swallow exceptions

with Managed():
    print("inside")
```

## Q50: How do you handle caching in REST APIs?
**A:** Use HTTP caching headers: Cache-Control (max-age, no-cache, private, public), ETag (entity tag for conditional requests), Last-Modified (timestamp-based validation), Expires (deprecated). Clients use If-None-Match (ETag) or If-Modified-Since (Last-Modified) for conditional GETs. Server responds 304 Not Modified if unchanged.

**Code:**
```python
class MyDict(dict):
    def __getitem__(self, key):         # obj[key]  read
        print("get", key)
        return super().__getitem__(key)
    def __setitem__(self, key, value):  # obj[key] = value  write
        print("set", key, value)
        super().__setitem__(key, value)

d = MyDict()
d["a"] = 1
print(d["a"])
```

## Q51: What is ETag?
**A:** ETag (Entity Tag) is an HTTP response header that uniquely identifies a specific version of a resource. It is typically a hash of the resource representation. Clients send If-None-Match with the ETag value; the server returns 304 Not Modified if the resource has not changed.

**Code:**
```python
nums = [1, 2, 3]              # iterable: has __iter__()
it = iter(nums)              # iterator: has __next__()
print(next(it), next(it))    # 1 2
```

## Q52: What is the difference between Cache-Control: no-cache and no-store?
**A:** no-cache means the resource must be revalidated with the server before each use (can use ETag). no-store means the response must not be stored in any cache at all (neither browser nor intermediate). no-cache allows caching with validation; no-store forbids caching entirely.

**Code:**
```python
class Counter:
    def __init__(self, limit):
        self.limit = limit
        self.n = 0
    def __iter__(self):
        return self
    def __next__(self):
        if self.n >= self.limit:
            raise StopIteration
        self.n += 1
        return self.n

print(list(Counter(3)))   # [1, 2, 3]
```

## Q53: What are conditional requests in REST?
**A:** Conditional requests use headers like If-Modified-Since (with Last-Modified) or If-None-Match (with ETag) to check if a resource has changed before sending it. The server returns 304 Not Modified if unchanged, saving bandwidth. Also used with If-Match for optimistic concurrency on writes.

**Code:**
```python
class Down:
    def __init__(self, top):
        self.top = top
    def __iter__(self):          # called once by iter()
        self.n = self.top
        return self
    def __next__(self):          # called each iteration step
        if self.n <= 0:
            raise StopIteration
        self.n -= 1
        return self.n + 1

print(list(Down(3)))   # [3, 2, 1]
```

## Q54: What is optimistic concurrency control in REST?
**A:** Optimistic concurrency uses If-Match header with the current ETag in PUT/PATCH/DELETE requests. The server only applies the change if the ETag matches (resource has not changed since the client fetched it). If another client modified it, the request fails with 412 Precondition Failed.

**Code:**
```python
from collections import namedtuple, deque, Counter, defaultdict, OrderedDict

Point = namedtuple("Point", ["x", "y"])
print(Point(1, 2))                      # tuple with named fields
print(deque([1, 2], maxlen=2))          # double-ended queue
print(Counter("aabbb"))                 # counting
print(defaultdict(list))                # dict with default factory
print(OrderedDict(a=1, b=2))            # insertion-ordered dict
```

## Q55: What does the 412 Precondition Failed status code mean?
**A:** 412 indicates that one or more preconditions (specified in If-Match, If-None-Match, If-Modified-Since headers) evaluated to false. It is commonly used in optimistic concurrency control when a resource has been modified by another client.

**Code:**
```python
from collections import defaultdict

dd = defaultdict(list)
dd["fruits"].append("apple")     # no KeyError; key auto-created
print(dd)
print(dd["nonexistent"])         # [] instead of raising
```

## Q56: What is query parameter vs path parameter in REST?
**A:** Path parameters identify a specific resource (/users/123). Query parameters filter, sort, or modify the response (/users?status=active). Path parameters are required and part of the resource identity. Query parameters are optional and modify the representation.

**Code:**
```python
from collections import namedtuple

Point = namedtuple("Point", ["x", "y"])   # tuple subclass with fields
p = Point(3, 4)
print(p.x, p[0])              # named and positional access
print(p._asdict())            # OrderedDict? No - dict support
```

## Q57: How do you design a REST API for a search endpoint?
**A:** Option 1: GET /search?q=term&type=users (simple). Option 2: POST /search with body for complex queries. Return search results with pagination metadata. Use 200 OK for valid searches (even with zero results). Consider dedicated search endpoints per resource: GET /users?q=term.

**Code:**
```python
class Slim:
    __slots__ = ("x", "y")      # no __dict__ per instance
    def __init__(self, x, y):
        self.x, self.y = x, y

s = Slim(1, 2)
print(hasattr(s, "__dict__"))   # False -> memory saved, faster access
```

## Q58: What is batch processing in REST APIs?
**A:** Batch processing allows sending multiple operations in a single HTTP request to reduce round trips. Implemented via: (1) a custom endpoint (/batch) that accepts an array of requests, (2) JSON-patch for batch updates, (3) asynchronous job submission for long-running operations.

**Code:**
```python
from enum import Enum, auto

class Color(Enum):
    RED = auto()          # auto-numbered
    GREEN = auto()
    BLUE = auto()

for c in Color:
    print(c.name, c.value)
```

## Q59: What is asynchronous processing in REST APIs?
**A:** For long-running operations, the API accepts the request, returns 202 Accepted with a Location header pointing to a status endpoint. The client polls the status endpoint to check progress. When complete, the status endpoint returns 303 See Other redirecting to the result.

**Code:**
```python
from enum import Enum, IntEnum

class Colors(Enum):
    RED = 1

class Numbers(IntEnum):
    ONE = 1

print(Colors.RED == 1)   # False - Enum is not an int
print(Numbers.ONE == 1)  # True  - IntEnum inherits int
print(Numbers.ONE + 2)   # 3    - arithmetic works
```

## Q60: What is the 202 Accepted status code?
**A:** 202 Accepted indicates the server has accepted the request for processing but has not completed it. The response includes a Location header with a URL to check the processing status. It is used for asynchronous operations that may take significant time.

**Code:**
```python
# module a.py
def run():
    from module_b import helper   # import inside function = lazy import
    return helper()

# restructure or lazy-import -- never fix cycles by deleting top-level imports
print("lazy imports break the cycle")
```

## Q61: What is the 303 See Other status code?
**A:** 303 indicates the response to the request can be found at another URI (specified in the Location header). It is used in async processing after completion: the status endpoint returns 303 redirecting to the actual result resource.

**Code:**
```python
import math                     # full module namespace
from math import sqrt           # specific name into namespace

print(math.floor(2.7))          # module.name
print(sqrt(16))                 # bare name
```

## Q62: How do you handle bulk operations in REST APIs?
**A:** Options: (1) POST /users/bulk with array of user objects, (2) JSON Patch (RFC 6902) for partial updates, (3) collection endpoints with transactions, (4) GraphQL mutations for batch operations. Each has trade-offs between RESTfulness and practicality.

**Code:**
```python
x = "global"

def outer():
    x = "enclosing"
    def inner():
        x = "local"            # L: Local
        print(x)
    inner()                    # prints "local"
    print(x)                   # E: Enclosing -> "enclosing"

outer()
print(x)                       # G: Global -> "global" 
```

## Q63: What is JSON Patch (RFC 6902)?
**A:** JSON Patch is a format for describing partial updates as an array of operations: add, remove, replace, move, copy, test. The Content-Type is application/json-patch+json. Example: [{ "op": "replace", "path": "/name", "value": "New Name" }].

**Code:**
```python
def make_counter():
    count = 0
    def increment():
        nonlocal count     # modify variable in enclosing function scope
        count += 1
        return count
    return increment

c = make_counter()
print(c(), c(), c())     # 1 2 3
```

## Q64: What is JSON API (JSON:API)?
**A:** JSON:API is a specification for building REST APIs in JSON. It standardizes conventions for resource naming, relationships, pagination, error handling, sparse fieldsets, and compound documents (including related resources). Content-Type: application/vnd.api+json.

**Code:**
```python
count = 0

def bump():
    global count           # write to module-level variable
    count += 1

bump(); bump()
print(count)               # 2
```

## Q65: What is OpenAPI (Swagger)?
**A:** OpenAPI is a specification for describing REST APIs in a machine-readable format (YAML or JSON). It defines endpoints, parameters, request/response schemas, authentication, and more. Tools generate documentation, client SDKs, and server stubs from OpenAPI specs.

**Code:**
```python
def combine(a, b, c):
    return a + b + c

nums = [1, 2, 3]
print(combine(*nums))                  # * unpacks iterable -> 6

kwargs = {"a": 1, "b": 2, "c": 3}
print(combine(**kwargs))               # ** unpacks mapping -> 6
```

## Q66: What is the difference between Swagger and OpenAPI?
**A:** OpenAPI is the specification. Swagger was the original name (Swagger 2.0) — the specification was renamed OpenAPI when it became a Linux Foundation project. Swagger also refers to the tooling ecosystem (Swagger UI, Swagger Editor, Swagger Codegen).

**Code:**
```python
name, score = "Ada", 95.5

print("Hello %s" % name)                    # %-formatting
print("Hello {}, score {:.1f}".format(name, score))  # str.format
print(f"Hello {name}, score {score:.1f}")   # f-string (preferred)
```

## Q67: What is API Blueprint?
**A:** API Blueprint is a documentation-oriented API description language using Markdown. It focuses on human readability first. Tools include Apiary for documentation and testing. It is less popular than OpenAPI but offers a simpler writing experience.

**Code:**
```python
name = "Ada"
print(f"{name}")                 # simple
print(f"{name!r}")               # repr conversion
print(f"{name:>10}")             # alignment / format specs

# Limitation: no backslashes inside {} (use a variable instead)
nl = "\n"
print(f"line1{nl}line2")
```

## Q68: What is Postman?
**A:** Postman is a popular API development and testing tool. It supports creating and sending HTTP requests, organizing collections, writing tests (JavaScript), environment variables, automated testing runners, API mocking, and documentation generation.

**Code:**
```python
big = 10 ** 30
print(big)                  # arbitrary precision - no overflow
print(big * big)
```

## Q69: How do you test REST APIs?
**A:** Testing levels: (1) Unit tests for serialization/deserialization, (2) Integration tests with test databases, (3) Contract tests (Pact, Spring Cloud Contract), (4) End-to-end tests with Postman/newman, (5) Load tests (k6, artillery), (6) Security tests (OWASP ZAP).

**Code:**
```python
r = range(1_000_000)              # Python 3: lazy, memory-efficient
print(type(r))                   # <class 'range'>
print(999_999 in r)              # O(1) membership
print(r[5:8])                    # slicing works
```

## Q70: What is contract testing for REST APIs?
**A:** Contract testing ensures that an API provider and consumer agree on the API contract. The consumer defines expected interactions (pact files), and the provider verifies it can satisfy those expectations. It catches breaking changes early without full end-to-end tests.

**Code:**
```python
from functools import reduce

nums = [1, 2, 3, 4]
print(list(map(lambda x: x * 2, nums)))            # [2,4,6,8]
print(list(filter(lambda x: x % 2 == 0, nums)))    # [2,4]
print(reduce(lambda a, b: a + b, nums))            # 10
```

## Q71: What is API gateway?
**A:** An API gateway is a single entry point for API requests. It handles authentication, rate limiting, routing, request/response transformation, caching, logging, and monitoring. Examples: Kong, AWS API Gateway, Apigee, Traefik, NGINX, Ambassador.

**Code:**
```python
print(any([0, 1, 2]))       # True  - at least one truthy
print(all([1, 2, 3]))       # True  - all truthy
print(any([]), all([]))     # False True (empty edge cases)
```

## Q72: What are the benefits of using an API gateway?
**A:** (1) Centralized authentication and authorization, (2) Rate limiting and throttling, (3) Request/response transformation, (4) Protocol translation (HTTP to gRPC), (5) Aggregation of multiple microservices, (6) Caching, (7) Monitoring and analytics, (8) API versioning.

**Code:**
```python
import argparse, sys

# sys.argv: list of CLI args, argv[0] = script name
print("script:", sys.argv[0])

parser = argparse.ArgumentParser()
parser.add_argument("--count", type=int, default=1)
parser.add_argument("name")
args = parser.parse_args(["--count", "3", "world"])   # simulated argv
print(args.name, args.count)
```

## Q73: What is the difference between API gateway and load balancer?
**A:** A load balancer distributes traffic across servers based on algorithms (round-robin, least connections). An API gateway performs higher-level functions: authentication, routing based on path, rate limiting, and protocol translation. An API gateway often includes a load balancer.

**Code:**
```python
import cProfile

def work():
    total = 0
    for i in range(1_000_000):
        total += i
    return total

cProfile.run("work()")
```

## Q74: What is idempotency in the context of payment APIs?
**A:** In payment APIs, idempotency ensures that a charge request is processed exactly once, even if the client retries due to network failures. The client sends an Idempotency-Key header. The server checks for duplicates before processing, preventing double charges.

**Code:**
```python
# file.py
def main():
    print("runs when executed directly")

if __name__ == "__main__":
    main()                # skipped when imported
```

## Q75: How do you handle partial success in batch operations?
**A:** Return 200 OK with a response detailing successes and failures per item: { "results": [ { "status": "success", "id": 1 }, { "status": "error", "id": 2, "error": "Validation failed" } ] }. Use 207 Multi-Status for WebDAV-style responses.

**Code:**
```python
from functools import wraps

def logged(func):
    @wraps(func)               # preserve __name__, __doc__
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

@logged
def greet():
    """Says hi."""
    return "hi"

print(greet.__name__, greet.__doc__)   # greet Says hi.
```

## Q76: What is the 207 Multi-Status response?
**A:** 207 Multi-Status (WebDAV) provides status for multiple independent operations in a single response body. Each operation has its own status code, headers, and body. It is useful for batch operations where each item may succeed or fail independently.

**Code:**
```python
from abc import ABC, abstractmethod

class Shape(ABC):
    @property
    @abstractmethod
    def area(self): ...        # must be implemented by subclasses

class Circle(Shape):
    def __init__(self, r):
        self.r = r
    @property
    def area(self):
        return 3.14159 * self.r ** 2

print(Circle(2).area)          # 12.56636
```

## Q77: How do you implement search with faceted filtering?
**A:** Faceted filtering returns aggregate counts alongside search results. The API accepts filter parameters and returns a facets object: { "facets": { "category": { "electronics": 42, "books": 15 }, "price_range": { "0-50": 100, "51-100": 50 } } }. Elasticsearch/Solr power such features.

**Code:**
```python
from abc import ABC, abstractmethod

class Animal(ABC):
    @abstractmethod
    def sound(self): ...

class Dog(Animal):             # must implement all abstract methods
    def sound(self):
        return "woof"

print(Dog().sound())
# Animal() -> TypeError: Can't instantiate abstract class
```

## Q78: What is the Richardson Maturity Model?
**A:** The Richardson Maturity Model (RMM) grades REST APIs on three levels: Level 0 (POX, single endpoint, SOAP-like), Level 1 (Resources, multiple endpoints), Level 2 (HTTP Verbs, proper method usage), Level 3 (HATEOAS, hypermedia controls). Level 3 is fully RESTful.

**Code:**
```python
class Positive:
    def __init__(self):
        self.data = {}
    def __get__(self, obj, objtype=None):     # reading the attribute
        return self.data[id(obj)]
    def __set__(self, obj, value):            # writing the attribute
        if value < 0:
            raise ValueError("must be >= 0")
        self.data[id(obj)] = value

class Prices:
    price = Positive()

p = Prices()
p.price = 5
print(p.price)      # 5
# p.price = -1   -> ValueError
```

## Q79: What is a RESTful vs REST-like API?
**A:** A RESTful API fully adheres to REST constraints (uniform interface, stateless, cacheable, HATEOAS). A REST-like API uses some REST principles (HTTP methods, resource URIs) but does not fully satisfy all constraints (e.g., no HATEOAS). Most real-world APIs are REST-like.

**Code:**
```python
class Descriptor:
    def __get__(self, obj, objtype=None):
        print("get")
        return obj.stored
    def __set__(self, obj, value):
        print("set")
        obj.stored = value
    def __delete__(self, obj):
        print("delete")
        del obj.stored

class Demo:
    x = Descriptor()
    def __init__(self):
        self.stored = None

d = Demo()
d.x = 10    # set -> get
print(d.x)
del d.x     # delete
```

## Q80: How do you handle API deprecation?
**A:** (1) Announce deprecation well in advance, (2) Add Deprecation and Sunset HTTP headers: Deprecation: true, Sunset: Sat, 1 Jan 2025 00:00:00 GMT, (3) Include deprecation info in response body, (4) Maintain backward compatibility during transition, (5) Log usage to identify affected clients.

**Code:**
```python
class Config:
    def __getattribute__(self, name):        # called for EVERY attribute read
        if name == "secret":
            raise AttributeError("denied")
        return super().__getattribute__(name)
    def __getattr__(self, name):             # only when attribute not found
        return "default"

c = Config()
c.visible = 1
print(c.visible)     # 1
print(c.anything)    # default (via __getattr__)
```

## Q81: What are Sunset and Deprecation headers?
**A:** The Deprecation header indicates the API is deprecated (value: true with optional version info). The Sunset header specifies the date when the API will be removed. These headers allow clients to discover deprecation programmatically.

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
print(a is b)       # True - always the same instance
```

## Q82: How do you handle API documentation?
**A:** Use OpenAPI/Swagger for machine-readable specs. Generate interactive documentation with Swagger UI, ReDoc, or Stoplight. Keep docs versioned alongside the API. Use examples, error code documentation, and quickstart guides. Auto-generate changelogs from API specs.

**Code:**
```python
class Adder:
    def __init__(self, n):
        self.n = n
    def __call__(self, x):       # makes instances callable
        return x + self.n

add5 = Adder(5)
print(add5(10))                  # 15
print(callable(add5))            # True
```

## Q83: What is API security best practices?
**A:** (1) Use HTTPS always, (2) Authenticate all requests, (3) Implement authorization checks per endpoint, (4) Rate limit to prevent abuse, (5) Validate and sanitize all inputs, (6) Use proper CORS configuration, (7) Implement audit logging, (8) Rotate API keys regularly, (9) Use OAuth 2.0 for delegated access.

**Code:**
```python
class Ctx:
    def __enter__(self):
        print("enter")
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        print("exit")
        return False

with Ctx():
    print("body")
```

## Q84: What is the difference between authentication and authorization in REST?
**A:** Authentication verifies who the client is (identity). Authorization determines what the client can do (permissions). Authentication typically happens first (via API key, JWT, OAuth token). Authorization checks permissions on each request using roles or scopes.

**Code:**
```python
from contextlib import suppress
import os

with suppress(FileNotFoundError):      # ignore, like except: pass
    os.remove("missing.txt")
print("nothing raised")
```

## Q85: What are OAuth 2.0 scopes?
**A:** Scopes define specific permissions granted to an access token. Examples: "read:users" (read user data), "write:orders" (create orders), "admin" (full access). Scopes are requested by the client during OAuth flow and presented by the token. The API checks scopes before processing requests.

**Code:**
```python
from contextlib import contextmanager

@contextmanager
def managed():
    print("before")        # runs on __enter__
    try:
        yield "value"      # yielded value becomes `as` target
    finally:
        print("after")     # runs on __exit__

with managed() as res:
    print("body", res)
```

## Q86: What is the Principle of Least Privilege in API security?
**A:** The Principle of Least Privilege means granting only the minimum permissions necessary for a client to perform its function. In APIs: use granular scopes, restrict resource access by ownership (users can only access their own data), and deny access by default.

**Code:**
```python
import json, pickle

data = {"a": 1, "b": [1, 2]}

print(json.dumps(data))              # readable, cross-language, safe
print(pickle.dumps(data))            # binary, Python-specific, unsafe
print(pickle.loads(pickle.dumps(data)))
```

## Q87: How do you prevent CSRF in REST APIs?
**A:** CSRF (Cross-Site Request Forgery) is less relevant for APIs using token-based authentication (JWT, Bearer tokens) since the token is not automatically sent by the browser. For cookie-based auth: use SameSite cookies, CSRF tokens, and check custom headers (X-Requested-By).

**Code:**
```python
class Connection:
    def __enter__(self):
        print("connected")
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        print("closed")
        return False      # True would suppress any exception

with Connection() as conn:
    raise ValueError("boom")   # __exit__ still runs, then propagates
```

## Q88: How do you prevent XSS in REST APIs?
**A:** (1) Never render user input as HTML without escaping, (2) Return Content-Type: application/json (not text/html), (3) Set X-Content-Type-Options: nosniff header, (4) Sanitize user input on input, (5) Implement Content Security Policy if serving web content.

**Code:**
```python
import gc

class Cache:
    def __new__(cls, data):        # create/return instance first
        obj = super().__new__(cls)
        obj._cached = data
        return obj
    def __init__(self, data):      # initialize after __new__
        self.data = data

c = Cache([1, 2])
print(c.data, c._cached)
```

## Q89: What is content-type sniffing and how to prevent it?
**A:** Content-type sniffing is when browsers guess the content type despite the declared Content-Type. Prevent with X-Content-Type-Options: nosniff header. This is especially important for APIs returning JSON to prevent MIME-type confusion attacks.

**Code:**
```python
class Parent:
    attr = "parent"

class Child(Parent):
    pass

c = Child()
print(c.attr)          # instance __dict__? no -> class -> parent (MRO)
c.attr = "own"         # now stored in instance __dict__
print(c.attr)
```

## Q90: How do you monitor REST API health?
**A:** (1) Health check endpoints (GET /health, GET /ready), (2) Metrics endpoints (Prometheus /metrics), (3) Distributed tracing (Jaeger, Zipkin), (4) Structured logging with correlation IDs, (5) Synthetic monitoring (ping endpoints periodically), (6) API analytics (request volume, latency, error rates).

**Code:**
```python
class WithDict:
    pass

class WithSlots:
    __slots__ = ("x",)

a, b = WithDict(), WithSlots()
print(hasattr(a, "__dict__"))    # True  - allows dynamic attrs
print(hasattr(b, "__dict__"))    # False - fixed slots only
```

## Q91: What is a health check endpoint?
**A:** A health check endpoint (typically GET /health or GET /healthz) returns the API's operational status. It may perform checks on dependencies (database, cache, external services) and return appropriate status codes: 200 OK (healthy), 503 Service Unavailable (unhealthy).

**Code:**
```python
import weakref

class Payload: pass

p = Payload()
ref = weakref.ref(p)      # weak reference; doesn't stop GC
print(ref() is p)         # True - object still alive

del p
print(ref())              # None - object collected
```

## Q92: What is the difference between /health and /ready endpoints?
**A:** /health (liveness) indicates if the application is running. /ready (readiness) indicates if the application is ready to serve traffic (dependencies are available). In Kubernetes, liveness probes restarts unresponsive pods; readiness probes stop routing traffic to unready pods.

**Code:**
```python
import weakref

class Payload: pass

cache = weakref.WeakValueDictionary()
p = Payload()
cache["k"] = p

print(len(cache))         # 1
del p
print(len(cache))         # 0 - entry auto-removed after GC
```

## Q93: How do you implement logging in REST APIs?
**A:** Use structured logging (JSON format) with correlation IDs. Log: request method, path, status code, latency, user ID, request ID, and errors. Include trace IDs for distributed tracing. Use log levels (debug, info, warn, error). Never log sensitive data (passwords, tokens, PII).

**Code:**
```python
class Temp:
    def __del__(self):      # called when instance is being destroyed
        print("cleaning up")

t = Temp()
del t                      # prints "cleaning up"
# Prefer context managers for guaranteed cleanup
```

## Q94: What is a correlation ID?
**A:** A correlation ID (or request ID) is a unique identifier assigned to each API request. It is generated by the client or the first service in the chain and propagated to all downstream services. It helps correlate logs, traces, and errors across distributed systems.

**Code:**
```python
print(isinstance(True, int))    # True  - checks inheritance chain
print(type(True) == int)        # False - exact type is bool
```

## Q95: What is distributed tracing?
**A:** Distributed tracing tracks a request as it flows through multiple microservices. Each service adds a span (operation) to the trace. Tools like Jaeger, Zipkin, and OpenTelemetry collect and visualize traces, showing latency breakdowns and error propagation across services.

**Code:**
```python
from functools import total_ordering

@total_ordering
class Score:
    def __init__(self, v):
        self.v = v
    def __eq__(self, other):
        return self.v == other.v
    def __lt__(self, other):            # total_ordering fills in the rest
        return self.v < other.v

print(Score(2) >= Score(1))    # True (auto-generated)
```

## Q96: What is the difference between synchronous and asynchronous REST APIs?
**A:** Synchronous APIs return the response immediately after processing (typical for CRUD). Asynchronous APIs accept the request, return 202 Accepted, and process the request later. The client polls a status endpoint or receives a webhook callback. Asynchronous is used for long-running operations.

**Code:**
```python
from functools import total_ordering

@total_ordering                 # generates missing comparison methods
class Version:
    def __init__(self, n):
        self.n = n
    def __eq__(self, other):
        return self.n == other.n
    def __lt__(self, other):
        return self.n < other.n

print(Version(2) > Version(1))   # True - derived from __eq__/__lt__
```

## Q97: What is a webhook in the context of REST APIs?
**A:** A webhook is a callback HTTP endpoint provided by the client, which the server calls when an event occurs. Instead of polling, the server POSTs a notification to the webhook URL. Webhooks are used for asynchronous notifications (payment confirmations, deployment status, data changes).

**Code:**
```python
from dataclasses import dataclass

@dataclass                   # generates __init__, __repr__, __eq__, ...
class Point:
    x: int
    y: int

p = Point(1, 2)
print(p)                     # Point(x=1, y=2)
print(p == Point(1, 2))      # True
```

## Q98: How do you secure webhooks?
**A:** (1) Sign the webhook payload (HMAC-SHA256) and include the signature in a header, (2) Verify the signature on the receiver side, (3) Use HTTPS, (4) Implement webhook secret rotation, (5) Validate the payload schema, (6) Respond with 200 OK quickly, (7) Implement retry logic with exponential backoff.

**Code:**
```python
from dataclasses import dataclass, field

@dataclass
class Item:
    name: str
    tags: list = field(default_factory=list)   # mutable default fix
    price: float = field(default=0.0, repr=False)

i = Item("pen")
i.tags.append("stationery")
print(i)                     # name in repr, price hidden
```

## Q99: What is the difference between server-sent events (SSE) and WebSocket for real-time APIs?
**A:** SSE is a unidirectional (server-to-client) protocol over HTTP, simple to implement, auto-reconnects, but limited to text data. WebSocket is bidirectional, full-duplex, supports binary data, but requires custom reconnection handling. SSE is simpler for push notifications; WebSocket is needed for interactive real-time apps.

**Code:**
```python
from dataclasses import dataclass

@dataclass
class Rect:
    w: float
    h: float
    area: float = 0.0

    def __post_init__(self):         # extra init logic after defaults set
        self.area = self.w * self.h

r = Rect(3, 4)
print(r.area)     # 12.0
```

## Q100: What is API-first development?
**A:** API-first development means designing the API contract (OpenAPI spec) before writing any implementation code. Benefits: parallel frontend/backend development, contract testing, automatic documentation, client SDK generation, and a design review process that catches issues early. The API spec becomes the single source of truth.

**Code:**
```python
from typing import NewType, List

Vector = List[float]                  # type alias
UserId = NewType("UserId", int)       # distinct type at type-check time

def dot(v: Vector) -> float:
    return sum(x * x for x in v)

print(dot([1.0, 2.0]))
uid = UserId(42)
print(uid)                            # runtime: plain int
```

