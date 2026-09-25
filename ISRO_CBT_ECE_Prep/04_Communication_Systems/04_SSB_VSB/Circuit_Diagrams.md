# SSB-SC and VSB — Circuit Diagrams

## 1. SSB by the Filter Method

- A balanced modulator first creates DSB-SC containing both sidebands.
- A sharply selective band-pass filter removes the unwanted sideband and any residual carrier.

```circuit
message = elm.SourceSin()
message.label('m(t)')
carrier = elm.SourceSin()
carrier.label('cos(ω_c t)')

elm.Line().at(message).right()
elm.Block().label('Balanced modulator')
elm.Line().at(carrier).down()
elm.Line().right()
elm.Block().label('DSB-SC\nUSB + LSB')
elm.Line().right()
elm.Block().label('BPF above f_c\nreject LSB')
elm.Line().right()
elm.Block().label('USB-SC, BW ≈ f_m')

selector = elm.Demux()
selector.label('Sideband choice')
elm.Line().at(selector).right()
elm.Block().label('Alternatively select LSB')
```

## 2. SSB Phase-Shift Generator

- The direct branch is multiplied by cos(ω_ct), while a 90° Hilbert-transform branch is multiplied by sin(ω_ct).
- Adding or subtracting the branches selects USB or LSB without a very steep filter.

```circuit
message = elm.SourceSin()
message.label('m(t)')
carrier = elm.SourceSin()
carrier.label('cos(ω_c t)')
quadrature = elm.SourceSin()
quadrature.label('sin(ω_c t)')
hilbert = elm.Block()
hilbert.label('Hilbert transform\nm_h(t)')

elm.Line().at(message).right()
elm.Block().label('× cos(ω_c t)')
elm.Line().at(carrier).down()
elm.Line().right()
elm.Block().label('Direct term\nm(t)cos(ω_c t)/2')

elm.Line().at(message).down()
elm.Line().at(hilbert).down()
elm.Block().label('× sin(ω_c t)')
elm.Line().at(quadrature).right()
elm.Line().right()
elm.Block().label('90° term\n∓m_h(t)sin(ω_c t)/2')

elm.Block().label('Subtract for USB\nAdd for LSB')
elm.Line().right()
elm.Demux().label('USB-SC / LSB-SC')
```

## 3. Coherent SSB Demodulator

- SSB-SC contains no transmitted carrier, so the receiver must synthesize a phase-coherent local oscillator.
- Multiplication followed by low-pass filtering leaves a scaled, undistorted message.

```circuit
ssb = elm.SourceSin()
ssb.label('Received SSB-SC')
local = elm.SourceSin()
local.label('Phase-locked local carrier')
mixer = elm.Block()
mixer.label('Multiplier')
lowpass = elm.Block()
lowpass.label('LPF: reject near 2f_c')

elm.Line().at(ssb).right()
elm.Line().at(mixer).right()
elm.Line().at(local).down()
elm.Line().at(mixer).right()
elm.Line().right()
elm.Line().at(lowpass).right()
elm.Line().right()
elm.Block().label('Recovered m(t)/2')

lock = elm.Block()
lock.label('Carrier recovery\nfrequency + phase synchronization')
elm.Line().at(lock).up()
```

## 4. VSB Transmit and Receive Chain

- VSB retains one complete sideband and only the vestige needed for practical filtering.
- A residual carrier supports envelope detection in broadcast systems such as analog television.

```circuit
source = elm.SourceSin()
source.label('Video/TV message')
elm.Line().at(source).right()
elm.Block().label('VSB modulator')
elm.Line().right()
elm.Block().label('BPF\nfull sideband + vestige')
elm.Line().right()
elm.Block().label('Residual carrier')
elm.Line().right()
elm.SourceSin().label('VSB channel')

received = elm.SourceSin()
received.label('Received VSB')
elm.Line().at(received).right()
elm.Block().label('VSB BPF')
elm.Line().right()
elm.Block().label('Envelope detector')
elm.Line().right()
elm.Block().label('Recovered video')

elm.Block().down().label('BW ≈ f_m + vestige\nbetween SSB and DSB')
```

## 5. AM-Family Bandwidth and Detection

- Conventional AM and DSB-SC occupy two message bandwidths; SSB occupies one.
- Envelope detection is simple for carrier-bearing AM and VSB, while suppressed-carrier forms require coherent detection.

```circuit
elm.Block().right().label('AM\ncarrier + 2 sidebands\nBW=2f_m')
elm.Line().right()
elm.Block().right().label('DSB-SC\n2 sidebands\nBW=2f_m')
elm.Line().right()
elm.Block().right().label('SSB-SC\n1 sideband\nBW=f_m')
elm.Line().right()
elm.Block().right().label('VSB\nsideband + vestige\ncarrier may remain')

elm.Block().down().label('Envelope: AM, VSB\nCoherent: DSB-SC, SSB-SC')
```
