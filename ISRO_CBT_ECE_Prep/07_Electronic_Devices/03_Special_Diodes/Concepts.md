# Special Diodes - Concepts

## Zener Diode

### Structure
- Heavily doped PN junction
- Designed for reverse breakdown operation
- VBR = VZ (Zener voltage)
- Available from ~2V to 200V

### Breakdown Mechanism
- Below 5V: Zener breakdown (tunneling)
- Above 6V: Avalanche breakdown
- 5-6V: Both mechanisms contribute
- Zener: negative temp coefficient
- Avalanche: positive temp coefficient

### V-I Characteristics
- Forward: normal diode behavior
- Reverse: sharp breakdown at VZ
- Constant voltage source in breakdown

### Applications
- Voltage regulation
- Reference voltage
- Overvoltage protection
- Clipping circuits

---

## Tunnel Diode (Esaki Diode)

### Structure
- Very heavily doped (10¹⁹-10²⁰ cm⁻³)
- Very narrow depletion region (~10 nm)
- Degenerate semiconductor (EF in band)

### Operating Principle
- Quantum mechanical tunneling
- Negative differential resistance (NDR) region
- Very fast switching (ps range)

### V-I Characteristics
- Peak voltage: VP ≈ 50-200 mV
- Valley voltage: VV ≈ 300-500 mV
- Peak current: IP (depends on doping)
- NDR region: VP < V < VV

### Applications
- High-frequency oscillators (>100 GHz)
- Fast switching circuits
- Microwave amplifiers
- Memory elements

---

## Varactor Diode (Varicap)

### Structure
- Reverse-biased PN junction
- Designed for voltage-dependent capacitance
- Special doping profile (abrupt, linear graded)

### Capacitance-Voltage Relationship
$$C_j = \frac{C_{j0}}{(1 + V_R/V_{bi})^m}$$

Where m depends on doping profile:
- m = 1/2: abrupt junction
- m = 1/3: linear graded
- m = 2-3: hyperabrupt

### Applications
- TV tuner circuits
- FM modulation
- Phase-locked loops
- Frequency multipliers
- Electronic tuning

---

## PIN Diode

### Structure
- P-type - Intrinsic - N-type
- Wide intrinsic region (10-200 μm)
- Low doping in I-region

### Forward Bias
- Injects carriers into I-region
- Conducts like resistor
- Resistance decreases with current
- R = ρI/(2A) (approximate)

### Reverse Bias
- Acts as capacitor
- Wide depletion region
- Low capacitance: C = εA/W
- Fast switching

### Applications
- RF switches
- Microwave attenuators
- Photodetectors
- High-voltage rectifiers

---

## Schottky Diode

### Structure
- Metal-semiconductor junction
- No depletion region like PN junction
- Majority carrier device
- Fast switching

### Barrier Potential
- Depends on metal and semiconductor
- Typical: 0.2-0.5V (Si)
- Lower than PN junction (0.7V)

### V-I Characteristics
$$I = I_s\left[\exp\left(\frac{V}{nV_T}\right) - 1\right]$$

Is much larger than PN junction diode

### Advantages
- Fast switching (no minority carriers)
- Low forward voltage drop
- Low noise
- High-frequency operation

### Applications
- Fast switching circuits
- RF detectors
- Solar cell contacts
- Low-voltage rectifiers

---

## LED (Light Emitting Diode)

### Structure
- Forward-biased PN junction
- Direct bandgap material (GaAs, GaN)
- Light emitted by recombination

### Emitted Photon Energy
$$E = h\nu = \frac{hc}{\lambda} \geq E_g$$

### Wavelength
$$\lambda = \frac{hc}{E_g} = \frac{1240}{E_g \text{ (eV)}} \text{ nm}$$

### Materials and Colors
| Material | Eg (eV) | λ (nm) | Color |
|----------|---------|--------|-------|
| GaAsP | 1.8 | 690 | Red |
| GaAsP | 2.0 | 620 | Orange |
| GaP | 2.2 | 565 | Green |
| GaN | 3.4 | 365 | Blue |
| InGaN | 2.5 | 496 | Blue |

### Efficiency
- Internal quantum efficiency
- External quantum efficiency
- Power efficiency
- Affected by: surface texturing, lens, material quality

---

## Photodiode

### Structure
- Reverse-biased PN junction
- Light generates electron-hole pairs
- Photoconductive mode

### Operating Modes
1. **Photoconductive**: reverse bias, fast response
2. **Photovoltaic**: zero bias, solar cell mode

### Photo Current
$$I_{ph} = q\eta A G L$$

Where:
- η = quantum efficiency
- A = area
- G = generation rate
- L = absorption length

### Spectral Response
- Cutoff wavelength: λc = hc/Eg
- Peak sensitivity varies with material
- Si: 400-1100 nm (peak ~900 nm)
- Ge: 400-1500 nm
- InGaAs: 900-1700 nm

### Applications
- Optical communication
- Light detection
- Solar cells
- Barcode readers
- Medical instruments

---

## PIN vs Schottky Comparison

| Parameter | PIN Diode | Schottky Diode |
|-----------|-----------|----------------|
| Structure | P-I-N | Metal-Semiconductor |
| Carriers | Minority + Majority | Majority only |
| Switching | Fast | Very fast |
| Forward Drop | ~0.7V | 0.2-0.5V |
| Reverse Recovery | Yes | No |
| Application | RF switches | High-speed digital |

---

## Power Diodes

### Structure
- Large area PN junction
- Drift region for high voltage
- Guard rings for edge protection

### Recovery Characteristics
- Soft recovery preferred
- Fast recovery: trr < 100 ns
- Ultrafast: trr < 50 ns

### Applications
- Rectifiers
- Power supplies
- Motor drives
- Inverters

---

## Step Recovery Diode

### Operating Principle
- Stores charge during forward bias
- Rapidly switches when charge depleted
- Produces sharp voltage pulses
- Used as frequency multiplier

### Applications
- Pulse generation
- Frequency multipliers
- Comb generators
- Sampling circuits

---

## IMPATT Diode

### Structure
- Reverse-biased PN junction
- Impact ionization + transit time
- Generates microwave power

### Applications
- Microwave oscillators
- Radar transmitters
- Communications

---

## TRAPATT Diode

### Structure
- Similar to IMPATT
- Lower frequency, higher efficiency
- Trapped plasma mode

### Applications
- Pulsed radar
- Low-noise oscillators

---

## Gunn Diode

### Structure
- Not a diode (two-terminal device)
- Uses negative differential mobility
- GaAs, InP materials

### Applications
- Microwave oscillators
- Local oscillators
- Radar systems

---

## ISRO Key Points
- Zener: voltage regulation, negative temp coefficient < 5V
- Tunnel: NDR region, very fast, high-frequency oscillators
- Varactor: voltage-controlled capacitor, C ∝ 1/√V
- PIN: RF switching, wide I-region
- Schottky: majority carrier, fast switching, low Vf
- LED: direct bandgap, λ = 1240/Eg
- Photodiode: light detection, reverse biased
