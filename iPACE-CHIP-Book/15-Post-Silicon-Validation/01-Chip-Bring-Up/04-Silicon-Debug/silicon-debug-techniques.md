# Silicon Debug Techniques

## 15.4.1 Overview

Silicon debug is the systematic process of identifying and resolving discrepancies between the expected behavior (as defined by the RTL design and verified in simulation) and the actual behavior observed in manufactured silicon. For the iPACE-CHIP, silicon debug is particularly critical because any undetected functional or parametric defect could have life-threatening consequences in a pacemaker application. This chapter covers the techniques, tools, and methodologies used to debug the iPACE-CHIP silicon, ranging from non-invasive software-based techniques to physical failure analysis.

## 15.4.2 Debug Strategy Framework

### Debug Hierarchy

The debug process follows a hierarchical approach, starting with the least invasive techniques and escalating only as necessary:

```
Level 1: Software-Based Debug (non-invasive)
  - Register reads and writes
  - Memory dump and analysis
  - Firmware-based diagnostic routines
  - JTAG breakpoints and stepping

Level 2: Signal-Based Debug (minimally invasive)
  - Logic analyzer capture
  - Boundary scan
  - On-chip trace buffer
  - Test point monitoring

Level 3: Electrical Debug (invasive)
  - Micro-probing on package pins
  - Current signature analysis
  - Timing measurement with high-bandwidth scope

Level 4: Physical Debug (destructive)
  - Decapsulation
  - E-beam probing
  - FIB (Focused Ion Beam) modification
  - Physical failure analysis
```

### Debug Decision Tree

```
Issue Observed
  |
  +-- Is it reproducible?
  |     |
  |     +-- Yes --> Characterize conditions (voltage, temp, pattern)
  |     |           |
  |     |           +-- Does it happen at nominal conditions?
  |     |                 |
  |     |                 +-- Yes --> Level 1 debug
  |     |                 |
  |     |                 +-- No (marginal) --> Level 2 debug + characterization
  |     |
  |     +-- No (intermittent) --> Statistical analysis, Level 2 debug
  |
  +-- Is it functional or parametric?
        |
        +-- Functional --> Focus on logic and state machine debug
        |
        +-- Parametric --> Focus on analog/circuit-level debug
```

## 15.4.3 JTAG-Based Debug

### On-Chip Debug Architecture

The iPACE-CHIP integrates an ARM CoreSight debug subsystem that provides comprehensive visibility into the ARM Cortex-M0+ processor and the custom digital logic. The debug subsystem includes:

- **Debug Access Port (DAP)**: JTAG/SWD interface for host connection
- **AHB-AP**: Advanced High-performance Bus Access Port for memory and register access
- **Breakpoint Unit (FPB)**: Flash Patch and Breakpoint unit with 4 breakpoints
- **Data Watchpoint and Trace (DWT)**: Data watchpoints and cycle counter
- **Instrumentation Trace Macrocell (ITM)**: Software trace via printf-like statements
- **Embedded Trace Buffer (ETB)**: On-chip trace storage (256 entries)

### JTAG Debug Operations

```
Operation               | JTAG Sequence                    | Expected Result
------------------------|----------------------------------|------------------
IDCODE scan             | IR=IDCODE, read DR              | 0x4BA00477
Halt CPU                | Write DBG_HCR, set_HALT bit      | CPU halts, DBG_SR.HALTED=1
Read register Rn        | Read AHB-AP, Rn address          | Current Rn value
Write register Rn       | Write AHB-AP, Rn address, value  | Rn updated
Read memory             | AHB-AP read, target address      | Memory contents
Write memory            | AHB-AP write, target address     | Memory updated
Single step             | Write DBG_HCR, set_STEP bit      | One instruction executes
Set breakpoint          | Write FPB comparator register    | BP address loaded
Resume execution        | Write DBG_HCR, clear_HALT bit    | CPU resumes
Read PC                 | Read AHB-AP, PC address          | Current PC value
Read PSR                | Read AHB-AP, PSR address         | Current PSR value
```

### Firmware Diagnostic Routines

The iPACE-CHIP boot ROM includes built-in diagnostic routines accessible via JTAG:

```
Diagnostic Command       | JTAG Trigger                    | Expected Output
-------------------------|---------------------------------|------------------
Self-test                | Write 0x01 to DIAG_CTRL        | Test results in DIAG_STATUS
Register dump            | Write 0x02 to DIAG_CTRL        | All registers via UART
Memory map               | Write 0x03 to DIAG_CTRL        | Peripheral base addresses
Clock tree               | Write 0x04 to DIAG_CTRL        | Clock frequencies
Power domains            | Write 0x05 to DIAG_CTRL        | Domain status
Peripheral ID            | Write 0x06 to DIAG_CTRL        | All peripheral IDs
```

## 15.4.4 Logic Analyzer Techniques

### Signal Capture Strategy

When JTAG-based debug is insufficient, the logic analyzer provides visibility into real-time digital signal behavior. The key signals to capture for the iPACE-CHIP are:

### Digital Interface Signals

```
Signal Group         | Signals                              | Sample Rate
---------------------|--------------------------------------|-------------
JTAG                 | TCK, TMS, TDI, TDO, nTRST           | 100 MSa/s
SPI Bus              | SCLK, MOSI, MISO, CS[3:0]           | 100 MSa/s
UART Debug           | TXD, RXD                             | 1 MSa/s
Interrupt Lines      | IRQ[7:0], NMI, FAULT                 | 50 MSa/s
Pacing Control       | PACE_EN, PACE_POL, PACE_SEL[1:0]    | 10 MSa/s
Timing Control       | RTC_CLK, TIMER_TICK, WDT_FEED       | 10 MSa/s
Power Control        | LDO_EN[3:0], RET_EN, HIB_EN         | 1 MSa/s
```

### Trigger Configuration

Effective use of the logic analyzer requires precise trigger configuration to capture the events of interest:

```
Trigger Scenario                    | Trigger Condition
------------------------------------|------------------------------------------
Boot sequence capture               | Rising edge on nTRST + Pattern on UART
JTAG command capture                | Falling edge on TMS + Pattern on TDI
SPI flash read                      | Falling edge on CS + Pattern on MOSI
Interrupt timing                    | Any edge on IRQ[7:0] simultaneously
Pacing pulse timing                 | Rising edge on PACE_EN + Timer counter
State machine debug                 | Pattern on state register output
```

### Protocol Decoding

Modern logic analyzers support protocol decoding for common interfaces. The iPACE-CHIP uses several protocols that benefit from hardware decoding:

- **JTAG TAP state machine**: Decode TMS/TCK transitions to identify IR/DR scan states
- **SPI protocol**: Decode MOSI/MISO data with clock, display as hex values
- **UART (115200 8N1)**: Decode start bit, data bits, stop bit, display ASCII
- **Custom pacing protocol**: Decode pacing enable/disable sequences with timing

## 15.4.5 On-Chip Trace Buffer

### ETB Configuration

The Embedded Trace Buffer (ETB) captures a trace of executed instructions and data accesses without requiring external probe connections. The ETB is configured through the debug interface:

```
ETB Configuration:
  - Trace source: ARM Cortex-M0+ instruction trace
  - Trace format: Compact (16-bit entries)
  - Trigger condition: Programmable PC address or debug event
  - Buffer depth: 256 entries
  - Overflow behavior: Circular buffer (overwrite oldest)
```

### Trace Analysis

The captured trace data provides a history of the last 256 instructions executed before a debug event (breakpoint, watchdog reset, or error). Analysis of the trace can reveal:

- **Program flow**: Sequence of branches and function calls
- **Timing anomalies**: Instructions taking longer than expected
- **Infinite loops**: Repetitive instruction sequences
- **Exception entry/exit**: Interrupt and fault handler invocations
- **Data access patterns**: Memory read/write sequences

### Trace Decode Example

```
Trace Entry | PC Address  | Instruction          | Notes
----------- |-------------|----------------------|---------------------------
1           | 0x08001000  | LDR R0, [R1, #0]    | Load status register
2           | 0x08001002  | TST R0, #0x01        | Test bit 0 (ready flag)
3           | 0x08001004  | BEQ 0x08001000       | Branch if not ready (loop)
4           | 0x08001006  | LDR R2, [R1, #4]    | Load data register
5           | 0x08001008  | STR R2, [R3, #0]     | Store to memory
6           | 0x0800100A  | BL 0x08002000        | Call function
7           | 0x08002000  | PUSH {R4-R7, LR}    | Function prologue
```

## 15.4.6 Boundary Scan Testing

### Boundary Scan Architecture

The iPACE-CHIP implements IEEE 1149.1 boundary scan on all I/O pads. Each pad has an associated boundary scan cell (BSC) that can capture the pad's input value or override the pad's output value.

### Interconnect Test

The primary use of boundary scan for silicon debug is testing PCB interconnects between the chip and other components:

```
Test Procedure:
1. Set all BSCs to output mode with known pattern (0xAAAAAAAA)
2. Capture BSCs on adjacent device
3. Verify captured pattern matches expected (accounting for routing)
4. Invert pattern (0x55555555)
5. Repeat capture and verify
6. Run walking-1 and walking-0 patterns for complete coverage
```

### Cluster Test

Boundary scan can also test internal chip clusters (logic between BSCs):

```
Test Procedure:
1. Identify BSCs at the boundary of the cluster under test
2. Set input BSCs to drive mode with test pattern
3. Propagate pattern through cluster
4. Capture output BSCs
5. Compare with expected output from simulation
```

## 15.4.7 Electrical Characterization Debug

### Current Signature Analysis

Monitoring the current drawn by each supply rail during specific operations provides a powerful diagnostic tool. The current signature acts as a fingerprint for each functional state:

```
Operation               | I_VDD_ANA (mA) | I_VDD_DIG (mA) | I_VDD_IO (mA)
------------------------|----------------|-----------------|---------------
Idle (all blocks off)   | 0.10           | 0.50            | 0.05
ADC sampling             | 1.20           | 0.80            | 0.05
Pacing pulse output     | 0.15           | 1.00            | 2.50
Telemetry TX            | 0.20           | 1.50            | 0.10
Telemetry RX            | 0.30           | 1.20            | 0.10
Full operation          | 1.50           | 3.00            | 0.20
Sleep mode              | 0.05           | 0.01            | 0.01
Deep sleep              | 0.01           | 0.005           | 0.005
```

By comparing measured current signatures against these expected values, anomalies can be quickly identified:

- **Higher than expected current**: Possible latch-up, stuck-at fault, or unintended switching
- **Lower than expected current**: Possible open circuit, clock not running, or block not enabled
- **Oscillating current**: Possible metastability, bus contention, or PLL instability

### Timing Measurement

Critical timing paths must be verified against specification using high-bandwidth oscilloscopes:

```
Timing Parameter               | Specification      | Measurement Method
-------------------------------|--------------------|-----------------------
Pacing pulse width             | 0.05-2.0 ms       | Scope on PACE_OUT
Sensing amplifier settling     | < 50 us            | Scope on AFE output
ADC conversion time            | < 100 us           | Scope on ADC_EOC
SPI clock frequency            | 0-10 MHz           | Scope on SCLK
UART baud rate accuracy        | +/- 2%             | Frequency counter on TXD
JTAG clock maximum             | 20 MHz             | Eye diagram on TCK
Interrupt latency              | < 10 us            | Scope on IRQ and LED toggle
```

## 15.4.8 Scan Chain Debug

### Scan Chain Architecture

The iPACE-CHIP includes a full scan chain for manufacturing test. The scan chain connects all flip-flops in the design into a shift register, allowing arbitrary state injection and observation:

```
Scan chain configuration:
  - Chain length: ~45,000 flip-flops
  - Scan clock: Maximum 10 MHz
  - Scan data width: 1 bit (serial)
  - Total shift time: ~4.5 ms per pattern
```

### Scan-Based Debug Procedure

```
Step 1: Shift in a known state pattern (captures current chip state)
Step 2: Capture pattern data for analysis
Step 3: Compare captured state with expected state from simulation
Step 4: Identify flip-flops that don't match
Step 5: Trace those flip-flops back to their logic cones
Step 6: Identify the root cause (logic bug, timing violation, or unknown)
```

### Scan Pattern Generation

Automatic Test Pattern Generation (ATPG) tools create scan patterns that target specific fault models:

| Fault Model | Description | Patterns Required |
|------------|-------------|-------------------|
| Stuck-at-0 | Node permanently stuck at logic 0 | ~500 |
| Stuck-at-1 | Node permanently stuck at logic 1 | ~500 |
| Transition delay | Node slow to rise or fall | ~1000 |
| Path delay | Cumulative delay along a timing path | ~2000 |
| Bridge fault | Unintended connection between nodes | ~800 |

## 15.4.9 Analog Debug Techniques

### Frequency Response Analysis

The iPACE-CHIP's analog front-end requires detailed frequency characterization to verify filtering performance:

```
Measurement Setup:
  Function Generator --> AFE Input --> ADC --> Data Capture
  Oscilloscope (monitor)    |                    |
                            +--- BNC cable ------+

Test Procedure:
  1. Generate sine wave at known amplitude
  2. Sweep frequency from 0.01 Hz to 1 kHz
  3. Record ADC output at each frequency
  4. Calculate gain = 20*log10(Vout/Vin)
  5. Plot Bode magnitude and phase
  6. Verify corner frequencies and roll-off rates
```

### Noise Measurement

Noise characterization of the analog front-end requires careful measurement setup to avoid external noise pickup:

```
Measurement Setup:
  - Shielded enclosure (Faraday cage)
  - Battery-powered signal source (no mains hum)
  - Low-noise preamplifier (optional, for sub-uV signals)
  - Averaging scope or FFT analyzer

Procedure:
  1. Short AFE inputs together
  2. Configure AFE for maximum gain
  3. Record 10,000 samples at maximum sample rate
  4. Perform FFT analysis
  5. Identify noise components:
     - 1/f noise (flicker): dominant below 10 Hz
     - Thermal noise: flat floor above 10 Hz
     - 50/60 Hz pickup: mains interference
     - Clock feedthrough: switching noise
  6. Integrate noise over bandwidth of interest
  7. Report input-referred RMS noise
```

### Offset and Drift Measurement

DC offset and temperature drift of the analog front-end are critical for sensing accuracy:

```
Procedure:
  1. Short inputs to common-mode voltage
  2. Record ADC output at 25C (room temperature)
  3. Set oven temperature to -40C, stabilize, record
  4. Set oven temperature to +85C, stabilize, record
  5. Calculate offset at each temperature
  6. Calculate temperature coefficient (ppm/C)
  7. Verify offset stays within specification across range
```

## 15.4.10 Timing Closure Debug

### Setup and Hold Violation Detection

Timing violations are among the most common silicon bugs. They manifest as intermittent functional failures that are sensitive to voltage, temperature, and data patterns:

```
Detection Methods:
  1. Scan chain testing: Shift data through at-speed, check capture
  2. Functional testing: Run at-speed patterns, check for errors
  3. BIST (Built-In Self Test): Run at-speed memory and logic tests
  4. Shmoo analysis: Test across voltage and frequency ranges

Resolution Methods:
  1. Reduce clock frequency (if specification allows)
  2. Increase supply voltage (if specification allows)
  3. Add pipeline stages (RTL change + respin)
  4. Restructure logic (RTL change + respin)
```

### Clock Domain Crossing Issues

The iPACE-CHIP has multiple clock domains (32 kHz RTC, 4 MHz system, and JTAG TCK). Metastability at clock domain crossings is a potential source of intermittent failures:

```
Debug Approach:
  1. Identify all clock domain crossing (CDC) points in the RTL
  2. Verify synchronization logic (double-flop, handshake) exists at each
  3. Run long-duration test with data toggling at CDC points
  4. Check for single-event upset (SEU) sensitivity
  5. Verify CDC timing constraints in synthesis
```

## 15.4.11 Debug Data Management

### Bug Tracking System

Every silicon issue discovered during debug is entered into a formal bug tracking system with the following fields:

```
Bug Report Structure:
  - Bug ID: Sequential number (iPACE-SIL-NNN)
  - Title: Brief description
  - Severity: Critical/Major/Minor/Cosmetic
  - Category: Functional/Parametric/Timing/Yield
  - Affected Blocks: List of RTL modules involved
  - Reproduction Steps: Detailed procedure to observe
  - Frequency: Always/Intermittent/Rare
  - Conditions: Voltage, temperature, pattern dependency
  - Root Cause: Identified cause (or TBD)
  - Fix: Proposed fix (RTL change, ECO, or workaround)
  - Affected Lots: Silicon lot and wafer numbers
  - Status: Open/Debugging/Fix-Verified/Closed
```

### Root Cause Analysis

For each silicon bug, a systematic root cause analysis is performed:

```
Analysis Methodology:
  1. Symptom characterization: Exactly what behavior is observed
  2. Scope narrowing: Which conditions trigger the bug
  3. Hypothesis generation: What could cause this behavior
  4. Hypothesis testing: Simulation, emulation, or measurement
  5. Root cause confirmation: Prove the identified cause
  6. Fix development: RTL change or workaround
  7. Fix verification: Confirm fix resolves issue without side effects
```

## 15.4.12 Debug Tool Requirements

### Equipment List

| Equipment | Model Examples | Purpose |
|-----------|---------------|---------|
| JTAG Adapter | ARM J-Link Pro, CMSIS-DAP | Chip debug interface |
| Logic Analyzer | Keysight 16862A, Saleae Logic Pro 16 | Digital signal capture |
| Oscilloscope | Keysight DSOX6004A, Tektronix MSO64 | Analog/timing measurement |
| Spectrum Analyzer | Keysight N9020B | Telemetry frequency analysis |
| Function Generator | Keysight 33500B | Test stimulus generation |
| Power Supply | Keysight E36312A | Clean, programmable power |
| Frequency Counter | Keysight 53230A | Precision frequency measurement |
| Thermal Chamber | Espec EWSH-408 | Temperature testing |
| Probe Station | Cascade Microtech | On-wafer measurement |
| Stereoscope | Zeiss Stemi 305 | Visual inspection |

### Software Tools

| Tool | Purpose |
|------|---------|
| pyOCD | Open-source JTAG/SWD host adapter |
| OpenOCD | On-chip debugger |
| Sigrok | Logic analyzer control and analysis |
| Python + pyvisa | Instrument automation |
| MATLAB | Signal processing and analysis |
| Synopsys Verdi | Waveform viewing and debug |
| Cadence SimVision | Mixed-signal debug |

## 15.4.13 Summary

Silicon debug for the iPACE-CHIP requires a methodical approach that leverages multiple levels of visibility, from software-based JTAG debug to physical failure analysis. The key to effective debug is thorough documentation, systematic hypothesis testing, and the discipline to follow the debug hierarchy. By investing in robust debug infrastructure (JTAG, boundary scan, on-chip trace) during the design phase, the validation team maximizes their ability to diagnose issues quickly and minimize the number of expensive silicon respins. The techniques described in this chapter, combined with the test board and measurement infrastructure described earlier, provide a comprehensive toolkit for resolving any silicon challenges that arise during the iPACE-CHIP validation campaign.
