# 02.1.1 — Pacemaker System Block Diagram

> **Section 02: Pacemaker System Architecture**
> **Subsection 01: System-Level Design — Block Diagram**

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [Top-Level System Overview](#2-top-level-system-overview)
3. [Core Functional Blocks](#3-core-functional-blocks)
   - 3.1 [Sensing Subsystem](#31-sensing-subsystem)
   - 3.2 [Pacing Output Subsystem](#32-pacing-output-subsystem)
   - 3.3 [Timing and Control Logic](#33-timing-and-control-logic)
   - 3.4 [Power Management Unit](#34-power-management-unit)
   - 3.5 [Telemetry and Communication](#35-telemetry-and-communication)
   - 3.6 [Non-Volatile Memory](#36-non-volatile-memory)
   - 3.7 [Battery and Energy Source](#37-battery-and-energy-source)
4. [Complete System Block Diagram](#4-complete-system-block-diagram)
5. [Signal Flow Analysis](#5-signal-flow-analysis)
6. [Inter-Block Interfaces](#6-inter-block-interfaces)
7. [Package and Lead Connections](#7-package-and-lead-connections)
8. [Redundancy and Safety Architecture](#8-redundancy-and-safety-architecture)
9. [Summary](#9-summary)
10. [References](#10-references)

---

## 1. Introduction

An implantable cardiac pacemaker is one of the most constrained mixed-signal
system-on-chip (SoC) designs in biomedical engineering. The entire device must
operate reliably for **8–15 years** on a single battery, occupy less than
**30 cm³** in total volume, weigh under **40 g**, and meet stringent
biocompatibility and electrical safety standards (ISO 14708, IEC 60601-1-2).

The block diagram is the single most important architectural artifact: it
defines every functional block, its data/control interfaces, power domains, and
fault boundaries. This chapter presents the canonical pacemaker block diagram
used across single- and dual-chamber devices, then elaborates every block in
sufficient detail for IC-level implementation.

### 1.1 Design Constraints Summary

| Parameter              | Typical Value                    |
|------------------------|----------------------------------|
| Battery voltage        | 2.5–3.2 V (LiI / LiCFx)        |
| Total chip area        | 4–12 mm² (CMOS 130–180 nm)      |
| Supply current (active)| 8–25 µA                          |
| Supply current (sleep) | 1–4 µA                           |
| Operating temperature  | 35–40 °C (in vivo)               |
| Sensing dynamic range  | 0.1–10 mV (intracardiac)        |
| Pacing output voltage  | 0.5–7.5 V (programmable)        |
| Pacing output pulse    | 0.05–1.5 ms (programmable)       |
| Telemetry frequency    | 175–210 kHz (MICS/MedRadio)     |
| Data rate (uplink)     | 8–256 kbps                       |
| Lifetime               | > 8 years (300 mAh battery)      |

---

## 2. Top-Level System Overview

The pacemaker can be decomposed into **seven major functional blocks** plus
the **battery**. The following diagram shows the top-level partitioning:

```
┌─────────────────────────────────────────────────────────────────────┐
│                     PACEMAKER IMPLANT (HERMETIC CASE)               │
│                                                                     │
│  ┌───────────┐  ┌───────────┐  ┌───────────┐  ┌─────────────────┐  │
│  │  SENSING  │  │  PACING   │  │  TIMING   │  │   TELEMETRY &   │  │
│  │SUBSYSTEM  │  │  OUTPUT   │  │  CONTROL  │  │ COMMUNICATION   │  │
│  │           │  │SUBSYSTEM  │  │   LOGIC   │  │                 │  │
│  │ ┌───────┐ │  │ ┌───────┐ │  │ ┌───────┐ │  │ ┌─────────────┐ │  │
│  │ │ LNA   │ │  │ │ HV    │ │  │ │ State │ │  │ │ RF Front-End│ │  │
│  │ │ + AFE │ │  │ │ Driver│ │  │ │Machine│ │  │ │ + Modulator │ │  │
│  │ └───────┘ │  │ └───────┘ │  │ └───────┘ │  │ └─────────────┘ │  │
│  │ ┌───────┐ │  │ ┌───────┐ │  │ ┌───────┐ │  │ ┌─────────────┐ │  │
│  │ │ ADC   │ │  │ │ Charge│ │  │ │ Timer │ │  │ │ Protocol    │ │  │
│  │ │ (ΣΔ)  │ │  │ │Pump   │ │  │ │ Array │ │  │ │ Engine      │ │  │
│  │ └───────┘ │  │ └───────┘ │  │ └───────┘ │  │ └─────────────┘ │  │
│  │ ┌───────┐ │  │ ┌───────┐ │  │ ┌───────┐ │  │ ┌─────────────┐ │  │
│  │ │ Band- │ │  │ │ Output│ │  │ │ µP /  │ │  │ │ EEPROM      │ │  │
│  │ │ pass  │ │  │ │Cap    │ │  │ │ µC    │ │  │ │ Controller  │ │  │
│  │ │ Filter│ │  │ │Bank   │ │  │ │ Core  │ │  │ └─────────────┘ │  │
│  │ └───────┘ │  │ └───────┘ │  │ └───────┘ │  │                 │  │
│  └─────┬─────┘  └─────┬─────┘  └─────┬─────┘  └────────┬────────┘  │
│        │              │              │                   │           │
│        │    ┌─────────┴─────────┐    │                   │           │
│        │    │                   │    │                   │           │
│        │    │  POWER MANAGEMENT │    │                   │           │
│        │    │       UNIT        │    │                   │           │
│        │    │  ┌─────────────┐  │    │                   │           │
│        │    │  │  DC-DC      │  │    │                   │           │
│        │    │  │  Converter  │  │    │                   │           │
│        │    │  └─────────────┘  │    │                   │           │
│        │    │  ┌─────────────┐  │    │                   │           │
│        │    │  │  Voltage    │  │    │                   │           │
│        │    │  │  Regulator  │  │    │                   │           │
│        │    │  └─────────────┘  │    │                   │           │
│        │    │  ┌─────────────┐  │    │                   │           │
│        │    │  │  Brownout   │  │    │                   │           │
│        │    │  │  Detector   │  │    │                   │           │
│        │    │  └─────────────┘  │    │                   │           │
│        │    └───────────────────┘    │                   │           │
│        │              │              │                   │           │
│   ┌────┴──────────────┴──────────────┴───────────────────┴────┐     │
│   │                    BATTERY / ENERGY SOURCE                 │     │
│   │              (LiI, LiCFx, or Solid-State Li-ion)          │     │
│   └───────────────────────────────────────────────────────────┘     │
│                                                                     │
│   ┌───────────────────────────────────────────────────────────┐     │
│   │              NON-VOLATILE MEMORY (EEPROM/FRAM)            │     │
│   │     Parameters │ Diagnostics │ Episode Data │ Log        │     │
│   └───────────────────────────────────────────────────────────┘     │
│                                                                     │
└───────────────────────────────────┬─────────────────────────────────┘
                                    │
                          Lead Connectors
                                    │
                    ┌───────────────┼───────────────┐
                    │               │               │
              ┌─────┴─────┐  ┌─────┴─────┐  ┌─────┴─────┐
              │  Atrial   │  │Ventricular│  │  (Optional │
              │   Lead    │  │   Lead    │  │  CRT Lead) │
              └───────────┘  └───────────┘  └───────────┘
```

---

## 3. Core Functional Blocks

### 3.1 Sensing Subsystem

The sensing subsystem detects the intrinsic cardiac electrical activity
(P-waves in the atrium, R-waves in the ventricle). It must reliably distinguish
true cardiac depolarization from noise, skeletal muscle artifacts, and
electromagnetic interference (EMI).

#### 3.1.1 Sensing Subsystem Internal Block Diagram

```
                        INTRACARDIAC SIGNAL
                              │
                              ▼
                  ┌───────────────────────┐
                  │   Protection Network  │
                  │   (ESD + Overvoltage) │
                  │                       │
                  │  ┌─────────────────┐  │
                  │  │ Back-to-back    │  │
                  │  │ clamp diodes    │  │
                  │  │ + TVS array     │  │
                  │  └─────────────────┘  │
                  └───────────┬───────────┘
                              │
                              ▼
                  ┌───────────────────────┐
                  │  Input MUX / Switch   │
                  │  (Polarity Reversal)  │
                  │                       │
                  │  Programmable:        │
                  │  • Bipolar / Unipolar │
                  │  • Polarity select    │
                  └───────────┬───────────┘
                              │
                              ▼
                  ┌───────────────────────┐
                  │  High-Pass Filter     │
                  │  (AC-coupled input)   │
                  │                       │
                  │  fc = 0.5–8 Hz        │
                  │  (programmable)       │
                  │                       │
                  │  Eliminates DC offset │
                  │  and baseline wander  │
                  └───────────┬───────────┘
                              │
                              ▼
                  ┌───────────────────────┐
                  │  Low-Noise Amplifier  │
                  │  (Instrumentation     │
                  │   Amplifier Topology) │
                  │                       │
                  │  Gain: 40–80 dB       │
                  │  CMRR: > 100 dB       │
                  │  Input noise: <1 µVrms│
                  │  Input impedance:     │
                  │    > 10 kΩ            │
                  │  GBW: ~500 kHz        │
                  └───────────┬───────────┘
                              │
                              ▼
                  ┌───────────────────────┐
                  │  Programmable Gain     │
                  │  Amplifier (PGA)       │
                  │                       │
                  │  Gain steps:          │
                  │  0.25x to 32x         │
                  │  (0.25 dB steps)      │
                  └───────────┬───────────┘
                              │
                              ▼
                  ┌───────────────────────┐
                  │  Band-Pass Filter     │
                  │  (Anti-alias + Signal │
                  │   conditioning)       │
                  │                       │
                  │  Low-pass: 80–200 Hz  │
                  │  High-pass: 0.5–20 Hz │
                  │  Notch: 50/60 Hz opt  │
                  └───────────┬───────────┘
                              │
                              ▼
                  ┌───────────────────────┐
                  │  Comparator /         │
                  │  Threshold Detector   │
                  │                       │
                  │  Programmable thresh: │
                  │  0.125–5.0 mV        │
                  │                       │
                  │  Auto-adjust:         │
                  │  • Auto-fail          │
                  │  • Sensitivity adapt  │
                  └───────────┬───────────┘
                              │
                              ▼
                  ┌───────────────────────┐
                  │  Blankling &          │
                  │  Refractory Logic     │
                  │                       │
                  │  • Post-pace blanking:│
                  │    200–500 ms         │
                  │  • Post-sense blank:  │
                  │    100–400 ms         │
                  │  • Noise sampling     │
                  │  • Double-count prev  │
                  └───────────┬───────────┘
                              │
                              ▼
                    SENSE DETECTED (DIGITAL)
                         │          │
                    ┌────┘          └────┐
                    ▼                    ▼
              Timer Interrupt      Event Counter
              (R-R / P-P          (for diagnostics)
               intervals)
```

#### 3.1.2 Sensing Subsystem Specifications

| Parameter                    | Minimum   | Typical    | Maximum   | Unit  |
|------------------------------|-----------|------------|-----------|-------|
| Input-referred noise         | —         | 0.6        | 1.5       | µVrms |
| Input impedance              | 10        | 100        | 1000      | kΩ    |
| CMRR                         | 80        | 100        | 120       | dB    |
| PSRR                         | 60        | 80         | —         | dB    |
| Total gain                   | 40        | 60         | 80        | dB    |
| Bandpass low corner          | 0.5       | 1.0        | 20        | Hz    |
| Bandpass high corner         | 80        | 100        | 200       | Hz    |
| Threshold resolution         | —         | 0.0625     | —         | mV    |
| Threshold range              | 0.125     | —          | 5.0       | mV    |
| Sensing dynamic range        | 0.1       | —          | 10.0      | mV    |
| Slew rate (input)            | 0.1       | —          | 5.0       | V/s   |
| Power consumption            | 1.5       | 3.0        | 8.0       | µA    |

#### 3.1.3 Noise Rejection Strategy

The sensing chain must reject multiple noise sources:

```
┌──────────────────────────────────────────────────────────────┐
│                  NOISE SOURCE REJECTION                       │
├─────────────────────┬──────────────────┬─────────────────────┤
│ Noise Source        │ Frequency Range  │ Rejection Method    │
├─────────────────────┼──────────────────┼─────────────────────┤
│ DC offset           │ 0 Hz             │ AC coupling (HPF)   │
│ Baseline wander     │ 0.05–0.5 Hz      │ HPF + adaptive      │
│ Respiratory artifact │ 0.1–0.5 Hz      │ HPF corner tuning   │
│ Muscle artifact (EMG)│ 20–2000 Hz      │ LPF + blanking      │
│ Power line          │ 50/60 Hz         │ Notch filter (opt)  │
│ RF interference     │ > 1 MHz          │ LPF + ESD network   │
│ T-wave oversensing  │ 1–10 Hz          │ Morphology + blank  │
│ Lead fracture noise │ Wideband         │ Impedance monitor   │
│ Electrosurgery      │ 100 kHz–5 MHz    │ Refractory + blank  │
│ Defibrillation      │ Transient        │ Post-shock blanking │
└─────────────────────┴──────────────────┴─────────────────────┘
```

---

### 3.2 Pacing Output Subsystem

The pacing output subsystem generates the precisely controlled electrical pulse
delivered to the myocardium through the pacing lead.

#### 3.2.1 Pacing Output Block Diagram

```
                    CONTROL SIGNALS FROM TIMING LOGIC
                              │
                              ▼
              ┌───────────────────────────────┐
              │     PACING CONTROL LOGIC      │
              │                               │
              │  • Pulse width timer          │
              │  • Amplitude DAC              │
              │  • Charge/discharge sequence  │
              │  • Safety shunt control       │
              │  • Polarity control           │
              └───────────┬───────────────────┘
                          │
                          ▼
              ┌───────────────────────────────┐
              │    CHARGE PUMP / HV DRIVER    │
              │                               │
              │  Input:  Vbat (2.5–3.2 V)     │
              │  Output: 0.5–7.5 V            │
              │  Efficiency: > 85%            │
              │                               │
              │  ┌─────────────────────────┐  │
              │  │  Boost Converter        │  │
              │  │  or Charge Pump         │  │
              │  │  (2x, 3x, or 4x)       │  │
              │  └─────────────────────────┘  │
              └───────────┬───────────────────┘
                          │
                          ▼
              ┌───────────────────────────────┐
              │   OUTPUT VOLTAGE DAC          │
              │                               │
              │  Resolution: 8–12 bit         │
              │  Range: 0.5–7.5 V            │
              │  Step size: < 20 mV          │
              │  Settling time: < 5 µs       │
              │  INL/DNL: < ±1 LSB          │
              └───────────┬───────────────────┘
                          │
                          ▼
              ┌───────────────────────────────┐
              │    OUTPUT CAPACITOR BANK      │
              │                               │
              │  ┌────┐ ┌────┐ ┌────┐        │
              │  │C1  │ │C2  │ │C3  │  ...   │
              │  │1µF │ │2µF │ │4µF │        │
              │  └────┘ └────┘ └────┘        │
              │                               │
              │  Total: 1–15 µF (selectable)  │
              │  Type: Ceramic / Tantalum     │
              │  ESR: < 100 mΩ               │
              │  Voltage rating: ≥ 10 V      │
              └───────────┬───────────────────┘
                          │
                          ▼
              ┌───────────────────────────────┐
              │    OUTPUT SWITCH NETWORK      │
              │                               │
              │  ┌─────────────────────────┐  │
              │  │  Anode/Cathode Mux     │  │
              │  │  (Polarity control)    │  │
              │  └─────────────────────────┘  │
              │  ┌─────────────────────────┐  │
              │  │  Safety Shunt Resistor │  │
              │  │  Rshunt = 1–10 kΩ     │  │
              │  │  (auto-discharge)      │  │
              │  └─────────────────────────┘  │
              └───────────┬───────────────────┘
                          │
                          ▼
                    TO PACING LEAD
                   (Anode / Cathode)
```

#### 3.2.2 Pacing Output Waveform

The pacing pulse is a truncated, controlled-current or controlled-voltage
waveform. The standard voltage-source + capacitor model produces:

```
  Voltage at
  Lead Tip (V)
      │
  Vmax├─────────┐
      │         │
      │         │ ← Capacitor discharge through lead impedance
      │         │    V(t) = Vmax · exp(-t/τ)
      │         │    where τ = Rlead · Cout
      │         │
      │         │         ╱
      │         │        ╱  ← Tail (depends on polarization)
      │         │───────╱
      │         │
  0   ├─────────┴───────────────────────────▶ Time
      │         │← pw →│
      │     Pulse start   Pulse end
      │
      │         ← Post-pulse polarization: typically 0.3–1.5 V
```

The delivered energy per pulse:

```
            V²max
  E = ───────────── · pw · (1 - exp(-2·pw/τ))
         Rlead

  Where:
    E     = Energy per pulse (Joules)
    Vmax  = Peak output voltage (V)
    Rlead = Lead impedance (Ω), typically 300–1500 Ω
    pw    = Pulse width (s), typically 0.05–1.5 ms
    τ     = Rlead · Cout (s)
```

#### 3.2.3 Pacing Output Specifications

| Parameter                    | Minimum | Typical  | Maximum | Unit   |
|------------------------------|---------|----------|---------|--------|
| Output voltage range         | 0.5     | 2.5–5.0  | 7.5     | V      |
| Output voltage resolution    | —       | 0.025    | 0.1     | V      |
| Pulse width range            | 0.05    | 0.4      | 1.5     | ms     |
| Pulse width resolution       | —       | 0.01     | 0.1     | ms     |
| Maximum output current       | 10      | 25       | 100     | mA     |
| Load impedance range         | 100     | 300–700  | 2000    | Ω      |
| Charge pump efficiency       | 70      | 85       | 95      | %      |
| Output capacitor range       | 1.0     | 3.3–10   | 15      | µF     |
| Safety shunt resistance      | 0.5     | 5.0      | 20      | kΩ     |
| Post-pulse discharge time    | —       | < 10     | 50      | ms     |
| Pulse amplitude accuracy     | —       | ±5%      | ±10     | %      |
| Pulse width accuracy         | —       | ±2%      | ±5      | %      |
| Power consumption (pacing)   | —       | 15       | 80      | µA     |

---

### 3.3 Timing and Control Logic

The timing and control logic is the "brain" of the pacemaker. It implements
the pacing algorithm, manages all subsystem coordination, and handles
diagnostic data collection.

#### 3.3.1 Timing and Control Block Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                   TIMING AND CONTROL LOGIC                       │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                    MICROCONTROLLER CORE                   │   │
│  │                                                          │   │
│  │  ┌──────────┐  ┌──────────┐  ┌───────────────────────┐ │   │
│  │  │  8/16-bit│  │  Program │  │   Data Memory         │ │   │
│  │  │  CPU     │  │  Memory  │  │   (SRAM + NVM)        │ │   │
│  │  │  Core    │  │  (ROM/   │  │                       │ │   │
│  │  │          │  │  Flash)  │  │   • Parameters        │ │   │
│  │  │  RISC    │  │  4–32 KB │  │   • State variables   │ │   │
│  │  │  ISA     │  │          │  │   • Diagnostic log    │ │   │
│  │  │          │  │          │  │   • Episode buffer    │ │   │
│  │  └──────────┘  └──────────┘  └───────────────────────┘ │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                  HARDWARE TIMER ARRAY                     │   │
│  │                                                          │   │
│  │  Timer 0: Lower Rate Interval (LRI)                      │   │
│  │  Timer 1: AV Delay (programmable)                        │   │
│  │  Timer 2: Refractory Period                              │   │
│  │  Timer 3: Blanking Period                                │   │
│  │  Timer 4: Maximum Tracking Rate                          │   │
│  │  Timer 5: Diagnostic sampling                            │   │
│  │  Timer 6: Watchdog / Safety timer                        │   │
│  │  Timer 7: Telemetry timebase                             │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │              PACING STATE MACHINE (HW)                    │   │
│  │                                                          │   │
│  │  ┌────────┐    ┌────────┐    ┌────────┐    ┌────────┐  │   │
│  │  │ IDLE   │───▶│ SENSING│───▶│ PACING │───▶│REFRACT.│  │   │
│  │  │        │◀───│  WAIT  │◀───│OUTPUT  │◀───│  PERIOD│  │   │
│  │  └────────┘    └────────┘    └────────┘    └────────┘  │   │
│  │      │                            │                     │   │
│  │      ▼                            ▼                     │   │
│  │  ┌────────┐                  ┌────────┐                 │   │
│  │  │ SLEEP  │                  │BLANKING│                 │   │
│  │  │  MODE  │                  │ PERIOD │                 │   │
│  │  └────────┘                  └────────┘                 │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                  SAFETY MONITORING                        │   │
│  │                                                          │   │
│  │  • Watchdog timer (hardware, non-maskable)               │   │
│  │  • Stack overflow detector                               │   │
│  │  • Clock monitor (external crystal + RC)                 │   │
│  │  • Voltage brownout detector                             │   │
│  │  • Radiation soft-error detection (ECC/parity)           │   │
│  │  • Program flow integrity (CRC check)                    │   │
│  │  • Hardware-locked pacing rate limits                    │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

#### 3.3.2 State Machine — DDD Pacing Mode

The following state machine represents the complete DDD (dual-demand-dual)
pacing mode, the most common mode for dual-chamber pacemakers:

```
                          ┌──────────────┐
                          │   POWER ON   │
                          │   RESET      │
                          └──────┬───────┘
                                 │
                                 ▼
                          ┌──────────────┐
                          │  INIT        │
                          │  (Load NVM   │
                          │   params)    │
                          └──────┬───────┘
                                 │
                    ┌────────────┤
                    ▼            ▼
             ┌──────────┐  ┌──────────┐
             │ ATRIAL   │  │VENTRICULR│
             │ WAIT     │  │ WAIT     │
             │ (LRI-a)  │  │ (LRI-v)  │
             └────┬─────┘  └────┬─────┘
                  │              │
          ┌───────┤        ┌────┤
          │       │        │    │
          ▼       ▼        ▼    ▼
    ┌─────────┐ ┌──────┐ ┌─────┐ ┌──────┐
    │A-SENSE  │ │A-PACE│ │V-   │ │V-    │
    │DETECTED │ │OUTPUT│ │SENSE│ │PACE  │
    └────┬────┘ └──┬───┘ │DETD │ │OUTPUT│
         │         │     └──┬──┘ └──┬───┘
         │         │        │       │
         ▼         ▼        ▼       ▼
    ┌────────────────────────────────────┐
    │         AV DELAY TIMER             │
    │    (sensed AV or paced AV)         │
    └──────────────┬─────────────────────┘
                   │
          ┌────────┤
          ▼        ▼
   ┌──────────┐ ┌──────┐
   │ V-SENSE  │ │V-PACE│
   │ IN window│ │OUTPUT│
   └────┬─────┘ └──┬───┘
        │           │
        ▼           ▼
   ┌────────────────────┐
   │ POST-V REFRACTORY  │
   │   (PVARP)          │
   └────────┬───────────┘
            │
            ▼
        (Return to
         ATRIAL WAIT)
```

---

### 3.4 Power Management Unit

The power management unit (PMU) is responsible for efficiently converting
battery voltage to all required supply rails while minimizing quiescent
current consumption.

#### 3.4.1 Power Management Block Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                   POWER MANAGEMENT UNIT                          │
│                                                                  │
│  BATTERY INPUT                                                   │
│  Vbat = 2.5–3.2 V                                               │
│     │                                                            │
│     ├──►┌─────────────────────┐                                  │
│     │   │ BATTERY VOLTAGE     │──── Vbat_monitor ──── ADC       │
│     │   │ MONITOR (Divider)   │                                  │
│     │   └─────────────────────┘                                  │
│     │                                                            │
│     ├──►┌─────────────────────┐                                  │
│     │   │ BROWNOUT DETECTOR   │──── BOD_interrupt ──── µC       │
│     │   │ Threshold: 2.0 V   │                                  │
│     │   │ Hysteresis: 100 mV │                                  │
│     │   └─────────────────────┘                                  │
│     │                                                            │
│     ├──►┌─────────────────────┐                                  │
│     │   │ MAIN LDO            │──── Vdd = 1.8 V                 │
│     │   │ (Low-dropout)       │     for Digital Core             │
│     │   │ Iq = 2–5 µA        │                                  │
│     │   │ PSRR: > 60 dB      │                                  │
│     │   └─────────────────────┘                                  │
│     │                                                            │
│     ├──►┌─────────────────────┐                                  │
│     │   │ ANALOG LDO          │──── Vdda = 1.8 V                │
│     │   │ (Low-noise)         │     for Analog Blocks            │
│     │   │ Iq = 1–3 µA        │     (Sensing, ADC)               │
│     │   │ PSRR: > 80 dB      │                                  │
│     │   │ Noise: < 10 µVrms  │                                  │
│     │   └─────────────────────┘                                  │
│     │                                                            │
│     ├──►┌─────────────────────┐                                  │
│     │   │ HV CHARGE PUMP      │──── Vhv = 5.0–7.5 V            │
│     │   │ (Boost / Dickson)   │     for Pacing Output            │
│     │   │ Efficiency: > 85%   │                                  │
│     │   │ Output: 0.5–7.5 V   │                                  │
│     │   └─────────────────────┘                                  │
│     │                                                            │
│     └──►┌─────────────────────┐                                  │
│         │ REFERENCE VOLTAGE   │──── Vref = 1.024 / 1.2 V       │
│         │ (Bandgap)           │     for DACs, ADCs               │
│         │ TC: < 50 ppm/°C    │                                  │
│         │ Accuracy: ±1%      │                                  │
│         └─────────────────────┘                                  │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │              POWER DOMAIN PARTITIONING                    │   │
│  │                                                          │   │
│  │  Domain 0: Always-on (Brownout, watchdog, RTC)           │   │
│  │  Domain 1: Sensing (can be duty-cycled)                  │   │
│  │  Domain 2: Pacing (active only during pulse)             │   │
│  │  Domain 3: Digital core (active during computation)      │   │
│  │  Domain 4: Telemetry (active during communication)       │   │
│  │  Domain 5: Memory (active during read/write)             │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

#### 3.4.2 Power Domain Specification

| Power Domain       | Voltage (V) | Quiescent (µA) | Active (µA) | Duty Cycle |
|--------------------|-------------|----------------|-------------|------------|
| Always-on          | 1.8         | 0.5            | 0.5         | 100%       |
| Sensing            | 1.8         | 0.1            | 3.0         | 5–30%      |
| Pacing             | 1.8 / HV    | 0.05           | 50          | 0.1%       |
| Digital core       | 1.8         | 0.2            | 8.0         | 10–50%     |
| Telemetry          | 1.8         | 0.1            | 12          | 1–5%       |
| Memory             | 1.8         | 0.05           | 2.0         | 2–10%      |
| **Total (typical)**| —           | **1.0**        | **75.5**    | —          |

---

### 3.5 Telemetry and Communication

#### 3.5.1 Telemetry Block Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                 TELEMETRY SUBSYSTEM                          │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐   │
│  │              DIGITAL BACKEND                          │   │
│  │                                                      │   │
│  │  ┌────────────┐  ┌────────────┐  ┌──────────────┐  │   │
│  │  │ Protocol   │  │ Data       │  │ Encryption   │  │   │
│  │  │ Encoder/   │  │ Framing    │  │ / Decryption │  │   │
│  │  │ Decoder    │  │ Engine     │  │ (AES-128)    │  │   │
│  │  └────────────┘  └────────────┘  └──────────────┘  │   │
│  │                                                      │   │
│  │  ┌────────────┐  ┌────────────┐  ┌──────────────┐  │   │
│  │  │ Packet     │  │ CRC/       │  │ Error        │  │   │
│  │  │ Buffer     │  │ Checksum   │  │ Correction   │  │   │
│  │  │ (FIFO)     │  │ Generator  │  │ (FEC)        │  │   │
│  │  └────────────┘  └────────────┘  └──────────────┘  │   │
│  └──────────────────────────────────────────────────────┘   │
│                              │                               │
│                              ▼                               │
│  ┌──────────────────────────────────────────────────────┐   │
│  │              ANALOG FRONT-END                         │   │
│  │                                                      │   │
│  │  TRANSMIT PATH:                                      │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────────────┐  │   │
│  │  │ Modulator│→ │ PA Driver│→ │ Power Amplifier   │  │   │
│  │  │ (FSK/ASK)│  │          │  │ (Class-E/C)       │  │   │
│  │  └──────────┘  └──────────┘  └──────────────────┘  │   │
│  │                                                      │   │
│  │  RECEIVE PATH:                                       │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────────────┐  │   │
│  │  │ LNA      │→ │ Mixer/   │→ │ Demodulator       │  │   │
│  │  │          │  │ IF Amp   │  │ (FSK/ASK)        │  │   │
│  │  └──────────┘  └──────────┘  └──────────────────┘  │   │
│  │                                                      │   │
│  │  ┌──────────────────────────────────────────────┐   │   │
│  │  │           ANTENNA TUNING NETWORK              │   │   │
│  │  │  L-match / Pi-match                          │   │   │
│  │  │  Frequency: 175–210 kHz (MedRadio)           │   │   │
│  │  │  or 401–406 MHz (MICS)                       │   │   │
│  │  └──────────────────────────────────────────────┘   │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

### 3.6 Non-Volatile Memory

#### 3.6.1 Memory Map Overview

```
┌─────────────────────────────────────────────────────────────┐
│              NON-VOLATILE MEMORY MAP                         │
│              Total: 16–128 KB EEPROM/FRAM                    │
│                                                              │
│  Address Range       │ Size    │ Purpose                     │
│  ────────────────────┼─────────┼─────────────────────────── │
│  0x0000 – 0x00FF     │ 256 B   │ Device ID & Serial Number  │
│  0x0100 – 0x03FF     │ 768 B   │ Factory Calibration Data   │
│  0x0400 – 0x07FF     │ 1 KB    │ Operating Parameters       │
│  0x0800 – 0x0FFF     │ 2 KB    │ Patient-Specific Params    │
│  0x1000 – 0x1FFF     │ 4 KB    │ Diagnostic Counters        │
│  0x2000 – 0x3FFF     │ 8 KB    │ Episode/EGM Storage        │
│  0x4000 – 0x5FFF     │ 8 KB    │ Event Log (FIFO)           │
│  0x6000 – 0x6FFF     │ 4 KB    │ Self-Test Results          │
│  0x7000 – 0x7FFF     │ 4 KB    │ Reserved / Scratchpad      │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐   │
│  │             PARAMETER BLOCK DETAIL                    │   │
│  │                                                      │   │
│  │  Offset  │ Parameter            │ Default            │   │
│  │  ────────┼──────────────────────┼────────────────────│   │
│  │  0x0400  │ Pacing Mode (bytes)  │ DDD (0x44 0x44 0x44)│  │
│  │  0x0403  │ Lower Rate (bpm)     │ 60                 │   │
│  │  0x0404  │ Upper Rate (bpm)     │ 120                │   │
│  │  0x0405  │ AV Delay (ms)        │ 150                │   │
│  │  0x0407  │ PVAI Delay (ms)      │ 250                │   │
│  │  0x0409  │ Atrial Amp (V)       │ 3.5                │   │
│  │  0x040A  │ Vent Amp (V)         │ 4.0                │   │
│  │  0x040B  │ Atrial PW (ms)       │ 0.4                │   │
│  │  0x040C  │ Vent PW (ms)         │ 0.4                │   │
│  │  0x040D  │ Atrial Sens (mV)     │ 1.0                │   │
│  │  0x040E  │ Vent Sens (mV)       │ 2.0                │   │
│  │  0x040F  │ Refractory A (ms)    │ 200                │   │
│  │  0x0411  │ Refractory V (ms)    │ 250                │   │
│  │  0x0413  │ PVARP (ms)           │ 300                │   │
│  │  0x0415  │ Sensitivity Mode     │ Auto               │   │
│  │  0x0416  │ Hysteresis (bpm)     │ 0 (off)            │   │
│  │  0x0417  │ Rate Drop Resp       │ Off                │   │
│  │  0x0418  │ Lead Config          │ Bipolar            │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

### 3.7 Battery and Energy Source

```
┌─────────────────────────────────────────────────────────────┐
│              BATTERY / ENERGY SOURCE                          │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐   │
│  │              PRIMARY CELL                             │   │
│  │                                                      │   │
│  │  Chemistry: LiI₂ or LiCFx (lithium carbon            │
│  │             monofluoride)                             │   │
│  │                                                      │   │
│  │  ┌────────────┐                                      │   │
│  │  │  ┌──────┐  │  Nominal voltage: 2.8 V (LiCFx)     │   │
│  │  │  │ Li   │  │  or 3.2 V (LiI₂)                    │   │
│  │  │  │Anode │  │                                      │   │
│  │  │  ├──────┤  │  Capacity: 1.0–3.0 Ah               │   │
│  │  │  │ I₂ / │  │  Energy density: 300–800 Wh/kg      │   │
│  │  │  │CFx   │  │  Self-discharge: < 1%/year           │   │
│  │  │  │Cathode│  │  Operating temp: 25–45 °C           │   │
│  │  │  └──────┘  │                                      │   │
│  │  │  Separator │  Internal resistance: 10–50 Ω       │   │
│  │  └────────────┘  (increases at end-of-life)          │   │
│  │                                                      │   │
│  │  ┌──────────────────────────────────────────────┐   │   │
│  │  │  BATTERY DISCHARGE CHARACTERISTIC            │   │   │
│  │  │                                              │   │   │
│  │  │  Vbat (V)                                    │   │   │
│  │  │  3.5 ┤                                       │   │   │
│  │  │      │╲                                      │   │   │
│  │  │  3.0 ┤ ╲_________________________            │   │   │
│  │  │      │                        ╲             │   │   │
│  │  │  2.5 ┤                         ╲____        │   │   │
│  │  │      │                              ╲       │   │   │
│  │  │  2.0 ┤                               ╲      │   │   │
│  │  │      │                                ╲     │   │   │
│  │  │  1.5 ┤                                 ╲    │   │   │
│  │  │      │         EOL                      ╲   │   │   │
│  │  │      ├──────┬──────┬──────┬──────┬──────╲─  │   │   │
│  │  │      0    2.5    5.0    7.5   10.0   12.5   │   │   │
│  │  │              Capacity Discharged (%)         │   │   │
│  │  └──────────────────────────────────────────────┘   │   │
│  │                                                      │   │
│  │  EOL Detection:                                      │   │
│  │  • Vbat < 2.4 V under load                          │   │
│  │  • Internal resistance > 100 Ω                      │   │
│  │  • Rate of voltage change > threshold               │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## 4. Complete System Block Diagram

The following is the fully integrated system block diagram showing all
blocks and their interconnections:

```
┌──────────────────────────────────────────────────────────────────────────────────┐
│                          COMPLETE PACEMAKER SoC BLOCK DIAGRAM                     │
│                                                                                  │
│  LEAD INPUTS                                                                     │
│  ══════════                                                                      │
│  Atrial+ ──┐                        ┌── Vdd  (1.8V Digital)                     │
│  Atrial- ──┤                        ├── Vdda (1.8V Analog)                      │
│            ├──►┌─────────────────┐  ├── Vref (1.024V)                           │
│  Vent+   ──┤  │  ESD / PROTECT  │  ├── Vhv   (5–7.5V Pacing)                   │
│  Vent-   ──┘  │  NETWORK        │  ├── Vbat  (2.5–3.2V)                        │
│               └────────┬────────┘  │                                             │
│                        │           │                                             │
│                        ▼           │  ┌───────────────────────────────────────┐  │
│               ┌─────────────────┐  │  │        TELEMETRY SUBSYSTEM            │  │
│               │  INPUT MUX      │  │  │                                       │  │
│               │  (Bipolar/Uni)  │  │  │  ┌─────────┐  ┌──────────┐          │  │
│               └────────┬────────┘  │  │  │ Mod/    │  │ Protocol │          │  │
│                        │           │  │  │ Demod   │  │ Engine   │          │  │
│           ┌────────────┤           │  │  └────┬────┘  └────┬─────┘          │  │
│           ▼            ▼           │  │       │            │                │  │
│   ┌──────────────┐ ┌──────────┐   │  │  ┌────┴────────────┴──────┐         │  │
│   │ ATRIAL SENS. │ │VENTR.    │   │  │  │   ANTENNA INTERFACE    │         │  │
│   │ CHAIN        │ │SENSING   │   │  │  │   (Tank + Matching)    │         │  │
│   │              │ │CHAIN     │   │  │  └────────────────────────┘         │  │
│   │ ┌──────────┐ │ │┌────────┐│   │  │                                     │  │
│   │ │HPF→LNA→ │ │ ││HPF→LNA││   │  └───────────────────────────────────────┘  │
│   │ │PGA→LPF→ │ │ ││→PGA→  ││   │                                             │
│   │ │Comp      │ │ ││LPF→   ││   │  ┌───────────────────────────────────────┐  │
│   │ └──────────┘ │ ││Comp   ││   │  │     NON-VOLATILE MEMORY                │  │
│   └──────┬───────┘ │└───────┘│   │  │                                       │  │
│          │         └────┬────┘   │  │  ┌─────────┐  ┌──────────┐          │  │
│          │              │        │  │  │ EEPROM  │  │ FRAM     │          │  │
│          │              │        │  │  │ 16–64KB │  │ (opt.)   │          │  │
│          ▼              ▼        │  │  └─────────┘  └──────────┘          │  │
│   ┌──────────────────────────┐   │  └───────────────────────────────────────┘  │
│   │                          │   │                                             │
│   │   TIMING & CONTROL LOGIC │   │  ┌───────────────────────────────────────┐  │
│   │                          │   │  │        PACING OUTPUT SUBSYSTEM        │  │
│   │  ┌────────────────────┐  │   │  │                                       │  │
│   │  │  µC/µP CORE       │  │◄──┤  │  ┌──────────┐  ┌─────────────┐      │  │
│   │  │  (8/16-bit RISC)  │──┼───┼─►│  │ Charge   │  │ Output DAC  │      │  │
│   │  └────────────────────┘  │   │  │  │ Pump/HV  │  │ (8–12 bit)  │      │  │
│   │  ┌────────────────────┐  │   │  │  └─────┬────┘  └──────┬──────┘      │  │
│   │  │  TIMER ARRAY       │  │   │  │        │              │             │  │
│   │  │  (8 timers)        │──┼───┼─►│  ┌─────┴──────────────┴──────┐      │  │
│   │  └────────────────────┘  │   │  │  │    OUTPUT SWITCH NETWORK  │      │  │
│   │  ┌────────────────────┐  │   │  │  │    (Polarity + Shunt)    │      │  │
│   │  │  SAFETY MONITOR    │  │   │  │  └──────────────┬───────────┘      │  │
│   │  │  (WDT, CLKMON)     │  │   │  │                 │                  │  │
│   │  └────────────────────┘  │   │  └─────────────────┼──────────────────┘  │
│   └──────────┬───────────────┘   │                    │                      │
│              │                   │                    │                      │
│              │                   │                    ▼                      │
│              │                   │            PACING LEAD OUTPUTS            │
│              ▼                   │         (Atrial + Ventricular)           │
│   ┌──────────────────────────┐   │                                          │
│   │  POWER MANAGEMENT UNIT   │   │                                          │
│   │                          │   │                                          │
│   │  ┌────────────────────┐  │   │                                          │
│   │  │ DC-DC / Charge Pump│  │   │                                          │
│   │  │ (Vbat → Vhv)       │  │   │                                          │
│   │  └────────────────────┘  │   │                                          │
│   │  ┌────────────────────┐  │   │                                          │
│   │  │ LDO (Digital)      │  │   │                                          │
│   │  │ Vbat → Vdd (1.8V) │  │   │                                          │
│   │  └────────────────────┘  │   │                                          │
│   │  ┌────────────────────┐  │   │                                          │
│   │  │ LDO (Analog)       │  │   │                                          │
│   │  │ Vbat → Vdda (1.8V)│  │   │                                          │
│   │  └────────────────────┘  │   │                                          │
│   │  ┌────────────────────┐  │   │                                          │
│   │  │ Bandgap Reference  │  │   │                                          │
│   │  │ Vref = 1.024V      │  │   │                                          │
│   │  └────────────────────┘  │   │                                          │
│   │  ┌────────────────────┐  │   │                                          │
│   │  │ Brownout Detector  │  │   │                                          │
│   │  └────────────────────┘  │   │                                          │
│   └──────────┬───────────────┘   │                                          │
│              │                   │                                          │
│              ▼                   │                                          │
│   ┌──────────────────────────┐   │                                          │
│   │    BATTERY (LiCFx)       │   │                                          │
│   │    2.8V nom, 1.5 Ah      │   │                                          │
│   │    10–15 year life       │   │                                          │
│   └──────────────────────────┘   │                                          │
│                                                                                  │
└──────────────────────────────────────────────────────────────────────────────────┘
```

---

## 5. Signal Flow Analysis

### 5.1 Sensing Signal Path

The complete signal path from the intracardiac electrode to the digital
sense event is:

```
Electrode → ESD Protection → Input MUX → AC Coupling (HPF) → LNA → PGA →
BPF → ADC/Comparator → Blank/Refractory Logic → Sense Event
```

**Total signal path delay (latency):**

```
  t_sense = t_ESD + t_MUX + t_HPF + t_LNA + t_PGA + t_BPF + t_comp

  Typical values:
    t_ESD  ≈ 0     (passive, instantaneous)
    t_MUX  ≈ 0.1 µs
    t_HPF  ≈ 0.5 ms (dominated by filter settling)
    t_LNA  ≈ 0.5 µs
    t_PGA  ≈ 0.5 µs
    t_BPF  ≈ 1.0 ms (dominated by group delay)
    t_comp ≈ 0.5 µs

  Total:  t_sense ≈ 1.5–2.5 ms
```

### 5.2 Pacing Output Signal Path

From the timing logic decision to the actual current delivery:

```
Timer Compare → DAC Set → Charge Pump Enable → Output Switch → Lead
```

**Total pacing output latency:**

```
  t_pace = t_DAC + t_charge + t_switch + t_lead

  Typical values:
    t_DAC    ≈ 2 µs  (settling time)
    t_charge ≈ 50 µs (charge pump ramp-up)
    t_switch ≈ 1 µs  (MOSFET switching)
    t_lead   ≈ 0.1 µs (lead electrical transit)

  Total:  t_pace ≈ 50–100 µs
```

### 5.3 Telemetry Signal Path

```
Data → Protocol Encoder → Modulator → PA → Antenna → (Body tissue) →
External Coil → Demodulator → Protocol Decoder → Host PC
```

---

## 6. Inter-Block Interfaces

### 6.1 Interface Summary Table

| Source Block        | Destination Block       | Interface Type     | Width | Protocol        |
|---------------------|-------------------------|--------------------|-------|-----------------|
| Sensing AFE         | Timing/Control          | Digital event      | 1 bit | Interrupt       |
| Sensing ADC         | Timing/Control          | Serial (SPI)       | 16 bit| SPI Master      |
| Timing/Control      | Pacing DAC              | Serial (SPI)       | 12 bit| SPI Master      |
| Timing/Control      | Pacing HV Enable        | Digital control    | 1 bit | GPIO            |
| Timing/Control      | Telemetry Modulator     | Serial (UART)      | 8 bit | Async serial    |
| Telemetry Demod     | Timing/Control          | Serial (UART)      | 8 bit | Async serial    |
| Timing/Control      | EEPROM                  | I²C / SPI          | 8 bit | I²C Master      |
| PMU → All           |                         | Power rails        | —     | LDO outputs     |
| Battery Monitor     | PMU → ADC               | Analog voltage     | 1 ch  | SAR ADC input   |
| Watchdog            | Timing/Control          | Non-maskable IRQ   | 1 bit | HW reset        |
| Clock Gen           | All blocks              | Clock signal       | 1 bit | 32.768 kHz      |

### 6.2 SPI Bus Architecture

```
                    SPI MASTER (µC Core)
                          │
                          │ MOSI    MISO    SCLK    CS
                          │  │       │       │      │
            ┌─────────────┼──┼───────┼───────┼──────┼──────────┐
            │             │  │       │       │      │          │
            ▼             ▼  ▲       ▲       ▼      ▼          │
        ┌───────┐    ┌──────────┐  ┌───────┐  ┌──────────┐    │
        │ ADC   │    │ Pacing   │  │ EEPROM│  │ Telemetry│    │
        │ (16b) │    │ DAC(12b) │  │ (8b)  │  │ Codec    │    │
        └───────┘    └──────────┘  └───────┘  └──────────┘    │
                                                               │
            Note: Individual CS lines for each peripheral       │
```

---

## 7. Package and Lead Connections

### 7.1 Hermetic Package

```
┌─────────────────────────────────────────────────────────────┐
│              PACEMAKER PACKAGE CROSS-SECTION                  │
│                                                              │
│  ┌───────────────────────────────────────────────────────┐  │
│  │                Titanium Header                         │  │
│  │  ┌─────┐  ┌─────┐  ┌─────┐  ┌─────┐  ┌─────┐       │  │
│  │  │Pin 1│  │Pin 2│  │Pin 3│  │Pin 4│  │Pin 5│  ...   │  │
│  │  │     │  │     │  │     │  │     │  │     │        │  │
│  │  └──┬──┘  └──┬──┘  └──┬──┘  └──┬──┘  └──┬──┘        │  │
│  └─────┼────────┼────────┼────────┼────────┼─────────────┘  │
│        │        │        │        │        │                  │
│  ┌─────┴────────┴────────┴────────┴────────┴─────────────┐  │
│  │                                                        │  │
│  │              Hermetic Sealed Case                      │  │
│  │              (Titanium, Grade 1/2)                     │  │
│  │              Wall thickness: 0.3–0.5 mm                │  │
│  │                                                        │  │
│  │  ┌────────────────────────────────────────────────┐   │  │
│  │  │           PACEMAKER SoC                        │   │  │
│  │  │           (Wire-bonded die)                    │   │  │
│  │  └────────────────────────────────────────────────┘   │  │
│  │                                                        │  │
│  │  ┌────────────────────────────────────────────────┐   │  │
│  │  │           BATTERY CELL                          │   │  │
│  │  │           (LiCFx or LiI₂)                      │   │  │
│  │  └────────────────────────────────────────────────┘   │  │
│  │                                                        │  │
│  │  ┌────────────────────────────────────────────────┐   │  │
│  │  │           HYBRID CIRCUIT SUBSTRATE              │   │  │
│  │  │           (Passive components)                  │   │  │
│  │  │  • Output capacitors (1–15 µF)                 │   │  │
│  │  │  • Filter capacitors                           │   │  │
│  │  │  • ESD protection components                   │   │  │
│  │  │  • Crystal oscillator                          │   │  │
│  │  └────────────────────────────────────────────────┘   │  │
│  │                                                        │  │
│  │              Glass-to-metal seals                      │  │
│  │              (for lead pins)                           │  │
│  │                                                        │  │
│  └────────────────────────────────────────────────────────┘  │
│                                                              │
│  Total Volume: < 30 cm³ (typical: 15–25 cm³)                │
│  Total Weight: < 40 g (typical: 20–35 g)                    │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### 7.2 Pin Assignment

| Pin # | Function            | Direction  | Notes                          |
|-------|---------------------|------------|--------------------------------|
| 1     | Atrial Tip          | I/O        | Sensing + Pacing               |
| 2     | Atrial Ring         | I/O        | Bipolar return / Unipolar GND  |
| 3     | Ventricle Tip       | I/O        | Sensing + Pacing               |
| 4     | Ventricle Ring      | I/O        | Bipolar return / Unipolar GND  |
| 5     | HV Charge Pump Cap  | I/O        | External charge pump capacitor |
| 6     | Vref Decoupling     | Output     | Reference voltage bypass       |
| 7     | Telemetry Coil      | I/O        | Inductive telemetry antenna    |
| 8     | Case Ground          | Ground     | Connected to titanium case     |
| 9     | Battery Anode       | Power      | Connected to battery +         |
| 10    | Battery Cathode     | Power      | Connected to battery −         |

---

## 8. Redundancy and Safety Architecture

### 8.1 Safety Features Hierarchy

```
┌─────────────────────────────────────────────────────────────┐
│              SAFETY ARCHITECTURE HIERARCHY                    │
│                                                              │
│  LEVEL 1: HARDWARE-ONLY SAFETY (no software dependency)     │
│  ├── Watchdog timer (non-maskable)                          │
│  ├── Voltage brownout detector                              │
│  ├── Hardware rate limiter (max pacing rate)                │
│  ├── Output voltage clamp                                   │
│  ├── Lead impedance short/open detector                     │
│  ├── Safety shunt resistor (passive discharge)              │
│  └── Radiation-hardened flip-flops (for SEU)                │
│                                                              │
│  LEVEL 2: FIRMWARE-ENFORCED SAFETY                          │
│  ├── Program flow integrity (CRC-based)                     │
│  ├── Stack overflow detection                               │
│  ├── Dual-processor cross-check (if implemented)            │
│  ├── Parameter reasonableness checks                        │
│  ├── Clock frequency monitor                                │
│  └── Temperature sensor + shutdown                          │
│                                                              │
│  LEVEL 3: EXTERNAL SAFETY (Clinician/System)                │
│  ├── Programmer telemetry verification                      │
│  ├── Parameter download confirmation                        │
│  ├── Remote monitoring data integrity                       │
│  └── Electromagnetic interference mode (ERI)                │
│                                                              │
│  LEVEL 4: FAIL-SAFE BEHAVIORS                               │
│  ├── Power-on reset → safe default parameters               │
│  ├── Loss of communication → revert to last-known params    │
│  ├── Invalid parameter checksum → revert to backup          │
│  ├── Battery EOL → mode switch to VOO (asynchronous)        │
│  └── Critical fault → asynchronous pacing at VOO 80 bpm     │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### 8.2 Failure Mode and Effects Summary

| Failure Mode                | Detection Method         | Response               | Safety Level |
|-----------------------------|--------------------------|------------------------|--------------|
| Battery voltage low         | BOD + ADC monitoring     | EOL alert, VOO mode   | Level 1      |
| Lead fracture (open)        | Impedance measurement    | Alert, reconfigure     | Level 1+2    |
| Lead short circuit          | Impedance measurement    | Disable output, alert  | Level 1      |
| Crystal oscillator failure  | Clock monitor            | Switch to RC backup    | Level 1+2    |
| Microcontroller lockup      | Watchdog timer           | Hardware reset         | Level 1      |
| Memory corruption           | CRC / ECC detection      | Reload from backup     | Level 2      |
| Sensing failure (no sense)  | Timeout detection        | Asynchronous pacing    | Level 1+2    |
| T-wave oversensing          | Morphology analysis      | Extend blanking        | Level 2      |
| EMI interference            | Energy detection + blank | Enter interference mode| Level 1+2    |
| Radiation (SEU event)       | ECC / parity check       | Correct / reset        | Level 1      |
| Over-temperature            | On-chip sensor           | Disable, alert         | Level 1+2    |
| DC-DC converter failure     | Output monitoring        | Bypass to battery      | Level 1      |

---

## 9. Summary

The pacemaker block diagram represents a highly integrated mixed-signal SoC
with seven major functional blocks:

1. **Sensing Subsystem**: Detects intrinsic cardiac activity with µV-level
   sensitivity and rejects multiple noise sources through cascaded filtering
   and blanking strategies.

2. **Pacing Output Subsystem**: Generates precisely controlled voltage pulses
   (0.5–7.5 V, 0.05–1.5 ms) through a charge-pump-driven output stage with
   programmable amplitude and pulse width.

3. **Timing and Control Logic**: Implements the complete pacing state machine
   (e.g., DDD mode) using a combination of hardware timers and a programmable
   microcontroller core.

4. **Power Management Unit**: Provides all supply rails (digital, analog, HV)
   from a single battery with ultra-low quiescent current (< 1 µA for
   always-on domain).

5. **Telemetry and Communication**: Enables bidirectional data exchange with
   external programmers through inductive or RF links at 175–406 MHz.

6. **Non-Volatile Memory**: Stores operating parameters, diagnostic data,
   and episode recordings with 16–128 KB capacity.

7. **Battery**: Primary lithium cell providing 2.5–3.2 V with 1.0–3.0 Ah
   capacity for 8–15 year implant lifetime.

The safety architecture employs four levels of redundancy, from
hardware-only protections to external verification, ensuring patient safety
under all foreseeable fault conditions.

---

## 10. References

1. ISO 14708-1:2014 — Implants for surgery — Active implantable medical devices
2. IEC 60601-1-2:2014 — EMC requirements for medical electrical equipment
3. ANSI/AAMI NASPE/DFB-002:2013 — Pacemaker terminology
4. Webster, A. "Design of Cardiac Pacemakers," IEEE Press, 1995.
5. Schaldach, M. "The Pacemaker Design Process," in *Advances in Pacemaker Technology*, Springer, 1985.
6. Greatbatch, W. "The Historical Development of the Pacemaker," *Pacing and Clinical Electrophysiology*, 1990.
7. Mallela, V.S. et al. "Trends in pacemaker technology," *IEEE Engineering in Medicine and Biology*, 2004.
8. Rudge, R. "Pacemaker Generator Design," in *Cardiac Pacemakers and Resynchronization Therapy*, Springer, 2014.

---

*Next: [02 — System Requirements Specification](../02-Requirements-Specification/system-requirements-specification.md)*
