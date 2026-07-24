# JTAG Boundary Scan

## Overview

The IEEE 1149.1 Test Access Port (TAP) and Boundary-Scan architecture provides the iPACE-CHIP with a standardized interface for board-level interconnect testing, in-system programming, and internal scan chain access. For a medical device pacemaker controller, the JTAG interface serves as the primary debug, production test, and field diagnostic gateway while maintaining strict safety controls to prevent inadvertent activation during patient-connected operation.

---

## 1. IEEE 1149.1 Architecture

### 1.1 TAP Interface

The iPACE-CHIP implements a 4-pin TAP interface (5-pin with optional TRST*):

```
┌─────────────────────────────────────────┐
│                 iPACE-CHIP               │
│                                          │
│  TCK ──►┌──────────────────────────┐    │
│  TMS ──►│                          │    │
│  TDI ──►│     TAP Controller       │    │
│  TDO ◄──│     (16-state FSM)       │    │
│ TRST*──►│                          │    │
│          └──────────┬───────────────┘    │
│                     │                    │
│          ┌──────────┴───────────────┐    │
│          │    Instruction Register   │    │
│          │    (8-bit for iPACE)      │    │
│          └──────────┬───────────────┘    │
│                     │                    │
│     ┌───────────────┼────────────────┐   │
│     │               │                │   │
│  ┌──┴───┐     ┌─────┴─────┐    ┌────┴─┐ │
│  │Bypass│     │ Boundary  │    │      │ │
│  │ Reg  │     │ Scan Cell │    │ ...  │ │
│  │(1-b) │     │ Array     │    │      │ │
│  └──────┘     └───────────┘    └──────┘ │
└─────────────────────────────────────────┘
```

**TAP Signal Definitions:**

| Signal | Direction | Description |
|--------|-----------|-------------|
| TCK | Input | Test clock (independent of functional clocks) |
| TMS | Input | Test mode select (controls TAP FSM transitions) |
| TDI | Input | Test data input (serial data shifted into IR/DR) |
| TDO | Output | Test data output (serial data shifted out of DR) |
| TRST* | Input | Test reset (active low, optional per IEEE 1149.1) |

### 1.2 TAP Controller State Machine

The 16-state FSM follows the IEEE 1149.1 standard exactly:

```
                        ┌──────────┐
              TMS=1     │Test-Logic│     TMS=0
         ┌─────────────│  Reset   │─────────────┐
         │              └──────────┘              │
         │ TMS=0                                   │
         ▼                                         ▼
    ┌─────────┐    TMS=1    ┌──────────┐    TMS=0  ┌─────────┐
    │ Run-    │────────────►│ Select-  │──────────►│Select-  │
    │ Test/   │             │ Test-IR  │           │ Test-DR │
    │ Idle    │             └────┬─────┘           └────┬────┘
    └────┬────┘                  │                      │
         │ TMS=0                 │ TMS=1                │ TMS=1
         ▼                       ▼                      ▼
    ┌─────────┐           ┌──────────┐           ┌──────────┐
    │Select-  │    TMS=0  │Capture-IR│           │Capture-DR│
    │Test-DR  │◄──────────│          │           │          │
    └─────────┘           └────┬─────┘           └────┬─────┘
                               │ TMS=0                │ TMS=0
                               ▼                      ▼
                          ┌──────────┐           ┌──────────┐
                          │Shift-IR  │           │Shift-DR  │
                          └────┬─────┘           └────┬─────┘
                               │ TMS=1                │ TMS=1
                               ▼                      ▼
                          ┌──────────┐           ┌──────────┐
                          │Exit1-IR  │           │Exit1-DR  │
                          └────┬─────┘           └────┬─────┘
                               │ TMS=1                │ TMS=1
                               ▼                      ▼
                          ┌──────────┐           ┌──────────┐
                          │Pause-IR  │           │Pause-DR  │
                          └────┬─────┘           └────┬─────┘
                               │ TMS=0                │ TMS=0
                               ▼                      ▼
                          ┌──────────┐           ┌──────────┐
                          │Exit2-IR  │           │Exit2-DR  │
                          └────┬─────┘           └────┬─────┘
                               │ TMS=1                │ TMS=1
                               ▼                      ▼
                          ┌──────────┐           ┌──────────┐
                          │Update-IR │           │Update-DR │
                          └──────────┘           └──────────┘
```

### 1.3 iPACE-CHIP TAP Specifications

| Parameter | Value | Notes |
|-----------|-------|-------|
| TCK max frequency | 20 MHz | Limited by package pin inductance |
| TAP instruction width | 8 bits | Supports 256 instructions |
| IR capture value | 0x01 | Device ID LSB (fixed) |
| Boundary cells | 248 | All I/O pads + test pads |
| Device ID | Custom | Per IEEE 1149.1 requirement |
| TRST* support | Yes | Asynchronous TAP reset |

---

## 2. Boundary Scan Cell Implementation

### 2.1 Boundary Cell Architecture

Each I/O pad on the iPACE-CHIP is equipped with a boundary scan cell (BSC). The BSC captures pad input data and controls pad output data during boundary scan operations:

```
                    Functional I/O Path
                    ────────────────────
    Pad Input ────► ┌────────┐ ────────► Core Logic Input
                    │  BSC   │
    Core Logic ────►│        │ ────────► Pad Output
    Output         └───┬────┘
                       │
              TDI ────►│──────► TDO
              (shift)
              Clock ───│
              Update ──│
              Mode ────│
```

**BSC Operating Modes:**

| Mode | Function | Description |
|------|----------|-------------|
| Normal | Transparent | BSC passes data transparently between pad and core |
| Capture | Sample | BSC captures pad input value on Capture-DR |
| Shift | Serial | BSC shifts stored value through TDI→TDO chain |
| Update | Drive | BSC drives pad output from update register |
| Inactive | Hi-Z | BSC does not affect pad (scan mode disabled) |

### 2.2 Boundary Cell Types

The iPACE-CHIP uses three boundary cell types:

**BC_1 (Input Cell):**
- Captures input pad value
- Does not drive output pad
- Used for input-only pads (e.g., TCK, TMS, TDI, reset pin)

**BC_2 (Output Cell):**
- Captures output pad value (feedback)
- Drives output pad with update register value
- Used for output-only pads (e.g., TDO, telemetry output)

**BC_4 (Bidirectional Cell):**
- Captures input pad value
- Drives output pad when output enable is active
- Tri-state control via separate update register
- Used for bidirectional pads (e.g., SPI bus, GPIO)

### 2.3 Boundary Scan Order

The iPACE-CHIP boundary scan chain orders cells sequentially from TDI to TDO:

```
TDI → [BSC#1] → [BSC#2] → ... → [BSC#248] → TDO

Pad grouping (logical ordering):
├── TAP pads: TCK(1), TMS(2), TDI(3), TRST*(4)
├── Power control pads: VDD_SENSE(5-6), GND_SENSE(7-8)
├── Pacing output pads: PACE_OUT_A(9), PACE_OUT_B(10)
├── Sensing input pads: SENSE_CH1(11), SENSE_CH2(12), ...
├── Telemetry pads: TELE_TX(45), TELE_RX(46)
├── SPI pads: SPI_CLK(50), SPI_MOSI(51), SPI_MISO(52), SPI_CS(53)
├── Clock pads: XTAL_IN(60), XTAL_OUT(61)
├── Test pads: SCAN_CLK(100), SCAN_SE(101), ...
└── Reserved pads: (200-248)
```

---

## 3. iPACE-CHIP JTAG Instructions

### 3.1 Mandatory Instructions (IEEE 1149.1)

| Instruction | Opcode | Description |
|-------------|--------|-------------|
| BYPASS | 0xFF | 1-bit bypass register between TDI and TDO |
| EXTEST | 0x00 | External test — drives/reads boundary cells |
| SAMPLE/PRELOAD | 0x01 | Sample I/O or preload boundary cells |
| IDCODE | 0x06 | Shift 32-bit device ID register |
| INTEST | 0x03 | Internal test — tests core logic via boundary cells |

### 3.2 iPACE-CHIP Custom Instructions

| Instruction | Opcode | Description |
|-------------|--------|-------------|
| SCAN_EN | 0x10 | Enables scan chain access through TAP |
| SCAN_SHIFT | 0x11 | Shifts scan chain data through TDI/TDO |
| SCAN_CAPTURE | 0x12 | Captures scan chain responses |
| MBIST_START | 0x20 | Triggers memory BIST execution |
| MBIST_STATUS | 0x21 | Reads MBIST status and fail information |
| LBIST_START | 0x22 | Triggers logic BIST execution |
| LBIST_STATUS | 0x23 | Reads LBIST status and signature |
| FUSE_READ | 0x30 | Reads OTP fuse values |
| FUSE_PROGRAM | 0x31 | Programs OTP fuses (one-time) |
| SECURITY_UNLOCK | 0x40 | Unlocks protected JTAG instructions |
| THERMAL_READ | 0x50 | Reads on-chip temperature sensor |
| VOLTAGE_READ | 0x51 | Reads on-chip voltage monitors |
| SELF_TEST | 0x60 | Initiates comprehensive self-test |
| RESET_CORE | 0x70 | Asserts software reset to core logic |
| DEVICE_STATUS | 0x71 | Reads 32-bit device status register |

### 3.3 Instruction Decode Logic

```
              TDI ──►┌──────────────┐
                     │ Instruction  │
                     │ Register     │───► Instruction Decoder
                     │ (8-bit)      │         │
                     └──────┬───────┘         │
                            │                 │
              TDO ◄─────────┘                 │
                                              │
                     ┌────────────────────────┤
                     │                        │
              ┌──────┴───────┐         ┌──────┴───────┐
              │ Bypass MUX   │         │ Control      │
              │ (1-bit reg   │         │ Signals      │
              │  selected by │         │ (TDO_EN,     │
              │  instruction)│         │  UPDATE,     │
              └──────────────┘         │  CAPTURE)    │
                                       └──────────────┘
```

---

## 4. Boundary Scan Test Operations

### 4.1 EXTEST for Interconnect Testing

EXTEST enables testing of solder joints and PCB traces between the iPACE-CHIP and other components on the implantable system board:

**Test Setup:**
1. Load EXTEST instruction into IR
2. Preload boundary cells with driving values via PRELOAD
3. Assert EXTEST — driving values appear on output pads
4. Capture received values on input boundary cells (Capture-DR)
5. Shift out captured data for comparison

**Interconnect Test Coverage:**
- Solder joint opens (100% detection)
- Solder bridges/shorts (100% detection when properly sequenced)
- PCB trace opens (detected by observing expected transitions)
- Weak connections (detected by timing margin testing)

**Test Vector Example (8-pin interconnect):**
```
Drive Pattern: 10101010
Expected:      10101010 (pass) or 10100010 (bridge on bit 3)

Drive Pattern: 01010101
Expected:      01010101 (pass) or 01011101 (bridge on bit 3 confirmed)

Walking-1 test: 10000000 → 01000000 → ... → 00000001
Walking-0 test: 01111111 → 10111111 → ... → 11111110
```

### 4.2 INTEST for Core Logic Testing

INTEST isolates the iPACE-CHIP core logic from external pads and tests internal logic using boundary cells as stimulus/response points:

**Operation:**
1. Load INTEST instruction
2. Stimulus vectors shifted into output boundary cells (one vector per shift)
3. Capture-DR reads core logic response at input boundary cells
4. Response compared with expected values
5. Iteration continues until all test vectors applied

**Limitations:**
- Sequential depth limited by boundary cell granularity
- Test time proportional to (number of inputs + outputs) × vector count
- Not suitable for at-speed testing (shift limited by TCK frequency)

### 4.3 SAMPLE Operation

SAMPLE mode captures a snapshot of pad values without affecting circuit operation:

```
Application: Runtime monitoring
- Capture pad states during functional operation
- Non-intrusive: core logic continues operating
- Useful for timing analysis and signal integrity verification

Application: Boundary scan verification
- After PRELOAD, SAMPLE confirms values are correctly driven
- Validates boundary cell connectivity
```

### 4.4 PRELOAD Operation

PRELOAD initializes boundary cells before EXTEST or INTEST:

```
Sequence: PRELOAD → EXTEST
1. Shift PRELOAD instruction into IR
2. Shift desired driving values into boundary cells
3. Load EXTEST instruction (update happens at Update-IR)
4. Boundary cells now drive new values on output pads
```

---

## 5. JTAG for Production Testing

### 5.1 Board-Level Test Flow

The iPACE-CHIP JTAG interface supports the following production test sequence:

```
1. Power-up and JTAG connection verification
   ├── Read Device ID register
   ├── Verify ID matches expected value
   └── Check IR and DR lengths

2. Boundary scan chain integrity
   ├── Shift 01010101 through full chain
   ├── Shift 10101010 through full chain
   └── Verify both patterns exit correctly

3. Interconnect test (board-level)
   ├── EXTEST on all output pads
   ├── Sample all input pads
   ├── Walking-1 and walking-0 patterns
   └── Bridge detection patterns

4. Internal scan chain access (via JTAG)
   ├── Load SCAN_EN instruction
   ├── Apply scan patterns through TDI/TDO
   ├── Verify scan chain operation
   └── Run production scan ATPG patterns

5. BIST execution (via JTAG trigger)
   ├── MBIST_START → wait for completion → MBIST_STATUS
   ├── LBIST_START → wait for completion → LBIST_STATUS
   └── Read pass/fail and diagnostic information

6. Non-volatile memory programming (via JTAG)
   ├── Enter fuse programming mode
   ├── Program trim values, calibration data
   ├── Program device unique ID
   └── Verify programmed values

7. Test mode lock-out
   ├── Program security fuse to disable debug JTAG
   ├── Verify lock-out by attempting IDCODE
   └── Confirm only limited JTAG instructions available
```

### 5.2 JTAG Frequency Management

The iPACE-CHIP supports multiple TCK frequencies for different test phases:

| Phase | TCK Frequency | Rationale |
|-------|---------------|-----------|
| Chain integrity | 20 MHz | Maximum speed, simple shift |
| Boundary scan test | 10 MHz | Adequate for DC-level testing |
| Scan chain operation | 5 MHz | Limited by scan mode power |
| At-speed capture | 100 MHz (functional) | Internal capture clock, not TCK |
| BIST operation | 25 MHz | Limited by memory access time |
| Fuse programming | 1 MHz | Slow for reliable programming |

### 5.3 JTAG Power Considerations

During JTAG operation, power dissipation must stay within the implantable device thermal envelope:

- **TCK toggle power:** Each TCK edge drives internal TAP logic (~50μW at 20MHz)
- **Scan shift power:** Dominant power source during scan operations (~500μW)
- **BIST power:** Highest power mode (~850μW during MBIST)
- **Total JTAG power budget:** <1.5mW during any JTAG operation

---

## 6. JTAG Security for Medical Devices

### 6.1 Security Architecture

The iPACE-CHIP implements a multi-layer security model for the JTAG interface:

```
┌────────────────────────────────────────────┐
│              Security Levels                │
│                                             │
│  Level 0: Full Debug Access                 │
│  ├── All JTAG instructions available        │
│  ├── Used during development                │
│  └── Disabled by security fuse              │
│                                             │
│  Level 1: Limited Production Test           │
│  ├── SCAN_EN, BIST, STATUS instructions     │
│  ├── No fuse programming                    │
│  ├── Used during wafer sort and final test  │
│  └── Disabled after final test              │
│                                             │
│  Level 2: Device ID Only                    │
│  ├── IDCODE and BYPASS only                 │
│  ├── EXTEST/SAMPLE for board test           │
│  ├── No internal access                     │
│  └── Permanent state after shipping         │
│                                             │
│  Level 3: JTAG Completely Disabled          │
│  ├── TAP controller frozen in Test-Logic-Reset│
│  ├── TDO permanently tri-stated             │
│  └── Irreversible (burned fuse)             │
└────────────────────────────────────────────┘
```

### 6.2 In-Field JTAG Lock-Out

For a device implanted in a patient:

- **Level 3 JTAG lock-out** is mandatory per ISO 14971 risk analysis
- No JTAG activity possible after implant programming is complete
- Hardware fuse ensures absolute lock-out (not software-defeatable)
- TAP pins may be left floating or tied to default states for EMI compliance

### 6.3 JTAG and Functional Safety

During patient-connected operation:

- JTAG TCK is monitored by the watchdog timer
- Any TCK activity during functional mode triggers a safety interrupt
- JTAG pin voltages are monitored for ESD damage
- Periodic TAP controller reset ensures stuck-in-reset state is maintained

---

## 7. JTAG Implementation Details

### 7.1 TAP Controller Physical Implementation

```
TCK Input Buffer:
├── Schmitt trigger for noise immunity
├── 50Ω termination resistor (on-chip)
├── ESD protection (±8kV HBM)
└── Maximum input voltage: VDD + 0.3V

TMS/TDI Input Buffer:
├── Schmitt trigger
├── Input hysteresis: 200mV
├── Setup time requirement: 5ns before TCK rising edge
└── Hold time requirement: 2ns after TCK rising edge

TDO Output Buffer:
├── Tri-state capable (high-Z when TAP inactive)
├── Drive strength: 4mA (configurable)
├── Output impedance: 50Ω
└── Maximum load capacitance: 20pF
```

### 7.2 Boundary Scan Cell Count Summary

| Pad Type | Count | Cell Type | Notes |
|----------|-------|-----------|-------|
| TAP pins | 4 | BC_1 | Input only |
| Pacing output | 2 | BC_2 | Output only |
| Sensing input | 16 | BC_1 | Input only |
| Telemetry I/O | 4 | BC_4 | Bidirectional |
| SPI bus | 4 | BC_4 | Bidirectional |
| Clock | 2 | BC_1 | Input only |
| Power monitor | 4 | BC_1 | Input only |
| Test/scan | 20 | BC_4 | Bidirectional |
| GPIO | 8 | BC_4 | Bidirectional |
| Reserved/future | 184 | BC_1 | Input for test |
| **Total** | **248** | | |

### 7.3 JTAG Timing Constraints

**Setup and Hold at TAP Interface:**

```
                    TCK
                     │    │    │
              ┌──────┘    └────┘    └──
              │
    TDI/TMS ──┤◄─tsu─►│
              │        │
              │        │◄─thold─►│

    tsu (setup time):   ≥ 5 ns
    thold (hold time):  ≥ 2 ns
    TCK period (min):   50 ns (20 MHz max)
    TCK pulse width:    ≥ 20 ns (40% - 60% duty cycle)
```

**TDO Output Timing:**

```
                    TCK
                     │    │    │
              ┌──────┘    └────┘    └──
              │
    TDO ──────┤           │
              │◄─tdo_delay─►│
              │           │
              │     Valid TDO data ──►│

    tdo_delay (TCK↑ to TDO valid): ≤ 20 ns
    TDO valid window: ≥ 30 ns (at 20 MHz TCK)
```

---

## 8. Boundary Scan Description Language (BSDL)

### 8.1 BSDL File Structure

The iPACE-CHIP BSDL file defines the boundary scan architecture for ATE and test tool integration:

```vhdl
-- Simplified BSDL excerpt for iPACE-CHIP
entity iPACE_CHIP is
    generic (PHYSICAL_PIN_MAP : string := "QFN64");
    port (
        TCK     : in bit;
        TMS     : in bit;
        TDI     : in bit;
        TDO     : out bit;
        TRST_L  : in bit;
        -- Functional pins
        PACE_A  : out bit;
        PACE_B  : out bit;
        SENSE1  : in bit;
        SENSE2  : in bit;
        -- ... additional pins
    );
    
    attribute PIN_MAP of iPACE_CHIP : entity is PHYSICAL_PIN_MAP;
    
    constant TAP_ID : bit_vector := X"0001ACE0";
    constant IR_LENGTH : integer := 8;
    
    attribute INSTRUCTION_SECRET of iPACE_CHIP : entity is
        "SECURITY_UNLOCK";
    attribute INSTRUCTION_SEQUENCE of iPACE_CHIP : entity is
        "SECURITY_UNLOCK";
end iPACE_CHIP;
```

### 8.2 Boundary Scan Register Description

Each boundary cell is defined with attributes:

```vhdl
attribute BSCAN_IS_CELL of BSC_PACE_A : label is TRUE;
attribute BSCAN_IS_INPUT of BSC_PACE_A : label is FALSE;
attribute BSCAN_IS_OUTPUT of BSC_PACE_A : label is TRUE;
attribute BSCAN_CLOCK_NET of BSC_PACE_A : label is "TCK";
attribute BSCAN_CLOCK_ENABLE of BSC_PACE_A : label is TRUE;
```

---

## 9. Summary

The JTAG boundary scan architecture provides the iPACE-CHIP with standardized test access for board-level interconnect verification, production test execution, and diagnostic capability. The multi-level security model ensures that JTAG access is progressively locked down as the device progresses from development through production to implantation. Boundary scan cells on all 248 I/O pads provide complete controllability and observability for external interconnect testing, while custom JTAG instructions extend the TAP interface to control internal scan chains and BIST operations. The implementation complies with IEEE 1149.1 and addresses medical device-specific security requirements through hardware fuse-based permanent lock-out.

---

## References

- IEEE 1149.1-2013: Standard Test Access Port and Boundary-Scan Architecture
- IEEE 1149.4-1999: Standard for a Mixed-Signal Test Bus
- IEEE 1149.6-2003: Standard for Boundary-Scan Testing of Advanced Digital Networks
- Parker, K.P. *The JTAG/Boundary-Scan Cookbook*. Agilent Technologies, 2003.
- IEC 62132-4: Integrated Circuit Electromagnetic Immunity — Direct Power Injection
- ISO 14971:2019: Medical Devices — Application of Risk Management to Medical Devices
