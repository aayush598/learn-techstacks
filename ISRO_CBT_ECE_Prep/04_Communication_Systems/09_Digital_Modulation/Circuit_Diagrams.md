# Digital Modulation — Circuit Diagrams

## 1. ASK / On-Off Keying Transmitter

- Binary data selects whether the carrier is present or absent.
- OOK is the two-level ASK special case in which amplitude levels are 0 and A_c.

```circuit
bits = elm.SourceSin()
bits.label('Binary data 0 or 1')
carrier = elm.SourceSin()
carrier.label('cos(2πf_ct)')
keyer = elm.Mux()
keyer.label('ASK switch / multiplier')
output = elm.Block()
output.label('OOK: 0→absent\n1→A_c cos(2πf_ct)')

elm.Line().at(bits).right()
elm.Line().at(keyer).right()
elm.Line().at(carrier).down()
elm.Line().at(keyer).down()
elm.Line().at(keyer).right()
elm.Line().right()
elm.Line().at(output).right()
```

## 2. FSK Transmitter

- The data input selects one of two local oscillators.
- Coherent or noncoherent demodulation at the receiver uses the known frequency alternatives.

```circuit
bits = elm.SourceSin()
bits.label('Binary data')
tone_a = elm.SourceSin()
tone_a.label('cos(2πf₁t)')
tone_b = elm.SourceSin()
tone_b.label('cos(2πf₂t)')
switch = elm.Mux()
switch.label('Frequency selector')
output = elm.Block()
output.label('FSK: 0→f₂, 1→f₁\nBW=2Δf+2R_b')

elm.Line().at(bits).right()
elm.Line().at(switch).right()
elm.Line().at(tone_a).down()
elm.Line().at(tone_a).right()
elm.Line().at(tone_b).down()
elm.Line().at(tone_b).right()
elm.Line().at(switch).right()
elm.Line().right()
elm.Line().at(output).right()
```

## 3. PSK / BPSK Transmitter

- BPSK changes only carrier phase; its constellation consists of two antipodal points and has constant envelope.
- For equal priors in AWGN, the BER is Q(√(2E_b/N₀)).

```circuit
bits = elm.SourceSin()
bits.label('Binary data')
carrier = elm.SourceSin()
carrier.label('cos(2πf_ct)')
inverted = elm.Block()
inverted.label('180° phase path\n−cos(2πf_ct)')
phase_switch = elm.Mux()
phase_switch.label('BPSK phase selector')
constellation = elm.Demux()
constellation.label('0 or π')
output = elm.Block()
output.label('BPSK\nP_b=Q(√(2E_b/N₀))')

elm.Line().at(bits).right()
elm.Line().at(phase_switch).right()
elm.Line().at(carrier).down()
elm.Line().at(phase_switch).down()
elm.Line().at(inverted).down()
elm.Line().at(phase_switch).down()
elm.Line().at(phase_switch).right()
elm.Line().right()
elm.Line().at(constellation).right()
elm.Line().right()
elm.Line().at(output).right()
```

## 4. QAM Transmitter with I and Q Branches

- Two parallel symbol streams drive cosine and sine carriers.
- Their scaled products are added to form M-QAM; 16-QAM carries four bits per symbol but requires higher SNR.

```circuit
serial_bits = elm.SourceSin()
serial_bits.label('Input bit stream')
splitter = elm.Demux()
splitter.label('Split into I and Q')
i_symbols = elm.Block()
i_symbols.label('Amplitude mapper\nI_n')
q_symbols = elm.Block()
q_symbols.label('Amplitude mapper\nQ_n')
cosine = elm.SourceSin()
cosine.label('cos(2πf_ct)')
sine = elm.SourceSin()
sine.label('sin(2πf_ct)')
i_branch = elm.Block()
i_branch.label('I_n × cos(2πf_ct)')
q_branch = elm.Block()
q_branch.label('Q_n × sin(2πf_ct)')
adder = elm.Block()
adder.label('Add I and Q branches')
output = elm.Block()
output.label('M-QAM passband signal\nR_b=R_s log₂M')

elm.Line().at(serial_bits).right()
elm.Line().at(splitter).right()
elm.Line().at(i_symbols).down()
elm.Line().at(i_branch).right()
elm.Line().at(cosine).down()
elm.Line().at(i_branch).down()
elm.Line().at(i_branch).right()
elm.Line().at(q_symbols).down()
elm.Line().at(q_branch).right()
elm.Line().at(sine).down()
elm.Line().at(q_branch).down()
elm.Line().at(q_branch).right()
elm.Line().at(adder).right()
elm.Line().right()
elm.Line().at(output).right()
```

## 5. Matched-Filter Symbol Detection and BER

- The matched filter maximizes SNR for known symbols in white Gaussian noise.
- A threshold device maps the sampled statistic to a bit, and the error counter divides errors by transmitted bits.

```circuit
received = elm.SourceSin()
received.label('Received waveform')
matched = elm.Block()
matched.label('Matched filter\nh(t)=s(T−t)')
sample = elm.Block()
sample.label('Sample at t=T')
decision = elm.Opamp()
decision.label('Threshold comparator')
bits = elm.Block()
bits.label('Recovered bit stream')
compare = elm.XorGate()
compare.label('Compare with transmitted bits')
counter = elm.Block()
counter.label('Error counter')
ber = elm.Block()
ber.label('BER=N_errors/N_bits')

elm.Line().at(received).right()
elm.Line().at(matched).right()
elm.Line().right()
elm.Line().at(sample).right()
elm.Line().right()
elm.Line().at(decision).right()
elm.Line().right()
elm.Line().at(bits).right()
elm.Line().right()
elm.Line().at(compare).right()
elm.Line().right()
elm.Line().at(counter).right()
elm.Line().right()
elm.Line().at(ber).right()
```
