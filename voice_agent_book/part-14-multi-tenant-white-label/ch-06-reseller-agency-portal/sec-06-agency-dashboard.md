# Section 06: Agency Dashboard & Analytics

The agency dashboard provides multi-tenant visibility across all sub-accounts. It shows aggregate metrics (total calls, active agents, revenue), per-sub-account performance tables, trend charts, and alerts for accounts that need attention. The dashboard is the reseller's primary operational tool for managing their portfolio.

Key dashboard components: portfolio overview (total sub-accounts, active vs inactive, trial expiring soon), revenue metrics (MRR, ARR, churn rate), usage analytics (call volume trends, top agents, peak hours), health scores (per-account indicators based on usage, sentiment, errors), and comparison views (top performers vs at-risk accounts).

The analytics system aggregates data from all sub-accounts using a separate analytics pipeline that respects tenant isolation. Aggregated data does not expose individual call content—only metadata and metrics. Resellers can export reports in CSV/PDF format for their own reporting.
