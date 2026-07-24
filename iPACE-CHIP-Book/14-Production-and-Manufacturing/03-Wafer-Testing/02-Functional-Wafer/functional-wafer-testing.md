# 14.3.2 Functional Wafer Testing for iPACE-CHIP

## Overview

Functional wafer testing verifies that every iPACE-CHIP die operates correctly across
all operational modes before committing to hermetic packaging. While parametric testing
measures individual electrical characteristics, functional testing exercises the complete
signal path from neural signal acquisition through stimulation delivery and wireless
telemetry. This chapter defines the functional test methodology, stimulus/response
sequences, test patterns, and pass/fail criteria that ensure zero-defect die ship to
the assembly line.

## Test Architecture

### Functional Test Philosophy

The iPACE-CHIP functional test applies known input stimuli and verifies expected output
responses, covering:

1. **Digital Logic**: RISC-V processor execution, memory read/write, register access
2. **Analog Signal Chain**: Amplifier response, filter behavior, ADC accuracy
3. **Stimulation Output**: Current source accuracy, pulse timing, compliance voltage
4. **Telemetry**: RF carrier generation, data encoding, modulation depth
5. **Power Management**: Regulator operation, power sequencing, brown-out detection
6. **Clock System**: Oscillator start-up, PLL lock, clock switching

### Test Setup Block Diagram

```
Wafer Probe Station with Functional Test

    +-------------------+     +-------------------+
    |   Digital Pattern  |     |   Analog Stimulus  |
    |   Generator        |     |   Source            |
    |   (DPG)            |     |   (AWG)            |
    +--------+----------+     +--------+----------+
             |                          |
             |    Probe Card            |
             +----------+---------------+
                        |
                   +----+----+
                   |  Probe  |
                   |  Tips   |
                   +----+----+
                        |
              +---------+---------+
              |   iPACE-CHIP Die  |
              |   on Wafer        |
              +-------------------+
                        |
                   +----+----+
                   |  Probe  |
                   |  Tips   |
                   +----+----+
                        |
             +----------+---------------+
             |                          |
    +--------+----------+     +--------+----------+
    |   Digital Capture  |     |   Analog Capture   |
    |   Unit (DCU)       |     |   Oscilloscope     |
    |                    |     |   /Digitizer       |
    +-------------------+     +-------------------+
                        |
                   +----+----+
                   |  Test   |
                   |  PC     |
                   +---------+
```

## Digital Functional Test

### Processor Core Test

The RISC-V control processor is tested using a comprehensive instruction sequence:

**Test Sequence**:

1. **Reset and Boot**: Apply reset, verify boot vector loads correctly
2. **Register Test**: Write/read all 32 general-purpose registers
3. **ALU Test**: Execute arithmetic and logical operations, verify results
4. **Branch Test**: Execute all branch types (beq, bne, blt, bge, etc.)
5. **Memory Test**: Write/read all SRAM locations with walking-1/0 patterns
6. **CSR Test**: Read/write control and status registers

**Key Timing Measurements**:

| Test | Measurement | Accept Criteria |
|------|------------|-----------------|
| Boot Time | Reset to first instruction | < 100 us |
| Clock Frequency | Maximum operating frequency | 1.0 MHz +/- 5% |
| Interrupt Latency | IRQ to ISR entry | < 20 us |
| Power Mode Transition | Active to sleep | < 10 us |

### Memory Test Patterns

**SRAM Test (on-chip, 64 KB)**:

| Pattern | Description | Purpose |
|---------|------------|---------|
| Walking-1 | 0000...0001, 0000...0010, ... | Stuck-at faults |
| Walking-0 | 1111...1110, 1111...1101, ... | Stuck-at faults |
| Checkerboard | 1010...1010 / 0101...0101 | Coupling faults |
| Galloping | Compare each cell to every other | Data retention, coupling |
| March C- | 6N pattern | Comprehensive coverage |

**Test Time Calculation**:

```
SRAM Size: 64 KB = 524,288 bits
March C- Length: 14N = 7,340,032 operations
Test Rate: 1 MHz (single-cycle per operation)
March C- Test Time: 7.34 seconds

Parallel Test (8 blocks): 7.34 / 8 = 0.92 seconds
```

**EEPROM Test (on-chip, 2 KB)**:

| Test | Method | Accept Criteria |
|------|--------|-----------------|
| Write | Program all locations | No errors |
| Read Back | Read all locations | 100% match |
| Endurance | 100 write/erase cycles | 0 failures |
| Retention | Write, wait 24 hr, read | 100% data integrity |
| ECC Function | Inject 1-bit error, verify correction | Corrected within 1 read cycle |

### Digital I/O Test

| Test | Input | Expected Output | Timing |
|------|-------|-----------------|--------|
| GPIO Write | Logic pattern on DIN pins | Verify on DOUT pins | < 1 us |
| SPI Write | MOSI pattern | MISO response | Per SPI spec |
| I2C ACK | Address byte | ACK received | < 100 us |
| UART Baud | 9600 baud test | Correct character | < 1 ms |

## Analog Functional Test

### Neural Amplifier Signal Chain Test

**Test Stimulus**:

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| Input Frequency | 1 kHz | Midband signal |
| Input Amplitude | 100 uVpp | Within expected neural signal range |
| Input Type | Differential | Match electrode configuration |
| Common-Mode Level | VDD/2 = 0.9V | Normal operating point |
| Common-Mode Interference | 50 Hz, 10 mVpp | Power line interference |

**Expected Response**:

| Parameter | Accept Criteria | Measurement |
|-----------|-----------------|-------------|
| Output Amplitude | 2.0 mVpp +/- 5% | Gain = 20 V/V |
| Output DC Level | VDD/2 +/- 50 mV | Bias point accuracy |
| THD | < 1% | Harmonic analysis |
| CMRR at 50 Hz | > 70 dB | Differential output / CM input |
| Noise (1-7 kHz) | < 2.0 uVrms input referred | 10-second RMS measurement |

### Filter Response Test

The iPACE-CHIP analog front end includes programmable high-pass and low-pass filters:

**Filter Transfer Function Test**:

```
Test Procedure:
1. Apply sine wave at multiple frequencies: 0.1, 0.5, 1, 2, 3, 5, 7, 10, 20 kHz
2. Measure output amplitude at each frequency
3. Construct Bode plot (magnitude vs. frequency)
4. Extract -3dB cutoff frequencies

Expected Bode Plot:

Gain (dB)
    |
  26|         _______________
    |        /
  20|       /
    |      /
    |     /    Passband
  0 |    /     (20 dB gain)
    |   /
-10 |  /  HPF @ 300 Hz
    | /
-20 |/  LPF @ 7 kHz
    |
    +-----+-----+-----+-----+-----+
       0.1   1    10   100  1000  10k
                    Frequency (Hz)
```

| Filter Parameter | Nominal | Accept Range | Measurement Method |
|-----------------|---------|-------------|-------------------|
| HPF Cutoff (-3dB) | 300 Hz | 250-350 Hz | Amplitude sweep |
| LPF Cutoff (-3dB) | 7.0 kHz | 6.0-8.0 kHz | Amplitude sweep |
| Passband Gain | 20 dB | 19-21 dB | 1 kHz measurement |
| Stopband Rejection | > 40 dB | > 35 dB at 20 kHz | 20 kHz measurement |
| Group Delay | < 100 us | < 150 us at 1 kHz | Phase measurement |

### ADC Functional Test

The iPACE-CHIP includes a 12-bit SAR ADC for digitizing neural signals:

**Linearity Test (Histogram Method)**:

1. Apply a full-scale ramp (0 to VREF) at the ADC input
2. Collect 100,000 samples
3. Build histogram of code occurrences
4. Calculate INL and DNL from histogram

**Expected Results**:

| Parameter | Accept Criteria | Test Condition |
|-----------|-----------------|----------------|
| INL | < +/- 1.0 LSB | Full range ramp |
| DNL | < +/- 0.5 LSB | Full range ramp |
| ENOB | > 10.5 bits | SNR measurement at 1 kHz |
| THD | < -60 dB | 1 kHz full-scale input |
| Conversion Rate | > 50 kSPS | Maximum clock rate |
| Offset Error | < +/- 5 LSB | Zero-scale measurement |
| Gain Error | < +/- 0.5% | Full-scale measurement |

## Stimulation Functional Test

### Current Source Test

The iPACE-CHIP generates biphasic stimulation pulses for neural modulation:

**Stimulation Waveform Verification**:

```
Ideal Stimulation Pulse:

Current (mA)
    |
  1.0|    +--------+
    |    |        |
    |    |        |
  0 +----+        +--------+--------+
    |                       |        |
    |                       |        |
 -1.0|                       +--------+
    |        |        |        |
    |<--Cathodic-->|<--Anodic-->|
    |   100 us  |  100 us    |
    |<---Charge Balanced--->|

Output Voltage (with 1 kOhm load):
    +--------+                  +--------+
    | 5V    |                  |        |
    |        |                  |        |
    +--------+                  +--------+
    |        |                  |        |
    |        +--------+--------+        |
    |                 |                 |
    |                 0V               |
```

**Stimulation Test Parameters**:

| Test | Parameter | Accept Criteria |
|------|-----------|-----------------|
| Amplitude Accuracy | Cathodic peak | 1.0 mA +/- 5% |
| Amplitude Accuracy | Anodic peak | 1.0 mA +/- 5% |
| Pulse Width | Cathodic phase | 100 us +/- 5% |
| Pulse Width | Anodic phase | 100 us +/- 5% |
| Charge Balance | Net charge | < 2% error |
| Rise Time | 10% to 90% | < 10 us |
| Fall Time | 90% to 10% | < 10 us |
| Interphase Delay | Between phases | 10 us +/- 1 us |
| Compliance Voltage | At 1 mA, 10 kOhm load | > 6V |
| Output Leakage | No stimulation, output on | < 10 nA |

### Multi-Channel Stimulation Test

For multi-channel operation, verify no crosstalk between channels:

| Test | Method | Accept Criteria |
|------|--------|-----------------|
| Channel Isolation | Stim Ch1, measure Ch2 | < 0.1% coupling |
| Simultaneous Stim | Stim all channels | Amplitude accuracy maintained |
| Sequence Accuracy | Timed burst pattern | Timing error < 5 us |
| Charge Monitor | Verify charge counter | Net charge < threshold |

## Telemetry Functional Test

### RF Carrier Test

**Test Parameters**:

| Parameter | Accept Criteria | Measurement |
|-----------|-----------------|-------------|
| Carrier Frequency | 13.56 MHz +/- 100 kHz | Frequency counter |
| Modulation Depth (ASK) | 10% +/- 2% | Oscilloscope envelope |
| Output Power | -10 to 0 dBm | RF power meter |
| Harmonic Content | > 30 dB below carrier | Spectrum analyzer |
| Sideband Suppression | > 25 dBc | Spectrum analyzer |

### Data Encoding Test

| Test | Input Data | Expected Output | Criteria |
|------|-----------|-----------------|----------|
| Manchester Encode | 0x55 (alternating) | 13.56 MHz modulated | Correct encoding |
| Packet Format | Test packet | Complete frame | CRC check pass |
| Data Rate | 100 kbps | Measured throughput | Within 5% of nominal |
| Bit Error Rate | 1 Mbit test | BER measurement | < 10^-6 |

### Telemetry Link Test

The functional test verifies end-to-end telemetry by:

1. Writing a known data pattern to the iPACE-CHIP telemetry buffer
2. Enabling RF transmission
3. Capturing the transmitted signal with a calibrated receiving antenna
4. Demodulating and decoding the received data
5. Comparing against the original pattern

**Accept Criteria**: Zero bit errors in a 1 Mbit data sequence.

## Power Management Functional Test

### Regulator and Sequencer Test

| Test | Condition | Expected Result |
|------|-----------|-----------------|
| Cold Start | Power-on from 0V | Output reaches regulation within 500 us |
| Input Range | VDD from 1.6V to 2.0V | All outputs within regulation |
| Load Step | 0 to 1 mA step | Recovery within 10 us, overshoot < 5% |
| Brown-Out | VDD drops below 1.5V | Reset asserted cleanly |
| Brown-Out Recovery | VDD returns above 1.6V | Clean release from reset |
| Power Mode 0 | Active mode | IDD = 5 mA typical |
| Power Mode 1 | Sleep mode | IDD = 50 uA typical |
| Power Mode 2 | Deep sleep | IDD = 5 uA typical |
| Mode Transition | Active to Sleep | Transition < 10 us |

### Current Consumption by Mode

| Mode | Description | Target | Max | Measurement |
|------|------------|--------|-----|-------------|
| Active | All blocks enabled | 5.0 mA | 8.0 mA | SMU at VDD |
| Amplifier Only | Analog front end | 0.5 mA | 0.8 mA | SMU at VDD |
| Stimulator Only | Current sources active | 1.0 mA | 2.0 mA | SMU at VDD |
| Telemetry Only | RF carrier on | 2.0 mA | 3.0 mA | SMU at VDD |
| Sleep | Core off, RAM retained | 50 uA | 100 uA | SMU at VDD |
| Deep Sleep | Everything off, wake on timer | 5 uA | 10 uA | SMU at VDD |

## Test Pattern Generation

### Vector File Format

The iPACE-CHIP functional test uses standardized vector formats:

**WaveGen Format for Analog Stimulus**:

```
# Analog Stimulus: Neural amplifier input
WAVEFORM neural_input
  TYPE SINE
  FREQ 1000
  AMP 0.0001
  OFFSET 0.9
  PHASE 0
END

# Digital Pattern: Processor boot sequence
VECTOR digital_boot
  CLK_PERIOD 1000 ns
  DATA_FORMAT HEX
  PIN_MAP RESET, SPI_CLK, SPI_MOSI, SPI_MISO, IRQ
  00000 0 00 0000 0000 0  ; Reset assert
  00000 0 00 0000 0000 0  ; Hold 100 us
  00001 0 00 0000 0000 0  ; Release reset
  00002 0 AA 0001 0000 0  ; Write SPI command
  ...
END
```

### Test Coverage Analysis

**Fault Coverage Model**:

| Test Category | Faults Targeted | Coverage Target |
|--------------|----------------|-----------------|
| Digital Logic | Stuck-at, transition | > 95% |
| Analog (DC) | Parametric shift | 100% CTQ parameters |
| Analog (AC) | Frequency response | All poles/zeros |
| Power | Regulator faults | All failure modes |
| Telemetry | Protocol errors | All frame formats |

## Data Logging and Traceability

### Per-Die Test Record

Every iPACE-CHIP die receives a unique test record:

```
Test Record Format:

Die ID:        IPACE-2025-W01-D1234-B0567
Wafer Lot:     W01
Wafer Number:  3 of 25
Die Position:  Row 12, Column 34
Bin:           1 (Ship)
Test Date:     2025-06-15
Test Program:  v2.3.1
Test Station:  TS-007

Parametric Results:
  VBG:      1.251 V    (PASS, Cpk=1.85)
  IBIAS:    9.8 uA     (PASS, Cpk=1.62)
  NOISE:    1.4 uVrms  (PASS, Cpk=1.95)
  STIM_CURR: 0.998 mA  (PASS, Cpk=2.10)
  ... (48 total measurements logged)

Functional Results:
  Digital Boot:  PASS (time: 47 us)
  SRAM Test:     PASS (0 errors, 524K bits)
  EEPROM Test:   PASS (100 cycles, 0 errors)
  Amp Response:  PASS (gain: 20.1 dB)
  Filter HPF:    PASS (cutoff: 310 Hz)
  Filter LPF:    PASS (cutoff: 6.8 kHz)
  ADC INL:       PASS (0.8 LSB)
  Stim Current:  PASS (0.998 mA, accuracy: 0.2%)
  Telemetry:     PASS (freq: 13.558 MHz, BER: 0)
  Power Modes:   PASS (all modes verified)

Decision: SHIP to assembly
Signature:  Automated (no manual override)
```

### Database Schema

| Field | Type | Description |
|-------|------|-------------|
| die_id | VARCHAR(32) | Unique die identifier |
| wafer_lot | VARCHAR(16) | Fab lot number |
| wafer_num | INT | Wafer sequence number |
| row | INT | Die row position |
| col | INT | Die column position |
| test_date | TIMESTAMP | Test execution time |
| test_program | VARCHAR(16) | Software version |
| test_station | VARCHAR(8) | Equipment identifier |
| bin_num | INT | Final bin assignment |
| param_data | JSONB | All parametric values |
| functional_data | JSONB | All functional results |
| test_duration | FLOAT | Total test time (seconds) |

## Summary

Functional wafer testing of the iPACE-CHIP verifies complete operational capability
across digital processing, analog signal acquisition, stimulation delivery, wireless
telemetry, and power management functions. The test methodology applies known input
stimuli and verifies expected output responses with defined tolerances, achieving
>95% fault coverage for digital logic and 100% coverage of critical analog parameters.
Comprehensive data logging enables full traceability from individual die through
finished device, supporting the iPACE-CHIP zero-defect manufacturing objective and
FDA traceability requirements for Class III implantable medical devices.

## References

1. JEDEC JESD35, "Procedure for Wafer-Level Testing of Thin-Film Dielectrics."
2. IEEE Std 1149.1, "Standard Test Access Port and Boundary Scan Architecture."
3. iPACE-CHIP Functional Test Specification, Internal Document, Rev 2.0.
4. A. Kuo, "Wafer-Level Functional Testing of Mixed-Signal ASICs," IEEE ITC, 2023.
5. iPACE-CHIP Test Program Source Code, Internal, Repository: test-fw-v2.3.1.
6. SEMI E10, "Equipment Reliability, Availability, and Maintainability."
7. 21 CFR 820, "Quality System Regulation," FDA.
