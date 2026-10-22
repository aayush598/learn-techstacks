# Scenario Archetype Playbook

> Section 2 · English & L&D · Behavioural & Scenario-Based ·  _Estimated reading time: 8 min_
> **Prerequisite:** [The Infosys-professional response framework](../01-concepts/02-infosys-professional-response-framework.md)

## In one sentence
**Twelve scenario archetypes cover essentially every behavioural item in the section — learn the trigger words, the correct recipient, and the answer shape for each and you can answer anything in this sub-type.**

## Why the pre-test tests this

- The stems are recycled across batches and across companies. The *situation* changes; the *shape* of the good
  answer does not.
- This page is the one to print or bookmark. It turns a 90-second read of an unfamiliar stem into a lookup.
- Karthik's retrospective advice, in one line: "the scenarios repeat; the answers are template-shaped."

## Core concept

### The 12 archetypes — quick reference

| # | Archetype | Trigger words you will see | First recipient | Answer shape (one line) | Typical distractor |
|---|-----------|---------------------------|-----------------|-------------------------|--------------------|
| 1 | Missed deadline | "behind schedule", "cannot finish", "delay" | Team lead | Quantify gap → inform early → 2 options (scope or date) → daily track | "Work over the weekend silently" |
| 2 | Credit taken | "took my credit", "presented my work" | The colleague, privately | Evidence → private ask to correct → then escalate in writing | "Reply-all to the team" |
| 3 | Disagreement with manager | "I believe this is wrong", "I disagree" | Your manager | Written rationale + data → request review → commit if it stands | "Send the data to the client" |
| 4 | Angry customer | "client is upset", "escalating complaint" | CRM via your lead | Listen fully → acknowledge impact → confirm what is known → commit to a time | "Apologise and agree to anything" |
| 5 | Bug before release | "critical defect", "found in testing" | Module owner + delivery manager | Quantify impact → inform → propose fix/release options → log → verify | "Fix it yourself and say nothing" |
| 6 | Overloaded | "too many tasks", "cannot manage" | Team lead | Task list with effort → flag the collision → ask for priority order | "Accept everything, work late" |
| 7 | Team conflict | "argument with a teammate", "friction" | The colleague first, then lead | Private, task-focused conversation → agree a split → involve lead as facilitator | "Raise it in front of the team" |
| 8 | Teammate's mistake | "he broke the build", "the config was wrong" | Contain first, then lead | Contain impact → help fix → report risk via channel → prevent | "Tell the client who caused it" |
| 9 | Your own mistake | "I missed the deadline", "I sent it wrong" | The affected person, immediately | Own → state impact → propose recovery → verify | "Explain that it was not your fault" |
| 10 | Unclear requirement | "ambiguous", "not clear what is needed" | The requester (BA/client) | Ask in writing → record the agreed interpretation → flag timeline risk | "Make a reasonable assumption and proceed" |
| 11 | Ethics / policy conflict | "asked to bypass", "against the policy" | The person asking, then the policy owner | Refuse the act → cite the policy → offer a compliant alternative → escalate if pressed | "Do it because it is the client" / "refuse and resign" |
| 12 | Unknown technology | "never used this", "no idea how" | Your lead / a senior engineer | Acknowledge the gap → ask for reference → propose a scoped task → pair up → set a check-in | "Say yes and start anyway" |

### The recipient rule

| Impact level | Recipient | Timing |
|--------------|-----------|--------|
| Your own task | Team lead | Same day |
| Sprint / release slipping | Delivery or project manager | Within hours |
| Client-visible | CRM, through your lead | Same day |
| HR / personal | HR / your manager | As soon as possible |
| Security, data, legal | Security / management | Immediately, no delay |

### The escalation-ladder in one line

```
private person → my team lead → delivery manager → CRM → (HR / top management only as a last resort)
```

### Pattern language that marks the professional option

| Category | Phrases |
|----------|---------|
| Ownership | take ownership, ensure it is resolved, drive to closure, I will handle |
| Early comms | inform immediately, share early, flag it now, raise it promptly |
| Right level | inform my manager, escalate appropriately, discuss with the delivery manager |
| Evidence | with the impact analysis, along with the test evidence, documented in writing, in the tracker |
| Plan | propose two options, suggest a revised date, agree a recovery plan, with a fallback |
| Closure | follow up, confirm the fix, track it to closure, verify before the demo |

### The 5-scenario self-check

Before committing to an option, verify:

- [ ] It names a role.
- [ ] It contains a work verb.
- [ ] It stays inside the escalation ladder.
- [ ] It contains no blame words and no threat.
- [ ] It has a closure clause or a plan.

## Worked example

> **Q.** You are reviewing a colleague's module before it goes to production and you find that its error handling
> swallows exceptions, which will hide failures. The release is in 4 hours. The author is in a client meeting.
>
> A. Message the author with the specific finding and a suggested fix, and copy the team lead so the release
>    decision can be made in time.
> B. Change the error handling yourself, since the release is too close for a discussion.
> C. Leave the code as it is; it is the author's design decision and it already works in the happy path.
> D. Raise a defect so that it is documented, and mention it in the next stand-up.

**Answer: A**

| Archetype | Bug before release → recipient: module owner + team lead |
|-----------|--------------------------------------------------------------|
| A | ✅ Correct — specific finding + suggested fix + copied the accountable decision-maker before the deadline. |
| B | Unilateral edit of someone else's code 4 hours before production, no review, no record. Process violation. |
| C | Passive — knowingly ships a defect and hides it. Also not a "design decision": swallowing exceptions is a defect, not a preference. |
| D | Under-escalating — a documented defect with no owner notified and no release decision triggered 4 hours before release. It also frames a fixable finding as something for a future meeting. |

**Note:** A copies the team lead *with a specific finding and a suggested fix*. Copying is not automatically
over-escalation — copying the person who must make a time-critical decision, with useful content attached, is
correct.

## Quick rules

- Look up the trigger word, not the story. The story is decoration.
- The archetype gives you the recipient. Get the recipient right and the option falls out.
- Two options with the right recipient: the one with a plan wins.
- Two options with a plan: the one with evidence wins.
- Everything else: the one with the most proportionate timing wins.
- Print this page if you print nothing else from this topic.

## Common traps

- **Memorising the story instead of the shape.** Batch 1's scenario is not batch 2's scenario, but the shape for
  "bug before release" is identical.
- **Assuming the correct answer always escalates highest.** It escalates **proportionately**.
- **Skipping the recipient step** and choosing based on how professional the option sounds. Sound is not structure.
- **Using "escalate appropriately" as a substitute for knowing to whom.** In the actual options, "appropriately"
  is accompanied by the right role.

## Checklist

- [ ] I identified the archetype from the trigger words.
- [ ] I checked the correct first recipient for that archetype.
- [ ] I applied the recipient + plan + evidence tie-breakers.
- [ ] I ran the 5-scenario self-check on my answer.
- [ ] This page is bookmarked or printed for the night before the test.

## Related

- [The four-option answer scheme](../01-concepts/01-the-four-option-answer-scheme.md)
- [The Infosys-professional response framework](../01-concepts/02-infosys-professional-response-framework.md)
- [Answer template bank](02-answer-template-bank.md)
- [The almost-right option](../04-pitfalls/01-the-almost-right-option.md)
- [Behavioural topic README](../README.md)
