# Chapter 32 — Single-File Cheatsheet: All Formulas, Methods, Techniques

> **The idea in one line:** the entire GATE Analog Circuits syllabus compressed
> into one file. Every formula, every "method to memorise," every trap in a
> single glance. Revise this the night before the exam and scan it in the break
> before the paper.

---

## 0. Constants & unit facts

```
V_T = kT/q ≈ 25 mV @ 300 K        Vγ(Si) = 0.7 V, (Ge) = 0.3 V
gm(BJT) = 40·I_C[mA] mA/V         (1 mA → 40 mA/V)
20·log10 for voltage ratios       10·log10 for powers
1/√2 = 0.707   √2 = 1.414
20 dB/dec = 6 dB/oct
```

---

## 1. Circuit fundamentals

```
Ohm:  V = IR            KCL: ΣI_in = ΣI_out        KVL: ΣV_loop = 0
Series: R = R1+R2        Parallel: R = R1R2/(R1+R2) ; 1/R = Σ1/Ri
Voltage divider: V1 = V·R1/(R1+R2)
Current divider: I1 = I·R2/(R1+R2)
Thevenin: V_th (open-ckt) + R_th (sources killed: V→short, I→open)
Norton: I_N = V_th/R_th ; R_N = R_th
Source transform: V + R series ⇔ V/R current source ∥ R
Superposition: linear circuits only; never for power
Max power: R_L = R_th → P_max = V_th²/(4R_th)
Capacitors: series C1C2/(C1+C2), parallel C1+C2 (opposite of R)
Z_R = R ; Z_C = -j/ωC (current leads); Z_L = jωL (current lags)
Phasor: V = Vm∠φ ; 1/j = -j
RMS sine = Vm/√2 ; HWR RMS = Vm/2 ; FWR RMS = Vm/√2
τ = RC (or L/R) ; value(t) = final + (initial−final)e^{-t/τ}
```

---

## 2. Diodes

```
Shockley:      i_D = I_S(e^{v_D/nV_T} − 1)
Dynamic res.:  r_d = n·V_T/I_D ≈ 25mV/I_D
Models:  Ideal (ON=short, OFF=open) | CVD (ON=Vγ) | PWL (ON=Vγ+r_d·i_D)
Method: remove diode → check V_anode−V_cathode → ON(OFF)
Q-point: solve I = (V − V_D)/R (model drops)
Zener pair clipper: ±(Vz + 0.7) per side
```
### Clipper / clamper
```
Clipper: follows input until threshold, then flat (cuts shape)
  series: diode passes that half    shunt: diode shorts it
  conduction start: sin⁻¹(Vbias/Vm), end at π − start
Clamper: shifts whole wave; amplitude unchanged
  + clamper → bottom at 0 (or +V_ref) ; − clamper → top at 0 (−V_ref)
  silicon exact: clamp level is 0.7 (or V_ref+0.7)
  RC large ⇒ no droop ; RC small ⇒ exponential droop
```

---

## 3. Rectifiers (MEMORISE TABLE)

| | HWR | FWR (CT & bridge) |
|---|---|---|
| V_dc | Vm/π | 2Vm/π |
| V_rms | Vm/2 | Vm/√2 |
| γ (ripple) | 1.21 | 0.48 |
| η | 40.6% | 81.2% |
| f_ripple | f | 2f |
| PIV | Vm | CT: 2Vm ; bridge: Vm |

```
With diode drops: HWR (Vm−0.7)/π ; CT-FWR (Vm−0.7)·2/π ; bridge (Vm−1.4)·2/π
Cap filter: V_r ≈ I_dc/(f_r·C) ; V_dc ≈ Vm − V_r/2 ; γ ≈ V_r/V_dc
To halve ripple: double C (or halve I_dc)
```

---

## 4. BJT

```
I_E = I_C + I_B     α = I_C/I_E     β = I_C/I_B
β = α/(1−α)         α = β/(β+1)     I_E = (β+1)I_B
Active (NPN): V_C > V_B > V_E       V_BE ≈ 0.7
Saturation: V_CE(sat) ≈ 0.2 V       test: β·I_B > I_C(sat)
```
### Small-signal (at Q)
```
gm = I_C/V_T        rπ = β/gm         re = V_T/I_E ≈ V_T/I_C
rπ = (β+1)·re       ro = V_A/I_C
I_C=1mA,β=100 → gm=40m, rπ=2.5k, re=25Ω
```
### Amplifiers
```
CE (bypassed):    A_v = −gm·(R_C∥R_L) ; R_in = R1∥R2∥rπ ; R_out = R_C
CE (unbypass R_E):A_v = −gm·R_C/(1+gm·R_E) ≈ −R_C/R_E
                  R_in = R1∥R2∥(β+1)(re+R_E) ; R_out = R_C
CB:               A_v = +gm·(R_C∥R_L) ; R_in ≈ re ; R_out = R_C
CC (follower):    A_v = (R_E∥R_L)/(re+R_E∥R_L) ≈ 1
                  R_in = Bias∥(β+1)(re+R_E∥R_L) ; R_out ≈ re + R_s/(β+1)
Cascade:          A_tot = Π(loaded A_v) ; dB add
```

---

## 5. MOSFET

```
Saturation:  I_D = ½k(V_GS−V_th)² (1+λV_DS)     [k = μn·Cox·W/L]
Triode:      I_D = k[(V_GS−V_th)V_DS − V_DS²/2]
Cutoff:      V_GS ≤ V_th
Region:      sat iff V_DS ≥ V_GS − V_th
```
### Small-signal
```
gm = k(V_GS−V_th) = 2I_D/(V_GS−V_th) = √(2kI_D)
ro = 1/(λI_D)          gmb = η·gm (η ≈ 0.1–0.3)
Gate input R = ∞ (no gate current)
```
### Bias
```
Divider:  V_G = V_DD·R2/(R1+R2)   (exact — no gate current)
V_GS = V_G − I_D·R_S ; solve quadratic; verify saturation
Drain feedback: V_G = V_D
```
### Amplifiers
```
CS (bypassed):     A_v = −gm·(R_D∥R_L) ; R_in = R_G ; R_out = R_D
CS (unbypass R_S): A_v ≈ −R_D/R_S ; R_in = R_G
CG:                A_v = +gm·(R_D∥R_L) ; R_in ≈ 1/gm ; R_out = R_D
CD (follower):     A_v = R_S/(R_S + 1/gm) ≈ 1 ; R_out ≈ 1/gm ; R_in = R_G
Note: bypass cap present? → big-gm gain ; unbypassed → resistor-ratio gain
```

---

## 6. Current mirrors

```
BJT:   I_out ≈ I_ref·β/(β+2) ; R_out = ro ; ratio via R_E (I_out≈I_ref·R_E1/R_E2)
MOS:   I_out/I_ref = (W2/L2)/(W1/L1)
       with λ: I_out = I_ref·(1+λV_DS2)/(1+λV_DS1) ; R_out = 1/(λI_D)
Widlar: I_out ≈ (V_T/R_E)·ln(I_ref/I_out)
Compliance: BJT ~0.2 V ; MOS ~(V_GS−V_th)
Wilson = high R_out ; Cascode = high R_out ; Widlar = small current from big ref
```

---

## 7. Differential amplifier

```
v_id = v1−v2     v_icm = (v1+v2)/2 ; each branch I = I_tail/2
Ad (diff-out) BJT = −gm·R_C ; single-end = −gm·R_C/2
Ad MOS = −gm·(R_D∥ro)
Ac ≈ −R_C/(2·R_tail)
CMRR = Ad/Ac ; dB = 20·log10(CMRR) ; stiff tail ⇒ Ac→0, CMRR→∞
MOS pair: R_in = ∞ ; BJT pair: R_in = 2rπ
```

---

## 8. Op-amp

```
Ideal: A=∞, R_in=∞, R_out=0, offset=0, CMRR=∞, SR=∞, BW=∞
Virtual short (negative feedback + linear): v+ = v− ; input current = 0
Inverting:    A_v = −R_f/R1 ; R_in = R1
Non-inverting: A_v = 1 + R_f/R1 ; R_in = ∞
Follower:     A_v = +1
Summer:       v_o = −R_f·Σ(v_i/R_i)
Difference:   v_o = (R2/R1)(v2 − v1) (matched R's)
Integrator:   v_o = −(1/RC)∫v_in dt ; H = −1/(jωRC)
  practical: add R_f across C → DC gain −R_f/R1
Differentiator: v_o = −RC·dv_in/dt ; H = −jωRC
  practical: add R_s in series with C
SR limit: SR ≥ 2π·f_max·V_pk
Saturation: output at rail; virtual short breaks
Real op-amp: V_os error at out = V_os(1+R_f/R1) ; finite CMRR/GBW
```

---

## 9. Filters

```
1st LPF:    H = 1/(1+jf/f_c) ; f_c = 1/(2πRC) ; 20 dB/dec
1st HPF:    H = (jf/f_c)/(1+jf/f_c)
Roll-off:   20·order dB/dec (2nd = 40)
Butterworth: Q = 1/√2 ≈ 0.707 (maximally flat)
Sallen-Key (equal R,C, unity): ω_o = 1/RC ; Q = 1/3
Sallen-Key gain k: Q = 1/(3−k)   (k→3 ⇒ oscillation)
Band-pass:  Q = f_o/BW ; BW = f_H − f_L
```

---

## 10. Schmitt trigger & comparator

```
Comparator: open loop → output ±V_sat ; no virtual short
Non-inverting Schmitt (v− = V_ref):
  UT = V_ref + V_sat·R1/R_f
  LT = V_ref − V_sat·R1/R_f
  Hysteresis = UT − LT = 2·V_sat·R1/R_f
Purpose: dead band stops chatter / noise re-triggering
```

---

## 11. Feedback

```
A_f = A/(1+Aβ)  (negative)      A_f = A/(1−Aβ)  (positive)
Deep: A_f ≈ 1/β
Effects: gain ↓(1+Aβ) ; stability ↑ ; BW up ×(1+Aβ) ; distortion ↓(1+Aβ)
Topologies:
  series mixing → R_in ↑ ; shunt mixing → R_in ↓
  voltage sampling → R_out ↓ ; current sampling → R_out ↑
```

---

## 12. Oscillators

```
Barkhausen: |Aβ| = 1 AND ∠Aβ = 0°
Phase-shift: f_o = 1/(2πRC√6) ; min gain = 29
Wien bridge: f_o = 1/(2πRC) ; gain = 3
Colpitts:    f_o = 1/(2π√(L·C_eff)) ; C_eff = C1C2/(C1+C2)
Hartley:     f_o = 1/(2π√((L1+L2)·C))
Relaxation:  T = 2RC·ln(1 + 2R1/R2) ; thresholds ±V_sat·R1/(R1+R2)
Square (Schmitt) + integrator → triangle ; freq from RC & divider
Crystal: highest stability (Q 10⁴–10⁵)
```

---

## 13. AC coupling / frequency response

```
Coupling/bypass caps = high-pass poles: f = 1/(2π·C·R_eq)
  bypass R_eq ≈ re + R_B/(β+1)  [NOT R_E]
Miller (inverting only — CE/CS): C_M = C·(1 + |A|)
f_H ≈ 1/(2π·R_char·C_in_total)
Bandwidth = f_H − f_L
GBW = A_m·BW ≈ const
N identical stages: f_H,tot ≈ f_H·√(2^(1/N) − 1)
```

---

## 14. Switch

```
BJT: OFF=cutoff (V_CE≈V_CC) ; ON=saturation (V_CE≈0.2 V)
     saturation test: β·I_B ≥ I_C(sat)=(V_CC−0.2)/R_C
MOS: OFF (V_GS<V_th) ; ON=triode R_ds(on)=1/[k(V_GS−V_th)]
BJT turn-off slow (storage time) ; MOSFET fast — favours switching CKT
```

---

## 15. Universal method (the whole subject in 4 steps)

```
① DC Q-point (open caps, kill AC; pick region; VERIFY active/sat)
② Small-signal params (gm, rπ/re, ro — from Q)
③ AC equivalent (short midband caps, ground supplies, replace device)
④ Solve v_out/v_in, R_in, R_out, bandwidth
```

---

## 16. Critical exam-day reminders (trap list)

```
- CE/CS inverts; CB/CG/CD/CC do NOT.
- Miller is inverting-only. Gain units mA/V × kΩ = V/V.
- HWR V_dc = Vm/π (avg) ≠ Vm/2 (rms). Always half vs full first.
- CT-FWR PIV = 2Vm ; bridge = Vm.
- Divider bias: approximate OK iff β·R_E ≳ 10·R2.
- Always verify the region after solving a transistor problem.
- Bypassed vs unbypassed R_E/R_S flips gain between −gm·R and ≈−R/R.
- Non-inverting gain has the "1 +". Inverting has not.
- Saturation kills the virtual short.
- Schmitt thresholds: V_ref ± V_sat·R1/R_f (hysteresis = difference).
- Colpitts series C ; Hartley series L.
- MOSFET gate current = 0 (never write I_G in solutions).
- 20 dB/dec per pole; 40 ⇒ two poles.
```

---

**Done — put this file beside your exam answer sheet and next to
`31-Practice-Bank-Every-Pattern.md` after a weekend of drills. Good luck.**