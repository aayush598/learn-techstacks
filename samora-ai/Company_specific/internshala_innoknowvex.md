# Innoknowvex — 100 Full Stack Interview Q&A

> Based on Innoknowvex — Full Stack Development Internship (edtech; AngularJS/PHP/MongoDB/MySQL/Bubble.io, entry-level)  > Candidate: Aayush Gid (React/Next.js/Node/Python FastAPI/MongoDB/MySQL/AI guardrails background)

---

## 1. Web & Frontend Fundamentals (Q1–Q14)

**Q1: What is the difference between the front end and back end of a web application?**  
A: The front end is the client-side code (HTML/CSS/JS) users see and interact with in the browser. The back end is server-side code and databases that process logic, store data, and serve APIs. As a React/Next.js developer, you already work across both with API routes.

**Q2: What are the core technologies of the web?**  
A: HTML structures content, CSS styles it, and JavaScript adds interactivity. Together they form the foundation of every web page before frameworks like React or AngularJS are layered on.

**Q3: Explain the client-server model.**  
A: A client (browser or app) sends a request to a server, which processes it and returns a response (often HTML or JSON). This request-response cycle is the basis of web communication.

**Q4: What is a URL and what are its parts?**  
A: A URL identifies a resource. It has a scheme (`https`), host (`example.com`), port (optional), path (`/api/users`), query (`?id=1`), and fragment (`#section`).

**Q5: What is the difference between a static and a dynamic website?**  
A: A static site serves the same pre-built HTML to every user. A dynamic site generates content on the fly from a server/database based on user input or data.

**Q6: What is HTTP and why is it important?**  
A: HTTP (HyperText Transfer Protocol) is the protocol browsers and servers use to exchange data. It defines methods like GET/POST and status codes like 200/404.

**Q7: What are HTTP methods and when do you use them?**  
A: GET retrieves data, POST creates, PUT/PATCH update, DELETE removes. You already use these daily in FastAPI and React `fetch` calls.

**Q8: What are status codes? Give examples.**  
A: They indicate request outcome: 2xx success (200), 3xx redirect, 4xx client error (404, 401), 5xx server error (500).

**Q9: What is the difference between HTTP and HTTPS?**  
A: HTTPS adds TLS encryption on top of HTTP, securing data in transit. It is essential for login forms and any authenticated traffic.

**Q10: What is a web browser's role in rendering a page?**  
A: The browser fetches HTML, parses it into the DOM, applies CSS, executes JS, and paints pixels. DevTools lets you inspect each step.

**Q11: What is the DOM?**  
A: The Document Object Model is a tree representation of the page's HTML that JS can read and manipulate to update the UI dynamically.

**Q12: What is the difference between a library and a framework?**  
A: A library (e.g., React) is a tool you call when you want. A framework (e.g., AngularJS, Next.js) calls your code and dictates structure. Your React/Next.js experience maps directly to learning AngularJS quickly.

**Q13: What is responsive web design?**  
A: It makes layouts adapt to screen sizes using fluid grids, flexible images, and media queries so sites work on phones and desktops.

**Q14: What does "supporting UI development" mean in a day-to-day internship?**  
A: It means building reusable components, fixing layout bugs, wiring forms to APIs, and following the team's design system under senior guidance—exactly the React component work you've done in SaaS Video Editor and Workflow-Canvas.

## 2. HTML & CSS (Q15–Q28)

**Q15: What is semantic HTML and why does it matter?**  
A: Semantic tags like `<header>`, `<nav>`, `<article>` describe meaning, improving accessibility and SEO. Screen readers and search engines parse them better than generic `<div>`s.

**Q16: What are the differences between `<div>`, `<span>`, and `<section>`?**  
A: `<div>` is a block-level generic container; `<span>` is inline; `<section>` is a semantic block grouping related content.

**Q17: How do you create a hyperlink and an image in HTML?**  
A:
```html
<a href="https://innoknowvex.com">Visit</a>
<img src="logo.png" alt="Innoknowvex logo" />
```

**Q18: What are forms and key input types?**  
A: Forms collect user input via `<input type="text|email|password|number|submit">`. You've built many forms with React state and validation.

**Q19: What is the `alt` attribute and why use it?**  
A: `alt` provides alternative text for images, critical for accessibility and when images fail to load.

**Q20: What are the three ways to apply CSS?**  
A: Inline (`style=""`), internal (`<style>` in head), and external (`<link rel="stylesheet">`). External is preferred for maintainability.

**Q21: Explain the CSS box model.**  
A: Every element has content, padding, border, and margin. Understanding it prevents layout surprises when sizing elements.

**Q22: What is the difference between `class` and `id` selectors?**  
A: A `class` can apply to many elements; an `id` is unique per page. Use classes for reusable styles.

**Q23: What are CSS Flexbox and Grid?**  
A: Flexbox lays out items in one dimension (row/column); Grid handles two-dimensional layouts. Your Tailwind/Framer Motion work already uses these concepts.

**Q24: How do you center a `div` horizontally and vertically?**  
A:
```css
.parent { display: flex; align-items: center; justify-content: center; }
```

**Q25: What is the difference between `margin` and `padding`?**  
A: `margin` is space outside the border (between elements); `padding` is space inside the border (between content and border).

**Q26: What are media queries?**  
A: They apply CSS based on device characteristics, e.g. `@media (max-width: 600px) { ... }`, enabling responsive designs.

**Q27: What is the difference between `position: relative`, `absolute`, and `fixed`?**  
A: `relative` offsets from its normal spot; `absolute` positions against the nearest positioned ancestor; `fixed` stays relative to the viewport.

**Q28: How do you make a webpage accessible (a11y)?**  
A: Use semantic HTML, `alt` text, proper labels on inputs, sufficient color contrast, and keyboard navigability. Accessibility matters for an edtech platform serving diverse students.

## 3. JavaScript Essentials (Q29–Q46)

**Q29: What are the main data types in JavaScript?**  
A: `string`, `number`, `boolean`, `null`, `undefined`, `symbol`, `bigint`, and `object` (including arrays and functions). Your ES6+ experience covers these well.

**Q30: What is the difference between `var`, `let`, and `const`?**  
A: `var` is function-scoped and hoisted; `let` and `const` are block-scoped. `const` cannot be reassigned (use it by default), `let` for mutable values.

**Q31: What are arrow functions?**  
A:
```js
const add = (a, b) => a + b;
```
They have concise syntax and lexically bind `this`, which you use constantly in React handlers.

**Q32: What is the difference between `==` and `===`?**  
A: `==` performs type coercion; `===` checks value and type strictly. Always prefer `===` to avoid bugs.

**Q33: Explain `map`, `filter`, and `reduce`.**  
A:
```js
[1,2,3].map(x => x*2);       // [2,4,6]
[1,2,3].filter(x => x>1);    // [2,3]
[1,2,3].reduce((s,x)=>s+x,0);// 6
```
These are core to rendering lists in React.

**Q34: What is a callback and what is callback hell?**  
A: A callback is a function passed to another function. Nesting many leads to "callback hell"; Promises and `async/await` solve it.

**Q35: What are Promises and `async/await`?**  
A:
```js
const res = await fetch('/api/users');
const data = await res.json();
```
Promises represent future values; `async/await` makes asynchronous code read like synchronous code.

**Q36: What is the difference between `null` and `undefined`?**  
A: `undefined` means a variable is declared but not assigned; `null` is an explicit "no value" assigned by the programmer.

**Q37: What is event delegation?**  
A: Attaching one listener to a parent instead of many children, using event bubbling. It improves performance for dynamic lists.

**Q38: What is the event loop?**  
A: JS is single-threaded; the event loop processes the callback queue after the call stack empties, enabling non-blocking async operations.

**Q39: How do you manipulate the DOM with JS?**  
A:
```js
document.getElementById('btn').addEventListener('click', () => {...});
```

**Q40: What are template literals?**  
A: Backtick strings allowing embedded expressions: `` `Hello ${name}` ``. You use them for API URLs and JSX text.

**Q41: What is destructuring?**  
A:
```js
const { name, age } = user;
const [first, ...rest] = arr;
```
It simplifies extracting values from objects/arrays.

**Q42: What is the difference between `localStorage` and `sessionStorage`?**  
A: `localStorage` persists until cleared; `sessionStorage` clears when the tab closes. Both store key-value strings client-side.

**Q43: What are ES6 modules (`import`/`export`)?**  
A: They let you split code into reusable files: `export const x` and `import { x } from './file'`. You use these in every React/Next.js project.

**Q44: How do you prevent common JS errors like `undefined is not a function`?**  
A: Guard with checks, use optional chaining `user?.profile?.name`, and write defensive code. Your TypeScript background helps catch these at compile time.

**Q45: What is JSON and how is it used?**  
A: JSON is a text format for structured data: `{"name":"Aayush"}`. APIs send/receive JSON; `JSON.parse`/`JSON.stringify` convert it.

**Q46: How would you debug JavaScript in the browser?**  
A: Use `console.log`, breakpoints in DevTools Sources panel, and the Network tab to inspect API calls—core to the "debug, test, troubleshoot" part of the role.

## 4. AngularJS & Bubble.io (Learnable from React) (Q47–Q58)

**Q47: I notice the role mentions AngularJS, but your resume shows React. How will you adapt?**  
A: React and AngularJS share component-based thinking, one-way/two-way data flow, and templating. I'll ramp up fast by mapping React concepts (components, props, state) to AngularJS (directives, bindings, scopes). My Next.js experience makes the learning curve short.

**Q48: What is a component in AngularJS vs React?**  
A: React components are JS functions returning JSX; AngularJS uses directives/controllers with HTML templates. Both encapsulate UI and logic—so the mental model transfers.

**Q49: What is two-way data binding in AngularJS?**  
A: `ng-model` syncs the view and model automatically. React uses one-way binding plus `useState`, but the concept of keeping UI and data in sync is the same.

**Q50: What are AngularJS directives?**  
A: Markers like `ng-repeat`, `ng-if` extend HTML behavior. React achieves similar results with JSX conditionals and `.map()`.

**Q51: What is `$scope` in AngularJS?**  
A: It's the glue object between controller and view holding data/methods. React's equivalent is component state/props.

**Q52: How would you structure an AngularJS app?**  
A: Modules → controllers/components → services → templates, similar to React's folder-by-feature structure. I'd follow the team's existing patterns.

**Q53: What is Bubble.io and where does it fit?**  
A: Bubble.io is a no-code platform for building web apps visually with workflows and a built-in database. It's useful for rapid edtech prototypes without writing much code.

**Q54: How does your React experience help with Bubble.io?**  
A: Bubble's visual components and workflows mirror React's component + state + event-handler model. I can quickly translate logic I'd write in React into Bubble workflows.

**Q55: When would you choose Bubble.io over hand-coding?**  
A: For quick internal tools or MVPs where speed beats customization. For complex, performant features, code (React/Node) is better—I'd recommend based on the use case.

**Q56: What is dependency injection in AngularJS?**  
A: Services are passed into controllers/components rather than instantiated manually, improving testability. FastAPI's DI and React context follow the same principle.

**Q57: How do you make an API call in AngularJS?**  
A: Using `$http` or the newer `HttpClient`:
```js
$http.get('/api/courses').then(res => $scope.courses = res.data);
```
This maps directly to your `fetch`/axios calls in React.

**Q58: What's your plan to get productive in AngularJS/Bubble.io within the internship?**  
A: I'll pair with seniors, study the existing codebase, build a small feature end-to-end in week one, and leverage my React/Next.js fundamentals. Within two months I'll be contributing confidently.

## 5. Backend, PHP & Server-Side Logic (Q59–Q70)

**Q59: The role lists PHP. You've used Python/Node—how do you approach learning PHP?**  
A: PHP shares server-side concepts I already know: request handling, DB queries, sessions, and templating. I'll learn its syntax and Laravel-style patterns quickly, just as I picked up FastAPI and Express.

**Q60: What is server-side rendering (SSR) and have you done it?**  
A: SSR renders HTML on the server before sending to the browser. Yes—Next.js does SSR/SSG, and PHP renders templates server-side, so the concept is familiar.

**Q61: Write a simple PHP script that connects to MySQL.**  
A:
```php
$conn = new mysqli("localhost", "user", "pass", "db");
if ($conn->connect_error) die("Error");
$res = $conn->query("SELECT * FROM courses");
```

**Q62: What is a session and how is it used?**  
A: A session stores per-user data on the server across requests (e.g., login state). PHP uses `$_SESSION`; in Node I use JWT or express-session.

**Q63: What is the difference between GET and POST form handling in PHP?**  
A: `$_GET` reads URL params (visible, limited); `$_POST` reads body data (hidden, larger)—used for login and form submits.

**Q64: How do you prevent SQL injection in PHP?**  
A: Use prepared statements:
```php
$stmt = $conn->prepare("SELECT * FROM users WHERE id = ?");
$stmt->bind_param("i", $id);
$stmt->execute();
```

**Q65: Explain RESTful API design principles.**  
A: Use nouns for resources (`/courses`), HTTP methods for actions, stateless requests, and JSON responses with proper status codes. You've built many REST APIs in FastAPI and Express.

**Q66: What is middleware?**  
A: Functions that run before/after a request (auth, logging, CORS). Express and FastAPI both use middleware—same idea in PHP frameworks like Laravel.

**Q67: How do you handle authentication on the backend?**  
A: Issue a JWT on login, verify it on protected routes via middleware. You've implemented JWT/OAuth in FastAPI and Clerk in Next.js.

**Q68: What is CORS and why does it matter?**  
A: CORS controls which domains can call your API from the browser. Misconfigured CORS blocks legit front-end requests; you set it in Express/FastAPI headers.

**Q69: How would you structure a small backend service?**  
A: Routes → controllers → services → database layer, with env-based config and error handling. This mirrors your FastAPI microservices at the Agentic AI internship.

**Q70: What is caching and how have you used Redis?**  
A: Caching stores frequent results to reduce DB load. At the Agentic AI role you used Redis to cache API responses and rate-limit—directly useful for edtech traffic spikes.

## 6. Databases: MongoDB & MySQL (Q71–Q84)

**Q71: What is the difference between SQL and NoSQL databases?**  
A: SQL (MySQL) uses structured tables with schemas and joins; NoSQL (MongoDB) stores flexible JSON-like documents. You're strong in both—a direct match for this role.

**Q72: When would you choose MongoDB over MySQL?**  
A: MongoDB for flexible, evolving schemas (user-generated content, logs); MySQL for relational data needing transactions and integrity (enrollments, payments).

**Q73: Write a basic MongoDB insert and find.**  
A:
```js
db.courses.insertOne({ title: "React 101", level: "beginner" });
db.courses.find({ level: "beginner" });
```

**Q74: Write a MySQL query to create a table and insert.**  
A:
```sql
CREATE TABLE students (id INT PRIMARY KEY AUTO_INCREMENT, name VARCHAR(100));
INSERT INTO students (name) VALUES ('Aayush');
```

**Q75: What is a primary key and a foreign key?**  
A: A primary key uniquely identifies a row; a foreign key links to another table's primary key, enforcing relationships (e.g., enrollments → students).

**Q76: Explain `JOIN` in MySQL with an example.**  
A:
```sql
SELECT s.name, c.title
FROM enrollments e
JOIN students s ON e.student_id = s.id
JOIN courses c ON e.course_id = c.id;
```

**Q77: What are MongoDB aggregation pipelines?**  
A: A sequence of stages (`$match`, `$group`, `$sort`) to transform data:
```js
db.orders.aggregate([{ $group: { _id: "$status", total: { $sum: "$amount" } } }]);
```

**Q78: What is an index and why use it?**  
A: Indexes speed up queries by avoiding full scans. You'd index fields like `email` in MySQL or `userId` in MongoDB.

**Q79: How do you model one-to-many relationships in MongoDB?**  
A: Embed sub-documents for small fixed sets, or reference IDs for large growing sets—similar to foreign keys but flexible.

**Q80: What is normalization?**  
A: Organizing tables to reduce redundancy (1NF–3NF). It prevents update anomalies in MySQL; MongoDB favors embedding for read performance instead.

**Q81: How do you update a document in MongoDB?**  
A:
```js
db.courses.updateOne({ _id: id }, { $set: { price: 99 } });
```

**Q82: What are transactions and when are they needed?**  
A: Transactions guarantee all-or-nothing multi-step writes. MySQL supports them natively; MongoDB supports them via `startSession()` for critical operations like payments.

**Q83: How have you used MongoDB and MySQL in past projects?**  
A: You used MongoDB for flexible data in guardrail/AI projects and MySQL/PostgreSQL in FastAPI services—directly matching Innoknowvex's stack.

**Q84: How do you back up and secure a database?**  
A: Regular dumps (`mysqldump`), least-privilege users, parameterized queries to prevent injection, and encrypted connections. You've handled DB auth in production FastAPI apps.

## 7. REST APIs & Third-Party Integrations (Q85–Q92)

**Q85: How do you consume a third-party REST API from the front end?**  
A:
```js
const res = await fetch('https://api.example.com/courses');
const data = await res.json();
```
You've integrated Cloudinary, Clerk, and external APIs in Next.js.

**Q86: What is an API key and how should you handle it securely?**  
A: An API key authenticates requests. Keep secrets in env variables/server-side, never expose them in client code. You use `.env` and Vercel/Render secret config.

**Q87: What is webhook and when is it used?**  
A: A webhook is an outbound HTTP call a service makes to notify your app of events (e.g., payment success). You verify signatures to avoid fake calls—like Clerk webhooks you've built.

**Q88: How do you handle API errors gracefully?**  
A: Check status codes, show user-friendly messages, retry with backoff, and log failures. Your Sim Studio work included robust error handling and tests.

**Q89: What is rate limiting and have you implemented it?**  
A: Rate limiting caps requests per client to prevent abuse. You used Redis for rate limiting at the Agentic AI internship.

**Q90: Explain OAuth briefly.**  
A: OAuth lets users login via a provider (Google) without sharing passwords, using access tokens. You've integrated OAuth via Clerk in GuardrailZ.

**Q91: How would you integrate a payment or email third-party service?**  
A: Wrap the provider SDK in a service module, store keys in env, handle webhooks for status, and add tests. Your FastAPI microservices experience fits this pattern.

**Q92: What is idempotency in APIs?**  
A: An operation produces the same result if retried (e.g., duplicate payment avoided). Use idempotency keys—important when integrating external services.

## 8. Git, Version Control & Collaboration (Q93–Q98)

**Q93: What is Git and why is it used?**  
A: Git tracks code changes, enabling collaboration and history. You use Git/GitHub daily across all projects.

**Q94: Explain the basic Git workflow.**  
A:
```bash
git clone <repo>
git checkout -b feature/login
git add . && git commit -m "Add login"
git push origin feature/login
```

**Q95: What is a branch and why use feature branches?**  
A: Branches isolate work so main stays stable. You open PRs from feature branches for code review—part of the internship's review process.

**Q96: What is a pull request and code review?**  
A: A PR proposes merging changes; teammates review for bugs, style, and correctness before merging. You've done this in open-source Sim Studio contributions.

**Q97: How do you resolve a merge conflict?**  
A: Open the conflicted file, choose the correct changes (or combine), remove conflict markers, then `git add` and commit. You've resolved conflicts in team repos.

**Q98: What are CI/CD and have you used GitHub Actions?**  
A: CI/CD automates testing and deployment. You set up GitHub Actions pipelines for Docker builds and tests at the Agentic AI internship—directly valuable here.

## 9. Behavioral, Learning Agility & Why Innoknowvex (Q99–Q100)

**Q99: Why do you want this Full Stack internship at Innoknowvex, an edtech company?**  
A: I'm passionate about building products that help students—edtech impacts careers directly. My React/Next.js, MongoDB/MySQL, and API experience let me contribute immediately, while learning AngularJS/PHP/Bubble.io expands my stack. Your mission of connecting students with internships and mentorship aligns with my own SIH and teaching background.

**Q100: You don't know AngularJS, Bubble.io, or PHP yet. How do you prove learning agility?**  
A: I've repeatedly ramped fast—picking up FastAPI, Docker, and Redis on the job, contributing to Sim Studio OSS, and shipping GuardrailZ live. I learn by building, pair with seniors, and document as I go. Within two months I'll be a reliable contributor across the full stack.
