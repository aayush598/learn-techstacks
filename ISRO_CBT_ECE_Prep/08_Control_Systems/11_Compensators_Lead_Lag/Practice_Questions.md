# Compensators (Lead, Lag) - Practice Questions

## Section A: Conceptual

**Q1.** What does a lead compensator do to bandwidth and phase margin?
**A1.** Increases phase margin AND increases bandwidth (faster response).

**Q2.** What does a lag compensator primarily improve?
**A2.** Steady-state accuracy (increases low-frequency gain / error constants).

**Q3.** State the lead compensator transfer function and identify the zero-pole arrangement.
**A3.** G_c(s)=(1+αTs)/(1+Ts), α>1. Zero at −1/αT, pole at −1/T. Zero closer to origin → phase lead.

**Q4.** When would you use a lag compensator?
**A4.** When steady-state error is too large but transient specs are roughly acceptable.

## Section B: Lead Compensator Number Problems

**Q5.** A lead compensator has α=5. Find φ_max.
**A5.** φ_max = sin⁻¹[(5−1)/(5+1)] = sin⁻¹(4/6) = sin⁻¹(0.667) ≈ 41.8°.

**Q6.** For φ_max = 30°, find required α.
**A6.** α = (1+sin30°)/(1−sin30°) = (1.5)/(0.5) = 3.

**Q7.** Lead compensator with T=0.1, α=4. Find ω_max.
**A7.** ω_max = 1/(T√α) = 1/(0.1·2) = 5 rad/s.

**Q8.** Magnitude boost of lead at ω_max for α=10.
**A8.** 10log₁₀(10) = 10 dB.

**Q9.** A lead compensator (1+2s)/(1+0.5s). Identify α and T.
**A9.** αT=2, T=0.5 → α=4. (α>1, lead.)

## Section C: Lag Compensator Problems

**Q10.** Lag compensator G_c(s)=(1+10s)/(1+100s). Identify which pole is closer to origin.
**A10.** Zero at s=−0.1, pole at s=−0.01. Pole (at 0.01) closer to origin → phase lag.

**Q11.** For the above, what's the low-frequency DC gain?
**A11.** G_c(0)=1 (normalized form); accuracy gain comes from the overall loop gain increase.

**Q12.** A lag compensator improve error by... what happens to error constant K_v?
**A12.** K_v increases → steady-state ramp error decreases.

## Section D: Choosing the Compensator

**Q13.** System has too much overshoot but acceptable steady-state error. Which compensator?
**A13.** Lead (improve PM, reduce overshoot).

**Q14.** System has large steady-state error but desired transient response is fine. Which?
**A14.** Lag.

**Q15.** Both overshoot too high AND steady-state error too high. Which?
**A15.** Lead-lag.

## Section E: Design Calculations

**Q16.** Uncompensated PM=20°. Want PM=50°. Find α for lead (add 5° margin → need 35° lead).
**A16.** φ_max=35° → α=(1+sin35)/(1−sin35)=(1+0.574)/(1−0.574)=1.574/0.426=3.69.

**Q17.** For the lead compensator with α=3.69, find the magnitude boost at ω_max.
**A17.** 10log₁₀(3.69) = 5.67 dB.

**Q18.** A lag compensator should add 20 dB low-frequency gain. What gain factor is needed (if not in normalized form)?
**A18.** 20 dB → 10× gain (20log10(10)=20).

## Section F: ISRO-Style

**Q19.** Which compensator is represented by (s+2)/(s+8)?
**A19.** Zero at −2, pole at −8. Zero closer to origin → lead compensator.

**Q20.** Which is (s+8)/(s+2)?
**A20.** Pole at −2, zero at −8. Pole closer to origin → lag compensator.

**Q21.** A lead compensator with α=9, T=0.2. Find φ_max and ω_max.
**A21.** φ_max=sin⁻¹[(9−1)/(9+1)]=sin⁻¹(0.8)=53.1°. ω_max=1/(0.2·3)=1.667 rad/s.

**Q22.** Why does a lead compensator increase crossover frequency?
**A22.** It adds +10log₁₀(α) dB magnitude boost at high frequency, raising the magnitude curve and pushing ω_gc higher.

**Q23.** A lag compensator placed with corner frequencies far below crossover — why?
**A23.** To avoid adding significant phase lag at crossover (which would reduce PM); the increasing low-frequency gain still improves accuracy.

**Q24.** Does lead compensation change the steady-state error much? 
**A24.** Generally little (it mainly addresses transient/phase margin), unless additional gain stages are added.

**Q25.** Identify: G_c(s) = (1+s/2)(1+s/0.5) / [(1+s/20)(1+s/0.05)] — is it lead or lag overall?
**A25.** It's a lead-lag (has both a high-frequency lead part and low-frequency lag part).

## Common Mistakes
1. Swapping zero/pole order for lead vs lag.
2. Using wrong α formula (α=(1+sin)/(1−sin) for lead).
3. Forgetting the 10log₁₀(α) magnitude boost in lead design.
4. Placing lag corner frequencies too close to crossover (reduces PM).
5. Confusing which spec each compensator targets.
