# Power Amplifiers - Concepts

## Classification of Power Amplifiers

---

## Class A Amplifier
- Transistor conducts for full 360 degrees of input cycle
- Maximum efficiency: 25% (resistive load), 50% (transformer coupled)
- Low distortion, high linearity
- Q-point at center of load line
- Applications: Small signal, audio pre-amplifiers

### Efficiency:
- Resistive load: max 25%
- Transformer coupled: max 50%
- Active load: approaches 50%

## Class B Amplifier
- Transistor conducts for 180 degrees (half cycle)
- Two transistors in push-pull configuration
- Maximum efficiency: 78.5% (pi/4)
- Crossover distortion at zero crossing
- Q-point at cutoff

### Push-Pull Configuration:
- Two complementary transistors (NPN + PNP)
- Each handles half the cycle
- Output combined at load
- Crossover distortion: Both transistors off near Vbe = 0.7V

## Class AB Amplifier
- Conducts for slightly more than 180 degrees
- Bias transistors slightly above cutoff (Vbe biasing)
- Eliminates crossover distortion
- Maximum efficiency: between 25% and 78.5%
- Practical efficiency: 50-60%
- Most commonly used in audio amplifiers

## Class C Amplifier
- Conducts for less than 180 degrees
- High efficiency: 80-90%
- Highly distorted output
- Used with tuned circuits (tank circuit) for sine wave recovery
- Applications: RF amplifiers, oscillators

## Class D Amplifier
- Switching mode operation (fully on or fully off)
- Theoretical efficiency: 100%
- Practical efficiency: 90-95%
- Uses PWM (Pulse Width Modulation)
- Output filter (LPF) recovers analog signal
- Applications: Audio power amplifiers, motor drives

## Class F Amplifier
- Uses harmonic resonators in output network
- Shapes output voltage waveform to square wave
- Current waveform is half-sine
- Theoretical efficiency: 100%
- Practical efficiency: 85-90%
- Uses odd harmonic resonators

---

## Comparison Table

| Class | Conduction Angle | Max Efficiency | Distortion | Q-point |
|-------|-----------------|----------------|------------|---------|
| A | 360 degrees | 25-50% | Lowest | Center |
| B | 180 degrees | 78.5% | Crossover | Cutoff |
| AB | 180-360 degrees | 50-60% | Low | Near cutoff |
| C | <180 degrees | 80-90% | High | Below cutoff |
| D | Switching | 90-95% | PWM based | On/Off |
| F | Switching | ~100% | Harmonic based | On/Off |

---

## ISRO Key Points
- Class B max efficiency = pi/4 = 78.5% (important formula)
- Class A max efficiency = 25% (resistive), 50% (transformer)
- Crossover distortion occurs in Class B due to dead zone
- Class AB eliminates crossover distortion with slight bias
- Class D uses PWM and LC output filter
