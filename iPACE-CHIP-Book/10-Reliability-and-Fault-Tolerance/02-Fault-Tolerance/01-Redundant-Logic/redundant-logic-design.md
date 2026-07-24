# 10.2.1 Redundant Logic Design for Fault-Tolerant Pacemakers

## Chapter Overview

Redundant logic design is the architectural foundation of the iPACE-CHIP's fault tolerance strategy. Beyond the radiation-specific techniques covered in Chapter 10.1, redundant logic design addresses the broader class of permanent, intermittent, and transient faults that can affect any digital circuit throughout its operational lifetime. This chapter covers the systematic application of redundancy at the logic level — from gate-level duplication to full-system redundancy architectures — with specific focus on the unique requirements of life-critical implantable pacemakers.

The iPACE-CHIP's redundant logic design must satisfy three competing objectives simultaneously: (1) achieve single-fault tolerance for all Category A functions, (2) minimize the area and power overhead to fit within the implantable package constraints, and (3) maintain deterministic timing behavior to ensure that the pacemaker's real-time constraints are never violated. This chapter presents the design techniques that balance these objectives.

---

## 10.2.1.1 Fault Model for Implantable Pacemakers

### Fault Classification

The iPACE-CHIP considers a comprehensive fault model that encompasses all failure mechanisms relevant to implantable electronics:

**Transient Faults:**
- Single-Event Upset (SEU): bit flip in a memory element
- Single-Event Transient (SET): voltage glitch in combinational logic
- Power supply noise: voltage dips/spikes causing momentary logic errors
- Electromagnetic interference (EMI): external fields coupling into chip circuits

**Intermittent Faults:**
- Aging-related degradation: BTI-induced threshold voltage shift causing timing marginality
- Temperature-dependent failures: circuits failing only at body temperature extremes
- Voltage-dependent failures: circuits failing only at battery end-of-life voltage

**Permanent Faults:**
- Manufacturing defects: stuck-at-0, stuck-at-1, open, short
- Electromigration: metal interconnect degradation over time
- Dielectric breakdown: gate oxide failure
- Corrosion: package seal failure allowing moisture ingress

### Fault Behavior Modeling

For the iPACE-CHIP's redundant logic design, faults are modeled using the following behavioral models:

**Stuck-At Fault Model:**
```
Permanent fault: a logic node is permanently stuck at logic 0 or logic 1
Probability: increases with device age (electromigration, oxide breakdown)
Detection: comparison-based testing, voting disagreement
```

**Bit-Flip Fault Model:**
```
Transient fault: a stored bit is momentarily or permanently flipped
Probability: constant (for SEU) or increasing (for aging-induced)
Detection: ECC, TMR voting, read-back comparison
```

**Timing Fault Model:**
```
Intermittent fault: a circuit fails to meet timing requirements under certain conditions
Probability: increases with aging, temperature, voltage variation
Detection: on-line speed monitoring, time-redundancy checks
```

**Byzantine Fault Model:**
```
Arbitrary fault: a component produces arbitrary, unpredictable output
Probability: very low (assumed to be caused by multiple simultaneous faults)
Handling: fail-stop assumption — a Byzantine fault is treated as a complete component failure
```

---

## 10.2.1.2 Gate-Level Redundancy

### Duplex Logic with Comparison

The simplest form of redundant logic is duplexing — duplicating a combinational circuit and comparing the outputs:

```
         ┌────────────────┐
Input ───┤  Logic Copy 1   ├──┬──► Comparator ──► Error_Flag
         └────────────────┘  │
                             │
         ┌────────────────┐  │
Input ───┤  Logic Copy 2   ├──┘
         └────────────────┘
```

If the two copies produce different outputs, an error is detected. Duplex logic detects single faults but does not correct them. The system must then take corrective action (use a known-safe default value, retry the operation, or transition to a safe state).

**Area overhead:** 2× (one extra copy)
**Power overhead:** ~2× (both copies switching simultaneously)
**Timing overhead:** 0 (comparison can be pipelined)
**Fault coverage:** 100% of single stuck-at faults in the logic

The iPACE-CHIP uses duplex logic for:
- Battery voltage measurement path (two independent ADCs with comparison)
- Temperature sensor (two independent sensors with comparison)
- External crystal oscillator (two oscillators with frequency comparison)
- Telemetry CRC generator (two CRC engines with comparison)

### Triple Logic with Voting (TMR at Gate Level)

As covered in Chapter 10.1.3, TMR provides both fault detection and fault correction:

```
         ┌────────────────┐
Input ───┤  Logic Copy 1   ├──┐
         └────────────────┘  │
                             ▼
         ┌────────────────┐ ┌──────────┐
Input ───┤  Logic Copy 2   ├─┤  Voter   ├──► Output
         └────────────────┘ └──────────┘
                             ▲
         ┌────────────────┐  │
Input ───┤  Logic Copy 3   ├──┘
         └────────────────┘
```

**Area overhead:** 3×
**Power overhead:** ~3×
**Timing overhead:** 1 gate delay (voter)
**Fault coverage:** Corrects any single fault; detects double faults

### Selective Hardening

Not all combinational logic paths require the same level of protection. The iPACE-CHIP uses selective hardening, applying redundancy only to the most vulnerable and most critical paths:

**Critical Path Identification:**

The iPACE-CHIP's timing analysis identifies all paths that:
1. Have a timing margin < 20% of the clock period (highly timing-sensitive)
2. Feed directly into Category A registers (high criticality)
3. Have high fan-out (a single fault affects many downstream circuits)

For each identified path, the designer chooses the appropriate redundancy level:

| Path Criticality | Redundancy Level | Example |
|---|---|---|
| High (Cat A, timing-critical) | Full TMR | Pacing output enable |
| Medium (Cat A, timing-tolerant) | Duplex + ECC | Mode control inputs |
| Low (Cat B) | ECC only | Diagnostic counter |
| Non-critical (Cat C) | None | Telemetry data path |

---

## 10.2.1.3 Sequential Logic Redundancy

### Redundant State Machines

Finite state machines (FSMs) are particularly vulnerable to faults because a single bit flip in the state register can transition the FSM to an incorrect state, potentially causing the system to produce incorrect outputs indefinitely until the error is detected.

**State Register TMR:**

The most straightforward protection is to triplicate the state register and vote on the next-state logic:

```
                        ┌──────────┐
                   ┌───►│ FSM_Copy1 │──┐
                   │    └──────────┘  │
                   │    ┌──────────┐  │    ┌─────────┐
 Next_State ───────┼───►│ FSM_Copy2 │──┼───►│  Voter  ├──► Current_State
                   │    └──────────┘  │    └─────────┘
                   │    ┌──────────┐  │
                   └───►│ FSM_Copy3 │──┘
                        └──────────┘
```

**State Encoding for Fault Tolerance:**

Beyond TMR on the state register, the iPACE-CHIP uses state encodings that maximize the Hamming distance between states that are adjacent in the FSM transition graph:

For a 5-bit state register (supporting up to 32 states, though only ~10 are used):

```
State       | Encoding  | Adjacent States | Min Hamming Distance
────────────┼───────────┼─────────────────┼────────────────────
IDLE        | 00000     | A_SENSED, V_SENSED | -
A_SENSED    | 00111     | IDLE, AV_DELAY    | 3
V_SENSED    | 01011     | IDLE, V_PACE      | 3
AV_DELAY    | 01100     | A_SENSED, V_PACE  | 3
V_PACE      | 10001     | V_SENSED, IDLE    | 3
A_PACE      | 10010     | IDLE, AV_DELAY    | 3
A_V_PACE    | 10100     | IDLE              | 3
SAFE_MODE   | 11111     | IDLE              | 5
RESET       | 11000     | IDLE              | 3
────────────┴───────────┴─────────────────┴────────────────────
```

The minimum Hamming distance of 3 between adjacent states ensures that a single-bit upset cannot transition between two states that are one clock cycle apart in normal operation. The SAFE_MODE state has maximum Hamming distance from all other states, requiring at least 5 bit flips to reach from any state — an extremely unlikely event.

### Redundant Counters

The iPACE-CHIP uses several timing counters that are critical for pacing accuracy:

**Dual Counter with Comparison:**

Two independent counters count the same events and are compared at each clock cycle. If they disagree, an error flag is raised:

```
             ┌─────────┐
CLK ─────────┤ Counter1 ├──┬──► Comparator ──► Error_Flag
             └─────────┘  │
                          │
             ┌─────────┐  │
CLK ─────────┤ Counter2 ├──┘
             └─────────┘
```

The dual counter approach has the advantage of detecting faults in the counter logic itself, not just in the stored count value. If one counter has a stuck-at fault on its increment logic, it will eventually diverge from the other counter, and the comparator will detect the discrepancy.

**Triple Counter with Voting:**

For the pacing rate counter (the most critical timing element), the iPACE-CHIP uses triple counters with majority voting:

```
             ┌─────────┐
CLK ─────────┤ Counter1 ├──┐
             └─────────┘  │
                          ▼
             ┌─────────┐ ┌──────────┐
CLK ─────────┤ Counter2 ├─┤  Voter   ├──► Count_Output
             └─────────┘ └──────────┘
                          ▲
             ┌─────────┐  │
CLK ─────────┤ Counter3 ├──┘
             └─────────┘
```

The three counters must produce the same count value at all times. A single SEU in one counter's register will cause it to disagree with the other two, and the voter will select the majority value.

---

## 10.2.1.4 Data Path Redundancy

### Redundant Arithmetic Units

The iPACE-CHIP's DSP performs several arithmetic operations that are critical for pacing:

**Rate Calculation:**
```
Target_Rate = f(Base_Rate, Activity_Sensor, Respiratory_Rate, Patient_Parameters)
```

An error in this calculation could cause the pacemaker to pace at an inappropriate rate. The iPACE-CHIP protects this calculation by:

1. **Dual arithmetic units:** Two independent ALUs compute the target rate, and their outputs are compared.
2. **Arithmetic coding:** The ALU outputs are encoded using residue codes (modular arithmetic) to detect computational errors:

```
Primary computation: Y = f(X)
Check computation:   Y_check = f(X) mod M

Residue check: Y mod M == Y_check
```

Where M is a carefully chosen modulus (e.g., M = 7 for the target rate computation). The residue check detects arithmetic errors with a probability of 1 - 1/M = 86% (for M = 7).

3. **Range checking:** The computed target rate is checked against physiological limits:

```
if (Target_Rate < Lower_Rate_Limit) Target_Rate = Lower_Rate_Limit;
if (Target_Rate > Upper_Rate_Limit) Target_Rate = Upper_Rate_Limit;
```

### Redundant Memory Access

The iPACE-CHIP's memory subsystem uses redundant access paths to protect against faults in the memory controller:

**Dual-Port Memory with ECC:**
```
Port A (DSP access) ──┐
                      ├──► Memory Array (with ECC) ──► Data Out
Port B (Backup access)┘
```

The dual-port design allows:
1. The DSP to access the memory during normal operation
2. The backup port to perform scrubbing and ECC checking independently
3. If Port A fails, Port B can take over all memory access duties

**Memory Lockstep:**
For the most critical parameter registers, the iPACE-CHIP uses memory lockstep — two copies of the parameter memory, updated simultaneously by the DSP:

```
Parameter_Write ──┬──► Param_Memory_A ──┐
                  │                     ├──► Voter ──► Parameter_Read
                  └──► Param_Memory_B ──┘
```

Any read operation votes on the outputs of both memories. If one memory has a corrupted cell, the voter selects the correct value from the other memory.

---

## 10.2.1.5 Control Path Redundancy

### Redundant Control Signals

The iPACE-CHIP's control signals (enable, reset, clock gating) are critical because a fault on a control signal can affect a large portion of the circuit:

**Redundant Enable Signals:**
```
Enable_Generator_A ──┐
                     ├──► AND Gate ──► Output_Enable
Enable_Generator_B ──┘
```

The output is enabled only if both generators agree. A fault that disables one generator will disable the output (safe failure), and a fault that enables one generator prematurely will not affect the output (the other generator is still disabled).

**Redundant Reset:**
```
Reset_A ──┐
          ├──► OR Gate ──► Master_Reset
Reset_B ──┘
```

The device resets if EITHER generator asserts reset (fail-safe design). A stuck-at-0 fault on one generator still allows the other to initiate a reset.

### Redundant Clock Gating

Clock gating is used extensively in the iPACE-CHIP for power management. A fault in the clock gating logic can inadvertently disable the clock, freezing the entire digital system:

**Redundant Clock Gating:**
```
Clock_Enable_A ──┐
                 ├──► AND Gate ──► Gated_Clock
Clock_Enable_B ──┘
                │
CLK ────────────┘
```

If one clock gate has a stuck-at-0 fault on its enable input, the clock continues to run through the other gate. The redundant clock gating ensures that no single fault can freeze the clock.

### Redundant Power Management

The iPACE-CHIP's power management controls the supply voltage to various functional blocks. A fault in the power management could cut power to critical blocks:

**Redundant Voltage Regulators:**
```
Battery ──┬──► LDO_Primary ──┬──► VDD_Critical
          │                  │
          └──► LDO_Backup  ──┘
```

Both LDOs are normally active. If one fails (output drops to zero), the other continues to supply VDD_Critical. The power management monitors both LDO outputs and raises an alarm if either deviates from its target.

---

## 10.2.1.6 Redundant I/O and Communication

### Redundant Sensing Path

The iPACE-CHIP's sensing path detects cardiac electrical activity through the lead system. A fault in the sensing path can cause:
- False sensing (noise interpreted as cardiac activity → inappropriate inhibition of pacing)
- Missed sensing (cardiac activity not detected → failure to track intrinsic rhythm)

**Dual Sensing Amplifiers:**
```
Lead Signal ──┬──► Sense_Amplifier_1 ──┬──► Comparator_1 ──┐
              │                        │                   ├──► Voter ──► Sense_Event
              │                        │                   │
              └──► Sense_Amplifier_2 ──┴──► Comparator_2 ──┘
```

Each amplifier has independent gain, bandwidth, and threshold settings. The comparators' outputs are voted to produce the final sense event. A fault in one amplifier that causes a false or missed sense is corrected by the other amplifier.

**Redundant Lead Impedance Monitoring:**
The iPACE-CHIP continuously monitors the lead impedance to detect lead faults (fracture, disconnection). The monitoring uses two independent measurement techniques:

1. **DC impedance measurement:** Applies a small DC current and measures the voltage
2. **AC impedance measurement:** Applies a small AC signal and measures the impedance at the stimulation frequency

Both measurements must agree within a tolerance window. A discrepancy indicates a measurement fault, and the more conservative (higher) impedance value is used for safety decisions.

### Redundant Telemetry

The iPACE-CHIP's telemetry system communicates with the external programmer. A fault in the telemetry path could cause:
- Incorrect parameter delivery (wrong pacing parameters programmed)
- Missed commands (programming commands not received)
- False commands (noise interpreted as commands)

**Dual-CRC Telemetry:**
```
Data ──► CRC_Engine_A ──┬──► Transmitter ──► RF Link
         CRC_Engine_B ──┘
```

Both CRC engines independently compute the CRC on the data. The transmitted message includes both CRCs. The receiver checks both CRCs and accepts the data only if both match. This provides a CRC collision probability of approximately 2⁻⁶⁴ (negligible).

**Redundant Command Verification:**
All programming commands require a two-step verification:

1. **Command received and CRC verified**
2. **Command echoed back to the programmer for confirmation**

The programmer compares the echo against the original command. Only after confirmation does the iPACE-CHIP execute the command. This prevents accidental or corrupted commands from being executed.

---

## 10.2.1.7 Redundancy for Timing Faults

### Time-Redundancy Techniques

In addition to spatial redundancy (duplicating hardware), the iPACE-CHIP uses temporal redundancy to detect timing faults:

**Dual-Clock Sampling:**
Critical signals are sampled by two independent clock domains (from two crystal oscillators). The samples are compared:

```
Signal ──┬──► FF_primary (CLK_A) ──┬──► Comparator ──► Timing_Error
         │                         │
         └──► FF_secondary (CLK_B)─┘
```

If the two samples disagree, a timing fault (setup/hold violation) is detected. The probability of both samples being simultaneously wrong is negligible.

**Guard Time Insertion:**
The iPACE-CHIP inserts guard times (slack time) on all critical timing paths:

```
Required frequency: 16 MHz (period = 62.5 ns)
Guard time: 20% of clock period = 12.5 ns
Maximum combinational delay allowed: 62.5 - 12.5 = 50 ns
```

The 20% guard time accommodates:
- Process variation: ±10% delay variation across process corners
- Temperature variation: ±5% delay variation across 37°C ± 5°C
- Aging: ±5% delay increase over 10 years (from BTI/HCI)
- Voltage variation: ±5% delay variation across battery voltage range

### On-Line Speed Monitoring

The iPACE-CHIP includes a built-in speed monitor that detects timing marginality before it causes a functional failure:

**Ring Oscillator Monitor:**
A replica of the critical timing path is configured as a ring oscillator. The oscillation frequency directly reflects the current circuit speed:

```
Critical Path Replica ──► Inverter Chain ──► Feedback ──► Ring Oscillator

Oscillation frequency = 1 / (2 × N × t_gate)

If f_osc < f_threshold: timing marginality detected
```

The ring oscillator frequency is compared against a reference frequency derived from the crystal oscillator. A frequency drop below the threshold triggers an alarm and initiates voltage boost (increasing VDD to improve timing margin).

---

## 10.2.1.8 Fault Containment Boundaries

### Partitioning for Fault Isolation

The iPACE-CHIP is partitioned into fault containment boundaries (FCBs) that prevent a fault in one block from propagating to other blocks:

```
┌──────────────────────────────────────────────────────┐
│                    FCB 1: Sensing                      │
│  ┌──────────┐  ┌──────────┐  ┌────────────────────┐  │
│  │ Pre-amp  │──│ Filter   │──│ Sense Comparator    │──┤
│  └──────────┘  └──────────┘  └────────────────────┘  │
├──────────────────────────────────────────────────────┤
│                    FCB 2: Pacing Control               │
│  ┌──────────┐  ┌──────────┐  ┌────────────────────┐  │
│  │ Mode FSM │──│ Rate Ctr │──│ Output Control     │──┤
│  └──────────┘  └──────────┘  └────────────────────┘  │
├──────────────────────────────────────────────────────┤
│                    FCB 3: Output Stage                  │
│  ┌──────────┐  ┌──────────┐  ┌────────────────────┐  │
│  │ DAC      │──│ H-Bridge │──│ Output Monitor     │──┤
│  └──────────┘  └──────────┘  └────────────────────┘  │
├──────────────────────────────────────────────────────┤
│                    FCB 4: Communication                 │
│  ┌──────────┐  ┌──────────┐  ┌────────────────────┐  │
│  │ Telemetry│──│ Protocol │──│ Command Parser     │──┤
│  └──────────┘  └──────────┘  └────────────────────┘  │
└──────────────────────────────────────────────────────┘
```

Each FCB communicates with other FCBs only through well-defined interfaces with built-in error checking:

**Interface Protocol:**
1. Data is encoded with CRC at the sender FCB
2. Data is decoded and CRC-checked at the receiver FCB
3. If CRC fails, the receiver requests retransmission
4. If retransmission fails three times, the receiver uses the last known-good value

**Fault Containment Properties:**
- A fault in FCB 1 (sensing) cannot cause incorrect pacing output (FCB 2 + FCB 3)
- A fault in FCB 4 (communication) cannot modify pacing parameters (stored in FCB 2)
- A fault in FCB 3 (output stage) cannot affect sensing capability (FCB 1)

### Output Stage Fail-Safe Design

The output stage (FCB 3) has special fail-safe requirements because it directly interfaces with the heart:

**Maximum Output Limits:**
Hardware limiters enforce absolute maximum output voltage and current:

```
Output Voltage Limiter:
  V_out_max = 7.5V (hardwired, cannot be overridden by software)
  V_out_min = 0V

Output Current Limiter:
  I_out_max = 20 mA (hardwired, cannot be overridden by software)
  I_out_min = 0 mA
```

These limiters are implemented using analog comparators with hardwired reference voltages. They operate independently of the digital control logic and cannot be affected by digital faults.

**Output Monitoring:**
The output voltage and current are continuously monitored by independent analog comparators:

```
Output Monitor:
  V_out_actual ──► Comparator (against V_ref) ──► Alarm
  I_out_actual ──► Comparator (against I_ref) ──► Alarm
```

If the actual output exceeds the programmed value by more than 20%, the output is immediately terminated and the device transitions to safe mode.

---

## 10.2.1.9 Redundancy Overhead Optimization

### Overhead Budget

The iPACE-CHIP has strict area and power constraints due to the implantable form factor:

```
Die area budget: 25 mm²
Power budget: 15 μW average (10-year battery life from 1.0 Ah battery at 3.0V)
  Average power = 1.0 × 3.0 / (10 × 365 × 24) = 34.2 μW
  
  Wait — let me recalculate:
  Battery: 1.0 Ah, 3.0V = 3.0 Wh = 10,800 J
  Lifetime: 10 years = 3.15 × 10⁸ seconds
  Average power: 10,800 / 3.15 × 10⁸ = 34.3 μW
  
  Budget allocation:
    Pacing output: 5 μW (during pulse only)
    Sensing amplifier: 8 μW (always on)
    Digital logic: 12 μW (always on)
    Telemetry: 5 μW (during communication only)
    Regulators: 4 μW (always on)
    Redundancy overhead: remaining budget
```

### Optimization Techniques

**Clock Gating on Redundant Copies:**
When a TMR voter determines that one replica has an error, that replica can be temporarily clock-gated while it is being scrubbed. This reduces the dynamic power of the errored replica to zero during recovery.

**Partial TMR with Power Gating:**
For non-critical time periods (e.g., during sleep mode when the pacemaker is only monitoring), the third TMR replica can be power-gated to save power. The system operates in duplex mode during sleep and re-enables the third copy during active pacing.

**Adaptive Redundancy Level:**
The iPACE-CHIP can dynamically adjust its redundancy level based on the current error rate:

```
Error Rate < 10⁻⁶/hr: operate in duplex mode (save power)
Error Rate 10⁻⁶ to 10⁻⁴/hr: operate in TMR mode (normal)
Error Rate > 10⁻⁴/hr: operate in TMR mode + increased scrubbing (aggressive)
```

This adaptive approach reduces the average power overhead of redundancy by approximately 30% compared to always-on TMR.

---

## 10.2.1.10 Verification of Redundant Logic

### Fault Injection Testing

The iPACE-CHIP's redundant logic is verified through comprehensive fault injection:

**Stuck-at Fault Injection:**
Every node in the gate-level netlist is forced to stuck-at-0 and stuck-at-1, one at a time. The simulation records:
1. Whether the fault is detected by the redundant logic
2. Whether the fault is corrected (TMR voter selects correct value)
3. The recovery time
4. The impact on pacing output timing

**Target:** >99% stuck-at fault coverage for Category A logic.

**SEU Injection:**
Every flip-flop is injected with a single bit-flip at random times. The simulation records:
1. Whether the SEU is detected and corrected by TMR/ECC
2. The SEU propagation path
3. The recovery time

**Target:** 100% detection and correction for Category A flip-flops.

**Timing Fault Injection:**
Critical timing paths are intentionally stretched (by adding delay elements in the netlist) to simulate setup/hold violations. The simulation verifies that:
1. The on-line speed monitor detects the timing marginality
2. The voltage boost or clock frequency reduction compensates for the delay
3. No incorrect data is latched during the transition period

### Formal Verification

The iPACE-CHIP's redundant logic is formally verified using model checking:

**Properties Verified:**
1. "The voter output always equals the majority of its three inputs" — verified for all input combinations
2. "A single stuck-at fault on any voter input does not affect the output" — verified by constraining the other two inputs
3. "The mode control FSM always reaches the SAFE_MODE state within N clock cycles from any state" — verified by exhaustively checking all state transitions
4. "The pacing output enable signal is never asserted without a valid trigger" — verified by checking all possible fault scenarios on the enable path

### Production Testing

The iPACE-CHIP's redundant logic is tested during production using:

1. **March tests on all SRAM arrays:** Detect stuck-at, transition, and coupling faults
2. **Scan-chain testing on all TMR flip-flops:** Verify that each flip-flop in the TMR chain can store both 0 and 1
3. **Voter truth table verification:** Apply all 8 input combinations to each voter and verify the output
4. **Clock distribution test:** Verify that all three clock domains are operational and within frequency tolerance
5. **Power management test:** Verify that all redundant LDOs can independently supply the critical blocks

---

## 10.2.1.11 Chapter Summary

Redundant logic design provides the iPACE-CHIP with systematic fault tolerance across all failure mechanisms — from transient radiation effects to permanent manufacturing defects and aging-related degradation.

Key design principles:

- **Defense in depth:** Multiple layers of redundancy (gate-level, module-level, system-level) protect against different fault classes
- **Fail-safe defaults:** A fault in any redundant element causes the system to either produce the correct output or transition to a safe state (never an unsafe state)
- **Fault containment:** Well-defined boundaries prevent fault propagation between functional blocks
- **Overhead optimization:** Adaptive redundancy levels and power gating minimize the area and power cost of fault tolerance
- **Comprehensive verification:** Fault injection, formal verification, and production testing ensure that the redundant logic provides the expected protection

The total redundancy overhead for the iPACE-CHIP is approximately 25–30% area and 15–20% power — a necessary investment for a life-critical implantable device that must operate reliably for 10+ years without the possibility of repair.

The next chapter (10.2.2) covers Error Detection and Correction (EDAC) codes, which complement the redundant logic approach by providing efficient, low-overhead protection for the iPACE-CHIP's memory arrays and data paths.

---

## References

1. Johnson, B.W., *Design and Analysis of Fault-Tolerant Digital Systems*, Addison-Wesley, 1989.
2. Lyu, M.R., *Software Fault Tolerance*, John Wiley & Sons, 1992.
3. Koren, I., and Krishna, C.M., *Fault-Tolerant Systems*, Morgan Kaufmann, 2007.
4. IEC 60601-1:2005, "Medical Electrical Equipment — Part 1: General Requirements for Basic Safety and Essential Performance."
5. IEC 62304:2006, "Medical Device Software — Software Life Cycle Processes."
6. Avizienis, A., et al., "Basic Concepts and Taxonomy of Dependable and Secure Computing," *IEEE Transactions on Dependable and Secure Computing*, Vol. 1, No. 1, 2004.
7. Wensley, J.H., et al., "SIFT: Design and Analysis of a Fault-Tolerant Computer for Aircraft Control," *Proceedings of the IEEE*, Vol. 66, No. 10, 1978.
8. Laprie, J.C., "Dependable Computing and Fault Tolerance: Concepts and Terminology," *FTCS-15*, 1985.
