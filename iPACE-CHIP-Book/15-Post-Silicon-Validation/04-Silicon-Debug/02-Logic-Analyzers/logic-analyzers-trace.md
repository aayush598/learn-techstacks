# Logic Analyzers and Trace

## 15.14.1 Overview

Logic analyzers and trace tools are the primary instruments for observing digital signal behavior in the iPACE-CHIP during post-silicon validation. While JTAG provides register-level visibility and the on-chip trace buffer captures historical data, logic analyzers capture real-time signal activity at the board level with high temporal resolution. This chapter details the selection, configuration, and usage of logic analyzers and trace tools for debugging the iPACE-CHIP's digital interfaces, timing, and protocol behavior.

## 15.14.2 Logic Analyzer Selection

### Requirements for iPACE-CHIP Debug

```
Signal Characteristics:
  - JTAG clock: Up to 20 MHz
  - SPI clock: Up to 10 MHz
  - UART: 115200 baud
  - Pacing control: 1-10 kHz edges
  - Telemetry: 128 kHz carrier, 8 kbps data
  - Interrupts: 1-100 kHz edges

Required Logic Analyzer Specifications:
  - Channel count: >= 16 (for simultaneous capture of multiple buses)
  - Sample rate: >= 200 MSa/s (5x oversampling of fastest signal)
  - Memory depth: >= 32 Mpts (for long captures)
  - Bandwidth: >= 100 MHz (for signal fidelity)
  - Protocol decoders: JTAG, SPI, UART (built-in)
  - Trigger: Pattern, edge, protocol event
  - Voltage threshold: 0.8V - 2.5V (CMOS logic levels)
```

### Recommended Instruments

| Instrument | Channels | Sample Rate | Memory | Protocol Decoders |
|-----------|----------|-------------|--------|--------------------|
| Keysight 16862A | 34 | 2 GSa/s | 2 Mpts | Yes (JTAG, SPI, UART) |
| Saleae Logic Pro 16 | 16 | 500 MSa/s | 100 Mpts | Yes (via software) |
| Tektronix MSO64 | 16 | 5 GSa/s | 125 Mpts | Yes (built-in) |
| DSLogic Plus (open source) | 32 | 400 MSa/s | 256 Mpts | Via PulseView |

### Cost-Effective Solution

For most iPACE-CHIP debug tasks, the Saleae Logic Pro 16 provides adequate performance at lower cost:

```
Saleae Logic Pro 16 Specifications:
  Digital channels: 16
  Maximum sample rate: 500 MSa/s (1 channel), 100 MSa/s (16 channels)
  Input voltage: -20V to +20V
  Threshold: Configurable (1.2V default for 1.8V logic)
  Memory: 100 Mpts per channel
  Protocol analyzers: JTAG, SPI, UART, I2C, CAN (free software)
  Price: ~$1,500

  Limitations:
  - Maximum 100 MSa/s with all 16 channels
  - No hardware protocol decoding (software only)
  - Less trigger flexibility than high-end instruments
```

## 15.14.3 JTAG Trace Analysis

### JTAG Signal Capture

```
Objective: Capture complete JTAG transactions for protocol analysis

Setup:
  - TCK: Channel 0 (clock reference)
  - TMS: Channel 1 (state machine control)
  - TDI: Channel 2 (data to chip)
  - TDO: Channel 3 (data from chip)
  - nTRST: Channel 4 (optional, for reset observation)

Trigger Configuration:
  - Trigger on: Rising edge on nTRST (capture boot sequence)
  - Pre-trigger: 50% (capture events before and after trigger)
  - Sample rate: 100 MSa/s (5x TCK at 20 MHz)
```

### JTAG Protocol Decoding

```
Logic analyzer JTAG decode example:

Capture of ARM CoreSight IDCODE scan:

TCK: |_|~|_|~|_|~|_|~|_|~|_|~|_|~|_|~|_|~|_|~|_|~|_|~|_|~|_|~|_|~|_|~|_|~|_|~|_|~|_|~|_|~|_|~|
TMS: ___|~~~~|___|_________|~~~~~|___|_______________|~~~~~~|_____________________|~~~~|_______|~
TDI: ___|1|0|1|0|0|0|0|0|0|0|0|0|0|0|0|0|0|1|0|1|1|1|0|0|0|0|1|1|1|0|0|1|1|1
TDO: ___|0|1|1|1|0|0|0|0|0|1|1|1|0|1|1|1|0|0|0|1|0|0|0|1|1|1|0|0|0|1|0|1|1

Decoded:
  State: Run-Test/Idle -> Select-DR-Scan -> Capture-DR -> Shift-DR
  DR Length: 32 bits
  DR Value (TDO): 0x4BA00477 (ARM Cortex-M0+ IDCODE)
  State: Exit1-DR -> Update-DR -> Run-Test/Idle

  Time per transaction: 2.1 us (at 20 MHz TCK)
  Total captured: 128 JTAG transactions
```

### JTAG Timing Analysis

```
Objective: Verify JTAG timing margins

Setup:
  - Sample rate: 500 MSa/s (highest available)
  - Measure: TCK setup time, TCK hold time, TDO access time

JTAG Timing Measurements:
  Parameter              | Measured  | Limit     | Margin
  -----------------------|-----------|-----------|--------
  TCK high period        | 25.2 ns   | Min 20 ns | +5.2 ns
  TCK low period         | 24.8 ns   | Min 20 ns | +4.8 ns
  TCK-to-TMS setup       | 5.1 ns    | Min 5 ns  | +0.1 ns
  TCK-to-TDI setup       | 4.8 ns    | Min 5 ns  | -0.2 ns *
  TCK-to-TDO access      | 12.3 ns   | Max 25 ns | +12.7 ns
  TDI hold after TCK     | 2.1 ns    | Min 0 ns  | +2.1 ns
  TMS hold after TCK     | 1.8 ns    | Min 0 ns  | +1.8 ns

  * TCK-to-TDI setup is marginally below spec. This may cause
    errors at maximum JTAG clock (20 MHz). Recommend reducing
    JTAG clock to 18 MHz for reliable operation.

Eye Diagram (TCK):
  Setup margin: 4.8 ns (from measurement)
  Hold margin: 2.1 ns
  Total eye opening: 46.9 ns out of 50 ns period (93.8%)
```

## 15.14.4 SPI Bus Analysis

### SPI Protocol Decode

```
Objective: Capture and decode SPI flash programming sequence

Setup:
  - SCLK: Channel 0
  - MOSI: Channel 1 (data to flash)
  - MISO: Channel 2 (data from flash)
  - CS0: Channel 3 (chip select)
  - Sample rate: 100 MSa/s

SPI Configuration:
  - Mode: CPOL=0, CPHA=0 (SPI Mode 0)
  - Bit order: MSB first
  - Clock: 8 MHz
  - Word size: 8 bits
```

### SPI Flash Read Decode

```
Decoded SPI Flash Read Transaction:

CS0: ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
SCLK: _|~|_|~|_|~|_|~|_|~|_|~|_|~|_|~|_|~|_|~|_|~|_|~|_|~|_|~|_|~|_|~|_|~|_|~|_|~|_|~|_|~|_|~|_|~|
MOSI: |0x03|0x00|0x00|0x10|0x00|0x00|0x00|0x00|0x00|0x00|0x00|0x00|0x00|0x00|0x00|0x00
MISO: |xx|xx|xx|xx|xx|0x49|0x50|0x41|0x43|0x2D|0x43|0x48|0x49|0x50|0x00|0x01

Decoded Protocol:
  Command: Read Data (0x03)
  Address: 0x000010 (24-bit address)
  Data: "iPACE-CHIP\0\x01" (device ID string)
  
  Transaction time: 14.4 us (112 clocks at 8 MHz)
  CS assertion to first clock: 100 ns (meets flash spec)
```

### SPI Clock Integrity

```
Objective: Verify SPI clock signal integrity

Measurement: Eye diagram on SCLK at 8 MHz

Results:
  Rise time (10%-90%): 3.2 ns (limit: < 10 ns)
  Fall time (10%-90%): 2.8 ns (limit: < 10 ns)
  Overshoot: 8% of VDD_IO (limit: < 20%)
  Undershoot: 5% of VDD_IO (limit: < 20%)
  Duty cycle: 49.8% (limit: 45%-55%)
  Jitter (peak-to-peak): 1.2 ns (limit: < 2 ns)
  
  Clock quality is adequate for 8 MHz SPI operation.
  Maximum achievable SPI clock: 16 MHz (with 2x safety margin on jitter).
```

## 15.14.5 UART Analysis

### UART Frame Decode

```
Objective: Capture and decode UART debug output

Setup:
  - TXD: Channel 0
  - RXD: Channel 1
  - Baud rate: 115200
  - Sample rate: 1 MSa/s (9x oversampling for reliable decode)

UART Configuration:
  - Data bits: 8
  - Parity: None
  - Stop bits: 1
  - Flow control: None
```

### UART Boot Message Capture

```
Captured UART Output (decoded from logic analyzer):

Frame 1: "iPACE-CHIP Boot ROM v1.0\r\n"
Frame 2: "Chip ID: 0x49504143\r\n"
Frame 3: "SRAM: 16 KB OK\r\n"
Frame 4: "Flash: 256 KB OK\r\n"
Frame 5: "AFE: Initializing...\r\n"
Frame 6: "AFE: Ready\r\n"
Frame 7: "Telemetry: Initializing...\r\n"
Frame 8: "Telemetry: Ready\r\n"
Frame 9: "Entering diagnostic mode...\r\n"

Timing between frames:
  Frame 1 to Frame 2: 12 ms
  Frame 2 to Frame 3: 3 ms
  Frame 3 to Frame 4: 5 ms
  Frame 4 to Frame 5: 8 ms
  Frame 5 to Frame 6: 15 ms (AFE initialization time)
  Frame 6 to Frame 7: 3 ms
  Frame 7 to Frame 8: 25 ms (telemetry calibration time)
  Frame 8 to Frame 9: 2 ms

Total boot time: 73 ms (from first character to "Entering diagnostic mode")
```

### UART Baud Rate Accuracy

```
Objective: Verify UART baud rate accuracy

Measurement: Measure actual bit period from captured UART frames

Results:
  Nominal bit period: 8.681 us (115200 baud)
  Measured bit period: 8.679 us
  Baud rate error: 0.023% (well within 2% specification)
  
  Jitter measurement:
  - Peak-to-peak jitter: 45 ns (0.52% of bit period)
  - RMS jitter: 12 ns
  - Both well within specification for reliable UART communication
```

## 15.14.6 Pacing Output Analysis

### Pacing Pulse Timing Capture

```
Objective: Verify pacing pulse characteristics with high-resolution timing

Setup:
  - PACE_OUT: Channel 0 (pacing output)
  - PACE_EN: Channel 1 (pacing enable, internal signal via ObsMUX)
  - Sample rate: 500 MSa/s (for sub-ns timing accuracy)

Captured Pacing Pulse:

PACE_EN: _______________|~~~~~~~~~~~~~~~~~~~~~~~~~~|__________________
PACE_OUT: _______________|~~~~|__________________________|~~~~~~~~~~~~
                    |<-->|<-0.5ms->|                  |<--0.5ms--|
                    |  200ns  |                          |  Recovery
                    |  rise   |                          |  phase

Timing Measurements:
  Parameter                    | Measured   | Specification
  -----------------------------|------------|-------------
  Enable to output rise        | 185 ns     | < 500 ns
  Pulse width (50%-50%)        | 498.2 us   | 500 us +/- 5%
  Pulse amplitude (peak)       | 3.48V      | 3.5V +/- 10%
  Rise time (10%-90%)          | 142 ns     | < 500 ns
  Fall time (10%-90%)          | 98 ns      | < 500 ns
  Overshoot                    | 2.1%       | < 5%
  Recovery phase duration      | 4.98 ms    | 5.0 ms +/- 5%
  Recovery phase amplitude     | -345 mV    | -350 mV +/- 10%

  All parameters within specification.
```

### Multi-Channel Pacing Timing

```
Objective: Verify A-V timing relationship in DDD mode

Setup:
  - A_PACE: Channel 0 (atrial pacing output)
  - V_PACE: Channel 1 (ventricular pacing output)
  - A_SENSE: Channel 2 (atrial sensing, via ObsMUX)
  - V_SENSE: Channel 3 (ventricular sensing, via ObsMUX)
  - Sample rate: 100 MSa/s

Captured Sequence:
  A_SENSE: ___|~~~~|______________________________________________
  V_PACE:  _________________________|~~~~|________________________
                            |<-AV->|
                            |200 ms|

  Timing:
  A-sense to V-pace: 199.8 ms (AV delay specification: 200 ms)
  AV delay accuracy: -0.1% (within 5% specification)
  
  Additional measurement: A-pace to V-pace
  A_PACE: ___|~~~~|______________________________________________
  V_PACE: _________________________|~~~~|________________________
                            |<-AV->|
                            |200.2 ms|
  
  A-pace to V-pace: 200.2 ms (+0.1% accuracy)
```

## 15.14.7 Telemetry Signal Analysis

### Telemetry Waveform Capture

```
Objective: Capture telemetry RF waveform for modulation analysis

Setup:
  - RF coil output: Channel 0 (via coupling transformer)
  - Data_in: Channel 1 (modulating data)
  - Sample rate: 500 MSa/s (for RF carrier detail)

Captured Waveform:
  Data_in: ______|~~~~|________|~~~~|________|~~~~|____
  RF Out:  _____|~~~~~|________|~~~~~|________|~~~~~|___
           |<-ASK->|  |<-ASK->|  |<-ASK->|
           | mod on|  | mod on|  | mod on|

Modulation Measurements:
  Carrier frequency: 128.002 kHz (+0.002% error)
  Modulation depth: 98.5% (specification: > 90%)
  Modulation rise time: 2.1 us (specification: < 5 us)
  Modulation fall time: 1.8 us (specification: < 5 us)
  Carrier duty cycle: 50.1% (specification: 45%-55%)
```

### Telemetry Packet Capture

```
Captured Telemetry Data Packet:

  Preamble: 0x5555 (16 bits)
  Sync: 0xAA (8 bits)
  Device ID: 0x49504143 (32 bits)
  Command: 0x01 (8 bits)
  Data Length: 0x20 (8 bits)
  Data: [32 bytes of status data]
  CRC-16: 0xXB4A2 (16 bits)

  Total packet length: 328 bits
  Packet time at 8 kbps: 41 ms
  Inter-packet gap: 50 ms
  Packet rate: 11 packets/second
```

## 15.14.8 Advanced Trigger Techniques

### Pattern Trigger

```
Objective: Capture specific state machine transition

Trigger Pattern:
  CH0 (State[0]): 1
  CH1 (State[1]): 0
  CH2 (State[2]): 1
  Pattern: 101 = State 5 (PACING state)

  Trigger fires when state machine enters PACING state.
  Capture includes 100 pre-trigger samples and 1000 post-trigger samples.
```

### Complex Trigger

```
Objective: Capture the first pacing pulse after a mode switch

Trigger Sequence:
  1. First event: Pattern match on mode_switch signal (CH4: high)
  2. Wait: 100 ms (time for mode switch to complete)
  3. Second event: Rising edge on PACE_EN (CH5)
  4. Capture: 500 samples centered on PACE_EN edge

This trigger captures the first pacing pulse after a mode change,
which is critical for verifying smooth mode transition behavior.
```

### Serial Pattern Trigger

```
Objective: Trigger on specific UART command

Using serial protocol decoder as trigger source:
  - Decode UART on CH0 (115200 baud, 8N1)
  - Trigger on decoded string: "ERROR"
  - This triggers capture when the chip reports an error on UART

This technique is invaluable for capturing the exact moment an error
condition occurs, even if the error is rare or intermittent.
```

## 15.14.9 Long-Duration Captures

### Streaming Mode

```
Objective: Capture 1 hour of telemetry activity for reliability analysis

Setup:
  - Saleae Logic Pro 16 in streaming mode
  - Sample rate: 1 MSa/s (2 channels)
  - Duration: 1 hour
  - Total samples: 3.6 billion per channel

Post-Processing:
  - Python script analyzes captured data
  - Counts telemetry packets per minute
  - Identifies CRC errors
  - Measures inter-packet timing
  - Detects any anomalous patterns

Results:
  Total packets: 39,600 (11 packets/second * 3600 seconds)
  CRC errors: 0
  Packet rate variation: +/- 0.1% (very stable)
  Anomalous patterns: None detected
```

### Segmented Memory

```
Objective: Capture multiple short events over a long period

Setup:
  - Segmented memory mode
  - 1000 segments
  - 10,000 samples per segment
  - Trigger: Pacing pulse (once per second)
  
  Total capture time: 1000 seconds (16.7 minutes)
  Memory usage: 1000 * 10,000 * 2 channels * 4 bytes = 80 MB
  
  Each segment captures one pacing pulse with context.
  Useful for verifying consistent pacing behavior over time.
```

## 15.14.10 Signal Integrity Measurements

### Rise Time and Fall Time

```
Objective: Verify digital signal integrity on all interfaces

Measurement Setup:
  - 20x passive probe (1 pF input capacitance)
  - Ground spring (short ground lead for minimal inductance)
  - Scope bandwidth: 1 GHz

Results by Signal:
  Signal       | Rise (ns) | Fall (ns) | Overshoot | Status
  TCK (JTAG)  | 3.2       | 2.8       | 8%        | PASS
  TMS (JTAG)  | 3.5       | 3.1       | 6%        | PASS
  TDI (JTAG)  | 3.1       | 2.9       | 7%        | PASS
  TDO (JTAG)  | 4.2       | 3.8       | 5%        | PASS
  SCLK (SPI)  | 3.2       | 2.8       | 8%        | PASS
  MOSI (SPI)  | 3.5       | 3.2       | 6%        | PASS
  MISO (SPI)  | 4.0       | 3.5       | 5%        | PASS
  TXD (UART)  | 5.1       | 4.8       | 3%        | PASS
  PACE_OUT    | 142       | 98        | 2%        | PASS

All signals meet timing specifications for their respective interfaces.
```

## 15.14.11 Summary

Logic analyzers and trace tools provide essential real-time visibility into the iPACE-CHIP's digital behavior during post-silicon validation. By capturing and decoding JTAG, SPI, UART, and telemetry protocols, the validation team can verify correct protocol operation, measure timing accuracy, and debug complex multi-signal interactions. Advanced trigger techniques enable precise capture of rare events, while long-duration captures support reliability analysis. The combination of hardware logic analyzer capture with software protocol decoding provides a powerful and flexible debug platform that complements the on-chip debug features described in the Design for Debug chapter.
