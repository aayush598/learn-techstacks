# Section 03: Access Reviews & Recertification

Periodic access reviews ensure that user access rights remain appropriate over time. SOC 2 requires regular review of logical access (quarterly for administrators, annually for all users). The access recertification system automates the review process: notifies managers, tracks completion, and automatically revokes stale access.

Access review process: system generates a list of all active users with their roles and permissions → reviewer (manager or security team) reviews each user's access → reviewer attests (approve, modify, or revoke) → if no response within deadline, access auto-revoked → changes are logged → next review scheduled. The process covers: platform admin access, tenant admin access, API keys, service accounts, and third-party integrations.

Recertification automation: access review campaigns are created quarterly. Campaigns include: user list, current permissions, last login date, and access justification. Reviewers receive email notifications with a link to the review dashboard. Outstanding reviews are escalated weekly. The system enforces: if a user hasn't logged in for 90 days, access is suspended; if a manager doesn't review by deadline, access is locked.
