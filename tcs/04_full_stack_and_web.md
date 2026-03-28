# Full-Stack and Web Development

**Q1. What is FastAPI and why prefer it over Flask or Django?**
**Answer:** FastAPI is a modern, high-performance web framework for building APIs in Python. 
I prefer FastAPI because:
1. **Speed:** It is incredibly fast, comparable to NodeJS and Go, built on Starlette and Pydantic.
2. **Asynchronous:** It supports native async/await, making it perfect for handling concurrent I/O API calls (like sending requests to AI models).
3. **Auto-docs:** It automatically generates interactive Swagger UI documentation.
Flask is great for microservices but lacks native async and typing, while Django is a heavy, batteries-included framework less suited for pure, lightweight AI microservices.

**Q2. Explain the component lifecycle in React and how functional components handle it.**
**Answer:** In older class-based React, the lifecycle consisted of mounting, updating, and unmounting phases (e.g., `componentDidMount`, `componentDidUpdate`, `componentWillUnmount`).
In modern functional React, we use the `useEffect` hook to handle side effects that map to these lifecycles. 
- Empty dependency array `[]` acts like `componentDidMount`.
- Specific dependencies `[data]` acts like `componentDidUpdate`.
- A return function inside `useEffect` acts as a cleanup or `componentWillUnmount`.

**Q3. Why choose Next.js over traditional React (Create React App)?**
**Answer:** Traditional React creates Single Page Applications (SPAs) where rendering happens entirely on the client-side, which can result in slow initial loads and poor SEO.
Next.js provides Server-Side Rendering (SSR) and Static Site Generation (SSG). This means the HTML is pre-rendered on the server, resulting in blazing fast page loads, excellent SEO, and built-in features like API routes and optimized routing.

**Q4. How do you secure endpoints inside your backend APIs?**
**Answer:** To secure endpoints, particularly in FastAPI and Express, I implement JWT (JSON Web Tokens) based authentication. 
1. The user logs in and the server validates credentials.
2. The server signs a JWT and returns it to the client.
3. The client includes the JWT in the `Authorization: Bearer <token>` header of subsequent requests.
4. I use middleware/dependencies to intercept the request, verify the JWT signature and expiration, and either allow access or return a 401 Unauthorized status. I also implement CORS configurations to prevent unauthorized cross-origin access.

**Q5. Explain middleware in the context of ExpressJS or FastAPI.**
**Answer:** Middleware is code that executes before a request reaches the route handler, or before the response is sent to the client. It intercepts incoming HTTP requests. 
Common uses include:
- Verifying authentication/authorization tokens.
- Logging request durations and IP addresses.
- Handling CORS.
- Parsing request bodies (e.g., JSON parsing).
