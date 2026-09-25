# Pulse Modulation and PCM — Circuit Diagrams

## 1. PAM Sampling and Hold

- A clocked switch extracts the message amplitude at regularly spaced sampling instants.
- The capacitor provides a practical flat-top or zero-order hold between updates.

```circuit
message = elm.SourceSin()
message.label('Analog m(t)')
clock = elm.SourceSin()
clock.label('Sampling clock')
switch = elm.Mux()
switch.label('Sampling switch')

elm.Line().at(message).right()
elm.Line().at(clock).down()
elm.Line().at(switch).right()
elm.Line().right()
elm.Dot().label('PAM samples')
elm.Capacitor().down().label('C: sample and hold')
elm.Line().right().label('Flat-top PAM output')
```

## 2. PCM Transmitter and Receiver

- Sampling, n-bit quantization, and binary encoding convert each analog sample into a PCM word.
- The decoder converts code words back to levels before a reconstruction filter restores the message waveform.

```circuit
source = elm.SourceSin()
source.label('Analog m(t)')
sampler = elm.Block()
sampler.label('Sampler\nf_s ≥ 2f_max')
quantizer = elm.Block()
quantizer.label('Quantizer\n2ⁿ levels')
encoder = elm.Block()
encoder.label('Binary encoder\nn bits/sample')
line = elm.Block()
line.label('PCM bitstream\nR_b = nf_s')
channel = elm.Block()
channel.label('Noisy channel')
decoder = elm.Block()
decoder.label('PCM decoder')
reconstructor = elm.Block()
reconstructor.label('Reconstruction LPF')
output = elm.SourceSin()
output.label('Recovered m̂(t)')

elm.Line().at(source).right()
elm.Line().at(sampler).right()
elm.Line().right()
elm.Line().at(quantizer).right()
elm.Line().right()
elm.Line().at(encoder).right()
elm.Line().right()
elm.Line().at(line).right()
elm.Line().right()
elm.Line().at(channel).right()
elm.Line().right()
elm.Line().at(decoder).right()
elm.Line().right()
elm.Line().at(reconstructor).right()
elm.Line().right()
elm.Line().at(output).right()
```

## 3. Differential PCM

- The encoder sends the difference between the current sample and a reconstructed previous sample.
- The decoder adds the received difference to feedback to recover the current level.

```circuit
sample = elm.SourceSin()
sample.label('Current x[n]')
feedback = elm.Block()
feedback.label('Previous estimate\nx̂[n−1]')
difference = elm.Block()
difference.label('Difference\nd[n]=x[n]−x̂[n−1]')
quantizer = elm.Block()
quantizer.label('Difference quantizer')
bits = elm.Block()
bits.label('PCM difference bits')

elm.Line().at(sample).right()
elm.Line().at(difference).right()
elm.Line().at(feedback).down()
elm.Line().at(difference).down()
elm.Line().at(quantizer).right()
elm.Line().right()
elm.Line().at(bits).right()
elm.Line().right()
elm.Block().label('DPCM channel')
elm.Line().right()
elm.Block().label('Difference decoder + adder')
elm.Line().right()
elm.Block().label('Reconstructed x̂[n]')
elm.Line().down()
elm.Line().at(feedback).left()
```

## 4. Delta Modulation and Demodulation

- A one-bit decision produces an upward or downward step based on the comparator error.
- At the receiver, the bit stream directly drives an accumulator; slope overload and granular noise are the two design limits.

```circuit
message = elm.SourceSin()
message.label('Message m(t)')
error = elm.Block()
error.label('m(nT_s) − ŷ(n−1)')
comparator = elm.Opamp()
comparator.label('One-bit comparator')
step = elm.Mux()
step.label('+Δ / −Δ step')
quantized = elm.Block()
quantized.label('DM bit stream')
accumulator = elm.Block()
accumulator.label('Integrating staircase')
output = elm.Block()
output.label('Staircase reconstruction')

elm.Line().at(message).right()
elm.Line().at(error).right()
elm.Line().right()
elm.Line().at(comparator).right()
elm.Line().at(step).right()
elm.Line().right()
elm.Line().at(quantized).right()
elm.Line().right()
elm.Block().label('DM channel')
elm.Line().right()
elm.Line().at(accumulator).right()
elm.Line().right()
elm.Line().at(output).right()
elm.Line().down()
elm.Line().at(error).left()

elm.Block().down().label('Δ/T_s ≥ max|dm/dt|\notherwise slope overload')
```

## 5. Quantization and Companding

- Increasing n provides 2ⁿ levels and improves full-scale sinusoid SQNR by about 6.02 dB per bit.
- A-law or μ-law companding allocates finer quantization near zero to improve low-level speech SQNR.

```circuit
analog = elm.SourceSin()
analog.label('Uniform-range voice')
compander = elm.Block()
compander.label('Compander\nA-law or μ-law')
encoder = elm.Block()
encoder.label('n-bit encoder')
channel = elm.Block()
channel.label('Digital channel')
decoder = elm.Block()
decoder.label('n-bit decoder')
expander = elm.Block()
expander.label('Expander')
output = elm.SourceSin()
output.label('Expanded PCM')

elm.Line().at(analog).right()
elm.Line().at(compander).right()
elm.Line().right()
elm.Line().at(encoder).right()
elm.Line().right()
elm.Line().at(channel).right()
elm.Line().right()
elm.Line().at(decoder).right()
elm.Line().right()
elm.Line().at(expander).right()
elm.Line().right()
elm.Line().at(output).right()

elm.Block().down().label('Δ=V_pp/2ⁿ\nN_q=Δ²/12\nSQNR≈6.02n+1.76 dB')
```
