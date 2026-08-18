# Identifying Key Stakeholders in a Recommendation System Project

## Table of Contents

1. [Overview](#overview)
2. [Primary Stakeholders](#primary-stakeholders)
3. [Secondary Stakeholders](#secondary-stakeholders)
4. [Hidden Stakeholders](#hidden-stakeholders)
5. [RACI Matrix for Recommendation Projects](#raci-matrix)
6. [DACI Framework](#daci-framework)
7. [DRI Model](#dri-model)
8. [Cross-Functional Dependency Mapping](#cross-functional-dependency-mapping)
9. [Stakeholder Communication Cadences](#stakeholder-communication-cadences)
10. [Organizational Structures at FAANG](#organizational-structures-at-faang)

---

## Overview

A recommendation system is not a siloed ML project. It is a cross-cutting product capability that touches nearly every part of the organization. Unlike a standalone microservice or a backend API, a recommendation engine simultaneously requires coordination across product strategy, data engineering, machine learning, infrastructure, design, legal, and business operations.

Identifying the right stakeholders early is critical because:

- **Missed stakeholders** cause late-stage blockers, rework, and political friction.
- **Over-inclusion** causes decision paralysis, meeting fatigue, and diffusion of responsibility.
- **Wrong ownership** leads to misaligned incentives and suboptimal outcomes.
- **Ignored legal/privacy stakeholders** can result in regulatory violations, fines, and reputational damage.

The goal is to build a precise stakeholder map that captures every person or team whose work, budget, approval, or domain is impacted by the recommendation system.

---

## Primary Stakeholders

Primary stakeholders are those who have direct ownership, accountability, or decision rights over the recommendation system. They are actively involved in day-to-day execution and strategic direction.

### Product Manager (PM)

The product manager owns the "what" and "why" of the recommendation system. They define the product vision, prioritize features, align business goals with technical capabilities, and are accountable for adoption and impact metrics.

**Key responsibilities:**
- Defining the recommendation strategy and roadmap
- Translating business goals into product requirements
- Prioritizing features using frameworks like RICE, ICE, or WSJF
- Running A/B tests and interpreting results
- Coordinating with engineering on timelines and trade-offs
- Reporting on KPIs and OKRs to leadership
- Managing stakeholder expectations across the organization

**Why they matter for recommendations specifically:**
Product managers must understand that recommendation systems are probabilistic, not deterministic. They need to accept ambiguity in outcomes, understand that model improvements may take weeks to show statistical significance, and manage expectations around "it depends" answers from ML engineers.

### Engineering Manager / Tech Lead

The engineering manager or tech lead owns the technical execution, team structure, and system architecture. They make build-vs-buy decisions, set technical standards, and ensure the system is production-grade.

**Key responsibilities:**
- Designing the overall system architecture
- Making technology selection decisions (frameworks, databases, serving infrastructure)
- Managing the engineering team's capacity and sprint planning
- Setting coding standards, review processes, and deployment practices
- Ensuring system reliability, scalability, and maintainability
- Coordinating with ML engineers on model serving and feature pipelines
- Managing technical debt

### Machine Learning Engineer / Data Scientist

ML engineers and data scientists own the models, algorithms, and statistical methods that power recommendations. They are responsible for the core intelligence of the system.

**Key responsibilities:**
- Designing and implementing recommendation algorithms
- Building and maintaining feature engineering pipelines
- Training, evaluating, and tuning models
- Designing and analyzing A/B experiments
- Monitoring model performance and detecting drift
- Researching new techniques and staying current with the field
- Collaborating with data engineers on data quality and availability
- Documenting model assumptions, limitations, and intended behavior

### Data Engineer

Data engineers own the data infrastructure that feeds the recommendation system. Without reliable, timely, and clean data, no recommendation model can perform well.

**Key responsibilities:**
- Building and maintaining ETL/ELT pipelines
- Ensuring data quality, completeness, and freshness
- Designing and managing the data warehouse and data lake
- Building real-time streaming pipelines for user events
- Managing data schemas and evolution
- Ensuring data governance and lineage
- Optimizing query performance for feature retrieval
- Managing data storage costs

### UX/UI Designer

Designers own the presentation layer of recommendations — how they appear to users, how users interact with them, and how feedback is captured.

**Key responsibilities:**
- Designing recommendation UI components (carousels, grids, "why this" explanations)
- Conducting user research on recommendation preferences
- Designing feedback mechanisms (thumbs up/down, "not interested")
- Creating personalization settings interfaces
- Designing A/B test variants
- Ensuring accessibility of recommendation interfaces
- Balancing discoverability with clutter
- Designing cold-start experiences (onboarding, preference selection)

### Quality Assurance (QA) / Test Engineer

QA engineers ensure the recommendation system works correctly across all scenarios, edge cases, and platforms.

**Key responsibilities:**
- Writing and maintaining test suites for recommendation logic
- Testing recommendation quality (relevance, diversity, freshness)
- Performance and load testing
- Regression testing after model updates
- Testing A/B test infrastructure for correctness
- Cross-platform and cross-device testing
- Testing fallback and degradation scenarios
- Automated monitoring and alerting validation

---

## Secondary Stakeholders

Secondary stakeholders are not involved in day-to-day execution but have significant influence over or are significantly impacted by the recommendation system.

### Business Stakeholders

#### Revenue / Monetization Team
- Owns advertising revenue, subscription revenue, or commerce revenue
- Cares about recommendation-driven conversion rates, average order value, and revenue per user
- May have specific requirements for sponsored or promoted recommendations
- Needs dashboards and reporting on recommendation performance

#### Marketing / Growth Team
- Uses recommendations for email campaigns, push notifications, and re-engagement
- Needs access to user segments and preference data
- May require recommendation-driven content for landing pages
- Cares about recommendation impact on acquisition and retention metrics

#### Customer Support / Operations
- Handles user complaints about recommendation quality
- Needs tools to understand why specific recommendations were shown
- May need ability to manually adjust or override recommendations
- Provides qualitative feedback on user pain points

### Legal and Compliance

#### Legal Team
- Reviews terms of service related to data usage for personalization
- Ensures compliance with data protection regulations (GDPR, CCPA, etc.)
- Reviews consent mechanisms for data collection
- Advises on liability for recommendation outcomes
- Reviews contractual obligations with content providers

#### Privacy / Data Protection Officer (DPO)
- Ensures recommendation data collection follows privacy regulations
- Reviews data retention policies for user behavior data
- Validates consent mechanisms and opt-out flows
- Conducts Privacy Impact Assessments (PIAs)
- Reviews data sharing agreements with third parties
- Monitors for compliance with emerging regulations (AI Act, etc.)

### Executive Stakeholders

#### C-Suite (CEO, CTO, CPO)
- Sets strategic direction and budget
- Cares about competitive differentiation and market position
- Needs high-level reporting on recommendation impact
- Makes build-vs-buy decisions at the architectural level
- Sets AI/ML organizational strategy

#### VP of Engineering / VP of Product
- Owns the technical and product roadmap at the portfolio level
- Allocates resources across teams
- Resolves cross-team conflicts and priorities
- Sets quality and performance standards

### Content / Supply Side

#### Content Creators / Sellers
- Their content or products are the items being recommended
- Care about algorithmic fairness and exposure
- May have contractual requirements around placement
- Provide metadata and content quality signals
- May need dashboards showing recommendation performance of their items

#### Content Moderation Team
- Ensures recommended content meets community guidelines
- May need to suppress or de-rank certain content
- Handles edge cases where recommendations surface inappropriate content
- Provides signals for content quality models

---

## Hidden Stakeholders

Hidden stakeholders are those who are not immediately obvious but can significantly impact the project. Failing to identify them is one of the most common reasons for project delays and failures.

### Infrastructure / Platform Team
- Owns the Kubernetes clusters, cloud infrastructure, and deployment pipelines
- May have capacity constraints that affect model serving
- Has their own SLAs and on-call rotations
- Controls networking, load balancing, and CDN configurations
- May need advance notice for resource-intensive model training jobs

### Security Team
- Reviews the recommendation system for attack vectors (adversarial manipulation, data poisoning)
- Approves data access patterns and API authentication
- Reviews model serving endpoints for vulnerabilities
- Conducts penetration testing on recommendation interfaces
- May flag ML model reverse-engineering risks

### Finance Team
- Approves budgets for cloud compute, storage, and third-party services
- Needs cost projections for model training and serving at scale
- May require ROI justification for infrastructure investments
- Tracks cost per recommendation, cost per training run

### Procurement / Vendor Management
- Involved if using third-party recommendation services (Amazon Personalize, Google Recommendations AI, etc.)
- Manages vendor contracts and negotiations
- Ensures vendor compliance with security and privacy requirements

### International / Localization Team
- Ensures recommendations work across languages and cultures
- May have specific content requirements for different markets
- Needs to understand how language affects NLP-based recommendations
- Manages regional content licensing that affects recommendation availability

### Accessibility Team
- Ensures recommendation interfaces meet WCAG standards
- Reviews screen reader compatibility of recommendation carousels
- Tests keyboard navigation of recommendation flows
- Validates color contrast and visual design of recommendation components

### Data Science / Analytics Team
- Provides the analytical foundation for understanding user behavior
- Builds dashboards and reports that inform recommendation strategy
- Conducts deep-dive analyses on recommendation performance
- May have competing priorities for data infrastructure

---

## RACI Matrix

The RACI (Responsible, Accountable, Consulted, Informed) matrix defines roles for each activity in the recommendation system project.

| Activity | PM | Eng Lead | ML Eng | Data Eng | Designer | QA | Legal | Exec |
|---|---|---|---|---|---|---|---|---|
| Define recommendation strategy | A | C | C | I | C | I | C | A |
| Design system architecture | C | A/R | C | C | I | I | I | I |
| Select ML algorithms | C | C | A/R | C | I | I | I | I |
| Build data pipelines | I | C | C | A/R | I | I | I | I |
| Design recommendation UI | C | I | I | I | A/R | C | I | I |
| Write model evaluation code | I | I | A/R | C | I | C | I | I |
| Conduct A/B tests | A/R | C | C | I | C | C | I | I |
| Define data governance policies | C | I | I | C | I | I | A/R | I |
| Deploy models to production | I | A/R | R | C | I | C | I | I |
| Monitor model performance | I | C | A/R | C | I | C | I | I |
| Handle user data requests (GDPR) | C | C | C | R | I | I | A | I |
| Report on business impact | A/R | I | C | C | I | I | I | I |
| Manage vendor relationships | A | C | I | I | I | I | C | I |
| Conduct security reviews | I | C | I | I | I | I | I | A |
| Budget allocation | A | C | I | I | I | I | I | A |

**Legend:**
- **R** = Responsible (does the work)
- **A** = Accountable (owns the outcome, can veto)
- **C** = Consulted (must be consulted before a decision)
- **I** = Informed (must be notified of decisions/outcomes)

---

## DACI Framework

The DACI (Driver, Approver, Contributor, Informed) framework is particularly useful for recommendation systems where a single "driver" must be empowered to make fast decisions.

### Driver
The person who drives the work forward, gathers input, and makes recommendations. For a recommendation system, this is typically the ML Tech Lead or the PM depending on the workstream.

**Example drivers:**
- Model selection decisions → ML Tech Lead
- UI/UX decisions → Product Designer
- Infrastructure decisions → Platform Engineering Lead
- Data governance decisions → Data Governance Lead

### Approver
The single person who makes the final decision. Having multiple approvers creates bottlenecks.

**Example approvers:**
- Go/no-go for model deployment → VP of Engineering
- Feature prioritization → Product Director
- Privacy-related decisions → DPO
- Budget decisions → CFO

### Contributors
People who provide input and do the work but do not make final decisions.

### Informed
People who need to know the outcome but are not involved in the decision-making process.

---

## DRI Model

The Directly Responsible Individual (DRI) model, popularized by Apple, assigns a single person to be directly responsible for every deliverable.

**DRI assignments for a recommendation system:**

| Deliverable | DRI |
|---|---|
| Recommendation algorithm accuracy | ML Lead |
| Data pipeline reliability | Data Engineering Lead |
| Model serving latency | ML Infra Lead |
| Recommendation UI quality | Product Designer |
| A/B test results interpretation | Data Science Lead |
| System uptime (99.9%) | SRE Lead |
| User feedback collection | PM |
| Content catalog quality | Content Ops Lead |
| Privacy compliance | DPO |
| Cost optimization | Engineering Manager |

**Rules for DRI assignment:**
- Each deliverable has exactly one DRI
- The DRI has full authority and full responsibility
- The DRI does not need to do all the work but must ensure it gets done
- DRIs are public and known to the entire team
- DRIs are reassessed quarterly as the project evolves

---

## Cross-Functional Dependency Mapping

Recommendation systems have deep cross-functional dependencies that must be explicitly mapped and managed.

### Data Dependencies

```
Content Catalog (Content Ops) 
    → Item Metadata (Data Eng)
    → Feature Store (ML Eng)
    → Model Training (ML Eng)
    → Model Registry (ML Infra)
    → Model Serving (ML Infra)
    → Recommendation API (Backend Eng)
    → UI Rendering (Frontend Eng)
```

```
User Events (Frontend/Backend)
    → Event Stream (Data Eng)
    → Real-time Features (ML Eng)
    → Batch Features (Data Eng)
    → Training Data (ML Eng)
    → Model Evaluation (ML Eng)
    → A/B Test Analysis (Data Science)
```

### Operational Dependencies

- **ML model deployment** depends on infrastructure capacity approval
- **A/B test launches** depend on traffic allocation from the platform team
- **Data pipeline changes** depend on schema review from data governance
- **UI changes** depend on design review and accessibility audit
- **Feature launches** depend on legal review for new data usage
- **Model retraining** depends on fresh training data availability
- **Performance optimization** depends on profiling data from monitoring

### Communication Dependencies

- **Model performance reports** must flow to product, business, and executives
- **A/B test results** must be communicated to product, design, and business
- **Incident reports** must be communicated to engineering, product, and customer support
- **Privacy incidents** must be communicated to legal, DPO, and executives
- **User feedback** must flow from support to product to ML teams

---

## Stakeholder Communication Cadences

### Daily
- **ML engineering standup**: Model training status, pipeline health, feature pipeline issues
- **Data engineering standup**: Pipeline health, data quality issues, infrastructure capacity
- **On-call rotation handoff**: System health, incidents, model performance anomalies

### Weekly
- **Product-ML sync**: Feature progress, A/B test updates, prioritization changes
- **Recommendation quality review**: Model metrics, user feedback trends, quality issues
- **Stakeholder office hours**: Open slot for any stakeholder to raise concerns or questions
- **Cross-team dependency review**: Unblock blocked work, renegotiate timelines

### Bi-weekly
- **Sprint review/demo**: Show completed work to all stakeholders
- **A/B test review board**: Review experiment results and go/no-go decisions
- **Model governance review**: Review model changes, versioning, rollback procedures

### Monthly
- **Executive business review**: High-level metrics, ROI, strategic alignment
- **Privacy and compliance review**: Data usage audit, regulatory updates
- **Technical architecture review**: System design evolution, capacity planning
- **User research debrief**: New insights about user behavior and preferences

### Quarterly
- **OKR review and planning**: Assess progress, set new objectives
- **Roadmap review**: Reprioritize features based on learnings
- **Technology radar review**: Evaluate new tools, frameworks, and techniques
- **Vendor review**: Assess third-party service performance and costs

### Ad-hoc
- **Incident response communication**: As needed during production incidents
- **Model emergency rollback**: When a deployed model causes harm
- **Regulatory inquiry response**: When legal/compliance needs information
- **Competitive response**: When a competitor launches a significant feature

---

## Organizational Structures at FAANG

### Netflix

Netflix organizes recommendation teams around specific product experiences:

- **Home Page Team**: Owns the row ordering, thumbnail selection, and personalization of the home page
- **Search & Discovery Team**: Owns search results and browse experience personalization
- **Content Selection Team**: Owns the recommendation algorithms and models
- **Machine Learning Platform Team**: Owns the ML infrastructure (Metaflow, training, serving)
- **Data Science Team**: Owns experimentation and causal inference

**Key insight**: Netflix separates the "what to recommend" (algorithms) from "how to present it" (product/UI) into separate teams with shared goals.

### Spotify

Spotify uses a squad-based model:

- **Recommendation Squads** (within tribes): Cross-functional teams of 6-8 people (PM, engineers, data scientists, designer)
- **Machine Learning Platform**: Central team providing infrastructure
- **Personalization Team**: Owns cross-product personalization strategy
- **Creator tools team**: Manages the supply-side of recommendations

**Key insight**: Spotify's squad model gives each recommendation surface (Discover Weekly, Release Radar, Daily Mix) its own dedicated cross-functional team.

### Amazon

Amazon uses a "two-pizza team" model:

- **Recommendation Algorithm Team**: Owns the core recommendation models
- **Front-end Personalization Team**: Owns the recommendation UI and presentation
- **Data Engineering Team**: Owns the data pipelines and feature stores
- **Applied Science Team**: Owns research and advanced prototyping
- **Product Manager**: Coordinates across teams

**Key insight**: Amazon's teams are small enough to be fed by two pizzas (6-8 people), with clear ownership boundaries and well-defined APIs between teams.

### Meta (Facebook)

Meta organizes around specific surfaces and surfaces:

- **News Feed Ranking Team**: Owns feed recommendations
- **Recommendations Team**: Owns "People You May Know," "Groups to Join," etc.
- **ML Platform Team**: Owns PyTorch-based training and serving infrastructure
- **Ads Ranking Team**: Owns ad recommendations (separate from organic)
- **Integrity Team**: Owns recommendation safety and content policy

**Key insight**: Meta separates organic recommendations from ads recommendations and has dedicated integrity teams to prevent harmful recommendations.

### Google / YouTube

Google uses a layered organizational model:

- **Recommendation Systems Team**: Owns core algorithms
- **User Understanding Team**: Owns user modeling and preferences
- **Content Understanding Team**: Owns item-side features and signals
- **Ranking Infrastructure Team**: Owns the serving infrastructure
- **Trust & Safety Team**: Owns content policy enforcement in recommendations

**Key insight**: Google separates user understanding from content understanding, allowing each team to specialize deeply in their domain.

---

## Best Practices for Stakeholder Management

### Start with a Stakeholder Register

Maintain a living document with:
- Name and role
- Interest level (High/Medium/Low)
- Influence level (High/Medium/Low)
- Current sentiment (Supportive/Neutral/Resistant)
- Communication preferences
- Key concerns or motivations
- Last contact date

### Use the Power-Interest Grid

| | Low Interest | High Interest |
|---|---|---|
| **High Power** | Keep Satisfied | Manage Closely |
| **Low Power** | Monitor | Keep Informed |

### Manage Resistant Stakeholders

1. **Understand their concerns**: Listen before trying to convince
2. **Find common ground**: Align on shared goals
3. **Address concerns directly**: Don't avoid difficult conversations
4. **Involve them early**: Give them a voice in the process
5. **Show, don't tell**: Use demos and data to demonstrate value
6. **Escalate when needed**: Don't let resistance become a blocker

### Avoid Common Pitfalls

- **Don't confuse stakeholders with users**: They have different needs
- **Don't treat all stakeholders equally**: Use the power-interest grid
- **Don't ignore the quiet stakeholders**: They may have the most influence
- **Don't forget the ops team**: They'll be supporting the system after launch
- **Don't skip legal/privacy**: Early engagement prevents late-stage blockers
- **Don't assume alignment**: Explicitly confirm understanding and agreement
