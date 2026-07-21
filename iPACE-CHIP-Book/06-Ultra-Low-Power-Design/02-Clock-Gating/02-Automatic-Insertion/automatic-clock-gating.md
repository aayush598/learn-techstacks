# Automatic Clock Gating Insertion for Implantable Pacemaker ASICs

## 1. Introduction to Automatic Clock Gating

Automatic clock gating insertion is an Electronic Design Automation (EDA) process that identifies opportunities to disable clock signals in idle logic blocks without manual RTL modifications. For the iPACE-CHIP pacemaker ASIC, automated clock gating is essential for systematically reducing dynamic power consumption while maintaining design productivity and correctness.

The automated flow analyzes switching activity, identifies enable conditions, and inserts Integrated Clock Gating (ICG) cells at optimal locations in the clock tree. This approach complements manual RTL-level clock gating by capturing opportunities that would be impractical to identify manually, particularly in complex data paths and control logic.

## 2. Clock Gating Analysis Methodology

### 2.1 Switching Activity Collection

```
Switching Activity Data Flow:

Step 1: RTL Simulation with Testbench
├── Run representative workloads
├── Generate VCD (Value Change Dump) file
├── Cover all operating modes
└── Capture minimum 10,000 clock cycles

Step 2: Activity Extraction
├── Toggle count per net
├── Signal probability per net
├── Clock domain identification
└── Enable condition recognition

Step 3: Activity File Generation
├── SAIF (Switching Activity Interchange Format)
├── VCD (compressed)
└── TCF (Transition Count Format)

Step 4: Analysis Tool Input
├── Read activity file
├── Map to synthesis netlist
├── Annotate switching data
└── Generate gating opportunities report
```

### 2.2 Enable Signal Identification

```
Enable Signal Detection Algorithm:

Input: Gate-level netlist + switching activity
Output: Candidate enable signals for clock gating

Algorithm Steps:
1. Identify all flip-flops in design
2. For each flip-flop:
   a. Trace D input to find combinational logic cone
   b. Identify signals that control whether D is sampled
   c. Check if signal is stable when not sampling
   d. Compute clock gating benefit (power saved)
   e. Compute timing overhead (setup/hold impact)
3. Rank candidates by benefit/overhead ratio
4. Select top candidates within area budget

Example Enable Conditions:
- Counter enable: `counter_enable = (state == COUNTING)`
- Register write enable: `wr_en = (bus_valid & bus_ready)`
- Pipeline stall: `!stall && !flush`
- Mode select: `active_mode && !sleep`
```

### 2.3 Power Savings Estimation

```
Clock Gating Benefit Calculation:

For each candidate gating opportunity:

P_saved = C_FF × V_DD² × f_CLK × α_CLK × N_FF × (1 - α_EN)

Where:
- C_FF: Capacitance per flip-flop (10 fF)
- V_DD: Supply voltage (1.8V)
- f_CLK: Clock frequency (32 kHz)
- α_CLK: Clock toggle rate (1.0)
- N_FF: Number of flip-flops gated together
- α_EN: Enable signal activity (0 = always gated, 1 = never gated)

Example Calculation:
- N_FF = 50 (50 flip-flops gated by same enable)
- α_EN = 0.3 (enable active 30% of time)
- P_saved = 10fF × 3.24V² × 32kHz × 1.0 × 50 × (1 - 0.3)
- P_saved = 10 × 3.24 × 32000 × 50 × 0.7 × 10⁻¹⁵
- P_saved = 363 nW

Overhead Calculation:
- ICG cell power: 0.21 nW
- ICG cell area: 21.3 μm²
- Net benefit: 363 - 0.21 = 362.8 nW
```

## 3. Automatic Insertion Flow

### 3.1 High-Level Flow Diagram

```
Automatic Clock Gating Insertion Flow:

┌─────────────────────┐
│ RTL Design          │
│ (Verilog/VHDL)      │
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│ Clock Gating        │
│ Analysis            │
│ (switching activity)│
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│ Enable Candidate    │
│ Identification      │
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│ Gating Opportunity  │
│ Ranking & Selection │
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│ ICG Cell Insertion  │
│ (gate-level)        │
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│ Clock Tree Synthesis│
│ (with ICGs)         │
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│ Timing Verification │
│ (setup/hold check)  │
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│ Power Verification  │
│ (activity check)    │
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│ Final Netlist       │
│ (with clock gating) │
└─────────────────────┘
```

### 3.2 Synthesis Tool Configuration

```
Synopsys Design Compiler Clock Gating Setup:

# Enable clock gating optimization
set_clock_gating_style -sequential_cell latch \
    -minimum_bitwidth 4 \
    -max_fanout 16 \
    -positive_edge_logic {integrated} \
    -negative_edge_logic {integrated} \
    -async_cell {reset} \
    -register_merging true \
    -hierarchical_flop true

# Clock gating threshold
set_clock_gating_threshold -setup 0.2 \
    -hold 0.05 \
    -clock_latency 0.1

# Clock gating power analysis
report_clock_gating -all_registers -gated_clock

# Clock gating insertion
compile_ultra -gate_clock

# Post-insertion verification
check_clock_gating
report_clock_gating -verbose
```

### 3.3 Tool-Specific Configuration

```
Cadence Genus Clock Gating Setup:

# Clock gating configuration
set_db clock_gating_enable_edge_detection true
set_db clock_gating_setup_slack_threshold 0.2
set_db clock_gating_hold_slack_threshold 0.05
set_db clock_gating_min_flops 4
set_db clock_gating_max_flops 64
set_db clock_gating_integrated_clock_gating true

# Enable register merging into clock gates
set_db clock_gating_register_merging true

# Hierarchical clock gating
set_db clock_gating_hierarchical true

# Compile with clock gating
syn_generic
syn_map
syn_opt

# Verify
report_clock_gating -summary
check_clock_gating -timing
```

## 4. Gating Strategies

### 4.1 Level-Sensitive Gating (Latch-Based)

```
Level-Sensitive Clock Gating:

This is the standard ICG approach used in iPACE-CHIP:

         EN
          │
          ▼
      ┌───┴───┐
      │ Latch │ (negative level-sensitive)
CLK ──┤       ├──┐
      └───────┘  │
                 ▼
              ┌──┴──┐
              │ AND  │──── GCLK
              └──────┘

Advantages:
- Glitch-free (no runt pulses)
- Simple timing model
- Well-supported by EDA tools
- Wide adoption in industry

Disadvantages:
- Introduces 0.5 clock cycle latency
- EN must be stable during CLK low
- Cannot gate mid-cycle

iPACE-CHIP Usage: 95% of clock gating instances
```

### 4.2 Edge-Sensitive Gating

```
Edge-Sensitive Clock Gating:

Uses a flip-flop instead of latch for EN sampling:

         EN
          │
          ▼
      ┌───┴───┐
      │  FF   │ (positive edge-triggered)
CLK ──┤       ├──┐
      └───────┘  │
                 ▼
              ┌──┴──┐
              │ AND  │──── GCLK
              └──────┘

Timing Diagram:
CLK      ─┐  ┌─┐  ┌─┐  ┌─┐  ┌─┐  ┌─┐
           └──┘  └──┘  └──┘  └──┘  └──┘
EN       ────────┐           ┌───────────
                 └───────────┘
EN_FF     ────────┐           ┌───────────
                  └───────────┘
GCLK     ─┐  ┌─┐           ┌─┐  ┌─┐
           └──┘           └──┘  └──┘

Advantages:
- Can gate any clock edge
- No transparency window concern
- More flexible gating patterns

Disadvantages:
- Introduces 1 clock cycle latency
- May miss short enable pulses
- Higher area overhead

iPACE-CHIP Usage: 5% (special cases only)
```

### 4.3 Hierarchical Clock Gating

```
Hierarchical Gating Architecture:

Level 1: Block-Level ICG
- Gates entire block clock
- Coarse granularity
- Maximum power savings
- Largest latency impact

Level 2: Module-Level ICG
- Gates individual modules
- Medium granularity
- Balanced savings and latency

Level 3: Register-Level ICG
- Gates individual register groups
- Fine granularity
- Minimum latency impact
- Smallest power savings per ICG

iPACE-CHIP Hierarchy:
                    ┌──────────┐
                    │ Level 1  │
                    │ (Block)  │
                    └────┬─────┘
            ┌────────────┼────────────┐
       ┌────┴────┐  ┌────┴────┐  ┌────┴────┐
       │ Level 2 │  │ Level 2 │  │ Level 2 │
       │ (Module)│  │ (Module)│  │ (Module)│
       └────┬────┘  └────┬────┘  └────┬────┘
       ┌────┴────┐  ┌────┴────┐  ┌────┴────┐
       │ Level 3 │  │ Level 3 │  │ Level 3 │
       │ (Reg)   │  │ (Reg)   │  │ (Reg)   │
       └─────────┘  └─────────┘  └─────────┘
```

## 5. Timing Closure with Clock Gating

### 5.1 Setup Time Analysis

```
ICG Setup Time Budget:

Path: EN → ICG Latch → AND Gate → FF_D

Required setup time:
t_setup_req = t_period - t_CLK_to_Q - t_logic - t_setup_FF

Where:
- t_period = 30.5 μs (32 kHz)
- t_CLK_to_Q = 0.33 ns (ICG output)
- t_logic = 0.20 ns (enable logic)
- t_setup_FF = 0.10 ns (flip-flop)

t_setup_req = 30500 - 0.33 - 0.20 - 0.10 = 30499.37 ns

Available time:
t_setup_avail = t_period - t_setup_FF = 30500 - 0.10 = 30499.90 ns

Slack = t_setup_avail - t_setup_req = 0.53 ns (positive = met)

At 256 kHz (period = 3.9 μs):
Slack = 3900 - 0.33 - 0.20 - 0.10 - 0.10 = 3899.27 ns (met)
```

### 5.2 Hold Time Analysis

```
ICG Hold Time Budget:

Path: CLK → ICG Latch → AND Gate → FF_D

Required hold time:
t_hold_req = t_hold_FF + t_logic - t_CLK_to_Q

Where:
- t_hold_FF = 0.05 ns (flip-flop)
- t_logic = 0.15 ns (enable logic)
- t_CLK_to_Q = 0.33 ns (ICG output)

t_hold_req = 0.05 + 0.15 - 0.33 = -0.13 ns

Negative hold requirement: hold time is always met
(no hold buffer insertion needed for ICG paths)

Verification:
- Fast corner (FF, 0°C): t_hold = 0.03 ns (still met)
- Slow corner (SS, 42°C): t_hold = -0.20 ns (marginally met)
```

### 5.3 Clock Skew Impact

```
Clock Skew Analysis with ICG:

Skew Sources:
1. ICG-to-ICG delay variation: Δt_ICG
2. Buffer delay variation: Δt_buf
3. Wire delay variation: Δt_wire
4. Load variation: Δt_load

Total Skew (RSS):
t_skew = √(Δt_ICG² + Δt_buf² + Δt_wire² + Δt_load²)

For iPACE-CHIP:
- Δt_ICG = 0.05 ns (2 identical ICGs)
- Δt_buf = 0.03 ns (matched buffers)
- Δt_wire = 0.02 ns (matched routing)
- Δt_load = 0.01 ns (similar fanout)

t_skew = √(0.0025 + 0.0009 + 0.0004 + 0.0001) = 0.063 ns

Impact on timing:
- Setup slack reduced by t_skew/2 = 0.032 ns
- Hold slack increased by t_skew/2 = 0.032 ns
- Both still met with adequate margin
```

## 6. Power Impact Analysis

### 6.1 Before and After Comparison

```
Clock Gating Impact on iPACE-CHIP Power:

Before Automatic Clock Gating:
┌─────────────────────┬──────────┬──────────┐
│ Block               │ Clock P  │ Logic P  │
├─────────────────────┼──────────┼──────────┤
│ Sensing amplifier   │ 50 nW    │ 180 nW   │
│ DSP engine          │ 500 nW   │ 530 nW   │
│ Stimulation control │ 30 nW    │ 45 nW    │
│ Communication       │ 100 nW   │ 100 nW   │
│ Housekeeping        │ 40 nW    │ 20 nW    │
│ Control logic       │ 150 nW   │ 80 nW    │
├─────────────────────┼──────────┼──────────┤
│ TOTAL               │ 870 nW   │ 955 nW   │
└─────────────────────┴──────────┴──────────┘

After Automatic Clock Gating:
┌─────────────────────┬──────────┬──────────┬──────────┐
│ Block               │ Clock P  │ Logic P  │ ICG P    │
├─────────────────────┼──────────┼──────────┼──────────┤
│ Sensing amplifier   │ 35 nW    │ 180 nW   │ 1 nW     │
│ DSP engine          │ 150 nW   │ 530 nW   │ 5 nW     │
│ Stimulation control │ 20 nW    │ 45 nW    │ 1 nW     │
│ Communication       │ 30 nW    │ 100 nW   │ 2 nW     │
│ Housekeeping        │ 10 nW    │ 20 nW    │ 1 nW     │
│ Control logic       │ 45 nW    │ 80 nW    │ 3 nW     │
├─────────────────────┼──────────┼──────────┼──────────┤
│ TOTAL               │ 290 nW   │ 955 nW   │ 13 nW    │
└─────────────────────┴──────────┴──────────┴──────────┘

Clock Power Savings: 580 nW (66.7%)
Total Power Savings: 567 nW (30.2% of total)
```

### 6.2 Mode-Specific Savings

```
Clock Gating Savings by Operating Mode:

Mode              │ Before  │ After   │ Savings │ % Saved
──────────────────┼─────────┼─────────┼─────────┼─────────
Active processing │ 1425 nW │ 1255 nW │ 170 nW  │ 11.9%
Monitoring        │ 400 nW  │ 180 nW  │ 220 nW  │ 55.0%
Idle (sleep)      │ 870 nW  │ 100 nW  │ 770 nW  │ 88.5%
Communication     │ 970 nW  │ 230 nW  │ 740 nW  │ 76.3%
──────────────────┼─────────┼─────────┼─────────┼─────────
Weighted Average  │ 870 nW  │ 290 nW  │ 580 nW  │ 66.7%

Key Insight: Clock gating is most effective during idle
and monitoring modes, which constitute 93% of operating time.
```

### 6.3 Energy Savings Projection

```
10-Year Energy Savings from Automatic Clock Gating:

Without clock gating:
- Clock power: 870 nW (always running)
- Energy over 10 years: 870 × 10⁻⁹ × 3.15 × 10⁸ = 274 mJ
- Battery percentage: 274 / 1123 = 24.4%

With clock gating:
- Clock power (weighted avg): 290 nW
- Energy over 10 years: 290 × 10⁻⁹ × 3.15 × 10⁸ = 91.4 mJ
- Battery percentage: 91.4 / 1123 = 8.1%

Energy Saved: 274 - 91.4 = 182.6 mJ
Battery Life Extension: 182.6 / 1123 = 16.3%
```

## 7. Advanced Clock Gating Techniques

### 7.1 Conditional Clock Gating

```
Conditional Gating Based on Data:

Instead of gating when enable is low, gate when data equals
current register value (no-change optimization):

Standard Enable Gating:
if (enable) Q <= D;
// Gate clock when enable = 0

Conditional (Data-Equal) Gating:
if (D != Q) Q <= D;
// Gate clock when D == Q (data unchanged)

Benefit: Additional 10-20% clock gating in pipelines
Area cost: Comparator per register group (0.5 area unit)

iPACE-CHIP Example:
- DSP pipeline registers: 30% of time D == Q
- Additional clock gating: 30% × 500 nW = 150 nW saved
```

### 7.2 Integrated Clock Gating with Logic

```
ICG with Embedded Logic:

Instead of separate enable logic + ICG, combine:

┌──────────────────────────────────────┐
│ ICG with embedded AND gate           │
│                                      │
│  EN ─────┐                           │
│          │                           │
│  A ──┐   │   ┌───────┐              │
│      ├───┴──►│ Latch │              │
│  B ──┘       └───┬───┘              │
│                  │                   │
│              ┌───▼───┐              │
│              │ AND   │              │
│              │ gate  │──► GCLK      │
│              └───────┘              │
└──────────────────────────────────────┘

Enable = A AND B (computed before latching)
Saves one AND gate level in the enable path
Reduces enable logic delay by 0.05 ns
```

### 7.3 Auto-Clock Gating in FSMs

```
FSM-Specific Clock Gating:

Finite State Machines often have states where most
registers do not change. Auto-gating detects these:

FSM State Analysis:
┌─────────────┬──────────┬──────────────┐
│ Current State│ Active FFs│ Gated FFs    │
├─────────────┼──────────┼──────────────┤
│ IDLE         │ 5/20     │ 15/20 (75%) │
│ SENSING      │ 18/20    │ 2/20 (10%)  │
│ PROCESSING   │ 20/20    │ 0/20 (0%)   │
│ STIMULATING  │ 12/20    │ 8/20 (40%)  │
│ COMMUNICATING│ 8/20     │ 12/20 (60%) │
└─────────────┴──────────┴──────────────┘

Auto-gating approach:
- Analyze state transition register usage
- Insert ICG for each state's active register set
- FSM encodes enable conditions implicitly

Average gating: (75+10+0+40+60)/5 = 37% additional
```

## 8. Verification of Automatic Insertion

### 8.1 Functional Verification

```
Post-Insertion Verification Flow:

Step 1: Equivalence Checking
├── Compare RTL vs. gate-level with ICG
├── Verify functional equivalence
├── Check for added functionality (ICG overhead only)
└── Tool: Formality/Cequency

Step 2: Gate-Level Simulation
├── Run same testbench as RTL
├── Verify identical outputs
├── Check GCLK signals for glitches
├── Verify enable timing
└── Compare VCD files

Step 3: Timing Verification
├── STA (Static Timing Analysis)
├── Check all ICG paths meet setup/hold
├── Verify clock skew within budget
├── Check min pulse width constraints
└── Tool: PrimeTime/Tempus

Step 4: Power Verification
├── Power analysis with annotated activity
├── Verify clock gating effectiveness
├── Check for ungated clock paths
├── Compare power vs. estimate
└── Tool: PrimePower/Voltus
```

### 8.2 Glitch Detection

```
Glitch-Free Verification Methodology:

Method 1: Simulation-Based
- Monitor GCLK output during gate-level simulation
- Check for runt pulses (pulse width < t_min)
- Check for glitch events (spurious transitions)
- Run for 100,000+ clock cycles

Method 2: Formal Verification
- Assert property: no runt pulses on GCLK
- Assert property: GCLK transitions only on CLK edges
- Assert property: GCLK = 0 when EN = 0 (settled)
- Use model checking to prove for all EN sequences

Method 3: Static Analysis
- Trace all paths from EN to GCLK
- Verify all paths include ICG latch
- Verify no combinational path from EN to GCLK
- Check for timing violations that could cause glitches
```

### 8.3 Power Verification

```
Post-Insertion Power Verification:

Verification Steps:
1. Extract switching activity from gate-level simulation
2. Run power analysis tool
3. Generate per-block clock power report
4. Compare with pre-insertion estimates
5. Verify all clock gating is effective

Expected Results:
┌─────────────────────┬──────────┬──────────┬──────────┐
│ Block               │ Estimated│ Actual   │ Error    │
├─────────────────────┼──────────┼──────────┼──────────┤
│ Sensing amplifier   │ 35 nW    │ 33 nW    │ -5.7%   │
│ DSP engine          │ 150 nW   │ 155 nW   │ +3.3%   │
│ Stimulation control │ 20 nW    │ 19 nW    │ -5.0%   │
│ Communication       │ 30 nW    │ 28 nW    │ -6.7%   │
│ Housekeeping        │ 10 nW    │ 11 nW    │ +10.0%  │
│ Control logic       │ 45 nW    │ 44 nW    │ -2.2%   │
├─────────────────────┼──────────┼──────────┼──────────┤
│ TOTAL               │ 290 nW   │ 290 nW   │ 0%      │
└─────────────────────┴──────────┴──────────┴──────────┘

Acceptable error: ±15% (all blocks within tolerance)
```

## 9. Integration with Design Flow

### 9.1 Complete RTL-to-GDSII Flow

```
Clock Gating in iPACE-CHIP Design Flow:

┌─────────────────────────────────────────────────┐
│ Step 1: RTL Design (with manual clock gating)   │
├─────────────────────────────────────────────────┤
│ Step 2: RTL Power Analysis (identify hotspots)  │
├─────────────────────────────────────────────────┤
│ Step 3: RTL Simulation (generate VCD/SAIF)      │
├─────────────────────────────────────────────────┤
│ Step 4: Automatic Clock Gating Insertion        │
│         (synthesis tool)                         │
├─────────────────────────────────────────────────┤
│ Step 5: Gate-Level Simulation (verify function) │
├─────────────────────────────────────────────────┤
│ Step 6: Clock Tree Synthesis (with ICGs)        │
├─────────────────────────────────────────────────┤
│ Step 7: STA (verify timing with ICGs)           │
├─────────────────────────────────────────────────┤
│ Step 8: Physical Design (place & route)         │
├─────────────────────────────────────────────────┤
│ Step 9: Post-Layout Power Analysis              │
├─────────────────────────────────────────────────┤
│ Step 10: Signoff Verification                   │
└─────────────────────────────────────────────────┘
```

### 9.2 Debug and Iteration

```
Clock Gating Debug Flow:

Issue: Power savings less than expected
├── Check: ICG cells inserted correctly?
├── Check: Enable signals properly annotated?
├── Check: Clock tree structure optimal?
└── Fix: Adjust ICG granularity or enable logic

Issue: Timing violations after clock gating
├── Check: ICG setup/hold constraints?
├── Check: Enable logic timing?
├── Check: Clock skew increased?
└── Fix: Add buffers, adjust ICG placement

Issue: Functional errors after clock gating
├── Check: Enable conditions correct?
├── Check: Reset/set behavior preserved?
├── Check: No glitch-induced errors?
└── Fix: Correct enable logic or ICG variant

Issue: Test failures after clock gating
├── Check: Scan chain integrity?
├── Check: ICG bypass in test mode?
├── Check: Clock gating disabled in test?
└── Fix: Add scan support to ICG cells
```

## 10. Summary

Automatic clock gating insertion in the iPACE-CHIP pacemaker ASIC achieves a 66.7% reduction in clock power, from 870 nW to 290 nW, while adding only 13 nW of ICG cell overhead. The automated flow identifies and implements 100 clock gating opportunities across the design, with the greatest savings occurring during idle and monitoring modes (88.5% and 55.0% respectively). The technique contributes 182.6 mJ of energy savings over the 10-year device lifetime, extending battery life by 16.3%. Integration with the standard RTL-to-GDSII flow ensures that clock gating does not compromise timing closure, testability, or functional correctness. The combination of automatic insertion with manual RTL-level gating provides comprehensive clock power optimization for the implantable pacemaker application.

## References

1. Benini, L., et al., "Automatic Synthesis of Low-Power Gated-Clock Finite State Machines," IEEE Trans. CAD, 1996.
2. iPACE-CHIP Project Internal Documentation: Clock Gating Methodology Guide, Rev 2.0.
3. Synopsys, "Design Compiler User Guide: Clock Gating," 2020.
4. Cadence, "Genus Synthesis Solution: Clock Gating," 2021.
5. Hu, Z., et al., "Automatic Clock Gating for Medical ASICs: A Practical Approach," IEEE ISLPED, 2018.
