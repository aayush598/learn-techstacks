# Noise in Communication Systems — Circuit Diagrams

## 1. Thermal-Noise Source and Resistor

- A resistor at temperature T produces a white Gaussian noise source with available power kTB over bandwidth B.
- The equivalent mean-square noise voltage is 4kTRB; the available noise power itself does not depend on R.

```circuit
noise_source = elm.SourceSin()
noise_source.label('Thermal noise n(t)\nwhite and Gaussian')
resistance = elm.Resistor()
resistance.label('R at temperature T')
bandwidth = elm.Block()
bandwidth.label('Equivalent noise bandwidth B')
noise_power = elm.Block()
noise_power.label('P_n = kTB')
noise_voltage = elm.Block()
noise_voltage.label('V_n,rms² = 4kTRB')
output = elm.Block()
output.label('Receiver input noise')

elm.Line().at(noise_source).right()
elm.Line().at(resistance).right()
elm.Line().right()
elm.Line().at(bandwidth).right()
elm.Line().right()
elm.Line().at(noise_power).right()
elm.Line().at(noise_voltage).right()
elm.Line().at(output).right()
```

## 2. Cascaded Receiver Noise Figure

- Gain and noise factor must be combined in linear units using Friis’ cascade relation.
- Because the first-stage contribution is not divided by preceding gain, a low-noise high-gain LNA should precede later stages.

```circuit
antenna = elm.SourceSin()
antenna.label('Antenna signal + kTB')
lna = elm.Block()
lna.label('Stage 1: LNA\nG₁, F₁')
filter = elm.Block()
filter.label('Band-pass filter\nG₂, F₂')
second = elm.Block()
second.label('Stage 2\nG₂, F₂')
receiver = elm.Block()
receiver.label('Receiver output')

elm.Line().at(antenna).right()
elm.Line().at(lna).right()
elm.Line().right()
elm.Line().at(filter).right()
elm.Line().right()
elm.Line().at(second).right()
elm.Line().right()
elm.Line().at(receiver).right()

cascade = elm.Block()
cascade.label('F_total=F₁+(F₂−1)/G₁+(F₃−1)/(G₁G₂)+…')
elm.Line().at(cascade).down()
```

## 3. Noise Addition

- Powers from uncorrelated noise sources add directly.
- Their RMS voltages combine in quadrature; adding two equal powers gives a 3 dB increase.

```circuit
thermal = elm.SourceSin()
thermal.label('Noise 1 power N₁')
interference = elm.SourceSin()
interference.label('Uncorrelated noise 2 power N₂')
adder = elm.Block()
adder.label('Add uncorrelated powers')
total = elm.Block()
total.label('N_total=N₁+N₂')
rms = elm.Block()
rms.label('V_total=√(V₁²+V₂²)')
equal = elm.Block()
equal.label('Equal sources: +3 dB')

elm.Line().at(thermal).right()
elm.Line().at(adder).right()
elm.Line().at(interference).down()
elm.Line().at(adder).down()
elm.Line().at(adder).right()
elm.Line().right()
elm.Line().at(total).right()
elm.Line().right()
elm.Line().at(rms).right()
elm.Line().down()
elm.Line().at(equal).left()
```

## 4. Receiver Sensitivity

- Sensitivity follows the receiver noise floor kTB plus the required SNR and noise figure.
- In dBm, the 290 K floor starts at −174 dBm/Hz and rises by 10log10B within bandwidth B.

```circuit
noise_floor = elm.Block()
noise_floor.label('Thermal floor\n−174 dBm/Hz at 290 K')
bandwidth = elm.Block()
bandwidth.label('Noise bandwidth\n10log₁₀B dB')
noise_figure = elm.Block()
noise_figure.label('Noise figure\nNF dB')
required_snr = elm.Block()
required_snr.label('Required SNR\nSNR_min dB')
budget = elm.Block()
budget.label('P_min=−174+10log₁₀B+NF+SNR_min')
antenna = elm.Block()
antenna.label('Minimum detectable signal')

elm.Line().at(noise_floor).right()
elm.Line().at(bandwidth).right()
elm.Line().right()
elm.Line().at(noise_figure).right()
elm.Line().right()
elm.Line().at(required_snr).right()
elm.Line().right()
elm.Line().at(budget).right()
elm.Line().right()
elm.Line().at(antenna).right()
```

## 5. Noise Effect in AM and Angle Modulation

- Additive noise perturbs the AM/PM envelope or phase directly and can become an audible error component.
- A limiter suppresses amplitude noise in FM, while pre-emphasis and de-emphasis reduce the high-frequency noise penalty.

```circuit
noise = elm.SourceSin()
noise.label('AWGN n(t)')
am_signal = elm.Block()
am_signal.label('AM signal + noise')
am_detector = elm.Block()
am_detector.label('Envelope detector\namplitude error')
am_output = elm.Block()
am_output.label('Noisy message')

elm.Line().at(noise).right()
elm.Line().at(am_signal).right()
elm.Line().right()
elm.Line().at(am_detector).right()
elm.Line().right()
elm.Line().at(am_output).right()

fm_signal = elm.Block()
fm_signal.label('FM signal + noise')
limiter = elm.Block()
limiter.label('Limiter\nremove amplitude noise')
discriminator = elm.Block()
discriminator.label('Discriminator')
deemphasis = elm.Block()
deemphasis.label('De-emphasis LPF')
fm_output = elm.Block()
fm_output.label('Improved message SNR')

elm.Line().at(fm_signal).right()
elm.Line().at(limiter).right()
elm.Line().right()
elm.Line().at(discriminator).right()
elm.Line().right()
elm.Line().at(deemphasis).right()
elm.Line().right()
elm.Line().at(fm_output).right()
```
