# Chapter: DC-DC Converter Design for the iPACE-CHIP

## Table of Contents

1. [Introduction](#1-introduction)
2. [Power Rail Architecture](#2-power-rail-architecture)
3. [Buck Converter for Low-Voltage Digital Rail](#3-buck-converter-for-low-voltage-digital-rail)
4. [LDO Regulator for Analog Rail](#4-ldo-regulator-for-analog-rail)
5. [Charge Pump for High-Voltage Telemetry Rail](#5-charge-pump-for-high-voltage-telemetry-rail)
6. [Efficiency Targets](#6-efficiency-targets)
7. [Output Noise Requirements](#7-output-noise-requirements)
8. [Start-Up Sequencing](#8-start-up-sequencing)
9. [Power-On Reset (POR)](#9-power-on-reset-por)
10. [Brown-Out Detection (BOD)](#10-brown-out-detection-bod)
11. [Summary](#11-summary)

---

## 1. Introduction

The Power Management Unit (PMU) of the iPACE-CHIP must efficiently convert the battery voltage (2.4–3.6V from a LiI₂ cell) into the multiple supply rails required by the analog, digital, and telemetry subsystems. The PMU is the most critical subsystem for maximizing battery life — every milliwatt saved in the PMU directly extends the implant lifetime.

The iPACE-CHIP requires the following supply rails:

| Rail | Voltage | Consumer | Requirement |
|------|---------|----------|-------------|
| VBAT | 2.4–3.6V | Battery directly | Pacing output, charge pump input |
| VDDD | 1.2V | Digital core, SRAM, Flash | Low power, fast switching |
| VDDA | 1.8V | Analog front-end, ADC, DAC | Ultra-low noise, high PSRR |
| VDDRF | 3.3V | Telemetry RF (PA, LNA) | Low noise, burst-mode capable |
| VDDH | 5–10V | Pacing output stage (boosted) | High efficiency, charge pump |

---

## 2. Power Rail Architecture

### 2.1 Complete Power Architecture

```
┌────────────────────────────────────────────────────────────────────┐
│                    PMU POWER RAIL ARCHITECTURE                      │
│                                                                     │
│  ┌──────────┐                                                      │
│  │  LiI₂    │                                                      │
│  │  Battery │ VBAT (2.4-3.6V)                                     │
│  │  2.8V    │                                                      │
│  └────┬─────┘                                                      │
│       │                                                            │
│       ├──────────────────────┬───────────────────────┐             │
│       │                      │                       │             │
│  ┌────▼─────┐          ┌────▼─────┐          ┌─────▼────┐       │
│  │  Buck    │          │  LDO     │          │  Charge  │       │
│  │Converter │          │  1.8V    │          │  Pump    │       │
│  │  1.2V    │          │ (Analog) │          │  3.3V    │       │
│  │(Digital) │          │          │          │ (Telem.) │       │
│  └────┬─────┘          └────┬─────┘          └─────┬────┘       │
│       │                      │                      │             │
│       ▼                      ▼                      ▼             │
│  ┌──────────┐          ┌──────────┐          ┌──────────┐       │
│  │  VDDD    │          │  VDDA    │          │  VDDRF   │       │
│  │  1.2V    │          │  1.8V    │          │  3.3V    │       │
│  │ Digital  │          │  Analog  │          │   RF     │       │
│  │ Core     │          │  F.E.    │          │  Telem.  │       │
│  └──────────┘          └──────────┘          └──────────┘       │
│                                                                     │
│  ┌──────────────────────────────────────────────────────────┐     │
│  │  MONITORING & CONTROL                                      │     │
│  │                                                            │     │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐               │     │
│  │  │ Brown-   │  │ Power-On │  │ Voltage  │               │     │
│  │  │ Out      │  │ Reset    │  │ Monitor  │               │     │
│  │  │ Detector │  │ (POR)    │  │ (ADC)    │               │     │
│  │  └──────────┘  └──────────┘  └──────────┘               │     │
│  │                                                            │     │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐               │     │
│  │  │ Current  │  │ Temp.    │  │ Sequence │               │     │
│  │  │ Monitor  │  │ Sensor   │  │ Control  │               │     │
│  │  │          │  │          │  │ Logic    │               │     │
│  │  └──────────┘  └──────────┘  └──────────┘               │     │
│  └──────────────────────────────────────────────────────────┘     │
└────────────────────────────────────────────────────────────────────┘
```

### 2.2 Power Distribution Summary

| Rail | Source | Input Range | Output | Max Load | Target η |
|------|--------|-------------|--------|----------|----------|
| VDDD | Buck converter | 2.4–3.6V | 1.2V ±3% | 200 µA | > 85% |
| VDDA | LDO | 2.4–3.6V | 1.8V ±2% | 20 µA | > 60% |
| VDDRF | Charge pump/LDO | 2.4–3.6V | 3.3V ±2% | 15 mA (burst) | > 75% |
| VDDH | Charge pump | 2.4–3.6V | 5–10V (prog.) | 25 mA (burst) | > 70% |

---

## 3. Buck Converter for Low-Voltage Digital Rail

### 3.1 Buck Converter Specifications

| Parameter | Specification | Notes |
|-----------|--------------|-------|
| Input voltage | 2.4–3.6V | LiI₂ battery range |
| Output voltage | 1.2V ±3% | Digital core supply |
| Output current | 0–200 µA | Typical: 50 µA |
| Switching frequency | 500 kHz | Low frequency for low noise |
| Efficiency target | > 85% at 50–200 µA | Critical for battery life |
| Output ripple | < 50 mVpp | Tolerable for digital |
| Load regulation | ±2% | No-load to full-load |
| Line regulation | ±1% | Over VBAT range |
| Quiescent current | < 2 µA | During operation |
| Sleep current | < 100 nA | When disabled |
| Start-up time | < 5 ms | From enable to regulated output |
| Output capacitance | 100 nF (external) | Ceramic, X5R |

### 3.2 Buck Converter Architecture

```
┌──────────────────────────────────────────────────────────┐
│              INTEGRATED BUCK CONVERTER                     │
│                                                            │
│  VBAT ────┐                                               │
│           │                                               │
│      ┌────▼────┐    ┌──────────┐    ┌──────────┐        │
│      │ High-   │    │  Inductor│    │ Output   │        │
│      │ Side    │───→│  L=4.7µH │───→│ Capacitor│──→ VDDD│
│      │ Switch  │    │          │    │ C=100nF  │  (1.2V)│
│      │ (PMOS)  │    └──────────┘    └──────────┘        │
│      └────┬────┘         │                               │
│      ┌────▼────┐         │                               │
│      │ Low-    │         │                               │
│      │ Side    │         │                               │
│      │ Switch  │←────────┘                               │
│      │ (NMOS)  │    Current sense                        │
│      └────┬────┘                                         │
│      ┌────▼────┐    ┌──────────┐    ┌──────────┐        │
│      │ PWM     │←───│ Error    │←───│ Feedback │←── VDDD│
│      │ Modulator│   │ Amplifier│    │ Divider  │        │
│      │         │    │          │    │ (R1,R2)  │        │
│      └─────────┘    └──────────┘    └──────────┘        │
│                                                            │
│  Control: PFM (Pulse Frequency Modulation) at light load │
│           PWM at heavy load                               │
│           Auto-transition at ~50 µA load                  │
└──────────────────────────────────────────────────────────┘
```

### 3.3 PFM vs. PWM Operation

| Mode | Load Range | Efficiency | Ripple | Quiescent Current |
|------|-----------|------------|--------|-------------------|
| PFM (Pulse Frequency Modulation) | 0–50 µA | > 85% | Higher (< 100 mVpp) | < 1 µA |
| PWM (Pulse Width Modulation) | 50–200 µA | > 80% | Lower (< 30 mVpp) | 2–5 µA |
| Sleep (output enabled) | 0 µA load | N/A | N/A | < 100 nA |

```
PFM Operation (Light Load):

  Each pulse delivers a fixed packet of energy:
  
  Energy per pulse = ½ × L × Ipeak²
  
  At light loads, pulses are infrequent:
  
  VBAT ──→ Pulse → VBAT → Pulse → VBAT → Pulse → VBAT
           │                    │                    │
  VDDD ──→─── ─── ─── ─── ─── ─── ─── ─── ─── ────→ Regulated
           
  Frequency of pulses is proportional to load current
  Between pulses: all switches off, very low quiescent current
```

### 3.4 Buck Converter Efficiency Analysis

```
Efficiency vs. Load Current:

Efficiency
(%)
  90 ─│              ╱╲
       │            ╱  ╲
  85 ─│───────────╱────╲────────────────── Target
       │          ╱      ╲
  80 ─│         ╱        ╲──────────────
       │        ╱          ╲
  75 ─│       ╱            ╲
       │      ╱              ╲
  70 ─│     ╱                ╲
       │    ╱                  ╲
  60 ─│   ╱                    ╲
       │  ╱
  50 ─│─╱
       │
       └──────────────────────────────────→ Load Current
       0.1µA  1µA   10µA  50µA  100µA  200µA

  Key observations:
  - PFM mode dominates at < 50 µA (better efficiency)
  - PWM mode takes over at > 50 µA (lower ripple)
  - Peak efficiency at 50-100 µA load
  - Efficiency drops at very light loads (quiescent current dominates)
  - Efficiency drops at heavy loads (switching/conduction losses)
```

---

## 4. LDO Regulator for Analog Rail

### 4.1 LDO Specifications

| Parameter | Specification | Notes |
|-----------|--------------|-------|
| Input voltage | 2.4–3.6V | VBAT range |
| Output voltage | 1.8V ±2% | Analog front-end supply |
| Output current | 0–20 µA | Typical: 10 µA |
| Dropout voltage | < 200 mV at 20 µA | At minimum VBAT |
| Output noise | < 10 µVrms (0.1–100 Hz) | Critical for sensing |
| PSRR | > 60 dB at 1 kHz | Reject battery noise |
| Load regulation | ±1% | No-load to full-load |
| Line regulation | ±0.5% | Over VBAT range |
| Quiescent current | < 3 µA | During operation |
| Sleep current | < 10 nA | When disabled |
| Start-up time | < 1 ms | From enable to regulated |
| Output capacitance | 1 µF (external) | Ceramic, X5R, low ESR |

### 4.2 LDO Architecture

```
┌──────────────────────────────────────────────────────────┐
│              LOW-DROPOUT REGULATOR (LDO)                  │
│                                                            │
│  VBAT ────┬───────────────────────────────┐              │
│           │                               │              │
│      ┌────▼────────────────────┐    ┌────▼────┐        │
│      │  Pass Transistor        │    │         │        │
│      │  (PMOS, W/L = 100/1)   │────│  Output │──→ VDDA│
│      │                         │    │  Cap    │  (1.8V)│
│      └────────┬────────────────┘    │  1 µF   │        │
│               │                      └─────────┘        │
│      ┌────────▼────────┐                                │
│      │  Error Amplifier │                                │
│      │  (OTA, gm=1mS)  │←── Feedback voltage             │
│      │                  │    (from output divider or     │
│      └─────────────────┘     from output directly)      │
│                                                            │
│  Frequency compensation:                                  │
│  - Internal dominant pole at error amplifier output       │
│  - External capacitor provides second pole               │
│  - Miller compensation for stability                      │
│  - Phase margin > 60° for all load conditions            │
│                                                            │
│  Noise reduction:                                         │
│  - Low-noise error amplifier design                       │
│  - PSRR > 60 dB at LDO ripple frequency                  │
│  - Internal low-pass filter on reference                  │
│  - External output capacitor filters high-frequency noise │
└──────────────────────────────────────────────────────────┘
```

### 4.3 LDO Noise Budget

```
LDO Output Noise Budget (VDDA = 1.8V):

  Total noise requirement: < 10 µVrms (0.1–100 Hz)
  
  Noise sources:
    1. Error amplifier (thermal): 3 µVrms (30%)
    2. Error amplifier (1/f):     4 µVrms (40%)
    3. Reference voltage noise:   2 µVrms (20%)
    4. PSRR-limited input noise:  1 µVrms (10%)
    
  Total (RSS): √(3² + 4² + 2² + 1²) = √(9+16+4+1) = √30 ≈ 5.5 µVrms
  
  Margin: 10 / 5.5 = 1.8× (adequate)
  
  Note: The LDO must reject battery noise (from switching converter
  and telemetry TX) with PSRR > 60 dB at frequencies up to 10 kHz.
```

---

## 5. Charge Pump for High-Voltage Telemetry Rail

### 5.1 Charge Pump Specifications

| Parameter | Specification | Notes |
|-----------|--------------|-------|
| Input voltage | 2.4–3.6V | VBAT range |
| Output voltage | 3.3V ±2% | Telemetry RF supply |
| Output current | 0–15 mA | Burst mode (during TX) |
| Efficiency target | > 75% at 5 mA | For telemetry efficiency |
| Output ripple | < 5 mVpp | Low noise for RF |
| Quiescent current | < 1 µA | When not transmitting |
| Start-up time | < 10 ms | Before telemetry TX |
| Output capacitance | 10 µF (external) | Ceramic, low ESR |

### 5.2 Charge Pump Architecture (Regulated 3.3V Output)

```
┌──────────────────────────────────────────────────────────┐
│              REGULATED CHARGE PUMP                         │
│                                                            │
│  VBAT ────┬───────────────────────────────┐              │
│           │                               │              │
│      ┌────▼────┐   ┌──────────┐   ┌─────▼────┐        │
│      │ Flying  │──→│ Output   │──→│ LDO      │──→ VDDRF│
│      │ Capac.  │   │ Capac.   │   │ (3.3V)   │  (3.3V)│
│      │ Cfly    │   │ Cout     │   │          │        │
│      └────┬────┘   └──────────┘   └──────────┘        │
│           │                                              │
│      ┌────▼────┐                                        │
│      │ Charge  │                                        │
│      │ Pump    │←── Regulator feedback                  │
│      │ Controller│   (adjusts pump frequency            │
│      │         │    to regulate output)                 │
│      └─────────┘                                        │
│                                                            │
│  Topology: 1:2 step-up charge pump                       │
│  VOUT = 2 × VBAT - losses                                │
│  Regulation: Frequency modulation (reduce f at light load)│
│                                                            │
│  At VBAT = 2.8V: VOUT = 2 × 2.8 = 5.6V (unregulated)   │
│  LDO regulates to 3.3V (efficient, Vdropout = 5.6-3.3=   │
│  2.3V × 15mA = 34.5 mW, η_LDO = 3.3/5.6 = 59%)         │
│                                                            │
│  Better approach: Direct regulated charge pump             │
│  (skip LDO, regulate by controlling pump clock)           │
└──────────────────────────────────────────────────────────┘
```

### 5.3 Charge Pump Output Ripple

```
Charge Pump Output Ripple:

  Vout
  │
  │    ╭─╮     ╭─╮     ╭─╮     ╭─╮
  │───╯  ╰────╯  ╰────╯  ╰────╯  ╰──
  │  │←─→│
  │   Ripple (< 5 mVpp)
  │
  └────────────────────────────────────→ Time

  Ripple reduction techniques:
  1. Increase output capacitance (10 µF)
  2. Increase switching frequency (1 MHz)
  3. Add post-regulator LDO (if power budget allows)
  4. Use overlapping clock phases (reduce charge sharing)
```

---

## 6. Efficiency Targets

### 6.1 Overall PMU Efficiency

```
PMU Efficiency = (Power delivered to loads) / (Power from battery)

  P_VDDD = 1.2V × 50 µA = 60 µW
  P_VDDA = 1.8V × 10 µA = 18 µW
  P_VDDRF = 3.3V × 15 mA × 0.003 (duty cycle) = 148.5 µW (average)
  
  Total load power = 60 + 18 + 148.5 = 226.5 µW

  P_VBAT (at 2.8V, 10 µA average):
    P_battery = 2.8V × 10 µA = 28 µW (during non-telemetry)
    During telemetry: 2.8V × 15 mA = 42 mW (peak)

  Quiescent power of PMU regulators:
    Buck: 1.2V × 1 µA = 1.2 µW
    LDO: 1.8V × 3 µA = 5.4 µW
    Charge pump: 3.3V × 1 µA = 3.3 µW
    Total quiescent: ~10 µW

  Overall efficiency (during normal operation, no telemetry):
    η = 78 µW / (78 + 10) µW = 88.6% (excellent!)
```

### 6.2 Efficiency by Load Condition

| Condition | VDDD η | VDDA η | VDDRF η | Overall η |
|-----------|--------|--------|---------|-----------|
| Idle (sensing only) | 88% | 60% | N/A (off) | 82% |
| Active (pacing) | 86% | 60% | N/A (off) | 80% |
| Telemetry TX | N/A | 60% | 78% | 75% |
| Deep sleep | N/A | N/A | N/A | N/A (PMU off) |
| **Weighted average** | **87%** | **60%** | **78%** | **81%** |

---

## 7. Output Noise Requirements

### 7.1 Noise Specifications by Rail

| Rail | Noise Requirement | Frequency Band | Rationale |
|------|-------------------|----------------|-----------|
| VDDD (1.2V) | < 50 mVpp | DC–10 MHz | Digital logic tolerates noise |
| VDDA (1.8V) | < 10 mVpp | DC–100 Hz | Critical for sensing amplifier |
| VDDA (1.8V) | < 100 µVrms | 0.1–100 Hz | Input-referred noise floor |
| VDDRF (3.3V) | < 5 mVpp | DC–1 MHz | RF performance |
| VDDRF (3.3V) | < 100 µVrms | 10 kHz–100 MHz | Phase noise for modulation |

### 7.2 Noise Source Analysis

```
Noise Sources in PMU:

  1. Buck Converter (VDDD):
     - Switching ripple: ~50 mVpp at 500 kHz
     - Spread-spectrum modulation for EMI reduction
     - Does NOT directly affect analog circuits (separate rail)

  2. LDO (VDDA):
     - Error amplifier noise: 3–5 µVrms (0.1–100 Hz)
     - Reference noise: 2–3 µVrms (0.1–100 Hz)
     - PSRR: Must reject VBAT noise (from buck switching)
     - Key metric: PSRR at buck switching frequency (500 kHz)
       → PSRR > 60 dB at 500 kHz

  3. Charge Pump (VDDRF):
     - Switching ripple: 5–20 mVpp (depends on f and Cout)
     - Clock feedthrough: Harmonics of switching frequency
     - Mitigated by post-LDO or increased output capacitance

  4. Battery noise:
     - Internal resistance noise: Vnoise = √(4kTR × BW)
     - At R = 200Ω, BW = 100 kHz: Vnoise = √(4 × 1.38e-23 × 310 × 200 × 1e5) = 18.6 µVrms
     - This is very small and does not significantly impact performance
```

### 7.3 Noise Filtering Techniques

| Technique | Applied To | Effectiveness | Complexity |
|-----------|-----------|--------------|------------|
| Post-LDO (additional regulator) | VDDRF | High | Medium |
| Increase output capacitance | All rails | Moderate | Low |
| Ferrite bead (if external) | VDDA input | High | Low (external) |
| Internal low-pass filter | Reference voltage | Moderate | Low |
| Spread-spectrum clocking | Buck converter | Moderate (EMI) | Low |
| Shielding (layout) | Analog circuits | High | Medium |
| Separate supply domains | All rails | Essential | Medium |

---

## 8. Start-Up Sequencing

### 8.1 Start-Up Sequence

```
Power-On Start-Up Sequence:

Time ─────────────────────────────────────────────────────────→

VBAT      ████████████████████████████████████████████████████
          (Battery connected to chip)

POR       ░░░░░░░░░███████████████████████████████████████████
          (Released after VBAT > 2.3V for 10ms)

VDDA      ░░░░░░░░░░░░░░░░██████████████████████████████████
          (LDO starts, stabilizes after 1ms)

VDDD      ░░░░░░░░░░░░░░░░░░░░░░░░██████████████████████████
          (Buck starts, stable after 5ms, PFM mode)

CPU       ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░██████████████
          (Boot ROM executes, configures peripherals)

AFE       ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░██████████████
          (AFE registers configured, sensing enabled)

Timer     ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░██████████████
          (Timing cycles begin)

Ready     ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░██████████
          (Full operation begins, first pace/sense possible)

Total start-up time: ~15 ms from VBAT connection to ready state
```

### 8.2 Start-Up Sequencing Logic

```
Start-Up State Machine:

  State: POWER_OFF
    │
    │ VBAT > 2.3V (POR threshold)
    ▼
  State: POR_ACTIVE (10 ms delay)
    │
    │ POR timer expires
    ▼
  State: VDDA_START (LDO enable)
    │
    │ LDO output stable (> 1.7V)
    ▼
  State: VDDD_START (Buck enable)
    │
    │ Buck output stable (> 1.1V)
    ▼
  State: CLOCK_START (oscillator enable)
    │
    │ Clock stable (XTAL lock or RC stable)
    ▼
  State: CPU_START (processor boot)
    │
    │ Boot ROM execution complete
    ▼
  State: SYSTEM_CONFIG (peripheral configuration)
    │
    │ AFE configured, timer loaded, PMU monitoring enabled
    ▼
  State: READY (full operation)

  If any step fails → State: SAFE_MODE (retry or hold safe state)
```

---

## 9. Power-On Reset (POR)

### 9.1 POR Specifications

| Parameter | Specification | Notes |
|-----------|--------------|-------|
| POR threshold (rising) | 2.3V | VBAT must exceed this to release POR |
| POR threshold (falling) | 2.1V | Hysteresis to prevent chatter |
| POR delay | 10 ms | After threshold crossed |
| POR output | Active-low reset to CPU | Directly to CPU reset pin |
| POR accuracy | ±100 mV | Threshold tolerance |
| POR current | < 100 nA | Quiescent |

### 9.2 POR Circuit

```
Power-On Reset Circuit:

  VBAT ──→ Voltage Detector ──→ Delay Circuit ──→ POR_bar (to CPU)
              │                      │
              │ Threshold: 2.3V      │ 10 ms RC delay
              │ (bandgap-referenced) │ (deglitch)
              │                      │
              └── Hysteresis ────────┘
                  (200 mV)

  Behavior:
  - VBAT < 2.1V: POR_bar = 0 (CPU held in reset)
  - VBAT crosses 2.3V: Start 10 ms delay
  - After 10 ms: POR_bar = 1 (CPU released from reset)
  - VBAT drops below 2.1V: POR_bar = 0 (immediate reset, no delay)
  - Hysteresis prevents oscillation at threshold
```

---

## 10. Brown-Out Detection (BOD)

### 10.1 BOD Specifications

| Parameter | Specification | Notes |
|-----------|--------------|-------|
| BOD threshold (warning) | 2.5V | Early warning |
| BOD threshold (critical) | 2.3V | Enter safe mode |
| BOD threshold (failure) | 2.0V | Maximum power conservation |
| Hysteresis | 100 mV | Per threshold |
| Response time | < 100 µs | From detection to action |
| BOD current | < 500 nA | Quiescent (always-on comparator) |

### 10.2 BOD Response Actions

```
BOD Response Hierarchy:

  VBAT Level    │ Action
  ──────────────┼────────────────────────────────────────
  > 2.6V        │ Normal operation
  2.5–2.6V      │ Log warning, increase monitoring frequency
  2.4–2.5V      │ Disable non-essential features
  2.3–2.4V      │ Enter safe mode (VOO at LRL)
                │ Disable telemetry, auto-capture, diagnostics
  2.0–2.3V      │ Maximum power conservation
                │ Disable all non-essential circuits
                │ Only basic pacing continues
  < 2.0V        │ System may not function reliably
                │ Log last state before failure
                │ Hardware watchdog continues (separate oscillator)
```

### 10.3 BOD Circuit Architecture

```
┌──────────────────────────────────────────────────────────┐
│              BROWN-OUT DETECTOR                            │
│                                                            │
│  VBAT ──→ Voltage ──→ Comparator ──→ Logic ──→ Actions  │
│           Dividers     │                        │         │
│           (for each    │                        │         │
│            threshold)  ▼                        ▼         │
│                    ┌──────────┐          ┌──────────┐   │
│                    │Bandgap   │          │Warning   │   │
│                    │Reference │          │flag      │   │
│                    │(1.2V)    │          │          │   │
│                    └──────────┘          │Critical  │   │
│                                          │flag      │   │
│                                          │          │   │
│                                          │Safe mode │   │
│                                          │request   │   │
│                                          └──────────┘   │
│                                                            │
│  Power: < 500 nA (always-on comparators)                  │
│  Response: < 100 µs from crossing to flag/assert          │
└──────────────────────────────────────────────────────────┘
```

---

## 11. Summary

### 11.1 PMU Design Summary

| Block | Topology | Input | Output | Efficiency | Noise |
|-------|----------|-------|--------|------------|-------|
| Digital supply | Buck converter | 2.4–3.6V | 1.2V ±3% | > 85% | < 50 mVpp |
| Analog supply | LDO | 2.4–3.6V | 1.8V ±2% | > 60% | < 10 µVrms |
| Telemetry supply | Charge pump | 2.4–3.6V | 3.3V ±2% | > 75% | < 5 mVpp |
| Pacing boost | Charge pump | 2.4–3.6V | 5–10V | > 70% | N/A (pulsed) |

### 11.2 Key PMU Specifications

| Parameter | Specification |
|-----------|--------------|
| Input voltage range | 2.4–3.6V (LiI₂) |
| Number of regulated outputs | 3 (+ 1 boosted) |
| Total quiescent current (all regulators) | < 8 µA |
| Buck converter frequency | 500 kHz (PFM/PWM) |
| LDO dropout voltage | < 200 mV at 20 µA |
| Output noise (analog rail) | < 10 µVrms (0.1–100 Hz) |
| PSRR (analog LDO) | > 60 dB at 1 kHz |
| Start-up time | < 15 ms (total sequence) |
| POR threshold | 2.3V ±100 mV |
| BOD thresholds | 2.5V / 2.3V / 2.0V |
| Sleep current (all regulators off) | < 100 nA |
| Overall weighted efficiency | > 81% |

### 11.3 Power Budget Allocation

| Consumer | Power (µW) | % of Total |
|----------|-----------|------------|
| AFE (sensing) | 30 | 15% |
| Digital controller | 60 | 30% |
| Timer engine | 5 | 3% |
| PMU quiescent | 10 | 5% |
| Telemetry (wake-up RX) | 0.3 | <1% |
| Telemetry (TX, averaged) | 80 | 40% |
| Pacing (averaged) | 12 | 6% |
| **Total** | **~197** | **100%** |

The PMU is designed to deliver all supply rails with the required voltage accuracy, noise performance, and efficiency while consuming minimal quiescent current. The combination of a buck converter (for the digital rail), an LDO (for the analog rail), and charge pumps (for the telemetry and pacing rails) provides the optimal balance of efficiency and performance for the iPACE-CHIP.

---

*Next Chapter: [Power Mode Management](../03-Power-Modes/power-mode-management.md)*
