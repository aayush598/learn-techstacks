# Multi-Chamber Pacing

## 2.2.4 Multi-Chamber Pacing

### 2.2.4.1 Pacing Mode Nomenclature (NBG Code)

The North American Society of Pacing and Electrophysiology (NASPE) and British
Pacing and Electrophysiology Group (BPEG) coding system defines pacemaker modes
using a standardized 5-letter code.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    NBG PACING MODE CODE                                      │
│                                                                             │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │                                                                      │  │
│  │  FORMAT: 1-2-3-4-5                                                   │  │
│  │                                                                      │  │
│  │  Position 1: Chamber Paced                                           │  │
│  │  ─────────────────────────                                           │  │
│  │  O = None (no pacing)                                                │  │
│  │  A = Atrium                                                          │  │
│  │  V = Ventricle                                                       │  │
│  │  D = Dual (A + V)                                                   │  │
│  │                                                                      │  │
│  │  Position 2: Chamber Sensed                                          │  │
│  │  ──────────────────────────                                          │  │
│  │  O = None (no sensing)                                               │  │
│  │  A = Atrium                                                          │  │
│  │  V = Ventricle                                                       │  │
│  │  D = Dual (A + V)                                                   │  │
│  │                                                                      │  │
│  │  Position 3: Response to Sensing                                     │  │
│  │  ─────────────────────────────                                       │  │
│  │  O = None (no response to sensing)                                   │  │
│  │  I = Inhibited (pace inhibited by sensed event)                      │  │
│  │  T = Triggered (sense triggers pace)                                 │  │
│  │  D = Dual (I + T)                                                   │  │
│  │                                                                      │  │
│  │  Position 4: Rate Response                                           │  │
│  │  ────────────────────────                                            │  │
│  │  O = No rate response (fixed rate)                                   │  │
│  │  R = Rate responsive (sensor-driven rate adjustment)                 │  │
│  │                                                                      │  │
│  │  Position 5: Multi-Site Pacing                                       │  │
│  │  ───────────────────────────                                         │  │
│  │  O = No multi-site pacing                                            │  │
│  │  A = Multi-site atrial pacing                                        │  │
│  │  V = Multi-site ventricular pacing (biventricular)                  │  │
│  │  D = Multi-site dual chamber pacing                                 │  │
│  │                                                                      │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
│  COMMON PACING MODES:                                                      │
│  ┌──────┬────────────────────────────────────────────────────────────┐    │
│  │ Mode │ Description                                                │    │
│  ├──────┼────────────────────────────────────────────────────────────┤    │
│  │ ODO  │ Monitor only (no pacing, no sensing response)             │    │
│  │ AAI  │ Atrial paced, atrial sensed, inhibited response          │    │
│  │ AAIR │ AAI + rate response                                      │    │
│  │ VVI  │ Ventricular paced, ventricular sensed, inhibited          │    │
│  │ VVIR │ VVI + rate response                                      │    │
│  │ DDD  │ Dual paced, dual sensed, dual response (inhibit+trigger)│    │
│  │ DDDR │ DDD + rate response                                      │    │
│  │ VOO  │ Ventricular asynchronous (no sensing)                    │    │
│  │ AOO  │ Atrial asynchronous (no sensing)                         │    │
│  │ DOO  │ Dual asynchronous (no sensing)                           │    │
│  │ VVT  │ Ventricular triggered (test mode)                        │    │
│  │ VAT  │ Atrial sensed → ventricular triggered (obsolete)         │    │
│  └──────┴────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 2.2.4.2 Mode-Specific Timing Cycles

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    MODE-SPECIFIC TIMING CYCLES                               │
│                                                                             │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │                                                                      │  │
│  │  VVI MODE TIMING:                                                   │  │
│  │  ────────────────                                                   │  │
│  │                                                                      │  │
│  │  VS = Ventricular Sense    VP = Ventricular Pace                    │  │
│  │                                                                      │  │
│  │  VS           VP           VP           VS           VP            │  │
│  │   │            │            │            │            │             │  │
│  │   ┌────────────┐            ┌────────────┐            ┌──────      │  │
│  │   │            │            │            │            │             │  │
│  │ ──┘            └────────────┘            └────────────┘             │  │
│  │   │            │            │            │            │             │  │
│  │   ◄── LRI ───►│            ◄── LRI ───►│            ◄── LRI ──►  │  │
│  │   (escape      │            (escape      │            (escape       │  │
│  │    interval)   │            interval)   │            interval)     │  │
│  │                                                                      │  │
│  │  Timing Rules:                                                      │  │
│  │  • If no sensed event within LRI → deliver VP (escape interval)   │  │
│  │  • If sensed event (VS) → reset LRI timer, inhibit pacing         │  │
│  │  • LRI = 60,000 / LRL (ms), where LRL = lower rate limit (ppm)  │  │
│  │                                                                      │  │
│  │  Example (LRL = 60 ppm):                                           │  │
│  │  • LRI = 60,000 / 60 = 1000 ms                                    │  │
│  │  • If no R-wave detected for 1000 ms → pace V                    │  │
│  │                                                                      │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │                                                                      │  │
│  │  DDD MODE TIMING:                                                   │  │
│  │  ────────────────                                                   │  │
│  │                                                                      │  │
│  │  AS = Atrial Sense    AP = Atrial Pace                              │  │
│  │  VS = Ventricular Sense    VP = Ventricular Pace                    │  │
│  │                                                                      │  │
│  │  AS     VP      AS     VP      AS     VP      AP     VP           │  │
│  │   │      │       │      │       │      │       │      │            │  │
│  │   │  ┌───┤       │  ┌───┤       │  ┌───┤   ┌───┤  ┌───┤            │  │
│  │   │  │AVD│       │  │AVD│       │  │AVD│   │AVD│  │AVD│            │  │
│  │   └──┘   └───    └──┘   └───    └──┘   └───┘   └──┘   └───       │  │
│  │   │      │       │      │       │      │       │      │            │  │
│  │   ◄─VA──►│       ◄─VA──►│       ◄─VA──►│       ◄─VA──►│           │  │
│  │    interval      interval      interval      interval              │  │
│  │                                                                      │  │
│  │  Timing Rules:                                                      │  │
│  │  1. VA interval: After VS/VP, wait VA interval before next AP/AS │  │
│  │  2. AV delay: After AS/AP, wait AV delay before next VP          │  │
│  │  3. VA interval = LRI - AV delay                                   │  │
│  │  4. Total cycle: VA + AV delay = LRI                              │  │
│  │                                                                      │  │
│  │  Example (LRL = 60 ppm, AV delay = 200 ms):                       │  │
│  │  • LRI = 1000 ms                                                   │  │
│  │  • VA interval = 1000 - 200 = 800 ms                              │  │
│  │  • Sequence: VS → wait 800ms → AP → wait 200ms → VP             │  │
│  │                                                                      │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │                                                                      │  │
│  │  AAI MODE TIMING:                                                   │  │
│  │  ────────────────                                                   │  │
│  │                                                                      │  │
│  │  AS     AP      AS     AP      AS     AP      AS     AP           │  │
│  │   │      │       │      │       │      │       │      │            │  │
│  │   │      │       │      │       │      │       │      │            │  │
│  │ ──┘      └───    └──┘   └───    └──┘   └───    └──┘   └───       │  │
│  │   │      │       │      │       │      │       │      │            │  │
│  │   ◄─LRI─►│       ◄─LRI─►│       ◄─LRI─►│       ◄─LRI─►│           │  │
│  │                                                                      │  │
│  │  Timing Rules:                                                      │  │
│  │  • If no P-wave sensed within LRI → deliver AP                    │  │
│  │  • If P-wave sensed (AS) → reset LRI, inhibit pacing             │  │
│  │  • No AV delay (single-chamber atrial pacing)                     │  │
│  │                                                                      │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │                                                                      │  │
│  │  DDDR MODE TIMING:                                                  │  │
│  │  ──────────────────                                                  │  │
│  │                                                                      │  │
│  │  Same as DDD, but LRI is adjusted by sensor:                       │  │
│  │                                                                      │  │
│  │  LRI = min(LRI_sensor, LRI_LRL)                                    │  │
│  │                                                                      │  │
│  │  Where:                                                              │  │
│  │  • LRI_sensor = 60,000 / SIR (sensor-indicated rate)              │  │
│  │  • LRI_LRL = 60,000 / LRL (lower rate limit)                     │  │
│  │  • SIR is determined by activity sensor (accelerometer)            │  │
│  │                                                                      │  │
│  │  Sensor Response Curve:                                             │  │
│  │                                                                      │  │
│  │  SIR (ppm)                                                           │  │
│  │    │                                                                 │  │
│  │ 120┤                              ╱──────── URL                    │  │
│  │    │                             ╱                                  │  │
│  │ 110┤                            ╱                                   │  │
│  │    │                           ╱                                    │  │
│  │ 100┤                          ╱                                     │  │
│  │    │                         ╱                                      │  │
│  │  90┤                        ╱                                       │  │
│  │    │                       ╱                                        │  │
│  │  80┤                      ╱                                         │  │
│  │    │                     ╱                                          │  │
│  │  70┤────────────────────╱─────── LRL                               │  │
│  │    │                   ╱                                            │  │
│  │  60┤                  ╱                                             │  │
│  │    └──────┼──────┼──────┼──────┼──────┼──────▶                     │  │
│  │           1      2      3      4      5    Activity Level (g)      │  │
│  │                                                                      │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 2.2.4.3 AV Delay and VA Interval Management

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    AV DELAY AND VA INTERVAL MANAGEMENT                       │
│                                                                             │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │                                                                      │  │
│  │  AV DELAY PARAMETERS:                                                │  │
│  │                                                                      │  │
│  │  • Programmed AV delay: Fixed value (e.g., 200 ms)                 │  │
│  │  • Sensor-indicated AV delay: Adjusts with sensor rate             │  │
│  │  • Rate-adaptive AV delay: Shortens at higher rates                │  │
│  │  • Dynamic AV delay: Automatically adjusts based on intrinsic AV   │  │
│  │                                                                      │  │
│  │  RATE-ADAPTIVE AV DELAY:                                             │  │
│  │                                                                      │  │
│  │  AV_delay = AV_min + (AV_max - AV_min) × (1 - (SIR-LRL)/(URL-LRL))│  │
│  │                                                                      │  │
│  │  Example:                                                           │  │
│  │  • AV_max = 300 ms (at LRL = 60 ppm)                              │  │
│  │  • AV_min = 120 ms (at URL = 120 ppm)                             │  │
│  │  • At SIR = 90 ppm: AV = 120 + (300-120) × (1 - 30/60) = 210 ms │  │
│  │                                                                      │  │
│  │  AV DELAY RATE RESPONSE CURVE:                                      │  │
│  │                                                                      │  │
│  │  AV Delay                                                           │  │
│  │  (ms)                                                                │  │
│  │    │                                                                 │  │
│  │  300┤────────────╲                                                  │  │
│  │     │             ╲                                                 │  │
│  │  250┤              ╲                                                │  │
│  │     │               ╲                                               │  │
│  │  200┤                ╲                                              │  │
│  │     │                 ╲                                             │  │
│  │  150┤                  ╲                                            │  │
│  │     │                   ╲                                           │  │
│  │  120┤────────────────────╲────── AV_min                            │  │
│  │     │                     ╲                                         │  │
│  │     └──────┼──────┼──────┼──────┼──────▶                           │  │
│  │            60     80    100    120     Sensor Rate (ppm)           │  │
│  │                                                                      │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │                                                                      │  │
│  │  VA INTERVAL MANAGEMENT:                                             │  │
│  │                                                                      │  │
│  │  VA interval = LRI - AV delay                                       │  │
│  │                                                                      │  │
│  │  For rate-adaptive modes:                                            │  │
│  │  VA_interval = (60,000 / SIR) - AV_delay                            │  │
│  │                                                                      │  │
│  │  Example at different rates:                                        │  │
│  │  ┌──────────┬────────┬──────────┬──────────┐                       │  │
│  │  │ Rate     │ LRI    │ AV Delay │ VA       │                       │  │
│  │  │ (ppm)    │ (ms)   │ (ms)     │ (ms)     │                       │  │
│  │  ├──────────┼────────┼──────────┼──────────┤                       │  │
│  │  │ 60       │ 1000   │ 300      │ 700      │                       │  │
│  │  │ 75       │ 800    │ 250      │ 550      │                       │  │
│  │  │ 90       │ 667    │ 200      │ 467      │                       │  │
│  │  │ 100      │ 600    │ 170      │ 430      │                       │  │
│  │  │ 120      │ 500    │ 130      │ 370      │                       │  │
│  │  └──────────┴────────┴──────────┴──────────┘                       │  │
│  │                                                                      │  │
│  │  MINIMUM VA INTERVAL:                                               │  │
│  │  • Must be > PVARP + PVAB to prevent far-field sensing            │  │
│  │  • Typical minimum: 300 ms                                         │  │
│  │  • At high rates, VA may be limited by minimum VA                  │  │
│  │                                                                      │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │                                                                      │  │
│  │  PVARP (POST-VENTRICULAR ATRIAL REFRACTORY PERIOD):                 │  │
│  │                                                                      │  │
│  │  Purpose: Prevents sensing of far-field R-waves on atrial channel  │  │
│  │                                                                      │  │
│  │  VP/VS                                                              │  │
│  │   │                                                                 │  │
│  │   ├──┐  ◄─ PVARP ────────────────────────────────────────────►   │  │
│  │   │  │    (typically 250-350 ms)                                   │  │
│  │   │  │                                                             │  │
│  │   │  │  Events during PVARP:                                       │  │
│  │   │  │  • Atrial sense → counted as refractory (not tracked)     │  │
│  │   │  │  • Does NOT reset VA interval                              │  │
│  │   │  │  • Used to prevent pacemaker-mediated tachycardia (PMT)   │  │
│  │   │                                                                 │  │
│  │   │  ◄─ PVAB ──►                                                  │  │
│  │   │   (100ms)                                                      │  │
│  │   │   (Post-Ventricular Atrial Blanking)                          │  │
│  │   │   Completely blanks atrial channel (no sensing at all)        │  │
│  │                                                                      │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 2.2.4.4 Upper Rate Limit and Mode Switching

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    UPPER RATE LIMIT AND MODE SWITCHING                       │
│                                                                             │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │                                                                      │  │
│  │  UPPER RATE LIMIT (URL):                                             │  │
│  │                                                                      │  │
│  │  Maximum tracking rate of the pacemaker in DDD/DDDR mode.          │  │
│  │  Prevents 1:1 tracking of rapid atrial rates (e.g., atrial        │  │
│  │  flutter at 300 bpm).                                               │  │
│  │                                                                      │  │
│  │  URL behavior:                                                      │  │
│  │  • If atrial rate > URL → Wenckebach or 2:1 block occurs          │  │
│  │  • Pacemaker tracks at URL with progressively longer AV delays     │  │
│  │  • Eventually 2:1 block (every other P-wave tracked)              │  │
│  │                                                                      │  │
│  │  Example (URL = 120 ppm):                                          │  │
│  │                                                                      │  │
│  │  Atrial rate:  150  140  130  120  110  100  90  80  70           │  │
│  │  Vent. rate:   120  120  120  120  110  100  90  80  70           │  │
│  │  AV delay:     260  240  220  200  200  200  200 200 200          │  │
│  │                                                                      │  │
│  │  At atrial rate > URL:                                              │  │
│  │  • AV delay extends progressively (Wenckebach behavior)            │  │
│  │  • Ventricular rate capped at URL                                  │  │
│  │                                                                      │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │                                                                      │  │
│  │  MODE SWITCHING (MS):                                                │  │
│  │                                                                      │  │
│  │  Automatic switch from DDD/DDDR to VVIR when atrial rate           │  │
│  │  exceeds threshold (indicating atrial fibrillation/flutter).        │  │
│  │                                                                      │  │
│  │  Detection criteria:                                                │  │
│  │  • Atrial rate > MS rate (programmable, typically 170-200 ppm)    │  │
│  │  • Duration > MS duration (programmable, typically 20-30 seconds) │  │
│  │  • Both criteria must be met simultaneously                        │  │
│  │                                                                      │  │
│  │  Mode Switch Transition:                                            │  │
│  │                                                                      │  │
│  │  DDD/DDDR                                                          │  │
│  │    │                                                                │  │
│  │    │  AF detected (rate > MS threshold for > MS duration)          │  │
│  │    │                                                                │  │
│  │    ▼                                                                │  │
│  │  VVIR                                                              │  │
│  │    │                                                                │  │
│  │    │  Ventricular pacing at sensor-indicated rate                  │  │
│  │    │  Atrial sensing inhibited (no atrial pacing)                 │  │
│  │    │                                                                │  │
│  │    │  AF terminated (atrial rate < MS threshold for > 1 minute)  │  │
│  │    │                                                                │  │
│  │    ▼                                                                │  │
│  │  DDD/DDDR (resumed)                                                │  │
│  │                                                                      │  │
│  │  Benefits:                                                          │  │
│  │  • Prevents rapid ventricular tracking of AF                       │  │
│  │  • Maintains hemodynamic stability                                 │  │
│  │  • Automatic and seamless transition                              │  │
│  │                                                                      │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │                                                                      │  │
│  │  PACEMAKER-MEDIATED TACHYCARDIA (PMT) PREVENTION:                  │  │
│  │                                                                      │  │
│  │  PMT is an endless-loop tachycardia using the AV delay as the      │  │
│  │  antegrade limb and the atrial sensing as the retrograde limb.     │  │
│  │                                                                      │  │
│  │  PMT Circuit:                                                       │  │
│  │  ┌──────────────────────────────────────────────────────────────┐  │  │
│  │  │                                                              │  │  │
│  │  │  VP ──→ Retrograde P-wave ──→ AS ──→ AV delay ──→ VP ──→  │  │  │
│  │  │  │                                                                │  │
│  │  │  └──────────────────────────────────────────────────────────┘  │  │
│  │  │                                                                      │  │
│  │  │  PMT Detection:                                                    │  │
│  │  │  • Rate > URL for > 8 beats                                       │  │
│  │  │  • Fixed AV interval (no variability)                            │  │
│  │  │  • Regular RR intervals                                           │  │
│  │  │                                                                      │  │
│  │  │  PMT Termination:                                                  │  │
│  │  │  • Extend PVARP for one cycle (breaks the loop)                  │  │
│  │  │  • Or: Deliver atrial pace without AV delay (overdrive)          │  │
│  │  │                                                                      │  │
│  │  └──────────────────────────────────────────────────────────────┘  │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 2.2.4.5 Biventricular Pacing (CRT)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    BIVENTRICULAR PACING (CARDIAC RESYNCHRONIZATION)          │
│                                                                             │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │                                                                      │  │
│  │  INDICATION:                                                        │  │
│  │  • Dilated cardiomyopathy with wide QRS (>120ms)                   │  │
│  │  • Left bundle branch block (LBBB) pattern                         │  │
│  │  • NYHA Class III-IV despite optimal medical therapy               │  │
│  │  • EF < 35%                                                         │  │
│  │                                                                      │  │
│  │  GOAL:                                                              │  │
│  │  Resynchronize left and right ventricular contraction to improve   │  │
│  │  cardiac output by 15-25%.                                         │  │
│  │                                                                      │  │
│  │  ┌──────────────────────────────────────────────────────────────┐   │  │
│  │  │                                                              │   │  │
│  │  │  WITHOUT CRT (LBBB):                                         │   │  │
│  │  │  ┌──────────────────────────────────────────────────────┐   │   │  │
│  │  │  │  RV ──────┐                                         │   │   │  │
│  │  │  │           │   Septum    LV                         │   │   │  │
│  │  │  │  Contract │   ──────→   Contract                  │   │   │  │
│  │  │  │  (early)  │   (delayed) (late)                    │   │   │  │
│  │  │  │           │                                         │   │   │  │
│  │  │  │  RV depol: 0ms    LV depol: 80ms                   │   │   │  │
│  │  │  │  (LBBB causes delayed LV activation)               │   │   │  │
│  │  │  └──────────────────────────────────────────────────────┘   │   │  │
│  │  │                                                              │   │  │
│  │  │  WITH CRT:                                                   │   │  │
│  │  │  ┌──────────────────────────────────────────────────────┐   │   │  │
│  │  │  │  RV ──────┐                                         │   │   │  │
│  │  │  │           │   Septum    LV                         │   │   │  │
│  │  │  │  Contract │   ──────→   Contract                  │   │   │  │
│  │  │  │  (simultaneous)                                    │   │   │  │
│  │  │  │           │                                         │   │   │  │
│  │  │  │  RV depol: 0ms    LV depol: 10ms                   │   │   │  │
│  │  │  │  (BiV pacing synchronizes activation)              │   │   │  │
│  │  │  └──────────────────────────────────────────────────────┘   │   │  │
│  │  │                                                              │   │  │
│  │  └──────────────────────────────────────────────────────────────┘   │  │
│  │                                                                      │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │                                                                      │  │
│  │  CRT PACING MODE: DDD/RV5 (BiV + sensor)                          │  │
│  │                                                                      │  │
│  │  Lead Configuration:                                                │  │
│  │  • RA lead: Right atrial appendage (sensing/pacing)                │  │
│  │  • RV lead: RV apex or septum (sensing/pacing)                     │  │
│  │  • LV lead: Coronary sinus / lateral vein (pacing only)            │  │
│  │                                                                      │  │
│  │  LV Lead Placement:                                                 │  │
│  │  ┌──────────────────────────────────────────────────────────────┐   │  │
│  │  │                                                              │   │  │
│  │  │         ┌──────────┐                                        │   │  │
│  │  │         │          │                                        │   │  │
│  │  │         │   RA     │                                        │   │  │
│  │  │         │  lead    │                                        │   │  │
│  │  │         │    │     │                                        │   │  │
│  │  │         │    ▼     │                                        │   │  │
│  │  │         │ ┌──────┐ │     ┌──────────┐                      │   │  │
│  │  │         │ │      │ │     │  LV lead │                      │   │  │
│  │  │         │ │  RV  │ │     │  (via    │                      │   │  │
│  │  │         │ │ lead │ │     │  coronary│                      │   │  │
│  │  │         │ │   │  │ │     │  sinus)  │                      │   │  │
│  │  │         │ │   ▼  │ │     │    │     │                      │   │  │
│  │  │         │ └──────┘ │     │    ▼     │                      │   │  │
│  │  │         │          │     │  LV free │                      │   │  │
│  │  │         └──────────┘     │  wall    │                      │   │  │
│  │  │                          └──────────┘                      │   │  │
│  │  │                                                              │   │  │
│  │  └──────────────────────────────────────────────────────────────┘   │  │
│  │                                                                      │  │
│  │  TIMING OPTIONS:                                                    │  │
│  │  • Simultaneous BiV: RV and LV paced simultaneously               │  │
│  │  • Sequential BiV: RV paced first, then LV (configurable delay)   │  │
│  │  • LV-only: Only LV paced (if RV sense occurring naturally)       │  │
│  │                                                                      │  │
│  │  LV OFFSET:                                                         │  │
│  │  • LV can be paced before, during, or after RV                    │  │
│  │  • Range: -80 ms to +80 ms (LV relative to RV)                    │  │
│  │  • Optimal offset determined by echocardiography or empiric       │  │
│  │                                                                      │  │
│  │  Example timing (simultaneous BiV):                                │  │
│  │  AS ──────► AV delay ──────► RV pace + LV pace (simultaneous)    │  │
│  │                                                                      │  │
│  │  Example timing (sequential BiV):                                  │  │
│  │  AS ──────► AV delay ──► RV pace ──► 20ms ──► LV pace           │  │
│  │                                                                      │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 2.2.4.6 Rate Response Algorithm

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    RATE RESPONSE ALGORITHM                                    │
│                                                                             │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │                                                                      │  │
│  │  SENSOR TYPES:                                                      │  │
│  │                                                                      │  │
│  │  1. ACCELEROMETER (Most common)                                    │  │
│  │     • Measures body vibration/movement                              │  │
│  │     • Low power (<1 µW)                                            │  │
│  │     • Response time: 10-15 seconds                                  │  │
│  │     • Limitation: Does not respond to non-movement exercise       │  │
│  │                                                                      │  │
│  │  2. IMPEDANCE PNEUMOGRAPHY                                          │  │
│  │     • Measures respiration rate via thoracic impedance             │  │
│  │     • Better correlation with metabolic demand                      │  │
│  │     • Higher power consumption                                     │  │
│  │     • Used in some dual-sensor systems                             │  │
│  │                                                                      │  │
│  │  3. QT INTERVAL                                                     │  │
│  │     • Measures QT interval from ventricular EGM                    │  │
│  │     • Shortens with exercise (sympathetic response)                │  │
│  │     • Very accurate but complex to implement                       │  │
│  │                                                                      │  │
│  │  4. DUAL SENSOR (Accelerometer + Impedance)                        │  │
│  │     • Combines benefits of both sensors                            │  │
│  │     • Better response across all activity types                    │  │
│  │     • Higher complexity and power                                  │  │
│  │                                                                      │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │                                                                      │  │
│  │  RATE RESPONSE ALGORITHM (ACCELEROMETER):                            │  │
│  │                                                                      │  │
│  │  ┌──────────────────────────────────────────────────────────────┐   │  │
│  │  │                                                              │   │  │
│  │  │  1. SAMPLE accelerometer at 32 Hz (every 31.25 ms)          │   │  │
│  │  │                                                              │   │  │
│  │  │  2. COMPUTE activity level:                                  │   │  │
│  │  │     Activity = |Accel[n] - Accel[n-1]| + |Accel[n-1] - ...| │   │  │
│  │  │     (Sum of absolute differences over 1-second window)       │   │  │
│  │  │                                                              │   │  │
│  │  │  3. APPLY smoothing filter:                                  │   │  │
│  │  │     Smoothed_Activity = α × Activity + (1-α) × Prev_Smooth │   │  │
│  │  │     (α = 0.1 for slow response, 0.5 for fast response)     │   │  │
│  │  │                                                              │   │  │
│  │  │  4. MAP to sensor-indicated rate (SIR):                     │   │  │
│  │  │     SIR = Lookup_Table(Smoothed_Activity)                   │   │  │
│  │  │                                                              │   │  │
│  │  │  5. APPLY rate smoothing:                                    │   │  │
│  │  │     • Maximum rate change: 12 bpm/beat (configurable)       │   │  │
│  │  │     • Prevents abrupt rate changes                           │   │  │
│  │  │                                                              │   │  │
│  │  │  6. CLAMP to allowed range:                                  │   │  │
│  │  │     SIR = max(LRL, min(URL, SIR))                          │   │  │
│  │  │                                                              │   │  │
│  │  └──────────────────────────────────────────────────────────────┘   │  │
│  │                                                                      │  │
│  │  LOOKUP TABLE:                                                      │  │
│  │                                                                      │  │
│  │  Activity Level: 0    10    20    30    40    50    60    70     │  │
│  │  SIR (ppm):      60   70    80    90   100   110   120   120    │  │
│  │                                                                      │  │
│  │  (Linear interpolation between points)                              │  │
│  │                                                                      │  │
│  │  RESPONSE CURVES:                                                   │  │
│  │                                                                      │  │
│  │  SIR (ppm)                                                           │  │
│  │    │                                                                 │  │
│  │ 120┤                              ╱──────── Fast response          │  │
│  │    │                             ╱  ╱─────── Medium response       │  │
│  │ 100┤                            ╱  ╱  ╱──── Slow response         │  │
│  │    │                           ╱  ╱  ╱                            │  │
│  │  80┤                          ╱  ╱  ╱                             │  │
│  │    │                         ╱  ╱  ╱                              │  │
│  │  60┤────────────────────────╱──╱──╱─────────── LRL               │  │
│  │    │                                                                    │  │
│  │    └──────┼──────┼──────┼──────┼──────┼──────▶                    │  │
│  │           10     20     30     40     50    Activity Level        │  │
│  │                                                                      │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │                                                                      │  │
│  │  RATE RESPONSE PARAMETERS:                                           │  │
│  │                                                                      │  │
│  │  ┌────────────────────────┬──────────────────────────────────────┐  │  │
│  │  │ Parameter              │ Typical Value                        │  │  │
│  │  ├────────────────────────┼──────────────────────────────────────┤  │  │
│  │  │ Lower rate limit (LRL) │ 60 ppm (programmable 50-90)         │  │  │
│  │  │ Upper rate limit (URL) │ 120 ppm (programmable 80-180)      │  │  │
│  │  │ Max rate increase      │ 12 bpm/beat (programmable 6-24)     │  │  │
│  │  │ Reaction time          │ 10 sec (programmable 5-30)          │  │  │
│  │  │ Recovery time          │ 5 min (programmable 2-10)           │  │  │
│  │  │ Sensor threshold       │ Programmed per patient               │  │  │
│  │  │ Sensor slope           │ Programmed per patient               │  │  │
│  │  │ Sensor blend           │ 50% accel + 50% impedance (dual)   │  │  │
│  │  └────────────────────────┴──────────────────────────────────────┘  │  │
│  │                                                                      │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 2.2.4.7 Timing Cycle Parameters Summary

| Parameter                 | Range          | Typical   | Step  | Notes                    |
|---------------------------|----------------|-----------|-------|--------------------------|
| Lower rate limit (LRL)    | 30–170 ppm     | 60 ppm    | 5 ppm | Minimum pacing rate      |
| Upper rate limit (URL)    | 80–180 ppm     | 120 ppm   | 5 ppm | Maximum tracking rate    |
| AV delay                  | 30–350 ms      | 200 ms    | 10 ms | Atrial-to-ventricular   |
| VA interval               | 200–1500 ms    | 800 ms    | 10 ms | Ventricular-to-atrial   |
| PVARP                     | 150–500 ms     | 300 ms    | 10 ms | Post-vent. atrial refr. |
| PVAB                      | 50–400 ms      | 100 ms    | 10 ms | Post-vent. atrial blank |
| Vent. blank period        | 50–200 ms      | 100 ms    | 10 ms | Post-pace/sense blank   |
| Atrial blank period       | 25–100 ms      | 50 ms     | 5 ms  | Post-pace/sense blank   |
| Post-pace blank (V)       | 50–200 ms      | 100 ms    | 10 ms | Extra blank after pace  |
| Post-pace blank (A)       | 25–100 ms      | 50 ms     | 5 ms  | Extra blank after pace  |
| Rate smoothing            | 3–24 bpm/beat  | 6 bpm     | 3 bpm | Max rate change per beat|
| Sensor reaction time      | 5–30 sec       | 10 sec    | 5 sec | Response to activity    |
| Sensor recovery time      | 2–10 min       | 5 min     | 1 min | Return to baseline      |
| MS detection rate         | 150–250 ppm    | 175 ppm   | 5 ppm | Mode switch threshold   |
| MS detection duration     | 10–60 sec      | 20 sec    | 5 sec | Confirmation window     |
| LV offset                 | -80 to +80 ms  | 0 ms      | 10 ms | LV vs RV timing (CRT)   |
| Rate-adaptive AV slope    | 0.5–2.0        | 1.0       | 0.1   | AV adjustment factor    |

### 2.2.4.8 Mode Selection Guide

| Clinical Scenario              | Recommended Mode | Rationale                              |
|--------------------------------|------------------|----------------------------------------|
| Sinus node dysfunction         | AAI/AAIR         | Atrial bradycardia, intact AV conduction|
| Complete heart block           | VVI/VVIR         | No AV conduction                       |
| Sinus bradycardia + intact AV  | AAI/AAIR         | Atrial pacing only                     |
| Intermittent AV block          | DDD/DDDR         | Dual-chamber support                   |
| Atrial fibrillation            | VVIR             | No atrial pacing useful                |
| Sick sinus syndrome + AV block | DDD/DDDR         | Full dual-chamber support              |
| Rate-variable response needed  | DDDR/VVIR        | Sensor-driven rate                     |
| Heart failure + wide QRS       | DDDR + BiV (CRT) | Cardiac resynchronization              |
| Elderly, limited activity     | VVI              | Simple, reliable                       |
| Active patient, normal AV      | AAI              | Maintain AV synchrony naturally        |
| Testing/troubleshooting        | VOO/AOO/DOO      | Asynchronous modes for testing         |

---

*Section 2.2.4 — Multi-Chamber Pacing*
*Previous: Section 2.2.3 — Lead Interface Design*
*Next: Section 2.3 — Power Management*
