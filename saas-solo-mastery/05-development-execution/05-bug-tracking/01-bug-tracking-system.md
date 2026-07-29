# Bug Tracking for Solo Founders

## Why Bug Tracking Matters (Even For One Person)

When you're the only developer, bugs don't disappear just because you didn't write them down. In fact, without a system, bugs multiply:

1. User reports a bug in email
2. You respond "I'll look into it"
3. You get distracted by something urgent
4. The bug is forgotten
5. User churns

A bug tracking system prevents this. It's not about bureaucracy—it's about making sure every bug gets the attention it deserves and nothing falls through the cracks.

---

## 1. The Solo Bug Tracking Philosophy

### The Minimum Viable Bug Tracker

Your bug tracker needs to do exactly 3 things:
1. **Capture**: Write down the bug before you forget
2. **Prioritize**: Decide if/when to fix it
3. **Track**: Know what's been fixed and what hasn't

That's it. You don't need workflows, statuses, custom fields, or automations.

### Bug Tracker = To-Do List for Problems

Think of your bug tracker as a to-do list, not a database. The simpler, the better.

### The Golden Rule

**Every bug gets tracked.** No exceptions. Even the tiny ones. Even the ones you think you'll remember. Write. It. Down.

---

## 2. Choosing a Bug Tracking Tool

### Tools for Solo

| Tool | Cost | Best For | Notes |
|------|------|----------|-------|
| **GitHub Issues** | Free | Developers | Integrated with code |
| **Linear** | Free | Fast workflow | Keyboard-driven |
| **Notion** | Free | All-in-one | Flexible but slower |
| **Todoist** | Free/Paid | Simple lists | Minimal |
| **Plane** | Free | Open-source | Self-hostable |
| **Paper trail (email)** | Free | Minimalists | Search your inbox |

### Recommended: GitHub Issues

For most solo founders, GitHub Issues is the best choice:
- Free
- Integrated with your code
- Links to commits and PRs
- Simple markdown
- Labels for prioritization
- Everyone expects it

### Setting Up GitHub Issues

```
Repository → Issues → Labels → Milestones → Projects
```

**Labels**:
```
bug (critical)
bug (high)
bug (medium)
bug (low)
user-reported
internal
```

**Milestones**:
```
v2.0 (current sprint)
v2.1 (next sprint)
v3.0 (future)
backlog
```

---

## 3. The Triage Process

### What Is Triage

Triage is the process of evaluating each bug and deciding:
- How bad is it? (severity)
- How many users does it affect? (scope)
- How hard is it to fix? (effort)
- Should we fix it now? (priority)

### The SOLO Triage Framework

**Step 1: Capture the bug**
Get it into the tracker immediately. One line is enough.

**Step 2: Reproduce**
Can you make the bug happen? If yes, document the steps. If no, note "could not reproduce."

**Step 3: Categorize**
- **P0 - Critical**: All users affected, data loss, security, payment broken
- **P1 - High**: Core feature broken for many users
- **P2 - Medium**: Feature broken for some users, workaround exists
- **P3 - Low**: Minor issue, cosmetic, edge case
- **P4 - Wishlist**: Enhancement, not a bug

**Step 4: Schedule**
- **P0**: Fix NOW. Drop everything.
- **P1**: Fix within 24 hours.
- **P2**: Fix this sprint.
- **P3**: Fix when you have time.
- **P4**: Add to "someday" list.

### The Triage Timebox

Don't spend more than 5 minutes per bug in triage:
- 1 minute: Read the report
- 1 minute: Try to reproduce
- 1 minute: Categorize
- 2 minutes: Write clear steps

---

## 4. The Bug Report Template

### Minimum Viable Bug Report

```markdown
## Bug: [Brief title]

**Environment**: 
- Browser: Chrome 120 / Firefox 121
- OS: macOS 14
- Account: user@example.com

**Steps to reproduce**:
1. Go to /dashboard
2. Click "Create Project"
3. Fill in name "Test"
4. Click "Save"

**Expected**: Project is created and appears in list
**Actual**: Nothing happens, no error shown

**Severity**: P2 (Medium)
**Frequency**: Every time
**Reported by**: user@example.com
```

### What Makes a Good Bug Report

A good bug report answers:
1. **What did you do?** (steps to reproduce)
2. **What did you expect to happen?** (expected behavior)
3. **What actually happened?** (actual behavior)
4. **What environment?** (browser, OS, account)
5. **How often does it happen?** (frequency)
6. **How bad is it?** (impact)

### The User-Facing Bug Report Form

If users report bugs through a form:

```markdown
# Report a Bug

**What were you trying to do?**
[text area]

**What happened instead?**
[text area]

**What browser/device are you using?**
[dropdown: Chrome, Firefox, Safari, Edge]
[dropdown: Windows, Mac, iOS, Android]

**Can you provide a screenshot?**
[file upload]

**Your email (optional, for follow-up):**
[email]
```

---

## 5. Bug Priority in Practice

### The Priority Matrix

| | Many Users | Few Users |
|--|------------|-----------|
| **Critical** | P0: Fix NOW | P1: Fix today |
| **High** | P1: Fix within 24h | P2: This sprint |
| **Medium** | P2: This sprint | P3: When you can |
| **Low** | P3: When you can | P4: Maybe never |

### Examples

```
P0: Payment not processing — Users can't pay. Drop everything.
P0: Data loss — Users losing their work. Drop everything.
P1: Login broken — All new users affected. Fix today.
P1: Dashboard not loading — Core feature broken. Fix today.
P2: Export fails in Safari — Some users affected. This sprint.
P2: Search returns wrong results — Many users, workaround. This sprint.
P3: Button color wrong on mobile — Cosmetic. When you have time.
P3: Typo on settings page — Minor. When you have time.
P4: "Would be nice if dashboard had charts" — Not a bug. Backlog.
```

### The 5-Bug Rule

Never have more than 5 open P0/P1 bugs. If you do:
1. Fix them before doing anything else
2. Once fixed, investigate why so many critical bugs occurred
3. Add prevention measures (tests, better review, more monitoring)

---

## 6. User-Reported Bugs

### Collecting Bugs from Users

**In-app bug report button**:
```html
<button class="fixed bottom-4 right-4 bg-red-500 text-white p-3 rounded-full shadow-lg"
        onclick="reportBug()">
  Report Bug
</button>
```

**Support email**: bugs@yourproduct.com → auto-creates GitHub issue

**In-app feedback widget**: 
- Canny, Featurebase, or custom
- Users can report bugs without leaving the app

### Responding to User Bug Reports

**Acknowledgment (immediate)**:
"Thanks for reporting this! I've logged it as #123 and will investigate."

**Follow-up (within 24 hours)**:
"I've reproduced the issue and identified the cause. Fix coming in the next deploy."

**Resolution (when fixed)**:
"This is now fixed in production. Thanks again for your help!"

### What Users Want

Users don't care about your bug tracking system. They care about:
1. Being heard (acknowledge their report)
2. Knowing it's being worked on (status update)
3. Knowing it's fixed (resolution notification)

---

## 7. The Bug Fix Workflow

### The Solo Bug Fix Cycle

```
Bug reported → Triage → Reproduce → Fix → Test → Deploy → Verify → Close
  (5 min)    (5 min)  (varies)  (varies)  (5 min) (5 min) (5 min) (1 min)
```

### P0 Bug Protocol

When a P0 bug is reported:

1. **Acknowledge**: "I'm aware and working on it" (immediate)
2. **Assess scope**: How many users affected? Data loss?
3. **Decide**: Fix forward or rollback?
4. **Fix**: Don't make it perfect, make it not broken
5. **Deploy**: Bypass normal process if needed
6. **Monitor**: Watch error rates drop
7. **Post-mortem**: Why did this happen? How to prevent?

### P1 Bug Protocol

1. **Acknowledge**: Within 4 hours during business days
2. **Schedule**: Fix within 24 hours
3. **Workaround**: If possible, provide a workaround
4. **Fix**: Normal process
5. **Deploy**: Next deploy cycle (or ASAP if severe)

### P2-P4 Bug Protocol

1. **Acknowledge**: Within 24 hours
2. **Triage**: Categorize and prioritize
3. **Schedule**: When it fits in the roadmap
4. **Fix**: Normal process
5. **Deploy**: Normal cycle

---

## 8. The Bug Tracker Dashboard

### What to Track

**Open bugs**:
```
P0: 0
P1: 2
P2: 5
P3: 12
P4: 23
Total: 42
```

**Bug trends**:
```
This week: 3 new bugs, 2 fixed
Last week: 5 new bugs, 4 fixed
Trend: Bugs decreasing 📉
```

**Bug age**:
```
Average time to fix: 2.3 days
Oldest open bug: 14 days (P3)
```

### The Weekly Bug Review

Every Friday (15 minutes):

1. Review all new bugs this week
2. Check if any P0/P1 bugs are open
3. Re-prioritize if needed
4. Close bugs that are fixed
5. Check if any patterns emerge

### Bug Metrics That Matter

| Metric | Target | Why |
|--------|--------|-----|
| Open P0/P1 | 0 | Critical issues should never be open |
| Time to fix (P0) | < 2 hours | Minimize user impact |
| Time to fix (P1) | < 24 hours | Keep users happy |
| Bugs found in production | Trending down | Quality improving |
| Bug report → Acknowledged | < 4 hours | Users feel heard |

---

## 9. Preventing Bugs

### Root Cause Analysis

For every P0 bug (and interesting P1s), ask:
1. What was the root cause?
2. Why wasn't it caught?
3. What can we do to prevent it?
4. What can we do to detect it earlier?

### The Bug Prevention Checklist

After fixing a bug:
- [ ] Write a test that would have caught this bug
- [ ] Add monitoring to detect this type of issue
- [ ] Check if similar bugs exist in other parts of the code
- [ ] Update documentation if needed

### Common Bug Causes in Solo SaaS

| Cause | Prevention |
|-------|------------|
| TypeScript errors not caught | Run `tsc --noEmit` before every deploy |
| Edge cases in forms | Add form validation library (Zod) |
| API response not handled | Use error boundaries, handle all HTTP status codes |
| Browser-specific issues | Test in Chrome + Safari at minimum |
| Race conditions | Fix with proper state management |
| Missing error states | Design empty, error, loading states for every component |
| Database migration issues | Test migrations against production-like data |

---

## 10. Bug Tracking Anti-Patterns

### Anti-Pattern 1: No Bug Tracker

"I'll just remember the bugs. There aren't that many."

**Reality**: You forget. Users get frustrated. Bugs multiply.

**Fix**: Use a simple tracker. GitHub Issues. Setup time: 2 minutes.

### Anti-Pattern 2: Over-Engineering

Custom fields, workflows, automations, SLAs, escalation policies.

**Reality**: You're one person. You don't need enterprise bug tracking.

**Fix**: Labels + priorities + simple board. That's it.

### Anti-Pattern 3: Bug Shame

"I shipped a bug. I must be a bad developer."

**Reality**: Every SaaS has bugs. It's inevitable. What matters is how quickly you fix them.

**Fix**: Accept bugs as normal. Focus on fixing them, not feeling bad about them.

### Anti-Pattern 4: Not Reproducing

"I'll just fix this without checking if I can reproduce it."

**Reality**: You spend 2 hours fixing a bug that doesn't exist, or miss the actual cause.

**Fix**: Always reproduce (or confirm you can't reproduce) before fixing.

### Anti-Pattern 5: P0 Overload

"Everything is P0!"

**Reality**: If everything is critical, nothing is critical.

**Fix**: Use the severity × frequency matrix. Be honest about what's actually critical.

---

## 11. The Bug Tracking Workflow

### Daily

- [ ] Check for new bug reports (2 min)
- [ ] Triage any new bugs (5 min)
- [ ] Fix any P0/P1 bugs (drop everything)

### Weekly

- [ ] Review all open bugs (10 min)
- [ ] Re-prioritize if needed (5 min)
- [ ] Close resolved bugs (2 min)
- [ ] Check bug trends (3 min)

### Monthly

- [ ] Full bug tracker cleanup (15 min)
- [ ] Review bug patterns (10 min)
- [ ] Update prevention measures (15 min)
- [ ] Archive old resolved bugs (5 min)

---

## 12. Bug Tracker Hygiene

### Closing Bugs

Close a bug when:
- The fix is verified in production
- You confirmed the fix works
- The user confirmed the fix (if user-reported)

### Reopening Bugs

Reopen a bug when:
- The fix didn't actually work
- The same issue occurs in a different context
- A regression occurs

### Archiving Bugs

Archive (not delete) bugs that are:
- Older than 6 months with no action
- Duplicates (link to the original)
- "Won't fix" decisions
- No longer relevant (feature removed)

### The "Won't Fix" Decision

Some bugs won't be fixed. Document why:
- Too risky to fix
- Feature is being removed anyway
- Only affects 1 user with a workaround
- Would require major architectural change

---

## 13. Tools Recommendation

### The Solo Bug Tracking Stack

**Phase 1: Getting Started**
- **GitHub Issues**: Free, integrated with code
- Labels: P0-P4, user-reported
- No milestones, no projects
- Setup time: 5 minutes

**Phase 2: Growth (100+ users)**
- **Linear**: Fast bug tracking
- **Canny**: User-facing feature requests + bug reports
- **Sentry**: Automatic bug reports from errors
- Weekly bug review

**Phase 3: Scale (1000+ users)**
- **Linear or Jira**: More structured tracking
- **Status page**: Communicate known issues
- **Bug bash**: Periodic focused bug fixing
- SLA tracking

---

## 14. The Bug Tracking Manifesto

1. **Every bug gets tracked** — No exceptions
2. **Triage within 24 hours** — Don't let bugs sit unclassified
3. **P0 means DROP EVERYTHING** — Nothing is more important
4. **Reproduce before fixing** — Don't guess at the problem
5. **Write a test after fixing** — Never fix the same bug twice
6. **Close bugs when verified** — Not when deployed, when verified
7. **Users deserve responses** — Acknowledge all bug reports
8. **Prioritize, don't ignore** — Low priority doesn't mean forgotten
9. **Track trends** — Are bugs increasing or decreasing?
10. **Simple is better** — Labels + priorities > custom workflows

Bug tracking isn't bureaucracy. It's a promise to your users that their problems won't be forgotten. A simple system with 100% capture is infinitely better than a complex system with 50% capture.
