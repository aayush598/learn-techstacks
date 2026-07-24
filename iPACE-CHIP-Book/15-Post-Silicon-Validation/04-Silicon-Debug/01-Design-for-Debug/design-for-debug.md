# Design for Debug

## 15.13.1 Overview

Design for Debug (DfD) is the practice of embedding debug and observability features directly into the silicon during the design phase. For the iPACE-CHIP, DfD is not a luxury but a necessity. Once the chip is fabricated and packaged, the only way to observe internal signals is through the debug features that were deliberately included in the RTL. Poor DfD decisions made during design cannot be remedied after tapeout; they can only be corrected through an expensive silicon respin. This chapter describes the DfD features implemented in the iPACE-CHIP, their rationale, and how they are used during post-silicon validation.

## 15.13.2 DfD Philosophy

### The Observability-Control Trade-off

```
Design Tension:
  - More debug features = more observability = easier debug
  - More debug features = more area, power, and complexity
  - More debug features = more potential security vulnerabilities
  - More debug features = more potential reliability concerns

iPACE-CHIP Approach:
  - Maximum debug capability during validation
  - Selective disable for production (security)
  - All debug features must be non-intrusive during normal operation
  - Debug features must not impact reliability or safety
```

### DfD Requirements

```
Requirement                              | Priority | Justification
-----------------------------------------|----------|------------------
JTAG/SWD debug interface                 | High     | Universal debug access
On-chip trace buffer                     | High     | Post-mortem analysis
Boundary scan (IEEE 1149.1)              | High     | Interconnect test
Built-In Self Test (BIST)               | High     | Manufacturing test
Internal scan chain                      | High     | Fault detection
Programmable observation MUX             | High     | Signal visibility
Performance counters                     | Medium   | System optimization
Watchdog timer                           | High     | Safety requirement
On-chip temperature sensor               | Medium   | Thermal monitoring
On-chip voltage sensor                    | Medium   | Brownout detection
Clock monitoring                         | Medium   | Clock integrity
Error logging (non-volatile)             | High     | Field failure analysis
Real-time telemetry (internal signals)   | Medium   | Remote debug
```

## 15.13.3 JTAG/SWD Interface

### Debug Access Port Architecture

```
iPACE-CHIP Debug Port Architecture:

                    Host PC
                      |
                 [JTAG Adapter]
                      |
              TCK  TMS  TDI  TDO  nTRST
                      |
              +-------+-------+
              |   JTAG TAP    |
              |   Controller  |
              +-------+-------+
                      |
              +-------+-------+
              |   DAP (Debug  |
              | Access Port)  |
              +-------+-------+
                      |
            +---------+---------+
            |                   |
     +------+------+    +------+------+
     |  AHB-AP     |    |  APB-AP     |
     | (Memory/Reg)|    | (Peripheral)|
     +------+------+    +------+------+
            |                   |
     +------+------+    +------+------+
     |  ARM Cortex |    |  iPACE-CHIP |
     |   M0+ Core  |    |  Custom     |
     +------+------+    |  Debug Regs |
            |            +------+------+
     +------+------+           |
     | CPU Debug   |    +------+------+
     | Features    |    |  BIST, Scan |
     | (FPB, DWT)  |    |  Trace, MUX |
     +-------------+    +-------------+
```

### JTAG Pin Allocation

```
JTAG Pin Assignment (directly bonded to package):

Pin | Package Pin | Function      | Description
----|-------------|---------------|---------------------------
TCK | 1           | Test Clock    | JTAG clock input (max 20 MHz)
TMS | 2           | Test Mode Sel | JTAG state machine control
TDI | 3           | Test Data In  | Serial data input
TDO | 4           | Test Data Out | Serial data output
nTRST| 5          | Test Reset    | Asynchronous TAP reset

Protection:
  - ESD protection on all JTAG pins (2 kV HBM)
  - 50-ohm series termination on TCK
  - Internal pull-ups on TMS, TDI, nTRST
  - Schmitt trigger on TCK for noise immunity
```

### SWD Alternative

```
The iPACE-CHIP also supports SWD (Serial Wire Debug) as an alternative
to JTAG. SWD uses only 2 pins (SWCLK, SWDIO) and is compatible with
ARM CoreSight architecture.

SWD Pin Mapping:
  SWCLK = TCK (shared)
  SWDIO = TMS (shared)

The TAP controller automatically detects SWD vs. JTAG mode based on
the initial protocol sequence on the TMS/SWDIO pin.
```

## 15.13.4 On-Chip Trace Buffer

### ETB (Embedded Trace Buffer) Implementation

```
iPACE-CHIP ETB Configuration:

Storage:
  - 512 entries x 32 bits = 2 KB SRAM
  - Circular buffer mode (oldest entries overwritten)
  - Trigger-controlled capture

Trigger Sources (selectable):
  - CPU halt event
  - Breakpoint hit (FPB comparator 0-3)
  - Watchpoint hit (DWT comparator 0-3)
  - External trigger (pin input)
  - Software trigger (write to debug register)
  - Error condition (ECC error, brownout, watchdog)

Capture Modes:
  - Instruction trace: 32-bit PC address per entry
  - Data trace: Address + data for load/store operations
  - Mixed trace: Interleaved instruction and data
```

### Trace Buffer Usage Example

```
Scenario: Debugging a watchdog reset

Step 1: Configure ETB
  - Set trigger: Watchdog reset event
  - Set mode: Instruction trace (capture PC addresses)
  - Set depth: Full 512 entries

Step 2: Allow system to run normally
  - Watchdog eventually resets chip (bug in firmware)

Step 3: Read ETB after reset
  - ETB contains last 512 PC values before reset

Step 4: Analyze trace
  PC Sequence:
  0x08001000: LDR R0, [R1]       ; Load sensor status
  0x08001002: TST R0, #0x01      ; Check ready bit
  0x08001004: BEQ 0x08001000     ; Loop if not ready
  0x08001006: LDR R0, [R1]       ; Re-read (stuck)
  0x08001008: TST R0, #0x01
  0x0800100A: BEQ 0x08001006     ; Infinite loop!
  
  Root cause: Sensor never sets ready bit (hardware fault or
  missing initialization). Firmware loops forever, watchdog resets.
```

## 15.13.5 Built-In Self Test (BIST)

### Memory BIST

```
iPACE-CHIP MBIST Architecture:

Memory Banks:
  - SRAM Bank 0: 4 KB (0x20000000)
  - SRAM Bank 1: 4 KB (0x20001000)
  - SRAM Bank 2: 4 KB (0x20002000)
  - SRAM Bank 3: 4 KB (0x20003000)
  - Flash: 256 KB (0x00000000)

MBIST Controller:
  - Dedicated hardware state machine (no firmware needed)
  - Runs March C- algorithm at full speed
  - Reports pass/fail per bank
  - Reports failing address and failing bit
  - Execution time: 16 ms for all SRAM banks

MBIST Register Interface:
  Address: 0x40008000
  Control:  Start test, select bank, reset
  Status:   Test complete, pass/fail, error count
  Error:    Failing address, failing bit position
```

### Logic BIST

```
iPACE-CHIP LBIST Architecture:

LBIST Controller:
  - Pseudo-Random Pattern Generator (PRPG)
  - Multiple Input Signature Register (MISR)
  - Compactor for scan chain output
  - Dedicated test controller

Test Modes:
  - Full scan: All flip-flops in scan chain (~45,000 FFs)
  - Partial scan: Selective scan chains for faster test
  - At-speed: Scan shift at full clock speed
  - Slow-speed: Scan shift at reduced clock for timing margin

Coverage:
  - Stuck-at fault coverage: > 98%
  - Transition fault coverage: > 95%
  - Test time: ~2 seconds for full LBIST
  
  Register Interface:
  Address: 0x40008100
  Control: Start LBIST, select mode
  Status: Complete, pass/fail, fault count
  Error: Failing scan chain, failing flip-flop index
```

## 15.13.6 Observation Multiplexer (ObsMUX)

### Signal Observation Architecture

The iPACE-CHIP includes a programmable observation MUX that routes internal signals to external test points:

```
ObsMUX Configuration:

Number of output channels: 16
Inputs per channel: 64 (selectable via 6-bit MUX select)
Total observable signals: 16 x 64 = 1024 signals

Observable Signal Categories:
  - CPU buses (AHB-AP, APB-AP): 128 signals
  - AFE digital control: 64 signals
  - Pacing state machine: 32 signals
  - Telemetry protocol: 48 signals
  - Power management: 32 signals
  - Clock tree: 16 signals
  - Interrupt signals: 16 signals
  - Memory interface: 64 signals
  - SPI bus: 16 signals
  - UART: 8 signals
  - Safety monitors: 32 signals
  - BIST status: 16 signals
  - Reserved: 560 signals (for future use)
```

### ObsMUX Control Register

```
Register Address Map:

Offset | Register       | R/W | Description
-------|----------------|-----|-----------------------------------
0x00   | OBSMUX_CTRL    | RW  | Enable, clock divider, mode
0x04   | CH0_SEL        | RW  | Channel 0 MUX select (6 bits)
0x08   | CH1_SEL        | RW  | Channel 1 MUX select (6 bits)
...    | ...            | ... | ...
0x3C   | CH15_SEL       | RW  | Channel 15 MUX select (6 bits)
0x40   | CH0_DATA       | R   | Channel 0 captured data (32 bits)
...    | ...            | ... | ...
0x7C   | CH15_DATA      | R   | Channel 15 captured data (32 bits)
0x80   | TRIGGER_CTRL   | RW  | Trigger configuration
0x84   | TRIGGER_PATTERN| RW  | Trigger match pattern
0x88   | TRIGGER_MASK   | RW  | Trigger enable mask
```

### Usage Example

```
Objective: Observe pacing state machine transitions

Procedure:
  1. Write CH0_SEL = 0x05 (pacing state machine group)
  2. Write CH1_SEL = 0x08 (pacing timing counter)
  3. Write CH2_SEL = 0x0F (pacing output enable)
  4. Write OBSMUX_CTRL = 0x0007 (enable channels 0, 1, 2)
  5. Connect oscilloscope to ObsMUX output pins
  6. Observe state transitions in real-time

Captured Data:
  Channel 0 (State): Cycles through IDLE -> SENSING -> PACING -> REFRAC -> IDLE
  Channel 1 (Timer): Decrements from 1000 to 0 (1 ms pacing interval)
  Channel 2 (Output): High during PACING state (0.5 ms pulse width)
```

## 15.13.7 Performance Counters

### Counter Resources

```
iPACE-CHIP Performance Counters:

ARM Cortex-M0+ Built-in:
  - DWT_CYCCNT: 32-bit cycle counter
  - DWT_CPICNT: CPI (cycles per instruction) counter
  - DWT_EXCCNT: External cycle counter
  - DWT_SLEEPCNT: Sleep cycle counter
  - DWT_LSUCNT: Load/store unit counter
  - DWT_FOLDCNT: Folded instruction counter
  - DWT_PCSR: Program counter sample register

Custom iPACE-CHIP Counters (8 counters):
  - PCNT_AFE_CLK: AFE clock cycles
  - PCNT_ADC_CONV: ADC conversion count
  - PCNT_PACE_PULSE: Pacing pulse count
  - PCNT_SENSE_EVENT: Sensing event count
  - PCNT_TELEM_TX: Telemetry TX byte count
  - PCNT_TELEM_RX: Telemetry RX byte count
  - PCNT_INT: Interrupt count (per source)
  - PCNT_BUS_STALL: AHB bus stall cycle count
```

### Performance Counter Usage

```
Example: Measuring ADC Conversion Time

Procedure:
  1. Write PCNT_AFE_CLK = 0 (reset counter)
  2. Write PCNT_ADC_CONV = 0 (reset counter)
  3. Start ADC conversion
  4. Wait for conversion complete
  5. Read PCNT_AFE_CLK (AFE clock cycles during conversion)
  6. Read PCNT_ADC_CONV (should be 1)

Results:
  PCNT_AFE_CLK = 380 (AFE clock at 4 MHz: 380/4MHz = 95 us)
  This matches the expected 95 us ADC conversion time.

Example: Measuring Interrupt Latency

Procedure:
  1. Configure DWT_CYCCNT (cycle counter)
  2. Configure DWT_EXCCNT (external trigger counter)
  3. Set external trigger on IRQ pin (rising edge)
  4. Start cycle counter
  5. Apply interrupt
  6. Read cycle count when ISR first instruction executes

Results:
  DWT_CYCCNT at ISR entry: 42 cycles
  At 4 MHz: 42/4MHz = 10.5 us interrupt latency
  This matches the expected < 15 us latency for Cortex-M0+.
```

## 15.13.8 Error Logging

### Non-Volatile Error Log

```
iPACE-CHIP Error Log Structure:

Location: Dedicated Flash sector (Sector 63, last 4 KB)
Size: 4096 bytes
Format: Circular log with timestamps

Log Entry Format (16 bytes per entry):
  Byte 0-1:   Error code (16-bit)
  Byte 2-3:   Error flags (16-bit)
  Byte 4-7:   Timestamp (32-bit, RTC seconds since boot)
  Byte 8-11:  Context data (32-bit, error-specific)
  Byte 12-15: CRC-32 (error detection)

Maximum entries: 256 (4096 / 16)
Oldest entries overwritten when log is full.

Error Codes:
  0x0001: ECC single-bit correction (Flash)
  0x0002: ECC double-bit error (Flash)
  0x0003: ECC single-bit correction (SRAM)
  0x0004: ECC double-bit error (SRAM)
  0x0005: Watchdog reset
  0x0006: Brownout reset
  0x0007: Temperature alarm
  0x0008: Lead impedance fault
  0x0009: Pacing capture loss
  0x000A: Telemetry CRC error
  0x000B: SPI communication error
  0x000C: ADC overflow
  0x000D: Clock switch failure
  0x000E: Power domain fault
  0x000F: Safety monitor violation
```

### Error Log Analysis

```
Example: Analyzing error log after field return

Procedure:
  1. Connect to device via telemetry
  2. Read error log sector via debug command
  3. Parse and decode entries
  4. Generate report

Sample Error Log:
  Entry | Time       | Code | Context | Description
  1     | 0x00012345 | 0x0001| 0x0000  | Flash ECC correction (address 0x00012340)
  2     | 0x00012346 | 0x0001| 0x0004  | Flash ECC correction (address 0x00012344)
  3     | 0x00056789 | 0x0008| 0x0001  | Lead impedance fault (channel 1)
  4     | 0x0009ABCD | 0x0009| 0x0002  | Capture loss (channel 2)
  5     | 0x00123456 | 0x0006| 0x0000  | Brownout reset (VDD_DIG < 0.95V)

Analysis:
  - Two Flash ECC corrections early in life (cosmic ray or weak cell)
  - Lead impedance fault (possible connector issue)
  - Capture loss (threshold shift, compensated by autocapture)
  - Brownout (possibly during battery replacement)
  - No systematic failures detected
```

## 15.13.9 Scan Chain Design

### Scan Chain Architecture

```
iPACE-CHIP Scan Chain Configuration:

Total flip-flops: ~45,000
Scan chains: 8 (for reduced shift time)
Flip-flops per chain: ~5,625 average

Scan Chain Allocation:
  Chain 0: ARM Cortex-M0+ core           (7,200 FFs)
  Chain 1: AFE digital control           (5,100 FFs)
  Chain 2: Pacing state machine + timing (4,800 FFs)
  Chain 3: Telemetry protocol engine     (3,900 FFs)
  Chain 4: SPI/UART interfaces           (3,200 FFs)
  Chain 5: Power management logic        (4,100 FFs)
  Chain 6: Safety monitors + BIST        (5,400 FFs)
  Chain 7: Clock management + misc       (11,300 FFs)

Scan Interface:
  - Shift clock: Maximum 10 MHz
  - Total shift time per pattern: 7,200 / 10 MHz = 0.72 ms (worst chain)
  - Capture cycle: 1 clock at functional speed
  - Full pattern set (~5000 patterns): 3.6 seconds
```

### Scan Compression

```
iPACE-CHIP Scan Compression:

Compressor: 128:1 on-chip compressor
Decompressor: 128:1 on-chip decompressor

Effect:
  - Input stimuli: 128 scan chains compressed to 1 input
  - Output response: 128 scan chains compressed from 1 output
  - Shift time reduced by 128x
  
  Uncompressed shift time: 0.72 ms per pattern
  Compressed shift time: 0.72 ms / 128 = 5.6 us per pattern
  
  Full pattern set with compression: 5.6 us * 5000 = 28 ms
  (vs. 3.6 seconds without compression)
```

## 15.13.10 Debug Pin Allocation

### Package Pin Budget for Debug

```
iPACE-CHIP 64-pin QFN Pin Allocation:

Total pins: 64
Debug-dedicated pins: 5 (JTAG/SWD)
Debug-shared pins: 3 (ObsMUX outputs, shared with GPIO)

Pin Category           | Count | Percentage
-----------------------|-------|----------
Power/Ground           | 12    | 18.8%
Analog I/O             | 8     | 12.5%
Pacing I/O             | 4     | 6.3%
Telemetry I/O          | 2     | 3.1%
JTAG/SWD (dedicated)   | 5     | 7.8%
ObsMUX output (shared) | 3     | 4.7%
SPI bus                | 4     | 6.3%
UART                   | 2     | 3.1%
GPIO/Interrupt         | 8     | 12.5%
Clock input            | 2     | 3.1%
Miscellaneous          | 4     | 6.3%
Reserved               | 12    | 18.8%

Debug overhead: 8 pins dedicated/shared = 12.5% of package
This is within the 15% budget allocated for debug features.
```

## 15.13.11 Security Considerations

### Debug Lock Mechanism

```
iPACE-CHIP Debug Security:

Security Levels:
  Level 0: Full debug access (default for validation)
  Level 1: JTAG disabled, boundary scan only
  Level 2: All debug disabled (production mode)

Lock Mechanism:
  - Write 0x00000000 to DEBUG_LOCK register (0x40000080)
  - Once written, cannot be unlocked without chip erase
  - Lock status readable via JTAG IDCODE scan
  - Lock survives power cycle and reset

Production Flow:
  1. Full debug access during validation (Level 0)
  2. After validation, lock debug to Level 1 (Level 1)
  3. Before shipping, lock debug to Level 2 (Level 2)
  4. Level 2 prevents any debug access (secure for implant)
```

### Debug Trace Sanitization

```
Objective: Ensure debug trace does not expose sensitive patient data

The iPACE-CHIP trace buffer captures PC addresses, not data values.
Sensitive information (patient ID, diagnostic data) is never stored
in the trace buffer. The trace buffer is cleared on power-up and
on debug lock transition to Level 2.
```

## 15.13.12 Summary

The Design for Debug implementation in the iPACE-CHIP provides comprehensive observability into the chip's internal operation while maintaining the security and reliability requirements for an implantable medical device. The JTAG/SWD interface provides standard debug access, the trace buffer enables post-mortem analysis, the observation MUX offers real-time signal visibility, and the BIST infrastructure supports manufacturing test. The debug lock mechanism ensures that all debug features are securely disabled before the device is shipped for clinical use. This DfD approach has been instrumental in the efficient debugging and validation of the iPACE-CHIP silicon.
