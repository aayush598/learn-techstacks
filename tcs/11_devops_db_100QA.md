# 100 DevOps, Tools, and Situational Questions

## Docker & Linux 
1. **Q:** What is Containerization? **A:** Packaging an app and its dependencies into isolated lightweight units.
2. **Q:** Difference between Docker and Virtual Machines? **A:** VMs mimic hardware with guest OS overheads; Docker mimics the OS allowing shared host kernels natively saving RAM/CPU.
3. **Q:** What is a Dockerfile? **A:** A text file containing sequential instructions to build a Docker Image.
4. **Q:** What is a Docker Image? **A:** A read-only template containing instructions/libraries to create a Docker container.
5. **Q:** Command to build a Docker image? **A:** `docker build -t name:tag .`
6. **Q:** Command to run a Docker container? **A:** `docker run -d -p host:container image`
7. **Q:** What is Docker Compose? **A:** A YAML tool used for defining and running multi-container Docker applications seamlessly.
8. **Q:** Basic Linux commands you use daily? **A:** `ls`, `cd`, `grep`, `pwd`, `tail`, `htop`, `chmod`, `chown`.
9. **Q:** Difference between `chmod` and `chown`? **A:** `chmod` changes permissions (R/W/X); `chown` changes user ownership.
10. **Q:** How to find a process running on port 80? **A:** `lsof -i :80` or `netstat -tulnp | grep :80`.
11. **Q:** What does `awk` or `sed` do? **A:** Terminal utilities used to manipulate and filter text stream strings.

## Git & GitHub Actions
12. **Q:** What is `git rebase` vs `git merge`? **A:** `merge` combines branches locally maintaining all history; `rebase` rewrites history giving a clean linear workflow.
13. **Q:** Command to save work without committing? **A:** `git stash`
14. **Q:** How do you resolve merge conflicts? **A:** Manually edit the conflicted files locally, drop markers `<<<<<`, run `git add`, and continue merge/rebase.
15. **Q:** What is a GitHub Action? **A:** A CI/CD automation tool reacting to repository events (like a PR) to execute workflows (build, test, deploy).
16. **Q:** What is CI/CD? **A:** Continuous Integration (testing code merges fast) / Continuous Deployment (automating deployments to servers).

## Advanced Integrations (n8n, APIs)
17. **Q:** How do n8n / Zapier work conceptually? **A:** Webhook/polling based event loop handlers moving data between API endpoints visually.
18. **Q:** What is an API? **A:** Application Programming Interface, rules governing communication between software elements.
19. **Q:** REST API principles? **A:** Client-server, stateless, cacheable, uniform interface, layered system.
20. **Q:** What is GraphQL? **A:** Query language for APIs allowing clients to specifically dictate exactly what data they want, no more no less.

## TCS Situational / HR / PM Questions
21. **Q:** What is Agile Methodology? **A:** An iterative approach emphasizing small frequent deployments via sprints rather than monolithic sequential loops (Waterfall).
22. **Q:** What is a Sprint? **A:** A timed container (e.g., 2 weeks) assigned for completing specific feature tickets.
23. **Q:** Explain Scrum. **A:** An agile framework containing daily standups, sprint planning, and retrospectives.
24. **Q:** "You found a bug right before deployment, what do you do?" **A:** Inform the lead. Gauge severity. If critical, delay rollout or patch instantly. If cosmetic, document in an issue tracker and patch next sprint.
25. **Q:** "A teammate is not completing their work. Your action?" **A:** Communicate directly asking if they face blockers. If prolonged, bring it up discreetly in scrum standups so the team can redistribute/aid.
26. **Q:** "You need to learn a whole new stack by next week for a project." **A:** Break down concepts. Relate it to my prior knowledge (Python/React concepts apply elsewhere). Build quick prototypes, relying heavily on documentation.
27. **Q:** Why a career in big Tech/TCS vs a startup? **A:** Exposure to massive-scale infrastructure, specialized team hierarchies, diversity of colossal enterprise projects (Banking/Health), and robust mentorship structures.
28. **Q:** "Describe your weaknesses." **A:** I sometimes dive too deeply into optimizing early on (premature optimization). I've learned to counteract this by building simple functional MVPs first before aggressively refining latency.
29. **Q:** "Describe your strengths." **A:** Immense capability for autonomous fast learning. Shown by moving from ECE to deploying full AI Docker stacks independently.
30. **Q:** "Tell me about your tech hobbies." **A:** Contributing to Python OS tools (like Agno/Cocotb) and experimenting with emerging local LLMs (Llama3) using RAG structures.
...
