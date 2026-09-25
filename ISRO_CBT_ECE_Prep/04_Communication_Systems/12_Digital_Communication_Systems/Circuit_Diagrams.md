# Digital Communication Systems — Circuit Diagrams

## 1. Complete Digital Communication Link

- Source coding removes redundancy, channel coding adds controlled redundancy, and the modulator maps bits to waveforms.
- At the receiver the inverse stages recover data despite channel noise, attenuation, and distortion.

```circuit
source = elm.SourceSin()
source.label('User source')
source_encoder = elm.Block()
source_encoder.label('Source encoder\ncompression')
channel_encoder = elm.Block()
channel_encoder.label('Channel encoder\nFEC redundancy')
modulator = elm.Block()
modulator.label('Modulator')
transmitter = elm.Block()
transmitter.label('TX filter and power amplifier')
channel = elm.Block()
channel.label('Channel\nnoise + distortion')
receiver = elm.Block()
receiver.label('RX filter and front end')
demodulator = elm.Block()
demodulator.label('Demodulator\ndecision statistics')
channel_decoder = elm.Block()
channel_decoder.label('Channel decoder\nFEC')
source_decoder = elm.Block()
source_decoder.label('Source decoder\ndecompression')
sink = elm.SourceSin()
sink.label('User destination')

elm.Line().at(source).right()
elm.Line().at(source_encoder).right()
elm.Line().right()
elm.Line().at(channel_encoder).right()
elm.Line().right()
elm.Line().at(modulator).right()
elm.Line().right()
elm.Line().at(transmitter).right()
elm.Line().right()
elm.Line().at(channel).right()
elm.Line().right()
elm.Line().at(receiver).right()
elm.Line().right()
elm.Line().at(demodulator).right()
elm.Line().right()
elm.Line().at(channel_decoder).right()
elm.Line().right()
elm.Line().at(source_decoder).right()
elm.Line().right()
elm.Line().at(sink).right()
```

## 2. Matched-Filter and MAP Receiver

- The matched filter provides the maximum-SNR statistic for each known candidate symbol.
- A likelihood or posterior-probability comparator makes the final symbol decision; equal priors make MAP equivalent to ML.

```circuit
received = elm.SourceSin()
received.label('Received r(t)')
filter = elm.Block()
filter.label('Matched filter\nh(t)=s(T−t)')
sample = elm.Block()
sample.label('Sample statistic y(T)')
likelihood = elm.Demux()
likelihood.label('Likelihoods\nP(r|s₀), P(r|s₁)')
prior = elm.Block()
prior.label('Multiply by priors P(sᵢ)')
map = elm.Opamp()
map.label('MAP comparator')
decision = elm.Mux()
decision.label('Choose symbol 0 or 1')
output = elm.Block()
output.label('Decoded bit')

elm.Line().at(received).right()
elm.Line().at(filter).right()
elm.Line().right()
elm.Line().at(sample).right()
elm.Line().right()
elm.Line().at(likelihood).right()
elm.Line().right()
elm.Line().at(prior).right()
elm.Line().right()
elm.Line().at(map).right()
elm.Line().right()
elm.Line().at(decision).right()
elm.Line().right()
elm.Line().at(output).right()
```

## 3. Multiple-Access Families

- FDMA separates users by frequency, TDMA by time, CDMA by code, and OFDMA by frequency-time resources.
- The receiver must identify and separate the selected user’s resource before decoding its data.

```circuit
users = elm.SourceSin()
users.label('Multiple user signals')
fdma = elm.Block()
fdma.label('FDMA\ndistinct frequency bands')
tdma = elm.Block()
tdma.label('TDMA\nrecurring time slots')
cdma = elm.Block()
cdma.label('CDMA\northogonal spreading codes')
ofdma = elm.Block()
ofdma.label('OFDMA\northogonal subcarriers + symbols')
channel = elm.Block()
channel.label('Shared channel')
separator = elm.Demux()
separator.label('Resource separation')
selected = elm.Block()
selected.label('Selected user baseband')
decoder = elm.Block()
decoder.label('User decoder')

elm.Line().at(users).right()
elm.Line().at(fdma).right()
elm.Line().at(tdma).down()
elm.Line().at(cdma).down()
elm.Line().at(ofdma).down()
elm.Line().at(channel).right()
elm.Line().right()
elm.Line().at(separator).right()
elm.Line().right()
elm.Line().at(selected).right()
elm.Line().right()
elm.Line().at(decoder).right()
```

## 4. Power–Bandwidth–Complexity Trade-off

- BPSK and QPSK use little bandwidth per bit and work at lower SNR, but carry fewer bits per symbol.
- Higher-order QAM increases spectral efficiency while requiring greater Eb/N0 and a more complex receiver.

```circuit
bpsk = elm.Block()
bpsk.label('BPSK\n1 bit/symbol\nrobust power efficiency')
qpsk = elm.Block()
qpsk.label('QPSK\n2 bits/symbol\nrobust')
qam = elm.Block()
qam.label('Higher-order QAM\nmany bits/symbol\nhigher Eb/N0 needed')
system = elm.Block()
system.label('Design frontier')
limit = elm.Block()
limit.label('Shannon limit\nC≤B log₂(1+SNR)')

elm.Line().at(bpsk).right()
elm.Line().right()
elm.Line().at(qpsk).right()
elm.Line().right()
elm.Line().at(qam).right()
elm.Line().right()
elm.Line().at(system).right()
elm.Line().right()
elm.Line().at(limit).right()
```

## 5. Telephone PCM Link Example

- A 4 kHz voice signal is sampled at 8 kHz and encoded with eight bits per sample.
- The resulting 64 kb/s stream demonstrates the connection between bandwidth, source coding, and transport.

```circuit
voice = elm.SourceSin()
voice.label('Voice bandwidth\n0–4 kHz')
sampler = elm.Block()
sampler.label('Sample at f_s=8 kHz')
quantizer = elm.Block()
quantizer.label('8-bit quantizer')
pcm = elm.Block()
pcm.label('PCM rate\nR_b=8×8000=64 kb/s')
codec = elm.Block()
codec.label('Telephone codec / channel')
decoder = elm.Block()
decoder.label('Decoder + reconstruction LPF')
output = elm.SourceSin()
output.label('Recovered voice')

elm.Line().at(voice).right()
elm.Line().at(sampler).right()
elm.Line().right()
elm.Line().at(quantizer).right()
elm.Line().right()
elm.Line().at(pcm).right()
elm.Line().right()
elm.Line().at(codec).right()
elm.Line().right()
elm.Line().at(decoder).right()
elm.Line().right()
elm.Line().at(output).right()
```
