# Eye Diagrams and BER — Circuit Diagrams

## 1. Eye-Diagram Measurement Setup

- A symbol-clock-triggered oscilloscope overlays many received two-symbol intervals.
- Eye height exposes amplitude margin, eye width exposes timing margin, and thickness and closure reveal noise, jitter, and ISI.

```circuit
pattern = elm.Block()
pattern.label('PRBS / symbol generator')
transmitter = elm.Block()
transmitter.label('Line driver')
channel = elm.Block()
channel.label('Lossy channel\nAWGN + ISI')
receiver = elm.Block()
receiver.label('Equalizer and RX front end')
symbol_clock = elm.SourceSin()
symbol_clock.label('Recovered symbol clock')
scope = elm.Block()
scope.label('Oscilloscope\nX-Y symbol traces')
eye = elm.Block()
eye.label('Eye overlay\nheight, width, closure')

elm.Line().at(pattern).right()
elm.Line().at(transmitter).right()
elm.Line().right()
elm.Line().at(channel).right()
elm.Line().right()
elm.Line().at(receiver).right()
elm.Line().right()
elm.Line().at(scope).right()
elm.Line().right()
elm.Line().at(eye).right()
elm.Line().at(symbol_clock).down()
elm.Line().at(symbol_clock).right()
```

## 2. BER Test Setup

- The error comparator checks each received bit against the known reference pattern.
- The error counter divides the error total by the transmitted bit count, producing the measured BER.

```circuit
pattern = elm.Block()
pattern.label('Reference PRBS')
transmit = elm.Block()
transmit.label('Transmit bits')
channel = elm.Block()
channel.label('Noisy link')
receive = elm.Block()
receive.label('Recovered bits')
xor_error = elm.XorGate()
xor_error.label('Reference XOR received')
error_count = elm.Block()
error_count.label('Count bit errors')
bit_count = elm.Block()
bit_count.label('Count transmitted bits')
ber = elm.Block()
ber.label('BER=errors/transmitted bits')
sweep = elm.Block()
sweep.label('Sweep Eb/N0 and plot BER')

elm.Line().at(pattern).right()
elm.Line().at(transmit).right()
elm.Line().right()
elm.Line().at(channel).right()
elm.Line().right()
elm.Line().at(receive).right()
elm.Line().at(xor_error).right()
elm.Line().at(pattern).down()
elm.Line().at(pattern).right()
elm.Line().at(xor_error).down()
elm.Line().at(xor_error).right()
elm.Line().right()
elm.Line().at(error_count).right()
elm.Line().right()
elm.Line().at(ber).right()
elm.Line().at(bit_count).down()
elm.Line().at(bit_count).right()
elm.Line().at(ber).down()
elm.Line().at(sweep).right()
```

## 3. Pulse Shaping and Equalization for Zero ISI

- A raised-cosine transmit filter controls excess bandwidth while maintaining zero intersymbol interference at the sampling instants.
- The receiver equalizer compensates residual channel distortion and restores eye opening.

```circuit
symbols = elm.SourceSin()
symbols.label('Symbol impulses')
upsample = elm.Block()
upsample.label('Upsample and shape')
raised_cosine = elm.Block()
raised_cosine.label('Raised-cosine TX filter\nB=(1+α)R_s/2')
channel = elm.Block()
channel.label('Dispersive channel')
equalizer = elm.Block()
equalizer.label('Zero-forcing or MMSE\nequalizer')
sampler = elm.Block()
sampler.label('Sample at center of eye')
output = elm.Block()
output.label('Open eye and lower BER')

elm.Line().at(symbols).right()
elm.Line().at(upsample).right()
elm.Line().right()
elm.Line().at(raised_cosine).right()
elm.Line().right()
elm.Line().at(channel).right()
elm.Line().right()
elm.Line().at(equalizer).right()
elm.Line().right()
elm.Line().at(sampler).right()
elm.Line().right()
elm.Line().at(output).right()
```

## 4. Coding Gain on a BER Curve

- Coding improves power efficiency by allowing the same BER at lower Eb/N0.
- On a log-BER plot, this coding gain appears as a leftward shift of the coded curve.

```circuit
uncoded = elm.Block()
uncoded.label('Uncoded link\nP_b=Q(√(2E_b/N₀))')
coded = elm.Block()
coded.label('Coded link\nlower required Eb/N0')
marker = elm.Block()
marker.label('Same target BER')
shift = elm.Block()
shift.label('Coding gain\nEb/N₀ uncoded − Eb/N₀ coded')

elm.Line().at(uncoded).right()
elm.Line().right()
elm.Line().at(marker).right()
elm.Line().at(coded).down()
elm.Line().at(coded).right()
elm.Line().at(marker).down()
elm.Line().at(marker).right()
elm.Line().right()
elm.Line().at(shift).right()
```
