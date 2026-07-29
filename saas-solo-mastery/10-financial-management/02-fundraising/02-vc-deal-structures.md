# Understanding VC Deals

A complete guide to venture capital deal structures for solo founders — SAFE notes, priced rounds, valuation, dilution, board control, and term sheet terms. Everything you need to know before signing.

---

## Part 1: The Solo Founder's VC Reality

### The Asymmetric Relationship

When you take venture capital, you enter a relationship where:
- The VC has lawyers who've done 100+ deals
- You've probably done 0
- The VC has standard documents drafted by their counsel
- You're paying for your own lawyer (out of pocket or future funds)
- The VC has portfolio leverage; you have your one company

**This is not a partnership of equals.** Your job is to understand the terms well enough to negotiate fairly.

### The Minimum You Must Know

Before your first VC meeting, understand these concepts:

1. Pre-money and post-money valuation
2. Dilution (how much of your company you give up)
3. Liquidation preference (who gets paid first)
4. Anti-dilution protection (what happens in a down round)
5. Board composition (who controls decisions)
6. Protective provisions (veto rights)
7. Vesting (earning your equity over time)
8. Information rights (what you must report)

---

## Part 2: SAFE Notes

### What is a SAFE?

A Simple Agreement for Future Equity (SAFE) is not debt — it's a warrant to purchase equity in a future priced round. Created by Y Combinator, it's the most common instrument for seed-stage SaaS companies.

### How SAFEs Work

```yaml
You raise $500K via SAFE
Investor gives you $500K now
In exchange, they get the right to convert that $500K into equity
WHEN: You do a future priced round (Series A)
AT: A discount to the Series A price (usually 15-25% off)

Example:
  Series A valuation: $10M
  SAFE discount: 20%
  SAFE investor converts at: $8M valuation ($10M × 0.80)
  SAFE investment: $500K
  SAFE investor gets: $500K / $8M = 6.25% of company at Series A
```

### SAFE Variants

```yaml
SAFE Type                     | Key Feature
Standard SAFE (no cap, no disc.)| Rarely used — converts at same price as Series A
SAFE with Discount Only        | Converts at 15-25% discount to Series A
SAFE with Valuation Cap Only   | Converts at lower of cap OR discount
SAFE with Discount AND Cap     | Most common — investor gets best of both

Most Common (YC Standard):
  - Discount: 20%
  - Valuation Cap: $5M - $20M
  - MFN (Most Favored Nation): If you raise another SAFE with better terms, this one improves too
```

### Example: SAFE with Cap and Discount

```yaml
SAFE Terms:
  Investment: $500K
  Discount: 20%
  Valuation Cap: $8M
  MFN: Yes

Scenario A: Series A at $10M pre-money
  Discount price: $10M × 0.80 = $8M
  Cap price: $8M (the cap)
  Lower of the two: $8M
  SAFE converts at $8M
  Investor gets: $500K / $8M = 6.25%

Scenario B: Series A at $15M pre-money
  Discount price: $15M × 0.80 = $12M
  Cap price: $8M
  Lower of the two: $8M (cap applies)
  SAFE converts at $8M
  Investor gets: $500K / $8M = 6.25%

Scenario C: Series A at $5M pre-money
  Discount price: $5M × 0.80 = $4M
  Cap price: $8M
  Lower of the two: $4M (discount applies)
  SAFE converts at $4M
  Investor gets: $500K / $4M = 12.5%
```

### Pro-Rata Rights in SAFEs

Some SAFEs include "pro-rata rights" — the investor can invest again in the next round to maintain their ownership percentage.

**Solo founder note:** Pro-rata rights can complicate future rounds. Limit these to only strategic investors.

### SAFE Advantages for Solo Founders

```yaml
Pros:
  - Simple (5-8 pages vs 100+ for Series A)
  - Low legal fees ($2K-$5K vs $20K-$50K+)
  - Fast (can close in 1-2 weeks)
  - No valuation argument (cap replaces valuation)
  - No board seat
  - No liquidation preference
  - No maturity date (no repayment risk)
  - Standardized (YC template is widely accepted)

Cons:
  - Uncertainty about final ownership (depends on Series A valuation)
  - Stacked SAFEs can create complex cap table
  - No SEC registration (harder for some investors)
  - Not all angels understand them
  - If you never raise a priced round, SAFE never converts (but can be converted via "safe conversion" at liquidity event)
```

---

## Part 3: Priced Rounds

### What is a Priced Round?

A priced round (Seed, Series A, Series B) assigns a specific valuation to the company and issues shares at a specific price. All existing instruments (SAFEs, convertible notes) convert to equity at this point.

### The Term Sheet

```yaml
KEY TERMS IN A PRICED ROUND TERM SHEET

Economic Terms:
  - Valuation (pre-money and post-money)
  - Investment amount
  - Price per share
  - Liquidation preference
  - Participation rights
  - Anti-dilution provisions
  - Dividend rights (rare for SaaS)
  - Redemption rights (rare for SaaS)

Control Terms:
  - Board composition
  - Protective provisions (veto rights)
  - Drag-along rights
  - Information rights
  - Right of first refusal
  - Co-sale rights
  - Pre-emptive rights (pro-rata)

Founder Terms:
  - Vesting schedule
  - Founder stock agreement
  - IP assignment
  - Non-compete / non-solicit
  - Employment terms
```

### Valuation: Pre-Money vs. Post-Money

```yaml
Pre-Money Valuation = Value of company BEFORE investment
Investment = Cash coming in
Post-Money Valuation = Pre-Money + Investment

Example:
  Pre-money: $8M
  Investment: $2M
  Post-money: $10M
  Investor gets: $2M / $10M = 20%

Founder dilution: 20%
```

### Valuation Benchmarks for Solo Founder SaaS

```yaml
Stage           | Typical Pre-Money | Revenue Multiple
Pre-Seed        | $2M - $5M         | N/A (pre-revenue or < $5K MRR)
Seed            | $5M - $12M        | 10-20x ARR
Series A        | $10M - $30M       | 15-25x ARR
Series B        | $30M - $100M      | 10-20x ARR (multiple shrinks as you grow)

Solo founder reality:
  - You may get slightly LOWER valuations (key person risk)
  - You may need to accept MORE dilution
  - You may face more stringent vesting/protective provisions
```

### Liquidation Preference

**The most important economic term after valuation.**

```yaml
Standard: 1x non-participating
  - Investor gets their money back FIRST
  - Then remaining proceeds distributed to common holders
  - If company sells for $10M and investor put in $2M:
    - Investor gets $2M (their money back)
    - Common holders split remaining $8M

Better for founders: 1x non-participating (standard)
Worse for founders: 2x+ participating
  - Investor gets 2x their money back ($4M on $2M investment)
  - THEN also gets their percentage of remaining proceeds

With 2x participating on $2M investment, $10M exit:
  Investor gets: $4M (2x preference) + 20% of $6M = $5.2M
  Common holders (including you): $4.8M (instead of $8M)

NEVER accept participating preferred.
NEVER accept >1x preference.
```

### Anti-Dilution Protection

```yaml
Full Ratchet (WORST for founders):
  If you raise a down round at a lower price, the investor's shares are repriced to the new, lower price.
  This CRUSHES common shareholders.
  Example: Series A at $10/share, Series B at $5/share
    Series A investor's shares convert as if they paid $5/share
    They get TWICE as many shares

Weighted Average (STANDARD):
  Adjusts the investor's price based on a formula that accounts for 
  the number of shares issued at the lower price.
  Less punitive than full ratchet.
  Two variants: Broad-based (better for founders) and narrow-based

Solo founder rule:
  - Accept broad-based weighted average anti-dilution (standard)
  - REJECT full ratchet
  - REJECT narrow-based weighted average
```

### Board Composition

```yaml
Pre-Seed / Seed (typical solo founder setup):
  - 1 founder seat (you)
  - 1 investor seat
  - 0-1 independent seat
  - = You control the board

Series A (typical):
  - 1 founder seat (you)
  - 1-2 investor seats
  - 1 independent seat (mutually agreed)
  - = Board is balanced

Series B and beyond:
  - 1 founder seat
  - 2-3 investor seats
  - 1-2 independent seats
  - = You may be outvoted

Solo founder board strategy:
  - Keep board to 3 people max
  - Founder always has a seat
  - Independent seat must be mutually agreed
  - No board can fire you without cause (negotiate this)
```

### Protective Provisions (Veto Rights)

Things investors can veto:

```yaml
Standard protective provisions (reasonable):
  - Changing authorized shares
  - Selling the company
  - Taking on significant debt (> $X)
  - Hiring/firing CEO
  - Changing business materially
  - Paying dividends

Aggressive protective provisions (push back on these):
  - Hiring/firing specific roles (not just CEO)
  - Setting annual budget
  - Decisions about products/features
  - Pricing changes
  - Hiring below a certain salary
  - Any expense above $X (micro-management)
```

---

## Part 4: Dilution — The Math You Must Understand

### The Dilution Ladder

```yaml
Starting: You own 100% of the company

Seed Round: Sell 20% for $1M
  You: 80%
  Investors: 20%

Series A: Sell 25% for $5M
  You: 80% × (1 - 0.25) = 60%
  Investors: 20% + (80% × 25%) = 40%

Series B: Sell 20% for $10M
  You: 60% × (1 - 0.20) = 48%
  Investors: 40% + (60% × 20%) = 52%

Option Pool: 10% dilution
  You: 48% × (1 - 0.10) = 43.2%
  Investors: 52% + (48% × 10%) = 56.8%

After 3 rounds + option pool:
  You own: ~43% (if you didn't sell secondary shares)
```

### The Real Dilution: What SARs Look Like

```yaml
TOTAL DILUTION OVER MULTIPLE ROUNDS

Rounds               | Cumulative Dilution
No funding           | 0%
Seed (20%)           | 20%
Seed + Series A (25%)| 40% (20% + 25% of remaining 80%)
Seed + A + B (20%)  | 52% (40% + 20% of remaining 60%)
+ Option pool (10%)  | 57% (52% + 10% of remaining 48%)
+ ESOP (15%)         | 63% (57% + 15% of remaining 43%)

Solo founder: After Seed + A + B + options:
  Best case: 30-40% ownership
  Typical: 15-25% ownership (if you had multiple rounds)
  Worst case: < 10% (multiple down rounds, large option pool)
```

### How to Think About Dilution

```yaml
Dilution is not inherently bad. It depends:

GOOD dilution:
  $1M seed → $10M ARR in 18 months → Company worth $100M
  Your 80% × $100M = $80M
  You're worth $80M after giving up 20%

BAD dilution:
  $1M seed → $2M ARR in 36 months → Company worth $20M
  Your 80% × $20M = $16M
  You'd have been better off bootstrapping to $2M ARR
  (and owning 100% of a $20M company = $20M vs $16M)

Dilution math:
  Value of your stake = (1 - Total_Dilution) × Company_Value
  
  If dilution is 50% but company value is 10x higher:
    You're better off (own half of 10x = 5x)
  
  If dilution is 50% and company value is same:
    You're worse off (own half of same = 0.5x)
```

### Option Pool Dilution

```yaml
Option pool = Shares reserved for future employees
Size: 10-20% of fully diluted shares
Who bears the cost: Usually founders (deducted from pre-money)

Example:
  Pre-money: $10M
  Option pool: 15% (newly created)
  Effective pre-money for founders: $10M × (1 - 0.15) = $8.5M
  The 15% option pool dilutes FOUNDERS, not investors

Negotiate:
  - Pool should be based on HIRING PLAN, not arbitrary percentage
  - Any unallocated pool should be canceled after 12-18 months
  - New investors should fund pool increases, not existing shareholders
  - 10% is typical for seed; 15-20% for Series A
```

---

## Part 5: Control Terms That Matter for Solo Founders

### Key Person Risk

```yaml
The problem for solo founders:
  - The business = you
  - If you leave/get sick, the business suffers
  - Investors want protection

What investors may ask for:
  - Key person insurance (paid by company, payable to company)
  - Vesting acceleration tied to your continued involvement
  - Right to replace you if you stop being effective

What to negotiate:
  - Key person insurance: Accept (industry standard, ~$1-2M policy)
  - Vesting acceleration: Accept single trigger (company sale) but REJECT double trigger (investor fires you)
  - Replacement: Only for cause (fraud, criminal conviction, gross negligence)
```

### Information Rights

```yaml
Standard information rights:
  - Monthly/quarterly financial statements
  - Annual audited financials (at $5M+ ARR)
  - Annual budget
  - Right to visit premises
  - Right to inspect books

Reasonable for solo founder:
  - Monthly: MRR, churn, cash balance (email update is fine)
  - Quarterly: Full P&L, balance sheet, metrics
  - Annual: Budget, business plan
  - 48 hours notice for visits (no surprise visits)
```

### Right of First Refusal (ROFR)

```yaml
If you want to sell your shares, investors get first dibs.

Standard: Company gets ROFR, then major investors
Period: 30-90 days

This matters if:
  - You want to do a secondary sale (sell some shares for liquidity)
  - You get an acquisition offer for your shares
  - You want to transfer shares to family

Negotiate: ROFR should not apply to:
  - Token transfers (< 1% of shares)
  - Transfers to family trusts
  - Charitable donations
```

### Drag-Along Rights

```yaml
If >50-67% of shareholders want to sell the company, 
minority holders must also sell.

Standard for growth companies.
Solo founder note: You'll likely control the majority, so this protects YOU from minority hold-outs.

Accept: Standard drag-along at 50-67% threshold
```

---

## Part 6: The Term Sheet Negotiation

### What's Negotiable vs. Not

```yaml
HIGHLY NEGOTIABLE (fight for these):
  - Valuation (pre-money)
  - Liquidation preference (insist on 1x non-participating)
  - Option pool size (should be based on hiring plan)
  - Board composition (you should have majority control)
  - Vesting (4-year with 1-year cliff is standard — don't let them accelerate)

SOMEWHAT NEGOTIABLE:
  - Anti-dilution (push back on full ratchet)
  - Protective provisions (limit to standard list)
  - Information rights (monthly is fine, audited is expensive)
  - Pro-rata rights (limit to $100K+ investors)
  - No-shop clause (limit to 30-45 days)

NOT NEGOTIABLE (focus elsewhere):
  - 4-year vesting (universal standard)
  - 1-year cliff (also universal)
  - Board observer rights (standard for investors)
  - Standard IP assignment
  - Standard confidentiality
```

### Red Flag Terms (Walk Away)

```yaml
These are deal-killers for solo founders:

❌ Participating preferred stock
  "We get our money back AND share in the upside"
  → This is greedy and unfair. Walk away.

❌ Full ratchet anti-dilution
  "If you raise at a lower price, we get free shares"
  → This makes raising a down round nearly impossible. Walk away.

❌ Investor-controlled board
  "We get 2 of 3 board seats"
  → You lose control of your company. Walk away.

❌ Vesting tied to employment (not equity)
  "If you leave, you lose ALL unvested shares"
  → Standard, but ensure single-trigger acceleration on sale.

❌ Personal guarantees
  "You personally guarantee the investment"
  → This is debt, not equity. Walk away.

❌ No-co-founder clause
  "We can veto your co-founder choices"
  → You should decide who you work with.
```

### Term Sheet Negotiation Script

```yaml
YOU: "We love working with you, and we're aligned on vision.
There's one term we need to adjust..."

INVESTOR: "Which one?"

YOU: "The liquidation preference. You proposed 2x participating.
For a seed-stage SaaS company, 1x non-participating is the standard.
We'd be setting a bad precedent for future rounds."

INVESTOR: "We need downside protection."

YOU: "I understand. 1x non-participating does protect your downside —
you get your full investment back before anyone else. Participating
would be unusual for a seed round and would complicate our Series A."

INVESTOR: "Let me check with my partners..."

[This works 70% of the time. 30% they'll say no — and you should walk.]
```

---

## Part 7: The Cap Table

### What a Cap Table Looks Like

```yaml
SIMPLIFIED CAP TABLE (Post-Series A)

Shareholder          | Shares    | % Ownership | Type
─────────────────────|───────────|─────────────|──────────
You (founder)        | 8,000,000 | 64.0%       | Common
Co-founder (if any)  | 0         | 0%          | N/A (solo)
SAFE Holders (converted)| 1,000,000 | 8.0%     | Common
Series A Investors   | 2,500,000 | 20.0%       | Preferred
Option Pool          | 1,000,000 | 8.0%        | Unissued
─────────────────────|───────────|─────────────|──────────
Total                | 12,500,000| 100%        |

Price per share: $2.00 (Series A: $5M / 2.5M shares)
Pre-money: $8M
Post-money: $13M
```

### Cap Table Management Tools

```yaml
Free / Low-cost:
  - Carta (free for first year, then $150/month)
  - Pulley (startup-friendly, from $0/month)
  - Gust (equity management, free basic tier)
  - Spreadsheet (works for simple cap tables, but dangerous)

Solo founder recommendation:
  - Use a spreadsheet until your first priced round
  - Then use Carta or Pulley (investors will expect it)
```

---

## Part 8: The Solo Founder's VC Survival Guide

### Before Taking VC Money

```yaml
1. Can you grow without VC?
  → Yes: Only take VC if terms are exceptional
  → No: VC is survival, not optional

2. Can you handle the pressure?
  - VCs expect 10x+ returns
  - Monthly board meetings
  - Constant pressure to grow faster
  - May push you to replace yourself with "more experienced" CEO

3. Do you want to build a $100M+ company?
  → Yes: VC aligns (they need big exits)
  → No (lifestyle or small exit): Bootstrap — VC will fire you

4. Do you understand what you're signing?
  → Yes: Proceed
  → No: Hire a startup lawyer ($500-$1K/hour, worth every penny)
```

### The Solo Founder VC Checklist

```yaml
Before signing:

☐ Interview 3+ references from this VC's portfolio
  "What happens when things go wrong?"
  "Do they add value or just add pressure?"

☐ Hire a startup lawyer (NOT your family attorney)
  "Review the term sheet for founder-unfriendly terms"

☐ Model your dilution through 3 more rounds
  "Do I still have meaningful ownership at Series C?"

☐ Know your walk-away terms
  "What terms would make me say no?"

☐ Read the entire term sheet
  "Do I understand every clause?"

☐ Have an exit strategy
  "What's my personal outcome if we sell for $50M?"
  "What if we sell for $10M?"
```

### The Most Important Thing

> **The best VC deal is the one you don't need.**
> 
> The more you need the money, the worse the terms will be.
> The less you need it, the better you can negotiate.
> 
> Raise when you have leverage. Not when you're desperate.

If you're a solo founder with $15K MRR, growing 15% MoM, with 12 months of runway — you have all the leverage. Terms will be founder-friendly. Investors will compete.

If you're at $3K MRR, growing 5% MoM, with 3 months of runway — you have no leverage. Terms will be harsh. You may be better off getting a job and building on the side.

## Remember

VC is a tool, not a prize. The goal is not to "get funded" — the goal is to build a valuable business. Sometimes funding helps. Sometimes it distracts. Know which camp you're in before you start.