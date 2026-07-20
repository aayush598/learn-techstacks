# Cardiac Arrhythmias

## 1. Introduction

Cardiac arrhythmias — abnormalities of heart rhythm — represent one of the leading causes of morbidity and mortality worldwide. The World Health Organization estimates that approximately 17.9 million people die annually from cardiovascular diseases, with arrhythmias contributing significantly to sudden cardiac death (SCD), stroke, and heart failure. For the development of implantable pacemaker chips, a thorough understanding of arrhythmia mechanisms, classifications, electrocardiographic manifestations, and treatment indications is indispensable.

The iPACE-CHIP must be capable of: (1) detecting arrhythmias through cardiac signal sensing, (2) discriminating pathological from physiological rhythms, (3) delivering appropriate pacing therapy, and (4) communicating diagnostic data to clinicians. Each of these capabilities requires a deep understanding of the arrhythmias the device is designed to treat.

This chapter provides a comprehensive classification of cardiac arrhythmias relevant to pacemaker therapy, including bradyarrhythmias, tachyarrhythmias, conduction disorders, and their ECG manifestations.

---

## 2. Classification of Cardiac Arrhythmias

### 2.1 Overview

Cardiac arrhythmias can be classified along multiple axes:

| Classification Basis | Categories |
|---------------------|------------|
| **Heart rate** | Bradyarrhythmias (<60 bpm), Tachyarrhythmias (>100 bpm) |
| **Mechanism** | Disorders of impulse formation, Disorders of impulse conduction, Combined |
| **Anatomical origin** | Sinus, Atrial, AV junctional, Ventricular |
| **Duration** | Paroxysmal (self-terminating), Persistent, Permanent/Chronic |
| **Hemodynamic impact** | Stable, Unstable, Cardiac arrest |

### 2.2 Classification by Mechanism

The Mechanistic Classification of Arrhythmias (modified from the Lewis classification):

```
Arrhythmias
├── Disorders of Impulse Formation
│   ├── Abnormal Automaticity
│   │   ├── Enhanced normal automaticity (e.g., sinus tachycardia)
│   │   └── Abnormal automaticity (e.g., ischemic ventricular rhythm)
│   │
│   ├── Triggered Activity
│   │   ├── Early Afterdepolarizations (EADs)
│   │   │   └── Torsades de Pointes, Long QT syndrome
│   │   └── Delayed Afterdepolarizations (DADs)
│   │       └── Digitalis toxicity, Catecholaminergic polymorphic VT
│   │
│   └── Parasystopic Foci
│       └── Ventricular parasystole
│
├── Disorders of Impulse Conduction
│   ├── Re-entry
│   │   ├── Anatomical re-entry (AVRT, AVNRT, atrial flutter, VT)
│   │   ├── Functional re-entry (atrial fibrillation, VF)
│   │   └── Leading circle, spiral wave (rotor), figure-of-eight
│   │
│   ├── Conduction block
│   │   ├── SA exit block
│   │   ├── AV block (1st, 2nd, 3rd degree)
│   │   └── Bundle branch block
│   │
│   └── Conduction delay
│       └── Intra-atrial conduction delay, Intraventricular conduction delay
│
└── Combined Mechanisms
    ├── Tachy-brady syndrome (sick sinus syndrome with atrial tachyarrhythmias)
    └── Atrial fibrillation with rapid ventricular response and AV block
```

---

## 3. Bradycardias and Conduction Disorders

### 3.1 Definition and Hemodynamic Significance

Bradycardia is defined as a heart rate below 60 beats per minute. However, the clinical significance depends on context:
- Athletic individuals may have resting heart rates of 40–50 bpm (physiological)
- Heart rates below 50 bpm at rest are generally considered pathological
- Symptoms include dizziness, lightheadedness, syncope, fatigue, dyspnea, and exercise intolerance

Hemodynamic consequences of bradycardia:

| Heart Rate | Cardiac Output Impact | Clinical Significance |
|-----------|----------------------|----------------------|
| 50–60 bpm | Usually well tolerated | Often asymptomatic |
| 40–50 bpm | Mild reduction in CO | May cause fatigue, reduced exercise capacity |
| 30–40 bpm | Significant CO reduction | Dizziness, presyncope, near-syncope |
| < 30 bpm | Severe CO reduction | Syncope, hemodynamic compromise |
| < 20 bpm | Near-arrest | Agonal rhythm, imminent cardiac arrest |

### 3.2 Sinus Node Dysfunction (Sick Sinus Syndrome)

Sick sinus syndrome (SSS) encompasses a spectrum of SA node abnormalities:

#### 3.2.1 Sinus Bradycardia

**Definition**: Persistent sinus rate < 60 bpm (or < 50 bpm if clearly abnormal)

**ECG findings**:
- Regular P waves before every QRS
- P wave morphology consistent with sinus origin (upright in leads I, II, aVF)
- PR interval: 120–200 ms
- Heart rate: < 60 bpm
- Gradual onset and offset (warms up and slows down)

**Causes**:
- Fibrotic degeneration of the SA node (most common in elderly)
- Increased vagal tone (athletes, during sleep)
- Medications: beta-blockers, calcium channel blockers (verapamil, diltiazem), digoxin, amiodarone, ivabradine
- Hypothyroidism
- Hyperkalemia
- Inferior myocardial infarction
- Post-cardiac surgery
- Hypothermia

#### 3.2.2 Sinus Arrest

**Definition**: Failure of the SA node to generate an impulse, resulting in a pause without P waves

**ECG findings**:
- Absent P waves for the duration of the arrest
- Duration > 3 seconds is clinically significant
- Escape rhythm (if present) may be junctional or ventricular
- No relationship between the pause duration and the preceding PP interval

**Clinical significance**: Prolonged sinus arrest (> 3 seconds) can cause syncope and is a Class I indication for permanent pacemaker implantation.

#### 3.2.3 Sinoatrial Exit Block

**Definition**: The SA node fires, but the impulse fails to exit the node and depolarize the atrium

**ECG findings**:
- Absent P wave (and therefore absent QRS) for one cycle
- The pause is an exact multiple of the preceding PP interval (2x, 3x, etc.)
- This distinguishes SA exit block from sinus arrest (where the pause is not a multiple)

**Types**:
- **1st degree SA exit block**: Cannot be diagnosed on surface ECG (prolonged conduction time but impulse still reaches atrium)
- **2nd degree SA exit block**: Intermittent failure (Mobitz Type I/Wenckebach: progressive PP shortening before the pause; Mobitz Type II: sudden pause without PP changes)
- **3rd degree SA exit block**: Complete failure of conduction to the atrium (indistinguishable from sinus arrest on surface ECG)

#### 3.2.4 Tachy-Brady Syndrome

**Definition**: Alternation between atrial tachyarrhythmias (typically atrial fibrillation or flutter) and bradycardia (sinus bradycardia, sinus arrest, or AV block)

**ECG findings**: Episodes of rapid atrial rhythm alternating with periods of marked bradycardia or asystole

**Clinical significance**: The bradycardia often becomes apparent when the atrial tachyarrhythmia terminates, as overdrive suppression of the SA node causes a prolonged pause. This is one of the most compelling indications for permanent pacemaker implantation.

### 3.3 Atrioventricular (AV) Conduction Blocks

AV blocks are classified into three degrees based on the severity of conduction impairment:

#### 3.3.1 First-Degree AV Block

**Definition**: Prolonged but consistent AV conduction; every atrial impulse reaches the ventricles

**ECG criteria**:
- PR interval > 200 ms (> 1 large box at standard 25 mm/s sweep speed)
- Consistent PR interval (no progressive prolongation or dropped beats)
- Every P wave is followed by a QRS complex

**ECG Example**:
```
Lead II:

P    P    P    P    P    P
│    │    │    │    │    │
│    │    │    │    │    │
QRS  QRS  QRS  QRS  QRS  QRS

PR = 280 ms (prolonged but consistent)
Rate = 72 bpm
```

**Anatomical correlates**:
- Most commonly delayed at the AV node (intranodal delay)
- Can also be delayed at the His-Purkinje system (infra-Hisian delay)
- Site of block can be determined by His-bundle electrogram

**Clinical significance**: Usually benign and asymptomatic. Does not typically require pacemaker implantation. However:
- May progress to higher-degree AV block (especially if infra-Hisian)
- Mobitz Type I progression is uncommon but possible
- May cause symptoms in patients with diastolic dysfunction (loss of atrial contribution)

#### 3.3.2 Second-Degree AV Block — Mobitz Type I (Wenckebach)

**Definition**: Progressive prolongation of the PR interval until a QRS complex is dropped (non-conducted P wave)

**ECG criteria**:
- Progressive PR prolongation before the dropped beat
- The PR increment is typically greatest in the early cycles and diminishes (group beating)
- The pause containing the dropped beat is less than twice the preceding PP interval
- The first PR after the pause is shorter than the last PR before the pause
- Often exhibits "group beating" (clusters of conducted beats separated by pauses)

**ECG Example**:
```
Lead II:

P   P   P   P      P   P   P   P
│   │   │   │      │   │   │   │
PR  PR  PR  ─      PR  PR  PR  ─
160 190 240 (dropped) 160 190 230 (dropped)
    QRS QRS         QRS QRS QRS

Wenckebach cycles: 4:3 conduction (4 P waves, 3 QRS complexes)
```

**Mechanism**: Incremental delay in the AV node due to progressive fatigue of conduction pathways. The Wenckebach phenomenon is a property of decremental conduction.

**Location**: Almost always at the level of the AV node (intranodal)

**Clinical significance**:
- Usually benign
- Often reversible (medication adjustment, inferior MI)
- Progression to complete heart block is uncommon (< 10% over 5–10 years)
- Usually does not require pacemaker implantation unless symptomatic
- In the setting of acute inferior MI, typically resolves within days

#### 3.3.3 Second-Degree AV Block — Mobitz Type II

**Definition**: Sudden dropped QRS complexes without prior PR prolongation

**ECG criteria**:
- Constant PR intervals in conducted beats
- Sudden, unpredictable dropped QRS complexes
- Often exhibits 2:1 AV block (every other P wave conducted) or 3:1 block
- The pause containing the dropped beat is exactly twice the preceding PP interval

**ECG Example — 2:1 AV Block**:
```
Lead II:

P      P      P      P      P      P
│      │      │      │      │      │
QRS    ─      QRS    ─      QRS    ─
(conducted) (dropped) (conducted) (dropped) (conducted) (dropped)

PR interval: 180 ms (constant in conducted beats)
Atrial rate: 100 bpm
Ventricular rate: 50 bpm
```

**ECG Example — 3:2 Mobitz Type II**:
```
Lead II:

P   P   P      P   P   P
│   │   │      │   │   │
QRS QRS ─      QRS QRS ─
PR  PR         PR  PR
160 160        160 160
(constant)     (constant)
```

**Mechanism**: Sudden failure of conduction at the His-Purkinje system due to structural disease. Unlike Mobitz Type I, this is NOT due to physiological decremental conduction.

**Location**: Usually infra-Hisian (Bundle of His or bundle branches), though can be at the AV node in certain conditions

**Clinical significance**: This is a dangerous arrhythmia:
- High risk of progression to complete (third-degree) AV block
- Associated with sudden cardiac death (especially in the setting of acute anterior MI)
- **Class I indication for permanent pacemaker implantation**
- Even asymptomatic Mobitz Type II is an indication for pacing

**Differentiation from Mobitz Type I**:

| Feature | Mobitz Type I (Wenckebach) | Mobitz Type II |
|---------|--------------------------|----------------|
| PR interval | Progressively prolongs | Constant |
| Dropped beat | Predictable (after longest PR) | Unpredictable |
| QRS duration | Usually narrow | Usually wide (LBBB/RBBB) |
| Location | AV node | His-Purkinje system |
| Prognosis | Usually benign | Dangerous |
| Pacemaker needed? | Usually no | Yes |
| Acute MI association | Inferior MI | Anterior MI |

#### 3.3.4 Third-Degree (Complete) AV Block

**Definition**: Complete failure of AV conduction; no atrial impulses reach the ventricles

**ECG criteria**:
- Complete AV dissociation (P waves and QRS complexes are independent)
- Atrial rate (P-P interval) is regular and faster than the ventricular rate (R-R interval)
- Escape rhythm present (junctional: 40–60 bpm; ventricular: 20–40 bpm)
- P waves may appear before, during, or after QRS complexes (marching through)

**ECG Example**:
```
Lead II:

P    P    P    P    P    P    P    P    P
│    │    │    │    │    │    │    │    │

QRS         QRS         QRS         QRS
│            │            │            │

Atrial rate: 95 bpm (regular P-P interval)
Ventricular rate: 38 bpm (regular R-R interval)
AV dissociation: Complete (P waves independent of QRS)
Escape rhythm: Junctional (narrow QRS, rate 38 bpm)
```

**Mechanisms**:
1. **Complete AV nodal block**: Usually due to fibrotic degeneration of the AV node; escape rhythm is junctional (narrow QRS)
2. **Complete infra-Hisian block**: Usually due to bilateral bundle branch disease; escape rhythm is ventricular (wide QRS, slower rate)

**Escape rhythm characteristics**:

| Escape Site | QRS Morphology | Rate | Reliability |
|------------|---------------|------|-------------|
| AV node (high) | Narrow (< 120 ms) | 50–60 bpm | Relatively reliable |
| Bundle of His | Narrow or slightly wide | 40–50 bpm | Moderately reliable |
| Bundle branches | Wide (> 120 ms) | 30–40 bpm | Unreliable |
| Ventricular myocardium | Wide (> 140 ms) | 20–30 bpm | Very unreliable |

**Clinical significance**: This is a life-threatening condition:
- Complete dependence on an unreliable escape rhythm
- Risk of asystole if the escape rhythm fails
- **Class I indication for permanent pacemaker implantation** (urgent/emergent)
- Patients with ventricular escape rhythms have worse prognosis than those with junctional escape

---

## 4. Tachyarrhythmias

### 4.1 Overview of Tachycardia Mechanisms

Tachycardias are defined as heart rates > 100 bpm. They can be categorized by mechanism:

| Mechanism | Description | Examples |
|-----------|-------------|---------|
| **Enhanced automaticity** | Accelerated Phase 4 depolarization in pacemaker or latent pacemaker cells | Sinus tachycardia, accelerated idioventricular rhythm |
| **Triggered activity** | Afterdepolarizations (EADs or DADs) that reach threshold | Torsades de Pointes, digitalis-induced VT |
| **Re-entry** | Circulating wavefront around a fixed or functional circuit | AVRT, AVNRT, atrial flutter, most monomorphic VTs |

### 4.2 Supraventricular Tachycardias (SVTs)

SVTs originate above the ventricles (at the level of the atria or AV junction):

#### 4.2.1 Sinus Tachycardia

**Rate**: 100–180 bpm (can exceed 200 bpm with maximal exertion)

**ECG features**:
- Normal P wave morphology (upright in II, III, aVF)
- Constant PR interval
- Rate depends on age, fitness, and physiological demand
- Gradual onset and offset ("warm-up" and "cool-down")

**Causes**: Exercise, fever, pain, anxiety, hyperthyroidism, anemia, dehydration, sepsis, drugs (caffeine, amphetamines, cocaine), heart failure

**Relevance to pacing**: The rate-responsive pacemaker must be able to track physiological sinus tachycardia during exercise and not misinterpret it as an abnormal tachyarrhythmia.

#### 4.2.2 Atrial Fibrillation (AF)

The most common sustained cardiac arrhythmia, affecting approximately 2–4% of the adult population (prevalence increases with age to > 10% in individuals > 80 years).

**Mechanism**: Multiple re-entrant wavelets (Moe hypothesis) or focal drivers with fibrillatory conduction (rotor theory). The atria activate at 350–600 impulses per minute in a disorganized fashion.

**ECG features**:
- **Irregularly irregular** ventricular response (hallmark finding)
- Absent discrete P waves; replaced by fibrillatory baseline ("f" waves)
- f waves may be fine (< 0.5 mm) or coarse (> 0.5 mm) — particularly prominent in lead V1
- Variable R-R intervals
- Ventricular rate depends on AV node conduction properties

**ECG Example**:
```
Lead II:

──f──f──f──QRS──f──f──f──f──f──QRS──f──f──QRS──f──f──f──f──QRS──
                        ↑                                    ↑
                   (short R-R)                         (long R-R)

Irregularly irregular rhythm
No discernible P waves
Fine fibrillatory baseline
Variable R-R intervals
Ventricular rate: approximately 90 bpm (controlled)
```

**Classification by ventricular rate**:
| Category | Ventricular Rate | Treatment Implications |
|----------|-----------------|----------------------|
| Controlled (slow) | < 60 bpm | May need pacemaker if drug-induced bradycardia |
| Controlled (moderate) | 60–100 bpm | Rate control achieved |
| Uncontrolled (rapid) | 100–150 bpm | Rate control or rhythm control needed |
| Very rapid | > 150 bpm | Emergency rate/rhythm control |

**Relevance to pacemakers**:
- Many patients with AF have coexisting bradycardia (tachy-brady syndrome)
- Dual-chamber pacemakers can provide rate support during bradycardic phases
- Some pacemakers have AF detection algorithms and can store diagnostic data
- Ventricular rate response during AF may be inadequate; pacemaker can provide rate support

#### 4.2.3 Atrial Flutter

**Mechanism**: Macro-reentrant circuit in the right atrium, typically involving the cavotricuspid isthmus (CTI) — the region of tissue between the inferior vena cava and the tricuspid valve annulus.

**ECG features**:
- Atrial rate: typically 250–350 bpm (usually ~300 bpm)
- Sawtooth (flutter) waves best seen in leads II, III, aVF, and V1
- Regular ventricular response (unlike AF) due to fixed AV conduction ratio
- Common conduction ratios: 2:1 (ventricular rate ~150 bpm), 3:1 (~100 bpm), 4:1 (~75 bpm)

**Types**:
| Type | Circuit | Atrial Rate | Flutter Wave Direction |
|------|---------|-------------|----------------------|
| **CTI-dependent (typical)** | Right atrial, counterclockwise | 250–350 bpm | Negative in II, III, aVF |
| **CTI-dependent (reverse typical)** | Right atrial, clockwise | 250–350 bpm | Positive in II, III, aVF |
| **Non-CTI-dependent** | Left atrial or atypical circuits | Variable | Variable morphology |

**ECG Example — 2:1 Atrial Flutter**:
```
Lead II:

F    F    F    F    F    F    F    F    F    F
╲    ╲    ╲    ╲    ╲    ╲    ╲    ╲    ╲    ╲
QRS      QRS      QRS      QRS      QRS      QRS

Atrial rate (F-F interval): 300 bpm (200 ms)
Ventricular rate: 150 bpm (400 ms)
Conduction ratio: 2:1
Sawtooth pattern in inferior leads
```

**Clinical significance**: Atrial flutter is less commonly the initial presentation compared to AF but is often a harbinger of AF development. It is associated with the same stroke and thromboembolism risks as AF.

#### 4.2.4 AV Nodal Reentrant Tachycardia (AVNRT)

The most common form of paroxysmal SVT (approximately 60% of regular narrow-complex tachycardias).

**Mechanism**: Re-entry within or near the AV node using dual AV nodal pathways:
- **Fast pathway (β)**: Fast conduction, long refractory period
- **Slow pathway (α)**: Slow conduction, short refractory period

**Typical AVNRT (slow-fast)**:
- Antegrade conduction via slow pathway
- Retrograde conduction via fast pathway
- Atrial and ventricular activation nearly simultaneous

**ECG features**:
- Narrow QRS complex (unless aberrant conduction)
- Rate: 150–250 bpm
- Onset: Usually sudden (paroxysmal)
- P waves: Often not visible (hidden in QRS) or seen as pseudo-r' in V1 or pseudo-S in inferior leads
- RP interval: Very short (< 70 ms) — the R-P interval is shorter than the P-R interval

**Relevance to pacing**: Antitachycardia pacing (ATP) from a dual-chamber pacemaker can terminate AVNRT by delivering a premature stimulus that enters the re-entrant circuit and creates bidirectional block.

#### 4.2.5 AV Reentrant Tachycardia (AVRT)

**Mechanism**: Re-entry using an accessory pathway (AP) that connects the atria and ventricles, bypassing the AV node.

**Types**:
| Type | Antegrade Pathway | Retrograde Pathway | QRS Width |
|------|------------------|-------------------|-----------|
| **Orthodromic (common)** | AV node | Accessory pathway | Narrow (< 120 ms) |
| **Antidromic (rare)** | Accessory pathway | AV node | Wide (> 120 ms, pre-excited) |

**Wolff-Parkinson-White (WPW) Syndrome**: The presence of an accessory pathway with the ECG characteristics of pre-excitation:
- Short PR interval (< 120 ms)
- Delta wave (slurred upstroke of QRS due to early ventricular activation via the AP)
- Wide QRS complex (> 120 ms)
- Secondary ST-T wave changes

**Critical clinical point**: In AF with an accessory pathway (WPW + AF), the accessory pathway may conduct rapidly to the ventricles (no rate-limiting AV nodal delay), potentially causing ventricular fibrillation and sudden death. **AVOID AV nodal blocking agents** (adenosine, verapamil, diltiazem, digoxin) in this situation, as they may enhance conduction through the accessory pathway. Procainamide or electrical cardioversion is the treatment of choice.

#### 4.2.6 Atrial Tachycardia

**Mechanism**: Can be due to enhanced automaticity, triggered activity, or micro-re-entry in a localized atrial focus

**ECG features**:
- Discrete P wave morphology different from sinus P wave
- Regular rhythm
- Rate: 100–250 bpm
- Constant or variable AV block (2:1, 3:1, etc.)
- RP interval: Usually > PR interval (unlike AVNRT)

### 4.3 Ventricular Tachyarrhythmias

#### 4.3.1 Ventricular Tachycardia (VT)

**Definition**: Three or more consecutive ventricular beats at a rate > 100 bpm

**Classification**:

| Type | Duration | Hemodynamic Impact | Treatment |
|------|----------|-------------------|-----------|
| **Non-sustained VT (NSVT)** | < 30 seconds | Usually tolerated | Assessment, possible ICD |
| **Sustained VT** | ≥ 30 seconds or causes hemodynamic collapse | Often unstable | Cardioversion, antiarrhythmics, ICD |
| **Monomorphic VT** | Consistent QRS morphology | Variable | ATP, cardioversion, ablation |
| **Polymorphic VT** | Changing QRS morphology | Usually unstable | Cardioversion, correct underlying cause |

**Monomorphic VT ECG features**:
- Wide QRS complex (> 120 ms, usually > 140 ms)
- Regular rhythm with consistent QRS morphology
- Rate: 100–250 bpm
- AV dissociation (P waves independent of QRS — pathognomonic when visible)
- Fusion beats and capture beats (if AV dissociation with occasional AV conduction)

**ECG Example — Monomorphic VT**:
```
Lead II:

QRS    QRS    QRS    QRS    QRS    QRS    QRS    QRS
╲      ╱╲     ╱╲     ╱╲     ╱╲     ╱╲     ╱╲     ╱╲
 ╲    ╱  ╲   ╱  ╲   ╱  ╲   ╱  ╲   ╱  ╲   ╱  ╲   ╱
  ╲──╱    ╲─╱    ╲─╱    ╲─╱    ╲─╱    ╲─╱    ╲─╱    ╲─╱

Wide QRS complex tachycardia
Regular rhythm
Rate: ~180 bpm
QRS duration: ~160 ms
Morphology consistent with RVOT VT (LBBB pattern, inferior axis)
```

**VT vs. SVT with aberrancy**: Distinguishing wide-complex tachycardia (WCT) as VT versus SVT with aberrant conduction is a critical clinical skill:

| Feature | VT | SVT with Aberrancy |
|---------|-----|-------------------|
| AV dissociation | Present (hallmark) | Absent (1:1 AV relation) |
| Fusion/capture beats | Present | Absent |
| Concordance (QRS same direction as T wave in precordial leads) | Positive concordance (all precordial leads positive) | Usually negative concordance |
| QRS duration | Usually > 160 ms | Usually < 140 ms |
| Morphology in V1 | Monophasic R, notching | rSR' (RBBB), rsR' (LBBB) |
| Morphology in V6 | QS or rS (LBBB-like) | Monophasic R |
| Onset | Usually sudden | May be gradual (rate-dependent) |

**Note**: When in doubt, always treat as VT. The consequences of misdiagnosing VT as SVT and giving AV nodal blocking agents can be fatal.

**Pacemaker/ICD relevance**: VT is a primary indication for implantable cardioverter-defibrillator (ICD) therapy. The iPACE-CHIP, while primarily a pacemaker, must understand VT detection criteria for discrimination purposes.

#### 4.3.2 Ventricular Fibrillation (VF)

**Mechanism**: Chaotic, disorganized ventricular electrical activity with no coordinated contraction

**ECG features**:
- No recognizable QRS complexes, P waves, or T waves
- Chaotic, irregular waveform of variable amplitude
- Coarse VF (> 0.5 mV) vs. fine VF (< 0.5 mV) — fine VF may progress to asystole

**Clinical significance**: VF is immediately life-threatening:
- No cardiac output → cardiac arrest
- Requires immediate defibrillation (electrical shock)
- The primary function of ICDs is to detect and defibrillate VF
- Survival decreases by approximately 10% per minute without defibrillation

#### 4.3.3 Torsades de Pointes (TdP)

A specific form of polymorphic VT associated with QT interval prolongation.

**Mechanism**: Early afterdepolarizations (EADs) in the setting of prolonged ventricular repolarization

**ECG features**:
- QRS complexes that appear to "twist" around the isoelectric baseline
- Rate: 200–300 bpm
- Typically self-terminating but may degenerate into VF
- Preceded by prolonged QT interval

**Causes of QT prolongation leading to TdP**:
| Category | Examples |
|----------|---------|
| **Congenital** | Long QT Syndrome (LQTS) types 1–17 |
| **Acquired — Drugs** | Sotalol, dofetilide, quinidine, procainamide, certain antibiotics (macrolides, fluoroquinolones), antipsychotics (haloperidol, ziprasidone) |
| **Acquired — Electrolyte** | Hypokalemia, hypomagnesemia, hypocalcemia |
| **Acquired — Other** | Bradycardia, liver disease, hypothyroidism, structural heart disease |

**Treatment**: IV magnesium sulfate, isoproterenol (to increase heart rate and shorten QT), temporary overdrive pacing, removal of offending agent.

**Pacing relevance**: Overdrive pacing (at a rate faster than the underlying rhythm) can suppress TdP by:
- Shortening the QT interval (rate-dependent)
- Suppressing bradycardia (a trigger for TdP in some LQTS types)
- Suppressing EADs by eliminating long pauses

---

## 5. Specific Arrhythmia Syndromes

### 5.1 Brugada Syndrome

A genetic channelopathy (typically SCN5A mutation) characterized by:
- Coved-type ST elevation in V1–V2
- Right bundle branch block pattern
- Risk of VF and sudden cardiac death, especially during sleep/rest
- No structural heart disease

**ECG pattern**:
- Type 1 (diagnostic): Coved ST segment ≥ 2 mm followed by negative T wave in V1–V2
- Type 2 (suspicious): ≥ 2 mm ST elevation with saddle-back morphology
- Type 3: Coved or saddle-back pattern with < 2 mm ST elevation

**Pacing relevance**: ICD implantation is indicated for patients who have survived cardiac arrest or have documented sustained VT. Bradycardia-dependent activation of the arrhythmia may benefit from prophylactic pacing.

### 5.2 Hypertrophic Cardiomyopathy (HCM)

A genetic disease of the cardiac sarcomere (most commonly mutations in β-myosin heavy chain or myosin-binding protein C) characterized by:
- Asymmetric septal hypertrophy (usually > 15 mm)
- Left ventricular outflow tract (LVOT) obstruction in ~70% of patients
- Myocardial disarray and fibrosis
- Risk of sudden cardiac death (especially in young athletes)

**Arrhythmia mechanisms in HCM**:
- Monomorphic VT (re-entry around fibrotic areas)
- VF (triggered by VT or directly)
- Atrial fibrillation (due to left atrial enlargement)
- Conduction disease (due to myocardial fibrosis)

**Pacing role**:
- ICD for primary and secondary prevention of sudden death
- Dual-chamber pacing with short AV delay can reduce LVOT gradient in some patients (by altering the activation sequence)
- CRT may be considered in patients with HCM and conduction disease

### 5.3 Arrhythmogenic Right Ventricular Cardiomyopathy (ARVC)

A desmosomal disease characterized by:
- Progressive fibrofatty replacement of RV myocardium
- Ventricular tachycardia with LBBB morphology (RV origin)
- Risk of sudden cardiac death (especially during exercise)
- T-wave inversions in V1–V3

**Pacing relevance**: ICD implantation for VT/VF prevention. Lead placement may be challenging due to RV wall thinning and fatty infiltration.

---

## 6. Pacemaker-Responsive Arrhythmias

### 6.1 Pacing for Bradyarrhythmias

The primary indication for permanent pacemaker implantation is symptomatic bradycardia due to:

| Arrhythmia | Mechanism | Pacing Mode |
|-----------|-----------|-------------|
| **Sick sinus syndrome** | SA node dysfunction | AAI/AAIR (intact AV conduction) or DDD/DDDR |
| **Complete AV block** | Complete failure of AV conduction | VVI/VVIR (single chamber) or DDD/DDDR (dual chamber) |
| **Mobitz Type II AV block** | His-Purkinje disease | DDD/DDDR |
| **Bilateral bundle branch block** | Progressive conduction disease | DDD/DDDR |
| **Drug-induced bradycardia** | Iatrogenic (medication side effect) | Pacing if drug cannot be discontinued |
| **Post-cardiac surgery** | Iatrogenic (surgical trauma) | Temporary → permanent if persistent |

### 6.2 Pacing to Prevent Tachyarrhythmias

Pacemakers can also play a role in tachycardia management:

| Strategy | Mechanism | Application |
|----------|-----------|-------------|
| **Overdrive pacing** | Pacing slightly faster than the tachycardia rate to suppress ectopic foci | Atrial tachycardia prevention |
| **Antitachycardia pacing (ATP)** | Delivering a burst or ramp of pacing to interrupt re-entrant circuits | AVNRT, AVRT, monomorphic VT |
| **Post-pacing pause prevention** | Backup pacing after ATP or defibrillation | Post-ATP asystole prevention |
| **Rate smoothing** | Limiting beat-to-beat rate changes to prevent triggered activity | AF rate regularization |
| **PAC suppression** | Pacing to suppress premature atrial contractions that trigger AF | AF prevention |
| **Cardiac resynchronization** | Biventricular pacing to improve hemodynamics and reduce arrhythmia substrate | Heart failure with dyssynchrony |

### 6.3 ICD Therapy for Tachyarrhythmias

The ICD extends pacemaker functionality to include:

| Therapy | Description | Target Arrhythmia |
|---------|-------------|-------------------|
| **ATP — Burst pacing** | 3–8 pulses at 80–88% of tachycardia cycle length | Monomorphic VT |
| **ATP — Ramp pacing** | Progressive decrementing pacing cycle length | Monomorphic VT |
| **Cardioversion** | Synchronized low-energy shock (0.5–5 J) | Stable monomorphic VT |
| **Defibrillation** | High-energy shock (20–40 J) | Unstable VT, VF |

---

## 7. ECG Diagnostic Criteria Summary

### 7.1 Key ECG Intervals and Their Arrhythmia Associations

| ECG Parameter | Normal Range | Abnormality | Associated Arrhythmia |
|---------------|-------------|------------|----------------------|
| **Heart rate** | 60–100 bpm | < 60 bpm | Bradycardia, SSS |
| | | > 100 bpm | Tachycardia (sinus, SVT, VT) |
| **PR interval** | 120–200 ms | > 200 ms | 1st degree AV block |
| | | Progressive prolongation | 2nd degree Type I |
| | | Variable | AV dissociation (3rd degree) |
| **QRS duration** | 60–100 ms | > 120 ms | Bundle branch block, VT |
| **QT interval** | < 440 ms (men), < 460 ms (women) | Prolonged | TdP risk, LQTS |
| **QTc (Bazett)** | < 440 ms | > 500 ms | High TdP risk |
| **RR interval** | 600–1000 ms | Highly variable | AF (irregularly irregular) |
| | | Fixed short | Tachycardia |
| | | Fixed long | Bradycardia |

### 7.2 Heart Rate Calculation Methods

For ECG rhythm strips at 25 mm/s sweep speed:

| Method | Calculation | Best For |
|--------|-------------|---------|
| **300 method** | HR = 300 / (number of large boxes between R waves) | Regular rhythms near 60–180 bpm |
| **1500 method** | HR = 1500 / (number of small boxes between R waves) | Regular rhythms, any rate |
| **RR interval** | HR = 60,000 / (RR interval in ms) | Any rhythm |
| **10-second strip** | HR = number of R waves in 10 seconds × 6 | Irregular rhythms |

---

## 8. Arrhythmia Detection Algorithms for Pacemakers

### 8.1 Sensing Requirements

The iPACE-CHIP must accurately sense cardiac signals to detect arrhythmias. Key requirements:

| Parameter | Atrial Sensing | Ventricular Sensing |
|-----------|---------------|-------------------|
| **Amplitude range** | 0.2–4.0 mV | 5–25 mV |
| **Bandwidth** | 0.5–100 Hz | 10–100 Hz |
| **Noise rejection** | Muscle artifact rejection | Muscle artifact rejection |
| **Sensitivity** | Programmable (typically 0.18–1.0 mV) | Programmable (typically 0.2–5.0 mV) |
| **Blanking period** | 200–400 ms (post-atrial pace) | 200–400 ms (post-ventricular pace) |
| **Refractory period** | 150–500 ms | 150–350 ms |

### 8.2 Arrhythmia Detection Criteria

| Arrhythmia | Detection Criterion | Duration Required |
|-----------|---------------------|-------------------|
| **Sinus bradycardia** | Rate < programmed lower rate limit | Consecutive cycles |
| **AF** | Irregularly irregular R-R + absent P waves + atrial rate > 400/min | 30–60 seconds |
| **Atrial flutter** | Atrial rate 200–500/min with regular atrial cycle length | 30–60 seconds |
| **Atrial tachycardia** | Atrial rate > programmed atrial tachy rate | Consecutive cycles |
| **VT** | Ventricular rate > programmed VT detection rate | Number of consecutive beats (typically 12–18) |
| **VF** | Ventricular rate > programmed VF detection rate + impedance/amplitude criteria | Typically 30/40 detection (30 of 40 intervals) |
| **Asystole** | No sensed ventricular event for > programmed duration (typically 3000–5000 ms) | Single episode |

### 8.3 Discrimination Algorithms

Modern pacemakers use sophisticated algorithms to discriminate true arrhythmias from artifacts:

1. **Morphology analysis**: Comparing the sensed QRS morphology to a stored template (V morphology discrimination)
2. **Onset analysis**: Sudden vs. gradual rate increase (sinus tachycardia has gradual onset; SVT/VT usually has sudden onset)
3. **Stability analysis**: Regularity of R-R intervals (VT is usually regular; AF is irregular)
4. **Atrial timing analysis**: PR association (1:1 association suggests SVT; AV dissociation suggests VT)
5. **Blanking and refractory period optimization**: To prevent double-sensing or T-wave oversensing

---

## 9. Summary

Cardiac arrhythmias represent a diverse spectrum of electrical disturbances, ranging from benign rhythm variations to immediately life-threatening emergencies. For the iPACE-CHIP developer, the key categories are:

1. **Bradycardias** (sinus node dysfunction, AV conduction blocks): The primary target for pacemaker therapy. Understanding the ECG manifestations, mechanisms, and progression patterns informs pacing mode selection and timing cycle programming.

2. **Tachyarrhythmias** (AF, flutter, SVT, VT, VF): While primarily managed by ICDs and antiarrhythmic drugs, pacemakers play supporting roles in rate management, ATP, and diagnostic monitoring.

3. **Conduction disorders**: The spectrum from first-degree to complete AV block represents progressive conduction system disease that may require pacemaker intervention.

4. **Specific syndromes** (Brugada, HCM, ARVC, LQTS): These carry significant arrhythmic risk and often require ICD implantation with pacemaker backup functions.

A thorough understanding of these arrhythmias — their mechanisms, ECG signatures, and treatment indications — is essential for designing a pacemaker chip that can accurately detect, discriminate, and appropriately treat the full spectrum of cardiac rhythm disorders.

---

## References

1. Zipes DP, et al. "ACC/AHA/ESC 2015 Guidelines for the Management of Patients with Supraventricular Tachycardia." *Circulation*. 2016;133(14):e506-e575.
2. Al-Khatib SM, et al. "2017 AHA/ACC/HRS Guideline for Management of Patients with Ventricular Arrhythmias." *Circulation*. 2018;138(13):e272-e391.
3. Hindricks G, et al. "2020 ESC Guidelines for the diagnosis and management of atrial fibrillation." *Eur Heart J*. 2021;42(5):373-498.
4. Brugada P, Brugada J. "Right bundle branch block, persistent ST segment elevation and sudden cardiac death: a distinct clinical and electrocardiographic syndrome." *J Am Coll Cardiol*. 1992;20(6):1391-1396.
5. Wellens HJ. "The ECG in emergency decision making." 2nd ed. Elsevier; 2012.
6. Marriott HJL, Conover MB. "Advanced concepts in arrhythmias." 3rd ed. Mosby; 1996.
7. Surawicz B, Knilans TK. "Chou's electrocardiography in clinical practice." 6th ed. Saunders; 2008.
8. Josephson ME. "Clinical cardiac electrophysiology: techniques and interpretations." 5th ed. Wolters Kluwer; 2016.
9. Scherlag BJ, et al. "Electrophysiology of the AV node." In: *Cardiac Electrophysiology: From Cell to Bedside*. 7th ed. Elsevier; 2018.
10. El-Sherif N, Turitto G, Dilaveris P, et al. "Classification of ventricular arrhythmias." In: *Cardiac Electrophysiology: From Cell to Bedside*. 7th ed. Elsevier; 2018.
11. Bayés de Luna A. "Textbook of clinical electrocardiography." 3rd ed. Springer; 2012.
12. Kusumoto FM, et al. "2017 ACC/AHA/HRS Guideline for the Evaluation and Management of Patients with Bradycardia and Cardiac Conduction Delay." *Circulation*. 2018;138(16):e373-e453.
