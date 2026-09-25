# Adders and Subtractors — Circuit Diagrams

## 1. Half Adder

The sum is one-bit parity, `A ⊕ B`, and carry is generated only when both inputs are high.

```circuit
a = elm.SourceI().right().at((-6, 1)).label('A')
b = elm.SourceI().right().at((-6, -1)).label('B')
sum_gate = elm.XorGate().at((-2, 0)).label('S = A ⊕ B')
carry_gate = elm.AndGate().at((-2, -3)).label('C = A · B')
elm.Line().right().at(a)
elm.Line().right().at(b)
elm.Line().right().at(sum_gate)
elm.Line().right().at(a)
elm.Line().right().at(b)
elm.Line().right().at(carry_gate)
```

## 2. Full Adder

The sum is the parity of `A`, `B`, and `Cin`. Carry-out is the majority function, high whenever at least two of those three inputs are high.

```circuit
a = elm.SourceI().right().at((-8, 1)).label('A')
b = elm.SourceI().right().at((-8, -1)).label('B')
cin = elm.SourceI().right().at((-8, -3)).label('Cin')
sum_logic = elm.Block().at((-3, 0)).label('S = A ⊕ B ⊕ Cin')
carry_logic = elm.Block().at((-3, -3)).label('Cout = AB + ACin + BCin')
elm.Line().right().at(a)
elm.Line().right().at(b)
elm.Line().right().at(cin)
elm.Line().right().at(sum_logic)
elm.Line().right().at(a)
elm.Line().right().at(b)
elm.Line().right().at(cin)
elm.Line().right().at(carry_logic)
```

## 3. N-Bit Ripple-Carry Adder

Every full adder receives its carry from the less-significant stage. The structure is regular and area-efficient, but carry-out must pass through every stage, so worst-case delay grows approximately with bit count.

```circuit
a = elm.SourceI().right().at((-11, 2)).label('A[3:0]')
b = elm.SourceI().right().at((-11, 0)).label('B[3:0]')
fa3 = elm.Block().at((-7, 1)).label('FA3')
fa2 = elm.Block().at((-3, 1)).label('FA2')
fa1 = elm.Block().at((1, 1)).label('FA1')
fa0 = elm.Block().at((5, 1)).label('FA0')
result = elm.SourceI().right().at((9, 1)).label('S[3:0]')
carry = elm.SourceI().right().at((9, 4)).label('C4')
elm.Line().right().at(a).to(fa3)
elm.Line().right().at(b).to(fa3)
elm.Line().right().at(fa3).to(fa2)
elm.Line().right().at(fa2).to(fa1)
elm.Line().right().at(fa1).to(fa0)
elm.Line().right().at(fa0)
elm.Line().up().at((7, 1)).to((7, 4))
elm.Line().right().at(result)
elm.Line().right().at(carry)
```

## 4. Carry Generate and Propagate Logic

Each bit position first computes generate, `Gi=AiBi`, and propagate, `Pi=Ai⊕Bi`. A local carry is then `Ci+1=Gi+PiCi`.

```circuit
a = elm.SourceI().right().at((-9, 1)).label('Aᵢ')
b = elm.SourceI().right().at((-9, -1)).label('Bᵢ')
carry_in = elm.SourceI().right().at((-9, -3)).label('Cᵢ')
generate = elm.AndGate().at((-5, 2)).label('Gᵢ = AᵢBᵢ')
propagate = elm.XorGate().at((-5, 0)).label('Pᵢ = Aᵢ ⊕ Bᵢ')
carry_logic = elm.Block().at((-1, 1)).label('Cᵢ₊₁ = Gᵢ + PᵢCᵢ')
sum_logic = elm.Block().at((3, 1)).label('Sᵢ = Pᵢ ⊕ Cᵢ')
elm.Line().right().at(a)
elm.Line().right().at(b)
elm.Line().right().at(generate)
elm.Line().right().at(a)
elm.Line().right().at(b)
elm.Line().right().at(propagate)
elm.Line().right().at(generate)
elm.Line().right().at(propagate)
elm.Line().right().at(carry_in)
elm.Line().right().at(carry_logic)
elm.Line().right().at(propagate)
elm.Line().right().at(carry_logic)
elm.Line().right().at(carry_logic)
elm.Line().right().at(sum_logic)
```

## 5. Four-Bit Carry-Lookahead Network

Expanding each carry equation exposes all generate and propagate terms in parallel. A 4-bit CLA replaces a serial chain with a wider but faster carry network.

```circuit
c0 = elm.SourceI().right().at((-11, 0)).label('C₀')
g0 = elm.SourceI().right().at((-11, 2)).label('G₀')
g1 = elm.SourceI().right().at((-11, 4)).label('G₁')
g2 = elm.SourceI().right().at((-11, 6)).label('G₂')
g3 = elm.SourceI().right().at((-11, 8)).label('G₃')
c1 = elm.Block().at((-5, 1)).label('C₁ = G₀ + P₀C₀')
c2 = elm.Block().at((-5, 3)).label('C₂ = G₁ + P₁G₀ + P₁P₀C₀')
c3 = elm.Block().at((-5, 5)).label('C₃ = G₂ + P₂G₁ + P₂P₁G₀ + P₂P₁P₀C₀')
c4 = elm.Block().at((-5, 8)).label('C₄ = G₃ + P₃G₂ + P₃P₂G₁\n+ P₃P₂P₁G₀ + P₃P₂P₁P₀C₀')
sum = elm.SourceI().right().at((1, 4)).label('Sᵢ = Pᵢ ⊕ Cᵢ')
elm.Line().up().at((-9, 0)).to((-9, 8))
elm.Line().right().at(c0)
elm.Line().right().at(g0)
elm.Line().right().at(g1)
elm.Line().right().at(g2)
elm.Line().right().at(g3)
elm.Line().right().at(c1)
elm.Line().right().at(c2)
elm.Line().right().at(c3)
elm.Line().right().at(c4)
elm.Line().right().at(sum)
```

## 6. Two's-Complement Subtraction

Subtraction reuses an adder. Invert `B`, add one, and interpret the carry-out as the unsigned overflow indication for the current width.

```circuit
a = elm.SourceI().right().at((-9, 1)).label('A')
b = elm.SourceI().right().at((-9, -1)).label('B')
invert = elm.NotGate().at((-5, -1)).label("B'")
adder = elm.Block().at((-1, 0)).label('A + B\' + 1')
difference = elm.SourceI().right().at((4, 0)).label('A − B')
carry_out = elm.SourceI().right().at((4, 3)).label('unsigned no-borrow\nindicator')
elm.Line().right().at(a).to(adder)
elm.Line().right().at(b)
elm.Line().right().at(invert)
elm.Line().right().at(invert)
elm.Line().right().at(adder)
elm.Line().right().at(difference)
elm.Line().up().at((2, 0)).to((2, 3))
elm.Line().right().at(carry_out)
```

## 7. Mode-Controlled Adder–Subtractor

The XOR gates conditionally complement `B`; the same signal is applied to carry-in. This single arithmetic block performs addition or subtraction without duplicating the main adder array.

```circuit
a = elm.SourceI().right().at((-10, 1)).label('A bus')
b = elm.SourceI().right().at((-10, -2)).label('B bus')
mode = elm.SourceI().right().at((-10, 4)).label('S: 0 add, 1 subtract')
xor_b = elm.Block().at((-5, -1)).label('B XOR S')
adder = elm.Block().at((0, 0)).label('shared adder')
cin = elm.Block().at((-5, 4)).label('Cin = S')
output = elm.SourceI().right().at((5, 0)).label('A + B or A − B')
elm.Line().right().at(a).to(adder)
elm.Line().right().at(b)
elm.Line().up().at((-7, -2)).to((-7, 4))
elm.Line().right().at(mode)
elm.Line().right().at(xor_b)
elm.Line().right().at(xor_b).to(adder)
elm.Line().right().at(cin)
elm.Line().right().at(adder)
elm.Line().right().at(output)
```

## 8. Serial and Parallel Arithmetic Paths

A serial adder processes one bit per clock through a shifting register. A parallel adder processes all bits simultaneously but uses a complete adder array and a longer combinational carry path.

```circuit
serial_in = elm.SourceI().right().at((-9, 2)).label('serial bit stream')
serial_reg = elm.Block().at((-4, 2)).label('shift register\none bit per clock')
serial_adder = elm.Block().at((1, 2)).label('single-bit adder\nAᵢ + Bᵢ + C')
serial_out = elm.SourceI().right().at((6, 2)).label('serial sum')
clock = elm.SourceI().right().at((-4, 5)).label('clock')
parallel_a = elm.SourceI().right().at((-9, -2)).label('A[N-1:0]')
parallel_b = elm.SourceI().right().at((-9, -4)).label('B[N-1:0]')
parallel_adder = elm.Block().at((-1, -3)).label('N parallel adders\nCLA or RCA')
parallel_out = elm.SourceI().right().at((6, -3)).label('parallel sum')
elm.Line().right().at(serial_in).to(serial_reg)
elm.Line().right().at(serial_reg).to(serial_adder)
elm.Line().right().at(serial_adder).to(serial_out)
elm.Line().up().at((-2, 2)).to((-2, 5))
elm.Line().right().at(clock)
elm.Line().right().at(parallel_a).to(parallel_adder)
elm.Line().right().at(parallel_b).to(parallel_adder)
elm.Line().right().at(parallel_adder).to(parallel_out)
```
