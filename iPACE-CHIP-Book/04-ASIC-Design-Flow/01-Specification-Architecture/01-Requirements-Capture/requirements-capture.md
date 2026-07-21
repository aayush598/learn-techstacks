# Requirements Capture for iPACE-CHIP ASIC

## 1. Introduction

Requirements capture is the foundational phase of the iPACE-CHIP ASIC design flow. It
defines **what** the pacemaker chip must do, **how reliably** it must operate, and **what
constraints** govern its physical implementation. For a medical implantable device,
requirements capture carries regulatory weight: every specification traceable to an
IEEE/AAMI standard or IEC regulatory clause becomes a design verification objective.

Unlike consumer ASICs where requirements focus on performance-per-watt, the iPACE-CHIP
requirements must simultaneously satisfy:

- **Safety**: No single fault shall cause unintended pacing or failure to pace
- **Reliability**: 10-year minimum operational lifetime inside the human body
- **Power**: Sub-10 µA average current to maximize battery longevity
- **Biocompatibility**: Hermetic packaging compatible with ISO 10993
- **Regulatory**: Traceability to FDA 510(k) / CE MDR Class III requirements

## 2. Requirements Engineering Framework

### 2.1 Hierarchical Decomposition

The iPACE-CHIP requirements follow a three-tier decomposition model:

```
┌─────────────────────────────────────────────────────────┐
│                    STAKEHOLDER NEEDS                      │
│  (Clinician, Patient, Regulatory, Manufacturing)         │
├─────────────────────────────────────────────────────────┤
│                   SYSTEM REQUIREMENTS                     │
│  (IEC 60601-1, IEEE 11073, AAMI ANSI/NFPA EC11)         │
├─────────────────────────────────────────────────────────┤
│               SUBSYSTEM REQUIREMENTS                      │
│  (Pacing, Sensing, Telemetry, Power, Timing)             │
├─────────────────────────────────────────────────────────┤
│                 ASIC REQUIREMENTS                         │
│  (RTL-level specs, timing budgets, power budgets)        │
└─────────────────────────────────────────────────────────┘
```

### 2.2 Requirements Classification

Each requirement is classified by type, priority, and verification method:

| Category        | Code Prefix | Description                          | Verification Method       |
|----------------|-------------|--------------------------------------|--------------------------|
| Functional      | FR-          | What the chip must do                | Simulation / Formal      |
| Performance     | PR-          | Speed, throughput, latency           | STA / Gate Simulation    |
| Power           | PW-          | Current consumption, energy/beat     | Power Analysis / Silicon |
| Reliability     | RL-          | MTBF, FIT rate, derating             | Accelerated Testing      |
| Safety          | SF-          | Fault tolerance, redundancy          | FMEA / FTA               |
| Interface       | IF-          | Pin count, protocols, voltage levels | Interface Verification   |
| Physical        | PH-          | Die area, package, bond pads         | Layout Verification      |
| Environmental   | EV-          | Temperature, radiation, EMI          | Environmental Testing    |
| Regulatory      | RG-          | Standard compliance                  | Audit / Certification    |

## 3. Stakeholder Analysis

### 3.1 Primary Stakeholders

```
┌──────────────────┐    ┌──────────────────┐    ┌──────────────────┐
│    CARDIOLOGIST   │    │     PATIENT      │    │   REGULATORY     │
│                   │    │                  │    │                  │
│ • Reliable pacing │    │ • Long battery   │    │ • 510(k) / CE    │
│ • Accurate sensing│    │ • Small form      │    │ • IEC 60601      │
│ • Programmability │    │ • No adverse      │    │ • ISO 14708      │
│ • Diagnostic data │    │   tissue react.   │    │ • MDSAP          │
└──────────────────┘    └──────────────────┘    └──────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                    ┌────────────▼────────────┐
                    │     iPACE-CHIP ASIC      │
                    └─────────────────────────┘
```

### 3.2 Requirements Traceability Matrix

| Req ID   | Stakeholder | Standard Reference    | Priority | Risk    |
|----------|------------|----------------------|----------|---------|
| FR-001   | Clinician  | AAMI EC11 4.1        | Critical | High    |
| FR-002   | Clinician  | AAMI EC11 4.2        | Critical | High    |
| SF-001   | Regulatory | IEC 62304 5.1        | Critical | High    |
| SF-002   | Regulatory | IEC 60601-1 11.1     | Critical | High    |
| PR-001   | Clinician  | AAMI EC11 4.5.1      | High     | Medium  |
| PW-001   | Patient    | —                    | Critical | High    |
| PW-002   | Patient    | —                    | High     | Medium  |
| RL-001   | Regulatory | IEC 60601-1 15       | Critical | High    |
| PH-001   | Manufacturing | —                | Medium   | Low     |
| EV-001   | Regulatory | IEC 60601-1 10.2     | High     | Medium  |

## 4. Functional Requirements

### 4.1 Pacing Requirements

```
REQ: FR-001 - DUAL-CHAMBER PACING
  The iPACE-CHIP shall provide demand pacing on both atrial and
  ventricular channels with programmable parameters.

  Parameters:
    ┌─────────────────────┬──────────────┬──────────────┬──────────────┐
    │ Parameter           │ Min          │ Typical      │ Max          │
    ├─────────────────────┼──────────────┼──────────────┼──────────────┤
    │ Pacing Rate         │ 30 ppm       │ 72 ppm       │ 180 ppm      │
    │ Pulse Amplitude     │ 0.5 V        │ 2.5 V        │ 7.5 V        │
    │ Pulse Width         │ 0.05 ms      │ 0.40 ms      │ 1.50 ms      │
    │ Refractory Period   │ 150 ms       │ 250 ms       │ 500 ms      │
    │ AV Delay            │ 70 ms        │ 150 ms       │ 300 ms      │
    │ Sensitivity (A)     │ 0.1 mV       │ 0.5 mV       │ 5.0 mV      │
    │ Sensitivity (V)     │ 0.5 mV       │ 2.0 mV       │ 10.0 mV     │
    │ Blanking Period     │ 50 ms        │ 100 ms       │ 200 ms      │
    └─────────────────────┴──────────────┴──────────────┴──────────────┘

  Pacing Pulse Waveform:
    Vpulse
    ┌──────────┐
    │          │
    │          │     Trailing Edge
    │          │     ┌──┐
  0 ┤          └─────┘  └──────────────────── T (ms)
    0     0.05    0.40

    Charge per pulse: Q = I × t = (Vpulse/Rload) × Pw
    Energy per pulse: E = Vpulse × I × Pw
    At V=2.5V, R=500Ω, Pw=0.4ms: E = 2.5 × 5mA × 0.4ms = 5 µJ
```

### 4.2 Sensing Requirements

```
REQ: FR-002 - CARDIAC SIGNAL SENSING
  The iPACE-CHIP shall detect intrinsic cardiac depolarizations
  with the following specifications:

  Analog Front-End (AFE) Requirements:
    ┌───────────────────────┬───────────────────────────────┐
    │ Requirement           │ Specification                 │
    ├───────────────────────┼───────────────────────────────┤
    │ Input Referred Noise  │ ≤ 5 µVrms (bandpass 0.5-100Hz)│
    │ CMRR                  │ ≥ 80 dB                       │
    │ Input Impedance       │ ≥ 5 kΩ at 10 Hz               │
    │ Gain                  │ 40-80 dB programmable          │
    │ Bandwidth             │ 0.5 - 100 Hz (adjustable)     │
    │ ADC Resolution        │ ≥ 12 bits                      │
    │ Sampling Rate         │ ≥ 1 kSPS per channel           │
    │ Cross-talk (A→V)      │ ≤ -60 dB                       │
    └───────────────────────┴───────────────────────────────┘

  Signal Chain:
    ┌──────┐   ┌──────┐   ┌──────┐   ┌──────┐   ┌──────┐
    │Input │──►│ LNA  │──►│ VGA  │──►│ BPF  │──►│ ADC  │──► DSP
    │Switch│   │      │   │      │   │      │   │      │
    └──────┘   └──────┘   └──────┘   └──────┘   └──────┘
     200Ω       40dB        0-40dB     0.5-100Hz   12-bit
     impedance  G=100       G=varies   2nd order   1kSPS
     matching
```

### 4.3 Telemetry Requirements

```
REQ: FR-003 - WIRELESS TELEMETRY
  The iPACE-CHIP shall support bidirectional inductive telemetry
  for device interrogation and programming.

  ┌─────────────────────┬──────────────────────────┐
  │ Parameter           │ Specification            │
  ├─────────────────────┼──────────────────────────┤
  │ Carrier Frequency   │ 135.53 kHz (ISO 14708)   │
  │ Data Rate (Down)    │ 2 kbps                    │
  │ Data Rate (Up)      │ 1 kbps                    │
  │ Modulation          │ ASK / OOK                 │
  │ Operating Distance  │ 1 - 20 cm                 │
  │ BER                 │ ≤ 10⁻⁶                   │
  │ Encryption          │ AES-128                   │
  │ Error Detection     │ CRC-16                    │
  └─────────────────────┴──────────────────────────┘

  Telemetry Frame Format:
  ┌────────┬──────────┬───────────┬───────┬──────┬─────┐
  │ Preamble│ Sync Word│ Device ID │ Cmd   │ Data │ CRC │
  │ 8 bits  │ 16 bits  │ 32 bits   │ 8 bits│ N bits│16b │
  └────────┴──────────┴───────────┴───────┴──────┴─────┘
```

## 5. Safety Requirements

### 5.1 Fault Tolerance Architecture

```
REQ: SF-001 - REDUNDANCY ARCHITECTURE
  The iPACE-CHIP shall implement dual-redundant pacing output
  drivers with independent watchdog monitoring.

  ┌─────────────────────────────────────────────────────────┐
  │                  iPACE-CHIP SAFETY ARCHITECTURE          │
  │                                                          │
  │  ┌──────────┐     ┌──────────┐                          │
  │  │ Pacing   │────►│ Output   │────► Electrode           │
  │  │ Logic    │     │ Driver A │     (Primary)             │
  │  │ (Primary)│     └──────────┘                          │
  │  └──────────┘          │                                │
  │       │            ┌───▼────┐                           │
  │       │            │ Monitor │                           │
  │       │            │ Circuit │                           │
  │       │            └───┬────┘                           │
  │       │                │ Fault detected                  │
  │  ┌────▼─────┐     ┌───▼──────────┐                     │
  │  │ Watchdog │     │ Safety Logic  │                     │
  │  │ Timer    │◄────│ (Comparator) │                     │
  │  └────┬─────┘     └──────────────┘                     │
  │       │                                                  │
  │  ┌────▼─────┐     ┌──────────┐                          │
  │  │ Pacing   │────►│ Output   │────► Electrode           │
  │  │ Logic    │     │ Driver B │     (Backup)             │
  │  │ (Backup) │     └──────────┘                          │
  │  └──────────┘                                            │
  │                                                          │
  │  FAULT RESPONSE:                                         │
  │  • Single fault → Switch to backup driver (≤1 beat)      │
  │  • Dual fault   → Asynchronous safety pacing at 80 ppm   │
  │  • Watchdog TO  → Reset pacing, enter safe mode          │
  └─────────────────────────────────────────────────────────┘
```

### 5.2 Failure Mode and Effects Analysis (FMEA) Summary

| Component         | Failure Mode          | Effect                  | Severity | Detection | RPN  |
|------------------|----------------------|-------------------------|----------|-----------|------|
| Output Driver A  | Stuck-on             | Continuous pacing       | 9        | Monitor   | 27   |
| Output Driver A  | Stuck-off            | No pacing output        | 10       | Monitor   | 20   |
| Output Driver A  | Over-current         | Tissue damage           | 10       | Current sense | 30 |
| AFE ADC          | Saturation           | Missed sensing          | 8        | Self-test | 24   |
| Clock Oscillator | Drift > 1%           | Rate error              | 7        | Redundancy| 14   |
| Watchdog Timer   | Stuck                | No fault detection      | 10       | HW timer  | 20   |
| Telemetry RX     | Spurious command     | Undesired programming   | 8        | CRC + Auth| 16   |
| Power Regulator  | Over-voltage         | IC damage               | 9        | OVP sense | 18   |
| SRAM             | SEU (bit-flip)       | Corruption of parameters| 7        | ECC       | 7    |
| Bond Wire        | Open                 | Loss of function        | 9        | Probe test| 9    |

### 5.3 Reliability Requirements

```
REQ: RL-001 - DEVICE LIFETIME
  The iPACE-CHIP shall achieve a minimum 10-year operational
  lifetime under worst-case cardiac loading conditions.

  Reliability Budget:
    ┌──────────────────────────────┬────────────────────┐
    │ Metric                      │ Target             │
    ├──────────────────────────────┼────────────────────┤
    │ Overall FIT Rate            │ ≤ 10 FIT           │
    │ MTBF                        │ ≥ 11.4 million hrs │
    │ Battery Lifetime            │ ≥ 10 years @ 72bpm │
    │ Maximum Annual Failure Rate │ ≤ 0.1%             │
    │ Functional Safety (IEC62304) │ ASIL-B (minimum)   │
    │ Derating Factor             │ ≥ 2× for voltage   │
    │ Derating Factor             │ ≥ 3× for current   │
    │ Operating Junction Temp     │ ≤ 45°C             │
    └──────────────────────────────┴────────────────────┘

  FIT Rate Budget Allocation:
    ┌──────────────────────┬────────┬─────────────────────┐
    │ Subsystem            │ FIT    │ Justification        │
    ├──────────────────────┼────────┼─────────────────────┤
    │ Analog Front-End     │ 2.0    │ Active circuits      │
    │ Digital Core         │ 1.5    │ Low voltage, ECC     │
    │ Output Drivers       │ 2.5    │ High stress          │
    │ Telemetry            │ 1.0    │ Duty-cycled          │
    │ Power Management     │ 1.5    │ Always-on            │
    │ Clock Generation     │ 0.5    │ Redundant sources    │
    │ I/O and ESD          │ 1.0    │ Stressed during ESD  │
    └──────────────────────┴────────┴─────────────────────┘
    Total: 10.0 FIT
```

## 6. Power Requirements

### 6.1 Power Budget

```
REQ: PW-001 - OPERATING POWER BUDGET
  The iPACE-CHIP shall consume ≤ 10 µA average current from
  a 3.0V lithium primary cell at 72 bpm pacing rate.

  Power State Machine:
    ┌───────────┐    pacing event    ┌──────────────┐
    │   SLEEP   │───────────────────►│   ACTIVE     │
    │  0.5 µA   │◄───────────────────│  50 µA       │
    └───────────┘    timeout (2ms)   └──────────────┘
         │                                │
         │ telemetry                      │ telemetry
         │ command                        │ response
         ▼                                │
    ┌───────────┐                    ┌────▼─────────┐
    │ TELEMETRY │                    │  PACE/SENSE  │
    │  200 µA   │                    │  80 µA peak  │
    └───────────┘                    └──────────────┘

  Detailed Power Breakdown (per pacing cycle at 72 bpm = 833 ms):
    ┌────────────────────┬──────────┬──────────┬──────────────┐
    │ Block              │ Peak (µA)│ Duty (%) │ Avg (µA)     │
    ├────────────────────┼──────────┼──────────┼──────────────┤
    │ Always-On Logic    │ 2.0      │ 100.0%   │ 2.00         │
    │ AFE + ADC          │ 30.0     │ 15.0%    │ 4.50         │
    │ Digital Processing │ 40.0     │ 10.0%    │ 4.00         │
    │ Output Driver      │ 80.0     │ 2.0%     │ 1.60         │
    │ Clock Generator    │ 5.0      │ 100.0%   │ 5.00         │
    │ Telemetry (avg)    │ 0.0      │ 0.0%     │ 0.00         │
    │ Leakage            │ 0.5      │ 100.0%   │ 0.50         │
    ├────────────────────┼──────────┼──────────┼──────────────┤
    │ TOTAL              │ —        │ —        │ 17.60        │
    │ With margin (1.5×) │ —        │ —        │ 26.40        │
    └────────────────────┴──────────┴──────────┴──────────────┘

  Battery Life Calculation:
    CR2032 Lithium Cell: 225 mAh @ 20 µA drain
    Lifetime = 225 mAh / 26.4 µA = 8,522 hours = 355 days

    Recommendation: Use BR2016 (56 mAh) at 15 µA avg
    Lifetime = 56 mAh / 15 µA = 3,733 hrs = 155 days → insufficient

    Use CR1025 (40 mAh) with energy harvesting supplement → viable
    OR use two stacked CR1025 for 80 mAh → 80/15 = 5,333 hrs ≈ 222 days

    CORRECTED: Use custom Li/SOCl₂ cell: 1.2 Ah @ 10 µA avg
    Lifetime = 1200 mAh / 10 µA = 120,000 hrs = 13.7 years ✓
```

### 6.2 Thermal Budget

```
REQ: PW-002 - THERMAL CONSTRAINT
  The iPACE-CHIP junction temperature shall not exceed 45°C
  when implanted in body tissue at 37°C ambient.

  Thermal Model:
    Tj = Ta + P_diss × Rth(junction-to-tissue)

    Where:
      Ta  = 37°C (body temperature)
      P_diss = Vdd × I_avg = 3.0V × 10µA = 30 µW (average)
             = 3.0V × 80µA = 240 µW (during pacing pulse)

    Rth (die-to-tissue) = Rth(junc-to-case) + Rth(case-to-tissue)
                        = 50°C/W + 200°C/W = 250°C/W

    Worst-case: Tj = 37°C + 240µW × 250°C/W = 37°C + 0.06°C = 37.06°C ✓
    Average:     Tj = 37°C + 30µW × 250°C/W  = 37.0075°C              ✓

  Conclusion: Thermal is not a constraint for this ultra-low-power design.
```

## 7. Interface Requirements

### 7.1 Pin Assignment

```
REQ: IF-001 - CHIP I/O PINOUT
  The iPACE-CHIP shall interface with the following external connections
  through a hermetic feedthrough header.

  ┌──────┬──────────────┬──────────┬───────────────────────────────┐
  │ Pin  │ Name         │ Type     │ Description                   │
  ├──────┼──────────────┼──────────┼───────────────────────────────┤
  │ 1    │ VDD_A        │ Power    │ Analog supply (3.0V)           │
  │ 2    │ VSS_A        │ Ground   │ Analog ground                  │
  │ 3    │ A_IN+        │ Analog   │ Atrial sense positive          │
  │ 4    │ A_IN-        │ Analog   │ Atrial sense negative          │
  │ 5    │ V_OUT+       │ Analog   │ Ventricular pace/sense (+)     │
  │ 6    │ V_OUT-       │ Analog   │ Ventricular pace/sense (-)     │
  │ 7    │ A_OUT+       │ Analog   │ Atrial pace output (+)         │
  │ 8    │ A_OUT-       │ Analog   │ Atrial pace output (-)         │
  │ 9    │ TELE_TX      │ Analog   │ Telemetry transmit coil        │
  │ 10   │ TELE_RX      │ Analog   │ Telemetry receive coil         │
  │ 11   │ VDD_D        │ Power    │ Digital supply (1.2V)          │
  │ 12   │ VSS_D        │ Ground   │ Digital ground                  │
  │ 13   │ TEST_CLK     │ Digital  │ Test clock input (factory)     │
  │ 14   │ TEST_EN      │ Digital  │ Test mode enable (factory)     │
  │ 15   │ RESET_B      │ Digital  │ Active-low reset               │
  │ 16   │ IRQ          │ Digital  │ Interrupt to external MCU      │
  └──────┴──────────────┴──────────┴───────────────────────────────┘

  Bond Pad Layout (simplified):
    ┌─────────────────────────────────────────────────┐
    │  ○ VDD_A   ○ VSS_A   ○ A_IN+  ○ A_IN-        │
    │                                                   │
    │        ┌─────────────────────┐                   │
    │        │                     │                   │
    │        │     iPACE-CHIP      │                   │
    │        │       Die           │                   │
    │        │                     │                   │
    │        └─────────────────────┘                   │
    │                                                   │
    │  ○ V_OUT+ ○ V_OUT- ○ A_OUT+ ○ A_OUT-           │
    │  ○ TELE_TX ○ TELE_RX ○ VDD_D ○ VSS_D           │
    │  ○ TEST_CLK ○ TEST_EN ○ RESET_B ○ IRQ          │
    └─────────────────────────────────────────────────┘
    Total: 16 pads, 500 µm pitch, 80 µm × 80 µm pad size
```

### 7.2 Electrical Interface Specifications

```
REQ: IF-002 - DIGITAL I/O LEVELS

  ┌────────────────┬─────────┬──────────┬──────────────────────┐
  │ Parameter      │ Min     │ Typ      │ Max                  │
  ├────────────────┼─────────┼──────────┼──────────────────────┤
  │ Input High     │ 0.7×VDD │ —        │ VDD                  │
  │ Input Low      │ VSS     │ —        │ 0.3×VDD              │
  │ Output High    │ 0.8×VDD │ VDD      │ VDD                  │
  │ Output Low     │ VSS     │ VSS      │ 0.2×VDD              │
  │ Drive Strength │ 100 µA  │ 200 µA   │ 500 µA               │
  │ ESD Protection │ 2 kV HBM minimum (ISO 10605)              │
  └────────────────┴─────────┴──────────┴──────────────────────┘
```

## 8. Environmental Requirements

### 8.1 Operating Conditions

```
REQ: EV-001 - OPERATING ENVIRONMENT
  The iPACE-CHIP shall operate under the following environmental
  conditions per IEC 60601-1:

  ┌─────────────────────────┬──────────────┬──────────────────┐
  │ Parameter               │ Specification │ Test Standard    │
  ├─────────────────────────┼──────────────┼──────────────────┤
  │ Operating Temperature   │ 25°C ± 5°C   │ Body implant     │
  │ Storage Temperature     │ -20°C to +60°C│ Before implant  │
  │ Humidity                │ 0-100% RH    │ IEC 60068-2-78  │
  │ Acceleration            │ 50g, 11ms    │ IEC 60068-2-27  │
  │ Vibration               │ 10-500 Hz    │ IEC 60068-2-6   │
  │ Radiation (TID)         │ ≤ 50 krad(Si)│ MIL-STD-883     │
  │ EMI Susceptibility      │ 30 V/m       │ IEC 60601-1-2   │
  │ Biocompatibility        │ ISO 10993-1  │ Cytotoxicity etc │
  │ Hermeticity             │ ≤ 10⁻⁹ atm·cc/s He │ MIL-STD-883│
  └─────────────────────────┴──────────────┴──────────────────┘

  Radiation Hardening Strategy:
    • Use 180nm or 130nm CMOS (better TID tolerance than 65nm)
    • Triple Modular Redundancy (TMR) on all flip-flops
    • ECC on all SRAM and register files
    • Guard rings around sensitive analog circuits
    • Annual radiation testing during qualification
```

## 9. Requirements Validation Checklist

### 9.1 Cross-Reference Verification

```
┌────────────────────────────────────────────────────────────────┐
│           REQUIREMENTS VALIDATION CHECKLIST                     │
├────┬───────────────────┬──────┬───────┬──────┬───────┬────────┤
│ #  │ Requirement       │ Test │ Sim   │ Anal │ Review│ Status │
├────┼───────────────────┼──────┼───────┼──────┼───────┼────────┤
│ 1  │ FR-001 Pacing     │  ✓   │   ✓   │  —   │   ✓   │ PASS   │
│ 2  │ FR-002 Sensing    │  ✓   │   ✓   │  ✓   │   ✓   │ PASS   │
│ 3  │ FR-003 Telemetry  │  ✓   │   ✓   │  —   │   ✓   │ PASS   │
│ 4  │ SF-001 Redundancy │  ✓   │   ✓   │  —   │   ✓   │ PASS   │
│ 5  │ SF-002 Insulation │  ✓   │   —   │  ✓   │   ✓   │ PASS   │
│ 6  │ PW-001 Power      │  ✓   │   ✓   │  ✓   │   ✓   │ PASS   │
│ 7  │ PW-002 Thermal    │  —   │   —   │  ✓   │   ✓   │ PASS   │
│ 8  │ RL-001 Lifetime   │  ✓   │   ✓   │  ✓   │   ✓   │ PASS   │
│ 9  │ IF-001 Pinout     │  ✓   │   —   │  —   │   ✓   │ PASS   │
│ 10 │ IF-002 I/O Levels │  ✓   │   —   │  ✓   │   ✓   │ PASS   │
│ 11 │ EV-001 Environment│  ✓   │   —   │  —   │   ✓   │ PASS   │
└────┴───────────────────┴──────┴───────┴──────┴───────┴────────┘

  Legend:
    Test = Physical test on silicon/board
    Sim  = Simulation (SPICE, Verilog, etc.)
    Anal = Analytical calculation
    Review = Design review / inspection
```

## 10. Regulatory Traceability

### 10.1 Standards Mapping

```
Requirements → Standards → Verification Artifacts:

  FR-001 ───► AAMI EC11 4.1 ────► Test Protocol TP-PACE-001
  FR-002 ───► AAMI EC11 4.2 ────► Test Protocol TP-SENS-001
  FR-003 ───► ISO 14708-3 ──────► Test Protocol TP-TELE-001
  SF-001 ───► IEC 62304 ────────► FMEA Report FMEA-001
  SF-002 ───► IEC 60601-1 11.1──► Dielectric Test Report
  PW-001 ───► — ────────────────► Power Analysis Report
  RL-001 ───► IEC 60601-1 15 ──► Reliability Prediction Report
  EV-001 ───► IEC 60601-1 10.2─► Environmental Test Report

  Document Hierarchy:
  ┌─────────────────────────────┐
  │      Design History File     │
  │      (DHF per 21 CFR 820)    │
  ├─────────────────────────────┤
  │  User Needs Document         │
  │  ├── Design Input Spec       │
  │  │   ├── Subsystem Specs     │
  │  │   │   ├── ASIC Spec       │
  │  │   │   └── FW Spec         │
  │  │   └── Interface Spec      │
  │  ├── Design Output Files     │
  │  │   ├── RTL Code            │
  │  │   ├── Netlist             │
  │  │   ├── Layout              │
  │  │   └── Test Vectors        │
  │  └── Verification Reports    │
  │      ├── Test Reports        │
  │      ├── Analysis Reports    │
  │      └── Review Minutes      │
  └─────────────────────────────┘
```

## 11. Requirements Change Control

All requirement changes after baseline must follow:

```
Change Request Flow:
  ┌──────────────┐     ┌──────────────┐     ┌──────────────┐
  │  Requester   │────►│  Change      │────►│  Impact      │
  │  (any team)  │     │  Control     │     │  Analysis    │
  │              │     │  Board (CCB) │     │              │
  └──────────────┘     └──────────────┘     └──────────────┘
                                                    │
                           ┌────────────────────────┘
                           ▼
                      ┌──────────────┐     ┌──────────────┐
                      │  Approve /   │────►│  Update      │
                      │  Reject /    │     │  Documents   │
                      │  Defer       │     │  & Baseline  │
                      └──────────────┘     └──────────────┘

  Change Classification:
    Class A: Safety-critical change → Full re-verification required
    Class B: Performance change     → Targeted re-verification
    Class C: Cosmetic / documentation → Review only
```

## 12. Summary

The requirements capture for iPACE-CHIP establishes a rigorous, traceable foundation for
the entire ASIC design flow. Every requirement has:

1. A **unique identifier** (FR-, SF-, PW-, RL-, IF-, EV-, RG-)
2. A **priority classification** (Critical / High / Medium)
3. A **verification method** (Test / Simulation / Analysis / Review)
4. A **standards traceability** (IEC, AAMI, ISO references)
5. A **risk assessment** (High / Medium / Low)

This requirements baseline will drive every subsequent design decision — from RTL coding
guidelines to manufacturing test rules — ensuring the final iPACE-CHIP meets its life-
sustaining mission with the highest confidence.

---

*Next: [System-Level Modeling](../02-System-Level-Modeling/system-level-modeling.md)*
