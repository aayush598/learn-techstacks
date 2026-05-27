# Chapter 09: Dunning Management & Failed Payments

> **Part:** 17 - Billing, Subscription & Monetization

---

## Sections

| # | Section | Description |
|---|---------|-------------|
| 01 | [Dunning Workflow Design](sec-01-dunning-workflow-design.md) | Dunning process stages, retry schedule, escalation path, communication timing |
| 02 | [Smart Retry Scheduling](sec-02-smart-retry-scheduling.md) | Exponential backoff retry, card network retry windows, optimal retry times, max retry limits |
| 03 | [Payment Method Update Flow](sec-03-payment-method-update-flow.md) | Payment link generation, customer portal redirect, in-app payment update, auto-retry after update |
| 04 | [Subscription Downgrade Rules](sec-04-subscription-downgrade-rules.md) | Automatic downgrade on failure, downgrade tiers, feature restriction enforcement, grace period |
| 05 | [Grace Period Handling](sec-05-grace-period-handling.md) | Service continuation during grace, grace period duration, feature restrictions during grace |
| 06 | [Recover Lost Revenue](sec-06-recover-lost-revenue.md) | Win-back email sequences, discount offers, re-activation flow, payment retry campaigns |
| 07 | [Dunning Communication](sec-07-dunning-communication.md) | Email templates per stage, SMS notifications, in-app banners, push notifications |
| 08 | [Involuntary Churn Monitoring](sec-08-involuntary-churn-monitoring.md) | Churn cause tracking, failure reason analysis, recovery rate metrics, dunning effectiveness |

---

## Dunning Schedule

| Day | Action | Channel |
|-----|--------|---------|
| 0 | Payment fails | Webhook received |
| 0 | First retry (immediate) | Card network |
| 1 | Day 1 email: "Payment failed, update method" | Email |
| 2 | Second retry | Card network |
| 3 | Day 3 email: "Update payment to continue service" | Email + In-app |
| 5 | Third retry | Card network |
| 7 | Day 7: Service restricted (read-only) | Email + In-app |
| 10 | Fourth retry | Card network |
| 14 | Day 14: Final notice before cancellation | Email + SMS |
| 21 | Automatic downgrade/ cancellation | System action |
| 30 | Send win-back offer | Email |
