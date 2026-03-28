# TCS Prime Specific Scenarios / System Design

**Q1. TCS Prime candidates are expected to handle complex architectures. How would you design a scalable system for an AI application handling thousands of concurrent users?**
**Answer:** To design a scalable AI application:
1. **Frontend:** Deployed on edge networks (like Vercel or AWS CloudFront) using Next.js for high availability.
2. **API Layer:** Use API Gateway to route traffic and handle rate limiting. Behind it, a load balanced cluster of FastAPI services.
3. **Compute:** As AI inference is heavy, requests should not be processed synchronously. The API should dump requests into a Message Queue (like RabbitMQ or Redis/Celery).
4. **Worker Nodes:** A fleet of autoscaling worker instances picks up messages from the queue, queries the LLMs/Models, and saves the output.
5. **Database:** Results stored in PostgreSQL, with heavily accessed data cached in Redis.
6. **Infrastructure:** Everything would be containerized via Docker and orchestrated via Kubernetes to auto-scale worker pods based on CPU/Queue length.

**Q2. How do you ensure code quality when collaborating in a large enterprise team (like at TCS)?**
**Answer:** 
1. **Version Control:** Strict Git flow schemas (e.g., feature branching, pull requests requiring approvals).
2. **CI/CD:** Automated pipelines enforcing linters (like Flake8/ESLint), formatters (like Black/Prettier), and testing (Pytest/Jest) before merges are allowed.
3. **Documentation:** Using self-documenting frameworks like FastAPI (Swagger), writing clear docstrings, and updating architectural flowcharts.
4. **Code Reviews:** Constructive peer reviews keeping edge-cases, security, and algorithmic efficiency in mind.

**Q3. If an API endpoint querying an external LLM (like OpenAI) is consistently returning timeouts, how would you troubleshoot and resolve it?**
**Answer:** 
1. **Monitoring:** First check logs and metrics (Prometheus/Grafana) to identify if the latency is on our server network, or from the external API provider.
2. **Timeouts & Retries:** Implement exponential backoff algorithms for retries, ensuring we don't overwhelm failing services.
3. **Decoupling:** If the endpoint is built synchronously, I would immediately transform it into an asynchronous task using Webhooks or Polling. Give the user a `202 Accepted` status and process the LLM request in a background Celery worker.
4. **Caching:** If the same queries are being repeated, cache previous LLM responses in Redis to drastically reduce API calls.

**Q4. Explain what you built for the Smart India Hackathon that won you the finalist spot.**
**Answer:** For SIH, we had to address secure data transmission. My team developed a robust software system featuring advanced cryptographic algorithms. We focused on highly secure end-to-end encryption mechanics, addressing potential vulnerabilities in key exchange and payload tampering. My contribution involved architecting the backend encryption pipelines and ensuring the mathematical implementation of the ciphers was efficient enough so as to not block system performance, allowing us to clear multiple rigorous evaluation rounds out of 500 competing teams.
