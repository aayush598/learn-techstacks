# BI Tools for Solo Founders

A practical guide to Business Intelligence (BI) tools that solo SaaS founders can use for free or at low cost. Covers Metabase, Apache Superset, Tableau Public, and Google Looker Studio — with setup instructions, use cases, and integration patterns.

---

## Part 1: Why Solo Founders Need a BI Tool

### When Analytics Tools Aren't Enough

Product analytics tools (PostHog, Amplitude) are great for user behavior. Dedicated SaaS metrics tools (ChartMogul) are great for subscription metrics. But both have limitations:

| Need | Analytics Tools | Metrics Tools | BI Tool (This Guide) |
|------|----------------|---------------|---------------------|
| Custom metrics | Limited | Fixed set | Any metric you can query |
| Cross-data joins | No | No | Yes (revenue + usage + support) |
| Raw data access | Aggregated | Aggregated | Raw tables |
| Custom dashboards | Template-based | Template-based | Fully custom |
| Self-host/control | Paid cloud | Paid cloud | Free self-host |

### When to Add a BI Tool

| Stage | Tool to Use | Why |
|-------|-------------|-----|
| Pre-revenue to $5K MRR | Stripe + Google Sheets | No need for BI yet |
| $5K - $15K MRR | Looker Studio (free) | Need basic reporting |
| $15K - $50K MRR | Metabase (self-hosted free) | Need custom SQL queries |
| $50K+ MRR | Superset or Metabase | Need advanced dashboards |

---

## Part 2: Tool Deep Dives

### Google Looker Studio (Formerly Google Data Studio)

**Best for:** Solo founders who want a free, cloud-based solution with no infrastructure to manage.

**Pricing:** Free

**Key Features:**
- Drag-and-drop report builder
- 800+ data connectors (Google Analytics, Sheets, Stripe via community connectors)
- Interactive filters and date controls
- Shareable reports (view-only or editable)
- Scheduled email delivery
- Embedding in websites

**Pros for Solo Founders:**
- Completely free
- No setup or maintenance
- Familiar Google ecosystem
- Easy to share with investors/partners
- Good for marketing dashboards

**Cons for Solo Founders:**
- Limited data transformation (need to pre-process data)
- Community connectors may break
- Can be slow with large datasets (> 100K rows)
- No self-host option (data on Google's servers)
- Limited visualization types compared to dedicated BI

**When to Use:**
- Marketing dashboards (Google Analytics + Google Ads data)
- Simple revenue reporting (Stripe CSV export → Sheets → Looker)
- Investor update reports (clean, shareable)

**Setup Process:**

```
Step 1: Prepare Your Data
  - Export reports from Stripe to Google Sheets (regularly)
  - Set up Google Analytics (if using for web traffic)
  - Create a "Data" sheet with clean, structured data

Step 2: Create Looker Studio Account
  - Go to lookerstudio.google.com
  - Sign in with Google account

Step 3: Create Data Source
  - Click "Create" → "Data Source"
  - Select "Google Sheets" (or another connector)
  - Choose your spreadsheet and sheet
  - Configure field types (date, number, currency)

Step 4: Build Report
  - Add charts: Time series (MRR over time), Scorecards (current MRR)
  - Add date range filter
  - Add calculated fields:
    MRR Growth % = (Current MRR - Previous MRR) / Previous MRR × 100
  - Style to your preference

Step 5: Share
  - Click "Share" → enter email addresses
  - Set permissions (can view, can edit)
  - Schedule email delivery (daily/weekly/monthly)
```

**Looker Studio Calculated Field Formulas:**

```yaml
MRR Growth Rate:
  (SUM(Current MRR) - SUM(Previous MRR)) / SUM(Previous MRR) * 100

CAC:
  SUM(Total S&M Spend) / COUNT_DISTINCT(Customer ID)

Monthly Churn Rate:
  COUNT_DISTINCT(CASE WHEN Status = 'Churned' THEN Customer ID END) / 
  COUNT_DISTINCT(Customer ID) * 100

ARR:
  SUM(Monthly MRR) * 12

LTV (Simple):
  AVG(ARPU) / (Churn Rate / 100)
```

**Sample Dashboard Layout:**

```yaml
Page 1: Executive Overview
  - Scorecard: Current MRR
  - Scorecard: MRR Growth %
  - Scorecard: Active Customers
  - Scorecard: Churn Rate
  - Time Series: MRR over last 12 months
  - Bar Chart: New Customers by Month

Page 2: Revenue Detail
  - Table: Revenue by Plan Tier
  - Time Series: New MRR vs Churn MRR
  - Bar Chart: Expansion MRR by Month

Page 3: Customer Analysis
  - Scorecard: ARPU
  - Scorecard: LTV/CAC
  - Table: Customers by Acquisition Channel
  - Pie Chart: Plan Distribution
```

### Metabase

**Best for:** Solo founders who want to connect directly to their database and run custom SQL queries for free.

**Pricing:** Free (self-hosted, open source), Cloud ($85/month)

**Key Features:**
- SQL query editor with autocomplete
- Visual query builder (no SQL)
- Auto-generated dashboards
- Dashboard subscriptions (email, Slack)
- Embedding
- Alerts (when metric crosses threshold)
- Data model management (define metrics, segments)

**Pros for Solo Founders:**
- Free self-hosted (Docker deployment, 15 minutes)
- Direct database connection (PostgreSQL, MySQL, MongoDB, etc.)
- SQL and visual query modes
- Clean, modern UI
- Active open source community
- Pulse/alert features for critical metrics

**Cons for Solo Founders:**
- Self-hosting requires a server (can run on $5/month VPS)
- Need basic SQL knowledge for best results
- No built-in data pipeline (need to get data into your DB)
- Limited visualization types (no custom charting)
- No mobile app

**When to Use:**
- Your app database already has revenue, user, and usage data
- You're comfortable with basic SQL
- You want alerts on key metrics (MRR drops, churn spikes)
- You need to share dashboards with co-founders or advisors

**Setup Process (Self-Hosted, Docker):**

```yaml
# docker-compose.yml
version: '3.8'
services:
  metabase:
    image: metabase/metabase:latest
    container_name: metabase
    ports:
      - "3000:3000"
    environment:
      MB_DB_TYPE: postgres
      MB_DB_DBNAME: metabase
      MB_DB_HOST: postgres
      MB_DB_PORT: 5432
      MB_DB_USER: metabase
      MB_DB_PASS: yourpassword
    volumes:
      - metabase_data:/metabase.db
    restart: always
  
  postgres:
    image: postgres:15
    container_name: metabase-db
    environment:
      POSTGRES_DB: metabase
      POSTGRES_USER: metabase
      POSTGRES_PASSWORD: yourpassword
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: always

volumes:
  metabase_data:
  postgres_data:
```

```bash
# Deploy
docker-compose up -d

# Access at http://localhost:3000
# Configure database connection in the UI
```

**Essential SQL Queries for Metabase:**

```sql
-- MRR by Month
SELECT 
  DATE_TRUNC('month', subscription_start_date) AS month,
  SUM(monthly_price) AS mrr
FROM subscriptions
WHERE status = 'active'
GROUP BY month
ORDER BY month DESC;

-- Monthly Churn Rate
WITH monthly_customers AS (
  SELECT 
    DATE_TRUNC('month', date) AS month,
    COUNT(DISTINCT customer_id) AS active_customers
  FROM subscription_events
  WHERE event_type = 'active'
  GROUP BY month
),
churned_customers AS (
  SELECT 
    DATE_TRUNC('month', cancellation_date) AS month,
    COUNT(DISTINCT customer_id) AS churned
  FROM subscriptions
  WHERE cancellation_date IS NOT NULL
  GROUP BY month
)
SELECT 
  m.month,
  m.active_customers,
  COALESCE(c.churned, 0) AS churned,
  ROUND(COALESCE(c.churned, 0) * 100.0 / m.active_customers, 2) AS churn_rate
FROM monthly_customers m
LEFT JOIN churned_customers c ON m.month = c.month
ORDER BY m.month DESC;

-- Feature Adoption (Count of users using each feature)
SELECT 
  feature_name,
  COUNT(DISTINCT user_id) AS users,
  COUNT(DISTINCT CASE WHEN event_date > CURRENT_DATE - 7 THEN user_id END) AS weekly_users
FROM feature_events
WHERE event_type = 'use'
GROUP BY feature_name
ORDER BY users DESC;

-- Cohort Retention
WITH first_activity AS (
  SELECT
    user_id,
    DATE_TRUNC('month', MIN(event_date)) AS cohort_month
  FROM user_events
  WHERE event_type = 'signup'
  GROUP BY user_id
),
monthly_activity AS (
  SELECT
    u.user_id,
    u.cohort_month,
    DATE_TRUNC('month', e.event_date) AS activity_month,
    EXTRACT('month' FROM e.event_date) - EXTRACT('month' FROM u.cohort_month) 
      + (EXTRACT('year' FROM e.event_date) - EXTRACT('year' FROM u.cohort_month)) * 12 AS month_number
  FROM first_activity u
  JOIN user_events e ON u.user_id = e.user_id
  WHERE e.event_type = 'active'
)
SELECT 
  cohort_month,
  month_number,
  COUNT(DISTINCT user_id) AS active_users
FROM monthly_activity
GROUP BY cohort_month, month_number
ORDER BY cohort_month, month_number;
```

**Alert Configuration:**

```yaml
Create an alert when:
  "Today's signups < 5" → Slack notification
  "MRR (this month) < MRR (last month) * 0.95" → Email
  "Error rate > 5%" → Slack notification

Setup:
  1. Run the query that defines your metric
  2. Click "Alert" → "Add alert"
  3. Set condition (e.g., "Results < 5")
  4. Choose channel (Slack, Email)
  5. Set check frequency (hourly, daily)
```

### Apache Superset

**Best for:** Solo founders who need advanced visualizations, drill-down capability, and are comfortable with Python/DevOps.

**Pricing:** Free (open source, self-hosted)

**Key Features:**
- Rich visualization library (50+ chart types)
- SQL Lab (ad-hoc SQL queries)
- Dashboard with drill-down and cross-filtering
- Semantic layer (define metrics once, reuse)
- Row-level security (for multi-tenant data)
- API for embedding and automation

**Pros for Solo Founders:**
- Most powerful visualization options
- SQL Lab is excellent for exploration
- Can handle very large datasets
- Active community and frequent updates
- Row-level security (useful if sharing with customers)

**Cons for Solo Founders:**
- Complex setup (requires Docker, Redis, database)
- Steeper learning curve than Metabase
- Heavier infrastructure requirements
- Overkill for simple reporting needs
- Documentation can be scattered

**When to Use:**
- You need advanced chart types (heat maps, sankey, deck.gl)
- You have complex data pipelines
- You need to embed analytics in your product (customer-facing dashboards)
- You're already using Python/Flask in your stack

**Setup Process (Docker):**

```yaml
# docker-compose.yml for Superset
version: '3.8'
services:
  redis:
    image: redis:7
    restart: always
    
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: superset
      POSTGRES_USER: superset
      POSTGRES_PASSWORD: superset
      POSTGRES_HOST: db
    restart: always
    
  superset:
    image: apache/superset:latest
    environment:
      SUPERSET_SECRET_KEY: your-secret-key-change-me
      SUPERSET__SQLALCHEMY_DATABASE_URI: postgresql://superset:superset@db:5432/superset
      SUPERSET__REDIS_CACHE_URL: redis://redis:6379/0
    ports:
      - "8088:8088"
    depends_on:
      - db
      - redis
    restart: always
```

```bash
# Initialize
docker-compose up -d
docker-compose exec superset superset fab create-admin \
  --username admin --firstname Admin --lastname User --email admin@example.com --password admin
docker-compose exec superset superset db upgrade
docker-compose exec superset superset init
```

### Tableau Public

**Best for:** Creating polished, interactive visualizations for public sharing (investor reports, blog posts).

**Pricing:** Free (Public), $75/user/month (Creator), $15/user/month (Viewer)

**Key Features:**
- Industry-leading visualization quality
- Drag-and-drop interface (no coding)
- Interactive dashboards (hover, filter, drill-down)
- Storytelling (sequence of dashboards)
- Public gallery for sharing

**Pros for Solo Founders:**
- Most beautiful visualization output
- Free for public content
- No infrastructure to manage (cloud-based)
- Strong community and learning resources
- Good for investor-facing materials

**Cons for Solo Founders:**
- Tableau Public dashboards are PUBLIC (anyone can see your data)
- Cannot connect to databases (files only: CSV, Excel, Google Sheets)
- Desktop app only (requires download)
- 15 million row limit on Public
- Free version watermarks your work

**When to Use:**
- Creating polished investor updates
- Publishing public benchmarks or reports
- Exploratory analysis (drag-and-drop is fast)
- One-time analysis (not recurring dashboards)

**Setup Process:**

```yaml
1. Download Tableau Public Desktop (free)
2. Prepare your data as CSV or Excel
3. Open Tableau Public → Connect to file
4. Drag dimensions and measures to create visualizations
5. Build dashboard sheets
6. Add interactivity (filters, tooltips, actions)
7. Save to Tableau Public Gallery
8. Share the link

Limitations for SaaS:
  - No live database connection (must export data)
  - Must manually refresh data
  - All dashboards are publicly visible
  - Not suitable for operational dashboards
```

---

## Part 3: Comparison Matrix

```yaml
                | Looker Studio | Metabase   | Superset    | Tableau Public
────────────────|───────────────|────────────|─────────────|───────────────
Price           | Free          | Free/$$    | Free        | Free (Public)
Hosting         | Google Cloud  | Self-host  | Self-host   | Desktop app
Setup Difficulty| Easy          | Medium     | Hard        | Easy
SQL Support     | Limited       | Excellent  | Excellent   | Limited
Visualizations  | 20+           | 20+        | 50+         | 100+
Database Conn.  | 800+          | Direct SQL | Direct SQL  | Files only
Data Pipeline   | No            | No         | No          | No
Alerts          | No            | Yes        | No          | No
Embedding       | Yes           | Yes        | Yes         | Yes (paid)
Sharing         | Link          | Link       | Link        | Public Gallery
Investor Ready  | Good          | Good       | Good        | Excellent
Mobile          | Yes           | Web only   | Web only    | Web only
Best for Solo   | Free, easy    | SQL-first  | Advanced viz| Polished viz
```

---

## Part 4: Building Your BI Stack

### The Solo Founder BI Architecture

```yaml
DATA LAYER (Free):
  PostgreSQL / SQLite (your app database)
  + Google Sheets (for manual data)
  + CSV exports from Stripe

ANALYTICS LAYER (Free):
  Metabase or Looker Studio

PRESENTATION LAYER:
  Metabase dashboards (internal)
  Looker Studio reports (investor/advisor)
```

### Data Pipeline (Minimal)

For the technical solo founder:

```yaml
1. Your App Database (PostgreSQL)
   ↕ nightly export (cron job or pg_dump)
2. Metabase connected directly
   ↕ dashboards built on live data
3. Optionally: Export to Google Sheets for Looker Studio
   using a script:
```

```python
# daily_export.py — Export key metrics to Google Sheets
import psycopg2
import gspread
from datetime import datetime

# Connect to database
conn = psycopg2.connect(
    dbname="yourdb",
    user="youruser",
    password="yourpass",
    host="localhost"
)

# Get daily metrics
cur = conn.cursor()
cur.execute("""
    SELECT 
        DATE_TRUNC('day', created_at) as day,
        COUNT(DISTINCT id) FILTER (WHERE event = 'signup') as signups,
        COUNT(DISTINCT id) FILTER (WHERE event = 'payment') as payments,
        SUM(amount) FILTER (WHERE event = 'payment') as revenue
    FROM events
    WHERE created_at > CURRENT_DATE - 1
    GROUP BY day
""")
data = cur.fetchall()

# Update Google Sheet
gc = gspread.service_account('credentials.json')
sh = gc.open('SaaS Metrics')
worksheet = sh.worksheet('Daily')
worksheet.append_rows(data)
```

### The Minimum Viable BI Setup

If you have 2 hours to set up a BI system:

```yaml
Hour 1: Google Looker Studio
  1. Export Stripe data to Google Sheets
  2. Create Looker Studio data source from Sheets
  3. Build 3 charts: MRR trend, new customers, churn rate
  4. Add date filter and scorecards

Hour 2: Metabase (optional, if you have a database)
  1. Deploy with Docker (15 min)
  2. Connect to your app database (10 min)
  3. Write 3 key SQL queries (20 min)
  4. Build simple dashboard (15 min)
```

---

## Part 5: Use Cases and Example Dashboards

### Use Case 1: SaaS KPI Dashboard (Metabase)

```yaml
Dashboard: "SaaS Executive Dashboard"
Refresh: Daily

Charts:
  1. MRR Trend (Time Series, last 12 months)
  2. MRR Breakdown (Stacked Area: New, Expansion, Churn)
  3. Customer Count (Scorecard, current)
  4. Monthly Churn Rate (Gauge, target < 5%)
  5. New Customers by Source (Bar Chart)
  6. ARPU Trend (Line Chart)
  7. LTV/CAC Ratio (Scorecard, target > 3x)
  8. Active Users (Number over time)
  9. Top 10 Customers by MRR (Table)
```

### Use Case 2: Investor Update Dashboard (Looker Studio)

```yaml
Dashboard: "Investor Update Q3 2024"
Refresh: Monthly, manually

Charts:
  1. Executive Summary (4 scorecards: MRR, ARR, Customers, Churn)
  2. MRR Growth (Time Series, 24 months)
  3. Revenue Retention (NRR Coaster)
  4. Cohort Retention Table (Monthly cohorts)
  5. Unit Economics (Scorecards: LTV, CAC, Payback)
  6. Channel Performance (Table: channel, spend, CAC, customers)
  7. Financial Summary (Revenue, COGS, OpEx, Net Income)
  8. Forward Outlook (Projected MRR, milestones)

Style:
  - Company logo
  - Consistent color scheme
  - Clean, minimal layout
  - PDF export for email
```

### Use Case 3: Marketing Dashboard (Looker Studio)

```yaml
Dashboard: "Marketing Performance"
Refresh: Weekly

Charts:
  1. Website Traffic (Time Series with source breakdown)
  2. Trial Signups (Time Series)
  3. Trial → Paid Conversion (Funnel)
  4. CAC by Channel (Bar Chart)
  5. Blog Post Performance (Table: views, clicks, signups)
  6. SEO Rankings (Table: keyword, position, traffic)
  7. Email Campaign Performance (Open rate, click rate)
  8. Cost per Lead (Line Chart over time)
```

### Use Case 4: Product Analytics Dashboard (Metabase)

```yaml
Dashboard: "Product Health"
Refresh: Daily

Charts:
  1. Daily Active Users (Time Series)
  2. Weekly Retention (Cohort Table)
  3. Feature Adoption (Bar Chart: % of users using each feature)
  4. Activation Funnel (Waterfall: signup → profile → action)
  5. Session Recordings to Review (Table: user, date, duration)
  6. Errors by Page (Table: page, error count)
  7. Page Load Time (Gauge, target < 2s)
```

### Use Case 5: Financial Dashboard (Looker Studio)

```yaml
Dashboard: "Financial Health"
Refresh: Monthly

Charts:
  1. Cash Balance (Time Series, projected 12 months)
  2. Runway (Scorecard, months remaining)
  3. Revenue vs Expenses (Overlaid area chart)
  4. Deferred Revenue (Scorecard)
  5. Gross Margin (Gauge, target > 75%)
  6. Burn Rate (Scorecard, monthly)
  7. Expense Breakdown (Pie or Treemap)
  8. P&L Summary (Table: revenue, COGS, OpEx, net income)
```

---

## Part 6: Common BI Mistakes and How to Avoid Them

### Mistake 1: BI Before Product-Market Fit

**Wrong:** Building a 20-dashboard BI system when you have 50 users and no PMF.

**Right:** Use Stripe + Google Sheets until you have consistent growth (> $5K MRR, > 100 customers).

### Mistake 2: Connecting Production Database Directly

**Wrong:** Running heavy BI queries against your production database (slows down your app).

**Right:** Use a read replica or a dedicated analytics database. If not possible, run queries during off-peak hours.

### Mistake 3: Over-Engineering the Data Pipeline

**Wrong:** Setting up Airflow, dbt, and data warehouse before you have business questions.

**Right:** Start with direct database connection (Metabase). Add pipeline complexity only when you need it.

### Mistake 4: Building Dashboards Nobody Looks At

**Wrong:** Spending 10 hours building a beautiful dashboard, then checking it once.

**Right:** Build one chart at a time. Only add a chart if you'll look at it weekly. Set reminders to review.

### Mistake 5: Not Pre-Aggregating Data

**Wrong:** Running queries that compute metrics from raw event data every time (slow).

**Right:** Create materialized views or pre-aggregated tables for common metrics.

```sql
-- Create a materialized view for daily MRR
CREATE MATERIALIZED VIEW daily_mrr AS
SELECT 
  DATE(created_at) as day,
  SUM(amount) as revenue,
  COUNT(DISTINCT customer_id) as active_customers
FROM subscriptions
WHERE status = 'active'
GROUP BY DATE(created_at);

-- Refresh daily
REFRESH MATERIALIZED VIEW daily_mrr;
```

---

## Part 7: The Solo Founder BI Decision Guide

### Questionnaire

```
1. Do you have a database with your app data?
   → Yes: Metabase (best for SQL querying)
   → No: Looker Studio (best for CSV/Sheets)
   → Both: Use both for different purposes

2. Do you need to share dashboards externally?
   → Yes (investors, partners): Looker Studio (easiest sharing)
   → No (internal only): Metabase or Superset

3. How technical are you?
   → Comfortable with SQL: Metabase
   → No SQL, prefer visual: Looker Studio

4. What's your budget?
   → $0/month: Looker Studio + Metabase (self-host)
   → $85/month: Metabase Cloud (skip self-hosting)

5. What's your data volume?
   → < 100K rows: Any tool works
   → 100K-1M rows: Metabase or Looker Studio
   → 1M+ rows: Superset (best performance at scale)
```

### Recommended Stack by Stage

```yaml
Pre-Seed ($0 revenue):
  Stack: Google Sheets + Looker Studio
  Cost: $0
  Time: 2 hours setup

Seed ($5K-$20K MRR):
  Stack: Metabase (self-host) + Looker Studio
  Cost: $5-10/month (VPS for Metabase)
  Time: 4 hours setup

Series A ($20K+ MRR):
  Stack: Metabase or Superset + Stripe analytics
  Cost: $10-50/month
  Time: 8 hours setup
```

## Quick Start: What to Do This Weekend

```
Saturday Morning (2 hours):
  1. Install Metabase via Docker:
     docker run -d -p 3000:3000 --name metabase metabase/metabase

  2. Connect to your database (or start with sample data)

  3. Write 3 SQL queries:
     - MRR by month
     - New customers by month  
     - Feature adoption rates

  4. Build a simple dashboard with 3 charts

Saturday Afternoon (1 hour):
  5. Connect Looker Studio to a Google Sheet
  6. Export key data manually to the sheet
  7. Build 3 charts in Looker Studio
  8. Share with one advisor for feedback

Sunday (30 min):
  9. Set Metabase alerts for:
     - MRR drops > 10%
     - Zero signups in 24 hours
  10. Schedule weekly email delivery of your dashboard
```

You now have a free BI system that gives you more insight than many $1,000/month setups. As you grow, you can incrementally upgrade — but for a solo founder, this is all you need.