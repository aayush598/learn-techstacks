# Microwave Passive Components - Concepts

## Why "Microwave" Components Differ
- At high freq, lumped elements approximate as distributed
- Waveguides/transmission lines used
- S-parameters characterize components

## Waveguide Components

### Directional Coupler
- 4-port: input, through, coupled, isolated
- Couples a fraction of power from main line to coupled port
- Directivity: isolation from reverse wave
- Coupling factor (dB), directivity (dB), isolation (dB)

### Magic Tee (Hybrid)
- 4-port junction (E-planar + H-planar tees combined)
- Sum port (E/H): splits/combines
- Isolation between certain ports
- Used in balanced mixers, power combining

### E-Plane Tee (series)
- Waveguide tee in E-plane (all three arms)
- Odd/even mode behavior

### H-Plane Tee (shunt)
- H-plane junction

### Circulator
- 3-port ferrite device: energy circulates in one direction (clockwise)
- Port 1 -> 2 -> 3 -> 1 (unidirectional)
- Used: duplexer (transmit/receive separation), isolators

### Isolator
- 2-port ferrite: transmits in one direction, absorbs reverse
- Reflected power absorbed in load (nonreciprocal loss)
- Used: protect sources from reflections

### Attenuator
- Reduces power in a controlled manner
- Fixed or variable (flap, rotary vane)
- Resistive or ferrite based

### Phase Shifter
- Introduces controlled phase shift
- Used: phased arrays, phase modulators

### TEE (E & H) Behavior
- Used for power splitting/combining
- Match considerations at junction (not all matched)

## Ferrite Devices
- Ferrite: ferromagnetic ceramic, nonreciprocal at microwave freq
- Magnetized -> gyromagnetic effect
- Basis of: isolators, circulators, phase shifters, circulators

## Transmission Components
### Connectors/Adaptors
- Coaxial to waveguide transitions
- Impedance matching/transitions (taper)

### Terminations / Loads
- Absorb power (matched load)
- Short circuit, open circuit for stub tuning
- Sliding short (tuner)

### Cavity Resonators
- Waveguide cavity with resonant frequency
- High Q (thousands), for filters & oscillators
- f0 determined by dimensions

## Filter types
- Waveguide bandpass, lowpass
- Coupling-based (directive filter)
- Stub resonators

---

## ISRO Key Points
- Isolator: 1-direction, protect source
- Circulator: 3-port rotary
- Directional coupler: coupling, directivity
- Magic tee: sum/diff combiner
- Ferrite: nonreciprocity
- Cavity: high Q resonator
