# Combinational Circuits — Circuit Diagrams

## 1. Half Adder

The XOR gate produces the sum bit, while the AND gate produces carry. A half adder has no carry input and therefore cannot directly extend across multiple bit positions.

```circuit
a = elm.SourceI().right().at((-6, 1)).label('A')
b = elm.SourceI().right().at((-6, -1)).label('B')
sum_gate = elm.XorGate().at((-2, 0)).label('Sum = A ⊕ B')
carry_gate = elm.AndGate().at((-2, -3)).label('Carry = A · B')
elm.Line().right().at(a)
elm.Line().right().at(b)
elm.Line().right().at(sum_gate)
elm.Line().right().at(a)
elm.Line().right().at(b)
elm.Line().right().at(carry_gate)
```

## 2. Full Adder from Two Half Adders

The first half adder sums `A` and `B`; the second adds its sum with `Cin`. An OR gate combines the two carry outputs.

```circuit
a = elm.SourceI().right().at((-9, 1)).label('A')
b = elm.SourceI().right().at((-9, -1)).label('B')
cin = elm.SourceI().right().at((-9, -4)).label('Cin')
ha1 = elm.Block().at((-5, 0)).label('HA1\nS₁ = A ⊕ B\nC₁ = A · B')
ha2 = elm.Block().at((-1, 0)).label('HA2\nS = S₁ ⊕ Cin\nC₂ = S₁ · Cin')
carry_or = elm.OrGate().at((3, 0)).label('Cout = C₁ + C₂')
sum = elm.SourceI().right().at((7, -2)).label('Sum')
cout = elm.SourceI().right().at((7, 2)).label('Cout')
elm.Line().right().at(a).to(ha1)
elm.Line().right().at(b).to(ha1)
elm.Line().right().at(ha1)
elm.Line().right().at(cin).to(ha2)
elm.Line().right().at(ha2)
elm.Line().right().at(carry_or)
elm.Line().right().at(ha2)
elm.Line().down().at((5, 0)).to((5, -2))
elm.Line().right().at(sum)
elm.Line().up().at((5, 0)).to((5, 2))
elm.Line().right().at(cout)
```

## 3. Half and Full Subtractors

The difference is a parity function of the three bits. Full-subtractor borrow is high when at least one of `B` and `Bin` is high while `A` is low.

```circuit
a = elm.SourceI().right().at((-8, 2)).label('A')
b = elm.SourceI().right().at((-8, 0)).label('B')
half_xor = elm.XorGate().at((-4, 1)).label('Half difference')
half_borrow = elm.AndGate().at((-4, -2)).label("Half borrow\nA' · B")
bin = elm.SourceI().right().at((-8, -5)).label('Bin')
full_logic = elm.Block().at((-2, -5)).label("full difference\nA ⊕ B ⊕ Bin\nborrow: A'B + A'Bin + BBin")
elm.Line().right().at(a)
elm.Line().right().at(b)
elm.Line().right().at(half_xor)
elm.Line().right().at(a)
elm.Line().right().at(b)
elm.Line().right().at(half_borrow)
elm.Line().right().at(bin)
elm.Line().right().at(full_logic)
```

## 4. Unified Adder–Subtractor

Mode `M=0` passes `B` and sets carry-in to zero for addition. Mode `M=1` complements every `B` bit and sets carry-in to one, implementing `A + B' + 1 = A − B`.

```circuit
a = elm.SourceI().right().at((-9, 0)).label('A bus')
b = elm.SourceI().right().at((-9, -3)).label('B bus')
mode = elm.SourceI().right().at((-9, 3)).label('M: 0 add, 1 subtract')
conditional_invert = elm.Mux().at((-4, -2)).label('B XOR M')
adder = elm.Block().at((1, 0)).label('n-bit adder')
cin = elm.Block().at((-4, 3)).label('Cin = M')
result = elm.SourceI().right().at((6, 0)).label('sum or difference')
cout = elm.SourceI().right().at((6, 3)).label('carry-out')
elm.Line().right().at(a).to(adder)
elm.Line().right().at(b)
elm.Line().up().at((-6, -3)).to((-6, 3))
elm.Line().right().at(mode)
elm.Line().right().at(conditional_invert)
elm.Line().up().at((-2, -2)).to((-2, 0))
elm.Line().right().at(conditional_invert)
elm.Line().right().at(cin)
elm.Line().right().at(adder)
elm.Line().right().at(result)
elm.Line().up().at((4, 0)).to((4, 3))
elm.Line().right().at(cout)
```

## 5. Magnitude Comparator and Priority Cascade

A one-bit comparator produces greater, equal, and less. A multi-bit comparator examines the MSB first; lower bits matter only when every higher bit pair is equal.

```circuit
a = elm.SourceI().right().at((-7, 1)).label('A')
b = elm.SourceI().right().at((-7, -1)).label('B')
greater = elm.AndGate().at((-3, 2)).label("A>B\nA · B'")
equal = elm.XnorGate().at((-3, 0)).label('A=B\nA XNOR B')
less = elm.AndGate().at((-3, -2)).label("A<B\nA' · B")
cascaded = elm.Block().at((2, 0)).label('4-bit MSB-first cascade\n7485-style outputs')
elm.Line().right().at(a)
elm.Line().right().at(b)
elm.Line().right().at(greater)
elm.Line().right().at(a)
elm.Line().right().at(b)
elm.Line().right().at(equal)
elm.Line().right().at(a)
elm.Line().right().at(b)
elm.Line().right().at(less)
elm.Line().right().at(greater)
elm.Line().right().at(equal)
elm.Line().right().at(less)
elm.Line().right().at(cascaded)
```

## 6. Parity Generator and Error Checker

The transmitter appends the XOR of all data bits. The receiver recomputes the parity of the complete word; a nonzero syndrome detects a parity violation, though even numbers of bit errors can remain undetected.

```circuit
word = elm.SourceI().right().at((-8, 0)).label('D₃D₂D₁D₀P')
x1 = elm.XorGate().at((-4, 0)).label('D₃ ⊕ D₂')
x2 = elm.XorGate().at((-1, 0)).label('D₁ ⊕ D₀')
x3 = elm.XorGate().at((2, 0)).label('data parity')
check = elm.XorGate().at((5, 0)).label('received syndrome')
error = elm.SourceI().right().at((8, 0)).label('even: 0 means valid')
elm.Line().right().at(word)
elm.Line().right().at(x1)
elm.Line().right().at(x2)
elm.Line().right().at(x3)
elm.Line().right().at(check)
elm.Line().right().at(error)
```

## 7. Binary–Gray and BCD–Excess-3 Converters

Parallel Gray conversion compares adjacent binary bits. A valid 8421 BCD digit maps to Excess-3 by adding `0011`; inputs 1010 through 1111 are invalid or don't-care for the ten-digit mapping.

```circuit
binary = elm.SourceI().right().at((-8, 1)).label('binary B[3:0]')
gray_encoder = elm.Block().at((-3, 1)).label('binary → Gray\nG = B ⊕ (B >> 1)')
bcd = elm.SourceI().right().at((-8, -2)).label('8421 BCD digit')
excess_encoder = elm.Block().at((-3, -2)).label('BCD → Excess-3\nE = B + 0011')
outputs = elm.Demux().at((3, 0)).label('converted code buses')
elm.Line().right().at(binary)
elm.Line().right().at(gray_encoder)
elm.Line().right().at(bcd)
elm.Line().right().at(excess_encoder)
elm.Line().right().at(gray_encoder)
elm.Line().right().at(excess_encoder)
elm.Line().right().at(outputs)
```

## 8. Four-to-Two Priority Encoder

If several request lines are active, `D3` has highest priority. The valid flag identifies whether any request exists, while the two output bits encode the highest active index.

```circuit
i0 = elm.SourceI().right().at((-9, -3)).label('I₀')
i1 = elm.SourceI().right().at((-9, -1)).label('I₁')
i2 = elm.SourceI().right().at((-9, 1)).label('I₂')
i3 = elm.SourceI().right().at((-9, 3)).label('I₃\nhighest priority')
encoder = elm.Block().at((-3, 0)).label('priority encoder\nD3 > D2 > D1 > D0')
y1 = elm.Block().at((1, 1)).label('Y₁ = D3 + D2')
y0 = elm.Block().at((1, -1)).label("Y₀ = D3 + D1D2'")
valid = elm.Block().at((1, -3)).label('V = I0 + I1 + I2 + I3')
elm.Line().right().at(i0).to(encoder)
elm.Line().right().at(i1).to(encoder)
elm.Line().right().at(i2).to(encoder)
elm.Line().right().at(i3).to(encoder)
elm.Line().right().at(encoder)
elm.Line().up().at((-1, 0)).to((-1, 1))
elm.Line().right().at(y1)
elm.Line().down().at((-1, 0)).to((-1, -1))
elm.Line().right().at(y0)
elm.Line().down().at((-1, -1)).to((-1, -3))
elm.Line().right().at(valid)
```

## 9. BCD-to-Seven-Segment Decoder

The four-bit BCD input activates the required segment lines. The segment arrangement is shown as a display interface; active-high or active-low polarity depends on the decoder and display type.

```circuit
bcd = elm.SourceI().right().at((-10, 0)).label('BCD[3:0]')
decoder = elm.Block().at((-5, 0)).label('BCD → seven-segment\ndecoder')
segment_a = elm.Block().at((0, 3)).label('a')
segment_b = elm.Block().at((3, 2)).label('b')
segment_c = elm.Block().at((3, -2)).label('c')
segment_d = elm.Block().at((0, -3)).label('d')
segment_e = elm.Block().at((-3, -2)).label('e')
segment_f = elm.Block().at((-3, 2)).label('f')
segment_g = elm.Block().at((0, 0)).label('g')
display = elm.Block().at((6, 0)).label('seven-segment\ndisplay')
elm.Line().right().at(bcd).to(decoder)
elm.Line().right().at(decoder)
elm.Line().up().at((-2, 0)).to((-2, 3))
elm.Line().right().at(segment_a)
elm.Line().right().at(segment_b)
elm.Line().right().at(segment_c)
elm.Line().right().at(segment_d)
elm.Line().right().at(segment_e)
elm.Line().right().at(segment_f)
elm.Line().right().at(segment_g)
elm.Line().right().at(display)
```

## 10. Two-by-Two Binary Multiplier

Four AND gates form partial products. The two lowest columns use an XOR-and-carry adder, and the high column adds `A₁B₁` to the carry from that adder.

```circuit
a1 = elm.SourceI().right().at((-10, 2)).label('A₁')
a0 = elm.SourceI().right().at((-10, 0)).label('A₀')
b1 = elm.SourceI().right().at((-10, -2)).label('B₁')
b0 = elm.SourceI().right().at((-10, -4)).label('B₀')
and00 = elm.AndGate().at((-6, -4)).label('A₀B₀ = P₀')
and01 = elm.AndGate().at((-6, -1)).label('A₀B₁')
and10 = elm.AndGate().at((-6, 1)).label('A₁B₀')
and11 = elm.AndGate().at((-6, 3)).label('A₁B₁')
low_add = elm.Block().at((-1, 0)).label('LSB adder\nP₁ = A₀B₁ ⊕ A₁B₀\nC = A₀B₁A₁B₀')
high_add = elm.Block().at((4, 1)).label('MSB adder\nP₂ = A₁B₁ ⊕ C\nP₃ = A₁B₁C')
product = elm.SourceI().right().at((8, 0)).label('P₃P₂P₁P₀')
elm.Line().right().at(a0).to(and00)
elm.Line().right().at(b0).to(and00)
elm.Line().right().at(a0).to(and01)
elm.Line().right().at(b1).to(and01)
elm.Line().right().at(a1).to(and10)
elm.Line().right().at(b0).to(and10)
elm.Line().right().at(a1).to(and11)
elm.Line().right().at(b1).to(and11)
elm.Line().right().at(and00)
elm.Line().right().at(and01)
elm.Line().right().at(and10)
elm.Line().right().at(low_add)
elm.Line().right().at(and11)
elm.Line().right().at(low_add).to(high_add)
elm.Line().right().at(high_add)
elm.Line().right().at(product)
```
