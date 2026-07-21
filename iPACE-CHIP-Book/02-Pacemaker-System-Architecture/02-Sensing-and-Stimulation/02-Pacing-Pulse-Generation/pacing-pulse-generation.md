# Pacing Pulse Generation

## 2.2.2 Stimulation Waveform Design and Output Stage

The pacing output stage generates the high-voltage, precisely timed current or
voltage pulses that stimulate the cardiac tissue. This chapter covers the
fundamentals of cardiac stimulation, the strength-duration relationship,
pacing waveform parameters, charge balancing, and the circuit design of the
pacing output stage.

---

## 2.6.1 Cardiac Tissue Stimulation Fundamentals

### Excitation Mechanism

Cardiac muscle cells (myocytes) are excitable tissue that responds to
electrical stimulation by generating an action potential. The stimulation
process involves:

1. **Current injection**: The pacing pulse injects current through the
   electrode into the surrounding tissue.
2. **Current spread**: The injected current spreads through the tissue,
   creating a potential gradient.
3. **Membrane depolarization**: The potential gradient across the cell
   membrane causes depolarization.
4. **Threshold crossing**: If the depolarization exceeds the threshold
   potential, an action potential is triggered.
5. **Propagation**: The action potential propagates through the myocardium,
   causing coordinated contraction.

### Strength-Duration Relationship

The strength-duration relationship describes the minimum current amplitude
required to stimulate the tissue as a function of pulse duration. This
relationship is fundamental to pacing and is described by the Weiss equation:

```
I(t) = I_r × (1 + t_ch / t)

where:
  I(t) = threshold current at pulse duration t
  I_r  = rheobase current (minimum current at infinite pulse duration)
  t_ch = chronaxie time (pulse duration at 2× rheobase current)
  t    = pulse duration
```

### Rheobase and Chronaxie

**Rheobase (I_r):**
- The minimum current amplitude that can stimulate the tissue at infinite
  pulse duration
- Typical values: 0.3-1.5 mA (ventricular), 0.5-2.0 mA (atrial)
- Depends on: electrode size, electrode-tissue interface, tissue proximity

**Chronaxie (t_ch):**
- The pulse duration at which the threshold current is twice the rheobase
- Typical values: 0.5-1.5 ms (ventricular), 0.3-1.0 ms (atrial)
- Represents the optimal pulse duration for energy-efficient pacing
- At chronaxie, the stimulation energy is approximately 1.4× the minimum

### Strength-Duration Curve

```
  Threshold
  Current (mA)
    │
  3.0├─────────────────────────────────────────╮
    │                                         ╱
  2.5├───────────────────────────────────────╱──
    │                                     ╱
  2.0├───────────────────────────────────╱──────
    │                               ╱
  1.5├─────────────────────────────╱─────────────
    │                         ╱
  1.0├───────────────────────╱────────────────────
    │                    ╱
  0.5├─────────────╱─────────────────────────────── I_r (Rheobase)
    │        ╱
  0.3├──────╱──────────────────────────────────────
    │  ╱
  0.1├╱─────────────────────────────────────────────
    │
  0.0├────┬────┬────┬────┬────┬────┬────┬────┬────
    0   0.1  0.2  0.4  0.6  0.8  1.0  1.5  2.0  t (ms)
                         │
                         t_ch (Chronaxie ≈ 0.5 ms)
```

### Lapicque Equation

A more accurate model of the strength-duration relationship is the Lapicque
equation:

```
I(t) = I_r / (1 - e^(-t/t_ch))

where:
  e = Euler's number (2.71828...)
  All other variables as defined above
```

The Lapicque equation provides a better fit to experimental data than the
Weiss equation, especially at short pulse durations.

### Energy Efficiency

The energy delivered by a pacing pulse is:

```
E = V × I × t = I² × R × t

where:
  E = energy (Joules)
  V = voltage across the electrode (Volts)
  I = current through the electrode (Amps)
  R = lead impedance (Ohms)
  t = pulse duration (seconds)
```

The optimal pulse duration for minimum energy delivery is approximately
1.4× the chronaxie time:

```
t_optimal ≈ 1.4 × t_ch
```

For a typical ventricular lead with t_ch = 0.5 ms:
- t_optimal ≈ 0.7 ms
- At t = 0.4 ms: energy is ~1.6× minimum
- At t = 1.0 ms: energy is ~1.2× minimum
- At t = 2.0 ms: energy is ~2.0× minimum

---

## 2.6.2 Pacing Waveform Parameters

### Monophasic vs. Biphasic Waveforms

**Monophasic waveform:**
- Single polarity pulse (typically cathodal)
- Simple to implement
- Higher charge imbalance (electrode polarization)
- Most common in clinical pacemakers

```
  Voltage
    │
  Vp├────────┐
    │        │
    │        │
    │        │
    │        │
  0 ├────────┘─────────────────────────────
    │        │← pw →│
    │        Pulse Width
    0        t
```

**Biphasic waveform:**
- Two-phase pulse: cathodal followed by anodal (or vice versa)
- First phase: stimulation
- Second phase: charge recovery (reduces polarization)
- Lower polarization artifacts
- Used in defibrillators and some advanced pacemakers

```
  Voltage
    │
  Vp├────────┐
    │        │
    │        │
    │        │
  0 ├────────┘────────────┐─────────────────
    │        │← p1 →│     │
    │        Phase 1      │← p2 →│
    │                     Phase 2
    │                     (Recovery)
  -Vr│                    └────────┘
    │
    0                    t
```

### Pulse Width

The pulse width (pw) is the duration of the pacing pulse:

| Parameter | Range | Default | Resolution | Unit |
|-----------|-------|---------|-----------|------|
| Monophasic pulse width | 0.05-2.0 | 0.4 | 0.01 | ms |
| Biphasic phase 1 width | 0.05-2.0 | 0.4 | 0.01 | ms |
| Biphasic phase 2 width | 0.05-2.0 | 0.4 | 0.01 | ms |
| Phase 2 amplitude ratio | 0.1-1.0 | 0.33 | 0.01 | — |

### Pulse Amplitude

The pulse amplitude is the voltage or current of the pacing pulse:

**Voltage pacing:**
| Parameter | Range | Default | Resolution | Unit |
|-----------|-------|---------|-----------|------|
| Voltage amplitude | 0.5-7.5 | 3.5 | 0.1 | V |
| Voltage resolution | — | — | 0.1 | V |

**Current pacing:**
| Parameter | Range | Default | Resolution | Unit |
|-----------|-------|---------|-----------|------|
| Current amplitude | 0.1-25 | 10 | 0.1 | mA |
| Current resolution | — | — | 0.1 | mA |

### Programmable Polarity

| Mode | Tip | Ring | Can | Description |
|------|-----|------|-----|-------------|
| Bipolar | Cathode | Anode | — | Current flows tip to ring |
| Unipolar | Cathode | — | Anode | Current flows tip to can |
| Auto | Selected by clinician | — | — | Polarity set at implant |

---

## 2.6.3 Charge Balancing

### Why Charge Balancing?

After a pacing pulse, residual charge remains on the electrode-tissue
interface. This residual charge causes:

1. **Electrode polarization**: A voltage develops across the electrode-
   tissue interface that can persist for seconds to minutes.
2. **Tissue damage**: Chronic charge imbalance can cause inflammation,
   fibrosis, and increased pacing threshold.
3. **Electrode corrosion**: Net DC charge flow can cause electrolysis
   and electrode material degradation.

### Charge Balancing Techniques

**Technique 1: Passive Discharge**

After the pacing pulse, the output capacitor is connected to ground through
a resistor, allowing the charge to dissipate naturally.

```
  Pacing Pulse          Passive Discharge
    │                      │
    ▼                      ▼
  ┌────┐                ┌────────────┐
  │    │                │            │
  │ C  │──▶ R_discharge │            │
  │    │                │            │
  └────┘                └────────────┘

  R_discharge = 1-10 kΩ
  τ_discharge = R_discharge × C_output
  Complete discharge: 5 × τ_discharge
```

**Technique 2: Active Discharge**

After the pacing pulse, an active circuit actively drives the electrode
to the baseline potential, providing faster and more complete charge
removal.

```
  Pacing Pulse          Active Discharge
    │                      │
    ▼                      ▼
  ┌────┐                ┌────────────┐
  │    │                │  Op-amp    │
  │ C  │──▶ Switch ────▶│  (Unity    │──▶ Electrode
  │    │                │   Gain)    │
  └────┘                └────────────┘

  Discharge time: < 1 ms
  Residual voltage: < 10 mV
```

**Technique 3: Biphasic Pulse**

The second phase of a biphasic pulse actively removes the charge deposited
by the first phase, achieving near-perfect charge balance.

```
  Charge deposited by Phase 1: Q1 = I1 × t1
  Charge removed by Phase 2: Q2 = I2 × t2
  Net charge: Q_net = Q1 - Q2 = 0 (if I1×t1 = I2×t2)
```

### Charge Balance Accuracy

| Parameter | Specification | Unit |
|-----------|--------------|------|
| Residual voltage after discharge | < 10 | mV |
| Charge balance accuracy | < 5% | of delivered charge |
| Discharge time | < 1 | ms |
| Residual charge | < 0.1 | µC |

---

## 2.6.4 Pacing Output Stage Circuit Design

### Voltage-Mode Pacing Output Stage

```
                    VOLTAGE-MODE PACING OUTPUT STAGE

  V_BAT (2.5-3.2V)
     │
     ▼
  ┌────────────┐
  │  CHARGE    │     V_PACE (3-8V)
  │  PUMP /    │─────────────────────────────┐
  │  BOOST     │                              │
  │  CONVERTER │                              │
  └────────────┘                              │
                                              │
                                              ▼
  Digital     ┌────────────┐           ┌────────────┐
  Control ────│  PULSE     │           │  OUTPUT    │
  (Width)     │  WIDTH     │──S1──────▶│  CAPACITOR │
              │  TIMER     │           │  (10-33µF) │
              └────────────┘           └─────┬──────┘
                                             │
                                             │
                                    S2       │
  Digital     ┌────────────┐      ┌───┤      │
  Control ────│  AMPLITUDE │──────┤   │      │
  (Amplitude) │  CONTROL   │      │   ▼      ▼
              └────────────┘      │  ┌────────────┐
                                  │  │  OUTPUT    │──▶ Tip Electrode
                                  └──│  SWITCH    │
                                     │  (MOSFET)  │
                                     └────────────┘

  S1 = Charge switch (connects V_PACE to C_out)
  S2 = Output switch (connects C_out to electrode)
```

### Current-Mode Pacing Output Stage

```
                    CURRENT-MODE PACING OUTPUT STAGE

  V_BAT (2.5-3.2V)
     │
     ▼
  ┌────────────┐
  │  DC-DC     │     V_REG (3-8V)
  │  CONVERTER │─────────────────────────────┐
  └────────────┘                              │
                                              │
                                              ▼
  Digital     ┌────────────┐           ┌────────────┐
  Control ────│  CURRENT   │           │  CURRENT   │
  (Amplitude) │  DAC       │──I_ref──▶│  MIRROR    │
              │  (6-10 bit)│           │  (Cascode) │
              └────────────┘           └─────┬──────┘
                                             │
                                             │ I_out
  Digital     ┌────────────┐                 │
  Control ────│  PULSE     │──S1─────────────┤
  (Width)     │  WIDTH     │                 │
              │  TIMER     │                 ▼
              └────────────┘           ┌────────────┐
                                       │  OUTPUT    │──▶ Tip Electrode
                                       │  SWITCH    │
                                       │  (MOSFET)  │
                                       └────────────┘
```

### H-Bridge Polarity Switch

The H-Bridge allows current to flow in either direction through the lead,
enabling both tip-positive and tip-negative pacing, as well as bipolar
pacing configurations.

```
                    H-BRIDGE POLARITY SWITCH

                    V_PACE
                      │
              ┌───────┼───────┐
              │       │       │
              ▼       │       ▼
         ┌────────┐   │   ┌────────┐
         │  Q1    │   │   │  Q3    │
         │ (PMOS) │   │   │ (PMOS) │
         └───┬────┘   │   └───┬────┘
             │        │       │
             ├────────┼───────┤
             │        │       │
             ▼        │       ▼
        Tip ──────────┤──────── Ring
             │        │       │
             ▲        │       ▲
             │        │       │
         ┌───┴────┐   │   ┌───┴────┐
         │  Q2    │   │   │  Q4    │
         │ (NMOS) │   │   │ (NMOS) │
         └───┬────┘   │   └───┬────┘
              │       │       │
              └───────┼───────┘
                      │
                     GND

  Tip-positive: Q1 ON, Q4 ON (current: V_PACE → Tip → Ring → GND)
  Tip-negative: Q3 ON, Q2 ON (current: V_PACE → Ring → Tip → GND)
  Bipolar:      Q1 ON, Q4 ON (or Q3 ON, Q2 ON)
  Unipolar:     Q1 ON, Q4 ON (Ring = open)
```

---

## 2.6.5 Charge Pump / Boost Converter Design

### Requirements

The charge pump or boost converter must provide the pacing voltage from the
low-voltage battery:

| Parameter | Specification | Unit |
|-----------|--------------|------|
| Input voltage | 2.4-3.2 | V |
| Output voltage | 3.0-8.0 | V (programmable) |
| Output current | ≤ 25 | mA |
| Output ripple | < 50 | mV |
| Efficiency | ≥ 80 | % |
| Start-up time | < 50 | µs |
| Output capacitance | 10-33 | µF |
| Quiescent current | < 5 | µA |

### Dickson Charge Pump

The Dickson charge pump is a simple, capacitor-based voltage multiplier
that can generate voltages higher than the battery voltage without an
inductor.

```
                    DICKSON CHARGE PUMP (4-Stage)

  V_BAT ──┬──▶│├──┬──▶│├──┬──▶│├──┬──▶│├──┬──▶ V_OUT
          │   C1    │   C2    │   C3    │   C4
          │   │     │   │     │   │     │   │
         GND  │    GND  │    GND  │    GND  │
              │         │         │         │
           φ1▼       φ2▼       φ1▼       φ2▼
           (CLK)    (CLK)    (CLK)    (CLK)

  V_OUT = V_BAT × (N + 1) × η
  where:
    N = number of stages (4-6)
    η = efficiency per stage (0.85-0.95)
    CLK = clock signal (100-500 kHz)
```

### Inductive Boost Converter

The inductive boost converter provides higher efficiency than a charge pump
for high-current applications, but requires an external inductor.

```
                    INDUCTIVE BOOST CONVERTER

  V_BAT ──────── L (1-10µH) ────────┬──── V_OUT
                         │           │
                         │          C_out (10-33µF)
                         │           │
                        Q1 (NMOS)   GND
                         │
                        GND

  When Q1 ON:  Energy stored in L (E = 0.5 × L × I²)
  When Q1 OFF: Energy transferred to C_out via diode/SR

  V_OUT = V_BAT / (1 - D)
  where D = duty cycle (0.3-0.7)
```

### Hybrid Topology

A hybrid approach combines a charge pump for initial startup with an
inductive converter for steady-state operation:

1. **Startup phase**: Charge pump generates intermediate voltage (3-4 V)
2. **Steady-state phase**: Inductive boost converter takes over for
   higher efficiency
3. **Fallback**: If inductor is not available, charge pump operates
   alone (lower efficiency)

---

## 2.6.6 Output Capacitor Sizing

### Energy Requirements

The energy stored in the output capacitor must be sufficient for a single
pacing pulse:

```
E_stored = 0.5 × C × (V_max² - V_min²)

where:
  E_stored = energy available for pacing pulse (J)
  C = output capacitance (F)
  V_max = maximum voltage across capacitor (V)
  V_min = minimum voltage for reliable pacing (V)
```

### Sizing Example

For a typical pacing pulse:
- Pulse amplitude: 5.0 V
- Pulse current: 10 mA
- Pulse width: 0.4 ms
- Lead impedance: 500 Ω

```
E_pulse = V × I × t = 5.0 × 0.01 × 0.0004 = 20 µJ

C_min = 2 × E_pulse / (V_max² - V_min²)
      = 2 × 20e-6 / (5.0² - 4.5²)
      = 40e-6 / (25 - 20.25)
      = 40e-6 / 4.75
      = 8.4 µF

With safety margin (2×): C = 16.8 µF → Use 22 µF standard value
```

### Capacitor Selection

| Parameter | Specification | Unit |
|-----------|--------------|------|
| Capacitance | 10-33 | µF |
| Voltage rating | ≥ 10 | V |
| ESR (at 100 kHz) | < 50 | mΩ |
| Temperature range | -40 to +85 | °C |
| Size (0402/0603) | < 2 × 1.5 × 1.0 | mm |
| Leakage current | < 1 | µA |
| Dielectric | X5R or X7R | — |

---

## 2.6.7 Pacing Output Accuracy

### Voltage Accuracy

| Parameter | Specification | Unit |
|-----------|--------------|------|
| Absolute accuracy | ±5% | of programmed value |
| Temperature coefficient | < 100 | ppm/°C |
| Load regulation | < 2% | for 100-2000 Ω load |
| Line regulation | < 1% | for 2.4-3.2 V input |
| Settling time | < 10 | µs |

### Current Accuracy

| Parameter | Specification | Unit |
|-----------|--------------|------|
| Absolute accuracy | ±5% | of programmed value |
| Temperature coefficient | < 150 | ppm/°C |
| Output impedance | > 100 | kΩ |
| Compliance voltage | ≥ 8 | V |

### Pulse Width Accuracy

| Parameter | Specification | Unit |
|-----------|--------------|------|
| Absolute accuracy | ±10% | of programmed value |
| Minimum pulse width | 0.05 | ms |
| Maximum pulse width | 2.0 | ms |
| Resolution | 0.01 | ms |
| Jitter | < 1 | µs |

---

## 2.6.8 Safety Limits

| Parameter | Minimum | Maximum | Unit | Action on Exceed |
|-----------|---------|---------|------|-----------------|
| Pulse amplitude | 0.5 | 7.5 | V | Clamp output |
| Pulse width | 0.05 | 2.0 | ms | Truncate pulse |
| Pulse current | 0.1 | 25 | mA | Current limit |
| Charge per pulse | 0 | 50 | µC | Limit output |
| Energy per pulse | 0 | 500 | µJ | Limit output |
| Pulse repetition rate | DC | URL | bpm | Rate limiting |

---

## 2.6.9 Evoked Response Detection

### Capture Verification

After each pacing pulse, the pacemaker can verify capture by detecting the
evoked response (the cardiac depolarization that follows a successful pacing
pulse).

**Capture detection methods:**

1. **Sensed evoked response**: Detect the R-wave (ventricular) or P-wave
   (atrial) that follows the pacing pulse. Requires sensing during the
   post-pace blanking period (challenging due to afterpotential).

2. **Threshold search**: Automatically adjusts the pacing output downward
   until loss of capture occurs, then sets the output to threshold + safety
   margin.

3. **Evoked response impedance**: Monitor the lead impedance during and
   after the pacing pulse to detect the impedance change associated with
   myocardial depolarization.

### Auto-Capture Algorithm

```
                    AUTO-CAPTURE ALGORITHM

  1. Start at programmed output (e.g., 3.5V, 0.4ms)
  2. Verify capture (detect evoked response)
  3. If capture confirmed:
     a. Reduce output by 0.25V (or 0.05ms)
     b. Wait N cycles (stability check)
     c. Verify capture at reduced output
     d. If capture maintained → continue reduction
     e. If loss of capture → increase output by 0.25V
     f. Set final output = threshold + 0.25V (safety margin)
  4. Repeat threshold search every 8-24 hours (programmable)
```

---

## 2.6.10 Summary

Pacing pulse generation requires careful optimization of:

1. **Strength-duration relationship**: Choose pulse width near chronaxie
   (0.5 ms) for energy-efficient pacing.

2. **Charge balancing**: Ensure net-zero charge delivery to prevent
   electrode polarization and tissue damage.

3. **Output accuracy**: Maintain ±5% voltage accuracy and ±10% pulse width
   accuracy across temperature and battery voltage variations.

4. **Safety limits**: Implement hardware limits on amplitude, width, and
   current to prevent tissue damage under fault conditions.

5. **Energy efficiency**: Optimize the output capacitor, charge pump, and
   switching circuits to minimize energy consumption from the battery.

The design of the pacing output stage is a critical subsystem that directly
impacts patient safety, battery life, and therapeutic efficacy. The circuits
and algorithms presented in this chapter provide the foundation for a
reliable, energy-efficient, and clinically effective pacing output system.
