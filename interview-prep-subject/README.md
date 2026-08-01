# Interview Prep — Subject-by-Subject Master Resource

> **One resource. Four subjects. Zero fluff.** Built to take you from absolute basics to FAANG/MAANG/YC production-level depth in a single structured reading pass. 456+ files, every section file follows the identical 22-block template (see [`TEMPLATE.md`](TEMPLATE.md)) so you always know where to find the answer.

## 📚 Subjects

| # | Subject | Folder | Files | Parts |
|---|---------|--------|------:|-------|
| 1 | Operating Systems | [`operating-system/`](operating-system/) | 148 | 10 |
| 2 | Computer Networks | [`computer-networks/`](computer-networks/) | 107 | 8 |
| 3 | DBMS (Database Systems) | [`dbms/`](dbms/) | 101 | 8 |
| 4 | OOPs + Design Patterns | [`oops/`](oops/) | 99 | 9 |

## 🧭 How to Use This Resource

1. **Read the master template first** — [`TEMPLATE.md`](TEMPLATE.md) explains the exact anatomy of every section file (the 22 blocks) and why it's structured that way.
2. **Follow study order**: inside each subject, parts are numbered `01 → 10`; chapters `01 → N`; sections `01 → N`. Read them in order — each section builds on the previous.
3. **Never skip the 4 "universal" questions** that every block answers: *Why does this exist? / How does it work? / When is it used? / Why wasn't another approach chosen?* — these are what interviewers probe.
4. **Use the last part of every subject**: `part-XX-interview-question-bank` contains Top-100 question banks, system-design flavored questions, company-specific sets (FAANG/MAANG/Tesla/NVIDIA/Samsung/YC-startup flavor), coding challenges, and a crash-course revision deck.
5. **Self-test every section**: each file ends with **Quiz** (MCQs), **Flashcards**, and **Revision**. Do the quiz *before* checking the answers.

## 🧠 What's Inside Every Section File (the 22-block template)

`1. Why Does This Exist?` → `2. How Does It Work?` → `3. When Is It Used?` → `4. Why Wasn't Another Approach Chosen?` → `5. Intuition` → `6. Real-World Analogy` → `7. Formal Definition` → `8. Example` → `9. Internal Working` → `10. Time Complexity` → `11. Advantages` → `12. Disadvantages` → `13. Interview Questions` → `14. Follow-Up Questions` → `15. Coding Example` → `16. Industry Usage` → `17. References` → `18. Cheat Sheet` → `19. Quiz` → `20. Flashcards` → `21. Revision` → `22. What Interview Questions Come From This Section?`

Every file covers **easy → medium → hard** interview questions including **tricky, practical, production, and scenario-based** ones.

## 🗺️ Subject Roadmaps

- **Operating Systems** — OS fundamentals → kernel architecture → processes/threads → CPU scheduling → synchronization → deadlocks → memory management → virtual memory → file systems → IPC & Linux internals → question bank.
- **Computer Networks** — fundamentals → OSI/TCP-IP → application layer (HTTP/DNS/email) → transport layer (TCP/UDP/QUIC) → network layer (IP/routing/NAT) → data link → physical → security → advanced architectures → question bank.
- **DBMS** — fundamentals → relational model & SQL → normalization → indexing & file organization → transactions & concurrency → recovery → query optimization → NoSQL → question bank.
- **OOPs** — fundamentals → classes/objects → encapsulation/abstraction → inheritance → polymorphism → associations → SOLID → design patterns (GoF) → language-specific (Java/C++/Python) → question bank + LLD guide.

## 🏢 Target Companies

This resource is calibrated for the highest-bar interviews: **Google, Meta, Amazon, Apple, Netflix, Microsoft (FAANG/MAANG)**, **Tesla**, **NVIDIA**, **Samsung**, **YC top startups**, and equivalent high-paying roles (SDE, Systems, Backend, Infrastructure, Data Engineering). The question banks in each subject's final part explicitly call out the company styles and expected depth.

## ✅ Accuracy & Sources

- OS & DBMS theory cross-checked against **Silberschatz (OS Concepts)**, **Tanenbaum**, and real kernel/database internals (Linux `task_struct`, CFS, page tables, InnoDB MVCC, Postgres WAL, ARIES).
- Networking cross-checked against **Kurose & Ross**, **Tanenbaum (Computer Networks)**, and RFCs (793, 8200, 8446, 9110, 9000, etc.).
- OOPs cross-checked against **Effective Java**, **GoF Design Patterns**, **Clean Code**, and JLS.
- References are real, verifiable links (RFC editor, kernel docs, PostgreSQL/MySQL docs).

## 📁 Folder Convention

```
subject/
└── part-XX-name/
    ├── README.md                 (what this part covers, study order, interview weight)
    └── chapter-XX-name/
        ├── README.md             (narrative connecting the sections)
        └── section-XX-topic.md   (ONE topic per file, full 22-block template)
```
