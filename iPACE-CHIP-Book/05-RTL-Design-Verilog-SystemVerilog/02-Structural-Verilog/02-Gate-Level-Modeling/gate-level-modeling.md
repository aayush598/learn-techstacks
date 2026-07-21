# Gate-Level Modeling in Verilog

## 5.2.2 — Overview

Gate-level modeling describes hardware using **primitive gates** — AND, OR,
NOT, NAND, NOR, XOR, flip-flops, and buffers. While most iPACE-CHIP RTL is
written at the behavioral level, gate-level models are essential for:

- Post-synthesis netlist verification
- Standard cell library modeling
- Timing-aware gate-level simulation
- Understanding synthesis output

---

## 5.2.3 — Built-in Primitives

### Logic Gates

| Primitive | Function | Example |
|-----------|----------|---------|
| `and` | AND | `and (out, a, b);` |
| `nand` | NAND | `nand (out, a, b);` |
| `or` | OR | `or (out, a, b);` |
| `nor` | NOR | `nor (out, a, b);` |
| `xor` | XOR | `xor (out, a, b);` |
| `xnor` | XNOR | `xnor (out, a, b);` |
| `not` | NOT | `not (out, in);` |

### Buffers

| Primitive | Function |
|-----------|----------|
| `buf` | Buffer (non-inverting) |
| `bufif0` | Tri-state buffer, active-low enable |
| `bufif1` | Tri-state buffer, active-high enable |

### Pull Resistors

| Primitive | Function |
|-----------|----------|
| `pullup` | Pull-up resistor |
| `pulldown` | Pull-down resistor |

---

## 5.2.4 — Gate Instantiation Syntax

```verilog
// One-output gates
gate_type instance_name (output, input1, input2, ...);

// Three-state gates
bufif0 instance_name (data_out, data_in, enable_low);
bufif1 instance_name (data_out, data_in, enable_high);
```

### Multi-Input Gates

```verilog
// Up to 9 inputs for standard gates
and u_and4 (out, a, b, c, d);       // 4-input AND
or  u_or8  (out, a, b, c, d, e, f, g, h);  // 8-input OR

// Fan-out: one gate driving multiple loads
buf u_buf1 (net1, input_signal);
buf u_buf2 (net2, input_signal);
buf u_buf3 (net3, input_signal);
```

---

## 5.2.5 — Truth Tables for All Primitives

### AND / NAND

| A | B | AND | NAND |
|---|---|-----|------|
| 0 | 0 | 0 | 1 |
| 0 | 1 | 0 | 1 |
| 1 | 0 | 0 | 1 |
| 1 | 1 | 1 | 0 |

### OR / NOR

| A | B | OR | NOR |
|---|---|-----|-----|
| 0 | 0 | 0 | 1 |
| 0 | 1 | 1 | 0 |
| 1 | 0 | 1 | 0 |
| 1 | 1 | 1 | 0 |

### XOR / XNOR

| A | B | XOR | XNOR |
|---|---|-----|------|
| 0 | 0 | 0 | 1 |
| 0 | 1 | 1 | 0 |
| 1 | 0 | 1 | 0 |
| 1 | 1 | 0 | 1 |

---

## 5.2.6 — Gate Delays

```verilog
// Single delay
and #1 (out, a, b);  // 1 time unit delay

// Rise/fall/turn-off delays
and #(1, 2, 3) (out, a, b);
// rise=1, fall=2, turn-off=3

// Min:typ:max delay specification
and #(1:2:3, 2:3:4) (out, a, b);
// rise(min:typ:max), fall(min:typ:max)
```

### Delay in Pacemaker Timing

```verilog
// Propagation delays for timing analysis
// (Gate-level simulation with SDF back-annotation)
nand #0.15 (nand_out, a, b);  // 150ps NAND delay
not  #0.08 (not_out, nand_out);  // 80ps NOT delay
```

---

## 5.2.7 — Practical Gate-Level Examples

### 2-to-1 Multiplexer

```verilog
module mux2_gate (
    input  wire a,
    input  wire b,
    input  wire sel,
    output wire y
);
    wire not_sel, and_a, and_b;

    not  u_not  (not_sel, sel);
    and  u_and_a (and_a, a, not_sel);
    and  u_and_b (and_b, b, sel);
    or   u_or   (y, and_a, and_b);

endmodule
```

### 4-to-1 Multiplexer

```verilog
module mux4_gate (
    input  wire [3:0] data_in,
    input  wire [1:0] sel,
    output wire       y
);
    wire [1:0] not_sel;
    wire [3:0] and_out;

    not u_n0 (not_sel[0], sel[0]);
    not u_n1 (not_sel[1], sel[1]);

    and u_a0 (and_out[0], data_in[0], not_sel[1], not_sel[0]);
    and u_a1 (and_out[1], data_in[1], not_sel[1], sel[0]);
    and u_a2 (and_out[2], data_in[2], sel[1], not_sel[0]);
    and u_a3 (and_out[3], data_in[3], sel[1], sel[0]);

    or  u_or (y, and_out[0], and_out[1], and_out[2], and_out[3]);

endmodule
```

### D Flip-Flop with Reset

```verilog
module dff_reset_gate (
    input  wire clk,
    input  wire rst_n,
    input  wire d,
    output wire q,
    output wire q_n
);
    wire d_nand1, d_nand2, clk_nand, set, reset;
    wire clk_n, d_gated;

    not u_clk_inv (clk_n, clk);

    // Gated D latch
    nand u_nd1 (d_nand1, d, clk);
    nand u_nd2 (d_nand2, d_nand1, clk);
    nand u_nd3 (q, d_nand1, q_n, rst_n);
    nand u_nd4 (q_n, d_nand2, q, rst_n);

endmodule
```

### SR Latch with Enable

```verilog
module sr_latch_gate (
    input  wire s,
    input  wire r,
    input  wire en,
    output wire q,
    output wire q_n
);
    wire s_gated, r_gated;
    wire not_s, not_r;

    and u_s (s_gated, s, en);
    and u_r (r_gated, r, en);

    nand u_q   (q,   s_gated, q_n);
    nand u_q_n (q_n, r_gated, q);

endmodule
```

---

## 5.2.8 — Tri-State Buffer Modeling

```verilog
module tristate_buffer (
    input  wire data_in,
    input  wire enable,
    output wire data_out
);
    bufif1 u_buf (data_out, data_in, enable);
endmodule

// 8-bit tri-state bus driver
module tristate_bus_8bit (
    input  wire [7:0] data_in,
    input  wire       enable,
    output wire [7:0] data_out
);
    genvar i;
    generate
        for (i = 0; i < 8; i = i + 1) begin : gen_tristate
            bufif1 u_buf (data_out[i], data_in[i], enable);
        end
    endgenerate
endmodule
```

### Pacemaker Pad-Level Tri-State

```verilog
// Bidirectional SPI data pad
module spi_pad_cell (
    input  wire spi_data_out,
    output wire spi_data_in,
    input  wire output_enable,
    inout  wire pad
);
    bufif1 u_out_buf  (pad, spi_data_out, output_enable);
    buf    u_in_buf   (spi_data_in, pad);
endmodule
```

---

## 5.2.9 — Pull Resistors

```verilog
// Open-drain bus with pull-up
module open_drain_driver (
    input  wire data_out,
    input  wire drive_enable,
    output wire bus_line
);
    pullup u_pullup (bus_line);
    bufif0 u_driver (bus_line, data_out, drive_enable);
    // drive_enable=1: drives bus to data_out
    // drive_enable=0: bus released, pulled high by pullup
endmodule

// Pacemaker: Active-low interrupt line with pull-up
wire irq_line;
pullup u_irq_pullup (irq_line);
bufif0 u_irq_driver (irq_line, 1'b0, interrupt_pending);
```

---

## 5.2.10 — Universal Gate Implementation

Any logic function can be implemented with NAND only or NOR only:

### AND from NAND

```verilog
module and_from_nand (
    input  wire a, b,
    output wire y
);
    wire nand_out;
    nand u1 (nand_out, a, b);
    nand u2 (y, nand_out, nand_out);  // NOT = NAND with tied inputs
endmodule
```

### OR from NAND

```verilog
module or_from_nand (
    input  wire a, b,
    output wire y
);
    wire not_a, not_b;
    nand u1 (not_a, a, a);  // NOT a
    nand u2 (not_b, b, b);  // NOT b
    nand u3 (y, not_a, not_b);  // DeMorgan: A+B = (A'·B')'
endmodule
```

### XOR from NAND

```verilog
module xor_from_nand (
    input  wire a, b,
    output wire y
);
    wire n1, n2, n3;
    nand u1 (n1, a, b);
    nand u2 (n2, a, n1);
    nand u3 (n3, b, n1);
    nand u4 (y, n2, n3);
endmodule
```

---

## 5.2.11 — Half Adder and Full Adder

### Half Adder

```verilog
module half_adder_gate (
    input  wire a, b,
    output wire sum, carry
);
    xor u_sum   (sum, a, b);
    and u_carry (carry, a, b);
endmodule
```

### Full Adder

```verilog
module full_adder_gate (
    input  wire a, b, cin,
    output wire sum, cout
);
    wire sum1, carry1, carry2;

    half_adder_gate u_ha1 (
        .a(a), .b(b), .sum(sum1), .carry(carry1)
    );
    half_adder_gate u_ha2 (
        .a(sum1), .b(cin), .sum(sum), .carry(carry2)
    );

    or u_cout (cout, carry1, carry2);
endmodule
```

### 12-Bit Ripple Carry Adder

```verilog
module adder_12bit_gate (
    input  wire [11:0] a,
    input  wire [11:0] b,
    input  wire        cin,
    output wire [11:0] sum,
    output wire        cout
);
    wire [12:0] carry;

    assign carry[0] = cin;

    genvar i;
    generate
        for (i = 0; i < 12; i = i + 1) begin : gen_adder
            full_adder_gate u_fa (
                .a(a[i]), .b(b[i]), .cin(carry[i]),
                .sum(sum[i]), .cout(carry[i+1])
            );
        end
    endgenerate

    assign cout = carry[12];

endmodule
```

---

## 5.2.12 — Decoder and Encoder

### 3-to-8 Decoder

```verilog
module decoder_3to8_gate (
    input  wire [2:0] sel,
    input  wire       enable,
    output wire [7:0] out
);
    wire [2:0] not_sel;

    not u_n0 (not_sel[0], sel[0]);
    not u_n1 (not_sel[1], sel[1]);
    not u_n2 (not_sel[2], sel[2]);

    and u_y0 (out[0], not_sel[2], not_sel[1], not_sel[0], enable);
    and u_y1 (out[1], not_sel[2], not_sel[1], sel[0],     enable);
    and u_y2 (out[2], not_sel[2], sel[1],     not_sel[0], enable);
    and u_y3 (out[3], not_sel[2], sel[1],     sel[0],     enable);
    and u_y4 (out[4], sel[2],     not_sel[1], not_sel[0], enable);
    and u_y5 (out[5], sel[2],     not_sel[1], sel[0],     enable);
    and u_y6 (out[6], sel[2],     sel[1],     not_sel[0], enable);
    and u_y7 (out[7], sel[2],     sel[1],     sel[0],     enable);

endmodule
```

---

## 5.2.13 — Gate-Level Netlist from Synthesis

After synthesis, the tool produces a gate-level netlist. Here is a simplified
example for a pacing timer:

```verilog
// Post-synthesis gate-level netlist (simplified)
module pacing_timer_netlist (
    input  wire clk,
    input  wire rst_n,
    input  wire enable,
    output wire timer_done
);
    wire [15:0] count;
    wire [15:0] next_count;
    wire enable_gated;
    wire count_eq_max;
    wire n_rst;

    not u_inv_rst (n_rst, rst_n);

    // Enable gating
    and u_en_gate (enable_gated, enable, timer_done_n);

    // Counter register (DFFs)
    genvar i;
    generate
        for (i = 0; i < 16; i = i + 1) begin : gen_ff
            // D flip-flop with async reset
            SDFFARX1 u_ff (
                .D(next_count[i]),
                .CK(clk),
                .RB(rst_n),
                .Q(count[i])
            );
        end
    endgenerate

    // Comparator: count == 16'hFFFF
    wire [15:0] nor_out;
    genvar j;
    generate
        for (j = 0; j < 16; j = j + 1) begin : gen_cmp
            xnor u_xnor (nor_out[j], count[j], 1'b1);
        end
    endgenerate

    wire [3:0] and_reduce;
    and u_a0 (and_reduce[0], nor_out[0],  nor_out[1],  nor_out[2],  nor_out[3]);
    and u_a1 (and_reduce[1], nor_out[4],  nor_out[5],  nor_out[6],  nor_out[7]);
    and u_a2 (and_reduce[2], nor_out[8],  nor_out[9],  nor_out[10], nor_out[11]);
    and u_a3 (and_reduce[3], nor_out[12], nor_out[13], nor_out[14], nor_out[15]);
    and u_eq  (count_eq_max, and_reduce[0], and_reduce[1], and_reduce[2], and_reduce[3]);

endmodule
```

---

## 5.2.14 — Best Practices

1. **Use behavioral RTL for design** — gate-level for verification only
2. **Understand gate-level output** — needed for STA and timing closure
3. **Name gate instances** — `u_and1`, `u_or2`, etc.
4. **Use `generate`** for repetitive gate structures
5. **SDF back-annotation** — essential for accurate gate-level timing simulation
6. **Check for `x` propagation** — gate-level may differ from behavioral
7. **Understand tri-state at pads** — gate-level tri-state for pad cells

---

## 5.2.15 — References

- IEEE Std 1364-2005, Section 7 — Gate and Switch Level Modeling
- Neil Weste, *CMOS VLSI Design*, Chapter 2 — MOS Transistor Circuits
- iPACE-CHIP ASIC Standard Cell Library Documentation
