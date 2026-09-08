# Microwave Devices - Quick Reference

## Device Summary Table
| Device | Negative R Mech | Use | Characteristics |
|--------|----------------|-----|-----------------|
| Gunn diode | Transferred electron (GaAs) | Oscillator | Medium power, moderate noise |
| IMPATT | Avalanche transit time | Oscillator | High power, high noise |
| Tunnel diode | Quantum tunneling | Oscillator | Very low power, very high freq |
| TWT | Slow-wave + beam | Broadband amp | Wide bandwidth, med-high power |
| Klystron | Velocity mod, bunching | Narrowband amp | High gain, narrowband |
| Magnetron | Crossed-E/B | High power osc | Very high power, radar |
| HEMT | Heterojunction | LNA | Very low noise, high gain |
| MESFET | FET in GaAs | Amp/switch | Medium |
| Schottky | MS junction | Mixer/detector | Fast, low drop |
| Varactor | - | Tuning | Variable C |

## Negative Resistance Device Types
```
Gunn -> transferred electron effect (bulk)
IMPATT -> impact ionization + transit time
Tunnel -> quantum tunneling
BARITT -> thermionic + transit
```

## Frequency/Power
```
Higher freq: solid state preferred but less power
Higher power: vacuum tubes (klystron, magnetron, TWT)
mm-wave highest power: solid state emerging
```

## Attenuators / passive (for contrast)
```
Directional coupler: samples power
Isolator: transmits one direction only (nonreciprocal, ferrite)
Circulator: three-port directional
```

## Key Numbers
```
Microwave band: 300 MHz - 300 GHz
Standard waveguide band designators (WR)
50 ohm convention
Media frequency allocations (C band: 4-8 GHz, Ku 12-18, Ka 24-40)
```

## Selection Guide
| Needs | Choose |
|-------|--------|
| HF power | Magnetron or klystron |
| Broadband | TWT |
| Low noise receive | HEMT LNA |
| Simple oscillator | Gunn |
| Low cost | Gunn diode |
| Variable freq tuning | YIG or varactor |
