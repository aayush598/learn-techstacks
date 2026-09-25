# AM Modulation — Circuit Diagrams

## 1. Conventional AM Transmitter

- The message controls carrier amplitude while the carrier frequency remains fixed.
- For μ ≤ 1, the multiplier and DC bias produce s(t) = A_c[1 + μm(t)]cos(2πf_ct).

```circuit
message = elm.SourceSin()
message.label('m(t), A_m')
carrier = elm.SourceSin()
carrier.label('cos(2πf_c t)')
bias = elm.Block()
bias.label('1')
scaling = elm.Block()
scaling.label('Scale A_c μ')

elm.Line().at(message).right()
elm.Line().at(scaling).down()
elm.Block().label('Modulating product\nA_c μm(t)cos(2πf_ct)')
elm.Line().right()
elm.Block().label('Add DC carrier\nA_c[1+μm(t)]cos(2πf_ct)')
elm.Line().right()
elm.Block().label('AM transmitter')

elm.Line().at(carrier).up()
elm.Line().at(bias).up()
```

## 2. DSB-SC Generation

- A balanced modulator multiplies the message directly by the carrier and suppresses the separate carrier component.
- The product contains only the upper and lower sidebands and requires coherent detection.

```circuit
message = elm.SourceSin()
message.label('m(t)')
carrier = elm.SourceSin()
carrier.label('cos(2πf_c t)')

elm.Line().at(message).right()
elm.Block().label('Balanced multiplier')
elm.Line().at(carrier).down()
elm.Line().right()
elm.Block().label('Carrier component\nsuppressed')
elm.Line().right()
elm.Block().label('DSB-SC\nA_c m(t)cos(2πf_ct)')

bands = elm.Demux()
bands.label('Sideband outputs')
elm.Line().at(bands).right()
elm.Block().label('USB: f_c+f_m')
elm.Block().down().label('LSB: f_c−f_m')
```

## 3. Coherent Detection for DSB-SC

- A phase-locked local carrier multiplies the received suppressed-carrier signal.
- A low-pass filter removes components near 2f_c and recovers a scaled message.

```circuit
received = elm.SourceSin()
received.label('DSB-SC signal')
local = elm.SourceSin()
local.label('Coherent local carrier')

elm.Line().at(received).right()
elm.Block().label('Multiplier')
elm.Line().at(local).down()
elm.Line().right()
elm.Block().label('LPF around f_m')
elm.Line().right()
elm.Block().label('Recovered m(t)/2')

lock = elm.Block()
lock.label('Carrier recovery\nfrequency and phase lock')
elm.Line().at(lock).up()
```

## 4. Envelope Detector for Conventional AM

- The diode rectifies the RF waveform; the resistor and capacitor follow the slow envelope.
- The time constant must let the capacitor discharge between carrier cycles while still tracking m(t).

```circuit
elm.SourceSin().right().label('AM RF input')
elm.Line().right()
elm.Diode().right().label('D')
elm.Line().right()
elm.Resistor().right().label('R')
elm.Line().right()
elm.Dot().label('Envelope output')

elm.Capacitor().down().label('C')
elm.Line().down()
elm.Dot()

elm.Line().right().label('Low-pass action\n1/ω_c ≪ RC ≪ 1/ω_m')
```

## 5. AM Power Allocation

- With μ = 1, one third of transmitted power is in useful sidebands and two thirds remains in the carrier.
- DSB-SC removes that carrier power, so all transmitted power is sideband power.

```circuit
carrier_source = elm.Block()
carrier_source.label('Carrier power P_c')
usb_source = elm.Block()
usb_source.label('USB = P_c μ²/4')
lsb_source = elm.Block()
lsb_source.label('LSB = P_c μ²/4')

elm.Line().at(carrier_source).right()
elm.Block().label('AM adder')
elm.Line().right()
elm.Block().label('P_total = P_c(1+μ²/2)')

elm.Line().at(usb_source).down()
elm.Line().at(lsb_source).down()
elm.Block().label('Useful sidebands\nP_sb = P_c μ²/2')

elm.Line().right()
elm.Block().label('Suppress carrier')
elm.Line().right()
elm.Block().label('DSB-SC: 100% in sidebands')
```
