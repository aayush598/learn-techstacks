# DRC/LVS Checks for iPACE-CHIP ASIC

## 1. Introduction

Design Rule Check (DRC) and Layout vs. Schematic (LVS) are the two most critical
physical verification steps before tapeout. DRC ensures the layout can be manufactured
reliably; LVS ensures the layout matches the intended circuit design.

For the iPACE-CHIP, DRC/LVS compliance is non-negotiable:
- A single DRC violation can cause a manufacturing defect → chip failure → patient risk
- An LVS mismatch means the physical chip won't function as designed
- Both must be 100% clean (zero violations) before tapeout authorization

## 2. DRC Methodology

### 2.1 DRC Rule Categories

```
DRC Rule Categories for TSMC 180nm:
═══════════════════════════════════════════════════════════════

  ┌──────────────────────┬──────────────────────────────────────┐
  │ Category             │ Description                          │
  ├──────────────────────┼──────────────────────────────────────┤
  │ Width Rules          │ Minimum width of features per layer  │
  │ Spacing Rules        │ Minimum space between same-layer      │
  │                      │ features                              │
  │ Enclosure Rules      │ One layer must fully enclose another  │
  │ Extension Rules      │ One layer must extend beyond another  │
  │ Area Rules           │ Minimum area of enclosed regions      │
  │ Notch Rules          │ No concave features smaller than min │
  │ Density Rules        │ Metal density within range per layer  │
  │ Via Rules            │ Via size, spacing, enclosure          │
  │ Grid Rules           │ All geometry on manufacturing grid    │
  │ Antenna Rules        │ Metal-to-gate ratio limits            │
  │ Latch-up Rules       │ N-well/p-sub spacing for CMOS        │
  │ ESD Rules            │ ESD device geometry requirements      │
  │ Seal Ring Rules      │ Continuous ring around die edge       │
  └──────────────────────┴──────────────────────────────────────┘
```

### 2.2 Key DRC Rules (Selected)

```
Selected DRC Rules - TSMC 180nm (representative):
═══════════════════════════════════════════════════════════════

  ┌──────┬──────────────────────────┬──────────┬──────────────┐
  │ Rule │ Description              │ Limit    │ iPACE Status │
  ├──────┼──────────────────────────┼──────────┼──────────────┤
  │ W1   │ Min poly width           │ 0.18 µm  │ 0.18 µm PASS │
  │ W2   │ Min M1 width             │ 0.18 µm  │ 0.18 µm PASS │
  │ W3   │ Min M2-M5 width          │ 0.20 µm  │ 0.20 µm PASS │
  │ W4   │ Min M6 (thick) width     │ 0.40 µm  │ 0.40 µm PASS │
  │ S1   │ Min poly spacing         │ 0.18 µm  │ 0.18 µm PASS │
  │ S2   │ Min M1 spacing           │ 0.18 µm  │ 0.18 µm PASS │
  │ S3   │ Min M2-M5 spacing        │ 0.20 µm  │ 0.20 µm PASS │
  │ E1   │ Poly enclosure of active │ 0.09 µm  │ 0.09 µm PASS │
  │ E2   │ M1 enclosure of contact  │ 0.05 µm  │ 0.05 µm PASS │
  │ E3   │ M2 enclosure of via      │ 0.05 µm  │ 0.05 µm PASS │
  │ A1   │ Min active area          │ 0.24 µm² │ 0.24 µm² PASS│
  │ A2   │ Min M1 area              │ 0.10 µm² │ 0.10 µm² PASS│
  │ N1   │ Min poly notch           │ 0.18 µm  │ 0.18 µm PASS │
  │ D1   │ M1 density min           │ 20%      │ 45.2% PASS   │
  │ D2   │ M1 density max           │ 80%      │ 45.2% PASS   │
  │ L1   │ N-well to P-sub spacing  │ 1.0 µm   │ 1.0 µm PASS  │
  │ L2   │ N+ to P+ spacing         │ 0.6 µm   │ 0.6 µm PASS  │
  │ AN1  │ M1 antenna ratio         │ 400      │ 185 PASS     │
  │ AN2  │ Via antenna ratio        │ 500      │ 210 PASS     │
  └──────┴──────────────────────────┴──────────┴──────────────┘
```

## 3. DRC Execution and Results

### 3.1 DRC Run Flow

```
DRC Execution Flow:
═══════════════════════════════════════════════════════════════

  ┌─────────────────────────────────────────────────────────────┐
  │  Step 1: INPUT PREPARATION                                  │
  │     • Load GDS-II file (ipace_chip_top.gds)                │
  │     • Load DRC rule deck (TSMC 180nm)                       │
  │     • Load technology parameters (SPICE models)             │
  │     • Set DRC run options                                   │
  └───────────────────────────┬─────────────────────────────────┘
                              │
  ┌───────────────────────────v─────────────────────────────────┐
  │  Step 2: RULE CHECKING                                      │
  │     • Tool: Calibre DRC / IC Validator / PVS               │
  │     • Execute all applicable rules                         │
  │     • Generate violation database                           │
  │     • Create violation markers on layout                    │
  └───────────────────────────┬─────────────────────────────────┘
                              │
  ┌───────────────────────────v─────────────────────────────────┐
  │  Step 3: VIOLATION ANALYSIS                                 │
  │     • Review each violation                                 │
  │     • Classify: real vs. false positive                     │
  │     • Fix real violations                                   │
  │     • Add waivers for false positives (with documentation)  │
  └───────────────────────────┬─────────────────────────────────┘
                              │
  ┌───────────────────────────v─────────────────────────────────┐
  │  Step 4: RE-RUN DRC                                         │
  │     • After fixes, re-run entire DRC                        │
  │     • Confirm 0 violations                                 │
  │     • Generate clean DRC report                            │
  └───────────────────────────┬─────────────────────────────────┘
                              │
  ┌───────────────────────────v─────────────────────────────────┐
  │  Step 5: DRC SIGNOFF                                        │
  │     • Design lead reviews DRC report                       │
  │     • Safety lead confirms zero violations                  │
  │     • Sign DRC signoff form                                 │
  │     • Archive DRC database and report                      │
  └─────────────────────────────────────────────────────────────┘
```

### 3.2 DRC Results Summary

```
DRC Results - iPACE-CHIP (Final Signoff):
═══════════════════════════════════════════════════════════════

  Tool: Calibre DRC (Mentor/Siemens EDA)
  Rule Deck: TSMC 180nm PDK DRC deck v3.2
  Run Date: 2024-01-15

  ┌─────────────────────────────────────┬──────┬──────────────┐
  │ Category                            │ Count│ Status       │
  ├─────────────────────────────────────┼──────┼──────────────┤
  │ WIDTH violations                    │ 0    │ CLEAN        │
  │ SPACING violations                  │ 0    │ CLEAN        │
  │ ENCLOSURE violations                │ 0    │ CLEAN        │
  │ EXTENSION violations                │ 0    │ CLEAN        │
  │ AREA violations                     │ 0    │ CLEAN        │
  │ NOTCH violations                    │ 0    │ CLEAN        │
  │ DENSITY violations                  │ 0    │ CLEAN        │
  │ VIA violations                      │ 0    │ CLEAN        │
  │ GRID violations                     │ 0    │ CLEAN        │
  │ ANTENNA violations                  │ 0    │ CLEAN        │
  │ LATCHUP violations                  │ 0    │ CLEAN        │
  │ ESD violations                      │ 0    │ CLEAN        │
  │ SEAL RING violations               │ 0    │ CLEAN        │
  │ WELL/SUBSTRATE violations          │ 0    │ CLEAN        │
  │ CROSS-LAYER violations             │ 0    │ CLEAN        │
  ├─────────────────────────────────────┼──────┼──────────────┤
  │ TOTAL DRC VIOLATIONS               │ 0    │ ALL CLEAN    │
  └─────────────────────────────────────┴──────┴──────────────┘

  Rules checked: 2,847
  Rules applicable: 1,245
  Violations found: 0
  DRC Run Time: 45 minutes
  Waivers issued: 0
```

## 4. LVS Methodology

### 4.1 LVS Comparison Strategy

```
LVS Comparison Strategy:
═══════════════════════════════════════════════════════════════

  Source: Gate-level netlist (post-route, extracted from layout)
  Layout: Physical geometry from GDS-II

  LVS Flow:
  ┌─────────────────────────────────────────────────────────────┐
  │  Source Netlist                 Layout Geometry             │
  │  ┌──────────────┐             ┌──────────────┐            │
  │  │ Extract      │             │ Extract      │            │
  │  │ schematic    │             │ layout       │            │
  │  │ netlist      │             │ netlist      │            │
  │  └──────┬───────┘             └──────┬───────┘            │
  │         │                             │                    │
  │         └──────────┬──────────────────┘                    │
  │                    │                                       │
  │           ┌────────▼────────┐                             │
  │           │  LVS COMPARISON │                             │
  │           │                 │                             │
  │           │  Compare:       │                             │
  │           │  • Instances    │                             │
  │           │  • Nets         │                             │
  │           │  • Pin names    │                             │
  │           │  • Devices      │                             │
  │           │  • Parameters   │                             │
  │           └────────┬────────┘                             │
  │                    │                                       │
  │           ┌────────▼────────┐                             │
  │           │  MATCH or       │                             │
  │           │  MISMATCH       │                             │
  │           └─────────────────┘                             │
  └─────────────────────────────────────────────────────────────┘
```

### 4.2 LVS Comparison Rules

```
LVS Rule Categories:
═══════════════════════════════════════════════════════════════

  ┌────────────────────────────┬──────────────────────────────┐
  │ Check                      │ What Is Compared             │
  ├────────────────────────────┼──────────────────────────────┤
  │ Instance Matching          │ Each gate/FF/SRAM must match │
  │                            │ between source and layout    │
  ├────────────────────────────┼──────────────────────────────┤
  │ Net Connectivity           │ All nets must connect the    │
  │                            │ same set of instances        │
  ├────────────────────────────┼──────────────────────────────┤
  │ Pin Matching               │ Each cell's pins must map    │
  │                            │ to correct layout geometry    │
  ├────────────────────────────┼──────────────────────────────┤
  │ Device Parameters          │ W/L ratios must match        │
  │                            │ (within tolerance, typically  │
  │                            │  5% for W, 10% for L)        │
  ├────────────────────────────┼──────────────────────────────┤
  │ Net Name Labels            │ Named nets must be in both   │
  │                            │ source and layout             │
  ├────────────────────────────┼──────────────────────────────┤
  │ Power/Ground Connectivity  │ VDD and VSS must be fully    │
  │                            │ connected in layout           │
  ├────────────────────────────┼──────────────────────────────┤
  │ ERC (Electrical Rules)     │ No floating inputs, no       │
  │                            │ multiple drivers, etc.        │
  └────────────────────────────┴──────────────────────────────┘
```

### 4.3 LVS Results

```
LVS Results - iPACE-CHIP (Final Signoff):
═══════════════════════════════════════════════════════════════

  Tool: Calibre LVS (Mentor/Siemens EDA)
  Rule Deck: TSMC 180nm PDK LVS deck v3.2
  Run Date: 2024-01-15

  ┌─────────────────────────────────────┬──────┬──────────────┐
  │ Comparison Item                     │ Result│ Status      │
  ├─────────────────────────────────────┼──────┼──────────────┤
  │ Top-level cell match                │ YES  │ MATCH        │
  │ Instance count (NMOS)              │ 12,450│ MATCH       │
  │ Instance count (PMOS)              │ 11,800│ MATCH       │
  │ Instance count (standard cells)    │ 16,000│ MATCH       │
  │ Instance count (SRAM)              │ 3    │ MATCH        │
  │ Instance count (analog)            │ 12   │ MATCH        │
  │ Instance count (I/O)               │ 16   │ MATCH        │
  │ Net count                          │ 4,850│ MATCH        │
  │ Pin mismatch count                 │ 0    │ CLEAN        │
  │ Short circuit count                │ 0    │ CLEAN        │
  │ Open circuit count                 │ 0    │ CLEAN        │
  │ Device W/L mismatch                │ 0    │ CLEAN        │
  │ Power net connectivity             │ PASS │ CLEAN        │
  │ Ground net connectivity            │ PASS │ CLEAN        │
  ├─────────────────────────────────────┼──────┼──────────────┤
  │ LVS STATUS                         │ —    │ CLEAN (LVS   │
  │                                    │      │  MATCHES)    │
  └─────────────────────────────────────┴──────┴──────────────┘

  LVS Run Time: 30 minutes
  Total devices compared: 24,250
  LVS waivers: 0
```

## 5. ERC (Electrical Rule Check)

```
ERC Results - iPACE-CHIP:
═══════════════════════════════════════════════════════════════

  ┌─────────────────────────────────────┬──────┬──────────────┐
  │ ERC Check                           │ Count│ Status       │
  ├─────────────────────────────────────┼──────┼──────────────┤
  │ Floating input pins                 │ 0    │ CLEAN        │
  │ Multiple drivers on net             │ 0    │ CLEAN        │
  │ Undriven outputs                    │ 0    │ CLEAN        │
  │ Missing power connections           │ 0    │ CLEAN        │
  │ Missing ground connections          │ 0    │ CLEAN        │
  │ No-connect pins                     │ 0    │ CLEAN        │
  │ Well/substrate unconnected          │ 0    │ CLEAN        │
  │ Power ground short                  │ 0    │ CLEAN        │
  ├─────────────────────────────────────┼──────┼──────────────┤
  │ ERC STATUS                          │ —    │ CLEAN        │
  └─────────────────────────────────────┴──────┴──────────────┘
```

## 6. DRC/LVS Fix Iterations

```
DRC/LVS Fix History:
═══════════════════════════════════════════════════════════════

  ┌────────┬──────────┬──────────┬──────────┬─────────────────┐
  │ Run #  │ DRC Viol │ LVS Viol │ Date     │ Actions Taken   │
  ├────────┼──────────┼──────────┼──────────┼─────────────────┤
  │ Run 1  │ 156      │ 3        │ 2023-11-20│ Initial P&R    │
  │        │          │          │          │ Route cleanup   │
  ├────────┼──────────┼──────────┼──────────┼─────────────────┤
  │ Run 2  │ 42       │ 1        │ 2023-12-01│ DRC: fix width  │
  │        │          │          │          │ LVS: pin swap   │
  ├────────┼──────────┼──────────┼──────────┼─────────────────┤
  │ Run 3  │ 12       │ 0        │ 2023-12-15│ DRC: enclosure  │
  │        │          │          │          │ fixes           │
  ├────────┼──────────┼──────────┼──────────┼─────────────────┤
  │ Run 4  │ 5        │ 0        │ 2023-12-20│ DRC: density    │
  │        │          │          │          │ fill added      │
  ├────────┼──────────┼──────────┼──────────┼─────────────────┤
  │ Run 5  │ 2        │ 0        │ 2024-01-05│ DRC: antenna    │
  │        │          │          │          │ diode fix       │
  ├────────┼──────────┼──────────┼──────────┼─────────────────┤
  │ Run 6  │ 0        │ 0        │ 2024-01-10│ DRC: spacing    │
  │        │          │          │          │ fix (final)     │
  ├────────┼──────────┼──────────┼──────────┼─────────────────┤
  │ Run 7  │ 0        │ 0        │ 2024-01-15│ SIGNOFF CLEAN   │
  │        │          │          │          │ (final verify)  │
  └────────┴──────────┴──────────┴──────────┴─────────────────┘

  Total fix iterations: 6 (before clean)
  Final clean: Run 7 (signoff verification)
  Average fix time per iteration: 2-3 days
```

## 7. DRC/LVS Waiver Process

```
DRC/LVS Waiver Policy:
═══════════════════════════════════════════════════════════════

  For iPACE-CHIP: NO waivers are allowed for:
  • Any safety-critical path DRC violation
  • Any LVS mismatch (zero tolerance)
  • Any ERC violation (zero tolerance)

  Waivers are ONLY permitted for:
  • Foundry-acknowledged false positives (with written confirmation)
  • Non-manufacturing text/annotation layers
  • Cosmetic issues that do not affect function or reliability

  Waiver Documentation Required:
  ┌─────────────────────────────────────────────────────────────┐
  │  DRC/LVS WAIVER FORM                                        │
  │                                                             │
  │  Violation ID: _________                                   │
  │  Rule Number:  _________                                   │
  │  Location:     _________                                   │
  │  Description:  _________                                   │
  │  Reason for Waiver: _________                              │
  │  Risk Assessment: _________                                │
  │  Supporting Evidence: _________                            │
  │                                                             │
  │  Approved by: _________ (Design Lead)                      │
  │  Approved by: _________ (Safety Lead)                      │
  │  Date:        _________                                    │
  └─────────────────────────────────────────────────────────────┘

  iPACE-CHIP Waivers Issued: 0
```

## 8. Summary

The iPACE-CHIP DRC/LVS verification confirms:

1. **Zero DRC violations** across 2,847 rules checked
2. **Full LVS match** — all 24,250 devices, 4,850 nets verified
3. **Zero ERC violations** — no floating pins or connectivity errors
4. **6 fix iterations** from initial layout to clean signoff
5. **Zero waivers** — all checks pass cleanly
6. **Foundry-certified tools** (Calibre) used for all checks

---

*Previous: [GDS-II Generation](../01-GDSII-Generation/gdsii-generation.md)*
