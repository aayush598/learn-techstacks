# Time Domain Specifications - Practice Questions

## Section A: Conceptual

**Q1.** Define percent overshoot and rise time.
**A1.** %OS = maximum overshoot above final value as % of final. Rise time = time from 10% to 90% of final value.

**Q2.** What are the 2% and 5% settling times in terms of ζω_n?
**A2.** t_s(2%) = 4/(ζω_n), t_s(5%) = 3/(ζω_n).

**Q3.** What is peak time?
**A3.** Time to the first (maximum) overshoot peak = π/ω_d.

## Section B: Overshoot & Damping

**Q4.** Find %OS for ζ=0.5.
**A4.** %OS = 100·e^{−π·0.5/√(1−0.25)} = 100·e^{−1.813} = 16.3%.

**Q5.** Find ζ for %OS=25%.
**A5.** OS=0.25. ζ=−ln(0.25)/√(π²+ln²(0.25)) = 1.386/√(9.87+1.921) = 1.386/3.43 = 0.404.

**Q6.** For ζ=0.707, %OS?
**A6.** %OS=100·e^{−π·0.707/√(0.5)}=100·e^{−π}=4.32%.

## Section C: Time Computations

**Q7.** ω_n=10, ζ=0.5. Find ω_d, t_p, t_s(2%), t_s(5%).
**A7.** ω_d=10√0.75=8.66. t_p=π/8.66=0.363 s. t_s2%=4/(0.5·10)=0.8 s. t_s5%=3/5=0.6 s.

**Q8.** ω_n=5, ζ=0.6. Find t_r and t_d.
**A8.** ω_d=5√(0.64)=4. β=cos⁻¹(0.6)=53.1°=0.927 rad. t_r=(π−0.927)/4=2.215/4=0.554 s. t_d=(1+0.7·0.6)/5=1.42/5=0.284 s.

**Q9.** Poles at −4±j3. Find ω_n, ζ, ω_d, %OS.
**A9.** σ=4, ω_d=3. ω_n=√(16+9)=5. ζ=4/5=0.8. %OS=100·e^{−π·0.8/√0.36}=100·e^{−4.19}=1.52%.

**Q10.** ω_n=20, ζ=0.2. Find t_p and t_s(2%).
**A10.** ω_d=20√(0.96)=19.6. t_p=π/19.6=0.16 s. t_s=4/(0.2·20)=4/4=1.0 s.

## Section D: Steady-State Error & Error Constants

**Q11.** Unity feedback, G(s)=10/((s+2)(s+5)). Find type, K_p, e_ss(step).
**A11.** Type 0 (no pole at origin). K_p=10/(2·5)=1. e_ss=1/(1+1)=0.5.

**Q12.** G(s)=20/[s(s+4)] unity feedback. Type, K_v, e_ss(ramp).
**A12.** Type 1. K_v=lim s·GH=20/4=5. e_ss=1/5=0.2.

**Q13.** G(s)=8/[s²(s+3)]. Type, K_a, e_ss(parabolic).
**A13.** Type 2. K_a=lim s²·GH=8/3≈2.67. e_ss=1/(8/3)=0.375.

**Q14.** G(s)=5/[s(s+2)]. Find e_ss to step and ramp.
**A14.** Type 1. Step: e_ss=0. Ramp: K_v=5/2=2.5, e_ss=1/2.5=0.4.

**Q15.** A type 0 system has K_p=4. e_ss(step)?
**A15.** e_ss=1/(1+4)=0.2.

## Section E: Type Number & Error Summary

**Q16.** Which type gives zero error to a parabolic input?
**A16.** Type ≥3 (type 2 gives finite error 1/K_a).

**Q17.** Type 1 system — errors to step, ramp, parabolic?
**A17.** Step: 0. Ramp: 1/K_v (finite). Parabolic: ∞.

**Q18.** For G(s)=K/[s(s+4)(s+8)], find K such that ramp error = 0.05.
**A18.** Type 1. K_v = lim s·G = K/(4·8)=K/32. e_ss=1/K_v=32/K=0.05 → K=640.

## Section F: ISRO-Style

**Q19.** A second-order system has ω_n=4, ζ=0.5. Find t_p and %OS.
**A19.** ω_d=4·√0.75=3.464. t_p=π/3.464=0.907. %OS=100·e^{−π·0.5/√0.75}=16.3%.

**Q20.** If poles are −2±j2, find ζ, ω_n, and %OS.
**A20.** σ=2, ω_d=2. ω_n=√8=2.83. ζ=2/2.83=0.707. %OS=4.32%.

**Q21.** A system with ζ=0.7 and ω_n=10 — what is settling time (2%)?
**A21.** t_s=4/(0.7·10)=0.571 s.

**Q22.** Given %OS=50%, compute the damping ratio.
**A22.** OS=0.5. ζ=−ln(0.5)/√(π²+ln²0.5)=0.693/√(9.87+0.48)=0.693/3.217=0.215.

**Q23.** Determine the steady-state error for a ramp input to unity feedback G(s)=K/[s(s+2)(s+3)] with K=30.
**A23.** Type 1. K_v=K/(2·3)=30/6=5. e_ss(ramp)=1/5=0.2.

**Q24.** What is the effect of increasing ω_n on t_p?
**A24.** t_p decreases (t_p = π/ω_d ∝ 1/ω_n) — faster peak.

**Q25.** What happens to %OS if ζ is increased?
**A25.** %OS decreases (more damping → less overshoot).

## Common Mistakes
1. Using t_s=4/(ζω_n) for 5% criterion (that's 3/ζω_n).
2. Confusing ω_n with ω_d in t_p/t_r.
3. Forgetting %OS uses fraction (OS) not percentage in ln.
4. Applying formulas to overdamped (ζ>1) — formulas for underdamped only.
5. Mixing type number and order.
