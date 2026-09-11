# Pulse Modulation / PCM - Practice Questions

---

### Q1. (Easy) In PCM, quantization:
(A) Converts analog to discrete amplitude levels  (B) Samples only  (C) Modulates carrier  (D) Multiplexes

**Answer: (A) Quantization - discrete amplitude levels from continuous values**

---

### Q2. (Moderate) Number of bits for 128 quantization levels:
(A) 7  (B) 8  (C) 6  (D) 128

**Solution:** 2^n = 128 -> n = 7
**Answer: (A) 7 bits**

---

### Q3. (Moderate) Quantization SNR (uniform) increases __ dB per bit:
(A) 6  (B) 3  (C) 10  (D) 20

**Answer: (A) ~6 dB/bit (SQNR = 6.02n + 1.76)**

---

### Q4. (Moderate) PAM is:
(A) Amplitude of pulses varied with sample  (B) Width varied  (C) Position varied  (D) Frequency

**Answer: (A) Pulse Amplitude Modulation - pulse amplitude = sample value**

---

### Q5. (Moderate) In PWM, information in:
(A) Pulse width  (B) Pulse amplitude  (C) Pulse position only  (D) Frequency

**Answer: (A) Width proportional to signal**

---

### Q6. (Moderate) PPM varies:
(A) Pulse position  (B) Amplitude  (C) Width (fixed positions moved)  (D) Frequency

**Answer: (A) Position of pulse proportional to sample**

---

### Q7. (Moderate) PCM is digital because:
(A) Quantized + encoded in binary  (B) Sampled  (C) Continuous  (D) AM

**Answer: (A) Digital: quantizes and encodes to binary bits (immune to noise)**

---

### Q8. (Moderate) Advantage of PCM vs analog (PAM/PWM/PPM):
(A) Noise immunity (digital), regeneration  (B) Less bandwidth use  (C) Simpler  (D) Cheaper

**Answer: (A) Noise immunity - can regenerate clean digital signal, unlimited distance**

---

### Q9. (Moderate) Delta modulation compares:
(A) Current sample vs previous (1-bit)  (B) Full 8-bit  (C) Only amplitude  (D) Only freq

**Answer: (A) Delta: 1-bit difference (sample - prediction); slope overload if too fast**

---

### Q10. (Moderate) Slope overload in delta modulation occurs when:
(A) Signal changes faster than step can follow  (B) Too slow  (C) No signal  (D) DC only

**Answer: (A) Slope overload when input rate exceeds step*fs**
