# Intrinsic Cardiac Signal Sensing

## 2.2.1 Intrinsic Cardiac Signal Sensing

### 2.2.1.1 Cardiac Signal Characteristics

Understanding the characteristics of intrinsic cardiac signals is fundamental to
designing the sensing front-end. The signals vary widely in amplitude, frequency
content, and morphology depending on the recording site, lead type, and patient
pathology.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    CARDIAC SIGNAL CHARACTERISTICS                            │
│                                                                             │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │                                                                      │   │
│  │  SIGNAL TYPE    AMPLITUDE        FREQUENCY        DURATION          │   │
│  │  ─────────────────────────────────────────────────────────────────  │   │
│  │                                                                      │   │
│  │  P-wave         0.2 - 3.0 mV     0.5 - 50 Hz     60 - 120 ms      │   │
│  │  (Atrial)       (typ: 0.5-1.5)   (peak ~10 Hz)                     │   │
│  │                                                                      │   │
│  │  QRS complex    2.0 - 20.0 mV    10 - 100 Hz     60 - 120 ms      │   │
│  │  (Ventricular)  (typ: 5-15)      (peak ~25 Hz)                     │   │
│  │                                                                      │   │
│  │  T-wave         0.1 - 5.0 mV     0.5 - 10 Hz     100 - 300 ms     │   │
│  │  (Ventricular)  (typ: 0.5-2)     (peak ~2 Hz)                      │   │
│  │                                                                      │   │
│  │  U-wave         0.05 - 0.3 mV    0.5 - 5 Hz      20 - 40 ms       │   │
│  │  (Optional)     (rarely seen)                                       │   │
│  │                                                                      │   │
│  │  Atrial         2.0 - 10.0 mV    10 - 100 Hz     20 - 50 ms       │   │
│  │  electrogram    (bipolar)        (peak ~30 Hz)                      │   │
│  │                                                                      │   │
│  │  Ventricular    5.0 - 30.0 mV    10 - 200 Hz     30 - 80 ms       │   │
│  │  electrogram    (bipolar)        (peak ~50 Hz)                      │   │
│  │                                                                      │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  TYPICAL CARDIAC SIGNAL WAVEFORMS:                                         │
│                                                                             │
│  Surface ECG (Lead II):                                                     │
│                                                                             │
│       P    QRS         T                                                    │
│       │    │           │                                                    │
│       │    │           │                                                    │
│       ┌────┐          ┌────────┐                                           │
│       │    │    ┌─────┘        └────┐                                     │
│  ─────┘    └────┘                   └─────                                │
│       │         │                   │                                      │
│       │         │                   │                                      │
│                                                                             │
│  Intracardiac Electrogram (Bipolar RV):                                    │
│                                                                             │
│       P         R                      T                                    │
│       │         │                      │                                   │
│  ~~~~~│~~~~~~~~~│~~~~~~~~~~~~~~~~~~~~~~│~~~~~  (baseline ~0.1 mV)         │
│       │         │                      │                                   │
│       └┐   ┌───┘                      │                                   │
│         └───┘                         │                                    │
│       0.5mV   10mV                   1mV                                  │
│                                                                             │
│  Intrinsic vs. Paced Signal Comparison:                                    │
│                                                                             │
│  Intrinsic QRS:    ┌──────┐                                                │
│                    │      │     (Narrow, ~80ms)                            │
│  ──────────────────┘      └───────────────                                │
│                                                                             │
│  Paced QRS:    ┌──────────────┐                                            │
│                │              │     (Wide, ~140ms)                         │
│  ──────────────┘              └───────────                                │
│                                                                             │
│  Paced T-wave:    ┌───────────────────┐                                    │
│                   │                   │  (Larger, wider)                   │
│  ─────────────────┘                   └─────                              │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 2.2.1.2 R-Wave Sensing Front-End Design

The R-wave sensing channel is the most critical, as it determines ventricular
sense timing for pacing and arrhythmia detection.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    R-WAVE SENSING CHANNEL                                    │
│                                                                             │
│  RV Lead ──┐                                                               │
│  (Tip)     │                                                               │
│            ▼                                                               │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │  STAGE 1: INPUT PROTECTION                                           │  │
│  │  ┌──────────────────────────────────────────────────────────────┐   │  │
│  │  │  • ESD clamps (bidirectional TVS)                            │   │  │
│  │  │  • DC-blocking capacitor (if unipolar)                       │   │  │
│  │  │  • Input impedance: >1 GΩ differential                       │   │  │
│  │  │  • Input capacitance: <10 pF                                 │   │  │
│  │  └──────────────────────────────────────────────────────────────┘   │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│            │                                                               │
│            ▼                                                               │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │  STAGE 2: LOW-NOISE AMPLIFIER (LNA)                                 │  │
│  │  ┌──────────────────────────────────────────────────────────────┐   │  │
│  │  │  • Topology: Chopper-stabilized folded cascode              │   │  │
│  │  │  • Gain: 40-80 dB (programmable in 6dB steps)              │   │  │
│  │  │  • Input-referred noise: <5 µVrms (0.5-100 Hz BW)         │   │  │
│  │  │  • Voltage noise density: <30 nV/√Hz @ 10 Hz              │   │  │
│  │  │  • Current noise: <0.1 pA/√Hz                              │   │  │
│  │  │  • CMRR: >80 dB @ 50/60 Hz                                 │   │  │
│  │  │  • PSRR: >60 dB                                             │   │  │
│  │  │  • THD: <-60 dB @ 10 mVpp input                             │   │  │
│  │  │  • Supply: 1.8V                                             │   │  │
│  │  │  • Power: <3 µW                                              │   │  │
│  │  └──────────────────────────────────────────────────────────────┘   │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│            │                                                               │
│            ▼                                                               │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │  STAGE 3: ANALOG FILTER                                              │  │
│  │  ┌──────────────────────────────────────────────────────────────┐   │  │
│  │  │  Type: 4th-order Butterworth bandpass                       │   │  │
│  │  │  Passband: 10 - 100 Hz (for R-wave)                        │   │  │
│  │  │  Stopband attenuation: >40 dB @ 0.5 Hz (T-wave reject)    │   │  │
│  │  │  Stopband attenuation: >40 dB @ 200 Hz (noise reject)     │   │  │
│  │  │  Implementation: Switched-capacitor (SC) filter            │   │  │
│  │  │  Clock frequency: 4.096 kHz (= 64 × 64 Hz)               │   │  │
│  │  │  Power: <2 µW                                               │   │  │
│  │  └──────────────────────────────────────────────────────────────┘   │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│            │                                                               │
│            ▼                                                               │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │  STAGE 4: THRESHOLD DETECTION                                        │  │
│  │  ┌──────────────────────────────────────────────────────────────┐   │  │
│  │  │  • Auto-adjusting threshold (AutoSense algorithm)           │   │  │
│  │  │  • Threshold = K × (recent peak amplitude)                  │   │  │
│  │  │  • K factor: 0.25 - 0.75 (programmable)                    │   │  │
│  │  │  • Blank period after detection: 200 ms                     │   │  │
│  │  │  • Refractory period: 300 ms                                │   │  │
│  │  │  • Output: Digital sense event pulse (1 ms width)          │   │  │
│  │  │  • Detection latency: <5 ms                                 │   │  │
│  │  └──────────────────────────────────────────────────────────────┘   │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│            │                                                               │
│            ▼                                                               │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │  STAGE 5: DIGITAL PROCESSING                                         │  │
│  │  ┌──────────────────────────────────────────────────────────────┐   │  │
│  │  │  • Event validation (morphology check)                      │   │  │
│  │  │  • Timing extraction (RR interval measurement)             │   │  │
│  │  │  • Rate calculation                                         │   │  │
│  │  │  • Oversensing detection                                    │   │  │
│  │  │  • Output to pacing timer and telemetry                     │   │  │
│  │  └──────────────────────────────────────────────────────────────┘   │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 2.2.1.3 P-Wave Sensing Design

P-wave sensing is more challenging than R-wave sensing due to the significantly
lower signal amplitude and higher susceptibility to far-field R-wave contamination.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    P-WAVE SENSING CHANNEL                                    │
│                                                                             │
│  CHALLENGES:                                                               │
│  ───────────                                                               │
│  1. Low amplitude: 0.2-3.0 mV (vs. 2-20 mV for R-wave)                  │
│  2. Low frequency: 0.5-50 Hz (more susceptible to baseline wander)       │
│  3. Far-field R-wave: 2-10 mV contaminant on atrial channel              │
│  4. Myopotential noise: 0.1-0.5 mV in pectoral region                    │
│  5. Atrial lead maturation: Amplitude may change over weeks/months       │
│                                                                             │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │                                                                      │  │
│  │  P-WAVE SENSING FILTER REQUIREMENTS:                                │  │
│  │                                                                      │  │
│  │  Passband: 0.5 - 50 Hz (narrower than R-wave channel)              │  │
│  │  Stopband: >30 dB rejection at 100 Hz (reject far-field R)         │  │
│  │  Filter type: 4th-order Butterworth (maximally flat passband)       │  │
│  │                                                                      │  │
│  │  Frequency Response:                                                │  │
│  │                                                                      │  │
│  │  Gain (dB)                                                           │  │
│  │   60 ┤                                                               │  │
│  │      │    ┌─────────────────────┐                                   │  │
│  │   40 ┤    │                     │                                   │  │
│  │      │    │   PASSBAND          │\                                  │  │
│  │   20 ┤    │   (0.5 - 50 Hz)     │ \                                 │  │
│  │      │    │                     │  \                                │  │
│  │    0 ┤────┤                     │   \                               │  │
│  │      │    │                     │    \──────────                   │  │
│  │  -20 ┤    │                     │                                  │  │
│  │      │    │                     │    STOPBAND                      │  │
│  │  -40 ┤    │                     │    (>30 dB @ 100 Hz)             │  │
│  │      │    │                     │                                  │  │
│  │  -60 ┤────┴─────────────────────┴──────────────────────            │  │
│  │      0.1    0.5      5      50     100     200   500   1k         │  │
│  │                    Frequency (Hz)                                  │  │
│  │                                                                      │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
│  FAR-FIELD R-WAVE REJECTION:                                              │
│  ──────────────────────────                                                │
│  The far-field R-wave appears on the atrial channel as a wide, low-       │
│  amplitude signal following the P-wave. rejection strategies:              │
│                                                                             │
│  Strategy 1: Bandpass filtering (frequency discrimination)                │
│  • P-wave energy concentrated at 5-20 Hz                                 │
│  • Far-field R energy at 10-50 Hz                                         │
│  • Limited discrimination due to overlap                                   │
│                                                                             │
│  Strategy 2: Blank/partial blank during ventricular event                │
│  • After ventricular sense/pace, blank atrial channel for 50-100 ms     │
│  • May miss late P-waves in short AV intervals                           │
│                                                                             │
│  Strategy 3: Morphology-based rejection                                   │
│  • P-wave: narrow, symmetric                                             │
│  • Far-field R: wide, often notched                                      │
│  • Requires DSP for real-time morphology analysis                        │
│                                                                             │
│  Strategy 4: Dual-sense with timing correlation                          │
│  • Require P-wave to appear within expected timing window                │
│  • RR interval correlation to reject out-of-sequence events              │
│                                                                             │
│  P-WAVE SENSING PERFORMANCE REQUIREMENTS:                                 │
│  ┌────────────────────────────┬──────────────────────────────────────┐    │
│  │ Parameter                  │ Specification                        │    │
│  ├────────────────────────────┼──────────────────────────────────────┤    │
│  │ Minimum detectable P-wave  │ 0.25 mV (2σ noise floor)           │    │
│  │ Nominal sensitivity        │ 0.5 mV (programmable 0.25-5.0)     │    │
│  │ SNR requirement            │ >10 dB                              │    │
│  │ Far-field rejection        │ >20 dB                              │    │
│  │ Myopotential rejection     │ >15 dB                              │    │
│  │ Sensing impedance range    │ 200-2000 Ω                          │    │
│  │ P-wave detection accuracy  │ ±5 ms                               │    │
│  │ P-wave undersensing rate   │ <2% (nominal signals)              │    │
│  │ P-wave oversensing rate    │ <1% (normal sinus rhythm)          │    │
│  └────────────────────────────┴──────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 2.2.1.4 T-Wave Discrimination

T-wave oversensing (TWOS) is one of the most common causes of inappropriate
pacemaker inhibition. The T-wave must be discriminated from the R-wave.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    T-WAVE DISCRIMINATION ALGORITHMS                          │
│                                                                             │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │  ALGORITHM 1: REFRACTORY PERIOD METHOD                               │  │
│  │                                                                      │  │
│  │  After R-wave detection, inhibit sensing for a fixed period:        │  │
│  │                                                                      │  │
│  │       R-wave                                                        │  │
│  │         │                                                           │  │
│  │    ┌────┘    T-wave (ignored)                                      │  │
│  │    │          │                                                     │  │
│  │  ──┤          ┌─────┐                                               │  │
│  │    │   ◄──────┤     │                                              │  │
│  │    │  Refractory                                                   │  │
│  │    │  Period (300ms)                                               │  │
│  │                                                                      │  │
│  │  Pros: Simple, reliable                                            │  │
│  │  Cons: Cannot sense events during refractory period                │  │
│  │                                                                      │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │  ALGORITHM 2: SLOPE-BASED DISCRIMINATION                             │  │
│  │                                                                      │  │
│  │  R-wave has higher dV/dt than T-wave:                               │  │
│  │                                                                      │  │
│  │  Signal:    R    T                                                   │  │
│  │            ┌┐    ┌──┐                                               │  │
│  │  ──────────┘└────┘  └──────                                        │  │
│  │                                                                      │  │
│  │  dV/dt:   ╱╲     ╱──╲                                               │  │
│  │  ────────╱  ╲───╱    ╲─────                                        │  │
│  │           │    │                                                    │  │
│  │        High  Low                                                   │  │
│  │                                                                      │  │
│  │  Implementation:                                                    │  │
│  │  • Compute dV/dt using digital differentiator                      │  │
│  │  • R-wave: dV/dt > 500 mV/s                                       │  │
│  │  • T-wave: dV/dt < 100 mV/s                                       │  │
│  │  • Apply hysteresis to prevent oscillation                         │  │
│  │                                                                      │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │  ALGORITHM 3: AMPLITUDE-BASED DISCRIMINATION                         │  │
│  │                                                                      │  │
│  │  T-wave amplitude is typically <30% of R-wave amplitude:           │  │
│  │                                                                      │  │
│  │  Peak detection:                                                    │  │
│  │  • Store peak amplitude of last R-wave (A_R)                       │  │
│  │  • T-wave threshold: A_T = K_T × A_R (K_T = 0.3)                  │  │
│  │  • Events below A_T are classified as T-waves                      │  │
│  │                                                                      │  │
│  │  Limitation: Fails when T-wave amplitude approaches R-wave         │  │
│  │  (e.g., hyperkalemia, certain cardiomyopathies)                     │  │
│  │                                                                      │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │  ALGORITHM 4: COMBINED APPROACH (RECOMMENDED)                        │  │
│  │                                                                      │  │
│  │  ┌──────────────────────────────────────────────────────────────┐   │  │
│  │  │  Stage 1: Refractory Period (300 ms)                        │   │  │
│  │  │  Stage 2: Slope check (dV/dt > threshold)                   │   │  │
│  │  │  Stage 3: Amplitude check (peak > threshold)                │   │  │
│  │  │  Stage 4: Timing check (RR interval within range)           │   │  │
│  │  │  Stage 5: Morphology check (if DSP available)               │   │  │
│  │  │                                                              │   │  │
│  │  │  ALL stages must pass for valid R-wave detection             │   │  │
│  │  └──────────────────────────────────────────────────────────────┘   │  │
│  │                                                                      │  │
│  │  Performance:                                                       │  │
│  │  • TWOS rejection: >99%                                             │  │
│  │  • R-wave detection: >99.5%                                         │  │
│  │  • Processing latency: <10 ms                                       │  │
│  │                                                                      │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 2.2.1.5 Blanking and Refractory Periods

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    BLANKING AND REFRACTORY PERIODS                           │
│                                                                             │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │                                                                      │  │
│  │  TERMINOLOGY:                                                        │  │
│  │  ─────────────                                                       │  │
│  │  • Blanking Period: Sensing amplifier is shut off (input grounded)  │  │
│  │  • Refractory Period: Sensing active but events are ignored        │  │
│  │  • Both serve to prevent inappropriate sensing                      │  │
│  │                                                                      │  │
│  │  VENTRICULAR TIMING:                                                │  │
│  │                                                                      │  │
│  │       VS/VP                                                         │  │
│  │         │                                                           │  │
│  │    ┌────┘                                                           │  │
│  │    │                                                                │  │
│  │    │  ◄──── Blank ────► ◄──── Refractory ────► ◄── Sensing ──►   │  │
│  │    │                                                                │  │
│  │    ├──────────┼──────────────────────┼─────────────────────────────┤  │
│  │    0         100ms                  300ms                        860ms│  │
│  │    │                                                                │  │
│  │    │  Blank (100ms): Absorbs pacing artifact, afterpotential       │  │
│  │    │  Refractory (200ms): Ignores T-wave, allows noise detection   │  │
│  │    │  Sensing window (560ms): Active sensing for next event        │  │
│  │                                                                      │  │
│  │                                                                      │  │
│  │  ATRIAL TIMING:                                                     │  │
│  │                                                                      │  │
│  │       AS/AP                                                         │  │
│  │         │                                                           │  │
│  │    ┌────┘                                                           │  │
│  │    │                                                                │  │
│  │    │  ◄─ Blank ─► ◄─── Refractory ───► ◄──── Sensing ──────────►  │  │
│  │    │                                                                │  │
│  │    ├──────────┼──────────────────────┼─────────────────────────────┤  │
│  │    0         50ms                   200ms                       860ms│  │
│  │    │                                                                │  │
│  │    │  Blank (50ms): Absorbs pacing artifact                        │  │
│  │    │  Refractory (150ms): Prevents far-field R-wave sensing        │  │
│  │    │  Sensing window (660ms): Active sensing for next P-wave       │  │
│  │                                                                      │  │
│  │                                                                      │  │
│  │  POST-VENTRICULAR ATRIAL BLANKING (PVAB):                           │  │
│  │                                                                      │  │
│  │  After a ventricular event, the atrial channel is blanked:          │  │
│  │                                                                      │  │
│  │  VP/VS                                                              │  │
│  │   │                                                                 │  │
│  │   ├──┐  ◄─ PVAB ─►                                                 │  │
│  │   │  │  (100ms)                                                     │  │
│  │   │  │  Prevents far-field R-wave sensing on atrial channel        │  │
│  │   │                                                                 │  │
│  │                                                                      │  │
│  │  POST-PACE REPOLARIZATION BLANKING:                                 │  │
│  │                                                                      │  │
│  │  After atrial/ventricular pace, additional blanking:                │  │
│  │  • Atrial pace: 50 ms additional blank                              │  │
│  │  • Ventricular pace: 100 ms additional blank                        │  │
│  │                                                                      │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
│  BLANKING PERIOD SUMMARY TABLE:                                            │
│  ┌─────────────────────────┬──────────┬──────────┬──────────────────────┐  │
│  │ Period                  │ Minimum  │ Typical  │ Maximum              │  │
│  ├─────────────────────────┼──────────┼──────────┼──────────────────────┤  │
│  │ Vent. Blank             │ 50 ms    │ 100 ms   │ 200 ms               │  │
│  │ Vent. Refractory        │ 150 ms   │ 300 ms   │ 500 ms               │  │
│  │ Atrial Blank            │ 25 ms    │ 50 ms    │ 100 ms               │  │
│  │ Atrial Refractory       │ 100 ms   │ 200 ms   │ 400 ms               │  │
│  │ PVAB                    │ 50 ms    │ 100 ms   │ 400 ms               │  │
│  │ Post-pace Blank (A)     │ 25 ms    │ 50 ms    │ 100 ms               │  │
│  │ Post-pace Blank (V)     │ 50 ms    │ 100 ms   │ 200 ms               │  │
│  └─────────────────────────┴──────────┴──────────┴──────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 2.2.1.6 Sensitivity Settings and AutoSense

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    SENSITIVITY SETTINGS AND AUTOSENSE                        │
│                                                                             │
│  SENSITIVITY DEFINITION:                                                   │
│  ───────────────────────                                                   │
│  Sensitivity is the minimum signal amplitude that triggers a sense event.  │
│  Lower sensitivity value = MORE sensitive (detects smaller signals)        │
│                                                                             │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │                                                                      │  │
│  │  FIXED SENSITIVITY MODE:                                             │  │
│  │                                                                      │  │
│  │  User sets fixed threshold:                                         │  │
│  │  • R-wave: 0.5 - 5.0 mV (typical: 2.0 mV)                        │  │
│  │  • P-wave: 0.25 - 5.0 mV (typical: 0.5 mV)                       │  │
│  │                                                                      │  │
│  │  Signal ──────┐                                                     │  │
│  │               │                                                     │  │
│  │               ┌───┐  ┌───┐  ┌───┐                                  │  │
│  │               │   │  │   │  │   │                                  │  │
│  │  ─────────────┘   └──┘   └──┘   └─────                            │  │
│  │                                                                      │  │
│  │  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ Threshold (2.0 mV)        │  │
│  │                                                                      │  │
│  │  Sense events:  ✓        ✓        ✓                                │  │
│  │                                                                      │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │                                                                      │  │
│  │  AUTOSENSE (AUTO-ADJUSTING SENSITIVITY):                            │  │
│  │                                                                      │  │
│  │  Threshold automatically adjusts based on recent signal amplitude:  │  │
│  │                                                                      │  │
│  │  Signal ──────┐                                                     │  │
│  │               │                                                     │  │
│  │               ┌───┐  ┌───┐  ┌───┐  ┌───┐  ┌───┐                  │  │
│  │               │   │  │   │  │   │  │   │  │   │                  │  │
│  │  ─────────────┘   └──┘   └──┘   └──┘   └──┘   └────             │  │
│  │                                                                      │  │
│  │  Threshold:  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─                │  │
│  │              (tracks peak with decay)                               │  │
│  │                                                                      │  │
│  │  Algorithm:                                                         │  │
│  │  1. After sense event, store peak amplitude (A_peak)               │  │
│  │  2. Set threshold = K × A_peak (K = 0.25-0.75)                   │  │
│  │  3. Decay threshold by factor D every decay time (T_decay)         │  │
│  │     New threshold = threshold × D                                  │  │
│  │  4. Decay until minimum threshold reached                          │  │
│  │                                                                      │  │
│  │  Typical values:                                                    │  │
│  │  • K factor: 0.5 (50% of peak)                                    │  │
│  │  • Decay factor D: 0.9375 (1/16 decrement)                        │  │
│  │  • Decay time T_decay: 8 seconds                                   │  │
│  │  • Minimum threshold: 0.25 mV (R-wave), 0.125 mV (P-wave)       │  │
│  │                                                                      │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
│  AUTOSENSE STATE MACHINE:                                                 │
│                                                                             │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │                                                                      │  │
│  │       ┌──────────┐                                                  │  │
│  │   ┌───│  SENSING  │◄──────────────────────────┐                    │  │
│  │   │   │  (Active) │                           │                    │  │
│  │   │   └─────┬────┘                           │                    │  │
│  │   │         │                                │                    │  │
│  │   │    Sense event                      No event for              │  │
│  │   │         │                           N cycles                  │  │
│  │   │         ▼                                │                    │  │
│  │   │   ┌──────────┐                    ┌──────┴─────┐             │  │
│  │   │   │  DETECT   │                    │  DECREASE   │             │  │
│  │   │   │  (Validate│                    │  SENSITIVITY│             │  │
│  │   │   │  event)   │                    │  (Lower K)  │             │  │
│  │   │   └─────┬────┘                    └──────┬─────┘             │  │
│  │   │         │                                │                    │  │
│  │   │    Valid                              Increased               │  │
│  │   │    event                              sensitivity            │  │
│  │   │         │                                │                    │  │
│  │   │         ▼                                │                    │  │
│  │   │   ┌──────────┐                          │                    │  │
│  │   │   │  UPDATE   │                          │                    │  │
│  │   │   │  THRESHOLD│                          │                    │  │
│  │   │   │  A_peak→  │                          │                    │  │
│  │   │   │  threshold│                          │                    │  │
│  │   │   └─────┬────┘                          │                    │  │
│  │   │         │                                │                    │  │
│  │   │         └────────────────────────────────┘                    │  │
│  │   │                                                                │  │
│  │   │   Noise event (oversensing)                                   │  │
│  │   │         │                                                     │  │
│  │   │         ▼                                                     │  │
│  │   │   ┌──────────┐                                                │  │
│  │   │   │  INCREASE │                                                │  │
│  │   │   │  THRESHOLD│                                                │  │
│  │   │   │  (More    │                                                │  │
│  │   │   │  rejective)│                                               │  │
│  │   │   └─────┬────┘                                                │  │
│  │   │         │                                                     │  │
│  │   └─────────┘                                                     │  │
│  │                                                                      │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 2.2.1.7 SNR and Noise Analysis

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    SIGNAL-TO-NOISE RATIO ANALYSIS                           │
│                                                                             │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │                                                                      │  │
│  │  NOISE SOURCES IN SENSING CHANNEL:                                   │  │
│  │                                                                      │  │
│  │  ┌──────────────────────────────────────────────────────────────┐   │  │
│  │  │ 1. ELECTRODE-FLUID NOISE (Johnson noise)                    │   │  │
│  │  │    • Source: Thermal noise at electrode-tissue interface     │   │  │
│  │  │    • Magnitude: ~1-5 µVrms                                   │   │  │
│  │  │    • Frequency: White (flat spectrum)                        │   │  │
│  │  │    • Formula: V_n = √(4kTRΔf)                              │   │  │
│  │  │      where R = lead impedance, Δf = bandwidth               │   │  │
│  │  │                                                              │   │  │
│  │  │ 2. AMPLIFIER NOISE (LNA)                                    │   │  │
│  │  │    • Source: Flicker (1/f) + thermal noise in MOSFETs       │   │  │
│  │  │    • Magnitude: ~2-5 µVrms (input-referred)                │   │  │
│  │  │    • 1/f corner: ~1-10 kHz (depends on process)            │   │  │
│  │  │    • Chopper stabilization reduces 1/f noise                │   │  │
│  │  │                                                              │   │  │
│  │  │ 3. ELECTROMYOGRAPHIC (EMG) NOISE                            │   │  │
│  │  │    • Source: Pectoral muscle activity                       │   │  │
│  │  │    • Magnitude: ~0.1-0.5 mV (near pectoral implant)       │   │  │
│  │  │    • Frequency: 20-500 Hz                                   │   │  │
│  │  │    • Intermittent (movement-dependent)                      │   │  │
│  │  │                                                              │   │  │
│  │  │ 4. 50/60 Hz POWER LINE INTERFERENCE                        │   │  │
│  │  │    • Source: External electromagnetic coupling              │   │  │
│  │  │    • Magnitude: ~0.01-0.1 mV                               │   │  │
│  │  │    • Frequency: 50 Hz or 60 Hz (narrowband)               │   │  │
│  │  │    • Rejection: CMRR + notch filter                        │   │  │
│  │  │                                                              │   │  │
│  │  │ 5. DIGITAL SWITCHING NOISE                                  │   │  │
│  │  │    • Source: On-chip digital circuits coupling to analog    │   │  │
│  │  │    • Magnitude: ~0.5-2 µV (at LNA input)                  │   │  │
│  │  │    • Frequency: Clock harmonics                            │   │  │
│  │  │    • Mitigation: Layout isolation, decoupling              │   │  │
│  │  │                                                              │   │  │
│  │  │ 6. LEAD NOISE (Motion artifact)                            │   │  │
│  │  │    • Source: Lead conductor motion in tissue               │   │  │
│  │  │    • Magnitude: ~0.1-1.0 mV (acute, decreases over time) │   │  │
│  │  │    • Frequency: 0.1-10 Hz                                  │   │  │
│  │  │    • Mitigation: Lead maturation period, filtering        │   │  │
│  │  │                                                              │   │  │
│  │  └──────────────────────────────────────────────────────────────┘   │  │
│  │                                                                      │  │
│  │  TOTAL NOISE BUDGET (R-wave channel, 10-100 Hz BW):                │  │
│  │                                                                      │  │
│  │  ┌──────────────────────────┬────────────────────────────────┐     │  │
│  │  │ Noise Source             │ Contribution (µVrms)           │     │  │
│  │  ├──────────────────────────┼────────────────────────────────┤     │  │
│  │  │ Electrode (500Ω load)   │ 0.9                            │     │  │
│  │  │ LNA (input-referred)    │ 3.0                            │     │  │
│  │  │ Filter + ADC quantization│ 0.5                           │     │  │
│  │  │ Digital coupling         │ 0.5                            │     │  │
│  │  │ 50/60 Hz (after CMRR)  │ 0.3                            │     │  │
│  │  │ ────────────────────────│───────────────────────────────│     │  │
│  │  │ RSS Total               │ 3.3 µVrms                      │     │  │
│  │  └──────────────────────────┴────────────────────────────────┘     │  │
│  │                                                                      │  │
│  │  SNR CALCULATION:                                                   │  │
│  │                                                                      │  │
│  │  SNR = 20 × log₁₀(V_signal / V_noise)                            │  │
│  │                                                                      │  │
│  │  For R-wave (5 mV): SNR = 20 × log₁₀(5000/3.3) = 63.6 dB        │  │
│  │  For P-wave (0.5 mV): SNR = 20 × log₁₀(500/3.3) = 43.6 dB       │  │
│  │                                                                      │  │
│  │  Minimum SNR for reliable sensing: >10 dB                          │  │
│  │  Design margin: >20 dB                                              │  │
│  │                                                                      │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 2.2.1.8 Far-Field Rejection Techniques

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    FAR-FIELD REJECTION TECHNIQUES                           │
│                                                                             │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │                                                                      │  │
│  │  TECHNIQUE 1: BIPOLAR SENSING                                        │  │
│  │  ─────────────────────────────                                       │  │
│  │                                                                      │  │
│  │  Unipolar: Tip-to-Can (large pickup area)                          │  │
│  │  ┌────────────────────────────────────────────────────────┐        │  │
│  │  │         ┌──────┐                                       │        │  │
│  │  │  Tip ───┤      ├─── Can (large area)                   │        │  │
│  │  │         │ Heart│        ┌──────────┐                   │        │  │
│  │  │         └──────┘        │  Can     │                   │        │  │
│  │  │                         └──────────┘                   │        │  │
│  │  │  Pickup area: Large (includes chest cavity)            │        │  │
│  │  │  Far-field rejection: Poor (~10 dB)                    │        │  │
│  │  └────────────────────────────────────────────────────────┘        │  │
│  │                                                                      │  │
│  │  Bipolar: Tip-to-Ring (small pickup area)                          │  │
│  │  ┌────────────────────────────────────────────────────────┐        │  │
│  │  │         ┌──────┐                                       │        │  │
│  │  │  Tip ───┤      ├─── Ring (2mm from tip)                │        │  │
│  │  │         │ Heart│        (close spacing)                 │        │  │
│  │  │         └──────┘                                       │        │  │
│  │  │  Pickup area: Small (localized to electrode tips)     │        │  │
│  │  │  Far-field rejection: Good (~20-30 dB)                 │        │  │
│  │  └────────────────────────────────────────────────────────┘        │  │
│  │                                                                      │  │
│  │  RECOMMENDATION: Always use bipolar sensing for dual-chamber       │  │
│  │  pacemakers to minimize far-field R-wave sensing on atrial channel│  │
│  │                                                                      │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │                                                                      │  │
│  │  TECHNIQUE 2: NOTCH FILTERING                                        │  │
│  │  ─────────────────────────────                                       │  │
│  │                                                                      │  │
│  │  50/60 Hz notch filter (programmable):                              │  │
│  │                                                                      │  │
│  │  Gain (dB)                                                           │  │
│  │    0 ┤──────────────────────╲   ╱──────────────────                 │  │
│  │      │                       ╲ ╱                                     │  │
│  │  -10 ┤                        │                                      │  │
│  │      │                        │                                      │  │
│  │  -20 ┤                        │                                      │  │
│  │      │                        │                                      │  │
│  │  -30 ┤                        │                                      │  │
│  │      │                        │                                      │  │
│  │  -40 ┤────────────────────────┴────────────────────                 │  │
│  │      40    45   48  49 50 51  52  55   60   70   80               │  │
│  │                    Frequency (Hz)                                    │  │
│  │                                                                      │  │
│  │  Implementation: SC (switched-capacitor) notch filter              │  │
│  │  Q-factor: 10-50 (programmable)                                    │  │
│  │  Notch depth: >40 dB                                               │  │
│  │                                                                      │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │                                                                      │  │
│  │  TECHNIQUE 3: CMRR OPTIMIZATION                                      │  │
│  │  ──────────────────────────────                                      │  │
│  │                                                                      │  │
│  │  Common-Mode Rejection Ratio (CMRR) = 20 log₁₀(Ad/Acm)           │  │
│  │                                                                      │  │
│  │  Sources of CMRR degradation:                                       │  │
│  │  • Resistor mismatch in feedback network                           │  │
│  │  • Capacitor mismatch in SC filter                                  │  │
│  │  • Parasitic capacitance imbalance                                 │  │
│  │                                                                      │  │
│  │  Improvement techniques:                                            │  │
│  │  • Chopper stabilization: >80 dB CMRR                             │  │
│  │  • Auto-zeroing: >70 dB CMRR                                      │  │
│  │  • Layout symmetry: Critical for matching                          │  │
│  │  • Guard rings: Reduce substrate coupling                          │  │
│  │                                                                      │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │                                                                      │  │
│  │  TECHNIQUE 4: MORPHOLOGY-BASED DISCRIMINATION                        │  │
│  │  ─────────────────────────────────────────────                       │  │
│  │                                                                      │  │
│  │  Waveform template matching:                                        │  │
│  │                                                                      │  │
│  │  P-wave template:        Far-field R template:                      │  │
│  │       ┌──┐                     ┌──────┐                             │  │
│  │       │  │                     │      │                             │  │
│  │  ─────┘  └─────           ─────┘      └──────                      │  │
│  │  (narrow, symmetric)      (wide, often notched)                    │  │
│  │                                                                      │  │
│  │  Cross-correlation coefficient (ρ):                                 │  │
│  │  • P-wave: ρ > 0.8 (high correlation with template)               │  │
│  │  • Far-field R: ρ < 0.5 (low correlation)                         │  │
│  │  • Threshold: ρ > 0.6 for valid P-wave                            │  │
│  │                                                                      │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 2.2.1.9 Sensing Performance Specifications Summary

| Parameter                    | Atrial Channel | Ventricular Channel | Unit   |
|------------------------------|----------------|---------------------|--------|
| Minimum detectable signal    | 0.25           | 2.0                 | mV     |
| Nominal sensitivity setting  | 0.5            | 2.0                 | mV     |
| Sensitivity range            | 0.25–5.0       | 0.5–10.0            | mV     |
| Sensitivity steps            | 0.25           | 0.5                 | mV     |
| Input impedance              | >1             | >1                  | GΩ     |
| Input capacitance            | <10            | <10                 | pF     |
| CMRR                         | >80            | >80                 | dB     |
| PSRR                         | >60            | >60                 | dB     |
| Input-referred noise         | <5             | <5                  | µVrms  |
| Voltage noise density (10Hz) | <30            | <30                 | nV/√Hz |
| Passband (lower)             | 0.5            | 10                  | Hz     |
| Passband (upper)             | 50             | 100                 | Hz     |
| Stopband attenuation         | >40            | >40                 | dB     |
| Blank period                 | 50             | 100                 | ms     |
| Refractory period            | 200            | 300                 | ms     |
| AutoSense K-factor           | 0.5            | 0.5                 | —      |
| Decay time                   | 8              | 8                   | s      |
| Minimum threshold            | 0.125          | 0.25                | mV     |
| Detection latency            | <5             | <5                  | ms     |
| Maximum heart rate           | 250            | 250                 | bpm    |
| Sensing impedance range      | 200–2000       | 200–2000            | Ω      |
| Far-field rejection          | >20            | N/A                 | dB     |
| T-wave rejection             | N/A            | >99                 | %      |
| Power per channel            | <5             | <5                  | µW     |

---

*Section 2.2.1 — Intrinsic Cardiac Signal Sensing*
*Next: Section 2.2.2 — Pacing Pulse Generation*
