# ISO 13485 Quality Management System

## Overview

ISO 13485 is the international standard specifying requirements for a quality management system (QMS) where an organization needs to demonstrate its ability to provide medical devices and related services that consistently meet customer and applicable regulatory requirements. For the iPACE-CHIP, ISO 13485 compliance is not optional — it is a regulatory prerequisite for market access in the European Union (CE marking under MDR), and is recognized by the FDA as harmonized with 21 CFR 820. This document details how the iPACE-CHIP development and manufacturing organization implements ISO 13485 across all phases.

---

## 1. Scope and Application

### 1.1 Scope Statement

```
Scope: The design, development, manufacturing, testing, and servicing 
of the iPACE-CHIP implantable pacemaker controller integrated circuit 
and related firmware, including:
  - Silicon wafer fabrication (outsourced, QMS-supervised)
  - Package assembly (outsourced, QMS-supervised)
  - Final test and calibration
  - Firmware development and validation
  - Field failure analysis
  - Post-market surveillance

Excluded clauses:
  - 8.5.1 (Customer property): No customer-furnished components
  - 7.5.5 (Particular requirements for sterile devices): 
    Device is not directly sterilized; sterile packaging applied 
    at system assembly level
```

### 1.2 Regulatory Context

| Regulation | Applicability | Relationship to ISO 13485 |
|-----------|--------------|--------------------------|
| EU MDR 2017/745 | Class III implantable | ISO 13485 is harmonized standard |
| FDA 21 CFR 820 | Class III PMA device | ISO 13485 aligned with CGMP |
| TGA (Australia) | Class AIMD | Recognizes ISO 13485 certification |
| Health Canada | Class IV | Recognizes ISO 13485 certification |
| MDSAP | Multi-jurisdiction | ISO 13485-based audit program |

---

## 2. Quality Management System Structure

### 2.1 Documentation Hierarchy

```
Level 1: Quality Manual
├── Quality policy and objectives
├── Scope of QMS
├── Exclusions with justification
├── Reference to documented procedures
└── Description of process interactions

Level 2: Standard Operating Procedures (SOPs)
├── Document control (SOP-001)
├── Record control (SOP-002)
├── Management responsibility (SOP-003)
├── Resource management (SOP-004)
├── Design and development (SOP-005)
├── Purchasing control (SOP-006)
├── Production control (SOP-007)
├── Corrective/preventive action (SOP-008)
├── Internal audit (SOP-009)
└── Risk management (SOP-010)

Level 3: Work Instructions
├── Test procedures (WI-TEST-001 through WI-TEST-050)
├── Calibration procedures (WI-CAL-001 through WI-CAL-020)
├── Handling procedures (WI-HANDLE-001 through WI-HANDLE-010)
└── Environmental controls (WI-ENV-001 through WI-ENV-005)

Level 4: Forms, Records, and Templates
├── Test data collection forms
├── Deviation/NCR forms
├── CAPA forms
├── Audit checklists
├── Training records
└── Supplier qualification records
```

### 2.2 Document Control

```
Document Control Requirements:
  Unique identification for all documents
  Version control with change history
  Review and approval authority defined
  Distribution control (controlled copies)
  Obsolete document prevention
  Change review process
  
Document Lifecycle:
  Draft -> Review -> Approve -> Release -> Implement -> Review -> Update
  
Review Cycle:
  Quality Manual: Annual
  SOPs: Every 2 years (or upon significant change)
  Work Instructions: Every 3 years
  Forms: Every 5 years
```

### 2.3 Record Control

```
Record Retention Requirements (iPACE-CHIP):
  Design history file: 15 years beyond product discontinuation
  Device master record: 15 years beyond product discontinuation
  Device history record: 15 years beyond product discontinuation
  Complaint records: 15 years beyond product discontinuation
  CAPA records: 15 years beyond product discontinuation
  Audit records: 10 years
  Training records: Duration of employment + 5 years
  Calibration records: 10 years
  
Record Storage:
  Electronic: Redundant backup, daily
  Physical: Secure archive, fireproof cabinet
  Access control: Role-based permissions
  Integrity: Electronic signatures, audit trail
```

---

## 3. Management Responsibility

### 3.1 Management Commitment

```
Management commitments for iPACE-CHIP QMS:
  1. Communicate importance of meeting regulatory requirements
  2. Establish and maintain quality policy
  3. Ensure quality objectives are established
  4. Conduct management reviews
  5. Ensure resource availability
  6. Ensure customer requirements are met
  7. Promote continual improvement
```

### 3.2 Management Review

```
Management Review Frequency: Quarterly (minimum)
Additional reviews: After significant nonconformances or CAPAs

Inputs:
  - Audit results (internal and external)
  - Customer feedback and complaints
  - Process performance and product conformity data
  - CAPA status
  - Follow-up actions from previous reviews
  - Changes that could affect the QMS
  - Recommendations for improvement
  - New regulatory requirements

Outputs:
  - Improvement actions
  - QMS modification needs
  - Resource requirements
  - Risk assessment updates
  - Quality objectives revision
```

### 3.3 Quality Policy

```
iPACE-CHIP Quality Policy:
  "To design and manufacture the highest quality implantable 
   pacemaker controller IC, ensuring patient safety through 
   rigorous quality management, zero-defect manufacturing, 
   and continuous improvement, in full compliance with all 
   applicable regulatory requirements."
   
  Signed: [CEO Name]
  Date: [Date]
  Review: Annual (next review: [Date])
```

---

## 4. Resource Management

### 4.1 Human Resources

```
Competency Requirements:
  Design engineers: ISO 14971 training, IEC 62304 training
  Test engineers: DFT, ATE operation, medical device testing
  Quality engineers: ISO 13485 auditor training, CAPA methodology
  Manufacturing: IPC certification, ESD handling, cleanroom protocols
  Management: ISO 13485 management representative training

Training Program:
  New hire orientation: QMS overview, quality policy
  Role-specific training: Job function SOPs
  Regulatory training: Annual update on regulatory changes
  GMP training: Annual CGMP refresher
  On-the-job training: Documented competency verification
  
Training Records:
  Training matrix maintained for all personnel
  Competency assessment after each training event
  Retraining required upon significant process change
  Annual competency review for all staff
```

### 4.2 Infrastructure

```
Infrastructure requirements for iPACE-CHIP QMS:
  Facilities:
    Cleanroom (Class 10,000) for wafer handling
    ESD-safe areas for device handling
    Climate-controlled test laboratories
    Secure document storage
    
  Equipment:
    Calibrated test equipment (annual calibration)
    ATE systems with preventive maintenance
    Environmental monitoring systems
    Data backup and recovery systems
    
  IT Systems:
    QMS document management system (e.g., MasterControl)
    CAPA tracking system
    ERP/MES system for production tracking
    Quality data analytics platform
```

---

## 5. Design and Development

### 5.1 Design Control

The iPACE-CHIP design control process follows a V-model:

```
Design Phases:
  Phase 1: Design Input
    ├── User needs and intended use
    ├── Regulatory requirements
    ├── Risk management plan
    ├── Design input specification
    └── Review: Formal design input review

  Phase 2: Architectural Design
    ├── System architecture
    ├── Block diagram
    ├── Interface specification
    └── Review: Architecture review

  Phase 3: Detailed Design
    ├── RTL design (VHDL/Verilog)
    ├── Physical design (layout)
    ├── Package design
    └── Review: Design reviews at each milestone

  Phase 4: Verification
    ├── Simulation
    ├── Fabrication
    ├── Testing (wafer sort, final test)
    └── Review: Verification review

  Phase 5: Validation
    ├── System-level testing
    ├── Biocompatibility testing
    ├── Clinical evaluation
    └── Review: Validation review

  Phase 6: Transfer
    ├── Manufacturing process qualification
    ├── Test transfer to production
    └── Review: Transfer review
```

### 5.2 Design History File (DHF)

```
DHF Contents for iPACE-CHIP:
  Design input documentation
    ├── User needs document
    ├── Intended use statement
    ├── Regulatory requirements list
    └── Risk analysis (ISO 14971)

  Design output documentation
    ├── IC specification document
    ├── Circuit schematics
    ├── Layout database
    ├── Package specification
    └── Test plan and procedures

  Design review records
    ├── Concept review minutes
    ├── Architecture review minutes
    ├── Detailed design review minutes
    └── Verification review minutes

  Verification records
    ├── Simulation results
    ├── DFT analysis reports
    ├── Wafer sort data
    ├── Final test data
    └── Failure analysis reports

  Validation records
    ├── System-level test results
    ├── Biocompatibility test reports
    └── Clinical evaluation report

  Design transfer records
    ├── Manufacturing process validation
    ├── Test program validation
    └── Production qualification data
```

---

## 6. Purchasing and Supplier Control

### 6.1 Supplier Qualification

```
Supplier qualification process for iPACE-CHIP:
  Step 1: Supplier assessment
    ├── QMS certification (ISO 9001/ISO 13485)
    ├── Financial stability assessment
    ├── Technical capability assessment
    ├── Regulatory compliance history
    └── Reference checks

  Step 2: On-site audit
    ├── Process audit
    ├── Quality system audit
    ├── Capacity assessment
    └── Environmental assessment

  Step 3: Qualification lot
    ├── First article inspection
    ├── Process capability study (Cpk > 1.33)
    ├── Reliability qualification
    └── Documentation review

  Step 4: Approval
    ├── Approved Supplier List (ASL) entry
    ├── Quality agreement signed
    ├── Monitoring plan established
    └── Annual re-evaluation scheduled

Critical suppliers for iPACE-CHIP:
  Wafer fab: Qualified, ISO 9001 certified, annual audit
  Assembly: Qualified, ISO 13485 certified, annual audit
  Test equipment: Qualified, ISO 17025 calibration
  Raw materials: Qualified per material specification
```

### 6.2 Incoming Inspection

```
Incoming inspection for iPACE-CHIP components:
  Wafer lots:
    ├── Visual inspection of wafer (sample)
    ├── Wafer sort data review
    ├── Electrical continuity check
    └── Package integrity (sample)

  Raw materials:
    ├── Certificate of Conformance (CoC) review
    ├── Material certification verification
    ├── Sample inspection per lot
    └── Shelf life verification

  Test equipment:
    ├── Calibration certificate verification
    ├── Functional verification
    └── Measurement uncertainty review
```

---

## 7. Production Control

### 7.1 Production Process Control

```
iPACE-CHIP production control:
  Process validation:
    ├── IQ (Installation Qualification) for all test equipment
    ├── OQ (Operational Qualification) for test programs
    ├── PQ (Performance Qualification) for production lots
    └── Revalidation upon significant changes

  In-process controls:
    ├── Statistical process control (SPC) on critical parameters
    ├── First article inspection at lot start
    ├── SPC monitoring during production
    └── End-of-lot verification

  Environmental controls:
    ├── Temperature: 22 +/- 2 deg-C
    ├── Humidity: 45 +/- 10% RH
    ├── ESD: Class 0 (>2000V HBM) handling
    └── Particulate: Class 10,000 cleanroom
```

### 7.2 Traceability

```
Traceability requirements:
  Wafer level:
    ├── Wafer ID (engraved on each wafer)
    ├── Fab lot number
    ├── Process recipe and parameters
    ├── Date of fabrication
    └── Test results (wafer sort)

  Assembly level:
    ├── Assembly lot number
    ├── Package type
    ├── Date of assembly
    ├── Bond wire material lot
    └── Mold compound lot

  Final test level:
    ├── Test date and ATE serial number
    ├── Test program version
    ├── Complete parametric data
    ├── Grade/bin assignment
    └── Operator ID

  Serial number:
    ├── Unique per device
    ├── Laser marked on package
    ├── Barcode format (Data Matrix)
    └── Linked to all test data in database
```

---

## 8. Corrective and Preventive Action (CAPA)

### 8.1 CAPA Process

```
CAPA workflow for iPACE-CHIP:
  Trigger:
    ├── Customer complaint
    ├── Internal nonconformance
    ├── Audit finding
    ├── Trend analysis
    └── Regulatory feedback

  Investigation:
    ├── Root cause analysis (5-Why, Ishikawa)
    ├── Scope assessment (isolated vs. systemic)
    ├── Risk assessment of nonconformance
    └── Interim containment action (if needed)

  Action:
    ├── Corrective action (eliminate root cause)
    ├── Preventive action (prevent recurrence)
    ├── Implementation plan with responsibilities
    └── Timeline for completion

  Verification:
    ├── Effectiveness check (30/60/90 days)
    ├── Document changes required
    ├── Training updates required
    └── Closure with quality approval
```

### 8.2 Complaint Handling

```
Complaint handling process:
  Receipt:
    ├── Log complaint within 24 hours
    ├── Assign severity classification
    └── Notify regulatory if required

  Investigation:
    ├── Technical investigation (engineering)
    ├── Risk assessment (quality)
    ├── Regulatory impact assessment
    └── Customer communication

  Resolution:
    ├── Root cause identification
    ├── CAPA initiation (if warranted)
    ├── Customer response (within 30 days)
    └── Regulatory filing (if required)

  Reporting:
    ├── Medical device reporting (MDR) to FDA if serious
    ├── Vigilance reporting to EU Notified Body
    └── Trend reporting (annual)
```

---

## 9. Internal Audit

### 9.1 Audit Program

```
Audit schedule for iPACE-CHIP QMS:
  Full system audit: Annual
  Process audits: Semi-annual
  Supplier audits: Annual (critical), biennial (non-critical)
  Product audits: Quarterly (on production lots)
  
Audit team:
  Lead auditor: ISO 13485 certified
  Internal auditors: Trained per ISO 19011
  Technical auditors: Subject matter experts
  Independence: Auditors cannot audit their own work
```

### 9.2 Audit Findings and Follow-Up

```
Finding classification:
  Major nonconformance: QMS failure or systemic issue
    └── Response required within 30 days
    └── Verification audit within 90 days
    
  Minor nonconformance: Isolated deviation
    └── Response required within 60 days
    └── Verification at next audit
    
  Observation: Opportunity for improvement
    └── No formal response required
    └── Consider for continual improvement
```

---

## 10. Monitoring and Measurement

### 10.1 Customer Satisfaction

```
Customer satisfaction monitoring:
  Complaint rate: Less than 1 per 100,000 devices
  Return rate: Less than 0.1%
  Customer surveys: Annual
  Advisory board feedback: Quarterly
  Field performance data: Continuous (post-market)
```

### 10.2 Process Performance

```
Key performance indicators:
  Yield: First-pass yield greater than 94%
  Test coverage: Greater than 99% stuck-at
  CAPA closure: Greater than 90% on time
  Audit findings: Zero major findings
  Training compliance: 100% current
  Supplier quality: Less than 500 DPM
```

### 10.3 Product Quality Metrics

```
Product quality metrics:
  Defective parts per million (DPPM): Less than 1
  Early life failure rate (ELFR): Less than 50 FIT
  Customer complaints: Less than 1 per 100K units
  Warranty claims: Less than 0.01%
  Regulatory actions: Zero
```

---

## 11. Continual Improvement

### 11.1 Improvement Methodology

```
Improvement process:
  Data collection:
    ├── SPC data analysis
    ├── Customer complaint trends
    ├── Internal nonconformance trends
    ├── Audit finding trends
    └── Supplier quality trends

  Analysis:
    ├── Pareto analysis of issues
    ├── Root cause analysis
    ├── Cost of quality analysis
    └── Risk-benefit analysis

  Action:
    ├── Improvement project initiation
    ├── Resource allocation
    ├── Implementation and verification
    └── Standardization of improvements
```

### 11.2 Cost of Quality

```
Cost of quality categories for iPACE-CHIP:
  Prevention costs:
    ├── Training
    ├── Quality planning
    ├── Design reviews
    └── Supplier qualification

  Appraisal costs:
    ├── Testing (wafer sort, final test)
    ├── Inspection
    ├── Calibration
    └── Auditing

  Internal failure costs:
    ├── Scrap (failed die, failed devices)
    ├── Rework (limited for IC products)
    ├── Yield loss
    └── Failure analysis

  External failure costs:
    ├── Warranty claims
    ├── Complaint handling
    ├── Product recalls
    └── Regulatory actions

Target: Prevention and appraisal costs at 15-20% of revenue
        Internal failure costs less than 5% of revenue
        External failure costs less than 0.1% of revenue
```

---

## 12. Summary

ISO 13485 provides the structured quality management framework that governs every aspect of iPACE-CHIP development, manufacturing, and post-market support. The comprehensive QMS ensures regulatory compliance across global markets, provides the foundation for consistent product quality, and supports the zero-defect manufacturing objective required for implantable medical devices. Through rigorous document control, design controls, supplier management, CAPA processes, and continual improvement, the QMS delivers the quality assurance necessary to protect patient safety.

---

## References

- ISO 13485:2016: Medical Devices - Quality Management Systems
- ISO 14971:2019: Application of Risk Management to Medical Devices
- IEC 62304:2006+A1:2015: Medical Device Software - Software Life Cycle
- EU MDR 2017/745: Medical Device Regulation
- FDA 21 CFR 820: Quality System Regulation
- ISO 19011:2018: Guidelines for Auditing Management Systems
- ICH Q10: Pharmaceutical Quality System
- MDSAP Audit Model: Medical Device Single Audit Program
