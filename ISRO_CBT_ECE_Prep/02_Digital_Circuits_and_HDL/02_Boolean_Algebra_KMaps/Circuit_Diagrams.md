# Boolean Algebra and K-Maps — Circuit Diagrams

## 1. Fundamental Logic Gates

AND requires every input to be high, OR requires at least one high input, NOT reverses one input, and XOR is high when an odd number of inputs are high.

```circuit
a = elm.SourceI().right().at((-6, 3)).label('A')
b = elm.SourceI().right().at((-6, 1)).label('B')
and_gate = elm.AndGate().at((-2, 2)).label('AND')
a2 = elm.SourceI().right().at((-6, -1)).label('A')
b2 = elm.SourceI().right().at((-6, -3)).label('B')
or_gate = elm.OrGate().at((-2, -2)).label('OR')
a3 = elm.SourceI().right().at((-6, -5)).label('A')
not_gate = elm.NotGate().at((-2, -5)).label('NOT')
a4 = elm.SourceI().right().at((-6, -7)).label('A')
b4 = elm.SourceI().right().at((-6, -9)).label('B')
xor_gate = elm.XorGate().at((-2, -8)).label('XOR')
elm.Line().right().at(a)
elm.Line().right().at(b)
elm.Line().right().at(and_gate)
elm.Line().right().at(a2)
elm.Line().right().at(b2)
elm.Line().right().at(or_gate)
elm.Line().right().at(a3)
elm.Line().right().at(not_gate)
elm.Line().right().at(a4)
elm.Line().right().at(b4)
elm.Line().right().at(xor_gate)
```

## 2. De Morgan Equivalent Forms

A bubbled OR input is equivalent to an AND of complemented inputs. A bubbled AND input is equivalent to an OR of complemented inputs; these are NOR and NAND forms.

```circuit
a = elm.SourceI().right().at((-8, 1)).label('A')
b = elm.SourceI().right().at((-8, -1)).label('B')
original = elm.OrGate().at((-4, 0)).label('A + B')
invert_result = elm.NotGate().at((0, 0)).label("(A + B)'")
elm.Line().right().at(a)
elm.Line().right().at(b)
elm.Line().right().at(original)
elm.Line().right().at(invert_result)
not_a = elm.NotGate().right().at((-6, -4)).label("A'")
not_b = elm.NotGate().right().at((-6, -6)).label("B'")
equivalent = elm.AndGate().at((-2, -5)).label("A' · B'")
elm.Line().right().at(not_a)
elm.Line().right().at(not_b)
elm.Line().right().at(equivalent)
```

## 3. Two-Level SOP and POS Networks

SOP uses an AND plane followed by an OR plane. POS reverses that structure. NAND-only realization is obtained from SOP by replacing both levels and complementing the final output; NOR-only realization analogously realizes POS.

```circuit
ab = elm.AndGate().at((-4, 2)).label('A · B')
cd = elm.AndGate().at((-4, -1)).label('C · D')
sop = elm.OrGate().at((0, 0)).label('SOP\nAB + CD')
a_or_c = elm.OrGate().at((-4, -5)).label('A + C')
b_or_d = elm.OrGate().at((-4, -7)).label('B + D')
pos = elm.AndGate().at((0, -6)).label('POS\n(A + C)(B + D)')
nand_output = elm.NotGate().at((4, 0)).label("NAND-only SOP\nfinal inversion")
nor_output = elm.NotGate().at((4, -6)).label("NOR-only POS\nfinal inversion")
elm.Line().right().at(ab)
elm.Line().right().at(cd)
elm.Line().right().at(sop)
elm.Line().right().at(a_or_c)
elm.Line().right().at(b_or_d)
elm.Line().right().at(pos)
elm.Line().right().at(sop)
elm.Line().right().at(nand_output)
elm.Line().right().at(pos)
elm.Line().right().at(nor_output)
```

## 4. Four-Variable Karnaugh Map

Gray-code ordering makes adjacent cells differ in one variable. A power-of-two group removes every variable that changes within that group.

```circuit
c00 = elm.Block().at((-5, 3)).label('m0')
c01 = elm.Block().at((-2, 3)).label('m1')
c03 = elm.Block().at((1, 3)).label('m3')
c02 = elm.Block().at((4, 3)).label('m2')
c04 = elm.Block().at((-5, 0)).label('m4')
c05 = elm.Block().at((-2, 0)).label('m5')
c07 = elm.Block().at((1, 0)).label('m7')
c06 = elm.Block().at((4, 0)).label('m6')
c12 = elm.Block().at((-5, -3)).label('m12')
c13 = elm.Block().at((-2, -3)).label('m13')
c15 = elm.Block().at((1, -3)).label('m15')
c14 = elm.Block().at((4, -3)).label('m14')
c08 = elm.Block().at((-5, -6)).label('m8')
c09 = elm.Block().at((-2, -6)).label('m9')
c11 = elm.Block().at((1, -6)).label('m11')
c10 = elm.Block().at((4, -6)).label('m10')
columns = elm.Block().at((0, 6)).label('columns: CD = 00, 01, 11, 10')
rows = elm.Block().at((-8, -1.5)).label('rows:\nAB = 00,\n01,\n11,\n10')
group = elm.Block().at((7, -1.5)).label('example group\nm4, m5, m12, m13\n→ B=1')
elm.Line().right().at(c00)
elm.Line().right().at(c01)
elm.Line().right().at(c03)
elm.Line().right().at(c02)
elm.Line().right().at(c04)
elm.Line().right().at(c05)
elm.Line().right().at(c07)
elm.Line().right().at(c06)
elm.Line().right().at(c12)
elm.Line().right().at(c13)
elm.Line().right().at(c15)
elm.Line().right().at(c14)
elm.Line().right().at(c08)
elm.Line().right().at(c09)
elm.Line().right().at(c11)
elm.Line().right().at(c10)
elm.Line().right().at(group)
```

## 5. Shannon Expansion with a MUX Tree

Shannon expansion splits a function on one variable. Each cofactor becomes a data input of a selector controlled by that variable; repeating the process yields a 2ⁿ:1 MUX implementation.

```circuit
selector = elm.SourceI().right().at((-8, 0)).label('select variable A')
f0 = elm.Block().at((-3, 2)).label("f₀ = f(0, B, C, …)")
f1 = elm.Block().at((-3, -2)).label("f₁ = f(1, B, C, …)")
mux = elm.Mux().at((2, 0)).label('cofactor selector')
f = elm.SourceI().right().at((6, 0)).label('f(A, B, C, …)')
elm.Line().up().at((-6, 0)).to((-6, 2))
elm.Line().right().at(selector)
elm.Line().down().at((-6, 0)).to((-6, -2))
elm.Line().right().at(f0)
elm.Line().right().at(f1)
elm.Line().right().at(mux)
elm.Line().right().at(f)
```

## 6. Consensus-Term Elimination

When the two non-consensus product terms contain complemented and uncomplemented versions of the controlling variable, their common consensus term is redundant.

```circuit
ab = elm.Block().at((-5, 2)).label('AB')
ac_bar = elm.Block().at((-5, 0)).label("A'C")
bc = elm.Block().at((-5, -2)).label('BC\nconsensus')
sum = elm.OrGate().at((0, 0)).label('AB + A\'C + BC')
simplified = elm.Block().at((5, 0)).label('absorb consensus BC\nAB + A\'C')
elm.Line().right().at(ab)
elm.Line().right().at(ac_bar)
elm.Line().right().at(bc)
elm.Line().right().at(sum)
elm.Line().right().at(simplified)
```
