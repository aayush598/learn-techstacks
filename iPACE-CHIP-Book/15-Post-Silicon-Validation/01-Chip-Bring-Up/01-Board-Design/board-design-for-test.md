# Board Design for Post-Silicon Test

## 15.1.1 Overview

The post-silicon validation phase for the iPACE-CHIP pacemaker begins with the design and fabrication of a dedicated test board. This board serves as the primary interface between the packaged silicon die and the laboratory test equipment. Unlike a production PCB, the test board is engineered for maximum flexibility, accessibility, and signal integrity rather than miniaturization. Every pad, every signal trace, and every power rail must be instrumented so that engineers can exercise every functional block of the iPACE-CHIP and observe its behavior under controlled conditions.

The test board is not a single-purpose artifact. It must support initial power-on sequencing, boundary-scan verification, JTAG debugging, analog front-end characterization, telemetry link validation, and environmental stress testing. Designing such a board requires a thorough understanding of the iPACE-CHIP architecture, the electrical characteristics of its I/O pads, the power delivery requirements of its internal regulators, and the test methodologies prescribed by the validation plan.

## 15.1.2 Design Requirements

### Functional Requirements

The board must expose every external pin of the iPACE-CHIP package. For the iPACE-CHIP in a 64-pin QFN package, this means routing all 64 pads to test points, headers, or programmable interconnects. Critical signals include:

- **Pacing output channels** (RV and LV leads)
- **Sensing input channels** (atrial and ventricular)
- **Telemetry antenna connections** (HF coil for inductive link)
- **Battery management pins** (VBAT sense, charge control)
- **JTAG/SWD debug interface** (TCK, TMS, TDI, TDO, nRESET)
- **SPI communication bus** (used for external flash programming)
- **GPIO and interrupt pins** (for external event triggers)
- **Power supply inputs** (VDD_ANA, VDD_DIG, VDD_IO, VBAT)
- **Reference voltage pins** (VREF, VBGAP)
- **Clock input/output** (32.768 kHz crystal pads)

### Electrical Requirements

The board must maintain signal integrity across all interfaces. For the analog front-end signals, which operate in the microvolt range, the board must achieve input-referred noise below 5 microvolts RMS. This imposes strict requirements on layout routing, shielding, and component placement. The power delivery network must support current transients up to 50 mA on the digital supply rail with less than 2% voltage droop, while the analog supply must maintain sub-microvolt noise in the frequency band of interest (0.5 Hz to 200 Hz).

### Mechanical Requirements

The board must accommodate the iPACE-CHIP package (64-pin QFN, 8 mm x 8 mm) with proper thermal pad soldering. The board dimensions should fit standard laboratory fixtures and automated test equipment (ATE) sockets. Mounting holes must align with probe station chucks for wafer-level testing if needed.

## 15.1.3 Board Architecture

### Layer Stackup

The test board uses a 6-layer stackup to provide adequate signal routing, power distribution, and shielding:

```
Layer 1: Signal (top)          - Component placement, signal routing
Layer 2: Ground plane (GND1)   - Continuous ground reference
Layer 3: Signal (inner 1)      - High-speed digital signals
Layer 4: Power plane (VDD1)    - Primary power distribution
Layer 5: Ground plane (GND2)   - Secondary ground reference
Layer 6: Signal (bottom)       - Connectors, test points
```

The continuous ground planes on layers 2 and 5 provide low-impedance return paths for all signals and act as shields between the analog and digital routing layers. Layer 3 carries high-speed digital signals (SPI, JTAG, telemetry) while layers 1 and 6 handle lower-speed analog signals and connectors.

### Power Distribution Network

The PDN is designed to support multiple independent supply rails with individual regulation and filtering:

```
VBAT Input (3.0V)
  |
  +-- LDO 1 --> VDD_ANA (2.5V analog supply)
  |     +-- Ferrite bead + 10uF + 100nF + 10nF filtering
  |
  +-- LDO 2 --> VDD_DIG (1.2V digital core)
  |     +-- Ferrite bead + 22uF + 100nF + 10nF filtering
  |
  +-- LDO 3 --> VDD_IO (1.8V I/O supply)
  |     +-- Ferrite bead + 10uF + 100nF filtering
  |
  +-- LDO 4 --> VDD_TELEM (2.5V telemetry supply)
        +-- Ferrite bead + 10uF + 100nF filtering
```

Each LDO is a low-dropout regulator with output noise below 10 microvolts RMS, specifically selected for the iPACE-CHIP's analog subsystem requirements. The ferrite beads isolate high-frequency switching noise from the LDOs, and the multi-valued capacitor banks provide low impedance across a wide frequency range.

### Current Measurement Infrastructure

Each power rail includes an inline current sense resistor (0.1 ohm for VDD_ANA, 0.01 ohm for VDD_DIG) with differential amplifier taps routed to BNC connectors for oscilloscope monitoring. This allows real-time measurement of current consumption during different operational modes:

| Rail | Sense Resistor | Voltage Range | Amplifier Gain | Effective Range |
|------|---------------|---------------|-----------------|-----------------|
| VDD_ANA | 0.1 ohm | 0-50 mV | x100 | 0-50 mA |
| VDD_DIG | 0.01 ohm | 0-500 mV | x10 | 0-500 mA |
| VDD_IO | 0.1 ohm | 0-10 mV | x100 | 0-10 mA |
| VDD_TELEM | 0.1 ohm | 0-50 mV | x100 | 0-50 mA |

## 15.1.4 Signal Routing Strategy

### Analog Front-End Routing

The iPACE-CHIP's analog front-end (AFE) processes cardiac signals in the microvolt range. The test board must preserve signal integrity from the BNC input connectors to the chip's sensing input pins. The routing strategy includes:

- **Differential pair routing** for all sensing inputs (AIN+, AIN-, VIN+, VIN-)
- **Guard traces** driven at the common-mode voltage to reduce crosstalk
- **Minimum 3x trace width clearance** from any digital signal
- **No vias** on critical analog traces to avoid impedance discontinuities
- **Input protection** with series resistors (1 kohm) and ESD clamps

The input signal chain on the board follows this topology:

```
BNC Connector --> ESD Protection --> AC Coupling Cap --> Anti-Alias Filter --> MUX --> Chip AFE Input
                  (TVS diode)      (1 uF ceramic)     (2nd order RC)      (on-chip)
```

### Digital Interface Routing

Digital interfaces (SPI, JTAG, UART) use controlled-impedance routing at 50 ohms single-ended. Series termination resistors (33 ohm) are placed at the driver end to minimize reflections. Clock signals use length-matched routing to maintain timing margins.

### Telemetry Coil Interface

The telemetry interface requires special attention due to its resonant tank circuit. The test board includes:

- A precision variable capacitor (1-10 pF, 0.1 pF resolution) for resonant frequency tuning
- A matched inductor socket for testing with different coil inductances
- An adjustable coupling transformer for simulating implant-to-external coupling
- 50-ohm matched BNC output for spectrum analyzer measurements

## 15.1.5 Connectors and Test Points

### Primary Connectors

| Connector | Type | Purpose |
|-----------|------|---------|
| J1 | 96-pin DIN 41612 | Main ATE interface |
| J2 | BNC (x8) | Analog signal I/O |
| J3 | SMA (x4) | High-frequency signals |
| J4 | DB-25 | Legacy serial interface |
| J5 | USB-C | Modern PC connectivity |
| J6 | RJ-45 | Ethernet for remote control |
| J7 | DIP socket | Battery simulator input |
| J8 | 10-pin IDC | JTAG debug header |
| J9 | 20-pin IDC | SPI flash programming |

### Test Point Allocation

The board provides test points on every significant signal node. Test points use gold-plated pads with 0.8 mm diameter, suitable for spring-loaded probe contacts (pogo pins). A total of 128 test points are distributed across the board:

- Power rails: 16 test points (4 per supply, at source and load ends)
- Analog signals: 24 test points (before and after each filter stage)
- Digital buses: 32 test points (all SPI, JTAG, and UART signals)
- Internal nodes: 48 test points (brought out via header jumpers)
- Debug signals: 8 test points (watchdog, reset, interrupt)

## 15.1.6 Protection Circuitry

### ESD Protection

All external connectors include TVS diode arrays rated at 15 kV contact discharge per IEC 61000-4-2. The protection is placed within 5 mm of each connector to minimize the stub length between the protection device and the entry point.

### Over-Current Protection

Each power rail includes a polyfuse rated at 2x the expected maximum current. The polyfuse placement is upstream of the current sense resistors to avoid measurement interference:

```
LDO Output --> Polyfuse --> Current Sense --> Ferrite Bead --> Decoupling --> Chip Pin
```

### Reverse Polarity Protection

The main battery input includes a P-channel MOSFET reverse polarity protection circuit with less than 10 mohm on-resistance, ensuring negligible voltage drop during normal operation.

## 15.1.7 Thermal Management

The iPACE-CHIP test board must operate reliably during extended characterization runs. The thermal management strategy includes:

- A 2 oz copper inner layer for heat spreading
- Thermal vias (0.3 mm diameter, 0.5 mm pitch) beneath the QFN thermal pad
- An optional heatsink attachment point on the bottom of the board
- Temperature sensor (RTD, PT1000) mounted within 5 mm of the chip for junction temperature estimation

The board is designed to maintain the chip junction temperature below 85 degrees Celsius during worst-case power dissipation (50 mW) in still air at 25 degrees Celsius ambient.

## 15.1.8 Component Selection

### Passive Components

All resistors on the signal path are thin-film type with 0.1% tolerance and 10 ppm/C temperature coefficient. Capacitors in the signal path use C0G/NP0 dielectric for stability. Decoupling capacitors use X7R dielectric for bulk capacitance and C0G for high-frequency bypassing.

| Component | Value | Package | Tolerance | Type |
|-----------|-------|---------|-----------|------|
| R_sense_VDDA | 0.1 ohm | 2512 | 0.1% | Thin-film |
| R_sense_VDDD | 0.01 ohm | 2512 | 0.5% | Thin-film |
| C_anti_alias | 10 nF | 0402 | 1% | C0G/NP0 |
| C_decoupling_bulk | 10 uF | 0805 | 10% | X7R |
| C_decoupling_hf | 100 nF | 0402 | 5% | C0G/NP0 |
| L_ferrite | 600 ohm@100MHz | 0603 | - | Ferrite bead |

### Active Components

| Component | Part Number | Function |
|-----------|-------------|----------|
| U_LDO_ANA | TPS7A2025 | 2.5V low-noise LDO |
| U_LDO_DIG | TPS62740 | 1.2V buck converter |
| U_LDO_IO | TPS7A1801 | 1.8V ultra-low-noise LDO |
| U_ESD | TPD2E001 | 2-channel ESD protection |
| U_AMP | INA828 | Current sense amplifier |
| U_MCU | STM32F407 | Board controller |

## 15.1.9 Board Controller

The on-board microcontroller (STM32F407) manages power sequencing, voltage monitoring, and test automation. It communicates with the host PC via USB and controls:

- **Power rail enable/disable** via GPIO-controlled MOSFET switches
- **Voltage DAC** for generating adjustable supply voltages
- **ADC channels** for monitoring all supply rails and temperatures
- **Relay switching** for signal routing reconfiguration
- **Status LEDs** for visual indication of board state

The board controller firmware implements a command protocol over USB CDC (virtual COM port) that allows the host test software to:

```
POWER ON VDD_ANA 2.50V      --> Enable and set analog supply
POWER ON VDD_DIG 1.20V      --> Enable and set digital supply
READ CURRENT VDD_ANA        --> Return current on analog rail
READ TEMPERATURE            --> Return board temperature
SET RELAY AFE_INPUT 1       --> Route BNC input 1 to AFE
SET MUX ANALOG_CH 3         --> Select analog channel 3
MEASURE ALL                 --> Read all ADC channels
```

## 15.1.10 PCB Layout Guidelines

### Analog vs. Digital Separation

The board is physically divided into analog and digital domains by a gap in the ground plane (connected only at a single star ground point near the power entry):

```
+---------------------------+---+---------------------------+
|                           | G |                           |
|     ANALOG DOMAIN         | N |      DIGITAL DOMAIN       |
|                           | D |                           |
|  AFE inputs, filters,     |   |  JTAG, SPI, UART,         |
|  sensing paths,           | * |  USB, board controller,   |
|  pacing output,           |   |  status LEDs,             |
|  telemetry tank           |   |  power sequencing         |
|                           |   |                           |
+---------------------------+---+---------------------------+
           Star ground point (GND*)
```

### Via Stitching

The board perimeter and the boundary between analog and digital domains feature via stitching at 2 mm pitch to provide a continuous ground reference along the board edges and reduce electromagnetic emissions.

### Copper Pour Strategy

- Layer 1: Ground pour in analog domain, signal routing in digital domain
- Layer 2: Continuous ground plane (no splits except at star ground)
- Layer 3: Signal routing only, no pour
- Layer 4: Power pour (split into regions for each supply rail)
- Layer 5: Continuous ground plane
- Layer 6: Ground pour under analog connectors, signal routing elsewhere

## 15.1.11 Design Verification

Before sending the board to fabrication, the design undergoes thorough verification:

### Electrical Rule Check (ERC)
- All nets have proper connectivity
- No unconnected inputs on active devices
- Power and ground nets properly sized
- Impedance-controlled nets meet target impedance (50 ohm +/- 10%)

### Thermal Simulation
- Steady-state thermal analysis at maximum power dissipation
- Transient thermal analysis for pulsed current scenarios
- Junction temperature estimation for all active components

### Signal Integrity Analysis
- Eye diagram simulation for SPI clock at 10 MHz
- Crosstalk analysis between adjacent analog channels
- Power integrity simulation showing PDN impedance vs. frequency
- S-parameter extraction for high-frequency paths

### Design Review Checklist

| Item | Status | Notes |
|------|--------|-------|
| All 64 package pins routed | Verified | No NC pins left floating |
| Ground plane continuity | Verified | Single star ground point |
| Analog trace clearance | Verified | 3x minimum spacing |
| Decoupling placement | Verified | Within 2mm of each VDD pin |
| Test point accessibility | Verified | All accessible from top |
| Connector orientation | Verified | Cables exit board edge |
| Thermal via array | Verified | 0.3mm, 0.5mm pitch under QFN |
| ESD protection coverage | Verified | All external connectors |
| Current sense accuracy | Verified | < 1% error from layout |
| Silkscreen labels | Verified | All components labeled |

## 15.1.12 Manufacturing Considerations

### Fabrication Specifications

- **Base material**: FR-4 high-Tg (Tg > 170C)
- **Copper weight**: 2 oz inner layers, 1 oz outer layers
- **Minimum trace width**: 4 mil (signal), 8 mil (power)
- **Minimum spacing**: 4 mil
- **Minimum drill**: 8 mil (via), 12 mil (component hole)
- **Surface finish**: ENIG (electroless nickel immersion gold)
- **Solder mask**: LPI green, opening on all test points and pads
- **Impedance control**: 50 ohm +/- 10% single-ended on layer 3

### Assembly Notes

The iPACE-CHIP package requires careful soldering due to its exposed thermal pad. The recommended reflow profile follows IPC/JEDEC J-STD-020 with a peak temperature of 245 degrees Celsius and a time above liquidus of 60-90 seconds. The thermal pad requires solder paste aperture optimization (65% coverage) to prevent voiding while ensuring adequate thermal contact.

## 15.1.13 Summary

The test board for iPACE-CHIP post-silicon validation is a critical piece of infrastructure that directly impacts the efficiency and accuracy of the entire validation campaign. Its design must balance the competing requirements of signal integrity, flexibility, testability, and reliability. By following the architecture, routing strategies, and component selection guidelines outlined in this chapter, the design team can ensure that the board provides a solid foundation for all subsequent bring-up, characterization, and validation activities. A well-designed test board reduces debug cycles, improves measurement accuracy, and accelerates the path from silicon to production.
