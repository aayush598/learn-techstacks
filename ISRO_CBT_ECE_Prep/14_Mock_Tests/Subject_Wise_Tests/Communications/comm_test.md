# Subject-Wise Test - Communication Systems

## 20 Questions, 25 Minutes, +1/−0.33

## Questions

**Q1.** An AM signal has 100 W carrier power and modulation index 0.4. Total transmitted power is:

A. 104 W  
B. 108 W  
C. 116 W  
D. 140 W

**Q2.** For AM with `μ=0.5`, the fraction of total power in sidebands is:

A. 11.1%  
B. 20.0%  
C. 25.0%  
D. 50.0%

**Q3.** Carson's rule gives bandwidth `2(Δf+fm)`. For `Δf=50 kHz` and `fm=10 kHz`, the FM bandwidth is:

A. 60 kHz  
B. 80 kHz  
C. 100 kHz  
D. 120 kHz

**Q4.** The minimum ideal sampling rate for a bandlimited signal of maximum frequency 4 kHz is:

A. 2 ksample/s  
B. 4 ksample/s  
C. 8 ksample/s  
D. 16 ksample/s

**Q5.** For ideal uniform PCM with 8 bits per sample, the approximate SQNR is:

A. 37.9 dB  
B. 42.1 dB  
C. 49.9 dB  
D. 56.0 dB

**Q6.** A 3 kHz channel has SNR 15. Shannon capacity is approximately:

A. 9 kbps  
B. 12 kbps  
C. 18 kbps  
D. 45 kbps

**Q7.** Coherent BPSK bit-error probability in AWGN is:

A. `Q(√(Eb/N0))`  
B. `Q(√(2Eb/N0))`  
C. `0.5 exp(−Eb/2N0)`  
D. `erfc(√(2Eb/N0))`

**Q8.** QPSK carries:

A. 1 bit/symbol  
B. 2 bits/symbol  
C. 3 bits/symbol  
D. 4 bits/symbol

**Q9.** Noncoherent binary FSK has bit-error probability:

A. `Q(√(Eb/N0))`  
B. `0.5 exp(−Eb/2N0)`  
C. `erfc(√(Eb/N0))`  
D. 0.5

**Q10.** A matched filter is used to:

A. Maximize output SNR for a known signal  
B. Remove all ISI only  
C. Quantize without error  
D. Increase carrier frequency

**Q11.** A widely open eye diagram generally indicates:

A. High timing jitter and noise  
B. Low noise and small timing jitter  
C. Channel overload  
D. No signal

**Q12.** A noise figure of 3 dB corresponds to a linear factor of approximately:

A. 0.5  
B. 1  
C. 2  
D. 3

**Q13.** For `F=2` and `T0=290 K`, equivalent noise temperature is:

A. 0 K  
B. 145 K  
C. 290 K  
D. 580 K

**Q14.** Companding in PCM is used mainly to:

A. Increase bandwidth  
B. Improve SQNR for small signals  
C. Prevent aliasing  
D. Synchronize carriers

**Q15.** Guard bands in FDM are provided to:

A. Store data  
B. Reduce adjacent-channel interference  
C. Increase quantization levels  
D. Correct phase errors only

**Q16.** An AMI violation is commonly used for:

A. In-band line coding  
B. Clock recovery and fault detection  
C. Antenna polarization  
D. Quantization

**Q17.** For a valid instantaneous Huffman code, average length satisfies:

A. `L<H`  
B. `H≤L<H+1`  
C. `L=H+1` always  
D. `H≤L+1`

**Q18.** TDM assigns distinct time slots to:

A. Parallel physical wires only  
B. Multiple channels sharing a transmission medium  
C. Antenna polarizations only  
D. Separate optical wavelengths only

**Q19.** To transmit 12 kbps through an SNR-15 channel, the minimum Shannon bandwidth is:

A. 1.5 kHz  
B. 3 kHz  
C. 4 kHz  
D. 12 kHz

**Q20.** A synchronous CDMA receiver distinguishes users mainly by:

A. Unique orthogonal spreading codes  
B. Carrier amplitude only  
C. Random time duration  
D. Equal polarization

## Answer Key

| Question | Answer | Question | Answer |
|---:|:---:|---:|:---:|
| 1 | B | 11 | B |
| 2 | A | 12 | C |
| 3 | D | 13 | C |
| 4 | C | 14 | B |
| 5 | C | 15 | B |
| 6 | B | 16 | B |
| 7 | B | 17 | B |
| 8 | B | 18 | B |
| 9 | B | 19 | B |
| 10 | A | 20 | A |

## Quick Solutions

1. `Pt=Pc(1+μ²/2)=108 W`.  
2. `ηmod=μ²/(2+μ²)=11.1%`.  
4. `fs,min=2fmax=8 ksample/s`.  
5. `SQNR≈6.02n+1.76=49.92 dB`.  
6. `C=3000 log₂16=12 kbps`.  
13. `Te=(F−1)T0=290 K`.  
19. `Bmin=C/log₂(16)=3 kHz`.
