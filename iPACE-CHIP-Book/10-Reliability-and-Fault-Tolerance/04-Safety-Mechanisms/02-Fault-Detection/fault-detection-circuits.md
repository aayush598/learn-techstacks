# 10.4.2 Fault Detection Circuits for Implantable Pacemaker ICs

## Chapter Overview

Fault detection circuits are the sensory system of the iPACE-CHIP — they continuously monitor the health of every critical subsystem and provide the information needed to trigger appropriate safety responses. A fault detection circuit that fails to detect a dangerous fault leaves the patient unprotected, while a fault detection circuit that falsely reports a fault causes unnecessary alarm states and may disrupt pacing therapy. This chapter covers the complete fault detection architecture for the iPACE-CHIP, including the analog monitoring circuits, the digital self-test mechanisms, and the diagnostic coverage analysis that ensures every critical fault is detected within the required time.

---

## 10.4.2.1 Fault Detection Architecture

### Detection Strategy

The iPACE-CHIP's fault detection follows a hierarchical strategy:

```
Level 1: Continuous Monitoring (real-time)
  - Output voltage/current monitoring
  - Supply voltage monitoring
  - Clock frequency monitoring
  - Lead impedance monitoring
  
Level 2: Periodic Self-Test (every 10 ms to 1 second)
  - Memory ECC verification
  - DSP program counter monitoring
  - Timer accuracy verification
  - Sensing chain self-test
  
Level 3: Startup Test (at every power-on)
  - Full memory scan
  - All analog circuit characterization
  - Digital logic BIST
  - Calibration verification
  
Level 4: Periodic Deep Test (every 10 minutes)
  - Full system self-test
  - All watchdog BIST
  - Redundant path verification
```

### Diagnostic Coverage Requirements

The iPACE-CHIP must achieve the following diagnostic coverage for SIL 3 compliance:

```
Diagnostic Coverage (DC) = lambda_detected / lambda_total

For SIL 3:
  DC > 99% for high-dangerous failure modes
  DC > 90% for medium-dangerous failure modes
  DC > 60% for low-dangerous failure modes
  
The iPACE-CHIP targets DC > 99% for all Category A functions.
```

---

## 10.4.2.2 Analog Fault Detection

### Supply Voltage Monitoring

The iPACE-CHIP monitors its supply voltage with two independent comparators:

```
Primary Supply Monitor:
  VDD ──► Comparator (vs V_low = 1.65V) ──► Brown-out Flag
          Comparator (vs V_high = 2.1V)  ──► Overvoltage Flag

  If VDD < 1.65V: brown-out detected
    Action: disable pacing output, enter low-power monitoring mode
    
  If VDD > 2.1V: overvoltage detected
    Action: disable output stage, alert clinician

Secondary Supply Monitor (independent):
  VDD ──► Window Comparator (1.65V to 2.1V) ──► Status Flag
  
  This secondary monitor uses different reference voltages and a
  different comparator topology to prevent common-mode failures.
  
  Agreement check: Primary and secondary flags must agree.
  If they disagree: both monitors may be faulty, enter safe mode.
```

### Bandgap Reference Monitoring

The bandgap reference voltage is monitored by two independent methods:

```
Method 1: Direct Voltage Monitoring
  V_ref ──► Window Comparator (1.20V to 1.30V) ──► Status Flag

Method 2: Ratiometric Check
  V_ref ──► ADC ──► Digital comparison against expected value
  V_DD   ──► ADC
  
  Computed ratio: V_ref / V_DD should be approximately 0.42 (for 3.0V battery)
  If ratio deviates > 5%: bandgap may be drifting
  
  Both methods must agree. If they disagree: use the more conservative
  (lower) value for safety-critical decisions.
```

### Temperature Monitoring

The iPACE-CHIP includes an on-chip temperature sensor:

```
Temperature Sensor:
  On-chip temperature diode (forward voltage varies with temperature)
  ──► ADC ──► Temperature computation
  
  Normal range: 35C to 39C (body temperature)
  Warning: 34C or 40C (outside normal range)
  Critical: < 32C or > 42C (potentially dangerous)
  
  If temperature is outside normal range:
    1. Log the temperature reading
    2. If within warning range: continue operation, alert at next telemetry
    3. If in critical range: switch to fixed output parameters
       (temperature-dependent timing variations may affect pacing accuracy)
```

### Output Stage Monitoring

The output stage is the most safety-critical analog block. It is monitored by:

```
Output Voltage Monitor:
  V_out ──► Dual-path measurement:
    Path 1: Precision ADC (12-bit, 10 kHz sampling)
    Path 2: Analog window comparator (hardware, no ADC)
    
  Both paths measure the output voltage during and after each pacing pulse.
  
  Acceptance criteria:
    During pulse: V_out within 80%-120% of programmed value
    After pulse: V_out returns to 0V within 100 us (no sticking)
    
  If criteria not met:
    1. Log the anomalous reading
    2. If within 10% of limit: warning, increase monitoring
    3. If outside 20% of limit: terminate pulse, retry once
    4. If retry fails: disable output stage, enter safe mode

Output Current Monitor:
  I_out ──► Sense resistor + ADC
  
  Acceptance criteria:
    During pulse: I_out within 80%-120% of expected value
    (expected value computed from V_out and lead impedance)
    
  If criteria not met: same response as voltage monitor

Output Timing Monitor:
  Start of pulse ──► Hardware timer ──► End of pulse
  Measurement: actual pulse width vs. programmed pulse width
  
  Acceptance criteria:
    |measured - programmed| / programmed < 20%
    
  If criteria not met: terminate pulse, log event
```

### Sensing Amplifier Monitoring

The sensing amplifier is monitored through:

```
DC Offset Monitoring:
  Measure the DC offset of the sensing amplifier output
  (should be 0V for a properly functioning amplifier)
  
  If |offset| > 50 mV: amplifier may be degraded
    Action: increase sensing threshold, alert clinician

Noise Floor Monitoring:
  During the refractory period (when no cardiac signals are expected),
  measure the RMS noise on the sensing amplifier output.
  
  Normal noise floor: < 50 uV
  Warning: > 100 uV (increased noise may indicate amplifier problem)
  Critical: > 500 uV (excessive noise may cause oversensing)
  
  If noise floor is critical:
    Action: switch to backup amplifier, or increase threshold

Self-Test Pulse Injection:
  Hardware injects a small test pulse (100 uV) into the amplifier input
  every 100 ms. The digital output must detect this pulse.
  
  If test pulse is not detected for 3 consecutive attempts:
    Action: amplifier may have failed
    Response: switch to backup amplifier
```

---

## 10.4.2.3 Digital Fault Detection

### Memory ECC Monitoring

All ECC-protected memories are monitored through the ECC mechanism:

```
ECC Error Detection:
  On every memory read:
    1. Compute syndrome
    2. If syndrome = 0: no error
    3. If syndrome indicates correctable error: correct and scrub
    4. If syndrome indicates uncorrectable error: raise alarm
    
  ECC Error Counter:
    Correctable errors: 16-bit counter (logs frequency of single-bit errors)
    Uncorrectable errors: 8-bit counter (critical, triggers safety response)
    
  If correctable error rate exceeds threshold:
    Warning: increased scrubbing rate
    Critical: memory may be degrading, switch to backup memory
    
  If uncorrectable error detected:
    Critical: immediately switch to backup storage
    Log the error address for failure analysis
```

### DSP Health Monitoring

The DSP is monitored through multiple mechanisms:

```
Program Counter Monitoring:
  DSP_PC ──► Range checker ──► Valid range: 0x0000 to 0x7FFF (flash space)
  
  If PC outside valid range: firmware may be corrupted
    Action: reset DSP, reload firmware

Stack Pointer Monitoring:
  DSP_SP ──► Range checker ──► Valid range: 0x2000 to 0x2FFF (SRAM stack)
  
  If SP outside valid range: stack overflow/underflow may have occurred
    Action: reset DSP, reload firmware

Register Parity Monitoring:
  Critical DSP registers are protected by parity bits
  (odd parity, checked on every read)
  
  If parity error detected: register value may be corrupted
    Action: reload register from backup, or reset DSP

Watchdog Pet Verification:
  As described in Chapter 10.2.3, the DSP must pet the watchdog
  with a correct challenge-response pattern.
  
  If pet is incorrect or missing: DSP may be malfunctioning
    Action: watchdog timeout triggers recovery
```

### Clock Monitoring

```
Clock Frequency Monitor:
  System clock ──► Frequency counter ──► Compare against reference
  
  Acceptance: 32,768 Hz +/- 500 Hz (for 32.768 kHz crystal)
  
  If frequency outside acceptance:
    Warning: crystal may be drifting
    Critical: clock may have failed, switch to backup oscillator
    
Clock Duty Cycle Monitor:
  System clock ──► Duty cycle measurement ──► Compare against 50% +/- 10%
  
  If duty cycle outside acceptance: oscillator may be degraded

Glitch Detection:
  System clock ──► Edge detector ──► Pulse width measurement
  
  If any clock pulse is narrower than 10 ns: glitch detected
    Action: ignore the glitch (do not propagate to logic)
    Log the glitch event
```

### Logic Monitoring

```
Control Signal Monitoring:
  Critical control signals (output enable, reset, clock enable) are
  monitored by independent circuits:
  
  Signal ──► Redundant copy ──► Comparison
  
  If primary and redundant copies disagree: fault detected
    Action: use the safer value (typically the one that disables output)

FSM State Monitoring:
  The pacing controller FSM state register is monitored:
  
  State ──► Valid state decoder ──► Valid/Invalid flag
  
  If FSM enters an invalid state: fault detected
    Action: force FSM to IDLE state, restart pacing cycle

Timing Monitor:
  Critical timing paths are monitored by ring oscillators:
  
  Ring oscillator frequency ──► Compare against nominal
  
  If frequency deviates > 20%: timing may be failing
    Action: reduce clock frequency (to increase timing margin)
    or increase supply voltage (adaptive voltage scaling)
```

---

## 10.4.2.4 Interconnect Fault Detection

### Bus Integrity Monitoring

All internal buses carry ECC-protected data:

```
Data Bus Monitoring:
  Source ──► ECC encode ──► 40-bit bus ──► ECC decode ──► Destination
                                    │
                                    └── Error detection at destination
  
  If ECC error on bus data: data may be corrupted
    Action: request retransmission from source
    If 3 retransmissions fail: use last known-good value
```

### Wire Bond Monitoring

```
Wire bond integrity is inferred from:
  1. I/O pad voltage measurements (during test mode)
  2. Lead impedance measurements (during normal operation)
  
  If a wire bond opens:
    1. The affected I/O will not respond
    2. The I/O monitor will detect the lack of response
    3. The system will use a redundant I/O path (if available)
    4. If no redundant path: alert clinician
```

### Cross-Talk Detection

```
For high-sensitivity analog circuits (sensing amplifier):
  Signal integrity is verified by injecting a known test signal
  on adjacent lines and measuring the coupling:
  
  Test signal on adjacent line ──► Measure coupling into signal line
  
  If coupling > -40 dB: excessive cross-talk may affect sensing
    Action: adjust sensing filter, or increase spacing (if programmable)
```

---

## 10.4.2.5 Fault Detection Timing

### Detection Latency Requirements

Different faults require different detection speeds:

```
Fault Type                | Max Detection Latency | Rationale
--------------------------|----------------------|----------------------------------
Output voltage exceedance | 100 us               | Must terminate pulse before damage
Lead short circuit        | 1 ms                 | Must limit current
Clock failure             | 10 ms                | Must switch to backup clock
Memory corruption         | 100 ms               | Must load backup before use
DSP malfunction           | 100 ms               | Must reset before wrong action
Sensing failure           | 500 ms               | Must switch to asynchronous mode
Parameter drift           | 1 second             | Must correct before clinical impact
Battery depletion         | 1 hour               | Must alert clinician
```

### Detection Circuit Response Time

The analog monitoring circuits are designed for fast response:

```
Output voltage comparator:
  Propagation delay: 50 ns (from overvoltage to output tri-state)
  Total response time: 50 ns (comparator) + 100 ns (logic) = 150 ns
  
  This is much faster than the minimum pacing pulse width (0.1 ms = 100,000 ns),
  providing > 600x margin for terminating an unsafe pulse.

Lead impedance monitor:
  Measurement time: 100 us (test pulse duration)
  Processing time: 50 us (ADC conversion + comparison)
  Total: 150 us
  
  This is fast enough to detect a lead short during the pacing pulse
  (pulse width > 100 us).

Supply voltage monitor:
  Response time: 1 us (for brown-out detection)
  This triggers pacing output disable before the supply drops to
  a level that could cause erratic circuit behavior.
```

---

## 10.4.2.6 Diagnostic Coverage Analysis

### Fault Detection Coverage Table

The following table summarizes the diagnostic coverage for each critical block:

```
Block              | Fault Type      | Detection Method     | DC (%) | Response Time
-------------------|-----------------|---------------------|--------|-------------
Output stage       | Overvoltage     | HW comparator       | 99.9   | 150 ns
Output stage       | Overcurrent     | HW current sense    | 99.9   | 500 ns
Output stage       | No output       | Output monitoring   | 99.5   | 1 pulse
Bandgap reference  | Voltage drift   | Dual monitoring     | 99.0   | 10 ms
Sensing amplifier  | Gain failure    | Self-test pulse     | 99.0   | 100 ms
Sensing amplifier  | Offset drift    | DC offset monitor   | 95.0   | 10 ms
Clock oscillator   | Frequency drift | Freq counter        | 99.5   | 10 ms
Clock oscillator   | Complete failure | Missing edge det    | 99.9   | 1 ms
Memory (SRAM)      | Stuck-at fault  | ECC + scrub         | 99.9   | 10 ms
Memory (flash)     | Bit flip        | ECC + CRC           | 99.9   | 100 ms
DSP                | Hang            | Watchdog            | 99.9   | 100 ms
DSP                | Code corruption | PC monitoring       | 99.0   | 10 ms
Power supply       | Brown-out       | Voltage comparator  | 99.9   | 1 us
Lead system        | Open circuit    | Impedance monitor   | 99.0   | 150 us
Lead system        | Short circuit   | Impedance monitor   | 99.0   | 150 us
-------------------|-----------------|---------------------|--------|-------------

Average diagnostic coverage: 99.3%
```

### Safety Integrity Level Assessment

Using the IEC 61508 SIL assessment methodology:

```
Safe Failure Fraction (SFF) = (safe failures + detected dangerous failures) / total failures

For the iPACE-CHIP:
  Safe failures: 85% (failures that lead to no-pacing or safe-state)
  Detected dangerous failures: 14.3% (detected by monitoring)
  Undetected dangerous failures: 0.7%
  
  SFF = (85% + 14.3%) / 100% = 99.3%
  
  For SIL 3:
    SFF > 99%: Required DC for dangerous failures > 99%
    Achieved DC: 99.3% -> SIL 3 COMPLIANT
```

### Common Cause Failure Analysis

Common cause failures (CCFs) can bypass redundant detection mechanisms:

```
CCF Sources:
  1. Power supply failure (affects all circuits simultaneously)
  2. Clock failure (affects all digital circuits simultaneously)
  3. Temperature extreme (affects all circuits simultaneously)
  4. Manufacturing defect (may affect multiple circuits)
  
CCF Prevention:
  1. Redundant power supplies (two LDOs for critical blocks)
  2. Redundant clocks (two crystal oscillators)
  3. Temperature monitoring with safe response
  4. Extensive production testing and burn-in
  
CCF Detection:
  1. Cross-checking between redundant circuits
  2. Periodic self-test of all monitoring circuits
  3. External monitoring (telemetry reports to clinician)
```

---

## 10.4.2.7 Self-Test Implementation

### Built-In Self-Test (BIST) Architecture

The iPACE-CHIP's BIST is implemented as a dedicated hardware block:

```
BIST Controller:
  ┌─────────────────────────────────────────┐
  │  Test Pattern Generator                  │
  │  (LFSR-based, produces deterministic     │
  │   but comprehensive test patterns)       │
  └────────────┬────────────────────────────┘
               │
  ┌────────────┴────────────────────────────┐
  │  Test Mux (selects target block)         │
  │                                          │
  │  Target blocks:                          │
  │    - Memory arrays                       │
  │    - Digital logic blocks                │
  │    - Analog circuits (via ADC)           │
  │    - I/O interfaces                      │
  └────────────┬────────────────────────────┘
               │
  ┌────────────┴────────────────────────────┐
  │  Response Analyzer                       │
  │  (compares actual response against       │
  │   expected response from golden model)   │
  └────────────┬────────────────────────────┘
               │
  ┌────────────┴────────────────────────────┐
  │  BIST Result Register                    │
  │  (stores pass/fail for each block)       │
  └─────────────────────────────────────────┘
```

### BIST Execution Schedule

```
Startup BIST (at every power-on):
  Duration: 500 ms
  Tests: All blocks (comprehensive)
  
  During startup BIST:
    1. Pacing output is DISABLED (no pacing during test)
    2. Sensing input is DISABLED
    3. After BIST completes: normal operation resumes
    4. If BIST fails: device enters safe mode

Periodic BIST (during normal operation):
  Duration: 10 ms (non-intrusive)
  Tests: Critical blocks only
  
  During periodic BIST:
    1. Pacing output continues normally
    2. Sensing continues normally
    3. BIST runs in the background on non-critical blocks
    4. If BIST fails: the affected block is flagged
       (pacing continues on the non-tested blocks)
```

### Memory BIST

```
March-CW Algorithm (for SRAM):
  Duration: 0.5 ms per Kbit
  
  For 56 Kbit total SRAM: 28 ms total
  
  Coverage: > 99.9% of stuck-at faults, coupling faults, and
            transition faults in the memory array

Flash BIST:
  Duration: 5 seconds (reading all flash pages and checking CRC)
  
  Coverage: 100% of flash data integrity (CRC-32 verification)
```

### Analog BIST

```
Analog Block BIST:
  1. Sense amplifier: inject test pulse, verify detection
  2. Bandgap reference: measure voltage, compare against bounds
  3. ADC: measure known reference voltage, verify accuracy
  4. Output stage: apply test load, verify output voltage/current
  
  Duration: 5 ms
  Coverage: > 99% of parametric failures in analog blocks
```

---

## 10.4.2.8 Diagnostic Data Management

### Diagnostic Memory Layout

The iPACE-CHIP allocates 2 Kbyte of non-volatile memory for diagnostic data:

```
Diagnostic Memory Map:
  Offset  Size    Contents
  0x0000  256B    Error log (most recent 64 errors, 4 bytes each)
  0x0100  64B     Error counters (by type and block)
  0x0140  32B     Last measurement values (voltages, currents, impedances)
  0x0160  16B     Device status (degradation level, active faults)
  0x0170  16B     Timestamp (RTC value of last significant event)
  0x0180  128B    Calibration data (analog trim values)
  0x0200  512B    Trend data (hourly averages of key parameters)
  0x0400  1024B   Reserved for future use
```

### Error Log Format

Each error log entry contains:

```
Error Log Entry (4 bytes):
  Bits [7:0]:    Error type code
  Bits [15:8]:   Block ID (which block reported the error)
  Bits [23:16]:  Error count (how many times this error occurred)
  Bits [31:24]:  Flags (severity, recoverable, first occurrence)
```

### Telemetry Reporting

Diagnostic data is available through telemetry:

```
Telemetry Commands:
  CMD_READ_ERROR_LOG:    Returns the last 64 error log entries
  CMD_READ_ERROR_COUNTS: Returns all error counters
  CMD_READ_MEASUREMENTS: Returns latest measurement values
  CMD_READ_STATUS:       Returns current device status
  CMD_CLEAR_LOG:         Clears the error log (clinician only)
  CMD_RUN_BIST:          Triggers an immediate BIST (clinician only)
```

---

## 10.4.2.9 Fault Detection Limitations

### Undetectable Faults

Some faults cannot be detected by on-chip monitoring:

```
1. Gradual analog parameter drift within tolerance
   (e.g., a gain drift of 5% that is within the 10% tolerance)
   Mitigation: Periodic calibration by clinician during follow-up visits
   
2. Intermittent faults that disappear during testing
   (e.g., a loose wire bond that makes contact during test)
   Mitigation: Burn-in testing, thermal cycling, and extended test duration
   
3. Correlated faults affecting multiple redundant circuits
   (e.g., a process defect that affects all three TMR replicas)
   Mitigation: Physical separation, diverse redundancy, production testing
   
4. Faults in the monitoring circuits themselves
   (e.g., a comparator that fails to detect overvoltage)
   Mitigation: Dual monitoring with cross-checking, periodic BIST
```

### Fault Detection Trade-offs

```
Trade-off 1: Detection Speed vs. Power
  Faster detection requires faster circuits (more power)
  The iPACE-CHIP uses the minimum detection speed needed for safety

Trade-off 2: Coverage vs. Area
  Higher diagnostic coverage requires more monitoring circuits (more area)
  The iPACE-CHIP targets 99% DC, which requires ~5% additional area

Trade-off 3: False Alarm Rate vs. Sensitivity
  More sensitive monitoring increases false alarm rate
  The iPACE-CHIP uses hysteresis and filtering to minimize false alarms
  while maintaining adequate sensitivity
```

---

## 10.4.2.10 Chapter Summary

The iPACE-CHIP's fault detection architecture provides comprehensive monitoring of all critical subsystems, achieving a diagnostic coverage of 99.3% and meeting SIL 3 requirements.

Key fault detection mechanisms:

- **Analog monitoring:** Supply voltage, bandgap reference, output voltage/current, sensing amplifier (continuous)
- **Digital monitoring:** Memory ECC, DSP health, clock frequency, FSM state (periodic)
- **Self-test:** Memory BIST, analog BIST, full system BIST (startup and periodic)
- **Interconnect monitoring:** Bus ECC, wire bond integrity, lead impedance
- **Diagnostic data:** 2 Kbyte diagnostic memory, error logging, telemetry reporting

The fault detection architecture is designed with the following principles:
- **Independence:** Monitoring circuits are independent of the circuits they monitor
- **Speed:** Detection latency is matched to the severity of the fault (100 ns for dangerous output faults, 100 ms for non-urgent faults)
- **Coverage:** >99% diagnostic coverage for all Category A functions
- **Transparency:** All diagnostic data is available through telemetry for clinical review

The next chapter (10.4.3) covers emergency backup systems that provide the ultimate safety net when all other fault detection and mitigation mechanisms have been exhausted.

---

## References

1. IEC 61508:2010, "Functional Safety of Electrical/Electronic/Programmable Electronic Safety-Related Systems."
2. IEC 60601-1:2005, "Medical Electrical Equipment -- Part 1."
3. Gilsinn, J., "Built-In Self-Test for Mixed-Signal ASICs," *IEEE Aerospace Conference*, 2003.
4. Raburn, K., "Analog BIST Techniques," *IEEE International Test Conference*, 2001.
5. IEC 62304:2006, "Medical Device Software -- Software Life Cycle Processes."
6. Avizienis, A., et al., "Basic Concepts and Taxonomy of Dependable and Secure Computing," *IEEE TDSC*, 2004.
7. Storey, N., *Safety-Critical Computer Systems*, Addison-Wesley, 1996.
8. ANSI/AAMI EC11:1991/(R)2001/(R)2007, "Diagnostic Electrocardiographic Devices."
