# Integrated Clock Gating (ICG) Cell Design for Implantable Pacemaker ASICs

## 1. Introduction to ICG Cells

Integrated Clock Gating (ICG) cells are fundamental building blocks for reducing dynamic power consumption in the iPACE-CHIP pacemaker ASIC. These cells intelligently disable the clock signal to downstream logic when the clocked elements do not need to operate, eliminating unnecessary switching activity and conserving precious battery energy.

ICG cells are more than simple AND gates with a clock enable signal. They incorporate edge-triggered latches and glitch-free control logic to ensure clean clock gating transitions, preventing runt pulses and race conditions that could corrupt data in flip-flops. For implantable medical devices, ICG cells must also meet stringent reliability requirements, including single-event upset (SEU) immunity and metastability protection.

## 2. ICG Cell Architecture

### 2.1 Basic Latch-Based ICG

```
Standard Latch-Based ICG Cell:

         EN
          │
          ▼
      ┌───┴───┐
      │  Latch│
CLK ──┤       ├──┐
      │ (neg) │  │
      └───────┘  │
                 ▼
              ┌──┴──┐
              │ AND  │──── GCLK (gated clock)
              │ gate │
         ─────┤      │
              └──────┘

Timing Diagram:
CLK      ─┐  ┌─┐  ┌─┐  ┌─┐  ┌─┐  ┌─┐  ┌─┐
           └──┘  └──┘  └──┘  └──┘  └──┘  └──┘
EN       ────────┐                     ┌──────
                 └─────────────────────┘
EN_latch ──┐     ┌─────────────────────┐
           └─────┘                     └──────
GCLK     ─┐  ┌─┐                    ┌─┐  ┌─┐
           └──┘                     └──┘  └──┘

Key Property: GCLK transitions ONLY on falling edge of CLK
when EN changes, preventing glitches.
```

### 2.2 Enhanced ICG with Set/Reset

```
ICG Cell with Set and Reset:

           EN   SET_n  RST_n
            │     │      │
            ▼     ▼      ▼
        ┌─────────────────────┐
        │   Latch (neg)       │
CLK ────┤                     ├──┐
        │   (with async RST)  │  │
        └─────────────────────┘  │
                                 ▼
                              ┌──┴──┐
                              │ AND  │──── GCLK
                              │ gate │
                    ──────────┤      │
                              └──────┘

Asynchronous Reset:
- RST_n = 0: Latch output forced to 0
- GCLK = 0 (clock disabled during reset)
- Ensures known state at startup

Asynchronous Set:
- SET_n = 0: Latch output forced to 1
- GCLK = CLK (clock enabled during set)
- Used for emergency clock enable
```

### 2.3 ICG Cell with Scan Chain

```
ICG Cell with DFT Scan Support:

           EN  SCAN_EN  SCAN_IN
            │    │        │
            ▼    ▼        ▼
        ┌──────────────────────┐
        │   Latch (neg)        │
CLK ────┤                      ├──┐
        │   with scan MUX     │  │
        └──────────────────────┘  │
                                  ▼
                              ┌───┴──┐
                              │ AND   │──── GCLK
                              │ gate  │
                    ──────────┤       │
                              └───────┘
                                  │
                              SCAN_OUT (from latch Q)

DFT Operation:
- Normal mode: SCAN_EN = 0, Latch captures EN
- Scan mode: SCAN_EN = 1, Scan chain bypasses EN latch
- Allows testing of downstream flip-flops
- Scan_out provides observability of latch state
```

## 3. Detailed Transistor-Level Design

### 3.1 Negative Latch Implementation

```
CMOS Negative Latch (passes CLK when CLK=0):

Transistor Schematic:

V_DD ──────────────────────┬─────────────────────┐
                           │                     │
                      ┌────┴────┐            ┌───┴───┐
                      │  PMOS   │            │  PMOS  │
                      │ M1      │            │ M3     │
                      │ (CLK')  │            │ (EN)   │
                      └────┬────┘            └───┬───┘
                           │                     │
EN ──┐              ┌─────┤              ┌──────┤
     │              │     │              │      │
  ┌──┴──┐          │  ┌───┴───┐          │   ┌──┴──┐
  │ NMOS │          │  │ NMOS  │          │   │ NMOS │
  │ M2   │          │  │ M4    │          │   │ M5   │
  │ (EN) │          │  │(CLK') │          │   │(CLK')│
  └──┬──┘          │  └───┬───┘          │   └──┬──┘
     │              │      │              │      │
     └──────────────┴──────┼──────────────┴──────┘
                           │
                      ┌────┴────┐
                      │ Inverter│──── Q (latch output)
                      │ M6, M7  │
                      └────┬────┘
                           │
GND ───────────────────────┴─────────────────────┘

Operation:
- CLK = 0: M1 ON, M4 ON → EN passes to Q
- CLK = 1: M1 OFF, M4 OFF → Q held by feedback
```

### 3.2 AND Gate for Clock Gating

```
Clock Gating AND Gate:

V_DD ──────────────┬─────────────┐
                   │             │
              ┌────┴────┐   ┌────┴────┐
              │  PMOS   │   │  PMOS   │
              │  M1     │   │  M2     │
              │(LATCH_Q)│   │ (CLK)   │
              └────┬────┘   └────┬────┘
                   │             │
                   └──────┬──────┘
                          │
                     ┌────┴────┐
                     │  Output │──── GCLK
                     │  Node   │
                     └────┬────┘
                          │
                   ┌──────┴──────┐
                   │             │
              ┌────┴────┐   ┌────┴────┐
              │  NMOS   │   │  NMOS   │
              │  M3     │   │  M4     │
              │(LATCH_Q)│   │ (CLK)   │
              └────┬────┘   └────┬────┘
                   │             │
GND ───────────────┴─────────────┘

When LATCH_Q = 1: GCLK = CLK
When LATCH_Q = 0: GCLK = 0 (gated)

Sizing: PMOS W=0.5μm, NMOS W=0.36μm (equal rise/fall)
```

### 3.3 Complete ICG Cell Layout

```
ICG Cell Physical Design:

┌──────────────────────────────────────────────┐
│                  ICG Cell                     │
│                                              │
│  ┌────────────┐  ┌────────────────────────┐  │
│  │            │  │                        │  │
│  │  LATCH     │  │  AND GATE              │  │
│  │  (M1-M7)   │  │  (M1-M4)              │  │
│  │            │  │                        │  │
│  │  3.2μm ×   │  │  2.4μm × 1.8μm        │  │
│  │  2.0μm     │  │                        │  │
│  │            │  │                        │  │
│  └────────────┘  └────────────────────────┘  │
│                                              │
│  Pins:                                       │
│  - CLK  (clock input, left side)             │
│  - EN   (enable input, left side)            │
│  - GCLK (gated clock output, right side)     │
│  - VDD  (power, top)                         │
│  - VSS (ground, bottom)                      │
│                                              │
│  Cell Area: 5.6μm × 3.8μm = 21.3 μm²       │
│  Total Transistors: 11                       │
│  Input Capacitance: 8 fF (CLK), 4 fF (EN)   │
└──────────────────────────────────────────────┘
```

## 4. Timing Analysis

### 4.1 Setup and Hold Requirements

```
ICG Cell Timing Constraints:

Setup Time (EN to CLK falling edge):
t_setup = t_latch_setup + t_and_delay
t_setup ≈ 0.15 ns + 0.05 ns = 0.20 ns

Hold Time (EN after CLK falling edge):
t_hold = t_latch_hold - t_and_delay
t_hold ≈ 0.05 ns - 0.03 ns = 0.02 ns

Clock-to-Q Delay (CLK falling edge to GCLK):
t_cq = t_latch_q + t_and_prop
t_cq ≈ 0.25 ns + 0.08 ns = 0.33 ns

Clock Duty Cycle:
- Minimum: 30% (latch transparency window)
- Maximum: 70%
- Nominal: 50%
```

### 4.2 Glitch-Free Operation

```
Glitch-Free Analysis:

Scenario 1: EN changes during CLK high
- Latch is opaque (holding previous value)
- EN change does not affect GCLK
- GCLK continues as CLK
- NO GLITCH

Scenario 2: EN changes during CLK low
- Latch is transparent (passing EN to AND gate)
- GCLK = EN AND CLK = EN AND 0 = 0
- GCLK remains 0 until CLK goes high
- If EN=1 when CLK goes high: GCLK starts cleanly
- If EN=0 when CLK goes high: GCLK remains 0
- NO GLITCH

Scenario 3: EN changes near CLK falling edge
- Latch captures EN on falling edge
- Setup/hold timing must be met
- If violated: metastable output possible
- Mitigation: Timing constraints enforce safe window

Verification: All scenarios produce clean clock transitions
```

### 4.3 Minimum Pulse Width

```
ICG Minimum Pulse Width Analysis:

When clock gating occurs, the last GCLK pulse must have
sufficient width for downstream flip-flops:

Minimum GCLK Pulse Width:
t_pulse_min = t_ff_setup + t_ff_hold + t_logic_delay
t_pulse_min ≈ 0.10 + 0.05 + 0.15 = 0.30 ns

For 32 kHz clock (period = 30.5 μs):
- 50% duty cycle: pulse width = 15.25 μs
- Well above minimum requirement
- No minimum pulse width violation possible

For 256 kHz clock (period = 3.9 μs):
- 50% duty cycle: pulse width = 1.95 μs
- Still well above minimum requirement
- Safe operation at all iPACE-CHIP frequencies
```

## 5. Power Analysis of ICG Cells

### 5.1 ICG Cell Internal Power

```
ICG Cell Power Consumption:

When GCLK is Active (clock passes through):
- AND gate switching: P_and = C_and × V_DD² × f
- AND gate capacitance: ~2 fF
- P_and = 2 fF × (1.8V)² × 32 kHz = 0.21 nW

When GCLK is Gated (clock disabled):
- Latch holding: P_hold ≈ 0 (static only)
- Leakage: ~10 pA × 1.8V = 18 pW
- Total gated power: 18 pW

EN switching overhead:
- Latch transitions: ~5 fF × (1.8V)² × f_EN
- If f_EN = f_CLK: P_latch = 5 fF × 3.24 × 32 kHz = 0.52 nW
- If f_EN = f_CLK/4: P_latch = 0.13 nW
```

### 5.2 Power Savings from ICG

```
Power Savings Analysis:

Without ICG (always running clock):
- Total clocked flip-flops: 5000
- Average capacitance per FF: 10 fF
- Total clock capacitance: 50 pF
- Clock power (32 kHz): 50 pF × (1.8V)² × 32 kHz = 5.18 μW

With ICG (assuming 70% clock gated):
- Active FFs: 30% of 5000 = 1500
- Active capacitance: 15 pF
- Clock power: 15 pF × 3.24 × 32 kHz = 1.55 μW
- ICG overhead: 50 cells × 0.2 nW = 10 nW
- Net savings: 5.18 - 1.55 - 0.01 = 3.62 μW

Savings Percentage: 69.9%
Energy per year saved: 3.62 μW × 3.15 × 10⁷ s = 114 mJ
```

### 5.3 ICG Granularity Impact

```
ICG Granularity Analysis:

Approach 1: Coarse-Grained (1 ICG per block)
- Number of ICG cells: 20
- Gating efficiency: 60% (less precise)
- Power savings: 2.9 μW
- Area overhead: 20 × 21.3 μm² = 426 μm²

Approach 2: Medium-Grained (1 ICG per module)
- Number of ICG cells: 100
- Gating efficiency: 70% (moderate precision)
- Power savings: 3.6 μW
- Area overhead: 100 × 21.3 μm² = 2130 μm²

Approach 3: Fine-Grained (1 ICG per register group)
- Number of ICG cells: 500
- Gating efficiency: 80% (high precision)
- Power savings: 4.1 μW
- Area overhead: 500 × 21.3 μm² = 10,650 μm²

iPACE-CHIP Recommendation:
- Medium-grained: 100 ICG cells
- Best balance of savings vs. overhead
- Gating efficiency: 70%
```

## 6. Clock Tree Integration

### 6.1 ICG Placement in Clock Tree

```
ICG Clock Tree Structure:

                ┌─────────┐
                │ 32 kHz  │
                │  OSC    │
                └────┬────┘
                     │
              ┌──────┴──────┐
              │   Buffer    │
              └──────┬──────┘
                     │
         ┌───────────┼───────────┐
         │           │           │
    ┌────┴────┐ ┌────┴────┐ ┌────┴────┐
    │  ICG-1  │ │  ICG-2  │ │  ICG-3  │
    │(Sensing)│ │  (DSP)  │ │(Stim)   │
    └────┬────┘ └────┬────┘ └────┬────┘
         │           │           │
    ┌────┴────┐ ┌────┴────┐ ┌────┴────┐
    │ Buffer  │ │ Buffer  │ │ Buffer  │
    └────┬────┘ └────┬────┘ └────┬────┘
         │           │           │
    ┌────┴────┐ ┌────┴────┐ ┌────┴────┐
    │ FF      │ │ FF      │ │ FF      │
    │ Array   │ │ Array   │ │ Array   │
    │ (200)   │ │ (2000)  │ │ (300)   │
    └─────────┘ └─────────┘ └─────────┘

ICG Placement Rules:
1. ICG placed BEFORE clock buffers in the tree
2. Buffer load minimized when clock is gated
3. ICG EN signal driven from control logic
4. Clock tree balanced after ICG insertion
```

### 6.2 Clock Skew Management

```
ICG-Induced Clock Skew Analysis:

Skew Sources:
1. Different ICG delays in parallel paths
2. Different wire lengths after ICG
3. Different buffer loads after ICG

Skew Budget:
- ICG delay variation: ±0.05 ns
- Buffer delay variation: ±0.03 ns
- Wire delay variation: ±0.02 ns
- Total skew: √(0.05² + 0.03² + 0.02²) = 0.063 ns

Skew Tolerance:
- Setup time margin: 0.20 ns
- Clock period (32 kHz): 30,500 ns
- Skew/period ratio: 0.063/30500 = 0.0002%
- No timing impact at 32 kHz

At 256 kHz (period = 3,900 ns):
- Skew/period ratio: 0.063/3900 = 0.002%
- Still negligible
```

### 6.3 Clock Tree Synthesis with ICG

```
CTS Flow with ICG Insertion:

Step 1: Pre-CTS ICG Insertion
- Insert ICG cells based on enable signals
- ICG placement in RTL or gate-level netlist
- Do NOT optimize ICG placement during CTS

Step 2: Clock Tree Building
- Build balanced clock tree from root to ICGs
- Insert buffers to balance ICG input delays
- Ensure ICG clock inputs have equal skew

Step 3: Post-ICG Balancing
- Build clock tree from ICG outputs to sinks
- Insert buffers for fanout management
- Balance skew between gated clock domains

Step 4: Timing Verification
- Check setup/hold for all flip-flops
- Verify clock skew within budget
- Check ICG enable timing constraints

Step 5: Power Verification
- Verify ICG switching activity
- Check enable signal timing
- Confirm clock gating is effective
```

## 7. Verification Methodology

### 7.1 Functional Verification

```
ICG Functional Test Cases:

Test 1: Basic Gating
- Enable = 0, verify GCLK = 0
- Enable = 1, verify GCLK = CLK
- Verify no glitches on GCLK transitions

Test 2: Enable During Clock High
- CLK = 1, toggle EN
- Verify GCLK does not change during CLK = 1
- Verify GCLK follows CLK when CLK goes low

Test 3: Enable During Clock Low
- CLK = 0, toggle EN
- Verify GCLK remains 0
- Verify GCLK starts cleanly when CLK goes high

Test 4: Fast Enable Toggling
- EN toggles at clock frequency
- Verify GCLK toggles every other cycle
- Verify no duty cycle distortion

Test 5: Simultaneous Enable/Reset
- Assert reset while EN = 1
- Verify GCLK = 0 during reset
- Verify GCLK resumes after reset release

Test 6: Metastability
- EN changes within setup/hold window
- Verify no metastable GCLK output
- Verify recovery within one clock cycle
```

### 7.2 Assertion-Based Verification

```
ICG SystemVerilog Assertions:

// Glitch-free assertion
property no_glitch_on_gclk;
  @(posedge CLK) disable iff (!RST_n)
    $fell(GCLK) |=> GCLK == 0 until !CLK;
endproperty

// Clock gating correctness
property clock_gated_when_disabled;
  @(posedge CLK) disable iff (!RST_n)
    !EN && $past(!EN) |=> GCLK == 0;
endproperty

// Clock passes when enabled
property clock_passes_when_enabled;
  @(posedge CLK) disable iff (!RST_n)
    EN && $past(EN) |=> GCLK == CLK;
endproperty

// No runt pulses
property no_runt_pulses;
  @(posedge CLK) disable iff (!RST_n)
    $rose(GCLK) |-> GCLK throughout 
    (##[1:$] $fell(CLK));
endproperty
```

### 7.3 Formal Verification

```
ICG Formal Verification Properties:

Equivalence Checking:
- RTL ICG cell ↔ Gate-level ICG cell
- Latch behavior equivalence
- AND gate behavior equivalence
- Reset/set behavior equivalence

Formal Properties to Prove:
1. GCLK is glitch-free for all EN sequences
2. GCLK = 0 when EN = 0 (after settling)
3. GCLK = CLK when EN = 1 (after settling)
4. Reset forces GCLK = 0
5. No combinational loops through ICG
6. EN signal is properly sampled

Abstraction:
- Clock domain: single domain
- Reset: asynchronous active-low
- Temperature: nominal (37°C)
- Process: nominal (TT corner)
```

## 8. DFT (Design for Test) Considerations

### 8.1 ICG Scan Chain Integration

```
ICG Scan Chain Architecture:

Normal Operation:
CLK ──► ICG ──► GCLK ──► FF array
EN ──────┘

Scan Operation:
SCAN_CLK ──────────────────────────► FF array
SCAN_EN ──► ICG (bypasses EN latch)
SCAN_IN ──► ICG (test access)

Test Mode:
1. Assert SCAN_EN = 1
2. ICG latch transparent to SCAN_IN
3. Scan chain operates normally
4. All flip-flops testable

DFT Rules for ICG:
1. ICG must have scan_in/scan_out pins
2. EN latch must be bypassable in scan mode
3. GCLK output must be observable
4. ICG must not block scan chain propagation
```

### 8.2 ICG Bypass for Test

```
ICG Test Bypass Mechanism:

┌─────────────────────────────────────────┐
│ ICG Test MUX                            │
│                                         │
│  EN ──────┐                             │
│           │    ┌───────────┐            │
│           ├───►│  Latch    │            │
│  CLK ─────┤    └─────┬─────┘            │
│           │          │                  │
│           │    ┌─────▼─────┐            │
│           ├───►│    AND    ├───► GCLK   │
│           │    └───────────┘            │
│  SCAN_EN ─┤                             │
│           │    ┌───────────┐            │
│  SCAN_IN ─┤───►│ Scan MUX  │            │
│           │    └───────────┘            │
└─────────────────────────────────────────┘

Bypass Operation:
- SCAN_EN = 0: Normal ICG operation
- SCAN_EN = 1: SCAN_IN replaces EN latch output
- Allows testing ICG cell itself
- Allows testing downstream logic without ICG
```

## 9. ICG Cell Variants

### 9.1 Standard ICG Variants

```
ICG Cell Library Variants:

Variant 1: Basic ICG
- Pins: CLK, EN, GCLK, VDD, VSS
- Area: 21.3 μm²
- Power: 0.21 nW active
- Use: General purpose

Variant 2: ICG with Enable Buffer
- Pins: CLK, EN, GCLK, VDD, VSS
- Area: 24.5 μm²
- Power: 0.25 nW active
- Use: High fanout enable signals

Variant 3: ICG with Scan
- Pins: CLK, EN, SCAN_EN, SCAN_IN, SCAN_OUT, GCLK, VDD, VSS
- Area: 28.0 μm²
- Power: 0.28 nW active
- Use: DFT-required blocks

Variant 4: ICG with Set/Reset
- Pins: CLK, EN, SET_n, RST_n, GCLK, VDD, VSS
- Area: 26.0 μm²
- Power: 0.26 nW active
- Use: Critical control paths

Variant 5: High-Drive ICG
- Pins: CLK, EN, GCLK, VDD, VSS
- Area: 35.0 μm²
- Power: 0.40 nW active
- Use: Clock tree root, high fanout
```

### 9.2 Specialized ICG for iPACE-CHIP

```
iPACE-CHIP Custom ICG Cell:

Design Requirements:
- Ultra-low leakage (< 10 pA)
- Radiation-hardened (SEU immune)
- Wide temperature range (-20°C to +50°C)
- Metastability-free design

Custom ICG Implementation:
┌──────────────────────────────────────────┐
│ iPACE-CHIP ICG-SEU                       │
│                                          │
│  Features:                               │
│  - Dual-edge latch (redundancy)          │
│  - Feedback triplicated (TMR)            │
│  - Glitch filter on EN input             │
│  - Power: 0.30 nW active                 │
│  - Leakage: 5 pA                         │
│  - Area: 38 μm²                          │
│  - SEU cross-section: < 10⁻⁹ cm²/bit    │
│                                          │
│  Use: All clock gating in pacemaker      │
│  logic where single Event Upset could    │
│  cause incorrect pacing                   │
└──────────────────────────────────────────┘
```

## 10. Summary

ICG cell design is a cornerstone of clock power management in the iPACE-CHIP pacemaker ASIC. The latch-based architecture ensures glitch-free clock gating, while proper timing constraints prevent metastability. With 100 ICG cells at medium granularity, the iPACE-CHIP achieves 70% clock gating efficiency, saving 3.6 μW of dynamic power. The custom iPACE-CHIP ICG cell incorporates radiation hardening for implantable medical device reliability, with ultra-low leakage of 5 pA and total cell area of 38 μm². Integration with the clock tree through proper CTS methodology ensures minimal skew impact, while DFT scan support enables complete testability. The ICG cells contribute significantly to meeting the 2.9 μW average power budget required for 10-year battery life.

## References

1. Benini, L., et al., "Optimal Signal Shifting for Low-Power CMOS Design," IEEE Trans. VLSI Systems, 1997.
2. Tsui, F., et al., "Power Issues in Mobile Computing," Springer, 1998.
3. iPACE-CHIP Project Internal Documentation: ICG Cell Design Specification, Rev 1.5.
4. Synopsys DesignWare Library: Clock Gating Cells Technical Reference Manual.
5. ARM Low-Power Design Guide: Clock Gating Methodology, 2019.
