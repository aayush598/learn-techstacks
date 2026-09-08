# Communication Systems - Practice Questions

# AM Modulation Questions

---

### Q1. (Easy) AM signal has carrier power Pc = 1kW and modulation index mu = 0.5. Total power is:
(A) 1.125 kW  (B) 1.25 kW  (C) 1.5 kW  (D) 2 kW

**Solution:** Ptotal = Pc(1+mu^2/2) = 1000*(1+0.25/2) = 1000*1.125 = 1125W = 1.125 kW
**Answer: (A) 1.125 kW**

---

### Q2. (Easy) If Vmax = 10V and Vmin = 2V on an AM waveform, modulation index is:
(A) 0.5  (B) 0.667  (C) 0.75  (D) 0.8

**Solution:** mu = (Vmax-Vmin)/(Vmax+Vmin) = (10-2)/(10+2) = 8/12 = 0.667
**Answer: (B) 0.667**

---

### Q3. (Moderate) DSB-SC signal has carrier frequency 1 MHz and modulating 5 kHz. Its bandwidth is:
(A) 5 kHz  (B) 10 kHz  (C) 1 MHz  (D) 20 kHz

**Solution:** DSB-SC bandwidth = 2*fm = 2*5kHz = 10 kHz
**Answer: (B) 10 kHz**

---

### Q4. (Moderate) The maximum efficiency of standard AM (mu=1) is:
(A) 25%  (B) 33.3%  (C) 50%  (D) 100%

**Solution:** eta = mu^2/(2+mu^2) = 1/(2+1) = 1/3 = 33.3%
**Answer: (B) 33.3%**

---

### Q5. (Moderate) AM transmitter radiates 8 kW when no modulation, and 9 kW when modulated. The modulation index is:
(A) 0.5  (B) 0.707  (C) 0.25  (D) 1

**Solution:** Ptotal = Pc(1+mu^2/2) => 1+mu^2/2 = 9/8 => mu^2/2 = 1/8 => mu^2 = 1/4 => mu = 0.5
**Answer: (A) 0.5**

# PCM Questions

---

### Q6. (Easy) SQNR of 12-bit PCM is approximately:
(A) 72 dB  (B) 73.6 dB  (C) 74 dB  (D) 76 dB

**Solution:** SQNR = 6.02n + 1.76 = 6.02*12 + 1.76 = 72.24 + 1.76 = 74 dB
**Answer: (C) 74 dB**

# Noise Figure Questions

---

### Q7. (Moderate) Three amplifiers with noise figures 2, 4, 8 (linear) and gains 10, 100, 1000 are cascaded. Overall noise figure is approximately:
(A) 14  (B) 2.03  (C) 2.3  (D) 8

**Solution:** F = F1 + (F2-1)/G1 + (F3-1)/(G1*G2) = 2 + 3/10 + 7/1000 = 2 + 0.3 + 0.007 = 2.307
**Answer: (C) 2.3**

# Information Theory Questions

---

### Q8. (Moderate) If a source produces symbols with probabilities 0.5, 0.25, 0.125, 0.125, its entropy is:
(A) 1.5 bits  (B) 1.75 bits  (C) 2 bits  (D) 2.5 bits

**Solution:** H = -[0.5*log2(0.5) + 0.25*log2(0.25) + 2*(0.125*log2(0.125))]
= -[0.5*(-1) + 0.25*(-2) + 2*(0.125*(-3))]
= -[-0.5 - 0.5 - 0.75] = 1.75 bits
**Answer: (B) 1.75 bits**
