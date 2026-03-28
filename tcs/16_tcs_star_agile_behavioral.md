# TCS HR, Managerial & Behavioral (STAR Method) Questions

The STAR method (Situation, Task, Action, Result) is highly recommended for behavior interviews, especially at companies like TCS where teamwork, leadership, and conflict resolution are paramount.

## Handling Conflict & Teamwork
1. **Q:** Tell me about a time you had a technical disagreement with a teammate. 
   **A (STAR):** 
   - *Situation:* During our SIH Hackathon, my teammate wanted to use a simple Vigenère cipher for fast execution, while I insisted on using AES for security.
   - *Task:* We had to finalize the encryption schema in 1 hour without breaking the codebase.
   - *Action:* I avoided arguing and instead quickly wrote a 20-line benchmarking script comparing AES vs Vigenère speed and security margins. I proved AES execution time was well within our limits.
   - *Result:* He agreed after seeing hard data, and this AES implementation helped us reach the Top 500 final.
2. **Q:** How do you stay motivated when working on boring or legacy code? 
   **A:** I view legacy code as a puzzle. During my work migrating Cocotb 1.x to 2.x, reading old HDL syntaxes was slow. But I stayed motivated by focusing on the "bigger picture"—that I was building an automation tool via LibCST that would save thousands of developer hours in the future.
3. **Q:** Have you ever failed to meet a deadline? 
   **A (STAR):** 
   - *Situation:* During my NullClass internship, I promised a Data Analytics Streamlit dashboard by Friday.
   - *Task:* Midway through, I realized the Pandas aggregations on the raw NLP data took twice as long to process than expected.
   - *Action:* On Wednesday, I proactively communicated the blocker to my mentor. I proposed a compromised solution: deliver a lighter dashboard by Friday showing top-level VADER metrics, and push the deep BERT metrics to Monday.
   - *Result:* The mentor appreciated the early warning and compromise. The pipeline shipped smoothly the following week.

## Client Communication & Agility
4. **Q:** How do you explain complex technical AI concepts to non-technical stakeholders or clients?
   **A:** I rely heavily on analogies rather than jargon. For instance, explaining RAG to a manager: "Instead of asking an AI to memorize all our manuals (fine-tuning, which is expensive), RAG acts like an open-book test—it pulls out the specific manual page when asked a question, ensuring the answer is fact-checked against our own data."
5. **Q:** What would you do if a client drastically changes requirements midway through the sprint?
   **A:** I would document the new requirements and escalate them to my Scrum Master or Project Manager. We’d assess the technical impact, estimate the extra time it costs, and put it in the backlog to swap out current sprint items. Code-wise, I always build components emphasizing loose-coupling so a changing requirement in the frontend doesn't shatter the backend.
6. **Q:** Describe a time you showed leadership without having a leadership title.
   **A:** During my Krip AI internship, our team was writing repetitive setup code for our FastAPI dockers. I took the initiative on a weekend to write a reusable GitHub Action YAML file that fully automated linting and dockerizing. I presented it to my manager on Monday, and it became the standard template for the team.

## Problem Solving & Ambiguity
7. **Q:** Describe a time you had to solve a bug with very little documentation.
   **A (STAR):** 
   - *Situation:* While contributing to the open-source Agno framework, there was an obscure bug in JSON filter parsing occurring in Crawl4AI that had almost zero documentation.
   - *Task:* Fix the bug so enterprise proxies could utilize the crawler framework.
   - *Action:* I thoroughly read the source code of the underlying libraries, set up isolated Pytest mock tests, and ran exhaustive print-statement/debugger step-throughs to pinpoint exactly where the JSON payload mutated strings.
   - *Result:* I submitted an optimized PR that got successfully merged into the parent repository.
8. **Q:** Why did you decide to publish an open-source PyPI package (Cocotb2-Migrator)?
   **A:** I strongly believe in giving back to the community. I recognized a tedious, repetitive pain point developers faced migrating HDLs, and since I enjoyed working with AST manipulation in Python, I wanted to automate the boring stuff for others. It taught me invaluable lessons about writing pip-installable packaging architectures.
9. **Q:** If hired as a TCS Prime associate, what do you expect to achieve in your first 90 days?
   **A:** 
   - Days 1-30: Intensely learn the internal tech stacks, understand the domain logic of my assigned project, and complete all onboarding smoothly.
   - Days 30-60: Take up minor bug fixing tickets, getting accustomed to the CI/CD deployment pipelines, and building rapport with my team.
   - Days 60-90: Deliver a fully fleshed-out feature, optimize an architecture element, and potentially propose an automation improvement using my AI background.
