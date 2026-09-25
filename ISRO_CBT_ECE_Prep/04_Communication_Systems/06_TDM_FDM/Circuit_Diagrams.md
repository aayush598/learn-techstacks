# TDM and FDM Multiplexing — Circuit Diagrams

## 1. Frequency-Division Multiplexing Transmitter

- Each baseband channel is modulated onto a different carrier and band-limited before summation.
- Nonoverlapping passbands and guard bands protect the channels from adjacent-channel crosstalk.

```circuit
channel_a = elm.SourceSin()
channel_a.label('Analog A')
channel_b = elm.SourceSin()
channel_b.label('Analog B')
channel_c = elm.SourceSin()
channel_c.label('Analog C')
mod_a = elm.Block()
mod_a.label('Modulator to f₁\nBPF')
mod_b = elm.Block()
mod_b.label('Modulator to f₂\nBPF')
mod_c = elm.Block()
mod_c.label('Modulator to f₃\nBPF')
spectrum = elm.Demux()
spectrum.label('Guard bands\nbetween channels')
adder = elm.Block()
adder.label('Frequency-domain summer')
output = elm.Block()
output.label('FDM composite\nN B_sig+(N−1)B_guard')

elm.Line().at(channel_a).right()
elm.Line().at(mod_a).right()
elm.Line().right()
elm.Line().at(spectrum).right()
elm.Line().right()
elm.Line().at(adder).right()
elm.Line().right()
elm.Line().at(output).right()

elm.Line().at(channel_b).down()
elm.Line().at(mod_b).down()
elm.Line().at(mod_b).right()
elm.Line().at(channel_c).down()
elm.Line().at(mod_c).down()
elm.Line().at(mod_c).right()
```

## 2. FDM Receiver Channel Separation

- A bank of tuned band-pass filters selects each assigned channel and rejects the other transmissions.
- Demodulation restores the original baseband signal for that channel.

```circuit
composite = elm.SourceSin()
composite.label('FDM input')
filter_bank = elm.Demux()
filter_bank.label('BPF bank')
channel_a = elm.Block()
channel_a.label('BPF around f₁')
channel_b = elm.Block()
channel_b.label('BPF around f₂')
channel_c = elm.Block()
channel_c.label('BPF around f₃')
demod_a = elm.Block()
demod_a.label('Demodulator')
demod_b = elm.Block()
demod_b.label('Demodulator')
demod_c = elm.Block()
demod_c.label('Demodulator')
outputs = elm.Mux()
outputs.label('Recovered channels')

elm.Line().at(composite).right()
elm.Line().at(filter_bank).right()
elm.Line().at(channel_a).down()
elm.Line().at(demod_a).right()
elm.Line().right()
elm.Line().at(outputs).right()
elm.Line().at(channel_b).down()
elm.Line().at(demod_b).right()
elm.Line().at(channel_c).down()
elm.Line().at(demod_c).right()
```

## 3. Synchronous TDM Frame

- A multiplexer assigns each equal-rate input a fixed slot in every recurring frame.
- A synchronized demultiplexer samples the same slot sequence and routes each slot to its destination.

```circuit
a = elm.SourceSin()
a.label('Channel A 64 kb/s')
b = elm.SourceSin()
b.label('Channel B 64 kb/s')
c = elm.SourceSin()
c.label('Channel C 64 kb/s')
clock = elm.SourceSin()
clock.label('Frame clock 8 kHz')
mux = elm.Mux()
mux.label('Synchronous TDM\nA,B,C slots')
stream = elm.Block()
stream.label('TDM stream\nN·R_channel')
demux = elm.Demux()
demux.label('Frame-synchronized\nTDM demux')

elm.Line().at(a).right()
elm.Line().at(mux).right()
elm.Line().at(clock).down()
elm.Line().at(b).down()
elm.Line().at(b).right()
elm.Line().at(c).down()
elm.Line().at(c).right()
elm.Line().at(mux).right()
elm.Line().right()
elm.Line().at(stream).right()
elm.Line().right()
elm.Line().at(demux).right()
elm.Line().right()
elm.Mux().label('Recover A,B,C')
```

## 4. T1 and E1 Frame Formats

- A T1 frame carries 24 voice words plus one framing bit; at 8000 frames/s its rate is 1.544 Mb/s.
- An E1 frame has 32 octets including synchronization and signaling slots, giving 2.048 Mb/s.

```circuit
t1 = elm.Block()
t1.label('T1 frame\n24×8 voice + 1 framing')
t1_clock = elm.SourceSin()
t1_clock.label('8000 frames/s')
t1_rate = elm.Block()
t1_rate.label('193×8000\n1.544 Mb/s')
t1_channel = elm.Block()
t1_channel.label('Voice channel\n8×8000 = 64 kb/s')

elm.Line().at(t1).right()
elm.Line().right()
elm.Line().at(t1_rate).right()
elm.Line().right()
elm.Line().at(t1_channel).right()
elm.Line().at(t1_clock).down()

e1 = elm.Block()
e1.label('E1 frame\n32×8 octets')
e1_clock = elm.SourceSin()
e1_clock.label('8000 frames/s')
e1_rate = elm.Block()
e1_rate.label('256×8000\n2.048 Mb/s')
e1_slots = elm.Block()
e1_slots.label('Slot 0 sync\nSlot 16 signaling\n30 traffic channels')

elm.Line().at(e1).right()
elm.Line().right()
elm.Line().at(e1_rate).right()
elm.Line().right()
elm.Line().at(e1_slots).right()
elm.Line().at(e1_clock).down()
```

## 5. Statistical TDM and Multiplexing Choice

- Statistical TDM stores bursty packets temporarily and adds addresses so slots can be assigned on demand.
- FDM shares frequency simultaneously, whereas synchronous TDM shares recurring time slots.

```circuit
packet_a = elm.SourceSin()
packet_a.label('Bursty input A')
packet_b = elm.SourceSin()
packet_b.label('Bursty input B')
buffer = elm.Block()
buffer.label('Queue and buffer')
address = elm.Block()
address.label('Add channel address')
mux = elm.Mux()
mux.label('Dynamic slot assignment')
demux = elm.Demux()
demux.label('Read address and route')

elm.Line().at(packet_a).right()
elm.Line().at(buffer).right()
elm.Line().at(packet_b).down()
elm.Line().at(packet_b).right()
elm.Line().at(buffer).right()
elm.Line().at(address).right()
elm.Line().right()
elm.Line().at(mux).right()
elm.Line().right()
elm.Line().at(demux).right()
elm.Line().right()
elm.Block().label('Statistical TDM\nhigher utilization')

elm.Block().down().label('FDM: simultaneous, frequency bands + guard\nTDM: sequential, clock and frame synchronization')
```
