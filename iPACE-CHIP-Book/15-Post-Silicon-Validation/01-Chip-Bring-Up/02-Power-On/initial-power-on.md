# Initial Power-On Procedure

## 15.2.1 Overview

The initial power-on of the iPACE-CHIP is the most critical and delicate moment in the post-silicon validation campaign. After months of design, simulation, and fabrication, this is the first time the silicon is energized and its behavior observed. A methodical, step-by-step approach is essential to avoid damaging the chip due to assembly errors, design flaws, or unexpected failure modes. This chapter details the complete power-on procedure, from pre-power checks through functional boot, covering every decision point and expected outcome.

## 15.2.2 Pre-Power-On Checklist

Before applying any power to the iPACE-CHIP, the following verification steps must be completed. Each step is a gate that must be passed before proceeding.

### Visual Inspection

The first and simplest check is a thorough visual inspection of the soldered chip on the test board. Using a stereo microscope at 10x-20x magnification, inspect:

- **Solder fillets** on all visible QFN perimeter pads. Each pad should show a smooth, concave fillet bridging the pad to the package lead.
- **Thermal pad voiding** by inspecting solder squeeze-out around the package edges. Excessive squeeze-out indicates proper wetting; no squeeze-out may indicate insufficient solder or voiding.
- **Solder bridges** between adjacent pads. Under the microscope, any bridge will appear as a metallic connection between pads. Even a single bridge can destroy the chip on power-up.
- **Package alignment** relative to the PCB footprint. The package should be centered within +/- 0.1 mm in both X and Y axes.
- **Board damage** from the soldering process. Check for lifted pads, delaminated traces, or charred solder mask.

### Resistance Measurements

Using a precision multimeter (6.5 digit or better), measure resistance between every pair of power and ground pins on the chip. These measurements serve as a sanity check that no shorts exist in the power delivery network.

```
Expected Measurements (power-off):
  VDD_ANA to GND:   50 kohm - 200 kohm (due to internal ESD structures)
  VDD_DIG to GND:   20 kohm - 100 kohm
  VDD_IO to GND:    30 kohm - 150 kohm
  VBAT to GND:      100 kohm - 500 kohm (charging circuit input impedance)

Unexpected Measurements:
  VDD_ANA to GND:   < 1 kohm  --> SUSPECT SHORT, do not power on
  Any VDD to GND:   < 10 ohm   --> DEAD SHORT, do not power on
  VBAT to any VDD:  < 100 ohm  --> Check LDO output path
```

### Continuity Verification

Verify that all signals are correctly routed from the chip pins to the board connectors by measuring continuity on key nets:

- JTAG signals (TCK, TMS, TDI, TDO) from chip to J8 header
- SPI signals (SCLK, MOSI, MISO, CS) from chip to J9 header
- UART TX/RX from chip to USB bridge IC
- Analog inputs from BNC connectors to chip AFE pins
- Pacing outputs from chip to BNC output connectors

### Power Supply Verification

Before connecting the power supplies to the board, verify the LDO outputs without the chip in the circuit (if socketed) or with the power enable signals held low:

| Rail | Target Voltage | Allowed Tolerance | Measured | Pass/Fail |
|------|---------------|-------------------|----------|-----------|
| VDD_ANA | 2.500 V | +/- 2% | ___ V | |
| VDD_DIG | 1.200 V | +/- 2% | ___ V | |
| VDD_IO | 1.800 V | +/- 2% | ___ V | |
| VDD_TELEM | 2.500 V | +/- 5% | ___ V | |

Also verify that the output noise on each rail is within specification:

| Rail | Noise Spec (RMS) | Measured | Pass/Fail |
|------|-----------------|----------|-----------|
| VDD_ANA | < 10 uV | ___ uV | |
| VDD_DIG | < 1 mV | ___ mV | |
| VDD_IO | < 100 uV | ___ uV | |

## 15.2.3 Power-On Sequence

### Step 1: Apply GND

Connect the board ground to the laboratory earth ground through a single-point connection. This establishes the common reference potential and provides a path for fault currents. Use a heavy-gauge wire (12 AWG or thicker) with minimal inductance.

### Step 2: Apply VDD_IO First

The I/O supply must be established first because the JTAG and debug interfaces operate on this domain. Applying VDD_IO before the other supplies ensures that the chip's I/O buffers are powered and the debug interface is accessible for monitoring the power-on sequence.

```
Action: Enable VDD_IO supply at 1.800 V
Monitor: I_VDD_IO current (expect < 1 mA quiescent)
Duration: Wait 100 ms for rail to settle
Check: VDD_IO voltage stable at 1.800 V +/- 2%
```

### Step 3: Apply VDD_DIG

Next, bring up the digital core supply. This rail powers the ARM Cortex-M0+ processor, the digital control logic, and the SRAM arrays.

```
Action: Enable VDD_DIG supply at 1.200 V
Monitor: I_VDD_DIG current (expect < 5 mA initially)
Duration: Wait 100 ms for rail to settle
Check: VDD_DIG voltage stable at 1.200 V +/- 2%
```

### Step 4: Apply VDD_ANA

The analog supply powers the sensing amplifiers, ADCs, DACs, and reference voltage generators. This rail must have the lowest noise of all supplies.

```
Action: Enable VDD_ANA supply at 2.500 V
Monitor: I_VDD_ANA current (expect < 2 mA initially)
Duration: Wait 100 ms for rail to settle
Check: VDD_ANA voltage stable at 2.500 V +/- 2%
```

### Step 5: Apply VDD_TELEM

The telemetry supply powers the RF front-end and telemetry modulator/demodulator.

```
Action: Enable VDD_TELEM supply at 2.500 V
Monitor: I_VDD_TELEM current (expect < 1 mA initially)
Duration: Wait 100 ms for rail to settle
Check: VDD_TELEM voltage stable at 2.500 V +/- 2%
```

### Step 6: Release nRESET

After all supplies are stable and within specification, release the chip from reset by deasserting the nRESET pin.

```
Action: Drive nRESET HIGH (1.8V)
Monitor: All supply currents for change
Duration: Wait 10 ms for boot sequence
Check: Current draw increases as logic begins operating
```

### Step 7: Verify Boot

The iPACE-CHIP boot sequence is indicated by activity on the UART debug port (115200 baud, 8N1). Within 50 ms of nRESET release, the boot ROM should transmit an identification string:

```
Expected output:
"iPACE-CHIP Boot ROM v1.0"
"Chip ID: 0x49504143"
"Entering diagnostic mode..."
```

If this output appears, the chip has successfully powered on and the digital core is functional.

## 15.2.4 Current Consumption Monitoring

Throughout the power-on sequence, continuous monitoring of all supply currents provides immediate feedback on the chip's health. The expected current profile during a successful power-on is:

### Power-Up Current Profile

```
Time (ms)  | VDD_IO (mA) | VDD_DIG (mA) | VDD_ANA (mA) | VDD_TELEM (mA)
-----------|-------------|---------------|---------------|----------------
0          | 0           | 0             | 0             | 0
0-10       | 0.5         | 0             | 0             | 0        (VDD_IO ramp)
10-100     | 0.3         | 0             | 0             | 0        (VDD_IO settled)
100-200    | 0.3         | 2.0           | 0             | 0        (VDD_DIG ramp)
200-300    | 0.3         | 1.5           | 0             | 0        (VDD_DIG settled)
300-400    | 0.3         | 1.5           | 1.5           | 0        (VDD_ANA ramp)
400-500    | 0.3         | 1.5           | 1.2           | 0        (VDD_ANA settled)
500-600    | 0.3         | 1.5           | 1.2           | 0.5      (VDD_TELEM ramp)
600-700    | 0.3         | 1.5           | 1.2           | 0.5      (VDD_TELEM settled)
700-710    | 0.3         | 3.0           | 1.8           | 0.5      (nRESET release)
710-800    | 0.3         | 5.0           | 2.0           | 0.5      (Boot sequence)
800+       | 0.3         | 2.5           | 1.5           | 0.5      (Steady state)
```

### Anomalous Current Signatures

Abnormal current patterns during power-on provide diagnostic information:

| Symptom | Likely Cause | Action |
|---------|-------------|--------|
| VDD_DIG > 50 mA immediately | Digital core short or latch-up | Remove power immediately |
| VDD_ANA > 20 mA immediately | Analog block latch-up | Check for ESD damage |
| All rails < 10 uA | Open bond wire or solder joint | Reball and resolder |
| VDD_DIG oscillating | PLL instability or clock issue | Check crystal/oscillator |
| Current increasing over time | Thermal runaway | Check junction temperature |
| Current pulsing periodically | Watchdog reset loop | Check boot ROM execution |

## 15.2.5 Latch-Up Prevention and Detection

Latch-up is the most dangerous failure mode during power-on. It occurs when parasitic thyristor structures in the CMOS substrate are triggered, creating a low-impedance path between VDD and GND. If not detected and addressed quickly, latch-up can permanently damage the chip.

### Prevention Measures

The iPACE-CHIP includes several design-level latch-up prevention features:

- **Guard rings** around all I/O cells
- **Well contacts** at regular intervals in the substrate
- **Current-limiting resistors** on all I/O pins
- **Power sequencing requirements** documented in the datasheet

During power-on, additional precautions include:

- Apply supplies in the specified order (VDD_IO, VDD_DIG, VDD_ANA, VDD_TELEM)
- Never exceed the absolute maximum voltage ratings
- Use current-limited power supplies (set current limit to 2x expected maximum)
- Monitor die temperature via the on-die temperature sensor

### Detection Circuit

The test board includes a dedicated latch-up detection circuit on each supply rail. The circuit monitors the voltage across the current sense resistor and triggers an alarm if the current exceeds a threshold for more than 1 ms:

```
Latch-up detection thresholds:
  VDD_ANA:  > 100 mA for > 1 ms  --> Emergency power-off
  VDD_DIG:  > 200 mA for > 1 ms  --> Emergency power-off
  VDD_IO:   > 50 mA for > 1 ms   --> Emergency power-off
  VDD_TELEM: > 100 mA for > 1 ms --> Emergency power-off
```

The emergency power-off is implemented using a fast-acting analog comparator that drives the LDO enable pins low through a hardware interlock, bypassing any software control. This ensures that latch-up is interrupted within 100 microseconds of detection.

## 15.2.6 JTAG Communication

Once the chip has powered on and the boot ROM has completed, the first interactive communication is typically through the JTAG interface. The JTAG TAP (Test Access Port) controller is active as soon as VDD_IO is applied, even before nRESET is released.

### JTAG Scan Chain Verification

```
Step 1: Connect JTAG adapter (ARM J-Link or equivalent)
Step 2: Set JTAG clock to 1 MHz (safe for initial communication)
Step 3: Execute IR scan with IDCODE instruction
Expected: IR length = 4 bits, IR value = 0x01 (IDCODE)
Step 4: Execute DR scan to read device ID
Expected: 0x4BA00477 (ARM Cortex-M0+ JTAG ID)
Step 5: Scan for additional TAPs in chain
Expected: iPACE-CHIP boundary scan TAP at position 2
```

### JTAG Chain Length

The iPACE-CHIP implements a JTAG chain with two TAPs:

1. **ARM Cortex-M0+ debug TAP** (IDCODE: 0x4BA00477)
2. **iPACE-CHIP boundary scan TAP** (IDCODE: 0x49504143)

The total IR length is 8 bits (4 bits per TAP). The DR length varies by instruction.

### Common JTAG Issues

| Problem | Symptom | Solution |
|---------|---------|----------|
| No JTAG response | IDCODE scan returns all 1s | Check VDD_IO, nRESET, TCK continuity |
| Wrong chain length | IR scan shows unexpected length | Check for solder bridges on JTAG pins |
| Intermittent communication | JTAG errors at higher clock | Reduce clock to 1 MHz, check signal integrity |
| Boundary scan TAP missing | Only one TAP detected | Check TDI/TDO daisy chain routing |

## 15.2.7 Register Map Verification

After establishing JTAG communication, the next step is to verify that the chip's internal register map is accessible and that critical registers contain expected default values.

### Essential Register Checks

```
Register Address | Register Name      | Expected Reset Value | Description
-----------------|--------------------|-----------------------|------------------
0x40000000       | CHIP_ID            | 0x49504143            | Chip identification
0x40000004       | CHIP_REV           | 0x00010000            | Revision A, version 0
0x40000008       | FIRMWARE_REV       | 0x00010002            | Boot ROM v1.2
0x40000010       | CLK_CTRL           | 0x00000001            | Internal osc enabled
0x40000014       | CLK_STATUS         | 0x00000003            | Osc stable, PLL locked
0x40000020       | PWR_CTRL           | 0x0000000F            | All power domains on
0x40000024       | PWR_STATUS         | 0x000000FF            | All rails good
0x40000030       | IO_CTRL            | 0x00000000            | All GPIO inputs
0x40000040       | AFE_CTRL           | 0x00000000            | AFE powered down
0x40000050       | DIG_CTRL           | 0x00000000            | Digital blocks reset
0x40000060       | TELEM_CTRL         | 0x00000000            | Telemetry powered down
0x40000070       | WDT_CTRL           | 0x00000001            | Watchdog enabled
0x40000074       | WDT_FEED           | 0x00000000            | Write-only feed reg
0x40000100       | SRAM_SIZE          | 0x00004000            | 16 KB SRAM
0x40000104       | FLASH_SIZE         | 0x00040000            | 256 KB Flash
```

### Register Read/Write Test

After verifying reset values, perform basic read/write operations on read-write registers:

```
Test Procedure:
1. Read CLK_CTRL (expect 0x00000001)
2. Write 0x00000003 to CLK_CTRL (enable both osc and PLL)
3. Read CLK_CTRL (expect 0x00000003)
4. Write 0x00000001 to CLK_CTRL (restore original)
5. Read CLK_CTRL (expect 0x00000001)
6. Verify CLK_STATUS reflects PLL lock within 10 ms
```

## 15.2.8 SRAM Integrity Check

The iPACE-CHIP includes 16 KB of on-chip SRAM organized as 4 KB banks. After power-on, each bank must be verified for data integrity.

### March Test Algorithm

The standard March C- algorithm is used for SRAM testing:

```
March C- Algorithm (for N-word memory):
  1. (Initialization): Write 0 to all cells
  2. (Up-read-write): For i = 0 to N-1:
       Read(i), expect 0; Write 1 to i
  3. (Up-read-write): For i = 0 to N-1:
       Read(i), expect 1; Write 0 to i
  4. (Down-read-write): For i = N-1 to 0:
       Read(i), expect 0; Write 1 to i
  5. (Down-read-write): For i = N-1 to 0:
       Read(i), expect 1; Write 0 to i
  6. (Final check): For i = 0 to N-1:
       Read(i), expect 0
```

This algorithm detects all single-bit stuck-at faults, transition faults, and coupling faults with O(N) complexity.

### SRAM Test Results

```
Bank | Address Range      | Size  | March C- Result | Time (ms)
-----|--------------------|-------|-----------------|----------
0    | 0x20000000-0x20000FFF | 4 KB | PASS            | 2.1
1    | 0x20001000-0x20001FFF | 4 KB | PASS            | 2.1
2    | 0x20002000-0x20002FFF | 4 KB | PASS            | 2.1
3    | 0x20003000-0x20003FFF | 4 KB | PASS            | 2.1
Total |                    | 16 KB | PASS            | 8.4
```

## 15.2.9 Clock System Verification

The iPACE-CHIP includes two clock sources:
- **Internal 32 kHz RC oscillator** (low accuracy, used for initial boot)
- **External 32.768 kHz crystal oscillator** (high accuracy, used for timing)

### Internal Oscillator Check

```
Step 1: Read CLK_STATUS register (internal osc should be running)
Step 2: Route internal osc to MCO (microcontroller clock output) pin
Step 3: Measure frequency on MCO with frequency counter
Expected: 32,768 Hz +/- 10% (RC oscillator tolerance)
Step 4: Measure frequency stability over 60 seconds
Expected: Drift < 1% over temperature range
```

### External Crystal Oscillator Check

```
Step 1: Connect 32.768 kHz crystal to XTAL_IN/XTAL_OUT pins
Step 2: Enable external oscillator in CLK_CTRL register
Step 3: Wait for PLL lock (poll CLK_STATUS register, expect bit 1 = 1)
Step 4: Measure frequency on MCO pin
Expected: 32,768 Hz +/- 20 ppm (crystal tolerance)
Step 5: Measure startup time from oscillator enable to stable clock
Expected: < 500 ms for 32.768 kHz crystal
```

## 15.2.10 Watchdog Timer Verification

The iPACE-CHIP includes a watchdog timer that must be verified during power-on. The watchdog is a safety mechanism that resets the chip if the firmware fails to service it within the expected time window.

### Watchdog Test Sequence

```
Step 1: Read WDT_CTRL register (should be enabled at reset)
Step 2: Read WDT_STATUS register (should show countdown from initial value)
Step 3: Write to WDT_FEED register to kick the watchdog
Step 4: Verify WDT_STATUS counter resets to initial value
Step 5: Disable watchdog by clearing WDT_CTRL.ENABLE bit
Step 6: Verify counter stops decrementing
Step 7: Re-enable watchdog
Step 8: Do not service watchdog for 2x timeout period
Step 9: Verify chip resets (check boot ROM message on UART)
```

## 15.2.11 Summary

The initial power-on procedure for the iPACE-CHIP is a carefully orchestrated sequence of checks and measurements designed to verify silicon integrity before committing to extensive characterization. Each step provides specific diagnostic information that either confirms correct operation or identifies the root cause of a problem. By following this procedure rigorously, the validation team can quickly isolate issues to specific subsystems and avoid the costly mistake of powering a damaged chip at full current for an extended period. The power-on data also serves as the baseline for all subsequent characterization measurements, providing reference current signatures and register values against which production parts will be compared.
