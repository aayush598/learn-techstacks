# Solved Scenarios — Part 1

> Section 2 · English & L&D · Behavioural & Scenario-Based ·  _Estimated reading time: 10 min_
> **Prerequisite:** [The 90-second scenario procedure](../02-techniques/01-the-90-second-scenario-procedure.md)

## In one sentence
**Five fully solved behavioural questions — missed deadline, credit stealing, angry customer, bug before release, and overload — each with the archetype label and a reason for every rejected option.**

## Why the pre-test tests this

- These five archetypes alone account for the majority of behavioural items in reported batches.
- The reasoning below is deliberately mechanical: archetype label → ladder check → recipient + plan test. That is
  the same chain you run under the 90-second cap.
- Read the **distractor analysis**, not just the answer. Knowing *why* D is wrong is what stops you picking it
  on a different stem.

## Core concept

The four labels used throughout this file:

| Label | Archetype |
|-------|-----------|
| **P** | Passive — avoids, delays, hides |
| **A** | Aggressive — blames, confronts, threatens |
| **O** | Over-escalating — bypasses the line of reporting |
| **F** | Professional — owns, communicates early, right level, documents, follows up |

## Worked example

### Q1. The missed deadline

> **Q.** You are 3 days from a delivery deadline and you have completed only 60% of the assigned module. You are
> working alone and cannot make up the gap in the time available.
>
> A. Work through the weekend without telling anyone so the delivery is not affected.
> B. Inform your manager immediately that the module will be delayed, quantify what is complete and what is not,
>    and propose two options — reduce the scope of the release or move the date by two days.
> C. Raise a formal complaint that you were assigned an unrealistic amount of work.
> D. Wait until the day before the deadline to raise it, in case you find a way to finish.

**Answer: B**

**Reasoning:**

| Step | Finding |
|------|---------|
| Trigger | Deadline risk, archetype "missed deadline" |
| Labels | A = P, B = F, C = A, D = P |
| Ladder check on B | Informs own manager = Level 2 ✅ no skip |
| Recipient + plan | Recipient: manager ✅. Plan: two options ✅. Ownership language: "quantify" + "propose" ✅ |

**Why not A:** Working the weekend is a private fix for a systemic problem. If the module slips anyway, the team
planned around a date that was never achievable, and you removed the only chance to replan. It is also a
**fitness-for-duty** problem you created by yourself.

**Why not C:** The complaint is aimed at the wrong target. The work allocation may have been reasonable given
information you do not have. The professional move is to surface the constraint while you can still act on it.

**Why not D:** Waiting until the last minute converts a solvable scheduling problem into a delivery incident.
"Delay" is the least attractive option in the whole set.

---

### Q2. The colleague who takes credit

> **Q.** In the project review, your manager announces that Rahul completed the reconciliation module. You wrote
> 80% of it. Rahul is your teammate, not your friend.
>
> A. Say nothing. The work was completed and the client is happy; that is what matters.
> B. Schedule a one-to-one with Rahul, show him the commit history and the code you wrote, and ask him to
>    clarify the attribution with the team; if it does not change, put the facts in writing to your manager.
> C. Reply-all to the project mail asking everyone to check the git history before assigning credit.
> D. Wait for the next review and, if it happens again, tell your manager that Rahul is dishonest.

**Answer: B**

**Reasoning:**

| Step | Finding |
|------|---------|
| Trigger | Credit taking → archetype "credit" |
| Labels | A = P, B = F, C = A, D = A (deferred aggression) |
| Ladder check on B | Private conversation first (Level 1–2), manager only as a conditional step ✅ |

**Why not A:** The work being delivered does not make the attribution accurate. Misattributed work corrupces the
track record you will be assessed on, and it puts Rahul in a position he cannot defend.

**Why not C:** A public "check the git history" message is a public accusation with extra steps. It damages the
team, it puts you in the middle of a dispute, and it looks like score-settling.

**Why not D:** "Dishonest" is a character judgement about a colleague, and it is deferred to a future review
while the immediate problem goes unaddressed. Notice that D also inverts the ladder: it goes to the manager
before trying a direct conversation.

**Note the shape:** B escalates *conditionally* ("if it does not change"). That conditional structure is a
hallmark of correct options.

---

### Q3. The angry customer

> **Q.** A client calls about a data mismatch in the report delivered last week. The client is angry and
> interrupts you repeatedly. Your delivery manager is in another meeting for the next 30 minutes.
>
> A. Tell the client the data pipeline is handled by a different team and offer to connect them.
> B. Listen fully without interrupting, acknowledge the impact on their business, state clearly what you can
>    confirm and what you cannot yet confirm, and commit to a specific callback time with the root-cause
>    analysis; inform the delivery manager immediately afterwards.
> C. Apologise repeatedly and agree to whatever the client asks for so the call ends quickly.
> D. Tell the client that a report of this size always has small variations and the issue is not serious.

**Answer: B**

**Reasoning:**

| Step | Finding |
|------|---------|
| Trigger | Angry customer → archetype "angry customer" |
| Labels | A = P (passing the buck), B = F, C = A (inappropriate commitment), D = A (dismissing) |
| Framework on B | Listen ✅, acknowledge ✅, confirm accurately ✅, commit to a time ✅, inform the manager ✅ |

**Why not A:** Redirecting to another team without first understanding and owning the client's problem is
precisely what makes a complaint escalate. The client did not ask which team owns it.

**Why not C:** "Agree to whatever the client asks" is a commitment you may not be able to honour. On a
data-correctness issue, agreeing to a false conclusion creates a second incident. And repeated apology without
action reads as panic.

**Why not D:** Minimising the issue to the client is the fastest way to lose the account. "Not serious" is a
judgement about the client's operations that you are not qualified to make.

**Key idea:** the professional answer here contains **no promise about the outcome** — only a promise about the
*process* (a callback time). That distinction is what exam writers reward.

---

### Q4. The bug you find before release

> **Q.** During final testing you find a critical bug in a module that another developer wrote. The release is
> tomorrow. Your developer is on leave.
>
> A. Fix the bug yourself, do not mention it to anyone, and let the release proceed since the fix is in.
> B. Inform the delivery manager immediately with the defect details and the business impact, ask whether to
>    release with the defect or delay, and log the issue in the defect tracker either way.
> C. Send the bug details to your developer on leave and copy the entire project team so someone takes
>    responsibility.
> D. Delay the release on your own authority until the developer returns and fixes it.

**Answer: B**

**Reasoning:**

| Step | Finding |
|------|---------|
| Trigger | Bug before release → archetype "bug" |
| Labels | A = P, B = F, C = O (CC-all + chasing an absent person), D = A (acting unilaterally) |
| Ladder check on B | Level 3 (delivery manager) for a release-stopping issue ✅ correct level |

**Why not A:** Fixing it makes the bug disappear from your dashboard, not from the project's risk register. If
your fix is incomplete, the release goes out with a defect nobody tracked. Also: you modified another
developer's code without review — a process failure in itself.

**Why not C:** Copying the whole project team to chase a person on leave is over-escalation and creates noise. It
also does not get you a decision; it gets you a bigger audience. The right action is to get a decision from the
person accountable for the release.

**Why not D:** Delaying a release unilaterally is a decision above your authority and it hands you the blame for
a date you did not own. The professional version: "inform the delivery manager and ask whether to release or
delay" — you surface the decision, the accountable person makes it.

---

### Q5. You are overloaded

> **Q.** You have 4 assignments due this week. Two are from your team lead, one from another team, and one
> personal request from a peer who is a friend. Your team lead believes all three of his are top priority.
>
> A. Accept all four and work late every night this week, then tell your team lead on Friday that you could not
>    finish them all.
> B. List your assignments with effort and dependency information, tell your team lead that the three
>    deadlines collide, and ask him to prioritise; offer to renegotiate the peer's request once the priority
>    order is set.
> C. Complete the peer's request first because they asked most recently, and tell the others you were busy.
> D. Tell your team lead that the peer is not doing his own work and ask him to have a word with the peer.

**Answer: B**

**Reasoning:**

| Step | Finding |
|------|---------|
| Trigger | Overload → archetype "overloaded" |
| Labels | A = P (silent failure), B = F, C = A (arbitrary priority), D = A (blaming a third party) |
| Framework on B | Evidence (list + effort) ✅, early communication ✅, right recipient (team lead owns priorities) ✅, plan (renegotiate) ✅ |

**Why not A:** The heroics option. It converts a planning failure into a delivery failure, and you still burn
yourself out. The point of telling someone early is that telling them late has no value.

**Why not C:** "Most recently asked" is not a prioritisation rule at work. Prioritisation is a decision for the
person accountable for the work.

**Why not D:** You have escalated to the team lead on a matter that is yours to resolve. A peer asking for help is
not misconduct, and framing it as "not doing his own work" hands your manager a complaint you did not need to
make.

## Quick rules

- In all five questions, the professional option was the only one that **contained a plan**.
- Two of the five (Q1, Q5) punish silent effort; two (Q2, Q4) punish bypass; Q3 punishes over-promising.
- Note that the passive option is **not** always the same shape: it can be "work silently" (Q1), "say nothing"
  (Q2), "fix it yourself" (Q4), or "accept everything" (Q5).
- The professional option is always the one that **keeps the decision with the accountable person**.

## Common traps

- **Mistaking A in Q1 for F.** Working the weekend "solves" the problem for one person and for nobody else.
- **Mistaking A in Q4 for F.** "I fixed it" is a real action, but an unreviewed unilateral fix to someone else's
  code before a release is a process violation.
- **Choosing the option that resolves fastest** (Q1 weekend, Q4 self-fix) over the option that resolves safely.
- **Over-reading a friendly-sounding stem.** Rahul being "a teammate, not a friend" is a hint that the correct
  answer must be professional about Rahul, not warm about the friendship.

## Checklist

- [ ] I identified the archetype before reading the options.
- [ ] I checked whether the professional option contained a plan or merely an attitude.
- [ ] I verified the escalation level of my chosen option.
- [ ] I did not pick an option that made me look decisive but wrong.

## Related

- [Solved scenarios, part 2](02-solved-scenarios-part-2.md)
- [The four-option answer scheme](../01-concepts/01-the-four-option-answer-scheme.md)
- [The Infosys-professional response framework](../01-concepts/02-infosys-professional-response-framework.md)
- [The almost-right option](../04-pitfalls/01-the-almost-right-option.md)
- [Scenario archetype playbook](../05-reference/01-scenario-archetype-playbook.md)
- [Behavioural topic README](../README.md)
