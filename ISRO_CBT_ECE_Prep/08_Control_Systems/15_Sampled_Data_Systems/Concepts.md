# Sampled Data Systems - Concepts

## 1. Introduction
- **Sampled-data systems** contain discrete-time signals, usually because a digital computer/controller is used.
- Signals are sampled at discrete instants (sampling instants), held between samples.
- Analysis uses the z-transform and z-plane rather than (only) s-plane.

## 2. Sampling & Reconstruction

### Sampling
- Continuous signal x(t) sampled at rate f_s = 1/T (T = sampling period).
- Sampled sequence: x[k] = x(kT).

### Ideal sampler output
x*(t) = Σ x(kT)·δ(t − kT)

## 3. Shannon/Nyquist Sampling Theorem
- To reconstruct a bandlimited signal x(t) (max frequency f_max) exactly, the sampling frequency must satisfy:
  **f_s ≥ 2·f_max**  (Nyquist rate)
- f_max = bandwidth. f_s/2 = Nyquist frequency.
- If f_s < 2f_max → **aliasing** (high frequencies fold into low-frequency range, distortion).

## 4. Aliasing
- Occurs when sampling below Nyquist rate.
- Different signals become indistinguishable.
- Prevention: anti-aliasing low-pass filter before sampling.

## 5. Zero-Order Hold (ZOH)
- The most common reconstruction: holds the sampled value constant until the next sample.
- Output is a staircase approximation.
- Transfer function (Laplace):
  **G_h0(s) = (1 − e^{−sT})/s**
- ZOH behaves like a low-pass filter with some phase lag.
- First-order hold reconstructs linearly between samples (better but more complex).

## 6. Z-Transform
- The discrete-time counterpart of the Laplace transform.
- Z{x[k]} = X(z) = Σ_{k=−∞}^∞ x[k]z^{−k}.
- Maps the digital signal to the z-domain.

### Common z-transforms
| x[k] | X(z) |
|---|---|
| δ[k] | 1 |
| u[k] (step) | z/(z−1) |
| a^k | z/(z−a) |
| k | z/(z−1)² |
| e^{−akT} = r^k (r=e^{−aT}) | z/(z−r) |

## 7. ZOH + Plant (Pulse Transfer Function)
- The z-transform of the sampled-data cascade (ZOH + continuous plant).
- Computed via: G(z) = (1−z^{−1})·Z{ G_p(s)/s }.

## 8. Sampling & s↔z Mapping
- z = e^{sT}.
- Stability boundary: s-plane jω axis maps to the unit circle |z|=1.
- LHP (Re(s)<0) maps to inside unit circle |z|<1.
- RHP maps to outside.

## 9. Stability in z-Plane
- A sampled-data (discrete) system is asymptotically stable ⇔ **all poles of the pulse transfer function lie INSIDE the unit circle |z|=1**.
- Poles on unit circle → marginally stable.
- Poles outside → unstable.

### Relationship to continuous stability
- Squeeze the s-plane LHP onto the unit disk.

## 10. Discrete Transfer Function (Pulse Transfer Function)
- Ratio of z-transforms of output to input (for sampled signals).
- G(z) = Y(z)/R(z).

### Closed-loop discrete system
T(z) = G(z)/[1 + G(z)H(z)]   (unity feedback analog)

## 11. Bilinear (Tustin) Approximation
- A method to convert a continuous transfer function to discrete form.
- Substitution: **s = (2/T)·[(z−1)/(z+1)]**
- Maps entire LHP to inside unit circle exactly (causal stable continuous → stable discrete).
- Good frequency fidelity ("frequency warping" occurs: ω_d = (2/T)tan(ω T/2)).

### Tustin substitution (forward/inverse)
- Discrete from continuous: replace s with (2/T)(z−1)/(z+1).
- Continuous from discrete: z = (1+sT/2)/(1−sT/2).

## 12. Other Discretization Methods (comparison)
- **Forward Euler**: s = (z−1)/T. Can map stable continuous to unstable discrete (not guaranteed stable).
- **Backward Euler**: s = (z−1)/(zT). Stable but distorts frequency.
- **Tustin (bilinear)**: stable mapping, best frequency preservation (with warping).

## 13. Difference Equation ↔ Transfer Function
Difference equation: y[k] + a₁y[k−1] + ... = b₀u[k] + ...
Takes z-transform to get G(z).

## 14. Sampled-Data Stability Tests
- z-plane: poles inside unit circle.
- Criterion transformation: substitute z = (w+1)/(w−1) → bilinear (w-plane) to use Routh in w-plane.
  - z → w mapping: z = (1+w)/(1−w)? variants; the key: unit circle maps to imaginary axis of w-plane. Then Routh applies.

## 15. Sampling Effect on System Performance
- Sampling adds time delay (half-period average) → reduces phase margin.
- Too-slow sampling can destabilize an otherwise stable controller.

## 16. ISRO Exam Relevance
- Sampling theorem / Nyquist rate.
- ZOH transfer function.
- z-transform pairs.
- Stability in z-plane (unit circle).
- Tustin / bilinear approximation.
- Discrete closed-loop transfer function.
