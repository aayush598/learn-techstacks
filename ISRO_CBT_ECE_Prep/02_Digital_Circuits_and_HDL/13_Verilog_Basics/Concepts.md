# Verilog Basics - Concepts

## What is Verilog
- IEEE 1364 Hardware Description Language
- Syntax C-like (C heritage)
- Two main modeling: module (structural) + behavioral (always)
- Widely used with VHDL in digital design

## Module (like entity+architecture)
```verilog
module and_gate(a, b, y);
  input a, b;
  output y;
  assign y = a & b;
endmodule
```
- Ports, internal wires/regs

## Data Types
```
wire: combinational signal (continuous assignment output)
reg:  holds value (procedural assignment, in always)
integer: 32-bit, real, time
input/output/inout (ports)
```

## Assignments
```
Continuous (assign): combinational, outside always
  assign y = a & b;
Procedural (=): blocking, in always
Procedural (<=): non-blocking, in always (for registers)
```

## Gate-level (structural)
```
and(y, a, b);         // 2-input AND
or, nand, nor, xor, xnor, not
And also UDP
```

## Dataflow (assign)
```
assign y = ~(a & b);   // NAND
assign s = a ^ b;
```

## Behavioral (always block)
```verilog
always @(a or b)       // combinational
  y = a & b;

always @(posedge clk)  // sequential register
  q <= d;
```

## Operators
```
Bitwise: & | ^ ~
Logical: && || !
Reduction: &a (AND all bits), |a, ^a (parity)
Shift: << >> (>> for unsigned, >>> signed)
Arithmetic: + - * /
Relational: == != < > <= >=
Concatenation: {a,b}
```

## reg vs wire
```
wire: only with assign / structural (no always)
reg: only inside always (stores state)
Multiple bit: reg [7:0] r; wire [3:0] w;
```

## if/else, case
```verilog
always @(*)      // @(*) = all inputs
  if (sel)
    y = a;
  else
    y = b;

always @(*)
  case (sel)
    2'b00: y = a;
    2'b01: y = b;
    default: y = 0;
  endcase
```

## Numbers
```
2'b10: 2-bit binary 10
8'hFF: hex, 4'd15: decimal
Width 'base 'value
```

## Define / Parameters
```verilog
parameter W = 8;    // local param
`define WIDTH 8     // macro
```

## Synthesis principles
- Combinational (always @(*), assign)
- Sequential (always @(posedge clk))
- Avoid latches (incomplete if/else without all assignments)

---

## ISRO Key Points
- module/endmodule
- wire (continuous) vs reg (procedural)
- assign (combinational), always (sequential/behavioral)
- blocking (=) vs non-blocking (<=)
- posedge clock for registers
- Operators &,|,^,{}
