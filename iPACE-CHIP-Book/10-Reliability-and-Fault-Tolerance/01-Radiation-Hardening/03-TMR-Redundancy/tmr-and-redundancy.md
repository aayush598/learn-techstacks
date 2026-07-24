# 10.1.3 Triple Modular Redundancy (TMR) and Redundancy Architectures

## Chapter Overview

Triple Modular Redundancy (TMR) is the cornerstone of the iPACE-CHIP's radiation hardness strategy for digital logic. While the concept — replicate a circuit three times and vote on the output — is deceptively simple, its practical implementation in a life-critical implantable pacemaker demands careful attention to voter design, error accumulation, area/power trade-offs, and interaction with other fault-tolerance mechanisms. This chapter provides a comprehensive treatment of TMR as applied to the iPACE-CHIP, covering classical TMR, advanced variants (quad modular redundancy, N-modular redundancy), partial TMR strategies, voter optimization, and the critical issue of common-mode failure prevention.

---

## 10.1.3.1 Classical TMR: Theory and Implementation

### Mathematical Foundation

TMR reliability can be modeled using binomial probability. If each module has a reliability R (probability of correct operation), the TMR system reliability is:

```
R_TMR = 3R² - 2R³

where:
  R = module reliability
  3R² = probability that at least 2 of 3 modules work (for combination: C(3,2)×R²×(1-R) + C(3,3)×R³)
  2R³ = correction for over-counting
```

For the iPACE-CHIP's Category A logic blocks:

```
Module reliability over 10 years (without TMR):
  R_module = 1 - P_SEU × N_years
  P_SEU = 10⁻⁹ per hour for critical logic (from Ch. 10.1.1)
  N_years = 10 × 365 × 24 = 87,600 hours
  P_SEU_total = 10⁻⁹ × 87,600 = 8.76 × 10⁻⁵
  R_module = 1 - 8.76 × 10⁻⁵ ≈ 0.999912

TMR reliability:
  R_TMR = 3 × (0.999912)² - 2 × (0.999912)³
        = 3 × 0.999824 - 2 × 0.999736
        = 2.999472 - 1.999472
        = 0.9999999999 (approximately 1 - 7.7 × 10⁻¹⁰)
```

TMR improves the reliability by approximately 5 orders of magnitude for the iPACE-CHIP's operating conditions.

### TMR Granularity Selection

The iPACE-CHIP employs TMR at three different granularities, each chosen based on the criticality and area constraints of the target block:

**Bit-Level TMR:** Each individual flip-flop is triplicated. This provides the finest granularity of protection but has the highest overhead. Used for:
- Mode control FSM state register (5 bits)
- Pacing output amplitude register (10 bits)
- Pacing pulse width register (8 bits)
- Sensing threshold register (6 bits)
- Rate limit registers (12 bits)
- Total: ~41 flip-flops × 3 = 123 flip-flops + voters

**Word-Level TMR:** Entire register files or data words are triplicated. The voter operates on complete words. Used for:
- Pacing rate counter (16-bit counter × 3)
- AV delay timer (12-bit timer × 3)
- Telemetry data register (32-bit word × 3)

**Module-Level TMR:** Entire functional blocks are triplicated. Used for:
- Digital filter bank for sensing signal processing
- CRC generator for telemetry
- Watchdog timer core

### Bit-Level TMR Implementation

The iPACE-CHIP's standard cell library includes dedicated TMR flip-flop cells:

```
TMRFlop_D (D-type TMR flip-flop):
  Inputs: D (data), CLK (clock), EN (enable)
  Outputs: Q (voted output), Q_raw1, Q_raw2, Q_raw3 (individual replicas)

Internal structure:
  FF1 ← D, CLK, EN → Q1 ─┐
  FF2 ← D, CLK, EN → Q2 ─┼→ Majority Voter → Q
  FF3 ← D, CLK, EN → Q3 ─┘
```

The TMR flip-flop cell has the following characteristics:

| Parameter | Value |
|---|---|
| Transistor count | 3 × 28 = 84 (for 3 D flip-flops) + 6 (voter) = 90 |
| Equivalent gate count | 22.5 gates |
| Delay (D to Q) | 0.8 ns (at 180nm, 1.8V, 25°C) |
| Setup time | 0.3 ns |
| Hold time | 0.1 ns |
| Power (switching) | 15 μW at 16 MHz |
| Power (static) | 0.5 μW |
| Area | 12 μm × 8 μm = 96 μm² |

Compared to a standard D flip-flop (30 μm²), the TMR flip-flop occupies 3.2× the area.

### Word-Level TMR Implementation

For word-level TMR, three copies of the register file are instantiated, and a word-level majority voter is placed at the output:

```
                    ┌──────────────┐
              ┌────►│  RegFile_1   │────┐
              │     │  (N bits)    │    │
              │     └──────────────┘    │
              │                         ▼
 Input ───────┼────►┌──────────────┐  ┌──────────┐
              │     │  RegFile_2   │──│  Word    │──► Output (N bits)
              │     │  (N bits)    │  │  Voter   │
              │     └──────────────┘  └──────────┘
              │                         ▲
              │     ┌──────────────┐    │
              └────►│  RegFile_3   │────┘
                    │  (N bits)    │
                    └──────────────┘
```

The word-level voter is implemented as N parallel bit-level voters:

```
For each bit position i (0 to N-1):
  Voted_bit[i] = (A[i] AND B[i]) OR (B[i] AND C[i]) OR (A[i] AND C[i])
```

This is highly efficient because:
- The voter logic is trivially parallelizable
- No inter-bit dependencies exist in the voter
- The voter delay is a single gate delay (AND-OR) regardless of word width

### Module-Level TMR Implementation

Module-level TMR requires that the module interface be carefully defined to ensure that:
1. All three replicas receive identical inputs
2. No shared state exists between replicas (except through the voter)
3. The voter operates on the module's outputs, not internal signals

```
                     ┌──────────────────┐
               ┌────►│  Module Replica 1│────┐
               │     │  (full module)   │    │
               │     └──────────────────┘    │
               │                             ▼
 Input ────────┼────►┌──────────────────┐  ┌──────────┐
               │     │  Module Replica 2│──│  Output  │──► Output
               │     │  (full module)   │  │  Voter   │
               │     └──────────────────┘  └──────────┘
               │                             ▲
               │     ┌──────────────────┐    │
               └────►│  Module Replica 3│────┘
                     │  (full module)   │
                     └──────────────────┘
```

For the iPACE-CHIP's digital filter module:

```
Module: 64-tap FIR filter
  Replica 1: 64 MAC units + 64 coefficient ROM + accumulator
  Replica 2: identical copy
  Replica 3: identical copy
  Output voter: 16-bit majority voter (for 16-bit filter output)
  
  Area overhead: 3× for the filter + 0.1% for the voter
  Power overhead: 3× for the filter + 0.1% for the voter
  Timing: no additional delay (voter is in the output path)
```

---

## 10.1.3.2 TMR Voter Design Optimization

### Static Majority Voter

The classical majority voter implements the Boolean function:

```
V = AB + BC + AC
```

This requires 3 AND gates and 2 OR gates (or equivalently, 3 AND-OR-Invert gates with an inverter). In CMOS, this translates to approximately 18 transistors for a single-bit voter.

**Optimized CMOS Implementation:**

The iPACE-CHIP uses an optimized static majority voter that reduces the transistor count to 12:

```
V = (A + B) · (B + C) · (A + C)
```

This is implemented using pass-transistor logic:

```
         A ──┤NMOS├──┬── VDD
              │       │
         B ──┤PMOS├──┘
              │
         B ──┤NMOS├──┬── VDD
              │       │
         C ──┤PMOS├──┘
              │
         A ──┤NMOS├──┬── VDD
              │       │
         C ──┤PMOS├──┘
              │
              ▼
         V_out
```

This pass-transistor implementation has the advantage of being a single-stage circuit (no internal nodes that could be affected by SEUs) and has symmetric timing for all input permutations.

### TMR Voter SEU Sensitivity

The voter itself is a combinational circuit that can be affected by SEUs. However, the voter's SEU sensitivity is fundamentally different from the modules it protects:

- A single-bit SEU in the voter can only affect the voter's output for one clock cycle (since the voter is combinational, there is no stored state to be permanently flipped).
- The voter has only 3 inputs (for a single-bit voter), so a single SEU can only flip one input's contribution to the output. Since the majority function requires 2 out of 3 inputs to agree, flipping one input only changes the output if the original vote was 2-to-1 (not 3-to-0).

The probability that a voter SEU causes an incorrect output is:

```
P_voter_SEU = P(SEU in voter) × P(original vote was 2-to-1)

For the iPACE-CHIP:
  P(SEU in voter) ≈ 10⁻¹⁰ per hour (voter is very small, ~12 transistors)
  P(2-to-1 vote) ≈ 0.3 (typical operating condition)
  P_voter_error = 3 × 10⁻¹¹ per hour
```

This is approximately 100× lower than the module SEU rate, so the voter is not the dominant contributor to the TMR system's failure rate.

### Dual-Stage Voter for Enhanced Protection

For the most critical Category A signals (pacing output enable, mode control), the iPACE-CHIP uses a dual-stage voter:

```
Stage 1: Three independent bit-level voters (each computing majority of 3 replicas)
Stage 2: A final voter that takes the three Stage-1 outputs and votes again

         Replica1 ──► Voter_A ──┐
         Replica2 ──► Voter_B ──┼──► Final Voter ──► Output
         Replica3 ──► Voter_C ──┘
```

This dual-stage voter provides:
1. Protection against a voter SEU: if one Stage-1 voter produces an incorrect output, the final voter corrects it.
2. Protection against a multi-replica SEU: if one replica has an SEU and one Stage-1 voter has an SEU, the remaining two Stage-1 voters can still provide the correct result.

The overhead is 3× the voter area (3 Stage-1 voters + 1 final voter), but for a single-bit voter this is only ~48 additional transistors — negligible compared to the total die area.

### Clocked Voter vs. Combinational Voter

**Combinational Voter:**
- Pro: No additional latency
- Pro: Simple design
- Con: Creates a long combinational path (three replicas → voter → output)
- Con: Timing closure can be difficult for complex functions

**Clocked Voter:**
- Pro: Breaks the combinational path, improving timing
- Pro: Provides an additional register stage for error detection
- Con: Adds one clock cycle of latency
- Con: Requires synchronization between replicas

The iPACE-CHIP uses a mix of both:
- **Combinational voters** for the pacing rate counter and AV delay timer (where timing is critical and the voter is simple)
- **Clocked voters** for the mode control FSM and telemetry data register (where timing is less critical and the additional registration provides a useful error-detection checkpoint)

---

## 10.1.3.3 Advanced TMR Variants

### Quad Modular Redundancy (QMR)

QMR uses four replicas instead of three. The primary advantage is the ability to detect and correct double errors (two replicas simultaneously incorrect):

```
QMR reliability:
  R_QMR = C(4,3)×R³×(1-R) + C(4,4)×R⁴
        = 4R³ - 3R⁴

For R = 0.999912:
  R_QMR = 4 × (0.999912)³ - 3 × (0.999912)⁴
        ≈ 1 - 3.1 × 10⁻¹⁰
```

Compared to TMR's 7.7 × 10⁻¹⁰, QMR improves reliability by approximately 2.5×. However, the area overhead is 4× (vs. 3× for TMR). The iPACE-CHIP evaluates QMR only for the mode control FSM, where the additional protection justifies the overhead.

### TMR with Self-Checking

TMR with self-checking adds error detection to the voting process:

```
         Replica1 ──┐
         Replica2 ──┼──► Voter ──► Output
         Replica3 ──┘
                    │
                    ▼
               Error_Detect = (A ≠ B) OR (B ≠ C) OR (A ≠ C)
```

If any two replicas disagree, an error flag is raised. This allows the system to:
1. Know that an SEU has occurred (even if the voter corrects it)
2. Trigger a scrub of the affected replica
3. Log the error for diagnostic purposes
4. Escalate the response if errors become frequent

The iPACE-CHIP's self-checking TMR raises a non-maskable interrupt on error detection, which triggers:
- ECC check on the affected register
- Re-writing of the register with the corrected value (scrubbing)
- Logging of the error in the diagnostic memory
- If three or more errors occur within one hour, triggering a safe-state transition

### TMR with Recovery

TMR with recovery goes beyond error detection to actively repair the errored replica:

```
         Replica1 ──┬──► Voter ──► Output ──┬──► Replica1 (feedback)
         Replica2 ──┤                       ├──► Replica2 (feedback)
         Replica3 ──┘                       └──► Replica3 (feedback)
```

The voted output is fed back to all three replicas' data inputs. This ensures that within one clock cycle, all three replicas are re-synchronized to the correct value. The errored replica is automatically "repaired" by the feedback mechanism.

**Critical Design Requirement:** The feedback path must be glitch-free. If the feedback carries an incorrect value (due to an SEU in the voter), all three replicas would be corrupted simultaneously. The dual-stage voter (described in Section 10.1.3.2) mitigates this risk.

### Modular Redundancy with Comparison (MRC)

Instead of voting, the iPACE-CHIP uses comparison for some non-critical paths where dual redundancy with error detection is sufficient:

```
         Module1 ──┬──► Comparator ──► Error Flag
         Module2 ──┘
```

If the two modules disagree, an error is detected but not corrected. The system can then take corrective action (e.g., use a known-safe default value, or switch to a redundant functional block).

MRC is used for the iPACE-CHIP's:
- Temperature sensor (disagreement triggers a recalibration)
- Battery voltage monitor (disagreement triggers a more precise measurement)
- Telemetry CRC checker (disagreement triggers a retransmission request)

---

## 10.1.3.4 Partial TMR Strategies

### Selective TMR

Full TMR on the entire iPACE-CHIP would consume approximately 3× the area and power — an unacceptable overhead for a battery-powered implantable device. The iPACE-CHIP therefore implements selective TMR, applying TMR only to the blocks that meet all of the following criteria:

1. **Criticality:** The block's correct operation is essential for patient safety (Category A or B)
2. **SEU Sensitivity:** The block's per-bit SEU rate is high enough to make TMR cost-effective
3. **Area Budget:** The TMR overhead fits within the die area budget

The selective TMR mapping for the iPACE-CHIP:

| Functional Block | Criticality | TMR Applied? | Justification |
|---|---|---|---|
| Mode control FSM | A | Full TMR | Single-fault tolerant |
| Pacing output register | A | Full TMR | Single-fault tolerant |
| Sensing threshold register | A | Full TMR | Single-fault tolerant |
| Rate limit registers | B | Full TMR | Redundant monitoring |
| Pacing rate counter | A | Full TMR | Timing-critical |
| AV delay timer | A | Full TMR | Timing-critical |
| Sensing digital filter | B | Module TMR | Large module, amortized cost |
| Telemetry encoder | C | MRC only | Non-life-critical |
| Diagnostic registers | C | ECC only | Logged and reported |
| Clock divider | B | Full TMR | Clock is single point of failure |
| Power management FSM | A | Full TMR | Supply control critical |
| Watchdog timer | A | Full TMR | Safety monitor |

### Time-Division TMR

For very large functional blocks where even module-level TMR is too expensive, the iPACE-CHIP evaluates time-division TMR: the module is replicated three times in time rather than space.

The module operates three times faster than needed (3× clock frequency), and the three results are latched and voted:

```
Module (3× clock) ──► Result1 ──┐
              (cycle 1)          │
Module (3× clock) ──► Result2 ──┼──► Voter ──► Output
              (cycle 2)          │
Module (3× clock) ──► Result3 ──┘
              (cycle 3)
```

Time-division TMR has the same reliability as spatial TMR but uses only 1/3 the area (at the cost of 3× the clock speed and 3× the power during the computation phase).

The iPACE-CHIP evaluates time-division TMR for the telemetry CRC generator, which is large but operates intermittently (only during telemetry transmission). By running the CRC computation three times at 48 MHz (3× the normal 16 MHz clock) and voting on the result, the iPACE-CHIP achieves TMR-equivalent protection without tripling the CRC hardware.

### Hierarchical TMR

The iPACE-CHIP uses a hierarchical TMR approach where the outer level is module-level TMR and the inner level is register-level TMR:

```
Module TMR (outer level):
  Module_1 (with internal register TMR) ──┐
  Module_2 (with internal register TMR) ──┼──► Module Voter ──► Output
  Module_3 (with internal register TMR) ──┘
```

This provides two levels of protection:
1. If one module produces an incorrect output due to an internal SEU, the module voter corrects it.
2. If an SEU occurs in a module's voter (inner level TMR voter), the module may produce an incorrect output, but the module voter (outer level) corrects it.

The hierarchical approach is used for the iPACE-CHIP's pacing output controller, which is the most critical functional block:

```
Pacing Controller TMR Architecture:

  Replica 1:                     Replica 2:                     Replica 3:
  ┌─────────────────┐           ┌─────────────────┐           ┌─────────────────┐
  │ Mode FSM (TMR)  │           │ Mode FSM (TMR)  │           │ Mode FSM (TMR)  │
  │ Rate Ctr (TMR)  │           │ Rate Ctr (TMR)  │           │ Rate Ctr (TMR)  │
  │ AV Timer (TMR)  │           │ AV Timer (TMR)  │           │ AV Timer (TMR)  │
  │ Output Reg (TMR)│           │ Output Reg (TMR)│           │ Output Reg (TMR)│
  └────────┬────────┘           └────────┬────────┘           └────────┬────────┘
           │                             │                             │
           └─────────────────────────────┼─────────────────────────────┘
                                         ▼
                                   Module Voter
                                         │
                                         ▼
                                   Output to Pulse Generator
```

---

## 10.1.3.5 Common-Mode Failure Prevention

### The Common-Mode Problem

TMR protects against independent failures in the three replicas. However, if a single event or condition causes all three replicas to fail simultaneously (common-mode failure), TMR provides no protection.

Common-mode failure sources in the iPACE-CHIP include:

1. **Power supply glitch:** A momentary drop in VDD can reset all three replicas simultaneously
2. **Clock glitch:** A single-event transient on the clock network can affect all three replicas simultaneously
3. **Shared combinational logic:** If the three replicas share a common input signal path, an SEU in that path affects all three replicas
4. **Process variation:** Systematic manufacturing defects can make all three replicas vulnerable to the same failure mode
5. **Radiation burst:** An extremely high-LET particle or a burst of multiple particles can upset multiple replicas simultaneously

### Common-Mode Mitigation Techniques

**Independent Power Domains:** The three TMR replicas for Category A blocks are powered by separate LDO regulators, each with its own decoupling capacitor. A supply glitch on one LDO does not affect the other two:

```
Battery ──► PMIC ──┬──► LDO_1 ──► Replica_1
                   ├──► LDO_2 ──► Replica_2
                   └──► LDO_3 ──► Replica_3
```

The area overhead for three separate LDOs is significant (~0.5 mm² total), but this is justified for Category A blocks.

**Independent Clock Domains:** Each TMR replica receives its clock from a separate clock buffer, driven by different physical locations on the clock tree:

```
Crystal Oscillator ──► Clock Buffer Tree:
                        ├──► Buffer_A ──► Replica_1_CLK
                        ├──► Buffer_B ──► Replica_2_CLK
                        └──► Buffer_C ──► Replica_3_CLK
```

An SET on one buffer affects only one replica's clock. The clock buffers are physically separated by >10 μm to prevent a single particle from affecting multiple buffers.

**Independent Input Paths:** The inputs to each TMR replica are driven by separate registers:

```
Input Register ──┬──► Input_Reg_1 ──► Replica_1
                 ├──► Input_Reg_2 ──► Replica_2
                 └──► Input_Reg_3 ──► Replica_3
```

Each input register is independently protected by ECC. An SEU in one input register affects only one replica.

**Diverse Redundancy:** For the most critical functions, the iPACE-CHIP uses diverse redundancy — implementing the same function using different circuit topologies:

```
Mode Control:
  Replica 1: Moore FSM (state depends only on current state)
  Replica 2: Mealy FSM (state depends on current state and inputs)
  Replica 3: Moore FSM (identical to Replica 1)

Output Voter: compares all three
```

Diverse redundancy protects against systematic errors that might affect two identical implementations but not a differently-designed implementation. However, it significantly increases the design and verification effort, so it is used only for the mode control FSM.

---

## 10.1.3.6 TMR and Error Correction Code Interaction

### Combined TMR+ECC Strategy

The iPACE-CHIP combines TMR and ECC for a layered protection approach:

**Category A Registers:** Full TMR with ECC on each replica's register. This provides:
- TMR correction of single-replica SEUs
- ECC correction of single-bit errors within a replica (independent of TMR)
- Combined detection of double errors within a single replica
- Self-checking capability for all error types

**Category B Registers:** ECC (SEC-DED) without TMR. The ECC corrects single-bit errors and detects double-bit errors. The detection capability allows the system to trigger a scrub before a third error occurs.

**Category C Registers:** ECC (SEC-DED) with periodic scrubbing. No real-time correction, but errors are detected and corrected during the next scrub cycle.

### TMR vs. ECC Cost-Benefit Analysis

| Parameter | TMR | ECC (SEC-DED) | TMR + ECC |
|---|---|---|---|
| Area overhead (for 32-bit register) | 3× register + voter | 15% (7 check bits per 32 data bits) | 3× + 15% |
| Power overhead | 3× | 10–15% | 3× + 15% |
| Corrects single-bit SEU | Yes (via voter) | Yes (via syndrome) | Yes (redundantly) |
| Detects double-bit SEU | Yes (error flag) | Yes (uncorrectable syndrome) | Yes |
| Corrects double-bit SEU | No | No | Partially (if bits are in different replicas) |
| Latency | 1 voter delay | 1 ECC check delay | 1 voter delay |
| Complexity | Low | Medium | Medium |

The iPACE-CHIP's combined approach is justified for Category A registers because:
1. The area overhead is acceptable (Category A registers are a small fraction of the die)
2. The combined protection provides defense-in-depth (TMR and ECC operate independently)
3. The self-checking capability enables proactive error management

---

## 10.1.3.7 TMR Timing and Synchronization

### Clock Skew Between Replicas

When three replicas are powered by separate LDOs and clocked by separate buffers, the clock edges may not be perfectly aligned. Clock skew between replicas can cause:

1. **Metastability at the voter:** If the three replicas are sampled at slightly different times, the voter may receive inconsistent data during transitions.
2. **Setup/hold violations at the voter:** If the skew exceeds the voter's timing margin, the voter may sample incorrect data.

**Mitigation:** The iPACE-CHIP uses a synchronization scheme for TMR replicas:

1. All three clock buffers are driven from the same crystal oscillator, minimizing the inherent skew.
2. The clock routing to each replica uses matched-length traces (within 5% length matching).
3. The voter includes a small synchronizer stage (a single flip-flop on each replica's output before voting) that adds 1 clock cycle of latency but ensures that the voter samples all three replicas at the same clock edge.

### Asynchronous TMR

For some applications in the iPACE-CHIP (particularly the analog-to-digital converter and the telemetry receiver), the three TMR replicas may not have a common clock — they may be free-running at slightly different frequencies. Asynchronous TMR requires:

1. **Synchronization FIFOs:** Each replica's output is buffered in a small FIFO and read by the voter at a common clock rate.
2. **Timestamp comparison:** The voter compares the timestamps of the three outputs and accepts the output with the most recent valid timestamp.
3. **Majority agreement window:** The voter waits for a configurable time window (typically 3 clock cycles) for all three replicas to produce results. If two or more agree within the window, the agreed value is accepted.

Asynchronous TMR is more complex and has higher latency than synchronous TMR, but it is necessary for the iPACE-CHIP's mixed-clock-domain architecture.

---

## 10.1.3.8 TMR Failure Modes and Diagnostics

### TMR Failure Taxonomy

| Failure Mode | Description | Detection Method | Recovery Action |
|---|---|---|---|
| Single-replica SEU | One replica's register flipped by SEU | Voter disagreement flag | Voter corrects, scrub triggered |
| Double-replica SEU | Two replicas' registers flipped | Voter detects disagreement | Emergency: use default value, safe-state |
| Triple-replica SEU | All three replicas flipped | Voter produces incorrect output | Catastrophic: safe-state transition |
| Voter SEU | Voter output temporarily incorrect | Self-checking voter flag | Dual-stage voter corrects |
| Clock SEU | One replica receives false clock edge | Replica output disagrees | Voter corrects, clock monitored |
| Power glitch | All replicas reset simultaneously | Watchdog timeout | Full system reset from backup |
| Latch-up | One replica latches up | Current monitoring | Power cycle the affected replica |

### Diagnostic Counter for TMR Errors

The iPACE-CHIP maintains a diagnostic counter that records the number of TMR errors detected by each voter:

```
TMR_Error_Counter[replica_i] = count of times replica_i was in the minority

If TMR_Error_Counter[replica_i] > threshold:
  Flag replica_i as potentially degraded
  Increase scrub frequency for replica_i
  If TMR_Error_Counter[replica_i] > critical_threshold:
    Disable replica_i and operate in dual-redundant mode
    Raise device alert
```

The threshold values are:
- Warning threshold: 3 errors in 24 hours
- Critical threshold: 10 errors in 24 hours

If a replica is flagged as degraded, the iPACE-CHIP operates in dual-redundant mode with comparison (no voting), and the patient is alerted for the next scheduled device check. This degraded mode is still safer than no redundancy, and it allows the device to continue operating until the next clinical follow-up.

---

## 10.1.3.9 TMR Physical Layout Considerations

### Placement Strategy

The physical placement of TMR replicas on the iPACE-CHIP die is critical to prevent common-mode failures:

**Minimum Separation:** Replicas must be separated by at least 10 μm to prevent a single particle from affecting multiple replicas. The separation applies in both X and Y directions.

**Maximum Separation:** Replicas must not be separated by more than 50 μm to prevent excessive clock skew and routing congestion.

**Placement Topology:** The iPACE-CHIP uses a triangular placement for three replicas:

```
         ┌─────────────┐
         │  Replica 1   │
         │  (x,y)       │
         └──────┬───────┘
                │
    ┌───────────┼───────────┐
    │           │           │
    │           │           │
┌───┴──────┐   │   ┌───────┴──┐
│Replica 2 │   │   │Replica 3 │
│(x-15,y-15)│  │   │(x+15,y-15)│
└──────────┘   │   └──────────┘
               │
          ┌────┴────┐
          │  Voter   │
          └─────────┘
```

The triangular placement ensures:
1. Equal spacing between all replica pairs (15 μm minimum)
2. The voter is equidistant from all three replicas (minimizing routing skew)
3. No two replicas share the same power rail routing

### Routing Strategy

**Dedicated Power Rails:** Each replica has its own VDD and VSS power rails, routed from different locations on the power grid. The power rails do not share any segments between replicas.

**Shielded Signal Routing:** The signals between replicas and the voter are shielded with grounded metal lines to prevent charge sharing through the interconnect.

**Redundant Vias:** All critical signal routes use redundant vias (at least 2 vias per metal-to-metal connection) to prevent opens from single-particle-induced electromigration.

---

## 10.1.3.10 Chapter Summary

TMR is the iPACE-CHIP's primary defense against single-event upsets in digital logic. The implementation strategy balances protection effectiveness against area and power overhead:

Key implementation decisions:

- **Register-level TMR** for individual critical registers (~2% area overhead)
- **Module-level TMR** for complete functional blocks (~8% area overhead)
- **Dual-stage voters** for Category A signals (voter self-protection)
- **Common-mode prevention** through independent power domains and clock buffers
- **Selective TMR** applied only to Category A and B functional blocks
- **TMR + ECC combination** for defense-in-depth on the most critical parameters
- **Physical separation** with triangular placement and dedicated routing

The total TMR overhead for the iPACE-CHIP is approximately 10–12% area and 12–15% power, which is the minimum necessary to achieve the required single-fault tolerance for a life-critical implantable pacemaker.

The next chapter (10.1.4) covers SEE rate calculation methodologies, including the environment characterization and cross-section modeling needed to predict the iPACE-CHIP's soft error rate in its implanted operating environment.

---

## References

1. Lyons, R.E., and Vanderkulk, W., "The Use of Triple-Modular Redundancy to Improve Computer Reliability," *IBM Journal of Research and Development*, Vol. 6, No. 2, 1962.
2. Pratt, V.R., et al., "Hierarchical TMR for Online Recovery from SEU," *IEEE Transactions on Nuclear Science*, Vol. 55, No. 4, 2008.
3. Nicolaidis, M., "Time Redundancy Based Soft-Error Tolerance to Rescue Nanometer Technologies," *IEEE VLSI Test Symposium*, 1998.
4. Mohanram, K., and Touba, N.A., "Partial TMR Solutions for FPGA-Based Designs Under Power and Area Constraints," *IEEE Aerospace Conference*, 2003.
5. Bolchini, C., et al., "A Self-Checking TMR Scheme for SEU Tolerance in SRAM-Based FPGAs," *IEEE Transactions on Nuclear Science*, Vol. 54, No. 4, 2007.
6. Love, A., et al., "SEU Mitigation Strategies for Digital ASICs in Radiation Environments," *GOMAC Conference*, 2009.
7. IEC 60601-1:2005, "Medical Electrical Equipment — Part 1: General Requirements for Basic Safety and Essential Performance."
8. JEDEC Standard JESD89A, "Measurement and Reporting of Alpha Particle and Terrestrial Cosmic Ray-Induced Soft Errors in Semiconductor Devices," 2006.
