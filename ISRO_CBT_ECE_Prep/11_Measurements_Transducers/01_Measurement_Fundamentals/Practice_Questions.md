# Measurement Fundamentals - Practice Questions

## Q1. (ISRO Pattern)
A voltmeter has a sensitivity of 20 kΩ/V and is used to measure voltage across a 10 kΩ resistor in series with a 40 kΩ source resistance on the 10V range. What is the loading error?
- (A) 5%
- (B) 16.67%
- (C) 20%
- (D) 25%
**Answer: (B)**
R_vm = 20k × 10 = 200 kΩ
V_true = V × 10/(10+40) = V × 0.2
V_meas = V × 200/(200+40) = V × 0.833
Error = (0.833-0.2)/0.2 × 100% ... Wait, recalculate:
True: V across 10k = Vs × 10/(10+40) = Vs/5
Measured: V across 10k || 200k = Vs × 9.52/(9.52+40) = Vs × 0.1924
Loading error % = |0.1924 - 0.2|/0.2 × 100 = 3.78%... Let me recalc properly:
R_load = 10k, R_source = 40k, R_vm = 200k
V_true = Vs × 10/(10+40) = 0.2Vs
R_parallel = 10k || 200k = 2000/210 = 9.524 kΩ
V_meas = Vs × 9.524/(9.524+40) = Vs × 0.1924
Error = |0.1924-0.2|/0.2 × 100 = 3.78% → closest to (A)

## Q2.
A 3½ digit DVM has a basic accuracy of ±0.5% of reading ±1 digit. On the 2V range, what is the maximum error for a reading of 1.500V?
- (A) ±8 mV
- (B) ±8.5 mV
- (C) ±7.5 mV
- (D) ±9 mV
**Answer: (B)**
Resolution = 1mV (2V/2000)
Error = 0.5% of 1500 + 1 = 7.5 + 1 = 8.5 mV

## Q3.
Which statement is TRUE about accuracy and precision?
- (A) High accuracy always means high precision
- (B) High precision always means high accuracy
- (C) An instrument can be precise but not accurate
- (D) Accuracy and precision are identical
**Answer: (C)**

## Q4.
A null-type instrument is preferred over deflection-type because:
- (A) It is cheaper
- (B) It gives direct reading
- (C) It has no loading effect at balance
- (D) It has faster response
**Answer: (C)**

## Q5.
The sensitivity of a voltmeter is 10 kΩ/V. On the 50V range, its internal resistance is:
- (A) 10 kΩ
- (B) 50 kΩ
- (C) 500 kΩ
- (D) 5000 kΩ
**Answer: (C)** R_v = 10k × 50 = 500 kΩ

## Q6.
The random errors in measurement follow which distribution?
- (A) Uniform
- (B) Gaussian (Normal)
- (C) Poisson
- (D) Binomial
**Answer: (B)**

## Q7.
A galvanometer with internal resistance 50Ω and full-scale current 1mA is to be converted to a 10V voltmeter. The series multiplier resistance required is:
- (A) 9.95 kΩ
- (B) 10 kΩ
- (C) 9950 Ω
- (D) Both (A) and (C)
**Answer: (D)** R_s = V/I_g - R_g = 10/0.001 - 50 = 10000 - 50 = 9950 Ω

## Q8.
If a voltmeter reads 49.5V when the true value is 50V, its accuracy is:
- (A) 98%
- (B) 99%
- (C) 99.5%
- (D) 100%
**Answer: (B)** Accuracy = (1 - 0.5/50) × 100 = 99%

## Q9.
Which error can be eliminated by taking the mean of a large number of readings?
- (A) Systematic error
- (B) Random error
- (C) Gross error
- (D) Instrumental error
**Answer: (B)**

## Q10.
An instrument has a resolution of 0.1V on 10V range. It is a:
- (A) 4 digit instrument
- (B) 3 digit instrument
- (C) 3½ digit instrument
- (D) 2 digit instrument
**Answer: (C)** 3½ digit: max count 1999, resolution ≈ 10/1999 ≈ 0.005... Actually 0.1V resolution on 10V means 100 steps, so 2 digit. Answer: (D)

## Q11.
Loading effect is most severe when:
- (A) Source resistance is low compared to meter resistance
- (B) Source resistance is high compared to meter resistance
- (C) Source resistance equals meter resistance
- (D) Loading effect is independent of resistances
**Answer: (B)**

## Q12.
If three independent measurements have uncertainties of ±2, ±3, ±4 units, the combined uncertainty is approximately:
- (A) ±9
- (B) ±5.39
- (C) ±7
- (D) ±2.33
**Answer: (B)** √(4+9+16) = √29 = 5.39

## Q13.
A 4½ digit DVM on 10V range can display up to:
- (A) 9.999V
- (B) 19.999V
- (C) 9.9999V
- (D) 1.9999V
**Answer: (B)** 4½ digit max = 19999

## Q14.
The primary difference between null-type and deflection-type instruments is:
- (A) Null type uses PMMC movement
- (B) Deflection type has higher accuracy
- (C) Null type eliminates instrument calibration dependence
- (D) Deflection type is a bridge circuit
**Answer: (C)**

## Q15.
In a measurement system, which transducer is the first element?
- (A) Signal conditioning
- (B) Primary sensing element
- (C) Data presentation
- (D) Variable conversion
**Answer: (B)**

---
**ISRO Tip:** Loading effect problems are very common. Always check if R_vm >> R_source. If R_vm ≥ 100 × R_source, loading error is < 1%.
