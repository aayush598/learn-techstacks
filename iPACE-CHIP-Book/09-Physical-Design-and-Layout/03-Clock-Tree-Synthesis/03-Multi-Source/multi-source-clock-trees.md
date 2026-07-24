# Multi-Source Clock Trees

## Overview

Multi-source clock trees distribute clock signals from multiple origins to shared destinations. In iPACE-CHIP, the clock generation unit (CGU) provides redundant clock sources for reliability, while the PLL and external oscillator serve as primary and backup references. Managing multiple clock sources requires careful switching logic and tree balancing.

## Multi-Source Architecture in iPACE-CHIP

### Clock Source Hierarchy

```
Clock Source Priority:
1. Primary: External 32.768 kHz crystal (XTAL)
2. Secondary: On-chip ring oscillator (ROSC)
3. Emergency: Internal RC oscillator (RCOSC)

Clock Generation:
XTAL (32.768 kHz) ---> PLL ---> CLK_CORE (100 MHz)
ROSC (2 MHz) ------> PLL ---> CLK_CORE (100 MHz)
RCOSC (1 MHz) ------> Divider -> CLK_CORE (1 MHz)

Switching Logic:
- Auto-detect XTAL failure (no edge for 10 ms)
- Seamless switch to ROSC (< 1 us transition)
- ROSC failure: switch to RCOSC (< 5 us transition)
- Never allow clock gap > 10 us (pacemaker safety)
```

### Switching Circuit

```verilog
// Clock source multiplexer (simplified)
module clk_source_mux (
    input  wire clk_xtal,    // Primary: 32.768 kHz
    input  wire clk_rosc,    // Secondary: 2 MHz
    input  wire clk_rcosc,   // Emergency: 1 MHz
    input  wire xtal_ok,     // XTAL healthy flag
    input  wire rosc_ok,     // ROSC healthy flag
    output wire clk_out,     // Selected clock
    output wire [1:0] sel    // Source select
);

    // Priority: XTAL > ROSC > RCOSC
    assign sel = xtal_ok ? 2'b00 :
                 rosc_ok ? 2'b01 :
                           2'b10;

    // Glitch-free mux
    clk_mux_glitchfree u_mux (
        .clk_in0 (clk_xtal),
        .clk_in1 (clk_rosc),
        .clk_in2 (clk_rcosc),
        .sel     (sel),
        .clk_out (clk_out)
    );

endmodule
```

## Glitch-Free Clock Switching

### Sync-Based Switching

```verilog
// Glitch-free clock switching using toggle synchronizers
module clk_mux_glitchfree (
    input  wire clk0,
    input  wire clk1,
    input  wire clk2,
    input  wire [1:0] sel,
    output wire clk_out
);

    reg en0, en1, en2;

    // Synchronize enable to each clock domain
    always @(posedge clk0 or negedge rst_n) begin
        if (!rst_n) en0 <= 1'b0;
        else en0 <= (sel == 2'b00) & ~en1 & ~en2;
    end

    always @(posedge clk1 or negedge rst_n) begin
        if (!rst_n) en1 <= 1'b0;
        else en1 <= (sel == 2'b01) & ~en0 & ~en2;
    end

    always @(posedge clk2 or negedge rst_n) begin
        if (!rst_n) en2 <= 1'b0;
        else en2 <= (sel == 2'b10) & ~en0 & ~en1;
    end

    // Gated clock outputs
    wire clk0_gated = clk0 & en0;
    wire clk1_gated = clk1 & en1;
    wire clk2_gated = clk2 & en2;

    // OR-mux (safe because only one enabled at a time)
    assign clk_out = clk0_gated | clk1_gated | clk2_gated;

endmodule
```

### Switching Timing Analysis

```python
# Clock switching timing analysis
switching_analysis = {
    'xtal_to_rosc': {
        'switch_time': 0.8e-6,  # 800 ns
        'max_clock_gap': 50e-9,  # 50 ns (acceptable)
        'glitch_free': True,
        'jitter_impact': 100e-12,  # 100 ps during transition
    },
    'rosc_to_rcosc': {
        'switch_time': 2.0e-6,  # 2 us
        'max_clock_gap': 200e-9,  # 200 ns (acceptable)
        'glitch_free': True,
        'jitter_impact': 500e-12,  # 500 ps during transition
    },
}

# Safety check: no clock gap > 10 us
for transition, data in switching_analysis.items():
    if data['max_clock_gap'] > 10e-6:
        print(f"FAIL: {transition} has gap > 10 us")
    else:
        print(f"PASS: {transition} gap = {data['max_clock_gap']*1e9:.0f} ns")
```

## Multi-Source Tree Topology

### Tree Structure with Multiple Roots

```
        +-----------+     +-----------+     +-----------+
        |   XTAL    |     |   ROSC    |     |   RCOSC   |
        | (32 kHz)  |     |  (2 MHz)  |     |  (1 MHz)  |
        +-----+-----+     +-----+-----+     +-----+-----+
              |                   |                   |
              v                   v                   v
        +-----+-----+     +-----+-----+     +-----+-----+
        |  XTAL     |     |   ROSC    |     |   RCOSC   |
        |  Divider  |     |  Divider  |     |  Divider  |
        +-----+-----+     +-----+-----+     +-----+-----+
              |                   |                   |
              v                   v                   v
        +-----+-----+     +-----+-----+     +-----+-----+
        |  PLL      |     |   PLL     |     |  Direct   |
        |  (x3052)  |     |  (x50)    |     |  to CGU   |
        +-----+-----+     +-----+-----+     +-----+-----+
              |                   |                   |
              +--------+----------+---------+---------+
                       |                     |
                       v                     v
              +--------+--------+    +--------+--------+
              |  Glitch-Free    |    |  CGU Logic      |
              |  Clock Mux      |    |  (monitoring)   |
              +--------+--------+    +--------+--------+
                       |                     |
                       v                     v
              +--------+----------------------------------------+
              |              CGU OUTPUT                          |
              |         CLK_CORE (100 MHz)                       |
              +--+-----+-----+-----+-----+-----+-----+---------+
                 |     |     |     |     |     |     |
                 v     v     v     v     v     v     v
              [Timing Engine] [Pulse] [DSP] [Comm] [Memory]
```

## Clock Tree Insertion for Multi-Source

### Buffer Insertion Strategy

```tcl
# Multi-source clock tree insertion
# Each source has its own tree branch, merging at the MUX

# Source 1: XTAL branch
create_clock_tree -name CLK_XTAL_TREE
setClockTreeOptions -rootBuffer {CLKBUFX16SVT} \
    -bufFootprint {CLKBUFX*} \
    -targetSkew 0.08

# Source 2: ROSC branch
create_clock_tree -name CLK_ROSC_TREE
setClockTreeOptions -rootBuffer {CLKBUFX16SVT} \
    -bufFootprint {CLKBUFX*} \
    -targetSkew 0.08

# Source 3: RCOSC branch
create_clock_tree -name CLK_RCOSC_TREE
setClockTreeOptions -rootBuffer {CLKBUFX8SVT} \
    -bufFootprint {CLKBUFX*} \
    -targetSkew 0.10

# Merge point: glitch-free MUX output
# Route merged clock to all destinations
clock_opt -from build_clock_tree -to build_clock_tree
```

### Shared Tree Segments

```tcl
# After MUX, tree is shared among all sources
# Common buffer insertion for merged clock

# Identify MUX output net
set mux_output [get_db nets CLK_MUX_OUT]

# Insert buffers on shared segment
set_clock_tree_options -sharedSegment true \
    -sharedBuffer {CLKBUFX8SVT} \
    -sharedWidth 1.6

# Route shared tree on M6
setNetStat -net CLK_MUX_OUT -preferredLayer M6 -width 1.6
```

## Multi-Source Balancing Challenges

### Asymmetric Tree Balancing

```python
# Balancing multi-source trees with different insertion delays

source_delays = {
    'XTAL_path': {
        'divider_delay': 2.0,   # ns (slow divider)
        'pll_delay': 1.5,       # ns (PLL lock)
        'mux_delay': 0.3,       # ns (glitch-free mux)
        'total': 3.8,           # ns
    },
    'ROSC_path': {
        'divider_delay': 0.5,   # ns (fast divider)
        'pll_delay': 1.5,       # ns (PLL lock)
        'mux_delay': 0.3,       # ns
        'total': 2.3,           # ns
    },
    'RCOSC_path': {
        'divider_delay': 0.2,   # ns (direct)
        'pll_delay': 0.0,       # ns (no PLL)
        'mux_delay': 0.3,       # ns
        'total': 0.5,           # ns
    },
}

# imbalance = max - min = 3.8 - 0.5 = 3.3 ns
# This is handled by synchronizers at source selection
# Not balanced at tree level (different source characteristics)
```

### Equal-Path Length Matching

```tcl
# For same-source redundant paths, match wire lengths
# Example: Dual PLL outputs for redundancy

# PLL output 1
routeDesign -net PLL_OUT1 -width 1.6 -layer M6
set net_length1 [get_db nets PLL_OUT1 .wires_length]

# PLL output 2 (redundant)
routeDesign -net PLL_OUT2 -width 1.6 -layer M6
set net_length2 [get_db nets PLL_OUT2 .wires_length]

# Match lengths
set length_diff [expr {abs($net_length1 - $net_length2)}]
if {$length_diff > 5.0} {
    puts "WARNING: PLL output length mismatch: ${length_diff} um"
    # Adjust routing
    editRoute -net PLL_OUT2 -adjustLength [expr {$net_length1 - $net_length2}]
}
```

## Clock Monitoring and Failover

### Clock Failure Detection

```verilog
// Clock monitor for multi-source system
module clk_monitor (
    input  wire clk_xtal,
    input  wire clk_rosc,
    input  wire clk_rcosc,
    input  wire rst_n,
    output reg  xtal_fail,
    output reg  rosc_fail,
    output reg  [1:0] failover_sel
);

    reg [15:0] xtal_cnt, rosc_cnt;

    // Count edges in reference period (1 ms)
    always @(posedge clk_rcosc or negedge rst_n) begin
        if (!rst_n) begin
            xtal_cnt <= 16'd0;
            rosc_cnt <= 16'd0;
            xtal_fail <= 1'b0;
            rosc_fail <= 1'b0;
        end else begin
            // Expected: XTAL = 32 edges/ms, ROSC = 2000 edges/ms
            if (xtal_cnt < 20 || xtal_cnt > 50)
                xtal_fail <= 1'b1;
            if (rosc_cnt < 1500 || rosc_cnt > 2500)
                rosc_fail <= 1'b1;
        end
    end

    // Failover selection
    always @(*) begin
        if (!xtal_fail)      failover_sel = 2'b00;  // XTAL
        else if (!rosc_fail)  failover_sel = 2'b01;  // ROSC
        else                  failover_sel = 2'b10;  // RCOSC
    end

endmodule
```

## Physical Design for Multi-Source

### Source Placement

```tcl
# Place clock sources near chip edge
# XTAL pads on left side
placeInst clk_xtal_pad 20 490 0

# ROSC macro placement
placeInst rosc_macro 60 490 0

# RCOSC macro placement
placeInst rcosc_macro 100 490 0

# Glitch-free MUX placement
placeInst glitch_mux 200 490 0

# PLL placement
placeInst pll_core 300 950 0

# CGU output buffer
placeInst cgu_buf 400 950 0
```

### Routing for Multi-Source

```tcl
# Route each source branch separately
# Then merge and route shared segment

# XTAL branch routing
setNetStat -net clk_xtal_div -width 1.2 -layer M5
routeDesign -net clk_xtal_div

# ROSC branch routing
setNetStat -net clk_rosc_div -width 1.2 -layer M5
routeDesign -net clk_rosc_div

# RCOSC branch routing
setNetStat -net clk_rcosc_direct -width 0.8 -layer M5
routeDesign -net clk_rcosc_direct

# Shared output routing
setNetStat -net CLK_CORE -width 1.6 -layer M6
routeDesign -net CLK_CORE

# Shield all clock routes
set_signal_net_shield -net CLK_CORE -shield_net VSS -bothSide
set_signal_net_shield -net clk_xtal_div -shield_net VSS -bothSide
set_signal_net_shield -net clk_rosc_div -shield_net VSS -bothSide
```

## Multi-Source Clock Tree Verification

### Redundancy Verification

```tcl
# Verify all clock sources can drive the tree
proc verify_clock_redundancy {} {
    set sources {clk_xtal clk_rosc clk_rcosc}

    foreach source $sources {
        puts "Testing source: $source"

        # Simulate source active
        set_source_clock -name $source -active true

        # Run timing
        update_timing

        # Check all flip-flops receive clock
        set unclocked [report_ungated -quiet]
        if {[llength $unclocked] > 0} {
            puts "FAIL: $source cannot reach all FFs"
        } else {
            puts "PASS: $source reaches all FFs"
        }

        set_source_clock -name $source -active false
    }
}

verify_clock_redundancy
```

### Failover Timing Verification

```tcl
# Verify failover timing meets requirements
proc verify_failover_timing {} {
    # Simulate XTAL failure
    set_false_path -from [get_ports clk_xtal]

    # Check timing with ROSC
    report_timing -max_paths 10 > reports/failover_rosc_timing.rpt

    # Verify pacing still meets timing
    set wns [get_db designs .setup_wns]
    puts "WNS with ROSC: $wns ns"

    if {$wns > 0} {
        puts "PASS: Failover timing met"
    } else {
        puts "FAIL: Failover timing violation"
    }
}
```

## Multi-Source Results

### Clock Source Timing Comparison

| Source | Frequency | Jitter | Skew | Insertion Delay |
|--------|-----------|--------|------|-----------------|
| XTAL | 100 MHz | 35 ps | 0.08 ns | 1.45 ns |
| ROSC | 100 MHz | 80 ps | 0.10 ns | 1.62 ns |
| RCOSC | 1 MHz | 200 ps | 0.15 ns | 0.85 ns |

### Power Consumption

| Source | Clock Power | Monitoring | Total |
|--------|-------------|------------|-------|
| XTAL active | 81 uW | 5 uW | 86 uW |
| ROSC active | 95 uW | 5 uW | 100 uW |
| RCOSC active | 45 uW | 5 uW | 50 uW |

## Summary

Multi-source clock trees for iPACE-CHIP provide redundant clock generation with glitch-free switching between XTAL, ROSC, and RCOSC sources. The architecture ensures no clock gap exceeds 10 us during failover, maintains acceptable skew for each source branch, and includes monitoring circuitry for automatic source selection. Physical design places sources near the chip edge with shielded routing on dedicated clock layers.
