# Technology Node Selection for Pacemaker SoC

## 2.1.4 Process Technology Evaluation and Selection

The selection of the semiconductor process technology node is one of the most
consequential decisions in the pacemaker SoC design. It directly impacts die
area, power consumption, cost, reliability, mixed-signal performance, and
time-to-market. This chapter provides a comprehensive evaluation of process
nodes from 180 nm to 40 nm, analyzing the trade-offs specific to
ultra-low-power medical implant applications.

---

## 2.4.1 Process Node Overview

Modern CMOS process nodes range from 180 nm (mature, high-voltage capable)
to 40 nm (advanced, high integration). Each node offers different advantages
for pacemaker SoC design:

| Node | Year Introduced | Min Gate Length | Min Supply Voltage | Max Metal Layers | Typical Foundry |
|------|----------------|----------------|-------------------|-----------------|----------------|
| 180 nm | 1999 | 0.18 µm | 1.8 V | 6 | TSMC, UMC, GlobalFoundries |
| 130 nm | 2001 | 0.13 µm | 1.2 V | 8 | TSMC, UMC, IBM |
| 90 nm | 2004 | 90 nm | 1.0 V | 9 | TSMC, UMC, Intel |
| 65 nm | 2006 | 65 nm | 0.9 V | 10 | TSMC, UMC, GlobalFoundries |
| 55 nm | 2008 | 55 nm | 0.8 V | 10 | TSMC, UMC |
| 40 nm | 2009 | 40 nm | 0.7 V | 12 | TSMC, GlobalFoundries |

---

## 2.4.2 Detailed Node Comparison

### 180 nm CMOS

**Process Characteristics:**
- Gate oxide thickness: 4.0-7.0 nm (dual oxide: thin for logic, thick for I/O)
- Supply voltage: 1.8 V core, 3.3 V I/O
- Threshold voltage: ~400 mV (standard), ~250 mV (low-Vt)
- Metal stack: 4-6 metal layers (Aluminum or Copper)
- Well-known, mature process with >20 years of production history

**Advantages for Pacemaker:**
- **High-voltage capability**: Native 3.3 V I/O transistors support direct
  connection to 3.3 V battery and pacing output stage without level shifting.
- **Excellent analog performance**: Thick gate oxide provides lower gate
  leakage (< 1 pA/µm), higher breakdown voltage, and better matching for
  analog circuits.
- **Mature design tools and PDKs**: Extensive characterization data,
  well-understood models, and large library of standard cells and IP.
- **Low cost**: $2,000-5,000 per mask set; $500-1,000 per wafer (200 mm).
- **Radiation tolerance**: Larger feature sizes provide inherently higher
  tolerance to single-event effects (SEE) and total ionizing dose (TID).

**Disadvantages:**
- **Large die area**: Digital logic density is ~100K gates/mm², compared to
  ~500K gates/mm² at 65 nm. A complex digital controller may require
  3-5 mm² of digital area.
- **Higher dynamic power**: Higher supply voltage (1.8 V vs. 0.9 V) results
  in 4× higher dynamic power for the same switching activity.
- **Limited integration**: Cannot easily integrate large SRAM blocks (> 16 KB)
  without significant area penalty.

**Pacemaker-Specific Considerations:**
- Ideal for simple pacemakers (VVI, AAI) with minimal digital complexity.
- Well-suited for the pacing output stage and high-voltage charge pump.
- Used in many production pacemakers from the 2000-2015 era.

### 130 nm CMOS

**Process Characteristics:**
- Gate oxide thickness: 2.0-5.0 nm (dual oxide)
- Supply voltage: 1.2 V core, 2.5 V I/O
- Threshold voltage: ~350 mV (standard), ~200 mV (low-Vt)
- Metal stack: 6-8 metal layers

**Advantages for Pacemaker:**
- **Better digital density**: ~200K gates/mm² enables more complex digital
  controllers and larger on-chip memory.
- **Lower dynamic power**: 1.2 V core supply reduces dynamic power by ~56%
  compared to 180 nm.
- **Mixed-signal sweet spot**: Good balance between analog and digital
  performance. Many medical device companies standardized on 130 nm for
  implantable devices.
- **Moderate cost**: $5,000-10,000 per mask set; $600-1,200 per wafer.

**Disadvantages:**
- **I/O voltage limitation**: 2.5 V I/O may not support direct connection to
  3.3 V battery without level shifting or thick-oxide I/O transistors.
- **Increased leakage**: Gate leakage becomes more significant with thinner
  oxide, impacting standby power.

**Pacemaker-Specific Considerations:**
- Used in many production pacemakers from the 2010-2020 era.
- Good balance of analog and digital performance for dual-chamber pacemakers.
- Supports integration of 8-32 KB SRAM on-chip.

### 90 nm CMOS

**Process Characteristics:**
- Gate oxide thickness: 1.2-4.0 nm (multi-oxide)
- Supply voltage: 1.0 V core, 1.8/2.5 V I/O
- Threshold voltage: ~300 mV (standard), ~180 mV (low-Vt), ~150 mV (ultra-low-Vt)
- Metal stack: 8-9 metal layers

**Advantages for Pacemaker:**
- **High digital density**: ~400K gates/mm² enables complex digital signal
  processing and larger on-chip memory (64-128 KB SRAM).
- **Low dynamic power**: 1.0 V core supply reduces dynamic power by ~69%
  compared to 180 nm.
- **Advanced IP availability**: Many analog and digital IP blocks are
  available at 90 nm (PLLs, ADCs, DACs, standard cell libraries).
- **Good mixed-signal performance**: Supports high-resolution ADCs (12-16 bit)
  and DACs (10-12 bit) with good matching.

**Disadvantages:**
- **Increased leakage**: Sub-threshold leakage becomes significant at 90 nm,
  especially with low-Vt transistors. Standby power may be 2-5× higher than
  130 nm for the same functionality.
- **Higher cost**: $10,000-20,000 per mask set; $800-1,500 per wafer.
- **Analog design complexity**: Reduced supply voltage headroom makes analog
  circuit design more challenging, especially for high-precision references
  and amplifiers.

**Pacemaker-Specific Considerations:**
- Used in advanced pacemakers with rate-adaptive features and enhanced
  diagnostics.
- Supports integration of 32-128 KB SRAM for electrogram storage.
- May require power gating to manage standby leakage.

### 65 nm CMOS

**Process Characteristics:**
- Gate oxide thickness: 1.0-3.5 nm (multi-oxide, including thick-oxide for I/O)
- Supply voltage: 0.9 V core, 1.8/2.5 V I/O
- Threshold voltage: ~280 mV (standard), ~160 mV (low-Vt), ~120 mV (ultra-low-Vt)
- Metal stack: 9-10 metal layers (Cu/low-k)

**Advantages for Pacemaker:**
- **Highest digital density**: ~800K gates/mm² enables highly integrated
  SoC with complex digital controllers, large memory, and hardware accelerators.
- **Lowest dynamic power**: 0.9 V core supply reduces dynamic power by ~75%
  compared to 180 nm.
- **Advanced features**: Supports embedded flash (for non-volatile parameter
  storage), SRAM (for working memory), and mixed-signal IP.
- **Excellent cost per gate**: Despite higher mask cost, the cost per
  functional gate is lower than 130 nm for complex designs.

**Disadvantages:**
- **Significant leakage**: Sub-threshold and gate leakage are major concerns.
  Standby power may be 5-10× higher than 130 nm without power gating.
- **Analog design challenges**: 0.9 V supply voltage severely limits analog
  signal swing and headroom. Requires advanced techniques (chopper
  stabilization, correlated double sampling) for precision analog circuits.
- **Higher cost**: $20,000-40,000 per mask set; $1,000-2,000 per wafer.
- **ESD sensitivity**: Thinner oxides are more susceptible to ESD damage,
  requiring more robust ESD protection circuits.

**Pacemaker-Specific Considerations:**
- Used in next-generation pacemakers with wireless telemetry, advanced
  diagnostics, and rate-adaptive algorithms.
- Requires aggressive power gating to manage leakage in sleep modes.
- Supports integration of 256 KB-1 MB SRAM for comprehensive diagnostic
  data storage.

### 55 nm CMOS

**Process Characteristics:**
- Gate oxide thickness: 0.9-3.0 nm (multi-oxide)
- Supply voltage: 0.8 V core, 1.8/2.5 V I/O
- Metal stack: 10 metal layers

**Advantages for Pacemaker:**
- **Enhanced digital density**: ~1.2M gates/mm² enables even more complex
  digital processing and larger memory.
- **Ultra-low dynamic power**: 0.8 V core supply further reduces dynamic
  power.
- **Cost-effective for high-volume**: Good balance of performance and cost
  for medium-to-high volume medical devices.

**Disadvantages:**
- **Analog design severely constrained**: 0.8 V supply makes high-performance
  analog design extremely challenging. Many traditional analog topologies
  cannot be used.
- **Leakage management critical**: Requires sophisticated power gating and
  retention techniques.
- **Limited foundry support**: Fewer foundries offer 55 nm processes with
  medical-grade qualification.

**Pacemaker-Specific Considerations:**
- May be suitable for highly integrated pacemaker-ICD hybrid devices.
- Requires custom analog IP development (not available from standard PDKs).
- Not commonly used in production pacemakers as of 2024.

### 40 nm CMOS

**Process Characteristics:**
- Gate oxide thickness: 0.8-2.5 nm (multi-oxide, including high-K dielectric
  options)
- Supply voltage: 0.7 V core, 1.8/2.5 V I/O
- Metal stack: 10-12 metal layers (Cu/low-k)

**Advantages for Pacemaker:**
- **Highest integration**: ~2M gates/mm² enables full SoC integration with
  advanced digital processing, large memory, and complex RF circuits.
- **Lowest dynamic power**: 0.7 V core supply provides the lowest dynamic
  power per gate.
- **Advanced features**: Supports embedded MRAM or FeRAM for non-volatile
  storage, high-speed I/O, and advanced RF circuits.

**Disadvantages:**
- **Extreme analog design challenges**: 0.7 V supply makes precision analog
  design extremely difficult. Requires innovative circuit techniques.
- **Highest leakage**: Sub-threshold leakage is the dominant power contributor
  in standby mode. Requires aggressive power gating with state retention.
- **Highest cost**: $40,000-80,000 per mask set; $1,500-3,000 per wafer.
- **Reliability concerns**: Thinner oxides have higher defect density and
  lower breakdown margins. Requires extensive reliability testing.
- **NRE cost**: Non-recurring engineering cost of $5-15M for a complete
  SoC design at 40 nm.

**Pacemaker-Specific Considerations:**
- Not commonly used for discrete pacemakers due to cost and analog challenges.
- May be suitable for highly integrated cardiac rhythm management (CRM)
  systems that combine pacing, sensing, and advanced signal processing.
- Future pacemaker designs may adopt 40 nm or below as analog design
  methodologies mature.

---

## 2.4.3 Process Selection Matrix

| Criterion | Weight | 180 nm | 130 nm | 90 nm | 65 nm | 55 nm | 40 nm |
|-----------|--------|--------|--------|-------|-------|-------|-------|
| Digital density | 15% | 3 | 5 | 7 | 9 | 9 | 10 |
| Dynamic power | 20% | 4 | 6 | 7 | 9 | 9 | 10 |
| Leakage power | 15% | 9 | 8 | 6 | 4 | 3 | 2 |
| Analog performance | 20% | 10 | 9 | 7 | 5 | 3 | 2 |
| Cost (mask + wafer) | 10% | 10 | 8 | 6 | 4 | 3 | 2 |
| NRE cost | 10% | 10 | 8 | 6 | 4 | 3 | 2 |
| Reliability | 10% | 9 | 8 | 7 | 6 | 5 | 4 |
| **Weighted Score** | **100%** | **6.75** | **7.25** | **6.70** | **6.25** | **5.25** | **4.70** |

**Scoring: 1 = Worst, 10 = Best**

### Recommended Node by Application

| Application | Recommended Node | Justification |
|------------|-----------------|---------------|
| Simple VVI pacemaker | 180 nm | High voltage, low cost, simple design |
| Dual-chamber DDD pacemaker | 130 nm | Best balance of analog/digital, proven reliability |
| DDDR with rate adaptation | 130 nm or 90 nm | Higher digital complexity, moderate power |
| Pacemaker with wireless telemetry | 90 nm or 65 nm | High digital density, low power, RF integration |
| Next-gen CRM system | 65 nm or 55 nm | Maximum integration, advanced features |
| Future multi-function device | 40 nm | Ultimate integration, lowest power per function |

---

## 2.4.4 Mixed-Signal Design Considerations

The pacemaker SoC is inherently a mixed-signal design, requiring both
high-performance analog circuits (AFE, output stage, references) and
complex digital circuits (controller, timers, memory). The process node
selection must balance the requirements of both domains.

### Analog Design Constraints by Node

| Parameter | 180 nm | 130 nm | 90 nm | 65 nm |
|-----------|--------|--------|-------|-------|
| Supply voltage | 1.8 V | 1.2 V | 1.0 V | 0.9 V |
| Max signal swing | 1.6 Vpp | 1.0 Vpp | 0.8 Vpp | 0.7 Vpp |
| Gate leakage (per µm) | < 0.1 pA | < 1 pA | < 10 pA | < 100 pA |
| Offset voltage (matched) | < 5 mV | < 3 mV | < 2 mV | < 1.5 mV |
| 1/f noise (flicker) | Low | Medium | High | Very High |
| Matching (σ_Vth) | ~5 mV | ~4 mV | ~3 mV | ~2.5 mV |
| Breakdown voltage | > 3.6 V | > 2.4 V | > 2.0 V | > 1.8 V |

### Analog Design Techniques by Node

**180 nm:**
- Traditional analog topologies (telescopic cascode, folded cascode)
- Direct battery connection possible
- Chopper stabilization optional (low 1/f noise)
- Simple references (bandgap, constant-gm)

**130 nm:**
- Modified analog topologies for reduced supply
- Level shifting required for battery connection
- Chopper stabilization recommended
- Advanced references (curvature-corrected bandgap)

**90 nm:**
- Low-voltage analog topologies (current-starved, inverter-based)
- Extensive use of chopper stabilization and auto-zeroing
- Digital calibration for analog imperfections
- Sub-threshold biasing for ultra-low-power analog circuits

**65 nm:**
- Ultra-low-voltage analog techniques (sub-threshold operation)
- Digital-intensive analog (sigma-delta ADCs, digitally calibrated DACs)
- Extensive use of power gating for analog blocks
- Requires custom analog IP (not available from standard PDK)

### Substrate Noise Isolation

Mixed-signal SoCs require careful substrate noise isolation to prevent
digital switching noise from degrading analog performance. Techniques
include:

1. **Guard rings**: Deep n-well and p+ guard rings around sensitive analog
   circuits. At 130 nm and below, deep trench isolation may be required.

2. **Separate supply domains**: Independent VDD/VSS domains for analog and
   digital circuits, with separate bond pads and package pins.

3. **Substrate ties**: Dedicated substrate tie-down connections to minimize
   substrate voltage variations.

4. **Layout isolation**: Physical separation between analog and digital
   circuits (≥ 50 µm at 180 nm, ≥ 100 µm at 65 nm).

5. **Shielding**: Metal shielding layers over sensitive analog routing to
   prevent capacitive coupling from digital signal lines.

---

## 2.4.5 Cost Analysis

### Mask Set Cost

| Node | Mask Set Cost | Turnaround Time | Mask Count |
|------|--------------|----------------|-----------|
| 180 nm | $2,000-5,000 | 4-6 weeks | 35-45 |
| 130 nm | $5,000-10,000 | 6-8 weeks | 45-55 |
| 90 nm | $10,000-20,000 | 8-10 weeks | 55-65 |
| 65 nm | $20,000-40,000 | 10-12 weeks | 65-80 |
| 55 nm | $30,000-60,000 | 12-14 weeks | 70-85 |
| 40 nm | $40,000-80,000 | 14-16 weeks | 80-100 |

### Wafer Cost

| Node | Wafer Diameter | Cost per Wafer | Good Die per Wafer | Cost per Die |
|------|---------------|---------------|-------------------|-------------|
| 180 nm | 200 mm | $500-1,000 | 400-600 | $1-2 |
| 130 nm | 200 mm | $600-1,200 | 500-800 | $1-2 |
| 90 nm | 200 mm | $800-1,500 | 800-1,200 | $1-2 |
| 65 nm | 200 mm | $1,000-2,000 | 1,200-2,000 | $1-2 |
| 55 nm | 300 mm | $1,500-3,000 | 2,000-3,000 | $1-2 |
| 40 nm | 300 mm | $2,000-4,000 | 3,000-5,000 | $1-1 |

### Total Development Cost

| Cost Category | 180 nm | 130 nm | 90 nm | 65 nm |
|--------------|--------|--------|-------|-------|
| Mask set | $5K | $10K | $20K | $40K |
| Wafer (first lot, 25 wafers) | $20K | $25K | $30K | $40K |
| Packaging (per unit) | $5-10 | $5-10 | $5-10 | $5-10 |
| Test (per unit) | $20-50 | $20-50 | $20-50 | $20-50 |
| NRE (design, verification) | $1-2M | $2-4M | $4-8M | $8-15M |
| Qualification | $0.5-1M | $1-2M | $2-3M | $3-5M |
| **Total NRE** | **$1.5-3M** | **$3-6M** | **$6-11M** | **$11-20M** |

---

## 2.4.6 Reliability Considerations

### Oxide Reliability

| Parameter | 180 nm | 130 nm | 90 nm | 65 nm |
|-----------|--------|--------|-------|-------|
| Gate oxide thickness (core) | 4.0 nm | 2.5 nm | 1.5 nm | 1.2 nm |
| TDDB lifetime (10 years, 125°C) | > 100 years | > 50 years | > 20 years | > 10 years |
| Hot carrier lifetime | > 100 years | > 50 years | > 30 years | > 15 years |
| ESD tolerance (HBM) | > 4 kV | > 4 kV | > 2 kV | > 2 kV |
| ESD tolerance (CDM) | > 500 V | > 500 V | > 250 V | > 250 V |

### Single-Event Effects (SEE)

| Parameter | 180 nm | 130 nm | 90 nm | 65 nm |
|-----------|--------|--------|-------|-------|
| Critical charge (Qcrit) | > 100 fC | > 50 fC | > 20 fC | > 10 fC |
| SEE cross-section | Very low | Low | Medium | High |
| SEL susceptibility | Low | Low | Medium | Medium |
| Mitigation required | None | None | EDAC, TMR | EDAC, TMR, SCR |

### Total Ionizing Dose (TID)

| Parameter | 180 nm | 130 nm | 90 nm | 65 nm |
|-----------|--------|--------|-------|-------|
| TID tolerance (unhardened) | > 100 krad | > 50 krad | > 30 krad | > 20 krad |
| TID tolerance (hardened) | > 1 Mrad | > 500 krad | > 200 krad | > 100 krad |
| Enclosed layout transistors | Recommended | Recommended | Required | Required |

### Pacemaker Reliability Requirements

The pacemaker must operate for ≥ 10 years in the human body environment
(37°C, saline). Key reliability considerations:

1. **Electromigration**: At 65 nm and below, electromigration becomes a
   concern for high-current paths (pacing output, charge pump). Requires
   conservative current density limits (< 1 MA/cm²) and redundancy.

2. **Hot carrier injection (HCI)**: Thinner oxides are more susceptible to
   HCI degradation. Must ensure that all transistors operate well within
   safe operating areas over the 10-year lifetime.

3. **Negative bias temperature instability (NBTI)**: PMOS threshold voltage
   shifts under negative gate bias at elevated temperature. Must account
   for NBTI-induced offset in analog circuits.

4. **Time-dependent dielectric breakdown (TDDB)**: Thinner oxides have
   lower breakdown margins. Must ensure that the maximum voltage across
   any oxide is well below the breakdown voltage.

---

## 2.4.7 Foundry Selection

### Major Foundries for Medical Implant SoCs

| Foundry | Nodes Available | Medical Qualification | DFM Support | IP Availability |
|---------|----------------|----------------------|------------|-----------------|
| TSMC | 180 nm to 5 nm | Yes (multiple qualifications) | Excellent | Extensive |
| UMC | 180 nm to 22 nm | Yes | Good | Good |
| GlobalFoundries | 180 nm to 22 nm | Yes | Good | Good |
| Samsung | 180 nm to 5 nm | Limited | Good | Good |
| X-FAB | 180 nm to 130 nm | Yes (specialty) | Good | Analog-focused |
| SK Hynix | 180 nm to 65 nm | Limited | Moderate | Limited |

### Medical Device Qualification

Foundries offering medical device qualification programs:

1. **TSMC**: Offers a comprehensive qualification program for medical
   devices, including accelerated life testing (ALT), highly accelerated
   stress testing (HAST), and moisture sensitivity level (MSL) testing.
   TSMC's process qualification data includes TDDB, HCI, NBTI, and
   electromigration characterization.

2. **GlobalFoundries**: Offers a medical device qualification program with
   extended reliability testing. Particularly strong at 65 nm and 55 nm
   for mixed-signal applications.

3. **X-FAB**: Specializes in analog/mixed-signal processes at 180 nm and
   130 nm. Offers a dedicated medical device qualification program with
   extended temperature range testing.

### Foundry Recommendation

For a production pacemaker SoC, **TSMC 130 nm** (e.g., TSMC 130 nm
mixed-signal/RF process) is recommended as the baseline technology due to:

1. Proven reliability track record in medical implants
2. Comprehensive qualification data available
3. Good balance of analog and digital performance
4. Moderate cost ($3-6M NRE)
5. Extensive IP ecosystem (standard cells, memory compilers, analog IP)
6. Strong DFM support for mixed-signal designs

For next-generation designs requiring higher integration, **TSMC 65 nm
low-power** process is recommended, with careful attention to leakage
management and analog design challenges.

---

## 2.4.8 Design Kit and IP Ecosystem

### Required IP Blocks

| IP Block | 180 nm | 130 nm | 90 nm | 65 nm |
|----------|--------|--------|-------|-------|
| Standard cell library | Yes | Yes | Yes | Yes |
| SRAM compiler | Yes (up to 64 KB) | Yes (up to 256 KB) | Yes (up to 1 MB) | Yes (up to 4 MB) |
| ROM compiler | Yes | Yes | Yes | Yes |
| I/O library (3.3V) | Yes | Yes (2.5V) | Yes (1.8V) | Yes (1.8V) |
| High-voltage I/O | Yes (5V) | Yes (3.3V) | Limited | No |
| PLL/DLL | Yes | Yes | Yes | Yes |
| ADC (SAR) | 10-bit | 12-bit | 12-bit | 14-bit |
| DAC | 10-bit | 12-bit | 12-bit | 14-bit |
| Bandgap reference | Yes | Yes | Yes | Yes |
| LDO regulator | Yes | Yes | Yes | Yes |
| DC-DC converter | External | On-chip option | On-chip | On-chip |
| RF transceiver | External | External/MICS | On-chip MICS | On-chip MICS |
| ESD protection | Yes | Yes | Yes | Yes |
| EEPROM (emulated) | Yes | Yes | Yes | Flash/MRAM |

---

## 2.4.9 Summary

The technology node selection for the pacemaker SoC is driven by the
following key factors:

1. **Application complexity**: Simple VVI pacemakers can use 180 nm, while
   complex DDDR pacemakers with wireless telemetry require 130 nm or 90 nm.

2. **Power budget**: The 10-year battery life target requires aggressive
   power optimization, favoring nodes with low supply voltage (90 nm and
   below) but requiring careful leakage management.

3. **Analog performance**: The AFE requires high-precision analog circuits
   with low noise and good matching, favoring mature nodes (180 nm, 130 nm)
   with thicker gate oxide and higher supply voltage.

4. **Cost**: The total development cost (NRE + mask + wafers + qualification)
   must be justified by the expected production volume and product lifetime.

5. **Reliability**: The 10-year implant lifetime in the body environment
   requires proven oxide reliability and radiation tolerance, favoring
   mature, well-characterized processes.

**Primary recommendation**: 130 nm CMOS for current-generation dual-chamber
pacemakers, offering the best balance of analog performance, digital density,
power, cost, and reliability.

**Future direction**: 65 nm CMOS for next-generation pacemakers with advanced
digital features, wireless telemetry, and enhanced diagnostics, with careful
attention to leakage management and analog design challenges.
