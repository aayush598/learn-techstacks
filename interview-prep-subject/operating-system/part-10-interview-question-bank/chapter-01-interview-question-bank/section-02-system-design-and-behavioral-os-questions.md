# System-Design and Behavioral OS Questions

> **TL;DR**: Beyond facts, interviews ask "design a scheduler / file system / IPC / allocator" and behavioral "debugging war story" questions. The winning move is a **framework**: clarify requirements → propose components → discuss trade-offs → give a concrete example. Behavioral answers use STAR (Situation, Task, Action, Result) and end with the lesson.

## 1. Why Does This Exist?
Top-100 questions test recall; "design a…" and behavioral questions test whether you can **apply** the concepts. An interviewer asking "design a scheduler" wants to see you gather requirements (OS vs embedded vs real-time?), choose the algorithm (RR vs CFS vs EDF), justify it (throughput vs latency), and flag the traps (starvation, convoy). Behavioral questions ("tell me about a time you debugged a hard problem") test communication, judgment, and ownership — the same qualities the OS questions test technically. Both are graded on *process*, not on "the right answer", because neither has one.

## 2. How Does It Work?
**Design-question framework (the 4-step loop)**:
1. **Requirements** — ask before designing: workload (I/O-bound vs CPU-bound?), constraints (hardware, real-time?, scale), what "good" means (latency/throughput/fairness). This alone separates strong candidates.
2. **Components** — name the pieces: for a scheduler: run queue, policy, preemption, aging; for a filesystem: metadata, allocation, crash safety, VFS integration.
3. **Trade-offs** — for each choice, state the cost: "RR is fair but poor for I/O-bound without priorities; CFS uses vruntime weights; EDF is optimal for deadlines but needs known deadlines".
4. **Concrete example + follow-ups** — walk a scenario, then handle the interviewer's "what if?" (a CPU hog, a disk full, a crash, a massive file).

**Behavioral framework (STAR)**: Situation (context), Task (your goal), Action (what *you* did), Result (measurable outcome) — plus "what did you learn / what would you change". Pick *technical* war stories: a race condition you debugged, a memory leak, a performance regression, an outage caused by a filesystem/permission issue.

## 3. When Is It Used?
- **Systems/OS loops**: every interviewer can ask "design a…" — it scales from intern to staff level.
- **Platform/infra interviews**: "how would you design the process manager", "the file system for a cache", "the IPC for a microservices mesh".
- **Behavioral screens**: "tell me about a hard debugging problem", "a time you disagreed with a design", "a production incident you fixed".
- **Follow-ups after Top-100 answers**: "great — now how would you actually implement that?" is the design pivot.

## 4. Why Wasn't Another Approach Chosen?
- **Jumping to a solution (rejected)**: without requirements, you design for the wrong problem; the interviewer grades requirements-gathering first.
- **One right answer (rejected)**: "design a filesystem" has many valid answers — the trade-off discussion is the deliverable.
- **Only technical / only behavioral (rejected)**: loops mix both; you must be fluent in each mode.
- **Memorized designs (rejected)**: a memorized "design a scheduler" collapses on the first "what if" — the framework survives any prompt.

## 5. Intuition
**Design questions = architecture sketches**: like a whiteboard exercise where the *thinking* is visible. You're a contractor: first you ask what the building is for (requirements), then you sketch the load-bearing walls (components), then you argue steel vs concrete (trade-offs), then you check for edge cases (flood, fire, tenants). The interviewer is the client who keeps asking "what about…?" — and each answer should reference a real design principle.

## 6. Real-World Analogy
**Planning a city's transit system**: you don't just say "build a metro". You ask: city size and density (requirements), pick modes (bus/metro/bike = components), weigh cost vs capacity vs latency (trade-offs), and stress-test with rush hour, floods, and events (edge cases). A systems-design interview is exactly this — the "city" is a scheduler, filesystem, or allocator, and the "traffic" is the workload.

## 7. Formal Definition
Design questions are open-ended prompts whose assessment criteria are: (1) **requirement elicitation** (asking about workload, constraints, SLOs), (2) **component identification** (naming the right subsystems with accurate kernel/CS grounding), (3) **trade-off analysis** (correctly pairing choices with costs: e.g., preemption vs throughput, journaling vs write amplification, contiguous vs indexed allocation), and (4) **robustness** (handling failure, edge cases, scaling). Behavioral questions use the STAR format with a focus on **agency** (first person "I"), **impact** (quantified), and **reflection** (learning).

## 8. Example
Prompt: **"Design a scheduler for a cloud microservice host."**
1. **Requirements**: many short requests (I/O-bound), some CPU-bound (queries, ML), want low tail latency + fair multi-tenant share; OS is Linux.
2. **Components**: use the Linux CFS (rbtree by vruntime) at the base; add cgroups (`cpu.weight`/`cpu.max`) for per-service budgets; NUMA awareness via `cpuset`; consider RT class for latency-critical (e.g., packet processing).
3. **Trade-offs**: CFS gives fairness but tail latency for noisy neighbors → cap with `cpu.max`; I/O-bound tasks benefit from short preemption (CFS handles) + I/O scheduling (mq-deadline); over-subscription handled by the OOM killer + memory cgroups.
4. **Edge cases**: a CPU hog (cpu.max throttles), a hung task (uninterruptible sleep + watchdog), a burst (CFS weights absorb), multi-tenant noise (cgroup isolation). 
**This** is the answer format: requirements first, then components with real kernel grounding, then trade-offs, then robustness.

Behavioral example (STAR): "Debugging a race condition in a logging service — Situation: prod writes intermittently dropped; Task: find and fix; Action: `strace`/`perf` showed a shared offset on fork-inherited fds (Part 09 Sec 03) causing interleaved writes → switched to per-open fds + O_APPEND; Result: drops went from 0.5% to 0, and I documented the fd-sharing footgun for the team."

## 9. Internal Working
1. On the design prompt: repeat it back, then ask 2–3 requirement questions (never design before understanding).
2. Sketch the architecture on the board (blocks + arrows), naming the kernel/CS structures honestly (task_struct, page cache, journal, page tables).
3. For every block, state one trade-off ("this costs X but buys Y").
4. Walk one end-to-end scenario (a request through the system), then stress it (crash, full disk, slow peer, many tenants).
5. For behavioral: pick a *technical* story, use STAR, quantify, and end with the lesson — never name-drop blame.

## 10. Time Complexity
- Design rounds: ~10–20 minutes per prompt; expected structure: 25% requirements, 40% components + trade-offs, 35% scenario/edge cases.
- Behavioral answers: 2–3 minutes each (STAR); keep Action ~60% of the time.

## 11. Advantages
- **Process-graded**: the framework is teachable and repeatable — a weak domain becomes a strong "I'd approach it this way".
- **Shows depth**: naming real kernel structures (vs generic "a queue") differentiates.
- **Survives follow-ups**: trade-off-based answers anticipate the interviewer's "what if".
- **Portable**: the same 4-step loop works for any design prompt, OS or not.

## 12. Disadvantages
- **Time pressure**: it's easy to design prematurely; the requirement phase can burn the clock if overdone.
- **Ambiguity**: without a framework, candidates freeze or ramble — the opposite of a crisp architecture sketch.
- **Behavioral traps**: blaming others, vague "we" language, and no quantified result kill STAR answers.

## 13. Interview Questions
1. **Q: How do you approach "design a scheduler"?** A: Requirements first (workload, constraints, SLO), then components (run queue, policy, preemption, aging, cgroups for multi-tenant), trade-offs (RR vs CFS vs EDF, fairness vs latency), then a scenario + edge cases (CPU hog, starved task, real-time).
2. **Q: How do you approach "design a file system"?** A: Requirements (file size profile, reliability, crash tolerance), components (inode/metadata, allocation — extents vs block lists, directory index, journal/CoW, VFS ops), trade-offs (journal vs write amplification, contiguous vs indexed), robustness (crash, full disk, fsck, RAID).
3. **Q: How do you approach "design an IPC system"?** A: Requirements (latency, throughput, local vs network, message size), components (pipe/MQ/shm/socket/signal choice per Section 06 of Part 09), trade-offs (shm needs sync; sockets general but heavier), robustness (buffer full, blocked sender, peer crash).
4. **Q: How do you approach "design a memory allocator"?** A: Requirements (size distribution, multithreading, fragmentation tolerance), components (bins/buddy/slab, thread-local caches, free-list), trade-offs (internal vs external fragmentation, fast path vs generality), robustness (OOM, use-after-free detection).
5. **Q: What are the top requirement questions to ask?** A: Workload (I/O vs CPU bound, read vs write heavy), scale (QPS, data size, # tenants), latency vs throughput priority, real-time constraints, failure tolerance, hardware/deployment.
6. **Q: How do you show depth in a design?** A: Name the real structures: task_struct/CFS/cgroups for scheduling; page cache/`address_space` for file I/O; futex for sync; PAGE_OFFSET/vmalloc for memory; JBD2/CoW for crash safety — then justify each with its trade-off.
7. **Q: What's the behavioral structure?** A: STAR — Situation (context), Task (your goal), Action (what you did, in first person), Result (quantified), plus the lesson/change. Pick a technical debugging story (race, memory leak, perf regression, outage).
8. **Q: What makes a good debugging story?** A: A real problem with a concrete diagnosis path (`strace`/`perf`/page-fault analysis), an actual fix, a measurable result, and a takeaway — the interviewer wants to see methodical debugging and ownership.
9. **Q: How do you handle "what if the interviewer keeps asking what if?"** A: That's the sign of a good design conversation — treat each as a new requirement/trade-off to fold into the framework (e.g., "then I'd add cpu.max throttling and an OOM policy").
10. **Q: What if you're asked to design something outside your expertise?** A: Use the framework anyway — requirements + analogies from what you know (e.g., "design a key-value store" → filesystem page-cache/DB indexing principles) — the interviewer grades the approach.
11. **Q: How do you prioritize trade-offs in the answer?** A: State the primary metric the requirements imply (latency vs throughput vs simplicity), then present each choice as "X buys Y at cost Z" and let the interviewer pick the direction.
12. **Q: How long should the architecture sketch take?** A: ~5 minutes of the 15–20 for the full design; the rest goes to the scenario walkthrough and edge cases — a sketch without robustness discussion is incomplete.

## 14. Follow-Up Questions
1. **Q: What is the difference between a design interview and a coding interview?** A: Coding = correctness + efficiency of implementation; design = architecture, trade-offs, communication. OS design rounds blur them: you may sketch a scheduler AND implement a piece.
2. **Q: How do you prepare for behavioral OS questions?** A: Prepare 3–4 technical STAR stories: a race/fix, a performance regression, a production incident, a cross-team disagreement — quantified, first-person, lesson-forward.
3. **Q: What's a common mistake in design answers?** A: Naming a solution without requirements, or listing components without trade-offs — both signal junior-level systems thinking.

## 15. Coding Example
```c
// A tiny scheduler "design" turned into code (the trade-off made concrete):
// RR with priority aging — naive but shows the framework's components.
#include <stdio.h>

#define N 3
typedef struct { int prio; int slice; int waiting; } task_t;

// Round-robin over ready tasks; aging raises waiters' effective priority.
int pick(task_t *t, int n, int *tick) {
    int best = -1;
    for (int i = 0; i < n; i++) {
        t[i].waiting++;
        if (t[i].slice > 0 &&
            (best < 0 || t[i].prio + t[i].waiting / 4 > t[best].prio + t[best].waiting / 4))
            best = i;   // effective priority = base + aging
    }
    if (best >= 0) { t[best].slice--; t[best].waiting = 0; (*tick)++; }
    return best;
}

int main(void) {
    task_t t[N] = {{ .prio = 5, .slice = 3 }, { .prio = 3, .slice = 3 }, { .prio = 1, .slice = 3 }};
    int tick = 0;
    for (int i = 0; i < 9 && pick(t, N, &tick) >= 0; i++)
        printf("tick %d ran task with base prio=%d\n", i, t[i % N].prio);
    return 0;
}
```
This is the "components + trade-off + edge case (aging defeats starvation)" answer rendered as a runnable sketch.

## 16. Industry Usage
- **Interview loops at systems companies**: FAANG systems/OS rounds, platform teams, cloud providers (GCP/AWS/Azure), databases (MongoDB, Redis Labs), infra (Cloudflare, Stripe) — all use design + behavioral OS prompts.
- **Staff/principal level**: designs scale up ("design the process isolation for a multi-tenant platform") and behavioral stories scale to incidents/architecture decisions.
- **Mock interviews**: the framework is standard practice for coaching and self-prep.

## 17. References
- Silberschatz (concepts for trade-off language), Tanenbaum (design discussion), Love (kernel depth to name structures).
- Cracking the Coding Interview (behavioral STAR framing), "Designing Data-Intensive Applications" (trade-off language for storage/scheduling at scale).
- This series: Part 03 (scheduling), Part 06/07 (allocators/memory), Part 08 (filesystems), Part 09 (IPC/Linux) — the source material for the design blocks.

## 18. Cheat Sheet
- Design loop: Requirements → Components → Trade-offs → Scenario + Edge cases.
- Always ask 2–3 requirement questions first.
- Name real structures (task_struct, CFS, page cache, JBD2, futex, sys_call_table).
- Every choice: "X buys Y at cost Z".
- Behavioral: STAR with first-person agency + quantified result + lesson.
- Debugging stories: diagnosis path → fix → measurable result → takeaway.
- Unknown topic → use the framework with analogies.

## 19. Quiz
1. First step in a design answer? a) solution b) requirements c) code d) trade-offs → **b**
2. The grader wants? a) one answer b) trade-off reasoning c) speed d) jargon → **b**
3. Behavioral format? a) PAR b) STAR c) RAS d) TASK → **b**
4. Depth is shown by? a) naming real kernel structs b) big words c) speed d) length → **a**
5. Handle "what if" by? a) ignoring b) folding into framework c) restating d) guessing → **b**
6. Action should be ~? a) 10% b) 60% c) 90% d) 0% → **b**

## 20. Flashcards
- **Q: Design loop?** → **A:** Requirements → Components → Trade-offs → Scenario.
- **Q: First question?** → **A:** What are the requirements/workload?
- **Q: Show depth?** → **A:** Name real kernel structures with trade-offs.
- **Q: Behavioral format?** → **A:** STAR + quantified result + lesson.
- **Q: Every choice costs?** → **A:** State the cost explicitly.
- **Q: Unknown topic?** → **A:** Use the framework + analogies.

## 21. Revision
Design and behavioral questions are the "apply" layer of the OS series. The design loop — requirements → components → trade-offs → scenario/edge cases — handles any prompt ("design a scheduler/filesystem/IPC/allocator") and rewards naming real kernel structures with their costs. Behavioral answers use STAR with agency, quantified impact, and a lesson; technical debugging stories (race, leak, regression, incident) are the strongest material. The framework is the deliverable: it turns ambiguity into a structured, survivable answer, and it's what separates recall (Section 01) from engineering judgment.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "How do you approach design a scheduler?" | 13 Q1 / 8 Example |
| "How do you approach design a filesystem?" | 13 Q2 / 8 Example |
| "Top requirement questions?" | 13 Q5 / 2 How |
| "How to show depth?" | 13 Q6 / 9 Internal |
| "Behavioral structure?" | 13 Q7 / 2 How |
| "Good debugging story?" | 13 Q8 / 8 Example |
| "Handle what-if?" | 13 Q9 / 9 Internal |
| "How long for the sketch?" | 13 Q12 / 10 Complexity |
