# Breakdown Mechanisms - Concepts

## Avalanche Breakdown

### Mechanism
1. High electric field accelerates carriers
2. Carriers gain kinetic energy
3. Impact ionization: carrier creates EHP
4. Multiplication: chain reaction
5. Current increases rapidly

### Conditions
- Depletion width: moderate
- Electric field: 10⁵-10⁶ V/cm
- Breakdown voltage: > 6V (Si)

### Temperature Dependence
- Positive temperature coefficient
- VBR increases with temperature
- Higher T → more phonon scattering → less energy for impact ionization

### Multiplication Factor
$$M = \frac{1}{1 - (V/V_{BR})^n}$$

Where n ≈ 4-6 for Si

---

## Zener Breakdown

### Mechanism
1. Very high electric field
2. Direct tunneling of electrons
3. Band-to-band tunneling
4. Current increases rapidly

### Conditions
- Depletion width: very narrow (< 10 nm)
- Electric field: > 10⁶ V/cm
- Doping: very heavy (> 10¹⁸ cm⁻³)
- Breakdown voltage: < 5V (Si)

### Temperature Dependence
- Negative temperature coefficient
- VBR decreases with temperature
- Higher T → narrower bandgap → easier tunneling

---

## Avalanche vs Zener Comparison

| Parameter | Avalanche | Zener |
|-----------|-----------|-------|
| Voltage | > 6V | < 5V |
| Temperature Coeff. | Positive | Negative |
| Doping | Moderate | Heavy |
| Depletion Width | Wide | Narrow |
| Mechanism | Impact ionization | Tunneling |
| Noise | Higher | Lower |
| Recovery | Slower | Faster |

### Transition Region (5-6V)
- Both mechanisms contribute
- Temperature coefficient ≈ 0
- Used for temperature-compensated references

---

## Punch-Through

### Mechanism
1. Reverse bias increases depletion width
2. Depletion region reaches emitter
3. Barrier collapses
4. Current flows directly

### Conditions
- Narrow base width
- High collector voltage
- Typical in BJTs

### Effects
- Sudden increase in IC
- Can cause device damage
- Must be avoided in normal operation

---

## Drain Breakdown (MOSFET)

### Mechanism
1. High drain voltage
2. Impact ionization near drain
3. Hot carriers injected into gate oxide
4. Gate oxide damage

### Conditions
- High VDS
- Short channel length
- High electric field near drain

### Prevention
- Drain engineering (LDD structure)
- Proper voltage rating
- Guard rings

---

## Hot Carrier Effects

### Mechanism
1. Carriers gain high energy from electric field
2. "Hot" carriers exceed thermal equilibrium
3. Can inject into gate oxide
4. Cause threshold voltage shift

### Effects
- VT shifts over time
- gm degradation
- Reliability concern
- Important in short-channel devices

### Types
1. **Hot electrons**: most common
2. **Hot holes**: in PMOS
3. **Substrate hot carriers**: from substrate

---

## Gate Oxide Breakdown

### Mechanism
1. High electric field across oxide
2. Fowler-Nordheim tunneling
3. Oxide breakdown
4. Permanent damage

### Conditions
- VGS > oxide rating
- Thin oxide (< 5 nm)
- High temperature

### Reliability
- Time-dependent dielectric breakdown (TDDB)
- Important for oxide reliability

---

## ESD (Electrostatic Discharge)

### Mechanism
1. Static charge builds up
2. Sudden discharge through device
3. High current pulse
4. Thermal damage

### Protection
1. Clamp diodes
2. Gas discharge tubes
3. Varistors
4. ESD protection circuits

---

## Thermal Breakdown

### Mechanism
1. Power dissipation heats junction
2. Temperature increases
3. Current increases (positive feedback)
4. Device destruction

### Conditions
- High power dissipation
- Poor heat sinking
- Thermal runaway

### Prevention
- Adequate heat sinking
- Thermal derating
- Current limiting

---

## Breakdown Voltage Relationships

### Avalanche (Empirical)
$$V_{BR} = 60\left(\frac{E_g}{1.1}\right)^{3/2}\left(\frac{N_B}{10^{16}}\right)^{-3/4}$$

### Doping Dependence
$$V_{BR} \propto N^{-3/4}$$

### Temperature Dependence
- Avalanche: dVBR/dT > 0
- Zener: dVBR/dT < 0

---

## ISRO Key Points
- Avalanche: > 6V, positive temp coefficient
- Zener: < 5V, negative temp coefficient
- Punch-through: base width modulation
- Hot carriers: reliability concern in MOSFETs
- At ~5.6V: temp coefficient ≈ 0
- VBR ∝ N⁻³/⁴ for both mechanisms
