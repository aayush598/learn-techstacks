# Pacing Pulse Generation

## 2.2.2 Pacing Pulse Generation

### 2.2.2.1 Pacing Pulse Fundamentals

A pacemaker delivers precisely controlled electrical pulses to cardiac tissue to
initiate depolarization and contraction. The pulse parameters must be carefully
optimized to achieve reliable capture while minimizing energy consumption.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    PACING PULSE FUNDAMENTALS                                 │
│                                                                             │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │                                                                      │  │
│  │  VOLTAGE PACING PULSE WAVEFORM:                                     │  │
│  │                                                                      │  │
│  │  Voltage                                                             │  │
│  │  (V)                                                                 │  │
│  │    │                                                                 │  │
│  │  5 ┤    ┌──────────────┐                                           │  │
│  │    │    │              │                                            │  │
│  │  4 ┤    │              │                                            │  │
│  │    │    │   Amplitude  │                                            │  │
│  │  3 ┤    │   (Vp)       │                                            │  │
│  │    │    │              │                                            │  │
│  │  2 ┤    │              │                                            │  │
│  │    │    │              │                                            │  │
│  │  1 ┤    │              │  ┌───── Afterpotential                    │  │
│  │    │    │              │  │      (exponential decay)               │  │
│  │  0 ┤────┘              └──┘─────────────────────────────────       │  │
│  │    │                                                                 │  │
│  │ -1 ┤                                                                 │  │
│  │    │    ◄── Pulse Width (PW) ──►                                   │  │
│  │    │                                                                 │  │
│  │    └──────┼─────────────────┼──────────────────────────────▶       │  │
│  │           0                 1ms                                    Time│  │
│  │                                                                     │  │
│  │                                                                      │  │
│  │  CURRENT PACING PULSE WAVEFORM:                                     │  │
│  │                                                                      │  │
│  │  Current                                                             │  │
│  │  (mA)                                                                │  │
│  │    │                                                                 │  │
│  │  20┤    ┌──────────────┐                                           │  │
│  │    │    │              │                                            │  │
│  │  15┤    │              │                                            │  │
│  │    │    │   Amplitude  │                                            │  │
│  │  10┤    │   (Ip)       │                                            │  │
│  │    │    │              │                                            │  │
│  │   5┤    │              │                                            │  │
│  │    │    │              │                                            │  │
│  │   0 ┤────┘              └───────────────────────────────────       │  │
│  │    │                                                                 │  │
│  │    └──────┼─────────────────┼──────────────────────────────▶       │  │
│  │           0                 1ms                                    Time│  │
│  │                                                                      │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
│  KEY PULSE PARAMETERS:                                                     │
│  ─────────────────────                                                     │
│  • Amplitude (Vp or Ip): Programmable 0.5-10V or 0.5-25mA                │
│  • Pulse Width (PW): Programmable 0.05-1.5 ms                            │
│  • Pulse Energy: E = Vp × Ip × PW (for voltage pacing)                  │
│  • Pulse Charge: Q = Ip × PW                                             │
│  • Leading-edge voltage: Applied immediately at pulse onset              │
│  • Trailing-edge voltage: Decays due to lead polarization                │
│                                                                             │
│  TYPICAL PULSE PARAMETERS:                                                │
│  ┌──────────────────────────┬────────────┬────────────┬────────────┐     │
│  │ Parameter                │ Minimum    │ Typical    │ Maximum    │     │
│  ├──────────────────────────┼────────────┼────────────┼────────────┤     │
│  │ Amplitude (voltage)      │ 0.5 V      │ 2.5 V      │ 10.0 V    │     │
│  │ Amplitude (current)      │ 0.5 mA     │ 5.0 mA     │ 25.0 mA   │     │
│  │ Pulse width              │ 0.05 ms    │ 0.4 ms     │ 1.5 ms    │     │
│  │ Pulse energy (typ)       │ 0.6 µJ     │ 5.0 µJ     │ 375 µJ    │     │
│  │ Pulse charge (typ)       │ 0.2 µC     │ 2.0 µC     │ 37.5 µC   │     │
│  │ Rise time                │ <10 µs     │ <5 µs      │ <2 µs     │     │
│  │ Pulse accuracy (amplitude)│ ±2%       │ ±2%        │ ±2%       │     │
│  │ Pulse accuracy (width)   │ ±5%        │ ±5%        │ ±5%       │     │
│  └──────────────────────────┴────────────┴────────────┴────────────┘     │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 2.2.2.2 Voltage vs. Current Pacing

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    VOLTAGE vs. CURRENT PACING                                │
│                                                                             │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │                                                                      │  │
│  │  VOLTAGE PACING:                                                    │  │
│  │  ────────────────                                                   │  │
│  │                                                                      │  │
│  │  Circuit:       Vdd ──┬── V pace                                    │  │
│  │                      │                                               │  │
│  │                      ├──── Output Capacitor (Cp)                    │  │
│  │                      │                                               │  │
│  │                      └──── Output Switch                            │  │
│  │                            │                                        │  │
│  │                            ├──── Lead Impedance (RL)                │  │
│  │                            │                                        │  │
│  │                            └──── Return (Can/Ring)                  │  │
│  │                                                                      │  │
│  │  Pros:                                                               │  │
│  │  • Simpler circuit                                                  │  │
│  │  • Lower quiescent current                                          │  │
│  │  • Industry standard                                                │  │
│  │                                                                      │  │
│  │  Cons:                                                               │  │
│  │  • Output current varies with lead impedance                        │  │
│  │  • Capture threshold varies with impedance changes                  │  │
│  │  • Difficult to measure impedance during pace                       │  │
│  │                                                                      │  │
│  │  Output voltage equation:                                           │  │
│  │  V(t) = Vp × e^(-t/τ)    where τ = RL × Cp                       │  │
│  │                                                                      │  │
│  │  Current delivered:                                                  │  │
│  │  I(t) = (Vp/RL) × e^(-t/τ)                                       │  │
│  │                                                                      │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │                                                                      │  │
│  │  CURRENT PACING:                                                    │  │
│  │  ────────────────                                                   │  │
│  │                                                                      │  │
│  │  Circuit:       Vdd ──┬── Current Source (DAC-controlled)           │  │
│  │                      │                                               │  │
│  │                      ├──── Output Switch                            │  │
│  │                      │        │                                     │  │
│  │                      │        ├──── Lead Impedance (RL)             │  │
│  │                      │        │                                     │  │
│  │                      │        └──── Return (Can/Ring)               │  │
│  │                      │                                               │  │
│  │                      └──── Voltage Compliance Limiter               │  │
│  │                                                                      │  │
│  │  Pros:                                                               │  │
│  │  • Constant current delivery (independent of RL)                   │  │
│  │  • Precise charge delivery                                         │  │
│  │  • Easy impedance measurement (V/I during pace)                    │  │
│  │  • Better strength-duration curve control                           │  │
│  │                                                                      │  │
│  │  Cons:                                                               │  │
│  │  • More complex circuit                                             │  │
│  │  • Higher voltage compliance required                               │  │
│  │  • Higher quiescent current                                         │  │
│  │                                                                      │  │
│  │  Output voltage equation:                                           │  │
│  │  V(t) = Ip × RL + Vpolarization(t)                                │  │
│  │                                                                      │  │
│  │  (Constant current through RL, voltage follows Ohm's law)          │  │
│  │                                                                      │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
│  COMPARISON SUMMARY:                                                       │
│  ┌─────────────────────┬──────────────────┬──────────────────┐            │
│  │ Parameter           │ Voltage Pacing   │ Current Pacing   │            │
│  ├─────────────────────┼──────────────────┼──────────────────┤            │
│  │ Circuit complexity  │ Low              │ Medium           │            │
│  │ Power efficiency    │ High             │ Medium           │            │
│  │ Impedance sensitivity│ High            │ Low              │            │
│  │ Charge delivery     │ Variable         │ Precise          │            │
│  │ Impedance measurement│ Difficult       │ Easy             │            │
│  │ Industry adoption   │ >90%             │ <10%             │            │
│  │ Recommended for     │ Standard pacing  │ Research/specialty│            │
│  └─────────────────────┴──────────────────┴──────────────────┘            │
│                                                                             │
│  iPACE-CHIP RECOMMENDATION: VOLTAGE PACING with output capacitor          │
│  (Industry standard, simpler design, lower power)                         │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 2.2.2.3 Strength-Duration Curve and Chronaxie/Rheobase

The strength-duration curve describes the relationship between pulse amplitude
and pulse width required to achieve cardiac capture. This fundamental
relationship is critical for optimizing pacing efficiency.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    STRENGTH-DURATION CURVE                                   │
│                                                                             │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │                                                                      │  │
│  │  Pulse                                                               │  │
│  │  Amplitude                                                          │  │
│  │  (V)                                                                 │  │
│  │    │                                                                 │  │
│  │  8 ┤                                                                 │  │
│  │    │                                                                 │  │
│  │  7 ┤                                                                 │  │
│  │    │                                                                 │  │
│  │  6 ┤                                                                 │  │
│  │    │    ╲                                                            │  │
│  │  5 ┤     ╲                                                           │  │
│  │    │      ╲                                                          │  │
│  │  4 ┤       ╲                                                         │  │
│  │    │        ╲                                                        │  │
│  │  3 ┤         ╲                                                       │  │
│  │    │          ╲                                                      │  │
│  │  2 ┤           ╲────────────── Rheobase (1.0V)                      │  │
│  │    │            ╲              ═══════════════════════               │  │
│  │  1 ┤             ╲───────────                                       │  │
│  │    │              │                                                  │  │
│  │  0 ┤──────────────┼──────────┼──────────┼──────────┼──────▶        │  │
│  │    0      0.2     │   0.5    │   1.0    │   1.5    │  2.0    PW(ms)│  │
│  │                    │                                                  │  │
│  │                 Chronaxie                                           │  │
│  │                 (0.5ms)                                             │  │
│  │                                                                      │  │
│  │  DEFINITIONS:                                                       │  │
│  │  ─────────────                                                       │  │
│  │  Rheobase (B): Minimum amplitude for infinitely wide pulse         │  │
│  │                (minimum voltage for capture)                        │  │
│  │                Typical: 0.5 - 2.0 V                                │  │
│  │                                                                      │  │
│  │  Chronaxie (τc): Pulse width at 2× rheobase amplitude             │  │
│  │                  (most efficient pulse width)                       │  │
│  │                  Typical: 0.3 - 0.8 ms                             │  │
│  │                                                                      │  │
│  │  Weiss's Law (for PW >> τc):                                       │  │
│  │    V = B × (1 + τc/PW)                                            │  │
│  │                                                                      │  │
│  │  Lapicque's Law (empirical):                                       │  │
│  │    V = B / (1 - e^(-PW/τc))                                       │  │
│  │                                                                      │  │
│  │  Irreversible damage: V > 50V or PW > 10ms                        │  │
│  │                                                                      │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │                                                                      │  │
│  │  ENERGY vs. PULSE WIDTH CURVE:                                       │  │
│  │                                                                      │  │
│  │  Energy                                                              │  │
│  │  (µJ)                                                                │  │
│  │    │                                                                 │  │
│  │  30┤                                                                 │  │
│  │    │                                                                 │  │
│  │  25┤     ╱                                                           │  │
│  │    │    ╱                                                            │  │
│  │  20┤   ╱                                                             │  │
│  │    │  ╱                                                              │  │
│  │  15┤ ╱                                                               │  │
│  │    │╱                                                                │  │
│  │  10┤───────┐                                                         │  │
│  │    │       │                                                         │  │
│  │   5┤       │                                                         │  │
│  │    │       └──── Minimum energy point                               │  │
│  │   0 ┤──────────┼──────────┼──────────┼──────────┼──────▶            │  │
│  │    0      0.2      0.4      0.6      0.8      1.0        PW(ms)   │  │
│  │                │                                                     │  │
│  │           Optimal PW                                                 │  │
│  │           (~0.4-0.6ms)                                              │  │
│  │                                                                      │  │
│  │  Minimum energy occurs at PW = τc × ln(2) ≈ 0.7 × τc             │  │
│  │  For τc = 0.5ms: optimal PW ≈ 0.35ms                               │  │
│  │                                                                      │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
│  PRACTICAL IMPLICATIONS:                                                   │
│  ───────────────────────                                                   │
│  1. Operating at chronaxie provides best energy efficiency               │
│  2. Shorter pulses require higher amplitude (less efficient)             │
│  3. Longer pulses waste energy (diminishing returns)                     │
│  4. For battery longevity: PW ≈ 0.4-0.6 ms at 2-3V                     │
│  5. Auto-capture algorithms sweep PW to find threshold daily             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 2.2.2.4 Output Stage Circuit Design

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    OUTPUT STAGE CIRCUIT DESIGN                              │
│                                                                             │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │                                                                      │  │
│  │  VOLTAGE PACING OUTPUT STAGE:                                       │  │
│  │                                                                      │  │
│  │  Vdd (3.0V)                                                         │  │
│  │    │                                                                 │  │
│  │    ├────────────────────────────┐                                   │  │
│  │    │                            │                                   │  │
│  │    │  ┌─────────────┐          │                                   │  │
│  │    │  │  Output     │          │                                   │  │
│  │    │  │  Capacitor  │          │                                   │  │
│  │    │  │  Cp         │          │                                   │  │
│  │    │  │  10-100 µF  │          │                                   │  │
│  │    │  └──────┬──────┘          │                                   │  │
│  │    │         │                 │                                   │  │
│  │    │    ┌────┴────┐            │                                   │  │
│  │    │    │ Charge  │            │                                   │  │
│  │    │    │ Pump    │            │                                   │  │
│  │    │    │ (Vdd →  │            │                                   │  │
│  │    │    │  2Vdd)  │            │                                   │  │
│  │    │    └────┬────┘            │                                   │  │
│  │    │         │                 │                                   │  │
│  │    │    ┌────┴────────────┐   │                                   │  │
│  │    │    │  Output Switch   │   │                                   │  │
│  │    │    │  (CMOS, Rds<50Ω)│   │                                   │  │
│  │    │    │                  │   │                                   │  │
│  │    │    │  Control:        │   │                                   │  │
│  │    │    │  PACE_CMD ──────┤   │                                   │  │
│  │    │    │                  │   │                                   │  │
│  │    │    └────────┬─────────┘   │                                   │  │
│  │    │             │             │                                   │  │
│  │    │        ┌────┴────┐        │                                   │  │
│  │    │        │  Tip    │        │                                   │  │
│  │    │        │  (Lead) │        │                                   │  │
│  │    │        └────┬────┘        │                                   │  │
│  │    │             │             │                                   │  │
│  │    │        ┌────┴────┐        │                                   │  │
│  │    │        │  Ring/  │        │                                   │  │
│  │    │        │  Can    │        │                                   │  │
│  │    │        │  (Return)│       │                                   │  │
│  │    │        └─────────┘        │                                   │  │
│  │    │                           │                                   │  │
│  │    │    ┌─────────────────┐   │                                   │  │
│  │    │    │  Charge Balance  │   │                                   │  │
│  │    │    │  Switch          │   │                                   │  │
│  │    │    │  (Auto-zero)    │   │                                   │  │
│  │    │    │  Control:        │   │                                   │  │
│  │    │    │  BAL_CMD ───────┤   │                                   │  │
│  │    │    └─────────────────┘   │                                   │  │
│  │    │                           │                                   │  │
│  │    └───────────────────────────┘                                   │  │
│  │                                                                      │  │
│  │  OPERATION SEQUENCE:                                                │  │
│  │  1. Charge pump activates: Vcp = 2 × Vdd = 6.0V                  │  │
│  │  2. Output capacitor charges to Vcp through charge pump           │  │
│  │  3. At pace time: output switch closes for PW duration            │  │
│  │  4. Capacitor discharges through lead: V(t) = Vcp × e^(-t/τ)    │  │
│  │  5. After pace: charge balance switch closes briefly              │  │
│  │  6. Charge pump resumes charging for next pace                    │  │
│  │                                                                      │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │                                                                      │  │
│  │  CURRENT PACING OUTPUT STAGE:                                       │  │
│  │                                                                      │  │
│  │  Vdd (3.0V)                                                         │  │
│  │    │                                                                 │  │
│  │    ├────────────────────────────┐                                   │  │
│  │    │                            │                                   │  │
│  │    │  ┌─────────────────────┐  │                                   │  │
│  │    │  │  Voltage Compliance │  │                                   │  │
│  │    │  │  Limiter            │  │                                   │  │
│  │    │  │  (Max Vout = 8V)   │  │                                   │  │
│  │    │  └──────────┬──────────┘  │                                   │  │
│  │    │             │             │                                   │  │
│  │    │  ┌──────────┴──────────┐  │                                   │  │
│  │    │  │  Programmable       │  │                                   │  │
│  │    │  │  Current Source     │  │                                   │  │
│  │    │  │  (DAC-controlled)   │  │                                   │  │
│  │    │  │                     │  │                                   │  │
│  │    │  │  DAC: 8-bit         │  │                                   │  │
│  │    │  │  Range: 0.5-25 mA   │  │                                   │  │
│  │    │  │  Step: 0.1 mA       │  │                                   │  │
│  │    │  │  Compliance: 8V     │  │                                   │  │
│  │    │  └──────────┬──────────┘  │                                   │  │
│  │    │             │             │                                   │  │
│  │    │    ┌────────┴────────┐   │                                   │  │
│  │    │    │  Output Switch   │   │                                   │  │
│  │    │    └────────┬────────┘   │                                   │  │
│  │    │             │             │                                   │  │
│  │    │        ┌────┴────┐        │                                   │  │
│  │    │        │  Lead   │        │                                   │  │
│  │    │        └────┬────┘        │                                   │  │
│  │    │             │             │                                   │  │
│  │    │        ┌────┴────┐        │                                   │  │
│  │    │        │ Return  │        │                                   │  │
│  │    │        └─────────┘        │                                   │  │
│  │    └───────────────────────────┘                                   │  │
│  │                                                                      │  │
│  │  KEY ADVANTAGE: Current is independent of lead impedance           │  │
│  │  I_out = DAC_value × I_LSB (constant regardless of RL)            │  │
│  │                                                                      │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 2.2.2.5 Charge Balancing

Charge balancing prevents the accumulation of residual charge at the
electrode-tissue interface, which can cause tissue damage and electrode
corrosion over time.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    CHARGE BALANCING                                          │
│                                                                             │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │                                                                      │  │
│  │  WHY CHARGE BALANCING IS NECESSARY:                                  │  │
│  │                                                                      │  │
│  │  After a pacing pulse, residual charge remains on the electrode:    │  │
│  │                                                                      │  │
│  │  Voltage                                                             │  │
│  │  at electrode:                                                       │  │
│  │    │                                                                 │  │
│  │    │    Pace pulse                                                   │  │
│  │    │    ┌──────┐                                                    │  │
│  │    │    │      │                                                    │  │
│  │  0 ┤────┘      └──────┬────────────────────────────               │  │
│  │    │                  │                                             │  │
│  │    │                  │  Afterpotential (decay)                     │  │
│  │    │                  │                                             │  │
│  │    │                  └────────────────────────────                 │  │
│  │    │                                                                 │  │
│  │    │  ◄─ Charge Q₁ ─► ◄─ Residual charge Q₂ ──────────────────►  │  │
│  │    │                    (must be removed!)                          │  │
│  │    │                                                                 │  │
│  │  If Q₂ is not removed:                                             │  │
│  │  • Electrolysis occurs (tissue damage)                             │  │
│  │  • Electrode corrosion accelerates                                  │  │
│  │  • Polarization voltage builds up (reduces sensing)                │  │
│  │                                                                      │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │                                                                      │  │
│  │  CHARGE BALANCING METHODS:                                           │  │
│  │                                                                      │  │
│  │  METHOD 1: PASSIVE CHARGE BALANCE                                   │  │
│  │  ────────────────────────────────                                    │  │
│  │  • Output capacitor decays naturally through lead resistance        │  │
│  │  • Additional parallel resistor ensures complete discharge          │  │
│  │  • Simple but slow (depends on RC time constant)                   │  │
│  │                                                                      │  │
│  │  Method 2: ACTIVE CHARGE BALANCE (Recommended)                      │  │
│  │  ──────────────────────────────────────────────                      │  │
│  │  • After pace, reverse current is applied briefly                   │  │
│  │  • Remaining charge is measured and compensated                    │  │
│  │  • Fast (<4 µs) and accurate                                       │  │
│  │                                                                      │  │
│  │  Voltage                                                             │  │
│  │    │                                                                 │  │
│  │    │    Pace     Balance                                           │  │
│  │    │    ┌──┐     ┌──┐                                              │  │
│  │    │    │  │     │  │                                              │  │
│  │  0 ┤────┘  └─────┘  └────────────────────────────                 │  │
│  │    │    │  │     │                                                  │  │
│  │    │    │  │     │                                                  │  │
│  │    │    │  │     └─── Reverse current                               │  │
│  │    │    │  │         (removes residual charge)                     │  │
│  │    │    ◄──►                                                       │  │
│  │    │   PW   Balance                                                │  │
│  │    │   (0.5ms) (4µs)                                              │  │
│  │                                                                      │  │
│  │  METHOD 3: CONTINUOUS CHARGE BALANCE                                │  │
│  │  ──────────────────────────────────                                  │  │
│  │  • Small reverse current applied continuously after pace            │  │
│  │  • Ensures charge balance over time                                │  │
│  │  • Used in some modern pacemakers                                   │  │
│  │                                                                      │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │                                                                      │  │
│  │  CHARGE BALANCE CIRCUIT:                                             │  │
│  │                                                                      │  │
│  │  Tip ──────┐                                                        │  │
│  │            │                                                         │  │
│  │       ┌────┴────┐                                                   │  │
│  │       │  V-to-I │                                                   │  │
│  │       │  Converter│                                                  │  │
│  │       └────┬────┘                                                   │  │
│  │            │                                                         │  │
│  │       ┌────┴────┐                                                   │  │
│  │       │  integrator │                                               │  │
│  │       │  (op-amp + C)│                                              │  │
│  │       └────┬────┘                                                   │  │
│  │            │                                                         │  │
│  │       ┌────┴────┐                                                   │  │
│  │       │  Comparator │                                               │  │
│  │       │  (zero    │                                                 │  │
│  │       │   crossing)│                                                │  │
│  │       └────┬────┘                                                   │  │
│  │            │                                                         │  │
│  │       ┌────┴────┐                                                   │  │
│  │       │  Balance │                                                   │  │
│  │       │  Switch  │                                                   │  │
│  │       │  Control │                                                   │  │
│  │       └─────────┘                                                   │  │
│  │                                                                      │  │
│  │  Performance:                                                       │  │
│  │  • Balance time: <4 µs                                              │  │
│  │  • Residual charge: <0.1 µC                                         │  │
│  │  • Afterpotential: <500 mV at 500 Ω                                │  │
│  │                                                                      │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 2.2.2.6 Output Pulse Timing and Control

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    OUTPUT PULSE TIMING AND CONTROL                           │
│                                                                             │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │                                                                      │  │
│  │  PULSE GENERATION STATE MACHINE:                                     │  │
│  │                                                                      │  │
│  │       ┌──────────┐                                                  │  │
│  │   ┌───│   IDLE    │◄──────────────────────┐                        │  │
│  │   │   │  (Waiting │                       │                        │  │
│  │   │   │  for pace │                       │                        │  │
│  │   │   │  command) │                       │                        │  │
│  │   │   └─────┬────┘                       │                        │  │
│  │   │         │                            │                        │  │
│  │   │    PACE_CMD                      BAL_DONE                      │  │
│  │   │         │                            │                        │  │
│  │   │         ▼                            │                        │  │
│  │   │   ┌──────────┐                       │                        │  │
│  │   │   │  CHARGE   │                       │                        │  │
│  │   │   │  (Capacitor│                      │                        │  │
│  │   │   │   charges  │                      │                        │  │
│  │   │   │   to Vcp)  │                      │                        │  │
│  │   │   └─────┬────┘                       │                        │  │
│  │   │         │                            │                        │  │
│  │   │    CHARGE_DONE                       │                        │  │
│  │   │         │                            │                        │  │
│  │   │         ▼                            │                        │  │
│  │   │   ┌──────────┐                       │                        │  │
│  │   │   │  DELIVER  │                       │                        │  │
│  │   │   │  (Output  │                       │                        │  │
│  │   │   │   switch  │                       │                        │  │
│  │   │   │   closed  │                       │                        │  │
│  │   │   │   for PW) │                       │                        │  │
│  │   │   └─────┬────┘                       │                        │  │
│  │   │         │                            │                        │  │
│  │   │    PW_EXPIRED                        │                        │  │
│  │   │         │                            │                        │  │
│  │   │         ▼                            │                        │  │
│  │   │   ┌──────────┐                       │                        │  │
│  │   │   │  BALANCE  │                       │                        │  │
│  │   │   │  (Charge  │                       │                        │  │
│  │   │   │   balance │                       │                        │  │
│  │   │   │   active) │                       │                        │  │
│  │   │   └─────┬────┘                       │                        │  │
│  │   │         │                            │                        │  │
│  │   │    BAL_DONE                          │                        │  │
│  │   │         │                            │                        │  │
│  │   └─────────┘                            │                        │  │
│  │                                          │                        │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │                                                                      │  │
│  │  TIMING DIAGRAM - COMPLETE PACE CYCLE:                              │  │
│  │                                                                      │  │
│  │  Time    0µs    100µs   200µs   300µs   400µs   500µs   600µs     │  │
│  │          │       │       │       │       │       │       │          │  │
│  │  PACE  ──┼───────┼───────┼───────┼───────┼───────┼───────┼──        │  │
│  │  CMD     │       │       │       │       │       │       │          │  │
│  │          │       │       │       │       │       │       │          │  │
│  │  CHARGE  ┌───────┐       │       │       │       │       │          │  │
│  │  ACTIVE  │       │       │       │       │       │       │          │  │
│  │          │       │       │       │       │       │       │          │  │
│  │  Vcp   ──┼───────╱───────╲───────╱───────╲───────╱───────╲──        │  │
│  │  (V)     │      6V       │       │       │       │       │          │  │
│  │          │       │       │       │       │       │       │          │  │
│  │  OUTPUT  │       ┌───────┐       │       │       │       │          │  │
│  │  SWITCH  │       │       │       │       │       │       │          │  │
│  │          │       │       │       │       │       │       │          │  │
│  │  Vout  ──┼───────┼───────╲───────╲───────╲───────╲───────╲──        │  │
│  │  (V)     │       │  5V   ╲       ╲       ╲       ╲       ╲          │  │
│  │          │       │       │  Exponential decay through RL           │  │
│  │          │       │       │       │       │       │       │          │  │
│  │  BALANCE │       │       │       │       │       ┌──┐    │          │  │
│  │  ACTIVE  │       │       │       │       │       │  │    │          │  │
│  │          │       │       │       │       │       │  │    │          │  │
│  │          ◄───────┼───────┼───────┼───────┼───────┼──┼────┤          │  │
│  │                  0      100     200     300     400  420  500       │  │
│  │                  │               │                         │        │  │
│  │               Charge          PW=400µs                   Balance   │  │
│  │               time             │                         time      │  │
│  │             (100µs)            │                        (20µs)     │  │
│  │                                                                      │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
│  TIMING REQUIREMENTS:                                                      │
│  ┌──────────────────────────┬────────────┬────────────┬────────────┐     │
│  │ Parameter                │ Minimum    │ Typical    │ Maximum    │     │
│  ├──────────────────────────┼────────────┼────────────┼────────────┤     │
│  │ Charge time              │ 50 µs      │ 100 µs     │ 200 µs     │     │
│  │ Pulse width              │ 50 µs      │ 400 µs     │ 1500 µs    │     │
│  │ Balance time             │ 4 µs       │ 10 µs      │ 20 µs      │     │
│  │ Total cycle time         │ 104 µs     │ 510 µs     │ 1720 µs    │     │
│  │ Rise time (0-90%)        │ <2 µs      │ <1 µs      │ <0.5 µs    │     │
│  │ Fall time (90-10%)       │ <5 µs      │ <3 µs      │ <2 µs      │     │
│  │ Pulse-to-pulse jitter    │ <1 µs      │ <0.5 µs    │ <0.2 µs    │     │
│  │ Amplitude settling       │ <10 µs     │ <5 µs      │ <2 µs      │     │
│  └──────────────────────────┴────────────┴────────────┴────────────┘     │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 2.2.2.7 Capture Threshold and Safety Margin

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    CAPTURE THRESHOLD AND SAFETY MARGIN                       │
│                                                                             │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │                                                                      │  │
│  │  CAPTURE THRESHOLD DEFINITION:                                      │  │
│  │                                                                      │  │
│  │  The minimum pulse amplitude (at a given width) that consistently   │  │
│  │  depolarizes cardiac tissue (captures the heart).                   │  │
│  │                                                                      │  │
│  │  Threshold measurement (manual):                                    │  │
│  │  1. Start at high output (5V, 0.5ms)                              │  │
│  │  2. Decrease amplitude by 0.5V steps                               │  │
│  │  3. At each level, deliver 8 pulses                                │  │
│  │  4. Capture: All 8 pulses result in contraction                    │  │
│  │  5. Threshold: Lowest amplitude with 100% capture                  │  │
│  │                                                                      │  │
│  │  Threshold Variation:                                               │  │
│  │  • Diurnal: ±0.5V (higher at night)                               │  │
│  │  • Post-exercise: ±0.3V (lower after exercise)                     │  │
│  │  • Lead maturation: 2-4× higher acutely (first 3 months)          │  │
│  │  • Long-term drift: 0.1-0.5V over 10 years                        │  │
│  │                                                                      │  │
│  │                                                                      │  │
│  │  SAFETY MARGIN:                                                     │  │
│  │                                                                      │  │
│  │  Output = Threshold × Safety Margin                                │  │
│  │                                                                      │  │
│  │  Typical safety margin: 2× (100% above threshold)                  │  │
│  │                                                                      │  │
│  │  Example:                                                          │  │
│  │  • Measured threshold: 1.0V @ 0.4ms                               │  │
│  │  • Output setting: 2.0V @ 0.4ms (2× margin)                       │  │
│  │  • This ensures capture even with threshold variations             │  │
│  │                                                                      │  │
│  │                                                                      │  │
│  │  AUTO-CAPTURE ALGORITHM:                                            │  │
│  │                                                                      │  │
│  │  Daily automatic threshold search:                                  │  │
│  │  1. During night (low activity), reduce output systematically      │  │
│  │  2. Find threshold by binary search                                │  │
│  │  3. Set output = threshold + 0.5V (or 2×, configurable)           │  │
│  │  4. Store threshold in EEPROM for trending                         │  │
│  │  5. If threshold exceeds safety limit, alert physician             │  │
│  │                                                                      │  │
│  │  Benefits:                                                          │  │
│  │  • Reduces average output by 30-50%                                │  │
│  │  • Extends battery life by 2-4 years                               │  │
│  │  • Adapts to threshold changes automatically                       │  │
│  │                                                                      │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │                                                                      │  │
│  │  CAPTURE VERIFICATION (POST-PACE):                                  │  │
│  │                                                                      │  │
│  │  After each pace pulse, the system checks for capture:              │  │
│  │                                                                      │  │
│  │  1. Deliver pace pulse                                              │  │
│  │  2. Wait for blanking period (100-200 ms)                          │  │
│  │  3. Sense for intrinsic depolarization (evoked response)           │  │
│  │  4. If sensed within window → Capture confirmed                     │  │
│  │  5. If not sensed → Non-capture detected                           │  │
│  │  6. Deliver backup pace at higher output                           │  │
│  │                                                                      │  │
│  │  Evoked response detection:                                         │  │
│  │  • Requires blanking to avoid afterpotential sensing               │  │
│  │  • Evoked R-wave amplitude: 5-15 mV                               │  │
│  │  • Detection window: 200-400 ms post-pace                         │  │
│  │                                                                      │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 2.2.2.8 Output Stage Specifications Summary

| Parameter                    | Specification              | Notes                    |
|------------------------------|----------------------------|--------------------------|
| Output voltage range         | 0.5–10.0 V                 | Programmable, 0.1V steps |
| Output current (max)         | 25 mA                      | Compliance limited       |
| Output resistance            | <50 Ω                      | During charge phase      |
| Output capacitor             | 10–100 µF                  | Tantalum or ceramic      |
| Charge pump voltage          | 2 × Vdd = 6.0 V           | For 3.0V battery         |
| Charge pump efficiency       | >80%                       | At 10µA average          |
| Charge pump frequency        | 100 kHz                    | Low EMI                  |
| Pulse width range            | 0.05–1.5 ms                | Programmable, 10µs steps |
| Pulse width accuracy         | ±5% or ±10µs               | Whichever greater        |
| Amplitude accuracy           | ±2%                        | After settling           |
| Rise time                    | <2 µs                      | 0 to 90%                 |
| Fall time                    | <5 µs                      | 90% to 0%                |
| Charge balance time          | <4 µs                      | Active balance           |
| Charge balance residual      | <0.1 µC                    | After balance            |
| Post-pace polarization       | <500 mV                    | At 500Ω load            |
| Pulse-to-pulse jitter        | <1 µs                      | Timing accuracy          |
| Simultaneous multi-site      | Yes (biventricular)        | If DDD/BiV mode         |
| Pacing mode support          | Unipolar/Bipolar            | Programmable             |
| Energy per pulse (typical)   | <10 µJ                     | At 2.5V, 0.4ms, 500Ω   |
| Maximum energy per pulse     | <100 µJ                    | Safety limit             |
| Output filtering             | RC low-pass (100Ω/10nF)    | Reduces artifacts        |
| ESD protection               | 8 kV HBM                   | At lead pins             |
| Power consumption (pacing)   | <15 µW average             | At 70 bpm, 2.5V, 0.4ms  |
| Charge pump power            | <5 µW                      | Continuous               |

---

*Section 2.2.2 — Pacing Pulse Generation*
*Previous: Section 2.2.1 — Signal Sensing | Next: Section 2.2.3 — Lead Interface Design*
