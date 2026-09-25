# Sampling Theorem — Circuit Diagrams

## 1. Anti-Aliasing Before Sampling

- The anti-alias low-pass filter removes energy above the signal bandwidth before the sampling switch.
- Sampling above 2f_max then creates nonoverlapping spectral replicas and prevents irreversible aliasing.

```circuit
input_signal = elm.SourceSin()
input_signal.label('Band-limited input plus\nout-of-band components')
anti_alias = elm.Block()
anti_alias.label('Anti-alias LPF\ncutoff f_max')
sampler = elm.Mux()
sampler.label('Clocked sampler')
clock = elm.SourceSin()
clock.label('f_s > 2f_max')
spectrum = elm.Block()
spectrum.label('Sampled spectrum\ncopies at kf_s')

elm.Line().at(input_signal).right()
elm.Line().at(anti_alias).right()
elm.Line().right()
elm.Line().at(sampler).right()
elm.Line().at(clock).down()
elm.Line().at(sampler).down()
elm.Line().right()
elm.Line().at(spectrum).right()
```

## 2. Nyquist-Rate Safety Margin

- The theoretical minimum sampling frequency is 2f_max.
- Real filters require a guard transition band, so practical designs commonly use about 2.2f_max to 2.5f_max.

```circuit
message = elm.SourceSin()
message.label('Highest message tone f_max')
limit = elm.Block()
limit.label('Band-limit below f_s/2')
rate = elm.Block()
rate.label('Nyquist rate\nf_s,min=2f_max')
sampler = elm.Mux()
sampler.label('Sample-and-hold')
clock = elm.SourceSin()
clock.label('Practical f_s\n2.2 to 2.5 times f_max')
aliasing = elm.Block()
aliasing.label('No spectral overlap')

elm.Line().at(message).right()
elm.Line().at(limit).right()
elm.Line().right()
elm.Line().at(rate).right()
elm.Line().right()
elm.Line().at(sampler).right()
elm.Line().at(clock).down()
elm.Line().at(aliasing).right()
```

## 3. Aliasing and Spectral Folding

- When f_s < 2f_max, adjacent spectral replicas overlap and high frequencies appear at false low frequencies.
- Once aliased, no later low-pass reconstruction filter can identify the original components.

```circuit
tone = elm.SourceSin()
tone.label('Input tone f')
sampler = elm.Mux()
sampler.label('Undersampler f_s')
clock = elm.SourceSin()
clock.label('f_s < 2f')
folding = elm.Block()
folding.label('Spectral replicas overlap')
alias = elm.Block()
alias.label('f_alias=|f−kf_s|')
output = elm.Block()
output.label('False low-frequency component')
irreversible = elm.Block()
irreversible.label('LPF cannot undo aliasing')

elm.Line().at(tone).right()
elm.Line().at(sampler).right()
elm.Line().at(clock).down()
elm.Line().at(folding).right()
elm.Line().right()
elm.Line().at(alias).right()
elm.Line().right()
elm.Line().at(output).right()
elm.Line().right()
elm.Line().at(irreversible).right()
```

## 4. Sample-and-Hold Reconstruction

- The zero-order hold stretches each sample across one sampling interval, introducing a sinc-shaped droop.
- A reconstruction low-pass filter removes the sampling images and, ideally, applies gain T for perfect recovery.

```circuit
samples = elm.SourceSin()
samples.label('Pulse samples\nx(nT)')
hold = elm.Block()
hold.label('Zero-order hold\n(1−e⁻ˢᵀ)/s')
reconstruction = elm.Block()
reconstruction.label('Reconstruction LPF\ncutoff f_max')
gain = elm.Block()
gain.label('Ideal gain T\nat |f|<f_max')
output = elm.SourceSin()
output.label('Reconstructed x(t)')

elm.Line().at(samples).right()
elm.Line().at(hold).right()
elm.Line().right()
elm.Line().at(reconstruction).right()
elm.Line().right()
elm.Line().at(gain).right()
elm.Line().right()
elm.Line().at(output).right()

elm.Capacitor().down().label('Practical hold capacitor')
```

## 5. Ideal Sinc Reconstruction

- Perfect interpolation is the sum of shifted sinc functions weighted by the sample values.
- The equivalent ideal low-pass filter passes only the original baseband around DC.

```circuit
sample_values = elm.SourceSin()
sample_values.label('x(nT)')
delays = elm.Demux()
delays.label('Shifted copies nT')
sinc = elm.Block()
sinc.label('Weight each copy by sinc[(t−nT)/T]')
summer = elm.Block()
summer.label('Sum over all n')
ideal_filter = elm.Block()
ideal_filter.label('Ideal LPF\nH(f)=T for |f|<f_max')
output = elm.SourceSin()
output.label('Exact bandlimited signal')

elm.Line().at(sample_values).right()
elm.Line().at(delays).right()
elm.Line().right()
elm.Line().at(sinc).right()
elm.Line().right()
elm.Line().at(summer).right()
elm.Line().right()
elm.Line().at(ideal_filter).right()
elm.Line().right()
elm.Line().at(output).right()
```
