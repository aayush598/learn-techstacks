# Operators and Expressions in Verilog

## 5.1.2 — Overview

Operators combine signals, constants, and variables into **expressions** that
drive logic. Correct operator usage is critical in pacemaker RTL where an
off-by-one in a comparison or an unintended sign extension can cause a pacing
failure. This chapter catalogs every Verilog operator with iPACE-CHIP–relevant
examples.

---

## 5.2.1 — Operator Precedence

| Precedence | Operator | Description |
|-----------|----------|-------------|
| 1 (highest) | `()` | Parentheses |
| 2 | `!`, `~`, `&`, `~&`, `\|`, `~\|`, `^`, `~^` | Unary reduction |
| 3 | `**` | Power |
| 4 | `*`, `/`, `%` | Multiplication, division, modulus |
| 5 | `+`, `-` | Binary addition, subtraction |
| 6 | `<<`, `>>`, `<<<`, `>>>` | Shifts |
| 7 | `<`, `<=`, `>`, `>=` | Relational |
| 8 | `==`, `!=`, `===`, `!==` | Equality |
| 9 | `&` | Bitwise AND |
| 10 | `^`, `~^` | Bitwise XOR, XNOR |
| 11 | `\|` | Bitwise OR |
| 12 | `&&` | Logical AND |
| 13 | `\|\|` | Logical OR |
| 14 | `?:` | Conditional (ternary) |
| 15 | `{}{{}}` | Concatenation, replication |

> **Always use parentheses** to avoid ambiguity. Precedence mistakes are a
> leading cause of RTL bugs.

---

## 5.2.2 — Bitwise Operators

Bitwise operators apply element-wise to each bit of the operands.

```verilog
// AND — masking bits
wire [7:0] masked_adc;
assign masked_adc = adc_data & 8'hF0;  // keep upper nibble

// OR — setting bits
wire [7:0] flags;
assign flags = status_a | status_b;

// XOR — toggling / parity
wire [7:0] inverted;
assign inverted = data ^ 8'hFF;  // bitwise inversion (same as ~data)

// NAND
wire nand_out;
assign nand_out = ~&(a & b);  // reduction NAND

// NOR
wire nor_out;
assign nor_out = ~|(a | b);  // reduction NOR
```

### Truth Tables

| A | B | A & B | A \| B | A ^ B | ~A |
|---|---|-------|--------|-------|-----|
| 0 | 0 | 0 | 0 | 0 | 1 |
| 0 | 1 | 0 | 1 | 1 | 1 |
| 1 | 0 | 0 | 1 | 1 | 0 |
| 1 | 1 | 1 | 1 | 0 | 0 |

### Pacemaker Example — Bitfield Manipulation

```verilog
// Control register bitfields
reg [7:0] ctrl_reg;

// Bit assignments
localparam CTRL_PACING_EN   = 0;
localparam CTRL_SENSING_EN  = 1;
localparam CTRL_TELEM_EN    = 2;
localparam CTRL_LOW_PWR     = 3;
localparam CTRL_MODE_SHIFT  = 4;
localparam CTRL_MODE_MASK   = 4'hF0;

// Set pacing enable bit
ctrl_reg = ctrl_reg | (1 << CTRL_PACING_EN);

// Clear sensing enable bit
ctrl_reg = ctrl_reg & ~(1 << CTRL_SENSING_EN);

// Read mode field
wire [3:0] mode = (ctrl_reg & CTRL_MODE_MASK) >> CTRL_MODE_SHIFT;

// Check if low-power mode
wire low_power = ctrl_reg[CTRL_LOW_PWR];
```

---

## 5.2.3 — Reduction Operators

Reduction operators collapse a multi-bit vector into a single bit.

```verilog
wire [7:0] data_bus;

wire all_ones  = &data_bus;   // 1 only if all bits are 1
wire any_zero  = ~|data_bus;  // 1 if any bit is 0
wire parity    = ^data_bus;   // even parity
wire odd_parity = ^~data_bus; // odd parity
```

### Application: Watchdog Health Check

```verilog
// Verify all telemetry sub-blocks reported status
wire [7:0] block_status;
wire all_blocks_healthy = &block_status;

// Detect any error flag set
wire any_error = |error_flags;

// Parity check on received data
wire [7:0] rx_byte;
wire rx_parity_ok = (^rx_byte) == rx_parity_bit;
```

### Application: Bus Width Conversion

```verilog
// AND-reduce to check if entire bus is zero
wire [31:0] timer_count;
wire timer_expired = (timer_count == 32'hFFFFFFFF);
wire timer_zero    = ~|timer_count;  // all bits zero
```

---

## 5.2.4 — Arithmetic Operators

```verilog
// Addition
wire [15:0] sum = a + b;

// Subtraction
wire [15:0] diff = a - b;

// Multiplication
wire [31:0] product = a * b;

// Division (non-restoring — synthesizes to combinational divider)
wire [15:0] quotient = dividend / divisor;

// Modulus
wire [7:0] remainder = dividend % divisor;

// Power (for loop bounds — not for synthesis in most cases)
wire [31:0] powers_of_2 = 2 ** index;
```

### Pacemaker: ADC Sample Averaging

```verilog
// Sum of 16 samples for averaging (12-bit ADC)
reg [15:0] sample_sum;
reg [3:0]  sample_idx;

wire [11:0] average = sample_sum >> 4;  // divide by 16 (shift)

always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
        sample_sum <= 16'd0;
        sample_idx <= 4'd0;
    end else if (adc_valid) begin
        if (sample_idx == 4'd15) begin
            sample_sum <= {4'b0, adc_data};  // start new accumulation
            sample_idx <= 4'd0;
        end else begin
            sample_sum <= sample_sum + adc_data;
            sample_idx <= sample_idx + 1'b1;
        end
    end
end
```

### Pacemaker: Timer Prescaler

```verilog
// 32 kHz clock → 1 Hz tick via prescaler
reg [14:0] prescaler;
wire       prescaler_tick = (prescaler == 15'd31999);

always @(posedge clk or negedge rst_n) begin
    if (!rst_n)
        prescaler <= 15'd0;
    else if (prescaler_tick)
        prescaler <= 15'd0;
    else
        prescaler <= prescaler + 1'b1;
end
```

---

## 5.2.5 — Shift Operators

| Operator | Type | Fills with |
|----------|------|------------|
| `<<` | Logical left | 0 on right |
| `>>` | Logical right | 0 on left |
| `<<<` | Arithmetic left | 0 on right (same as `<<`) |
| `>>>` | Arithmetic right | sign bit on left |

```verilog
wire [7:0] shifted_left  = data << 2;   // data * 4
wire [7:0] shifted_right = data >> 3;   // data / 8

wire signed [7:0] signed_val = -8'sd16;
wire signed [7:0] arith_right = signed_val >>> 2;  // -4 (sign-extended)
wire        [7:0] log_right   = signed_val >> 2;   // 60 (zero-extended)
```

### Pacemaker: DAC Output Scaling

```verilog
// Scale 12-bit sensor value to 8-bit DAC output
wire [11:0] sensor_raw;
wire [7:0]  dac_input;

// Logical shift right by 4 (divide by 16)
assign dac_input = sensor_raw[11:4];

// Programmable gain
reg [1:0] gain_shift;  // 0=unity, 1=/2, 2=/4, 3=/8
wire [11:0] scaled_output;
assign scaled_output = sensor_raw >> gain_shift;
```

---

## 5.2.6 — Relational and Equality Operators

### Relational

```verilog
wire gt  = (a > b);
wire lt  = (a < b);
wire gte = (a >= b);
wire lte = (a <= b);
```

### Equality

```verilog
wire eq     = (a == b);   // logical equality
wire neq    = (a != b);   // logical inequality
wire seq    = (a === b);  // case equality (including x/z)
wire sneq   = (a !== b);  // case inequality
```

### Pacemaker: Threshold Comparisons

```verilog
// Heart rate threshold detection
wire [11:0] measured_amplitude;
wire [11:0] atrial_threshold;

// Compare ADC reading to programmable threshold
wire amplitude_exceeds = (measured_amplitude > atrial_threshold);
wire amplitude_below   = (measured_amplitude < minimum_amplitude);

// Detect specific status pattern (including x handling)
wire [3:0] status_nibble;
wire is_init_state = (status_nibble === 4'b01x1);  // matches with x bits
```

### Signed vs Unsigned Comparison Pitfall

```verilog
reg signed [7:0] signed_a = -8'sd5;
reg        [7:0] unsigned_b = 8'd250;

// BUG: mixed signed/unsigned comparison
wire wrong_result = (signed_a < unsigned_b);  // unsigned comparison → false

// FIX: explicit signed comparison
wire correct_result = ($signed(signed_a) < $signed(signed_b));
// or cast both to signed
```

---

## 5.2.7 — Logical Operators

```verilog
wire condition1 = (timer_count > threshold_high);
wire condition2 = (mode == 2'b11);
wire condition3 = !reset_active;

// Combined condition
wire pacing_needed = condition1 && condition2 && condition3;
wire event_trigger = condition1 || condition2;
wire inhibit       = !(condition1 && condition2);
```

### Logical vs Bitwise

```verilog
// Logical: operands → 0 or 1, result → 0 or 1
wire logic_and = (a && b);   // 1 only if both a,b nonzero

// Bitwise: operates on every bit
wire bit_and = a & b;        // bitwise AND of all bits
```

### Pacemaker: Mode-Dependent Enable

```verilog
// Pacing enabled only when:
// 1. Global enable is set
// 2. Not in test mode
// 3. Battery voltage is above minimum
// 4. Timer has expired
wire pacing_enable = global_enable
                  && !test_mode
                  && (battery_voltage > MIN_BAT_VOLTAGE)
                  && timer_expired;
```

---

## 5.2.8 — Conditional (Ternary) Operator

```verilog
wire [7:0] result = condition ? value_if_true : value_if_false;

// Nested ternary (use sparingly)
wire [7:0] priority_mux = (sel == 2'b00) ? input_a :
                           (sel == 2'b01) ? input_b :
                           (sel == 2'b10) ? input_c :
                                            input_d;
```

### Pacemaker: Output Mux

```verilog
// Select pacing pulse width based on mode
wire [15:0] pulse_width = (mode == MODE_VVI) ? vvi_width :
                          (mode == MODE_AAI) ? aai_width :
                          (mode == MODE_DDD) ? ddd_width :
                                               DEFAULT_WIDTH;

// Amplitude scaling for safety
wire [7:0] safe_amplitude = (override) ? max_safe_value :
                            (requested_amplitude > max_safe_value) ?
                                max_safe_value :
                                requested_amplitude;
```

---

## 5.2.9 — Concatenation and Replication

### Concatenation

```verilog
// Join bits together
wire [3:0] high_nibble;
wire [3:0] low_nibble;
wire [7:0] byte = {high_nibble, low_nibble};

// Reverse bit order
wire [7:0] reversed = {data[0], data[1], data[2], data[3],
                       data[4], data[5], data[6], data[7]};
```

### Replication

```verilog
// Replicate a pattern
wire [7:0] all_ones  = {8{1'b1}};            // 8'hFF
wire [15:0] pattern  = {4{4'b1010}};         // 16'hAAAA

// Sign extension via replication
wire [15:0] extended = {{8{data[7]}}, data}; // 8-bit to 16-bit
```

### Pacemaker: Register Pack/Unpack

```verilog
// Pack configuration fields into 32-bit register
wire [1:0] pacing_mode;
wire [3:0] sensitivity;
wire [7:0] pulse_width;
wire [7:0] pulse_amp;
wire [5:0] refractory;
wire [1:0] reserved;

wire [31:0] config_reg = { pacing_mode,   // [31:30]
                           sensitivity,    // [29:26]
                           pulse_width,    // [25:18]
                           pulse_amp,      // [17:10]
                           refractory,     // [9:4]
                           reserved        // [3:0] };

// Unpack on read
wire [1:0] read_mode      = config_reg[31:30];
wire [3:0] read_sens      = config_reg[29:26];
wire [7:0] read_width     = config_reg[25:18];
wire [7:0] read_amp       = config_reg[17:10];
wire [5:0] read_refract   = config_reg[9:4];
```

---

## 5.2.10 — Unary Operators

```verilog
// Unary NOT
wire inverted = !flag;  // logical NOT (0 or 1)
wire bitwise_inv = ~data;  // bitwise NOT

// Unary AND (reduction)
wire all_set = &vector;   // 1 if all bits are 1

// Unary OR (reduction)
wire any_set = |vector;   // 1 if any bit is 1

// Unary XOR (reduction)
wire parity = ^vector;    // even parity
```

### Pacemaker: Interrupt Priority Encoder

```verilog
// 8-bit interrupt request vector
wire [7:0] irq_pending;

// Check if any interrupt is pending
wire any_irq = |irq_pending;

// Priority encode (highest bit = highest priority)
wire [2:0] irq_priority = irq_pending[7] ? 3'd7 :
                           irq_pending[6] ? 3'd6 :
                           irq_pending[5] ? 3'd5 :
                           irq_pending[4] ? 3'd4 :
                           irq_pending[3] ? 3'd3 :
                           irq_pending[2] ? 3'd2 :
                           irq_pending[1] ? 3'd1 :
                                            3'd0;
```

---

## 5.2.11 — Parentheses and Expression Clarity

### Common Mistakes

```verilog
// AMBIGUOUS — relies on precedence
wire result = a & b == c;

// CORRECT — explicit precedence
wire result = a & (b == c);

// AMBIGUOUS — mixed operators
wire [7:0] x = a + b << 2;  // is it (a+b)<<2 or a+(b<<2)?

// CORRECT
wire [7:0] x = (a + b) << 2;
wire [7:0] y = a + (b << 2);
```

### iPACE-CHIP Coding Standard

> **Rule 5.2.1:** All compound expressions shall use explicit parentheses.
> **Rule 5.2.2:** Never rely on operator precedence for correctness.

---

## 5.2.12 — Expression Width Rules

Verilog expressions follow implicit width extension rules:

```verilog
wire [7:0] a = 8'hFF;
wire [7:0] b = 8'h01;

// Width of result is max(width(a), width(b))
wire [7:0] sum = a + b;          // 8-bit result: 8'h00 (overflow!)

// Extend before arithmetic
wire [8:0] safe_sum = {1'b0, a} + {1'b0, b};  // 9-bit: 9'h100
```

### Pacemaker: Safe Arithmetic

```verilog
// 16-bit counter increment — prevent overflow
reg [15:0] timer_count;
wire [16:0] next_count = {1'b0, timer_count} + 17'd1;

always @(posedge clk or negedge rst_n) begin
    if (!rst_n)
        timer_count <= 16'd0;
    else if (!timer_count[15])  // not yet at max
        timer_count <= next_count[15:0];
end
```

---

## 5.2.13 — Bit Select and Part Select

```verilog
wire [31:0] data_word;

// Bit select
wire msb = data_word[31];
wire lsb = data_word[0];

// Part select (constant indices)
wire [7:0] upper_byte = data_word[31:24];
wire [7:0] lower_byte = data_word[7:0];

// Variable part select (indexed)
reg [2:0] byte_sel;
wire [7:0] selected_byte = data_word[byte_sel*8 +: 8];  // ascending
wire [7:0] selected_byte2 = data_word[byte_sel*8 + 7 -: 8]; // descending
```

### Pacemaker: Register File Access

```verilog
reg [31:0] reg_file [0:15];  // 16 x 32-bit register file
reg [3:0]  addr;
reg [1:0]  byte_addr;

// Read with variable select
wire [31:0] reg_data = reg_file[addr];

// Byte-level write
always @(posedge clk) begin
    if (write_en) begin
        case (byte_addr)
            2'b00: reg_file[addr][7:0]   <= write_data[7:0];
            2'b01: reg_file[addr][15:8]  <= write_data[7:0];
            2'b10: reg_file[addr][23:16] <= write_data[7:0];
            2'b11: reg_file[addr][31:24] <= write_data[7:0];
        endcase
    end
end
```

---

## 5.2.14 — Summary of Operator Categories

| Category | Operators | Example |
|----------|-----------|---------|
| Bitwise | `&` `\|` `^` `~` `~&` `~\|` `~^` | `a & b` |
| Reduction | `&` `\|` `^` `~&` `~\|` `~^` | `&vector` |
| Arithmetic | `+` `-` `*` `/` `%` `**` | `a + b` |
| Shift | `<<` `>>` `<<<` `>>>` | `a << 2` |
| Relational | `<` `<=` `>` `>=` | `a > b` |
| Equality | `==` `!=` `===` `!==` | `a == b` |
| Logical | `&&` `\|\|` `!` | `a && b` |
| Conditional | `?:` | `cond ? x : y` |
| Concatenation | `{}` | `{a, b}` |
| Replication | `{{}}` | `{4{1'b1}}` |

---

## 5.2.15 — References

- IEEE Std 1364-2005, Section 4. — Operators
- IEEE Std 1800-2017, Section 11. — Operators and Expressions
- Clifford Cummings, *Synopsys SNUG Paper: Operator Considerations in Verilog*
- iPACE-CHIP RTL Coding Guidelines, Section 3.2
