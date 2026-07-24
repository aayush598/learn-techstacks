# Scan Chain Insertion

## Overview

Scan chain insertion is the foundational Design-for-Test (DFT) technique used in the iPACE-CHIP to achieve high controllability and observability of internal flip-flop states. By converting sequential elements into a serial shift path, scan chains transform an otherwise untestable sequential circuit into a combinational testing problem, enabling deterministic fault detection with minimal test pin overhead.

For a medical-grade pacemaker controller like the iPACE-CHIP, scan chain insertion must balance testability goals against strict constraints on die area, power consumption, timing closure, and functional reliability. Every scan insertion decision must be validated against ISO 14971 risk analysis and IEC 60601-1 safety requirements.

---

## 1. Fundamental Concepts

### 1.1 Why Scan Chains Are Necessary

In a combinational circuit, every internal node can be directly controlled through primary inputs and observed through primary outputs. Sequential circuits contain flip-flops and latches that form internal state, breaking this direct controllability/observability path. Without DFT structures:

- Internal flip-flop states cannot be set to arbitrary values
- Faults behind sequential elements are unobservable
- Test generation complexity grows exponentially with sequential depth
- Fault coverage plateaus well below the 99%+ required for medical devices

Scan chain insertion solves this by replacing each flip-flop with a scan flip-flop (SFF) that has two data inputs: the functional input and a scan input. A multiplexer selects between these based on a scan-enable (SE) signal. When SE is asserted, the chip enters scan mode, and data shifts serially through all SFFs.

### 1.2 Scan Flip-Flop Architecture

The basic scan flip-flop consists of:

```
                    ┌──────────┐
   Functional D ───►│          │
                    │   MUX    ├───► D (to flip-flop)
   Scan SI    ────►│          │
                    └────┬─────┘
                         │
                    SE ──┘ (select)

                    ┌──────────┐
                    │ Flip-Flop├───► Q (functional output)
                    │          ├───► SO (scan output)
                    └──────────┘
```

The SE signal serves dual purpose during scan mode (shift) and functional mode (capture). In medical device applications, additional safety logic may be added to detect inadvertent entry into scan mode during normal operation.

### 1.3 Scan Operation Modes

**Shift Mode (SE = 1):**
- Test patterns are serially shifted into the scan chain through SI
- Data propagates from SI through each SFF to SO
- Shift frequency is typically limited to ensure safe power dissipation

**Capture Mode (SE = 0):**
- One clock pulse captures the combinational logic response
- Functional mode is briefly activated to capture fault effects
- Results are stored in SFFs for subsequent shift-out

**Functional Mode (SE = 0):**
- Normal chip operation with no test activity
- Scan chain is transparent to functional logic
- Must meet all timing constraints in this mode

---

## 2. Scan Chain Architecture for iPACE-CHIP

### 2.1 Single-Chain vs. Multi-Chain Design

The iPACE-CHIP employs a multi-chain architecture for the following reasons:

| Parameter | Single Chain | Multi Chain (8-ch) |
|-----------|-------------|-------------------|
| Shift time (10K FFs) | 10,000 cycles | 1,250 cycles |
| Test application time | Very long | 8× reduction |
| SI/SO pin count | 2 | 16 |
| Area overhead | Lower | Slightly higher |
| Power during shift | Distributed | Concentrated |

The 8-chain configuration was selected as the optimal trade-off for the iPACE-CHIP, providing:

- Test time reduction compatible with production test cost targets
- Limited additional pin count (16 dedicated test pins)
- Manageable shift-mode power dissipation
- Compatibility with the ATE pin count budget

### 2.2 Chain Balancing

Unequal chain lengths cause scan chain imbalance, where shorter chains idle while longer chains continue shifting. The iPACE-CHIP targets chain length variation of less than 5%:

```
Chain 0: 1250 FFs
Chain 1: 1248 FFs
Chain 2: 1252 FFs
Chain 3: 1249 FFs
Chain 4: 1251 FFs
Chain 5: 1247 FFs
Chain 6: 1253 FFs
Chain 7: 1250 FFs
─────────────────
Total:   10,000 FFs
Max variation: 0.4%
```

### 2.3 Scan Chain Routing Guidelines

Physical routing of scan chains follows strict guidelines to minimize impact on functional signal integrity:

- **Proximity routing:** Scan SI/SO signals follow the same metal layer as adjacent functional routing to minimize coupling impedance mismatch
- **Shielded clock lines:** Scan clocks (SCAN_CLK) are shielded with VDD/VSS on both sides
- **Avoidance zones:** Scan routing avoids sensitive analog blocks (bandgap reference, charge pump, sense amplifiers)
- **EMI compliance:** Scan chain switching activity during shift must not create electromagnetic emissions exceeding IEC 60601-1-2 limits if any test mode could be inadvertently activated

---

## 3. Scan Insertion Methodology

### 3.1 Pre-Insertion Checks

Before scan insertion, the RTL and gate-level netlist undergo extensive verification:

1. **Clock domain crossing (CDC) analysis** — All CDC paths must be properly synchronized; scan chain routing must not create new CDC violations
2. **Reset tree analysis** — Asynchronous resets must be properly controlled during scan mode to prevent unknown states
3. **Latch transparency audit** — Latches must be wrapped or converted to flip-flop-based scan elements
4. **Constraint definition** — Scan-mode timing constraints, DRC rules, and exception lists are prepared

### 3.2 Scan Insertion Flow

The iPACE-CHIP scan insertion follows a structured flow:

```
Step 1: Read gate-level netlist
        ├── Technology library
        ├── Scan cell library (SFF, SLATCH)
        └── Scan chain specification file

Step 2: Identify scan-eligible flip-flops
        ├── Exclude flip-flops on hardened timing paths
        ├── Exclude clock-gating cells (ICG) output FFs
        └── Mark async-set/reset FFs for special handling

Step 3: Apply scan replacement
        ├── Replace functional FFs with SFFs
        ├── Map SI/SO connections per chain specification
        └── Insert scan clock gating logic

Step 4: Verify scan chain connectivity
        ├── Shift path ATPG (chain test pattern)
        ├── Scan chain broken/short detection
        └── Flooding analysis for long hold paths

Step 5: Post-insertion timing verification
        ├── Functional mode STA
        ├── Scan mode STA (shift and capture)
        └── Scan shift power analysis
```

### 3.3 Handling Non-Scan Elements

Certain flip-flops in the iPACE-CHIP cannot be converted to scan elements:

**Clock-gating integrated cells (ICGs):** The clock output of ICG cells feeds a subset of flip-flops. These FFs may not be directly scannable through the gated clock path. Solutions include:
- Adding scan-mode bypass around the ICG
- Using dedicated scan clock insertion points
- Implementing test clock muxing at ICG inputs

**Asynchronous reset/set flip-flops:** FFs with async controls require special handling during scan:
- The async reset must be deasserted during capture to allow combinational logic to drive the FF
- Scan-shift mode must not trigger async set/reset
- Scan-only reset override logic is inserted

**Memory elements:** Embedded SRAM blocks are not scanned directly; they are accessed through memory BIST (MBIST) logic and tested separately.

### 3.4 Scan Compression

The iPACE-CHIP employs on-chip scan compression to reduce test data volume and test time:

**Compression Architecture:**
- Decompressor at scan chain inputs (1:8 ratio)
- Compressor at scan chain outputs (8:1 ratio)
- Total compression ratio: ~64×

**Benefits for Medical Device Testing:**
- Reduced ATE memory requirements (smaller test program)
- Faster test execution (shorter shift time per pattern)
- Lower ATE channel count requirements
- Enables at-speed testing within budget constraints

**Compression Impact on Fault Coverage:**

| Metric | No Compression | 64× Compression |
|--------|---------------|-----------------|
| Patterns | 15,000 | 250 |
| Shift cycles/pattern | 10,000 | 156 |
| Total shift time | 150M cycles | 39K cycles |
| Fault coverage | 99.2% | 99.1% |
| Test data volume | 150 Mbits | 0.39 Mbits |

The 0.1% fault coverage reduction is acceptable due to complementary testing through BIST and functional patterns.

---

## 4. Scan Chain DRC and Verification

### 4.1 Design Rule Checks

Scan DRC ensures the inserted scan chains are structurally correct and testable:

**Chain DRC Rules:**
1. **SC-P1:** Every scan flip-flop must be connected in a chain from SI to SO
2. **SC-P2:** No combinational loops in the scan path
3. **SC-P3:** Scan clock must reach all SFFs with skew < 5% of shift period
4. **SC-P4:** Scan enable must have valid timing for setup/hold at every SFF
5. **SC-P5:** No undriven scan inputs (SI of first FF in chain)
6. **SC-P6:** No floating scan outputs (SO of last FF in chain)
7. **SC-P7:** Scan mode power must not exceed thermal limits

**Functional DRC Rules:**
1. **SC-F1:** Functional logic must not observe scan enable during normal mode
2. **SC-F2:** Scan clock must not contaminate functional clock paths
3. **SC-F3:** Scan shift must not violate async control timing requirements

### 4.2 Scan Chain Verification Tests

**Chain Integrity Test:**
```
Shift known pattern (e.g., 01010101...) through each chain
Verify output matches expected pattern after full shift-through
Detect: broken chains, shorts between chains, stuck-at faults on SI/SO
```

**Scan Chain Flooding Test:**
```
Verify that scan shift frequency does not cause timing violations
Long combinational paths between adjacent SFFs may cause hold violations
Solution: Minimum delay insertion (lockup latches) between chain segments
```

**Scan Chain Skew Test:**
```
Measure clock arrival time variation across SFFs in each chain
Ensure skew budget supports capture window requirements
Report any SFFs outside skew tolerance
```

### 4.3 Scan Chain Lockup Latches

To prevent hold time violations during scan shift at high frequencies, lockup latches are inserted between chain segments:

```
Chain Segment 1 ──── [Lockup Latch] ──── Chain Segment 2
                       (transparent on                        (transparent on
                        falling edge)                          rising edge)
```

Lockup latch density in the iPACE-CHIP is approximately one per 50-100 SFFs, adding <0.5% area overhead.

---

## 5. Scan Power Management

### 5.1 Shift-Mode Power Analysis

During scan shift, approximately 50% of all flip-flops toggle on each shift clock edge, creating significantly higher dynamic power than functional operation. For the iPACE-CHIP:

| Mode | Toggle Rate | Dynamic Power |
|------|-------------|---------------|
| Functional | ~12% | 180 μW |
| Scan shift | ~50% | 850 μW |
| Capture (at-speed) | ~15% | 220 μW |

### 5.2 Power Reduction Techniques

**Scan clock gating:** Disable scan clock to inactive chains during shift to reduce simultaneous switching:

```
Chain active signals (decoded from chain select):
  CHAIN_EN[0] ──┐
  CHAIN_EN[1] ──┤
  ...           ├──► SCAN_CLK gated per chain
  CHAIN_EN[7] ──┘
```

**Low-power shift ordering:** ATPG tools reorder scan flip-flop assignments within chains to minimize toggles between consecutive patterns:

- Weighted random fill prefers 0-to-0 and 1-to-1 transitions
- X-tolerance algorithms avoid propagating unknown values that require costly re-fill
- Pattern merging combines patterns with similar fill to reduce transitions

**Scan segment power management:** Chains are divided into segments with independent clock gating, reducing instantaneous power by up to 4× during shift.

### 5.3 Thermal Constraints During Scan

Medical device reliability requires that no test mode exceeds the thermal limits established during reliability qualification:

- Junction temperature during scan shift: ≤ 85°C (vs. 105°C functional max)
- Thermal cycling during scan must not exceed qualified limits
- Hotspot analysis confirms no localized heating above package thermal rating

---

## 6. Scan Chain Timing Analysis

### 6.1 Scan Shift-Mode Timing

During scan shift, the timing path is:

```
SFF_Q ──► Combinational Logic ──► SFF_D
    │                                  │
    └── Scan chain routing ────────────┘

Setup: T_shift > T_clk_to_q + T_logic + T_setup
Hold:  T_clk_to_q + T_logic > T_hold
```

Where T_shift is the scan shift period (typically 50-100 ns for production testing).

### 6.2 Scan Capture-Mode Timing

Capture mode timing is more critical as it may run at functional speed (at-speed capture):

```
Capture period: T_functional (e.g., 10 ns for 100 MHz)
Setup: T_functional > T_clk_to_q + T_logic_capture + T_setup
Hold:  T_clk_to_q + T_logic_capture > T_hold
```

At-speed capture enables transition fault testing, which requires two consecutive capture pulses:

```
Launch pulse:  SFF launches transition
Capture pulse: SFF captures fault effect (1 period later)
```

### 6.3 Scan Mode Exceptions

Some timing paths are relaxed during scan mode:

- **Shift-only false paths:** Paths that are only active during shift (not capture) can be timed at slower shift frequency
- **Scan enable reconvergence:** SE path from pad to all SFFs may have large fanout; this is constrained as a shift-only path
- **Multi-cycle scan paths:** Some logic between SFF segments may require multi-cycle constraints during shift

---

## 7. Medical Device-Specific Considerations

### 7.1 Scan Mode Lock-Out

For the iPACE-CHIP, inadvertent entry into scan mode during patient-connected operation is a catastrophic safety hazard. The following protections are implemented:

**Hardware scan-disable lock:**
```
SCAN_EN pad ──┬──► [ECC-protected fuse] ──► SE global signal
              │
              └──► [Watchdog timer] ──► Force SE = 0 if scan mode
                                        detected during functional clock
```

**Fuse-programmed scan disable:**
- After production testing, a one-time-programmable fuse disables scan enable
- Scan mode cannot be re-entered without destroying the chip (irreversible)
- This is the primary defense against in-field scan activation

**Power-on reset scan guard:**
- Scan enable is held low during power-on-reset sequence
- Functional mode must be confirmed (PLL lock, watchdog check) before SE could theoretically be released

### 7.2 Scan Test Coverage for Safety-Critical Logic

ISO 14971 risk analysis identifies safety-critical logic blocks that require enhanced scan test coverage:

| Safety Function | Fault Coverage Target | Justification |
|----------------|----------------------|---------------|
| Pacing output driver | 99.9% | Patient harm if malfunction |
| Lead impedance monitor | 99.9% | False impedance reading |
| Arrhythmia detector | 99.5% | Missed/diagonal arrhythmia |
| Telemetry controller | 99.0% | Communication failure |
| Power management | 99.5% | Loss of device operation |

### 7.3 Defect Coverage Validation

Scan chain fault coverage is validated through silicon correlation:

- Known defective die are retained from wafer sort
- Scan patterns are applied and response analyzed
- Defect types are correlated with physical failure analysis (PFA)
- Coverage models are refined based on actual defect distributions

---

## 8. Integration with ATE

### 8.1 Scan Chain ATE Requirements

The iPACE-CHIP scan testing requires specific ATE capabilities:

- **Pin count:** Minimum 16 digital channels for 8 scan chains (SI/SO pairs)
- **Timing resolution:** 1 ns edge placement for at-speed capture
- **Memory depth:** 128 Mbits per channel for pattern storage
- **Scan clock rate:** Up to 50 MHz shift frequency
- **Waveform formatting:** RZ and NRZ formats for launch/capture timing
- **Comparator accuracy:** ±5 mV for voltage-based pass/fail detection

### 8.2 Scan Pattern Application Sequence

Production scan test follows a strict sequence:

```
1. Power-up and mode entry
   ├── Assert test mode signal
   ├── Configure PLL for test frequency
   └── Verify scan chain reset state

2. Chain integrity check
   ├── Shift known pattern through all chains
   ├── Verify output matches expected
   └── Flag any mismatched chains

3. At-speed capture test
   ├── Apply scan shift patterns (compressed)
   ├── Perform at-speed capture
   ├── Shift out results
   └── Compare against golden reference

4. Transition fault test
   ├── Apply transition fault patterns
   ├── Launch-on-shift or launch-on-capture
   ├── Capture at-speed response
   └── Verify no timing-related failures

5. Scan mode exit
   ├── Deassert test mode signal
   ├── Resume functional mode
   └── Verify functional operation
```

---

## 9. Summary

Scan chain insertion is the cornerstone of the iPACE-CHIP DFT strategy. The multi-chain architecture with compression provides the test accessibility needed to achieve >99% stuck-at fault coverage while meeting production test time and cost constraints. Safety-critical protections ensure that scan structures cannot compromise patient safety during normal device operation. The integration of scan testing with BIST, JTAG, and functional test creates a comprehensive test strategy meeting the zero-defect quality requirements of implantable medical devices.

---

## References

- Bushnell, M.L. & Agrawal, V.D. *Essentials of Electronic Testing*. Springer, 2000.
- Abramovici, M., Breuer, M.A., & Friedman, A.D. *Digital Systems Testing and Testable Design*. IEEE Press, 1990.
- IEC 62132-4: Integrated Circuit Electromagnetic Immunity — Direct Power Injection
- IEEE 1149.1-2013: Standard Test Access Port and Boundary-Scan Architecture
- ISO 14971:2019: Medical Devices — Application of Risk Management to Medical Devices
- IEC 60601-1:2005+A1:2012+A2:2020: Medical Electrical Equipment — General Requirements for Basic Safety and Essential Performance
