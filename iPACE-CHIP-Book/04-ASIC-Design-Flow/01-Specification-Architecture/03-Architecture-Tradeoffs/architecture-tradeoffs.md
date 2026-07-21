# Architecture Tradeoffs for iPACE-CHIP ASIC

## 1. Introduction

Architecture definition is the most consequential decision in the iPACE-CHIP design flow.
Choices made at this stage — process node, core voltage, IP partitioning, memory
architecture, and clock strategy — propagate through every downstream activity and are
largely irreversible once RTL coding begins.

This document systematically evaluates the major architectural tradeoffs for an
implantable pacemaker ASIC, balancing medical safety, power consumption, die area,
manufacturing cost, and design risk.

## 2. Process Technology Selection

### 2.1 Technology Node Comparison

```
┌──────────┬──────────┬──────────┬──────────┬──────────┬──────────┐
│ Feature  │ 350 nm   │ 180 nm   │ 130 nm   │ 65 nm    │ 28 nm    │
├──────────┼──────────┼──────────┼──────────┼──────────┼──────────┤
│ Vdd (nom)│ 3.3V     │ 1.8V     │ 1.2V     │ 1.0V     │ 0.9V     │
│ Gate Len │ 350 nm   │ 180 nm   │ 130 nm   │ 65 nm    │ 28 nm    │
│ Leff     │ 300 nm   │ 150 nm   │ 100 nm   │ 45 nm    │ 22 nm    │
│ SRAM     │ 12T      │ 8T/6T    │ 6T       │ 6T       │ 6T       │
│ Cell     │          │          │          │          │          │
│ Density  │ 1× (ref) │ 2.5×     │ 4×       │ 10×      │ 25×      │
│ Power    │ High     │ Medium   │ Low      │ Very Low │ Ultra Low│
│ (dyn)    │          │          │          │          │          │
│ Leakage  │ Very Low │ Low      │ Medium   │ High     │ V. High  │
│ TID      │ Excellent│ Good     │ Fair     │ Poor     │ Very Poor│
│ Tolerance│          │          │          │          │          │
│ ESD      │ Easy     │ Moderate │ Hard     │ V. Hard  │ Extreme  │
│ Cost/mm² │ $0.50    │ $0.80    │ $1.50    │ $3.00    │ $8.00    │
│ NRE      │ $2M      │ $3M      │ $5M      │ $15M     │ $40M     │
│ Maturity │ Mature   │ Mature   │ Mature   │ Mature   │ Moderate │
│ Foundry  │ TSMC     │ TSMC     │ TSMC     │ TSMC     │ TSMC     │
│ Options  │ 350μ     │ 180um    │ 130um    │ 65LP     │ 28nm     │
│          │          │          │          │          │ HPC+     │
└──────────┴──────────┴──────────┴──────────┴──────────┴──────────┘
```

### 2.2 iPACE-CHIP Selection: 180 nm CMOS

```
Decision Matrix (weighted scoring):
═══════════════════════════════════════════════════════════════

  Criteria        Weight   350nm  180nm  130nm  65nm   28nm
  ──────────────  ──────   ─────  ─────  ─────  ─────  ─────
  TID Tolerance    20%      10     8      5      2      1
  Leakage Power    20%       8     7      6      4      3
  Dynamic Power    15%       3     6      7      8      9
  Die Area/Cost    15%       3     7      6      7      8
  Design Maturity  10%       9     9      8      7      5
  NRE Cost         10%       9     8      6      3      1
  Reliability      10%       9     8      7      5      4
  ──────────────  ──────   ─────  ─────  ─────  ─────  ─────
  WEIGHTED SCORE   100%     7.20   7.45   6.35   4.95   4.00

  ┌─────────────────────────────────────────────────────────────┐
  │  SELECTED: 180 nm TSMC G (1.8V/3.3V thick-oxide)          │
  │                                                             │
  │  Rationale:                                                 │
  │  • Best balance of TID tolerance and power efficiency       │
  │  • Mature 3.3V I/O for electrode driving                    │
  │  • Low leakage (<1 nA/mm at 25°C)                           │
  │  • Proven medical device track record (many pacemakers)     │
  │  • Dual voltage: 1.8V core + 3.3V I/O on same die         │
  │  • SRAM density adequate for 4KB data + 1KB program         │
  │  • TID tolerance > 100 krad(Si) without special process    │
  │  • NRE and mask costs manageable for medical volumes        │
  └─────────────────────────────────────────────────────────────┘
```

### 2.3 Process-Dependent Design Decisions

```
180 nm TSMC G Process Specific Considerations:

  1. Core Voltage: VDD = 1.8V (±10%)
     ┌──────────────────────────────────────────────┐
     │ Speed vs Voltage:                             │
     │                                               │
     │ Delay ∝ Vdd / (Vdd - Vth)^α                  │
     │                                               │
     │ At 1.8V: Normal speed                        │
     │ At 1.62V: ~20% slower, ~30% less dynamic P  │
     │ At 1.98V: ~15% faster, ~20% more dynamic P  │
     │                                               │
     │ iPACE-CHIP Strategy: 1.5V nominal operation  │
     │ • Reduces dynamic power by ~31%              │
     │ • Reduces leakage by ~40%                    │
     │ • Accepts ~30% slower logic (OK at 33kHz)   │
     └──────────────────────────────────────────────┘

  2. Thick-Oxide I/O: 3.3V
     • Required for electrode driving (AAMI spec)
     • Provides higher voltage headroom for pace pulses
     • ESD tolerance: >4kV HBM on I/O pads

  3. Metal Stack: 6 metal layers (1P5M + top thick metal)
     • M1-M5: Signal routing
     • M6 (top): Power distribution, inductors for telemetry
     • Minimum width: 0.18 µm (M1), 0.20 µm (M2-M5)
     • Minimum spacing: 0.18 µm (M1), 0.20 µm (M2-M5)

  4. ESD Protection: diode-clamp + grounded-gate NMOS
     • All I/O pads: >4kV HBM, >200V CDM
     • Analog input pads: Low-capacitance ESD (<2pF)
     • Power pads: Multi-finger ggNMOS
```

## 3. Core Architecture

### 3.1 Processor vs. Hardwired Decision

```
Architecture Option A: Microcontroller-Based
═══════════════════════════════════════════════

  ┌─────────────────────────────────────────────────┐
  │  ┌──────────┐    ┌──────────┐    ┌──────────┐ │
  │  │  ARM     │    │  Custom  │    │  Custom  │ │
  │  │ Cortex-M0│◄──►│  AFE     │◄──►│  Output  │ │
  │  │  (MCU)   │    │  (Analog)│    │  Driver  │ │
  │  └────┬─────┘    └──────────┘    └──────────┘ │
  │       │                                         │
  │  ┌────▼─────┐    ┌──────────┐    ┌──────────┐ │
  │  │  SRAM    │    │  Timer   │    │ Telemetry│ │
  │  │  8KB     │◄──►│  + PLL   │◄──►│  UART    │ │
  │  └──────────┘    └──────────┘    └──────────┘ │
  └─────────────────────────────────────────────────┘

  Pros:                              Cons:
  + Flexible (FW updates)            - Higher power (CPU always on)
  + Faster development               - Larger die area
  + Mature tools                     - FW bugs possible
  + Easier certification path        - Timing harder to guarantee
                                     - More complex verification

  Power estimate: 15-25 µA average (FW-dependent)
  Die area estimate: 2.5 mm²
```

```
Architecture Option B: Hardwired State Machine (SELECTED)
═══════════════════════════════════════════════════════════════

  ┌─────────────────────────────────────────────────┐
  │                                                  │
  │  ┌──────────┐    ┌──────────────────────────┐   │
  │  │  Analog  │    │   Digital Core            │   │
  │  │  Front   │◄──►│                           │   │
  │  │  End     │    │  ┌────────┐  ┌────────┐  │   │
  │  └──────────┘    │  │Pacing  │  │Sensing │  │   │
  │                   │  │Engine  │  │Engine  │  │   │
  │  ┌──────────┐    │  │(FSM)   │  │(DSP)   │  │   │
  │  │  Output  │◄──►│  └────────┘  └────────┘  │   │
  │  │  Driver  │    │  ┌────────┐  ┌────────┐  │   │
  │  │  (Dual)  │    │  │Timing  │  │Tele    │  │   │
  │  └──────────┘    │  │Control │  │Engine  │  │   │
  │                   │  │(HW)    │  │(HW)    │  │   │
  │  ┌──────────┐    │  └────────┘  └────────┘  │   │
  │  │Telemetry │◄──►│  ┌────────────────────┐  │   │
  │  │Coil      │    │  │  Parameter Store   │  │   │
  │  └──────────┘    │  │  (SRAM + ECC)      │  │   │
  │                   │  └────────────────────┘  │   │
  │                   └──────────────────────────┘   │
  └─────────────────────────────────────────────────┘

  Pros:                              Cons:
  + Ultra-low power                  - Inflexible (no FW updates)
  + Smaller die area                 - Longer development time
  + Deterministic timing             - More complex RTL
  + Fewer failure modes              - New ASIC for each variant
  + Easier to verify completely      - Requires thorough upfront design
  + No FW-related safety issues

  Power estimate: 8-12 µA average
  Die area estimate: 1.8 mm²
```

### 3.2 Architecture Comparison Summary

```
┌──────────────────────┬────────────────┬────────────────────┐
│ Metric               │ MCU-Based      │ Hardwired FSM      │
├──────────────────────┼────────────────┼────────────────────┤
│ Avg Power (µA)       │ 15-25          │ 8-12               │
│ Die Area (mm²)       │ 2.5            │ 1.8                │
│ SRAM (KB)            │ 8              │ 4                  │
│ Gate Count           │ ~50K           │ ~15K               │
│ Max Clock Freq       │ 4 MHz          │ 33 kHz             │
│ Design Time          │ 12 months      │ 18 months          │
│ FW Updateable        │ Yes            │ No                 │
│ Failure Modes        │ Many (FW)      │ Few (HW only)      │
│ Verification Effort  │ Medium         │ High               │
│ Battery Life Impact  │ 7-10 years     │ 10-15 years        │
│ Certification Risk   │ Lower          │ Lower (simpler SW) │
│ Unit Cost (at 1K)    │ $8             │ $5                 │
│ Unit Cost (at 10K)   │ $4             │ $2.50              │
│ NRE (one-time)       │ $3M            │ $3.5M              │
└──────────────────────┴────────────────┴────────────────────┘

  ┌─────────────────────────────────────────────────────────────┐
  │  DECISION: Hardwired FSM Architecture                       │
  │                                                             │
  │  Justification:                                             │
  │  • 10-year battery life requires minimum power              │
  │  • No FW bugs eliminates major safety concern               │
  │  • Deterministic timing critical for real-time pacing       │
  │  • Implantable pacemaker parameters change rarely           │
  │  • Programming via telemetry reconfigures FSM registers     │
  │  • Regulatory path simpler with fewer failure modes         │
  │  • Volume production justifies higher NRE                   │
  └─────────────────────────────────────────────────────────────┘
```

## 4. Memory Architecture

### 4.1 Memory Technology Options

```
Memory Options for 180nm:
═══════════════════════════════════════════════════════════════

  ┌────────────┬─────────┬─────────┬──────────┬──────────────┐
  │ Type       │ Density │ Access  │ Power    │ Rad Tolerant │
  ├────────────┼─────────┼─────────┼──────────┼──────────────┤
  │ 6T SRAM    │ 0.7 µm² │ <1 ns   │ High     │ Poor (SEU)   │
  │ 8T SRAM    │ 1.2 µm² │ <1 ns   │ Medium   │ Moderate     │
  │ 12T SRAM   │ 2.0 µm² │ <1 ns   │ Low      │ Good (RHBD)  │
  │ eFuse      │ 0.3 µm² │ 10 ns   │ Ultra-low│ N/A (WORM)   │
  │ ROM        │ 0.2 µm² │ 5 ns    │ Ultra-low│ Excellent    │
  │ Register   │ ~4× SRAM│ <1 ns   │ High     │ V. Good      │
  │  File      │          │         │          │ (TMR)        │
  └────────────┴─────────┴─────────┴──────────┴──────────────┘

  iPACE-CHIP Memory Architecture:
    ┌──────────────────────────────────────────────┐
    │  Memory Map (4 KB total SRAM + 1 KB ROM)     │
    │                                               │
    │  0x0000 - 0x03FF │ ROM (1KB)                  │
    │  │ Boot code, config defaults, CRC tables    │
    │  │ Technology: Mask ROM (2-transistor cell)   │
    │                                               │
    │  0x0400 - 0x0BFF │ SRAM (2KB) - Parameters    │
    │  │ Pace parameters, sensitivity settings      │
    │  │ Technology: 12T RHBD SRAM                  │
    │  │ ECC: SECDED (7-bit Hamming)                │
    │                                               │
    │  0x0C00 - 0x0FFF │ SRAM (1KB) - Data Buffer   │
    │  │ Sense data FIFO, telemetry buffer          │
    │  │ Technology: 12T RHBD SRAM                  │
    │  │ ECC: SECDED                                │
    │                                               │
    │  0x1000 - 0x13FF │ SRAM (1KB) - Stack + Temp  │
    │  │ Temporary computation, FSM stack           │
    │  │ Technology: 8T SRAM (lower area)           │
    │  │ ECC: Parity only (transient data)          │
    └──────────────────────────────────────────────┘
```

### 4.2 SRAM Reliability: ECC Architecture

```
SECDED (Single-Error-Correct, Double-Error-Detect) Hamming Code:
═══════════════════════════════════════════════════════════════

  Data width: 32 bits
  Parity bits: 6 (for SECDED: 2^(6-1) ≥ 32+6+1 = 39)
  Total stored: 38 bits (32 data + 6 parity)

  ┌────┬────┬────┬────┬────┬────┬────┬────┬────┬────┬────┬───┐
  │ P1 │ P2 │ D1 │ P4 │ D2 │ D3 │ D4 │ P8 │ D5 │ D6 │ D7 │...│
  │bit1│bit2│bit3│bit4│bit5│bit6│bit7│bit8│bit9│bt10│bt11│   │
  └────┴────┴────┴────┴────┴────┴────┴────┴────┴────┴────┴───┘

  Parity Coverage Matrix:
  ┌─────────┬─────┬─────┬─────┬─────┬─────┬─────┐
  │ Bit Pos │ P1  │ P2  │ P4  │ P8  │ P16 │ P32 │
  ├─────────┼─────┼─────┼─────┼─────┼─────┼─────┤
  │ P1  (1) │  X  │     │     │     │     │     │
  │ P2  (2) │     │  X  │     │     │     │     │
  │ D1  (3) │  X  │  X  │     │     │     │     │
  │ P4  (4) │     │     │  X  │     │     │     │
  │ D2  (5) │  X  │     │  X  │     │     │     │
  │ D3  (6) │     │  X  │  X  │     │     │     │
  │ D4  (7) │  X  │  X  │  X  │     │     │     │
  │ P8  (8) │     │     │     │  X  │     │     │
  │ D5  (9) │  X  │     │     │  X  │     │     │
  │ ...     │     │     │     │     │     │     │
  └─────────┴─────┴─────┴─────┴─────┴─────┴─────┘

  Single-Bit Error: Correctable (syndrome → bit position)
  Double-Bit Error: Detected, not corrected → FAULT signal
  Triple-Bit+: Not detectable (extremely rare with 12T SRAM)

  SEU Rate Estimation:
    At 50 krad(Si) TID, ~1 SEU per 10⁶ device-hours per Mbit
    4KB SRAM = 0.032 Mbit → SEU rate = 3.2 × 10⁻⁸ /device-hour
    Over 10 years: ~0.0028 SEUs expected → very low risk ✓
```

## 5. Clock Architecture

### 5.1 Clock Source Options

```
┌──────────────────┬───────────┬───────────┬───────────┬──────────┐
│ Option           │ Accuracy  │ Power     │ Startup   │ Cost     │
├──────────────────┼───────────┼───────────┼───────────┼──────────┤
│ RC Oscillator    │ ±5-10%    │ <1 µA     │ <1 µs     │ Free     │
│ Crystal (32.768k)│ ±20 ppm   │ 0.5 µA   │ 100 ms    │ $0.10    │
│ Crystal (32.768k)│ ±5 ppm    │ 1.0 µA   │ 100 ms    │ $0.50    │
│  (watch-grade)   │           │           │           │          │
│ MEMS Oscillator  │ ±10 ppm   │ 10 µA    │ 1 ms      │ $0.20    │
│ PLL + XTAL       │ ±20 ppm   │ 5-50 µA  │ 1 ms      │ $0.30    │
│ TCXO             │ ±0.5 ppm  │ 50 µA    │ 1 ms      │ $2.00    │
└──────────────────┴───────────┴───────────┴───────────┴──────────┘

  ┌─────────────────────────────────────────────────────────────┐
  │  SELECTED: Dual-clock architecture                          │
  │                                                             │
  │  Primary: 32.768 kHz watch crystal (±5 ppm, aged)          │
  │  • Always-on reference for pacing timing                   │
  │  • Provides accurate heart rate measurement                │
  │  • Ultra-low power: <0.5 µA oscillator core               │
  │                                                             │
  │  Secondary: RC Oscillator (on-chip)                        │
  │  • ±5% accuracy sufficient for telemetry baud rate         │
  │  • Starts instantly (no crystal warm-up)                   │
  │  • Used during crystal startup as fallback                 │
  │  • Power: <0.1 µA                                         │
  │                                                             │
  │  Telemetry Clock: PLL derived from crystal                 │
  │  • 32.768 kHz × 32 = 1.048576 MHz                         │
  │  • Active only during telemetry sessions                   │
  │  • Power: ~10 µA when enabled                              │
  └─────────────────────────────────────────────────────────────┘
```

### 5.2 Clock Distribution Architecture

```
Clock Tree for iPACE-CHIP:
═══════════════════════════════════════════════════════════════

  ┌──────────┐     ┌──────────┐
  │ 32.768 kHz│     │ On-chip  │
  │ Crystal   │     │ RC OSC   │
  │           │     │ (backup) │
  └─────┬─────┘     └────┬─────┘
        │                │
        ▼                ▼
  ┌──────────┐     ┌──────────┐
  │ Crystal  │     │ RC OSC   │
  │ Osc Amp  │     │ Buffer   │
  └─────┬─────┘     └────┬─────┘
        │                │
        └───────┬────────┘
                │
                ▼
        ┌──────────────┐
        │  Clock MUX   │
        │  (glitch-free)│
        └───────┬──────┘
                │
                ▼
        ┌──────────────┐     ┌──────────────┐
        │  Global      │────►│  Telemetry   │
        │  Clock       │     │  Clock       │
        │  32.768 kHz  │     │  (PLL output)│
        └──────┬───────┘     └──────┬───────┘
               │                     │
     ┌─────────┼─────────┐           │
     ▼         ▼         ▼           ▼
  ┌──────┐ ┌──────┐ ┌──────┐   ┌──────┐
  │Pacing│ │Sensing│ │Timer │   │UART  │
  │Logic │ │Engine │ │Block │   │+ CRC │
  └──────┘ └──────┘ └──────┘   └──────┘

  Clock Gating Strategy:
    • Global clock gated to sensing engine when in sleep mode
    • Global clock gated to pacing logic between beats (dangerous)
    • Timer always running (not gated)
    • Telemetry clock only active during tele sessions
    • PLL locked indication used before switching to PLL clock
```

## 6. Power Architecture

### 6.1 Voltage Domain Architecture

```
iPACE-CHIP Voltage Domains:
═══════════════════════════════════════════════════════════════

  ┌─────────────────────────────────────────────────────────────┐
  │  VBAT (3.0V Li/SOCl₂)                                      │
  │       │                                                     │
  │       ▼                                                     │
  │  ┌──────────────┐                                          │
  │  │ LDO Regulator│──── VDD_IO (3.3V)                        │
  │  │ (always-on)  │     │                                     │
  │  │ Iq = 0.3 µA  │     ├── I/O pads                          │
  │  └──────┬───────┘     ├── Output drivers (high-voltage)    │
  │         │             └── Telemetry coil driver             │
  │         ▼                                                   │
  │  ┌──────────────┐                                          │
  │  │ Switched     │──── VDD_CORE (1.5V, reduced from 1.8V)   │
  │  │ Capacitor DC │     │                                     │
  │  │ DC (future)  │     ├── Digital logic (FSM, counters)     │
  │  │              │     ├── SRAM arrays                       │
  │  │ OR           │     └── PLL (when active)                 │
  │  │ LDO (simple) │                                          │
  │  └──────────────┘                                          │
  │                                                             │
  │  Power Gating:                                              │
  │  • VDD_A analog: Always-on (AFE bias references)           │
  │  • VDD_A analog_sleep: Gated between sensing windows       │
  │  • VDD_D core: Always-on (low-power retention mode)        │
  │  • VDD_D active: Gated to active sub-blocks only           │
  └─────────────────────────────────────────────────────────────┘

  Voltage Scaling for Ultra-Low Power:
    P_dynamic = α × C × V² × f

    At Vdd = 1.8V (nominal):  P = α × C × 3.24 × f
    At Vdd = 1.5V (reduced): P = α × C × 2.25 × f
    Savings = (3.24 - 2.25) / 3.24 = 30.6% reduction ✓

    Note: 1.5V is within 180nm spec (Vdd_min = 1.08V for 80% of nom)
```

## 7. Analog Architecture

### 7.1 AFE Topology Selection

```
AFE Topology Comparison:
═══════════════════════════════════════════════════════════════

  Option A: Fully Integrated AFE (SELECTED)
  ┌─────────────────────────────────────────────────┐
  │  ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐ ┌─────┐ │
  │  │Input │►│ LNA  │►│ VGA  │►│ BPF  │►│ SAR │► │
  │  │Switch│ │G=100 │ │0-40dB│ │2nd   │ │ ADC │  │
  │  │      │ │      │ │      │ │order │ │12bit│  │
  │  └──────┘ └──────┘ └──────┘ └──────┘ └─────┘ │
  └─────────────────────────────────────────────────┘

  Pros: Small area, fewer external components
  Cons: Higher noise, limited dynamic range

  Option B: Discrete Front-End + On-Chip ADC
  ┌──────────┐ ┌──────────────────────────────┐
  │ External │ │  On-chip                      │
  │ LNA +    │►│  ┌──────┐ ┌──────┐ ┌──────┐ │
  │ Filter   │ │  │ VGA  │►│ BPF  │►│ SAR  │ │
  │ (off-chip│ │  │      │ │      │ │ ADC  │ │
  │  component)│ │  └──────┘ └──────┘ └──────┘ │
  └──────────┘ └──────────────────────────────┘

  Pros: Better noise performance
  Cons: More external components, larger package

  ┌─────────────────────────────────────────────────────────────┐
  │  SELECTED: Option A (Fully Integrated)                      │
  │                                                             │
  │  Rationale:                                                 │
  │  • Medical implants demand minimal external components      │
  │  • 5 µVrms noise floor achievable with 180nm CMOS          │
  │  • Reduces package pin count and hermetic feedthrough       │
  │  • All critical specs met with integrated approach          │
  │  • External components = additional failure points          │
  └─────────────────────────────────────────────────────────────┘
```

## 8. Reliability Architecture

### 8.1 Radiation Hardening Strategy

```
Radiation Effects on 180nm CMOS:
═══════════════════════════════════════════════════════════════

  Effect           │ Mechanism              │ Mitigation
  ─────────────────┼────────────────────────┼──────────────────
  TID              │ Threshold shift,       │ Guard rings,
  (Total Ionizing  │ leakage increase       │ annealing
   Dose)           │                        │ design
  ─────────────────┼────────────────────────┼──────────────────
  SEU              │ Bit-flip in SRAM/FF    │ ECC, TMR,
  (Single-Event    │                        │ redundancy
   Upset)          │                        │
  ─────────────────┼────────────────────────┼──────────────────
  SEL              │ Parasitic latchup      │ SOI substrate,
  (Single-Event    │ → destructive          │ current limiters
   Latchup)        │                        │

  iPACE-CHIP RHBD (Rad-Hard By Design) Techniques:
  ┌────────────────────────────────────────────────────────────┐
  │                                                            │
  │  1. Triple Modular Redundancy (TMR) on all flip-flops      │
  │     ┌──────┐ ┌──────┐ ┌──────┐                            │
  │     │ FF_A │ │ FF_B │ │ FF_C │                            │
  │     └──┬───┘ └──┬───┘ └──┬───┘                            │
  │        └────────┼────────┘                                 │
  │                 ▼                                          │
  │         ┌──────────┐                                       │
  │         │ Majority │                                      │
  │         │ Voter    │                                      │
  │         └──────────┘                                       │
  │                                                            │
  │  2. ECC on all SRAM (SECDED)                               │
  │     • 12T SRAM cell for SEU immunity (vs 6T for area)     │
  │     • Write-back on correctable error detected             │
  │     • Non-correctable error → safety mode                  │
  │                                                            │
  │  3. Guard rings around analog circuits                     │
  │     • n+ guard ring around p-substrate devices             │
  │     • p+ guard ring around n-well devices                  │
  │     • Reduces charge collection by 60-80%                  │
  │                                                            │
  │  4. Temporal redundancy on critical counters               │
  │     • Sample counter value at two time points              │
  │     • Compare for consistency                              │
  │     • Detects SEU-induced counter jumps                    │
  └────────────────────────────────────────────────────────────┘
```

## 9. Telemetry Architecture

### 9.1 Inductive Link Design

```
Inductive Telemetry Link Budget:
═══════════════════════════════════════════════════════════════

  Carrier Frequency: 135.53 kHz (ISO 14708-3)

  Link Budget Calculation:
  ┌────────────────────────┬──────────────┬───────────────────┐
  │ Parameter              │ Value        │ Notes             │
  ├────────────────────────┼──────────────┼───────────────────┤
  │ Tx Coil Turns          │ 50           │ External (progger)│
  │ Tx Coil Diameter       │ 30 mm        │                  │
  │ Tx Current             │ 100 mA peak  │                  │
  │ Frequency              │ 135.53 kHz   │                  │
  │ Rx Coil Turns          │ 20           │ On-chip (implant) │
  │ Rx Coil Diameter       │ 8 mm         │ Within housing    │
  │ Coupling Coeff (k)     │ 0.01-0.1     │ Distance-dependent│
  │ Mutual Inductance (M)  │ 0.1-1.0 µH   │ M = k√(L1×L2)    │
  │ Induced Voltage (V)    │ 10-100 mV    │ V = ω×M×I         │
  │ Required SNR          │ > 20 dB      │ For BER < 10⁻⁶   │
  │ Noise Floor            │ 5 µVrms      │ Thermal + circuit  │
  │ Operating Distance     │ 1-20 cm      │                  │
  └────────────────────────┴──────────────┴───────────────────┘

  Modulation Schemes Evaluated:
  ┌────────────┬────────────┬───────────┬──────────────────────┐
  │ Scheme     │ Data Rate  │ Complexity│ iPACE-CHIP Choice    │
  ├────────────┼────────────┼───────────┼──────────────────────┤
  │ ASK/OOK    │ 1-10 kbps  │ Low       │ Selected (uplink)    │
  │ FSK        │ 1-10 kbps  │ Medium    │ Not needed           │
  │ PSK        │ 10+ kbps   │ High      │ Overkill for 1-2 kbps│
  │ Backscatter│ <1 kbps    │ Very Low  │ Power-limited        │
  └────────────┴────────────┴───────────┴──────────────────────┘
```

## 10. Design-For-Test Architecture

### 10.1 DFT Strategy

```
iPACE-CHIP DFT Architecture:
═══════════════════════════════════════════════════════════════

  Test Modes:
  ┌──────────────┬───────────────────────────────────────────┐
  │ Test Mode    │ Description                               │
  ├──────────────┼───────────────────────────────────────────┤
  │ Normal       │ Clinical operation mode                   │
  │ Factory Test │ Full scan test, memory BIST, analog test  │
  │ Self-Test    │ Power-on self-test (POST) for field use   │
  │ Diagnostic   │ Readback of registers and counters        │
  │ Burn-in      │ High-speed stress test for screening      │
  └──────────────┴───────────────────────────────────────────┘

  DFT Features:
  • Scan chain: All flip-flops serially connected
  • MBIST: March C- algorithm for SRAM testing
  • Analog BIST: Self-test of AFE gain, offset, bandwidth
  • JTAG-like test port: 4-wire (TEST_CLK, TEST_EN, TEST_IN, TEST_OUT)
  • Test mode disable: Permanently disabled in field via eFuse

  DFT Pin Usage:
    ┌──────────────────────────────────────────────────────┐
    │  Pin        │ Normal Mode  │ Test Mode               │
    ├─────────────┼──────────────┼─────────────────────────┤
    │  TEST_CLK   │  Hi-Z (ext) │  Test clock input        │
    │  TEST_EN    │  0 (GND)    │  1 (enables test mode)   │
    │  TEST_DATA  │  Hi-Z       │  Serial scan I/O         │
    │  TEST_DONE  │  Hi-Z       │  Test complete flag       │
    └─────────────┴──────────────┴─────────────────────────┘

  Safety: TEST_EN tied to GND via internal pull-down
          eFuse blow option for permanent test disable
```

## 11. Architecture Tradeoff Summary

```
┌──────────────────────────────┬──────────────────────────────────┐
│ Decision Area                │ iPACE-CHIP Selection              │
├──────────────────────────────┼──────────────────────────────────┤
│ Process Node                 │ 180nm CMOS (TSMC G)              │
│ Core Voltage                 │ 1.5V (reduced from nom 1.8V)     │
│ I/O Voltage                  │ 3.3V (thick oxide)               │
│ Architecture                 │ Hardwired FSM (no MCU)           │
│ Clock Source                 │ Dual: 32.768kHz XTAL + RC OSC    │
│ SRAM Technology              │ 12T RHBD SRAM (parameters)       │
│ SRAM Size                    │ 4KB total (2KB param + 2KB data) │
│ ROM Size                     │ 1KB (boot code, defaults)        │
│ ECC                          │ SECDED on all SRAM               │
│ TMR                          │ On all flip-flops                │
│ AFE Topology                 │ Fully integrated (LNA+VGA+BPF+ADC)│
│ ADC Type                     │ SAR, 12-bit, 1 kSPS             │
│ Output Driver                │ Dual-redundant H-bridge          │
│ Telemetry                    │ Inductive ASK, 135.53 kHz        │
│ Encryption                   │ AES-128 (HW accelerator)         │
│ DFT                          │ Scan + MBIST + Analog BIST       │
│ Test Interface               │ 4-wire JTAG-like                 │
│ Estimated Die Area           │ 1.8 mm² (core) + pads           │
│ Estimated Gate Count         │ ~15K equivalent gates            │
│ Estimated Power              │ 8-12 µA average                  │
│ Estimated Battery Life       │ 12-15 years                      │
└──────────────────────────────┴──────────────────────────────────┘
```

## 12. Summary

The iPACE-CHIP architecture is optimized for the unique demands of an implantable
pacemaker: ultra-low power, extreme reliability, deterministic timing, and minimal
failure modes. The hardwired FSM architecture, 180nm process, and radiation-tolerant
design techniques collectively ensure the chip meets its 10-year lifetime target while
providing the clinical functionality required by cardiologists and patients.

---

*Previous: [System-Level Modeling](../02-System-Level-Modeling/system-level-modeling.md) | Next: [IP Selection](../04-IP-Selection/ip-selection.md)*
