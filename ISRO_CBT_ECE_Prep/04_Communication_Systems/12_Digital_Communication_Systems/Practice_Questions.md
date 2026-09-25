# Digital Communication Systems - Practice Questions

---

### Q1. (Easy) In a digital communication transmitter, the block immediately before the channel encoder is:
(A) Source encoder  (B) Modulator  (C) Channel  (D) Source decoder

**Answer: (A) Source encoder**

---

### Q2. (Easy) The main purpose of channel coding is to:
(A) Increase redundancy to detect or correct transmission errors  (B) Remove source redundancy  (C) Convert bits to audio  (D) Increase sampling rate

**Answer: (A) Increase controlled redundancy for error control.**

---

### Q3. (Moderate) A 4 kHz voice signal is sampled at 8 kHz and encoded using 8 bits/sample. The PCM bit rate is:
(A) 8 kb/s  (B) 32 kb/s  (C) 64 kb/s  (D) 128 kb/s

**Solution:** Rb = fs n = 8000 x 8 = 64,000 bits/s.
**Answer: (C) 64 kb/s**

---

### Q4. (Moderate) An M-QAM symbol carries:
(A) M bits  (B) log2(M) bits  (C) M/2 bits only  (D) One bit

**Answer: (B) log2(M) bits**

---

### Q5. (Moderate) The Shannon capacity of an AWGN channel with bandwidth B and SNR S is:
(A) B/S  (B) B log2(1 + S)  (C) S log2(B)  (D) B/(1 + S)

**Answer: (B) C = B log2(1 + S)**

---

### Q6. (Moderate) Which scheme generally has the best power efficiency at a target BER?
(A) BPSK  (B) 256-QAM  (C) ASK  (D) AM

**Answer: (A) BPSK**

---

### Q7. (Moderate) Which scheme generally has the highest ideal spectral efficiency?
(A) BPSK  (B) QPSK  (C) 16-QAM  (D) 64-QAM

**Answer: (D) 64-QAM**

---

### Q8. (Moderate) For a known pulse s(t), the matched-filter impulse response is:
(A) h(t) = s(t)  (B) h(t) = s*(T-t)  (C) h(t) = |s(t)|^2  (D) h(t) = s(t) - T

**Answer: (B) h(t) = s*(T-t)**

---

### Q9. (Moderate) FDMA, TDMA, and CDMA separate users respectively by:
(A) Frequency, time, and code  (B) Time, code, and frequency  (C) Code, frequency, and time  (D) Power, time, and frequency

**Answer: (A) Frequency, time, and code**

---

### Q10. (Moderate) For coherent BPSK in AWGN, the bit error probability is:
(A) Q(sqrt(2Eb/N0))  (B) Q(Eb/N0)  (C) 0.5 erfc(sqrt(Eb/N0))  (D) 1

**Answer: (A) Pb = Q(sqrt(2Eb/N0))**

---

### Q11. (Moderate) A code has rate 2/3. For 6,000 information bits, the minimum encoded length is:
(A) 4,000 bits  (B) 6,000 bits  (C) 9,000 bits  (D) 12,000 bits

**Solution:** Number of transmitted bits = information bits / rate = 6000/(2/3) = 9000.
**Answer: (C) 9,000 bits**

---

### Q12. (Moderate) A 10 MHz channel has SNR = 31. Its Shannon capacity is approximately:
(A) 50 Mb/s  (B) 31 Mb/s  (C) 10 Mb/s  (D) 310 Mb/s

**Solution:** C = 10 x log2(32) = 10 x 5 = 50 Mb/s.
**Answer: (A) 50 Mb/s**

---

### Q13. (Moderate) For a full-scale sine input, an ideal 12-bit uniform quantizer has SQNR approximately:
(A) 24 dB  (B) 48 dB  (C) 74 dB  (D) 96 dB

**Solution:** SQNR = 6.02(12) + 1.76 = 74 dB.
**Answer: (C) 74 dB**

---

### Q14. (Moderate) Increasing the order of QAM generally:
(A) Reduces spectral efficiency and requires lower Eb/N0  (B) Increases spectral efficiency and usually requires higher Eb/N0  (C) Does not change either quantity  (D) Changes only source coding

**Answer: (B) Increases spectral efficiency and usually requires higher Eb/N0.**

---

### Q15. (Moderate) In a fading link, outage probability is:
(A) Probability that the received SNR is below a required threshold  (B) Probability of source compression  (C) Ratio of antenna gain to loss  (D) Quantization step size

**Answer: (A) Probability that the received SNR is below a required threshold.**
