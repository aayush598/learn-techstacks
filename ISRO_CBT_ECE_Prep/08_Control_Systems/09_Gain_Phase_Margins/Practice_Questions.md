# Gain & Phase Margins - Practice Questions

## Section A: Conceptual

**Q1.** Define gain margin and where it is evaluated.
**A1.** GM is the factor by which open-loop gain can rise before instability, evaluated at the phase crossover frequency (phase=−180°).

**Q2.** Define phase margin.
**A2.** PM is the additional phase lag that causes instability, evaluated at the gain crossover frequency (|GH|=1).

**Q3.** What are typical good design values for GM and PM?
**A3.** PM 30–60° (target ~45°), GM ≥ 6 dB (typically 6–12 dB).

**Q4.** For a stable (P=0) system, what do positive GM and PM indicate?
**A4.** Closed-loop stability.

## Section B: Computing Margins

**Q5.** Phase crossover at ω=10 where |GH|=2. Find GM in linear and dB.
**A5.** GM=1/2=0.5 (linear) → −6 dB. Negative → unstable.

**Q6.** At gain crossover ω=5, phase=−140°. Find PM.
**A6.** PM = 180° + (−140°) = 40°.

**Q7.** At phase crossover |GH| = 0.2. Find GM.
**A7.** GM = 1/0.2 = 5 (linear) = 20log(5) = 13.98 dB. Stable.

**Q8.** Phase at gain crossover = −100°. PM?
**A8.** PM = 180−100 = 80°.

**Q9.** GM = +8 dB. Convert to linear.
**A9.** 20log(GM_lin)=8 → GM_lin = 10^(8/20)=10^0.4 ≈ 2.51.

## Section C: PM ↔ ζ ↔ Overshoot

**Q10.** Estimate the damping ratio for PM=45°.
**A10.** ζ ≈ 45/100 = 0.45.

**Q11.** For ζ=0.5, estimate PM and overshoot.
**A11.** PM ≈ 50°, OS = 100·e^{−π·0.5/√(1−0.25)} = 100·e^{−1.813} = 100·0.163 = 16.3%.

**Q12.** A system has 25% overshoot. Estimate ζ and the required PM.
**A12.** OS=0.25 → ln(0.25)=−1.386=−πζ/√(1−ζ²). ζ/√(1−ζ²)=0.441 → ζ≈0.4. PM≈40°.

**Q13.** Find PM for ζ=0.3.
**A13.** PM ≈ 30° (approx). OS=100·e^{−π0.3/√(0.91)}=100·e^{−0.987}=37%.

**Q14.** A second-order system has PM=60°. Estimate ζ.
**A14.** ζ ≈ 0.6.

## Section D: Effect of Gain & Delay

**Q15.** Increasing open-loop gain generally does what to PM?
**A15.** Reduces PM (gain crossover shifts to higher frequency where phase is more negative).

**Q16.** A system has PM=50° and gain crossover at ω=10. A transport delay of 0.02 s is added. New PM?
**A16.** Delay phase = 57.3·10·0.02 = 11.46°. New PM = 50−11.46 = 38.54°.

**Q17.** For the above, would the system remain stable?
**A17.** Yes, PM still positive (38.5°), but margin reduced.

## Section E: ISRO-Style

**Q18.** A unity feedback system has open-loop G(s)=K/(s(s+2)(s+4)). Find K for PM=45°.
**A18.** |G|dB → compute phase: −90°−atan(ω/2)−atan(ω/4). For PM=45, phase=−135° → atan(ω/2)+atan(ω/4)=45°. Try ω=2: atan(1)+atan(0.5)=45+26.6=71.6 (too high). ω=2.5: atan1.25+atan0.625=51.3+32=83.3. ω small... Solve atan(ω/2)+atan(ω/4)=45 → ω≈? atan(ω/2)=A, atan(ω/4)=B, A+B=45. tan(A+B)=(ω/2+ω/4)/(1−(ω/2)(ω/4))=1 → (3ω/4)/(1−ω²/8)=1 → 3ω/4 = 1−ω²/8 → multiply 8: 6ω=8−ω² → ω²+6ω−8=0 → ω=[−6+√(36+32)]/2=[−6+8.246]/2=1.123. Hmm that gives negative phase sum? Let me recheck: at ω=1.123, atan(0.56)=29.3, atan(0.28)=15.7, sum=45. ✓. Phase=−90−45=−135 → PM=45. Now |G|=K/[1.123·√(1.26)·√(4.26)]=K/[1.123·1.123·2.06]=K/2.6. Set=1 → K=2.6.

**Q19.** Given G(s)=10/[s(1+0.1s)], find GM.
**A19.** Phase=−90°−atan(0.1ω). For −180: atan(0.1ω)=90 → 0.1ω=∞ → no finite. Phase→−180 only as ω→∞. So GM=+∞ (no crossing). Stable.

**Q20.** A type 1 system has PM=40°. Roughly what ζ does it correspond to? What overshoot?
**A20.** ζ≈0.4. OS≈25%.

**Q21.** For a system with GM=+∞ and PM=∞, classify stability.
**A21.** Very robustly stable (phase never reaches −180° and magnitude never below... typically first-order). Very well damped, no oscillation.

**Q22.** A system with negative GM but positive PM — is it stable?
**A22.** For P=0 systems, a negative GM normally implies instability; but signs can conflict when there are multiple crossings. Generally inconsistent margins indicate caution.

**Q23.** Typical required phase margin for a servo control design?
**A23.** 40–60° (commonly 45°).

**Q24.** If PM is too large (e.g., 80°), what design trade-off occurs?
**A24.** Sluggish response but robust; reduced overshoot, slower settling.

**Q25.** Compute PM for G(jω) with magnitude 1 at ω=6 and phase −165°.
**A25.** PM = 180−165 = 15° (small margin → near oscillatory).

## Common Mistakes
1. Using the wrong crossover (gain vs phase).
2. Mistaking sign of dB gain margin.
3. Applying PM≈100ζ beyond its valid range (ζ<0.6).
4. Forgetting delay phase in computing PM.
5. Assuming positive margins guarantee stability for non-minimum phase systems.

## Section H: Margin Numericals (Direct)

**Q26.** A Bode plot shows −14 dB magnitude at the phase crossover (ω=ω_pc). Find GM.
**A26.** GM = −(−14) = +14 dB. Convert: 10^(14/20) = 5.01 (linear). Stable.

**Q27.** GM=12 dB. Maximum gain increase possible (linear)?
**A27.** 12 dB → 10^(12/20)=10^0.6 ≈ 3.98×.

**Q28.** A gain of 25 dB is at ω_pc for a system with GM=+8 dB. If you double the gain, what's the new GM?
**A28.** Doubling = +6 dB: new GM = 8 − 6 = +2 dB (still stable but slim).

**Q29.** PM drops from 60° to 20° when gain is raised. What is implied about robustness to gain?
**A29.** Lower PM → closer to instability; delay sensitivity increased.

## Section I: Margin-Spec Design Checks

**Q30.** A servo spec requires OS ≤ 10%. Approx min PM needed?
**A30.** OS=0.1 → ζ≈0.59 (from tables) → PM ≈ 60°.

**Q31.** If PM=30° is measured, estimate ζ and OS.
**A31.** ζ≈0.3 → OS≈37%.

**Q32.** With ω_gc=50 rad/s and PM=45°, what transport delay brings it to PM=15°?
**A32.** ΔPM=30°=0.524 rad. T=0.524/50=0.0105 s.

**Q33.** Two systems: A PM=20°, B PM=70°. Which is more robust to model error but slower?
**A33.** B (higher PM → more robust, slower).

**Q34.** A conditionally stable system arises when the phase crosses −180° at two distinct frequencies. What does the middle stability region imply?
**A34.** Stable only for an intermediate gain band.

## Margin Decision Table
| Observed | Likely issue | Fix |
|---|---|---|
| PM too low | overshoot, near instability | lead compensation |
| GM too low | gain sensitivity | reduce gain or add compensation |
| PM high & slow | sluggish | increase gain / lead |
| large e_ss | accuracy | lag / PI |
