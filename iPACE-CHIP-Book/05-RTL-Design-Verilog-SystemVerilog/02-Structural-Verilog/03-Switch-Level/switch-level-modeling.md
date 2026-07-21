# Switch-Level Modeling in Verilog

## 5.2.3 — Overview

Switch-level modeling describes digital circuits at the **transistor switch**
level using MOSFET primitives. While iPACE-CHIP RTL is primarily behavioral
and gate-level, understanding switch-level modeling is essential for:

- CMOS standard cell library characterization
- Pass-transistor logic design
- Pre-silicon analog/mixed-signal interface verification
- Understanding FPGA lookup-table (LUT) internals

---

## 5.2.4 — MOSFET Primitives

### nMOS Transistor

```verilog
nmos instance_name (drain, source, gate);
```

- Conducts when `gate = 1`
- Passes strong `0`, degraded `1` (threshold voltage drop)
- Used for pull-down networks

### pMOS Transistor

```verilog
pmos instance_name (drain, source, gate);
```

- Conducts when `gate = 0`
- Passes strong `1`, degraded `0`
- Used for pull-up networks

### cMOS (Complementary MOS)

```verilog
cmos instance_name (drain, source, gate_n, gate_p);
```

- Bidirectional switch
- Equivalent to nMOS + pMOS in parallel

### rcMOS (Resistive cMOS)

```verilog
rcmos instance_name (drain, source, gate_n, gate_p);
```

- High-impedance version of cMOS
- Models weak driving strength

---

## 5.2.5 — Signal Strength Model

Verilog uses a strength system for switch-level signals:

### Strength Levels

| Level | Name | Value |
|-------|------|-------|
| 7 | supply | Driven by power supply |
| 6 | strong | Normal gate drive |
| 5 | pull | Pull-up/pull-down |
| 4 | large | Large capacitor |
| 3 | medium | Medium capacitor |
| 2 | small | Small capacitor |
| 1 | highz | High impedance |

### Signal Resolution

```verilog
// Multiple drivers resolve by strength
supply1 VDD;  // VDD = strong 1
supply0 VSS;  // VSS = strong 0

// A node driven by both VDD and VSS = contention (x)
wire conflict;
supply1 vdd_node;
supply0 vss_node;
// vdd_node = 1 (supply), vss_node = 0 (supply)
// If both drive same net → 'x' (contention)
```

---

## 5.2.6 — CMOS Inverter

```verilog
module cmos_inverter (
    input  wire a,
    output wire y
);
    supply1 VDD;
    supply0 VSS;

    pmos u_pmos (y, VDD, a);  // PMOS: conducts when a=0, pulls y to VDD
    nmos u_nmos (y, VSS, a);  // NMOS: conducts when a=1, pulls y to VSS

endmodule
```

---

## 5.2.7 — CMOS NAND Gate

```verilog
module cmos_nand2 (
    input  wire a,
    input  wire b,
    output wire y
);
    supply1 VDD;
    supply0 VSS;
    wire ab;

    // Pull-up network: two pMOS in parallel
    pmos u_p1 (y, VDD, a);
    pmos u_p2 (y, VDD, b);

    // Pull-down network: two nMOS in series
    nmos u_n1 (ab, VSS, a);
    nmos u_n2 (y,  ab,  b);

endmodule
```

### Truth Table Verification

| A | B | PMOS(AB) | PMOS(B) | NMOS(A) | NMOS(B) | Y |
|---|---|----------|---------|---------|---------|---|
| 0 | 0 | ON→VDD | ON→VDD | OFF | OFF | 1 |
| 0 | 1 | ON→VDD | OFF | OFF | ON | 1 |
| 1 | 0 | OFF | ON→VDD | ON→GND | OFF | 1 |
| 1 | 1 | OFF | OFF | ON | ON→GND | 0 |

---

## 5.2.8 — CMOS NOR Gate

```verilog
module cmos_nor2 (
    input  wire a,
    input  wire b,
    output wire y
);
    supply1 VDD;
    supply0 VSS;
    wire ab;

    // Pull-up network: two pMOS in series
    pmos u_p1 (ab, VDD, a);
    pmos u_p2 (y,  ab,  b);

    // Pull-down network: two nMOS in parallel
    nmos u_n1 (y, VSS, a);
    nmos u_n2 (y, VSS, b);

endmodule
```

---

## 5.2.9 — Transmission Gate

```verilog
module transmission_gate (
    input  wire data_in,
    input  wire enable,
    input  wire enable_n,
    output wire data_out
);
    nmos u_nmos (data_out, data_in, enable);
    pmos u_pmos (data_out, data_in, enable_n);
    // Both transistors conduct simultaneously
    // Passes strong 0 and strong 1
endmodule
```

### Pacemaker: Analog MUX for ADC Input Selection

```verilog
module adc_input_mux_4to1 (
    input  wire [3:0] analog_in,
    input  wire [1:0] sel,
    output wire       analog_out,
    input  wire       enable
);
    wire [3:0] sel_decoded;
    wire [3:0] sel_n;

    // Decode select
    not u_n0 (sel_n[0], sel[0]);
    not u_n1 (sel_n[1], sel[1]);

    and u_d0 (sel_decoded[0], sel_n[1], sel_n[0], enable);
    and u_d1 (sel_decoded[1], sel_n[1], sel[0],   enable);
    and u_d2 (sel_decoded[2], sel[1],   sel_n[0], enable);
    and u_d3 (sel_decoded[3], sel[1],   sel[0],   enable);

    // Transmission gates for each channel
    genvar i;
    generate
        for (i = 0; i < 4; i = i + 1) begin : gen_tg
            wire sel_inv;
            not u_inv (sel_inv, sel_decoded[i]);
            nmos u_n  (analog_out, analog_in[i], sel_decoded[i]);
            pmos u_p  (analog_out, analog_in[i], sel_inv);
        end
    endgenerate

endmodule
```

---

## 5.2.10 — Pass-Transistor Logic

### 2-to-1 MUX with Pass Transistors

```verilog
module pt_mux2 (
    input  wire a,
    input  wire b,
    input  wire sel,
    output wire y
);
    wire not_sel;

    not u_not (not_sel, sel);

    // Pass transistor network
    nmos u_n1 (y, a, not_sel);  // pass a when sel=0
    nmos u_n2 (y, b, sel);      // pass b when sel=1

    // Restore signal levels with feedback
    // (In real CMOS, add weak feedback inverter)

endmodule
```

### Dynamic Logic (Precharge-Evaluate)

```verilog
module dynamic_nand2 (
    input  wire clk,
    input  wire a,
    input  wire b,
    output wire y
);
    supply1 VDD;
    supply0 VSS;
    wire eval_node;

    // Precharge PMOS (controlled by clock)
    pmos u_pre (eval_node, VDD, clk);

    // Evaluate NMOS network (series)
    nmos u_e1  (eval_node, VSS, a);
    nmos u_e2  (y, eval_node, b);

    // Output inverter
    supply1 VDD2;
    supply0 VSS2;
    pmos u_out_p (y, VDD2, eval_node);
    nmos u_out_n (y, VSS2, eval_node);

endmodule
```

---

## 5.2.11 — Tri-State Inverter

```verilog
module tri_state_inverter (
    input  wire a,
    input  wire enable,
    output wire y
);
    supply1 VDD;
    supply0 VSS;
    wire a_n;

    // Inverter core
    pmos u_p (y, VDD, a_n);
    nmos u_n (y, VSS, a_n);

    // Enable control (series with output)
    wire enable_n;
    not u_en_inv (enable_n, enable);

    // Controlled pull-up/pull-down
    pmos u_pe (y, VDD, enable);
    nmos u_ne (y, VSS, enable_n);

endmodule
```

---

## 5.2.12 — SRAM Bit Cell

```verilog
module sram_bit_cell (
    input  wire word_line,
    input  wire bit_line,
    input  wire bit_line_n,
    output wire q
);
    supply1 VDD;
    supply0 VSS;

    // Cross-coupled inverters (storage)
    wire q_n;
    wire sr1, sr2;

    // Inverter 1
    pmos u_p1 (sr1, VDD, q_n);
    nmos u_n1 (sr1, VSS, q_n);

    // Inverter 2
    pmos u_p2 (q_n, VDD, sr1);
    nmos u_n2 (q_n, VSS, sr1);

    // Access transistors (word-line gated)
    nmos u_a1 (sr1, bit_line, word_line);
    nmos u_a2 (q_n, bit_line_n, word_line);

    assign q = sr1;

endmodule
```

---

## 5.2.13 — Pacemaker SRAM Wrapper

```verilog
module pacemaker_sram_wrapper #(
    parameter ADDR_WIDTH = 8,
    parameter DATA_WIDTH = 32
)(
    input  wire                    clk,
    input  wire                    rst_n,
    input  wire                    write_en,
    input  wire [ADDR_WIDTH-1:0]  addr,
    input  wire [DATA_WIDTH-1:0]  write_data,
    output wire [DATA_WIDTH-1:0]  read_data
);
    // Behavioral SRAM model (synthesizable inference)
    reg [DATA_WIDTH-1:0] memory [0:(1<<ADDR_WIDTH)-1];

    // Synchronous write
    always @(posedge clk) begin
        if (write_en)
            memory[addr] <= write_data;
    end

    // Asynchronous read (or synchronous depending on architecture)
    assign read_data = memory[addr];

endmodule
```

---

## 5.2.14 — Switch-Level Timing

### Delay Modeling

```verilog
// Switch delay (simplified)
nmos #(0.1) u_n (y, a, sel);  // 100ps nMOS delay
pmos #(0.15) u_p (y, b, sel_n);  // 150ps pMOS delay

// Rise/fall asymmetry
nmos #(0.08, 0.12) u_n (y, a, sel);  // rise=80ps, fall=120ps
```

### Parasitic Capacitance

```verilog
// Model wire capacitance
wire node_a;
wire node_b;
capacitor u_c1 (node_a, gnd, 1e-15);  // 1 fF

// In practice, use extracted parasitics from layout
```

---

## 5.2.15 — Switch-Level Simulation Considerations

| Aspect | Behavioral | Gate-Level | Switch-Level |
|--------|-----------|------------|--------------|
| Abstraction | Algorithm | Logic gates | Transistors |
| Speed | Fastest | Medium | Slowest |
| Accuracy | Functional | Timing+func | Full analog-like |
| Use case | Design | Verification | Cell characterization |
| Signal model | 0/1/x/z | 0/1/x/z + strength | Full strength resolution |

---

## 5.2.16 — Best Practices

1. **Use switch-level sparingly** — only for cell characterization or pass-transistor logic
2. **Model VDD/VSS explicitly** — `supply1` and `supply0`
3. **Include delays** for timing-aware switch-level simulation
4. **Verify with SPICE** — switch-level is approximate; SPICE is golden
5. **Use behavioral models for most design** — switch-level for understanding
6. **Understand strength resolution** — essential for tri-state bus verification
7. **Check for contention** — multiple strong drivers on same net

---

## 5.2.17 — References

- IEEE Std 1364-2005, Section 5 — Switch-Level Modeling
- Neil Weste, *CMOS VLSI Design*, Chapter 2 — MOS Transistors
- Rabaey, *Digital Integrated Circuits*, Chapter 5 — CMOS Logic Gates
- iPACE-CHIP Standard Cell Library Datasheet
