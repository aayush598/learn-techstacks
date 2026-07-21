# IP Selection for iPACE-CHIP ASIC

## 1. Introduction

Intellectual Property (IP) selection determines which functional blocks in the iPACE-CHIP
are designed from scratch, licensed from third-party vendors, or reused from previous
designs. For a medical implantable device, IP selection carries unique constraints:

- **Qualification burden**: Third-party IP must be verified for medical reliability
- **Safety certification**: IP must support IEC 62304 compliance
- **Support lifecycle**: Vendor must support the IP for the chip's production lifetime
- **Liability**: Third-party IP failures may complicate regulatory submissions
- **Radiation tolerance**: Standard IP may not meet implant radiation requirements

## 2. IP Classification Framework

### 2.1 IP Types

```
┌────────────────┬──────────────────────┬──────────────────────────┐
│ IP Category    │ Description          │ Example in iPACE-CHIP    │
├────────────────┼──────────────────────┼──────────────────────────┤
│ Hard IP        │ Pre-designed, fixed   │ PHY, PLL, memory macros  │
│                │ layout, validated     │                          │
├────────────────┼──────────────────────┼──────────────────────────┤
│ Soft IP        │ RTL source code,     │ Encryption engine,       │
│                │ synthesizable        │ CRC calculator           │
├────────────────┼──────────────────────┼──────────────────────────┤
│ Firm IP        │ Layout-aware RTL,    │ Standard cell library,   │
│                │ technology-mapped    │ I/O cell library         │
├────────────────┼──────────────────────┼──────────────────────────┤
│ Analog IP      │ Custom analog blocks │ AFE, LDO, bandgap       │
│                │                      │ reference, oscillator     │
├────────────────┼──────────────────────┼──────────────────────────┤
│ Platform IP    │ Complete subsystems  │ UART, SPI, Timer         │
│                │                      │                          │
├────────────────┼──────────────────────┼──────────────────────────┤
│ Process IP     │ Foundry-provided     │ Standard cells, IO cells,│
│                │                      │ SRAM compilers, eFuse    │
└────────────────┴──────────────────────┴──────────────────────────┘
```

### 2.2 IP Sourcing Strategy

```
iPACE-CHIP IP Sourcing Decision Tree:

  Is the block available as proven IP?
  │
  ├── YES ──► Is it medical-grade qualified?
  │           │
  │           ├── YES ──► License from vendor
  │           │           (with customization rights)
  │           │
  │           └── NO ───► Can it be qualified with
  │                       additional verification?
  │                       │
  │                       ├── YES ──► License + augment
  │                       │           with safety wrapper
  │                       │
  │                       └── NO ───► Design in-house
  │
  └── NO ───► Is it safety-critical?
              │
              ├── YES ──► Design in-house
              │           (full control, traceability)
              │
              └── NO ───► Design in-house or
                          design from reference architecture
```

## 3. Process Design Kit (PDK)

### 3.1 PDK Components

```
┌──────────────────────────────────────────────────────────────┐
│                TSMC 180nm PDK Components                      │
├──────────────────────┬───────────────────────────────────────┤
│ Component            │ Contents                              │
├──────────────────────┼───────────────────────────────────────┤
│ Device Models        │ BSIM3v3 for NMOS/PMOS (TT, SS, FF,  │
│                      │ SF, FS corners)                      │
│                      │ Resistor models (poly, diff, Nwell)  │
│                      │ Capacitor models (MIM, MOS)          │
│                      │ Diode models (ESD, protection)       │
│                      │ BJT models (NPN, PNP for bandgap)   │
├──────────────────────┼───────────────────────────────────────┤
│ Standard Cell Lib    │ combinational: AND, OR, XOR, MUX     │
│ (tcbn180ghp)         │ sequential: DFF, latch, scan FF     │
│                      │ Special: clock buffer, tie-high      │
│                      │ VT variants: HVT, SVT, LVT          │
├──────────────────────┼───────────────────────────────────────┤
│ I/O Cell Library     │ 3.3V I/O: input, output, bidir      │
│ (tpdn18ghp)          │ ESD protection: diode-clamp, ggNMOS │
│                      │ Drive strengths: 2mA, 4mA, 8mA      │
├──────────────────────┼───────────────────────────────────────┤
│ SRAM Compiler        │ Configurable: 64x8 to 512x32        │
│                      │ Configurations: 1R1W, 2R1W, 2RW     │
│                      │ Built-in ECC option                  │
├──────────────────────┼───────────────────────────────────────┤
│ eFuse                │ 256-bit programmable array            │
│                      │ One-time programmable (WORM)          │
├──────────────────────┼───────────────────────────────────────┤
│ Layout Rules         │ DRC, LVS, ERC, Antenna rules        │
├──────────────────────┼───────────────────────────────────────┤
│ PCells/SKILL         │ Parameterized layout generators      │
└──────────────────────┴───────────────────────────────────────┘
```

### 3.2 Standard Cell Library Analysis

```
TSMC 180nm Standard Cell Characteristics (VDD=1.5V):

┌──────────────┬─────────┬──────────┬──────────┬─────────────┐
│ Cell         │ Delay   │ Power    │ Area     │ Leakage     │
├──────────────┼─────────┼──────────┼──────────┼─────────────┤
│ INV (1x)     │ 45 ps   │ 0.8 uW  │ 1.17 um2 │ 0.02 nA    │
│ NAND2 (1x)   │ 58 ps   │ 1.1 uW  │ 1.73 um2 │ 0.03 nA    │
│ NOR2 (1x)    │ 52 ps   │ 0.9 uW  │ 1.73 um2 │ 0.02 nA    │
│ AOI21 (1x)   │ 62 ps   │ 1.3 uW  │ 2.30 um2 │ 0.04 nA    │
│ DFF (HVT)    │ 180 ps  │ 3.2 uW  │ 7.78 um2 │ 0.08 nA    │
│ DFF (SVT)    │ 130 ps  │ 5.8 uW  │ 7.78 um2 │ 0.15 nA    │
│ DFF (LVT)    │ 95 ps   │ 9.1 uW  │ 7.78 um2 │ 0.35 nA    │
│ MUX2 (1x)    │ 70 ps   │ 1.5 uW  │ 2.87 um2 │ 0.05 nA    │
│ BUFG (16x)   │ 35 ps   │ 12.0 uW │ 8.91 um2 │ 0.40 nA    │
└──────────────┴─────────┴──────────┴──────────┴─────────────┘

iPACE-CHIP Usage Strategy:
  HVT cells: 80% of logic (timing not critical at 33kHz)
  SVT cells: 15% of logic (timing-sensitive paths)
  LVT cells:  5% of logic (telemetry datapath only)
  This minimizes leakage power significantly.
```

## 4. Custom Analog IP

### 4.1 Analog Blocks to Design In-House

```
┌──────────────────────────────────────────────────────────────┐
│           CUSTOM ANALOG IP BLOCKS FOR iPACE-CHIP             │
├──────────────────────┬───────────────────────────────────────┤
│ Block                │ Rationale                             │
├──────────────────────┼───────────────────────────────────────┤
│ LNA                  │ Unique electrode interface            │
│                      │ Ultra-low noise (5uVrms), high CMRR  │
├──────────────────────┼───────────────────────────────────────┤
│ VGA                  │ Programmable gain matched to LNA      │
│                      │ Must track across PVT variations      │
├──────────────────────┼───────────────────────────────────────┤
│ Bandpass Filter      │ 0.5-100 Hz cutoff (cardiac-specific)  │
│                      │ No commercial IP at this freq band    │
├──────────────────────┼───────────────────────────────────────┤
│ 12-bit SAR ADC       │ Ultra-low power at 1 kSPS            │
│                      │ Must work at 1.5V core voltage       │
├──────────────────────┼───────────────────────────────────────┤
│ Bandgap Reference    │ Provides Vref for ADC and LDO        │
│                      │ Low-power, temperature-stable         │
├──────────────────────┼───────────────────────────────────────┤
│ LDO Regulator        │ Ultra-low quiescent current (<300nA) │
│                      │ High PSRR at 32kHz                    │
├──────────────────────┼───────────────────────────────────────┤
│ Crystal Oscillator   │ Ultra-low power startup (<1uA)       │
│                      │ Must start within 100ms               │
├──────────────────────┼───────────────────────────────────────┤
│ Output Drivers (x2)  │ H-bridge for bipolar pacing          │
│                      │ Dual-redundant for safety             │
├──────────────────────┼───────────────────────────────────────┤
│ Current Sense Amp    │ Monitors output driver current        │
│                      │ Over-current detection (<1us)         │
├──────────────────────┼───────────────────────────────────────┤
│ Telemetry Coil Driver│ Inductive link interface              │
│                      │ 135.53 kHz carrier generation         │
├──────────────────────┼───────────────────────────────────────┤
│ Brownout Detector    │ Monitors battery voltage              │
│                      │ Triggers safe mode at VBAT < 2.4V    │
└──────────────────────┴───────────────────────────────────────┘
```

### 4.2 LNA Specification and Topology

```
LNA Design Specification:

┌──────────────────────┬──────────────┬────────────────────┐
│ Parameter            │ Specification│ Design Target      │
├──────────────────────┼──────────────┼────────────────────┤
│ Input Referred Noise │ <= 5 uVrms   │ 3.5 uVrms         │
│ Gain                 │ 40 dB (x100) │ 40.2 dB            │
│ CMRR                 │ >= 80 dB     │ 85 dB              │
│ PSRR                 │ >= 60 dB     │ 65 dB              │
│ Input Impedance      │ >= 5 kOhm    │ 8 kOhm             │
│ Input Offset         │ <= 50 uV     │ 25 uV (cal)        │
│ Supply Current       │ <= 2 uA      │ 1.5 uA             │
│ Supply Voltage       │ 1.5V         │ 1.5V               │
│ Bandwidth            │ 0.5-100 Hz   │ 0.5-100 Hz         │
│ THD                  │ <= -60 dB    │ -65 dB             │
└──────────────────────┴──────────────┴────────────────────┘

Topology: Chopper-Stabilized Instrumentation Amplifier

  Vin+ -->[CHOP]-->┌──────┐--[CHOP]--> Vout+
                    │ OpAmp │
  Vin- -->[CHOP]-->│  (1) │--[CHOP]--> Vout-
                    └──────┘
                      │
                 ┌────v────┐
                 │ Feedback │
                 │ Network  │
                 └─────────┘

Chopping Frequency: 10 kHz (above 1/f corner of CMOS)
Ripple Removal: Notch filter at chopper frequency

Noise Analysis:
  Thermal noise: Vn = sqrt(4kTR x BW)
  At R=1kOhm, BW=99.5Hz: Vn = 1.28 uVrms
  1/f corner of 180nm PMOS: ~50 kHz (after chopping)
  Chopper moves 1/f noise to 10kHz (outside signal band)
  Total input-referred noise: ~3.5 uVrms PASS
```

## 5. Third-Party Licensed IP

### 5.1 AES-128 Encryption Engine

```
AES-128 HW Accelerator Selection:

  Vendor Options:
  ┌─────────────────┬──────────┬──────────┬──────────┬────────┐
  │ Vendor          │ Area     │ Power    │ Latency  │ Price  │
  ├─────────────────┼──────────┼──────────┼──────────┼────────┤
  │ CAST            │ 12K gates│ 15 uW    │ 110 clk  │ $25K   │
  │ CryptoTech      │ 8K gates │ 8 uW     │ 160 clk  │ $40K   │
  │ In-house design │ 10K gates│ 12 uW    │ 110 clk  │ $50K   │
  └─────────────────┴──────────┴──────────┴──────────┴────────┘

  SELECTED: In-house AES-128 implementation
  Rationale:
    Full control over implementation for medical certification
    Can add hardware tamper detection
    Key storage in eFuse with secure erase
    No third-party IP liability in safety-critical path
    Telemetry rate (1-2 kbps) makes latency non-critical

  AES-128 Architecture (simplified):
  ┌──────────────────────────────────────────────────────────┐
  │  128-bit Data Input                                      │
  │       │                                                  │
  │       v                                                  │
  │  ┌──────────┐   ┌──────────┐   ┌──────────┐           │
  │  │ SubBytes │-->│ ShiftRow │-->│ MixCol   │-->┐        │
  │  │ (S-box)  │   │          │   │ (10 rnd) │   │        │
  │  └──────────┘   └──────────┘   └──────────┘   │        │
  │       ^                                         │         │
  │       │         ┌──────────┐                   │         │
  │       └────────-│AddRndKey │<-------------------┘        │
  │                 └──────────┘                              │
  │       │                                                  │
  │       v                                                  │
  │  128-bit Data Output                                     │
  │                                                          │
  │  Key Schedule: 10 round keys from master key             │
  │  Area: ~10K gates                                        │
  │  Throughput: ~1 Mbit/s @ 1MHz clock                      │
  │  Power: 12 uW @ 1.5V, 1MHz                               │
  └──────────────────────────────────────────────────────────┘
```

### 5.2 CRC-16 Engine

```
CRC-16 for Telemetry Error Detection:

  Polynomial: x^16 + x^15 + x^2 + 1 (CRC-16-IBM, 0x8005)
  Implementation: LFSR (Linear Feedback Shift Register)

  ┌────┬────┬────┬────┬────┬────┬────┬────┐
  │ FF0│ FF1│ FF2│ FF3│ FF4│ FF5│ FF6│ FF7│
  └──┬─┴──┬─┴──┬─┴──┬─┴──┬─┴──┬─┴──┬─┴──┬─┘
     │    │    │    │    │    │    │    │
     └──┬─┘    │    └──┬─┘    │    └──┬─┘
        │XOR   │       │XOR   │       │XOR
  ┌─────┘      └───────┘      └───────┘
  │ Data In                    CRC Out (16 bits)
  │ (serial)                   │
  │                            v
  │  ┌────┬────┬────┬────┬────┬────┬────┬────┐
  │  │FF8 │ FF9│FF10│FF11│FF12│FF13│FF14│FF15│
  │  └────┴────┴────┴────┴────┴────┴────┴────┘

  Gate count: ~150 gates (16 flip-flops + XOR network)
  Throughput: 1 bit/clock (serial) or 8/16 bits/clock (parallel)
  Area: ~0.005 mm2
```

### 5.3 Standard Platform IP

```
Platform IP Licensed from Foundry (TSMC):

┌──────────────────┬────────────┬────────────────────────────┐
│ IP Block         │ Source     │ Notes                      │
├──────────────────┼────────────┼────────────────────────────┤
│ Standard Cell Lib│ TSMC       │ tcbn180ghp (HVT/SVT/LVT)  │
│ I/O Cell Library  │ TSMC       │ tpdn18ghp (3.3V)          │
│ SRAM Compiler     │ TSMC       │ Embedded RAM compiler      │
│ eFuse Macro       │ TSMC       │ 256-bit, one-time prog     │
│ Pad Library       │ TSMC       │ Wire bond pads             │
│ ESD Clamp         │ TSMC       │ Power clamp cells          │
└──────────────────┴────────────┴────────────────────────────┘

SRAM Compiler Configurations:
  Instance 1: Parameters SRAM
    Size: 256 x 64 bits = 2 KB
    Type: 1R1W (dual-port)
    ECC: SECDED (7-bit Hamming)
    Technology: 12T RHBD cell
    Area: ~0.12 mm2

  Instance 2: Data Buffer SRAM
    Size: 128 x 64 bits = 1 KB
    Type: 1RW (single-port)
    ECC: SECDED
    Technology: 12T RHBD cell
    Area: ~0.06 mm2

  Instance 3: Stack/Temp SRAM
    Size: 128 x 64 bits = 1 KB
    Type: 1RW (single-port)
    ECC: Parity only
    Technology: 8T standard cell (lower area)
    Area: ~0.04 mm2
```

## 6. IP Integration Plan

### 6.1 Block-Level IP Map

```
iPACE-CHIP IP Integration Map:
═══════════════════════════════════════════════════════════════

┌────────────────────────────────────────────────────────────────┐
│                     iPACE-CHIP Top Level                        │
│                                                                │
│  ┌──────────────────────────────────────────────────────┐     │
│  │                ANALOG SUBSYSTEM                        │     │
│  │  ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ ┌──────────────┐ │     │
│  │  │ LNA │►│ VGA │►│ BPF │►│ SAR │  │ Bandgap Ref  │ │     │
│  │  │CUST │ │CUST │ │CUST │ │ADC  │  │ CUST         │ │     │
│  │  └─────┘ └─────┘ └─────┘ │CUST │  └──────────────┘ │     │
│  │                           └─────┘                    │     │
│  │  ┌─────┐ ┌──────┐ ┌────────────┐ ┌──────────────┐  │     │
│  │  │XOSC │ │ LDO  │ │Output Drv A│ │Output Drv B  │  │     │
│  │  │CUST │ │CUST  │ │CUST        │ │CUST          │  │     │
│  │  └─────┘ └──────┘ └────────────┘ └──────────────┘  │     │
│  │  ┌──────────────┐ ┌──────────────┐ ┌────────────┐  │     │
│  │  │Current Sense │ │Telemetry Coil│ │Brownout Det│  │     │
│  │  │CUST          │ │Driver CUST   │ │CUST        │  │     │
│  │  └──────────────┘ └──────────────┘ └────────────┘  │     │
│  └──────────────────────────────────────────────────────┘     │
│                                                                │
│  ┌──────────────────────────────────────────────────────┐     │
│  │                DIGITAL SUBSYSTEM                       │     │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────────────────┐ │     │
│  │  │Pacing FSM│ │Sensing   │ │AES-128 Engine        │ │     │
│  │  │ IN-HOUSE │ │Engine    │ │ IN-HOUSE             │ │     │
│  │  │          │ │ IN-HOUSE │ └──────────────────────┘ │     │
│  │  └──────────┘ └──────────┘                          │     │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────────────────┐ │     │
│  │  │Timer/    │ │Telemetry │ │CRC-16 Engine         │ │     │
│  │  │Counter   │ │UART      │ │ IN-HOUSE             │ │     │
│  │  │ IN-HOUSE │ │ IN-HOUSE │ └──────────────────────┘ │     │
│  │  └──────────┘ └──────────┘                          │     │
│  │  ┌──────────────────┐ ┌──────────────────────────┐ │     │
│  │  │Parameter Store   │ │Watchdog Timer             │ │     │
│  │  │IN-HOUSE + ECC    │ │ IN-HOUSE                 │ │     │
│  │  └──────────────────┘ └──────────────────────────┘ │     │
│  └──────────────────────────────────────────────────────┘     │
│                                                                │
│  ┌──────────────────────────────────────────────────────┐     │
│  │                MEMORY                                  │     │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐             │     │
│  │  │ROM 1KB   │ │SRAM 2KB  │ │SRAM 2KB  │             │     │
│  │  │TSMC      │ │TSMC ECC  │ │TSMC ECC  │             │     │
│  │  └──────────┘ └──────────┘ └──────────┘             │     │
│  └──────────────────────────────────────────────────────┘     │
│                                                                │
│  ┌──────────────────────────────────────────────────────┐     │
│  │                PROCESS IP (TSMC)                       │     │
│  │  Standard Cells | IO Cells | eFuse | ESD Clamps      │     │
│  └──────────────────────────────────────────────────────┘     │
└────────────────────────────────────────────────────────────────┘
```

## 7. IP Quality Assessment

### 7.1 Verification Checklist for Each IP Block

```
IP Qualification Checklist:
═══════════════════════════════════════════════════════════════

┌────┬─────────────────────────────┬──────┬──────┬──────┬──────┐
│ #  │ Criterion                   │ LNA  │ AES  │ SRAM │ XOSC │
├────┼─────────────────────────────┼──────┼──────┼──────┼──────┤
│ 1  │ Functional spec complete    │ YES  │ YES  │ YES  │ YES  │
│ 2  │ RTL/code review passed      │ YES  │ YES  │ N/A  │ N/A  │
│ 3  │ Gate simulation passed      │ YES  │ YES  │ N/A  │ N/A  │
│ 4  │ SPICE simulation (corners)  │ YES  │ N/A  │ YES  │ YES  │
│ 5  │ Layout completed            │ YES  │ YES  │ YES  │ YES  │
│ 6  │ DRC clean                   │ YES  │ YES  │ YES  │ YES  │
│ 7  │ LVS clean                   │ YES  │ YES  │ YES  │ YES  │
│ 8  │ Post-layout sim passed      │ YES  │ YES  │ YES  │ YES  │
│ 9  │ Power analysis completed    │ YES  │ YES  │ YES  │ YES  │
│ 10 │ Radiation analysis          │ YES  │ YES  │ YES  │ YES  │
│ 11 │ Reliability analysis        │ YES  │ YES  │ YES  │ YES  │
│ 12 │ Documentation complete      │ YES  │ YES  │ YES  │ YES  │
│ 13 │ Integration test passed     │ PEND │ PEND │ PEND │ PEND │
│ 14 │ DFT coverage >= 95%        │ YES  │ YES  │ N/A  │ N/A  │
│ 15 │ Safety review passed        │ PEND │ PEND │ PEND │ PEND │
└────┴─────────────────────────────┴──────┴──────┴──────┴──────┘
```

## 8. Cost Summary

```
IP Cost Summary for iPACE-CHIP:
═══════════════════════════════════════════════════════════════

┌────────────────────┬────────────┬─────────────┬─────────────┐
│ IP Category        │ One-Time   │ Per-Unit    │ Total       │
│                    │ Cost (NRE) │ Cost (at 1K)│ (at 1K)     │
├────────────────────┼────────────┼─────────────┼─────────────┤
│ PDK License (TSMC) │ $50K       │ $0.20/wafer │ $2/wafer    │
│ Standard Cell Lib  │ Included   │ $0          │ $0          │
│ SRAM Compiler      │ $20K       │ $0.50/chip  │ $500        │
│ eFuse Macro        │ $10K       │ $0.10/chip  │ $100        │
│ I/O Library        │ $15K       │ $0.15/chip  │ $150        │
│ Custom Analog (12) │ $800K NRE  │ $0          │ $800K       │
│ Custom Digital     │ $500K NRE  │ $0          │ $500K       │
│ DFT Infrastructure │ $50K NRE   │ $0          │ $50K        │
│ Verification       │ $200K NRE  │ $0          │ $200K       │
├────────────────────┼────────────┼─────────────┼─────────────┤
│ TOTAL NRE          │ ~$1.645M   │             │             │
│ Per-unit IP cost   │            │ ~$0.75      │             │
└────────────────────┴────────────┴─────────────┴─────────────┘

  Note: At medical device volumes (100-1000/year), the per-unit
  cost is dominated by wafer cost and packaging, not IP licensing.
  Total chip cost (all-in) estimated at $15-25 per unit at 1K volume.
```

## 9. Risk Assessment

```
IP Selection Risk Matrix:

┌──────────────────────┬────────────┬────────────┬──────────────┐
│ Risk                 │ Likelihood │ Impact     │ Mitigation   │
├──────────────────────┼────────────┼────────────┼──────────────┤
│ SRAM compiler issues │ Low        │ High       │ Pre-silicon  │
│ (ECC not working)    │            │            │ BIST + sim   │
├──────────────────────┼────────────┼────────────┼──────────────┤
│ LNA noise exceeds    │ Medium     │ High       │ Chopper +    │
│ spec                 │            │            │ auto-calib   │
├──────────────────────┼────────────┼────────────┼──────────────┤
│ Output driver stress │ Low        │ Critical   │ Derate 2x,   │
│ (reliability)        │            │            │ redundant    │
├──────────────────────┼────────────┼────────────┼──────────────┤
│ eFuse reliability    │ Low        │ Medium     │ Use only for │
│                      │            │            │ non-critical  │
├──────────────────────┼────────────┼────────────┼──────────────┤
│ PDK model accuracy   │ Low        │ High       │ Wafer shuttle│
│                      │            │            │ test chip    │
├──────────────────────┼────────────┼────────────┼──────────────┤
│ XOSC start failure   │ Low        │ Critical   │ RC backup +  │
│                      │            │            │ restart seq  │
└──────────────────────┴────────────┴────────────┴──────────────┘
```

## 10. Summary

IP selection for iPACE-CHIP prioritizes **safety and control** over cost and development
speed. Key decisions:

- **12 custom analog blocks** designed in-house for full control of medical-critical specs
- **AES-128 and CRC-16** designed in-house to avoid third-party liability
- **Process IP (TSMC 180nm PDK)** provides standard cells, SRAM, and eFuse
- **No third-party soft IP** in safety-critical signal path
- Total NRE for IP: ~$1.65M, per-unit IP cost: ~$0.75

---

*Previous: [Architecture Tradeoffs](../03-Architecture-Tradeoffs/architecture-tradeoffs.md)*
