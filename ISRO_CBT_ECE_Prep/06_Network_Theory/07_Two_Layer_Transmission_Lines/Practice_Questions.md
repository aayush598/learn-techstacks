# Two-Layer Transmission Lines - Practice Questions

## Instructions
Each question has one correct option. Assume a lossless quasi-TEM microstrip unless conductor or dielectric loss is explicitly mentioned.

## Questions

### Q1. Effective permittivity of homogeneous microstrip [Easy]
A dielectric substrate has `εᵣ=4`. The effective relative permittivity of microstrip on a homogeneous substrate is approximately:

A. 1  
B. 2.5  
C. 4  
D. 8

**Answer:** B  
**Explanation:** For homogeneous microstrip, `ε_eff=(εᵣ+1)/2=2.5`.

### Q2. Bounds on effective permittivity [Medium]
For a conventional microstrip on a substrate of relative permittivity `εᵣ>1`, neglecting fringing:

A. `1<ε_eff<εᵣ`  
B. `(εᵣ+1)/2≤ε_eff≤εᵣ`  
C. `ε_eff<1`  
D. `ε_eff=εᵣ` always

**Answer:** B  
**Explanation:** The quasi-TEM effective permittivity lies between the homogeneous value `(εᵣ+1)/2` and the substrate value `εᵣ`, with finite-conductor effects determining the exact value.

### Q3. Guided wavelength [Medium]
A microstrip has `ε_eff=2.5` and carries a 3 GHz signal. The guided wavelength is approximately:

A. 6.32 cm  
B. 10.0 cm  
C. 15.8 cm  
D. 25.0 cm

**Answer:** A  
**Explanation:** `v_p=c/√ε_eff=1.897×10⁸ m/s`; `λ_g=v_p/f=0.0632 m=6.32 cm`.

### Q4. Substrate-thickness trend [Medium]
With substrate permittivity and strip width held fixed, increasing substrate thickness generally:

A. Increases `Z₀`  
B. Decreases `Z₀`  
C. Sets `Z₀=50 Ω`  
D. Has no effect at any frequency

**Answer:** B  
**Explanation:** More dielectric beneath the strip increases capacitance per unit length and generally lowers the characteristic impedance.

### Q5. Width trend [Easy]
Holding substrate thickness and permittivity fixed, increasing microstrip width generally:

A. Decreases `Z₀`  
B. Increases `Z₀`  
C. Makes `Z₀` infinite  
D. Exactly doubles `Z₀`

**Answer:** A  
**Explanation:** A wider conductor has lower inductance and higher capacitance per unit length, resulting in lower `Z₀=√(L/C)`.

### Q6. Wide-line limit [Medium]
As microstrip width becomes very large compared with substrate thickness, the characteristic impedance approaches:

A. 0 Ω  
B. `1/√(ε_eff)` Ω  
C. 50 Ω  
D. `√(ε_r)` Ω

**Answer:** B  
**Explanation:** The wide-line limit is the parallel-plate value `Z₀→1/√(ε_eff)`, with the finite-conductor microstrip limit in practice.

### Q7. Quasi-TEM validity [Easy]
Microstrip quasi-TEM behavior is most accurate when:

A. `h≪λ` and `W≪λ`  
B. `h≫λ`  
C. `W≫λ` only  
D. The substrate is lossless only

**Answer:** A  
**Explanation:** The transverse dimensions must be small compared with wavelength for quasi-static TEM behavior.

### Q8. Dispersion [Medium]
A microstrip's effective permittivity generally increases with frequency because:

A. More field becomes confined within the substrate  
B. The conductor becomes dielectric  
C. Radiation increases  
D. The substrate thickness decreases

**Answer:** A  
**Explanation:** At higher frequency, fields are less able to spread into the surrounding air, so more electric field lies in the dielectric substrate and `ε_eff` rises.

### Q9. Dielectric loss [Easy]
A dielectric substrate has loss tangent `tanδ`. The approximate dielectric attenuation is proportional to:

A. `tanδ`  
B. `1/tanδ`  
C. `tan²δ` only  
D. Zero

**Answer:** A  
**Explanation:** Dielectric loss increases with loss tangent and with the fraction of electric energy stored in the substrate.

### Q10. Conductor loss trend [Easy]
For a fixed-width microstrip, increasing frequency generally makes the conductor-loss contribution:

A. Decrease because skin depth increases  
B. Remain exactly constant  
C. Increase because skin depth decreases  
D. Become zero

**Answer:** C  
**Explanation:** Skin depth `δ≈√(2/(ωμσ))` decreases with frequency, increasing conductor surface resistance and loss.

## Answer Key
1. B  
2. B  
3. A  
4. B  
5. A  
6. B  
7. A  
8. A  
9. A  
10. C
