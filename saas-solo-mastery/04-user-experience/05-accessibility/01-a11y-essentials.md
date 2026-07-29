# Web Accessibility Essentials for SaaS

## Why Accessibility Matters for Solo Founders

Accessibility is often seen as an "enterprise concern" — something to worry about when you have a compliance department or government contracts. This is a dangerous misconception. Accessibility matters at every stage:

- **Legal risk**: Accessibility lawsuits are increasing. Even small SaaS products can be targeted.
- **Market reach**: 15% of the global population has a disability. That's a huge market you're excluding.
- **SEO benefits**: Many accessibility practices improve search rankings (alt text, semantic HTML, headings).
- **Better UX for everyone**: Curb cuts (sidewalk ramps) benefit everyone, not just wheelchair users. The same applies to digital accessibility.
- **Future-proofing**: Building accessibility in later is 10x more expensive than building it in now.

For a solo founder, the key insight is: **accessibility is a compounding investment**. The sooner you build it in, the less it costs, and the more it pays off over time.

---

## 1. Accessibility Fundamentals

### The Four Principles (POUR)

The WCAG (Web Content Accessibility Guidelines) are built on four principles:

1. **Perceivable**: Information must be presentable to users in ways they can perceive. (Can't see the screen? Can they hear it?)
2. **Operable**: UI components must be operable. (Can't use a mouse? Can they use a keyboard?)
3. **Understandable**: Information and UI must be understandable. (Can users understand the content and how to use it?)
4. **Robust**: Content must be robust enough to be interpreted by a wide variety of user agents, including assistive technologies.

### Disability Categories

| Category | Example | How They Use Your SaaS |
|----------|---------|------------------------|
| Visual | Blind, low vision, color blind | Screen reader, screen magnifier, high contrast mode |
| Hearing | Deaf, hard of hearing | Captions, transcripts, visual indicators |
| Motor | Limited mobility, tremor, paralysis | Keyboard-only navigation, voice control, switch devices |
| Cognitive | ADHD, dyslexia, autism, memory impairment | Clear layout, simple language, consistent navigation |

### Accessibility Levels

WCAG defines three conformance levels:

| Level | Description | Effort |
|-------|-------------|--------|
| **A** | Minimum, must-have | Low |
| **AA** | Standard, most common target | Medium |
| **AAA** | Highest, specialized | High |

For most SaaS products, **WCAG AA is the target**. It covers the most important accessibility issues without the extreme effort of AAA.

---

## 2. Automated Testing Tools

### Free Tools

| Tool | Type | What It Checks | Integration |
|------|------|----------------|-------------|
| **axe DevTools** | Browser extension | WCAG violations, best practices | Chrome, Firefox, Edge |
| **WAVE** | Browser extension | Visual issues, contrast, ARIA | Chrome, Firefox |
| **Lighthouse** | Built into Chrome | a11y score, best practices | Chrome DevTools, CI |
| **Pa11y** | CLI tool | WCAG compliance | CI/CD pipeline |
| **Accessibility Insights** | Full suite | Fast pass, assessment | Windows, browser |
| **Chrome DevTools** | Built-in | Contrast, keyboard, labels | Chrome |

### Paid Tools

| Tool | Price | Best For |
|------|-------|----------|
| **Deque Axe** | Enterprise | Comprehensive testing |
| **Siteimprove** | Enterprise | Monitoring at scale |
| **AudioEye** | Per-month | Ongoing compliance |
| **AccessiBe** | Per-month | Automated remediation (use with caution) |

### Setting Up Automated Checks

**In the browser**:
1. Install axe DevTools extension
2. Open any page of your SaaS
3. Run accessibility scan
4. Review violations (critical, serious, moderate, minor)
5. Fix critical/serious issues

**In CI/CD**:
```yaml
# GitHub Actions: Automated a11y check
- name: Run axe checks
  run: |
    npx axe http://localhost:3000 --exit --stdout
```

**In tests**:
```js
// Playwright + axe
import { injectAxe, checkA11y } from 'axe-playwright'

test('Dashboard is accessible', async ({ page }) => {
  await page.goto('/dashboard')
  await injectAxe(page)
  await checkA11y(page, null, {
    includedImpacts: ['critical', 'serious']
  })
})
```

### What Automation Can and Can't Catch

**Automation catches** (~30% of issues):
- Missing alt text
- Insufficient color contrast
- Missing form labels
- Improper heading hierarchy
- Missing ARIA attributes
- Keyboard traps

**Automation misses** (~70% of issues):
- Meaningful alt text
- Logical focus order
- Screen reader announcement quality
- Whether headings describe content accurately
- Whether instructions are clear
- Whether navigation makes sense

Automated tools are a safety net, not a complete solution. Manual testing is essential.

---

## 3. Keyboard Accessibility

### Why Keyboard Accessibility Matters

Many users cannot use a mouse:
- Blind users (use keyboard + screen reader)
- Motor impaired users (limited fine motor control)
- Power users who prefer keyboard navigation
- Temporary conditions (broken arm, RSI)

### Making Your SaaS Keyboard Accessible

**All interactive elements must be reachable via keyboard**:
- Links: `<a href="...">`
- Buttons: `<button>` or `role="button"`
- Form inputs: `<input>`, `<select>`, `<textarea>`
- Custom components: Must have `tabindex="0"` and proper keyboard handlers

**Implementation checklist**:
- [ ] All interactive elements have visible focus indicators
- [ ] Tab order follows logical page flow (left to right, top to bottom)
- [ ] No keyboard traps (user can't get stuck in an element)
- [ ] All functionality accessible via keyboard (no mouse-only interactions)
- [ ] Keyboard shortcuts documented and configurable
- [ ] Escape key closes modals, dropdowns, menus
- [ ] Enter/Space activates focused elements

### Focus Indicators

**Never remove focus outlines**:
```css
/* Bad - removes focus for everyone */
*:focus { outline: none; }

/* Good - custom focus style that's still visible */
*:focus-visible {
  outline: 2px solid var(--primary);
  outline-offset: 2px;
}
```

**Focus indicator requirements** (WCAG 2.4.7):
- Minimum 2px thick
- Contrast ratio of at least 3:1 against adjacent background
- Visible in all lighting conditions

### Custom Components Keyboard Support

| Component | Keyboard Interaction |
|-----------|---------------------|
| Button | Enter/Space to activate |
| Link | Enter to navigate |
| Checkbox | Space to toggle |
| Radio group | Arrow keys to navigate, Space to select |
| Select/Combobox | Enter to open, Arrow keys to navigate, Enter to select, Escape to close |
| Modal | Escape to close, Tab trap inside modal |
| Menu | Enter to open, Arrow keys to navigate, Escape to close |
| Slider | Arrow keys to adjust, Home/End for min/max |
| Accordion | Enter/Space to toggle, Arrow keys if nested |
| Tabs | Arrow keys to switch tabs |

### Implementing Keyboard Support

```jsx
// Accessible button
<button
  onClick={handleClick}
  onKeyDown={(e) => {
    if (e.key === 'Enter' || e.key === ' ') {
      handleClick()
    }
  }}
>
  Submit
</button>

// Shadcn/ui components handle this for you
<Button onClick={handleClick}>Submit</Button>
```

---

## 4. Screen Reader Accessibility

### How Screen Readers Work

Screen readers (JAWS, NVDA, VoiceOver, TalkBack):
- Read content linearly (top to bottom, left to right)
- Navigate by headings, links, landmarks, form fields
- Announce element types ("button", "link", "heading level 2")
- Read ARIA attributes for additional context

### Semantic HTML

Semantic HTML is the foundation of screen reader accessibility.

**Use correct HTML elements**:
```html
<!-- Bad: div as button -->
<div class="button" onclick="submit()">Submit</div>

<!-- Good: actual button -->
<button onclick="submit()">Submit</button>

<!-- Bad: div as heading -->
<div class="heading">Welcome</div>

<!-- Good: actual heading -->
<h1>Welcome</h1>

<!-- Bad: div as link -->
<div onclick="navigate()">Go to dashboard</div>

<!-- Good: actual link -->
<a href="/dashboard">Go to dashboard</a>
```

### Headings

Headings are the primary navigation method for screen reader users.

**Rules**:
- One `h1` per page (describes the page purpose)
- Headings in logical order (h1 → h2 → h3, never skip levels)
- Headings describe the content that follows
- Don't use headings for styling only

```html
<h1>Dashboard</h1>
  <h2>Projects</h2>
    <h3>Active Projects</h3>
    <h3>Completed Projects</h3>
  <h2>Team</h2>
    <h3>Members</h3>
    <h3>Invitations</h3>
```

### Landmarks

Landmarks help screen reader users navigate to major sections:

```html
<header role="banner">Site header with navigation</header>
<nav role="navigation">Main navigation</nav>
<main role="main">Primary content</main>
<aside role="complementary">Sidebar</aside>
<footer role="contentinfo">Footer</footer>
<form role="search">Search form</form>
```

HTML5 elements automatically have landmark roles. Using semantic HTML gives you landmarks for free.

### Form Accessibility

**Each form field needs**:
- A visible `<label>` element
- `id` on input matching `for` on label
- Error messages associated with the field via `aria-describedby`

```html
<div class="form-group">
  <label for="email">Email address</label>
  <input 
    type="email" 
    id="email" 
    name="email"
    aria-describedby="email-hint email-error"
    aria-invalid="false"
    required
  />
  <p id="email-hint">We'll never share your email.</p>
  <p id="email-error" role="alert" hidden>
    Please enter a valid email address.
  </p>
</div>
```

### Images

**All images need alt text**:

```html
<!-- Decorative image: empty alt (screen reader skips it) -->
<img src="decoration.png" alt="" />

<!-- Informative image: describe what's shown -->
<img src="chart.png" alt="Revenue grew 40% from Q1 to Q2, from $100k to $140k" />

<!-- Functional image (icon button): describe the action -->
<button>
  <img src="settings-icon.png" alt="Settings" />
</button>
```

### ARIA (Accessible Rich Internet Applications)

ARIA attributes supplement HTML when semantic HTML isn't enough.

**ARIA rules**:
1. Don't use ARIA if you can use semantic HTML
2. Don't override native semantics (don't add `role="heading"` to an H1)
3. All interactive ARIA elements must be keyboard accessible

**Common ARIA attributes**:

```html
<!-- Live region: announces dynamic content changes -->
<div aria-live="polite" aria-atomic="true">
  New notification: You have 3 unread messages
</div>

<!-- Expanded state for accordions/menus -->
<button aria-expanded="false" aria-controls="menu-content">
  Menu
</button>
<div id="menu-content" hidden>
  Menu items here
</div>

<!-- Current page in navigation -->
<a href="/dashboard" aria-current="page">Dashboard</a>

<!-- Progress indicator -->
<div role="progressbar" aria-valuenow="70" aria-valuemin="0" aria-valuemax="100">
  70% complete
</div>
```

---

## 5. Color and Contrast

### Contrast Requirements

| Text Type | Ratio | WCAG Level |
|-----------|-------|------------|
| Normal text (< 18px) | 4.5:1 | AA |
| Large text (> 18px bold, > 24px regular) | 3:1 | AA |
| Normal text | 7:1 | AAA |
| UI components (icons, borders) | 3:1 | AA |

### Checking Contrast

Use tools to verify contrast ratios:
- **WebAIM Contrast Checker**: Enter two colors, get ratio
- **Chrome DevTools**: Inspect element → Color picker → Contrast ratio
- **Stark** (Figma plugin): Check contrast in design phase
- **axe DevTools**: Automatic contrast checking

### Safe Color Combinations

| Background | Text | Ratio |
|------------|------|-------|
| White (#fff) | Dark gray (#333) | 12:1 |
| White (#fff) | Gray (#666) | 4.6:1 |
| Light gray (#f5f5f5) | Dark (#333) | 8.6:1 |
| Primary blue (#6366f1) | White (#fff) | 6.2:1 |

### Don't Use Color Alone

Information conveyed through color must also be available without color:

```html
<!-- Bad: only color indicates status -->
<span class="text-red-500">Overdue</span>
<span class="text-green-500">Paid</span>

<!-- Good: icon + color + text -->
<span class="text-red-500">
  <AlertCircle class="inline" />
  Overdue
</span>
<span class="text-green-500">
  <CheckCircle class="inline" />
  Paid
</span>
```

### High Contrast Mode

Test your SaaS in Windows High Contrast Mode and prefers-contrast: more:

```css
/* Support high contrast mode */
@media (prefers-contrast: more) {
  :root {
    --text-primary: #000000;
    --bg-primary: #ffffff;
  }
}

/* Ensure images/icons don't disappear in high contrast */
.icon {
  forced-color-adjust: none;
}
```

---

## 6. Accessible Forms

### Form Structure

Every form should follow this pattern:

```html
<form aria-label="Sign up form" novalidate>
  <h2 id="form-heading">Create your account</h2>

  <div class="field">
    <label for="name">Full name</label>
    <input 
      type="text" 
      id="name" 
      name="name"
      autocomplete="name"
      aria-required="true"
    />
  </div>

  <div class="field">
    <label for="email">Email address</label>
    <input 
      type="email" 
      id="email" 
      name="email"
      autocomplete="email"
      aria-required="true"
      aria-describedby="email-format"
    />
    <p id="email-format" class="hint">Enter your work email</p>
  </div>

  <div class="field">
    <label for="password">Password</label>
    <input 
      type="password" 
      id="password" 
      name="password"
      autocomplete="new-password"
      aria-required="true"
      aria-describedby="password-rules"
      aria-invalid="false"
    />
    <ul id="password-rules" class="hints">
      <li>At least 8 characters</li>
      <li>One uppercase letter</li>
      <li>One number</li>
    </ul>
  </div>

  <button type="submit">Sign up</button>
</form>
```

### Error Validation

**Inline errors** (accessible pattern):

```html
<div class="field" aria-invalid="true">
  <label for="email">Email</label>
  <input 
    type="email" 
    id="email" 
    aria-invalid="true"
    aria-describedby="email-error"
  />
  <p id="email-error" role="alert">
    Please enter a valid email address.
  </p>
</div>
```

**Error summary** (for form-level errors):

```html
<div role="alert" aria-live="assertive">
  <h2>There are 3 errors in your form</h2>
  <ul>
    <li><a href="#name">Name is required</a></li>
    <li><a href="#email">Email is invalid</a></li>
    <li><a href="#password">Password is too short</a></li>
  </ul>
</div>
```

### Form Design for Accessibility

- **Single column**: Easier to follow for screen reader users and cognitive accessibility
- **Clear labels**: Always visible (not placeholder-only which disappears)
- **Error placement**: Error messages between label and input, or immediately after input
- **Auto-focus on first error**: When form submits with errors, focus the first error field

---

## 7. Accessible Navigation

### Navigation Patterns

**Skip link**: Allow keyboard users to skip navigation

```html
<a href="#main-content" class="skip-link">
  Skip to main content
</a>
```

**Current page indicator**:

```html
<nav aria-label="Main navigation">
  <ul>
    <li><a href="/dashboard" aria-current="page">Dashboard</a></li>
    <li><a href="/projects">Projects</a></li>
    <li><a href="/settings">Settings</a></li>
  </ul>
</nav>
```

**Breadcrumbs**:

```html
<nav aria-label="Breadcrumb">
  <ol>
    <li><a href="/">Home</a></li>
    <li><a href="/projects">Projects</a></li>
    <li aria-current="page">Current Project</li>
  </ol>
</nav>
```

### Accessible Dropdowns

```html
<div class="dropdown">
  <button 
    aria-haspopup="true" 
    aria-expanded="false"
    id="dropdown-button"
  >
    Menu
  </button>
  <ul 
    role="menu" 
    aria-labelledby="dropdown-button"
    hidden
  >
    <li role="menuitem"><a href="/profile">Profile</a></li>
    <li role="menuitem"><a href="/settings">Settings</a></li>
    <li role="menuitem"><button>Log out</button></li>
  </ul>
</div>
```

### Accessible Modals

```html
<div 
  role="dialog" 
  aria-modal="true"
  aria-labelledby="modal-title"
  aria-describedby="modal-description"
>
  <h2 id="modal-title">Confirm deletion</h2>
  <p id="modal-description">
    Are you sure you want to delete this project? This action cannot be undone.
  </p>
  <button>Delete</button>
  <button>Cancel</button>
</div>
```

Modal requirements:
- Focus is trapped inside the modal (Tab cycles within modal)
- Escape key closes the modal
- Focus returns to trigger when modal closes
- Modal content is announced to screen reader
- Background content is inert (not focusable)

Shadcn/ui Dialogs handle all of this automatically.

---

## 8. Motion and Animations

### Respecting User Preferences

Some users experience nausea, dizziness, or vestibular disorders from motion/animation. Use the `prefers-reduced-motion` media query:

```css
/* Reduce motion for users who prefer it */
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```

### Animation Guidelines

| Animation | Accessibility Concern | Mitigation |
|-----------|---------------------|------------|
| Auto-playing video | Distracting, can't be avoided | Add play button, no autoplay |
| Parallax scrolling | Nausea, disorientation | Disable when prefers-reduced-motion |
| Continuous animations | Distracting for ADHD users | Keep under 5 seconds, or allow pause |
| Flashing content | Seizure trigger (3 flashes/sec max) | Never use rapid flashing |
| Page transitions | Disorienting | Keep under 300ms, simple |

### Accessible Loading States

```html
<!-- Loading spinner with screen reader announcement -->
<div role="status" aria-live="polite">
  <Spinner />
  <span class="sr-only">Loading your data...</span>
</div>

<!-- Skeleton loading -->
<div aria-busy="true">
  <div class="skeleton h-8 w-48"></div>
  <div class="skeleton h-4 w-full mt-4"></div>
  <div class="skeleton h-4 w-3/4 mt-2"></div>
</div>
```

---

## 9. Accessibility in Your Design System

### Using Accessible Component Libraries

If you use shadcn/ui (built on Radix UI), most accessibility is handled for you:

**What shadcn/ui provides**:
- Proper ARIA attributes
- Keyboard navigation
- Focus management
- Screen reader announcements
- Role mappings

**What you still need to do**:
- Write meaningful alt text for images
- Ensure sufficient color contrast
- Write clear, descriptive labels
- Structure content with proper headings
- Test with real assistive technology

### Custom Components

When building custom components, follow the ARIA Authoring Practices Guide (APG):

```jsx
// Accessible accordion component
function Accordion({ title, children }) {
  const [isOpen, setIsOpen] = useState(false)
  const panelId = useId()
  const triggerId = useId()

  return (
    <div>
      <h3>
        <button
          id={triggerId}
          aria-expanded={isOpen}
          aria-controls={panelId}
          onClick={() => setIsOpen(!isOpen)}
        >
          {title}
        </button>
      </h3>
      <div
        id={panelId}
        role="region"
        aria-labelledby={triggerId}
        hidden={!isOpen}
      >
        {children}
      </div>
    </div>
  )
}
```

---

## 10. Testing with Assistive Technology

### Screen Reader Testing

**Required testing**:
1. Test your core flows with at least one screen reader
2. Test on both desktop (NVDA or JAWS on Windows, VoiceOver on Mac) and mobile (VoiceOver on iOS, TalkBack on Android)
3. Test all states: loading, empty, error, success

**Screen reader testing checklist**:
- [ ] All content is read in logical order
- [ ] All interactive elements are announced correctly
- [ ] Dynamic content changes are announced
- [ ] Error messages are announced
- [ ] Modals and overlays announce their content
- [ ] Navigation by headings works (H key in NVDA/VoiceOver)
- [ ] Navigation by landmarks works
- [ ] Forms can be completed with screen reader only

### Keyboard-Only Testing

**Process**:
1. Unplug your mouse or disable your trackpad
2. Navigate your entire product using only keyboard
3. Complete core flows (signup, create, edit, delete)
4. Note every issue

**Keyboard testing checklist**:
- [ ] Can I navigate to every interactive element?
- [ ] Is the focus indicator always visible?
- [ ] Is the focus order logical?
- [ ] Can I complete all core flows?
- [ ] Can I close all modals/popups? (Escape key)
- [ ] Can I use all dropdowns and menus?
- [ ] No keyboard traps (stuck on an element)?

### Automated Testing

Set up automated checks to catch regressions:

```bash
# Run axe in CI
npx axe https://your-saas.com --exit --show-errors

# Lighthouse CI
npx lhci collect && npx lhci assert
```

---

## 11. Accessibility Implementation Priority

### MVP (Minimum Viable Accessible)

**Must do** (WCAG A level):
1. All images have alt text (decorative: alt="")
2. All form fields have labels
3. All interactive elements are keyboard accessible
4. Color is not the only indicator of information
5. Page has a title (`<title>` element)
6. Language is specified (`<html lang="en">`)
7. Links have meaningful text (not "click here")
8. Error messages are clear and descriptive

### Growth (WCAG AA level)

**Should do**:
1. Sufficient color contrast (4.5:1 text, 3:1 large text)
2. Visible focus indicators
3. Proper heading hierarchy
4. ARIA landmarks for navigation
5. Skip navigation link
6. Accessible modals and popups
7. Form error association (aria-describedby)
8. Captions for video content
9. Consistent navigation throughout
10. Identify and fix all automated tool violations

### Scale (WCAG AAA level)

**Nice to have**:
1. Enhanced contrast (7:1)
2. Sign language for video content
3. Extended time limits configurable
4. Pre-recorded audio descriptions
5. Section headings for all content sections

---

## 12. Accessibility Statement

### Creating an Accessibility Statement

An accessibility statement shows users and regulators that you care about accessibility.

```
# Accessibility Statement for [Product Name]

## Our Commitment
[Product Name] is committed to ensuring digital accessibility for people 
with disabilities. We are continually improving the user experience for 
everyone, and applying the relevant accessibility standards.

## Conformance Status
The Web Content Accessibility Guidelines (WCAG) define requirements for 
designers and developers to improve accessibility for people with 
disabilities. [Product Name] aims to conform to WCAG 2.1 Level AA.

## Known Limitations
- [List any known issues and when you plan to fix them]
- [Example: Some older dashboards may have color contrast issues]

## Feedback
We welcome your feedback on the accessibility of [Product Name]. 
Please let us know if you encounter accessibility barriers:

- Email: accessibility@yourproduct.com
- Phone: [optional]
- [Any other contact method]

## Technical Specifications
Accessibility of [Product Name] relies on the following technologies:
- HTML
- WAI-ARIA
- CSS
- JavaScript

## Assessment Approach
We assess accessibility through:
- Automated testing (axe DevTools)
- Manual testing by our team
- Periodic external audits

## Date
This statement was last updated on [Date].
```

---

## 13. Quick Wins: This Week

### Day 1: Install Testing Tools
- Install axe DevTools browser extension
- Install WAVE browser extension

### Day 2: Run First Scan
- Scan your landing page, signup flow, dashboard
- Fix all "Critical" and "Serious" issues
- Most are quick fixes (alt text, labels, contrast)

### Day 3: Keyboard Test
- Navigate your core flows without a mouse
- Fix focus indicators if missing
- Ensure Tab order is logical

### Day 4: Screen Reader Test
- Test core flows with NVDA (Windows) or VoiceOver (Mac)
- Fix major navigation issues

### Day 5: Set Up CI
- Add axe to your CI/CD pipeline
- Create a baseline and track violations

### Day 6: Write Accessibility Statement
- Draft your accessibility statement
- Publish it on your site (footer link)

### Day 7: Create Issue Tracker
- Document remaining accessibility issues
- Prioritize and schedule fixes

---

## 14. The Solo Accessibility Manifesto

1. **A11y is not optional** — It's a fundamental quality requirement
2. **Start early** — Fixing a11y in code is cheap; retrofitting is expensive
3. **Use accessible component libraries** — shadcn/ui, Radix, Headless UI
4. **Test with real tools** — Automated + keyboard + screen reader
5. **Write semantic HTML** — It's the foundation of accessibility
6. **Respect user preferences** — prefers-reduced-motion, prefers-color-scheme, prefers-contrast
7. **Communicate clearly** — Labels, instructions, error messages
8. **Don't use color alone** — Always pair with text, icons, or patterns
9. **Design for keyboard** — Every interaction should work without a mouse
10. **Accessibility is ongoing** — Test after every change, not once

Accessibility isn't a feature you bolt on at the end. It's a quality attribute of good software. Building an accessible SaaS from the start costs little extra time, saves enormous effort later, and makes your product better for everyone.
