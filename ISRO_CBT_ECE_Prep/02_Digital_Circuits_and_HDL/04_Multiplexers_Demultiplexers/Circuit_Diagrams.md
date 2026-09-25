# Multiplexers and Demultiplexers — Circuit Diagrams

## 1. 2-to-1 Multiplexer

The select line chooses `I0` when `S=0` and `I1` when `S=1`, giving `Y = S'I0 + SI1`. An optional enable forces the output to its inactive value.

```circuit
i0 = elm.SourceI().right().at((-7, 2)).label('I₀')
i1 = elm.SourceI().right().at((-7, -2)).label('I₁')
select = elm.SourceI().right().at((-7, 0)).label('S')
mux = elm.Mux().at((0, 0)).label('2:1 MUX\nY = S\'I₀ + SI₁')
enable = elm.SourceI().right().at((0, 3)).label('E, if present')
output = elm.SourceI().right().at((5, 0)).label('Y')
elm.Line().right().at(i0)
elm.Line().right().at(i1)
elm.Line().right().at(select)
elm.Line().right().at(mux)
elm.Line().up().at((2, 0)).to((2, 3))
elm.Line().right().at(enable)
elm.Line().right().at(output)
```

## 2. 4-to-1 Multiplexer

Two select bits address one of four data inputs. The output is the OR of four mutually exclusive select minterms multiplied by their corresponding data values.

```circuit
i0 = elm.SourceI().right().at((-8, 3)).label('I₀')
i1 = elm.SourceI().right().at((-8, 1)).label('I₁')
i2 = elm.SourceI().right().at((-8, -1)).label('I₂')
i3 = elm.SourceI().right().at((-8, -3)).label('I₃')
s1 = elm.SourceI().right().at((-8, 5)).label('S₁')
s0 = elm.SourceI().right().at((-8, -5)).label('S₀')
mux = elm.Mux().at((0, 0)).label('4:1 MUX\nS₁S₀ selects\nI₀…I₃')
output = elm.SourceI().right().at((5, 0)).label('selected data')
elm.Line().right().at(i0)
elm.Line().right().at(i1)
elm.Line().right().at(i2)
elm.Line().right().at(i3)
elm.Line().right().at(s1)
elm.Line().right().at(s0)
elm.Line().right().at(mux)
elm.Line().right().at(output)
```

## 3. 8-to-1 Multiplexer

Three select lines choose one of eight inputs. This device can realize any four-variable function when three variables address the data inputs and the remaining variable, its complement, zero, or one is placed on each input.

```circuit
i0 = elm.SourceI().right().at((-9, 3)).label('I₀')
i1 = elm.SourceI().right().at((-9, 2)).label('I₁')
i2 = elm.SourceI().right().at((-9, 1)).label('I₂')
i3 = elm.SourceI().right().at((-9, 0)).label('I₃')
i4 = elm.SourceI().right().at((-9, -1)).label('I₄')
i5 = elm.SourceI().right().at((-9, -2)).label('I₅')
i6 = elm.SourceI().right().at((-9, -3)).label('I₆')
i7 = elm.SourceI().right().at((-9, -4)).label('I₇')
select = elm.SourceI().right().at((-9, 6)).label('S₂ S₁ S₀')
mux = elm.Mux().at((0, 0)).label('8:1 MUX')
output = elm.SourceI().right().at((5, 0)).label('Y')
elm.Line().right().at(i0)
elm.Line().right().at(i1)
elm.Line().right().at(i2)
elm.Line().right().at(i3)
elm.Line().right().at(i4)
elm.Line().right().at(i5)
elm.Line().right().at(i6)
elm.Line().right().at(i7)
elm.Line().right().at(select)
elm.Line().right().at(mux)
elm.Line().right().at(output)
```

## 4. MUX as a Universal Logic Implementer

For a three-variable function, `A` and `B` become the select inputs of a 4:1 MUX. For each `AB` assignment, the selected input is `C`, `C'`, 0, or 1 according to the function's truth table.

```circuit
a = elm.SourceI().right().at((-9, 4)).label('A')
b = elm.SourceI().right().at((-9, 2)).label('B')
c = elm.SourceI().right().at((-9, 0)).label('C')
d0 = elm.Block().at((-3, 3)).label('I₀: f when AB=00')
d1 = elm.Block().at((-3, 1)).label('I₁: f when AB=01')
d2 = elm.Block().at((-3, -1)).label('I₂: f when AB=10')
d3 = elm.Block().at((-3, -3)).label('I₃: f when AB=11')
mux = elm.Mux().at((2, 0)).label('4:1 MUX\nA, B on select\nIₖ = 0, 1, C, or C\'')
f = elm.SourceI().right().at((6, 0)).label('f(A, B, C)')
elm.Line().right().at(a)
elm.Line().right().at(b)
elm.Line().right().at(d0)
elm.Line().right().at(d1)
elm.Line().right().at(d2)
elm.Line().right().at(d3)
elm.Line().right().at(mux)
elm.Line().right().at(f)
```

## 5. MUX Used as a Decoder with OR Reduction

A MUX can gate each data input with a select minterm. ORing the selected outputs produces the same function as a binary decoder followed by an OR gate.

```circuit
address = elm.SourceI().right().at((-9, 0)).label('A, B select bits')
mux = elm.Mux().at((-4, 0)).label('MUX data paths')
or_tree = elm.Block().at((1, 0)).label('OR reduction')
f = elm.SourceI().right().at((5, 0)).label('sum of selected minterms')
elm.Line().right().at(address).to(mux)
elm.Line().right().at(mux)
elm.Line().right().at(or_tree)
elm.Line().right().at(f)
```

## 6. 1-to-4 Demultiplexer

A demultiplexer has one data input and routes it to the output selected by the address. All nonselected outputs are inactive, making it the inverse signal-routing operation of a MUX.

```circuit
data = elm.SourceI().right().at((-8, 0)).label('data input D')
select = elm.SourceI().right().at((-8, 3)).label('S₁ S₀')
demux = elm.Demux().at((-2, 0)).label('1:4 DEMUX')
y0 = elm.Block().at((3, 3)).label('Y₀')
y1 = elm.Block().at((3, 1)).label('Y₁')
y2 = elm.Block().at((3, -1)).label('Y₂')
y3 = elm.Block().at((3, -3)).label('Y₃')
elm.Line().right().at(data).to(demux)
elm.Line().up().at((-5, 0)).to((-5, 3))
elm.Line().right().at(select)
elm.Line().right().at(demux)
elm.Line().right().at(y0)
elm.Line().right().at(y1)
elm.Line().right().at(y2)
elm.Line().right().at(y3)
```

## 7. Serial-to-Parallel Demultiplexing

A demultiplexer can distribute successive serial symbols to separate parallel destinations. A destination register or memory row can capture each addressed word.

```circuit
serial = elm.SourceI().right().at((-9, 0)).label('serial bit stream')
address = elm.SourceI().right().at((-9, 3)).label('destination address')
demux = elm.Demux().at((-4, 0)).label('serial-to-parallel\ndemultiplexer')
channel0 = elm.Block().at((2, 3)).label('destination 0')
channel1 = elm.Block().at((2, 1)).label('destination 1')
channel2 = elm.Block().at((2, -1)).label('destination 2')
channel3 = elm.Block().at((2, -3)).label('destination 3')
elm.Line().right().at(serial).to(demux)
elm.Line().up().at((-6, 0)).to((-6, 3))
elm.Line().right().at(address)
elm.Line().right().at(demux)
elm.Line().right().at(channel0)
elm.Line().right().at(channel1)
elm.Line().right().at(channel2)
elm.Line().right().at(channel3)
```

## 8. Cascaded Demultiplexer Tree

Two 1-to-4 demultiplexers driven by the same address produce a 1-to-8 distribution function. The first stage selects a group and the second stage selects within that group.

```circuit
data = elm.SourceI().right().at((-10, 0)).label('data D')
address = elm.SourceI().right().at((-10, 4)).label('S₂ S₁ S₀')
stage1 = elm.Demux().at((-5, 0)).label('stage 1: S₂')
stage2 = elm.Demux().at((0, 2)).label('stage 2: S₁S₀')
stage3 = elm.Demux().at((0, -2)).label('stage 2: S₁S₀')
outputs = elm.Demux().at((5, 0)).label('eight destination lines')
elm.Line().right().at(data).to(stage1)
elm.Line().up().at((-7, 0)).to((-7, 4))
elm.Line().right().at(address)
elm.Line().up().at((-3, 0)).to((-3, 2))
elm.Line().right().at(stage1).to(stage2)
elm.Line().down().at((-3, 0)).to((-3, -2))
elm.Line().right().at(stage1).to(stage3)
elm.Line().right().at(stage2)
elm.Line().right().at(stage3)
elm.Line().right().at(outputs)
```
