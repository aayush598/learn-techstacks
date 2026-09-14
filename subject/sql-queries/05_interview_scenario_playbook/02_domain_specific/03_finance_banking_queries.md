# Finance and Banking SQL Scenarios — 100 Interview Q&A

Core schema hints (columns used vary by query; `+` marks extras beyond the base list):
- `accounts(account_id, customer_id, balance, opened_at, product_type)`
- `transactions(tx_id, account_id, tx_type, amount, tx_time, merchant, status, ccy, correlated_tx_id)` — `tx_type` ∈ {credit, debit, purchase, payment, transfer, atm, fee, interest}; benchmark: credit/payment/interest are inflows, debit/purchase/atm/transfer/fee are outflows.
- `cards(card_id, account_id, credit_limit, apr)`
- `loans(loan_id, customer_id, principal, rate, term_months, originated_at, status, paid_principal, pd_pct, lgd_pct)`
- `loan_payments(loan_id, payment_no, amount, paid_at)`, `payments(payment_id, account_id, amount, initiated_at, settled_at, status, sender_country, recipient_country)`
- `deposits(account_id, amount, rate, opened_at, maturity_date)`
- `receivables(account_id, due_date, paid_date, amount)`
- `trades(trade_id, account_id, symbol, side, qty, price, traded_at, realized_pnl)`, `portfolio(portfolio_id, customer_id, name, units)`, `holdings(portfolio_id, symbol, qty)`, `prices(symbol, px_date, close, volume)`, `securities(symbol, name, sector, asset_class)`
- `fx_rates(ccy_pair, rate_date, rate)`, `customers(customer_id, name, country, kyc_status, passport, address, phone, email, id_doc_expiry)`
- Insurance: `insurance(policy_id, policy_type, premium, claims_paid, status, effective, expiry)`, `claims(policy_id, claim_amount, status, filed_at, settled_at)`, `renewals(policy_id, renewal, prev_policy_type)`
- Risk: `trader_limits(trader_id, limit_amount)`, `risk_limits(portfolio_id, limit_amount)`, `exposures(bank_id, asset_class, exposure)`, `asset_classes(asset_class, risk_weight)`, `targets(portfolio_id, symbol, target_w)`, `benchmark_returns(px_date, ret)`, `cashflows(flow_date, ccy, amount, category)`, `fx_positions(ccy, notional, side, entry_rate)`, `card_authorizations(card_id, status, decline_reason)`

## Q1: Running account balance from the transaction stream

**Query:**
```sql
SELECT account_id, tx_id, tx_time, amount,
       SUM(CASE WHEN tx_type IN ('credit','payment','interest') THEN amount
                ELSE -amount END)
           OVER (PARTITION BY account_id ORDER BY tx_time, tx_id
                 ROWS UNBOUNDED PRECEDING) AS running_balance
FROM transactions
ORDER BY account_id, tx_time;
```
**Explanation:** A cumulative window sum converts each transaction into a signed delta; ordering by `tx_time, tx_id` makes tie-breaking deterministic.

**Alt1:**
```sql
-- MySQL 8 (same result, explicit frame)
SELECT account_id, tx_id, tx_time, amount,
       SUM(CASE WHEN tx_type IN ('credit','payment','interest') THEN amount
                ELSE -amount END)
           OVER (PARTITION BY account_id ORDER BY tx_time, tx_id
                 ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS running_balance
FROM transactions;
```

## Q2: Accounts whose running balance ever goes negative

**Query:**
```sql
WITH bal AS (
  SELECT account_id, tx_time,
         SUM(CASE WHEN tx_type IN ('credit','payment','interest') THEN amount
                  ELSE -amount END)
             OVER (PARTITION BY account_id ORDER BY tx_time, tx_id) AS running
  FROM transactions
)
SELECT DISTINCT account_id
FROM bal
WHERE running < 0;
```
**Explanation:** Compute the running balance per account, then keep only accounts where at least one row is below zero.

**Alt1:**
```sql
SELECT DISTINCT account_id
FROM transactions t
WHERE (
  SELECT SUM(CASE WHEN tx_type IN ('credit','payment','interest') THEN amount
                  ELSE -amount END)
  FROM transactions t2
  WHERE t2.account_id = t.account_id
    AND t2.tx_time <= t.tx_time
) < 0;
```

## Q3: First transaction that pushed an account negative

**Query:**
```sql
-- PostgreSQL
WITH bal AS (
  SELECT account_id, tx_id, tx_time,
         SUM(CASE WHEN tx_type IN ('credit','payment','interest') THEN amount
                  ELSE -amount END)
             OVER (PARTITION BY account_id ORDER BY tx_time, tx_id) AS running
  FROM transactions
),
with_prev AS (
  SELECT *, LAG(running, 1, 0) OVER (PARTITION BY account_id ORDER BY tx_time, tx_id) AS prev_bal
  FROM bal
)
SELECT account_id, tx_id, tx_time, running AS balance_after
FROM with_prev
WHERE running < 0 AND prev_bal >= 0
ORDER BY account_id, tx_time;
```
**Explanation:** `LAG` captures the balance before each transaction; the tie-breaker row is where the balance crosses from non-negative to negative.

## Q4: Minimum daily balance per account per day

**Query:**
```sql
-- PostgreSQL
WITH bal AS (
  SELECT account_id, tx_time::date AS day, tx_id,
         SUM(CASE WHEN tx_type IN ('credit','payment','interest') THEN amount
                  ELSE -amount END)
             OVER (PARTITION BY account_id ORDER BY tx_time, tx_id) AS running
  FROM transactions
)
SELECT account_id, day, MIN(running) AS min_daily_balance
FROM bal
GROUP BY account_id, day
ORDER BY account_id, day;
```
**Explanation:** Snapshot the running balance at every transaction, then take the minimum within each account-day.

## Q5: Categorize transactions with CASE

**Query:**
```sql
SELECT tx_id, account_id, tx_type, amount,
       CASE
         WHEN tx_type = 'atm'    AND amount > 5000  THEN 'large_cash_withdrawal'
         WHEN tx_type IN ('purchase')               THEN 'card_purchase'
         WHEN tx_type = 'payment'                   THEN 'credit_card_payment'
         WHEN tx_type = 'transfer' AND amount > 10000 THEN 'large_transfer'
         WHEN tx_type = 'fee'                       THEN 'bank_fee'
         WHEN tx_type = 'interest'                  THEN 'interest_credit'
         ELSE 'routine'
       END AS category
FROM transactions;
```
**Explanation:** A CASE ladder maps each transaction into a business bucket; order matters — test the most specific conditions first.

## Q6: Count transactions per category per account

**Query:**
```sql
SELECT account_id,
       SUM(CASE WHEN tx_type IN ('credit','payment','interest') THEN 1 ELSE 0 END) AS inflows,
       SUM(CASE WHEN tx_type IN ('debit','purchase','atm','transfer','fee') THEN 1 ELSE 0 END) AS outflows,
       COUNT(*) AS total_tx
FROM transactions
GROUP BY account_id
ORDER BY total_tx DESC;
```
**Explanation:** `SUM(CASE...)` is the portable way to pivot row counts into columns.

## Q7: Detect overdraft events (debit causes balance below zero)

**Query:**
```sql
WITH bal AS (
  SELECT account_id, tx_id, tx_time, tx_type, amount,
         SUM(CASE WHEN tx_type IN ('credit','payment','interest') THEN amount
                  ELSE -amount END)
             OVER (PARTITION BY account_id ORDER BY tx_time, tx_id) AS running,
         COALESCE(SUM(CASE WHEN tx_type IN ('credit','payment','interest') THEN amount
                           ELSE -amount END)
             OVER (PARTITION BY account_id ORDER BY tx_time, tx_id
                   ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING), 0) AS before_tx
  FROM transactions
)
SELECT account_id, tx_id, tx_time, amount
FROM bal
WHERE running < 0 AND before_tx >= 0;
```
**Explanation:** Two window frames give the balance after and before a transaction; an overdraft event is a transition from non-negative to negative.

## Q8: Transaction velocity — count of transactions in the trailing hour

**Query:**
```sql
-- PostgreSQL (RANGE frame with interval)
SELECT account_id, tx_time,
       COUNT(*) OVER (PARTITION BY account_id ORDER BY tx_time
                      RANGE BETWEEN INTERVAL '1 hour' PRECEDING AND CURRENT ROW) AS tx_in_last_hour
FROM transactions
ORDER BY tx_in_last_hour DESC, account_id;
```
**Explanation:** A `RANGE` frame counts peers whose timestamp sits inside the trailing 60-minute window without needing a self-join.

## Q9: Same velocity metric using a self-join (MySQL)

**Query:**
```sql
-- MySQL
SELECT t1.account_id, t1.tx_id, t1.tx_time, COUNT(*) AS tx_in_next_hour
FROM transactions t1
JOIN transactions t2
  ON t2.account_id = t1.account_id
 AND t2.tx_time >= t1.tx_time
 AND t2.tx_time <  DATE_ADD(t1.tx_time, INTERVAL 1 HOUR)
GROUP BY t1.account_id, t1.tx_id, t1.tx_time
HAVING COUNT(*) >= 10;
```
**Explanation:** Every transaction counts itself plus all transactions in the following hour; `HAVING` surfaces the high-velocity windows the bank should flag.

## Q10: Fraud flags — combination of velocity and atypical amount

**Query:**
```sql
-- MySQL 8
WITH stats AS (
  SELECT account_id, AVG(amount) AS avg_amt, STDDEV_POP(amount) AS sd_amt
  FROM transactions
  GROUP BY account_id
),
vel AS (
  SELECT t.account_id, t.tx_id, t.tx_time, t.amount,
         (SELECT COUNT(*) FROM transactions t2
           WHERE t2.account_id = t.account_id
             AND t2.tx_time BETWEEN t.tx_time - INTERVAL 60 MINUTE AND t.tx_time) AS cnt_60m
  FROM transactions t
)
SELECT v.account_id, v.tx_id, v.tx_time, v.amount,
       CASE WHEN v.amount > s.avg_amt + 3 * s.sd_amt THEN 'amount_anomaly' END AS amount_flag,
       CASE WHEN v.cnt_60m >= 10 THEN 'velocity' END AS velocity_flag
FROM vel v
LEFT JOIN stats s ON s.account_id = v.account_id
WHERE v.amount > s.avg_amt + 3 * s.sd_amt OR v.cnt_60m >= 10;
```
**Explanation:** Atypical amount uses a 3-sigma rule against the account's own history; velocity uses a 60-minute count. Either condition raises the row into the fraud queue.

**Alt1:**
```sql
-- SQL Server (self-join count, avoiding interval RANGE frames)
SELECT t1.account_id, t1.tx_id,
       CASE WHEN t1.amount > s.avg_amt + 3 * s.sd_amt THEN 'amount_anomaly' END AS amount_flag,
       CASE WHEN v.cnt_60m >= 10 THEN 'velocity' END AS velocity_flag
FROM transactions t1
JOIN (SELECT account_id, AVG(amount) AS avg_amt, STDEV(amount) AS sd_amt
      FROM transactions GROUP BY account_id) s ON s.account_id = t1.account_id
CROSS APPLY (
  SELECT COUNT(*) AS cnt_60m
  FROM transactions t2
  WHERE t2.account_id = t1.account_id
    AND t2.tx_time BETWEEN DATEADD(MINUTE, -60, t1.tx_time) AND t1.tx_time
) v
WHERE t1.amount > s.avg_amt + 3 * s.sd_amt OR v.cnt_60m >= 10;

```
## Q11: Duplicate transaction detection (same amount, merchant, near time)

**Query:**
```sql
SELECT a.tx_id AS original_tx, b.tx_id AS possible_duplicate,
       a.account_id, a.amount, a.merchant, a.tx_time
FROM transactions a
JOIN transactions b
  ON b.account_id = a.account_id
 AND b.amount     = a.amount
 AND b.merchant   = a.merchant
 AND a.tx_id < b.tx_id
 AND TIMESTAMPDIFF(MINUTE, a.tx_time, b.tx_time) <= 5
ORDER BY a.tx_id;
```
**Explanation:** Self-join on account+amount+merchant, restricted to later IDs and a 5-minute window, isolates candidates for double-charging investigation.

## Q12: Suspicious large outgoing transfers per account

**Query:**
```sql
SELECT account_id, COUNT(*) AS large_transfers, SUM(amount) AS total_large_transfer_value
FROM transactions
WHERE tx_type = 'transfer'
  AND amount > 10000
  AND tx_time >= DATE_SUB(CURDATE(), INTERVAL 1 MONTH)
GROUP BY account_id
HAVING COUNT(*) >= 2
ORDER BY total_large_transfer_value DESC;
```
**Explanation:** Filters transfers above threshold in the last month and keeps accounts with repeated occurrences — a common structuring/AML trigger.

## Q13: Large cash withdrawals flagged for AML

**Query:**
```sql
SELECT a.customer_id, t.account_id, t.amount, t.tx_time
FROM transactions t
JOIN accounts a ON a.account_id = t.account_id
WHERE t.tx_type = 'atm'
  AND t.amount > 9000
  AND t.status = 'completed';
```
**Explanation:** Any single cash withdrawal near the reporting threshold is pulled into the AML queue; status filtering removes reversals and pending rows.

**Alt1:**
```sql
-- PostgreSQL
SELECT a.customer_id, t.account_id, t.amount, t.tx_time
FROM transactions t
JOIN accounts a USING (account_id)
WHERE t.tx_type = 'atm'
  AND t.amount > 9000
  AND t.status = 'completed'
ORDER BY t.tx_time DESC;

```
## Q14: Credit card balance — payments vs purchases

**Query:**
```sql
SELECT c.card_id,
       SUM(CASE WHEN t.tx_type = 'purchase' THEN t.amount ELSE 0 END) AS purchases,
       SUM(CASE WHEN t.tx_type = 'payment'  THEN t.amount ELSE 0 END) AS payments,
       SUM(CASE WHEN t.tx_type = 'purchase' THEN t.amount
                WHEN t.tx_type = 'payment'  THEN -t.amount ELSE 0 END) AS net_outstanding
FROM cards c
JOIN transactions t ON t.account_id = c.account_id
GROUP BY c.card_id;
```
**Explanation:** Net outstanding is purchases minus payments; the signed CASE makes the balance direction explicit.

## Q15: Credit utilization ratio per card

**Query:**
```sql
-- PostgreSQL
SELECT c.card_id, c.credit_limit,
       COALESCE(SUM(t.amount) FILTER (WHERE t.tx_type = 'purchase'), 0)
         - COALESCE(SUM(t.amount) FILTER (WHERE t.tx_type = 'payment'), 0) AS outstanding,
       ROUND(
         (COALESCE(SUM(t.amount) FILTER (WHERE t.tx_type = 'purchase'), 0)
          - COALESCE(SUM(t.amount) FILTER (WHERE t.tx_type = 'payment'), 0))
         / NULLIF(c.credit_limit, 0) * 100, 2) AS utilization_pct
FROM cards c
LEFT JOIN transactions t ON t.account_id = c.account_id
GROUP BY c.card_id, c.credit_limit;
```
**Explanation:** Utilization = outstanding ÷ credit limit; `FILTER` reads cleanly and `NULLIF` protects against zero limits.

**Alt1:**
```sql
SELECT c.card_id, c.credit_limit,
       SUM(CASE WHEN t.tx_type = 'purchase' THEN t.amount
                WHEN t.tx_type = 'payment'  THEN -t.amount ELSE 0 END) AS outstanding,
       ROUND(SUM(CASE WHEN t.tx_type = 'purchase' THEN t.amount
                      WHEN t.tx_type = 'payment' THEN -t.amount ELSE 0 END)
             / NULLIF(c.credit_limit,0) * 100, 2) AS utilization_pct
FROM cards c
LEFT JOIN transactions t ON t.account_id = c.account_id
GROUP BY c.card_id, c.credit_limit;
```

## Q16: Cards approaching their credit limit

**Query:**
```sql
WITH util AS (
  SELECT c.card_id, c.account_id, c.credit_limit,
         COALESCE(SUM(CASE WHEN t.tx_type = 'purchase' THEN t.amount
                           WHEN t.tx_type = 'payment' THEN -t.amount END), 0) AS outstanding
  FROM cards c
  LEFT JOIN transactions t ON t.account_id = c.account_id
  GROUP BY c.card_id, c.account_id, c.credit_limit
)
SELECT account_id, card_id,
       CASE WHEN outstanding / credit_limit > 0.90 THEN 'near_limit'
            WHEN outstanding / credit_limit > 0.70 THEN 'watch'
            ELSE 'headroom' END AS utilization_status
FROM util
WHERE credit_limit > 0
ORDER BY outstanding / credit_limit DESC;
```
**Explanation:** Ratio bands map to risk labels; the CTE keeps the query legible and O(n) with a single scan.

## Q17: Loan EMI schedule generation — recursive (PostgreSQL)

**Query:**
```sql
-- PostgreSQL
WITH RECURSIVE sched AS (
  SELECT loan_id, 1 AS install_no,
         principal AS balance_before,
         ROUND(principal * (rate/1200.0) / (1 - POWER(1 + rate/1200.0, -term_months)), 2) AS emi
  FROM loans
  WHERE loan_id = 1001
  UNION ALL
  SELECT s.loan_id, s.install_no + 1,
         s.balance_before - (s.emi - ROUND(s.balance_before * (rate/1200.0), 2)),
         s.emi
  FROM sched s
  JOIN loans l ON l.loan_id = s.loan_id
  WHERE s.install_no < l.term_months
)
SELECT install_no, emi,
       ROUND(balance_before * (rate/1200.0), 2) AS interest_part,
       ROUND(emi - balance_before * (rate/1200.0), 2) AS principal_part,
       ROUND(balance_before - (emi - balance_before * (rate/1200.0)), 2) AS balance_after
FROM sched
JOIN loans USING (loan_id)
ORDER BY install_no;
```
**Explanation:** An anchor row seeds installment 1; the recursive member decrements principal and terminates after `term_months` rows. EMI is the standard annuity formula.

## Q18: Same EMI schedule in SQL Server

**Query:**
```sql
-- SQL Server
WITH sched AS (
  SELECT loan_id, 1 AS install_no, principal AS balance_before,
         CAST(principal * (rate/1200.0) / (1 - POWER(1 + rate/1200.0, -term_months)) AS numeric(18,2)) AS emi
  FROM loans
  WHERE loan_id = 1002
  UNION ALL
  SELECT s.loan_id, s.install_no + 1,
         CAST(s.balance_before - (s.emi - s.balance_before * rate/1200.0) AS numeric(18,2)),
         s.emi
  FROM sched s
  JOIN loans l ON l.loan_id = s.loan_id
  WHERE s.install_no < l.term_months
)
SELECT * FROM sched
ORDER BY install_no;
```
**Explanation:** Syntax is the same recursion; `CAST` to explicit precision prevents float drift in currency values.

**Alt1:**
```sql
-- Oracle: CONNECT BY recursion is the idiomatic alternative
SELECT LEVEL AS install_no,
       principal * (rate/1200) / (1 - POWER(1 + rate/1200, -term_months)) AS emi
FROM loans
WHERE loan_id = 1002
CONNECT BY LEVEL <= term_months;
```

## Q19: EMI schedule with an interest-only grace period (MySQL 8)

**Query:**
```sql
-- MySQL 8 (WITH RECURSIVE)
WITH RECURSIVE sched AS (
  SELECT loan_id, 1 AS mo,
         principal AS balance,
         ROUND(principal * rate/1200, 2) AS interest,
         ROUND(principal * rate/1200, 2) AS payment,
         ROUND(principal * (rate/1200) / (1 - POWER(1 + rate/1200, -term_months)), 2) AS emi
  FROM loans WHERE loan_id = 1003
  UNION ALL
  SELECT s.loan_id, s.mo + 1,
         ROUND(s.balance - (s.payment - s.interest), 2),
         ROUND(s.balance * rate/1200, 2),
         IF(s.mo < 3, s.interest, s.emi),
         s.emi
  FROM sched s
  JOIN loans l ON l.loan_id = s.loan_id
  WHERE s.mo < l.term_months
)
SELECT mo, payment, interest, balance AS balance_after
FROM sched;
```
**Explanation:** During the first three months `payment = interest` (no principal amortized); afterwards it flips to the full EMI — a structure loan lenders actually use.

## Q20: Remaining principal after 12 EMIs — closed-form formula

**Query:**
```sql
SELECT loan_id,
       ROUND(
         principal * POWER(1 + rate/1200.0, term_months - 12)
         - (principal * (rate/1200.0) / (1 - POWER(1 + rate/1200.0, -term_months)))
           * (POWER(1 + rate/1200.0, term_months - 12) - 1) / (rate/1200.0),
         2) AS balance_after_12_emis
FROM loans
WHERE term_months > 12;
```
**Explanation:** Each EMI repays `EMI − interest`; compounding that over 12 periods yields the outstanding balance without generating all rows.

## Q21: Months remaining until payoff at current amortization rate

**Query:**
```sql
SELECT loan_id,
       CEIL(-LN(1 - (rate/1200.0) * (principal - paid_principal) / NULLIF(emi, 0))
            / LN(1 + rate/1200.0)) AS months_to_payoff
FROM (
  SELECT loan_id, rate, principal, paid_principal,
         (principal * (rate/1200.0)) / (1 - POWER(1 + rate/1200.0, -term_months)) AS emi
  FROM loans
) x;
```
**Explanation:** Solving the annuity equation `P = EMI·(1 − (1+r)^−n)/r` for `n` gives months remaining; `LN` and `CEIL` round up to a full payment.

**Alt1:**
```sql
-- PostgreSQL (verification by simulating each month with generate_series)
SELECT l.loan_id, COUNT(*) AS months_to_payoff
FROM loans l
CROSS JOIN LATERAL (
  SELECT (l.principal * (l.rate/1200.0)) / (1 - POWER(1 + l.rate/1200.0, -l.term_months)) AS emi
) e
CROSS JOIN LATERAL (
  SELECT gs AS mo,
         l.principal * POWER(1 + l.rate/1200.0, gs)
         - e.emi * (POWER(1 + l.rate/1200.0, gs) - 1) / (l.rate/1200.0) AS outstanding
  FROM generate_series(1, l.term_months) AS gs
) a
WHERE a.outstanding > 0
GROUP BY l.loan_id;

```
## Q22: Simple daily interest accrual on the outstanding principal

**Query:**
```sql
SELECT loan_id,
       ROUND((principal - paid_principal) * (rate/100.0) / 365.0, 2) AS daily_simple_interest
FROM loans
WHERE status = 'active';
```
**Explanation:** Simple interest divides the annual rate by 365 and applies it to the current outstanding balance.

## Q23: Daily compounded interest (PostgreSQL generate_series)

**Query:**
```sql
-- PostgreSQL
WITH daily AS (
  SELECT l.loan_id,
         gs::date AS day,
         ROUND(l.principal * POWER(1 + l.rate/100.0/365.0,
               (gs::date - l.originated_at::date)), 2) AS compounded_balance
  FROM loans l
  CROSS JOIN LATERAL generate_series(l.originated_at::date, CURRENT_DATE, 1) AS gs
  WHERE l.loan_id = 1001
)
SELECT * FROM daily
ORDER BY day DESC
LIMIT 1;
```
**Explanation:** `generate_series` materializes each compounding date; the exponent is the day count, giving balance under daily compounding.

## Q24: Accounts opened per month

**Query:**
```sql
-- PostgreSQL
SELECT DATE_TRUNC('month', opened_at) AS month, COUNT(*) AS accounts_opened
FROM accounts
GROUP BY 1
ORDER BY 1;
```
**Explanation:** Truncate to month and aggregate — the standard cohort-by-arrival report.

**Alt1:**
```sql
-- MySQL
SELECT DATE_FORMAT(opened_at, '%Y-%m') AS month, COUNT(*) AS accounts_opened
FROM accounts
GROUP BY 1
ORDER BY 1;
```

## Q25: Dormant accounts — no transactions in the last 90 days

**Query:**
```sql
-- PostgreSQL
SELECT a.account_id, a.customer_id,
       COALESCE(MAX(t.tx_time), a.opened_at) AS last_activity
FROM accounts a
LEFT JOIN transactions t ON t.account_id = a.account_id
GROUP BY a.account_id, a.customer_id, a.opened_at
HAVING MAX(t.tx_time) IS NULL OR MAX(t.tx_time) < CURRENT_DATE - INTERVAL '90 days';
```
**Explanation:** Left join keeps never-used accounts; the GROUP BY + HAVING tests the last-activity cutoff.

**Alt1:**
```sql
-- MySQL
SELECT a.account_id, a.customer_id
FROM accounts a
LEFT JOIN transactions t ON t.account_id = a.account_id
GROUP BY a.account_id, a.customer_id
HAVING MAX(t.tx_time) IS NULL OR MAX(t.tx_time) < CURRENT_DATE - INTERVAL 90 DAY;
```

## Q26: Customer total exposure — balances + credit limits + loan outstanding

**Query:**
```sql
-- PostgreSQL
SELECT c.customer_id,
       COALESCE(a.bal, 0) + COALESCE(crd.limits, 0) + COALESCE(lo.out, 0) AS total_exposure
FROM customers c
LEFT JOIN (SELECT customer_id, SUM(balance) AS bal FROM accounts GROUP BY customer_id) a USING (customer_id)
LEFT JOIN (SELECT ac.customer_id, SUM(cc.credit_limit) AS limits
           FROM cards cc JOIN accounts ac USING (account_id) GROUP BY ac.customer_id) crd USING (customer_id)
LEFT JOIN (SELECT customer_id, SUM(principal - paid_principal) AS out
           FROM loans GROUP BY customer_id) lo USING (customer_id)
ORDER BY total_exposure DESC;
```
**Explanation:** Three pre-aggregated subqueries are outer-joined so a customer missing a product still yields zero instead of NULL.

## Q27: Savings customers with no credit card — cross-sell list

**Query:**
```sql
SELECT c.customer_id, c.name
FROM customers c
WHERE EXISTS (SELECT 1 FROM accounts a WHERE a.customer_id = c.customer_id)
  AND NOT EXISTS (
        SELECT 1
        FROM accounts a JOIN cards cd ON cd.account_id = a.account_id
        WHERE a.customer_id = c.customer_id
      );
```
**Explanation:** EXISTS/anti-EXISTS express "has an account" and "has no card" without join multiplication.

**Alt1:**
```sql
SELECT ac.customer_id
FROM accounts ac
LEFT JOIN cards cd ON cd.account_id = ac.account_id
GROUP BY ac.customer_id
HAVING COUNT(ac.account_id) > 0 AND COUNT(cd.card_id) = 0;
```

## Q28: New vs returning customers per month

**Query:**
```sql
-- PostgreSQL
WITH first_tx AS (
  SELECT customer_id, MIN(tx_time)::date AS first_date
  FROM transactions JOIN accounts USING (account_id)
  GROUP BY customer_id
),
activity AS (
  SELECT DATE_TRUNC('month', tx_time) AS m, customer_id
  FROM transactions JOIN accounts USING (account_id)
  GROUP BY 1, 2
)
SELECT a.m,
       COUNT(DISTINCT CASE WHEN f.first_date >= a.m::date THEN a.customer_id END) AS new_customers,
       COUNT(DISTINCT CASE WHEN f.first_date <  a.m::date THEN a.customer_id END) AS returning_customers
FROM activity a
JOIN first_tx f USING (customer_id)
GROUP BY a.m
ORDER BY a.m;
```
**Explanation:** First-transaction date splits each month's active customers into new (first time) and returning (seen before).

## Q29: Products per customer — customers using 3+ products

**Query:**
```sql
SELECT customer_id, COUNT(*) AS product_holdings
FROM (
  SELECT customer_id, 'account' AS product FROM accounts
  UNION ALL
  SELECT a.customer_id, 'card' FROM accounts a JOIN cards c ON c.account_id = a.account_id
  UNION ALL
  SELECT customer_id, 'loan' FROM loans
  UNION ALL
  SELECT customer_id, 'policy' FROM insurance
) p
GROUP BY customer_id
HAVING COUNT(*) >= 3
ORDER BY product_holdings DESC;
```
**Explanation:** UNION ALL tallies each product family; HAVING keeps multi-product relationships, the core of a cross-sell campaign.

## Q30: Transfers between two accounts of the same customer (internal netting)

**Query:**
```sql
SELECT out_t.account_id AS from_account, in_t.account_id AS to_account,
       out_t.amount, out_t.tx_time
FROM transactions out_t
JOIN accounts fa     ON fa.account_id = out_t.account_id
JOIN transactions in_t ON in_t.tx_id = out_t.correlated_tx_id
JOIN accounts ta     ON ta.account_id = in_t.account_id
WHERE in_t.tx_id IS NOT NULL
  AND fa.customer_id = ta.customer_id;
```
**Explanation:** `correlated_tx_id` links the outgoing and incoming legs; the join exposes self-transfers that net to zero across the customer.

**Alt1:**
```sql
-- Fallback without a link column: pair legs on identical amount + timestamp
SELECT a.account_id AS from_account, b.account_id AS to_account,
       a.amount, a.tx_time
FROM transactions a
JOIN transactions b
  ON b.amount   = a.amount
 AND b.tx_time  = a.tx_time
 AND a.tx_type  IN ('transfer','debit')
 AND b.tx_type  IN ('transfer','credit')
 AND a.tx_id < b.tx_id
JOIN accounts fa ON fa.account_id = a.account_id
JOIN accounts tb ON tb.account_id = b.account_id
WHERE fa.customer_id = tb.customer_id;

```
## Q31: Netting — total inflow vs outflow per account

**Query:**
```sql
SELECT account_id,
       SUM(CASE WHEN tx_type IN ('credit','payment','interest') THEN amount ELSE 0 END) AS inflow,
       SUM(CASE WHEN tx_type IN ('debit','purchase','atm','transfer','fee') THEN amount ELSE 0 END) AS outflow,
       SUM(CASE WHEN tx_type IN ('credit','payment','interest') THEN amount ELSE -amount END) AS net_position
FROM transactions
GROUP BY account_id
ORDER BY ABS(SUM(CASE WHEN tx_type IN ('credit','payment','interest') THEN amount ELSE -amount END)) DESC;
```
**Explanation:** One pass with two directional CASE columns gives gross inflows/outflows and the signed net.

**Alt1:**
```sql
SELECT account_id,
       SUM(amount) FILTER (WHERE tx_type IN ('credit','payment','interest')) AS inflow,
       SUM(-amount) FILTER (WHERE tx_type IN ('debit','purchase','atm','transfer','fee')) AS outflow
FROM transactions
GROUP BY account_id;
```

## Q32: NSF events — debits that would overdraw, plus the fee booked

**Query:**
```sql
WITH bal AS (
  SELECT account_id, tx_id, tx_time, tx_type, amount,
         COALESCE(SUM(CASE WHEN tx_type IN ('credit','payment','interest') THEN amount
                           ELSE -amount END)
             OVER (PARTITION BY account_id ORDER BY tx_time, tx_id
                   ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING), 0) AS balance_before
  FROM transactions
)
SELECT account_id, tx_id, tx_time, amount,
       CAST(35.00 AS DECIMAL(10,2)) AS nsf_fee_charged
FROM bal
WHERE tx_type IN ('debit','purchase','atm','transfer')
  AND balance_before < amount
  AND balance_before >= 0;
```
**Explanation:** Keep transactions where the pre-balance is sufficient only momentarily; those are the NSF-worthy debits a bank fees.

## Q33: Average payment processing time (initiation to settlement)

**Query:**
```sql
-- MySQL
SELECT AVG(TIMESTAMPDIFF(MINUTE, initiated_at, settled_at)) / 60.0 AS avg_processing_hours,
       COUNT(*) AS settled_count
FROM payments
WHERE status = 'settled' AND settled_at IS NOT NULL;
```
**Explanation:** `TIMESTAMPDIFF` measures elapsed time per payment; averaging gives the operational SLA in hours.

**Alt1:**
```sql
-- PostgreSQL
SELECT AVG(EXTRACT(EPOCH FROM (settled_at - initiated_at)))/3600.0 AS avg_processing_hours
FROM payments
WHERE status = 'settled';
```

## Q34: Payment reconciliation — discrepancies between ledger and bank statement

**Query:**
```sql
SELECT COALESCE(l.recorded_date, b.recorded_date) AS business_date,
       COALESCE(l.ledger_amt, 0)  AS ledger_amount,
       COALESCE(b.bank_amt, 0)    AS bank_amount,
       COALESCE(l.ledger_amt, 0) - COALESCE(b.bank_amt, 0) AS difference
FROM ledger l
FULL OUTER JOIN bank_statement b ON b.recorded_date = l.recorded_date
WHERE COALESCE(l.ledger_amt, 0) <> COALESCE(b.bank_amt, 0)
ORDER BY business_date;
```
**Explanation:** A FULL OUTER JOIN keeps rows present on only one side; `COALESCE` makes the difference arithmetic NULL-safe.

## Q35: Interest rate tiers based on balance bands

**Query:**
```sql
SELECT account_id, balance,
       CASE WHEN balance > 100000 THEN 0.035
            WHEN balance >  50000 THEN 0.025
            WHEN balance >  10000 THEN 0.015
            ELSE 0.005 END AS tier_rate
FROM accounts;
```
**Explanation:** Banding maps each balance to the applicable rate; CASE evaluates top-down.

**Alt1:**
```sql
-- Blended interest across all bands (marginal-rate calculation)
SELECT account_id, balance,
       ROUND(
         LEAST(balance, 10000) * 0.005
         + GREATEST(LEAST(balance, 50000) - 10000, 0) * 0.015
         + GREATEST(LEAST(balance, 100000) - 50000, 0) * 0.025
         + GREATEST(balance - 100000, 0) * 0.035
       , 2) AS total_annual_interest
FROM accounts;
```

## Q36: Vintage analysis — loan book performance by origination month

**Query:**
```sql
-- PostgreSQL
SELECT DATE_TRUNC('month', originated_at) AS vintage,
       COUNT(*) AS loans_originated,
       COUNT(*) FILTER (WHERE status = 'default') AS defaults,
       ROUND(100.0 * COUNT(*) FILTER (WHERE status = 'default') / COUNT(*), 2) AS default_rate_pct
FROM loans
GROUP BY vintage
ORDER BY vintage;
```
**Explanation:** Cohort loans by origination month and compare default rates so underwriting quality can be read across vintages.

**Alt1:**
```sql
-- MySQL
SELECT DATE_FORMAT(originated_at, '%Y-%m') AS vintage,
       COUNT(*) AS loans_originated,
       SUM(status = 'default') AS defaults,
       ROUND(100.0 * SUM(status = 'default') / COUNT(*), 2) AS default_rate_pct
FROM loans
GROUP BY 1
ORDER BY 1;
```

## Q37: Aging — overdue buckets 0-30 / 30-60 / 60-90 / 90+

**Query:**
```sql
-- PostgreSQL
SELECT CASE
         WHEN days_overdue <  0 THEN 'not_due'
         WHEN days_overdue < 30 THEN '0-30'
         WHEN days_overdue < 60 THEN '31-60'
         WHEN days_overdue < 90 THEN '61-90'
         ELSE '90+' END AS bucket,
       COUNT(*) AS receivables,
       SUM(amount) AS outstanding_amount
FROM (
  SELECT amount, CURRENT_DATE - paid_date AS days_overdue
  FROM receivables
  WHERE paid_date IS NULL
) d
GROUP BY 1
ORDER BY 1;
```
**Explanation:** Days past due from the missing payment date; CASE buckets feed the standard collections waterfall.

**Alt1:**
```sql
-- MySQL
SELECT CASE
         WHEN DATEDIFF(CURDATE(), due_date) < 30 THEN '0-30'
         WHEN DATEDIFF(CURDATE(), due_date) < 60 THEN '31-60'
         WHEN DATEDIFF(CURDATE(), due_date) < 90 THEN '61-90'
         ELSE '90+' END AS bucket,
       COUNT(*) AS receivables,
       SUM(amount) AS outstanding_amount
FROM receivables
WHERE paid_date IS NULL
GROUP BY 1
ORDER BY CASE
         WHEN DATEDIFF(CURDATE(), due_date) < 30 THEN 1
         WHEN DATEDIFF(CURDATE(), due_date) < 60 THEN 2
         WHEN DATEDIFF(CURDATE(), due_date) < 90 THEN 3
         ELSE 4 END;

```
## Q38: Delinquency ratio by account product type

**Query:**
```sql
-- PostgreSQL
SELECT a.product_type,
       COUNT(DISTINCT a.account_id) AS total_accounts,
       COUNT(DISTINCT a.account_id) FILTER (WHERE r.due_date < CURRENT_DATE AND r.paid_date IS NULL) AS delinquent,
       ROUND(100.0
         * COUNT(DISTINCT a.account_id) FILTER (WHERE r.due_date < CURRENT_DATE AND r.paid_date IS NULL)
         / NULLIF(COUNT(DISTINCT a.account_id), 0), 2) AS delinquency_rate_pct
FROM accounts a
LEFT JOIN receivables r ON r.account_id = a.account_id
GROUP BY a.product_type;
```
**Explanation:** Only unpaid, past-due receivables count as delinquent; the rate is per product family.

## Q39: KYC completeness — missing documents per field

**Query:**
```sql
SELECT 'passport' AS field, COUNT(*) FILTER (WHERE passport IS NULL) AS missing
FROM customers
UNION ALL SELECT 'address', COUNT(*) FILTER (WHERE address IS NULL) FROM customers
UNION ALL SELECT 'phone',   COUNT(*) FILTER (WHERE phone   IS NULL) FROM customers
UNION ALL SELECT 'email',   COUNT(*) FILTER (WHERE email   IS NULL) FROM customers;
```
**Explanation:** Four scalar aggregates are stacked with UNION ALL to produce a drill-down of onboarding gaps.

**Alt1:**
```sql
SELECT SUM(CASE WHEN passport IS NULL THEN 1 ELSE 0 END) AS missing_passport,
       SUM(CASE WHEN address  IS NULL THEN 1 ELSE 0 END) AS missing_address,
       SUM(CASE WHEN phone    IS NULL THEN 1 ELSE 0 END) AS missing_phone,
       SUM(CASE WHEN email    IS NULL THEN 1 ELSE 0 END) AS missing_email
FROM customers;
```

## Q40: KYC documents expiring within 90 days

**Query:**
```sql
SELECT customer_id, name, id_doc_expiry
FROM customers
WHERE id_doc_expiry BETWEEN CURRENT_DATE AND CURRENT_DATE + INTERVAL '90 days'
ORDER BY id_doc_expiry;
```
**Explanation:** A bounded range over the expiry date yields the re-verification workload.

## Q41: Customer risk rating from transaction behavior

**Query:**
```sql
SELECT a.customer_id,
       COUNT(*) AS total_tx,
       SUM(amount > 10000) AS large_tx_count,
       CASE WHEN COUNT(*) > 1000                       THEN 'high'
            WHEN SUM(amount > 10000) > 20              THEN 'high'
            WHEN COUNT(*) > 200 AND SUM(tx_type='transfer') > 50 THEN 'medium'
            ELSE 'low' END AS risk_rating
FROM transactions t
JOIN accounts a ON a.account_id = t.account_id
GROUP BY a.customer_id;
```
**Explanation:** Volume and large-transfer thresholds drive a rule-based risk score; the CASE evaluates from highest risk down.

## Q42: Tax withheld per country on customer interest

**Query:**
```sql
SELECT c.country,
       ROUND(SUM(t.amount), 2) AS gross_interest,
       ROUND(SUM(t.amount) * 0.30, 2) AS withholding_tax_30pct
FROM transactions t
JOIN accounts a  ON a.account_id  = t.account_id
JOIN customers c ON c.customer_id = a.customer_id
WHERE t.tx_type = 'interest'
GROUP BY c.country
ORDER BY withholding_tax_30pct DESC;
```
**Explanation:** Interest-credit rows are joined to country of residence and taxed at a flat 30% per jurisdiction.

## Q43: Claims ratio by policy type

**Query:**
```sql
SELECT policy_type,
       SUM(premium_earned)  AS premium_earned,
       SUM(claims_paid)     AS claims_paid,
       ROUND(100.0 * SUM(claims_paid) / NULLIF(SUM(premium_earned), 0), 2) AS claims_ratio_pct
FROM insurance
WHERE status = 'in_force'
GROUP BY policy_type;
```
**Explanation:** Claims ratio = claims paid ÷ earned premium; a ratio above ~100% signals an underpriced book.

## Q44: Lapse ratio — policies not renewed

**Query:**
```sql
-- PostgreSQL
SELECT DATE_TRUNC('month', expiry) AS expiry_month,
       COUNT(*) AS expiring,
       COUNT(*) FILTER (WHERE status = 'lapsed') AS lapsed,
       ROUND(100.0 * COUNT(*) FILTER (WHERE status = 'lapsed') / COUNT(*), 2) AS lapse_rate_pct
FROM insurance
GROUP BY 1
ORDER BY 1;
```
**Explanation:** Group policies by their expiry month and measure how many fell into lapsed status.

**Alt1:**
```sql
-- SQL Server
SELECT FORMAT(expiry, 'yyyy-MM') AS expiry_month,
       SUM(CASE WHEN status = 'lapsed' THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS lapse_rate_pct
FROM insurance
GROUP BY FORMAT(expiry, 'yyyy-MM');
```

## Q45: Customer retention — active both this month and last

**Query:**
```sql
-- PostgreSQL
WITH activity AS (
  SELECT customer_id, DATE_TRUNC('month', tx_time) AS m
  FROM transactions JOIN accounts USING (account_id)
  GROUP BY 1, 2
),
prev AS (
  SELECT customer_id, m,
         LAG(m) OVER (PARTITION BY customer_id ORDER BY m) AS prev_m
  FROM activity
)
SELECT m,
       COUNT(*) AS active_customers,
       ROUND(100.0 * COUNT(*) FILTER (WHERE prev_m = m - INTERVAL '1 month') / COUNT(*), 2) AS retention_pct
FROM prev
GROUP BY m
ORDER BY m;
```
**Explanation:** `LAG` finds each customer's prior active month; retention is the share active in consecutive months.

## Q46: Convert transaction amounts to USD using the FX table

**Query:**
```sql
-- PostgreSQL
SELECT t.tx_id, a.customer_id, t.ccy,
       ROUND(t.amount * fx.rate, 2) AS amount_in_usd
FROM transactions t
JOIN accounts a USING (account_id)
JOIN fx_rates fx
  ON fx.ccy_pair = t.ccy || 'USD'
 AND fx.rate_date = t.tx_time::date
WHERE t.ccy <> 'USD'
ORDER BY t.tx_id;
```
**Explanation:** The pair key is built from the transaction's currency, and the rate is looked up for the exact business date.

**Alt1:**
```sql
SELECT t.tx_id, t.ccy, t.amount * fx.rate AS amount_in_usd
FROM transactions t
JOIN fx_rates fx
  ON fx.ccy_pair = CONCAT(t.ccy, 'USD')
 AND fx.rate_date = DATE(t.tx_time);
```

## Q47: Net FX exposure per currency translated to USD

**Query:**
```sql
-- PostgreSQL
SELECT t.ccy,
       ROUND(SUM(CASE WHEN t.tx_type IN ('credit','payment','interest') THEN t.amount
                      ELSE -t.amount END) * COALESCE(fx.rate, 1), 2) AS net_exposure_usd
FROM transactions t
LEFT JOIN fx_rates fx
  ON fx.ccy_pair = t.ccy || 'USD'
 AND fx.rate_date = (SELECT MAX(rate_date) FROM fx_rates)
GROUP BY t.ccy, COALESCE(fx.rate, 1)
ORDER BY ABS(SUM(CASE WHEN t.tx_type IN ('credit','payment','interest') THEN t.amount
                      ELSE -t.amount END)) DESC;
```
**Explanation:** The LEFT JOIN makes USD native (rate 1); net longs/shorts per currency are revalued at the latest rate.

## Q48: Payment success rate by corridor (sender → recipient country)

**Query:**
```sql
-- PostgreSQL
SELECT sender_country, recipient_country,
       COUNT(*) AS total_payments,
       COUNT(*) FILTER (WHERE status = 'settled') AS settled,
       ROUND(100.0 * COUNT(*) FILTER (WHERE status = 'settled') / COUNT(*), 2) AS success_rate_pct
FROM payments
GROUP BY 1, 2
ORDER BY success_rate_pct ASC;
```
**Explanation:** Pivoting payments by corridor highlights lanes with chronic settlement failures that operations should fix.

## Q49: Chargeback rate per card

**Query:**
```sql
SELECT card_id,
       COUNT(*) AS purchases,
       COUNT(*) FILTER (WHERE status = 'chargeback') AS chargebacks,
       ROUND(100.0 * COUNT(*) FILTER (WHERE status = 'chargeback') / COUNT(*), 2) AS chargeback_rate_pct
FROM transactions
WHERE tx_type = 'purchase'
GROUP BY card_id
HAVING COUNT(*) >= 20;
```
**Explanation:** Only cards with a minimum purchase volume get a stable chargeback rate; high outliers go to the acquiring risk desk.

## Q50: Monthly interest expense accrual on deposits

**Query:**
```sql
-- PostgreSQL
SELECT DATE_TRUNC('month', tx_time) AS month,
       ROUND(SUM(CASE WHEN tx_type = 'interest' THEN amount ELSE 0 END), 2) AS interest_expense
FROM transactions
GROUP BY 1
ORDER BY 1;
```
**Explanation:** Summing positive interest credits per month approximates the funding cost line of the income statement.

**Alt1:**
```sql
-- MySQL
SELECT DATE_FORMAT(tx_time, '%Y-%m') AS month,
       ROUND(SUM(CASE WHEN tx_type = 'interest' THEN amount ELSE 0 END), 2) AS interest_expense
FROM transactions
GROUP BY 1
ORDER BY 1;

```
## Q51: Portfolio holdings valued at the latest price

**Query:**
```sql
SELECT h.portfolio_id, h.symbol, h.qty,
       lp.close AS last_close,
       ROUND(h.qty * lp.close, 2) AS market_value
FROM holdings h
JOIN (
  SELECT symbol, close,
         ROW_NUMBER() OVER (PARTITION BY symbol ORDER BY px_date DESC) AS rn
  FROM prices
) lp ON lp.symbol = h.symbol AND lp.rn = 1
ORDER BY market_value DESC;
```
**Explanation:** A `ROW_NUMBER = 1` subquery keeps each symbol's most recent price; multiplying by quantity gives mark-to-market.

## Q52: Portfolio mark-to-market across the full price history

**Query:**
```sql
SELECT h.portfolio_id, p.px_date,
       ROUND(SUM(h.qty * p.close), 2) AS portfolio_value
FROM holdings h
JOIN prices p USING (symbol)
GROUP BY h.portfolio_id, p.px_date
ORDER BY h.portfolio_id, p.px_date;
```
**Explanation:** Joining positions to every price date produces the NAV time series needed for PnL, drawdown, and vol.

## Q53: Daily PnL — portfolio mark-to-market change day over day

**Query:**
```sql
-- PostgreSQL
WITH mv AS (
  SELECT h.portfolio_id, p.px_date,
         SUM(h.qty * p.close) AS value
  FROM holdings h JOIN prices p USING (symbol)
  GROUP BY h.portfolio_id, p.px_date
)
SELECT portfolio_id, px_date, ROUND(value, 2) AS mtm,
       ROUND(value - LAG(value) OVER (PARTITION BY portfolio_id ORDER BY px_date), 2) AS daily_pnl
FROM mv
ORDER BY portfolio_id, px_date;
```
**Explanation:** `LAG` captures yesterday's value, so today's PnL is the first difference of the MTM series.

**Alt1:**
```sql
SELECT h.portfolio_id, p.px_date,
       SUM(h.qty * p.close) AS value,
       SUM(h.qty * p.close) - SUM(h.qty * LAG(p.close) OVER (PARTITION BY p.symbol ORDER BY p.px_date)) AS daily_pnl_alt
FROM holdings h JOIN prices p USING (symbol)
GROUP BY h.portfolio_id, p.px_date;
```

## Q54: Trade returns per instrument (average entry cost vs current price)

**Query:**
```sql
-- PostgreSQL
WITH entries AS (
  SELECT account_id, symbol,
         SUM(qty) AS qty,
         SUM(qty * price) AS cost
  FROM trades
  WHERE side = 'BUY'
  GROUP BY account_id, symbol
),
last_px AS (
  SELECT symbol, close,
         ROW_NUMBER() OVER (PARTITION BY symbol ORDER BY px_date DESC) AS rn
  FROM prices
)
SELECT e.account_id, e.symbol, e.qty,
       ROUND(e.cost / e.qty, 2) AS avg_cost,
       lp.close AS last_price,
       ROUND((lp.close - e.cost / e.qty) / NULLIF(e.cost / e.qty, 0) * 100, 2) AS return_pct
FROM entries e
JOIN last_px lp ON lp.symbol = e.symbol AND lp.rn = 1
ORDER BY return_pct DESC;
```
**Explanation:** Weighted average buy cost per symbol is compared to the last close; return is the percentage off that cost basis.

## Q55: Win rate, average win, average loss on closed trades

**Query:**
```sql
-- PostgreSQL
SELECT account_id,
       COUNT(*) AS closed_trades,
       COUNT(*) FILTER (WHERE realized_pnl > 0) AS wins,
       ROUND(100.0 * COUNT(*) FILTER (WHERE realized_pnl > 0) / COUNT(*), 2) AS win_rate_pct,
       ROUND(AVG(realized_pnl) FILTER (WHERE realized_pnl > 0), 2) AS avg_win,
       ROUND(AVG(ABS(realized_pnl)) FILTER (WHERE realized_pnl < 0), 2) AS avg_loss
FROM trades
WHERE side = 'SELL'
GROUP BY account_id;
```
**Explanation:** Conditioned aggregates dissect realized PnL into frequency (win rate) and magnitude (win/loss sizes).

## Q56: Profit factor — gross wins divided by gross losses

**Query:**
```sql
SELECT ROUND(
         SUM(realized_pnl) FILTER (WHERE realized_pnl > 0)
         / NULLIF(-SUM(realized_pnl) FILTER (WHERE realized_pnl < 0), 0),
       2) AS profit_factor
FROM trades
WHERE side = 'SELL';
```
**Explanation:** Values above 1 mean the strategy earns more than it loses; NULLIF avoids division by a zero-loss book.

## Q57: 20-day moving average vs current price (trading signal)

**Query:**
```sql
WITH px AS (
  SELECT symbol, px_date, close,
         AVG(close) OVER (PARTITION BY symbol ORDER BY px_date
                          ROWS BETWEEN 19 PRECEDING AND CURRENT ROW) AS ma20
  FROM prices
)
SELECT symbol, px_date, ROUND(close, 2), ROUND(ma20, 2),
       CASE WHEN close > ma20 THEN 'bullish_above_ma20'
            WHEN close < ma20 THEN 'bearish_below_ma20'
            ELSE 'at_ma20' END AS signal
FROM px
WHERE px_date = (SELECT MAX(px_date) FROM prices);
```
**Explanation:** A 20-row frame computes the SMA; comparing today's close against it yields the classic trend signal.

## Q58: Maximum drawdown (peak-to-trough) per portfolio

**Query:**
```sql
-- PostgreSQL
WITH daily AS (
  SELECT h.portfolio_id, p.px_date, SUM(h.qty * p.close) AS value
  FROM holdings h JOIN prices p USING (symbol)
  GROUP BY h.portfolio_id, p.px_date
),
dd AS (
  SELECT portfolio_id, px_date, value,
         MAX(value) OVER (PARTITION BY portfolio_id ORDER BY px_date) AS peak
  FROM daily
)
SELECT portfolio_id,
       ROUND(MIN((value - peak) / NULLIF(peak, 0)) * 100, 2) AS max_drawdown_pct
FROM dd
GROUP BY portfolio_id
ORDER BY max_drawdown_pct;
```
**Explanation:** Running max gives the peak so far; drawdown is the worst percentage distance below it, aggregated per portfolio.

**Alt1:**
```sql
-- SQL Server
SELECT TOP 1 *,
       (value - peak) / peak * 100.0 AS drawdown_pct
FROM (
  SELECT px_date, value,
         MAX(value) OVER (ORDER BY px_date) AS peak
  FROM daily_nav
) d
ORDER BY drawdown_pct;
```

## Q59: Days currently below the all-time high (underwater duration)

**Query:**
```sql
SELECT COUNT(*) AS underwater_days
FROM (
  SELECT px_date,
         SUM(qty * close) AS value,
         MAX(SUM(qty * close)) OVER (ORDER BY px_date) AS peak
  FROM holdings JOIN prices USING (symbol)
  GROUP BY px_date
) x
WHERE value < peak;
```
**Explanation:** Every day whose NAV sits below the running peak counts toward the underwater streak the investor is stuck in.

## Q60: 52-week high/low per stock with current close

**Query:**
```sql
-- PostgreSQL
SELECT symbol,
       MAX(close) FILTER (WHERE px_date >= CURRENT_DATE - INTERVAL '52 weeks') AS high_52w,
       MIN(close) FILTER (WHERE px_date >= CURRENT_DATE - INTERVAL '52 weeks') AS low_52w,
       (ARRAY_AGG(close ORDER BY px_date DESC))[1] AS last_close
FROM prices
GROUP BY symbol;
```
**Explanation:** FILTER bounds the HIGH/LOW aggregates to a year; ARRAY_AGG orders all closes and reads the newest one.

## Q61: Sector allocation percentage

**Query:**
```sql
-- PostgreSQL
WITH sector_mv AS (
  SELECT s.sector, SUM(h.qty * p.close) AS sector_market_value
  FROM holdings h
  JOIN prices p       USING (symbol)
  JOIN securities s   USING (symbol)
  WHERE p.px_date = (SELECT MAX(px_date) FROM prices)
  GROUP BY s.sector
)
SELECT sector,
       ROUND(sector_market_value, 2),
       ROUND(100.0 * sector_market_value / SUM(sector_market_value) OVER (), 2) AS allocation_pct
FROM sector_mv
ORDER BY allocation_pct DESC;
```
**Explanation:** Sector values are weighted against the whole book via a windowed SUM over all rows.

**Alt1:**
```sql
SELECT sec.sector,
       ROUND(100.0 * SUM(h.qty * p.close) /
             (SELECT SUM(h2.qty * p2.close) FROM holdings h2
              JOIN prices p2 USING (symbol)
              WHERE p2.px_date = (SELECT MAX(px_date) FROM prices)), 2) AS allocation_pct
FROM holdings h
JOIN prices p     USING (symbol)
JOIN securities sec USING (symbol)
WHERE p.px_date = (SELECT MAX(px_date) FROM prices)
GROUP BY sec.sector;
```

## Q62: Hedging — offsetting long and short positions per instrument

**Query:**
```sql
WITH pos AS (
  SELECT symbol, account_id, SUM(qty) AS net_qty
  FROM trades
  GROUP BY symbol, account_id
)
SELECT long.symbol,
       long.net_qty   AS long_qty,
       short.net_qty  AS short_qty,
       long.net_qty + short.net_qty AS residual_qty
FROM pos long
JOIN pos short ON short.symbol = long.symbol
WHERE long.net_qty  > 0
  AND short.net_qty < 0
ORDER BY ABS(long.net_qty + short.net_qty);
```
**Explanation:** Joining a long position to a short position in the same symbol reveals the residual — effectively hedged when near zero.

## Q63: Fund NAV per portfolio given total units

**Query:**
```sql
WITH last_px AS (
  SELECT symbol, close,
         ROW_NUMBER() OVER (PARTITION BY symbol ORDER BY px_date DESC) AS rn
  FROM prices
)
SELECT pf.portfolio_id,
       ROUND(SUM(h.qty * lp.close), 2) AS nav_in_base_ccy,
       pf.units,
       ROUND(SUM(h.qty * lp.close) / NULLIF(pf.units, 0), 4) AS nav_per_unit
FROM portfolio pf
JOIN holdings h USING (portfolio_id)
JOIN last_px lp ON lp.symbol = h.symbol AND lp.rn = 1
GROUP BY pf.portfolio_id, pf.units;
```
**Explanation:** NAV = book value of holdings; NAV per unit divides by outstanding units for investor statements.

## Q64: Realized vs unrealized PnL

**Query:**
```sql
-- PostgreSQL
WITH realized AS (
  SELECT account_id, SUM(COALESCE(realized_pnl, 0)) AS realized
  FROM trades
  GROUP BY account_id
),
open_pos AS (
  SELECT account_id, symbol, SUM(qty) AS qty, SUM(qty * price) / SUM(qty) AS avg_cost
  FROM trades
  WHERE side = 'BUY'
  GROUP BY account_id, symbol
),
unrealized AS (
  SELECT o.account_id,
         SUM((lp.close - o.avg_cost) * o.qty) AS unrealized
  FROM open_pos o
  JOIN (SELECT symbol, close,
               ROW_NUMBER() OVER (PARTITION BY symbol ORDER BY px_date DESC) AS rn
        FROM prices) lp ON lp.symbol = o.symbol AND lp.rn = 1
  GROUP BY o.account_id
)
SELECT a.account_id,
       ROUND(COALESCE(r.realized, 0), 2)  AS realized_pnl,
       ROUND(COALESCE(u.unrealized, 0), 2) AS unrealized_pnl,
       ROUND(COALESCE(r.realized, 0) + COALESCE(u.unrealized, 0), 2) AS total_pnl
FROM accounts a
LEFT JOIN realized r   USING (account_id)
LEFT JOIN unrealized u USING (account_id);
```
**Explanation:** Realized PnL comes straight from closed trades; unrealized revalues open positions off their average cost.

## Q65: Concentration — weight of the top 10 holdings

**Query:**
```sql
WITH latest_px AS (
  SELECT symbol, close,
         ROW_NUMBER() OVER (PARTITION BY symbol ORDER BY px_date DESC) AS rn
  FROM prices
),
pos AS (
  SELECT h.portfolio_id, h.symbol, SUM(h.qty * lp.close) AS mv
  FROM holdings h
  JOIN latest_px lp ON lp.symbol = h.symbol AND lp.rn = 1
  GROUP BY h.portfolio_id, h.symbol
),
ranked AS (
  SELECT portfolio_id, mv,
         ROW_NUMBER() OVER (PARTITION BY portfolio_id ORDER BY mv DESC) AS rn
  FROM pos
)
SELECT portfolio_id,
       COUNT(*) AS holdings,
       ROUND(SUM(CASE WHEN rn <= 10 THEN mv END), 2) AS top10_value,
       ROUND(SUM(mv), 2) AS portfolio_value,
       ROUND(100.0 * SUM(CASE WHEN rn <= 10 THEN mv END) / SUM(mv), 2) AS pct_in_top10
FROM ranked
GROUP BY portfolio_id;
```
**Explanation:** Rank holdings within each portfolio and measure how much of the book sits in the ten largest names.

## Q66: Average daily volume — liquidity screen per symbol

**Query:**
```sql
SELECT symbol,
       ROUND(AVG(volume), 0) AS avg_daily_volume,
       COUNT(*) AS price_days
FROM prices
WHERE px_date >= CURRENT_DATE - INTERVAL '90 days'
GROUP BY symbol
ORDER BY avg_daily_volume DESC;
```
**Explanation:** Illiquid names (low average volume) are flagged before any sizing or execution decision.

**Alt1:**
```sql
-- MySQL
SELECT symbol, ROUND(AVG(volume), 0) AS avg_daily_volume
FROM prices
WHERE px_date >= DATE_SUB(CURDATE(), INTERVAL 90 DAY)
GROUP BY symbol
ORDER BY avg_daily_volume DESC;

```
## Q67: Rebalancing drift — current weight vs target weight

**Query:**
```sql
-- PostgreSQL
WITH latest_px AS (
  SELECT symbol, close,
         ROW_NUMBER() OVER (PARTITION BY symbol ORDER BY px_date DESC) AS rn
  FROM prices
),
w AS (
  SELECT h.portfolio_id, h.symbol,
         ROUND(100.0 * SUM(h.qty * lp.close)
               / NULLIF(SUM(SUM(h.qty * lp.close)) OVER (PARTITION BY h.portfolio_id), 0), 2) AS current_w
  FROM holdings h
  JOIN latest_px lp ON lp.symbol = h.symbol AND lp.rn = 1
  GROUP BY h.portfolio_id, h.symbol
)
SELECT w.portfolio_id, w.symbol, w.current_w, t.target_w,
       w.current_w - t.target_w AS drift
FROM w
JOIN targets t USING (portfolio_id, symbol)
WHERE ABS(w.current_w - t.target_w) > 5;
```
**Explanation:** Weights are computed vs the book total in the same scan; drift over ±5 points triggers the manager's rebalance list.

## Q68: Portfolio turnover per year

**Query:**
```sql
-- MySQL
SELECT account_id, YEAR(traded_at) AS yr,
       ROUND(SUM(qty * price), 2) AS traded_notional
FROM trades
GROUP BY account_id, YEAR(traded_at)
ORDER BY yr, traded_notional DESC;
```
**Explanation:** Summed buy+sell notional per year is the base input for turnover (against average assets).

## Q69: Portfolio beta vs benchmark

**Query:**
```sql
-- PostgreSQL
WITH daily AS (
  SELECT px_date, SUM(h.qty * p.close) AS value
  FROM holdings h JOIN prices p USING (symbol)
  GROUP BY px_date
),
port_ret AS (
  SELECT px_date,
         (value - LAG(value) OVER (ORDER BY px_date)) / NULLIF(LAG(value) OVER (ORDER BY px_date), 0) AS ret
  FROM daily
)
SELECT ROUND(COVAR_POP(pr.ret, br.ret) / VAR_POP(br.ret), 3) AS beta
FROM port_ret pr
JOIN benchmark_returns br USING (px_date);
```
**Explanation:** Beta is the covariance of portfolio vs market returns divided by market variance — a single windowed CTE plus two aggregates.

## Q70: Net cash-flow forecast for the next 7 days

**Query:**
```sql
SELECT ccy,
       ROUND(SUM(amount), 2) AS net_7_day_flow,
       MIN(flow_date) AS first_flow_date
FROM cashflows
WHERE flow_date BETWEEN CURRENT_DATE AND CURRENT_DATE + INTERVAL '6 days'
GROUP BY ccy
ORDER BY net_7_day_flow;
```
**Explanation:** Summing scheduled flows over the horizon gives the treasury the short-term funding gap per currency.

**Alt1:**
```sql
-- SQL Server
SELECT ccy, SUM(amount) AS net_7_day_flow
FROM cashflows
WHERE flow_date BETWEEN CAST(GETDATE() AS DATE) AND DATEADD(day, 6, CAST(GETDATE() AS DATE))
GROUP BY ccy;
```

## Q71: Expected credit loss (EAD × PD × LGD)

**Query:**
```sql
SELECT loan_id,
       (principal - paid_principal) AS ead,
       ROUND(pd_pct, 4) AS probability_of_default,
       ROUND(lgd_pct, 4) AS loss_given_default,
       ROUND((principal - paid_principal) * (pd_pct / 100.0) * (lgd_pct / 100.0), 2) AS expected_loss
FROM loans
WHERE status = 'active';
```
**Explanation:** ECL is the standard product of exposure, probability of default, and loss severity — the input to impairment reserves.

## Q72: Deposit maturity ladder — what matures and when

**Query:**
```sql
SELECT maturity_date,
       COUNT(*) AS maturing_deposits,
       ROUND(SUM(amount), 2) AS maturing_balance
FROM deposits
WHERE maturity_date BETWEEN CURRENT_DATE AND CURRENT_DATE + INTERVAL '1 year'
GROUP BY maturity_date
ORDER BY maturity_date;
```
**Explanation:** Grouping by maturity date builds the ladder asset-liability managers use to see refinancing cliffs.

## Q73: Early-withdrawal penalty — six months of foregone interest

**Query:**
```sql
-- MySQL
SELECT d.account_id, d.amount, d.rate,
       ROUND(d.amount * (d.rate / 100.0) * 0.5 * DATEDIFF(d.maturity_date, d.opened_at) / 365.0, 2) AS early_penalty
FROM deposits d
WHERE d.account_id = 2025;
```
**Explanation:** Penalty = balance × rate × 0.5 years; using the term in days keeps the accrued interest comparable across products.

## Q74: FX cross rate — derive EURJPY from EURUSD × USDJPY

**Query:**
```sql
SELECT e.rate_date,
       ROUND(e.rate * j.rate, 4) AS eurjpy_cross
FROM fx_rates e
JOIN fx_rates j
  ON j.rate_date = e.rate_date
 AND j.ccy_pair  = 'USDJPY'
WHERE e.ccy_pair = 'EURUSD'
ORDER BY e.rate_date DESC
LIMIT 1;
```
**Explanation:** Chaining through USD multiplies the two direct rates, synthesizing a cross no market quote provides.

## Q75: Declined card authorizations by reason

**Query:**
```sql
SELECT decline_reason,
       COUNT(*) AS declines,
       ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 2) AS share_pct
FROM card_authorizations
WHERE status = 'declined'
GROUP BY decline_reason
ORDER BY declines DESC;
```
**Explanation:** A windowed SUM over the total decline count turns each reason into a share of the decline funnel.

## Q76: Monthly portfolio returns

**Query:**
```sql
-- PostgreSQL
WITH mv AS (
  SELECT portfolio_id, DATE_TRUNC('month', px_date) AS m,
         SUM(h.qty * p.close) AS value
  FROM holdings h JOIN prices p USING (symbol)
  GROUP BY 1, 2
)
SELECT portfolio_id, m, ROUND(value, 2) AS end_of_month_value,
       ROUND(100.0 * (value - LAG(value) OVER (PARTITION BY portfolio_id ORDER BY m))
             / LAG(value) OVER (PARTITION BY portfolio_id ORDER BY m), 2) AS monthly_return_pct
FROM mv
ORDER BY portfolio_id, m;
```
**Explanation:** Month-end NAVs are differenced via LAG; the result is the return series used for performance reporting.

## Q77: Annualized volatility of daily portfolio returns

**Query:**
```sql
-- PostgreSQL
WITH daily AS (
  SELECT portfolio_id, px_date, SUM(h.qty * p.close) AS value
  FROM holdings h JOIN prices p USING (symbol)
  GROUP BY portfolio_id, px_date
),
ret AS (
  SELECT portfolio_id, px_date,
         (value - LAG(value) OVER (PARTITION BY portfolio_id ORDER BY px_date))
         / NULLIF(LAG(value) OVER (PARTITION BY portfolio_id ORDER BY px_date), 0) AS r
  FROM daily
)
SELECT portfolio_id,
       ROUND(STDDEV_POP(r) * SQRT(252), 3) AS annualized_vol
FROM ret
GROUP BY portfolio_id;
```
**Explanation:** Annualization multiplies the daily standard deviation by the square root of trading days (252).

## Q78: One-day 95% Value-at-Risk (5th percentile of daily PnL)

**Query:**
```sql
-- PostgreSQL
WITH mv AS (
  SELECT portfolio_id, px_date, SUM(h.qty * p.close) AS v
  FROM holdings h JOIN prices p USING (symbol)
  GROUP BY portfolio_id, px_date
),
pnl AS (
  SELECT portfolio_id,
         v - LAG(v) OVER (PARTITION BY portfolio_id ORDER BY px_date) AS day_pnl
  FROM mv
)
SELECT DISTINCT portfolio_id,
       (SELECT ROUND(percentile_cont(0.05) WITHIN GROUP (ORDER BY pnl2.day_pnl), 2)
        FROM pnl pnl2 WHERE pnl2.portfolio_id = pnl.portfolio_id) AS var_95_1day
FROM pnl;
```
**Explanation:** The 5th percentile of observed daily PnL is the worst daily move expected with 95% confidence — a distributional risk metric.

## Q79: Exposure vs trader risk limit (breach detection)

**Query:**
```sql
-- PostgreSQL
SELECT t.trader_id, tl.limit_amount,
       ROUND(SUM(t.qty * t.price), 2) AS gross_today_notional,
       CASE WHEN SUM(t.qty * t.price) > tl.limit_amount THEN 'BREACH' ELSE 'OK' END AS limit_status
FROM trades t
JOIN trader_limits tl USING (trader_id)
WHERE t.traded_at::date = CURRENT_DATE
GROUP BY t.trader_id, tl.limit_amount;
```
**Explanation:** Same-day traded notional against the trader's cap; any excess is surfaced immediately as a breach.

**Alt1:**
```sql
-- MySQL 8 (same check with a window helper)
SELECT trader_id, limit_amount, SUM(qty * price) AS gross,
       IF(SUM(qty * price) > limit_amount, 'BREACH', 'OK') AS limit_status
FROM trades JOIN trader_limits USING (trader_id)
WHERE traded_at >= CURRENT_DATE
GROUP BY trader_id, limit_amount;
```

## Q80: Portfolio concentration — number of positions and top-10 weight

**Query:**
```sql
WITH latest_px AS (
  SELECT symbol, close,
         ROW_NUMBER() OVER (PARTITION BY symbol ORDER BY px_date DESC) AS rn
  FROM prices
),
pos AS (
  SELECT h.portfolio_id, h.symbol, SUM(h.qty * lp.close) AS mv
  FROM holdings h
  JOIN latest_px lp ON lp.symbol = h.symbol AND lp.rn = 1
  GROUP BY h.portfolio_id, h.symbol
),
ranked AS (
  SELECT portfolio_id, mv,
         ROW_NUMBER() OVER (PARTITION BY portfolio_id ORDER BY mv DESC) AS rn
  FROM pos
)
SELECT portfolio_id,
       COUNT(*) AS positions,
       ROUND(SUM(CASE WHEN rn <= 10 THEN mv END), 2) AS top10_value,
       ROUND(SUM(mv), 2) AS total_value,
       ROUND(100.0 * SUM(CASE WHEN rn <= 10 THEN mv END) / NULLIF(SUM(mv), 0), 2) AS top10_weight_pct
FROM ranked
GROUP BY portfolio_id;
```
**Explanation:** Clouding the position roster with a concentration measure tells whether the book is diversified or a handful of bets.

## Q81: Stop-loss scan — open positions more than 10% underwater

**Query:**
```sql
WITH open_pos AS (
  SELECT account_id, symbol, SUM(qty) AS qty, SUM(qty * price) / SUM(qty) AS avg_cost
  FROM trades
  WHERE side = 'BUY'
  GROUP BY account_id, symbol
)
SELECT o.account_id, o.symbol, o.qty,
       ROUND(o.avg_cost, 2) AS avg_cost,
       ROUND(lp.close, 2) AS last_close,
       ROUND(100.0 * (lp.close - o.avg_cost) / o.avg_cost, 2) AS unrealized_return_pct
FROM open_pos o
JOIN (SELECT symbol, close,
             ROW_NUMBER() OVER (PARTITION BY symbol ORDER BY px_date DESC) AS rn
      FROM prices) lp ON lp.symbol = o.symbol AND lp.rn = 1
WHERE lp.close < o.avg_cost * 0.90
ORDER BY unrealized_return_pct;
```
**Explanation:** Any open position below 90% of its average cost is a candidate for the risk desk's stop-out list.

## Q82: Best and worst performing open positions

**Query:**
```sql
-- PostgreSQL (top 5 gainers)
WITH open_pos AS (
  SELECT account_id, symbol, SUM(qty) AS qty, SUM(qty * price) / SUM(qty) AS avg_cost
  FROM trades WHERE side = 'BUY'
  GROUP BY account_id, symbol
),
last_px AS (
  SELECT symbol, close,
         ROW_NUMBER() OVER (PARTITION BY symbol ORDER BY px_date DESC) AS rn
  FROM prices
)
SELECT o.account_id, o.symbol,
       ROUND(((lp.close - o.avg_cost) / o.avg_cost) * 100, 2) AS return_pct
FROM open_pos o
JOIN last_px lp ON lp.symbol = o.symbol AND lp.rn = 1
WHERE o.avg_cost > 0
ORDER BY return_pct DESC
LIMIT 5;
```
**Explanation:** Reusing the open-position CTE, ORDER BY on the return ranks the book's winners; swapping DESC for ASC gives the losers.

## Q83: FX hedge tolerance — net exposure per currency versus limits

**Query:**
```sql
SELECT ccy,
       SUM(CASE WHEN side = 'BUY'  THEN notional
                WHEN side = 'SELL' THEN -notional END) AS net_notional,
       CASE WHEN ABS(SUM(CASE WHEN side = 'BUY' THEN notional
                              WHEN side = 'SELL' THEN -notional END)) < 1000000
            THEN 'hedged_within_tolerance'
            ELSE 'unhedged' END AS hedge_status
FROM fx_positions
GROUP BY ccy;
```
**Explanation:** Long/short sign handling nets each currency; small residuals mean the book is effectively hedged.

## Q84: Claims severity distribution

**Query:**
```sql
SELECT CASE
         WHEN claim_amount <  10000     THEN 'low'
         WHEN claim_amount <  100000    THEN 'medium'
         WHEN claim_amount <  1000000   THEN 'high'
         ELSE 'catastrophic' END AS severity_band,
       COUNT(*) AS claims,
       ROUND(AVG(claim_amount), 2) AS avg_claim,
       ROUND(SUM(claim_amount), 2) AS total_claims
FROM claims
WHERE status = 'settled'
GROUP BY 1
ORDER BY MIN(claim_amount);
```
**Explanation:** CASE bands produce the severity ladder; ORDER BY on the minimum amount keeps bands in natural order.

## Q85: Earned premium (pro-rata over the policy term)

**Query:**
```sql
-- PostgreSQL
SELECT policy_id,
       ROUND(premium * LEAST(1.0, GREATEST((CURRENT_DATE - effective) / 365.0, 0.0)), 2) AS earned_premium,
       ROUND(premium, 2) - ROUND(premium * LEAST(1.0, GREATEST((CURRENT_DATE - effective) / 365.0, 0.0)), 2) AS unearned_premium
FROM policies
WHERE status IN ('in_force', 'lapsed')
ORDER BY unearned_premium DESC;
```
**Explanation:** Days elapsed over policy term clip to [0,1] via LEAST/GREATEST; what is not earned stays in the unearned reserve.

## Q86: Policy churn — lapse counts by prior product type

**Query:**
```sql
SELECT prev_policy_type,
       COUNT(*) AS renewals_expected,
       COUNT(*) FILTER (WHERE renewal = 'lapsed') AS churned,
       ROUND(100.0 * COUNT(*) FILTER (WHERE renewal = 'lapsed') / COUNT(*), 2) AS churn_rate_pct
FROM renewals
GROUP BY prev_policy_type
ORDER BY churn_rate_pct DESC;
```
**Explanation:** Renewal outcomes per product family quantify where the book leaks customers most.

## Q87: Offsetting (wash-style) trades — buy then sell same day

**Query:**
```sql
-- PostgreSQL
SELECT buy.trade_id  AS buy_trade, sell.trade_id AS sell_trade,
       buy.symbol, buy.account_id, buy.traded_at
FROM trades buy
JOIN trades sell
  ON sell.account_id  = buy.account_id
 AND sell.symbol      = buy.symbol
 AND sell.side        = 'SELL'
 AND buy.side         = 'BUY'
 AND sell.traded_at::date = buy.traded_at::date
 AND sell.traded_at > buy.traded_at;
```
**Explanation:** Rounding behavior — buying and selling the same name intraday — is the pattern audit and compliance watch for.

## Q88: Capstone pipeline — step 1: size the book (mark-to-market NAV)

**Query:**
```sql
WITH latest_px AS (
  SELECT symbol, close,
         ROW_NUMBER() OVER (PARTITION BY symbol ORDER BY px_date DESC) AS rn
  FROM prices
)
SELECT pf.portfolio_id, pf.name,
       ROUND(SUM(h.qty * lp.close), 2) AS nav_mtm
FROM portfolio pf
JOIN holdings h USING (portfolio_id)
JOIN latest_px lp ON lp.symbol = h.symbol AND lp.rn = 1
GROUP BY pf.portfolio_id, pf.name
ORDER BY nav_mtm DESC;
```
**Explanation:** Latest-price join against every holding yields the current market value of each book.

## Q89: Capstone pipeline — step 2: day-over-day PnL and MTM series

**Query:**
```sql
WITH mv AS (
  SELECT h.portfolio_id, p.px_date, SUM(h.qty * p.close) AS value
  FROM holdings h JOIN prices p USING (symbol)
  GROUP BY h.portfolio_id, p.px_date
)
SELECT portfolio_id, px_date,
       ROUND(value, 2) AS mtm,
       ROUND(value - LAG(value) OVER (PARTITION BY portfolio_id ORDER BY px_date), 2) AS daily_pnl
FROM mv
ORDER BY portfolio_id, px_date;
```
**Explanation:** Revalues the full price history and differences it — the PnL engine feeding risk and P&L attribution.

## Q90: Capstone pipeline — step 3: risk limit check against current NAV

**Query:**
```sql
WITH latest_px AS (
  SELECT symbol, close,
         ROW_NUMBER() OVER (PARTITION BY symbol ORDER BY px_date DESC) AS rn
  FROM prices
),
exposure AS (
  SELECT h.portfolio_id, SUM(h.qty * lp.close) AS gross_exposure
  FROM holdings h
  JOIN latest_px lp ON lp.symbol = h.symbol AND lp.rn = 1
  GROUP BY h.portfolio_id
)
SELECT e.portfolio_id,
       ROUND(e.gross_exposure, 2) AS exposure,
       rl.limit_amount,
       CASE WHEN e.gross_exposure > rl.limit_amount THEN 'BREACH' ELSE 'OK' END AS limit_status
FROM exposure e
JOIN risk_limits rl USING (portfolio_id)
ORDER BY limit_status, exposure DESC;
```
**Explanation:** Gross exposure is compared with each portfolio's configured limit; breaches bubble to the top.

**Alt1:**
```sql
-- SQL Server (same limit check with an explicit windowed latest-price CTE)
WITH last_px AS (
  SELECT symbol, close,
         ROW_NUMBER() OVER (PARTITION BY symbol ORDER BY px_date DESC) AS rn
  FROM prices
)
SELECT e.portfolio_id,
       ROUND(e.gross_exposure, 2) AS exposure,
       rl.limit_amount,
       CASE WHEN e.gross_exposure > rl.limit_amount THEN 'BREACH' ELSE 'OK' END AS limit_status
FROM (
  SELECT h.portfolio_id, SUM(h.qty * lp.close) AS gross_exposure
  FROM holdings h
  JOIN last_px lp ON lp.symbol = h.symbol AND lp.rn = 1
  GROUP BY h.portfolio_id
) e
JOIN risk_limits rl ON rl.portfolio_id = e.portfolio_id
ORDER BY limit_status, exposure DESC;

```
## Q91: Capstone pipeline — step 4: sector concentration limit check

**Query:**
```sql
-- PostgreSQL
WITH latest_px AS (
  SELECT symbol, close,
         ROW_NUMBER() OVER (PARTITION BY symbol ORDER BY px_date DESC) AS rn
  FROM prices
),
sector_mv AS (
  SELECT h.portfolio_id, sec.sector,
         SUM(h.qty * lp.close) AS smv,
         SUM(SUM(h.qty * lp.close)) OVER (PARTITION BY h.portfolio_id) AS total
  FROM holdings h
  JOIN latest_px lp ON lp.symbol = h.symbol AND lp.rn = 1
  JOIN securities sec USING (symbol)
  GROUP BY h.portfolio_id, sec.sector
)
SELECT portfolio_id, sector,
       ROUND(100.0 * smv / NULLIF(total, 0), 2) AS weight_pct,
       CASE WHEN 100.0 * smv / NULLIF(total, 0) > 25 THEN 'SECTOR_LIMIT_BREACH' ELSE 'OK' END AS check_status
FROM sector_mv
ORDER BY portfolio_id, weight_pct DESC;
```
**Explanation:** Sector weights are computed in the same pass as the portfolio totals; a 25% cap flags over-concentration.

## Q92: Capstone pipeline — step 5: translate multi-currency NAV to base currency

**Query:**
```sql
-- PostgreSQL
WITH latest_px AS (
  SELECT symbol, close,
         ROW_NUMBER() OVER (PARTITION BY symbol ORDER BY px_date DESC) AS rn
  FROM prices
),
mtm AS (
  SELECT h.portfolio_id, h.symbol, sec.ccy, h.qty * lp.close AS market_value_local
  FROM holdings h
  JOIN latest_px lp ON lp.symbol = h.symbol AND lp.rn = 1
  JOIN securities sec USING (symbol)
)
SELECT m.portfolio_id, m.ccy,
       ROUND(SUM(m.market_value_local), 2) AS local_value,
       ROUND(SUM(m.market_value_local * COALESCE(fx.rate, 1)), 2) AS value_in_reference_ccy
FROM mtm m
LEFT JOIN fx_rates fx
  ON fx.ccy_pair = m.ccy || 'USD'
 AND fx.rate_date = (SELECT MAX(rate_date) FROM fx_rates)
GROUP BY m.portfolio_id, m.ccy
ORDER BY m.portfolio_id;
```
**Explanation:** Securities carry a currency; each local value is revalued via the FX table with USD treated as rate 1.

## Q93: Stress test — NAV under a 20% equity haircut

**Query:**
```sql
WITH latest_px AS (
  SELECT symbol, close,
         ROW_NUMBER() OVER (PARTITION BY symbol ORDER BY px_date DESC) AS rn
  FROM prices
)
SELECT h.portfolio_id,
       ROUND(SUM(h.qty * lp.close), 2) AS base_nav,
       ROUND(SUM(CASE WHEN sec.asset_class = 'equity'
                      THEN h.qty * lp.close * 0.80
                      ELSE h.qty * lp.close END), 2) AS stressed_nav_20pct
FROM holdings h
JOIN latest_px lp ON lp.symbol = h.symbol AND lp.rn = 1
JOIN securities sec USING (symbol)
GROUP BY h.portfolio_id
ORDER BY stressed_nav_20pct;
```
**Explanation:** A scenario-scalar applied only to equities yields the shocked NAV the board wants in the risk pack.

## Q94: Margin watch — account equity (cash + securities) below zero

**Query:**
```sql
WITH open_pos AS (
  SELECT account_id, symbol, SUM(qty) AS qty, SUM(qty * price) / SUM(qty) AS avg_cost
  FROM trades WHERE side = 'BUY'
  GROUP BY account_id, symbol
),
unreal AS (
  SELECT o.account_id, SUM((lp.close - o.avg_cost) * o.qty) AS unrealized
  FROM open_pos o
  JOIN (SELECT symbol, close,
               ROW_NUMBER() OVER (PARTITION BY symbol ORDER BY px_date DESC) AS rn
        FROM prices) lp ON lp.symbol = o.symbol AND lp.rn = 1
  GROUP BY o.account_id
)
SELECT a.account_id, ROUND(a.balance, 2) AS cash_balance,
       ROUND(u.unrealized, 2) AS unrealized_pnl,
       ROUND(a.balance + u.unrealized, 2) AS account_equity
FROM accounts a
JOIN unreal u USING (account_id)
WHERE a.balance + u.unrealized < 0;
```
**Explanation:** Equity is cash plus open-position gains/losses; negative equity is the margin call or liquidation queue.

## Q95: AML — customers breaching the single-day credit threshold

**Query:**
```sql
-- PostgreSQL
SELECT a.customer_id, t.tx_time::date AS day,
       ROUND(SUM(t.amount), 2) AS daily_inflow
FROM transactions t
JOIN accounts a USING (account_id)
WHERE t.tx_type IN ('credit', 'payment')
GROUP BY a.customer_id, t.tx_time::date
HAVING SUM(t.amount) > 50000
ORDER BY daily_inflow DESC;
```
**Explanation:** Aggregating same-day inflows per customer uncovers rapid-credit patterns that exceed the monitored threshold.

## Q96: FX position PnL from revaluation against the latest rate

**Query:**
```sql
-- PostgreSQL
SELECT f.ccy, f.notional,
       fx.rate AS latest_rate,
       ROUND(f.notional * fx.rate, 2) AS value_in_usd,
       ROUND(f.notional * (fx.rate - COALESCE(f.entry_rate, 1)), 2) AS pnI_to_date
FROM fx_positions f
JOIN fx_rates fx
  ON fx.ccy_pair = f.ccy || 'USD'
 AND fx.rate_date = (SELECT MAX(rate_date) FROM fx_rates)
ORDER BY pnI_to_date;
```
**Explanation:** Notional revalued at the spot rate minus the entry rate gives the current FX mark-to-market PnL.

## Q97: Assets under management by portfolio manager

**Query:**
```sql
WITH latest_px AS (
  SELECT symbol, close,
         ROW_NUMBER() OVER (PARTITION BY symbol ORDER BY px_date DESC) AS rn
  FROM prices
)
SELECT pm.pm_name,
       ROUND(SUM(h.qty * lp.close), 2) AS aum
FROM portfolio_managers pm
JOIN portfolio pf USING (pm_id)
JOIN holdings h USING (portfolio_id)
JOIN latest_px lp ON lp.symbol = h.symbol AND lp.rn = 1
GROUP BY pm.pm_name
ORDER BY aum DESC;
```
**Explanation:** Joining managers → portfolios → holdings → latest price aggregates each manager's book.

## Q98: Trailing stop signal — 20-day peak versus today's close

**Query:**
```sql
-- PostgreSQL (WINDOW clause for reuse)
WITH w AS (
  SELECT symbol, px_date, close,
         MAX(close) OVER w AS peak_20
  FROM prices
  WINDOW w AS (PARTITION BY symbol ORDER BY px_date
               ROWS BETWEEN 20 PRECEDING AND CURRENT ROW)
)
SELECT symbol, px_date, ROUND(close, 2) AS close,
       ROUND(peak_20, 2) AS peak_20d,
       CASE WHEN close <= 0.90 * peak_20 THEN 'STOP' ELSE 'HOLD' END AS signal
FROM w
WHERE px_date = (SELECT MAX(px_date) FROM prices);
```
**Explanation:** A named WINDOW frames the rolling peak; a 10% drop off it triggers the trailing stop.

## Q99: Capital adequacy — risk-weighted assets by bank

**Query:**
```sql
SELECT e.bank_id,
       ROUND(SUM(e.exposure), 2) AS gross_exposure,
       ROUND(SUM(e.exposure * a.risk_weight), 2) AS risk_weighted_assets,
       ROUND(SUM(e.exposure * a.risk_weight) / NULLIF(SUM(e.exposure), 0), 4) AS avg_risk_weight
FROM exposures e
JOIN asset_classes a USING (asset_class)
GROUP BY e.bank_id
ORDER BY risk_weighted_assets DESC;
```
**Explanation:** Exposure per asset class is weighted by its regulatory risk weight; totals feed the capital ratio numerator.

## Q100: Capstone — full mark-to-market + risk-limit check pipeline

**Query:**
```sql
-- PostgreSQL
WITH latest_px AS (
  SELECT symbol, px_date, close,
         ROW_NUMBER() OVER (PARTITION BY symbol ORDER BY px_date DESC) AS rn
  FROM prices
),
mtm AS (
  SELECT h.portfolio_id, h.symbol, h.qty, lp.close,
         h.qty * lp.close AS market_value
  FROM holdings h
  JOIN latest_px lp ON lp.symbol = h.symbol AND lp.rn = 1
),
nav AS (
  SELECT portfolio_id, ROUND(SUM(market_value), 2) AS mtm_value
  FROM mtm GROUP BY portfolio_id
),
series AS (
  SELECT h.portfolio_id, p.px_date, SUM(h.qty * p.close) AS portfolio_value
  FROM holdings h JOIN prices p USING (symbol)
  GROUP BY h.portfolio_id, p.px_date
),
daily_pnl AS (
  SELECT portfolio_id, px_date,
         ROUND(portfolio_value - LAG(portfolio_value)
               OVER (PARTITION BY portfolio_id ORDER BY px_date), 2) AS pnl
  FROM series
)
SELECT n.portfolio_id,
       n.mtm_value,
       MAX(dp.pnl) FILTER (WHERE dp.px_date = (SELECT MAX(px_date) FROM prices)) AS last_daily_pnl,
       rl.limit_amount,
       CASE WHEN n.mtm_value > rl.limit_amount
            THEN 'BREACH'
            WHEN MAX(dp.pnl) FILTER (WHERE dp.px_date = (SELECT MAX(px_date) FROM prices)) < 0
            THEN 'MARGIN_WATCH'
            ELSE 'OK' END AS pipeline_status
FROM nav n
JOIN risk_limits rl USING (portfolio_id)
LEFT JOIN daily_pnl dp USING (portfolio_id)
GROUP BY n.portfolio_id, n.mtm_value, rl.limit_amount
ORDER BY n.mtm_value DESC;
```
**Explanation:** Five chained CTEs — latest price, mark-to-market, NAV, PnL series, and limit comparison — execute the whole risk workflow in one query, emitting a single breach/margin exception report.

**Alt1:**
```sql
-- SQL Server (same pipeline, materialized step by step with temp tables)
SELECT symbol, close
INTO #latest_px
FROM (
  SELECT symbol, close,
         ROW_NUMBER() OVER (PARTITION BY symbol ORDER BY px_date DESC) AS rn
  FROM prices
) x
WHERE rn = 1;

SELECT h.portfolio_id, SUM(h.qty * lp.close) AS mtm_value
INTO #nav
FROM holdings h
JOIN #latest_px lp ON lp.symbol = h.symbol
GROUP BY h.portfolio_id;

SELECT n.portfolio_id, n.mtm_value, rl.limit_amount,
       CASE WHEN n.mtm_value > rl.limit_amount THEN 'BREACH' ELSE 'OK' END AS pipeline_status
FROM #nav n
JOIN risk_limits rl ON rl.portfolio_id = n.portfolio_id
ORDER BY n.mtm_value DESC;

DROP TABLE #latest_px, #nav;

```
