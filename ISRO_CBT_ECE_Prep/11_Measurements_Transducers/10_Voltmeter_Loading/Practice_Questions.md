# Voltmeter Loading Effect - Practice Questions

## Q1. (ISRO Pattern)
A voltmeter has sensitivity 20 kohm/V and is used on 10V range to measure voltage across a 10 kohm resistor in series with 40 kohm source resistance. The loading error is:
- (A) 3.77%
- (B) 16.67%
- (C) 20%
- (D) 5%
**Answer: (A)**
Rv = 20k x 10 = 200 kohm
Rth = 10k || 40k = 8 kohm (looking back from voltmeter terminals)
Wait, Rth is source resistance looking back from load:
Thevenin at load: Vth = Vs x 10/(10+40) = Vs/5
Rth = 10k || 40k = 8 kohm
V_meas = Vth x Rv/(Rth+Rv) = (Vs/5) x 200/(208) = Vs x 0.1923
V_true = Vs/5 = 0.2Vs
Error = |0.1923 - 0.2|/0.2 x 100 = 3.85% -> (A)

## Q2.
A voltmeter with sensitivity 5 kohm/V is used on 20V range. Its internal resistance is:
- (A) 100 kohm
- (B) 50 kohm
- (C) 20 kohm
- (D) 5 kohm
**Answer: (A)** Rv = 5k x 20 = 100 kohm

## Q3.
To measure a voltage across a circuit with Thevenin resistance 50 kohm with less than 1% loading error, the minimum voltmeter resistance is:
- (A) 500 kohm
- (B) 5 M ohm
- (C) 50 kohm
- (D) 1 M ohm
**Answer: (B)** Rv = 50k x (1/0.01 - 1) = 50k x 99 = 4.95 MOhm -> (B)

## Q4.
A DVM with 10 MOhm input impedance is used to measure voltage across a circuit with 1 MOhm Thevenin resistance. The loading error is:
- (A) 0.1%
- (B) 1%
- (C) 9.09%
- (D) 10%
**Answer: (C)** Error = 1M/(1M+10M) x 100 = 9.09%

## Q5.
Loading effect is LEAST when:
- (A) Source resistance is high
- (B) Voltmeter resistance is low
- (C) Source resistance is low compared to voltmeter resistance
- (D) Both resistances are equal
**Answer: (C)**

## Q6.
If Rv = 100 kohm and Rs = 1 kohm, the loading error is approximately:
- (A) 1%
- (B) 10%
- (C) 0.1%
- (D) 50%
**Answer: (A)** Error = 1k/(1k+100k) x 100 = 0.99% approx 1%

## Q7.
A voltmeter reads 9.5V. The true value is 10V. The loading error is:
- (A) -5%
- (B) +5%
- (C) -0.5V
- (D) Both (A) and (C)
**Answer: (D)** Error = (9.5-10)/10 x 100 = -5% and -0.5V

## Q8.
For a voltmeter with S = 10 kohm/V on 5V range measuring across Rth = 45 kohm, loading error is:
- (A) 47.4%
- (B) 9.5%
- (C) 4.74%
- (D) 50%
**Answer: (A)** Rv = 10k x 5 = 50 kohm
Error = 45k/(45k+50k) x 100 = 47.4%

## Q9.
To reduce loading error, we should:
- (A) Use lower sensitivity voltmeter
- (B) Use higher sensitivity voltmeter
- (C) Increase source resistance
- (D) Decrease voltmeter resistance
**Answer: (B)**

## Q10.
The sensitivity of a PMMC movement with Ifs = 50 uA is:
- (A) 20 kohm/V
- (B) 50 kohm/V
- (C) 100 kohm/V
- (D) 5 kohm/V
**Answer: (A)** S = 1/50uA = 20 kohm/V

## Q11.
A 20 kohm/V voltmeter on 10V range reads voltage across a voltage divider. If source resistance is 10 kohm, the voltmeter draws:
- (A) 50 uA
- (B) 5 uA
- (C) 500 uA
- (D) 0.5 uA
**Answer: (B)** I = V/Rv = 10/200k = 50 uA... wait
I = V/Rv. Rv = 200 kohm. If measuring 10V: I = 10/200k = 50 uA -> (A)

## Q12.
Loading error percentage depends on:
- (A) Only voltmeter resistance
- (B) Only source resistance
- (C) Ratio of source to voltmeter resistance
- (D) Measured voltage value
**Answer: (C)**

## Q13.
If loading error must be less than 0.5% and Rs = 20 kohm, minimum Rv:
- (A) 2 M ohm
- (B) 4 M ohm
- (C) 200 kohm
- (D) 400 kohm
**Answer: (B)** Rv = 20k x (1/0.005 - 1) = 20k x 199 = 3.98 MOhm -> (B)

## Q14.
The main advantage of DVM over analog voltmeter for loading is:
- (A) Higher sensitivity at all ranges
- (B) Constant high input impedance (10 MOhm)
- (C) Lower cost
- (D) Faster response
**Answer: (B)**

## Q15.
A voltmeter with 10 kohm/V sensitivity on 25V range measures across a circuit with Rth = 50 kohm. Loading error:
- (A) 16.7%
- (B) 50%
- (C) 33.3%
- (D) 25%
**Answer: (A)** Rv = 10k x 25 = 250 kohm
Error = 50k/(50k+250k) x 100 = 16.7%

---
**ISRO Tip:** Loading error = Rth/(Rth+Rv) x 100% is the most important formula. Rv = S x V_range.
