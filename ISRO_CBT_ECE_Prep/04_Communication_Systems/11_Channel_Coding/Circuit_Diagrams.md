# Channel Coding and Error Control — Circuit Diagrams

## 1. Hamming Encoder and Syndrome Decoder

- The (7,4) encoder converts four information bits into a seven-bit codeword using three parity bits.
- Multiplying the received vector by the parity-check matrix gives a syndrome; a nonzero syndrome identifies a correctable single-bit error.

```circuit
message = elm.SourceSin()
message.label('k=4 information bits')
generator = elm.Block()
generator.label('Generator matrix G\nc=mG')
codeword = elm.Block()
codeword.label('n=7 codeword')
channel = elm.Block()
channel.label('Channel + error e')
received = elm.Block()
received.label('Received r=c+e')
parity = elm.Block()
parity.label('Syndrome s=Hrᵀ')
lookup = elm.Block()
lookup.label('Syndrome lookup\ncorrect one error')
decoder = elm.Block()
decoder.label('ĉ=r+ê')
output = elm.SourceSin()
output.label('Corrected 4 data bits')

elm.Line().at(message).right()
elm.Line().at(generator).right()
elm.Line().right()
elm.Line().at(codeword).right()
elm.Line().right()
elm.Line().at(channel).right()
elm.Line().right()
elm.Line().at(received).right()
elm.Line().right()
elm.Line().at(parity).right()
elm.Line().right()
elm.Line().at(lookup).right()
elm.Line().right()
elm.Line().at(decoder).right()
elm.Line().right()
elm.Line().at(output).right()
```

## 2. Detection and Correction Capability

- Minimum Hamming distance d_min determines how many bit errors a code can detect or correct.
- A (7,4) Hamming code has d_min = 3, so it detects two errors or corrects one error.

```circuit
codewords = elm.SourceSin()
codewords.label('Set of valid codewords')
distance = elm.Block()
distance.label('Compute pairwise Hamming distance')
minimum = elm.Block()
minimum.label('Minimum d_min')
detection = elm.Block()
detection.label('Detect up to d_min−1 errors')
correction = elm.Block()
correction.label('Correct t=floor[(d_min−1)/2]')
example = elm.Block()
example.label('(7,4): d_min=3\ndetect 2, correct 1')

elm.Line().at(codewords).right()
elm.Line().at(distance).right()
elm.Line().right()
elm.Line().at(minimum).right()
elm.Line().right()
elm.Line().at(detection).right()
elm.Line().right()
elm.Line().at(correction).right()
elm.Line().down()
elm.Line().at(example).left()
```

## 3. Stop-and-Wait ARQ

- The receiver checks each block and returns an acknowledgement only when the block is valid.
- A missing or negative acknowledgement causes retransmission until the sender receives confirmation.

```circuit
data = elm.SourceSin()
data.label('Source block')
encoder = elm.Block()
encoder.label('Error-detecting encoder')
transmit = elm.Block()
transmit.label('Transmit block')
decoder = elm.Block()
decoder.label('Check codeword')
decision = elm.Mux()
decision.label('Valid block?')
ack = elm.Block()
ack.label('ACK')
retransmit = elm.Block()
retransmit.label('Timer expires / NACK\nresend block')
sink = elm.SourceSin()
sink.label('Accepted data')

elm.Line().at(data).right()
elm.Line().at(encoder).right()
elm.Line().right()
elm.Line().at(transmit).right()
elm.Line().right()
elm.Line().at(decoder).right()
elm.Line().right()
elm.Line().at(decision).right()
elm.Line().at(decision).right()
elm.Line().at(sink).right()
elm.Line().at(decision).down()
elm.Line().at(retransmit).right()
elm.Line().right()
elm.Line().at(ack).down()
elm.Line().at(transmit).down()
```

## 4. Convolutional Encoding and Viterbi Decoding

- A shift register continuously generates redundant symbols for the current input bit and its memory.
- Viterbi decoding retains the most likely surviving path through the trellis at each time step.

```circuit
input_bit = elm.SourceSin()
input_bit.label('Input bit u_t')
memory = elm.Demux()
memory.label('Shift register\nK−1 memory bits')
encoder = elm.Block()
encoder.label('Convolutional encoder\nrate k/n')
transmit = elm.Block()
transmit.label('Encoded symbol stream')
channel = elm.Block()
channel.label('Noisy channel')
viterbi = elm.Block()
viterbi.label('Viterbi decoder\nsurviving paths')
estimate = elm.Block()
estimate.label('Estimated bit stream')

elm.Line().at(input_bit).right()
elm.Line().at(memory).right()
elm.Line().right()
elm.Line().at(encoder).right()
elm.Line().right()
elm.Line().at(transmit).right()
elm.Line().right()
elm.Line().at(channel).right()
elm.Line().right()
elm.Line().at(viterbi).right()
elm.Line().right()
elm.Line().at(estimate).right()

trellis = elm.Block()
trellis.label('Trellis states grow with 2^(K−1)')
elm.Line().at(trellis).down()
```

## 5. Interleaving with FEC

- The interleaver permutes consecutive coded symbols so a burst error is spread over time.
- The deinterleaver restores order before the FEC decoder, turning a difficult burst into isolated correctable errors.

```circuit
fec_encoder = elm.Block()
fec_encoder.label('FEC encoder')
interleaver = elm.Block()
interleaver.label('Interleaver\ntranspose across time')
burst_channel = elm.Block()
burst_channel.label('Channel with burst error')
deinterleaver = elm.Block()
deinterleaver.label('Deinterleaver')
fec_decoder = elm.Block()
fec_decoder.label('FEC decoder')
output = elm.Block()
output.label('Corrected data')

elm.Line().at(fec_encoder).right()
elm.Line().right()
elm.Line().at(interleaver).right()
elm.Line().right()
elm.Line().at(burst_channel).right()
elm.Line().right()
elm.Line().at(deinterleaver).right()
elm.Line().right()
elm.Line().at(fec_decoder).right()
elm.Line().right()
elm.Line().at(output).right()

elm.Block().down().label('Burst errors → separated errors\nHarder to correct, less burst clustering')
```

## 6. CRC-Encoded Link

- A generator polynomial divides the shifted message and appends the remainder as a CRC field.
- Dividing the received word by the same polynomial yields zero only when no detectable error is present.

```circuit
message = elm.SourceSin()
message.label('Message M(x)')
generator = elm.Block()
generator.label('CRC generator G(x)')
division = elm.Block()
division.label('M(x)x^r mod G(x)')
frame = elm.Block()
frame.label('M(x)x^r + R(x)')
channel = elm.Block()
channel.label('Transmission channel')
check = elm.Block()
check.label('Divide received word by G(x)')
status = elm.Block()
status.label('Remainder 0: accepted\nNonzero: error detected')

elm.Line().at(message).right()
elm.Line().at(generator).right()
elm.Line().at(division).right()
elm.Line().right()
elm.Line().at(frame).right()
elm.Line().right()
elm.Line().at(channel).right()
elm.Line().right()
elm.Line().at(check).right()
elm.Line().right()
elm.Line().at(status).right()
```
