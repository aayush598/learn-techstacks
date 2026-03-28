# 100 Web Development, React, FastAPI, and Database Questions

## FastAPI & Python Web Servers
1. **Q:** What makes FastAPI so fast? **A:** It is built on Starlette (for asynchronous web parts) and Pydantic (for data validation).
2. **Q:** What is Pydantic? **A:** A data validation library enforcing type hints in Python.
3. **Q:** Why use async/await in FastAPI? **A:** To handle hundreds of I/O bound requests concurrently without blocking the server thread.
4. **Q:** What is Uvicorn? **A:** An ASGI (Asynchronous Server Gateway Interface) web server implementation used to run FastAPI.
5. **Q:** ASGI vs WSGI? **A:** WSGI is synchronous (gunicorn, uWSGI); ASGI is asynchronous (uvicorn).
6. **Q:** How do you handle path parameters in FastAPI? **A:** Passed directly into route function variables using `{item_id}` in the path decorator.
7. **Q:** Query Params in FastAPI? **A:** Function parameters not declared in the route path automatically act as query parameters.
8. **Q:** Explain Dependency Injection in FastAPI. **A:** Using `Depends()` to share logic like database sessions or auth checks cleanly across handlers.
9. **Q:** What is Swagger UI? **A:** Automatically generated interactive API documentation provided natively by FastAPI via OpenAPI spec.

## React & Next.js Core
10. **Q:** What is the Virtual DOM? **A:** A lightweight in-memory representation of the DOM; React updates it, diffs it, and patches only changed parts into the real DOM.
11. **Q:** What is JSX? **A:** Syntax extension that looks like HTML used within JavaScript React files.
12. **Q:** Props vs State? **A:** Props convey data passed down from parents (read-only); state manages data locally within the component.
13. **Q:** `useState` hook? **A:** Allows functional components to keep and update local state variables.
14. **Q:** `useEffect` hook? **A:** Handles side effects like fetching data, subscriptions, or manually changing DOM.
15. **Q:** What is Context API? **A:** A React structure predicting prop-drilling by sharing state globally across the app component tree.
16. **Q:** Server-Side Rendering (SSR)? **A:** Rendering React on the server to send full HTML to clients, beneficial for SEO and loading speed (used heavily in Next.js).
17. **Q:** Static Site Generation (SSG)? **A:** Pre-rendering pages entirely at build time, served statically via CDNs.
18. **Q:** Why Next.js caching? **A:** Speeds up response times by utilizing massive cache stores natively across endpoints.
19. **Q:** CSR vs SSR? **A:** CSR renders browser-side taking time and risking SEO; SSR sends ready UI fast but demands server computational power.

## Security & Auth
20. **Q:** What is JWT? **A:** JSON Web Token; a compact url-safe token securely transmitting data natively using JSON objects, widely used for stateless API auth.
21. **Q:** How do you store JWTs? **A:** Secure HttpOnly cookies (to prevent XSS) or local storage (if HttpOnly is not feasible, though slightly less secure).
22. **Q:** What is CORS? **A:** Cross-Origin Resource Sharing; browser security feature preventing websites from malicious cross-origin API calls.
23. **Q:** SQL Injection? **A:** Injecting malicious SQL into input fields to manipulate backend DBs; stopped using parameterized queries/ORMs.
24. **Q:** XSS (Cross-Site Scripting)? **A:** Injecting malicious JS into a site viewed by others; blocked by escaping inputs and React's default DOM escaping.
25. **Q:** CSRF? **A:** Forcing users to execute unwanted actions on a site they’re authenticated on; stopped using CSRF tokens.

## Databases (Relational & Non-Relational)
26. **Q:** SQL vs NoSQL? **A:** SQL is tabular with strict schemas (Postgres, MySQL); NoSQL uses documents, graphs, key-values loosely structured (MongoDB).
27. **Q:** What are ACID properties? **A:** Atomicity, Consistency, Isolation, Durability; guarantees database transactions are processed reliably.
28. **Q:** What is normalization? **A:** Organizing relational DB tables to reduce redundancy and improve data integrity (1NF, 2NF, 3NF).
29. **Q:** Explain database indexes. **A:** Data structures (often B-Trees) improving querying speeds exponentially at the cost of slower writes and memory.
30. **Q:** INNER JOIN vs LEFT JOIN? **A:** Inner returns rows matched in both tables; Left returns all rows in the left table and matched ones in the right.
31. **Q:** Primary Key vs Foreign Key? **A:** Primary uniquely identifies a row; Foreign links a row to the primary key in another table.
32. **Q:** PostgreSQL vs SQLite? **A:** Postgres is a monstrous network DB handling thousands of requests; SQLite is a local file-based DB suitable for light embedded loads.
33. **Q:** What is migration? **A:** Systematic version-controlling of database schemas.

## Web General
34. **Q:** Difference between PUT and PATCH? **A:** PUT replaces the whole resource; PATCH performs partial updates.
35. **Q:** HTTP error code 404 vs 500? **A:** 404 is Not Found (client requested something stupid); 500 is Internal Server Error (server crashed).
36. **Q:** What are WebSockets? **A:** Full-duplex persistent communication channels running over a single TCP connection.
37. **Q:** Concept of local storage, session storage, cookies. **A:** Local doesn't expire. Session dumps on tab close. Cookies are tiny and auto-sent to servers.
38. **Q:** What is Redux? **A:** A predictable state container used extensively over deep/broad applications to hold state globally.
...
