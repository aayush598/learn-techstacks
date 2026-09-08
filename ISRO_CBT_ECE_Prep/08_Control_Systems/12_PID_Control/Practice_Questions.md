# PID Control - Practice Questions

## Section A: Conceptual

**Q1.** Write the time-domain PID control law.
**A1.** u(t) = K_p·e(t) + K_i·∫e(t)dt + K_d·de(t)/dt.

**Q2.** Which PID action eliminates steady-state error?
**A2.** Integral (I) action.

**Q3.** What is the main disadvantage of derivative action?
**A3.** Amplifies high-frequency noise.

**Q4.** What happens with too much integral action?
**A4.** Can cause oscillation / instability and integral windup.

## Section B: Transfer Functions

**Q5.** Find G_c(s) for a PI controller.
**A5.** G_c(s) = K_p + K_i/s = K_p(1 + 1/(T_i·s)).

**Q6.** Given K_p=4, K_i=2, K_d=0.5, write G_c(s).
**A6.** G_c(s) = 4 + 2/s + 0.5s = (0.5s²+4s+2)/s.

**Q7.** Find T_i and T_d for K_p=10, K_i=5, K_d=2.
**A7.** T_i = K_p/K_i = 2. T_d = K_d/K_p = 0.2.

**Q8.** For K_p=3, T_i=1.5, T_d=0.25, find K_i and K_d.
**A8.** K_i = K_p/T_i = 3/1.5 = 2. K_d = K_p·T_d = 3·0.25 = 0.75.

## Section C: Effects of Each Term

**Q9.** Which controller (P, I, or D) leaves a steady-state offset for step input?
**A9.** P alone (proportional) leaves offset.

**Q10.** Which action increases phase margin / provides anticipation?
**A10.** Derivative (adds phase lead, anticipates error change).

**Q11.** Which action adds phase lag?
**A11.** Integral (adds 90° at all freq, phase lag).

**Q12.** Increasing K_p generally does what to overshoot?
**A12.** Increases overshoot (and reduces offset but not to zero).

## Section D: Ziegler-Nichols

**Q13.** In Z-N closed-loop method, what is recorded?
**A13.** Ultimate gain K_u and ultimate period P_u (from sustained oscillation using P-only).

**Q14.** K_u=10, P_u=4. Find ZN PID gains (K_p, T_i, T_d, K_i, K_d).
**A14.** K_p=0.6·10=6. T_i=4/2=2. T_d=4/8=0.5. K_i=K_p/T_i=3. K_d=K_p·T_d=3.

**Q15.** K_u=30, P_u=6. Find ZN PI gains.
**A15.** K_p=0.45·30=13.5. T_i=6/1.2=5. K_i=K_p/T_i=2.7.

**Q16.** In reaction-curve method, K=2, T=4, L=1. Find ZN PID gains.
**A16.** K_p=1.2·T/(K·L)=1.2·4/(2·1)=2.4. T_i=2L=2. T_d=0.5L=0.5.

## Section E: Steady-State / Type Impact

**Q17.** A type-0 plant with a PI controller — what's the resulting type and step error?
**A17.** Type increases to 1 → zero steady-state error to step.

**Q18.** How does adding integral action affect the open-loop type number?
**A18.** Increases by 1 (adds a pole at origin).

**Q19.** A pure P controller on a type-0 plant leaves what step error?
**A19.** Finite (nonzero) — cannot be eliminated with P alone.

## Section F: Digital Implementation

**Q20.** Write the discrete derivative using backward difference.
**A20.** de/dt ≈ (e[k] − e[k−1])/T_s.

**Q21.** Write the incremental (velocity) PID update formula.
**A21.** Δu[k] = K_p(e[k]−e[k−1]) + K_i·T_s·e[k] + (K_d/T_s)(e[k]−2e[k−1]+e[k−2]).

**Q22.** Advantage of velocity-form PID over positional?
**A22.** Avoids reset/integral windup on actuator saturation; smoother switching.

## Section G: ISRO-Style

**Q23.** Which controller gives the fastest response but leaves offset?
**A23.** P controller.

**Q24.** A controller combines the ability to remove steady-state error and reduce overshoot — identify.
**A24.** PID (PI removes error, D reduces overshoot).

**Q25.** G_c(s)=(s²+6s+5)/s. Identify the controller type and terms.
**A25.** Numerator (s²+6s+5) → K_d=1, K_p=6, K_i=5. It's a PID controller.

**Q26.** What is integral windup and one remedy?
**A26.** Integrator keeps accumulating during actuator saturation causing overshoot; remedy = anti-windup/clamping.

**Q27.** A derivative filter is often added. Why?
**A27.** To limit high-frequency noise amplification of ideal derivative.

**Q28.** In the Z-N closed loop method, why disable I and D first?
**A28.** To get a clean sustained oscillation from proportional gain alone, determining K_u and P_u.

## Common Mistakes
1. Confusing K_i ↔ K_p/T_i conversion.
2. Forgetting PID adds a pole at origin.
3. Using wrong Z-N table (open vs closed loop).
4. Thinking P eliminates steady-state error (it doesn't; I does).
5. Ignoring derivative noise sensitivity.
