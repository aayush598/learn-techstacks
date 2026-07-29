# Selling Code Templates & Developer Products

## Why Code Templates Are the Ultimate Passive Income

Code templates have near-zero marginal cost, infinite scalability, and a global market of developers who will pay for time saved.

**The product types covered in this guide:**
- UI kits & component libraries
- Boilerplates & starter kits
- WordPress themes & plugins
- VS Code extensions
- CLI tools & scripts
- Design system packages
- API wrappers & SDKs

---

## UI Kits & Component Libraries

### What Sells Best

**1. Tailwind Component Libraries ($29-$149)**
Pre-built components using Tailwind CSS. Every developer needs them.

Best sellers:
- SaaS landing page components (hero, features, pricing, FAQ, CTA)
- Admin dashboard components (tables, charts, sidebar, header)
- E-commerce components (product cards, cart, checkout)
- Form components (inputs, selects, multi-step, validation)
- Marketing site components (blog cards, testimonials, team)

**2. React Component Libraries ($49-$199)**
Production-ready React components with TypeScript.

Best sellers:
- Data tables with sorting, filtering, pagination
- Form builders with validation
- Modal/dialog systems
- Drag-and-drop interfaces
- Charts and data visualization
- Calendar/date picker components

**3. Vue/Nuxt Component Libraries ($49-$149)**
Same as React but for the Vue ecosystem.

**4. Figma to Code Libraries ($39-$99)**
Design system components available in both Figma and code.

### Building a UI Kit

**Structure:**

```
ui-kit-name/
  src/
    components/
      Button/
        Button.tsx
        Button.stories.tsx
        Button.test.tsx
        variants.ts
      Card/
        Card.tsx
        Card.stories.tsx
      Modal/
        Modal.tsx
        Modal.stories.tsx
      ...
  dist/          # Compiled output
  docs/          # Documentation site
  tailwind.config.js  # If using Tailwind
  package.json
  README.md
  LICENSE.md
```

**Key features that command higher prices:**
- TypeScript support (mandatory for $50+)
- Storybook documentation
- Unit tests
- Accessibility (a11y) compliance
- Dark mode support
- Responsive design
- Animation/transition support
- Customization via theme tokens

### Pricing UI Kits

| Kit Type | Price | Units (Year 1) | Revenue |
|----------|-------|----------------|---------|
| Basic (20-30 components) | $49 | 200 | $9,800 |
| Standard (50-80 components) | $99 | 300 | $29,700 |
| Premium (100+ components) | $199 | 150 | $29,850 |
| Enterprise (source + license) | $499 | 30 | $14,970 |

**Best seller:** $99 standard kit. 300 sales = $29,700/year.

### Distribution

1. **Gumroad/Lemon Squeezy** (83-89% payout)
2. **UI marketplace** (ThemeForest $15-$60, 50-70% cut)
3. **Your own site** (100% margin, hardest to get traffic)
4. **GitHub Sponsors** (free for open-source version, paid for pro)

### Marketing UI Kits

- Live demo site showing all components in action
- Side-by-side comparison: "Before (plain) vs After (your kit)"
- "Built with this kit" showcase featuring real projects
- Free starter kit (5 components) -> upsell full kit
- Tutorial: "How to build a landing page in 30 minutes with [kit]"

---

## Boilerplates & Starter Kits

### High-Demand Boilerplate Types

**1. SaaS Boilerplate ($79-$299)**
The most popular boilerplate category.

Includes:
- User authentication (email + social)
- Subscription billing (Stripe)
- Database ORM + migrations
- API routes with auth middleware
- Admin dashboard
- Landing page
- Email templates
- Deployment config

**2. Full-Stack App Boilerplate ($49-$149)**
For general web applications.

Includes:
- Auth system
- CRUD patterns
- File uploads
- Search functionality
- Pagination
- Error handling
- Logging

**3. API Boilerplate ($49-$149)**
Backend API starter.

Includes:
- Auth (JWT or session-based)
- Rate limiting
- Request validation
- API documentation (Swagger/OpenAPI)
- Error handling
- Database models
- Testing setup

**4. WordPress Plugin Boilerplate ($29-$79)**
Modern WordPress plugin development.

Includes:
- Plugin structure
- Custom post types
- Gutenberg blocks
- REST API endpoints
- Settings pages
- Shortcodes
- Internationalization

**5. Mobile App Boilerplate ($79-$299)**
React Native or Flutter.

Includes:
- Navigation setup
- Auth flow
- API integration
- State management
- Push notifications
- Deep linking
- Theme system

### What Makes a Boilerplate Worth $149+

| Feature | $49 | $99 | $149 | $299 |
|---------|-----|-----|------|------|
| Auth (email) | Yes | Yes | Yes | Yes |
| Auth (social) | No | Yes | Yes | Yes |
| Stripe integration | No | Basic | Full (webhooks, portal) | Full + multi-plan |
| Database | SQLite | PostgreSQL | PostgreSQL + Redis | Multi-DB support |
| UI components | Minimal | Basic kit | Full kit | Full + animated |
| Testing | No | Basic | Comprehensive | Full CI/CD |
| Documentation | README | README + guides | Full docs site | Docs + video |
| Updates | None | 6 months | 12 months | Lifetime |
| Support | Email | Email + Discord | Priority | Slack + calls |

### Boilerplate Pricing Strategy

| Tier | Price | What You Get | Target Buyer |
|------|-------|-------------|--------------|
| Lite | $49 | Core features, basic docs | Budget-conscious |
| Pro | $149 | Everything, 12 months updates | Serious builders |
| Premium | $299 | Everything + lifetime + priority | Agency/enterprise |
| Commercial | $999 | Extended license, source code | Companies |

**The decoy effect:**
- Lite ($49) - basic, no updates
- Pro ($149) - full features, 12 months updates (YOUR TARGET)
- Premium ($299) - lifetime updates, Discord access

Pro looks like the best value. Premium makes Pro look reasonable. Lite makes Pro look like more.

### Pre-Built Demo Requirement

Every boilerplate must have a LIVE demo:
- Deployed on Vercel/Netlify
- Fully functional
- Admin login credentials in README
- Real data pre-populated

**Without a live demo, your conversion rate drops by 60%.**

### Building in Public for Boilerplates

Document your boilerplate build process on Twitter:

```
Day 1: Started building [Boilerplate]. Structure decided.
Day 3: Auth is working. Email + Google login.
Day 5: Stripe integration done. Webhooks handling subscriptions.
Day 7: Admin dashboard coming together. 15 components so far.
Day 10: Documentation site live. First 50 pages written.
Launch: Pre-orders open. $99 launch price.

Result: 200 pre-orders in 2 weeks = $19,800 before launch.
```

---

## WordPress Themes & Plugins

### The WordPress Market

WordPress powers 43% of all websites. The theme and plugin market is massive:

- ThemeForest: 50,000+ themes, top sellers make $50k-$500k/year
- Plugin market: Top plugins on WordPress.org have 1M+ downloads
- Premium plugins: $29-$199/year per site

### WordPress Theme Types That Sell

| Theme Type | Price | Monthly Sales (Top 10%) | Monthly Revenue |
|-----------|-------|------------------------|-----------------|
| Multipurpose | $59-$89 | 500-2,000 | $30k-$180k |
| Blog/Magazine | $39-$69 | 300-1,000 | $12k-$69k |
| E-commerce | $59-$89 | 400-1,500 | $24k-$134k |
| Business/Corporate | $49-$79 | 300-800 | $15k-$63k |
| Portfolio/Creative | $39-$59 | 200-600 | $8k-$35k |
| LMS/Education | $49-$79 | 100-400 | $5k-$32k |
| Membership | $59-$89 | 100-300 | $6k-$27k |

### WordPress Plugin Types That Sell

| Plugin Type | Price | Market Size |
|------------|-------|-------------|
| Page builder add-ons | $29-$99 | Very large |
| SEO tools | $49-$199 | Large |
| Security | $39-$149 | Large |
| Performance optimization | $29-$79 | Large |
| Membership/subscription | $49-$199 | Medium-large |
| LMS add-ons | $49-$149 | Medium |
| Booking/appointment | $39-$99 | Medium |
| Directory/listings | $49-$149 | Medium |
| Multi-vendor marketplace | $99-$299 | Small-medium |
| Automation/workflow | $29-$79 | Medium |

### The Agency Business Model for Themes

Build a theme, sell it to agencies who white-label it:

"Build your client sites 3x faster with [Theme]. White-label it as your own. One license covers unlimited client sites."

- Your price to agency: $199/year
- Agency builds 20 client sites/year with your theme
- Value to agency: 20 sites x 10 hours saved x $100/hr = $20,000 saved
- Your annual recurring revenue: $199 x 500 agencies = $99,500/year

### Theme Development Best Practices

**Must-haves for a successful theme:**
1. Clean, modern design (first impression matters most)
2. Responsive (60%+ of traffic is mobile)
3. Fast loading (under 1 second on demo)
4. SEO-optimized markup
5. WooCommerce compatible (even for non-ecommerce themes)
6. Translation-ready (international market)
7. Customizer settings (not bloated options panels)
8. Demo import with 1 click
9. Regular updates (WordPress core changes constantly)
10. Support forum (required by ThemeForest)

### Publishing on ThemeForest

**Steps:**
1. Create an Envato account
2. Apply to become an author (takes 1-3 weeks)
3. Build your theme according to their requirements
4. Submit for review (2-4 weeks)
5. Pass quality checks (70% fail on first submission)
6. Start selling (70-30 revenue split in your favor)

**Revenue split:** 70% to you (first $3,750), then 82.5% to you
**Pricing:** Fixed price $39-$89 for most themes
**Exclusivity:** Non-exclusive allowed (sell anywhere)

---

## VS Code Extensions

### Why Build VS Code Extensions

- 70%+ of developers use VS Code
- Extension marketplace has 30,000+ extensions
- Good extensions get 10k-500k installs
- Monetize through: paid extensions, sponsorships, premium features

### Extension Types That Make Money

**1. Snippet Extensions ($5-$19)**
Language/framework-specific code snippets.

Examples:
- React snippet pack: $9 (50k+ installs at $9 = $450k)
- Go snippets: $5
- Laravel snippets: $9
- CSS animation snippets: $9

**2. Theme Packs ($5-$19)**
Premium color themes with unique designs.

Examples:
- Dracula Official (free) -> premium variant
- Material Theme (free) -> premium icon pack
- Custom theme for companies

**3. Productivity Extensions ($9-$49)**
Tools that save developer time.

Examples:
- Git history viewer
- TODO highlighter
- Color picker
- Image preview
- Code timer/analytics

**4. Integration Extensions ($19-$99)**
Connect VS Code to external services.

Examples:
- Jira integration
- Linear integration
- Notion integration
- Azure DevOps integration
- AWS SSM parameter browser

### Monetization Models

**1. Free + Sponsorship (Open Source)**
- Extension is free
- Add "Sponsor" link in extension
- GitHub Sponsors / Open Collective
- Income: $100-$2,000/month

**2. Freemium (Best for Extensions)**
- Basic features free
- Premium features paid
- Use VS Code's built-in payment system
- Income: $500-$10,000/month

**3. Paid Extension**
- $5-$49 one-time purchase
- Must provide significant value
- Income: $1,000-$20,000/month

**4. Enterprise License**
- Company-wide license
- $99-$999/year per company
- Income: $5,000-$50,000/year

### Building a VS Code Extension

**Quick start:**
```
npx yo code  # Yeoman generator for VS Code extensions
```

**Structure:**
```
my-extension/
  src/
    extension.ts     # Entry point
    commands/        # Command handlers
    providers/       # Tree views, etc.
    snippets/        # Code snippets
  package.json       # Extension manifest
  README.md          # Marketplace listing
  CHANGELOG.md       # Update log
  .vscodeignore      # What to exclude from package
```

### Marketing VS Code Extensions

- **Marketplace SEO:** Title, description, tags optimized for search
- **GitHub repo:** Each star = free marketing
- **Twitter:** Show your extension in action in coding videos
- **Reddit:** r/vscode, r/webdev (post useful tips using your extension)
- **YouTube:** "5 VS Code extensions you need" -> include yours
- **Blog posts:** "I built a VS Code extension that saved me [X] hours"

### Case Study: $5,000/month from a VS Code Extension

**Developer:** Senior frontend engineer
**Extension:** React snippet pack ($9)
**Users:** 80,000 installs

**Monetization:**
- 80k installs x 2% conversion to paid = 1,600 purchases
- 1,600 x $9 = $14,400 (first year)
- Renewals/updates: 500 purchases/year = $4,500
- Sponsorship from companies: $1,000/month
- **Total: ~$5,000/month**

**Time investment:**
- Initial build: 40 hours
- Maintenance: 2 hours/month
- Marketing: 4 hours/month
- **Hourly rate at scale: $5,000/month / 24 hours = $208/hour**

---

## CLI Tools & Scripts

### CLI Tools That Sell

Developers love the command line. CLI tools that solve specific problems sell well.

**Best-selling CLI tools:**
- Project scaffolding tools: "Create [framework] app" (like create-react-app but for niche stacks)
- Deployment tools: One-command deploy to various hosts
- Code generators: Generate boilerplate code for APIs, models, etc.
- Data migration tools: Transfer data between services
- Testing utilities: Generate test data, run bulk tests

### Pricing CLI Tools

| Type | Price | Sales Volume | Total Revenue |
|------|-------|-------------|---------------|
| Simple script | $9-$29 | 1,000-5,000 | $9k-$145k |
| Full CLI tool | $29-$99 | 500-2,000 | $15k-$198k |
| Pro version | $99-$299 | 100-500 | $10k-$150k |
| Enterprise license | $499-$999 | 20-100 | $10k-$100k |

### Distribution for CLI Tools

- **npm/PyPI/Homebrew:** Package manager distribution
- **GitHub:** Open source the base, sell the pro version
- **Product Hunt:** Launch for developer audience
- **Awesome lists:** Get listed on relevant "awesome" lists

---

## Design System Packages

### What They Are

Complete design systems with components, tokens, and documentation. Companies pay $500-$5,000+ for a design system that would cost $50k+ to build internally.

### Design System Components

A complete design system package includes:

1. **Design tokens** (colors, spacing, typography, shadows, breakpoints)
2. **Component library** (buttons, inputs, cards, modals, navigation)
3. **Pattern library** (common page layouts, form patterns, data display)
4. **Documentation** (usage guidelines, code examples, best practices)
5. **Figma file** (design components matching code components)
6. **Storybook** (interactive component playground)
7. **Theme customization** (brand colors, fonts, spacing)

### Pricing Design Systems

| Tier | Price | Includes | Target |
|------|-------|----------|--------|
| Starter | $299 | Core components, basic docs | Solo devs |
| Professional | $999 | Full system, Figma, Storybook | Small teams |
| Enterprise | $4,999 | Custom branding, training, support | Companies |

### The Agency Model for Design Systems

Agencies pay $999-$4,999 for a design system that lets them:
- Deliver projects 3x faster
- Maintain consistent quality
- Onboard new designers/devs in hours, not weeks
- Present a professional system to clients

"Your agency needs a design system. Building one costs $50k+ and takes 6 months. Ours costs $999 and works today."

---

## API Wrappers & SDKs

### What They Are

Thin code layers on top of popular APIs that make them easier to use. Developers pay for convenience and speed.

### Best-Selling API Wrappers

**1. Payment Gateway Wrappers ($29-$99)**
- Stripe SDK for [language]
- PayPal integration helper
- Multi-payment gateway abstraction layer

**2. Shipping API Wrappers ($29-$79)**
- UPS/FedEx/USPS unified API
- Shipping rate comparison
- Label generation helper
- E-commerce shipping integration

**3. Social Media API Wrappers ($19-$59)**
- Twitter/X API helper
- Instagram posting tool
- LinkedIn automation (within API limits)
- Multi-platform social poster

**4. Email Service Wrappers ($19-$49)**
- SendGrid/Mailgun/SES unified interface
- Email template manager
- Newsletter sending helper

**5. AI/ML API Wrappers ($29-$99)**
- OpenAI API with retry logic, rate limiting
- Multi-AI provider abstraction
- Prompt template system

### Building and Selling API Wrappers

**Key to success:** Solve a specific pain point. "I got tired of rewriting Stripe integration code for every project, so I built this."

**Structure:**
```
api-wrapper/
  src/
    client.ts         # HTTP client with retry, rate limiting
    resources/        # API resource handlers
    types.ts          # TypeScript types
    errors.ts         # Custom error handling
  tests/
  examples/
  README.md
  package.json
```

### Pricing API Wrappers

| Tier | Price | What's Included |
|------|-------|-----------------|
| Free (OSS) | $0 | Basic wrapper, limited docs |
| Pro | $49 | Full wrapper, TypeScript, examples |
| Team | $149 | Pro + team support, priority bug fixes |
| Enterprise | $499 | Team + custom integrations, SLA |

---

## Digital Product Launch Strategy

### Pre-Launch (2-4 Weeks Before)

1. **Build a waitlist** - Landing page with email capture
2. **Share progress** - Daily Twitter updates on your build
3. **Beta testers** - Give 10-20 people free access in exchange for feedback
4. **Collect testimonials** - From beta testers (critical for conversion)
5. **Prepare assets** - Screenshots, demo video, pricing page, documentation

### Launch Week

1. **Product Hunt launch** (if applicable)
   - Best for developer tools
   - Schedule for Tuesday-Thursday
   - Have 10+ people ready to comment
   - Prepare FAQ and respond quickly

2. **Email list announcement**
   - Send to your entire list
   - Launch discount (30-50% off for first 48 hours)
   - Clear CTA with direct link

3. **Social media blitz**
   - Twitter: Thread announcing launch
   - LinkedIn: Personal post
   - Reddit: Relevant subreddits (follow rules)
   - Dev.to: Launch post

4. **Community posts**
   - Indie Hackers
   - Hacker News (if you have a compelling story)
   - Relevant Slack/Discord communities
   - Niche Facebook groups

### Post-Launch (First 30 Days)

1. **Fix issues immediately** - Bugs from early adopters get priority
2. **Collect and publish testimonials** - Social proof drives sales
3. **Send update emails** - "We fixed X, added Y based on your feedback"
4. **Optimize conversion** - A/B test pricing page, improve copy
5. **Content marketing** - Tutorials showing how to use your product

---

## Distribution Channels

### Marketplace Distribution

| Marketplace | Cut | Traffic | Best For |
|-------------|-----|---------|----------|
| Gumroad | 8-17% | Medium | Code, templates, courses |
| Lemon Squeezy | 11% + $0.50 | Medium | Code, SaaS products |
| ThemeForest | 30-50% | High | WordPress themes |
| CodeCanyon | 30-50% | High | Plugins, scripts |
| VS Code Marketplace | 0% (free) | Very high | Extensions |
| GitHub Marketplace | 0% | High | Actions, apps |
| npm | 0% | Very high | Packages (free) |
| Product Hunt | 0% | High (one-time) | All products |

**Best strategy:** Sell on your own site (highest margin) AND list on marketplaces (traffic). Use marketplaces for discovery, upsell to your direct channel.

### Own Site Distribution

**Traffic sources for your own site:**
1. SEO (content marketing) - slow but compounding
2. Social media - Twitter/X is best for developer products
3. Email list - your most valuable asset
4. Referrals - happy customers telling others
5. Partnerships - cross-promotion with complementary products

---

## Pricing Strategies for Code Products

### Value-Based Pricing

Price based on TIME SAVED, not features or LOC:

| Product | Time Saved | Hourly Rate | Time Value | Your Price |
|---------|-----------|-------------|------------|------------|
| Boilerplate | 40 hours | $100/hr | $4,000 | $149 |
| UI kit | 20 hours | $100/hr | $2,000 | $99 |
| WordPress theme | 30 hours | $75/hr | $2,250 | $59 |
| VS Code extension | 10 hours/month | $100/hr | $12,000/yr | $49 |
| CLI tool | 5 hours/setup | $100/hr | $500 | $29 |

**Goal:** Price at 3-10% of the value delivered. This feels like a no-brainer to the buyer.

### Tiered Pricing

| Feature | Free | Pro ($49) | Premium ($149) |
|---------|------|-----------|----------------|
| Core components | 10 | 50 | 100+ |
| TypeScript | No | Yes | Yes |
| Documentation | Basic | Full | Full + videos |
| Updates | None | 6 months | Lifetime |
| Support | GitHub Issues | Email | Discord + email |
| License | MIT (personal) | Single project | Unlimited projects |

### Discount Strategy

| Discount Type | Amount | When | Impact |
|--------------|--------|------|--------|
| Launch discount | 30-50% | First 48 hours | Creates urgency |
| Bundle discount | 20-30% | Multiple products | Increases AOV |
| Annual (for SaaS) | 15-20% | Annual vs monthly | Improves retention |
| Affiliate/Referral | 10-20% | Referral link | Acquires customers |
| Education | 50% | .edu email | Brand loyalty |
| Enterprise | Custom | 5+ seats | High-value deals |

**Never discount below 50%.** It devalues your product and signals low quality.

---

## Protecting Your Code Products

### Licensing

| License Type | Restriction | Best For |
|-------------|-------------|----------|
| Regular License | Single end product | Individual buyers |
| Extended License | Multiple end products, SaaS use | Agencies |
| Developer License | Unlimited personal use | Professional developers |
| Enterprise License | Company-wide, all projects | Companies |

### Anti-Piracy Measures

1. **License keys** - Each purchase gets unique key
2. **Domain locking** - For WordPress themes/plugins
3. **Watermarked demo** - Show but don't allow full copy
4. **Obfuscation** - Minify/uglify JavaScript (not foolproof but helps)
5. **Updates requiring key** - Only paid customers get updates

**Reality check:** You can't stop all piracy. 20-30% of users will pirate. Focus on making buying so convenient that most people pay. Add-ons like updates and support are harder to pirate.

---

## Customer Support for Code Products

### Support Triage

| Issue Type | Response Time | Channel |
|-----------|--------------|---------|
| Bug in my code | 24 hours | Email/Discord |
| Installation issue | 24 hours | Email/Discord |
| Feature request | 1 week | GitHub Issues |
| "How do I..." question | 48 hours | Documentation + email |
| Refund request | Immediate | Email |

### Managing Support at Scale

**Phase 1 (1-50 customers):** You handle all support personally
**Phase 2 (50-500 customers):** Add FAQ + Discord community (peer support)
**Phase 3 (500-5,000 customers):** Hire VA for first-line support
**Phase 4 (5,000+ customers):** Full-time support person + knowledge base

**The 80/20 rule for support:** 80% of support questions are answered by 20% of your documentation. Write good docs and FAQ, and you cut support tickets by 80%.

---

## Year 1 Revenue Goal

| Month | Products Published | Revenue Target | Cumulative |
|-------|-------------------|----------------|------------|
| 1 | 1 (launch) | $500 | $500 |
| 2 | 2 | $1,000 | $1,500 |
| 3 | 3 | $2,000 | $3,500 |
| 4 | 3 | $2,500 | $6,000 |
| 5 | 4 | $3,000 | $9,000 |
| 6 | 4 | $3,500 | $12,500 |
| 7 | 5 | $4,000 | $16,500 |
| 8 | 5 | $4,500 | $21,000 |
| 9 | 6 | $5,000 | $26,000 |
| 10 | 6 | $5,500 | $31,500 |
| 11 | 6 | $6,000 | $37,500 |
| 12 | 7+ | $7,000 | $44,500 |

**Key: Don't spread yourself thin. Launch 1 product, market it well, then launch the next.**

---

## Action Plan: First Product in 30 Days

### Week 1: Choose and Plan
- Pick ONE product type from this guide
- Identify the specific pain point you're solving
- Research competitors (what do they charge? what's missing?)
- Define your scope (what's included? what's excluded?)
- Set your price (based on value delivered)

### Week 2: Build MVP
- Build the minimum viable version
- Core features only (cut everything else)
- Focus on what makes it valuable, not what makes it pretty
- Write documentation as you go

### Week 3: Polish and Package
- Clean up code and structure
- Write complete README
- Create landing page with screenshots/demo
- Set up payment processing
- Prepare launch assets

### Week 4: Launch
- Email your network
- Post on Twitter (build in public thread)
- List on relevant marketplace
- Launch discount for first 50 buyers
- Respond to all feedback immediately

### Day 30: You have a sellable product.
Congratulations. You're now a digital product creator.
