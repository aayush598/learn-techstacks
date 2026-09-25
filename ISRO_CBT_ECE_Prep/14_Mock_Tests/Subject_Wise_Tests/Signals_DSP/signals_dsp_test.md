# Subject-Wise Test - Signals, Systems and DSP

## 20 Questions, 25 Minutes, +1/−0.33

## Questions

**Q1.** Convolution with `δ(t)` produces:

A. 0  
B. The time derivative of the signal  
C. The original signal  
D. The signal integral

**Q2.** If `X(ω)` is the Fourier transform of `x(t)`, then `x(t−t₀)` transforms to:

A. `X(ω)`  
B. `e⁻ʲωt₀X(ω)`  
C. `e⁺ʲωt₀X(ω)`  
D. `ωX(ω)`

**Q3.** Multiplication by `e⁺ʲω₀t` causes a frequency shift:

A. By `−2ω₀`  
B. By `−ω₀` only  
C. By `+ω₀`  
D. To zero

**Q4.** Parseval's theorem relates time-domain and frequency-domain energies through:

A. Equality of the squared L2 norms  
B. The sum of eigenvalues  
C. Pole locations  
D. ROC radius

**Q5.** The Laplace transform of `e⁻ᵃᵗu(t)` is:

A. `1/(s−a)`  
B. `1/(s+a)`, ROC `Re(s)>−a`  
C. `1/(a−s)` only  
D. `s/(s+a)`

**Q6.** For a rational causal continuous-time LTI system, BIBO stability requires poles to lie:

A. In the right half-plane  
B. Only on the imaginary axis  
C. Strictly in the left half-plane  
D. At zero

**Q7.** A causal right-sided Z-transform has an ROC:

A. Inside the smallest nonzero pole  
B. Outside the largest pole in magnitude  
C. Always the full plane  
D. Only at `|z|=1`

**Q8.** A left-sided anti-causal rational Z-transform generally has an ROC:

A. Inside the smallest nonzero pole  
B. Outside the largest pole  
C. Between every pole and zero  
D. Outside the unit circle only

**Q9.** A DTFT is:

A. Discrete-time and generally nonperiodic  
B. Continuous-time and periodic  
C. Discrete-time and generally periodic  
D. Always finite-duration

**Q10.** The N-point DFT produces N frequency samples for:

A. N time samples  
B. N/2 time samples only  
C. N² time samples  
D. One time sample

**Q11.** A radix-2 FFT of 4096 points has how many stages?

A. 10  
B. 11  
C. 12  
D. 4096

**Q12.** A radix-2 FFT butterfly stage requires how many complex multiplications for `N/2` independent butterflies?

A. `N`  
B. `N/2`  
C. `N²`  
D. 2

**Q13.** In convolution, multiplication in one domain corresponds to:

A. Convolution in the other domain  
B. Addition in the other domain only  
C. Differentiation in both domains  
D. Sampling in both domains

**Q14.** The system `y[n]=0.5y[n−1]+x[n]` has transfer function:

A. `H(z)=1/(1−0.5z⁻¹)`  
B. `H(z)=1/(1+0.5z⁻¹)` only  
C. `H(z)=1−0.5z⁻¹`  
D. `H(z)=z/2`

**Q15.** A causal discrete-time rational system is BIBO stable when all poles are:

A. Outside the unit circle  
B. Inside the unit circle  
C. Exactly on the unit circle  
D. At the origin only

**Q16.** Sampling a 9 kHz sinusoid at 12 ksample/s creates an alias at:

A. 3 kHz  
B. 6 kHz  
C. 9 kHz only  
D. 12 kHz

**Q17.** Ideal uniform quantization SQNR increases by approximately:

A. 6 dB per bit  
B. 1 bit per bit  
C. 20 dB per bit  
D. 3 dB per bit

**Q18.** Before decimating by integer factor `M`, a signal should be:

A. Low-pass filtered below the new Nyquist frequency  
B. Differentiated once  
C. Modulated only  
D. Quantized to 1 bit

**Q19.** Interpolation inserts additional samples and generally requires:

A. Reconstruction filtering  
B. Only random noise  
C. A zero-order hold with no reconstruction  
D. A lower sampling rate

**Q20.** Every finite-length FIR filter is BIBO stable because its impulse response is:

A. Absolutely summable  
B. Always infinite  
C. Strictly increasing  
D. Undefined

## Answer Key

| Question | Answer | Question | Answer |
|---:|:---:|---:|:---:|
| 1 | C | 11 | C |
| 2 | B | 12 | B |
| 3 | C | 13 | A |
| 4 | A | 14 | A |
| 5 | B | 15 | B |
| 6 | C | 16 | A |
| 7 | B | 17 | A |
| 8 | A | 18 | A |
| 9 | C | 19 | A |
| 10 | A | 20 | A |

## Quick Solutions

2. The time-shift factor is `e⁻ʲωt₀`.  
11. `log₂4096=12`.  
12. A standard radix-2 butterfly uses one complex multiplication.  
16. The alias frequency is `|9−12|=3 kHz`.  
17. `SQNR≈6.02n+1.76 dB`, so each bit adds about 6 dB.
