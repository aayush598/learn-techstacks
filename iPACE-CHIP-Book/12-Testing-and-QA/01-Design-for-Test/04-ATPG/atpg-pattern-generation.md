# ATPG Pattern Generation

## Overview

Automatic Test Pattern Generation (ATPG) is the process of creating deterministic test vectors that detect specific fault models in the iPACE-CHIP digital logic. Unlike pseudo-random BIST patterns, ATPG uses fault-simulation-driven algorithms to generate compact, high-coverage test sets that target every detectable fault in the design. For the iPACE-CHIP medical device, achieving >99% stuck-at fault coverage with <5% untestable/undetectable faults is mandatory per ISO 14971 risk analysis.

---

## 1. Fault Models

### 1.1 Stuck-At Fault Model

The primary fault model for iPACE-CHIP production testing is the single stuck-at fault (SSF) model:

**Definition:** A single net in the circuit is permanently tied to logic 0 (stuck-at-0, SA0) or logic 1 (stuck-at-1, SA1).

```
Normal circuit:        Faulty circuit (net X stuck-at-1):
                       
  A ──┬──► AND         A ──┬──► AND
      │                  │      │
  B ──┴──►    ──► Y     B ──┴──►    ──► Y
                        X stuck-at-1 forces output
                        regardless of B input
```

**Fault count estimation:**
- Average fault count: ~3.5 × gate count
- iPACE-CHIP (~500K gates): ~1.75M potential faults
- After fault collapsing: ~650K unique equivalent faults
- Detectable: ~97% of collapsed faults
- Untestable (redundant): ~3%
- ATPG untestable (testability limited): <0.5%

### 1.2 Transition Fault Model

Transition (delay) faults model slow-to-rise and slow-to-fall behavior:

**Types:**
- **Slow-to-rise (STR):** Net takes abnormally long to transition 0→1
- **Slow-to-fall (STF):** Net takes abnormally long to transition 1→0

**Detection requirement:** Two-pattern test
1. **Initialization:** Set net to initial value
2. **Launch:** Apply transition and capture response at-speed

**iPACE-CHIP transition fault coverage:** 95.8% (limited by multi-cycle paths)

### 1.3 Bridging Fault Model

Bridging faults model unintended shorts between nets:

**Types:**
- **AND-bridge:** Shorted nets resolve to AND of their intended values
- **OR-bridge:** Shorted nets resolve to OR of their intended values
- **Wired-AND/OR:** Depends on driver strengths

**Detection methodology:**
```
Victim net: Force logic 1
Aggressor net: Force logic 0
Expected: If bridged, victim reads 0 (AND) or aggressor reads 1 (OR)

Walking-0/Walking-1 patterns systematically test all potential bridges
```

### 1.4 Path Delay Fault Model

Path delay faults model cumulative delay along a sensitized path:

**Critical paths in iPACE-CHIP:**
- Timing controller → pacing output (safety-critical)
- ADC interface → arrhythmia detector → lead output
- Clock distribution → all major logic blocks

**Path delay fault coverage:** Tested through at-speed scan with launch-on-capture (LOC) or launch-on-shift (LOS) methodologies.

### 1.5 IDDQ Fault Model

Quiescent current (IDDQ) testing detects faults that cause abnormal supply current:

**Target faults:**
- CMOS stuck-open faults
- Gate-oxide shorts
- Channel leaks
- Subthreshold leakage defects

**Measurement technique:**
```
Apply test vector
Wait for current to stabilize (≥10μs)
Measure IDDQ
Compare against baseline (±10% tolerance)
Flag die exceeding threshold for further analysis
```

---

## 2. ATPG Algorithms

### 2.1 D-Algorithm

The foundational ATPG algorithm that uses D-calculus for fault propagation:

```
1. Activate fault (set fault site to opposite of stuck-at value)
2. Justify fault activation (trace back to primary inputs)
3. Propagate fault effect to primary output (sensitize path)
4. Verify: fault simulation confirms detection
5. If undetected: backtrack and try alternative paths
```

**D-calculus notation:**
- D: 1 at fault site, 0 at good circuit
- D̄: 0 at fault site, 1 at good circuit

### 2.2 PODEM (Path-Oriented Decision Making)

PODEM uses a branch-and-bound approach with backtrace to primary inputs:

```
PODEM Algorithm:
1. Select target fault
2. Initialize all nets to X (unknown)
3. Backtrace from fault site to find PI assignment
4. Forward trace to determine if fault is propagated
5. If not propagated: try alternative backtrace
6. If all paths exhausted: fault is undetectable
7. If propagated to PO: pattern found
8. Record pattern and move to next fault
```

### 2.3 FAN (Fanout-Oriented Test Generation)

FAN improves PODEM by:
- Identifying unique sensitizable paths through fanout stems
- Using multi-backtrace to reduce decision count
- Implementing efficient conflict-driven learning

### 2.4 Modern ATPG (Commercial Tools)

The iPACE-CHIP uses industry-standard ATPG tools with advanced features:

| Feature | Description | Benefit |
|---------|-------------|---------|
| Fault simulation | Fast parallel fault simulation | Reduces pattern count |
| Dynamic compaction | Merge compatible patterns | Fewer total patterns |
| X-tolerance | Handle unknown values | Higher effective coverage |
| Fault dropping | Remove detected faults | Faster convergence |
| Test point insertion | Add controllability/observability points | Improves coverage |
| Scan chain reordering | Optimize FF assignment | Reduces pattern count |

---

## 3. ATPG for iPACE-CHIP

### 3.1 ATPG Constraints and Rules

**Primary input constraints:**
- Scan enable (SE) = 0 during capture
- Test clocks follow prescribed timing
- Asynchronous resets held inactive
- Analog blocks disabled during digital testing

**Scan chain rules:**
- All SFFs must be scannable
- No combinational loops in scan path
- Scan clock skew < 5% of shift period
- Lockup latches required for high-speed shift

**Functional constraints:**
- Clock gating cells properly controlled during test
- Bus contention prevented during EXTEST
- Power supply decoupled for separate IDDQ measurement

### 3.2 ATPG Setup for iPACE-CHIP

```
ATPG Configuration:
├── Fault model: Stuck-at (single) + transition (launch-on-capture)
├── Compression: 64× on-chip decompressor/compressor
├── Pattern format: Scan pattern (shift + capture cycles)
├── Fill: Weighted random (100-fill for random testable, X-fill for hard faults)
├── X-tolerance: 3 unknowns per capture cycle
├── Fault simulation: Parallel (64-bit words)
├── Pattern ordering: Transition-weighted (minimize toggles)
└── Target coverage: 99.2% stuck-at, 95.5% transition
```

### 3.3 ATPG Pattern Generation Flow

```
Step 1: Read netlist and scan chain specification
        ├── Gate-level netlist (Verilog/VHDL)
        ├── Scan chain mapping file
        ├── Timing constraints (SDC)
        └── DRC rule file

Step 2: Run design rule checks
        ├── Scan chain integrity
        ├── Scan enable timing
        ├── Clock domain violations
        └── Fix any DRC errors before proceeding

Step 3: Fault list generation
        ├── Enumerate all single stuck-at faults
        ├── Apply fault collapsing (equivalent faults)
        ├── Identify redundant (untestable) faults
        └── Generate fault dictionary

Step 4: Pattern generation
        ├── Seed: weighted random patterns
        ├── Iterative: target undetected faults
        ├── Compact: merge compatible patterns
        └── Verify: fault simulation after each pattern

Step 5: Pattern verification
        ├── Re-simulate all patterns (gate-level)
        ├── Verify timing (setup/hold at capture)
        ├── Check power (shift and capture modes)
        └── Confirm coverage meets target

Step 6: Output generation
        ├── Pattern file (ATE format)
        ├── Coverage report
        ├── Untestable fault list with reasons
        └── Diagnostic fault dictionary
```

### 3.4 ATPG Coverage Report Summary

| Fault Category | Count | Percentage |
|---------------|-------|------------|
| Total faults (pre-collapse) | 1,750,000 | 100% |
| Collapsed faults | 650,000 | 37.1% |
| Detected (stuck-at) | 644,700 | 99.18% |
| Detected (transition) | 622,700 | 95.8% |
| Untestable (redundant) | 13,000 | 2.0% |
| ATPG untestable | 2,600 | 0.4% |
| Not attempted (BIST-covered) | 9,700 | 1.5% |
| **Effective stuck-at coverage** | | **99.18%** |

---

## 4. Untestable and Redundant Faults

### 4.1 Redundancy Analysis

Redundant faults represent intentional circuit redundancy (e.g., majority voters, ECC logic):

```
Redundancy Classification:
├── Structural redundancy: Intentional redundant logic
│   ├── Triple modular redundancy (TMR) voters
│   ├── ECC parity check logic
│   └── Watchdog timer handshake logic
│
├── Constraint-based untestable:
│   ├── Conflicting constraints make fault undetectable
│   └── Example: Bus hold circuitry
│
└── ATPG untestable:
    ├── Cannot justify or propagate within pattern limit
    └── May be testable with additional test points
```

### 4.2 ATPG Untestable Fault Analysis

ATPG-untestable faults require investigation to confirm they are truly untestable:

| Cause | Count | Resolution |
|-------|-------|------------|
| Incompatible constraints | 800 | Review constraints, confirm valid |
| Observability limited | 600 | Consider test point insertion |
| Controllability limited | 500 | Consider test point insertion |
| Multi-cycle path | 400 | Add multi-cycle ATPG constraints |
| False path | 300 | Confirm as false path, document |

### 4.3 Test Point Insertion

For faults that become testable with minimal design modification:

**Controllability test points:**
- Observation point: Capture value of internal node through scan FF
- Control point: Drive internal node through scan FF + MUX

**Impact on iPACE-CHIP:**
- ~200 test points added
- 0.1% area overhead
- +1.2% coverage improvement (99.18% → 99.5%)
- No timing impact (test points bypassed in functional mode)

---

## 5. Pattern Formats and Application

### 5.1 Scan Pattern Structure

Each ATPG pattern consists of:

```
Pattern N:
├── Scan chain 0: [SI_0_0, SI_0_1, ..., SI_0_1249] (shift-in)
├── Scan chain 1: [SI_1_0, SI_1_1, ..., SI_1_1247]
├── ...
├── Scan chain 7: [SI_7_0, SI_7_1, ..., SI_7_1252]
├── Capture timing: Launch → Capture (1 or 2 cycles)
├── Scan chain 0: [SO_0_0, SO_0_1, ..., SO_0_1249] (shift-out expected)
├── Scan chain 1: [SO_1_0, SO_1_1, ..., SO_1_1247]
├── ...
└── Scan chain 7: [SO_7_0, SO_7_1, ..., SO_7_1252]
```

### 5.2 Launch-On-Shift (LOS) vs. Launch-On-Capture (LOC)

| Parameter | LOS | LOC |
|-----------|-----|-----|
| Launch timing | Last shift edge | First capture edge |
| Capture timing | Next shift edge | Second capture edge |
| Period | Shift period | Capture period (at-speed) |
| Speed accuracy | Slower than functional | At-speed |
| Implementation | SE toggle on shift | Two capture pulses |
| Fault coverage | Transition faults | Transition faults |
| iPACE-CHIP use | Stuck-at test | Transition fault test |

### 5.3 Pattern Compression Impact

On-chip compression dramatically reduces test time and data volume:

```
Uncompressed patterns:
- 15,000 patterns × 10,000 bits/pattern = 150 Mbits
- Shift time: 15,000 × 10,000 = 150M clock cycles
- ATE data rate: 200 Mbps → 750 seconds test time

Compressed patterns (64×):
- 250 patterns × 156 bits/pattern = 39 Kbits
- Shift time: 250 × 156 = 39K clock cycles
- ATE data rate: 200 Mbps → 0.195 seconds test time

Test time reduction: 3,846×
ATE memory reduction: 3,846×
```

---

## 6. Fault Simulation

### 6.1 Fault Simulation Methods

**Serial fault simulation:**
- Simulate one fault at a time
- Accurate but very slow
- Used for final verification only

**Parallel fault simulation:**
- Simulate N faults simultaneously (N-bit machine word)
- 64-bit machine: 64× speedup over serial
- Used for production ATPG

**Critical path tracing:**
- Trace from fault site to primary outputs
- Very fast but less accurate
- Used for initial fault classification

### 6.2 Fault Simulation Accuracy

The iPACE-CHIP fault simulation uses:

- **Gate-level simulation** with back-annotated timing
- **Parallel fault simulation** (64 fault machines)
- **X-valued simulation** for unknown handling
- **Multi-cycle capture** for transition fault detection

### 6.3 Diagnostic Fault Dictionary

The ATPG tool generates a fault dictionary mapping each fault to its unique detection pattern(s) and response:

```
Fault Dictionary Entry:
├── Fault ID: SA0 on net U123/A
├── Detection patterns: [452, 1207, 8934]
├── Detected by: Chain 3, scan cell 847
├── Failure response: SO_3[847] = 0 (expected 1)
├── Equivalent faults: [SA0 on U123/A, SA1 on U123/B]
└── Location: Module > Submodule > Gate > Pin
```

---

## 7. Production ATPG Flow

### 7.1 Wafer Sort ATPG

During wafer-level testing, ATPG patterns are applied after BIST:

```
1. Probe contact check
2. IDDQ baseline measurement
3. MBIST (all memories)
4. LBIST (3 seeds, in-field subset)
5. Scan chain integrity check
6. Stuck-at ATPG patterns (250 compressed patterns)
7. Transition fault ATPG patterns (100 compressed patterns)
8. IDDQ measurement (all pattern sets)
9. Pass/Fail marking
```

### 7.2 Final Test ATPG

Packaged device testing adds voltage/temperature corner testing:

```
Corner 1: 1.8V, 25°C — Nominal
├── All stuck-at patterns
├── Transition patterns at 100 MHz capture

Corner 2: 2.0V, -40°C — Fast
├── Subset of stuck-at patterns (20%)
├── Transition patterns at 120 MHz capture

Corner 3: 1.6V, 85°C — Slow
├── All stuck-at patterns
├── Transition patterns at 80 MHz capture

Corner 4: 1.6V, 105°C — Worst-case (reliability)
├── Critical safety-path patterns only
├── Transition at 60 MHz capture
├── IDDQ at elevated temperature
```

### 7.3 ATPG Pattern Count Summary

| Test Phase | Stuck-At | Transition | Total Patterns |
|------------|----------|------------|----------------|
| Wafer sort | 250 | 100 | 350 |
| Final test (×3 corners) | 750 | 300 | 1,050 |
| Reliability screening | 50 | 25 | 75 |
| **Total production** | **1,050** | **425** | **1,475** |

---

## 8. Diagnostic ATPG

### 8.1 Diagnostic Pattern Generation

When a specific fault type is suspected, diagnostic ATPG generates patterns that distinguish between candidate faults:

```
Diagnostic scenario: IDDQ failure at pattern #452
Candidate faults:
├── Gate G1: SA0 on input A
├── Gate G2: SA1 on output Y
├── Gate G3: Bridging between inputs A and B
└── Gate G4: Stuck-open on transistor N1

Diagnostic patterns:
├── Pattern D1: Detects G1/A only
├── Pattern D2: Detects G2/Y only
├── Pattern D3: Detects G3 bridge only
├── Pattern D4: Detects G4 stuck-open only
└── Apply all diagnostic patterns → identify failing pattern → isolate defect
```

### 8.2 Failure Bitmap Correlation

ATPG pattern results are correlated with physical failure analysis:

```
Pattern response bitmap → Failing scan cell → Logic cone → Physical location

Example:
Pattern 127 fails on Chain 5, Cell 342
→ Scan cell 342 is in module: arrhythmia_detector
→ Logic cone traces to: comparator U456 input B
→ Physical location: (x=1250, y=800) on die
→ Candidate defect: gate-oxide short at U456/B
```

---

## 9. Summary

ATPG pattern generation provides the iPACE-CHIP with deterministic, high-coverage fault detection that complements pseudo-random BIST and functional testing. The combination of stuck-at and transition fault testing with on-chip compression achieves >99% stuck-at coverage at minimal test time and ATE resource cost. The diagnostic fault dictionary and failure bitmap correlation capabilities enable efficient root cause analysis during yield improvement campaigns, supporting the zero-defect quality requirements of the medical device manufacturing process.

---

## References

- Bushnell, M.L. & Agrawal, V.D. *Essentials of Electronic Testing*. Springer, 2000.
- Abramovici, M., Breuer, M.A., & Friedman, A.D. *Digital Systems Testing and Testable Design*. IEEE Press, 1990.
- Brglez, F. "On Testability of Combinational Networks." *Proc. IEEE Int. Symp. Circuits and Systems*, 1984.
- IEC 62132-4: Integrated Circuit Electromagnetic Immunity
- ISO 14971:2019: Medical Devices — Application of Risk Management
- Synopsys TetraMAX ATPG User Guide
- Cadence Modus DFT User Guide
