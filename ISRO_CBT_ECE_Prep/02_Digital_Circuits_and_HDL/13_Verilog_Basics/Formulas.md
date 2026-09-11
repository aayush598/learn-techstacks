# Verilog Basics - Syntax Reference

## Module Skeleton
```verilog
module name (port1, port2, ...);
  input  [W-1:0] port1;
  output [M-1:0] port2;
  ...
  // body
endmodule
```

## Combinational: assign
```verilog
assign y = a & b;          // AND
assign y = (a & b) | (c & d);
assign {carry, sum} = a + b;  // concat
```

## Structural gates
```verilog
and g1(y, a, b);     // and(output, in1, in2)
nand, or, nor, xor, xnor, not
```

## Sequential: always @(posedge clk)
```verilog
// D register
reg [7:0] q;
always @(posedge clk)
  q <= d;

// counter
reg [3:0] cnt;
always @(posedge clk or posedge rst)
  if (rst) cnt <= 4'b0;
  else cnt <= cnt + 1;

// with enable
always @(posedge clk)
  if (en) cnt <= cnt + 1;
```

## Blocking vs Non-blocking
```verilog
// Non-blocking (<=) - for sequential/registers (preferred)
always @(posedge clk) begin
  a <= b;
  b <= a;     // both see OLD values -> swap
end

// Blocking (=) - for combinational
always @(*) begin
  y = a & b;
end
```
Rule: use <= for sequential, = for combinational

## if / case
```verilog
always @(*)
  if (en) y = a; else y = b;

always @(*)
  case (sel)
    2'b00: y = a;
    2'b01: y = b;
    default: y = {2{1'b0}};
  endcase
```

## Operators summary
```verilog
a & b   // bitwise AND
a | b   // OR
a ^ b   // XOR
~a      // NOT
&a      // reduction AND (all bits)
^a      // parity (XOR of bits)
{a,b}   // concatenation
a << 1  // shift left
```

## Numbers
```verilog
4'b1010     // binary
8'hFF       // hex
16'd255     // decimal
4'b1010     // z, x allowed
```

## Parameters & Macros
```verilog
parameter WIDTH = 8;        // parameter
reg [WIDTH-1:0] r;
`define BUS 8               // macro
`include "file.v"           // include
```

## Common utilities
```verilog
// testbench clock
initial clk = 0;
always #5 clk = ~clk;        // 10ns period

// stimulus
initial begin
  a = 0; b = 0;
  #10 a = 1; #10 b = 1;
  $finish;
end
```

## Quick Reference
| Construct | Use |
|-----------|-----|
| wire | continuous (assign) |
| reg | procedural (always) |
| assign | combinational |
| always @(posedge clk) | sequential |
| = | blocking (comb) |
| <= | non-blocking (seq) |
| @(*) | all-input sensitivity |
