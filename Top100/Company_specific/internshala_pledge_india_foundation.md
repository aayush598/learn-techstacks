# Pledge India Foundation — 100 Backend Interview Q&A

> Based on Pledge India Foundation — Backend Development Internship (WFH, entry-level web/backend, HTML-focused)  > Candidate: Aayush Gid (Python/FastAPI/REST/DB/React background)

---

## 1. HTML & Web Fundamentals (Q1–Q14)

**Q1: What does HTML stand for and what is its role in web development?**  
A: HTML (HyperText Markup Language) is the standard markup language used to structure content on the web. It defines the skeleton of a page using elements like headings, paragraphs, links, and forms that browsers render.

**Q2: What is the difference between an element and a tag in HTML?**  
A: A tag is the markup syntax written between angle brackets (e.g., `<p>`), while an element is the full structure including the opening tag, content, and closing tag (e.g., `<p>Hello</p>`).

**Q3: Explain the structure of a basic HTML5 document.**  
A: A minimal HTML5 document includes the doctype, `html`, `head` (with `meta` and `title`), and `body`:
```html
<!DOCTYPE html>
<html lang="en">
<head><meta charset="UTF-8"><title>Page</title></head>
<body><h1>Hello</h1></body>
</html>
```

**Q4: What are semantic HTML elements and why are they important?**  
A: Semantic elements like `<header>`, `<nav>`, `<article>`, and `<footer>` describe their meaning to browsers and screen readers. They improve accessibility, SEO, and code readability.

**Q5: What is the difference between `<div>` and `<span>`?**  
A: `<div>` is a block-level element used to group large sections, while `<span>` is inline and used to style small snippets of text within content.

**Q6: How do you create a hyperlink in HTML?**  
A: Use the anchor tag with an `href` attribute:
```html
<a href="https://example.com">Visit Site</a>
```

**Q7: What are the main form elements and how do you submit data?**  
A: Forms use `<form>` with `action` and `method` attributes, plus inputs like `<input>`, `<textarea>`, and `<button>`. Data is submitted via GET or POST to a backend endpoint.

**Q8: What is the purpose of the `alt` attribute on images?**  
A: The `alt` attribute provides alternative text for screen readers and displays when an image fails to load, improving accessibility and SEO.

**Q9: Explain the difference between GET and POST in HTML forms.**  
A: GET appends data to the URL (visible, cached, limited size) and is for retrieval; POST sends data in the request body (hidden, larger, used for creating/updating data).

**Q10: What are HTML attributes vs HTML content?**  
A: Attributes are additional settings on a tag (e.g., `class`, `id`, `src`), while content is the text or nested elements between the opening and closing tags.

**Q11: How do you embed a video or audio file in HTML?**  
A: Use the `<video>` and `<audio>` elements with `controls`:
```html
<video src="clip.mp4" controls width="320"></video>
```

**Q12: What is the `meta` viewport tag and why is it needed?**  
A: `<meta name="viewport" content="width=device-width, initial-scale=1.0">` makes pages responsive by matching the device width, essential for mobile-friendly sites.

**Q13: What are the differences between `<head>` and `<body>`?**  
A: `<head>` contains metadata (title, links, scripts) not shown directly, while `<body>` holds the visible content rendered to users.

**Q14: How would you validate an HTML form client-side?**  
A: Use HTML5 attributes like `required`, `type="email"`, and `pattern`, plus the `novalidate` removal, or JS `checkValidity()`:
```html
<input type="email" required>
```

---

## 2. CSS & Frontend Basics (Q15–Q24)

**Q15: What is the purpose of CSS and how do you include it?**  
A: CSS (Cascading Style Sheets) controls presentation. Include it via `<link rel="stylesheet" href="style.css">`, an inline `style` attribute, or a `<style>` block.

**Q16: Explain the box model.**  
A: Every element has content, padding, border, and margin. Width calculations include padding and border unless `box-sizing: border-box` is set.

**Q17: What is the difference between classes and IDs in CSS?**  
A: Classes (`.name`) can be reused across many elements; IDs (`#name`) must be unique per page and have higher specificity.

**Q18: How do you center a `div` horizontally and vertically?**  
A: With flexbox:
```css
.parent { display: flex; justify-content: center; align-items: center; }
```

**Q19: What are CSS flexbox and grid used for?**  
A: Flexbox arranges items in one dimension (row/column); Grid handles two-dimensional layouts. Both simplify responsive design.

**Q20: What are media queries and why are they used?**  
A: Media queries apply styles based on device characteristics like width, enabling responsive designs:
```css
@media (max-width: 600px) { body { font-size: 14px; } }
```

**Q21: What is the difference between `position: relative`, `absolute`, and `fixed`?**  
A: `relative` offsets from its normal place; `absolute` positions relative to the nearest positioned ancestor; `fixed` positions relative to the viewport.

**Q22: How do you make a website responsive as a backend intern touching the frontend?**  
A: Use viewport meta, flexible units (%, `rem`), media queries, and CSS frameworks, ensuring layouts adapt without breaking backend-rendered content.

**Q23: What is the difference between `margin` and `padding`?**  
A: Margin is the outer space around an element; padding is the inner space between content and the border.

**Q24: How can you optimize CSS for faster page loads?**  
A: Minify CSS, remove unused rules, use `link` preload, avoid render-blocking by placing styles in `<head>`, and use efficient selectors.

---

## 3. JavaScript & ES6+ (Q25–Q38)

**Q25: What is the difference between `var`, `let`, and `const`?**  
A: `var` is function-scoped and hoisted; `let` and `const` are block-scoped, with `const` preventing reassignment. Prefer `const`/`let` in modern code.

**Q26: Explain arrow functions in ES6.**  
A: Arrow functions provide concise syntax and do not rebind `this`:
```javascript
const add = (a, b) => a + b;
```

**Q27: What is the difference between `==` and `===`?**  
A: `==` performs type coercion; `===` checks both value and type strictly. Always use `===` to avoid bugs.

**Q28: What are template literals?**  
A: Backtick strings allowing embedded expressions and multiline text:
```javascript
const msg = `Hello ${name}, you have ${count} messages`;
```

**Q29: Explain `map`, `filter`, and `reduce`.**  
A: `map` transforms each item, `filter` selects items by condition, `reduce` accumulates into a single value:
```javascript
[1,2,3].map(n=>n*2); // [2,4,6]
[1,2,3].filter(n=>n>1); // [2,3]
[1,2,3].reduce((s,n)=>s+n,0); // 6
```

**Q30: What is the difference between `let` scope and closure?**  
A: A closure is a function retaining access to its lexical scope even after the outer function returns, enabling data privacy and callbacks.

**Q31: How does `fetch` work for API calls?**  
A: `fetch` returns a promise; parse with `.json()`:
```javascript
const res = await fetch('/api/users');
const data = await res.json();
```

**Q32: What are promises and async/await?**  
A: Promises represent future values; `async/await` is syntactic sugar for cleaner asynchronous code that reads like synchronous logic.

**Q33: What is event delegation?**  
A: Attaching a listener to a parent element to handle events from children via bubbling, improving performance for dynamic lists.

**Q34: How do you prevent default form submission in JS?**  
A: Call `event.preventDefault()` inside the submit handler to stop the browser's native reload.

**Q35: What are the differences between `localStorage` and `sessionStorage`?**  
A: Both store key-value strings client-side; `localStorage` persists until cleared, `sessionStorage` clears when the tab closes.

**Q36: What is JSON and how is it used in backend communication?**  
A: JSON (JavaScript Object Notation) is a lightweight data format; backends serialize data to JSON for APIs that frontend code parses with `JSON.parse`.

**Q37: How do you debug JavaScript in the browser?**  
A: Use `console.log`, the DevTools Sources debugger with breakpoints, and `debugger;` statements to step through code.

**Q38: What is the difference between `null` and `undefined`?**  
A: `undefined` means a variable is declared but not assigned; `null` is an explicit assignment representing "no value".

---

## 4. Python & Backend Basics (Q39–Q52)

**Q39: Why is Python a good choice for backend development?**  
A: Python has clean syntax, a vast ecosystem (FastAPI, Django, Flask), strong libraries for data/AI, and rapid development speed—ideal for a non-profit's quick iterations.

**Q40: What are Python virtual environments and why use them?**  
A: `venv` isolates dependencies per project, avoiding version conflicts:
```bash
python -m venv .venv && source .venv/bin/activate
```

**Q41: Explain the difference between lists, tuples, and sets.**  
A: Lists are mutable ordered sequences; tuples are immutable ordered; sets are unordered collections of unique items, good for deduplication.

**Q42: What are Python dictionaries and how are they used in APIs?**  
A: Dictionaries store key-value pairs, the natural structure for JSON-like request/response payloads in backends.

**Q43: How do you handle errors in Python?**  
A: Use `try/except` blocks to catch and handle exceptions gracefully:
```python
try:
    x = 1 / 0
except ZeroDivisionError as e:
    print("Error:", e)
```

**Q44: What is the difference between a function and a class in Python?**  
A: A function performs a task; a class bundles data (attributes) and behavior (methods) into reusable objects.

**Q45: Explain list comprehensions.**  
A: A concise way to build lists:
```python
squares = [n*n for n in range(5)]  # [0,1,4,9,16]
```

**Q46: What are *args and **kwargs?**  
A: `*args` collects positional arguments into a tuple; `**kwargs` collects keyword arguments into a dict, enabling flexible function signatures.

**Q47: How do you read and write files in Python?**  
A: Use context managers to ensure closure:
```python
with open("data.txt") as f:
    content = f.read()
```

**Q48: What is PEP 8 and why does it matter?**  
A: PEP 8 is Python's style guide (naming, indentation, line length) that keeps code consistent and readable across a team.

**Q49: How do you make an HTTP request from Python?**  
A: Use the `requests` library:
```python
import requests
r = requests.get("https://api.example.com/users")
print(r.json())
```

**Q50: Explain the difference between synchronous and asynchronous Python.**  
A: Synchronous code runs sequentially; async (with `asyncio`/`await`) lets a single thread handle many I/O tasks concurrently, boosting API throughput.

**Q51: What are Python decorators?**  
A: Functions that wrap other functions to add behavior (e.g., auth checks, logging) without modifying the original code.

**Q52: How would you structure a small Python backend project?**  
A: Separate `routers/`, `models/`, `schemas/`, `services/`, and `config/` modules, with a `main.py` entrypoint and a `requirements.txt` for dependencies.

---

## 5. FastAPI & Flask (Q53–Q64)

**Q53: What is FastAPI and why is it popular?**  
A: FastAPI is a modern Python web framework offering automatic OpenAPI docs, data validation via Pydantic, and high performance using async—great for building APIs quickly.

**Q54: How do you define a simple FastAPI route?**  
A:
```python
from fastapi import FastAPI
app = FastAPI()
@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id}
```

**Q55: What is Pydantic and how is it used in FastAPI?**  
A: Pydantic provides runtime data validation and typing via models, automatically parsing and validating request bodies and producing clear errors.

**Q56: How does FastAPI auto-generate documentation?**  
A: It serves interactive Swagger UI at `/docs` and ReDoc at `/redoc` built from your route definitions and type hints.

**Q57: What is the difference between FastAPI and Flask?**  
A: Flask is minimal and synchronous; FastAPI is async-native, with built-in validation, dependency injection, and auto-docs. I used both in my Agentic AI and AI Agent internships.

**Q58: How do you handle path and query parameters in FastAPI?**  
A: Path params go in the route (e.g., `{id}`) and are typed; query params are function arguments with defaults:
```python
@app.get("/users/{user_id}")
def get_user(user_id: int, active: bool = True): ...
```

**Q59: How do you return custom status codes and responses?**  
A: Use `status_code` on the decorator or return `JSONResponse(status_code=201, content={"ok": True})`.

**Q60: What are FastAPI dependencies and when would you use them?**  
A: Dependencies are reusable callables injected into routes—ideal for auth checks, DB sessions, and shared validation, reducing duplication.

**Q61: How do you connect a database in FastAPI?**  
A: Use an engine/session (e.g., SQLAlchemy) initialized at startup and provided via dependency injection to each route.

**Q62: How would you add CORS to a FastAPI app for the frontend team?**  
A:
```python
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"])
```

**Q63: How do you run a FastAPI app locally and in production?**  
A: Locally with `uvicorn main:app --reload`; in production with `uvicorn main:app --workers 4` behind a server like Gunicorn or on Render/Vercel.

**Q64: In your Sim Studio OSS contribution, what backend issue did you fix?**  
A: I added SSRF protection by validating and blocking internal/localhost URLs before the server fetched them, plus handled localhost HTTP requests safely and wrote tests to prevent regressions.

---

## 6. RESTful API Design & Authentication (Q65–Q76)

**Q65: What is REST and what are its core principles?**  
A: REST is an architectural style using stateless, resource-oriented HTTP endpoints with standard methods (GET, POST, PUT, DELETE) and predictable URLs.

**Q66: What is the difference between PUT and PATCH?**  
A: PUT replaces the entire resource; PATCH partially updates only the provided fields.

**Q67: What HTTP status codes should a backend return?**  
A: 200 OK, 201 Created, 204 No Content, 400 Bad Request, 401 Unauthorized, 403 Forbidden, 404 Not Found, 500 Internal Error.

**Q68: What is the difference between authentication and authorization?**  
A: Authentication verifies who you are (login); authorization determines what you are allowed to do (permissions/roles).

**Q69: How does JWT authentication work?**  
A: The server issues a signed token after login; the client sends it in the `Authorization` header; the server verifies the signature on each request without storing sessions.

**Q70: What is OAuth and when is it used?**  
A: OAuth is a delegation protocol letting apps access resources on behalf of a user via tokens (e.g., "Login with Google"), commonly used for third-party auth.

**Q71: How would you secure a RESTful API?**  
A: Use HTTPS, validate inputs, authenticate with JWT/OAuth, rate-limit, sanitize against injection, and follow least-privilege access.

**Q72: What is idempotency in API design?**  
A: An idempotent operation yields the same result no matter how many times it is repeated (GET, PUT, DELETE are idempotent; POST is not).

**Q73: How do you version an API?**  
A: Common approaches: URL prefix (`/v1/users`), query param (`?v=1`), or header. URL versioning is simplest and clearest.

**Q74: What is request validation and why does it matter?**  
A: Validating incoming data types/shapes (e.g., Pydantic) prevents crashes, injection, and bad data from reaching the database.

**Q75: How do you handle file uploads in a backend API?**  
A: Accept `UploadFile` (FastAPI) or `multipart/form-data`, validate type/size, then store locally or on Cloudinary/S3 before returning a URL.

**Q76: How do you document and test your APIs?**  
A: Use FastAPI's auto `/docs`, write pytest integration tests, and optionally OpenAPI specs so the frontend team can rely on clear contracts.

---

## 7. Databases: SQL & NoSQL (Q77–Q88)

**Q77: What is the difference between SQL and NoSQL databases?**  
A: SQL databases (PostgreSQL, MySQL) are relational with schemas and ACID compliance; NoSQL (MongoDB) are flexible, document-oriented, and scale horizontally.

**Q78: Write a basic SQL query to fetch users ordered by name.**  
A:
```sql
SELECT id, name, email FROM users ORDER BY name ASC;
```

**Q79: What is a primary key and a foreign key?**  
A: A primary key uniquely identifies a row; a foreign key links a row in one table to a row in another, enforcing relationships.

**Q80: What is a JOIN and name the common types?**  
A: JOINs combine rows from tables. Common types: INNER, LEFT, RIGHT, and FULL OUTER JOIN.

**Q81: What are indexes and why are they important?**  
A: Indexes speed up queries by creating a lookup structure, at the cost of extra write overhead and storage—use them on frequently filtered columns.

**Q82: How do you prevent SQL injection?**  
A: Use parameterized queries / ORM (SQLAlchemy) instead of string formatting:
```python
cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
```

**Q83: What is normalization?**  
A: Organizing tables to reduce redundancy and dependency issues (1NF, 2NF, 3NF), improving data integrity.

**Q84: When would you choose MongoDB over PostgreSQL?**  
A: For flexible or evolving schemas, rapid prototyping, or hierarchical JSON-like data—such as logging or content with variable fields.

**Q85: What is Redis and where have you used it?**  
A: Redis is an in-memory key-value store for caching and queues. I used it in my Agentic AI internship to cache API responses and speed up microservices.

**Q86: How do you model relationships in a non-profit donation system?**  
A: `donors` 1-to-many `donations`, `campaigns` 1-to-many `donations`, with foreign keys linking records for reporting.

**Q87: What is a migration and why is it needed?**  
A: A migration is a versioned script that changes schema safely over time (e.g., Alembic), keeping dev and prod databases in sync.

**Q88: How do you back up and restore a database?**  
A: Use `pg_dump` for PostgreSQL or `mongodump` for MongoDB, store backups securely, and test restores periodically.

---

## 8. Git, GitHub & Version Control (Q89–Q94)

**Q89: What is Git and why is it essential for teams?**  
A: Git is a distributed version control system tracking changes, enabling collaboration, branching, and safe rollbacks across the intern team.

**Q90: What is the difference between `git clone`, `git pull`, and `git fetch`?**  
A: `clone` copies a repo first time; `fetch` downloads changes without merging; `pull` fetches and merges into the current branch.

**Q91: Explain branching and a typical workflow.**  
A: Create a feature branch, commit changes, open a PR, review, then merge to `main`:
```bash
git checkout -b feature/login
git add . && git commit -m "Add login"
git push -u origin feature/login
```

**Q92: How do you resolve a merge conflict?**  
A: Open the conflicted file, choose the correct changes between `<<<<<<<` markers, `git add` the file, then commit to finish the merge.

**Q93: What is a `.gitignore` and why use it?**  
A: It lists files Git should ignore (e.g., `.env`, `__pycache__`, `node_modules`) to avoid committing secrets and build artifacts.

**Q94: How do you write a good commit message?**  
A: Use a short imperative subject ("Add JWT auth"), optionally a blank line then a body explaining the why, keeping it clear for reviewers.

---

## 9. DevOps: Docker, CI/CD & Deployment (Q95–Q100)

**Q95: What problem does Docker solve?**  
A: Docker packages apps with dependencies into containers that run identically across machines, eliminating "works on my machine" issues.

**Q96: Write a minimal Dockerfile for a FastAPI app.**  
A:
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Q97: What is CI/CD and how have you used GitHub Actions?**  
A: CI/CD automates testing and deployment. I used GitHub Actions to run tests and build Docker images on every push, catching errors before merge.

**Q98: How would you deploy a backend for this internship?**  
A: Containerize with Docker and deploy to Render or Vercel, connect the database, set environment variables, and add a CI pipeline to auto-deploy on `main`.

**Q99: What is the difference between environment variables and hardcoded config?**  
A: Environment variables (via `.env`) keep secrets and config out of code, making apps portable and secure across dev, staging, and prod.

**Q100: Why are you interested in the Pledge India Foundation backend internship?**  
A: I want to apply my Python/FastAPI and web skills to a mission-driven non-profit, contribute reliable backend systems for education/health initiatives, and grow through real-world, collaborative work.
