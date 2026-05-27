# Chapter 03: Campaign Scheduling & Timezone Handling

> **Part:** 09 - Campaign Management

---

## Sections

| # | Section | Description |
|---|---------|-------------|
| 01 | [Schedule Definition Types](sec-01-schedule-definition-types.md) | One-time, recurring, advanced schedule types — cron expressions, time windows, recurrence rules |
| 02 | [Timezone Detection & Resolution](sec-02-timezone-detection-resolution.md) | Phone number timezone lookup, IP geolocation, area code mapping, user-provided timezone |
| 03 | [Calling Window Enforcement](sec-03-calling-window-enforcement.md) | Configurable calling windows — per-contact timezone windows, statutory limits, window calculation |
| 04 | [DST Transition Handling](sec-04-dst-transition-handling.md) | Daylight saving time transitions — spring-forward/fall-back handling, schedule adjustment |
| 05 | [Blackout Dates & Holiday Calendar](sec-05-blackout-dates-holiday-calendar.md) | Global and per-campaign blackout dates, holiday calendar integration, legal holiday compliance |
| 06 | [Timezone-Aware Dialing Engine](sec-06-timezone-aware-dialing-engine.md) | Dialing engine with timezone awareness — look-ahead scheduling, timezone sorting, window checking |
| 07 | [Compliance Hour Configuration](sec-07-compliance-hour-configuration.md) | Per-state/province compliance hours — configurable rules, regulation database, automatic enforcement |
| 08 | [Schedule Optimization Analytics](sec-08-schedule-optimization-analytics.md) | Best calling time analysis, schedule effectiveness metrics, A/B schedule testing |

---

## Key Takeaways

- Timezone detection must combine multiple sources (phone, IP, user-provided) for accuracy
- Calling windows must respect both configurable business rules and statutory regulations
- DST transitions require careful handling to avoid schedule gaps or double-dialing
- Blackout dates and holidays must be checked before every dial attempt
- Compliance hours vary by jurisdiction and must be configurable per campaign
