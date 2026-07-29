# Hacker News Launch Guide: Show HN Best Practices

## Why Hacker News Matters for Solo Founders

Hacker News (HN) is the most influential tech community in the world. A successful Show HN can:

- Drive 10,000-100,000+ highly qualified visitors in a single day
- Attract technical co-founders, early employees, and advisors
- Generate deep technical feedback that improves your product
- Create a permanent SEO asset (HN posts rank well for technical queries)
- Get your product in front of investors, VCs, and journalists who read HN daily
- Provide raw, honest feedback from sophisticated technical users

HN is particularly valuable for developer tools, technical SaaS, and products built by solo founders. The community respects craftsmanship, technical depth, and authenticity over marketing polish.

## How HN Differs from Product Hunt

| Dimension | Product Hunt | Hacker News |
|-----------|-------------|-------------|
| **Audience** | General tech + early adopters | Technical founders, engineers, CS crowd |
| **Vibe** | Supportive, promotional | Skeptical, meritocratic |
| **What Works** | Beautiful design, clear value prop | Technical depth, open source, clever solutions |
| **Tone** | Positive, celebratory | Constructively critical |
| **Algorithm** | Vote-based + curator picks | Vote + time decay, anti-spam |
| **Best Time** | Midnight PT (reset time) | 6-9 AM PT (weekday) |
| **Engagement** | Comments are supportive | Comments are technical debates |
| **Post-Launch** | Social proof badge | Ongoing discussion for days |

## Phase 1: Is Your Product Ready for HN?

### The Show HN Readiness Test

Answer honestly:

1. **Is your product actually useful for HN's audience?**
   - HN readers are primarily technical (engineers, founders, technically-savvy operators)
   - Developer tools, infrastructure, programming resources, technical SaaS do best
   - Consumer products, no-code tools, and purely business apps often struggle

2. **Is your product polished enough?**
   - HN is ruthless about broken links, bad UX, slow load times, and half-baked features
   - Your product should be stable, fast, and complete enough for someone to try immediately
   - No "coming soon" features, no broken signup flows, no placeholder pages

3. **Do you have something genuinely interesting to share?**
   - "Yet another [category tool]" will be ignored or criticized
   - You need a unique approach, technical innovation, or clever solution
   - Even in a crowded space, a well-executed product with a unique angle can succeed

4. **Are you ready for critical feedback?**
   - HN will tell you what's wrong with your product
   - You must be emotionally prepared for direct, sometimes blunt criticism
   - Every criticism is a gift — it shows someone cared enough to engage

5. **Can you handle the traffic?**
   - A front-page HN post can bring 50K+ visitors in hours
   - Your server, database, and infrastructure must scale
   - 500+ concurrent users is a realistic minimum

### What Performs Well on Show HN

Based on analysis of top Show HN posts:

- **Open source projects** (especially with GitHub stars as social proof)
- **Developer tools** (CLI tools, editors, debugging, monitoring)
- **Technical demonstrations** (impressive engineering feats)
- **New programming languages or frameworks**
- **Databases, storage systems, infrastructure tools**
- **Unique visualizations or interactive demos**
- **Tools that solve a specific, painful technical problem**
- **Well-executed "small" tools** (done one thing well)
- **AI/ML projects with a technical angle** (not just wrapper UIs)

### What Performs Poorly

- **SaaS landing pages with no actual product** (people can't try it)
- **Overly salesy or marketing-heavy copy** (HN hates marketing speak)
- **"AI wrapper" products** (must have genuine technical depth)
- **Products that require signup to see value** (let them try before signup)
- **Generic "Top 10" or blog-spam content**
- **Products targeting non-technical audiences** (HN is not your ICP)
- **Broken links, slow pages, bad mobile layouts** (HN judges instantly)

## Phase 2: Pre-Launch Preparation (2-3 Weeks Before)

### Week 3: Build HN Credibility

You cannot post on HN once and expect to succeed. Build a presence:

1. **Create an HN account with history** — Accounts created solely to post a Show HN link are treated with suspicion. Comment on relevant threads for 2-4 weeks before your launch.

2. **Engage meaningfully** — Add thoughtful technical comments to threads. Upvote good content. Build a reputation as someone who contributes.

3. **Understand the culture** — Read the HN guidelines (https://news.ycombinator.com/newsguidelines.html). Understand what's valued: intellectual honesty, technical depth, respectful disagreement.

4. **Don't ask for upvotes** — This violates HN rules and will get you banned. Organic upvotes only.

### Week 2: Prepare Your HN Post

**The Title**

This is the single most important element. The title determines whether people click.

**Show HN Title Formula:**
```
Show HN: [Product Name] — [What it does] for [Who it's for]

Show HN: DocuFlow — Generate API docs from code comments
Show HN: LogViz — Real-time log visualization for Kubernetes
Show HN: Tidy — A CLI tool that organizes your files by AI content analysis
```

**Show HN Title Best Practices:**

1. **Start with "Show HN:"** — This is mandatory for Show HN posts. Without it, your post may be flagged.

2. **Be descriptive, not clever** — "Show HN: My Amazing Tool" tells me nothing. "Show HN: QueryGPT — Write SQL using natural language in your terminal" tells me exactly what it is.

3. **Include the problem you solve** — The best titles imply the problem in the description.

4. **Keep it under 80 characters** — Titles truncate on mobile and in listings.

5. **Avoid hype words** — "Revolutionary," "game-changing," "best ever" — HN hates these. Be factual.

6. **Don't include pricing** — "Show HN: MyTool — $10/mo" looks spammy. Let the product page discuss pricing.

7. **Don't include "HN" or "Hacker News" in the title** — Redundant.

**Test Your Title:**
- Before posting, test 3-5 title variations with a friend who knows HN culture
- Pick the most factual, descriptive, and technically interesting one
- The title should make a technical person think "I need to see how they did that"

### Week 2: Prepare Your Product

Before the HN crowd arrives, ensure:

1. **No signup wall** — The number one complaint on Show HN is "I have to sign up to see anything." If possible, let people experience your product without creating an account. A demo, sandbox, or preview mode is ideal.

2. **Fast loading** — Under 2 seconds. Use a CDN. Pre-warm your server. Consider static rendering for the landing page.

3. **Mobile responsive** — ~40% of HN traffic is mobile. Check your site on a phone.

4. **Clear value in 5 seconds** — When someone lands on your page, they should immediately understand:
   - What the product does (headline + subheadline + screenshot)
   - Why it's interesting (unique approach, technical depth)
   - How to try it (call to action)

5. **Open source (optional but powerful)** — If your product is open source, link to the GitHub repo prominently. HN loves open source.

6. **NO PAYWALLS** — If your product requires payment to use at all, Show HN is probably not the right approach. Have a free tier or trial.

7. **Working signup/auth flow** — If you require signup, it should work flawlessly. No error messages, no broken email confirmation, no captcha from hell.

### Week 1: Pre-Post Outreach

Unlike Product Hunt, you cannot have a "launch army" for HN. HN's anti-spam algorithms detect coordinated voting. However, you can:

1. **Tell a few friends** — "I'm posting a Show HN on Tuesday. Please don't upvote unless you genuinely find it interesting." (Never ask for upvotes.)

2. **Prepare to engage** — Clear your schedule for 48 hours after posting. You need to be available to reply to comments.

3. **Check HN's rules** — Re-read the guidelines. Make sure your post complies.

4. **Prepare for worst-case traffic** — Have your infrastructure ready to handle 50K+ visitors.

## Phase 3: Launch Day Playbook

### Choosing the Right Time

HN's algorithm favors early morning posts:

**Best times (Pacific Time):**
- **Monday-Thursday, 6-8 AM PT** — This is when HN traffic peaks. A post at this time stays on the front page through the day.
- **Avoid weekends** — Lower traffic and fewer upvotes. Unless your product specifically targets weekend tinkerers.
- **Avoid holidays** — Low engagement.

**The timing strategy:**
- Post between 6-7 AM PT for maximum exposure
- If you're in a different timezone, schedule your post or set an alarm
- HN doesn't have a "scheduled post" feature — you post manually

### The Post Goes Live

**Step 1: Submit the post**
Go to https://news.ycombinator.com/submit
- Title: Your prepared title starting with "Show HN:"
- URL: Your landing page or product URL
- Text: Leave blank (HN doesn't allow both URL and text for Show HN)

**Step 2: Prepare your first comment**
After posting, prepare to comment on your own post if needed:
- HN doesn't automatically give you a way to add context (unless you use the text post option, but URL posts are better)
- You CAN add a comment to your own post explaining more
- Some founders add a comment with background, technical details, or what they're looking for feedback on
- Keep it humble and informative

**Step 3: Monitor the post**
- Check the "new" page: https://news.ycombinator.com/newest
- Your post appears here first
- If it gets enough upvotes quickly, it moves to the front page
- The first 30 minutes are critical

### The First 60 Minutes (Critical Window)

In the first hour, your post needs to get enough upvotes from the "new" page to reach the front page.

**What you should be doing:**

1. **Do NOT upvote your own post** — HN detects this and it can get you penalized. Logged-in users who click their own post are automatically upvoted, which is fine, but don't create multiple accounts.

2. **Do NOT ask anyone to upvote** — This is against HN rules and will get you banned.

3. **Monitor the "new" page** — See if your post is getting traction. If it has 3+ upvotes in 15 minutes, it has a chance at the front page.

4. **Wait for comments** — First comments may appear within 5-30 minutes. Be ready to reply.

**Upvote velocity for front-page success:**
| Time | Upvotes needed | Probability |
|------|----------------|-------------|
| 15 minutes | 3-5 | Front page possible |
| 30 minutes | 5-10 | Front page likely |
| 60 minutes | 10-15 | Front page probable |
| 2 hours | 20-30 | Front page secured |

These numbers vary by day and competition. Monday and Tuesday are most competitive.

### Engaging with Comments

This is where Show HN is won or lost. The quality of your responses matters more than the product itself in many cases.

**Comment Response Strategy:**

```
1. Reply to EVERY comment within 1 hour
   - HN rewards engagement
   - Unanswered comments make you look uninterested
   - Every comment is an opportunity

2. Be humble and grateful
   - "Thank you for checking it out" is always appropriate
   - Even if the comment is critical, thank them
   - HN respects founders who handle criticism well

3. Answer technical questions thoroughly
   - This is a technical audience
   - "We used X because Y" is better than "We used X"
   - Show your technical depth
   - If you don't know the answer, say "I'm not sure, but here's my best understanding"

4. Acknowledge limitations honestly
   - "Yes, this doesn't support X yet. We're working on it."
   - "That's a valid concern. Here's how we're thinking about it."
   - "We chose not to do X because Y tradeoff."
   - Honesty builds trust with HN

5. Don't be defensive
   - HN comments can be blunt. Do not argue.
   - "You're right, that's a limitation. Here's our reasoning."
   - If someone says "This is useless because X," respond with "Fair point. Here's who this is useful for despite that limitation."
   - NEVER tell someone they're wrong for not liking your product.

6. Ask follow-up questions
   - "What would make this useful for your use case?"
   - "How are you currently solving this problem?"
   - "What's the one thing you'd change?"
   - This shows you care about the feedback and turns critics into contributors.

7. Reference the HN guidelines in replies
   - "Per the HN guidelines, I won't ask for upvotes, but I appreciate your feedback."
   - This shows you're a community member, not a drive-by marketer.
```

**Common HN Comments and How to Handle Them:**

| Comment Type | Response Strategy |
|--------------|-------------------|
| "How is this different from X?" | Acknowledge X, give 2-3 specific differences, invite comparison |
| "This is just a wrapper around GPT" | Acknowledge the simplicity, explain the value-add layers, technical details |
| "Your site is slow" | Apologize, explain the cause (if known), share timeline for fix |
| "I don't see why I'd use this" | Ask about their workflow, explain the niche use case, stay gracious |
| "The pricing is too high" | Explain your pricing rationale, ask what they'd consider fair |
| "Great work!" | Thank them, ask what they'd like to see next |
| "This is exactly what I needed" | Thank them, offer help getting started, ask for specific feature requests |
| "You should use X instead of Y" | Thank them for the suggestion, explain your choice, stay open |
| "The UI is confusing" | Ask for specifics, thank them for the usability feedback |

### Managing Traffic

If your post hits the front page:

1. **Monitor your server** — Keep a terminal open with `htop` or your cloud dashboard
2. **Check error rates** — 500 errors will kill your momentum
3. **Check database connection pool** — This is the most common bottleneck
4. **Check CDN cache hit rate** — Static assets should be cached
5. **API response times** — Should stay under 200ms

**Quick fixes if you're overwhelmed:**
- Cache your landing page aggressively (static HTML, no DB queries)
- Scale your server vertically or horizontally
- Turn on auto-scaling if using cloud services
- If using a serverless platform (Vercel, Netlify), you're probably fine
- Static serve as much as possible
- Put Cloudflare in front for CDN + DDoS protection

### Throughout the Day

- **Check HN every 15-30 minutes** — Reply to new comments immediately
- **Post shouldn't require constant monitoring** — But first 6 hours need attention
- **Share on Twitter once, if it's on the front page** — "Made the front page of HN! Ask me anything about [technical detail]"
- **Don't post about it on social media multiple times** — HN values organic discovery
- **Don't post "Upvote my HN post" anywhere** — Gets you banned

## Phase 4: Post-Launch Follow-Up

### Day 1-2: Capitalize on Traffic

1. **Review all comments** — Even after the post leaves the front page, comments may continue for 48-72 hours
2. **Identify recurring themes** — What questions kept coming up? What criticisms were most common?
3. **Add an FAQ to your landing page** — Address the top 5 questions from HN comments
4. **Fix the low-hanging fruit** — If 5 people said the same thing is broken, fix it immediately
5. **Send a thank-you email** — To your existing users who may have seen the HN post
6. **Welcome new users** — Send a personal email to every signup from HN (track with UTM)

**HN Signup Welcome Email:**
```
Subject: From HN to your inbox — welcome to [Product Name]

Hi [Name],

Saw you signed up after the HN post! Thanks for checking us out.

I'd love to know: what brought you here and what are you hoping
to accomplish?

As a solo founder, every signup matters to me. If you have any
questions or feedback — especially the honest, critical kind —
please reply directly. I read every email.

Best,
[Your Name]
```

### Day 3-7: Analyze and Act

**Metrics to Review:**
- Total HN upvotes (check the post page)
- Total HN comments (count or estimate)
- Referral traffic from HN (UTM or referrer header)
- Signup conversion rate from HN traffic
- Bounce rate of HN traffic (HN visitors bounce fast if the page doesn't load or isn't relevant)
- Time on site for HN visitors
- Feature adoption among HN signups

**Apply Learnings:**
- What aspect of your product got the most attention? Double down.
- What confused people? Clarify your messaging.
- What technical limitations were called out? Fix or prioritize.
- What feature requests came up most? Consider for roadmap.

### Day 7-30: Convert HN Visitors into Long-Term Users

HN traffic is high volume but often low conversion to paid (the audience is technical and expects free tools). Strategies to convert:

1. **Free tier with real value** — If HN users can't use your product for free, most won't convert. But if they can use it and love it, some will upgrade.
2. **Generous trial** — 30-60 day trial, no credit card required
3. **Personal onboarding** — Reach out to the most engaged HN signups for 1:1 onboarding
4. **Community building** — Invite HN signups to a Slack/Discord community
5. **Build what they asked for** — Ship the features HN commenters suggested, then post a follow-up comment on your HN thread

**The 30-day HN follow-up email:**
```
Subject: Quick question — 30 days after HN

Hi [Name],

It's been about a month since [Product Name] was on HN.

Quick questions:
1. Did you stick with [Product Name]? Why or why not?
2. What would make it indispensable for you?
3. Is there anything I should build next?

Your honest feedback helps me build something useful.

Reply anytime. I'd love to hear from you.

Best,
[Your Name]
```

## Show HN Dos and Don'ts

### DO

- **Do** submit a URL (not a text post)
- **Do** start your title with "Show HN:"
- **Do** make your product accessible without signup if possible
- **Do** ensure your site loads fast and handles traffic
- **Do** reply to every comment thoughtfully
- **Do** be honest about limitations
- **Do** acknowledge competitors and alternatives
- **Do** thank people for their time and feedback
- **Do** follow through on promises ("I'll fix that" → actually fix it)
- **Do** read and follow HN guidelines
- **Do** have an HN account with some history before posting
- **Do** post on a weekday morning PT

### DON'T

- **Don't** ask for upvotes (ever, in any form)
- **Don't** create multiple accounts to upvote
- **Don't** post if your product requires payment to try
- **Don't** use marketing hype in your title or comments
- **Don't** be defensive about criticism
- **Don't** ignore questions
- **Don't** edit your title after posting (it will be flagged)
- **Don't** repost the same product repeatedly (one shot per major version)
- **Don't** post blog posts or articles as Show HN (it's for products)
- **Don't** post if your product isn't ready (broken links, half-built features)
- **Don't** post on weekends or holidays
- **Don't** share your HN post on social media asking for upvotes

## HN Launch Day Support Strategy

As a solo founder, being on HN all day conflicts with everything else. Here's how to manage:

**Ideal scenario:**
- Block 48 hours after posting
- No meetings, no commitments, no distractions
- One monitor with HN open, one with your server dashboard
- Phone notifications on for critical alerts only
- Partner with another founder to watch your back if possible

**If you can't block 48 hours:**
- Post on a day you can be available for at least 12 hours
- Have a friend monitor the thread and ping you for important comments
- Set up email alerts for HN mentions of your product name
- Accept that you'll miss some comments and reply as soon as you can

**Energy management:**
- HN engagement is emotionally intense
- Take 5-minute breaks every hour
- Eat real meals (not desk-snacking)
- Step away for 10 minutes if a critical comment gets to you
- Remember: HN is one day. The product is forever.

## What If Your Show HN Doesn't Take Off?

**The post gets 2 upvotes and dies on the "new" page:**

1. **It's okay** — Most Show HN posts don't hit the front page. It doesn't mean your product is bad.
2. **Reasons it might have failed:**
   - Title wasn't descriptive enough
   - Title targeted the wrong angle
   - Product isn't interesting to the HN audience
   - Bad timing (same day as a major tech news story)
   - HN algorithm just didn't favor you
3. **What NOT to do:**
   - Don't repost immediately (will be flagged)
   - Don't complain about HN on HN (will get you banned)
   - Don't create a new account to post again (banned)
4. **What to do instead:**
   - Wait 6-12 months, improve the product significantly, and post again
   - Try Product Hunt or other channels instead
   - Analyze why your product didn't resonate with the technical audience
   - Keep building and growing through other channels

## Advanced Show HN Strategies

### The Open Source Advantage

If your product is open source:
- Mention it in your title: "Show HN: MyTool — Open source [description]"
- Link to GitHub as the primary URL (not your SaaS landing page)
- HN users will check the GitHub repo for code quality, README, issues
- A well-maintained open source project with good documentation gets more traction

### The "Demo First" Approach

Instead of making people sign up, provide a working demo:
- Hosted demo instance with sample data (for web apps)
- `npx` or `pip install` one-liner (for CLI tools)
- Docker image that runs locally (for infrastructure tools)
- Replit/Codesandbox playground (for code libraries)

The easier you make it for someone to try your product without commitment, the better HN engagement.

### The Technical Deep-Dive

Alongside your Show HN post, write a technical blog post about how you built something interesting. HN users love:
- Performance benchmarks
- Architecture decisions with tradeoffs explained
- How you solved a hard technical problem
- Data structures, algorithms, or systems design choices

Post the blog as a separate HN submission a few days after your Show HN, or link it in your Show HN comments.

### The "Ask HN" Follow-Up

A week after your Show HN, post an Ask HN:
"Ask HN: Feedback on my approach to [problem domain]"
This positions you as someone seeking wisdom rather than promoting, and can generate deeper discussions.

## HN Launch Timeline

### 3 Weeks Before
- [ ] Create HN account (if you don't have one)
- [ ] Start engaging in HN discussions (build comment history)
- [ ] Read HN guidelines thoroughly
- [ ] Study 10 successful Show HN posts in your category

### 2 Weeks Before
- [ ] Finalize Show HN title (test 3-5 variations)
- [ ] Ensure product loads fast (test from multiple locations)
- [ ] Set up CDN and caching
- [ ] Implement demo/sandbox mode (no signup required)
- [ ] Load test your infrastructure
- [ ] Set up error monitoring

### 1 Week Before
- [ ] Mobile-responsive testing
- [ ] Signup flow testing (from multiple devices/browsers)
- [ ] Draft your first comment (background, context, ask)
- [ ] Prepare for traffic spikes
- [ ] Clear your calendar for launch day +1

### Launch Day
- [ ] Post at 6-7 AM PT
- [ ] Monitor "new" page for first 60 minutes
- [ ] Reply to every comment within 1 hour
- [ ] Monitor server performance
- [ ] Engage actively for 12+ hours
- [ ] Don't ask for upvotes

### Day 2-7
- [ ] Reply to remaining comments
- [ ] Analyze traffic and conversion data
- [ ] Fix critical issues mentioned in comments
- [ ] Add FAQ based on common questions
- [ ] Send thank-you to HN signups
- [ ] Post follow-up comment on your HN thread with updates

### Day 7-30
- [ ] Ship features based on top HN feedback
- [ ] Convert HN visitors to paid users
- [ ] Set up retargeting for HN traffic
- [ ] Write a retrospective blog post about the HN experience
- [ ] Apply learnings to next launch

## The Solo Founder's HN Survival Kit

- **Coffee/tea** — You'll be up early and engaged all day
- **Two monitors** — One for HN, one for everything else
- **Server dashboard** — `htop`, Cloudflare analytics, error logs
- **Comment template snippets** — For common responses (save typing time)
- **A supportive friend** — Text them when you need to vent about a mean comment
- **Thick skin** — HN can be brutal. Your product is not your identity.
- **Phone fully charged** — In case you need to step away but still monitor
- **Last-resort "scale button"** — Know how to quickly scale your server

## Key HN Launch Metrics

| Metric | Target | Notes |
|--------|--------|-------|
| Upvotes (Show HN) | 50+ for front page | 100-200+ for top 10 |
| Comments | 30+ for engaged thread | Quality > quantity |
| Traffic from HN | 5K-50K visitors | 10K-100K for top posts |
| Signups from HN | 100-1,000 | Depends on conversion rate |
| Signup conversion rate | 2-5% | Lower than PH, higher quality |
| Bounce rate (HN traffic) | < 50% | HN visitors are scanners |
| Time on site | > 2 minutes | Indicates genuine interest |
| HN → Paid (30 day) | 1-3% | Lower conversion, higher LTV |

## Alternatives If HN Isn't Right for You

Not every product is suited for Show HN. Alternatives:

- **Product Hunt** — Better for design-forward, non-technical products
- **Reddit** — Post in relevant subreddits (not just for upvotes, for genuine discussion)
- **Lobsters** — Similar to HN, smaller community, technical audience
- **Indie Hackers** — Supportive community of solo founders
- **Hacker News "Ask HN"** — "Ask HN: What tools do you use for [problem]?" can generate leads without a product post
- **Technical newsletters** — Reach out to newsletter authors covering your space

## Final Thoughts

- **HN is not a launch strategy, it's a feedback channel.** The real value is the quality of feedback from technical peers. Even a "failed" launch that generates 20 thoughtful comments is valuable.
- **Don't build for HN.** Build for your customers. HN is a distribution channel, not your target market.
- **Authenticity > polish.** HN can smell marketing a mile away. Be honest, be technical, be humble.
- **You only get one shot (per major version).** Make it count. Don't post a half-baked product.
- **The best Show HN posts are from founders who genuinely want feedback.** If you're just looking for traffic, HN will sense it and reject you.

Good luck. HN is unforgiving but fair. Build something great, share it honestly, and engage thoughtfully. The rest takes care of itself.
