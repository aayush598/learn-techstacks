# Carrier Mobility & Scattering - Formulas

## Basic Mobility Relations

### Definition
$$\mu = \frac{v_d}{E} \quad \text{(cm}^2\text{/V·s)}$$

### Einstein Relation
$$\frac{D}{\mu} = \frac{kT}{q} = V_T$$

### Diffusion Coefficients
$$D_n = \mu_n V_T$$
$$D_p = \mu_p V_T$$

---

## Drift Velocity

### Low Field
$$v_d = \mu E$$

### High Field (Empirical)
$$v_d = \frac{\mu E}{1 + \mu E/v_{sat}}$$

### Saturation Velocity
$$v_{sat} \approx 10^7 \text{ cm/s (Si)}$$

### Critical Field
$$E_{sat} = \frac{2v_{sat}}{\mu_n}$$

---

## Scattering Mechanisms

### Matthiessen's Rule
$$\frac{1}{\mu} = \frac{1}{\mu_L} + \frac{1}{\mu_I} + \frac{1}{\mu_N}$$

### Lattice Scattering
$$\mu_L \propto T^{-3/2}$$

### Ionized Impurity Scattering
$$\mu_I \propto \frac{T^{3/2}}{N_I}$$

### Neutral Impurity Scattering
$$\mu_N \propto \frac{1}{N_N}$$

---

## Mobility-Doping Relation

### Empirical Formula
$$\mu = \frac{\mu_0}{1 + \left(\frac{N}{N_{ref}}\right)^\gamma}$$

### Parameters (Si, 300K)
| Carrier | μ₀ (cm²/V·s) | Nref (cm⁻³) | γ |
|---------|--------------|-------------|---|
| Electrons | 92 | 1.3 × 10¹⁷ | 0.91 |
| Holes | 54 | 2.35 × 10¹⁷ | 0.88 |

### Approximate (Low Doping)
$$\mu \approx \mu_0 \quad \text{for } N << N_{ref}$$

### Approximate (High Doping)
$$\mu \approx \mu_0 \left(\frac{N_{ref}}{N}\right)^\gamma \quad \text{for } N >> N_{ref}$$

---

## Temperature Dependence

### Combined Mobility
$$\mu(T) = \frac{\mu_L(T) \mu_I(T)}{\mu_L(T) + \mu_I(T)}$$

### High Temperature (Lattice Dominant)
$$\mu(T) \approx \mu_L(T) = \mu_L(T_0) \left(\frac{T_0}{T}\right)^{3/2}$$

### Low Temperature (Impurity Dominant)
$$\mu(T) \approx \mu_I(T) = \mu_I(T_0) \left(\frac{T}{T_0}\right)^{3/2}$$

### Room Temperature
$$\mu(T) \approx \mu(300K) \left(\frac{300}{T}\right)^n$$

Where n ≈ 1.5-2.5 (depends on doping)

---

## Effective Mobility (MOSFET)

### Definition
$$\mu_{eff} = \frac{L g_{ds}}{W C_{ox} (V_{GS} - V_T)}$$

### Field Dependence
$$\mu_{eff} = \frac{\mu_0}{1 + \theta(V_{GS} - V_T)}$$

Where θ = mobility degradation factor

### Vertical Field Effect
$$\mu_{eff} = \frac{\mu_0}{1 + E_{eff}/E_c}$$

---

## Saturation Velocity Effects

### Modified Current (Velocity Saturation)
$$I_{D,sat} = W C_{ox} v_{sat} (V_{GS} - V_T)$$

### Modified gm
$$g_m = W C_{ox} v_{sat}$$

### Velocity Saturation Parameter
$$K_{vs} = \frac{v_{sat}}{\mu_n E_{sat}} = \frac{1}{2}$$ (by definition)

---

## Carrier Statistics

### Mean Free Time
$$\tau = \frac{\mu m^*}{q}$$

### Mean Free Path
$$\lambda = v_{th} \tau = v_{th} \frac{\mu m^*}{q}$$

### Thermal Velocity
$$v_{th} = \sqrt{\frac{3kT}{m^*}}$$

---

## Temperature Coefficients

### Mobility Temperature Coefficient
$$\frac{1}{\mu}\frac{d\mu}{dT} = -\frac{3}{2T} \quad \text{(lattice)}$$

$$\frac{1}{\mu}\frac{d\mu}{dT} = +\frac{3}{2T} \quad \text{(impurity)}$$

### Conductivity Temperature Coefficient
$$\frac{1}{\sigma}\frac{d\sigma}{dT} = \frac{1}{\mu}\frac{d\mu}{dT}$$

---

## ISRO Quick Reference

### Key Formulas
1. μ = vd/E
2. D = μVT
3. vsat ≈ 10⁷ cm/s (Si)
4. μL ∝ T⁻³/²
5. μI ∝ T³/²

### Key Values
| Parameter | Si | Ge | GaAs |
|-----------|-----|-----|------|
| μn | 1350 | 3900 | 8500 |
| μp | 480 | 1900 | 400 |
| vsat | 1.0 | 0.6 | 0.8 ×10⁷ |

### Relations
1. μn > μp always
2. μ decreases with doping
3. μ decreases with temperature (room T)
4. Einstein: D/μ = VT = 26 mV
