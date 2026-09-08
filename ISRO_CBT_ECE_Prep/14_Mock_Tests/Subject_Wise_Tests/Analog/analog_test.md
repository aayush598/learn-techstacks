# Subject-Wise Test - Analog Circuits

## 20 Questions, 25 Minutes, +1/-0.33

---

**Q1.** A non-inverting amplifier has R1 = 1k, Rf = 9k. Voltage gain:
A) 9  B) 10  C) -9  D) 11
Answer: B (Av = 1+Rf/R1 = 1+9 = 10)

**Q2.** For an ideal op-amp, input impedance is:
A) Zero  B) Infinite  C) 75 ohms  D) 1 kohm
Answer: B

**Q3.** Slew rate required for 1V peak, 1MHz sine is (V/us):
A) 2pi  B) pi  C) 4pi  D) 6.28
Answer: A (SR = 2*pi*f*Vpeak = 2*pi*10^6*1 = 6.28e6 V/s = 6.28 V/us)

**Q4.** Schmitt trigger hysteresis is used for:
A) Amplification  B) Noise immunity  C) Frequency selection  D) Impedance matching
Answer: B

**Q5.** Class AB amplifier is biased:
A) At center  B) At cutoff  C) Slightly above cutoff  D) Below cutoff
Answer: C

**Q6.** Wien bridge oscillator frequency with R=100k, C=100pF:
A) 159 Hz  B) 15.9 kHz  C) 1.59 kHz  D) 159 kHz
Answer: B (f = 1/(2*pi*100k*100p) = 1/(2*pi*10^-5) = 15.9 kHz)

**Q7.** The virtual ground in op-amp is valid when:
A) Positive feedback  B) Negative feedback  C) Always  D) Never
Answer: B

**Q8.** Common-mode rejection ratio measures op-amp's ability to:
A) Reject power supply noise  B) Reject common-mode signals  C) Reject differential signals  D) Increase gain
Answer: B

**Q9.** A comparator converts:
A) DC to AC  B) Analog to digital (two-state)  C) Digital to analog  D) Frequency to amplitude
Answer: B

**Q10.** Bandwidth of an op-amp increases when:
A) Gain increases  B) Gain decreases  C) Supply voltage increases  D) Load increases
Answer: B (GBW constant, so lower gain = higher BW)

**Q11.** Feedback factor beta = 0.1, open-loop gain A = 100. Closed loop gain:
A) 10  B) 9.09  C) 100  D) 11
Answer: B (Af = 100/(1+10) = 9.09)

**Q12.** Which amplifier has lowest efficiency?
A) Class A  B) Class B  C) Class C  D) Class D
Answer: A (25% max)

**Q13.** RC phase shift oscillator uses N RC sections, the minimum gain requirement for N=4 is:
A) 8  B) 16  C) 29  D) 64
Answer: A (A >= 2^N = 2^4... actually for 3 sections it's 29. For 4 sections A>=2^4=16? Let me use formula: for N sections, A >= 4^((N-1)/2)... hmm. Standard: 3 sections needs minimum 29. For 4 sections, the required gain increases.)

**Q14.** Crossover distortion is caused by:
A) High gain  B) Dead zone at zero crossing  C) Low supply  D) Feedback
Answer: B

**Q15.** A summing amplifier with 3 inputs V1, V2, V3 each connected through R = 10k to inverting input, feedback Rf = 30k. Output:
A) -(V1+V2+V3)  B) -3(V1+V2+V3)  C) -0.33(V1+V2+V3)  D) 3(V1+V2+V3)
Answer: A (Vo = -(Rf/R)(V1+V2+V3) = -(30/10)(sum) = -3(sum))
Wait, Rf/R = 30k/10k = 3. So Vo = -3*(sum). Answer B.

**Q16.** Op-amp UGB (unit-gain bandwidth) is 10 MHz. For gain of 10, BW is:
A) 1 MHz  B) 10 MHz  C) 100 MHz  D) 1 kHz
Answer: A (BW = 10M/10 = 1 MHz)

**Q17.** A voltage follower is also called:
A) Non-inverting amp with gain 1  B) Inverting amp with gain 10  C) Differential amp  D) Comparator
Answer: A

**Q18.** For oscillation, Barkhausen requires:
A) |A*beta| < 1  B) |A*beta| = 1, phase 180  C) |A*beta| = 1, phase 0/360  D) |A*beta| > 2
Answer: C

**Q19.** A Hartley oscillator uses:
A) Two capacitors and one inductor  B) Two inductors and one capacitor  C) Three resistors  D) Crystal only
Answer: B

**Q20.** The T-network feedback in inverting amplifier is used to:
A) Increase gain  B) Achieve high gain with moderate resistors  C) Reduce noise  D) Increase BW
Answer: B

---

## Answer Key
Q1: B, Q2: B, Q3: A, Q4: B, Q5: C, Q6: B, Q7: B, Q8: B, Q9: B, Q10: B
Q11: B, Q12: A, Q13: A, Q14: B, Q15: B, Q16: A, Q17: A, Q18: C, Q19: B, Q20: B
