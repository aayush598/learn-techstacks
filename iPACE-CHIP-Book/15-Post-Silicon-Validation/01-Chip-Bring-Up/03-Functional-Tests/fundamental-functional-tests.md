# Fundamental Functional Tests

## 15.3.1 Overview

Following a successful power-on, the fundamental functional tests verify that each major subsystem of the iPACE-CHIP operates correctly at the basic level. These tests are not exhaustive characterizations but rather go/no-go checks that confirm the silicon implementation matches the design intent. Each test exercises a specific functional block, verifies expected behavior against the specification, and records pass/fail status for the validation report. The tests are organized in dependency order, with each test building on the results of previous tests.

## 15.3.2 Test Infrastructure

### Automated Test Environment

The fundamental functional tests are executed using an automated test framework that communicates with the iPACE-CHIP through JTAG and UART interfaces. The test controller (a host PC running Python scripts via pyOCD) orchestrates the following:

- Register reads and writes via JTAG
- Stimulus generation via board DACs
- Response capture via board ADCs
- Timing measurements via oscilloscope triggering
- Result logging to a structured data file

### Test Sequence Overview

The complete test suite consists of 47 individual tests organized into 8 functional groups:

```
Test Group                    | Test Count | Estimated Time
------------------------------|------------|----------------
1. Digital Core               | 6          | 2 minutes
2. Memory Subsystem           | 8          | 5 minutes
3. Clock and Timer            | 7          | 10 minutes
4. Analog Front-End           | 10         | 30 minutes
5. Digital Control Logic      | 5          | 15 minutes
6. Pacing Output              | 4          | 10 minutes
7. Telemetry Interface        | 3          | 10 minutes
8. Safety Mechanisms          | 4          | 15 minutes
------------------------------|------------|----------------
Total                         | 47         | 97 minutes
```

## 15.3.3 Digital Core Tests

### Test DC-01: CPU Boot Verification

```
Objective: Verify ARM Cortex-M0+ boots from internal ROM
Preconditions: All supplies nominal, nRESET released
Procedure:
  1. Read program counter via JTAG
  2. Verify PC is within boot ROM address range (0x00000000 - 0x00003FFF)
  3. Step through first 100 instructions
  4. Verify UART output matches expected boot string
Pass Criteria: PC starts at 0x00000004, UART outputs boot identification
```

### Test DC-02 through DC-06

```
DC-02: Register Access
  Write known patterns to R0-R12, read back and compare.
  Test SP, LR, PSR. All registers match expected after read/write.

DC-03: ALU Operations
  Execute ADD with carry, SUB with borrow, MUL, AND/ORR/EOR, barrel shift.
  Verify APSR flags after each operation. All ALU operations correct.

DC-04: Interrupt Controller
  Enable 3 test interrupts with known priorities, trigger all simultaneously.
  Verify highest priority serviced first, lower pending, nesting works.

DC-05: Debug Interface
  Halt CPU, read registers, single-step, set breakpoint, resume.
  All debug operations complete without error.

DC-06: Low-Power Modes
  Enter Sleep (WFI), verify current < 500 uA, wake via interrupt.
  Enter Deep Sleep, verify current < 50 uA, wake. Enter Hibernate, verify < 1 uA.
```

## 15.3.4 Memory Subsystem Tests

### Test MEM-01: SRAM Read/Write

```
Objective: Verify basic SRAM functionality
Procedure:
  1. Write pattern 0x00000000 to all SRAM locations
  2. Read back, verify all locations match
  3. Write pattern 0xFFFFFFFF, read and verify
  4. Write alternating 0xAAAAAAAA / 0x55555555, read and verify
  5. Write incrementing address pattern, read and verify
Pass Criteria: All SRAM locations correctly store and retrieve data
```

### Test MEM-02: SRAM March Test

```
Objective: Detect stuck-at faults and coupling faults in SRAM
Procedure: Execute March C- algorithm on each 4 KB SRAM bank independently
Pass Criteria: March C- completes without error on all 4 banks
```

### Test MEM-03: Flash Read

```
Objective: Verify Flash memory read functionality
Procedure:
  1. Read Flash ID register (expect manufacturer/device ID)
  2. Read first 256 bytes (boot ROM area), compare with golden reference
  3. Read from middle and end of Flash array
  4. Verify ECC status for all reads
Pass Criteria: Flash ID correct, data matches reference, no ECC errors
```

### Test MEM-04: Flash Program/Erase

```
Objective: Verify Flash write and erase functionality
Procedure:
  1. Read target sector, save as backup
  2. Erase sector (~50 ms per 2 KB sector), read back verify 0xFF
  3. Program known pattern, read back verify data matches
  4. Restore original data from backup
Pass Criteria: Erase sets 0xFF, program writes correctly
```

### Test MEM-05 through MEM-08

```
MEM-05: Flash ECC
  Inject single-bit error (corrected), double-bit error (detected, NMI).
  Verify ECC error status register reflects error type correctly.

MEM-06: Memory Protection (MPU)
  Configure MPU to protect Flash sector 0 as read-only.
  Write from user mode generates HardFault. Write from privileged succeeds.

MEM-07: DMA Transfer
  Memory-to-memory 1024-word transfer via DMA channel.
  Verify DMA complete interrupt and data integrity.

MEM-08: Memory Arbitration
  Concurrent CPU execution from SRAM and DMA transfer.
  Both complete without error, no data corruption.
```

## 15.3.5 Clock and Timer Tests

### Test CLK-01: Internal Oscillator Frequency

```
Objective: Verify internal RC oscillator frequency accuracy
Procedure:
  1. Route internal oscillator to MCO pin
  2. Measure frequency with 7-digit frequency counter
  3. Record frequency at room temperature (25C)
  4. Calculate error from 32,768 Hz target
Pass Criteria: Frequency within 32,768 Hz +/- 10%
```

### Test CLK-02: External Crystal Oscillator

```
Objective: Verify external crystal oscillator startup and accuracy
Procedure:
  1. Connect 32.768 kHz crystal to XTAL pins
  2. Enable external oscillator, measure time to CLK_STATUS.READY
  3. Measure frequency on MCO, calculate error
Pass Criteria: Startup < 500 ms, frequency within +/- 20 ppm
```

### Test CLK-03 through CLK-07

```
CLK-03: PLL Lock
  Configure PLL for 4 MHz from 32.768 kHz source.
  Lock within 10 ms, output frequency stable within +/- 1%.

CLK-04: Timer Accuracy
  Configure Timer 0 for 1 ms period interrupt, count for 60 seconds.
  Timer accuracy within +/- 1% of target period.

CLK-05: Timer Capture/Compare
  1 kHz input capture measures correctly, 2 kHz output compare verified.

CLK-06: Real-Time Clock
  Initialize RTC with known time, verify advancement and alarm interrupt.

CLK-07: Clock Source Switching
  Switch from internal oscillator to external crystal, verify glitch-free
  transition on MCO output, system continues running.
```

## 15.3.6 Analog Front-End Tests

### Test AFE-01: Input Buffer Operation

```
Objective: Verify AFE input buffer amplification
Procedure:
  1. Apply 1 mV DC to AIN+ input (differential)
  2. Set AFE gain to x1, read ADC output
  3. Change gain to x4, x8, x16, verify output scales correctly
Pass Criteria: Output within 5% of expected value at each gain setting
```

### Test AFE-02: Input Impedance

```
Objective: Verify AFE input impedance meets specification
Procedure:
  1. Connect precision 10 MOhm resistor in series with signal source
  2. Apply known voltage, measure voltage at AFE input
  3. Calculate input impedance from voltage divider equation
Pass Criteria: Input impedance > 100 MOhm at DC
```

### Test AFE-03: Bandwidth

```
Objective: Verify AFE analog bandwidth
Procedure:
  1. Apply 100 uV sine wave at 1 Hz, measure output amplitude
  2. Sweep frequency from 0.1 Hz to 1 kHz, plot amplitude vs. frequency
  3. Identify -3 dB point (cutoff frequency)
Pass Criteria: -3 dB bandwidth is 0.5 Hz to 200 Hz (bandpass)
```

### Test AFE-04 through AFE-10

```
AFE-04: CMRR
  Apply 100 mV common-mode signal, measure differential output.
  CMRR = 20*log10(Vcm/Vout_diff) > 80 dB at 50 Hz.

AFE-05: Noise Floor
  Short both inputs, record 10,000 ADC samples at max gain.
  Calculate RMS noise, refer to input. Input-referred noise < 5 uV RMS.

AFE-06: ADC Linearity (DNL/INL)
  Apply DC ramp from -10 mV to +10 mV, record 256 evenly-spaced points.
  Calculate DNL and INL. |DNL| < 1 LSB, |INL| < 2 LSB.

AFE-07: ADC Offset and Gain Error
  Apply 0V differential (offset), full-scale differential (gain).
  |Offset| < 5 LSB, |Gain error| < 1%.

AFE-08: Channel-to-Channel Isolation
  Apply 10 mV signal to AIN1, measure AIN2/AIN3.
  Channel isolation > 60 dB for all channel pairs.

AFE-09: PGA Gain Accuracy
  Apply 1 mV signal, set PGA to gains 1/2/4/8/16.
  All gain settings within 2% of nominal.

AFE-10: Input Protection
  Apply +5V and -1V to AFE input, verify current limiting and recovery.
  AFE returns to normal operation after overvoltage removal.
```

## 15.3.7 Digital Control Logic Tests

### Test DCL-01: Pacing State Machine

```
Objective: Verify pacemaker mode state machine operation
Procedure:
  1. Configure chip in VVI mode
  2. Apply no input signal, verify pacing at lower rate limit
  3. Verify pacing pulse width and amplitude match settings
  4. Apply sensed event during refractory period
  5. Verify pacing is not inhibited during refractory period
Pass Criteria: State machine correctly transitions between states
```

### Test DCL-02 through DCL-05

```
DCL-02: Sensing Algorithm
  Configure threshold to 0.5 mV. Apply 0.3 mV (no detect), 0.7 mV (detect).
  Sweep 0.1-1.0 mV, record detection probability. Transition at 0.4-0.6 mV.

DCL-03: Refractory Period
  Configure AREF=250 ms, RREF=500 ms. Deliver pacing pulse.
  Event at 100 ms (within AREF): not sensed. Event at 300 ms (REF): sensed but no reset.
  Event at 600 ms: sensed and resets timing. Boundaries correct within 5 ms.

DCL-04: Pacing Output Waveform
  Configure 3.5V/0.5 ms, capture on oscilloscope.
  Amplitude within 10% of setting, pulse width within 5%.

DCL-05: Autocapture Verification
  Start at 3.5V, reduce by 0.5V until capture loss.
  Find threshold, set output to threshold + 0.5V safety margin.
```

## 15.3.8 Pacing Output Tests

### Test PO-01 through PO-04

```
PO-01: Multi-Channel Output
  DDD mode with atrial tracking. Verify AV delay between atrial sense
  and ventricular pace. Both channels produce correct waveforms simultaneously.

PO-02: Output Polarity
  Configure tip-positive, capture waveform. Switch to tip-negative, capture.
  Polarity switches correctly, amplitude unaffected.

PO-03: Maximum Output
  Set 7.5V/2.0 ms. Verify amplitude and pulse width. Measure current < 10 mA.

PO-04: Output Disable
  Disable output via register. Verify high-impedance state, leakage < 1 uA.
  Re-enable, verify normal operation.
```

## 15.3.9 Telemetry Interface Tests

### Test TEL-01 through TEL-03

```
TEL-01: Link Establishment
  Place reader at 2 cm, initiate link. Verify chip detects reader and responds.
  Link established within 1 second with bidirectional data exchange.

TEL-02: Data Integrity
  Read/write 1 KB via telemetry, compare with JTAG register reads.
  100% data integrity with CRC verification.

TEL-03: Range Test
  Sweep distance from 0.5 cm to 5 cm in 0.5 cm steps.
  Record maximum distance for reliable communication. Verify close-range safety.
```

## 15.3.10 Safety Mechanism Tests

### Test SAF-01 through SAF-04

```
SAF-01: Watchdog Timer
  Configure 1 s timeout, do not service watchdog. Verify reset after timeout.
  Reset cause register shows watchdog. Firmware restarts correctly.

SAF-02: Voltage Monitor (Brownout Detection)
  Reduce VDD_DIG from 1.2V. BOD interrupt at 1.05V, reset at 0.95V.
  Hysteresis 100 mV between interrupt and reset thresholds.

SAF-03: Temperature Sensor
  Read temperature at 25C (compare to external sensor). Heat to 40C.
  Verify reading within 2C. Set alarm at 42C, verify triggers correctly.

SAF-04: ECC Error Handling
  Inject single-bit error (corrected), double-bit error (detected, NMI).
  Verify error counters increment. SECDED functional.
```

## 15.3.11 Test Results Summary

The complete test results are recorded in a structured format for traceability:

```
Test ID | Test Name                    | Result | Notes
--------|------------------------------|--------|---------------------------
DC-01   | CPU Boot Verification        | PASS   | Boot ROM v1.2 detected
DC-02   | Register Access              | PASS   | All R0-R15 verified
DC-03   | ALU Operations               | PASS   | All operations correct
DC-04   | Interrupt Controller         | PASS   | Priority nesting correct
DC-05   | Debug Interface              | PASS   | JTAG and SWD functional
DC-06   | Low-Power Modes              | PASS   | Sleep current 450 uA
MEM-01  | SRAM Read/Write              | PASS   | All patterns correct
MEM-02  | SRAM March Test              | PASS   | No faults detected
MEM-03  | Flash Read                   | PASS   | Boot ROM verified
MEM-04  | Flash Program/Erase          | PASS   | Sector erase 48 ms avg
MEM-05  | Flash ECC                    | PASS   | SECDED functional
MEM-06  | Memory Protection            | PASS   | MPU regions enforced
MEM-07  | DMA Transfer                 | PASS   | 32-bit transfer verified
MEM-08  | Memory Arbitration           | PASS   | No bus contention
CLK-01  | Internal Oscillator          | PASS   | 33,012 Hz (+0.74%)
CLK-02  | External Crystal             | PASS   | 32,768.1 Hz (+0.003%)
CLK-03  | PLL Lock                     | PASS   | Lock time 8.2 ms
CLK-04  | Timer Accuracy               | PASS   | 0.02% error
CLK-05  | Timer Capture/Compare        | PASS   | Both directions verified
CLK-06  | Real-Time Clock              | PASS   | Drift < 1 ppm
CLK-07  | Clock Source Switching       | PASS   | Glitch-free transition
AFE-01  | Input Buffer Operation       | PASS   | Gain within 1.5%
AFE-02  | Input Impedance              | PASS   | > 150 MOhm measured
AFE-03  | Bandwidth                    | PASS   | 0.5-200 Hz verified
AFE-04  | CMRR                         | PASS   | 86 dB at 50 Hz
AFE-05  | Noise Floor                  | PASS   | 3.8 uV RMS
AFE-06  | ADC Linearity                | PASS   | DNL < 0.8 LSB, INL < 1.5 LSB
AFE-07  | ADC Offset and Gain          | PASS   | Offset 2 LSB, Gain 0.3%
AFE-08  | Channel Isolation            | PASS   | > 65 dB all pairs
AFE-09  | PGA Gain Accuracy            | PASS   | Within 1.8% all gains
AFE-10  | Input Protection             | PASS   | Survived 5V, recovered
DCL-01  | Pacing State Machine         | PASS   | VVI mode correct
DCL-02  | Sensing Algorithm            | PASS   | Threshold at 0.48 mV
DCL-03  | Refractory Period            | PASS   | AREF 252 ms, RREF 498 ms
DCL-04  | Pacing Output Waveform       | PASS   | 3.45V, 0.49 ms measured
DCL-05  | Autocapture Verification     | PASS   | Threshold 2.8V, margin 0.7V
PO-01   | Multi-Channel Output         | PASS   | AV delay 198 ms (200 set)
PO-02   | Output Polarity              | PASS   | Both polarities verified
PO-03   | Maximum Output               | PASS   | 7.45V, 1.98 ms
PO-04   | Output Disable               | PASS   | Leakage 0.3 uA
TEL-01  | Link Establishment           | PASS   | Link in 0.8 s
TEL-02  | Data Integrity               | PASS   | CRC verified, 0 errors
TEL-03  | Range Test                   | PASS   | 0.5-5.5 cm range
SAF-01  | Watchdog Timer               | PASS   | Reset at 1.01 s
SAF-02  | Voltage Monitor              | PASS   | BOD 1.04V, reset 0.96V
SAF-03  | Temperature Monitor          | PASS   | 1.5C accuracy
SAF-04  | ECC Error Handling           | PASS   | SECDED functional

Overall Result: ALL 47 TESTS PASSED
```

## 15.3.12 Summary

The fundamental functional tests confirm that the iPACE-CHIP silicon is operationally sound across all major subsystems. With all 47 tests passing, the validation team can proceed with confidence to the characterization phase, where detailed parametric measurements will be performed. The test results also provide a baseline reference for production testing, establishing the expected behavior and parameter ranges for known-good silicon. Any test failures at this stage would trigger a debug investigation using the techniques described in the Silicon Debug chapter, potentially leading to silicon respin if the failure is due to a design bug rather than a test setup issue.
