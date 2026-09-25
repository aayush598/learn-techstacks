# Decoders and Encoders — Circuit Diagrams

## 1. 2-to-4 Decoder

A two-bit input selects exactly one of four mutually exclusive minterm outputs. With an active-high enable, `Yi=E·minterm(i)`.

```circuit
a = elm.SourceI().right().at((-9, 1)).label('A')
b = elm.SourceI().right().at((-9, -1)).label('B')
enable = elm.SourceI().right().at((-9, 4)).label('E')
decoder = elm.Block().at((-4, 0)).label('2-to-4 decoder')
y0 = elm.Block().at((2, 3)).label("Y₀ = E·A'B'")
y1 = elm.Block().at((2, 1)).label("Y₁ = E·A'B")
y2 = elm.Block().at((2, -1)).label("Y₂ = E·AB'")
y3 = elm.Block().at((2, -3)).label("Y₃ = E·AB")
elm.Line().right().at(a).to(decoder)
elm.Line().right().at(b).to(decoder)
elm.Line().up().at((-6, 0)).to((-6, 4))
elm.Line().right().at(enable)
elm.Line().right().at(decoder)
elm.Line().right().at(y0)
elm.Line().right().at(y1)
elm.Line().right().at(y2)
elm.Line().right().at(y3)
```

## 2. 3-to-8 Decoder

Each output is one three-variable minterm. The decoder therefore converts a binary code into a one-hot selection useful for address routing and function generation.

```circuit
address = elm.SourceI().right().at((-10, 0)).label('A B C')
decoder = elm.Block().at((-5, 0)).label('3-to-8 decoder')
y0 = elm.Block().at((0, 4)).label("Y₀ = A'B'C'")
y1 = elm.Block().at((0, 3)).label("Y₁ = A'B'C")
y2 = elm.Block().at((0, 2)).label("Y₂ = A'BC'")
y3 = elm.Block().at((0, 1)).label("Y₃ = A'BC")
y4 = elm.Block().at((0, 0)).label("Y₄ = AB'C'")
y5 = elm.Block().at((0, -1)).label("Y₅ = AB'C")
y6 = elm.Block().at((0, -2)).label("Y₆ = ABC'")
y7 = elm.Block().at((0, -3)).label("Y₇ = ABC")
elm.Line().right().at(address).to(decoder)
elm.Line().right().at(decoder)
elm.Line().right().at(y0)
elm.Line().right().at(y1)
elm.Line().right().at(y2)
elm.Line().right().at(y3)
elm.Line().right().at(y4)
elm.Line().right().at(y5)
elm.Line().right().at(y6)
elm.Line().right().at(y7)
```

## 3. 4-to-2 Encoder

A one-hot input `D0` through `D3` is encoded as two binary bits. This ordinary encoder assumes that no more than one input is active.

```circuit
d0 = elm.SourceI().right().at((-9, 3)).label('D₀')
d1 = elm.SourceI().right().at((-9, 1)).label('D₁')
d2 = elm.SourceI().right().at((-9, -1)).label('D₂')
d3 = elm.SourceI().right().at((-9, -3)).label('D₃')
encoder = elm.Block().at((-4, 0)).label('4-to-2 encoder')
a_out = elm.Block().at((1, 1)).label('A = D1 + D3')
b_out = elm.Block().at((1, -1)).label('B = D2 + D3')
elm.Line().right().at(d0).to(encoder)
elm.Line().right().at(d1).to(encoder)
elm.Line().right().at(d2).to(encoder)
elm.Line().right().at(d3).to(encoder)
elm.Line().right().at(encoder)
elm.Line().up().at((-2, 0)).to((-2, 1))
elm.Line().right().at(a_out)
elm.Line().down().at((-2, 0)).to((-2, -1))
elm.Line().right().at(b_out)
```

## 4. 4-to-2 Priority Encoder

The priority encoder resolves simultaneous requests by selecting the highest active input. The valid flag is the OR of all request lines, while the code is driven only when at least one request exists.

```circuit
i0 = elm.SourceI().right().at((-9, -3)).label('I₀')
i1 = elm.SourceI().right().at((-9, -1)).label('I₁')
i2 = elm.SourceI().right().at((-9, 1)).label('I₂')
i3 = elm.SourceI().right().at((-9, 3)).label('I₃ highest')
encoder = elm.Block().at((-4, 0)).label('priority encoder\nD3 > D2 > D1 > D0')
code = elm.Block().at((1, 0)).label('Y₁Y₀')
valid = elm.Block().at((1, -3)).label('V = I0 + I1 + I2 + I3')
elm.Line().right().at(i0).to(encoder)
elm.Line().right().at(i1).to(encoder)
elm.Line().right().at(i2).to(encoder)
elm.Line().right().at(i3).to(encoder)
elm.Line().right().at(encoder)
elm.Line().right().at(code)
elm.Line().down().at((-2, 0)).to((-2, -3))
elm.Line().right().at(valid)
```

## 5. Decoder with Active-Low Enable

A low enable turns every output off. When enabled, the decoder produces the one-hot output corresponding to the input code; the enable input is especially useful when combining decoder blocks.

```circuit
address = elm.SourceI().right().at((-8, 1)).label('address A B')
enable_bar = elm.SourceI().right().at((-8, 4)).label("active-low enable E'")
decoder = elm.Block().at((-3, 0)).label('2-to-4 decoder\nE low: all Y=0')
outputs = elm.Demux().at((3, 0)).label('Y₀ Y₁ Y₂ Y₃')
elm.Line().right().at(address).to(decoder)
elm.Line().up().at((-5, 0)).to((-5, 4))
elm.Line().right().at(enable_bar)
elm.Line().right().at(decoder)
elm.Line().right().at(outputs)
```

## 6. Cascaded 4-to-16 Decoder

Two 3-to-8 decoders share the three low-order address bits. The fourth address bit enables one decoder and disables the other, producing sixteen one-hot outputs.

```circuit
low_bits = elm.SourceI().right().at((-10, 0)).label('A₂ A₁ A₀')
high_bit = elm.SourceI().right().at((-10, 4)).label('A₃')
decoder_low = elm.Block().at((-5, -1)).label('3-to-8 decoder\nlow group')
decoder_high = elm.Block().at((-5, 3)).label('3-to-8 decoder\nhigh group')
outputs = elm.Demux().at((2, 1)).label('Y₀ … Y₁₅')
elm.Line().right().at(low_bits)
elm.Line().up().at((-7, 0)).to((-7, 3))
elm.Line().right().at(high_bit)
elm.Line().right().at(decoder_low)
elm.Line().right().at(decoder_high)
elm.Line().right().at(outputs)
```

## 7. Decoder and OR Gate as a Universal Function Generator

A decoder generates all minterms of the input variables. Connecting the outputs corresponding to `1`s in the truth table to an OR gate realizes any sum-of-products function.

```circuit
variables = elm.SourceI().right().at((-10, 0)).label('variables A, B, C')
decoder = elm.Block().at((-5, 0)).label('decoder\nm₀ … m₇')
selected = elm.Block().at((0, 0)).label('OR selected minterms\nfor Σm(i)')
function = elm.SourceI().right().at((5, 0)).label('f(A, B, C)')
elm.Line().right().at(variables).to(decoder)
elm.Line().right().at(decoder)
elm.Line().right().at(selected)
elm.Line().right().at(function)
```
