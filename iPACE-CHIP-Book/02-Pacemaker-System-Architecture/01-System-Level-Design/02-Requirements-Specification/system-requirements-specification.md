# System Requirements Specification

## 2.1.2 iPACE-CHIP Requirements Specification Document

### Document Control

| Field            | Value                                    |
|------------------|------------------------------------------|
| Document ID      | iPACE-CHIP-SRS-001                       |
| Revision         | 2.0                                      |
| Classification   | Design Input — ISO 13485 §7.3           |
| Safety Class     | Class III Medical Device (FDA) / AIMD (EU) |
| Applicable Standards | ISO 14708-1, IEC 60601-1-2, IEC 62304 |
| Risk Classification | Class III (FDA 21 CFR 870)            |

---

### 2.1.2.1 Functional Requirements

#### FR-SENSE: Cardiac Signal Sensing

| Req ID    | Requirement                                                                 | Priority | Verification |
|-----------|-----------------------------------------------------------------------------|----------|--------------|
| FR-SENSE-01 | The system shall detect intrinsic R-waves with amplitude ≥ 2.0 mV (2σ)  | Mandatory | Test         |
| FR-SENSE-02 | The system shall detect intrinsic P-waves with amplitude ≥ 0.5 mV (2σ)  | Mandatory | Test         |
| FR-SENSE-03 | The system shall provide programmable sensitivity from 0.25 mV to 5.0 mV | Mandatory | Test         |
| FR-SENSE-04 | The system shall sense on bipolar and unipolar configurations            | Mandatory | Test         |
| FR-SENSE-05 | The system shall reject T-waves exceeding 50% of R-wave amplitude       | Mandatory | Test         |
| FR-SENSE-06 | The system shall reject far-field signals (EMG, diaphragm) by >20 dB     | Mandatory | Test         |
| FR-SENSE-07 | The system shall achieve sensing signal-to-noise ratio (SNR) >10 dB      | Mandatory | Test         |
| FR-SENSE-08 | The system shall provide automatic sensitivity adjustment (AutoSense)     | Desirable | Test         |
| FR-SENSE-09 | The system shall detect oversensing within 2 sensing cycles              | Mandatory | Test         |
| FR-SENSE-10 | The system shall support 4 independent sensing channels (RA, RV, LV, Ext)| Mandatory | Test         |

#### FR-PACE: Pacing Pulse Generation

| Req ID    | Requirement                                                                 | Priority | Verification |
|-----------|-----------------------------------------------------------------------------|----------|--------------|
| FR-PACE-01 | The system shall generate pacing pulses with programmable amplitude       | Mandatory | Test         |
| FR-PACE-02 | Amplitude range: 0.5V to 10.0V in 0.1V steps (unipolar)                  | Mandatory | Test         |
| FR-PACE-03 | Amplitude range: 0.5V to 7.5V in 0.1V steps (bipolar)                   | Mandatory | Test         |
| FR-PACE-04 | The system shall generate pulses with programmable width: 0.05 ms–1.5 ms | Mandatory | Test         |
| FR-PACE-05 | Pulse width accuracy: ±5% or ±10 µs, whichever is greater               | Mandatory | Test         |
| FR-PACE-06 | The system shall perform automatic charge balancing within 4 µs post-pace | Mandatory | Test         |
| FR-PACE-07 | Post-pace polarization shall not exceed 500 mV at 500 Ω load            | Mandatory | Test         |
| FR-PACE-08 | Output capacitor shall be charged to within 1% of target before pacing    | Mandatory | Test         |
| FR-PACE-09 | The system shall support simultaneous multi-site pacing (biventricular)   | Desirable | Test         |
| FR-PACE-10 | The system shall pace in unipolar and bipolar configurations              | Mandatory | Test         |

#### FR-TIMER: Timing Cycles

| Req ID    | Requirement                                                                 | Priority | Verification |
|-----------|-----------------------------------------------------------------------------|----------|--------------|
| FR-TIMER-01 | The system shall implement lower rate interval (LRI): 300–1700 ms        | Mandatory | Test         |
| FR-TIMER-02 | The system shall implement upper rate limit (URL): 80–180 ppm            | Mandatory | Test         |
| FR-TIMER-03 | AV delay range: 30–350 ms (programmable)                                  | Mandatory | Test         |
| FR-TIMER-04 | VA interval range: 200–1500 ms (programmable)                            | Mandatory | Test         |
| FR-TIMER-05 | PVARP range: 150–500 ms (programmable)                                   | Mandatory | Test         |
| FR-TIMER-06 | Post-ventricular atrial blanking (PVAB): 50–400 ms                       | Mandatory | Test         |
| FR-TIMER-07 | Timer accuracy: ±2% or ±2 ms, whichever is greater                      | Mandatory | Test         |
| FR-TIMER-08 | The system shall support rate response (sensor-driven)                    | Desirable | Test         |
| FR-TIMER-09 | The system shall implement rate smoothing algorithm                       | Desirable | Test         |

#### FR-MODE: Operating Modes

| Req ID    | Requirement                                                                 | Priority | Verification |
|-----------|-----------------------------------------------------------------------------|----------|--------------|
| FR-MODE-01 | The system shall support VVI mode (ventricular demand pacing)             | Mandatory | Test         |
| FR-MODE-02 | The system shall support VVI/R mode (with rate response)                  | Mandatory | Test         |
| FR-MODE-03 | The system shall support AAI mode (atrial demand pacing)                  | Mandatory | Test         |
| FR-MODE-04 | The system shall support DDD mode (dual-chamber demand)                   | Mandatory | Test         |
| FR-MODE-05 | The system shall support DDDR mode (dual-chamber rate-responsive)         | Mandatory | Test         |
| FR-MODE-06 | The system shall support DDD/R mode (automatic mode switching)            | Mandatory | Test         |
| FR-MODE-07 | The system shall support ODO mode (monitoring only, no pacing)            | Desirable | Test         |
| FR-MODE-08 | Mode shall be programmable without requiring device explant               | Mandatory | Test         |
| FR-MODE-09 | The system shall transition between modes safely within 1 cardiac cycle   | Mandatory | Test         |

#### FR-TELEM: Telemetry and Programming

| Req ID    | Requirement                                                                 | Priority | Verification |
|-----------|-----------------------------------------------------------------------------|----------|--------------|
| FR-TELEM-01 | The system shall support RF telemetry via MICS band (402–405 MHz)        | Mandatory | Test         |
| FR-TELEM-02 | The system shall support magnet-activated interrogation mode              | Mandatory | Test         |
| FR-TELEM-03 | The system shall transmit real-time electrograms (EGM) via telemetry      | Mandatory | Test         |
| FR-TELEM-04 | The system shall support over-the-air (OTA) firmware update capability    | Desirable | Test         |
| FR-TELEM-05 | All telemetry packets shall include CRC-16 error detection                | Mandatory | Test         |
| FR-TELEM-06 | The system shall transmit stored diagnostic data (up to 512 events)       | Mandatory | Test         |
| FR-TELEM-07 | Telemetry data rate: 8–256 kbps (programmable)                           | Mandatory | Test         |
| FR-TELEM-08 | The system shall support bidirectional communication                      | Mandatory | Test         |

---

### 2.1.2.2 Performance Requirements

| Req ID    | Requirement                                                                 | Value      | Tolerance |
|-----------|-----------------------------------------------------------------------------|------------|-----------|
| PR-01     | Sensing input impedance (differential)                                     | >1 GΩ     | —         |
| PR-02     | Sensing input impedance (common-mode)                                      | >10 GΩ    | —         |
| PR-03     | LNA voltage noise density (at 10 Hz)                                       | <30 nV/√Hz | —        |
| PR-04     | LNA current noise density (at 10 Hz)                                       | <0.1 pA/√Hz| —        |
| PR-05     | CMRR (at 50/60 Hz)                                                         | >80 dB     | —         |
| PR-06     | Input-referred noise (0.5–100 Hz BW)                                       | <5 µVrms   | —         |
| PR-07     | ADC resolution                                                              | 12-bit     | ±1 LSB   |
| PR-08     | ADC sampling rate                                                           | 1024 Hz    | ±1%      |
| PR-09     | ADC INL/DNL                                                                | <±1 LSB   | —         |
| PR-10     | Output voltage accuracy                                                     | ±2%        | ±0.1V    |
| PR-11     | Output pulse width accuracy                                                 | ±5%        | ±10 µs   |
| PR-12     | Output DC resistance (during charge phase)                                 | <50 Ω     | —         |
| PR-13     | Charge balancing residual                                                   | <1 µC      | —         |
| PR-14     | Sensing-sensing crosstalk                                                   | <-60 dB    | —         |
| PR-15     | Output-sensing isolation                                                     | >100 dB    | —         |
| PR-16     | Telemetry range (through tissue)                                           | 2–5 cm     | —         |
| PR-17     | Telemetry bit error rate (BER)                                             | <10⁻⁶     | —         |
| PR-18     | Data storage capacity (EGM events)                                         | ≥512 events| —         |
| PR-19     | Parameter storage (EEPROM)                                                 | ≥4 KB      | —         |
| PR-20     | MCU instruction cycle time                                                  | 500 ns     | ±2%      |

---

### 2.1.2.3 Safety Requirements

| Req ID    | Requirement                                                                 | Standard  |
|-----------|-----------------------------------------------------------------------------|-----------|
| SF-01     | Maximum output voltage shall not exceed 10.0 V under any single fault    | ISO 14708 |
| SF-02     | Maximum output energy per pulse shall not exceed 100 µJ at 500 Ω        | ISO 14708 |
| SF-03     | The system shall include a watchdog timer with 8-second timeout           | IEC 60601 |
| SF-04     | The system shall reset to safe default parameters on power-on             | ISO 14708 |
| SF-05     | The system shall detect and indicate lead impedance out-of-range          | ISO 14708 |
| SF-06     | The system shall not deliver pacing pulses during sensing blanking period | IEC 60601 |
| SF-07     | The system shall detect battery end-of-life (EOL) at 2.5V               | ISO 14708 |
| SF-08     | The system shall enter hibernation mode on battery depletion             | ISO 14708 |
| SF-09     | No single fault condition shall result in patient harm                    | IEC 62304 |
| SF-10     | The system shall log all safety-related events with timestamps           | IEC 62304 |
| SF-11     | The system shall support emergency magnet reset                           | ISO 14708 |
| SF-12     | Tamper detection on parameter changes (checksum verification)            | IEC 62304 |
| SF-13     | The system shall prevent unintended mode transitions                      | IEC 62304 |
| SF-14     | The system shall detect oversensing and inhibit inappropriate pacing     | IEC 60601 |
| SF-15     | Maximum leakage current through leads: <10 µA DC                         | IEC 60601 |

---

### 2.1.2.4 Power Requirements

| Req ID    | Requirement                                                                 | Value      |
|-----------|-----------------------------------------------------------------------------|------------|
| PW-01     | Battery chemistry                                                           | Li-SVO     |
| PW-02     | Nominal battery voltage                                                     | 3.0 V      |
| PW-03     | Battery capacity                                                            | ≥1.0 Ah    |
| PW-04     | Battery self-discharge rate                                                 | <1%/year   |
| PW-05     | Total system current drain (nominal pacing)                                | <20 µA avg |
| PW-06     | Total system current drain (sleep mode)                                    | <2 µA      |
| PW-07     | Total system current drain (hibernate)                                     | <0.5 µA    |
| PW-08     | DC-DC converter efficiency (at 10 µA load)                                 | >80%       |
| PW-09     | LDO dropout voltage                                                        | <200 mV    |
| PW-10     | LDO output noise                                                           | <10 mVpp   |
| PW-11     | Power-on reset (POR) threshold                                             | 2.4 V      |
| PW-12     | Brown-out reset (BOR) threshold                                             | 2.6 V      |
| PW-13     | BOR hysteresis                                                              | 100 mV     |
| PW-14     | Power-on reset delay                                                       | 1–5 ms     |
| PW-15     | Target implant lifetime                                                     | ≥10 years  |
| PW-16     | Battery end-of-life indicator voltage                                       | 2.5 V      |
| PW-17     | Charge pump efficiency (if used)                                            | >70%       |

---

### 2.1.2.5 Area and Physical Requirements

| Req ID    | Requirement                                                                 | Value      |
|-----------|-----------------------------------------------------------------------------|------------|
| AR-01     | Die area (active)                                                           | ≤30 mm²   |
| AR-02     | Package dimensions                                                          | 38×42×6 mm |
| AR-03     | Package weight                                                              | ≤25 g      |
| AR-04     | Number of hermetic feedthrough pins                                         | ≤12        |
| AR-05     | Feedthrough material                                                        | Pt/Ir (90/10)|
| AR-06     | Feedthrough seal type                                                       | Ceramic-metal |
| AR-07     | Hermeticity (He leak rate)                                                  | <1×10⁻⁹ atm·cc/s |
| AR-08     | Lead connector type                                                         | IS-1 / DF-4 |
| AR-09     | Maximum lead pin diameter                                                   | 1.27 mm    |
| AR-10     | Case material                                                               | Ti Grade 1 |
| AR-11     | Case wall thickness                                                         | 0.3–0.5 mm |
| AR-12     | Telemetry coil diameter                                                     | 20–30 mm   |
| AR-13     | Accelerometer placement                                                     | Center of die |

---

### 2.1.2.6 Timing Requirements

| Req ID    | Requirement                                                                 | Value      |
|-----------|-----------------------------------------------------------------------------|------------|
| TR-01     | System wake-up time from hibernate                                          | <50 ms     |
| TR-02     | System wake-up time from sleep                                              | <5 ms      |
| TR-03     | Sensing-to-pacing response time (escape interval)                          | <5 ms      |
| TR-04     | Telemetry TX start-up time                                                  | <10 ms     |
| TR-05     | Telemetry RX start-up time                                                  | <20 ms     |
| TR-06     | ADC conversion time                                                          | <100 µs    |
| TR-07     | DAC settling time                                                            | <50 µs     |
| TR-08     | Charge balance completion time                                               | <4 µs      |
| TR-09     | Parameter write time (EEPROM)                                               | <5 ms      |
| TR-10     | Watchdog timeout period                                                      | 8.0 ± 0.5 s|
| TR-11     | Timer resolution (pacing)                                                    | 1 µs       |
| TR-12     | Timer resolution (diagnostic)                                                | 1 ms       |
| TR-13     | Maximum sensing-to-detection latency                                        | <100 ms    |
| TR-14     | Maximum mode switching latency                                               | <1 cycle   |
| TR-15     | Magnet reed switch debounce time                                            | 5–20 ms    |

---

### 2.1.2.7 Environmental Requirements

| Req ID    | Requirement                                                                 | Standard  |
|-----------|-----------------------------------------------------------------------------|-----------|
| ENV-01    | Operating temperature range (implanted)                                     | 35–41°C   |
| ENV-02    | Storage temperature range                                                    | -40–+60°C |
| ENV-03    | Operating humidity                                                           | 100% (body fluid) |
| ENV-04    | Vibration resistance                                                         | 10–500 Hz  |
| ENV-05    | Shock resistance                                                             | 1000 G     |
| ENV-06    | Electromagnetic compatibility (EMC)                                         | IEC 60601-1-2 |
| ENV-07    | Electrostatic discharge (ESD) immunity                                      | 8 kV HBM  |
| ENV-08    | RF field immunity (400 MHz–3 GHz)                                           | 200 V/m    |
| ENV-09    | Magnetic field immunity (MRI conditional)                                   | 1.5 T      |
| ENV-10    | Radiation tolerance (total ionizing dose)                                   | 100 krad   |
| ENV-11    | Single-event upset (SEU) rate                                               | <10⁻⁹/bit/day |
| ENV-12    | Corrosion resistance (body fluid immersion)                                 | >10 years  |
| ENV-13    | Biocompatibility (cytotoxicity)                                             | ISO 10993-5 |
| ENV-14    | Biocompatibility (sensitization)                                            | ISO 10993-10 |
| ENV-15    | Biocompatibility (implantation)                                              | ISO 10993-6 |

---

### 2.1.2.8 Biocompatibility Requirements

| Req ID    | Requirement                                                                 | Standard  |
|-----------|-----------------------------------------------------------------------------|-----------|
| BIO-01    | Case material shall be biocompatible per ISO 10993                          | ISO 10993 |
| BIO-02    | Lead connector shall be biocompatible per ISO 10993                         | ISO 10993 |
| BIO-03    | All external surfaces shall be passivated (TiO₂ or Pt coating)             | ISO 10993 |
| BIO-04    | No cytotoxic leachables from packaging materials                            | ISO 10993-5 |
| BIO-05    | No sensitization from implant materials                                     | ISO 10993-10 |
| BIO-06    | Material shall resist body fluid corrosion for >15 years                    | ASTM F2129 |
| BIO-07    | Titanium case shall be Grade 1 or Grade 2 CP Ti                            | ASTM F67   |
| BIO-08    | Feedthrough pins shall be Pt/Ir 90/10 alloy                                | ASTM F560  |
| BIO-09    | Solder/interconnect materials shall be Pb-free and RoHS compliant           | IEC 62321  |
| BIO-10    | Sterilization: Etylene Oxide (EtO) or gamma radiation                       | ISO 11135/11137 |

---

### 2.1.2.9 Reliability Requirements

| Req ID    | Requirement                                                                 | Value      |
|-----------|-----------------------------------------------------------------------------|------------|
| REL-01    | Mean time between failures (MTBF)                                           | >100 years |
| REL-02    | Failure rate (critical function)                                            | <10 FIT    |
| REL-03    | Failure rate (non-critical function)                                        | <100 FIT   |
| REL-04    | Random hardware failure rate (life-critical)                                | <10⁻⁸/hour |
| REL-05    | Software failure rate                                                       | <10⁻⁷/hour |
| REL-06    | Battery calendar life (at 37°C, nominal load)                              | >10 years  |
| REL-07    | EEPROM endurance (write cycles)                                             | >10⁶ cycles|
| REL-08    | Flash endurance (write cycles)                                               | >10⁵ cycles|
| REL-09    | Lead fracture rate (per year)                                               | <0.5%      |
| REL-10    | Lead insulation breach rate (per year)                                      | <0.1%      |
| REL-11    | Hermetic seal lifetime                                                       | >20 years  |
| REL-12    | Capacitor derating (for electrolytic)                                       | 50%        |
| REL-13    | Resistor derating                                                           | 50%        |
| REL-14    | Voltage derating (on-chip)                                                   | 80%        |
| REL-15    | Temperature derating (junction)                                              | <85°C      |

---

### 2.1.2.10 Requirements Traceability Matrix

```
┌─────────────────┬──────────┬──────────┬──────────┬──────────┬──────────┐
│ Requirement     │ System   │ Hardware │ Firmware │ Test     │ Risk     │
│ ID              │ Design   │ Design   │ Design   │ Protocol │ Analysis │
├─────────────────┼──────────┼──────────┼──────────┼──────────┼──────────┤
│ FR-SENSE-01     │ §2.1.1   │ §3.2     │ §4.1     │ §5.1     │ RA-001   │
│ FR-SENSE-02     │ §2.1.1   │ §3.2     │ §4.1     │ §5.1     │ RA-001   │
│ FR-SENSE-03     │ §2.1.1   │ §3.2     │ §4.1     │ §5.1     │ RA-002   │
│ FR-SENSE-04     │ §2.1.1   │ §3.2     │ §4.1     │ §5.1     │ RA-002   │
│ FR-SENSE-05     │ §2.1.1   │ §3.2     │ §4.1     │ §5.2     │ RA-003   │
│ FR-SENSE-06     │ §2.1.1   │ §3.2     │ §4.1     │ §5.2     │ RA-003   │
│ FR-SENSE-07     │ §2.1.1   │ §3.2     │ §4.1     │ §5.1     │ RA-002   │
│ FR-SENSE-08     │ §2.1.1   │ §3.2     │ §4.1     │ §5.3     │ RA-004   │
│ FR-SENSE-09     │ §2.1.1   │ §3.2     │ §4.1     │ §5.2     │ RA-005   │
│ FR-SENSE-10     │ §2.1.1   │ §3.1     │ §4.1     │ §5.1     │ RA-001   │
│                 │          │          │          │          │          │
│ FR-PACE-01      │ §2.1.1   │ §3.3     │ §4.2     │ §5.4     │ RA-006   │
│ FR-PACE-02      │ §2.1.1   │ §3.3     │ §4.2     │ §5.4     │ RA-006   │
│ FR-PACE-03      │ §2.1.1   │ §3.3     │ §4.2     │ §5.4     │ RA-006   │
│ FR-PACE-04      │ §2.1.1   │ §3.3     │ §4.2     │ §5.4     │ RA-007   │
│ FR-PACE-05      │ §2.1.1   │ §3.3     │ §4.2     │ §5.4     │ RA-007   │
│ FR-PACE-06      │ §2.1.1   │ §3.3     │ §4.2     │ §5.4     │ RA-008   │
│ FR-PACE-07      │ §2.1.1   │ §3.3     │ §4.2     │ §5.4     │ RA-008   │
│ FR-PACE-08      │ §2.1.1   │ §3.3     │ §4.2     │ §5.4     │ RA-006   │
│ FR-PACE-09      │ §2.1.1   │ §3.3     │ §4.2     │ §5.4     │ RA-009   │
│ FR-PACE-10      │ §2.1.1   │ §3.3     │ §4.2     │ §5.4     │ RA-006   │
│                 │          │          │          │          │          │
│ FR-TIMER-01     │ §2.1.1   │ §3.4     │ §4.3     │ §5.5     │ RA-010   │
│ FR-TIMER-02     │ §2.1.1   │ §3.4     │ §4.3     │ §5.5     │ RA-010   │
│ FR-TIMER-03     │ §2.1.1   │ §3.4     │ §4.3     │ §5.5     │ RA-011   │
│ FR-TIMER-04     │ §2.1.1   │ §3.4     │ §4.3     │ §5.5     │ RA-011   │
│ FR-TIMER-05     │ §2.1.1   │ §3.4     │ §4.3     │ §5.5     │ RA-012   │
│ FR-TIMER-06     │ §2.1.1   │ §3.4     │ §4.3     │ §5.5     │ RA-012   │
│ FR-TIMER-07     │ §2.1.1   │ §3.4     │ §4.3     │ §5.5     │ RA-010   │
│ FR-TIMER-08     │ §2.1.1   │ §3.4     │ §4.3     │ §5.6     │ RA-013   │
│ FR-TIMER-09     │ §2.1.1   │ §3.4     │ §4.3     │ §5.5     │ RA-010   │
│                 │          │          │          │          │          │
│ FR-MODE-01      │ §2.1.1   │ §3.1     │ §4.4     │ §5.7     │ RA-014   │
│ FR-MODE-02      │ §2.1.1   │ §3.1     │ §4.4     │ §5.7     │ RA-014   │
│ FR-MODE-03      │ §2.1.1   │ §3.1     │ §4.4     │ §5.7     │ RA-014   │
│ FR-MODE-04      │ §2.1.1   │ §3.1     │ §4.4     │ §5.7     │ RA-015   │
│ FR-MODE-05      │ §2.1.1   │ §3.1     │ §4.4     │ §5.7     │ RA-015   │
│ FR-MODE-06      │ §2.1.1   │ §3.1     │ §4.4     │ §5.7     │ RA-016   │
│ FR-MODE-07      │ §2.1.1   │ §3.1     │ §4.4     │ §5.7     │ RA-017   │
│ FR-MODE-08      │ §2.1.1   │ §3.1     │ §4.4     │ §5.7     │ RA-018   │
│ FR-MODE-09      │ §2.1.1   │ §3.1     │ §4.4     │ §5.7     │ RA-015   │
│                 │          │          │          │          │          │
│ FR-TELEM-01     │ §2.1.1   │ §3.5     │ §4.5     │ §5.8     │ RA-019   │
│ FR-TELEM-02     │ §2.1.1   │ §3.5     │ §4.5     │ §5.8     │ RA-020   │
│ FR-TELEM-03     │ §2.1.1   │ §3.5     │ §4.5     │ §5.8     │ RA-021   │
│ FR-TELEM-04     │ §2.1.1   │ §3.5     │ §4.5     │ §5.8     │ RA-022   │
│ FR-TELEM-05     │ §2.1.1   │ §3.5     │ §4.5     │ §5.8     │ RA-023   │
│ FR-TELEM-06     │ §2.1.1   │ §3.5     │ §4.5     │ §5.8     │ RA-021   │
│ FR-TELEM-07     │ §2.1.1   │ §3.5     │ §4.5     │ §5.8     │ RA-019   │
│ FR-TELEM-08     │ §2.1.1   │ §3.5     │ §4.5     │ §5.8     │ RA-019   │
│                 │          │          │          │          │          │
│ SF-01           │ §2.1.1   │ §3.3     │ §4.6     │ §5.9     │ RA-024   │
│ SF-02           │ §2.1.1   │ §3.3     │ §4.6     │ §5.9     │ RA-024   │
│ SF-03           │ §2.1.1   │ §3.4     │ §4.6     │ §5.9     │ RA-025   │
│ SF-04           │ §2.1.1   │ §3.1     │ §4.6     │ §5.9     │ RA-026   │
│ SF-05           │ §2.1.1   │ §3.2     │ §4.6     │ §5.9     │ RA-027   │
│ SF-06           │ §2.1.1   │ §3.3     │ §4.6     │ §5.9     │ RA-028   │
│ SF-07           │ §2.1.1   │ §3.6     │ §4.6     │ §5.9     │ RA-029   │
│ SF-08           │ §2.1.1   │ §3.6     │ §4.6     │ §5.9     │ RA-029   │
│ SF-09           │ §2.1.1   │ §3.1     │ §4.6     │ §5.9     │ RA-030   │
│ SF-10           │ §2.1.1   │ §3.4     │ §4.6     │ §5.9     │ RA-031   │
│ SF-11           │ §2.1.1   │ §3.5     │ §4.6     │ §5.9     │ RA-032   │
│ SF-12           │ §2.1.1   │ §3.4     │ §4.6     │ §5.9     │ RA-033   │
│ SF-13           │ §2.1.1   │ §3.1     │ §4.6     │ §5.9     │ RA-034   │
│ SF-14           │ §2.1.1   │ §3.2     │ §4.6     │ §5.9     │ RA-005   │
│ SF-15           │ §2.1.1   │ §3.3     │ §4.6     │ §5.9     │ RA-035   │
└─────────────────┴──────────┴──────────┴──────────┴──────────┴──────────┘
```

### 2.1.2.11 Requirements Allocation to Subsystems

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    REQUIREMENTS ALLOCATION DIAGRAM                          │
│                                                                             │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │                    SYSTEM-LEVEL REQUIREMENTS                          │   │
│  │  FR-SENSE (10)  FR-PACE (10)  FR-TIMER (9)  FR-MODE (9)           │   │
│  │  FR-TELEM (8)   SF-01..15     PR-01..20     PW-01..17              │   │
│  │  AR-01..13      TR-01..15     ENV-01..15    BIO-01..10             │   │
│  │  REL-01..15                                                          │   │
│  └────────────────────────────────────┬─────────────────────────────────┘   │
│                                       │                                    │
│              ┌────────────────────────┼────────────────────────┐            │
│              │                        │                        │            │
│              ▼                        ▼                        ▼            │
│  ┌───────────────────┐  ┌───────────────────┐  ┌───────────────────┐      │
│  │  AFE SUBSYSTEM     │  │  DIGITAL CTRL     │  │  POWER SUBSYSTEM  │      │
│  │                    │  │  SUBSYSTEM        │  │                    │      │
│  │  FR-SENSE: 10     │  │  FR-TIMER: 9     │  │  PW-01..17: 17    │      │
│  │  PR-01..09: 9     │  │  FR-MODE: 9      │  │  SF-07..08: 2     │      │
│  │  SF-05,14: 2      │  │  FR-SENSE(DSP): 3│  │  TR-01..02: 2     │      │
│  │  AR: area alloc   │  │  SF-03,10-13: 5  │  │  AR: area alloc   │      │
│  │  PW: <3µW/ch      │  │  PR-20: 1        │  │  PW: total budget │      │
│  │                    │  │  TR-11..15: 5    │  │                    │      │
│  │  Subtotal: ~21     │  │  AR: area alloc  │  │  Subtotal: ~21    │      │
│  └───────────────────┘  │                    │  └───────────────────┘      │
│                          │  Subtotal: ~31    │                              │
│  ┌───────────────────┐  └───────────────────┘  ┌───────────────────┐      │
│  │  OUTPUT STAGE     │  ┌───────────────────┐  │  TELEMETRY        │      │
│  │  SUBSYSTEM        │  │  SAFETY SUBSYSTEM │  │  SUBSYSTEM        │      │
│  │                    │  │                    │  │                    │      │
│  │  FR-PACE: 10     │  │  SF-01..15: 15    │  │  FR-TELEM: 8     │      │
│  │  PR-10..15: 6    │  │  REL-01..05: 5    │  │  PR-16..19: 4     │      │
│  │  SF-01,02,06: 3  │  │  ENV-06..11: 6    │  │  SF-11,12: 2      │      │
│  │  TR-07,08: 2     │  │  BIO: 10          │  │  TR-03..05: 3     │      │
│  │  AR: area alloc  │  │  REL: 15          │  │  AR: area alloc   │      │
│  │                    │  │                    │  │                    │      │
│  │  Subtotal: ~21    │  │  Subtotal: ~51    │  │  Subtotal: ~17    │      │
│  └───────────────────┘  └───────────────────┘  └───────────────────┘      │
│                                                                             │
│  TOTAL REQUIREMENTS: 137 (Functional: 47, Performance: 20, Safety: 15,    │
│                          Power: 17, Area: 13, Timing: 15, Environmental: 15│
│                          Biocompatibility: 10, Reliability: 15)            │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 2.1.2.12 Priority and Risk Classification

| Category        | Mandatory | Desirable | Total | Critical (Patient Safety) |
|-----------------|-----------|-----------|-------|---------------------------|
| Functional      | 38        | 9         | 47    | 22                        |
| Performance     | 20        | 0         | 20    | 8                         |
| Safety          | 15        | 0         | 15    | 15                        |
| Power           | 15        | 2         | 17    | 5                         |
| Area/Physical   | 11        | 2         | 13    | 2                         |
| Timing          | 13        | 2         | 15    | 8                         |
| Environmental   | 15        | 0         | 15    | 6                         |
| Biocompatibility| 10        | 0         | 10    | 10                        |
| Reliability     | 13        | 2         | 15    | 12                        |
| **Total**       | **150**   | **17**    | **167**| **88**                   |

### 2.1.2.13 Design Input Verification Checklist

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    DESIGN INPUT VERIFICATION CHECKLIST                       │
│                                                                             │
│  [ ] All functional requirements mapped to design specifications            │
│  [ ] All performance requirements have measurable acceptance criteria      │
│  [ ] All safety requirements traceable to hazard analysis                  │
│  [ ] All environmental requirements per applicable standards               │
│  [ ] All biocompatibility requirements per ISO 10993                       │
│  [ ] All reliability requirements per MIL-HDBK-217F/NPRD-2016             │
│  [ ] All requirements have defined verification method                     │
│  [ ] All requirements have defined acceptance criteria                     │
│  [ ] All requirements have defined responsible party                       │
│  [ ] Design input reviewed by multidisciplinary team                       │
│  [ ] Requirements are unambiguous and verifiable                           │
│  [ ] Requirements are free from contradictions                             │
│  [ ] Requirements are complete (no missing categories)                     │
│  [ ] Requirements reflect intended use and user needs                      │
│  [ ] Risk analysis performed for all safety requirements                   │
│  [ ] Design input formally approved per QMS                                │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

*Section 2.1.2 — System Requirements Specification*
*Previous: Section 2.1.1 — Block Diagram | Next: Section 2.1.3 — Functional Architecture*
