# 02.1.2 — System Requirements Specification

> **Section 02: Pacemaker System Architecture**
> **Subsection 01: System-Level Design — Requirements Specification**

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [Applicable Standards and Regulations](#2-applicable-standards-and-regulations)
3. [Functional Requirements](#3-functional-requirements)
4. [Performance Requirements](#4-performance-requirements)
5. [Electrical Requirements](#5-electrical-requirements)
6. [Mechanical Requirements](#6-mechanical-requirements)
7. [Environmental Requirements](#7-environmental-requirements)
8. [Safety Requirements](#8-safety-requirements)
9. [Biocompatibility Requirements](#9-biocompatibility-requirements)
10. [Telemetry Requirements](#10-telemetry-requirements)
11. [Software Requirements](#11-software-requirements)
12. [Reliability Requirements](#12-reliability-requirements)
13. [Electromagnetic Compatibility Requirements](#13-electromagnetic-compatibility-requirements)
14. [Traceability Matrix](#14-traceability-matrix)
15. [Requirements Verification](#15-requirements-verification)
16. [Summary](#16-summary)
17. [References](#17-references)

---

## 1. Introduction

This document defines the complete set of system-level requirements for an
implantable cardiac pacemaker. Requirements are derived from:

- International standards (ISO, IEC)
- Regulatory body guidance (FDA, CE/Medical Device Regulation)
- Clinical needs and physician input
- Patient safety considerations
- Engineering constraints

### 1.1 Requirement Classification

Requirements are classified using the following scheme:

```
┌─────────────────────────────────────────────────────────────────┐
│              REQUIREMENT CLASSIFICATION SCHEMA                   │
│                                                                  │
│  ┌──────────┐                                                   │
│  │  Class A  │  Mandatory — Must be met; no exceptions           │
│  │  (Critical)│  Failure = patient safety risk                  │
│  └──────────┘                                                   │
│  ┌──────────┐                                                   │
│  │  Class B  │  Important — Must be met with documented          │
│  │ (Essential)│  rationale for any deviation                    │
│  └──────────┘                                                   │
│  ┌──────────┐                                                   │
│  │  Class C  │  Desirable — Should be met when feasible;        │
│  │(Preferred)│  trade-off analysis acceptable                   │
│  └──────────┘                                                   │
│                                                                  │
│  Priority: A > B > C                                            │
│  Traceability: Every requirement must trace to a source         │
│  (Standard, Clinical Need, or Design Decision)                  │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 1.2 Requirement ID Convention

```
REQ-[Section]-[Subsection]-[Sequential Number]

Example: REQ-SEN-001 = Sensing subsystem, first requirement
         REQ-POW-015 = Power subsystem, 15th requirement
         REQ-SAF-003 = Safety subsystem, 3rd requirement
```

---

## 2. Applicable Standards and Regulations

| Standard ID        | Title                                              | Relevance          |
|--------------------|----------------------------------------------------|--------------------|
| ISO 14708-1:2014   | Active implantable medical devices — General        | Core design        |
| ISO 14708-3:2017   | Implantable cardiac pacemakers                      | Pacemaker-specific |
| ISO 10993-1:2018   | Biological evaluation of medical devices            | Biocompatibility   |
| ISO 10993-5:2009   | Tests for in vitro cytotoxicity                     | Material safety    |
| ISO 10993-10:2021  | Tests for skin sensitization and irritation         | Material safety    |
| IEC 60601-1:2005   | Medical electrical equipment — General safety       | Electrical safety  |
| IEC 60601-1-2:2014 | EMC requirements                                    | EMC compliance     |
| IEC 60601-1-6:2010 | Usability                                            | Human factors      |
| IEC 62304:2015     | Medical device software lifecycle                   | Software safety    |
| IEC 62366-1:2015   | Usability engineering                               | Human factors      |
| ANSI/AAMI NASPE-12 | Pacemaker terminology                               | Nomenclature       |
| FDA 21 CFR 820     | Quality system regulation                           | Manufacturing     |
| EU MDR 2017/745    | Medical Device Regulation (EU)                      | EU compliance      |
| ASTM F2182-19      | RF heating of implants                              | MRI safety         |
| ISO 11137:2006     | Sterilization of health care products               | Sterility          |
| Telcordia GR-468   | Reliability qualification for electronic components | Reliability       |

---

## 3. Functional Requirements

### 3.1 Pacing Modes

| Req ID         | Class | Requirement                                                                 |
|----------------|-------|-----------------------------------------------------------------------------|
| REQ-FUN-001    | A     | The device shall support a minimum of six pacing modes: VVI, VVI-R, AAI,  |
|                |       | AAI-R, DDD, DDD-R                                                          |
| REQ-FUN-002    | A     | The device shall support mode switching from DDD-R to VVI or VVIR when    |
|                |       | atrial fibrillation is detected (automatic mode switch)                    |
| REQ-FUN-003    | A     | The device shall allow non-destructive mode changes via telemetry          |
| REQ-FUN-004    | B     | The device shall support single-chamber (VVI, AAI) and dual-chamber (DDD)  |
|                |       | configurations                                                              |
| REQ-FUN-005    | B     | The device shall support CRT (cardiac resynchronization therapy) in a       |
|                |       | biventricular configuration (DDD-VB)                                       |
| REQ-FUN-006    | C     | The device shall support rate-adaptive pacing (suffix -R) using an         |
|                |       | accelerometer or minute-ventilation sensor                                 |

### 3.2 Sensing Functions

| Req ID         | Class | Requirement                                                                 |
|----------------|-------|-----------------------------------------------------------------------------|
| REQ-FUN-010    | A     | The device shall sense intrinsic P-waves (atrial) and R-waves (ventricle)  |
|                |       | independently                                                              |
| REQ-FUN-011    | A     | The device shall support programmable sensitivity threshold for each        |
|                |       | sensing channel                                                           |
| REQ-FUN-012    | A     | The device shall support both unipolar and bipolar sensing configurations  |
| REQ-FUN-013    | B     | The device shall support auto-sensitivity adjustment with a minimum of     |
|                |       | 8 programmable levels                                                      |
| REQ-FUN-014    | B     | The device shall provide oversensing rejection through blanking and        |
|                |       | refractory period management                                               |
| REQ-FUN-015    | A     | The device shall not interpret T-waves as R-waves when blanking is        |
|                |       | properly configured                                                        |
| REQ-FUN-016    | B     | The device shall detect lead noise (lead fracture) and inhibit pacing      |
|                |       | or switch to asynchronous mode                                              |

### 3.3 Pacing Functions

| Req ID         | Class | Requirement                                                                 |
|----------------|-------|-----------------------------------------------------------------------------|
| REQ-FUN-020    | A     | The device shall deliver pacing pulses with programmable amplitude and      |
|                |       | pulse width                                                                |
| REQ-FUN-021    | A     | The device shall support both unipolar and bipolar pacing configurations   |
| REQ-FUN-022    | A     | The device shall provide automatic output safety (capture confirmation)    |
| REQ-FUN-023    | B     | The device shall support automatic threshold search and output adjustment  |
| REQ-FUN-024    | A     | The device shall deliver pacing pulses with amplitude accuracy of          |
|                |       | ±10% and pulse width accuracy of ±5%                                       |
| REQ-FUN-025    | B     | The device shall support multichannel (up to 3) simultaneous pacing       |
| REQ-FUN-026    | B     | The device shall support a post-pulse safety shunt for passive charge     |
|                |       | dissipation within 50 ms                                                   |
| REQ-FUN-027    | A     | The device shall cease pacing output immediately upon detection of         |
|                |       | intrinsic activity during the escape interval                              |

### 3.4 Timing Functions

| Req ID         | Class | Requirement                                                                 |
|----------------|-------|-----------------------------------------------------------------------------|
| REQ-FUN-030    | A     | The device shall implement programmable lower rate interval (LRI)          |
| REQ-FUN-031    | A     | The device shall implement programmable upper tracking rate (UTR)          |
| REQ-FUN-032    | A     | The device shall implement programmable AV delay (sensed and paced)        |
| REQ-FUN-033    | A     | The device shall implement programmable post-ventricular atrial             |
|                |       | refractory period (PVARP)                                                  |
| REQ-FUN-034    | B     | The device shall implement programmable refractory periods for each         |
|                |       | chamber                                                                    |
| REQ-FUN-035    | B     | The device shall implement blanking periods synchronous with pacing        |
|                |       | output                                                                     |
| REQ-FUN-036    | A     | The device shall maintain timing accuracy of ±1% across all timer         |
|                |       | intervals                                                                  |

### 3.5 Rate Response

| Req ID         | Class | Requirement                                                                 |
|----------------|-------|-----------------------------------------------------------------------------|
| REQ-FUN-040    | C     | The device shall adjust pacing rate in response to detected physical       |
|                |       | activity (accelerometer-based)                                             |
| REQ-FUN-041    | C     | The device shall provide programmable rate-response parameters including    |
|                |       │ slope, threshold, and response time                                        |
| REQ-FUN-042    | C     | The rate-adaptive algorithm shall achieve target rate within 60 seconds    |
|                |       | of activity onset                                                          |
| REQ-FUN-043    | C     | The rate-adaptive algorithm shall return to lower rate within 5 minutes    |
|                |       | of activity cessation                                                      |

---

## 4. Performance Requirements

### 4.1 Timing Performance

| Req ID         | Class | Parameter                  | Value               | Unit |
|----------------|-------|----------------------------|----------------------|------|
| REQ-PER-001    | A     | LRI range                  | 300–2000            | ms   |
| REQ-PER-002    | A     | LRI resolution             | 10                   | ms   |
| REQ-PER-003    | A     | LRI accuracy               | ±1% (±5 ms max)     | —    |
| REQ-PER-004    | A     | AV delay range (paced)     | 30–350              | ms   |
| REQ-PER-005    | A     | AV delay range (sensed)    | 30–300              | ms   |
| REQ-PER-006    | A     | AV delay resolution        | 10                   | ms   |
| REQ-PER-007    | A     | AV delay accuracy          | ±5% (±5 ms max)     | —    |
| REQ-PER-008    | A     | Upper tracking rate        | 100–180             | bpm  |
| REQ-PER-009    | B     | Upper sensor rate          | 100–180             | bpm  |
| REQ-PER-010    | A     | PVARP range                | 150–500             | ms   |
| REQ-PER-011    | A     | Refractory period range    | 100–400             | ms   |
| REQ-PER-012    | A     | Blanking period range      | 100–600             | ms   |
| REQ-PER-013    | A     | Interspike interval jitter | < ±1                | ms   |

### 4.2 Sensing Performance

| Req ID         | Class | Parameter                  | Value               | Unit |
|----------------|-------|----------------------------|----------------------|------|
| REQ-PER-020    | A     | Sensing threshold range    | 0.125–5.0           | mV   |
| REQ-PER-021    | A     | Sensing threshold resolution| 0.125               | mV   |
| REQ-PER-022    | A     | Input-referred noise       | ≤ 1.5               | µVrms|
| REQ-PER-023    | A     | Input impedance            | ≥ 10                | kΩ   |
| REQ-PER-024    | A     | CMRR                       | ≥ 80                | dB   |
| REQ-PER-025    | A     | Sensing amplitude range    | 0.1–10.0            | mV   |
| REQ-PER-026    | B     | Sensing slew rate range    | 0.1–5.0             | V/s  |
| REQ-PER-027    | A     | Sensing detection latency  | ≤ 3                 | ms   |
| REQ-PER-028    | A     | Sensing polarity           | Uni/Bipolar select  | —    |
| REQ-PER-029    | B     | Auto-sensitivity range     | 0.25–4.0            | mV   |

### 4.3 Pacing Performance

| Req ID         | Class | Parameter                  | Value               | Unit |
|----------------|-------|----------------------------|----------------------|------|
| REQ-PER-030    | A     | Output voltage range       | 0.5–7.5             | V    |
| REQ-PER-031    | A     | Output voltage resolution  | ≤ 0.1               | V    |
| REQ-PER-032    | A     | Pulse width range          | 0.05–1.5            | ms   |
| REQ-PER-033    | A     | Pulse width resolution     | ≤ 0.1               | ms   |
| REQ-PER-034    | A     | Pulse amplitude accuracy   | ±10                 | %    |
| REQ-PER-035    | A     | Pulse width accuracy       | ±5                  | %    |
| REQ-PER-036    | A     | Maximum output current     | ≥ 100               | mA   |
| REQ-PER-037    | A     | Load impedance range       | 100–2000            | Ω    |
| REQ-PER-038    | B     | Safety shunt time constant | ≤ 50                | ms   |
| REQ-PER-039    | B     | Pacing output power        | ≤ 80                | µW   |

---

## 5. Electrical Requirements

### 5.1 Supply Requirements

| Req ID         | Class | Parameter                  | Value               | Unit |
|----------------|-------|----------------------------|----------------------|------|
| REQ-ELE-001    | A     | Battery voltage range      | 2.5–3.2             | V    |
| REQ-ELE-002    | A     | Digital supply (Vdd)       | 1.8 ± 0.1          | V    |
| REQ-ELE-003    | A     | Analog supply (Vdda)       | 1.8 ± 0.1          | V    |
| REQ-ELE-004    | A     | Reference voltage          | 1.024 ± 1%         | V    |
| REQ-ELE-005    | A     | Reference TC               | ≤ 50                | ppm/°C|
| REQ-ELE-006    | A     | HV supply range            | 0.5–7.5 (prog.)    | V    |
| REQ-ELE-007    | B     | LDO dropout voltage        | ≤ 200               | mV   |
| REQ-ELE-008    | A     | LDO PSRR (digital)        | ≥ 60                | dB   |
| REQ-ELE-009    | A     | LDO PSRR (analog)         | ≥ 80                | dB   |
| REQ-ELE-010    | B     | LDO line regulation        | ≤ 1% / V            | —    |
| REQ-ELE-011    | B     | LDO load regulation        | ≤ 2% / mA           | —    |

### 5.2 Current Consumption

| Req ID         | Class | Parameter                  | Value               | Unit |
|----------------|-------|----------------------------|----------------------|------|
| REQ-ELE-020    | A     | Quiescent current (all off)| ≤ 2.0               | µA   |
| REQ-ELE-021    | A     | Sensing mode current       | ≤ 8.0               | µA   |
| REQ-ELE-022    | A     | Pacing mode current        | ≤ 25                | µA   |
| REQ-ELE-023    | B     | Telemetry active current   | ≤ 30                | µA   |
| REQ-ELE-024    | B     | Charge pump efficiency     | ≥ 80                | %    |
| REQ-ELE-025    | A     | Total average current     | ≤ 15                | µA   |

### 5.3 ADC Requirements

| Req ID         | Class | Parameter                  | Value               | Unit |
|----------------|-------|----------------------------|----------------------|------|
| REQ-ELE-030    | B     | Resolution                 | ≥ 12                | bit  |
| REQ-ELE-031    | B     | INL                        | ≤ ±2                | LSB  |
| REQ-ELE-032    | B     | DNL                        | ≤ ±1                | LSB  |
| REQ-ELE-033    | B     | Sampling rate              | ≥ 256               | Sps  |
| REQ-ELE-034    | B     | SNR                        | ≥ 70                | dB   |
| REQ-ELE-035    | B     | Power consumption          | ≤ 5                 | µA   |

---

## 6. Mechanical Requirements

### 6.1 Package Dimensions

| Req ID         | Class | Parameter                  | Value               | Unit |
|----------------|-------|----------------------------|----------------------|------|
| REQ-MEC-001    | A     | Total device volume        | ≤ 30                | cm³  |
| REQ-MEC-002    | A     | Total device weight        | ≤ 40                | g    |
| REQ-MEC-003    | A     | Case material              | Titanium Grade 1/2  | —    |
| REQ-MEC-004    | A     | Case wall thickness        | 0.3–0.5             | mm   |
| REQ-MEC-005    | A     | Hermeticity                | ≤ 1 × 10⁻⁹         | atm·cc/s |
| REQ-MEC-006    | A     | Header material            | Ceramic or polymer  | —    |
| REQ-MEC-007    | A     | Lead connector             | IS-1 or DF-1 std   | —    |
| REQ-MEC-008    | B     | Connector insertion force  | 2–15                | N    |
| REQ-MEC-009    | B     | Connector retention force  | ≥ 10                | N    |
| REQ-MEC-010    | A     | Lead bore seal integrity   | Leak rate < 10⁻⁸    | atm·cc/s |

### 6.2 Vibration and Shock

| Req ID         | Class | Parameter                  | Value               | Unit |
|----------------|-------|----------------------------|----------------------|------|
| REQ-MEC-020    | A     | Random vibration           | 10–2000 Hz, 7.7g RMS | —   |
| REQ-MEC-021    | A     | Mechanical shock           | 1500g, 0.5 ms       | —    |
| REQ-MEC-022    | B     | Vibration duration         | 1 hour per axis     | —    |
| REQ-MEC-023    | B     | Post-vibration functional  | All parameters pass | —    |

---

## 7. Environmental Requirements

| Req ID         | Class | Parameter                  | Value               | Unit |
|----------------|-------|----------------------------|----------------------|------|
| REQ-ENV-001    | A     | Operating temperature      | 35–42               | °C   |
| REQ-ENV-002    | A     | Storage temperature        | -40 to +60          | °C   |
| REQ-ENV-003    | A     | Humidity (storage)         | 10–95% RH          | —    |
| REQ-ENV-004    | A     | Immersion depth            | Up to 2 m           | m    |
| REQ-ENV-005    | A     | Sterilization method       | Ethylene oxide (EtO) | —   |
| REQ-ENV-006    | A     | Sterility assurance level  | 10⁻⁶               | SAL  |
| REQ-ENV-007    | B     | Package shelf life         | ≥ 5 years           | years|
| REQ-ENV-008    | B     | Shelf storage conditions   | 15–30 °C, < 60% RH | —    |
| REQ-ENV-009    | B     | MRI conditional (1.5T)     | MR Conditional      | —    |
| REQ-ENV-010    | B     | MRI conditional (3.0T)     | MR Conditional      | —    |

---

## 8. Safety Requirements

### 8.1 Electrical Safety

| Req ID         | Class | Requirement                                                                 |
|----------------|-------|-----------------------------------------------------------------------------|
| REQ-SAF-001    | A     | The device shall limit maximum output current to 100 mA under all          |
|                |       │ conditions                                                                 |
| REQ-SAF-002    | A     | The device shall detect lead impedance < 100 Ω (short) and > 2000 Ω      |
|                |       │ (open) and generate an alert                                               |
| REQ-SAF-003    | A     | The device shall not deliver a pacing pulse with energy > 100 µJ           |
|                |       │ without capture verification                                               |
| REQ-SAF-004    | A     | The device shall limit leakage current to < 10 µA DC under normal         |
|                |       │ operating conditions                                                        |
| REQ-SAF-005    | A     | The device shall provide a passive safety shunt (≥ 1 kΩ) across pacing    |
|                |       │ output to dissipate stored energy within 50 ms of output disable           |

### 8.2 Hardware Safety

| Req ID         | Class | Requirement                                                                 |
|----------------|-------|-----------------------------------------------------------------------------|
| REQ-SAF-010    | A     | The device shall include a hardware watchdog timer with a timeout of        |
|                |       │ ≤ 2 seconds                                                                 |
| REQ-SAF-011    | A     | The device shall detect brownout (Vbat < 2.0 V) and enter safe mode        |
| REQ-SAF-012    | A     | The device shall implement hardware-enforced maximum pacing rate limit of   |
|                |       │ 180 bpm (hard limit)                                                        |
| REQ-SAF-013    | A     | The device shall include clock frequency monitoring with ±10% tolerance    |
| REQ-SAF-014    | B     | The device shall detect single-event upset (SEU) through CRC or parity     |
|                |       │ and recover within 100 ms                                                   |
| REQ-SAF-015    | A     | The device shall revert to asynchronous pacing (VOO/DOO at 80 bpm) on     |
|                |       │ any unrecoverable fault                                                      |

### 8.3 Fail-Safe Mode

| Req ID         | Class | Requirement                                                                 |
|----------------|-------|-----------------------------------------------------------------------------|
| REQ-SAF-020    | A     | The fail-safe mode shall operate with battery voltage as low as 2.0 V      |
| REQ-SAF-021    | A     | The fail-safe mode shall deliver pacing at ≥ 60 bpm                        |
| REQ-SAF-022    | A     | The fail-safe mode shall use non-critical parameters stored in NVM        |
| REQ-SAF-023    | A     | The fail-safe mode shall be entered within 500 ms of fault detection       |

---

## 9. Biocompatibility Requirements

| Req ID         | Class | Requirement                                                                 |
|----------------|-------|-----------------------------------------------------------------------------|
| REQ-BIO-001    | A     | All patient-contacting materials shall pass ISO 10993-1 biocompatibility   |
|                |       │ evaluation                                                                  |
| REQ-BIO-002    | A     | Titanium case material shall pass cytotoxicity test (ISO 10993-5)          |
| REQ-BIO-003    | A     | Header epoxy/silicone shall pass sensitization test (ISO 10993-10)         |
| REQ-BIO-004    | A     | Lead connector bore materials shall pass irritation test                    |
| REQ-BIO-005    | A     | All materials shall demonstrate chemical compatibility with body            |
|                |       │ fluids for ≥ 10 years                                                       |
| REQ-BIO-006    | B     | The device shall use no materials containing known carcinogens or           |
|                |       │ mutagens                                                                    |
| REQ-BIO-007    | B     | The device outer surface shall be passivated titanium oxide                |

---

## 10. Telemetry Requirements

### 10.1 RF Performance

| Req ID         | Class | Parameter                  | Value               | Unit |
|----------------|-------|----------------------------|----------------------|------|
| REQ-TEL-001    | A     | Carrier frequency          | 175–210             | kHz  |
| REQ-TEL-002    | A     | Modulation type            | FSK or ASK          | —    |
| REQ-TEL-003    | A     | Uplink data rate           | 8–256               | kbps |
| REQ-TEL-004    | A     | Downlink data rate         | 2–64                | kbps |
| REQ-TEL-005    | A     | Communication distance     | ≥ 5                 | cm   |
| REQ-TEL-006    | B     | Bit error rate             | ≤ 10⁻⁶             | —    |
| REQ-TEL-007    | A     | Encryption                 | AES-128 or stronger | —    |
| REQ-TEL-008    | A     | Authentication             | Mutual auth req'd   | —    |
| REQ-TEL-009    | B     | Packet CRC                 | CRC-16 minimum      | —    |
| REQ-TEL-010    | A     | Parameter write verify     | Read-back confirm   | —    |

### 10.2 Telemetry Data

| Req ID         | Class | Requirement                                                                 |
|----------------|-------|-----------------------------------------------------------------------------|
| REQ-TEL-020    | A     | The device shall transmit all current parameters on demand                  |
| REQ-TEL-021    | A     | The device shall transmit battery status (voltage, estimated remaining)     |
| REQ-TEL-022    | B     | The device shall store and transmit at least 50 episode recordings          |
| REQ-TEL-023    | B     | The device shall transmit real-time EGM data at ≥ 256 Sps                  |
| REQ-TEL-024    | B     | The device shall support remote monitoring data transmission               |
| REQ-TEL-025    | A     | All parameter writes shall require clinician authentication                |

---

## 11. Software Requirements

| Req ID         | Class | Requirement                                                                 |
|----------------|-------|-----------------------------------------------------------------------------|
| REQ-SW-001     | A     | Software shall be developed per IEC 62304 Class C (highest safety class)   |
| REQ-SW-002     | A     | All safety-critical software units shall have ≥ 100% MC/DC coverage        |
| REQ-SW-003     | A     | No dynamic memory allocation shall be used in safety-critical paths        |
| REQ-SW-004     | A     | All arithmetic operations shall include overflow checking                  |
| REQ-SW-005     | B     | Stack depth shall be statically analyzed and verified                      |
| REQ-SW-006     | A     | Software shall implement CRC-based program integrity verification         |
| REQ-SW-007     | B     | Firmware update capability (OTA) with signed image verification           |
| REQ-SW-008     | A     | All software shall be developed in MISRA-C compliant C or equivalent      |
| REQ-SW-009     | B     | Software unit testing shall achieve ≥ 95% branch coverage                 |
| REQ-SW-010     | A     | No use of recursion in safety-critical code                                |

---

## 12. Reliability Requirements

### 12.1 Lifetime and Failure Rates

| Req ID         | Class | Parameter                  | Value               | Unit |
|----------------|-------|----------------------------|----------------------|------|
| REQ-REL-001    | A     | Design lifetime            | ≥ 10                | years|
| REQ-REL-002    | A     | Battery capacity           | ≥ 1.0               | Ah   |
| REQ-REL-003    | A     | System failure rate (FIT)  | ≤ 10                | FIT  |
| REQ-REL-004    | A     | Confidence level           | 95                  | %    |
| REQ-REL-005    | A     | Mean time to failure       | ≥ 100,000           | hours|
| REQ-REL-006    | B     | Intrinsic failure rate     | ≤ 2                 | FIT  |

> **Note:** 1 FIT = 1 failure per 10⁹ device-hours

### 12.2 Reliability Calculations

The system failure rate is the sum of all component failure rates:

```
  λ_system = λ_battery + λ_asic + λ_passive + λ_lead + λ_header + λ_software

  Where:
    λ_battery  = Battery failure rate (typically 1–3 FIT)
    λ_asic     = ASIC/chip failure rate (typically 1–5 FIT)
    λ_passive  = Passive components failure rate (typically 1–2 FIT)
    λ_lead     = Lead failure rate (typically 2–5 FIT)
    λ_header   = Header/connector failure rate (typically 0.5–1 FIT)
    λ_software = Software latent fault rate (typically 0.5–2 FIT)

  Total: λ_system ≤ 10 FIT (target)
```

### 12.3 Accelerated Life Testing

| Req ID         | Class | Test                          | Conditions           |
|----------------|-------|-------------------------------|----------------------|
| REQ-REL-010    | A     | High-temperature operating    | 45°C, 10,000 hrs    |
| REQ-REL-011    | A     | Temperature cycling           | -40/+60°C, 500 cyc  |
| REQ-REL-012    | A     | Humidity aging                | 85°C/85%RH, 1000 hrs|
| REQ-REL-013    | A     | Mechanical shock              | 1500g, 3 axes        |
| REQ-REL-014    | B     | ESD immunity                  | ±8 kV contact, ±15 kV air |
| REQ-REL-015    | A     | Battery aging                 | 45°C, 5000 hrs      |

---

## 13. Electromagnetic Compatibility Requirements

### 13.1 Emission Limits

| Req ID         | Class | Parameter                  | Value               | Standard      |
|----------------|-------|----------------------------|----------------------|---------------|
| REQ-EMC-001    | A     | Conducted emissions        | Per CISPR 11, Group 1| IEC 60601-1-2|
| REQ-EMC-002    | A     | Radiated emissions         | Per CISPR 11, Group 1| IEC 60601-1-2|
| REQ-EMC-003    | A     | Harmonic emissions         | Per IEC 61000-3-2    | IEC 60601-1-2|

### 13.2 Immunity Limits

| Req ID         | Class | Test                        | Level              | Standard      |
|----------------|-------|-----------------------------|---------------------|---------------|
| REQ-EMC-010    | A     | ESD immunity (contact)      | ±8 kV              | IEC 61000-4-2 |
| REQ-EMC-011    | A     | ESD immunity (air)          | ±15 kV             | IEC 61000-4-2 |
| REQ-EMC-012    | A     | Radiated immunity           | 3 V/m, 80 MHz–2.7 GHz | IEC 61000-4-3 |
| REQ-EMC-013    | A     | Conducted immunity          | 3 Vrms, 150 kHz–80 MHz | IEC 61000-4-6 |
| REQ-EMC-014    | A     | EFT/burst                    | ±2 kV              | IEC 61000-4-4 |
| REQ-EMC-015    | A     | Surge immunity              | ±1 kV              | IEC 61000-4-5 |
| REQ-EMC-016    | A     | Power frequency magnetic    | 30 A/m             | IEC 61000-4-8 |
| REQ-EMC-017    | A     | Electrosurgery (ESU)        | 40 W, 500 kHz      | IEC 60601-1-2 |
| REQ-EMC-018    | A     | Defibrillation pulse        | 360 J / 50 Ω      | IEC 60601-1-2 |

### 13.3 EMI Response Behavior

| Req ID         | Class | EMI Condition               | Required Response   |
|----------------|-------|-----------------------------|---------------------|
| REQ-EMC-020    | A     | Electrosurgery detected     | Enter interference mode, no inappropriate pacing |
| REQ-EMC-021    | A     | Defibrillation pulse        | Post-shock reset, resume within 500 ms |
| REQ-EMC-022    | A     | External RF field detected  | Inhibit/async mode as configured |
| REQ-EMC-023    | A     | Magnetic switch (reed)      | Enter magnet mode (programmable response) |

---

## 14. Traceability Matrix

The following matrix maps each requirement category to its source(s):

```
┌──────────────────────┬────────────┬────────────┬───────────┬────────────┐
│ Requirement Category │ ISO 14708  │ IEC 60601  │ FDA 21CFR │ Clinical   │
├──────────────────────┼────────────┼────────────┼───────────┼────────────┤
│ Pacing Modes         │     X      │            │     X     │     X      │
│ Sensing Functions    │     X      │            │           │     X      │
│ Pacing Functions     │     X      │            │     X     │     X      │
│ Timing               │     X      │            │           │     X      │
│ Performance          │     X      │            │     X     │            │
│ Electrical Safety    │            │     X      │     X     │            │
│ Mechanical           │     X      │            │           │            │
│ Environmental        │     X      │            │     X     │            │
│ Biocompatibility     │     X      │            │     X     │            │
│ Telemetry            │     X      │     X      │     X     │     X      │
│ Software             │            │            │     X     │            │
│ Reliability          │     X      │            │     X     │            │
│ EMC                  │            │     X      │     X     │            │
│ Safety               │     X      │     X      │     X     │     X      │
└──────────────────────┴────────────┴────────────┴───────────┴────────────┘
```

---

## 15. Requirements Verification

### 15.1 Verification Methods

Each requirement shall be verified using one or more of the following methods:

| Method              | Symbol | Description                                      |
|---------------------|--------|--------------------------------------------------|
| Inspection          | INSP   | Visual or dimensional examination                |
| Analysis            | ANA    | Mathematical analysis or simulation              |
| Test                | TEST   | Physical measurement under defined conditions    |
| Design Review       | DR     | Formal review of design documentation            |
| Demonstration       | DEMO   | Operational demonstration of functionality       |
| Audit               | AUDIT  | Process or documentation audit                   |

### 15.2 Verification Matrix (Abbreviated)

| Req ID       | Method(s)            | Acceptance Criteria                                  |
|--------------|----------------------|------------------------------------------------------|
| REQ-FUN-001  | TEST, DEMO           | All 6 modes functional per IEC 60601-1-6             |
| REQ-PER-003  | TEST                 | LRI measured ±1% across temperature range            |
| REQ-ELE-025  | TEST                 | Total current ≤ 15 µA measured at Vbat = 2.8V       |
| REQ-MEC-001  | INSP, TEST           | Volume ≤ 30 cm³ (dimensional measurement)            |
| REQ-SAF-001  | TEST                 | Max output current ≤ 100 mA under all conditions     |
| REQ-REL-001  | ANLA, TEST (ALT)     | Projected lifetime ≥ 10 years at 95% confidence      |
| REQ-EMC-012  | TEST                 | No malfunction during 3 V/m immunity test            |
| REQ-BIO-001  | TEST (ISO 10993)     | Pass all biocompatibility endpoints                   |

---

## 16. Summary

This System Requirements Specification defines **127 total requirements**
across 13 categories:

```
┌──────────────────────────────────────────────────────┐
│           REQUIREMENTS SUMMARY BY CATEGORY           │
├─────────────────────────┬───────┬───────┬───────┬────┤
│ Category                │Class A│Class B│Class C│Tot │
├─────────────────────────┼───────┼───────┼───────┼────┤
│ Functional              │   8   │   5   │   4   │ 17 │
│ Performance (Timing)    │  10   │   2   │   0   │ 12 │
│ Performance (Sensing)   │   6   │   3   │   0   │  9 │
│ Performance (Pacing)    │   8   │   2   │   0   │ 10 │
│ Electrical              │  10   │   6   │   0   │ 16 │
│ Mechanical              │   6   │   4   │   0   │ 10 │
│ Environmental           │   6   │   4   │   0   │ 10 │
│ Safety                  │  12   │   1   │   0   │ 13 │
│ Biocompatibility        │   5   │   2   │   0   │  7 │
│ Telemetry               │   5   │   4   │   0   │  9 │
│ Software                │   6   │   4   │   0   │ 10 │
│ Reliability             │   5   │   1   │   0   │  6 │
│ EMC                     │  10   │   0   │   0   │ 10 │
├─────────────────────────┼───────┼───────┼───────┼────┤
│ TOTAL                   │  97   │  38   │   4   │139 │
└─────────────────────────┴───────┴───────┴───────┴────┘

  Class A (Mandatory):  70%
  Class B (Important):  27%
  Class C (Desirable):   3%
```

---

## 17. References

1. ISO 14708-1:2014 — Implants for surgery — Active implantable medical devices
2. ISO 14708-3:2017 — Implantable cardiac pacemakers
3. IEC 60601-1:2005 — Medical electrical equipment — General requirements for basic safety and essential performance
4. IEC 60601-1-2:2014 — EMC requirements and tests
5. IEC 62304:2015 — Medical device software lifecycle processes
6. ISO 10993-1:2018 — Biological evaluation of medical devices
7. FDA Guidance: Pacemaker Devices — Premarket Notification (510(k))
8. EU MDR 2017/745 — Medical Device Regulation
9. ANSI/AAMI NASPE-12 — Glossary of Terminology for Cardiac Pacemakers
10. MIL-HDBK-217F — Reliability Prediction of Electronic Equipment

---

*Previous: [01 — Block Diagram](../01-Block-Diagram/pacemaker-block-diagram.md)*
*Next: [03 — Functional Architecture](../03-Functional-Architecture/functional-architecture.md)*
