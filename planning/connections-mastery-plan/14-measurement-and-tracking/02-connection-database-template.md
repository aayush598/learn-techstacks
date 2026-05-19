# Connection Database Template

## Ready-to-Use CRM Structure

### Google Sheets Template

**Create a new Google Sheet with these columns:**

```
Copy and paste this header row:

Full Name | Domain | Subdomain | Organization | Title | LinkedIn URL | Email | Phone | Location | Connection Level | Relationship Strength | How We Met | Date First Contacted | Last Contact Date | Next Action | Next Action Date | Value I Gave | Value They Gave | Notes | Mutual Connections | Priority | Status
```

### Notion Database Template

**To recreate in Notion:**

Create a new database. Add these properties:

**1. Name** (Title field)
**2. Domain** (Select)
Options: Politics, Tech, Finance, Healthcare, Legal, Military, Academia, Arts, Cybersecurity, Corporate, Foreign, Other

**3. Subdomain** (Select - varies by domain)
Example for Politics: Minister, Bureaucrat, Advisor, Campaign, Party Official, Local Gov
Example for Tech: Founder, CTO, Engineer, VC, Researcher, Community Leader

**4. Organization** (Text)
**5. Title** (Text)
**6. LinkedIn URL** (URL)
**7. Email** (Email)
**8. Phone** (Phone)
**9. Location** (Text)
**10. Connection Level** (Select)
Options: 1st - Direct, 2nd - Introduced, 3rd - Cold

**11. Relationship Strength** (Select)
Options: 1 - Weak, 2 - Casual, 3 - Moderate, 4 - Strong, 5 - Strategic

**12. How We Met** (Text)
e.g., "LinkedIn outreach", "Conference: TechSummit 2025", "Introduced by [Name]"

**13. Date First Contacted** (Date)
**14. Last Contact Date** (Date)
**15. Next Action** (Text)
e.g., "Send article about AI in healthcare", "Schedule coffee meeting"

**16. Next Action Date** (Date)
**17. Value I've Given** (Text)
Multiline. e.g., "- Introduced them to [Name]\n- Shared resource on [topic]"

**18. Value They've Given** (Text)
Multiline.

**19. Notes** (Text)
Multiline. e.g., "Has two kids. Interested in AI ethics. Mentioned wanting to connect with [Person]."

**20. Mutual Connections** (Relation)
Link to other entries in this database.

**21. Priority** (Select)
Options: A - High, B - Medium, C - Low

**22. Status** (Select)
Options: New, Contacted, Connected, Meeting Scheduled, Met, Nurturing, Dormant, Parked

### Views for Notion

**Create these views:**

**1. All Connections** — Table view, sorted by Last Contact Date descending
**2. Today's Actions** — Table, filter: Next Action Date = Today
**3. Needs Follow-Up** — Table, filter: Next Action Date < Today
**4. By Domain** — Board view, grouped by Domain
**5. Priority A** — Table, filter: Priority = A - High
**6. Dormant Connections** — Table, filter: Last Contact Date < 90 days ago, Status ≠ Dormant
**7. Recently Added** — Table, filter: Created in last 30 days

### CSV Import Template

If you want to import existing data:

```
Name,Domain,Organization,Title,LinkedIn,Email,Notes
John Smith,Tech,Google,CTO,https://linkedin.com/in/...,john@example.com,Met at conference
```

### Manual Entry Quick Form

For quick entry after events:

```
Name: ___
Domain: ___
Organization: ___
Title: ___
LinkedIn: ___
How We Met: ___
Notes: ___
Next Action: ___
Priority: ___
```

### Lifecycle Stage Definitions

| Stage | Definition | Next Action |
|-------|-----------|-------------|
| New | Just added, no contact yet | Send first message |
| Contacted | Sent outreach, awaiting response | Follow up in 5-7 days |
| Connected | They accepted/replied | Send value, suggest call |
| Meeting Scheduled | Call/meeting booked | Prepare, show up, follow up |
| Met | Had meaningful interaction | Log notes, send follow-up |
| Nurturing | Active relationship | Regular touchpoints |
| Dormant | No contact >90 days | Re-engage or archive |
| Parked | Multiple outreach attempts failed | Retry in 3 months |

### Database Maintenance Rules

1. **New entry within 24 hours** of meeting someone
2. **Last Contact updated** same day as interaction
3. **Next Action Date set** before closing any entry
4. **Notes updated** immediately after calls/meetings
5. **Dormant review** monthly
6. **Backup exported** monthly
