# Source Coding and Huffman — Circuit Diagrams

## 1. Huffman Tree Construction

- Combine the two least-probability nodes at each step until only the root remains.
- The more probable branch receives the shorter codeword, so frequent symbols use fewer bits.

```circuit
a = elm.Block()
a.label('A: 0.40')
b = elm.Block()
b.label('B: 0.30')
c = elm.Block()
c.label('C: 0.20')
d = elm.Block()
d.label('D: 0.10')
cd = elm.Block()
cd.label('C+D: 0.30')
bcd = elm.Block()
bcd.label('B+(C+D): 0.60')
root = elm.Block()
root.label('Root: 1.00')
codes = elm.Demux()
codes.label('Prefix codewords')

elm.Line().at(c).right()
elm.Line().at(d).right()
elm.Line().at(c).down()
elm.Line().at(d).down()
elm.Line().at(cd).right()
elm.Line().at(b).right()
elm.Line().at(cd).right()
elm.Line().at(b).down()
elm.Line().at(bcd).right()
elm.Line().at(a).right()
elm.Line().at(bcd).right()
elm.Line().at(a).down()
elm.Line().at(root).right()
elm.Line().at(root).right()
elm.Line().at(codes).right()
```

## 2. Huffman Encoder and Prefix Decoder

- The encoder traverses the tree using source symbols and emits the corresponding variable-length bit sequence.
- The decoder follows branch bits until a leaf is reached, then outputs the symbol without needing lookahead.

```circuit
source = elm.SourceSin()
source.label('Source symbols\nA,B,C,D')
encoder = elm.Block()
encoder.label('Huffman encoder\nA→0, B→10, C→110, D→111')
bitstream = elm.Block()
bitstream.label('Variable-length bitstream')
decoder = elm.Block()
decoder.label('Prefix tree decoder')
leaf = elm.Mux()
leaf.label('Stop at leaf and emit symbol')
output = elm.SourceSin()
output.label('Recovered symbol')

elm.Line().at(source).right()
elm.Line().at(encoder).right()
elm.Line().right()
elm.Line().at(bitstream).right()
elm.Line().right()
elm.Line().at(decoder).right()
elm.Line().right()
elm.Line().at(leaf).right()
elm.Line().right()
elm.Line().at(output).right()
```

## 3. Fixed-Length, Variable-Length, and Kraft Check

- Fixed-length coding is simple and resynchronizes quickly but spends equal bits on every symbol.
- A prefix code satisfies Σ2⁻ˡᵢ ≤ 1; Huffman average length obeys H ≤ L_avg < H+1.

```circuit
fixed_source = elm.SourceSin()
fixed_source.label('Fixed-size symbols')
fixed_encoder = elm.Block()
fixed_encoder.label('Fixed n-bit encoder')
fixed_channel = elm.Block()
fixed_channel.label('Equal-length codewords')

elm.Line().at(fixed_source).right()
elm.Line().at(fixed_encoder).right()
elm.Line().right()
elm.Line().at(fixed_channel).right()

variable_source = elm.SourceSin()
variable_source.label('Skewed source')
variable_encoder = elm.Block()
variable_encoder.label('Huffman encoder')
variable_channel = elm.Block()
variable_channel.label('Prefix variable-length words')
metrics = elm.Block()
metrics.label('H≤L_avg<H+1\nΣ2⁻ˡᵢ≤1\nEfficiency=H/L_avg')

elm.Line().at(variable_source).right()
elm.Line().at(variable_encoder).right()
elm.Line().right()
elm.Line().at(variable_channel).right()
elm.Line().right()
elm.Line().at(metrics).right()
```
