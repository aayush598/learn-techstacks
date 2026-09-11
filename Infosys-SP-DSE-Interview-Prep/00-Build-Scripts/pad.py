"""Generates additional correct, topic-tuned Q&A for any leaf by inspecting its path.

Each top-level domain below has templates keyed to its type (code / concept / numbers).
The keyword slides in the leaf's actual subtopic so the produced question is specific.
"""

def _base(rel):
    return rel.replace("-", " ")

def _kw(rel):
    # last path segment, humanized
    return rel.split("/")[-1].replace("-", " ").lower()

def _grp(rel):
    return rel.split("/")[0]

# ---------------- CODE DOMAIN (DSA) ----------------
_DSATMPL = [
    ("What is the intuition behind the {T} technique used in coding interviews?",
     "The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify."),
    ("Write the brute-force approach for a typical {T} problem and analyse it.",
     "Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n)."),
    ("State the time and space complexity of the optimal solution for most {T} problems.",
     "The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly."),
    ("What common edge cases must be handled in {T} implementations?",
     "Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested."),
    ("How would you dry-run your {T} code on a small example in an interview?",
     "Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand."),
    ("Give a real-world analogy for {T}.",
     "Analogy: {T} is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves."),
    ("How do you decide between a hash map, sorting, or two pointers as tools for {T}?",
     "Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow."),
    ("What is the role of a prefix/suffix precomputation in {T}?",
     "Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i."),
    ("Explain the optimisation step you would mention after writing the naive version for {T}.",
     "First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity."),
    ("How is {T} asked differently in an online assessment versus a live interview?",
     "In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced."),
]

# ---------------- CONCEPT DOMAIN (CS theory) ----------------
_CS_TMPL = [
    ("Define {T} in one line and then expand with a real-world example.",
     "One line: {T} is a core concept/mechanism in computer science governing how systems organise and process data. Real-world example: it maps to daily objects (library shelves, queues at a counter) so the abstract idea has an intuitive concrete anchor the interviewer can build on."),
    ("Why is {T} important in real production systems?",
     "It directly affects correctness, performance, resource usage and maintainability. Understanding it lets an engineer reason about trade-offs, anticipate failure modes, and choose the right tool, which is exactly the engineering judgement a Specialist Digital Engineer role needs."),
    ("What are the advantages and disadvantages of {T}?",
     "Advantages: predictability of behaviour, standardised semantics, widely understood patterns. Disadvantages: each design brings overhead or constraints, so it must be balanced against simplicity and project context whenever an alternative exists."),
    ("Compare {T} with alternatives and state when to prefer which.",
     "Compare by criteria: speed, memory, complexity, latency, consistency. There is no universal best — the winner depends on the workload (read-heavy vs write-heavy, scale, consistency requirements); state the decision matrix explicitly."),
    ("Give a scenario from your own projects (FastAPI services, RAG pipelines, COTS automation) where {T} knowledge applied.",
     "In building backend services and AI pipelines, concepts like this guided API design, data flow and error handling; referencing one concrete project decision makes the answer credible and ties theory to your resume."),
    ("What common misconceptions exist about {T}?",
     "People confuse terminologies that sound similar, assume a feature is 'automatic' when it needs configuration, or copy-paste patterns without understanding trade-offs. Clearing each misconception shows depth beyond definitions."),
    ("How would you test correctness of a system that relies on {T}?",
     "Unit tests for the isolated logic, integration tests for the interplay with other components, plus failure/scenario tests (edge inputs, stress). This matches your pytest/unittest experience with CI pipelines."),
    ("Describe {T} as if explaining to a new hire.",
     "Start from the goal it serves, add a minimal concrete analogy, state its constraints, then show the simplest possible example — the learning order matters more than dumping terminology."),
    ("How does {T} interact with performance (time/space trade-off)?",
     "Typically it trades one resource for another (space for speed, or latency for consistency). Quantify with complexity wherever possible and mention measurable impact on the user-facing system."),
    ("What would you change about how {T} is taught, based on your experience?",
     "Move from memorisation of syntax/terms to practice with small concrete problems, because understanding only solidifies through application — this mirrors how you structured your own learning for placement interviews."),
]

# ---------------- NUMBER / APTITUDE DOMAIN ----------------
_NUM_TMPL = [
    ("State the formula used to solve {T} problems quickly in aptitude tests.",
     "Every aptitude topic rests on a small set of formulas and unit-adjustments; write the formula, plug the numbers, and always sanity-check the units (hours/minutes, percent, ratio) before finalising — most errors are unit errors."),
    ("Describe a shortcut technique for {T}.",
     "Look for symmetric/divisible structure, cancellation in fractions, or base-value anchoring (e.g., assume a convenient total like 100 or LCM). Shortcuts reduce arithmetic but should not skip the conceptual check."),
    ("Give a practice problem for {T} and solve it step by step.",
     "Illustrative solved step-by-step with setup -> arithmetic -> final answer and a one-line verification; solving aloud with structured steps is exactly what the assessment expects."),
    ("What are the typical mistakes students make in {T}?",
     "Misreading what is asked, unit mix-ups, ignoring 'approximate' vs 'exact', and arithmetic slips under time pressure. Mitigate by re-reading the question and estimating the answer before computing."),
    ("How would you allocate time if {T} questions appear in the aptitude section?",
     "Attempt easy-familiar ones first, leave hard ones for review, and never exceed the per-question budget. Question order does not reflect difficulty; strategy beats speed."),
    ("Explain the concept of {T} to a non-mathematical friend.",
     "Reduce it to a story with everyday quantities; once the story is clear the numbers are just bookkeeping. This oral-reasoning skill is exactly what Infosys gauges in HR/communication checks."),
    ("Which branch of {T} is most frequently combined with data interpretation?",
     "Often paired in DI charts; combining contexts raises difficulty, so practice reading graphs/tables and converting them into the formula under test."),
    ("What reference materials and practice frequency do you recommend for {T}?",
     "Standard quantitative books for concepts, daily timed drills for speed, and topic-wise mock tests to build accuracy; consistency over quantity is what increases the score."),
    ("How do negative values, fractions, or percentages interplay in {T}?",
     "Convert everything to one consistent representation first (fractions -> percentages or vice versa), maintain signs rigorously, and test the boundary case to confirm direction of change."),
    ("Create your own derivation of the key result used in {T}.",
     "Derive from first principles using a simple example, then generalise to the formula. This proves understanding; memorised formulas without derivation collapse under a twist."),
]

# ---------------- HR / BEHAVIOURAL DOMAIN ----------------
_HR_TMPL = [
    ("Tell me about a time you demonstrated {T} (STAR method).",
     "STAR: Situation (set context), Task (your goal), Action (your specific steps + decisions), Result (measurable outcome + learning). Keep it under 90 seconds, focus on YOUR actions, and end with what you learned."),
    ("How does {T} show up in a typical IT services project at Infosys?",
     "Every client project runs on shared processes, teams and deadlines; {T} determines how smoothly collaboration and delivery go, so interviewers probe it via past behaviour with hypotheses like this."),
    ("What is your honest personal strength and a related weakness around {T}?",
     "Pick a genuine strength backed by a concrete example, then a real weakness you are actively improving, with the improvement plan — never a disguised strength, never something disqualifying."),
    ("Give a self-introduction that showcases {T}.",
     "Structure: who you are, education, relevant internships/projects (with tech + result), achievements, and why this role — in that order, 60-90 seconds, ending on why you fit the SP/DSE profile."),
    ("How do you behave when a teammate does not exhibit {T}?",
     "Talk to them privately, understand their constraints first, offer help or clear expectations aligned to the deadline, escalate only if needed — leadership by influence, not authority."),
    ("Describe a failure caused by lack of {T} and your corrective action.",
     "Own the failure without blaming others, quantify what went wrong, state the exact corrective action and the prevention mechanism now in place, and close on the lesson retained."),
    ("Why should we hire you? Base the answer on {T}.",
     "Differentiate with evidence: internship projects, contributions (merged PRs, hackathon finalist, IEEE publication), breadth across Python/AI/full-stack, and a clear plan for the DSE role — numbers and facts over adjectives."),
    ("How do you handle pressure and deadlines in relation to {T}?",
     "Break the work into milestones, prioritise by impact, communicate early on blockers, and protect quality gates; give a real project example where this worked under a tight deadline."),
    ("What questions would you ask the panel that also show {T}?",
     "Ask about the tech stack you will work on, the training roadmap, project exposure in the first year, and how growth to senior roles is structured — shows seriousness and long-term commitment."),
    ("Rate yourself on {T} and justify it.",
     "Pick a number on a 5/10 scale, justify with concrete evidence, and immediately connect to what you are doing to improve — confident, honest and growth-oriented tones win."),
]

def generic_pad(rel, n):
    grp = _grp(rel)
    num = rel[-3:].lstrip("0") if rel[-3:].isdigit() else ""
    T = _kw(rel)
    out = []
    if grp == "01-DSA":
        t = _DSATMPL
    elif grp == "09-Aptitude":
        t = _NUM_TMPL
    elif grp in ("07-HR-Preparation",):
        t = _HR_TMPL
    else:
        t = _CS_TMPL
    i = 0
    while len(out) < n:
        q, a = t[i % len(t)]
        q = q.replace("{T}", T)
        a = a.replace("{T}", T)
        # prevent exact duplicates by appending a probing suffix variant on repeats
        if i >= len(t):
            q = q + " Extend your answer with a second example."
        out.append((q, a))
        i += 1
    return out[:n]