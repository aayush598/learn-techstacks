# FM and Angle Modulation — Circuit Diagrams

## 1. FM Transmitter with Message Integration

- Integrating the message creates the phase term required for frequency modulation.
- A VCO converts the integrated control voltage into a constant-amplitude carrier whose instantaneous frequency is f_c + k_fm(t).

```circuit
message = elm.SourceSin()
message.label('m(t)')
integrator = elm.Block()
integrator.label('Integrator\n∫m(τ)dτ')
oscillator = elm.Block()
oscillator.label('VCO / phase modulator')

elm.Line().at(message).right()
elm.Line().at(integrator).right()
elm.Line().right()
elm.Line().at(oscillator).right()
elm.Line().right()
elm.Block().label('FM signal\nA_c cos[2πf_ct+2πk_f∫m(t)dt]')

carrier = elm.SourceSin()
carrier.label('Carrier reference')
elm.Line().at(carrier).up()
```

## 2. Direct Phase Modulation

- Unlike FM, the PM block uses m(t) directly as its phase control input.
- Instantaneous frequency deviation is proportional to dm(t)/dt, so PM deviation depends on message frequency.

```circuit
message = elm.SourceSin()
message.label('m(t)')
carrier = elm.SourceSin()
carrier.label('cos(2πf_c t)')

elm.Line().at(message).right()
elm.Block().label('Phase modulator\n+k_p m(t)')
elm.Line().at(carrier).down()
elm.Line().right()
elm.Block().label('PM signal\nA_c cos[2πf_ct+k_pm(t)]')

frequency = elm.Block()
frequency.label('Differentiation\nf_inst = f_c + (k_p/2π)dm/dt')
elm.Line().at(frequency).down()
```

## 3. FM Discriminator Chain

- A limiter removes amplitude noise before the frequency-to-voltage discriminator.
- The receiver low-pass filter rejects high-order FM sideband products and retains the recovered message bandwidth.

```circuit
received = elm.SourceSin()
received.label('FM RF input')
limiter = elm.Block()
limiter.label('Limiter\nconstant amplitude')
discriminator = elm.Block()
discriminator.label('Frequency discriminator')
lowpass = elm.Block()
lowpass.label('Low-pass filter\ncutoff near f_m')

elm.Line().at(received).right()
elm.Line().at(limiter).right()
elm.Line().right()
elm.Line().at(discriminator).right()
elm.Line().right()
elm.Line().at(lowpass).right()
elm.Line().right()
elm.Block().label('Demodulated m(t)')

output = elm.SourceSin()
output.label('Audio output')
elm.Line().at(output).up()
```

## 4. Pre-Emphasis and De-Emphasis

- A high-pass network at the transmitter boosts high-frequency message components before FM transmission.
- A complementary low-pass network at the receiver restores the original spectral balance and suppresses high-frequency noise.

```circuit
message = elm.SourceSin()
message.label('Voice m(t)')

elm.Line().at(message).right()
elm.Capacitor().right().label('Series C')
elm.Line().right()
elm.Dot().label('High-frequency output')
elm.Resistor().down().label('Shunt R')
elm.Line().down()
elm.Block().label('Pre-emphasis\nhigh-pass shaping')

received = elm.Block()
received.label('FM receiver output')
elm.Line().at(received).right()
elm.Resistor().right().label('Series R')
elm.Line().right()
elm.Dot().label('Audio output')
elm.Capacitor().down().label('Shunt C')
elm.Line().down()
elm.Block().label('De-emphasis\nlow-pass shaping')
```

## 5. Carson Bandwidth and Deviation Ratio

- Frequency deviation Δf and message bandwidth f_m set the occupied FM bandwidth.
- The deviation ratio β = Δf/f_m separates narrowband and wideband operating regions.

```circuit
message = elm.SourceSin()
message.label('Single-tone m(t), f_m')
deviation = elm.Block()
deviation.label('Δf = k_f A_m')
ratio = elm.Block()
ratio.label('β = Δf/f_m')
carson = elm.Block()
carson.label('BW ≈ 2(Δf+f_m)\n= 2f_m(β+1)')

elm.Line().at(message).right()
elm.Line().at(deviation).right()
elm.Line().right()
elm.Line().at(ratio).right()
elm.Line().right()
elm.Line().at(carson).right()
elm.Line().right()
elm.Block().label('Approx. 98% of FM power')

elm.Block().down().label('β ≪ 1: narrowband FM\nβ > 1: wideband FM')
```
