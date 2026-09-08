# Communication Systems - Memory Tricks

## Modulation Index Mnemonic
- **mu = (Vmax - Vmin)/(Vmax + Vmin)**
- "**Max minus Min over Max plus Min**" - Both almays together

## AM Power Memory
- **Ptotal = Pc(1 + mu^2/2)**
- "**Half the square of mu multiplied by Pc**"
- At mu = 1: Total = 1.5*Pc (sidebands add 50%)

## PCM SQNR Memory
- **6.02n + 1.76 dB**
- Each extra bit = **6 dB** improvement (6 dB per bit rule)
- 8-bit = 50 dB (approximately), 12-bit = 74 dB

## Shannon Capacity Mnemonic
- **C = B log2(1 + SNR)**
- "**Capacity = Bandwidth times log of (1 + SNR)**"
- Doubling bandwidth doubles capacity (if SNR constant)
- Doubling SNR adds 1 bit/symbol (only 1 bit, not linear)

## Detection Methods
- **AM uses envelope detector** - "**Simple signal, simple receiver**"
- **DSB-SC/SSB uses coherent detector** - "**Suppressed carrier needs re-carrier**"

## Polarization of Signals
- AM and FM are analog methods
- BPSK, QPSK, QAM are digital (symbol-based)
- FSK uses frequency to represent bits

## Huffman Coding Memory
- **Most probable symbol gets SHORTEST code**
- "**Frequent gets short, rare gets long**"
- Average length is between H and H+1 bits

## Digital Modulation Error Probability
- **BPSK = Q(sqrt(2Eb/N0))** - "**B for 2**"
- **QPSK = same as BPSK** (performance identical, uses 2 bits)
- **FSK = Q(sqrt(Eb/N0))** - "**F for 1 (fall short)**"
