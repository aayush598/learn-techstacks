# Op-Amp Non-Linear Circuits - Practice Questions

## ISRO-Style MCQs

### Question 1 (Easy)
**An inverting Schmitt trigger has Vsat = 10V, R1 = 10kΩ, R2 = 40kΩ. What is the UTP?**

(a) 2V
(b) -2V
(c) 8V
(d) 5V

**Answer: (a) 2V**
**Solution:** UTP = +Vsat × R1/(R1+R2) = 10 × 10/50 = 2V.

---

### Question 2 (Easy)
**What is the hysteresis width for Question 1's Schmitt trigger?**

(a) 2V
(b) 4V
(c) 8V
(d) 10V

**Answer: (b) 4V**
**Solution:** H = 2 × Vsat × R1/(R1+R2) = 2 × 2 = 4V. Also UTP - LTP = 2 - (-2) = 4V.

---

### Question 3 (Moderate)
**A comparator has Vsat = ±12V. Input is applied to inverting terminal with Vref = 5V. What is Vout for Vin = 6V?**

(a) +12V
(b) -12V
(c) 0V
(d) 5V

**Answer: (b) -12V**
**Solution:** Inverting comparator: Vin > Vref → Vout = -Vsat = -12V.

---

### Question 4 (Moderate)
**A window comparator has VrefHigh = 5V and VrefLow = 2V. For Vin = 3V, what is the output (with active-high AND logic)?**

(a) HIGH
(b) LOW
(c) Undefined
(d) Toggles

**Answer: (a) HIGH**
**Solution:** 2V < 3V < 5V, so input is within window → output HIGH.

---

### Question 5 (Hard)
**A zero-crossing detector (non-inverting) has a 10V peak sine wave at 1kHz. How many output transitions occur per second?**

(a) 1000
(b) 2000
(c) 4000
(d) 100

**Answer: (b) 2000**
**Solution:** Each sine wave cycle crosses zero twice → 2 × 1000 = 2000 transitions/second.

---

### Question 6 (Easy)
**Which circuit provides better noise immunity?**

(a) Comparator
(b) Schmitt trigger
(c) Zero-crossing detector
(d) Window comparator

**Answer: (b) Schmitt trigger**
**Solution:** Hysteresis prevents multiple switching on noisy signals.

---

### Question 7 (Moderate)
**For a non-inverting Schmitt trigger with Vsat = ±9V and R1 = R2 = 10kΩ, what is the hysteresis width?**

(a) 4.5V
(b) 9V
(c) 18V
(d) 2.25V

**Answer: (b) 9V**
**Solution:** H = 2 × Vsat × R2/(R1+R2) = 2 × 9 × 10/20 = 9V.

---

### Question 8 (Hard)
**A Schmitt trigger has UTP = 3V and LTP = -1V. What is the center of the hysteresis band?**

(a) 2V
(b) 1V
(c) -1V
(d) 3V

**Answer: (b) 1V**
**Solution:** Center = (UTP + LTP)/2 = (3 + (-1))/2 = 1V.

---

### Question 9 (Moderate)
**A window comparator monitors a battery. VrefHigh = 4.2V, VrefLow = 3.0V. What is the window width?**

(a) 1.2V
(b) 3.6V
(c) 0.6V
(d) 7.2V

**Answer: (a) 1.2V**
**Solution:** W = VrefHigh - VrefLow = 4.2 - 3.0 = 1.2V.

---

### Question 10 (Easy)
**What is the main disadvantage of using a basic comparator for noisy signals?**

(a) Too slow
(b) Multiple output transitions
(c) Low gain
(d) Limited voltage range

**Answer: (b) Multiple output transitions**
**Solution:** Noise causes the input to cross threshold multiple times, causing chatter.

---

### Question 11 (Hard)
**A comparator responds in 100ns. What is the maximum input frequency that can be reliably detected?**

(a) 1MHz
(b) 3.5MHz
(c) 10MHz
(d) 35MHz

**Answer: (b) 3.5MHz**
**Solution:** fmax ≈ 0.35/tpd = 0.35/100ns = 3.5MHz.

---

### Question 12 (Moderate)
**An inverting Schmitt trigger has R1 = 1kΩ, R2 = 9kΩ, and supply of ±15V. What is UTP?**

(a) 1.5V
(b) 15V
(c) 13.5V
(d) 1.67V

**Answer: (a) 1.5V**
**Solution:** UTP = 15 × 1k/(1k+9k) = 15 × 0.1 = 1.5V. Note: use Vsat ≈ supply voltage.

---

### Question 13 (Easy)
**Which circuit converts a sine wave to a square wave?**

(a) Integrator
(b) Differentiator
(c) Comparator
(d) Summing amplifier

**Answer: (c) Comparator**
**Solution:** Comparator switches output between saturation levels based on input polarity.

---

### Question 14 (Hard)
**A Schmitt trigger needs 100mV noise immunity. With Vsat = 10V, what R1/R2 ratio is needed?**

(a) 1:50
(b) 1:100
(c) 1:200
(d) 1:1000

**Answer: (b) 1:100**
**Solution:** H = 2×Vsat×R1/(R1+R2) ≥ 100mV. 2×10×R1/(R1+R2) ≥ 0.1 → R1/(R1+R2) ≥ 0.005 → R2/R1 ≤ 199 ≈ 200. For R1:R2 = 1:100, H = 20×1/101 ≈ 198mV ✓.

---

### Question 15 (Moderate)
**What is the output of an inverting zero-crossing detector for a negative input voltage?**

(a) +Vsat
(b) -Vsat
(c) 0V
(d) Undefined

**Answer: (a) +Vsat**
**Solution:** Inverting configuration: Vin < 0 → Vout = +Vsat.

---

### Question 16 (Easy)
**Sample-and-hold: what happens to the output during hold mode?**

(a) Follows input
(b) Maintains last sampled value
(c) Goes to zero
(d) Inverts input

**Answer: (b) Maintains last sampled value**
**Solution:** During hold, capacitor retains voltage, output remains at sampled value.

---

### Question 17 (Hard)
**For a switch with 5pC charge injection and 100pF hold capacitor, what is the voltage error?**

(a) 5mV
(b) 50mV
(c) 500mV
(d) 5V

**Answer: (b) 50mV**
**Solution:** Error = Qinj/C = 5pC/100pF = 0.05V = 50mV.

---

### Question 18 (Moderate)
**A Schmitt trigger with R1 = 5kΩ, R2 = 15kΩ, Vsat = +10V/-10V. What is the ratio UTP:LTP?**

(a) 1:1
(b) 1:-1
(c) 2:5
(d) 5:2

**Answer: (b) 1:-1**
**Solution:** UTP = 10×5/20 = 2.5V, LTP = -10×5/20 = -2.5V. Ratio = 1:-1 (symmetric).

---

### Question 19 (Easy)
**What type of feedback does a Schmitt trigger use?**

(a) Negative
(b) Positive
(c) Both
(d) None

**Answer: (b) Positive**
**Solution:** Positive feedback through voltage divider creates hysteresis.

---

### Question 20 (Moderate)
**An inverting Schmitt trigger has UTP = 5V, LTP = 1V, Vsat = 10V. What is R1/R2 ratio?**

(a) 1/5
(b) 1/3
(c) 2/5
(d) 1/4

**Answer: (b) 1/3**
**Solution:** Using H = UTP - LTP = 4V and H = 2×Vsat×R1/(R1+R2): 4 = 20×R1/(R1+R2) → R1/(R1+R2) = 0.2 → R1/R2 = 0.25... Let's verify: R1=1,R2=3: R1/(R1+R2)=0.25, H=20×0.25=5V. Not 4V. Recheck: for UTP=5, LTP=1, Vsat=10: UTP = 10×R1/(R1+R2) = 5 → R1/(R1+R2) = 0.5 → R1=R2 → ratio 1:1.

**Correction: Ratio is 1:1 (R1 = R2).**

---

## ISRO Exam Tips for This Topic

### Quick Solving Tricks
1. UTP/LTP symmetric about zero when Vsat symmetric and no offset
2. Hysteresis width is always 2×UTP for symmetric triggers
3. Window comparator: test each comparator separately then combine
4. Zero-crossing detector: count both positive and negative crossings

### Common Pitfalls
- Forgetting non-inverting Schmitt uses R2 factor, not R1
- Confusing which output state occurs for given input
- Assuming Vsat equals supply voltage (it's slightly less)
- Not accounting for both crossings in frequency counting

### ISRO-Specific Patterns
- Schmitt trigger calculations very common
- Window comparator logic states frequently tested
- Noise immunity → hysteresis relationship
- Zero-crossing for frequency measurement
- Sample-and-hold error sources
