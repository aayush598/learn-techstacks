# Empty States and Guidance

## The Most Overlooked UX Opportunity

Empty states are what users see when there's no data to display: a new account's dashboard, a search with no results, an inbox with no messages. Most developers treat empty states as afterthoughts—a quick "No data" message and move on.

This is a massive mistake. Empty states are often the **first thing a new user sees** after signing up. They set the tone for the entire product experience. A good empty state can turn a cold start into an engaging onboarding moment.

For solo founders, well-designed empty states are a high-leverage investment: they're easy to implement (no complex logic), they dramatically improve first impressions, and they directly impact activation and retention.

---

## 1. The Role of Empty States

### What Empty States Communicate

Every empty state sends a message to the user:

| Message Type | Example |
|-------------|---------|
| **"This product is dead"** | Blank page with no guidance |
| **"This product is hard"** | "No data" with no next steps |
| **"This product cares"** | Friendly illustration with clear action |
| **"This product is valuable"** | Shows what the page will look like with data |

The first two messages cause churn. The last two drive activation.

### The Three Functions of Empty States

1. **Educate**: Tell users what this page/section is for
2. **Activate**: Show users what to do next
3. **Motivate**: Help users imagine the future state with data

### Empty State Types

| Type | Example | Goal |
|------|---------|------|
| First visit | New user dashboard | Get user started |
| Empty result | Search with no matches | Suggest alternatives |
| Cleared state | All tasks completed | Celebrate, suggest next |
| Error state | Failed to load data | Recover gracefully |
| Feature not used | Unused integration tab | Encourage feature adoption |

---

## 2. Anatomy of a Great Empty State

### Core Components

Every empty state should include:

1. **Illustration or icon**: Visual that communicates the empty state (friendly, not sad)
2. **Headline**: What this page is (1-5 words)
3. **Description**: Why it's empty and what to do next (1-2 sentences)
4. **Primary CTA**: The action to take (one button, clearly visible)
5. **Secondary option**: Alternative action or "Learn more" link

### The Empty State Template

```
[Illustration: Friendly character or simple icon]

## Headline: Get started with your first project

Description: Projects help you organize your work. 
Create your first project and start tracking your progress.

[Create Your First Project] ← Primary CTA

Or import from another tool → ← Secondary option
```

### Illustration Guidelines

- **Tone**: Friendly, approachable, not sad or punitive
- **Style**: Simple, consistent with your brand
- **Size**: Large enough to be noticed, not overwhelming
- **Position**: Above or next to the content (not replacing it entirely)

If you can't afford custom illustrations:
- Use simple geometric shapes or abstract art
- Use a large icon from your icon set
- Use a subtle gradient background
- Use an emoji (😊 🚀 ✨) as a low-cost alternative

### Copywriting for Empty States

**Do say**:
- "Start tracking your first project"
- "No invoices yet. Create your first one."
- "Invite your team to get started"

**Don't say**:
- "No data available"
- "You have no projects"
- "Empty"
- "Nothing here yet"

The difference is agency. The first set gives the user a clear action. The second set just describes the void.

---

## 3. Empty State Patterns by Context

### Pattern 1: New Account Empty State

**When**: User just signed up, first visit
**Goal**: Get user to take the first action

**Example**: Asana's "Welcome to Asana" card
```
[Illustration: Rocket or friendly character]

Welcome to Asana!

Create your first project to get started.
You can organize tasks, set deadlines, and collaborate.

[Create Project] [Import from Trello]
```

**Key considerations**:
- This is the most important empty state in your product
- Use the friendliest, most encouraging tone
- Make the CTA impossible to miss
- Offer an alternative (import, template, tutorial)

### Pattern 2: Empty Search Results

**When**: User searches and finds nothing
**Goal**: Help user find what they need or create it

**Example**: Notion's empty search
```
[Icon: Magnifying glass]

No results found for "team meetings"

Suggestions:
- Check your spelling
- Try a different search term
- Search in all workspaces (not just this one)

[Create "team meetings" page] → ← Smart suggestion
```

**Key considerations**:
- Don't blame the user ("No results found" is OK)
- Suggest alternatives (spelling, filters, broader search)
- Offer to create what they searched for (if applicable)
- Show recently used items as alternatives

### Pattern 3: Filtered View Empty State

**When**: User applies filters and sees no results
**Goal**: Help user adjust filters

**Example**: Linear's empty filtered view
```
[Subtle icon]

No issues match your filters

[Clear Filters] → ← Prominent action

Filters applied: Status: Done, Assignee: You, Priority: High
```

**Key considerations**:
- Show which filters are active
- One-click "Clear filters" button
- Suggest removing one filter at a time

### Pattern 4: Task Complete Empty State

**When**: User completes all items in a list
**Goal**: Celebrate and suggest next action

**Example**: Todoist's "Completed all tasks"
```
[Icon: Celebration/confetti]

You're all done! 🎉

You've completed everything in this project.

[Create a new task] [Review completed tasks]
```

**Key considerations**:
- Celebrate the accomplishment
- Keep the momentum going with a next action
- This is a positive moment—make it feel good

### Pattern 5: Feature Not Yet Used

**When**: User navigates to a feature they haven't used
**Goal**: Explain the feature and encourage adoption

**Example**: Slack's "App Directory" for a new workspace
```
[Illustration: App icon grid]

Discover apps to customize your Slack

Bring your tools into Slack to streamline your workflow.
Connect Google Drive, Zoom, and hundreds more.

[Browse App Directory] → [Learn more about apps]
```

**Key considerations**:
- Explain what this feature does (user may not know they need it)
- Show value before asking for action
- Link to relevant help docs

### Pattern 6: Error Empty State

**When**: Data failed to load
**Goal**: Recover gracefully

**Example**: GitHub's error state
```
[Icon: Warning or broken page]

Something went wrong

We couldn't load this data. This is usually a temporary issue.

[Try Again] [Go to Dashboard] [Report Issue]
```

**Key considerations**:
- Don't blame user or make them feel responsible
- Offer immediate recovery (retry button)
- Provide alternative destinations
- Show data freshness info if available

---

## 4. Guided Setup Wizards

### When to Use a Wizard

A guided setup wizard is a step-by-step flow that helps users configure their account and get started. Use one when:

- Your product requires configuration before value (analytics tools)
- Users need to make decisions that affect their experience (CRM setup)
- There's a natural sequence of actions (import → configure → use)
- The alternative (blank dashboard) is overwhelming

### Wizard Design Principles

**1. Show progress**
```html
[Step 1 of 4: Import Data] [=====>-----------------] 25%
```

**2. One thing per step**
Each step should have exactly one question or action. Don't ask for multiple things on one screen.

**3. Save automatically**
If the user closes the wizard, their progress should be saved.

**4. Allow skipping**
Every step should have a "Skip for now" option. Users can always come back.

**5. Show the end state**
Preview what the product will look like after setup.

### Wizard Structure

```
Step 1: Welcome + value prop (15 sec)
  "We'll help you set up in 4 quick steps"

Step 2: Core configuration (30 sec)
  "What's your company name? [text input]"

Step 3: Import data (1 min)
  "Import your data or start fresh"
  [Import CSV] [Connect Integration] [Start Fresh]

Step 4: Customize (30 sec)
  "Choose your focus" [Option A] [Option B] [Option C]

Step 5: See your workspace! (activation)
  "You're all set! Here's your workspace."
  [Go to Dashboard]
```

### The Solo-Friendly Wizard Template

```html
<!-- Wizard container -->
<div class="max-w-2xl mx-auto px-6 py-12">
  
  <!-- Progress bar -->
  <div class="mb-8">
    <div class="flex justify-between mb-2">
      <span class="text-sm font-medium">Step 2 of 4</span>
      <span class="text-sm text-gray-500">Import your data</span>
    </div>
    <div class="w-full bg-gray-200 rounded-full h-2">
      <div class="bg-primary h-2 rounded-full" style="width: 50%"></div>
    </div>
  </div>

  <!-- Step content -->
  <div class="bg-white rounded-xl border p-8">
    <h2 class="text-2xl font-bold mb-2">Import your data</h2>
    <p class="text-gray-600 mb-6">
      Bring your existing data in one click.
    </p>

    <!-- Options -->
    <div class="space-y-4">
      <button class="w-full border rounded-lg p-4 text-left hover:border-primary">
        Upload CSV file
      </button>
      <button class="w-full border rounded-lg p-4 text-left hover:border-primary">
        Connect from Trello/Asana
      </button>
      <button class="w-full border rounded-lg p-4 text-left hover:border-primary">
        Start with a template
      </button>
    </div>
  </div>

  <!-- Actions -->
  <div class="flex justify-between mt-6">
    <button class="text-gray-500 hover:text-gray-700">Skip for now</button>
    <button class="bg-primary text-white px-6 py-2 rounded-lg">Continue</button>
  </div>
</div>
```

---

## 5. Contextual Help and Tooltips

### Types of In-App Guidance

| Type | When to Use | Content Length |
|------|-------------|----------------|
| **Tooltip** | Explain an icon or brief term | 5-10 words |
| **Popover** | Explain a feature or field | 1-2 sentences |
| **Banner** | Important announcement or tip | 1-3 sentences |
| **Slideout panel** | Detailed guidance | Paragraph |
| **Hotspot** | Draw attention to a new feature | Brief label |
| **Checklist** | Multi-step guidance | 3-5 items |

### Tooltip Best Practices

**When to show tooltips**:
- Icon-only buttons (no label)
- Technical terms users might not know
- Fields with specific formatting requirements
- Features that are easy to miss
- First-time user orientation

**When NOT to show tooltips**:
- Obvious elements (everyone knows what "Save" does)
- Critical information users need to act on (use inline text instead)
- Complex explanations (use a separate help page)
- On hover only (not accessible on mobile)

**Tooltip design**:
- Short: 5-10 words max
- Actionable: Tell user what they need to know
- Dismissible: Always have a way to close
- Positioned: Above or below the element (not covering it)
- Delayed: 500ms delay before showing on hover

```html
<!-- Good tooltip -->
<button aria-label="Sort by date">
  <SortIcon />
  <span class="tooltip">Sort by date (newest first)</span>
</button>
```

### The Tooltip Sequence

For guiding users through a complex flow, use a sequence of tooltips (max 5):

```
Tooltip 1: "Welcome! Here's your dashboard."
    ↓
Tooltip 2: "This is your activity feed."
    ↓
Tooltip 3: "Click here to create a new project."
    ↓
Tooltip 4: "Your settings are always here."
    ↓
Tooltip 5: "Need help? We're here."
```

Each tooltip:
- Has a "Next" button
- Has a "Skip tour" option
- Highlights the relevant element
- Disappears after user completes the action (if applicable)

### Contextual Help Integration

**Pattern 1: Question mark icons**
Place a small `?` icon next to complex fields. On click/hover, show a tooltip explanation.

**Pattern 2: Help sidebar**
A slide-out panel with contextual help based on the current page.

**Pattern 3: Inline help text**
Short text below a field: "Password must be at least 8 characters."

**Pattern 4: "Learn more" links**
Link to documentation for complex topics: "What is a workspace? Learn more →"

### Implementation with shadcn/ui

```jsx
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from '@/components/ui/tooltip'

<TooltipProvider>
  <Tooltip>
    <TooltipTrigger asChild>
      <Button variant="ghost" size="icon">
        <HelpCircle className="h-4 w-4" />
      </Button>
    </TooltipTrigger>
    <TooltipContent>
      <p>This shows your monthly active users.</p>
    </TooltipContent>
  </Tooltip>
</TooltipProvider>
```

---

## 6. The Onboarding Checklist

### Why Checklists Work

Checklists are one of the most effective onboarding patterns:
- **Progress visualization**: Users see what they've done and what's left
- **Motivation**: Completing items feels good (Zeigarnik effect)
- **Structure**: Users know what to do next without thinking
- **Focus**: Only 5-7 items, so it's not overwhelming

### The Checklist Template

```
## Get Started Checklist

[ ] Create your first project
[ ] Import your data
[ ] Invite a team member
[ ] Customize your settings
[ ] Explore the dashboard

Progress: 2/5 complete
```

### Checklist Design Guidelines

1. **5-7 items maximum**: Any more is overwhelming
2. **Clear actions**: Each item should be a specific action, not a concept
3. **Celebrate completion**: Confetti, animation, or at least a satisfying checkmark
4. **Show progress**: "3 of 5 complete" is motivating
5. **Re-orderable**: Let users choose what to do first
6. **Persistent**: Stay visible until all items are done
7. **Dismissible**: Let users hide it if they're not interested

### Implementation Pattern

```jsx
const checklistItems = [
  { id: 1, text: 'Create your first project', action: '/projects/new', completed: false },
  { id: 2, text: 'Import your data', action: '/import', completed: false },
  { id: 3, text: 'Invite a team member', action: '/team/invite', completed: false },
]

function OnboardingChecklist({ items }) {
  const completed = items.filter(i => i.completed).length
  return (
    <div className="bg-white rounded-xl border p-6 shadow-sm">
      <h3 className="font-semibold mb-1">Get Started</h3>
      <p className="text-sm text-gray-500 mb-4">{completed}/{items.length} complete</p>
      <Progress value={(completed / items.length) * 100} className="mb-4" />
      <ul className="space-y-3">
        {items.map(item => (
          <li key={item.id} className="flex items-center gap-3">
            <Checkbox checked={item.completed} />
            <span className={item.completed ? 'line-through text-gray-400' : ''}>
              {item.text}
            </span>
          </li>
        ))}
      </ul>
    </div>
  )
}
```

---

## 7. Guidance for Feature Discovery

### The Feature Discovery Problem

Users don't use features they don't know exist. With dozens of features, most SaaS products suffer from poor feature adoption because features are hidden behind menus, buried in settings, or never surfaced at the right moment.

### Discovery Patterns

**Pattern 1: The "What's New" modal**
Show a modal after major updates:
```
## What's New in TimeTracker

✓ Bulk edit: Edit multiple tasks at once
✓ Dark mode: Easier on the eyes
✓ New reports: See team productivity at a glance

[Try Bulk Edit] [Dismiss]
```

**Pattern 2: Contextual suggestions**
```
User just finished creating 5 tasks manually.
Tooltip: "Create multiple tasks faster with bulk import"
```

**Pattern 3: Feature adoption nudges**
```
User hasn't used reports after 30 days.
Banner: "Did you know? Reports show you your team's productivity trends."
```

**Pattern 4: Empty state prompts**
```
User navigates to Integrations tab (with no integrations).
"We support 50+ integrations. Connect your tools to streamline work."
```

**Pattern 5: Anniversary nudges**
```
User has been active for 30 days.
"Congratulations! As a power user, you now have access to our API."
```

### The Feature Adoption Funnel

```
1. Feature exists (user may not know)
2. User discovers feature (sees it, reads about it)
3. User tries feature (first interaction)
4. User adopts feature (uses it regularly)
5. User advocates feature (tells others)

Each stage has drop-off. Empty states and guidance help move users through the funnel.
```

---

## 8. Building a Help System

### The Solo Help System

As a solo founder, you can't build a comprehensive help center immediately. Start with this:

**Phase 1: In-app help (minimum)**
- Tooltips on complex elements
- A "Help" button in the navigation
- A FAQ page (notion or markdown)
- Email support (you personally)

**Phase 2: Knowledge base (growth)**
- Help articles for common tasks
- Searchable knowledge base
- Video tutorials for key features
- Link to help from relevant pages

**Phase 3: Community-driven (scale)**
- User forum or community
- User-contributed tips and tricks
- Feature request board
- Status page

### Phase 1 Implementation

```html
<!-- Help button in navigation -->
<button class="fixed bottom-4 right-4 bg-primary text-white w-12 h-12 rounded-full shadow-lg">
  ?
</button>

<!-- Help panel (slideout) -->
<div class="fixed right-0 top-0 h-full w-80 bg-white shadow-xl p-6">
  <h3>How can we help?</h3>
  <input placeholder="Search help..." />
  <div class="mt-4">
    <h4>Popular topics</h4>
    <ul>
      <li>Getting started guide</li>
      <li>How to create a project</li>
      <li>Importing your data</li>
      <li>Inviting team members</li>
    </ul>
  </div>
  <div class="mt-4">
    <p>Still need help? <a href="mailto:help@yourproduct.com">Email us</a></p>
  </div>
</div>
```

### The FAQ Page Template

```
# Frequently Asked Questions

## Getting Started
Q: How do I create my first project?
A: Click the "New Project" button on the dashboard. ...

Q: Can I import data from other tools?
A: Yes! We support imports from CSV, Trello, and Asana. ...

## Account and Billing
Q: Can I change my plan?
A: Yes, you can upgrade or downgrade anytime from your billing settings. ...

## Troubleshooting
Q: Why isn't my data loading?
A: Try refreshing the page. If the issue persists, contact support. ...
```

---

## 9. Error Messages and Recovery

### The Anatomy of a Good Error Message

**Good error**:
```
"Your session expired. Please sign in again to continue."
```
- What happened: clear explanation
- Why it happened: user can understand
- How to fix it: specific action

**Bad error**:
```
"Error 401: Unauthorized"
```
- What happened: cryptic
- Why it happened: unclear
- How to fix it: nothing

### Error Message Template

```
[Icon: Issue type - warning, error, info]

### [Short headline describing the issue]

[Simple explanation of what happened]

[Action to fix it] → CTA button or link

[If applicable: alternative actions]
```

### Common SaaS Error States

| Error | Message | Fix |
|-------|---------|-----|
| Network error | "Couldn't load data. Check your connection." | Retry button |
| Server error | "Something went wrong on our end." | Retry, auto-retry |
| Permission denied | "You don't have access to this page." | Contact admin link |
| Validation error | "Invalid email format." | Inline field error |
| Rate limited | "Too many requests. Please wait." | Time estimate |
| Not found | "This page doesn't exist." | Go to dashboard link |
| Payment failed | "Your payment didn't go through." | Update payment method |

### Error Prevention vs. Recovery

Invest 80% in error prevention, 20% in error recovery.

**Prevention**:
- Validate fields in real-time
- Disable buttons until form is valid
- Confirm destructive actions
- Save drafts automatically
- Warn before navigating away

**Recovery**:
- Clear error messages
- One-click fix actions
- Auto-save drafts for recovery
- Undo for destructive actions
- Support contact available

---

## 10. Implementing as a Solo Founder

### Priority Order

1. **Empty states on every page** — Every page should have an empty state designed (not a developer placeholder)
2. **Error states on every API call** — Every API interaction should handle success, loading, and error
3. **Tooltips on confusing elements** — Add tooltips as you notice confusion through session recordings
4. **Onboarding checklist** — Add a simple checklist for the first session
5. **Contextual help** — Link to help articles from relevant pages
6. **Guided setup wizard** — Add if your product needs configuration

### The Minimum Viable Empty State

If you can only do one thing, do this for every empty page:

```html
<div class="flex flex-col items-center justify-center py-16">
  <Icon className="h-16 w-16 text-gray-300 mb-4" />
  <h3 class="text-xl font-semibold text-gray-900 mb-2">
    [Page name] will appear here
  </h3>
  <p class="text-gray-500 text-center max-w-md mb-6">
    [Description of what this page does and why it's empty]
  </p>
  <Button>[Primary Action]</Button>
  <a href="#" class="text-sm text-gray-400 mt-3 hover:text-gray-600">
    Learn more →
  </a>
</div>
```

### Testing Your Empty States

1. Create a brand new account and go through the product
2. Note every page that shows empty/loading state
3. Is each state helpful? Does it guide you?
4. Is there a clear next action?
5. Does it match the product's tone and brand?

Fix all empty states that say "No data" or are completely blank.

### Checklist for Every Page

- [ ] Empty state designed (not just "No data")
- [ ] Error state designed (not just raw error message)
- [ ] Loading state designed (skeleton or spinner)
- [ ] Primary action visible in empty state
- [ ] Contextual help available for complex elements
- [ ] Tooltips for icon-only buttons
- [ ] Help documentation accessible from this page

---

## 11. Common Empty State Mistakes

### Mistake 1: Showing "No Data"

The most common and worst empty state. It's cold, unhelpful, and makes users feel like they broke something.

**Fix**: Explain why there's no data and what to do about it.

### Mistake 2: Designing Only for Happy Path

"Users will have data immediately" — no, they won't. Design for the first visit, for searches with no results, for filtered views with no matches.

**Fix**: Every view needs empty, loading, error, and success states.

### Mistake 3: Inconsistent Tone

Empty state is playful ("Nothing here yet! 🎈") but the product is serious (enterprise B2B). Or vice versa.

**Fix**: Match the tone to your brand. A developer tool can be direct; a consumer app can be playful.

### Mistake 4: No Clear Action

"Your feed is empty." — OK, what should I do about it?

**Fix**: Every empty state has a CTA (or "skip" if the action isn't mandatory).

### Mistake 5: Overwhelming Options

"You can create a project, import data, invite team, configure settings, explore templates, or watch a tutorial." — Too many choices.

**Fix**: One primary CTA, one secondary. That's it.

### Mistake 6: Using Generic Illustrations

A sad file icon for every empty state. Uninspired and doesn't help the user understand what to do.

**Fix**: Match the illustration to the context. Search icon for empty results. Setup icon for new account.

---

## 12. Guidance Best Practices Summary

| Pattern | When to Use | Key Principle |
|---------|-------------|---------------|
| Empty state | Page has no data | Show path forward, not empty void |
| Tooltip | Complex/icon-only elements | Brief, dismissible, delayed |
| Onboarding checklist | New users | 5-7 items, shows progress |
| Guided wizard | Products needing setup | One step at a time, skippable |
| Contextual help | Feature-specific questions | Page-relevant, searchable |
| Error recovery | Something went wrong | Explain, apologize, fix |
| Feature discovery | Unused features | Right time, right place |
| What's new modal | After major updates | Brief, actionable, dismissible |

---

## 13. The Empty State and Guidance Manifesto

1. **Every page needs 4 states**: Loading, empty, error, and success
2. **Empty is an opportunity, not a problem** — Use it to guide and motivate
3. **Never say "No data"** — Always provide context and a next step
4. **One primary action per empty state** — Don't overwhelm with choices
5. **Design empty states first** — They're more important than full states for new users
6. **Tooltips teach; banners promote** — Use the right tool for the right job
7. **Help is contextual** — Show help where users need it, not in a separate page
8. **Errors are UX, not exceptions** — Design error states as carefully as normal states
9. **Celebrate completion** — Empty states after finishing feel great
10. **Test with fresh eyes** — You're blind to your own empty states

Empty states and guidance are your product's welcome mat. A welcoming empty state can be the difference between a user who leaves in the first 30 seconds and one who becomes a lifelong customer. Don't leave them as an afterthought—design them with as much care as your core features.
