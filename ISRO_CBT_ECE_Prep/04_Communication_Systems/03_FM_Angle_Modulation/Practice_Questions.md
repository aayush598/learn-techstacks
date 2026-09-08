# FM and Angle Modulation - Practice Questions

---

### Q1. (Easy) FM carrier has delta_f = 75 kHz, modulating frequency = 15 kHz. Bandwidth (Carson):
(A) 90 kHz  (B) 150 kHz  (C) 180 kHz  (D) 225 kHz

**Solution:** BW = 2*(delta_f + fm) = 2*(75+15) = 2*90 = 180 kHz
**Answer: (C) 180 kHz**

---

### Q2. (Easy) FM modulation index for delta_f = 75 kHz, fm = 15 kHz:
(A) 2  (B) 4  (C) 5  (D) 75

**Solution:** beta = delta_f/fm = 75/15 = 5
**Answer: (C) 5**

---

### Q3. (Moderate) A PM modulator with kp = 2 rad/V, message Am = 3V, fm = 4 kHz. Maximum frequency deviation:
(A) 6 kHz  (B) 12 kHz  (C) 24 kHz  (D) 3 kHz

**Solution:** delta_f = kp*fm*Am = 2*4000*3 = 24000 Hz = 24 kHz
**Answer: (C) 24 kHz**

---

### Q4. (Moderate) If FM modulating frequency doubles while beta remains constant, bandwidth:
(A) Doubles  (B) Halves  (C) Same  (D) Quadruples

**Solution:** beta constant, fm doubles -> BW = 2*fm*(beta+1) doubles
**Answer: (A) Doubles**

---

### Q5. (Moderate) In FM, if the modulating frequency is doubled but deviation kept the same, beta:
(A) Doubles  (B) Halves  (C) Same  (D) Quadruples

**Solution:** beta = delta_f/fm. delta_f same, fm doubles -> beta halves
**Answer: (B) Halves**

---

### Q6. (Hard) A wideband FM with beta = 2.405 has carrier amplitude J0(2.405). What is carrier power?
(A) Maximum  (B) Zero (carrier suppressed)  (C) Half of total  (D) Quarter of total

**Solution:** J0(2.405) = 0, so the carrier component is suppressed
**Answer: (B) Zero (carrier suppressed)**

---

### Q7. (Moderate) Pre-emphasis circuit at transmitter is:
(A) Low-pass filter  (B) High-pass filter  (C) Band-pass  (D) Notch filter

**Solution:** Boost high-frequency message components => high-pass
**Answer: (B) High-pass filter**

---

### Q8. (Moderate) FM offers better SNR than AM because:
(A) Wider bandwidth  (B) Constant amplitude  (C) Bessel functions  (D) Lower power

**Solution:** FM trades bandwidth for SNR; figure of merit 3*beta^2*(beta+1) >> 1/3
**Answer: (A) Wider bandwidth**
