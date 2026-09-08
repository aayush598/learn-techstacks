# Sampled Data Systems - Practice Questions

## Section A: Conceptual

**Q1.** State the sampling theorem (Nyquist).
**A1.** To reconstruct a bandlimited signal exactly, the sampling frequency must be at least twice the highest frequency: f_s ≥ 2·f_max.

**Q2.** What is aliasing and when does it occur?
**A2.** Distortion where high frequencies fold into low-frequency range; occurs when sampling below the Nyquist rate.

**Q3.** What is the transfer function of a Zero-Order Hold?
**A3.** G_h0(s) = (1 − e^{−sT})/s.

**Q4.** What is the stability condition for a sampled-data system in the z-plane?
**A4.** All poles of the pulse transfer function must lie inside the unit circle |z|<1.

## Section B: Sampling Theorem

**Q5.** A signal has bandwidth 5 kHz. Find minimum sampling frequency.
**A5.** f_s ≥ 2·5 = 10 kHz.

**Q6.** A signal with max frequency 100 Hz is sampled at 150 Hz. What happens?
**A6.** f_s=150 < 2·100=200 → below Nyquist → aliasing.

**Q7.** Sampling frequency 2 kHz. What max signal frequency can be reconstructed?
**A7.** f_max = f_s/2 = 1 kHz.

## Section C: Z-Transforms

**Q8.** Find Z-transform of the unit step u[k].
**A8.** X(z) = z/(z−1).

**Q9.** Find Z-transform of a^k.
**A9.** X(z) = z/(z−a).

**Q10.** Find Z-transform of e^{−3k}.
**A10.** Let a=e^{−3}. X(z)=z/(z−e^{−3}).

**Q11.** Find the z-transform of x[k]=2δ[k]+3u[k].
**A11.** X(z)=2+3z/(z−1) = (2(z−1)+3z)/(z−1)=(5z−2)/(z−1).

**Q12.** Inverse z-transform of X(z)=z/(z−4).
**A12.** x[k]=4^k (for k≥0).

## Section D: Stability in z-Plane

**Q13.** A discrete system has pole at z=0.5. Stable?
**A13.** Yes (|z|<1, inside unit circle).

**Q14.** Pole at z=1.2. Stability?
**A14.** Outside unit circle → unstable.

**Q15.** Pole at z=−1. Stability?
**A15.** |z|=1 on unit circle → marginally stable (oscillation).

**Q16.** G(z)=1/(z−2). Stable?
**A16.** Pole z=2 outside unit circle → unstable.

**Q17.** G(z)=z/((z−0.5)(z−1.5))? Stability?
**A17.** Poles 0.5 (inside) and 1.5 (outside) → unstable.

## Section E: Tustin / Bilinear

**Q18.** Apply Tustin to convert s-plane pole s=−2 to z with T=0.1.
**A18.** Inv bilinear: z=(1+sT/2)/(1−sT/2). s=−2: z=(1−0.1)/(1+0.1)=0.9/1.1=0.818 (inside unit circle ✓ stable).

**Q19.** For Tustin, what's the substitution for s?
**A19.** s = (2/T)·(z−1)/(z+1).

**Q20.** Frequency warping: continuous ω=1, T=0.1. Discrete ω_d?
**A20.** ω_d=(2/T)tan(ωT/2)=(2/0.1)tan(0.05)=20·0.05=1.0 (approx for small ωT).

## Section F: Discrete Transfer Functions

**Q21.** Difference equation y[k]+0.5y[k−1]=u[k]. Find G(z).
**A21.** z-transform: Y(z)+0.5z^{−1}Y(z)=U(z) → Y(z)(1+0.5z^{−1})=U(z) → G(z)=1/(1+0.5z^{−1})=z/(z+0.5).

**Q22.** G(z)=z/(z−0.5) in unity feedback. Find T(z) and stability.
**A22.** T(z)=G/(1+G)=[z/(z−0.5)]/[1+z/(z−0.5)]=z/(2z−0.5). Pole: 2z−0.5=0→z=0.25 inside unit circle → stable.

**Q23.** Cascade G₁(z) and G₂(z). Total?
**A23.** G(z)=G₁(z)·G₂(z).

## Section G: ISRO-Style

**Q24.** A control signal is sampled at 1 kHz. What's the sampling period and Nyquist frequency?
**A24.** T=1 ms. f_N=f_s/2=500 Hz.

**Q25.** Explain why the LHP of s-plane maps to inside the unit circle in z-plane.
**A25.** z=e^{sT}; for Re(s)<0, |z|=e^{Re(s)T}<1 → inside unit circle.

**Q26.** A discrete system G(z)=K/(z−0.9). For what K range is it stable?
**A26.** Pole fixed at z=0.9 (inside unit circle) regardless of K (K is numerator). Stable for all K≠0 (gain only scales). Actually pole=0.9 → always stable.

**Q27.** Convert continuous G(s)=1/(s+1), T=0.5, using Tustin.
**A27.** s=(2/0.5)(z−1)/(z+1)=4(z−1)/(z+1). G(z)=1/(4(z−1)/(z+1)+1)= (z+1)/(4z−4+z+1)=(z+1)/(5z−3).

**Q28.** Pole z=1 on unit circle — what continuous equivalent?
**A28.** s=0 (integrator) → marginal stability.

**Q29.** Why does sampling reduce phase margin in continuous design?
**A29.** The ZOH adds a time delay (~T/2), which adds phase lag → reduces phase margin.

## Common Mistakes
1. Sampling below Nyquist → aliasing.
2. Forgetting z=0 inside unit circle is stable.
3. Confusing forward/backward Euler with Tustin.
4. ZOH TF misremembered as (1−e^{−sT})/s incorrect occasionally.
5. Applying continuous BIBO (LHP) test to z-plane (should be unit circle).
