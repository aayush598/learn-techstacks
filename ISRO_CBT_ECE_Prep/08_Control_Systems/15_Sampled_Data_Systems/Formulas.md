# Sampled Data Systems - Formulas

## 1. Sampling Frequency / Period
f_s = 1/T (Hz),  ω_s = 2π/T (rad/s)

## 2. Nyquist / Shannon Theorem
f_s ≥ 2·f_max  (Nyquist rate)
ω_s ≥ 2·ω_max

## 3. Nyquist Frequency
f_N = f_s/2

## 4. Sampling of Continuous Signal
x*[k] = x(kT)
Ideal sampler (Laplace): X*(s) = Σ_{k=0}^∞ x(kT)e^{−skT}

## 5. Z-Transform
X(z) = Z{x[k]} = Σ_{k=−∞}^∞ x[k] z^{−k}

### Properties
- Linearity: Z{a x[k]+b y[k]} = aX(z)+bY(z)
- Time shift (delay): Z{x[k−1]} = z^{−1}X(z)
- Advance: Z{x[k+1]} = zX(z) − z·x[0]
- Initial value: x[0] = lim_{z→∞} X(z)
- Final value (if poles inside unit circle): x[∞] = lim_{z→1} (1−z^{−1})X(z)

## 6. Common Z-Transform Pairs
| x[k] | X(z) | ROC |
|---|---|---|
| δ[k] | 1 | all z |
| u[k] | z/(z−1) | |z|>1 |
| a^k | z/(z−a) | |z|>|a| |
| k | z/(z−1)² | |z|>1 |
| k·a^k | az/(z−a)² | |z|>|a| |
| r^k·cos(...) etc. | combos | |

### From exponentials with T
e^{−akT} = (e^{−aT})^k = r^k → X(z) = z/(z−r), r=e^{−aT}

## 7. Zero-Order Hold Transfer Function
G_h0(s) = (1 − e^{−sT})/s

## 8. Pulse Transfer Function with ZOH + Plant
G(z) = (1 − z^{−1}) · Z{ G_p(s)/s }

(Compute Z-transform of the step response of the plant using tables.)

## 9. Closed-Loop Discrete Transfer Function (unity feedback)
T(z) = G(z)/[1 + G(z)]

General: T(z) = G(z)/[1 + G(z)H(z)]

## 10. Stability in z-Plane
- Stable ⇔ all poles of G(z) inside unit circle |z| < 1.
- Unit circle = marginal stability boundary.
- z = e^{sT} mapping.

### Mapping details
- jω axis (s) → unit circle (z).
- LHP → inside unit circle.
- RHP → outside.

## 11. Bilinear (Tustin) Transformation
s = (2/T)·[(z−1)/(z+1)]

### Inverse
z = (1 + sT/2)/(1 − sT/2)

### Frequency warping
ω (continuous) → ω_d (discrete effective):
ω_d = (2/T)·tan(ω·T/2)

## 12. Other Discretization Formulas

### Forward Euler
s = (z−1)/T

### Backward Euler
s = (z−1)/(z·T)

## 13. z-Transform of Difference Equation
Given: y[k] + a₁y[k−1]+...+a_n y[k−n] = b₀u[k]+...+b_m u[k−m]
Apply delay: z^{−i} corresponds to [k−i].
G(z) = (b₀+b₁z^{−1}+...+b_m z^{−m})/(1+a₁z^{−1}+...+a_n z^{−n})

Multiplying by z^n: G(z)=z^{n−m}·(b₀ z^m+...)/(z^n+...).

## 14. Routh in w-plane (discrete stability test)
Apply bilinear: z = (1+w)/(1−w)  (or z=(w+1)/(w−1) per convention).
- Unit circle |z|=1 maps to imaginary axis of w-plane.
- Inside unit circle maps to LHP of w-plane.
- Then apply Routh-Hurwitz on w-plane polynomial.

## Formula Cheatsheet (Sampled Data)
| Quantity | Formula |
|---|---|
| Nyquist rate | f_s ≥ 2 f_max |
| ZOH | (1−e^{−sT})/s |
| ZOH+plant | (1−z^{−1})Z{G_p/s} |
| Discrete stability | poles inside unit circle |
| z = e^{sT} | s↔z map |
| Tustin | s=(2/T)(z−1)/(z+1) |
| Forward Euler | s=(z−1)/T |
| Backward Euler | s=(z−1)/(zT) |
| Closed loop | G(z)/(1+G(z)) |

## Notes
- For impulse-invariance method (alternative):
  G(z) = Z{continuous impulse response h(t) sampled}.
- Frequency warping important in digital filter/controller design.
