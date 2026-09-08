# Power Amplifiers - Practice Questions

---

### Q1. (Easy) The maximum theoretical efficiency of a Class B push-pull amplifier is:
(A) 25%  (B) 50%  (C) 78.5%  (D) 100%

**Solution:** Class B max efficiency = pi/4 = 78.5%
**Answer: (C) 78.5%**

---

### Q2. (Easy) Crossover distortion is observed in:
(A) Class A  (B) Class B  (C) Class AB  (D) Class D

**Solution:** Class B push-pull has dead zone where both transistors are off near zero crossing.
**Answer: (B) Class B**

---

### Q3. (Moderate) A Class A amplifier has Vcc = 20V, Icq = 200mA, and drives a 50 ohm load. Its maximum efficiency is:
(A) 25%  (B) 50%  (C) 12.5%  (D) 10%

**Solution:** Pdc = Vcc*Icq = 20*0.2 = 4W
Po_max = Vcc*Icq/2 = 2W (for resistive load, max 25%)
eta = Po/Pdc = 2/4 = 50%... but this is only if Vce can swing full Vcc.
With resistive load: actual max swing is limited. Vce_q = Vcc/2 = 10V, Icq = 10V/50ohm = 200mA.
Po_max = (10)^2/(2*50) = 1W. Pdc = 20*0.2 = 4W. eta = 1/4 = 25%.
**Answer: (A) 25%**

---

### Q4. (Moderate) Class C amplifiers use a tank circuit at the output to:
(A) Increase gain  (B) Increase bandwidth  (C) Recover sinusoidal waveform  (D) Reduce power consumption

**Solution:** Class C conducts for <180 degrees producing pulses. Tank circuit at resonant frequency filters harmonics to recover sine wave.
**Answer: (C) Recover sinusoidal waveform**

---

### Q5. (Hard) In a Class B amplifier with Vcc = 15V and Rl = 100 ohms, the maximum AC output power is:
(A) 1.125W  (B) 2.25W  (C) 4.5W  (D) 0.56W

**Solution:** Po_max = Vcc^2/(2*Rl) = 225/200 = 1.125W
**Answer: (A) 1.125W**

---

### Q6. (Easy) Class D amplifier works on the principle of:
(A) Linear amplification  (B) PWM (Pulse Width Modulation)  (C) Frequency modulation  (D) Amplitude modulation

**Solution:** Class D uses switching transistors with PWM to achieve high efficiency.
**Answer: (B) PWM**

---

### Q7. (Moderate) To eliminate crossover distortion in Class B, we use:
(A) Negative feedback  (B) Class AB biasing  (C) Higher supply voltage  (D) Lower load resistance

**Solution:** Slightly biasing both transistors above cutoff (Vbe biasing) eliminates the dead zone.
**Answer: (B) Class AB biasing**

---

### Q8. (Hard) The power dissipation in a Class B amplifier is maximum when:
(A) Output is maximum  (B) Output is zero  (C) Output is at 50% of maximum  (D) Supply is disconnected

**Solution:** In Class B, Pd is maximum at approximately 50% of maximum output power. At max output, efficiency is highest so less power is dissipated.
**Answer: (C) Output is at 50% of maximum**

---

### Q9. (Easy) The maximum efficiency of a transformer-coupled Class A amplifier is:
(A) 25%  (B) 50%  (C) 78.5%  (D) 100%

**Solution:** Transformer coupling allows full swing from 0 to 2*Vcc, achieving 50% efficiency.
**Answer: (B) 50%**

---

### Q10. (Moderate) Class F amplifier achieves near 100% efficiency by:
(A) Using switching mode  (B) Shaping voltage and current waveforms  (C) Using feedback  (D) Using multiple stages

**Solution:** Class F uses harmonic resonators to shape V and I waveforms so they don't overlap, minimizing transistor power dissipation.
**Answer: (B) Shaping voltage and current waveforms**
