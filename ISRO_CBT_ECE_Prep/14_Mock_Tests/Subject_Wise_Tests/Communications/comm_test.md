# Subject-Wise Test - Communication Systems

## 20 Questions, 25 Minutes, +1/-0.33

---

**Q1.** AM carrier power = 100W, mu = 0.8. Total power:
A) 112W  B) 132W  C) 164W  D) 180W
Answer: B (P = 100(1+0.64/2) = 100*1.32 = 132W)

**Q2.** FM bandwidth (Carson) for delta_f = 50kHz, fm = 10kHz:
A) 60 kHz  B) 100 kHz  C) 120 kHz  D) 200 kHz
Answer: C (BW = 2*(50+10) = 120 kHz)

**Q3.** 6-bit PCM SQNR is:
A) 36 dB  B) 37.88 dB  C) 42 dB  D) 48 dB
Answer: B (6.02*6+1.76 = 36.12+1.76 = 37.88 dB)

**Q4.** Signal of 10kHz sampled at 30kHz, presence of 12kHz component. This sampling:
A) Adequate  B) Causes aliasing  C) Meets Nyquist  D) Fails Nyquist
Answer: D (fs=30 < 2*12=24? No, 30 > 24, so adequate. But 2*fmax = 20 < 30, so adequate)
Wait: fmax = 10kHz, Nyquist = 20kHz, fs = 30 > 20, so adequate. Answer: A/C.

**Q5.** Shannon capacity for B=4kHz, SNR=15:
A) 4 kbps  B) 8 kbps  C) 16 kbps  D) 60 kbps
Answer: C (C = 4000*log2(16) = 4000*4 = 16000 bps)

**Q6.** Entropy of 4 equidistant symbols (each p=0.25):
A) 1 bit  B) 1.5 bits  C) 2 bits  D) 4 bits
Answer: C (H = 4*0.25*log2(4) = 4*0.25*2 = 2 bits)

**Q7.** Symbol error probability of BPSK:
A) Q(sqrt(Eb/N0))  B) Q(sqrt(2Eb/N0))  C) Q(sqrt(Eb/(2N0)))  D) exp(-Eb/N0)
Answer: B

**Q8.** In binary symmetric channel with error probability p, channel capacity:
A) 1  B) 1-H(p)  C) 1-2p  D) H(p)
Answer: B

**Q9.** A-law companding with A=87.6 vs linear quantization for small signals:
A) Better SQNR  B) Worse SQNR  C) Same  D) No effect
Answer: A

**Q10.** Guard band in FDM is used to:
A) Improve SNR  B) Prevent channel interference  C) Reduce bandwidth  D) Increase data rate
Answer: B

**Q11.** For a 4kHz telephone channel, PCM with 8-bit sampling at Nyquist rate gives bit rate:
A) 32 kbps  B) 64 kbps  C) 128 kbps  D) 256 kbps
Answer: B (8000 samples/s * 8 bits = 64000 bps)

**Q12.** QPSK can transmit how many bits per symbol?
A) 1  B) 2  C) 4  D) 8
Answer: B (QPSK = 4 phases => 2 bits/symbol)

**Q13.** If noise figure F = 2 (linear), noise temperature Te =:
A) 145K  B) 290K  C) 580K  D) 0K
Answer: A (Te = (2-1)*290 = 290K)  Wait, Te = (F-1)*T0 = (2-1)*290 = 290K. Answer: B.

**Q14.** Eye diagram wide opening indicates:
A) High noise  B) Low noise and jitter  C) Fast data  D) High bandwidth
Answer: B

**Q15.** For AM with mu = 0.5, sideband power fraction of total:
A) 11.1%  B) 20%  C) 33.3%  D) 50%
Answer: A (Psb/Ptotal = mu^2/(2+mu^2) = 0.25/2.25 = 11.1%)

**Q16.** T1 carrier streams: 24 voice channels at 64kbps each. Total bit rate:
A) 1.544 Mbps  B) 2.048 Mbps  C) 1.5 Mbps  D) 64 Mbps
Answer: A

**Q17.** If FSK is noncoherent, error probability:
A) Q(sqrt(Eb/N0))  B) 0.5*exp(-Eb/(2N0))  C) 1/2  D) 1
Answer: B

**Q18.** A DSB-SC signal requires which demodulator?
A) Envelope detector  B) Coherent detector  C) Ratio detector  D) Slope detector
Answer: B

**Q19.** Source with p(0) = 0.9, p(1) = 0.1. Huffman code lengths:
A) 1 and 1  B) 1 and 2  C) 2 and 2  D) 3 and 3
Answer: A (Huffman: most probable gets 1 bit, less gets 1 bit)

**Q20.** FM has constant amplitude because:
A) Modulation is amplitude  B) Modulation is frequency  C) No modulation  D) Filtering
Answer: B

---

## Answer Key
Q1: B, Q2: C, Q3: B, Q4: A, Q5: C, Q6: C, Q7: B, Q8: B, Q9: A, Q10: B
Q11: B, Q12: B, Q13: B, Q14: B, Q15: A, Q16: A, Q17: B, Q18: B, Q19: A, Q20: B
