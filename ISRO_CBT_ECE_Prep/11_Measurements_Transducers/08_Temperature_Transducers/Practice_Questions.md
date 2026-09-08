# Temperature Transducers - Practice Questions

## Q1. (ISRO Pattern)
A Pt100 RTD has α = 0.00385/°C. What is its resistance at 200°C?
- (A) 200Ω
- (B) 177Ω
- (C) 138.5Ω
- (D) 277Ω
**Answer: (B)** R = 100[1 + 0.00385 × 200] = 100 × 1.77 = 177Ω

## Q2.
The Seebeck effect is the principle of operation of:
- (A) RTD
- (B) Thermistor
- (C) Thermocouple
- (D) IC sensor
**Answer: (C)**

## Q3.
An NTC thermistor has B = 4000K. At 25°C (298K), its resistance is 10kΩ. At 75°C (348K), resistance is approximately:
- (A) 5 kΩ
- (B) 2 kΩ
- (C) 1 kΩ
- (D) 10 kΩ
**Answer: (B)** R = 10k × exp[4000(1/348 - 1/298)] = 10k × exp(-0.193) ≈ 10k × 0.824 = 8.24kΩ... 
Hmm, let me recalc: exp[4000(1/348 - 1/298)] = exp[4000 × (298-348)/(348×298)] = exp[4000 × (-50)/(103704)] = exp[-1.929] = 0.145
R = 10k × 0.145 = 1.45kΩ → closest to (B) 2 kΩ

## Q4.
LM35 gives an output of:
- (A) 1 mV/°C
- (B) 10 mV/°C
- (C) 100 mV/°C
- (D) 1 V/°C
**Answer: (B)**

## Q5.
Which temperature transducer has the widest measurement range?
- (A) RTD
- (B) Thermocouple
- (C) Thermistor
- (D) IC sensor
**Answer: (B)** Thermocouples can measure up to 1450°C+.

## Q6.
A Type K thermocouple has S = 41 μV/°C. If reference junction is at 25°C and measured EMF is 10.25 mV, the hot junction temperature is:
- (A) 250°C
- (B) 275°C
- (C) 225°C
- (D) 300°C
**Answer: (B)** V = S(T_hot - T_ref) → 10.25mV = 41μV × (T-25) → T-25 = 250 → T = 275°C

## Q7.
The 3-wire RTD connection compensates for:
- (A) Self-heating
- (B) Lead wire resistance
- (C) Non-linearity
- (D) Reference junction temperature
**Answer: (B)**

## Q8.
NTC thermistor sensitivity is typically:
- (A) +0.385%/°C
- (B) -3% to -6%/°C
- (C) +10 mV/°C
- (D) 41 μV/°C
**Answer: (B)**

## Q9.
The thermocouple law of intermediate metals states:
- (A) EMF depends on wire length
- (B) Third metal doesn't affect EMF if both junctions at same temp
- (C) EMF is proportional to wire diameter
- (D) All metals have same Seebeck coefficient
**Answer: (B)**

## Q10.
At what temperature does a Pt100 have exactly 100Ω?
- (A) 25°C
- (B) 100°C
- (C) 0°C
- (D) 32°F
**Answer: (C)**

## Q11.
The output of AD590 at 25°C (298K) is:
- (A) 25 μA
- (B) 298 μA
- (C) 29.8 μA
- (D) 2.98 mA
**Answer: (B)**

## Q12.
Self-heating error in thermistor is minimized by:
- (A) Increasing excitation current
- (B) Decreasing excitation current
- (C) Using AC excitation
- (D) Using higher resistance thermistor
**Answer: (B)**

## Q13.
Which has the highest sensitivity?
- (A) RTD
- (B) NTC Thermistor
- (C) Thermocouple
- (D) LM35
**Answer: (B)** NTC has -3% to -6%/°C change.

## Q14.
A thermocouple with S = 52 μV/°C measures 26 mV with reference at 0°C. Temperature is:
- (A) 260°C
- (B) 500°C
- (C) 520°C
- (D) 250°C
**Answer: (B)** T = 26mV / 52μV = 500°C

## Q15.
The most linear temperature transducer is:
- (A) NTC thermistor
- (B) RTD
- (C) Thermocouple
- (D) PTC thermistor
**Answer: (B)** RTD has excellent linearity.

---
**ISRO Tip:** Pt100 calculation (R = 100(1+0.00385T)) and thermocouple EMF (V = SΔT) are the most tested formulas.
