# DevOps, Databases, and Automation

**Q1. Describe your experience with Docker. Why containerize applications?**
**Answer:** During my Krip AI internship, I containerized our FastAPI backend services using Docker. 
Containerization packages an application along with all its dependencies, libraries, and configurations into a single image. This eliminates the "it works on my machine" problem, ensuring consistency across development, testing, and production environments. It also makes deployment and scaling much easier.

**Q2. How do you implement a CI/CD pipeline using GitHub Actions?**
**Answer:** I created workflows in GitHub Actions using `.yml` files in the `.github/workflows` directory. A typical pipeline triggers on a push or PR to the `main` branch. 
First, it checks out the code. Then it sets up the environment (e.g., installing Python/Node). Next, it runs formatting checks and executes the test suites (using `pytest`). If the tests pass, the CD side takes over to build the Docker image, pushes it to a container registry, and pulls the latest image on the production server.

**Q3. You have used both SQLite and PostgreSQL. When should you use which?**
**Answer:** 
- **SQLite:** A lightweight, serverless database that stores data in a single local file. I use it for prototyping, local development, edge devices, or small-scale applications (like in my ScriptVector project) where concurrent writes won't be an issue.
- **PostgreSQL:** A powerful, open-source, client-server relational database. It supports heavy concurrent connections, advanced indexing, and complex queries. It is the standard for production enterprise applications that require scalability and high reliability.

**Q4. What is the role of automation platforms like n8n, Zapier, and Make.com?**
**Answer:** These are Low-Code/No-Code platforms that allow systems to connect APIs via visual workflows. 
In my Clone Futura internship, I used these to interconnect different services without writing boilerplate glue code. For instance, creating a trigger when a new user registers in a database, filtering that data, and automatically generating an AI personalized welcome email and sending it via an SMTP node. It drastically speeds up business logic implementation.

**Q5. Explain the importance of Unit testing vs Integration testing.**
**Answer:** 
- **Unit Testing** focuses on testing individual, isolated components or functions. (e.g., testing if an addition function returns 4 given 2 and 2). I use `pytest` for this.
- **Integration Testing** tests how different modules or services work together. (e.g., testing if my FastAPI route correctly connects to the database, queries the data, and returns the correct JSON response). Both are vital for maintaining code reliability before deploying to production.
