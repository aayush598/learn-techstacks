# Network Theory - Practice Questions

---

### Q1. (Easy) Three resistors 6, 3, 2 ohm in parallel. Equivalent:
(A) 1 ohm  (B) 11 ohm  (C) 0.5 ohm  (D) 2 ohm

**Solution:** 1/Req = 1/6+1/3+1/2 = (1+2+3)/6 = 6/6 = 1 -> Req=1 ohm
**Answer: (A) 1 ohm**

---

### Q2. (Easy) Thevenin equivalent of 12V source with 4 ohm series resistance; load for max power:
(A) 4 ohm  (B) 8 ohm  (C) 12 ohm  (D) 1 ohm

**Answer: (A) 4 ohm (RL = Rth)**

---

### Q3. (Moderate) Vmax = 10V, Vmin = 4V for AM. Modulation index:
(A) 0.4  (B) 0.43  (C) 0.5  (D) 0.6

**Solution:** mu = (10-4)/(10+4) = 6/14 = 0.43
**Answer: (B) 0.43**

---

### Q4. (Moderate) Series RLC resonance, L=10mH, C=100nF. Resonant freq:
(A) 1.59 kHz  (B) 15.9 kHz  (C) 159 Hz  (D) 5 kHz

**Solution:** f = 1/(2pi sqrt(LC)) = 1/(2pi sqrt(1e-6)) = 1/(2pi*1e-3)=159.15 Hz
Wait sqrt(10e-3*100e-9) = sqrt(1e-9) = 3.16e-5 s. f = 1/(2pi*3.16e-5)=5030 Hz~5kHz
**Answer: (D) ~5 kHz**

---

### Q5. (Moderate) In a series RLC at resonance, impedance is:
(A) Maximum  (B) Minimum  (C) Zero  (D) Infinite

**Answer: (B) Minimum (=R)**

---

### Q6. (Moderate) Q of series circuit with R=10, L=10mH, f0=10kHz:
(A) 62.8  (B) 6.28  (C) 100  (D) 628

**Solution:** Q = w0 L/R = 2pi*1e4*1e-2/10 = 6.283e2/10 = 62.8
**Answer: (A) 62.8**

---

### Q7. (Moderate) Mutual inductance of coils L1=4H, L2=9H, k=0.5:
(A) 3 H  (B) 6 H  (C) 13 H  (D) 4H

**Solution:** M = k sqrt(L1L2) = 0.5*sqrt(36) = 0.5*6 = 3 H
**Answer: (A) 3 H**

---

### Q8. (Moderate) Two-port network with Z11=10, Z22=20, Z12=5, Z21=5 (ohms). Is it reciprocal?
(A) Yes  (B) No  (C) Can't tell  (D) Only if symmetric

**Solution:** Z12 = Z21 = 5 -> reciprocal (passive)
**Answer: (A) Yes**

---

### Q9. (Moderate) RC low-pass filter with R=1k, C=1uF cutoff:
(A) 159 Hz  (B) 1590 Hz  (C) 15.9 kHz  (D) 1.59 kHz

**Solution:** fc = 1/(2pi RC) = 1/(2pi*1e3*1e-6)= 1/(2pi*1e-3)=159.15 Hz
**Answer: (A) ~159 Hz**

---

### Q10. (Moderate) For a lossless capacitor at DC steady state, it behaves as:
(A) Short  (B) Open  (C) Resistor  (D) Voltage source

**Answer: (B) Open (I=0 at DC steady state)**
