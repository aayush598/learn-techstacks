# Information Theory — Circuit Diagrams

## 1. Entropy and Source-Redundancy Model

- A source symbol distribution produces average information H = −Σpᵢlog₂pᵢ.
- Uniform M-ary sources maximize entropy; nonuniform distributions contain redundancy that coding can remove.

```circuit
source = elm.SourceSin()
source.label('Information source')
alphabet = elm.Demux()
alphabet.label('M symbols with p₁…p_M')
measure = elm.Block()
measure.label('Entropy\nH=−Σpᵢlog₂pᵢ')
maximum = elm.Block()
maximum.label('Maximum entropy\nH_max=log₂M')
redundancy = elm.Block()
redundancy.label('Redundancy\nH_max−H')
encoder = elm.Block()
encoder.label('Source encoder\nremoves redundancy')

elm.Line().at(source).right()
elm.Line().at(alphabet).right()
elm.Line().at(measure).right()
elm.Line().right()
elm.Line().at(maximum).down()
elm.Line().at(measure).down()
elm.Line().at(redundancy).right()
elm.Line().right()
elm.Line().at(encoder).right()
```

## 2. Shannon–Hartley Capacity

- AWGN capacity grows linearly with bandwidth and logarithmically with SNR.
- Reliable rates above C = B log₂(1+SNR) are impossible under the stated channel model.

```circuit
bandwidth = elm.SourceSin()
bandwidth.label('Bandwidth B Hz')
snr = elm.SourceSin()
snr.label('Linear SNR=P_s/P_n')
channel = elm.Block()
channel.label('AWGN channel')
capacity = elm.Block()
capacity.label('Shannon capacity\nC=B log₂(1+SNR)')
reliable = elm.Block()
reliable.label('Reliable operation\nR≤C')
coding = elm.Block()
coding.label('Approach capacity\nwith efficient codes')

elm.Line().at(bandwidth).right()
elm.Line().at(channel).right()
elm.Line().at(snr).down()
elm.Line().at(snr).right()
elm.Line().at(channel).down()
elm.Line().at(channel).right()
elm.Line().at(capacity).right()
elm.Line().right()
elm.Line().at(reliable).right()
elm.Line().right()
elm.Line().at(coding).right()
```

## 3. Binary Symmetric Channel

- A transmitted bit is independently flipped with crossover probability p.
- Each use conveys C = 1 − H₂(p) bits, becoming zero at p = 0.5.

```circuit
source = elm.SourceSin()
source.label('Binary input bit')
transmit = elm.Block()
transmit.label('Transmit 0 or 1')
flip = elm.Mux()
flip.label('Flip with probability p')
output = elm.Block()
output.label('Received bit')
decoder = elm.Block()
decoder.label('Channel decoder')
capacity = elm.Block()
capacity.label('C=1−H₂(p) bits/use')
check = elm.Block()
check.label('p=0: C=1 bit\np=0.5: C=0')

elm.Line().at(source).right()
elm.Line().at(transmit).right()
elm.Line().at(flip).right()
elm.Line().right()
elm.Line().at(output).right()
elm.Line().right()
elm.Line().at(decoder).right()
elm.Line().right()
elm.Line().at(capacity).right()
elm.Line().down()
elm.Line().at(check).left()
```
