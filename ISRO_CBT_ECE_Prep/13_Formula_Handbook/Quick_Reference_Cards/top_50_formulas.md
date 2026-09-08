# Quick Reference Card - Top 50 Must-Know Formulas

## Before Exam - Last Minute Review

---

## 1-10: Analog Circuits
1. Inverting amp: Av = -Rf/R1
2. Non-inverting amp: Av = 1 + Rf/R1
3. Schmitt UTP = +Vsat*R1/(R1+R2)
4. Wien bridge f = 1/(2*pi*RC), gain >= 3
5. Class B max efficiency = pi/4 = 78.5%
6. GBW = Gain * BW (constant)
7. SR = 2*pi*f*Vpeak
8. Crossover distortion in Class B, eliminated by Class AB
9. Feedback: Af = A/(1+A*beta)
10. Virtual ground: V+ = V- (with negative feedback)

## 11-20: Digital Circuits
11. De Morgan: (A+B)' = A'B', (AB)' = A'+B'
12. K-map Gray code: 00,01,11,10
13. JK FF: Q+ = JQ' + K'Q
14. D FF: Q+ = D
15. MUX for n vars: 2^(n-1):1 MUX
16. ADC SNR = 6.02n + 1.76 dB
17. MTBF = e^(Tsetup/tau)/(fclk*fdata*T0)
18. Metastability: setup/hold violation
19. Mod-n counter: n states, ceil(log2(n)) FF
20. VHDL: signal <=, variable :=

## 21-30: EM, Microwaves, Antennas
21. Z0 = sqrt(L/C) (transmission line)
22. Gamma = (ZL-Z0)/(ZL+Z0)
23. VSWR = (1+|Gamma|)/(1-|Gamma|)
24. Quarter-wave: Zin = Z0^2/ZL
25. Waveguide fc = c/(2a) for TE10
26. vp*vg = c^2
27. Friis: Pr = Pt*Gt*Gr*(lambda/4piR)^2
28. EIRP = Pt*Gt
29. Half-wave dipole Rr = 73 ohms
30. eta = sqrt(mu/epsilon) = 377 ohms (free space)

## 31-40: Communication Systems
31. AM power: P = Pc(1+mu^2/2)
32. AM efficiency: mu^2/(2+mu^2)
33. FM BW (Carson): 2*fm*(beta+1)
34. PCM SQNR = 6.02n + 1.76 dB
35. Shannon: C = B*log2(1+SNR)
36. Nyquist rate: fs >= 2*fmax
37. Noise power: N = kTB
38. Cascaded NF: F = F1+(F2-1)/G1
39. BPSK Pe = Q(sqrt(2Eb/N0))
40. Huffman: H <= L < H+1

## 41-50: Networks, Signals, Control, Others
41. RC tau = RC, RL tau = L/R
42. RLC resonance: f0 = 1/(2*pi*sqrt(LC))
43. Q = w0*L/R (series), Q = R/(w0*L) (parallel)
44. BW = f0/Q
45. x(t)*delta(t) = x(t) (convolution identity)
46. Routh-Hurwitz: no sign change = stable
47. Phase margin = 180 + angle at 0dB crossing
48. State space: G(s) = C(sI-A)^(-1)B + D
49. Buck: Vo = D*Vin, Boost: Vo = Vin/(1-D)
50. Vbi = (kT/q)*ln(NA*ND/ni^2)
