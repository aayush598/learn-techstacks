# ECG Signal Fundamentals

## 1. Introduction

The electrocardiogram (ECG or EKG) is the fundamental diagnostic tool of cardiac electrophysiology and the primary signal source for pacemaker sensing and discrimination algorithms. First recorded by Willem Einthoven in 1901 (for which he received the Nobel Prize in Physiology or Medicine in 1924), the ECG has become the most widely performed cardiac diagnostic test worldwide, with an estimated 300 million ECGs performed annually.

For the engineer designing the iPACE-CHIP, the ECG signal is not merely a diagnostic waveform — it is the electrical signal the device must sense, interpret, and respond to in real-time. The chip's sensing amplifiers, filters, analog-to-digital converters, and detection algorithms must be designed to faithfully capture the cardiac signal while rejecting noise and artifact. This requires deep knowledge of ECG signal morphology, amplitude, frequency content, noise sources, and signal processing requirements.

This chapter provides a comprehensive treatment of ECG signal characteristics from both a clinical and an engineering perspective.

---

## 2. Historical Context

### 2.1 The Discovery of Bioelectric Phenomena

| Year | Event | Key Figure |
|------|-------|-----------|
| 1791 | Discovery of bioelectricity in frog legs | Luigi Galvani |
| 1842 | First recording of cardiac electrical activity (in dogs) | Carlo Matteucci |
| 1887 | First human ECG recording using capillary electrometer | Augustus Waller |
| 1901 | Development of the string galvanometer; clinical ECG | Willem Einthoven |
| 1903 | Einthoven's triangle and standard limb lead system | Willem Einthoven |
| 1930s | Precordial (chest) leads introduced | Frank Wilson |
| 1942 | 12-lead ECG system standardized | Wilson et al. |
| 1960s | Vectorcardiography developed | Various |
| 1980s | Holter monitoring widely adopted | Norman Holter |
| 2000s | High-resolution ECG, body surface mapping | Various |
| 2020s | AI-based ECG analysis, wearable ECG monitors | Various |

### 2.2 Einthoven's Contributions

Willem Einthoven established the foundational concepts of clinical ECG:

1. **Einthoven's Triangle**: The three limb leads (I, II, III) form an equilateral triangle with the heart at the center
2. **Einthoven's Law**: Lead II = Lead I + Lead III (mathematical relationship between limb leads)
3. **Standard calibration**: 1 mV = 10 mm deflection at standard sensitivity; 25 mm/s paper speed
4. **Naming convention**: P, Q, R, S, T waves (using letters from the middle of the alphabet)

---

## 3. Standard ECG Lead Systems

### 3.1 The 12-Lead ECG

The standard 12-lead ECG consists of 10 electrodes producing 12 different views of the heart's electrical activity:

| Lead | Electrode Combination | View | Primary Information |
|------|----------------------|------|-------------------|
| **I** | LA - RA | Lateral | Left atrial/ventricular lateral wall |
| **II** | LL - RA | Inferior | Inferior wall (dominant R wave in normal) |
| **III** | LL - LA | Inferior | Inferior wall |
| **aVR** | RA - (LA+LL)/2 | Right superior | Right atrium, right superior ventricle |
| **aVL** | LA - (RA+LL)/2 | High lateral | High lateral wall |
| **aVF** | LL - (RA+LA)/2 | Inferior | Inferior wall |
| **V1** | V1 electrode - Wilson's CT | Septal/anterior | RV, interventricular septum |
| **V2** | V2 electrode - Wilson's CT | Septal | Interventricular septum |
| **V3** | V3 electrode - Wilson's CT | Anterior | Anterior wall |
| **V4** | V4 electrode - Wilson's CT | Anterior/apex | Anterior wall, apex |
| **V5** | V5 electrode - Wilson's CT | Lateral | Lateral wall |
| **V6** | V6 electrode - Wilson's CT | Lateral | Lateral wall (low) |

**Wilson's Central Terminal (CT)**: The average potential of the three limb electrodes (RA + LA + LL) / 3, serving as the reference electrode for precordial leads.

### 3.2 Electrode Placement

**Limb electrodes**:
- **RA (Right Arm)**: Right subclavicular region or right wrist
- **LA (Left Arm)**: Left subclavicular region or left wrist
- **LL (Left Leg)**: Left lower abdomen or left ankle

**Precordial electrodes** (placed on the anterior chest wall):
- **V1**: 4th intercostal space, right sternal border
- **V2**: 4th intercostal space, left sternal border
- **V3**: Midway between V2 and V4
- **V4**: 5th intercostal space, left mid-clavicular line
- **V5**: 5th intercostal space, left anterior axillary line
- **V6**: 5th intercostal space, left mid-axillary line

### 3.3 Lead Systems Relevant to Pacemakers

While the 12-lead ECG is used for diagnostic purposes, pacemakers use a limited lead system:

| Lead System | Electrodes | Use |
|------------|------------|-----|
| **Intracardiac electrogram (IEGM)** | Tip and ring of atrial and ventricular leads | Sensing, pacing, diagnostics |
| **Surface ECG (monitoring)** | Standard 12-lead or 5-lead | Intra-procedural monitoring |
| **Far-field ECG** | Can + header as antenna | R-wave detection in some devices |

---

## 4. ECG Waveform Components

### 4.1 The P Wave

The P wave represents atrial depolarization — the spread of electrical activation across both atria.

**Characteristics**:

| Parameter | Normal Value | Clinical Significance of Abnormality |
|-----------|-------------| Enlargement, conduction delay |
| **Duration** | 60–120 ms | > 120 ms → atrial conduction delay, LA enlargement |
| **Amplitude** | 0.2–0.25 mV (limb leads) | > 0.25 mV → RA enlargement |
| | 0.1–0.2 mV (precordial leads) | |
| **Morphology** | Upright in I, II, aVF; inverted in aVR | Abnormal axis suggests ectopic origin |
| **Axis** | 0° to +75° | Left axis: ectopic left atrial focus |
| **P-R interval** | 120–200 ms | > 200 ms: 1st degree AV block |

**P wave morphology and atrial enlargement**:

| Condition | ECG Finding | Criteria |
|-----------|-------------|----------|
| **Right atrial enlargement (RAE)** | Peaked P wave in II, III, aVF | P > 0.25 mV, P > 120 ms |
| **Left atrial enlargement (LAE)** | P bifid in II; negative P terminal force in V1 | P > 120 ms; PTF-V1 > 40 mm·ms |
| **Bilateral atrial enlargement** | Both RAE and LAE criteria | Combined features |

**Engineering considerations for P wave sensing**:

The P wave is the smallest major cardiac signal and the most challenging to sense reliably:

- **Amplitude**: 0.2–4.0 mV (intracardiac), typically 0.5–2.0 mV from atrial appendage
- **Frequency content**: 0.5–40 Hz (fundamental at ~5–15 Hz)
- **dV/dt**: Lower than R wave, requiring careful sensing threshold settings
- **Morphology**: Variable with body position, respiration, and lead position

### 4.2 The PR Interval (Segment)

The PR interval extends from the onset of the P wave to the onset of the QRS complex. It includes:
- **P wave duration** (atrial depolarization)
- **PR segment** (conduction through the AV node, Bundle of His, and proximal bundle branches)

**Duration**: 120–200 ms in adults

**Components and timing**:
```
  P wave    PR segment
├────────┤├──────────────┤
         │               │
         AV node delay   Bundle of His + bundle branches
         ~50-80 ms       ~30-50 ms
         (majority)      (minority)
```

### 4.3 The QRS Complex

The QRS complex represents ventricular depolarization — the spread of electrical activation across both ventricles via the specialized conduction system and ventricular myocardium.

**Components** (by convention):
- **Q wave**: First negative deflection after the P wave (if present)
- **R wave**: First positive deflection
- **S wave**: First negative deflection after the R wave
- **R' wave**: Second positive deflection (if present)
- **S' wave**: Second negative deflection (if present)

**Nomenclature examples**:
- qR: Small Q, dominant R
- Rs: Dominant R, small S
- rS: Small R, dominant S
- qRs: Small Q, dominant R, small S
- QS: Single negative deflection (no positive component)

**Characteristics**:

| Parameter | Normal Value | Clinical Significance |
|-----------|-------------|----------------------|
| **Duration** | 60–100 ms | > 120 ms: bundle branch block, VT |
| **Amplitude (R wave)** | Variable by lead | |
| V1 | < 1.0 mV (rS pattern) | > 1.0 mV: RVH, RBBB, posterior MI |
| V5, V6 | < 2.5 mV | > 2.5 mV: LVH |
| Limb leads | < 2.0 mV (R in I, II) | > 2.0 mV: ventricular hypertrophy |
| **Axis** | -30° to +90° | Abnormal: bundle branch block, hemiblock, ventricular hypertrophy |
| **Progression in precordial leads** | R wave progression V1→V6 | Poor progression: anterior MI, LVH |

**R wave progression**:
```
     V1     V2     V3     V4     V5     V6
Normal: rS     rS     Rs     R      R      Rs
         ↓      ↓      ↓      ↓      ↓      ↓
         Small  Small  Transition  Dominant R waves
         R      R      zone        in lateral leads
```

**Abnormal R wave progression**:
- **Poor R wave progression (PRWP)**: R wave amplitude in V3 < 0.3 mV; suggests anterior MI
- **Poor R wave progression**: Can also be seen in LVH, LBBB, and left axis deviation

**Engineering considerations for QRS sensing**:

The R wave is the largest cardiac signal and the easiest to sense:
- **Amplitude**: 5–25 mV (intracardiac), typically 10–20 mV from RV apex
- **dV/dt**: High slew rate (500–1000 V/s intracardiacally)
- **Frequency content**: 10–100 Hz (fundamental at ~10–25 Hz)
- **Signal-to-noise ratio**: Highest of all cardiac signals

The R wave's large amplitude and sharp onset make it the reference signal for pacemaker timing cycles (the ventricular event triggers the V-A interval, V-V interval, and post-ventricular timing periods).

### 4.4 The ST Segment

The ST segment connects the QRS complex to the T wave, representing the period when the ventricles are fully depolarized (the plateau phase of the ventricular action potential).

**Characteristics**:
- **Normal position**: Isoelectric (on the TP baseline) or slightly elevated/depressed (< 0.5 mm in limb leads; < 1.0 mm in precordial leads)
- **Duration**: Variable (begins at the J point and ends at the onset of the T wave)

**Abnormalities**:

| Finding | Definition | Clinical Significance |
|---------|-----------|----------------------|
| **ST elevation** | ≥ 1 mm in ≥ 2 contiguous limb leads, or ≥ 2 mm in ≥ 2 contiguous precordial leads | Acute MI (STEMI), pericarditis, Brugada syndrome |
| **ST depression** | ≥ 0.5 mm in ≥ 2 contiguous leads | Myocardial ischemia, digoxin effect, LVH |
| **J-point elevation** | Elevation at the junction of QRS and ST segment | Normal variant (early repolarization), Brugada |

**Relevance to pacemakers**: ST-segment monitoring can be a diagnostic feature of advanced pacemakers. Changes in ST-segment may indicate myocardial ischemia, and some devices can store ST-segment measurements for diagnostic purposes.

### 4.5 The T Wave

The T wave represents ventricular repolarization — the return of the ventricular myocardium from the depolarized to the resting state.

**Characteristics**:

| Parameter | Normal Value | Clinical Significance |
|-----------|-------------|----------------------|
| **Amplitude** | < 0.5 mV (limb leads); < 1.0 mV (precordial leads) | Tall T waves: hyperkalemia, acute MI, LQTS |
| **Morphology** | Asymmetric, smooth, rounded | Peaked (hyperkalemia), inverted (ischemia), biphasic |
| **Direction** | Same as QRS in most leads | Inversion in leads with dominant R wave may indicate ischemia |
| **Duration** | 120–200 ms | Prolonged: LQTS, hypokalemia |
| **Peak to end** | < 100 ms | > 100 ms: diagnostic of LQTS in certain leads |

**Engineering considerations**: The T wave must be correctly identified and rejected by the sensing circuit to avoid "double counting" (interpreting the T wave as an R wave). This is achieved through:
- **Refractory periods**: A programmable blanking/refractory period after the R wave during which the sensing circuit is inactive
- **T-wave discrimination algorithms**: Morphology-based algorithms that distinguish T waves from R waves based on amplitude, slope, and frequency content

### 4.6 The U Wave

The U wave is a small, low-frequency deflection that occasionally follows the T wave.

**Characteristics**:
- **Amplitude**: < 0.05 mV (very small; often not visible)
- **Duration**: ~100–200 ms
- **Direction**: Usually in the same direction as the T wave
- **Rate**: Best seen at slow heart rates

**Proposed mechanisms**:
1. Repolarization of the Purkinje fibers
2. Repolarization of the mid-myocardial (M) cells
3. Mechanical-electrical coupling (stretch-activated channels)
4. Afterpotentials in ventricular myocytes

**Clinical significance**:
- Prominent U waves: hypokalemia, hypomagnesemia, bradycardia, certain drugs (sotalol, amiodarone)
- U wave inversion: may indicate ischemia or LVH

---

## 5. ECG Signal Characteristics — Engineering Perspective

### 5.1 Signal Amplitude

The ECG signal spans a wide range of amplitudes depending on the recording method:

| Recording Method | Signal Amplitude | Typical Application |
|-----------------|-----------------|-------------------|
| **Body surface (standard 12-lead)** | 0.5–3.0 mV | Diagnostic ECG, Holter monitoring |
| **Intracardiac (bipolar)** | 0.5–25 mV | Pacemaker sensing, EP studies |
| **Esophageal** | 0.5–3.0 mV | Atrial electrogram recording |
| ** epicardial** | 1.0–5.0 mV | Intraoperative monitoring |

**Intracardiac signal amplitudes (most relevant for iPACE-CHIP)**:

| Signal | Amplitude Range | Typical Value |
|--------|----------------|---------------|
| **P wave (atrial IEGM)** | 0.2–4.0 mV | 0.5–2.0 mV |
| **R wave (ventricular IEGM)** | 5–25 mV | 10–20 mV |
| **T wave (ventricular IEGM)** | 0.1–3.0 mV | 0.5–1.5 mV |
| **Pacing artifact** | Variable (depends on output) | 5–50 mV at the electrode |
| **Far-field R wave (atrial lead)** | 0.1–1.0 mV | 0.2–0.5 mV |
| **Myopotentials (skeletal muscle)** | 0.05–0.5 mV | 0.1–0.3 mV |
| **Electromagnetic interference** | 0.01–10+ mV | Variable |
| **Lead noise (fracture)** | 0.1–50+ mV | Variable |

### 5.2 Signal Frequency Content

The frequency content of the ECG signal varies by component:

| Component | Frequency Range | Dominant Frequency | Engineering Implication |
|-----------|----------------|-------------------|----------------------|
| **P wave** | 0.5–40 Hz | 5–15 Hz | Bandpass filter: 0.5–50 Hz |
| **QRS complex** | 5–200 Hz | 10–40 Hz | Bandpass filter: 10–100 Hz |
| **T wave** | 0.5–10 Hz | 1–5 Hz | Low-frequency; filter to reject |
| **ST segment** | DC–1 Hz | 0.05–0.5 Hz | Very low frequency; requires DC stability |
| **U wave** | 0.5–7 Hz | 1–3 Hz | Very low amplitude |
| **ECG baseline (noise)** | 0.01–0.5 Hz | — | High-pass filter to remove |
| **Power line interference** | 50/60 Hz | 50/60 Hz | Notch filter |
| **Muscle artifact (EMG)** | 5–2000 Hz | 50–500 Hz | Bandpass filtering |

### 5.3 Power Spectral Density

The ECG signal's power spectral density (PSD) follows an approximately 1/f^α distribution, with most energy concentrated below 40 Hz:

```
Power
(dB)
  │
  │██
  │████
  │██████
  │████████
  │██████████
  │████████████
  │████████████████
  │████████████████████████
  │████████████████████████████████████
  │██████████████████████████████████████████████████████
  └────────────────────────────────────────────────────── Frequency (Hz)
  0    10    20    40    60    100    200    500

  ← 95% of ECG energy →
     is below 40 Hz
```

### 5.4 Slew Rate (dV/dt)

The slew rate of different ECG components varies significantly:

| Component | Slew Rate (typical) | Significance |
|-----------|--------------------:|-------------|
| **P wave** | 0.5–2.0 V/s | Requires sensitive amplifier with low noise |
| **QRS complex (R wave)** | 1.0–10.0 V/s (intracardiac) | Sharp, easily detectable |
| | 10–500 V/s (surface, lead-dependent) | |
| **T wave** | 0.1–1.0 V/s | Slow; must be discriminated from R wave |
| **Pacing artifact** | 100–10000 V/s | Very sharp; can saturate amplifiers |
| **Lead fracture artifact** | 10–1000+ V/s | Abrupt, irregular; can mimic R waves |

---

## 6. ECG Noise Sources and Artifacts

### 6.1 Overview of Noise Sources

Noise in ECG recordings can be categorized by origin:

```
ECG Noise Sources
├── Patient-related
│   ├── Electromyographic (EMG) noise (skeletal muscle)
│   ├── Baseline wander (respiration, body movement)
│   ├── Electrosurgical interference (during procedures)
│   └── Tremor (Parkinson's disease, anxiety)
│
├── Electrode-related
│   ├── Electrode-skin impedance mismatch
│   ├── Electrode motion artifact
│   ├── Half-cell potential drift
│   └── Polarization
│
├── Environmental
│   ├── Power line interference (50/60 Hz)
│   ├── Electromagnetic interference (EMI)
│   ├── Radiofrequency interference (RFI)
│   └── Diathermy/surgical electrocautery
│
├── Device-related
│   ├── Amplifier noise (thermal, shot, 1/f)
│   ├── Quantization noise (ADC)
│   ├── Aliasing (insufficient sampling rate)
│   └── Lead fracture/loose connection
│
└── Physiological artifacts
    ├── Pacing artifact (in paced rhythm)
    ├── T-wave oversensing
    ├── Far-field R-wave sensing (in atrial lead)
    └── After-potentials
```

### 6.2 Power Line Interference (50/60 Hz)

**Characteristics**:
- Frequency: 50 Hz (Europe, Asia, Africa, Australia) or 60 Hz (Americas, parts of Asia)
- Amplitude: Can be up to 10× the ECG signal amplitude
- Mechanism: Capacitive coupling from power lines to patient and leads

**Rejection methods**:

| Method | Mechanism | Effectiveness |
|--------|-----------|---------------|
| **Right Leg Drive (RLD)** | Active feedback circuit that drives the patient with the inverted common-mode signal | 20–40 dB reduction |
| **Instrumentation amplifier** | High CMRR (> 80 dB) rejects common-mode signals | 40–80 dB reduction |
| **Notch filter** | Narrow band-reject filter at 50/60 Hz | Effective but introduces phase distortion |
| **Digital filtering** | Adaptive notch filter | Minimal phase distortion |
| **Shielded cabling** | Reduces capacitive coupling | 10–20 dB reduction |
| **Optical isolation** | Breaks ground loop path | Eliminates ground loop noise |

**Common-Mode Rejection Ratio (CMRR)**:

The CMRR is a critical specification for ECG amplifiers:

```
CMRR = 20 · log₁₀(Ad / Acm)

Where:
  Ad  = differential gain (signal of interest)
  Acm = common-mode gain (noise to be rejected)

Typical requirements:
  Surface ECG: CMRR > 100 dB
  Intracardiac (pacemaker): CMRR > 60 dB
```

### 6.3 Electromyographic (EMG) Noise

**Characteristics**:
- Frequency: 5–2000 Hz (overlapping with ECG signal)
- Amplitude: 0.05–3.0 mV (surface); 0.05–0.5 mV (intracardiac)
- Mechanism: Skeletal muscle contraction, especially pectoral muscles near the pacemaker pocket

**Impact on pacemakers**: EMG noise can cause:
- **Oversensing**: Incorrect detection of EMG as cardiac signals → inappropriate inhibition of pacing
- **Mode switching**: AF detection algorithms may误判 EMG as atrial fibrillation

**Mitigation strategies**:
- Bandpass filtering (low-pass at 40–100 Hz for cardiac sensing)
- Auto-adjusting sensitivity algorithms
- Blanking periods during high-noise episodes
- Sense amplifier design with frequency-dependent gain

### 6.4 Baseline Wander

**Characteristics**:
- Frequency: 0.05–0.5 Hz
- Amplitude: Up to ±3 mV
- Primary cause: Respiration (thoracic impedance changes during breathing)

**Impact on ECG**: Causes the ECG baseline to drift up and down, potentially:
- Causing ST segment misinterpretation
- Affecting T-wave detection
- Saturating high-gain amplifiers

**Mitigation**: High-pass filtering (cutoff: 0.05–0.5 Hz); for diagnostic ECG, use very low cutoff (0.05 Hz) to preserve ST information; for pacemaker sensing, use higher cutoff (0.5–5 Hz).

### 6.5 Lead Fracture and Noise

**Characteristics**:
- Abrupt, high-amplitude deflections
- Irregular, non-physiological morphology
- May mimic R waves (causing oversensing) or T waves

**Impact on pacemakers**: Lead fracture noise can cause:
- Inappropriate inhibition of pacing (if noise is sensed as cardiac events)
- Inappropriate mode switching
- False detection of tachyarrhythmias

**Detection and mitigation**:
- Lead impedance monitoring (sudden impedance changes indicate fracture)
- Noise reversion algorithms (automatic switching to asynchronous pacing during sustained noise)
- Discrimination algorithms based on signal morphology

### 6.6 Pacing Artifact (Stimulation Artifact)

**Characteristics**:
- Amplitude: 5–50 mV (at the sensing electrode)
- Duration: 0.05–2.0 ms
- Slew rate: > 1000 V/s
- Frequency content: Broad spectrum, extending to > 10 kHz

**Impact on sensing**: The pacing artifact can:
- Saturate the sensing amplifier
- Be mistaken for a cardiac signal
- Cause blanking of the subsequent cardiac signal

**Mitigation**: Post-pace blanking period — a programmable period (typically 200–400 ms) after each pacing pulse during which the sensing circuit is inactive.

---

## 7. ECG Signal Processing for Pacemakers

### 7.1 Analog Front-End Design

The analog front-end (AFE) of a pacemaker sensing circuit must:

1. **Amplify** the small intracardiac signal (0.2–25 mV) to a level suitable for digitization
2. **Filter** the signal to remove noise outside the cardiac frequency band
3. **Protect** against high-voltage signals (pacing artifacts, defibrillation shocks, electrocautery)

**Typical AFE architecture**:

```
IEGM → [Protection] → [Input Filter] → [Instrumentation Amp] → [Bandpass Filter] → [Programmable Gain Amp] → [ADC]
  │                     │                    │                      │                      │                   │
  │                     │                    │                      │                      │                   │
  Zener              1st order           G = 10-100           0.5-100 Hz            G = 1-100           8-12 bit
  clamp              high-pass                              (switchable)          (auto-ranging)        SAR or ΣΔ
  (< 5V)            (> 0.1 Hz)          CMRR > 80 dB                                               converter
```

### 7.2 Filtering Requirements

| Filter Stage | Type | Cutoff Frequency | Purpose |
|-------------|------|-----------------|---------|
| **Input protection** | Clamp/limiter | N/A | Protect from high-voltage signals |
| **Anti-aliasing** | Low-pass (passive RC) | 250–500 Hz | Prevent aliasing before ADC |
| **High-pass** | 1st or 2nd order | 0.1–5 Hz | Remove baseline wander and DC offset |
| **Low-pass** | 2nd–4th order | 40–100 Hz | Remove EMG noise and high-frequency interference |
| **Notch** | Adaptive notch | 50/60 Hz (optional) | Remove power line interference |
| **Post-ADC digital filter** | FIR or IIR | Programmable | Further noise rejection and signal conditioning |

### 7.3 Amplifier Specifications

| Parameter | Requirement | Rationale |
|-----------|------------|-----------|
| **Input-referred noise** | < 5 μV RMS | Must detect 0.2 mV P waves with SNR > 10:1 |
| **Input impedance** | > 100 MΩ (surface); > 1 MΩ (intracardiac) | Minimize signal attenuation |
| **CMRR** | > 80 dB (10,000:1) | Reject common-mode interference |
| **Input bias current** | < 10 nA | Minimize offset voltage |
| **Slew rate** | > 5 V/μs | Track QRS complex without distortion |
| **Input voltage range** | ±5 mV (signal) / ±1 V (overload) | Accommodate signal + noise + artifacts |
| **Power supply** | 1.2–3.3 V | Low power for implantable devices |
| **Current consumption** | < 5 μA | Critical for battery longevity |

### 7.4 Sampling and Digitization

| Parameter | Specification | Rationale |
|-----------|--------------|-----------|
| **Sampling rate** | 128–512 Hz (typical: 256 Hz) | Nyquist: > 2× max frequency of interest |
| **Resolution** | 8–12 bits | 10 bits minimum for adequate dynamic range |
| **Dynamic range** | > 60 dB | Accommodate P wave (0.2 mV) to R wave (25 mV) |
| **ADC type** | SAR or Sigma-Delta | SAR: fast; ΣΔ: high resolution, low power |
| **Anti-aliasing filter** | > 3rd order Butterworth at 0.5 × Fs | Prevent aliasing |

### 7.5 Digital Signal Processing Algorithms

Modern pacemakers implement several digital signal processing algorithms:

#### 7.5.1 Automatic Gain Control (AGC)

The sensing amplifier must adapt its gain to accommodate the wide dynamic range of intracardiac signals:
- **P wave sensing**: Higher gain needed (0.2–4.0 mV)
- **R wave sensing**: Lower gain sufficient (5–25 mV)
- **After pacing**: Automatic reduction to prevent sensing of pacing artifact and afterpotentials

#### 7.5.2 Dynamic Sensitivity

The sensing threshold adjusts dynamically after each sensed or paced event:

```
Time after event:
│
Sensitivity
(mV)
│
0.2 ─┤ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ Baseline sensitivity
│                                    ╱
0.5 ─┤                               ╱
│                              ╱
1.0 ─┤                         ╱
│                        ╱
2.0 ─┤                   ╱
│                  ╱
4.0 ─┤             ╱
│            ╱
8.0 ─┤  ╱─╱
│ ╱  ← Sensitivity increases
16 ─┤╱    after each event
│ (to avoid T-wave oversensing)
└────────────────────────────── Time
    │← blanking →│← recovery →│← baseline →│
```

#### 7.5.3 Cardiac Signal Classification

Digital algorithms classify each sensed event:

| Classification | Criteria | Action |
|---------------|----------|--------|
| **True cardiac event** | Appropriate amplitude, slew rate, morphology | Trigger timing cycles |
| **T wave** | Low slew rate, lower amplitude than R wave | Ignored (during post-R refractory period) |
| **Myopotential** | High-frequency, low amplitude | Ignored or triggers noise reversion |
| **Lead noise** | Abrupt, non-physiological morphology | May trigger noise reversion |
| **Far-field R wave** | Lower amplitude than near-field, different morphology | Rejected by sensing configuration |
| **Pacing artifact** | Very high amplitude, very short duration | Ignored during post-pace blanking |

---

## 8. ECG Recording Standards

### 8.1 Standard Recording Parameters

| Parameter | Diagnostic ECG | Holter Monitor | Pacemaker IEGM |
|-----------|---------------|---------------|---------------|
| **Paper speed** | 25 mm/s (or 50 mm/s) | Not applicable | Not applicable |
| **Sensitivity** | 10 mm/mV | 10 mm/mV | Variable (auto) |
| **Frequency response** | 0.05–150 Hz | 0.05–100 Hz | 0.5–100 Hz |
| **Sampling rate** | 500–1000 Hz | 128–400 Hz | 128–512 Hz |
| **Resolution** | 5–10 μV (16-bit ADC) | 5–10 μV | 10–50 μV (8-12 bit ADC) |
| **Number of leads** | 12 | 3–7 | 2 (bipolar atrial, bipolar ventricular) |

### 8.2 Clinical ECG Standards

| Standard | Description |
|----------|-------------|
| **AHA/ACC guidelines** | Recommendations for ECG recording and interpretation |
| **IEC 60601-2-25** | Particular requirements for basic safety and essential performance of electrocardiographs |
| **IEC 60601-2-47** | Particular requirements for ambulatory electrocardiographic systems |
| **ANSI/AAMI EC11** | Diagnostic electrocardiographic devices |
| **ISO 14708-3** | Active implantable neurostimulators (includes pacing systems) |

### 8.3 ECG Signal Quality Metrics

| Metric | Definition | Target Value |
|--------|-----------|-------------|
| **SNR (Signal-to-Noise Ratio)** | Ratio of signal power to noise power | > 20 dB for reliable sensing |
| **Artifacts per minute** | Number of non-cardiac signal detections | < 1% of total detections |
| **False positive rate** | Non-cardiac events detected as cardiac | < 0.1% for R wave; < 1% for P wave |
| **False negative rate** | True cardiac events not detected | < 0.01% (critical events must not be missed) |
| **Baseline wander** | Low-frequency noise amplitude | < 0.3 mV peak-to-peak |
| **Power line rejection** | 50/60 Hz attenuation | > 40 dB |

---

## 9. ECG in Special Populations

### 9.1 Neonates and Children

| Parameter | Neonate | Adult | Significance |
|-----------|---------|-------|-------------|
| **Heart rate** | 120–160 bpm | 60–100 bpm | Higher rates require faster sensing/sampling |
| **P wave amplitude** | 0.1–0.3 mV | 0.2–0.25 mV | Lower amplitude challenges atrial sensing |
| **QRS duration** | 40–60 ms | 60–100 ms | Narrower QRS requires faster sensing circuits |
| **QT interval** | 300–400 ms | 350–450 ms | Shorter QT may require modified detection |
| **Axis** | +60° to +180° (right axis) | -30° to +90° | Right axis is normal in neonates |

### 9.2 Elderly Patients

- **Increased fibrosis**: SA node and conduction system fibrosis → lower P wave and R wave amplitudes
- **Conduction delays**: Widened QRS, prolonged PR interval
- **Atrial fibrillation**: Higher prevalence → altered signal characteristics
- **Reduced HRV**: Lower heart rate variability
- **Lead impedance changes**: Tissue changes may affect lead impedance over time

### 9.3 Patients with Implantable Devices

When recording ECGs in patients with pacemakers or ICDs:
- **Pacing artifacts** appear as sharp vertical deflections
- **Stimulated cardiac complexes** (paced P waves, paced QRS complexes) differ in morphology from intrinsic complexes
- **Far-field signals** from other device leads may be visible
- **Device telemetry** may cause electromagnetic interference

---

## 10. ECG Signal Modeling for Chip Design

### 10.1 Synthetic ECG Generation

For testing the iPACE-CHIP's sensing algorithms, synthetic ECG signals can be generated using mathematical models:

**P wave model (Gaussian)**:
```
P(t) = Ap · exp(-(t - tp)² / (2·σp²))

Where:
  Ap  = P wave amplitude (0.2–2.0 mV)
  tp  = P wave peak time (~100 ms after P onset)
  σp  = P wave width parameter (~30 ms)
```

**QRS model (combination of Gaussians)**:
```
QRS(t) = Ar · exp(-(t - tr)² / (2·σr²)) 
        - Aq · exp(-(t - tq)² / (2·σq²))
        - As · exp(-(t - ts)² / (2·σs²))

Where:
  Ar, Aq, As = R, Q, S wave amplitudes
  tr, tq, ts = peak times
  σr, σq, σs = width parameters
```

**T wave model (Gaussian or asymmetric sigmoid)**:
```
T(t) = At · exp(-(t - tt)² / (2·σt²))

Where:
  At  = T wave amplitude (0.1–0.5 mV)
  tt  = T wave peak time (~300 ms after QRS)
  σt  = T wave width parameter (~80 ms)
```

### 10.2 Noise Models

**Power line interference**:
```
n_pli(t) = A_pli · sin(2π · f_pli · t + φ_pli)

Where:
  A_pli  = 0.5–5.0 mV (can exceed ECG amplitude)
  f_pli  = 50 Hz or 60 Hz
  φ_pli  = random phase
```

**EMG noise**:
```
n_emg(t) = filtered white noise with bandwidth 5–200 Hz
         = H(z) · w(t)

Where:
  H(z) = bandpass filter (5-200 Hz)
  w(t) = white Gaussian noise
```

**Baseline wander**:
```
n_bw(t) = A_bw · sin(2π · f_bw · t)

Where:
  A_bw = 0.2–2.0 mV
  f_bw = 0.15–0.3 Hz (respiratory frequency)
```

### 10.3 Lead Impedance Model

The electrical impedance between the pacemaker lead and cardiac tissue affects signal quality:

```
Z_total = R_electrode + R_tissue + Z_CPE

Where:
  R_electrode = electrode-electrolyte interface resistance (50-500 Ω)
  R_tissue    = myocardial resistance (10-100 Ω)
  Z_CPE       = constant phase element (models double-layer capacitance)
              = 1 / (Q · (jω)^n)
              where 0 < n < 1 (n = 1 for ideal capacitor)

Typical values at 1 kHz:
  Fresh implant: 300–600 Ω
  Chronic (6+ months): 500–1500 Ω
  Lead fracture: > 2000 Ω or < 100 Ω (short circuit)
```

---

## 11. ECG Signal Quality Assurance

### 11.1 Testing Standards for Pacemaker Sensing

| Test | Standard | Description |
|------|---------|-------------|
| **Sensitivity testing** | IEC 60601-1, ISO 14708-1 | Minimum detectable signal amplitude |
| **Specificity testing** | IEC 60601-1 | Rejection of non-cardiac signals |
| **Noise immunity** | IEC 60601-1 | Performance in presence of 50/60 Hz, EMG, EMI |
| **Leakage current** | IEC 60601-1 | Patient safety (≤ 10 μA for type CF applied parts) |
| **Battery simulation** | ANSI/AAMI | Performance over battery depletion curve |

### 11.2 Bench Testing with Simulated ECG

Pacemaker bench testing uses standardized ECG waveforms:

| Waveform | Standard | Description |
|----------|---------|-------------|
| **Telefax waveform** | ANSI/AAMI EC11 | Standard test P, QRS, T waveform |
| **Calibration pulse** | IEC 60601-2-25 | 1 mV, 10 ms rectangular pulse |
| **Noise signal** | Custom | Simulated EMG, power line, lead noise |
| **Arrhythmia simulation** | Custom | AF, VT, asystole, bradycardia |

---

## 12. Summary

The ECG signal is the fundamental input to the pacemaker sensing system. Key engineering considerations include:

1. **Amplitude range**: The sensing system must accommodate signals from 0.2 mV (P wave) to 25+ mV (R wave) — a dynamic range of approximately 40 dB.

2. **Frequency content**: The diagnostic ECG spans 0.05–150 Hz, but pacemaker sensing typically uses a narrower band (1–100 Hz) optimized for cardiac signal detection and noise rejection.

3. **Noise sources**: Power line interference, EMG noise, baseline wander, lead fracture artifact, and pacing artifacts all pose challenges that must be addressed through careful amplifier design, filtering, and digital signal processing.

4. **Signal processing**: Dynamic sensitivity adjustment, blanking/refractory periods, auto-gain control, and sophisticated discrimination algorithms are essential for reliable cardiac sensing.

5. **Testing and standards**: The iPACE-CHIP must meet rigorous international standards (IEC 60601-1, ISO 14708-1) for sensing performance, noise immunity, and patient safety.

6. **Synthetic ECG models**: Mathematical models of ECG components and noise sources enable systematic testing and validation of sensing algorithms during chip design.

A thorough understanding of ECG signal characteristics — from both the clinical and engineering perspectives — is essential for designing a pacemaker chip that reliably senses, discriminates, and responds to the full spectrum of cardiac electrical activity.

---

## References

1. Einthoven W. "Über die Richtung und die mechanische Bedeutung der Herzaktionsschwankungen." *Archiv für die gesamte Physiologie*. 1908;122:517-548.
2. Mason JW, et al. "AHA/ACCF/HRS recommendations for the standardization and interpretation of the electrocardiogram." *Circulation*. 2007;115(9):1306-1324.
3. Scher AM. "The electrocardiogram." In: *Medical Physiology*. Boron WF, Boulpaep EL, eds. Elsevier; 2017.
4. Webster JG. *Medical Instrumentation: Application and Design*. 5th ed. Wiley; 2020.
5. Webster JG. *Design of Cardiac Pacemakers*. IEEE Press; 1995.
6. Kazui T, et al. "ECG signal processing for pacemaker applications." In: *Biomedical Signal Processing*. Springer; 2019.
7. IEC 60601-1:2012. Medical electrical equipment — Part 1: General requirements for basic safety and essential performance.
8. IEC 60601-2-25:2011. Particular requirements for the basic safety and essential performance of electrocardiographs.
9. ANSI/AAMI EC11:1991/(R)2001/(R)2007. Diagnostic electrocardiographic devices.
10. ISO 14708-1:2014. Implants for surgery — Active implantable medical devices — Part 1: General requirements for safety, marking and for information to be provided by the manufacturer.
11. Pahlm O, et al. *Concise Guide to Cardiac Arrhythmias*. 2nd ed. Blackwell Publishing; 2007.
12. Sörnmo L, Laguna P. *Bioelectrical Signal Processing in Cardiac and Neurological Applications*. Elsevier Academic Press; 2005.
13. Clifford GD, Azuaje F, McSharry PE, eds. *Advanced Methods and Tools for ECG Data Analysis*. Artech House; 2006.
14. Kligfield P, et al. "Recommendations for the standardization and interpretation of the electrographiogram." *J Am Coll Cardiol*. 2007;49(10):1109-1127.
15. Rautaharju PM, et al. "AHA/ACCF/HRS recommendations for the standardization and interpretation of the electrocardiogram: part IV." *Circulation*. 2009;119(10):e241-e250.
