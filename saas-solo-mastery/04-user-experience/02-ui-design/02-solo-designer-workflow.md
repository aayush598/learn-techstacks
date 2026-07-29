# Solo Designer Workflow

## Designing When You're Not a Designer

Most solo founders are not designers. They're developers, marketers, or domain experts who need to build a UI because there's no one else to do it. This guide is for you: how to produce professional-quality UI design without a design background, without a design team, and without spending months learning design tools.

The core insight: **You don't need to be a good designer. You need to be a good assembler of pre-made design decisions.** The best solo-designed products don't invent new design patterns—they combine existing patterns effectively.

---

## 1. The Solo Design Mindset

### Design is a Skill, Not a Talent

Design is a learnable skill like any other. You don't need to be born with an "eye for design." You need to:
- Learn a few fundamental principles
- Use good tools and templates
- Follow established patterns
- Get feedback and iterate

The bar for "good enough" design in B2B SaaS is surprisingly low. Most SaaS products have mediocre UI. If yours is clean, consistent, and functional, you're already above average.

### The 80/20 of Design

20% of design knowledge gives you 80% of the results:

1. **Consistency**: Use the same patterns everywhere
2. **Hierarchy**: Make important things prominent
3. **Whitespace**: Don't crowd elements
4. **Alignment**: Everything should line up
5. **Contrast**: Text should be readable
6. **Color restraint**: Use 1-2 colors max
7. **Typography**: One font, 3 sizes max

That's it. Master these seven things and your product will look better than 90% of solo-built SaaS.

### You Are Not Your User

The biggest design mistake solo founders make is designing for themselves. You know your product inside and out. You know what every button does. Your users don't. Always design for the person seeing your product for the first time.

---

## 2. The Design Workflow for Non-Designers

### The Solo Design Pipeline

```
Research → Sketch → Wireframe → Prototype → Build → Review
  (30 min)  (30 min)  (1-2 hrs)   (1 hr)     (done)  (30 min)
```

Each step is lightweight. The goal is not pixel-perfect mockups—it's a shared understanding of what to build. Skip steps at your own risk.

### Step 1: Research (30 min)

Before opening any design tool:
1. **Look at 3 competitors**: Screenshot their similar page/feature
2. **Identify patterns**: What do they all do the same? (That's the convention.)
3. **Note differentiators**: What does one do differently that you like?
4. **Save to a reference board**: Miro, Notion, or even a folder of screenshots

### Step 2: Sketch (30 min)

On paper, whiteboard, or tablet:
1. Draw rough boxes for each section
2. Label what goes in each box
3. Draw arrows for user flow
4. Note interactions (click, hover, drag)
5. Take a photo and move on

Don't worry about beauty. The sketch is for you to think through the layout.

### Step 3: Wireframe (1-2 hours)

Using a tool (mention in section below):
1. Create boxes with rough labels
2. Use placeholder content
3. Define the layout structure
4. No colors, no images, no real text yet
5. Focus on information hierarchy

### Step 4: Prototype (1 hour)

Add interactivity:
1. Link screens together
2. Define click targets
3. Show transitions
4. Test the flow yourself
5. Share with 1-2 people for feedback

### Step 5: Build (Implementation)

This step happens in code:
1. Use your design system components (see design-systems-for-solo.md)
2. Implement the layout from wireframes
3. Add content and real data
4. Style with your design tokens
5. Test on real devices

### Step 6: Review (30 min)

After building:
1. Compare to your wireframe (does it match?)
2. Check for consistency (same patterns as rest of app)
3. Test on mobile
4. Check with a fresh set of eyes (even your own, after a break)
5. Fix any issues before shipping

---

## 3. Design Tools for Solo Founders

### The Tool Stack

You don't need a complex toolchain. Here's the minimum:

**Essential** (free):
- **Figma**: Design, prototyping, collaboration (free tier is generous)
- **Excalidraw**: Hand-drawn wireframing (free, no account needed)
- **Pen and paper**: Quick sketching

**Nice to have**:
- **Unsplash / Pexels**: Stock photos
- **Humaaans / Open Peeps**: Illustration components
- **Coolors**: Color palette generator
- **Fontsource**: Self-hosted fonts

**Optional**:
- **Framer**: Design-to-code for simpler pages
- **Spline**: 3D for landing pages
- **Screen Studio**: Professional screen recordings

### Figma for Solo

Figma is the industry standard and works well for solo founders. Here's how to use it effectively:

**Setup (30 min)**:
1. Create a Figma account (free)
2. Duplicate a SaaS UI kit (search "SaaS Figma template")
3. Set up your pages: Landing, Dashboard, Settings, Pricing
4. Create component library from your design system (or use Community files)

**Workflow**:
1. Wireframe in Excalidraw (fast, no pressure)
2. Refine in Figma using your UI kit components
3. Use Auto Layout for responsive design
4. Create variants for component states
5. Use the Prototype tab for basic interactions
6. Share with dev mode (so you or others can inspect CSS)

**Figma plugins for solo**:
- **Iconify**: Access to thousands of icons
- **Unsplash**: Stock photos without leaving Figma
- **Content Reel**: Auto-generated content
- **Stark**: Accessibility/contrast checker
- **Fig to Tailwind**: Export to Tailwind classes
- **Batch Styler**: Bulk edit styles

### The "No-Figma" Alternative

If you don't want to learn Figma (and you don't need to—many solo founders never use it):

**Design in the browser**:
1. Use Tailwind Play (play.tailwindcss.com) to prototype
2. Build directly with shadcn/ui components
3. Adjust styles in real time
4. Copy code to your project

**Low-fi wireframing**:
- Excalidraw for layout
- Whimsical for flows
- Miro for whiteboarding

**Design directly in code**:
- Tailwind CSS utilities for styling
- Browser DevTools for tweaking
- shadcn/ui for components
- Preview branches for feedback

This is faster for developers and produces production-ready code, not mockups that need to be re-built.

---

## 4. Design Templates and Starting Points

### Why Templates Work

Using a template is not cheating. Every designer uses references and inspiration. Templates give you:
- A proven layout structure
- Professional typography and spacing
- Built-in responsive behavior
- A head start on implementation

### Finding Good Templates

**Free**:
- **Tailwind UI** component examples (free snippets)
- **shadcn/ui** examples
- **Cruip** (free Tailwind templates)
- **HTML5 UP** (responsive HTML templates)

**Paid**:
- **Tailwind UI** ($299 - full templates, worth every penny)
- **Cruip Pro** ($69 - excellent Tailwind templates)
- **ThemeForest** (variable quality, many SaaS templates)

**SaaS-specific templates**:
- SaaS landing page templates
- Dashboard/analytics layouts
- Pricing page templates
- Authentication screens
- User settings/profile pages

### The Template Customization Process

1. **Choose a template** that matches your needs
2. **Replace content** with your own (copy, images, data)
3. **Adapt branding** - swap colors and fonts
4. **Remove what you don't need** - simplify
5. **Add what's missing** - unique features
6. **Test and iterate**

Don't customize more than necessary. A good template with your content looks better than a heavily customized template.

---

## 5. Design Inspiration and Reference

### Where to Look for Inspiration

**SaaS-specific galleries**:
- SaaS Landing Page examples (saaslandingpage.com)
- Landing Folio (landingfolio.com)
- Really Good UX (reallygoodux.io)
- UI Movement (uimovement.com)
- Mobbin (mobile app patterns)
- Pages.xyz (SaaS pages)

**Design communities**:
- Dribbble (search "SaaS dashboard")
- Behance (search "web application UI")
- Uplabs (SaaS UI kits)

**Competitor analysis**:
- Sign up for 5 competing products
- Screenshot every screen
- Note what works and what doesn't
- Use as reference for your own design

### How to Use Inspiration Without Copying

1. Identify the **pattern**, not the pixel
2. Ask WHY a design works (good hierarchy? clear call-to-action?)
3. Extract the principle (not the visual)
4. Apply the principle in your own context

**Example**:
- Competitor has a blue "Get Started" button on a dark hero section
- Principle: High-contrast CTA on a value-focused headline
- Your application: Orange CTA on a navy hero with ROI-focused headline

### Building a Reference Library

Save screenshots and notes organized by:
- **Layout patterns**: Hero sections, feature grids, pricing tables
- **Component treatments**: Navigation, forms, cards
- **Interaction patterns**: Hover effects, transitions, scroll behaviors
- **Copy patterns**: Headlines, CTAs, testimonials

Use a simple folder structure or a tool like Eagle, Milanote, or even a Notion page.

---

## 6. From Design to Code

### The Handoff (To Yourself)

As a solo founder, you're both designer and developer. The handoff is from your designer brain to your developer brain. Make it easy for yourself:

**Design documentation** for each page:
1. Screenshot or Figma link
2. Component list (what components are on this page)
3. Content (headline, body copy, button text)
4. States (loading, empty, error, success)
5. Interactions (hover, click, animation)
6. Responsive behavior (how it looks on mobile)

### Design-to-Code Workflow

**Option 1: Direct CSS from Figma**
- Use Figma's "Inspect" tab to get CSS values
- Convert to Tailwind classes manually or with plugins
- Recreate layout with your components

**Option 2: Code-first design**
- Skip Figma entirely
- Design in browser with live reload
- Use Tailwind DevTools to tweak
- Save iterations as git commits

**Option 3: Copy from templates**
- Buy Tailwind UI or similar
- Copy the HTML/Tailwind code
- Adapt to your components
- Replace content

**Option 4: AI-assisted design**
- Describe what you want to Cursor/Copilot
- Generate component code
- Review and adapt
- Test in browser

### The CSS-Tailwind Conversion

Common CSS to Tailwind mapping:

```css
/* CSS */
.my-button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 8px 16px;
  border-radius: 6px;
  font-weight: 500;
  background-color: #6366f1;
  color: white;
}
```

```html
<!-- Tailwind -->
<button class="inline-flex items-center justify-center px-4 py-2 
               rounded-md font-medium bg-indigo-500 text-white">
```

---

## 7. Designing Common SaaS Pages

### Landing Page Hero

**Structure**:
1. Headline (your value proposition in 8 words)
2. Subheadline (what you do, who it's for)
3. CTA button (primary action)
4. Secondary CTA (learn more / see demo)
5. Hero image / video / illustration
6. Social proof bar (logos, testimonials)

**Design tips**:
- Center-aligned or left-aligned layout
- Maximum 2 lines for headline
- CTA should be the most visually prominent element
- Hero image should show the product in use
- Above the fold (no scroll on desktop)

### Dashboard

**Structure**:
1. Navigation (sidebar or top nav)
2. Header (page title, user menu, notifications)
3. Main content area (stats, data, actions)
4. Widget area (secondary information)

**Design tips**:
- Show the most important metric prominently
- Use cards for grouping information
- Only show 5-7 widgets maximum
- Include a clear primary action
- Use real data from day one (avoid lorem ipsum)

### Pricing Page

**Structure**:
1. Header (pricing headline, subheadline)
2. Plan comparison table / cards
3. Feature breakdown
4. FAQ section
5. CTA buttons per plan

**Design tips**:
- 3 plans maximum (confusing with more)
- Highlight recommended plan
- Annual/monthly toggle
- Clear feature lists with checkmarks
- Price anchoring (most popular highlighted)

### Settings Page

**Structure**:
1. Section navigation (tabs or sidebar)
2. Grouped settings with clear headings
3. Save button (or auto-save)
4. Cancel/reset option

**Design tips**:
- Group settings logically (Profile, Security, Billing, Notifications)
- Use clear, descriptive labels
- Show current state clearly
- Inline validation for critical fields
- Confirmation for destructive actions

---

## 8. Color for Developers

### The Solo Color Strategy

Don't spend hours choosing colors. Use this proven system:

**Primary color**: Pick one from a curated palette
- Blue: Trustworthy, professional (most SaaS)
- Green: Growth, financial (fintech, health)
- Purple: Creative, premium (design tools)
- Orange: Energetic, friendly (consumer apps)
- Red: Urgent, powerful (sales tools)

**Neutral palette**: Gray scale with a hint of your primary
- 50 - 950 scale from Tailwind or similar

**Semantic colors**:
- Green = Success
- Red = Error / Danger
- Yellow = Warning
- Blue = Information

**Accent color**: Secondary brand color, used sparingly

### The Color Formula

1. Pick one primary hue (e.g., Indigo 500 from Tailwind)
2. Use 5 shades: 50 (light bg), 100 (hover bg), 500 (primary), 700 (dark text), 900 (headers)
3. Gray scale for everything else
4. One accent color for highlights
5. Semantic colors as needed

```css
/* Example: Indigo theme */
--primary-50: #eef2ff;
--primary-100: #e0e7ff;
--primary-500: #6366f1;
--primary-700: #4338ca;
--primary-900: #312e81;

--gray-50: #f8fafc;
--gray-100: #f1f5f9;
--gray-200: #e2e8f0;
--gray-400: #94a3b8;
--gray-600: #475569;
--gray-800: #1e293b;
--gray-900: #0f172a;

--success: #22c55e;
--error: #ef4444;
--warning: #f59e0b;
--info: #3b82f6;
```

### Color Accessibility

Always check contrast:
- **AA normal text**: 4.5:1 contrast ratio
- **AA large text**: 3:1 contrast ratio
- **AAA normal text**: 7:1 contrast ratio

Use tools:
- WebAIM Contrast Checker
- Stark plugin for Figma
- Chrome DevTools contrast checker
- axe DevTools

### Dark Mode Strategy

If offering dark mode:
1. Define all colors as CSS variables
2. Create a dark color scheme
3. Use `prefers-color-scheme` media query
4. Add a manual toggle
5. Test all combinations

Tailwind makes this easy:
```css
:root {
  --bg-primary: #ffffff;
  --text-primary: #0f172a;
}

.dark {
  --bg-primary: #0f172a;
  --text-primary: #f8fafc;
}
```

---

## 9. Typography for Developers

### The Solo Typography Strategy

**One font** is enough. Two max.

**For body text**:
- Inter (free, great legibility, professional)
- System font stack (fast, no download)
- Open Sans or Source Sans (accessible)

**For headings**:
- Same as body (safe, consistent)
- A slightly bolder weight
- Or: a distinct display font (Cabinet Grotesk, Satoshi)

### Font Sizing System

```css
/* Proportional scale: 1.25 ratio */
--text-xs: 0.75rem;    /* 12px - small labels */
--text-sm: 0.875rem;   /* 14px - secondary text */
--text-base: 1rem;     /* 16px - body */
--text-lg: 1.125rem;   /* 18px - large body */
--text-xl: 1.25rem;    /* 20px - subheadings */
--text-2xl: 1.5rem;    /* 24px - section headings */
--text-3xl: 1.875rem;  /* 30px - page headings */
--text-4xl: 2.25rem;   /* 36px - hero headings */
```

### Line Height

```css
--leading-tight: 1.25;   /* Headings */
--leading-normal: 1.5;   /* Body text */
--leading-relaxed: 1.625; /* Large body text */
```

### Line Length

- Maximum 66-75 characters per line for readability
- Use `max-w-prose` in Tailwind (`65ch`)
- Wider for data-heavy interfaces

### Typography Tips

- Avoid text under 12px (except legal)
- Use uppercase sparingly (for labels only)
- Don't center-align body text (hard to read)
- Use font-weight: 400 for body, 600 for emphasis, 700 for headings
- Avoid underlining (it's for links)
- Limit to 3 font sizes per page

---

## 10. Layout and Composition

### The Solo Layout System

**Use a grid**:
- 12-column grid for flexibility
- 24px gutter between columns
- 80px max content width (1200px for desktops)

**Spacing system** (4px base):
```css
--space-1: 4px;
--space-2: 8px;
--space-3: 12px;
--space-4: 16px;
--space-5: 20px;
--space-6: 24px;
--space-8: 32px;
--space-10: 40px;
--space-12: 48px;
--space-16: 64px;
--space-20: 80px;
```

### Layout Principles

**Visual hierarchy** (most to least important):
1. Primary headline/action (largest, boldest)
2. Secondary headings
3. Body content
4. Navigation
5. Secondary actions
6. Legal/Footer

**The F-Pattern**: Users scan in an F shape:
- First they read the top line fully
- Then they scan down the left side
- They read occasional lines fully

Place important content along these paths.

**Whitespace**:
- Too little: feels cramped, overwhelming
- Too much: feels empty, hard to scan
- Right amount: feels premium, easy to digest

Rule of thumb: if it feels slightly too spacious, it's probably right.

---

## 11. Common Design Mistakes and Fixes

### Mistake 1: Too Many Colors

**Problem**: Using 5+ colors throughout the interface

**Fix**: Limit to 1 primary, 1 neutral, 1 accent, 4 semantic

### Mistake 2: Inconsistent Spacing

**Problem**: Random margins and padding (10px here, 15px there)

**Fix**: Use a spacing scale (4, 8, 12, 16, 24, 32, 48, 64) exclusively

### Mistake 3: No Visual Hierarchy

**Problem**: Everything is the same size and weight

**Fix**: Make important elements noticeably larger/bolder

### Mistake 4: Too Many Fonts

**Problem**: 3+ different fonts on the same page

**Fix**: One font for everything, or one for headings and one for body

### Mistake 5: Low Contrast Text

**Problem**: Gray text on gray background

**Fix**: Use the 50/900 rule: text is gray-900 on gray-50 backgrounds

### Mistake 6: Cluttered Interface

**Problem**: Too many elements competing for attention

**Fix**: Remove anything that's not essential. When in doubt, take it out.

### Mistake 7: Inconsistent Button Styles

**Problem**: Different button styles for the same type of action

**Fix**: Define 4 button variants (primary, secondary, outline, ghost) and use them consistently

### Mistake 8: No Empty States

**Problem**: "No data" shows a blank page

**Fix**: Always design empty states with helpful guidance

### Mistake 9: Missing Hover and Focus States

**Problem**: Interactive elements don't respond to interaction

**Fix**: Always add hover (darken), focus (ring), and active (press) states

### Mistake 10: Copy That's Too Long

**Problem**: Paragraphs of text describing what the button does

**Fix**: Cut copy by 50%. Users don't read, they scan.

---

## 12. Getting Design Feedback Without a Designer

### Self-Review Checklist

Before asking anyone else:
- [ ] Is there a clear hierarchy? (most important thing is most prominent)
- [ ] Are colors consistent? (no random color usage)
- [ ] Is spacing consistent? (no random margins)
- [ ] Are fonts consistent? (no mixing)
- [ ] Is the primary action obvious?
- [ ] Are all states handled? (loading, empty, error, success)
- [ ] Does it work on mobile?
- [ ] Is the contrast adequate?
- [ ] Are interactive elements clearly interactive?
- [ ] Is the copy clear and concise?

### Getting Feedback from Users

Ask specific questions:
- "What would you click first?"
- "What does this page do?" (5-second test)
- "What's confusing?"
- "Where would you expect to find [feature]?"

Don't ask: "Do you like it?" (Users will say yes to be nice.)

### Getting Feedback from Other Founders

Trade design reviews with another solo founder:
1. You review their UI (you have fresh eyes)
2. They review your UI (they have fresh eyes)
3. Focus on the checklist above
4. Be honest but constructive

---

## 13. Tools and Resources Summary

### Design Tools

| Tool | Cost | Use |
|------|------|-----|
| Figma | Free | Full design, prototyping |
| Excalidraw | Free | Quick wireframing |
| Penpot | Free | Open source Figma alternative |
| Canva | Free | Landing page graphics |
| Photopea | Free | Photoshop alternative |

### Design Assets

| Resource | Cost | Use |
|----------|------|-----|
| Unsplash | Free | Stock photos |
| Icons8 | Free | Icons |
| Lucide | Free | Open source icons |
| Humaaans | Free | Illustration components |
| Open Peeps | Free | Illustration library |
| Blush | Free | Customizable illustrations |

### Design Learning

| Resource | Cost | Use |
|----------|------|-----|
| Refactoring UI ($99) | Paid | Best design book for devs |
| Learn UI Design (scrimba) | Free | Interactive tutorials |
| DesignCourse (YouTube) | Free | Practical design tutorials |
| Flux Academy (YouTube) | Free | Design for non-designers |

### Design Systems

| System | Cost | Use |
|--------|------|-----|
| shadcn/ui | Free | React components |
| Tailwind UI | $299 | Full templates |
| Radix UI | Free | Unstyled accessible components |
| Primer (GitHub) | Free | Open source design system |

---

## 14. Building Design Skills Over Time

### The Solo Design Learning Path

**Month 1**: Learn to use a design system (Tailwind + shadcn/ui)
**Month 2**: Learn basic layout principles (hierarchy, spacing, grids)
**Month 3**: Learn color theory (palette creation, contrast)
**Month 4**: Learn typography (fonts, sizing, line-height)
**Month 5**: Learn prototyping in Figma (optional but useful)
**Month 6**: Learn design critique (reviewing your own work)

Each month, spend 2-3 hours on design learning. That's 12-18 hours total over 6 months. For that investment, you'll have professional-quality design skills that serve you for every product you ever build.

### Daily Design Practice

- **5 minutes**: Browse one SaaS design gallery
- **10 minutes**: Critique one competitor screen
- **15 minutes**: Tweak one part of your UI
- **Weekly**: Design one small component from scratch
- **Monthly**: Full design audit of your product

You don't need to become a professional designer. You need to become good enough to build a professional-looking product. With the systems, templates, and workflows in this guide, you can get there faster than you think.
