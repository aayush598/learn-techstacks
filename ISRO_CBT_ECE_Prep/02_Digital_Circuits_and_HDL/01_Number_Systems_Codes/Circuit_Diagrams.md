# Number Systems and Codes — Circuit Diagrams

## 1. Two's-Complement Negation

Two's-complement negation complements every input bit and then adds one. In fixed-width logic, discarding carry-out preserves the result in the same number of bits.

```circuit
value = elm.SourceI().right().at((-6, 0)).label('N [n bits]')
invert = elm.NotGate().at((-3, 0)).label('bitwise NOT')
add_one = elm.Block().at((0, 0)).label('add 1\nignore carry-out')
result = elm.SourceI().right().at((3, 0)).label('−N mod 2ⁿ')
elm.Line().right().at(value)
elm.Line().right().at(invert)
elm.Line().right().at(add_one)
elm.Line().right().at(result)
```

## 2. 8421 BCD Adder with Decimal Correction

Two 8421 BCD digits are first added as binary. A correction of `0110` is selected whenever the raw sum exceeds nine or the fourth bit carries.

```circuit
left = elm.SourceI().right().at((-7, 1)).label('A: 4-bit BCD')
right = elm.SourceI().right().at((-7, -1)).label('B: 4-bit BCD')
binary_sum = elm.Block().at((-3, 0)).label('4-bit binary adder')
digit_test = elm.Block().at((1, 1)).label('sum > 1001\nor carry = 1')
six = elm.SourceI().right().at((1, -1)).label('0110')
corrector = elm.Mux().at((5, 0)).label('decimal corrector')
output = elm.SourceI().right().at((9, 0)).label('BCD sum')
elm.Line().right().at(left).to(binary_sum)
elm.Line().right().at(right).to(binary_sum)
elm.Line().right().at(binary_sum)
elm.Line().up().at((1, 1)).to((1, 0))
elm.Line().right().at(digit_test)
elm.Line().up().at((1, -1)).to((1, 0))
elm.Line().right().at(six)
elm.Line().right().at(digit_test)
elm.Line().right().at(corrector)
elm.Line().right().at(corrector)
elm.Line().right().at(output)
```

## 3. 8421, Excess-3, and 2421 Code Mapping

A decimal digit is encoded independently in each weighted or non-weighted BCD system. The three outputs represent the same decimal value.

```circuit
digit = elm.SourceI().right().at((-6, 0)).label('decimal digit d')
encoder_8421 = elm.Block().at((-2, 2)).label('8421 encoder\nvalue d')
encoder_excess3 = elm.Block().at((-2, 0)).label('Excess-3 encoder\nvalue d + 0011')
encoder_2421 = elm.Block().at((-2, -2)).label('2421 encoder\nweighted code')
outputs = elm.Demux().at((3, 0)).label('parallel codewords')
elm.Line().up().at((-4, 0)).to((-4, 2))
elm.Line().right().at(digit)
elm.Line().down().at((-4, 0)).to((-4, -2))
elm.Line().right().at(encoder_8421)
elm.Line().right().at(encoder_excess3)
elm.Line().right().at(encoder_2421)
elm.Line().right().at(outputs)
```

## 4. Binary-to-Gray Converter

Each Gray bit is the XOR of two adjacent binary bits; the most significant Gray bit is copied directly. Consecutive binary values therefore produce single-bit Gray transitions.

```circuit
b3 = elm.SourceI().right().at((-7, 3)).label('B₃')
b2 = elm.SourceI().right().at((-7, 1)).label('B₂')
b1 = elm.SourceI().right().at((-7, -1)).label('B₁')
b0 = elm.SourceI().right().at((-7, -3)).label('B₀')
g3 = elm.Block().right().at((-2, 3)).label('G₃ = B₃')
g2 = elm.XorGate().at((-2, 1)).label('G₂ = B₃ ⊕ B₂')
g1 = elm.XorGate().at((-2, -1)).label('G₁ = B₂ ⊕ B₁')
g0 = elm.XorGate().at((-2, -3)).label('G₀ = B₁ ⊕ B₀')
gray = elm.SourceI().right().at((3, 0)).label('G₃G₂G₁G₀')
elm.Line().right().at(b3)
elm.Line().right().at(b3)
elm.Line().down().at((-5, 3)).to((-5, 1))
elm.Line().right().at(b2)
elm.Line().right().at(b2)
elm.Line().down().at((-5, 1)).to((-5, -1))
elm.Line().right().at(b1)
elm.Line().right().at(b1)
elm.Line().down().at((-5, -1)).to((-5, -3))
elm.Line().right().at(b0)
elm.Line().right().at(g3)
elm.Line().right().at(g2)
elm.Line().right().at(g1)
elm.Line().right().at(g0)
elm.Line().right().at(gray)
```

## 5. Gray-to-Binary Converter

Gray-to-binary conversion is a prefix XOR. Starting with the Gray MSB, each binary bit is formed from the previously reconstructed binary bit and the next Gray bit.

```circuit
g3 = elm.SourceI().right().at((-7, 3)).label('G₃')
g2 = elm.SourceI().right().at((-7, 1)).label('G₂')
g1 = elm.SourceI().right().at((-7, -1)).label('G₁')
g0 = elm.SourceI().right().at((-7, -3)).label('G₀')
b3 = elm.Block().right().at((-2, 3)).label('B₃ = G₃')
b2 = elm.XorGate().at((-2, 1)).label('B₂ = B₃ ⊕ G₂')
b1 = elm.XorGate().at((-2, -1)).label('B₁ = B₂ ⊕ G₁')
b0 = elm.XorGate().at((-2, -3)).label('B₀ = B₁ ⊕ G₀')
binary = elm.SourceI().right().at((3, 0)).label('B₃B₂B₁B₀')
elm.Line().right().at(g3)
elm.Line().right().at(g3)
elm.Line().down().at((-5, 3)).to((-5, 1))
elm.Line().right().at(g2)
elm.Line().right().at(g2)
elm.Line().down().at((-5, 1)).to((-5, -1))
elm.Line().right().at(g1)
elm.Line().right().at(g1)
elm.Line().down().at((-5, -1)).to((-5, -3))
elm.Line().right().at(g0)
elm.Line().right().at(b3)
elm.Line().right().at(b2)
elm.Line().right().at(b1)
elm.Line().right().at(b0)
elm.Line().right().at(binary)
```

## 6. Parity Generation and Checking

An XOR tree generates even parity. The checker XORs every received bit with the transmitted parity bit; zero means the received even-parity word is correct.

```circuit
data = elm.SourceI().right().at((-7, 1)).label('data D[3:0]')
xor1 = elm.XorGate().at((-3, 1)).label('D₃ ⊕ D₂')
xor2 = elm.XorGate().at((0, 1)).label('D₁ ⊕ D₀')
parity = elm.XorGate().at((3, 1)).label('even parity P')
check = elm.XorGate().at((6, 0)).label('received-word XOR')
error = elm.SourceI().right().at((9, 0)).label('0: valid, 1: error')
elm.Line().right().at(data)
elm.Line().right().at(xor1)
elm.Line().right().at(xor2)
elm.Line().right().at(parity)
elm.Line().down().at((4, 1)).to((4, 0))
elm.Line().right().at(parity)
elm.Line().right().at(check)
elm.Line().right().at(error)
```

## 7. Hamming SEC-DED Encoder and Syndrome Decoder

Parity bits occupy positions 1, 2, 4, 8, and so on. At the receiver, the parity-check result forms a syndrome that identifies a correctable single-bit position and distinguishes a detected double-bit error.

```circuit
data = elm.SourceI().right().at((-8, 0)).label('data word')
encoder = elm.Block().at((-4, 0)).label('Hamming encoder\nP1, P2, P4 placed at\npositions 1, 2, 4')
channel = elm.Block().at((0, 0)).label('noisy SEC-DED codeword')
syndrome = elm.Block().at((4, 0)).label('parity checks\nproduce syndrome')
decision = elm.Block().at((8, 0)).label('0: no error\nnonzero: locate error\n1-bit: correct')
elm.Line().right().at(data)
elm.Line().right().at(encoder)
elm.Line().right().at(channel)
elm.Line().right().at(syndrome)
elm.Line().right().at(decision)
```

## 8. ASCII Case-Conversion Hardware

ASCII upper- and lowercase letters differ by bit 5, with a difference of 32. Clearing bit 5 converts uppercase to lowercase; setting it converts lowercase to uppercase.

```circuit
ascii = elm.SourceI().right().at((-7, 0)).label('7-bit ASCII [6:0]')
uppercase = elm.Block().at((-2, 1)).label("uppercase range\n'0' to '9', 'A' to 'Z'")
lowercase = elm.Block().at((-2, -1)).label("lowercase range\n'a' to 'z'")
clear_bit5 = elm.Block().at((2, 1)).label('upper → lower\nclear bit 5')
set_bit5 = elm.Block().at((2, -1)).label('lower → upper\nset bit 5')
result = elm.Mux().at((6, 0)).label('ASCII result')
elm.Line().up().at((-5, 0)).to((-5, 1))
elm.Line().right().at(ascii)
elm.Line().down().at((-5, 0)).to((-5, -1))
elm.Line().right().at(uppercase)
elm.Line().right().at(lowercase)
elm.Line().right().at(clear_bit5)
elm.Line().right().at(set_bit5)
elm.Line().right().at(result)
```
