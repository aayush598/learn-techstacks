# Client Handover

## The Handover Process That Prevents Support Hell

A great handover is the difference between a client who disappears happily and one who calls you every week forever. Proper handover sets boundaries, creates closure, and positions you for future work.

This guide covers the complete handover process, documentation requirements, training, knowledge transfer, and post-launch support structure.

---

## Why Handover Matters

### The Cost of Bad Handover

| Problem | Impact | Cost |
|---------|--------|------|
| No documentation | Client calls you for every question | 5+ hours/month forever |
| No training | Client struggles, blames your work | Reputation damage |
| No knowledge transfer | Client can't maintain | Scope creep into support |
| No boundaries | Support requests forever | Lost focus on new projects |
| No closure | No upsell opportunity | Lost revenue |

### The Handover ROI

| Investment | Return |
|------------|--------|
| 4 hours on handover document | Saves 20+ hours of support calls |
| 1 hour on training | Reduces support by 80% |
| 2 hours on knowledge transfer | Client can self-serve |
| 30 min on upsell discussion | 40% chance of retainer |

---

## The Handover Timeline

### 30 Days Before Launch

- Begin writing handover document
- Schedule training sessions
- Plan knowledge transfer

### 14 Days Before Launch

- Share draft handover document
- Confirm training schedule
- Set launch date

### 7 Days Before Launch

- Finalize handover document
- Conduct training sessions
- Set up monitoring and alerts

### Launch Day

- Deploy to production
- Verify everything works
- Send launch announcement
- Begin post-launch support period

### Post-Launch Support Period

| Week | Focus | Client Involvement |
|------|-------|-------------------|
| Week 1 | Active monitoring, bug fixes | High — daily check-ins |
| Week 2 | Issue resolution, polish | Medium — every 2 days |
| Week 3 | Handover completion | Low — weekly check-in |
| Week 4 | Final handover, close out | Low — final review |

---

## The Handover Document

### What to Include

**1. Project Overview**
```
Project Name:
Client:
Date:
Author:
Version:

Brief project description:
What was built:
Key features:
```

**2. Technical Architecture**
```
System architecture diagram (or reference to it)
Technology stack:
  - Frontend: [Framework, version]
  - Backend: [Framework, version]
  - Database: [Database, version]
  - Infrastructure: [Hosting, CI/CD]
  - Third-party services: [List with API key locations]

Architecture decisions and rationale:
```

**3. Code Repository Information**
```
Repository location: [URL]
Branch structure:
  - main: Production
  - staging: Pre-production testing
  - develop: Active development

Access instructions:
Deployment permissions:
```

**4. Environment Information**
```
Environment | URL | Access Method
Production  | [URL] | [How to access]
Staging     | [URL] | [How to access]
Development | [URL] | [How to access]

Environment variables:
  - Key: [Name] — Description — Location
  - Key: [Name] — Description — Location

Database information:
  - Type: [PostgreSQL/MySQL/MongoDB]
  - Version: [Version]
  - Connection: [How to connect]
  - Backups: [Schedule and location]
```

**5. Deployment Process**
```
Deployment method:
Deployment steps:
  1. [Step]
  2. [Step]
  3. [Step]

Rollback procedure:
  1. [Step]
  2. [Step]

CI/CD pipeline: [Description]
Deployment frequency recommendation:
```

**6. Admin/User Guide**
```
How to log in:
How to manage users:
How to update content:
How to configure settings:
Common tasks:
  - Task 1: [Instructions]
  - Task 2: [Instructions]
  - Task 3: [Instructions]
```

**7. Monitoring and Alerts**
```
Monitoring tools used:
Key metrics to watch:
Alert thresholds:
Who gets alerts:
Incident response process:
  1. [Step]
  2. [Step]
```

**8. Known Issues and Limitations**
```
Known issues:
  - Issue 1: [Description, workaround, planned fix timeline]
  - Issue 2: [Description, workaround, planned fix timeline]

Limitations:
  - Limitation 1: [Description, recommended solution]
  - Limitation 2: [Description, recommended solution]
```

**9. Maintenance Schedule**
```
Daily:
  - [Task]

Weekly:
  - [Task]

Monthly:
  - [Task]

Quarterly:
  - [Task]
```

**10. Support and Contact**
```
Primary contact:
Escalation contact:
Support hours:
Response times:
Emergency process:
End of support date:
```

### Handover Document Template

```markdown
# [Project Name] — Handover Document

## 1. Project Overview
[Brief description]

## 2. Quick Start
[How to access and verify the system is working]

## 3. Architecture
[Link to architecture diagram]
[Brief description of how components interact]

## 4. Environments

| Environment | URL | Purpose |
|-------------|-----|---------|
| Production | [URL] | Live system |
| Staging | [URL] | Testing |
| Development | [URL] | Development |

## 5. Access

| System | Access Method | Credentials Location |
|--------|---------------|---------------------|
| Hosting | [Link] | [Password manager] |
| Database | [Connection string] | [Password manager] |
| Admin panel | [URL] | [Password manager] |
| Analytics | [URL] | [Password manager] |

## 6. Common Tasks

### Update Content
[Step-by-step instructions]

### Add User
[Step-by-step instructions]

### Deploy Update
[Step-by-step instructions]

### Rollback
[Step-by-step instructions]

## 7. Troubleshooting

### Problem: [Common issue]
Solution: [Steps to resolve]

### Problem: [Common issue]
Solution: [Steps to resolve]

## 8. Support
Support available through [date].
Contact: [email/phone]
Emergency: [process]
```

---

## Training and Knowledge Transfer

### Training Session Structure

**Session 1: Admin Training (60 minutes)**
- System overview
- Admin panel walkthrough
- User management
- Content management
- Common tasks
- Q&A

**Session 2: Technical Training (60 minutes)**
- Architecture overview
- Code structure
- Deployment process
- Monitoring and alerts
- Troubleshooting
- Q&A

**Session 3: Maintenance Training (30 minutes)**
- Regular maintenance tasks
- Backup verification
- Performance monitoring
- Security updates
- Q&A

### Training Delivery

**Live Training:**
- Record the session (client can rewatch)
- Follow along with the system
- Let them do tasks themselves
- Provide written step-by-step guides
- End with Q&A

**Async Training:**
- Create Loom videos for each topic
- Provide written documentation alongside
- Give them tasks to complete independently
- Schedule office hours for questions

### Knowledge Transfer Checklist

```
☐ Admin training completed
☐ Technical training completed
☐ Maintenance training completed
☐ Training recordings delivered
☐ Written guides provided
☐ Client can perform basic tasks independently
☐ Client knows who to contact for issues
☐ Client understands support boundaries
☐ Client has tested admin tasks
☐ Client has deployed a change (if applicable)
```

### Training Completion Criteria

The client can independently:
1. Log in and navigate the system
2. Perform basic admin tasks (add users, update content)
3. Understand what to monitor
4. Know how to report issues
5. Differentiate between support and new work

---

## Credential Transfer

### Secure Credential Transfer Process

**NEVER send credentials via:**
- Email (unencrypted)
- Slack
- Text message
- Written notes

**ALWAYS use:**
- Password manager shared vault (1Password, Bitwarden)
- Encrypted document (with separate channel for password)
- In-person handover for critical credentials

### Credential Handover Checklist

```
☐ Hosting/cloud provider access
☐ Domain registrar access
☐ DNS management access
☐ Database access
☐ Admin panel login
☐ Email service access
☐ Analytics access
☐ SSL certificate management
☐ CDN management
☐ Monitoring tool access
☐ Error tracking access
☐ Third-party service accounts
☐ API keys regenerated (for security)
☐ Shared password vault created
☐ Access revoked for temporary accounts
```

### Credential Transition Best Practices

1. **Create new, strong passwords** for handover
2. **Add client as owner/admin**, remove yourself
3. **Document all services and billing accounts**
4. **Set up billing alerts** so client knows when payments are due
5. **Keep backup access** for support period, then remove

---

## Post-Launch Support

### Support Period Structure

| Period | Duration | Focus |
|--------|----------|-------|
| Hyper-care | Days 1-3 | Active monitoring, immediate response |
| Active support | Days 4-14 | Bug fixes, minor adjustments |
| Transition | Days 15-30 | Client independence, knowledge transfer |
| Handover complete | Day 31+ | Support ends (or retainer begins) |

### What's Included in Post-Launch Support

**In scope:**
- Bug fixes for delivered features
- Minor UI adjustments (less than 2 hours)
- Questions about system usage
- Troubleshooting guidance
- Emergency response for critical issues

**Out of scope (billable separately):**
- New features
- Content creation/updates
- Major design changes
- Third-party integration changes
- Training additional team members
- Performance optimization beyond fixes

### Support Communication

**Issue Reporting Process:**
1. Client reports issue via [Slack/Email/Portal]
2. You acknowledge within [response time]
3. You triage: Critical / Major / Minor / Question
4. You provide fix or timeline
5. You resolve and close

**Issue Severity Levels:**

| Severity | Definition | Response Time | Resolution Time |
|----------|------------|---------------|-----------------|
| Critical | System down, data loss | 1 hour | 4 hours |
| Major | Feature broken, workaround exists | 4 hours | 24 hours |
| Minor | Cosmetic, non-blocking | 24 hours | 1 week |
| Question | How-to, clarification | 24 hours | 48 hours |

### Support Boundaries Script

"As we move into post-launch support, here's how it works:

**Included in support (through [date]):**
- Bug fixes for anything we built
- Minor adjustments under 2 hours
- Questions about how the system works

**Not included (we can scope separately):**
- New features or functionality
- Content updates
- Third-party integration changes

To report an issue, just [Slack/Email]. I'll respond within [timeframe] and keep you updated until resolution.

For critical issues (system down), here's my emergency contact: [phone]."

---

## Post-Launch Review Meeting

### Schedule (2-4 Weeks After Launch)

**Agenda:**
1. How's the system performing? (10 min)
2. Any issues or concerns? (10 min)
3. Metrics and results review (10 min)
4. Feedback on working together (5 min)
5. Future opportunities (10 min)
6. Next steps (5 min)

### Review Meeting Script

"Thanks for joining. The purpose of this meeting is to review how everything's going and discuss next steps.

**Performance:**
The system has been [uptime]% uptime. We've resolved [X] issues since launch. Performance metrics are [metrics].

**Your Experience:**
How has the system been working for you? Any frustrations or things you'd like improved?

**Results:**
Based on the goals we set at the beginning, here's how we're tracking: [results vs. goals].

**Future Opportunities:**
Based on what we've learned, here are some things I'd recommend for Phase 2:
1. [Opportunity 1]
2. [Opportunity 2]
3. [Opportunity 3]

Would you like to discuss any of these?

**Feedback:**
How was your experience working with me? What could I do better next time?

**Next Steps:**
Support continues through [date]. After that, we can discuss a maintenance retainer or new project."

---

## Closure and Transition

### Support Closeout

**At the end of the support period:**

1. **Final review** — Confirm all known issues are resolved
2. **Documentation update** — Add any new knowledge gained during support
3. **Credential transition** — Remove your access (if appropriate)
4. **Final invoice** — Close out any remaining billing
5. **Feedback collection** — Get testimonial and case study
6. **Referral request** — Ask for introductions

### Transition to Independence

Help the client become self-sufficient:

1. **Knowledge base** — All documentation in one place
2. **Troubleshooting guides** — Common issues and solutions
3. **Vendor contacts** — Who to call for each service
4. **Maintenance calendar** — When to do what
5. **Decision framework** — When to call you vs. DIY

### Closing Email Template

Subject: [Project] — Handover Complete

"Hi [Name],

As we wrap up the post-launch support period, I wanted to make sure you have everything you need.

**What's been delivered:**
- [Project] is live and running
- Handover documentation complete
- Training completed
- [X] support tickets resolved

**What happens next:**
- Support period ends on [date]
- After that, I'm available for new projects or a maintenance retainer
- System documentation is in [location]
- Credentials are in [password manager]

**To keep things running smoothly:**
- [Maintenance checklist]
- [Monitoring recommendations]
- [Who to contact for each service]

**Next steps (if interested):**
If you'd like to discuss ongoing maintenance or new features, let me know and we can schedule a call.

It's been a pleasure working on this project. If you're happy with the results, I'd appreciate a testimonial or LinkedIn recommendation.

Best,
[Your name]"

---

## The Handover Scorecard

### Self-Assessment

Rate each area after every project:

| Area | Score (1-5) | Notes |
|------|-------------|-------|
| Handover document completeness | | |
| Training effectiveness | | |
| Client independence | | |
| Support issue volume | | |
| Client satisfaction | | |
| Upsell conversation | | |
| Referral received | | |

**Target:** 4+ average

### Continuous Improvement

After each handover:
1. What went well?
2. What could be better?
3. What should I add to my handover template?
4. What should I add to my FAQ/documentation?

---

## The Million-Dollar Handover Mindset

The handover is not the end of the relationship. It's the beginning of the next phase.

A great handover makes the client feel confident, capable, and cared for. They don't feel abandoned — they feel equipped.

When you hand over well:
- They refer you without hesitation
- They hire you for the next project
- They sign a retainer for maintenance
- They become a case study that wins you more clients

Every handover is an investment in future revenue. Do it well. Do it thoroughly. Charge accordingly.
