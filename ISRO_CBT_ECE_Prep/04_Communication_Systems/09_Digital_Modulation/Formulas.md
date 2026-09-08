# Digital Modulation - Formulas

## Bandwidth
```
BPSK: BW = 2*Rb
QPSK: BW = Rb (bit rate doubled per symbol)
FSK: BW = 2*delta_f + 2*Rb
M-ary PSK: BW = 2*Rb/log2(M)
M-ary QAM: BW = 2*Rb/log2(M)
```

## Bit Rate, Symbol Rate
```
Rb = Rs*log2(M)
Rs = symbol rate = bit rate / bits per symbol
For 16-QAM: Rs = Rb/4, for 8-PSK: Rs = Rb/3
```

## Error Probability (AWGN)
```
BPSK / QPSK: Pb = Q(sqrt(2Eb/N0))
Coherent FSK: Pb = Q(sqrt(Eb/N0))
Noncoherent FSK: Pb = 0.5*exp(-Eb/(2N0))
DPSK: Pb = 0.5*exp(-Eb/N0)
M-PSK symbol: Ps = 2*Q(sqrt(2Eb*log2(M)*sin^2(pi/M)/N0))
QAM symbol (approx): Ps ~ 2Q(sqrt(3*Es/((M-1)*N0)))
```

## Q Function
```
Q(x) = 0.5*erfc(x/sqrt(2))
For high x: Q(x) ~ (1/(x*sqrt(2pi)))*exp(-x^2/2)
Q(0) = 0.5, Q(inf) = 0
```

## Spectral Efficiency
```
Efficiency = Rb/BW = log2(M) for ideal Nyquist M-ary
BPSK: 1, QPSK: 2, 16-QAM: 4, 64-QAM: 6 bits/s/Hz
```

## Matched Filter
```
For AWGN optimal detection (matched filter / correlation):
  SNR_out = 2*E/N0 (where E = symbol energy)
  Ideal observation: adds no noise, maximizes SNR
```

## Eb/N0 Relationship
```
Eb/N0 (dB) = SNR(dB) + 10*log10(BW/Rb)
C/N = Eb/N0 * Rb/BW (for bandwidth B)
```

## Quick Reference
| Scheme | Bits/sym | BW | Pb (AWGN) |
|--------|----------|-----|-----------|
| BPSK | 1 | 2Rb | Q(sqrt(2Eb/N0)) |
| QPSK | 2 | Rb | Q(sqrt(2Eb/N0)) |
| 8-PSK | 3 | 2Rb/3 | ~Q(...) |
| 16-QAM | 4 | Rb/2 | ~Q(...) |
| FSK(co) | 1 | 2df+2Rb | Q(sqrt(Eb/N0)) |
| FSK(nc) | 1 | 2df+2Rb | 0.5e^(-Eb/2N0) |
