# Binary Communication — Circuit Diagrams

## 1. Correlator Receiver

- Multiply the received waveform by each known candidate waveform and integrate over one symbol interval.
- Compare the resulting correlations to a threshold; for equal priors this is equivalent to matched-filter ML detection.

```circuit
received = elm.SourceSin()
received.label('Received r(t)')
reference = elm.SourceSin()
reference.label('Reference s₁(t)')
multiply = elm.Block()
multiply.label('Multiplier')
integrate = elm.Block()
integrate.label('Integrate 0 to T')
sample = elm.Block()
sample.label('Sample y(T)')
threshold = elm.Opamp()
threshold.label('Compare with threshold')
decision = elm.Mux()
decision.label('Decide s₀ or s₁')
output = elm.Block()
output.label('Recovered bit')

elm.Line().at(received).right()
elm.Line().at(multiply).right()
elm.Line().at(reference).down()
elm.Line().at(multiply).down()
elm.Line().at(multiply).right()
elm.Line().right()
elm.Line().at(integrate).right()
elm.Line().right()
elm.Line().at(sample).right()
elm.Line().right()
elm.Line().at(threshold).right()
elm.Line().right()
elm.Line().at(decision).right()
elm.Line().right()
elm.Line().at(output).right()
```

## 2. Matched-Filter Receiver

- The known pulse is time-reversed and delayed to form h(t) = s(T−t).
- Sampling its output at t = T maximizes output SNR to 2E/N0 in white Gaussian noise.

```circuit
received = elm.SourceSin()
received.label('Received r(t)+n(t)')
known_pulse = elm.Block()
known_pulse.label('Known pulse s(t)')
reverse = elm.Block()
reverse.label('Time reverse and delay\nh(t)=s(T−t)')
filter = elm.Block()
filter.label('Matched filter')
sample = elm.Block()
sample.label('Sample at t=T')
snr = elm.Block()
snr.label('Maximum SNR_out=2E/N₀')
decision = elm.Block()
decision.label('Threshold decision')

elm.Line().at(received).right()
elm.Line().at(filter).right()
elm.Line().right()
elm.Line().at(sample).right()
elm.Line().right()
elm.Line().at(decision).right()

elm.Line().at(known_pulse).right()
elm.Line().at(reverse).right()
elm.Line().at(reverse).right()
elm.Line().at(filter).down()
elm.Line().at(snr).down()
elm.Line().at(decision).down()
```

## 3. Antipodal and Orthogonal Binary Signaling

- Antipodal BPSK points lie at opposite ends of one axis and have distance 2√E_b.
- Orthogonal FSK points are perpendicular with distance √(2E_b), so antipodal signaling gains 3 dB at equal bit energy.

```circuit
antipodal = elm.SourceSin()
antipodal.label('BPSK\ns₁=+√E_b, s₀=−√E_b')
orthogonal = elm.SourceSin()
orthogonal.label('FSK\northogonal basis points')
distance = elm.Block()
distance.label('Compare minimum distance')
antipodal_metric = elm.Block()
antipodal_metric.label('d_min²=4E_b\nP_b=Q(√(2E_b/N₀))')
orthogonal_metric = elm.Block()
orthogonal_metric.label('d_min²=2E_b\nP_b=Q(√(E_b/N₀))')
verdict = elm.Block()
verdict.label('Antipodal is 3 dB better\nat equal Eb')

elm.Line().at(antipodal).right()
elm.Line().at(distance).right()
elm.Line().at(orthogonal).down()
elm.Line().at(orthogonal).right()
elm.Line().at(distance).down()
elm.Line().at(distance).right()
elm.Line().right()
elm.Line().at(antipodal_metric).right()
elm.Line().at(orthogonal_metric).down()
elm.Line().at(verdict).right()
```

## 4. ML, MAP, and Decision Threshold

- ML compares likelihoods P(r|s), whereas MAP includes the prior P(s).
- For symmetric binary signals the equal-prior ML threshold is the midpoint; unequal priors or unequal costs shift it.

```circuit
statistic = elm.SourceSin()
statistic.label('Test statistic y')
likelihoods = elm.Demux()
likelihoods.label('P(r|s₀), P(r|s₁)')
priors = elm.Block()
priors.label('Multiply by P(s₀), P(s₁)')
map = elm.Opamp()
map.label('MAP comparator')
equal = elm.Block()
equal.label('Equal priors → ML=MAP\nγ=(μ₀+μ₁)/2')
unequal = elm.Block()
unequal.label('Unequal priors\nthreshold shifts')
decision = elm.Mux()
decision.label('Estimate symbol')

elm.Line().at(statistic).right()
elm.Line().at(likelihoods).right()
elm.Line().right()
elm.Line().at(priors).right()
elm.Line().right()
elm.Line().at(map).right()
elm.Line().right()
elm.Line().at(decision).right()
elm.Line().at(map).down()
elm.Line().at(equal).right()
elm.Line().at(unequal).down()
elm.Line().at(decision).down()
```

## 5. Binary Error-Rate Test Loop

- Transmit known antipodal symbols through AWGN and pass the received signal through a matched filter.
- Count threshold-crossing mistakes to estimate the error probability for the chosen Eb/N0.

```circuit
bits = elm.SourceSin()
bits.label('Known binary data')
modulator = elm.Block()
modulator.label('BPSK modulator')
noise = elm.SourceSin()
noise.label('AWGN n(t), two-sided PSD N₀/2')
adder = elm.Block()
adder.label('Add signal and noise')
matched = elm.Block()
matched.label('Matched filter')
sampler = elm.Block()
sampler.label('Sample at T')
comparator = elm.XorGate()
comparator.label('Compare decision with reference')
counter = elm.Block()
counter.label('Count false decisions')
ber = elm.Block()
ber.label('Estimate P_b at selected Eb/N₀')

elm.Line().at(bits).right()
elm.Line().at(modulator).right()
elm.Line().right()
elm.Line().at(adder).right()
elm.Line().at(noise).down()
elm.Line().at(noise).right()
elm.Line().at(adder).down()
elm.Line().at(adder).right()
elm.Line().right()
elm.Line().at(matched).right()
elm.Line().right()
elm.Line().at(sampler).right()
elm.Line().right()
elm.Line().at(comparator).right()
elm.Line().at(bits).down()
elm.Line().at(bits).right()
elm.Line().at(comparator).down()
elm.Line().at(comparator).right()
elm.Line().right()
elm.Line().at(counter).right()
elm.Line().right()
elm.Line().at(ber).right()
```
