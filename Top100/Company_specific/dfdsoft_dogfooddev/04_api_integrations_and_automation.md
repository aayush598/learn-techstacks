# DFDSOFT / DogFoodDev — API Integrations & Automation (100 Q&A)
> Role: AI Coding & Agent Development Specialist  > Candidate: Aayush Gid (REST APIs/Gmail/Twitter/YouTube APIs/Google Drive automation/webhooks background)
---

## Section 1: REST API Fundamentals

**Q1: What are the main HTTP methods and their intended semantics?**
A: `GET` (read, safe, idempotent), `POST` (create), `PUT` (full replace, idempotent), `PATCH` (partial update), `DELETE` (remove, idempotent). In your Marketing AI Agent, you'd use GET for fetching tweets, POST for sending Gmail drafts, PUT/PATCH for updating Google Drive metadata.

**Q2: What is the difference between idempotent and safe HTTP methods?**
A: Safe methods don't mutate server state (GET, HEAD, OPTIONS). Idempotent methods produce the same result when called multiple times (GET, PUT, DELETE, HEAD, OPTIONS). POST and PATCH are neither safe nor idempotent. This matters for retry logic — if your Twitter API call fails, you can safely retry a GET but not necessarily a POST.

**Q3: Explain common HTTP status code categories.**
A: 1xx (informational), 2xx (success: 200 OK, 201 Created, 204 No Content), 3xx (redirection: 301, 302, 304 Not Modified), 4xx (client error: 400 Bad Request, 401 Unauthorized, 403 Forbidden, 404 Not Found, 429 Too Many Requests), 5xx (server error: 500, 502, 503, 504). Your API integrations should handle 429 and 5xx with retries.

**Q4: When should you return 201 vs 200 for a POST request?**
A: 201 Created when a new resource is successfully created (include a `Location` header pointing to the new resource). 200 OK for general success, such as a POST that triggers an action rather than creating a resource. For example, posting a tweet via Twitter API returns 201; posting to a webhook endpoint might return 200.

**Q5: What are path parameters vs query parameters?**
A: Path parameters identify a specific resource and are part of the URL structure: `GET /users/{userId}/tweets`. Query parameters filter or paginate: `GET /tweets?max_results=10&since_id=123`. Path params are required identifiers; query params are optional modifiers.

**Q6: What role do HTTP headers play in API communication?**
A: Headers carry metadata. Key ones: `Content-Type` (application/json), `Authorization` (Bearer token), `Accept`, `X-Request-ID` (tracing), `Cache-Control`, `RateLimit-*` (rate limit info). In your Google Drive integration, `Authorization: Bearer {token}` and `Content-Type: multipart/form-data` for file uploads are essential.

**Q7: What is the request/response body and when is it used?**
A: The body carries payload data for POST, PUT, PATCH requests. GET and DELETE typically have no body. Always set `Content-Type` header. Example for Gmail API:
```python
import json
resp = requests.post(url, headers={"Content-Type": "application/json"}, data=json.dumps({"to": "x@y.com", "subject": "Hi"}))
```

**Q8: What is content negotiation in HTTP?**
A: Client and server agree on data format via `Accept` (client) and `Content-Type` (server) headers. A client sends `Accept: application/json` to request JSON; the server responds with `Content-Type: application/json`. If the server can't serve that format, it returns 406 Not Acceptable.

**Q9: What is the difference between 401 and 403?**
A: 401 Unauthorized means "you are not authenticated" — include a valid `WWW-Authenticate` header. 403 Forbidden means "you are authenticated but not authorized" for this resource. If your Twitter API token is expired you get 401; if your token is valid but lacks the `tweet.write` scope, you get 403.

**Q10: How does content type `application/x-www-form-urlencoded` differ from `application/json`?**
A: `x-www-form-urlencoded` is the default for HTML forms — key=value pairs encoded with `&` and `%`-escaping. `application/json` sends structured JSON data. JSON is preferred for modern APIs because it supports nested objects, arrays, and is easier to parse. Use form-encoded for OAuth token exchanges (e.g., getting Gmail OAuth tokens).

---

## Section 2: API Authentication

**Q11: Explain API key authentication and its tradeoffs.**
A: A static secret string passed as a header or query param. Simple but no per-request signing, no expiry, no fine-grained scopes. Good for server-to-server with controlled environments. Example: `X-API-Key: abc123`. Risk: key leaks expose the API permanently. Use environment variables, never commit keys.

**Q12: What is OAuth2 and why does it exist?**
A: OAuth2 is an authorization framework that lets third-party apps access user resources without sharing passwords. The user authorizes your app, the app receives access/refresh tokens. This is how your Marketing AI Agent accesses Gmail — users authorize without giving you their password.

**Q13: Describe the OAuth2 Authorization Code flow.**
A: 1) Client redirects user to auth server with `client_id`, `redirect_uri`, `scope`, `state`. 2) User logs in and consents. 3) Auth server redirects back with an authorization `code`. 4) Client exchanges code for `access_token` + `refresh_token` via server-side POST. This is the standard flow for web apps accessing Gmail, Google Drive.

**Q14: What is PKCE and when should you use it?**
A: Proof Key for Code Exchange. Adds a `code_verifier`/`code_challenge` pair to the Authorization Code flow to prevent authorization code interception. Required for public clients (mobile apps, SPAs, CLI tools). Even for confidential clients, PKCE is now recommended as best practice.
```python
import hashlib, base64, secrets
verifier = secrets.token_urlsafe(64)
challenge = base64.urlsafe_b64encode(hashlib.sha256(verifier.encode()).digest()).rstrip(b"=").decode()
```

**Q15: What is the Client Credentials flow?**
A: For machine-to-machine auth with no user context. Client sends `client_id` + `client_secret` directly to the token endpoint and receives an `access_token`. Use for server-side services that call APIs like internal tools, CI/CD pipelines, or backend services talking to each other.

**Q16: Explain JWT structure and how it's validated.**
A: JWT has three base64url-encoded parts: Header (algorithm, type), Payload (claims: `sub`, `iss`, `exp`, `aud`, custom data), Signature (header+payload signed with secret/public key). Validation: check signature, verify `exp` hasn't passed, verify `iss` and `aud` match. JWTs are stateless — no server lookup needed but can't be revoked without a blocklist.

**Q17: What are refresh tokens and why are they needed?**
A: Access tokens are short-lived (e.g., 1 hour). Refresh tokens are long-lived and used to obtain new access tokens without re-authentication. Critical for long-running automations like your Google Drive sync that needs persistent access. Always store refresh tokens securely, rotate them on use.

**Q18: What are OAuth scopes and how do they work?**
A: Scopes define the granular permissions a token grants. Example for Gmail: `https://www.googleapis.com/auth/gmail.readonly`, `https://www.googleapis.com/auth/gmail.send`. The user sees these during consent. Tokens can only perform actions within their granted scopes. Principle of least privilege: request only what you need.

**Q19: How do you handle token expiry in an automation pipeline?**
A: Proactively refresh before expiry. Store the `expires_at` timestamp with the token. Check remaining TTL before each API call; if below threshold (e.g., 5 minutes), refresh first. Handle 401 responses by attempting one refresh before failing.
```python
def get_valid_token(token_data):
    if time.time() > token_data["expires_at"] - 300:
        token_data = refresh_access_token(token_data["refresh_token"])
    return token_data["access_token"]
```

**Q20: What is a bearer token and how is it used?**
A: A bearer token is a credential that grants access to whoever "bears" (presents) it. Sent in the `Authorization: Bearer {token}` header. No additional proof of possession required — if intercepted, anyone can use it. That's why HTTPS is mandatory and tokens should be short-lived.

---

## Section 3: Webhooks

**Q21: What are webhooks and how do they differ from polling?**
A: Webhooks are push-based — the source server sends an HTTP POST to your registered URL when an event occurs. Polling is pull-based — your client repeatedly queries the API. Webhooks are more efficient (no wasted requests), lower latency, and reduce server load. For example, instead of polling Twitter's API every minute for new mentions, register a webhook to get instant notifications.

**Q22: How do you design a webhook receiver endpoint?**
A: Must be publicly accessible, handle POST requests, validate the signature, parse the payload, return 2xx quickly (< 5s), and process asynchronously.
```python
from fastapi import FastAPI, Request, HTTPException
import hmac, hashlib

app = FastAPI()

@app.post("/webhooks/twitter")
async def receive_twitter_webhook(request: Request):
    body = await request.body()
    signature = request.headers.get("x-twitter-webhook-signature")
    if not verify_hmac(body, signature, WEBHOOK_SECRET):
        raise HTTPException(status_code=401)
    # Queue for async processing
    await process_event(body)
    return {"status": "ok"}  # Return quickly
```

**Q23: What is HMAC signature verification for webhooks?**
A: HMAC (Hash-based Message Authentication Code) proves the payload hasn't been tampered with and came from the expected sender. The sender signs the payload with a shared secret; the receiver recomputes the signature and compares. Never skip this — without it, anyone could POST fake events to your endpoint.

**Q24: Implement HMAC-SHA256 verification in Python.**
A:
```python
import hmac, hashlib

def verify_hmac(payload: bytes, signature: str, secret: str) -> bool:
    expected = hmac.new(
        secret.encode(), payload, hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(f"sha256={expected}", signature)
```
Use `hmac.compare_digest` to prevent timing attacks. Check your provider's prefix convention (GitHub uses `sha256=`, Stripe uses `v1=`).

**Q25: What are webhook retries and why do they matter?**
A: If your endpoint returns non-2xx or times out, the sender retries with exponential backoff. Stripe retries up to 3 days; GitHub retries 3 times. Your endpoint MUST be idempotent — process the same event multiple times without side effects. Use an event ID to deduplicate.

**Q26: How do you ensure webhook idempotency?**
A: Track processed event IDs in a database or cache with a TTL. On receipt, check if the ID exists; if yes, return 200 without processing.
```python
async def handle_webhook(event_id: str, payload: dict):
    if await redis.exists(f"webhook:{event_id}"):
        return  # Already processed
    await process_event(payload)
    await redis.setex(f"webhook:{event_id}", 86400, "1")  # TTL 24h
```

**Q27: What is webhook payload verification beyond HMAC?**
A: Timestamp validation — reject events older than a threshold (e.g., 5 minutes) to prevent replay attacks. Nonce usage — some providers include a unique nonce per event. IP allowlisting — restrict to provider's known IPs. Always combine HMAC + timestamp validation.

**Q28: What is the difference between synchronous and asynchronous webhook processing?**
A: Synchronous: process the event in the request handler and return the result. Risk: if processing is slow, the sender may timeout. Asynchronous: accept the event immediately (return 200), queue it for background processing. Recommended for anything beyond trivial logic. Use a message queue (Redis, SQS, n8n's queue).

**Q29: How does Stripe's webhook pattern differ from GitHub's?**
A: Stripe: sign payload with `whsec_` secret, signature in `Stripe-Signature` header (includes timestamp), retries for days, extensive event catalog. GitHub: HMAC-SHA256, signature in `X-Hub-Signature-256`, retries 3 times, uses `X-GitHub-Event` header for event type. Both use the `id` field for deduplication.

**Q30: What is a webhook vs an event-driven architecture?**
A: Webhooks are a specific implementation of event-driven architecture — HTTP-based push notifications between services. Event-driven architecture is broader: includes message queues (Kafka, RabbitMQ), event buses, pub/sub patterns, CQRS, and event sourcing. Webhooks are the simplest form for cross-service communication.

---

## Section 4: API Design Best Practices

**Q31: How should you version a REST API?**
A: URL path versioning is most common: `/v1/users`, `/v2/users`. Other approaches: header (`Accept: application/vnd.api+json;version=2`), query param (`?version=2`). URL path is simplest and most visible. Never break existing versions. Deprecate with `Sunset` and `Deprecation` headers, give 6-12 months notice.

**Q32: What are the main pagination strategies?**
A: **Offset-based**: `?page=2&per_page=20` — simple but fragile with concurrent inserts/deletes. **Cursor-based**: `?cursor=abc123&limit=20` — stable, uses a pointer to the next record (Twitter API uses `next_token`). **Keyset**: `?created_after=2024-01-01&limit=20` — efficient for large datasets. For your Marketing AI Agent fetching Twitter data, cursor-based is ideal.

**Q33: What is RFC 7807 Problem Details?**
A: A standardized error response format:
```json
{
  "type": "https://api.example.com/errors/validation",
  "title": "Validation Error",
  "status": 422,
  "detail": "The 'email' field must be a valid email address",
  "instance": "/users/123"
}
```
Provides machine-readable `type`, human-readable `title`/`detail`, and a `status` code. Better than ad-hoc error objects.

**Q34: How should rate limiting information be communicated?**
A: Via response headers: `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset` (Unix timestamp). On 429, include `Retry-After` header. Your API client should parse these and proactively throttle before hitting limits.

**Q35: What is HATEOAS and is it practical?**
A: Hypermedia As the Engine of Application State — API responses include links to related actions/resources. Example: `{"links": {"self": "/users/1", "tweets": "/users/1/tweets"}}`. Theoretically elegant for discoverability, but adds complexity and most modern APIs skip it in favor of OpenAPI documentation. Mention it in interviews for bonus points.

**Q36: What is OpenAPI/Swagger and why use it?**
A: OpenAPI (formerly Swagger) is a specification for describing REST APIs. It defines endpoints, request/response schemas, authentication, and examples. Benefits: auto-generate client SDKs, interactive docs (Swagger UI), contract testing, server stubs. Great for team collaboration and integration partner onboarding.

**Q37: How do you handle filtering, sorting, and field selection in an API?**
A: `GET /tweets?author_id=123&sort_by=created_at&order=desc&fields=id,text,created_at`. Use consistent conventions: `sort_by`/`sort_order`, `fields` for sparse fieldsets, `q` for text search. Document allowed filter combinations. Validate unsupported filters with 400, not silent ignoring.

**Q38: What is the difference between PUT and PATCH?**
A: PUT replaces the entire resource — you must send all fields. PATCH applies partial updates — only the fields you want to change. PUT is idempotent; PATCH may or may not be depending on implementation. For your Google Drive file metadata updates, PATCH is more efficient — update just the name without resending parent and MIME type.

**Q39: Why should API error responses be structured?**
A: Structured errors enable consistent client handling. Always include: HTTP status code, machine-readable error code, human-readable message, and optionally a request ID for debugging. Example: `{"error": {"code": "RATE_LIMITED", "message": "...", "retry_after": 30, "request_id": "req_abc123"}}`.

**Q40: What is API gateway pattern and when to use it?**
A: An API gateway is a single entry point that routes requests to backend services, handles authentication, rate limiting, request transformation, and response aggregation. Use when you have microservices or want to consolidate cross-cutting concerns. Examples: Kong, AWS API Gateway, Cloudflare Workers. Avoids duplicating auth/rate-limit logic in every service.

---

## Section 5: SaaS Integrations

**Q41: Walk through building a Gmail API integration to send emails.**
A: 1) Set up OAuth2 credentials in Google Cloud Console. 2) Request `gmail.send` scope. 3) Complete OAuth flow to get tokens. 4) Encode email as base64url MIME message. 5) POST to `https://gmail.googleapis.com/gmail/v1/users/me/messages/send`.
```python
import base64
from email.mime.text import MIMEText

def send_gmail(service, to, subject, body):
    message = MIMEText(body)
    message["to"] = to
    message["subject"] = subject
    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
    return service.users().messages().send(
        userId="me", body={"raw": raw}
    ).execute()
```

**Q42: What are the key considerations for Google Drive API automation?**
A: Handle token refresh for long-running syncs. Use service accounts for domain-wide delegation when automating across an organization. Respect quota limits (100 queries/100 seconds per user). Use `files.list` with `pageToken` for pagination. Watch for file size limits on uploads. Implement retry for 429/503 responses.

**Q43: How do you integrate with the Twitter/X API v2?**
A: Use OAuth 2.0 with PKCE (preferred) or OAuth 1.0a. Key endpoints: `GET /2/tweets/search/recent`, `POST /2/tweets`, `GET /2/users/:id/tweets`. Twitter uses bearer tokens for read-only and OAuth for write. Respect rate limits (300 tweets/15 min for search). Use `expansions` and `tweet.fields` for efficient data retrieval.

**Q44: What are Google Workspace API quota and best practices?**
A: Default quota: 100 requests/100 seconds/user (varies by API). Best practices: batch requests (up to 100 per batch), cache responses, use `fields` parameter to reduce payload, implement exponential backoff on 429s, use service accounts for server-to-server, and handle token refresh gracefully.

**Q45: How do you handle OAuth token refresh in a multi-user system?**
A: Store tokens per user in a database with `expires_at`. Before each API call, check TTL. If expired, refresh using the refresh token and update the database. Handle invalid_grant errors (refresh token revoked) by prompting re-authorization. Use database transactions to prevent race conditions during concurrent refreshes.

**Q46: What is the Stripe webhook integration pattern?**
A: 1) Register webhook endpoint in Stripe Dashboard. 2) Select events (e.g., `payment_intent.succeeded`, `invoice.paid`). 3) Verify `Stripe-Signature` header with your `whsec_` secret. 4) Parse the event type and handle accordingly. 5) Return 200 immediately, process async. 6) Store event ID for deduplication.

**Q47: How do you build a GitHub API integration for automation?**
A: Use Personal Access Tokens for simple cases, GitHub Apps for production. Key endpoints: `GET /repos/{owner}/{repo}/issues`, `POST /repos/{owner}/{repo}/issues/{issue_number}/comments`. Use Octokit SDKs or direct REST calls. Handle rate limits via `X-RateLimit-*` headers. For webhooks, verify with HMAC-SHA256 and the webhook secret.

**Q48: What are common pitfalls when integrating with multiple SaaS APIs?**
A: Inconsistent auth mechanisms (OAuth vs API keys vs JWT), different rate limit strategies, varying webhook formats, timezone handling inconsistencies, different pagination styles, and error response formats. Create an abstraction layer that normalizes these differences. Log everything for debugging cross-service issues.

**Q49: How do you handle API changes and breaking versions?**
A: Pin to specific API versions where possible. Use feature detection over version detection. Abstract API calls behind client classes so changes are isolated. Monitor provider changelogs and deprecation notices. Implement circuit breakers — if a new version breaks, fall back to a known working version.

**Q50: What is a service account and when should you use one?**
A: A service account is a non-human identity for server-to-server communication. No user interaction needed. Use for: backend services, CI/CD, cron jobs, cross-user automation. In Google Workspace, enable domain-wide delegation to act on behalf of users without individual OAuth flows. Never expose service account keys in client-side code.

---

## Section 6: No-Code Automation

**Q51: Explain Zapier's architecture and when to use it.**
A: Zapier uses "Zaps" — automated workflows with a trigger and one or more actions. Triggers are events (new Gmail email, new row in Google Sheets). Actions are operations (send Slack message, create GitHub issue). Filters and formatters add logic. Best for simple, linear workflows that non-technical team members need to manage. Rate: ~100 tasks/month on free tier.

**Q52: How does Make (formerly Integromat) differ from Zapier?**
A: Make uses visual "scenarios" with branching, routers (conditional paths), iterators (loop over arrays), aggregators, and error handlers. More powerful data transformation, supports complex logic that Zapier can't handle easily. Better for multi-step workflows with parallel branches. Pricing is based on operations, not tasks.

**Q53: What is n8n and what advantages does it offer?**
A: n8n is a self-hostable, open-source workflow automation tool. Advantages: no vendor lock-in, unlimited executions on self-hosted, custom code nodes (JavaScript/Python), direct database access, webhooks as first-class citizens, and a visual editor. Ideal for DFDSOFT's DogFoodDev where you want full control, custom logic, and no per-task pricing.

**Q54: When should you use no-code tools vs writing custom code?**
A: **No-code**: Simple integrations, quick prototypes, non-technical maintainers, standard triggers/actions, low data volume. **Custom code**: Complex logic, performance-critical paths, custom authentication, large data processing, need for version control, unique error handling. In your role, you'll use both — n8n for team workflows, custom Python for agent logic.

**Q55: How do you build a multi-step Zapier workflow for lead processing?**
A: Trigger: New Google Sheets row (new lead). Action 1: Filter — only process if `status = "new"`. Action 2: Format email body with lead data. Action 3: Send via Gmail. Action 4: Update row status to "contacted". Action 5: Create Trello card for follow-up. Add error handling by setting up a Slack notification on failure.

**Q56: Explain Make's router and iterator modules.**
A: **Router**: Splits workflow into parallel branches based on conditions. E.g., route leads to different email templates based on company size. **Iterator**: Loops over an array of items, executing subsequent modules for each. E.g., iterate over an array of recipients and send individual emails. Use aggregators to recombine results after iteration.

**Q57: How do you handle errors in n8n workflows?**
A: Use the Error Trigger node to catch failures. Configure each node's "On Error" setting: `Continue` (skip and continue), `Stop Workflow` (halt), or `Continue Regularly` (use fallback output). Use the IF node to branch on error conditions. Log errors to a database or notification service. Set up retry policies on nodes that call external APIs.

**Q58: What is webhook-based triggering in no-code tools?**
A: All three tools support webhooks as triggers. You get a unique URL; when an external service POSTs to it, the workflow fires. This is how you'd connect your custom Python service to Zapier/Make/n8n. In n8n, the Webhook node returns the payload directly. In Zapier, use "Webhooks by Zapier" as the trigger.

**Q59: How do you debug failed automations in Make?**
A: Make provides an execution history with step-by-step inspection. Check the input/output data of each module. Common issues: missing data mapping (wrong variable reference), rate limits, authentication expiry, incorrect data formatting. Use the "Scenario Blueprint" to export/import for sharing. Enable error notifications to Slack/email.

**Q60: When would you recommend n8n over Zapier/Make for a client?**
A: When the client needs: data privacy (self-hosted), unlimited executions, custom code integration, complex branching with code nodes, webhook-heavy architectures, or budget constraints at scale. For DFDSOFT's DogFoodDev projects, n8n is ideal since it can be deployed alongside your infrastructure, version-controlled as code, and extended with custom nodes.

---

## Section 7: Python for Automation

**Q61: Compare `requests` and `httpx` for API automation.**
A: `requests` is synchronous, battle-tested, wide ecosystem. `httpx` supports both sync and async (`httpx.AsyncClient`), HTTP/2, timeouts, and a requests-compatible API. For automation pipelines hitting multiple APIs concurrently, `httpx` with async is preferred:
```python
async with httpx.AsyncClient() as client:
    r = await client.get("https://api.twitter.com/2/tweets", headers=headers)
```

**Q62: How do you build a retry mechanism with exponential backoff in Python?**
A:
```python
import time, random

def retry_with_backoff(func, max_retries=5, base_delay=1):
    for attempt in range(max_retries):
        try:
            return func()
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            delay = base_delay * (2 ** attempt) + random.uniform(0, 1)
            time.sleep(delay)
```
Add jitter to prevent thundering herd. Use `tenacity` library for production: `@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))`.

**Q63: How do you use `aiohttp` for concurrent API calls?**
A:
```python
import asyncio, aiohttp

async def fetch_all(urls):
    async with aiohttp.ClientSession() as session:
        tasks = [session.get(url) for url in urls]
        responses = await asyncio.gather(*tasks, return_exceptions=True)
        return [await r.json() if not isinstance(r, Exception) else None for r in responses]

results = asyncio.run(fetch_all([url1, url2, url3]))
```
Use `Semaphore` to limit concurrency: `sem = asyncio.Semaphore(10)` to avoid overwhelming the API.

**Q64: How do you use Playwright for web scraping/automation?**
A:
```python
from playwright.async_api import async_playwright

async def scrape_data():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto("https://example.com")
        data = await page.query_selector_all(".item")
        results = [await el.inner_text() for el in data]
        await browser.close()
        return results
```
Playwright handles JS-rendered pages, authentication, and file downloads better than requests. Use for scraping dynamic dashboards.

**Q65: What is the `schedule` library and when to use it?**
A: `schedule` is a lightweight in-process job scheduler for Python:
```python
import schedule, time

def sync_gdrive():
    # sync logic here
    pass

schedule.every(15).minutes.do(sync_gdrive)
while True:
    schedule.run_pending()
    time.sleep(1)
```
Use for simple single-process cron-like tasks. Not suitable for distributed systems — use Celery, Redis queues, or system cron for that.

**Q66: How do you implement a file watcher for automation?**
A: Use `watchdog` for file system events:
```python
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class MyHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            upload_to_drive(event.src_path)

observer = Observer()
observer.schedule(MyHandler(), path="/uploads", recursive=False)
observer.start()
```
Useful for automating uploads when files appear in a local directory.

**Q67: How do you handle rate limiting in Python API clients?**
A: Track request timestamps and sleep when approaching limits:
```python
import time
from collections import deque

class RateLimiter:
    def __init__(self, max_requests, window_seconds):
        self.max_requests = max_requests
        self.window = window_seconds
        self.timestamps = deque()
    
    def wait_if_needed(self):
        now = time.time()
        while self.timestamps and self.timestamps[0] < now - self.window:
            self.timestamps.popleft()
        if len(self.timestamps) >= self.max_requests:
            sleep_time = self.timestamps[0] + self.window - now
            time.sleep(sleep_time)
        self.timestamps.append(time.time())
```

**Q68: How do you build a CLI tool for API automation?**
A: Use `click` or `typer`:
```python
import typer

app = typer.Typer()

@app.command()
def sync_emails(label: str = "INBOX", max_results: int = 100):
    """Sync emails from Gmail."""
    service = get_gmail_service()
    messages = service.users().messages().list(
        userId="me", labelIds=[label], maxResults=max_results
    ).execute()
    typer.echo(f"Found {len(messages.get('messages', []))} emails")

if __name__ == "__main__":
    app()
```
Package with `poetry` or `pipx` for easy distribution.

**Q69: What Python libraries should every API automation developer know?**
A: Core: `requests`/`httpx` (HTTP), `pydantic` (data validation), `fastapi`/`flask` (webhook servers), `celery` (async tasks), `redis` (caching/queues), `aiohttp`/`asyncio` (concurrency), `tenacity` (retries), `python-dotenv` (env vars), `click`/`typer` (CLI), `pytest` (testing), `responses`/`respx` (HTTP mocking).

**Q70: How do you manage secrets and environment variables in automation scripts?**
A: Never hardcode. Use `python-dotenv` for local development, environment variables in production. For multi-service setups, use a secrets manager (AWS Secrets Manager, HashiCorp Vault, Doppler). In n8n, use the Credentials system. For CI/CD, use platform secrets (GitHub Actions secrets, Vercel environment variables).

---

## Section 8: JSON and Data Formats

**Q71: What are JSON parsing pitfalls to watch for?**
A: Trailing commas (not valid JSON), numeric precision loss (large IDs), `null` vs missing keys, Unicode escaping, nested objects getting flattened, date strings not being actual Date objects. In Python, `json.loads()` handles most; use `orjson` or `ujson` for performance with large payloads.

**Q72: How do you validate JSON payloads with Pydantic?**
A:
```python
from pydantic import BaseModel, EmailStr, Field

class WebhookPayload(BaseModel):
    event_type: str = Field(..., alias="type")
    data: dict
    timestamp: int
    id: str

    class Config:
        extra = "forbid"  # Reject unknown fields

# Validates and raises ValidationError on invalid input
payload = WebhookPayload.model_validate_json(raw_json)
```
Use `forbid` mode in production to catch unexpected fields early.

**Q73: When should you use YAML over JSON?**
A: YAML for: configuration files (docker-compose, n8n workflows, GitHub Actions), human-edited data, documents with comments. JSON for: API request/response bodies, data interchange between services, where parsing speed matters. YAML supports comments and is more readable but has gotchas (indentation-sensitive, type coercion surprises).

**Q74: What is JSON Schema and how does it help?**
A: JSON Schema defines the structure, types, and constraints of JSON data:
```json
{
  "type": "object",
  "properties": {
    "email": {"type": "string", "format": "email"},
    "age": {"type": "integer", "minimum": 0}
  },
  "required": ["email"],
  "additionalProperties": false
}
```
Use for: validating webhook payloads, documenting API contracts, generating Pydantic models, testing integrations. Tools: `jsonschema` Python library, `fastjsonschema` for speed.

**Q75: What are the basics of XML that API developers should know?**
A: XML is still used in legacy enterprise APIs (SOAP, some banking/finteware). Key concepts: elements, attributes, namespaces (prevent tag conflicts), CDATA sections, XPath for querying. In Python, use `xml.etree.ElementTree` for parsing. Be aware of XXE (XML External Entity) attacks — always disable external entity processing.

**Q76: What is Protocol Buffers (protobuf) and why use it?**
A: A binary serialization format by Google. Smaller payloads, faster parsing than JSON. Defines message schemas in `.proto` files. Used heavily in gRPC, internal microservice communication, and performance-critical systems. Tradeoff: not human-readable, requires schema compilation. For external APIs, JSON is typically preferred.

**Q77: How do you handle large JSON payloads efficiently?**
A: Use streaming parsers: `ijson` for iteratively parsing large JSON arrays, `orjson` for faster serialization, `ujson` as an alternative. Avoid loading entire large payloads into memory. Process records one at a time:
```python
import ijson

with open("large_file.json", "rb") as f:
    for record in ijson.items(f, "data.item"):
        process(record)
```

**Q78: How do you convert between data formats in Python?**
A: JSON to Python dict: `json.loads()`. Python dict to JSON: `json.dumps()`. CSV: `csv.DictReader`/`DictWriter`. XML to dict: `xmltodict.parse()`. YAML: `yaml.safe_load()` (never `yaml.load()` — security risk). For complex transformations, use `pandas` for tabular data or write custom converters.

**Q79: What is the best way to handle datetime serialization in APIs?**
A: Always use ISO 8601 format: `2024-01-15T10:30:00Z`. In Python:
```python
from datetime import datetime, timezone
import json

class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)

# Or use pydantic with: model_config = {"json_encoders": {datetime: lambda v: v.isoformat()}}
```
Always use UTC internally, convert to local timezone only for display.

**Q80: When should you use streaming responses vs buffered responses?**
A: Stream when: file downloads, large datasets, real-time data, server-sent events. Buffer when: small responses, need complete data before processing, simpler error handling. For API integrations, use streaming for large paginated responses and file transfers. In Python: `requests.get(url, stream=True)` then iterate over `response.iter_content()`.

---

## Section 9: Integration Patterns

**Q81: Explain the circuit breaker pattern and when to use it.**
A: Prevents cascading failures when a downstream service is down. Three states: **Closed** (normal operation, counting failures), **Open** (service is failing, fast-fail all requests), **Half-Open** (allow one test request to check recovery). Use when calling external APIs in production. Python: `pybreaker` library or custom implementation.
```python
import pybreaker

breaker = pybreaker.CircuitBreaker(fail_max=5, reset_timeout=60)

@breaker
def call_external_api():
    return requests.get("https://api.example.com/data")
```

**Q82: What is exponential backoff with jitter?**
A: Retry strategy where delay doubles each attempt plus random jitter. Without jitter, all clients retry at the same time (thundering herd). With jitter, retries are spread out:
```python
import random
delay = min(base * (2 ** attempt) + random.uniform(0, 1), max_delay)
```
Always set a max delay and max retries. Essential for 429 (rate limit) and 503 (service unavailable) responses.

**Q83: Explain the fan-out/fan-in pattern.**
A: Fan-out: one task distributes work to multiple parallel workers. Fan-in: results from all workers are collected/aggregated. Example: Marketing AI Agent fans out to fetch data from Gmail, Twitter, YouTube simultaneously, then fans in to create a unified dashboard. Implement with `asyncio.gather()` or Celery group/chord.

**Q84: What is a dead letter queue (DLQ)?**
A: A queue where messages go when they can't be processed after maximum retries. Prevents poison messages from blocking the queue. Use for: debugging failed events, replaying failed operations, auditing. Set up alerts on DLQ depth. AWS SQS, RabbitMQ, and n8n's error workflows all support DLQ patterns.

**Q85: What is the saga pattern?**
A: A sequence of local transactions where each step publishes an event triggering the next. If a step fails, compensating transactions undo previous steps. Example for a multi-API integration: 1) Create user in CRM, 2) Add to email list, 3) Create project. If step 3 fails, compensate: remove from email list, delete CRM user. Two implementations: choreography (events) or orchestration (central coordinator).

**Q86: How do you implement idempotency in API clients?**
A: Generate a unique idempotency key per logical operation and include it in the request (as header or body). Server-side: store the key with the response; on duplicate key, return the stored response without re-executing. Stripe and many payment APIs support this natively.
```python
import uuid

def make_idempotent_request(func, *args, **kwargs):
    idempotency_key = str(uuid.uuid4())
    kwargs["headers"] = {**kwargs.get("headers", {}), "Idempotency-Key": idempotency_key}
    return func(*args, **kwargs)
```

**Q87: What is the strangler fig pattern in API migration?**
A: Gradually replace a legacy system by routing traffic through a proxy/facade. New functionality goes to the new system; old routes stay on legacy. Over time, more traffic migrates until the legacy system is fully replaced. Use when migrating monolithic APIs to microservices. The facade handles routing, authentication, and response transformation.

**Q88: What is request/response transformation in integrations?**
A: Adapting data formats between systems that don't speak the same schema. E.g., your automation receives a Slack webhook (JSON) but needs to create a Jira issue (different JSON schema). Use middleware or an integration layer to map fields, transform types, and enrich data. Tools: n8n's Set/Code nodes, Make's Data Store, or custom Python transformation functions.

**Q89: How do you handle eventually consistent data across integrated systems?**
A: Accept that data may be temporarily out of sync. Strategies: 1) Use webhooks for near-real-time updates, 2) Periodic reconciliation jobs (compare and sync), 3) Display "last updated" timestamps, 4) Implement read-your-writes consistency where the user immediately sees their own changes, 5) Use CRDTs or merge strategies for conflicts.

**Q90: What is event sourcing and when is it relevant for integrations?**
A: Instead of storing current state, store every change as an immutable event. Enables: complete audit trail, time-travel debugging, replaying events to rebuild state, and multiple read models from the same data. Relevant for integrations when you need to audit all cross-service operations, replay failed integrations, or maintain consistency across eventually consistent systems.

---

## Section 10: Building Custom Integrations

**Q91: How do you design a reusable API client class?**
A:
```python
import httpx
from typing import Optional

class APIClient:
    def __init__(self, base_url: str, token: str):
        self.client = httpx.AsyncClient(
            base_url=base_url,
            headers={"Authorization": f"Bearer {token}"},
            timeout=30.0
        )
    
    async def request(self, method: str, path: str, **kwargs):
        response = await self.client.request(method, path, **kwargs)
        if response.status_code == 429:
            await self._handle_rate_limit(response)
        response.raise_for_status()
        return response.json()
    
    async def get(self, path: str, params: Optional[dict] = None):
        return await self.request("GET", path, params=params)
    
    async def post(self, path: str, data: dict):
        return await self.request("POST", path, json=data)
    
    async def _handle_rate_limit(self, response):
        retry_after = int(response.headers.get("Retry-After", 60))
        await asyncio.sleep(retry_after)
```
This gives you a base for Gmail, Twitter, Drive clients — each inherits and adds service-specific methods.

**Q92: How do you generate an SDK from an OpenAPI spec?**
A: Use OpenAPI Generator: `openapi-generator generate -i spec.yaml -g python -o ./sdk`. This creates a Python package with typed request/response models, auth handling, and documentation. For TypeScript: `-g typescript-fetch`. Customize with templates. For private APIs, generate both client and server stubs. Saves time and ensures consistency.

**Q93: Walk through implementing an OAuth2 Authorization Code flow in a web app.**
A: 1) Redirect user: `https://accounts.google.com/o/oauth2/auth?client_id=X&redirect_uri=Y&scope=Z&response_type=code&state=STATE`. 2) Handle callback at `/auth/callback`: extract `code` and verify `state`. 3) Exchange code: POST to token endpoint with `code`, `client_id`, `client_secret`, `redirect_uri`. 4) Store tokens securely. 5) Use access token for API calls. 6) Use refresh token when access token expires.

**Q94: How do you test webhook integrations end-to-end?**
A: 1) Use `ngrok` or `cloudflared` to expose local endpoint to the internet. 2) Register the public URL with the webhook provider. 3) Trigger test events in the provider's dashboard (e.g., Stripe test mode, GitHub test webhook). 4) Verify payload is received and processed correctly. 5) Test error scenarios: invalid signature, malformed payload, server timeout. 6) Use provider's test/sandbox modes.

**Q95: How do you build a webhook relay service?**
A: A service that receives webhooks from multiple sources and routes them to appropriate handlers. Useful when you have many integrations:
```python
@app.post("/relay/{provider}")
async def relay(provider: str, request: Request):
    body = await request.body()
    verify_signature(provider, body, request.headers)
    event = parse_event(provider, body)
    await queue.publish(f"events.{provider}", event)
    return {"received": True}
```
Supports fan-out to multiple consumers, retry logic, and dead letter queues.

**Q96: What strategies do you use for integration testing?**
A: 1) **Contract testing** (Pact): verify API consumers and providers agree on schemas. 2) **WireMock/MockServer**: simulate external APIs for deterministic tests. 3) **Integration tests with real APIs**: use sandbox/test modes (Stripe test keys, GitHub test repos). 4) **Record and replay**: capture real HTTP responses, replay in tests. 5) **Chaos testing**: simulate failures to test retry/circuit breaker logic.

**Q97: How do you version and manage multiple API integrations across projects?**
A: Create an `integrations/` package with: one module per service (`integrations/gmail.py`, `integrations/twitter.py`), shared base client, environment-based configuration, dependency injection for testability. Version the package independently. Pin API versions in config. Maintain a CHANGELOG documenting upstream API changes. Use feature flags for gradual rollouts of integration updates.

**Q98: How do you handle file uploads to cloud storage via API?**
A: For Google Drive with multipart upload:
```python
from googleapiclient.http import MediaFileUpload

def upload_file(service, file_path, folder_id=None):
    media = MediaFileUpload(file_path, resumable=True)
    file_metadata = {"name": os.path.basename(file_path)}
    if folder_id:
        file_metadata["parents"] = [folder_id]
    return service.files().create(
        body=file_metadata, media_body=media, fields="id"
    ).execute()
```
For large files (>5MB), use resumable uploads. Always check MIME type compatibility and handle 413 (too large) errors.

**Q99: How do you monitor and observe integration health in production?**
A: 1) **Structured logging**: log every API call with request/response metadata, latency, status code. 2) **Metrics**: track success rate, error rate, latency percentiles, rate limit headroom. 3) **Alerting**: set alerts on error rate spikes, webhook processing delays, token expiry approaching. 4) **Dashboards**: Grafana/Datadog showing integration health at a glance. 5) **Distributed tracing**: correlate requests across services with trace IDs.

**Q100: What would you build first in your first 30 days at DFDSOFT to demonstrate API integration expertise?**
A: 1) Audit existing integrations and document them (create an integration catalog). 2) Build a reusable API client library with auth, retries, rate limiting, and logging. 3) Set up n8n for team automations with proper error handling. 4) Create a webhook receiver service with signature verification and event routing. 5) Build a monitoring dashboard showing integration health. 6) Migrate any manual API calls to automated workflows. This demonstrates breadth (multiple integration types) and depth (production-quality patterns).
