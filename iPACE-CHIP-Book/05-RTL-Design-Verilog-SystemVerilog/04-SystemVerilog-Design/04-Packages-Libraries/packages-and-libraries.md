# Packages and Libraries in SystemVerilog

## 5.4.4 — Overview

SystemVerilog **packages** provide a namespace for shared types, constants,
functions, and tasks. They prevent name collisions, enable code reuse, and
establish a single source of truth for project-wide definitions. For iPACE-CHIP,
packages centralize register definitions, timing constants, and utility
functions used across all subsystems.

---

## 5.4.5 — Package Declaration

### Basic Package

```systemverilog
package ipace_types;
    // Type definitions
    typedef enum logic [2:0] {
        S_IDLE   = 3'd0,
        S_PACE   = 3'd1,
        S_SENSE  = 3'd2,
        S_REFRACT= 3'd3,
        S_TELEM  = 3'd4,
        S_SLEEP  = 3'd5,
        S_FAULT  = 3'd7
    } fsm_state_t;

    typedef enum logic [1:0] {
        MODE_OFF = 2'b00,
        MODE_VVI = 2'b01,
        MODE_AAI = 2'b10,
        MODE_DDD = 2'b11
    } pacing_mode_t;

    // Struct definitions
    typedef struct packed {
        logic [7:0]  ctrl;
        logic [7:0]  status;
        logic [15:0] timer_count;
        logic [7:0]  pulse_width;
        logic [7:0]  pulse_amp;
        logic [7:0]  sensitivity;
        logic [7:0]  refractory;
    } config_regs_t;

    // Constants
    localparam ADC_WIDTH      = 12;
    localparam TIMER_WIDTH    = 16;
    localparam SPI_CLK_DIV    = 4;
    localparam DEFAULT_THRESH = 12'd2048;

    // Functions
    function automatic logic [7:0] calc_crc8(
        input logic [7:0] data,
        input logic [7:0] crc_in
    );
        logic [7:0] crc;
        int i;
        begin
            crc = crc_in ^ data;
            for (i = 0; i < 8; i++)
                crc = crc[7] ? ((crc << 1) ^ 8'h07) : (crc << 1);
            return crc;
        end
    endfunction

endpackage
```

---

## 5.4.6 — Importing Packages

### Import All

```systemverilog
import ipace_types::*;

// Now all package items are available
fsm_state_t state;
pacing_mode_t mode;
config_regs_t config;
logic [7:0] crc = calc_crc8(data, 8'hFF);
```

### Import Specific Items

```systemverilog
import ipace_types::fsm_state_t;
import ipace_types::MODE_VVI;
import ipace_types::ADC_WIDTH;
import ipace_types::calc_crc8;
```

### Package Scope Resolution

```systemverilog
// Use without import — fully qualified
ipace_types::fsm_state_t state;
ipace_types::pacing_mode_t mode;
logic [7:0] crc = ipace_types::calc_crc8(data, 8'hFF);
```

---

## 5.4.7 — Using Packages in Modules

```systemverilog
import ipace_types::*;

module pacing_controller (
    input  logic          clk,
    input  logic          rst_n,
    input  pacing_mode_t  mode,
    input  logic          timer_expired,
    input  logic          sense_event,
    output logic          pace_out
);

    fsm_state_t state, next_state;

    always_ff @(posedge clk or negedge rst_n) begin
        if (!rst_n)
            state <= S_IDLE;
        else
            state <= next_state;
    end

    always_comb begin
        next_state = state;
        case (state)
            S_IDLE: if (timer_expired) next_state = S_PACE;
            S_PACE: next_state = S_REFRACT;
            S_REFRACT: if (timer_expired) next_state = S_IDLE;
            default: next_state = S_IDLE;
        endcase
    end

    assign pace_out = (state == S_PACE);

endmodule
```

---

## 5.4.8 — Pacemaker Package Hierarchy

### Package: ipace_hw_config

```systemverilog
package ipace_hw_config;
    // Hardware configuration constants
    localparam NUM_ADC_CHANNELS   = 2;
    localparam ADC_RESOLUTION     = 12;
    localparam SYSTEM_CLK_HZ      = 32768;
    localparam TIMER_PRESCALER    = 1;
    localparam SPI_DATA_WIDTH     = 8;
    localparam REG_ADDR_WIDTH     = 8;
    localparam REG_DATA_WIDTH     = 8;

    // Timing constants (in clock cycles)
    localparam REFRACTORY_MIN     = 16'd150;    // 4.57 ms
    localparam REFRACTORY_MAX     = 16'd600;    // 18.3 ms
    localparam PACE_PULSE_MIN     = 16'd5;      // 0.15 ms
    localparam PACE_PULSE_MAX     = 16'd150;    // 4.57 ms
    localparam DEBOUNCE_CYCLES    = 16'd100;    // 3.05 ms

    // Amplitude limits
    localparam AMP_MIN            = 8'd10;
    localparam AMP_MAX            = 8'd250;
    localparam AMP_DEFAULT        = 8'd80;
endpackage
```

### Package: ipace_reg_map

```systemverilog
package ipace_reg_map;
    // Register addresses
    localparam REG_CTRL           = 8'h00;
    localparam REG_STATUS         = 8'h01;
    localparam REG_MODE           = 8'h02;
    localparam REG_SENSITIVITY    = 8'h03;
    localparam REG_PULSE_WIDTH    = 8'h04;
    localparam REG_PULSE_AMP      = 8'h05;
    localparam REG_REFRACTORY     = 8'h06;
    localparam REG_TIMER_LOW      = 8'h07;
    localparam REG_TIMER_HIGH     = 8'h08;
    localparam REG_ADC_A          = 8'h09;
    localparam REG_ADC_V          = 8'h0A;
    localparam REG_BATT_VOLTAGE   = 8'h0B;
    localparam REG_LEAD_IMP       = 8'h0C;
    localparam REG_ALARM          = 8'h0D;
    localparam REG_INT_ENABLE     = 8'h0E;
    localparam REG_INT_STATUS     = 8'h0F;

    // Control register bit fields
    localparam CTRL_PACING_EN     = 0;
    localparam CTRL_SENSING_EN    = 1;
    localparam CTRL_TELEM_EN      = 2;
    localparam CTRL_LOW_POWER     = 3;
    localparam CTRL_TEST_MODE     = 4;
    localparam CTRL_SOFT_RESET    = 7;

    // Status register bit fields
    localparam STATUS_PACING      = 0;
    localparam STATUS_SENSING     = 1;
    localparam STATUS_TELEM       = 2;
    localparam STATUS_LOW_BATT    = 3;
    localparam STATUS_FAULT       = 7;
endpackage
```

### Package: ipace_util

```systemverilog
package ipace_util;
    // Utility functions

    // Absolute value
    function automatic logic [11:0] abs12(
        input logic signed [11:0] x
    );
        return (x < 0) ? -x : x;
    endfunction

    // Clamp to range
    function automatic logic [11:0] clamp12(
        input logic [11:0] value,
        input logic [11:0] min_val,
        input logic [11:0] max_val
    );
        if (value < min_val) return min_val;
        else if (value > max_val) return max_val;
        else return value;
    endfunction

    // Popcount
    function automatic logic [3:0] popcount8(
        input logic [7:0] x
    );
        logic [3:0] count;
        int i;
        begin
            count = 0;
            for (i = 0; i < 8; i++)
                count = count + x[i];
            return count;
        end
    endfunction

    // Min of two values
    function automatic logic [11:0] min12(
        input logic [11:0] a,
        input logic [11:0] b
    );
        return (a < b) ? a : b;
    endfunction

    // Max of two values
    function automatic logic [11:0] max12(
        input logic [11:0] a,
        input logic [11:0] b
    );
        return (a > b) ? a : b;
    endfunction
endpackage
```

---

## 5.4.9 — Package Compilation Order

```
// Compilation order matters!
// File list (compile order):
1. ipace_hw_config.sv      (hardware constants)
2. ipace_reg_map.sv        (register addresses)
3. ipace_util.sv           (utility functions)
4. ipace_types.sv          (types and structs)
5. pacing_timer.sv         (uses ipace_types)
6. pacing_controller.sv    (uses ipace_types, ipace_reg_map)
7. sensing_adc.sv          (uses ipace_types, ipace_util)
8. telemetry_controller.sv (uses ipace_types, ipace_reg_map)
9. power_controller.sv     (uses ipace_types)
10. ipace_digital_top.sv   (instantiates all)
```

### Simulation Compilation

```bash
# VCS
vcs -full64 -sverilog \
    +incdir+./packages \
    ./packages/ipace_hw_config.sv \
    ./packages/ipace_reg_map.sv \
    ./packages/ipace_util.sv \
    ./packages/ipace_types.sv \
    ./rtl/*.sv \
    ./tb/*.sv

# Xcelium
xrun -sv \
    -incdir ./packages \
    ./packages/*.sv \
    ./rtl/*.sv \
    ./tb/*.sv
```

---

## 5.4.10 — Package vs Parameter

| Feature | Package | Parameter |
|---------|---------|-----------|
| Scope | Project-wide | Module-level |
| Content | Types, functions, constants | Configurable values |
| Override | No (fixed at compile) | Yes (at instantiation) |
| Reuse | Across all modules | Per instance |

### When to Use Each

```systemverilog
// PACKAGE — fixed project-wide constant
package ipace_hw_config;
    localparam ADC_WIDTH = 12;  // always 12-bit ADC
endpackage

// PARAMETER — configurable per instance
module pacing_timer #(
    parameter WIDTH = 16  // can be 8, 16, or 32 per instance
)(...);
```

---

## 5.4.11 — Library Files and Includes

### Header File Approach (Legacy)

```systemverilog
// ipace_defs.vh — legacy header
`ifndef IPACE_DEFS_VH
`define IPACE_DEFS_VH

`define ADC_WIDTH 12
`define TIMER_WIDTH 16

`endif

// In module file:
`include "ipace_defs.vh"
module my_module (...);
    wire [`ADC_WIDTH-1:0] data;  // preprocessor expansion
endmodule
```

### Package Approach (Preferred)

```systemverilog
// Modern approach — use packages instead of includes
package ipace_config;
    localparam ADC_WIDTH = 12;
endpackage

import ipace_config::*;
module my_module (...);
    wire [ADC_WIDTH-1:0] data;  // package constant
endmodule
```

---

## 5.4.12 — Best Practices

1. **Use packages** for all shared types and constants
2. **Separate concerns** — different packages for different domains
3. **Document compilation order** — packages must compile before users
4. **Use `import` at module scope** — not file scope
5. **Avoid wildcard imports** in production code — use explicit imports
6. **Use `function automatic`** in packages — reentrant calls
7. **Version control packages** — they define project-wide API
8. **Use `localparam`** in packages — not `parameter` (no override needed)
9. **Consistent naming** — `ipace_xxx` prefix for iPACE packages
10. **Check for name collisions** — packages create their own namespace

---

## 5.4.13 — References

- IEEE Std 1800-2017, Section 26 — Packages
- SystemVerilog for Verification, Chris Spear, Chapter 6
- iPACE-CHIP Coding Standard, Section 4.2 — Package Usage
