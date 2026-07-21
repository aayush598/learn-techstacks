# Timing Analysis for iPACE-CHIP ASIC

## 1. Introduction

Static Timing Analysis (STA) verifies that all signal paths in the iPACE-CHIP
gate-level netlist meet their timing constraints. Unlike simulation, STA exhaustively
analyzes every possible path without requiring test vectors, making it the definitive
signoff methodology for timing verification.

For the iPACE-CHIP, STA has unique characteristics:
- **Ultra-slow clock**: 32.768 kHz (30,518 ns period) — timing closure is trivial
- **Mixed clock domains**: 33 kHz core + 1 MHz telemetry
- **Safety derating**: Additional margin on safety-critical paths
- **Multi-corner analysis**: Must pass at all 6 operating corners
- **Aging analysis**: Must meet timing after 10-year NBTI/PBTI degradation

## 2. STA Setup and Methodology

### 2.1 STA Flow

```
iPACE-CHIP STA Flow:
═══════════════════════════════════════════════════════════════

  ┌─────────────────────────────────────────────────────────────┐
  │  Step 1: Read Netlist + Libraries + Constraints              │
  │     read_verilog ipace_chip_top.v                          │
  │     read_sdc ipace_chip_top.sdc                            │
  │     read_lib tcbn180ghpwc.lib (all corners)                │
  └───────────────────────────┬─────────────────────────────────┘
                              │
  ┌───────────────────────────v─────────────────────────────────┐
  │  Step 2: Build Timing Graph                                 │
  │     • Enumerate all launch/capture FFs                      │
  │     • Calculate arrival times (forward propagation)         │
  │     • Calculate required times (backward propagation)       │
  │     • Compute slack = required - arrival                    │
  └───────────────────────────┬─────────────────────────────────┘
                              │
  ┌───────────────────────────v─────────────────────────────────┐
  │  Step 3: Check Timing Constraints                           │
  │     • Setup checks: slack >= 0                              │
  │     • Hold checks: slack >= 0                               │
  │     • Recovery/removal checks (async reset)                 │
  │     • Clock gating checks                                   │
  │     • Max transition checks                                 │
  └───────────────────────────┬─────────────────────────────────┘
                              │
  ┌───────────────────────────v─────────────────────────────────┐
  │  Step 4: Report and Fix Violations                          │
  │     • Generate timing report                                │
  │     • Identify violation root cause                         │
  │     • Fix: resize cells, add buffers, rewrite RTL           │
  │     • Re-run synthesis and re-check                         │
  └───────────────────────────┬─────────────────────────────────┘
                              │
  ┌───────────────────────────v─────────────────────────────────┐
  │  Step 5: Multi-Corner Signoff                               │
  │     • Run at TT (nominal), FF (best), SS (worst)          │
  │     • Run at aged models (10-year NBTI/PBTI)              │
  │     • Confirm zero violations at all corners               │
  └─────────────────────────────────────────────────────────────┘
```

### 2.2 Operating Conditions

```
Operating Corners for iPACE-CHIP:
═══════════════════════════════════════════════════════════════

┌──────────────────┬───────┬─────────┬────────┬──────────────┐
│ Corner Name      │ Vdd   │ Temp    │ Vth    │ Usage        │
├──────────────────┼───────┼─────────┼────────┼──────────────┤
│ TT_1V5_025C      │ 1.50V │ 25°C    │ Typ    │ Nominal      │
│ TT_1V5_075C      │ 1.50V │ 75°C    │ Typ    │ Body temp    │
│ FF_1V8_025C      │ 1.80V │ 25°C    │ Fast   │ Best case    │
│ FF_1V8_M40C      │ 1.80V │ -40°C   │ Fast   │ Cold start   │
│ SS_0V9_125C      │ 0.90V │ 125°C   │ Slow   │ Worst case   │
│ SS_1V0_125C      │ 1.00V │ 125°C   │ Slow   │ Aging margin │
│ TT_1V5_025C_AGED │ 1.50V │ 25°C    │ Typ+   │ 10-yr aged   │
│ FF_1V8_025C_AGED │ 1.80V │ 25°C    │ Fast+  │ 10-yr aged   │
└──────────────────┴───────┴─────────┴────────┴──────────────┘

  Signoff Criteria:
    • Setup: Zero violations at worst-case (SS_0V9_125C)
    • Hold:  Zero violations at best-case (FF_1V8_M40C)
    • Recovery/Removal: Zero violations at all corners
    • Aged:  Zero violations at aged corners
```

## 3. Timing Analysis Types

### 3.1 Setup Time Analysis

```
Setup Time Check:
═══════════════════════════════════════════════════════════════

  The setup check ensures data arrives before the capturing
  clock edge:

  Clock Period (Tclk):  30,518 ns
  Setup Time (Tsetup):  0.18 ns (for HVT DFF at 1.5V)
  Clock Uncertainty:    0.50 ns
  Clock Latency diff:   0.30 ns

  Required Time:
    Trequired = Tclk - Tsetup - Tuncertainty - Tlatency_diff
              = 30,518 - 0.18 - 0.50 - 0.30
              = 30,517.02 ns

  Arrival Time (typical path):
    Tarrival = Tclk_latency + Tlogic + Trouting
             = 0.50 + 15.0 + 5.0
             = 20.50 ns

  Setup Slack:
    Slack_setup = Trequired - Tarrival
                = 30,517.02 - 20.50
                = +30,496.52 ns  ✓ (massive margin)

  This is expected: a 33 kHz clock has enormous timing margin.
  The real challenge is hold timing and min-delay paths.

  ┌─────────────────────────────────────────────────────────────┐
  │  Timeline (not to scale):                                    │
  │                                                               │
  │  0 ns          20.5 ns      30,517.02 ns    30,518 ns       │
  │  ├──────────────┤              │               │              │
  │  │ Launch Clock │              │ Required      │ Capture Clk │
  │  │ + Data Path  │              │ Setup Edge    │              │
  │  │              │              │               │              │
  │  ◄── Slack = 30,496.52 ns ───────────────────►               │
  │              (1000x margin over typical ASIC!)               │
  └─────────────────────────────────────────────────────────────┘
```

### 3.2 Hold Time Analysis

```
Hold Time Check:
═══════════════════════════════════════════════════════════════

  The hold check ensures data doesn't change too quickly
  after the capturing clock edge:

  Hold Time (Thold):  0.05 ns (for HVT DFF at 1.5V)
  Clock Uncertainty:  0.20 ns (hold)

  Required Time:
    Trequired_hold = Thold + Tuncertainty_hold
                   = 0.05 + 0.20
                   = 0.25 ns

  Data Contamination Delay (fastest path):
    Tcontam = Tcell_contam + Trouting_min
            = 0.05 + 0.01
            = 0.06 ns

  Hold Slack:
    Slack_hold = Tcontam - Trequired_hold
               = 0.06 - 0.25
               = -0.19 ns  !! VIOLATION !!

  Hold violations are more likely because they depend on
  the MINIMUM path delay, not the maximum.

  Fix: Insert buffer delay cells on fast paths
  ┌─────────────────────────────────────────────────────────────┐
  │  Before fix:                                                 │
  │  Launch FF ────────► Capture FF (too fast!)                 │
  │                                                               │
  │  After fix:                                                   │
  │  Launch FF ──►[BUF]──►[BUF]──► Capture FF (delay added)    │
  │                                                               │
  │  Each buffer adds ~0.08 ns delay at 1.5V                    │
  │  Need 3 buffers: 0.06 + 3*0.08 = 0.30 ns > 0.25 ns ✓     │
  └─────────────────────────────────────────────────────────────┘
```

## 4. Timing Reports

### 4.1 Critical Path Analysis

```
STA Timing Report - Worst Setup Path (SS_0V9_125C):
═══════════════════════════════════════════════════════════════

Startpoint: u_sensing_engine/rr_cnt_reg[15]/CK
  (rising edge-triggered flip-flop clocked by clk_core)
Endpoint: u_pacing_engine/rate_cnt_reg[7]/D
  (rising edge-triggered flip-flop clocked by clk_core)

Path Group: clk_core
Path Type: setup

  Pin                                    Delay    Arrival
  ──────────────────────────────────────────────────────
  clock clk_core (rise edge)             0.00      0.00
  clock source latency                   0.50      0.50
  u_icg_sensing/Q (CKLNQD1)             0.45      0.95
  u_sensing_engine/rr_cnt_reg[15]/CK              0.95
  u_sensing_engine/rr_cnt_reg[15]/Q     0.45      1.40
  u_sensing_engine/u_rr_avg/CKLNQD1/Q   0.40      1.80
  u_pacing_engine/u_rate_cmp/AO21D1/Z   0.35      2.15
  u_pacing_engine/u_rate_mux/MUX2D1/Z   0.30      2.45
  u_pacing_engine/rate_cnt_reg[7]/D               2.45

  Data Path Delay: 1.50 ns
  Required Time:   30,517.02 ns
  Slack:           +30,495.52 ns  ✓ PASS

  (Note: Path is simplified for illustration)
```

### 4.2 Clock Gating Check

```
Clock Gating Check (ICG Timing):
═══════════════════════════════════════════════════════════════

  The enable signal of a clock gating cell must be stable
  before the latch closes (on negative clock edge):

  ICG Setup Check:
    Enable arrival: Tlogic_before_ICG = 5.0 ns
    Required: Tclk/2 - Tuncertainty - Tlatch_setup
            = 15,259 - 0.50 - 0.20
            = 15,258.30 ns
    Slack: 15,258.30 - 5.0 = +15,253.30 ns ✓

  ICG Hold Check:
    Enable arrival: Tcontam = 0.05 ns
    Required: Tlatch_hold + Tuncertainty_hold
            = 0.05 + 0.20
            = 0.25 ns
    Slack: 0.05 - 0.25 = -0.20 ns
    Fix: Add buffer on enable path (same as regular hold fix)
```

### 4.3 Recovery/Removal Check

```
Recovery/Removal Check (Async Reset):
═══════════════════════════════════════════════════════════════

  Recovery check: async reset deassert must happen before
  the next active clock edge:

  Reset deassert arrival: Treset_path = 2.0 ns
  Recovery required: Tclk - Trecovery - Tuncertainty
                   = 30,518 - 0.30 - 0.50
                   = 30,517.20 ns
  Slack: 30,517.20 - 2.0 = +30,515.20 ns ✓

  Removal check: async reset must be held long enough
  after the active clock edge:

  Reset hold: Treset_hold = 1.0 ns
  Removal required: Trecovery + Tuncertainty
                  = 0.30 + 0.20
                  = 0.50 ns
  Slack: 1.0 - 0.50 = +0.50 ns ✓
```

## 5. Multi-Corner Analysis

### 5.1 Corner-by-Corner Summary

```
STA Summary Across All Corners:
═══════════════════════════════════════════════════════════════

┌──────────────────┬────────┬────────┬────────┬──────────────┐
│ Corner           │Setup   │Hold    │Recovery│ Notes        │
│                  │Slack   │Slack   │Slack   │              │
├──────────────────┼────────┼────────┼────────┼──────────────┤
│ SS_0V9_125C      │+30,495 │+0.30   │+30,515 │ Worst setup │
│ (worst)          │ ns     │ ns     │ ns     │              │
├──────────────────┼────────┼────────┼────────┼──────────────┤
│ SS_1V0_125C      │+30,496 │+0.32   │+30,516 │ Aging case  │
│                  │ ns     │ ns     │ ns     │              │
├──────────────────┼────────┼────────┼────────┼──────────────┤
│ TT_1V5_025C      │+30,498 │+0.35   │+30,517 │ Nominal     │
│ (typical)        │ ns     │ ns     │ ns     │              │
├──────────────────┼────────┼────────┼────────┼──────────────┤
│ TT_1V5_075C      │+30,497 │+0.33   │+30,516 │ Body temp   │
│                  │ ns     │ ns     │ ns     │              │
├──────────────────┼────────┼────────┼────────┼──────────────┤
│ FF_1V8_025C      │+30,500 │+0.28   │+30,518 │ Best case   │
│ (best)           │ ns     │ ns     │ ns     │              │
├──────────────────┼────────┼────────┼────────┼──────────────┤
│ FF_1V8_M40C      │+30,501 │+0.25   │+30,519 │ Cold start  │
│                  │ ns     │ ns     │ ns     │              │
├──────────────────┼────────┼────────┼────────┼──────────────┤
│ TT_1V5_025C_AGED │+30,495 │+0.30   │+30,515 │ 10-yr aged  │
│                  │ ns     │ ns     │ ns     │              │
├──────────────────┼────────┼────────┼────────┼──────────────┤
│ FF_1V8_025C_AGED │+30,498 │+0.27   │+30,517 │ 10-yr aged  │
│                  │ ns     │ ns     │ ns     │              │
└──────────────────┴────────┴────────┴────────┴──────────────┘

  ALL corners: PASS (zero violations at all analysis points)
  Margin varies: ~30,495 to ~30,501 ns (setup)
```

## 6. Clock Domain Crossing Analysis

### 6.1 CDC Path Enumeration

```
CDC Paths in iPACE-CHIP:
═══════════════════════════════════════════════════════════════

  Clock Domains:
    clk_core:  32.768 kHz (main digital logic)
    clk_tele:  1.048576 MHz (telemetry subsystem)

  CDC Paths (crossing clk_core → clk_tele):
  ┌────┬───────────────────────┬──────────────────┬───────────┐
  │ #  │ Source (clk_core)     │ Dest (clk_tele)  │ Sync Type │
  ├────┼───────────────────────┼──────────────────┼───────────┤
  │  1 │ param_store.data_out  │ tele_tx.data_in  │ 2-FF sync │
  │  2 │ pacing_engine.status  │ tele_rx.status   │ 2-FF sync │
  │  3 │ sensing_engine.rate   │ tele_rx.rate_out │ 2-FF sync │
  │  4 │ watchdog.ok           │ tele_rx.wdog_st  │ 2-FF sync │
  └────┴───────────────────────┴──────────────────┴───────────┘

  CDC Paths (crossing clk_tele → clk_core):
  ┌────┬───────────────────────┬──────────────────┬───────────┐
  │ #  │ Source (clk_tele)     │ Dest (clk_core)  │ Sync Type │
  ├────┼───────────────────────┼──────────────────┼───────────┤
  │  5 │ tele_rx.cmd_data      │ param_store.wr   │ 2-FF sync │
  │  6 │ tele_rx.cmd_valid     │ param_store.wr_en│ 2-FF sync │
  │  7 │ tele_rx.mode_select   │ pwr_mgr.mode     │ 2-FF sync │
  └────┴───────────────────────┴──────────────────┴───────────┘

  Note: ALL CDC paths have designated 2-FF synchronizers
  (inserted by synthesis from cdc_2ff_sync module)
```

## 7. Safety-Critical Path Analysis

```
Safety-Critical Timing Paths:
═══════════════════════════════════════════════════════════════

  Safety-critical paths receive additional timing derating:

  ┌──────────────────────────────┬────────┬────────────────────┐
  │ Path                         │ Derate │ Rationale          │
  ├──────────────────────────────┼────────┼────────────────────┤
  │ Watchdog timeout signal      │ 0.90   │ Must trigger safe   │
  │                              │        │ mode within 1 beat  │
  ├──────────────────────────────┼────────┼────────────────────┤
  │ Output driver enable/disable │ 0.92   │ Prevent runaway     │
  │                              │        │ pacing              │
  ├──────────────────────────────┼────────┼────────────────────┤
  │ Safety FSM state register    │ 0.90   │ Correct state       │
  │                              │        │ transition          │
  ├──────────────────────────────┼────────┼────────────────────┤
  │ ECC error detection          │ 0.95   │ Detect SRAM errors  │
  │                              │        │ promptly            │
  ├──────────────────────────────┼────────┼────────────────────┤
  │ Current sense comparator     │ 0.90   │ Detect overcurrent  │
  │                              │        │ within 1 µs         │
  └──────────────────────────────┴────────┴────────────────────┘

  Even with 10% derating, all paths still have ~30,000 ns
  of slack — safety timing is trivially met at 33 kHz.
```

## 8. Aging Analysis

```
NBTI/PBTI Aging Impact (10-Year Projection):
═══════════════════════════════════════════════════════════════

  NBTI (Negative Bias Temperature Instability):
    • Affects PMOS transistors under negative Vgs stress
    • Increases threshold voltage over time
    • Effect: slower cell delays

  PBTI (Positive Bias Temperature Instability):
    • Affects NMOS transistors under positive Vgs stress
    • Less severe than NBTI in most technologies
    • Effect: slower cell delays

  Aging Derate Calculation (180nm, 10-year):
  ┌──────────────┬──────────┬──────────┬──────────┬───────────┐
  │ Parameter    │ Fresh    │ 5-year   │ 10-year  │ 20-year   │
  ├──────────────┼──────────┼──────────┼──────────┼───────────┤
  │ Vth shift    │ 0 mV     │ +15 mV   │ +25 mV   │ +35 mV   │
  │ Delay factor│ 1.000    │ 1.035    │ 1.055    │ 1.075    │
  │ Leakage      │ 1.000    │ 0.950    │ 0.900    │ 0.850    │
  └──────────────┴──────────┴──────────┴──────────┴───────────┘

  Impact on iPACE-CHIP:
    • Worst-case path delay increases by 5.5% after 10 years
    • At 33 kHz clock: 30,518 ns × 0.055 = 1,678 ns consumed
    • Remaining slack: ~28,800 ns (still massive) ✓
    • Leakage decreases (beneficial for battery life) ✓
    • No design changes needed for aging at this clock speed
```

## 9. Summary

Static Timing Analysis for iPACE-CHIP demonstrates:

1. **Zero timing violations** at all 8 operating corners
2. **~30,000 ns setup slack** — trivial timing closure at 33 kHz
3. **Hold violations fixed** with buffer insertion on fast paths
4. **All CDC paths** properly synchronized with 2-FF chains
5. **Safety-critical paths** pass with 10% additional derating
6. **10-year aging** adds only 5.5% delay — well within margin
7. **Clock gating checks** pass for all ICG cells

The ultra-low clock frequency makes timing the least challenging aspect of iPACE-CHIP
verification. The real design challenges lie in power optimization, safety verification,
and analog/mixed-signal validation.

---

*Previous: [Gate-Level Netlist](../03-Gate-Level-Netlist/gate-level-netlist.md)*
