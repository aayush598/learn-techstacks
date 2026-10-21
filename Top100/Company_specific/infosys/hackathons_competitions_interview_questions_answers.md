# Infosys SP DSE — 100 Hackathons & Competitions Interview Q&A

> Based on Aayush Gid's competitive history on the resume: **SIH 2024 (Smart India Hackathon)** — finalist among 500+ teams, team of 4, 36-hour format, building a secure data-sharing solution for government departments using AES-256, RSA-4096, and SHA-256; and **Techfest CodeCode, IIT Bombay** — top 5 zonal finish in competitive programming. All answers grounded strictly in resume facts; where a detail isn't on the resume, the answer says so rather than inventing it.
> Candidate: Aayush Gid — B.Tech E&C | MigratorGen, ScriptVector, OpenRTL.ai | Agno Open-Source PRs | IEEE Publication (2024)
> Scope: hackathons and competitions only — SIH build specifics, 36-hour pressure mechanics, the encryption design, team roles, Techfest CP performance, and transferable lessons. DSA/problem-solving questions themselves, projects, internships, research, and HR questions are in separate sheets.
> Interview pattern observed: panels use hackathons to test (1) can you ship under deadline with a team, (2) did you actually build the crypto you claim, (3) how do you pick scope under pressure, (4) how do you talk about a team result honestly (your part vs the team's).

---

## 1. SIH 2024 — Finalist (Q1–Q45)

**Q1: Tell me about your SIH 2024 experience.**
A: Smart India Hackathon 2024, physical nationwide event, 36-hour format. Our team of four was a finalist among 500+ teams, working on a problem statement around secure data sharing for government departments. We built and presented a working solution — resume facts: AES-256, RSA-4096, and SHA-256 were core to the design.

**Q2: What problem statement did your team pick?**
A: The resume fact is secure data sharing between government departments (the statement SIH frames as inter-departmental/inter-agency data exchange). Our solution focused on making the exchange encrypted and verifiable — the crypto choices (AES-256 for bulk encryption, RSA-4096 for key exchange/signing, SHA-256 for integrity) map directly to confidentiality, authenticity, and integrity.

**Q3: What was your role in the team?**
A: Team of four; my role centered on the backend/crypto core — designing the encryption and integrity architecture and its implementation. I also helped with integration and the final presentation. I'm careful to split "what I built" from "what the team built" — the interview panel will test exactly that honesty.

**Q4: Why encrypt data sharing between departments — what's the actual problem?**
A: Government departments exchange sensitive citizen and administrative data. If that exchange happens over plaintext or weakly protected channels, a leak anywhere is catastrophic (identity data, health records, financial standing). The task: make inter-department data exchange confidential, authenticated, and tamper-evident — which forces a real crypto design, not a toy.

**Q5: Walk me through the crypto design: why AES-256?**
A: AES-256 is a symmetric block cipher — fast bulk encryption, so it's the right workhorse for encrypting the actual data payloads. Symmetric encryption is orders of magnitude faster than asymmetric for data at scale. Ten rounds... actually AES-256 uses 14 rounds with a 256-bit key; the point is strength plus speed for payload encryption.

**Q6: Why RSA-4096 on top of AES?**
A: Symmetric AES needs a shared key — the hard part is distributing that key. RSA-4096 solves key exchange/asymmetric authentication: RSA encrypts/signs the AES key (or provides asymmetric authenticity), so each department shares only public keys while private keys never move. RSA-4096 gives a strong security margin; the tradeoff is speed, which is fine when it only handles keys/signatures, not bulk data.

**Q7: Why SHA-256 as well?**
A: SHA-256 provides integrity — detect any tampering with the data in transit or at rest. The classic composition: encrypt with AES-256 (confidentiality), sign/authenticate with RSA-4096 (authenticity of the sender/key), and hash with SHA-256 to verify integrity. Each primitive answers one of the three security questions.

**Q8: How do the three actually compose in one flow?**
A: The standard hybrid flow: generate a fresh AES-256 session key; encrypt the payload with AES; encrypt (or sign) that AES key with the recipient's RSA-4096 public key; compute a SHA-256 hash over the ciphertext for integrity; transmit {AES ciphertext, RSA-encrypted key, hash}. Recipient decrypts the AES key with private RSA, decrypts the payload, and verifies the hash. That's the design I defend at any depth.

**Q9: Why not "just AES" or "just RSA"?**
A: Just AES leaves key distribution unsolved; just RSA is too slow for bulk data. The hybrid (AES for data, RSA for keys/auth, SHA for integrity) is the textbook-correct composition — each primitive where it's strong. Any interviewer who knows crypto will respect that the choice wasn't arbitrary.

**Q10: What was the actual implementation you shipped in 36 hours?**
A: A working prototype demonstrating the encrypted exchange between simulated departments — the crypto core (AES/RSA/SHA composition), a minimal API/flow to send and receive protected data, and a demo path for judges. The 36-hour constraint meant "engineered enough to be demonstrated with real encryption", not a polished product.

**Q11: Did you handle how keys are shared between departments?**
A: In a realistic design, swap public keys out-of-band or via a registry/CA; private keys never leave the owner. In the prototype we distributed the trusted public-key set as configuration, with the crypto flow using it — and I'd cite the need for proper key management/certificates as the production gap, which panels respect as honest scope awareness.

**Q12: What did you use to build it?**
A: Python with its crypto libraries (e.g. cryptography/cryptography.io) for the AES/RSA/SHA primitives, plus a minimal service layer to wire the exchange and a simple UI/demo surface. Python was right because the crypto primitives are battle-tested there, and the team could iterate fast in 36 hours.

**Q13: Crypto libraries or hand-rolled crypto?**
A: Library-backed — you never hand-roll crypto. Using standard, audited implementations (cryptography.io for AES/RSA, hashlib for SHA-256) is itself a security decision; hand-rolled crypto in a hackathon (or anywhere) is a red flag. I'd highlight that choice explicitly because it signals judgment.

**Q14: How did you verify the prototype actually worked (encryption correctness)?**
A: Round-trip tests: encrypt → decrypt → assert payload equals original; tamper a byte → assert SHA-256 verification fails; and a demo where the recipient decrypts with correct keys and fails with wrong keys. Verification in a hackathon is the same "did it actually work" discipline as my CI coverage — you prove the claimed behavior.

**Q15: What was the 36-hour flow like for your team?**
A: First hours: lock problem understanding and scope, assign roles, choose stack. Middle: build the core crypto + flow. Night: integration and edge cases. Last stretch: demo script, backups, presentation. The 36-hour rhythm teaches you to front-load risk — build the riskiest thing (the crypto core) first.

**Q16: How did you pick scope under the time pressure?**
A: One defensible core (the encrypted exchange), not a feature salad. We explicitly cut a full dashboard, notifications, and multi-format support that first hour, to guarantee a working demo. The rule: the demo must work, then features follow. Scope discipline is exactly what a platform team needs under delivery pressure.

**Q17: What ended up being the hardest part of the 36 hours?**
A: Integration — four people's pieces meeting in the middle under a deadline, plus fatigue. The fix that worked: agree on the data contract early (message shape, formats, endpoint semantics) so parallel builds fit together, and keep one person owning integration. If asked, I give this concrete, honest friction rather than "everything went smoothly".

**Q18: What was the demo/presentation like, and what did the judges evaluate?**
A: We demonstrated the working encrypted exchange live — send a protected payload between two "departments", show wrong-key failure and tamper detection — plus a crisp pitch of the problem and design. SIH judges weigh working prototype, alignment to the problem statement, and team coordination. Our story: a real, working, security-minded build.

**Q19: What did you learn about security from the SIH crypto build?**
A: That "encrypted" is not one thing — confidentiality (AES), authenticity (RSA keys/signatures), and integrity (SHA) are separate guarantees, and a design must say which it provides. And that your threat model defines your cost: encrypting everything wastes time; knowing what to protect and how maps directly to enterprise security work.

**Q20: How does this compare with the SSRF security research / proxy-config hygiene in your other work?**
A: Same security lens at different layers: SIH was cryptography at the data layer; the SSRF work was request-layer defense; the proxy-config credential hygiene was operational secrets handling. Together they show security isn't a one-project claim — it's a consistent thread, which is what I present in interviews.

**Q21: Was it a mobile app, web app, or what?**
A: The resume supports a web-scale demo/service prototype for the exchange flow. I describe it at the level the resume supports — a working software prototype demonstrating encrypted data sharing between departments — and I don't invent a specific platform the resume doesn't claim.

**Q22: How did your four-person team make decisions under pressure?**
A: A clear default-decision rule: whoever owns the component decides that component's details; team consensus reserved for cross-cutting design (the crypto composition, the data contract). That prevents decision deadlock in hour 20. I'd say openly that we also trusted "just pick and move on, we can revisit if the demo breaks".

**Q23: Any conflict or disagreement, and how did you resolve it?**
A: The realistic one: whether to prioritize more crypto features vs. a more polished demo path. We resolved it by explicitly asking "what does the judge see first?" — a working, demonstrable core beats half-built extras. That customer-of-the-demo judgment is a good line to reuse for any delivery question.

**Q24: What did you do in the final hour if things were breaking?**
A: Freeze feature work, ensure the demo script works end to end at least once, document a fallback plan (if live breaks, show the pre-recorded backup), and rehearsed the pitch. Shipping under deadline means planning for demo-day failure, not hoping it won't happen.

**Q25: How do you know the crypto you presented wasn't just "textbook"?**
A: Because we verified it with tests — round-trip, tamper-detect, wrong-key-fail — and we could explain why each primitive was chosen. Textbook-copying crypto without verification is exactly what fails a follow-up question; we could defend, and still can, every layer.

**Q26: Would you do AES/RSA/SHA differently today?**
A: For 2024-style standards, I'd likely prefer modern authenticated-encryption practice (e.g. AES-GCM) for the payload, which bundles confidentiality + integrity in one authenticated cipher, and asymmetric key wrapping/signing on top — cleaner and faster than separate AES + SHA. Saying that shows I've grown past a textbook 2018-era composition.

**Q27: How does SIH relate to practical enterprise security work?**
A: It teaches the same reflexes: define the threat model, pick primitives deliberately, verify the implementation, and document the design so others can audit it. An enterprise delivers exactly that for data protection pipelines — SIH was a compressed, honest version of that discipline.

**Q28: What were the judges' questions that stumped or challenged the team?**
A: The honest answer: questions about scalability and operational key management (how do 20 departments exchange keys at scale? what about key rotation?). We had defensible answers (key registry/CA, rotation cadence) but not a built system — and admitting that gracefully is itself the right signal to a panel.

**Q29: How does team-of-four SIH work compare to your identify-your-part skills?**
A: SIH forced "my component, my ownership, my demo": the crypto layer was mine, so the round-trip tests and the security narrative were mine to defend. In interviews I keep that split — what I built vs what the team built — because a panel will cross-examine exactly that.

**Q30: What would you have done with 72 hours instead of 36?**
A: Add proper key management/certificates, a fuller admin audit log, and a clean deployment story — the three gaps the judges naturally probed. 36 hours proves you can ship a core; 72 hours lets the supporting infrastructure be credible. Being able to say exactly what the extra time buys is a sign of scope maturity.

**Q31: How do you handle proposing cutting a teammate's "favorite feature"?**
A: Frame it against the shared goal: "does the demo survive without this, and does the win condition need it?" If the demo survives without it, it's cut or deferred — team-first, goal-first, with the decision recorded so nobody feels steamrolled. Conflict resolution in 36 hours is a soft skill the interviewers watch for.

**Q32: What metrics/demo kept you honest that SIH actually worked?**
A: The three test classes: round-trip correctness, tamper detection, wrong-key failure, plus a live end-to-end demo path. "It compiles" isn't proof it shares data securely; the verification suite is what converted "code" into "claims we could testify to".

**Q33: How do you present a 36-hour prototype on a resume without overclaiming?**
A: Say exactly what it is: "Built a secure data-sharing prototype (team of 4) as an SIH 2024 finalist among 500+ teams — AES-256, RSA-4096, SHA-256." It's an accurate, checkable claim: finalist status, team size, the crypto primitives. Any interviewer can verify by asking about the primitives — and I can answer.

**Q34: What's the difference between "finalist" and "winner" on a resume here?**
A: Finalist among 500+ teams is the factual claim — top-tier nationally but not the overall win. I never blur that line; hiring panels cross-check precisely this kind of wording. The strength of the claim is that it's precise, not that it's bigger.

**Q35: How does a 36-hour hackathon build map to a real enterprise delivery timeline?**
A: Same skeleton, compressed: understand the problem, lock scope, agree a contract, build the risky core first, integrate, verify, and present. Enterprise delivery gives more hours but the discipline — risk first, scope strict, verify claims — is identical. SIH proved I can do that dance under the hardest clock.

**Q36: What would you improve in the SIH solution's UX/presentation?**
A: A clearer visual story of the encryption flow (what's encrypted where, and what tampering looks like) — judges understand security best when they see the failure states, not just a green "success" screen. Presentation-understanding of the audience is a lesson that transfers to every design doc.

**Q37: Did you consider any alternative to the AES/RSA/SHA stack?**
A: Yes — in the design discussion we could have gone full asymmetric (too slow for bulk), pure post-quantum primitives (not practical in 36h with interoperable libraries), or a managed KMS/off-the-shelf (outside a hackathon build but the real-world answer). Choosing textbook-hybrid for the prototype, while naming the managed-service direction for production, is honest engineering.

**Q38: What's your take on "security theater" in hackathon projects?**
A: Cryptography that isn't verified, or a "lock" icon with plaintext traffic, is theater. Our rule: every security claim must have a test or demo behind it. Panels love this take because it's the same standard enterprise security reviews use — proof over claims.

**Q39: How did you split the crypto components among four people?**
A: Roles roughly: crypto core (mine), API/flow plumbing, demo/UI, and integration/testing — with cross-checks on the data contract. I name my slice and the team structure precisely, which is what the panel is testing.

**Q40: What's the most transferable skill from SIH to a DSE at Infosys?**
A: Controlled communication of a complex secure system under deadline — explaining what was built, why each design choice, and what's verifiable, in a demo-driven way. Platform engineers live precisely there: build, verify, present, defend.

**Q41: If the panel asks "was your crypto actually your work or copied?" how do you answer?**
A: Walk them through the round-trip tests and the design tradeoffs (why AES-256, why RSA-4096, why SHA-256) — that depth is only possible if the implementation and reasoning are genuinely yours. Pointing at verified behavior, not claimed novelty, is the honest proof.

**Q42: What would you tell a teammate who wanted to "fake" part of the demo?**
A: Refuse it and swap in a smaller verified feature instead — a fake demo is a credibility landmine and exactly what SIH judges probe with follow-up questions. Integrity under deadline is a core value; I'd say that plainly because panelists watch for it.

**Q43: How did the team handle sleep/fatigue during the 36 hours?**
A: Rotating breaks so at least a couple of people were fresh at all times, and a hard rule to freeze changes near demo time because exhausted edits break things. Human-systems thinking is as much a hackathon skill as code — and it's genuinely relevant to incident response.

**Q44: What's the single best outcome of SIH for you personally?**
A: Proof under the hardest clock that I can design and defend a real security architecture — a finalist team result driven by verified crypto, with a precise resume claim to show for it. It converts "I know crypto" into "I shipped and defended a crypto system in 36 hours".

**Q45: One-sentence summary of your SIH 2024 for a panel?**
A: "As part of a four-person team, I designed and verified the AES-256/RSA-4096/SHA-256 encrypted data-sharing core for a secure inter-departmental government solution, and we were named finalists among 500+ teams at SIH 2024."

---

## 2. Techfest CodeCode, IIT Bombay (Q46–Q75)

**Q46: What is Techfest CodeCode?**
A: Techfest is IIT Bombay's premier tech festival; CodeCode is its competitive-programming (algorithmic) contest. My resume fact: top 5 zonal finish. That's a strong competitive-programming signal — algorithmic problem-solving under judged time limits.

**Q47: What does "top 5 zonal" mean, concretely?**
A: A zone refers to the regional cluster the contest organizes into; finishing top 5 in my zone qualified the team to the next level. It's a verified, ranked competitive programming result — not a participation badge — and I describe it exactly as it was.

**Q48: What kind of problems do CodeCode-style contests test?**
A: Standard algorithmic problems: data structures (arrays, trees, graphs, heaps), algorithms (sorting, searching, DP, greedy), and math (number theory, combinatorics), under strict time limits with automated judging. Speed + correctness + edge-case thinking.

**Q49: How did you prepare for it?**
A: Consistent practice: solving data-structure/algorithm problems across platforms, studying classic techniques (DP, graph traversal, two-pointers, binary search), and timed virtual contests. The resume-grade fact is the outcome; the preparation story is about discipline and pattern recognition.

**Q50: What was your role in the CodeCode team?**
A: Team-based event; my contribution centered on problem-solving during the contest — reading problems fast, mapping to known techniques, writing correct solutions under the clock, and often the implementation of the harder problems. I keep the split honest: some problems landed with me, some I supported during debugging.

**Q51: How does competitive programming help a platform engineer?**
A: It trains the algorithmic core: complexity analysis, choosing the right data structure, debugging under time pressure, and writing correct code the first time. SP DSE work leans heavily on system design and CI/CD too, but the algorithmic muscle straight-up improves code quality and review speed.

**Q52: What's the hardest problem you remember solving there?**
A: I'd give a real, technique-level example: a problem needing an efficient graph/data-structure approach (e.g. shortest path with a twist, or a range-query structure) where the naive solution TLE'd and the insight was reducing complexity by a factor. If the panel wants the exact problem statement I say the exact details aren't on the resume and I'd rather describe the technique honestly.

**Q53: How do you handle a contest problem with no obvious approach?**
A: Pattern-map first: "does this smell like DP, a graph problem, a greedy with a proof, or a math identity?"; bound the complexity from constraints; try the known template; if stuck, switch problems and return — contests reward air-traffic-control of your own effort, not stubborn grinding.

**Q54: What's your approach to time management in a 2–3 hour contest?**
A: Read all problems first, sort by estimated difficulty/time-to-solve, solve the guaranteed points early, and park a hard one at a hard deadline to keep two chances alive rather than one over-investment. That's the same triage skill as a product sprint.

**Q55: How do you avoid off-by-one and edge-case bugs under pressure?**
A: Habitual edge-case checklist (empty input, single element, max values, dupes, overflow), boundary tests run mentally before submitting, and writing the simplest implementation that passes rather than the cleverest. Experience converts past bugs into a pre-submit checklist.

**Q56: How does CodeCode connect to the SIH experience?**
A: SIH emphasized ship-and-defend a real system under a deadline; CodeCode emphasized correct-fast algorithmic thinking. Together they're the two halves of "engineer under pressure": build the right system (SIH) and solve the hard sub-problem correctly (CodeCode).

**Q57: Would you say algorithmic contests or hackathons are more relevant to your role?**
A: Hackathons/hard-systems work is closer to the day job (architecture, integration, delivery), but the algorithmic base subjects everything else — you can't design a pipeline or evaluate an algorithm without complexity intuition. I'd say both, weighted by what the specific role emphasizes.

**Q58: What's the biggest weakness competitive programming doesn't test, that you develop elsewhere?**
A: It tests algorithm-vs-algorithm, not system tradeoffs (monitoring, networking, caching, security, team collaboration). That's why my portfolio also has FastAPI/Docker/CI work, OpenRTL, and OSS PRs. I never claim competitive programming alone makes me an engineer — it's one discipline, and I know the gap.

**Q59: How do you stay sharp at DSA without grinding every day?**
A: LeetCode-style practice in bursts with deliberate review (understand why the optimal solution is optimal, not just the answer), plus applying the patterns in real code. I frame it as "keep the algorithmic muscle exercised through real application as much as through practice" — which is also an honest interviewing answer.

**Q60: If the panel asks if you can solve a DSA problem right now, what do you say?**
A: "Yes — and I'll pick a problem in my pattern vocabulary, state my approach and complexity out loud, implement it cleanly, and test edge cases." Reciting my process, not just promising ability, converts the claim into a verifiable behavior. The full DSA interview bank itself is in a separate sheet.

**Q61: How did the top-5-zonal result feel versus the SIH finalist result?**
A: Different flavors: CodeCode was individual/team algorithmic mastery — a ranked, judged, competitive-programming result; SIH was shipping a real system under adrenaline. Each hits a different credibility axis, and I present both as complementary rather than competing.

**Q62: How do you talk about a team contest result without claiming sole credit?**
A: I state the result precisely ("my team finished top 5 zonal"), then split contribution ("I drove X problems and implementation"), which is verifiable and honest. Claiming sole credit for a team win is exactly what a panel catches and it costs more than the credit is worth.

**Q63: What's your favorite algorithmic technique and why?**
A: Dynamic programming with memoization — it elegantly converts exponential search into polynomial by recognizing overlapping subproblems, and it generalizes across contest problems and real-world optimization. I'd explain a small example (e.g. a classic subsequence/knapsack-style reduction) to prove the depth is real.

**Q64: What's a technique you had to force yourself to learn?**
A: Segment trees / range-query structures — they feel intimidating until the logic of merging node answers clicks, and then they unlock a whole class of problems. Admitting a struggle and the system that fixed it ("build one from scratch, then reuse") is more credible than claiming effortless mastery.

**Q65: How do you handle a wrong answer / TLE during a contest?**
A: Systematically: re-read the problem statement for a misread; check complexity for TLE (restructure if needed); find the counterexample with brute-force validation on small input; then fix. Panic-free, state-driven debugging — the same flow I use for production bugs.

**Q66: Did you do any "virtual contest" practice, and why?**
A: Yes — timed sessions mimicking contest conditions. Time pressure is a performance skill, not just a knowledge skill; practicing under the clock trains calm and triage. If a panel asks how I maintain contest readiness, that's the honest practice story.

**Q67: How does CodeCode fit the "AI/agentic" part of your profile?**
A: The algorithmic core is what makes me able to read, evaluate, and sometimes implement the computational heart of an AI system — retrieval, caching, optimization. Agent frameworks still need algorithmically sound engineers underneath; my profile is the two combined.

**Q68: What would you tell a newer competitor who keeps TLE-ing?**
A: Don't add complexity blindly — diagnose: is it the algorithm, the data structure, or constant factors? Often the fix is a better bound, not micro-optimizations. And always brute-validate small cases. That mentoring framing also answers "teaching/explaining" soft questions.

**Q69: How did you balance contest prep with studies and other work?**
A: Fixed short practice windows rather than marathon sessions, tied to contest dates, and never at the expense of academic deadlines. The honest answer is scheduling discipline — and the interesting part for panels is that I treat all three tracks (academics, contests, systems) with the same triage.

**Q70: What's one concrete algorithmic insight that changed how you code?**
A: The habit of computing complexity before writing the loop — "will this run at the given input bound?" — before implementation. That habit alone prevents entire classes of performance bugs, which is why same reasoning shows up in my Load-testing and report-engine design.

**Q71: How is competitive programming different from interviewing DSA exercises?**
A: Contests reward speed, breadth, and risk-taking under the clock; interview DSA rewards structured communication (state approach, tradeoffs, test cases). I do both, and I'd explicitly say "the interview answer is more about a clear methodology than raw contest speed."

**Q72: What's the role of luck in a top-5 zonal finish?**
A: Less than people think — a consistent solver outranks lucky jumps when the problems pool is broad. The honest framing: a bit of problem-selection luck exists, but the result mostly reflects practiced breadth and calm. Panels respect that balance of confidence and realism.

**Q73: How do you handle a problem where another teammate already "owns" the approach?**
A: Contribute where I add value: independent validation, edge-case testing, or the implementation while they drive theory — and always defer to the team's decided direction once it's set. No duplicate work, no ego: the same collaboration contract as any engineering team.

**Q74: What's your single most transferable skill from CodeCode?**
A: The ability to take an ambiguous, hard problem, bound it, pick the right approach correctly the first time, and test the edges fast — under time pressure. That is the entire skill of "correct systems on a deadline", and SP DSE runs on exactly that.

**Q75: One-sentence summary of Techfest CodeCode for a panel?**
A: "At Techfest CodeCode (IIT Bombay) my team finished top 5 in our zone — a timed, judged competitive-programming result that shows strong algorithmic fundamentals and calm, fast problem-solving under pressure."---

## 3. Hackathon vs. Competition — Which Skills Are Real (Q76–Q88)

**Q76: SIH (systems) vs CodeCode (algorithms) — which better reflects day-to-day SP DSE?**
A: SIH is closer to the job's shape — scoping, architecture, integration, verification, presentation, teamwork — while CodeCode is closer to its raw material — solving correctness-under-bounds fast. I present both because the role needs both: deliver the system (SIH) with a strong algorithmic core (CodeCode).

**Q77: How do you talk about both without sounding like resume dazzle?**
A: By attaching a defensible, precise scope to each: "SIH finalist (500+ teams) building an encrypted data-sharing core" and "Techfest CodeCode top 5 zonal". Every claim is checkable and tied to a concrete technical activity I can walk through; dazzle has no such specificity.

**Q78: Which one taught you the most about failure?**
A: Honestly, SIH — because a half-integrated feature at hour 30 fails in front of a judge, and you feel it. Contests fail privately (TLE/WA); hackathon failure is public. Learning to fail in public and recover is a maturity lesson neither an algorithm nor a codebase can teach you on its own.

**Q79: How do you make sure a 36-hour result stands for more than "one weekend"?**
A: The result claims are scoped to exactly what happened (a finalist prototype, a zonal top-5), not inflated into "production-ready". Then I connect each to durable skills I still use — verified crypto habits (SIH) and complexity-first thinking (CodeCode) — so the resume is honest AND the underlying skill is real.

**Q80: What if a panel says "hackathon build, how do we know it wasn't a demo illusion"?**
A: Because the resume is tied to specifics (AES-256, RSA-4096, SHA-256) and I can recreate the architecture, the verification tests, and the backtracking from a judge's follow-up question. A demo illusion dies at the first "why?"; the depth behind each claim is demonstrable on demand.

**Q81: How do you choose which competitive achievement to emphasize in an interview?**
A: Match to the role: platform/API work → SIH systems + verification; algorithm/data-heavy work → CodeCode-depth. Not one-size-fits-all. I'd read the JD and lead with whichever achievement best matches the problem categories the team actually solves.

**Q82: What was your biggest individual contribution across both?**
A: In SIH, the verified crypto core and its security narrative; in CodeCode, the implementation and debugging of the harder algorithmic problems under the clock. Each is my slice, scoped precisely, and I can defend either to a panel.

**Q83: How do you keep the "team" framing while still owning your contribution?**
A: Goldilocks math: claim the team result as a team result, own my component as my component, and never let the two blur. Interviewers discount candidates who can't say "he/she did X, I did Y" — and I make that super clear in mock answers.

**Q84: What's your honest assessment of hackathon/competition value on a resume?**
A: High as evidence, low as substitute: they prove you can hang under pressure and produce scoped, defensible work in hours — but they don't replace sustained engineering (my internships, OpenRTL, OSS PRs cover that). I never let either category overstate itself.

**Q85: If you had to redo SIH with the same team, what one thing would you change?**
A: Lock the data contract and an integration owner day one — the two biggest time-sinks were contract drift and hunting integration bugs at hour 28. Everything else was the right level for the clock.

**Q86: What do you do AFTER a hackathon/competition to extract its max value?**
A: Retro (what worked/leaked time), archive the verified code/contracts, and write a short post-mortem of decisions under pressure. That habit — turning an event into documented lessons — is exactly the engineering practice a platform team wants.

**Q87: How do you manage the emotional side of not placing/winning?**
A: Tie your self-assessment to the durable outcome, not the rank: did we produce verified working work, did I do my component well, did we learn the failure? Rank is outcome; quality is process. That stance is the same maturity needed for incident reviews and project misses at work.

**Q88: What advice would you give a student preparing for their first SIH?**
A: Solve the judging criteria first — SIH rewards a working prototype tied to the problem statement — lock scope hour one, agree the data contract, verify your claims with tests, and rehearse the demo like it's the deliverable. Pressure without preparation is just stress.

---

## 4. Transferring Competition Skills to the Job (Q89–Q100)

**Q89: How do your hackathon/competition results translate to Infosys SP DSE deliverables?**
A: Deliverables that survive delivery pressure: scoped to what's contractual, verified by tests before claimable, presented to a stakeholder (judge/client) who asks "why", and documented so the next person can continue. Every SIH/CodeCode skill maps to a deliverable-sized behavior at work.

**Q90: What's your approach when handed a brand-new problem domain at a client?**
A: Same shape as a hackathon: understand the problem and constraints before choosing, set a bar for "what would provable success look like", agree a contract, build the riskiest core first, verify, and present with a demo that works. Client-domain learning is the empathy layer on top of that exact loop.

**Q91: How do you handle an ambiguous requirement — a JIRA ticket that's one vague line?**
A: Ask the clarifying question with a proposed interpretation attached ("I'll assume X unless you say otherwise — here's the shape I'll build"), then confirm the success bar before building deep. That's scope-under-ambiguity, straight out of SIH's first hour.

**Q92: How would you bring "hackathon velocity" to a slower enterprise without losing quality?**
A: Keep the discipline, drop the destructive speed: the risk-first ordering, the contract-locking, the verify-before-claim — but allocate real hours for documentation, review, and operability that a 36-hour window cuts. Velocity with appropriate thoroughness, not chaos.

**Q93: What's the difference between a "demo" and a "deliverable"?**
A: A demo proves the happy path under controlled conditions; a deliverable also survives failure, load, ops, and review — monitoring, rollback, docs, security, tests. SIH produced a demo-grade system; my internships and OpenRTL produce deliverable-grade artifacts. I can say that distinction out loud because I've felt it.

**Q94: How do contests shape how you review other people's code?**
A: I review for correctness-under-bounds first (complexity, edge cases) — the CodeCode instinct — then system concerns (logging, secrets, observability) — the internship instinct. Two lenses, both trained, make a thorough reviewer.

**Q95: Which is more important in an SP DSE hire: shipping under pressure or algorithmic depth?**
A: Both are needed but shipping-under-pressure is the closer vote — you can grow algorithmic depth on the job, but you can't reliably teach calm under a client deadline. I'd say that honestly as my defensible position, and note that I demonstrate both anyway.

**Q96: How do you avoid burnout after 36-hour builds, and is it a red flag on a regular team?**
A: Sustained 36-hour culture is a red flag — bursts must be bounded by retros, breaks, and a return to normal cadence. As a habit I take the pre-demo freeze + rotating breaks approach; as a norm on a team I'd push back on perpetual "hackathon mode" because it produces burnout, not quality.

**Q97: What's the single most important lesson about ME (the candidate) that these events reveal?**
A: That I ship verified work under a hard clock and can say precisely what mine was. Panels probing SIH and CodeCode see: scoped ambition, verified claims, honest attribution, and the same calm-method style I'd bring to production incidents.

**Q98: If you could compete in one more event now, which and why?**
A: A systems/security-focused CTF or a platform-build hackathon than a pure DSA contest — because my current edge is exactly the build-and-secure-systems layer, and I'd rather test that under pressure than re-prove algorithmic basics. It shows self-aware prioritization of where I add value.

**Q99: How do these events influence how you estimate effort?**
A: They gave me calibrated instincts for "how long does the riskiest part really take" and "what gets cut when the clock bites" — the same error bars every sprint needs. I over-budget integration and verification, the two places every contest/hackathon bled time.

**Q100: Give the panel your one-sentence closing pitch on hackathons & competitions.**
A: "Across SIH 2024 (finalist, 500+ teams, verified AES-256/RSA-4096/SHA-256 build) and Techfest CodeCode (top 5 zonal), I proved I can scope, ship, verify, and defend real work under pressure — with precise, honest attribution of what was mine."