# Heuristic Evaluation for Solo Founders

## What Is a Heuristic Evaluation?

A heuristic evaluation is a systematic inspection of a user interface against established usability principles ("heuristics"). Unlike user testing (which involves real users), a heuristic evaluation is done by you, the founder, acting as the usability expert.

For solo founders, heuristic evaluations are **gold**: they cost nothing but your time, they catch 70-80% of usability issues, and they can be done in a single focused session. When you can't afford a professional UX audit, a structured self-evaluation is the next best thing.

### Why This Matters for Solo Founders

- **No users needed**: Evaluate your product anytime, even before launch
- **Cheap**: Zero cost beyond your time
- **Fast**: A full evaluation takes 2-4 hours
- **Comprehensive**: Catches issues across all aspects of UX
- **Repeatable**: Run one every month to track improvement
- **Educational**: Makes you a better designer with each iteration

---

## 1. Nielsen's 10 Usability Heuristics

Jakob Nielsen's 10 heuristics are the industry standard. Each is a principle for creating usable interfaces. For each heuristic, I've included SaaS-specific examples and evaluation questions.

### Heuristic 1: Visibility of System Status

**Principle**: The system should always keep users informed about what's going on through appropriate feedback within reasonable time.

**SaaS examples**:
- Loading spinners when data is being fetched
- Progress bars during file uploads
- "Saving..." indicator when autosave triggers
- Breadcrumb showing current location in deep navigation
- "Email sent!" confirmation after sending a message

**Evaluation questions**:
- When the user performs an action, does something happen within 1 second?
- For longer operations, is there a progress indicator?
- Is there a way to see the current state (logged in/out, connected/disconnected)?
- Do status messages persist long enough to be read?
- Are notifications clear about what just happened?

**Common violations**:
- Clicking a button with no visual feedback
- Page loading without any progress indicator
- Form submission with no success/error message
- Background processes with no status indication

### Heuristic 2: Match Between System and the Real World

**Principle**: The system should speak the users' language, with words, phrases, and concepts familiar to the user, rather than system-oriented terms. Follow real-world conventions.

**SaaS examples**:
- "Shopping cart" instead of "order container"
- "Inbox" instead of "message queue"
- "Trash" instead of "deletion buffer"
- Calendar showing actual dates, not timestamps
- Natural language: "You have 3 unread messages" vs "Unread count: 3"

**Evaluation questions**:
- Does the UI use jargon or technical terms?
- Are icons and labels intuitive (trash = delete, + = add)?
- Do date/times use familiar formats?
- Are error messages in plain language?
- Does the information architecture match user mental models?

**Common violations**:
- Technical error codes (Error 0x2837AB)
- Internal terminology (SKU, CRUD, API endpoint)
- Unclear icons without labels
- Date formats that confuse international users

### Heuristic 3: User Control and Freedom

**Principle**: Users often choose system functions by mistake and will need a clearly marked "emergency exit" to leave the unwanted state without having to go through an extended dialogue.

**SaaS examples**:
- "Undo" for destructive actions (delete email, move item)
- Cancel button on multi-step processes
- "Edit" option after saving
- Back/forward navigation in wizards
- Easy account cancellation (not hidden in settings)

**Evaluation questions**:
- Can users undo mistakes?
- Is there a clear way to go back?
- Can users cancel a process in progress?
- Is there a confirmation dialog for destructive actions?
- Can users easily navigate back to a known state?

**Common violations**:
- No undo for accidental deletes
- One-way wizards with no back button
- Cancel hidden or hard to find
- Double-click submits a form twice
- No confirmation before sending

### Heuristic 4: Consistency and Standards

**Principle**: Users should not have to wonder whether different words, situations, or actions mean the same thing. Follow platform conventions.

**SaaS examples**:
- Same button style for same actions throughout
- Consistent navigation placement
- Standard keyboard shortcuts (Cmd+Z, Ctrl+S)
- Same terminology used everywhere (not "users" on one page and "members" on another)
- Consistent placement of actions (always save on the right)

**Evaluation questions**:
- Are similar elements displayed consistently?
- Do colors have consistent meaning (red = error, green = success)?
- Is the same terminology used consistently?
- Do patterns repeat across pages?
- Are platform conventions followed (buttons, links, inputs)?

**Common violations**:
- Different colors for the same type of button
- "Save" on one page, "Update" on another
- Inconsistent icon usage
- Mixing design patterns from different libraries
- Links that look like buttons and vice versa

### Heuristic 5: Error Prevention

**Principle**: Even better than good error messages is a careful design that prevents a problem from occurring in the first place.

**SaaS examples**:
- Confirm before deleting
- Gray out unavailable options
- Validate form fields on input (not on submit)
- Prevent double-submission of forms
- Warn before navigating away with unsaved changes

**Evaluation questions**:
- Are error-prone conditions eliminated or checked for?
- Are users asked to confirm before destructive actions?
- Are form fields validated before submission?
- Are constraints communicated upfront (file size limits, character limits)?
- Are optional/required fields clearly marked?

**Common violations**:
- No confirmation on delete
- Submit button clickable when form is invalid (with no feedback)
- Allowing duplicate submissions
- No character limits on text fields (causing silent truncation)
- Unclear constraints on file uploads

### Heuristic 6: Recognition Rather Than Recall

**Principle**: Minimize the user's memory load by making objects, actions, and options visible. The user should not have to remember information from one part of the dialogue to another.

**SaaS examples**:
- Recent files displayed on dashboard
- Autocomplete in search fields
- Visible navigation menu (not hidden behind hamburger)
- Recently used tools/options
- "Remember me" on login

**Evaluation questions**:
- Are navigation options visible at all times?
- Does the interface surface recently used items?
- Are there hints, autocomplete, or suggestions?
- Do users need to remember info from one step to the next?
- Is critical information displayed where it's needed?

**Common violations**:
- Deep navigation hierarchy with no breadcrumbs
- Search that requires exact phrasing
- Hidden navigation (hamburger menu with poor discovery)
- Requiring users to remember complex identifiers
- Info needed in one step only shown in a previous step

### Heuristic 7: Flexibility and Efficiency of Use

**Principle**: Accelerators — unseen by the novice user — may often speed up the interaction for the expert user such that the system can cater to both inexperienced and experienced users.

**SaaS examples**:
- Keyboard shortcuts
- Batch operations (select all, bulk edit)
- Customizable workflows/templates
- Saved filters and searches
- Power user features without overwhelming beginners

**Evaluation questions**:
- Are there shortcuts for frequent actions?
- Can users customize their experience?
- Are there advanced features for power users?
- Can users perform actions in bulk?
- Are frequently used features easily accessible?

**Common violations**:
- No keyboard shortcuts for repetitive tasks
- No bulk operations (each item requires separate action)
- One-size-fits-all interface with no customization
- Power-user features hidden or missing
- No way to save common configurations

### Heuristic 8: Aesthetic and Minimalist Design

**Principle**: Dialogues should not contain information that is irrelevant or rarely needed. Every extra unit of information in a dialogue competes with the relevant units of information and diminishes their relative visibility.

**SaaS examples**:
- Clean, uncluttered dashboard
- Progressive disclosure of advanced options
- Focused primary action per page
- White space used effectively
- Information hierarchy maintained (headings, sections)

**Evaluation questions**:
- Is every element on the page necessary?
- Is the most important content prominent?
- Is there unnecessary decoration or visual noise?
- Are complex tasks broken into manageable steps?
- Is the visual hierarchy clear?

**Common violations**:
- Dashboard with too many widgets
- Forms with too many fields
- Unnecessary decorative elements
- Walls of text with no visual hierarchy
- Features piled on without organization

### Heuristic 9: Help Users Recognize, Diagnose, and Recover from Errors

**Principle**: Error messages should be expressed in plain language (no codes), precisely indicate the problem, and constructively suggest a solution.

**SaaS examples**:
- "Invalid email format" (not "Error 400")
- "Password needs at least 8 characters and one number" (not "Invalid password")
- "Your session expired. Please log in again." (not "401")
- "This field is required" on specific empty fields
- Suggestive error recovery: "Did you mean...?"

**Evaluation questions**:
- Are error messages in plain language?
- Do errors explain what happened and how to fix it?
- Are errors presented right where they occurred?
- Is there a clear path to resolve the error?
- Are errors logged for the user to review later?

**Common violations**:
- "An error occurred" with no details
- Technical error messages (stack traces, SQL errors)
- Errors that disappear too quickly
- Generic "Please try again"
- Errors at the top of the page instead of near the field

### Heuristic 10: Help and Documentation

**Principle**: Even though it is better if the system can be used without documentation, it may be necessary to provide help and documentation.

**SaaS examples**:
- Contextual tooltips on complex fields
- "What's this?" links next to unfamiliar terms
- Searchable knowledge base
- Interactive onboarding tooltip sequence
- FAQ section for common questions

**Evaluation questions**:
- Are help resources easy to find?
- Is help contextually relevant?
- Is documentation searchable?
- Are help articles focused on tasks (not features)?
- Can users get help without leaving their current task?

**Common violations**:
- No help or tooltips anywhere
- Help that's just a PDF manual
- Outdated documentation
- Help that requires leaving the current workflow
- No search in documentation

---

## 2. SaaS-Specific Heuristics

In addition to Nielsen's 10, here are heuristics specific to SaaS products:

### SaaS Heuristic A: Time-to-Value

The product should deliver value within the first session, ideally within 5 minutes of signup.

**Evaluation questions**:
- Can a new user experience the core value in under 5 minutes?
- Is there a clear "first action" after signup?
- Is demo data pre-populated?
- Is the onboarding focused on the core action, not feature exploration?

### SaaS Heuristic B: Pricing Transparency

Pricing information should be easy to find, understand, and compare.

**Evaluation questions**:
- Can users find pricing without signing up?
- Are feature comparisons clear between plans?
- Is there a clear free trial or free tier?
- Are upgrade paths obvious from within the product?

### SaaS Heuristic C: Trust and Security

Users should feel their data is safe and their privacy is respected.

**Evaluation questions**:
- Are SSL/security badges visible?
- Is privacy policy clearly linked?
- Are data handling practices explained?
- Is there clear information about backups and uptime?

### SaaS Heuristic D: Export and Portability

Users should be able to export their data and cancel without friction.

**Evaluation questions**:
- Can users export their data?
- Is the export format useful (CSV, PDF, API)?
- Can users delete their account easily?
- Are there contracts or lock-in periods?

### SaaS Heuristic E: Notifications and Communication

Communication with users should be timely, relevant, and non-intrusive.

**Evaluation questions**:
- Are notification preferences easy to manage?
- Is in-app communication contextual and helpful?
- Are email notifications relevant and not excessive?
- Is there a clear way to mute/disable notifications?

---

## 3. Conducting a Heuristic Evaluation

### Preparation (30 min)

1. **Define scope**: Which part of the product are you evaluating? (Don't try to evaluate everything at once.)
2. **Create scenarios**: Define 3-5 realistic tasks users would perform
3. **Print or open the heuristics list**: Have it visible as you evaluate
4. **Set up recording**: Use Loom or QuickTime to record your screen and voice

### Evaluation Session (1-2 hours per evaluator)

**Step 1: Walk through each scenario**
Go through each task as if you're a user. For each step, note violations against the heuristics.

**Step 2: Go heuristic by heuristic**
After the scenarios, go through each heuristic systematically and look for violations you might have missed.

**Step 3: Rate each issue**

| Severity | Meaning | Action |
|----------|---------|--------|
| 0 | Not a usability issue | Ignore |
| 1 | Cosmetic issue only | Fix if time |
| 2 | Minor usability problem | Low priority |
| 3 | Major usability problem | High priority |
| 4 | Usability catastrophe | Fix immediately |

**Step 4: Document findings**
For each issue, record:
- Heuristic violated
- Location (page, component)
- Description of the issue
- Severity rating
- Screenshot or video
- Suggested fix

### The Evaluation Template

```
## Heuristic Evaluation Report

**Product**: 
**Evaluator**: 
**Date**: 
**Scope**: 
**Scenarios Evaluated**:

### Issues Found

#### Issue 1: [Title]
- **Location**: 
- **Heuristic Violated**: 
- **Description**: 
- **Severity**: [0-4]
- **Evidence**: [screenshot/video reference]
- **Suggested Fix**: 

### Severity Summary
- Catastrophes (4): 
- Major (3): 
- Minor (2): 
- Cosmetic (1): 
- Total: 

### Top 3 Recommendations
1. 
2. 
3. 
```

---

## 4. The Solo Evaluation Process

### Quick Weekly Check (30 min)

Every week, evaluate one flow or page:

1. Pick one part of your product (dashboard, settings, checkout)
2. List the 10 heuristics on a notepad
3. Spend 2 minutes per heuristic looking for violations
4. Note any severity 3+ issues
5. Fix the top issue that week

### Monthly Deep Dive (2 hours)

Once a month, do a thorough evaluation:

1. Pick a critical flow (onboarding, core feature, upgrade)
2. Record yourself going through the flow
3. Review the recording, noting violations
4. Rate all issues by severity
5. Create a prioritized fix list
6. Schedule the top 3 fixes in your next sprint

### Pre-Launch Evaluation (4 hours)

Before launching a new feature or major update:

1. Evaluate the entire new feature flow
2. Recruit 1-2 users to test it (in addition to your evaluation)
3. Fix all severity 3+ issues
4. Fix as many severity 2 issues as possible
5. Document known issues and workarounds

---

## 5. Common SaaS UX Patterns

### Pattern 1: The Dashboard

**What users expect**:
- Overview of their most important data
- Quick access to frequent actions
- Recent activity or changes
- Clear status indicators

**Common heuristic violations**:
- Too many widgets (violates aesthetic/minimalist design)
- No clear primary action (violates recognition)
- Stale data (violates visibility of system status)
- Confusing metrics (violates match with real world)

**Best practices**:
- Limit to 5-7 widgets max
- Show most important metric prominently
- Include timeframes on all data ("Last 30 days")
- Provide a single primary action button
- Personalize based on user behavior

### Pattern 2: The Table/List View

**What users expect**:
- Sortable columns
- Search/filter capability
- Action menu per row
- Bulk selection

**Common heuristic violations**:
- No search (violates flexibility)
- No sort on columns (violates user control)
- Actions hidden (violates recognition)
- No pagination or infinite scroll indication (violates visibility)

**Best practices**:
- Always provide search
- Make columns sortable by default
- Show row count ("Showing 1-20 of 143")
- Include visible row actions (edit, delete icons)
- Support keyboard navigation

### Pattern 3: The Form

**What users expect**:
- Clear labels
- Helpful validation
- Logical field order
- Save progress

**Common heuristic violations**:
- No inline validation (violates error prevention)
- Generic error messages (violates error recovery)
- Too many fields (violates minimalist design)
- No save/auto-save (violates user control)

**Best practices**:
- Single column layouts convert better
- Inline validation on blur
- Smart defaults
- Progress indicator for multi-step forms
- Save drafts automatically

### Pattern 4: The Settings Page

**What users expect**:
- Organized sections
- Search for settings
- Immediate save
- Clear defaults

**Common heuristic violations**:
- Unorganized sections (violates consistency)
- No save indicator (violates visibility)
- Buried important settings (violates recognition)
- No way to revert changes (violates user control)

**Best practices**:
- Group settings into logical sections
- Add a search bar for settings
- Auto-save or clear "save" button
- Show "saved" confirmation
- Provide "reset to defaults"

### Pattern 5: The Modal/Dialog

**What users expect**:
- Clear title
- Close button (X)
- Overlay backdrop
- Escape key to close

**Common heuristic violations**:
- No close button (violates user control)
- Clicking outside doesn't close (violates user control)
- No clear primary action (violates consistency)
- Content too long for modal (violates aesthetic)

**Best practices**:
- Always provide X button and Escape key
- Focus trapping inside modal
- Clear primary/secondary buttons
- Scroll within modal if needed
- Don't stack modals

---

## 6. Accessibility Basics for Heuristic Evaluation

### Why Accessibility Matters in Heuristics

Accessibility is not separate from usability. An inaccessible interface is, by definition, unusable for people with disabilities. Incorporating basic accessibility checks into your heuristic evaluation costs nothing and catches issues that affect all users.

### The Quick Accessibility Check

Add these to your heuristic evaluation:

**Visual accessibility**:
- Is there sufficient color contrast? (Minimum 4.5:1 for normal text)
- Is information conveyed without color alone?
- Is text resizable up to 200% without loss of content?
- Are clickable areas at least 44x44px for touch targets?

**Keyboard accessibility**:
- Can all functions be reached via keyboard?
- Is there a visible focus indicator?
- Does tab order follow logical page flow?
- Are there no keyboard traps?

**Screen reader accessibility**:
- Do images have alt text?
- Are form fields properly labeled?
- Are headings properly nested (h1 > h2 > h3)?
- Are ARIA landmarks used correctly?

**Cognitive accessibility**:
- Is the language clear and simple?
- Are instructions easy to follow?
- Are animations minimal (or prefer-reduced-motion respected)?
- Are error messages clear and helpful?

### Adding Accessibility to Heuristic Severity Ratings

When you find an accessibility issue, it's at minimum a Severity 2 issue, and often Severity 3 or 4:

- **Severity 4**: Users with disabilities cannot complete a core task
- **Severity 3**: Users with disabilities can complete the task but with significant difficulty
- **Severity 2**: Users with disabilities can complete the task with some difficulty
- **Severity 1**: Minor inconvenience for users with disabilities

---

## 7. From Evaluation to Action

### The Fix Priority Matrix

| | Easy Fix (< 2 hrs) | Hard Fix (> 2 hrs) |
|--|-------------------|--------------------|
| **High Severity (3-4)** | Fix immediately | Plan for this sprint |
| **Low Severity (1-2)** | Fix when convenient | Add to backlog |

### Creating Your UX Debt List

Maintain a running list of UX issues discovered through heuristic evaluations. Like technical debt, UX debt accumulates and compounds if not addressed.

| Issue | Heuristic | Severity | Effort | Found | Status |
|-------|-----------|----------|--------|-------|--------|
| No loading state on submit | Visibility | 3 | 2 hrs | Jan 15 | Fixed |
| Delete button too close to edit | Error prevention | 2 | 30 min | Jan 22 | Backlog |
| Inconsistent button colors | Consistency | 1 | 1 hr | Feb 1 | Backlog |

### The 20-Minute Fix Sprint

Most heuristic evaluation issues have a quick fix. Dedicate 20 minutes:

1. Pick the highest-severity issue that can be fixed in 20 minutes
2. Fix it
3. Deploy it
4. Move to the next

Over a month, this approach can fix 10-15 UX issues.

---

## 8. Automation for Heuristic Evaluations

### What Can Be Automated

Some heuristic violations can be caught automatically:

- **Color contrast**: Axe DevTools, WAVE, or Lighthouse
- **HTML validation**: Validator tools
- **Accessibility issues**: Axe-core, pa11y
- **Broken links**: Link checkers
- **Performance issues**: Lighthouse
- **Mobile responsiveness**: Chrome DevTools device mode

### Setting Up Automated Checks

Integrate accessibility and basic UX checks into your CI/CD pipeline:

```yaml
# GitHub Actions example
- name: Run accessibility check
  run: npx axe --exit public/
```

Run these weekly and review results as part of your evaluation.

### Limitations of Automation

Automated tools catch about 30% of usability issues. They can check:
- Color contrast ratios
- Missing alt text
- Improper heading hierarchy
- Missing form labels

But they CANNOT catch:
- Whether navigation makes sense
- Whether copy is clear
- Whether the flow matches user mental models
- Whether the design is aesthetically pleasing

Automated checks supplement, not replace, heuristic evaluation.

---

## 9. Scaling Your Evaluation Practice

### When to Do a Full Evaluation

Schedule full heuristic evaluations at these milestones:
- Before public launch (one full evaluation)
- After major UI redesigns
- Every quarter for critical flows
- When churn increases without clear reason
- When support tickets spike

### Getting a Second Perspective

As a solo founder, you have blind spots. Get a second perspective:

- **Swap evaluations with another solo founder**: You evaluate their product, they evaluate yours (free)
- **Hire a freelance UX reviewer**: $500-1000 for a thorough evaluation
- **Use a UX audit service**: Services like UserCheck offer affordable audits
- **Post in UX forums**: Some UX professionals will review for free

Even one additional perspective can catch issues you've become blind to.

### Building a UX Review Habit

The most important thing is consistency. Set up:

- **Weekly**: 30-minute heuristic check of one flow
- **Monthly**: 2-hour deep evaluation of critical flows
- **Quarterly**: Full product evaluation with external review
- **Pre-launch**: Evaluation of every new feature

Track your findings over time. If the number of severity 3+ issues is decreasing, your UX is improving.

---

## 10. Quick Reference: Heuristic Evaluation Checklist

Print this and use it during your evaluations:

### Nielsen's 10 Heuristics

- [ ] **1. Visibility of system status**: Is the user always informed of what's happening?
- [ ] **2. Match with real world**: Does the product speak the user's language?
- [ ] **3. User control and freedom**: Can users undo mistakes and go back?
- [ ] **4. Consistency and standards**: Are similar things treated similarly?
- [ ] **5. Error prevention**: Are errors designed out of the system?
- [ ] **6. Recognition over recall**: Are options visible, not remembered?
- [ ] **7. Flexibility and efficiency**: Are there shortcuts for power users?
- [ ] **8. Aesthetic and minimalist design**: Is the interface focused and clean?
- [ ] **9. Error recovery**: Are error messages clear and actionable?
- [ ] **10. Help and documentation**: Is help available and contextual?

### SaaS-Specific Checks

- [ ] **A. Time-to-value**: Can users get value in < 5 minutes?
- [ ] **B. Pricing transparency**: Is pricing clear and easy to find?
- [ ] **C. Trust and security**: Are security measures visible?
- [ ] **D. Export and portability**: Can users export data and cancel?
- [ ] **E. Notifications**: Are notifications relevant and manageable?

### Accessibility Checks

- [ ] Color contrast meets WCAG AA standards
- [ ] All functionality available via keyboard
- [ ] Proper heading hierarchy
- [ ] Form fields have labels
- [ ] Images have appropriate alt text
- [ ] Touch targets are ≥ 44x44px
- [ ] Focus indicators visible
- [ ] Text resizable to 200%

Run through this checklist for every major UI change. It will catch 80% of common UX issues and ensure your SaaS is usable, accessible, and conversion-optimized.
