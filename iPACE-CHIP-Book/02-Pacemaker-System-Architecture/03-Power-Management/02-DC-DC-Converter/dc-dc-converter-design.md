# DC-DC Converter Design for Pacemaker SoC

## 2.3.2 Power Supply Architecture and Regulator Design

The DC-DC converter and voltage regulators form the backbone of the pacemaker's
power management system, converting the battery voltage to the multiple supply
rails required by the analog and digital subsystems. This chapter covers the
design of buck converters, charge pumps, LDO regulators, and the power-on
reset (POR) and brown-out detection (BOD) circuits.

---

## 2.10.1 Power Supply Requirements

### Supply Rails

| Rail | Voltage | Current | Noise | Load | Application |
|------|---------|---------|-------|------|------------|
| V_ANA | 2.8 V | 1-5 µA | < 10 µV RMS | AFE, DAC, references |
| V_DIG | 1.2 V | 2-10 µA | < 50 mV p-p | Digital logic, timers |
| V_PACE | 3-8 V | 0-25 mA | < 50 mV | Pacing output stage |
| V_RF | 1.8 V | 0-5 mA | < 1 mV RMS | RF transceiver |
| VREF | 1.25 V | 10 µA | < 5 µV RMS | Bandgap reference |

### Converter Requirements

| Parameter | Specification | Unit |
|-----------|--------------|------|
| Input voltage range | 2.4-3.2 | V |
| Output voltage accuracy | ±2% | — |
| Line regulation | < 1% | for 2.4-3.2 V input |
| Load regulation | < 2% | for 0-100% load |
| Output noise | < 10 µV RMS | (10 Hz - 100 kHz) |
| PSRR | > 60 dB | @ 100 kHz |
| Efficiency | ≥ 80% | — |
| Quiescent current | < 2 | µA |
| Start-up time | < 1 | ms |
| Output capacitance | 1-10 | µF |
| Ripple voltage | < 10 | mV |

---

## 2.10.2 Buck Converter Design

### Topology

The buck converter steps down the battery voltage (2.5-3.2 V) to the
digital supply voltage (1.2 V) with high efficiency.

```
                    BUCK CONVERTER TOPOLOGY

  V_BAT (2.5-3.2V)
     │
     ▼
  ┌────────┐     ┌────────┐     ┌────────┐     ┌────────┐
  │  Q1    │     │  L     │     │  C_out │     │  Load  │
  │ (PMOS) │────▶│ (1-10µH)│────▶│ (1-10µF)│────▶│        │
  └───┬────┘     └────────┘     └────────┘     └────────┘
      │
      ▼
  ┌────────┐
  │  Q2    │
  │ (NMOS) │
  └───┬────┘
      │
     GND

  Control: PWM or PFM
  Switching frequency: 100 kHz - 1 MHz
  Output voltage: V_OUT = V_BAT × D
  where D = duty cycle (0.4-0.5 for 1.2V output from 2.8V input)
```

### Operating Modes

**PWM (Pulse Width Modulation) Mode:**
- Fixed switching frequency
- Constant output ripple
- Higher efficiency at medium-to-heavy loads
- Used during active pacing and telemetry

**PFM (Pulse Frequency Modulation) Mode:**
- Variable switching frequency
- Lower quiescent current
- Higher efficiency at light loads
- Used during sleep and idle modes

### PWM Control Loop

```
                    PWM CONTROL LOOP

  V_OUT ──▶┌──────────┐    ┌──────────┐    ┌──────────┐
           │  Error   │    │  PWM     │    │  Power   │
  V_REF ──▶│  Amp     │───▶│  Comp.   │───▶│  Stage   │──▶ V_OUT
           │          │    │          │    │  (Q1,Q2) │
           └──────────┘    └──────────┘    └──────────┘
                │                              │
                │         ┌──────────┐         │
                └─────────│  Slope   │◀────────┘
                          │  Comp.   │
                          └──────────┘
```

### Inductor Selection

```
  L = (V_BAT - V_OUT) × D / (f_sw × ΔI_L)

  where:
    V_BAT = 2.8 V (nominal)
    V_OUT = 1.2 V
    D = V_OUT / V_BAT = 0.43
    f_sw = 500 kHz (switching frequency)
    ΔI_L = 0.5 × I_OUT (ripple current, 50% of load)

  For I_OUT = 5 µA:
    ΔI_L = 2.5 µA
    L = (2.8 - 1.2) × 0.43 / (500e3 × 2.5e-6)
    L = 0.688 / 1.25
    L = 0.55 H → Too large for light load

  Practical approach: Use PFM mode for light loads (< 10 µA)
  and PWM mode for heavier loads (> 10 µA)
```

### Output Capacitor Selection

```
  C_out = ΔI_L / (8 × f_sw × ΔV_OUT)

  where:
    ΔI_L = inductor ripple current
    ΔV_OUT = output voltage ripple

  For ΔI_L = 0.5 mA (PWM mode), ΔV_OUT = 5 mV, f_sw = 500 kHz:
    C_out = 0.5e-3 / (8 × 500e3 × 5e-3)
    C_out = 0.5e-3 / 20
    C_out = 25 µF → Use 22 µF standard value

  ESR requirement:
    ESR < ΔV_OUT / ΔI_L = 5e-3 / 0.5e-3 = 10 Ω
    Practical: ESR < 100 mΩ (ceramic capacitor)
```

---

## 2.10.3 Charge Pump Design

### Dickson Charge Pump (Voltage Doubler)

The Dickson charge pump is used to generate the analog supply voltage
(2.8 V) from the battery (2.5-3.2 V) without an inductor:

```
                    DICKSON CHARGE PUMP

  V_BAT ──┬──▶|├──┬──▶|├──┬──▶|├──┬──▶ V_OUT
          │   C1    │   C2    │   C3    │
          │   │     │   │     │   │     │
         GND  │    GND  │    GND  │    GND
              │         │         │
           φ1▼       φ2▼       φ1▼
           (CLK)    (CLK)    (CLK)

  V_OUT = (N + 1) × V_BAT × η

  where:
    N = number of stages (2-3)
    η = charge transfer efficiency (0.85-0.95)
    f_CLK = clock frequency (100-500 kHz)

  For N = 2, V_BAT = 2.8V, η = 0.9:
    V_OUT = 3 × 2.8 × 0.9 = 7.56V → Too high for analog supply
```

### LDO Post-Regulator

A low-dropout (LDO) regulator is used after the charge pump to provide
a low-noise, well-regulated analog supply:

```
                    LDO POST-REGULATOR

  V_CP (charge pump output)
     │
     ▼
  ┌────────────────────────────────────┐
  │  LDO REGULATOR                     │
  │                                    │
  │  V_CP ──▶┌────────┐               │
  │          │ PMOS   │               │
  │          │ Pass   │               │
  │          │ Trans. │               │
  │          └───┬────┘               │
  │              │                     │
  │              ▼                     │
  │  V_REF ──▶┌────────┐──▶ V_OUT     │
  │           │ Error  │    (2.8V)     │
  │           │ Amp    │               │
  │           └────────┘               │
  │                                    │
  │  Dropout voltage: < 200 mV         │
  │  PSRR: > 60 dB @ 100 kHz          │
  │  Output noise: < 10 µV RMS         │
  │  Quiescent current: < 1 µA         │
  └────────────────────────────────────┘
```

---

## 2.10.4 LDO Regulator Design

### LDO Architecture

```
                    LDO REGULATOR DETAILED

  V_IN ────────────────┬────────────────────────────
                       │
                       ▼
                  ┌─────────┐
                  │  PMOS   │
                  │  Pass   │
                  │  Trans. │
                  │  (W/L)  │
                  └────┬────┘
                       │
                       ├──────────────────────────── V_OUT
                       │
                       ▼
                  ┌─────────┐
                  │  C_out  │ (1-10 µF)
                  │         │
                  └────┬────┘
                       │
                      GND

  Control Loop:
  
  V_OUT ──▶┌──────────┐    ┌──────────┐
           │  Voltage │    │  Error   │
  V_REF ──▶│  Divider │───▶│  Amp    │──▶ Gate of PMOS
           │  (R1/R2) │    │          │
           └──────────┘    └──────────┘
```

### LDO Specifications

| Parameter | Specification | Unit |
|-----------|--------------|------|
| Input voltage | 2.5-3.2 | V |
| Output voltage | 2.8 | V |
| Dropout voltage | < 200 | mV |
| Output current | 0-50 | µA |
| Line regulation | < 0.1% | /V |
| Load regulation | < 0.5% | /mA |
| PSRR (100 kHz) | > 60 | dB |
| Output noise | < 10 | µV RMS |
| Quiescent current | < 1 | µA |
| Load transient response | < 50 | µs settling |
| Stability (phase margin) | > 60 | degrees |

### Pass Transistor Sizing

The PMOS pass transistor must be sized to handle the maximum load current
with the minimum dropout voltage:

```
  R_on = 1 / (µ_p × C_ox × (W/L) × (V_GS - V_th))

  For: V_dropout = 200 mV, I_load = 50 µA
  R_on_max = V_dropout / I_load = 200 mV / 50 µA = 4 kΩ

  For: µ_p × C_ox = 50 µA/V², V_th = -0.4V, V_GS = -2.8V
  (W/L) = 1 / (µ_p × C_ox × R_on × (|V_GS| - |V_th|))
        = 1 / (50e-6 × 4000 × (2.8 - 0.4))
        = 1 / (50e-6 × 4000 × 2.4)
        = 1 / 0.48
        = 2.08

  Use W/L = 10/1 (conservative sizing for process variation)
```

### Compensation Network

The LDO requires frequency compensation to ensure stability:

```
  Compensation components:

  C_out: Main output capacitor (1-10 µF)
    - Provides the dominant pole
    - Must be ceramic (low ESR) for stability

  C_c: Compensation capacitor (10-100 pF)
    - Provides the second pole
    - Connected from output to error amp input

  R_c: Compensation resistor (10-100 kΩ)
    - Provides the zero
    - Compensates the ESR zero of C_out

  Phase margin: > 60° (target: 70-80°)
  Gain margin: > 10 dB
  Unity-gain bandwidth: > 100 kHz
```

### PSRR Analysis

Power Supply Rejection Ratio (PSRR) is critical for the analog supply:

```
  PSRR(f) = 20 × log₁₀(ΔV_IN / ΔV_OUT)

  At DC: PSRR = A_OL × β (open-loop gain × feedback factor)
  At high frequency: PSRR limited by output capacitor ESR

  Target: PSRR > 60 dB at 100 kHz
  This requires:
    - High open-loop gain (> 60 dB)
    - High unity-gain bandwidth (> 1 MHz)
    - Low ESR output capacitor (< 100 mΩ)
    - Proper compensation (phase margin > 60°)
```

---

## 2.10.5 Power-On Reset (POR) Circuit

### POR Requirements

| Parameter | Specification | Unit |
|-----------|--------------|------|
| Rising threshold | 2.1-2.3 | V |
| Hysteresis | 50-100 | mV |
| Propagation delay | < 10 | µs |
| Reset pulse width | 1-10 | ms |
| Glitch rejection | < 1 | µs |
| Quiescent current | < 100 | nA |
| Operating voltage | 1.5-3.5 | V |

### POR Circuit Design

```
                    POR CIRCUIT

  V_BAT ────────┬────────────────────────────────
                │
                ▼
           ┌─────────┐
           │  Voltage │
           │  Detect  │ (Comparator with hysteresis)
           │  (V_th = │
           │   2.2V)  │
           └────┬─────┘
                │
                ▼
           ┌─────────┐
           │  Delay  │ (RC delay for glitch rejection)
           │  Filter │
           │  (1-10µs)│
           └────┬─────┘
                │
                ▼
           ┌─────────┐
           │  One-   │ (Generates clean reset pulse)
           │  Shot   │
           │  (1-10ms)│
           └────┬─────┘
                │
                ▼
           ┌─────────┐
           │  RESET  │ (Active-high reset signal)
           │  OUTPUT │
           └─────────┘
```

### POR Timing Diagram

```
  V_BAT
    │
  2.5├────────────────────────────────────────
    │         ┌──────────────────────────────
  2.3├─────────┤
    │         │ ← Rising threshold
  2.1├─────────┤
    │         │
  1.5├─────────┤
    │         │
    0├─────────┤
    │         │
    │         │     RESET
    │         │     │
    │         │     ▼
    │         │     ┌──────────────────────────
    │         │     │
    │         │     │ ← Reset active (low)
    │         │     │
    │         │     └─────────────────────────
    │         │         ↑
    │         │         Reset released
    │         │         (after delay)
    │
    0├────┬────┬────┬────┬────┬────┬────
         t0   t1   t2   t3   t4
         │    │    │    │    │
         │    │    │    │    System operational
         │    │    │    Reset released
         │    │    Delay expires
         │    Threshold crossed
         Power applied
```

---

## 2.10.6 Brown-Out Detection (BOD) Circuit

### BOD Requirements

| Parameter | Specification | Unit |
|-----------|--------------|------|
| Low threshold | 2.4-2.5 | V |
| High threshold | 2.5-2.6 | V |
| Hysteresis | 50-100 | mV |
| Propagation delay | < 10 | µs |
| Quiescent current | < 100 | nA |
| Alert generation | Yes | — |
| Safe mode entry | Yes | — |

### BOD Circuit Design

```
                    BROWN-OUT DETECTION

  V_BAT ────────┬────────────────────────────────
                │
                ▼
           ┌─────────┐
           │  Voltage │
           │  Detect  │ (Comparator with hysteresis)
           │  (V_low = │
           │   2.4V,  │
           │   V_high =│
           │   2.5V)  │
           └────┬─────┘
                │
                ├──▶ BOD_ALERT (to digital controller)
                │
                └──▶ SAFE_MODE_ENTRY (to power management)
```

### BOD Timing Diagram

```
  V_BAT
    │
  2.8├────────────────────────────────────────
    │
  2.6├────────────────────────────────────────
    │
  2.5├──────┐           ┌───────────────────── Hysteresis high
    │       │           │
  2.4├──────┘           └───────────────────── Hysteresis low
    │       │           │
  2.2├──────┤           ├─────────────────────
    │       │           │
  2.0├──────┤           ├─────────────────────
    │       │           │
    0├──────┤           ├─────────────────────
    │       │           │
    │       │ BOD_ALERT │
    │       │ │         │
    │       ▼ │         ▼
    │    ┌────┤     ┌────┤
    │    │ ON │     │OFF │
    │    └────┘     └────┘
```

---

## 2.10.7 High-Voltage Charge Pump for Pacing

### Requirements

The pacing output stage requires a programmable high voltage (3-8 V) from
the low-voltage battery (2.5-3.2 V):

| Parameter | Specification | Unit |
|-----------|--------------|------|
| Input voltage | 2.4-3.2 | V |
| Output voltage | 3.0-8.0 | V (programmable) |
| Output current | 0-25 | mA |
| Output ripple | < 50 | mV |
| Efficiency | ≥ 80 | % |
| Start-up time | < 50 | µs |
| Output capacitance | 10-33 | µF |
| Quiescent current | < 5 | µA |

### Topology Selection

For the pacing output stage, a Dickson charge pump is preferred over an
inductive boost converter because:

1. **No external inductor**: The charge pump uses only capacitors, which
   are smaller and cheaper than inductors.
2. **Lower EMI**: No magnetic switching noise that could interfere with
   sensitive sensing circuits.
3. **Simpler layout**: No need for magnetic component placement and
   shielding.
4. **Sufficient current**: 25 mA is achievable with a multi-stage charge
   pump.

### Dickson Charge Pump Design

```
                    DICKSON CHARGE PUMP (6-Stage)

  V_BAT ──┬──▶|├──┬──▶|├──┬──▶|├──┬──▶|├──┬──▶|├──┬──▶|├──┬──▶ V_PACE
          │   C1    │   C2    │   C3    │   C4    │   C5    │   C6
          │   │     │   │     │   │     │   │     │   │     │
         GND  │    GND  │    GND  │    GND  │    GND  │    GND
              │         │         │         │         │
           φ1▼       φ2▼       φ1▼       φ2▼       φ1▼       φ2▼
           (CLK1)   (CLK2)   (CLK1)   (CLK2)   (CLK1)   (CLK2)

  V_PACE = V_BAT × (N + 1) × η

  For N = 6, V_BAT = 2.8V, η = 0.85:
    V_PACE = 7 × 2.8 × 0.85 = 16.66V → Too high!

  Practical design: N = 2-3 stages with regulation
  V_PACE = 3-8V (programmable via clock duty cycle)
```

### Output Voltage Regulation

The output voltage is regulated by adjusting the clock duty cycle or
frequency:

```
  Regulation methods:

  1. Duty cycle modulation:
     V_OUT = V_BAT × (N + 1) × D × η
     where D = duty cycle (0.3-0.8)

  2. Frequency modulation:
     Higher frequency → higher output voltage
     Lower frequency → lower output voltage

  3. Stage bypassing:
     Connect/disconnect charge pump stages
     Fewer stages → lower output voltage

  4. Post-regulation:
     LDO after charge pump for fine regulation
     Less efficient but simpler control
```

---

## 2.10.8 Power Sequencing

### Start-Up Sequence

```
                    POWER SEQUENCING

  Step 1: Battery Connected
    │
    ▼
  Step 2: POR detects V_BAT > V_threshold
    │
    ▼
  Step 3: Enable bandgap reference
    │
    ▼
  Step 4: Enable LDO regulators (V_ANA, V_DIG)
    │
    ▼
  Step 5: Wait for regulators to settle (< 1 ms)
    │
    ▼
  Step 6: Enable clock oscillator
    │
    ▼
  Step 7: Release digital reset
    │
    ▼
  Step 8: Execute Power-On Self-Test (POST)
    │
    ▼
  Step 9: Load parameters from EEPROM
    │
    ▼
  Step 10: Enter normal operation mode
    │
    ▼
  Step 11: Begin sensing and pacing
```

### Shutdown Sequence

```
  Step 1: Low-battery detected (V_BAT < 2.4V)
    │
    ▼
  Step 2: Reduce pacing output to minimum
    │
    ▼
  Step 3: Disable telemetry
    │
    ▼
  Step 4: Disable non-essential functions
    │
    ▼
  Step 5: Enter minimum-power pacing mode (VOO at 60 bpm)
    │
    ▼
  Step 6: Critical battery (V_BAT < 2.2V)
    │
    ▼
  Step 7: Enter hibernate mode (timer-only operation)
    │
    ▼
  Step 8: Device end-of-life (V_BAT < 2.0V)
    │
    ▼
  Step 9: Device ceases operation
```

---

## 2.10.9 Efficiency Analysis

### Converter Efficiency

```
  Efficiency = P_OUT / P_IN = (V_OUT × I_OUT) / (V_BAT × I_BAT)

  Buck converter losses:
    P_loss = P_switching + P_conduction + P_gate + P_quiescent

  P_switching = 0.5 × C_oss × V² × f_sw (output capacitance loss)
  P_conduction = I² × R_on × D (conduction loss)
  P_gate = Q_g × V_GS × f_sw (gate drive loss)
  P_quiescent = V_BAT × I_quiescent (quiescent loss)
```

### Efficiency vs. Load Current

```
  Efficiency
  (%)
    │
  100├──────────────────────────────────────
    │
   90├─────────────╲    ╱──────────────────
    │               ╲  ╱
   80├────────────────╲╱──────────────────── PWM mode
    │                 ╳
   70├────────────────╱╲────────────────────
    │               ╱  ╲
   60├─────────────╱    ╲──────────────────
    │            ╱      ╲
   50├──────────╱        ╲─────────────────
    │         ╱
   40├────────╱──────────────────────────── PFM mode
    │       ╱
   30├──────╱───────────────────────────────
    │     ╱
   20├────╱─────────────────────────────────
    │
   10├───╱──────────────────────────────────
    │
    0├───┬────┬────┬────┬────┬────┬────
    0  0.1µA 1µA  10µA 100µA 1mA  10mA
              Load Current

    PFM mode: Higher efficiency at light loads
    PWM mode: Higher efficiency at heavy loads
    Crossover: ~10-50 µA (programmable)
```

---

## 2.10.10 Summary

The DC-DC converter and voltage regulator design is critical for:

1. **Efficiency**: High converter efficiency (> 80%) directly extends
   battery life by reducing wasted energy.

2. **Noise**: Low-noise analog supply (V_ANA) with < 10 µV RMS noise
   and > 60 dB PSRR is essential for sensitive cardiac signal detection.

3. **Regulation**: Tight voltage regulation (±2%) ensures consistent
   pacing output and accurate threshold detection.

4. **Power sequencing**: Proper start-up and shutdown sequences prevent
   latch-up, ensure safe operation, and protect patient safety.

5. **Safety**: POR and BOD circuits provide fail-safe operation under
   all power conditions, including brown-out and battery depletion.

The combination of a buck converter (for digital supply), charge pump with
LDO (for analog supply), and high-voltage charge pump (for pacing output)
provides an efficient, low-noise, and reliable power management system for
the implantable pacemaker.
