# Patient Selection Criteria for Pacemaker Implantation

## 1. Introduction

Selecting the appropriate patient for permanent pacemaker implantation is a multifaceted clinical decision that extends far beyond confirming a bradyarrhythmia on ECG. It requires a comprehensive evaluation of the patient's symptoms, their correlation with documented rhythm disturbances, assessment of comorbidities that may affect outcomes, evaluation of anatomical considerations, review of medications that may contribute to bradycardia, assessment of life expectancy and quality of life goals, and shared decision-making with the patient. For the developer of the iPACE-CHIP, understanding patient selection criteria provides insight into the diverse clinical scenarios the device must accommodate and the performance specifications it must meet.

---

## 2. Pre-Implantation Patient Evaluation

### 2.1 Clinical History

A thorough clinical history is the foundation of patient selection:

**Symptoms to evaluate**:

| Symptom | Description | Relevance |
|---------|-------------|-----------|
| **Syncope** | Transient loss of consciousness with loss of postural tone | Cardinal symptom of hemodynamically significant bradycardia |
| **Presyncope** | Near-fainting, dizziness, lightheadedness | May be more common than frank syncope |
| **Fatigue** | Excessive tiredness, reduced energy | Common in bradycardia and chronotropic incompetence |
| **Dyspnea on exertion** | Shortness of breath during physical activity | May indicate reduced cardiac output from bradycardia |
| **Exercise intolerance** | Inability to perform usual physical activities | Often due to chronotropic incompetence |
| **Cognitive impairment** | Confusion, memory problems | May result from reduced cerebral perfusion |
| **Palpitations** | Awareness of irregular heartbeat | May indicate tachyarrhythmias or PVCs |
| **Chest pain** | May occur with very slow rates and increased myocardial oxygen demand | Less common but possible |

**Critical question**: Is there a **temporal correlation** between the symptom and a documented rhythm disturbance? This is the single most important determinant of whether a pacemaker will benefit the patient.

### 2.2 Diagnostic Workup

#### 2.2.1 Electrocardiography (12-Lead ECG)

| Finding | Assessment |
|---------|-----------|
| Sinus rate | Document resting heart rate |
| P wave morphology | Assess atrial rhythm and conduction |
| PR interval | Evaluate for AV conduction disease |
| QRS duration | Assess for bundle branch block |
| QT interval | Evaluate for QT prolongation |
| ST-T changes | Assess for ischemia |
| Paced vs. intrinsic rhythm | Document current state |

#### 2.2.2 Ambulatory ECG Monitoring (Holter)

| Duration | Application |
|----------|------------|
| **24-hour** | Short-term rhythm assessment; may miss infrequent events |
| **48–72 hours** | Extended monitoring for more sensitive detection |
| **7–14 days** | Patch monitors (e.g., Zio Patch, SEEQ Mobile Cardiac Outpatient Telemetry) |
| **30 days** | Extended continuous monitoring |
| **Implantable loop recorder** | 1–3 years of continuous monitoring; for highly selected cases |

**Monitoring indications**:
- In patients with syncope, ≥ 24-hour Holter monitoring is recommended (Class I)
- Loop recorders recommended when syncope is unexplained after initial workup
- Useful for documenting intermittent bradycardia, tachycardia, and conduction disturbances

#### 2.2.3 Electrophysiological Study (EPS)

**Indications for EPS in the evaluation of bradycardia**:
- Syncope of uncertain etiology with suspected conduction disease
- Bifascicular block with unexplained syncope
- Assessment of HV interval (prolonged > 100 ms indicates high risk of progression to complete heart block)
- Provocation testing for tachyarrhythmias

**EPS parameters relevant to pacing decisions**:

| Parameter | Normal | Abnormal | Significance |
|-----------|--------|----------|-------------|
| **AH interval** | 50–120 ms | > 120 ms | AV nodal conduction delay |
| **HV interval** | 35–55 ms | > 55 ms (prolonged); > 100 ms (severe) | His-Purkinje disease; > 100 ms → pacing indicated |
| **Wenckebach cycle length** | 330–500 ms | < 330 ms | AV nodal function |
| **Sinoatrial conduction time** | 35–120 ms | > 120 ms | SA node conduction |
| **Corrected sinus node recovery time** | < 525 ms | > 525 ms | SA node automaticity |

#### 2.2.4 Echocardiography

**Purpose**: Assess cardiac structure and function to:
- Evaluate left ventricular ejection fraction (LVEF) — relevant for CRT decision-making
- Detect structural heart disease (valvular disease, cardiomyopathy)
- Assess chamber sizes (relevant for atrial lead placement)
- Rule out pericardial effusion before implantation

#### 2.2.5 Blood Tests

| Test | Purpose |
|------|---------|
| **Complete blood count** | Rule out anemia (can exacerbate bradycardia symptoms) |
| **Thyroid function tests (TSH, free T4)** | Hypothyroidism causes bradycardia |
| **Basic metabolic panel** | Electrolyte abnormalities (hyperkalemia can cause conduction disease) |
| **Coagulation studies** | Baseline before implantation; assess bleeding risk |
| **Renal function** | Important for MRI-conditional considerations and drug dosing |

---

## 3. Contraindications to Pacemaker Implantation

### 3.1 Absolute Contraindications

| Contraindication | Rationale |
|-----------------|-----------|
| **Active systemic infection** | Risk of device infection; defer until infection resolved |
| **Active endocarditis** | Risk of seeding the device; defer until treated |
| **Unresolved bacteremia** | Transient bacteremia may seed the device |
| **Patient refusal (competent)** | Informed consent is mandatory |
| **Life expectancy < 6 months** | Pacemaker unlikely to improve quality of remaining life |
| **No identifiable indication for pacing** | Risk-benefit ratio unfavorable |

### 3.2 Relative Contraindications

| Contraindication | Rationale | Management |
|-----------------|-----------|-----------|
| **Severe coagulopathy** | Risk of pocket hematoma | Correct coagulopathy before implantation |
| **Therapeutic anticoagulation (INR > 2.0)** | Increased bleeding risk | Consider bridging or deferring if possible |
| **Active skin infection over implant site** | Risk of wound infection | Treat infection first |
| **Severe tricuspid regurgitation** | Lead crossing tricuspid valve may worsen; risk of lead entanglement | Consider leadless pacing; careful risk-benefit assessment |
| **Obstructive inferior vena cava thrombosis** | Cannot pass lead through IVC | Consider alternative venous access or leadless pacing |
| **Mechanical tricuspid valve** | Lead may interfere with valve function; risk of thrombosis | Consider epicardial leads or leadless pacing |
| **Severe pectus excavatum** | Anatomic distortion may complicate implantation | May still be possible with expertise |

---

## 4. Medications and Drug-Induced Bradycardia

### 4.1 Common Medications Causing Bradycardia

| Drug Class | Examples | Mechanism |
|-----------|---------|-----------|
| **Beta-blockers** | Metoprolol, atenolol, bisoprolol, carvedilol | β1-adrenergic blockade; ↓SA node automaticity; ↓AV conduction |
| **Calcium channel blockers (non-dihydropyridine)** | Verapamil, diltiazem | ↓AV conduction (Ca²⁺-dependent) |
| **Digoxin** | Digoxin | ↑Vagal tone; ↓AV conduction |
| **Amiodarone** | Amiodarone | Multi-channel blockade; ↓SA node, ↓AV node conduction |
| **Ivabradine** | Ivabradine | Selective If blockade; ↓SA node automaticity |
| **Cholinesterase inhibitors** | Donepezil, rivastigmine | ↑Acetylcholine; ↓SA node rate |
| **SSRIs/SNRIs** | Fluoxetine, venlafaxine | Sympatholytic effects |
| **Opioids** | Morphine, fentanyl, methadone | Vagal stimulation; ↓sympathetic tone |
| **Antipsychotics** | Haloperidol, quetiapine | Na⁺ channel blockade; ↓SA node conduction |
| **Clonidine** | Clonidine | Central α2-adrenergic agonist; ↓sympathetic outflow |
| **Theophylline (at high doses)** | Theophylline | Paradoxically can cause bradycardia |

### 4.2 Management Algorithm

```
Drug-induced bradycardia identified
    │
    ├── Can the offending drug be discontinued or dose reduced?
    │       │
    │       ├── YES → Discontinue/reduce; observe for resolution
    │       │         │
    │       │         ├── Resolves → No pacemaker needed
    │       │         └── Does not resolve → Consider pacemaker
    │       │
    │       └── NO (drug essential for life-threatening condition)
    │               │
    │               └── Is there an alternative drug?
    │                       │
    │                       ├── YES → Try alternative
    │                       └── NO → Pacemaker implantation indicated
    │                                  (allows continuation of essential drug)
```

---

## 5. Age-Related Considerations

### 5.1 Pediatric Patients

| Consideration | Detail |
|--------------|--------|
| **Minimum body size** | Device must be appropriate for patient's body habitus |
| **Growth considerations** | Lead length must accommodate growth; looped leads may be needed |
| **Anesthetic risk** | General anesthesia usually required (higher risk in neonates/infants) |
| **Venous access** | May be limited in small patients |
| **Device longevity** | More replacements over lifetime; minimizing implantations is important |
| **Developmental considerations** | Impact of device on physical activity, sports participation |

### 5.2 Adult Patients

| Age Group | Considerations |
|-----------|---------------|
| **Young adults (18–40)** | Long device longevity critical; activity level considerations; reproductive counseling (MRI compatibility) |
| **Middle-aged (40–65)** | Balancing device benefits with comorbidities; occupational considerations |
| **Elderly (> 65)** | Higher prevalence of comorbidities; frailty assessment; cognitive status; fall risk; life expectancy considerations |

### 5.3 Very Elderly Patients (> 80 Years)

| Factor | Consideration |
|--------|--------------|
| **Frailty** | Frailty index affects procedural risk and recovery |
| **Cognitive status** | Dementia may limit ability to participate in decision-making |
| **Comorbidity burden** | Multiple comorbidities may limit benefit |
| **Life expectancy** | Estimated life expectancy should exceed device benefit timeline |
| **Polypharmacy** | Multiple medications may contribute to bradycardia |
| **Patient preferences** | Goals of care may prioritize comfort over longevity |

**Evidence**: Studies show that even patients aged ≥ 80–90 years benefit from pacemaker implantation with acceptable complication rates, but careful patient selection is important.

---

## 6. Comorbidity Assessment

### 6.1 Cardiac Comorbidities

| Comorbidity | Impact on Pacing Decision |
|------------|--------------------------|
| **Heart failure (HFrEF)** | May need CRT instead of standard pacing; optimize LV pacing site |
| **Heart failure (HFpEF)** | Consider AV optimization; avoid unnecessary RV pacing |
| **Atrial fibrillation** | May need AV node ablation + VVIR pacing; rate control considerations |
| **Valvular heart disease** | Mechanical valve affects lead placement; TR affects lead crossing |
| **Hypertrophic cardiomyopathy** | May benefit from DDD pacing with short AV delay |
| **Prior cardiac surgery** | Leads may be difficult to place; consider epicardial approach |
| **Congenital heart disease** | Anatomy may preclude standard transvenous approach |

### 6.2 Non-Cardiac Comorbidities

| Comorbidity | Impact on Pacing Decision |
|------------|--------------------------|
| **Chronic kidney disease** | Electrolyte imbalance risk; MRI considerations |
| **Diabetes mellitus** | Autonomic neuropathy may affect pacing needs; infection risk |
| **COPD/pulmonary disease** | Minute ventilation sensing affected; respiratory sinus arrhythmia altered |
| **Obesity** | Surgical complexity; lead placement challenges |
| **Renal failure (dialysis)** | AV fistula access considerations; MRI compatibility |
| **Liver disease** | Coagulopathy; drug metabolism |
| **Hematological disorders** | Coagulopathy; thrombocytopenia |
| **Immunosuppression** | Increased infection risk |

### 6.3 Infection Risk Assessment

| Risk Factor | Increased Risk? | Management |
|------------|----------------|-----------|
| Diabetes mellitus | Yes | Optimize glucose control |
| Immunosuppression | Yes | Minimize immunosuppressive agents if possible |
| Chronic kidney disease | Yes | Optimize renal function |
| Active skin infection | Yes (contraindication) | Treat before implantation |
| History of device infection | Yes | Consider antibiotic-eluting envelope; pre-operative antibiotics |
| Malnutrition | Yes | Nutritional optimization |

### 6.4 Bleeding Risk Assessment

| Factor | Consideration |
|--------|--------------|
| **Anticoagulation status** | Warfarin (INR), DOACs (apixaban, rivarelbaan, dabigatran, edoxaban) |
| **Antiplatelet therapy** | Aspirin, clopidogrel, ticagrelor, prasugrel |
| **Platelet count** | Thrombocytopenia increases bleeding risk |
| **Coagulation factors** | Inherited or acquired coagulopathy |
| **Recent surgery** | May need to delay implantation |

**Management of anticoagulation during implantation**:
- **Warfarin**: May continue with INR 2.0–3.0 (Class I, Level B evidence)
- **DOACs**: May continue or hold for 24–48 hours (Class I, Level B evidence)
- **Dual antiplatelet therapy**: Increased bleeding risk; consider holding if possible

---

## 7. Anatomical Considerations

### 7.1 Venous Access

**Standard approach**: Pectoral pocket + cephalic or subclavian vein puncture

| Anatomical Factor | Impact | Alternative Approach |
|-------------------|--------|---------------------|
| Central venous obstruction | Lead passage impossible | Contrast venography; angioplasty; leadless pacing |
| Pacemaker on contralateral side | ipsilateral lead placement may be difficult | Ipsilateral placement with careful planning |
| History of subclavian crush | Lead fracture risk | Alternative venous access |
| Dialysis fistula | Avoid same arm | Contralateral implantation |

### 7.2 Cardiac Anatomy

| Factor | Impact |
|--------|--------|
| Dextrocardia | Lead placement on opposite side; flipped anatomy |
| Situs inversus | Mirror-image anatomy |
| Ebstein's anomaly | Tricuspid valve displacement; difficult lead positioning |
| Repaired congenital heart disease | Surgical changes to anatomy; may need epicardial leads |
| Severe scoliosis | Chest wall distortion; pocket placement challenges |

### 7.3 Body Habitus

| Factor | Consideration |
|--------|--------------|
| **Thin patient** | Risk of device erosion through skin |
| **Obese patient** | Deep pocket; lead routing challenges |
| **Muscular patient** | Pectoral muscle may compress lead (subclavian crush) |
| **Cachectic patient** | Increased erosion risk; less tissue coverage |

---

## 8. Shared Decision-Making

### 8.1 Principles

Shared decision-making is an ethical and clinical imperative for pacemaker implantation:

1. **Informed consent**: Patient must understand the benefits, risks, alternatives, and complications of pacemaker implantation
2. **Patient values**: The decision should align with the patient's values, goals, and preferences
3. **Risk-benefit discussion**: Clear communication of expected outcomes and potential complications
4. **Alternative treatments**: Discussion of medical management, observation, or alternative procedures
5. **Documentation**: Informed consent must be documented in the medical record

### 8.2 Key Discussion Points

| Topic | Discussion Content |
|-------|-------------------|
| **Indication** | Why is a pacemaker being recommended? What symptom or condition will it address? |
| **Benefits** | Expected symptom improvement, syncope prevention, improved quality of life |
| **Risks** | Bleeding, infection, lead complications, pneumothorax, cardiac perforation, device malfunction |
| **Alternatives** | Medical therapy (if applicable), observation, leadless pacing (if available) |
| **Device longevity** | How long the device battery will last; need for future replacements |
| **MRI considerations** | Whether the device is MRI-compatible; implications for future imaging |
| **Activity restrictions** | Post-implant restrictions; driving restrictions; exercise guidelines |
| **Follow-up requirements** | Regular device interrogation; remote monitoring |
| **Cost** | Device cost, procedural cost, follow-up cost (especially relevant in India) |

### 8.3 Special Decision-Making Situations

| Situation | Consideration |
|-----------|--------------|
| **Cognitively impaired patient** | Proxy decision-maker; advance directives |
| **Pediatric patient** | Parental consent; age-appropriate explanation |
| **Palliative care patient** | Goals of care; may decide against implantation |
| **Religious/cultural considerations** | Some patients may have concerns about implanted devices |
| **Limited access to follow-up** | May affect appropriateness of implantation |

---

## 9. MRI Compatibility Considerations

### 9.1 Pre-Implantation MRI Assessment

| Question | Decision Point |
|----------|---------------|
| Will the patient likely need MRI in the future? | Consider MRI-conditional system |
| What body regions may need MRI? | System must be labeled for the specific body region |
| What MRI field strengths are available at the patient's institution? | 1.5T vs. 3T compatibility |
| Are there specific MRI safety protocols at the implanting institution? | Protocol development and training |

### 9.2 MRI-Conditional Device Requirements

| Requirement | Specification |
|------------|--------------|
| Device labeling | Must be labeled as MRI-conditional by the manufacturer |
| Lead type | Must use MRI-conditional leads |
| Lead configuration | Specific lead length and routing requirements |
| Programming mode | Must switch to MRI mode before scanning |
| Post-scan programming | Must restore normal mode after scanning |
| Documentation | MRI conditional parameters must be documented |

---

## 10. Patient Selection in the Indian Context

### 10.1 Unique Challenges in India

| Challenge | Impact on Patient Selection |
|-----------|---------------------------|
| **Cost sensitivity** | Many patients pay out-of-pocket; cost influences device choice |
| **Late presentation** | Patients may present with advanced conduction disease |
| **Rheumatic heart disease** | Valvular disease complicating lead placement |
| **Tropical infections** | Higher infection rates (TB, infective endocarditis) |
| **Limited follow-up infrastructure** | Patients in rural areas may have difficulty with regular follow-up |
| **Polypharmacy with herbal/alternative medicine** | Unknown drug interactions |
| **High diabetes prevalence** | 10–12% diabetes prevalence; affects infection risk and autonomic function |
| **Young age at presentation** | Some conditions present earlier; longer device lifetime needed |

### 10.2 India-Specific Considerations

| Factor | Indian Context | Recommendation |
|--------|---------------|---------------|
| **Cost** | Average income ₹15,000–30,000/month; pacemaker costs ₹1–3 lakh | Affordable device development is critical |
| **Access** | 70% of population in rural areas; limited specialist access | Remote monitoring; simplified follow-up |
| **Infection rates** | Higher than Western countries | Strict aseptic technique; consider antibiotic envelopes |
| **Device longevity** | Patients may be younger; longer device life needed | High-efficiency battery design |
| **MRI access** | Growing MRI infrastructure; increasing demand | MRI-conditional design essential |
| **Regulatory framework** | CDSCO (Central Drugs Standard Control Organisation) approval required | Must meet Indian regulatory standards |
| **Insurance coverage** | Government insurance (Ayushman Bharat) may cover pacemakers | Cost-effective design aligns with public health goals |

### 10.3 Patient Selection Algorithm for iPACE-CHIP Candidates

```
Patient presents with bradycardia symptoms
    │
    ├── 1. Confirm bradycardia (ECG, Holter, monitoring)
    │       │
    │       └── YES → Proceed
    │       └── NO → Consider alternative diagnoses
    │
    ├── 2. Evaluate for reversible causes
    │       │
    │       ├── Reversible → Treat cause; reassess
    │       └── Non-reversible → Proceed
    │
    ├── 3. Assess comorbidities and bleeding/infection risk
    │       │
    │       ├── High risk → Optimize before implantation
    │       └── Acceptable risk → Proceed
    │
    ├── 4. Evaluate anatomy (venous access, cardiac structure)
    │       │
    │       ├── Standard anatomy → Standard transvenous approach
    │       └── Complex anatomy → Consider alternative (leadless, epicardial)
    │
    ├── 5. Shared decision-making
    │       │
    │       ├── Patient agrees → Proceed to implantation
    │       └── Patient declines → Document; offer follow-up
    │
    └── 6. Implantation
            │
            ├── Standard → iPACE-CHIP based system (if approved)
            └── Complex → Traditional imported system
```

---

## 11. Summary

Patient selection for pacemaker implantation requires:

1. **Symptom-documentation correlation**: The most critical factor — symptoms must be attributable to a documented rhythm disturbance.

2. **Comprehensive workup**: ECG, Holter monitoring, blood tests, echocardiography, and potentially EPS to establish the indication.

3. **Comorbidity assessment**: Cardiac and non-cardiac comorbidities influence procedural risk, device selection, and expected outcomes.

4. **Contraindication screening**: Active infection, severe coagulopathy, and patient refusal are absolute contraindications.

5. **Medication review**: Drug-induced bradycardia must be identified and addressed before implantation.

6. **Anatomical evaluation**: Venous access, cardiac anatomy, and body habitus affect implantation approach.

7. **MRI considerations**: The growing availability of MRI makes MRI-conditional device selection increasingly important.

8. **Shared decision-making**: Informed consent, patient values, and goals of care must guide the decision.

9. **India-specific factors**: Cost, access, infection risk, and regulatory requirements uniquely influence patient selection in the Indian context.

10. **iPACE-CHIP alignment**: The device must be designed to address the specific needs of the patient populations most likely to benefit from indigenous pacemaker technology.

---

## References

1. Kusumoto FM, et al. "2017 AHA/ACC/HRS Guideline for the Evaluation and Management of Patients with Bradycardia and Cardiac Conduction Delay." *Circulation*. 2018;138(16):e373-e453.
2. Brignole M, et al. "2018 ESC Guidelines for the diagnosis and management of syncope." *Eur Heart J*. 2018;39(21):1883-1948.
3. Epstein AE, et al. "2008 Guidelines for Device-Based Therapy of Cardiac Rhythm Abnormalities." *Circulation*. 2008;117(21):e350-e408.
4. Hendricks M, et al. "Pacemaker implantation in the elderly: a systematic review." *J Am Heart Assoc*. 2019;8(11):e012262.
5. Birnie D, et al. "Pacemaker pocket complications." *J Am Coll Cardiol*. 2013;61(17):1881-1891.
6. Cano O, et al. "Routine anticoagulation management during pacemaker and ICD implantation." *Europace*. 2018;20(11):1870-1877.
7. Indian Heart Rhythm Society. "Guidelines for cardiac pacing in India." *Indian Pacing Electrophysiol J*. 2020;20(1):1-24.
8. Indian Council of Medical Research. "Cardiovascular diseases in India." 2022.
9. Mond HG, Proctor M, Cao H, et al. "The world survey of cardiac pacing and ICDs: calendar year 2011." *Pacing Clin Electrophysiol*. 2013;36(3):322-334.
10. Padeletti L, et al. "Pacemaker implantation in India: a comprehensive review." *Indian Heart J*. 2021;73(2):123-132.
11. Varma N, et al. "Appropriate use criteria for ambulatory ECG monitoring." *Heart Rhythm*. 2017;14(8):e503-e531.
12. Sweeney MO, et al. "Minimal ventricular pacing in dual-chamber pacemakers." *Circulation*. 2007;115(25):3153-3160.
13. ISO 14708-1:2014. Implants for surgery — Active implantable medical devices — Part 1: General requirements for safety, marking and for information to be provided by the manufacturer.
14. IS 16046:2012. Implantable cardiac pacemakers — Requirements (Bureau of Indian Standards).
15. World Health Organization. "Cardiovascular diseases (CVDs) — Fact sheet." 2023.
