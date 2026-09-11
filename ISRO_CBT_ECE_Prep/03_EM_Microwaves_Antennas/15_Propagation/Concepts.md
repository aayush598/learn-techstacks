# Radio Wave Propagation - Concepts

## Modes of Propagation
| Mode | Frequency | Application |
|------|-----------|-------------|
| Ground wave | up to ~3 MHz | AM broadcast, maritime |
| Sky wave | 3-30 MHz (HF) | international broadcasting, amateur |
| Space wave (LOS) | >30 MHz | FM, TV, radar, satellite |
| Tropospheric scatter | VHF/UHF | beyond horizon |

## Ground Wave Propagation
- Follows earth's curvature
- Suitable low freq (<~ few MHz)
- Attenuates with distance (surface wave)
- Soil conductivity affects range (better over sea)
- Used for local AM broadcasting

## Sky Wave (Ionospheric) Propagation
- Radio waves refracted/reflected by ionosphere
- Ionosphere: ionized layers (D, E, F1, F2)
- F layer (day: F1+F2, night: F2) primary for HF
- Skip distance: minimum ground distance for reception
- MUF (Maximum Usable Frequency): highest freq usable for sky wave to given distance
- Skip zone: area of no reception between ground wave and sky wave

## Ionosphere Layers
| Layer | Height (km) | Effect |
|-------|-------------|--------|
| D | 60-90 | Absorbs HF, dies at night |
| E | 90-120 | Weak reflection |
| F1 | 200-250 | Day only |
| F2 | 250-400 | Main HF reflector |

## Critical Frequency (f_crit)
- Highest freq reflected at vertical incidence
- MUF = f_crit / cos(theta_incidence) (secant law)
- Optimum Working Frequency (OWF) ~ 0.85 MUF

## Space Wave (LOS) Propagation
- Direct + reflected ray
- Requires line of sight
- Radio horizon > optical horizon (~4/3 earth radius effect)
- Horizon distance: d ~ sqrt(2 h/Re)*... (approx: d_km ~ 4.12 sqrt(h_m))
```

## Troposphere
- Below ionosphere, contains weather, refraction
- Bends signal (favorable for slightly beyond LOS)
- Refraction index variation with height
- Tropospheric scatter: beyond horizon, weak

## Fading
- Signal strength variation
- Types: fast (multipath) and slow (large-scale)
- Multipath fading: multiple reflected paths combine (Rayleigh/Rician)
- Selective fading: different frequencies fade differently
- Mitigation: diversity (space, frequency, time), adaptive

## Frequency Assignments
- Long wave (LF): 30-300 kHz (ground wave)
- Medium (MF): 300-3000 kHz (ground+sky at night)
- Short (HF): 3-30 MHz (sky wave)
- VHF: 30-300 MHz (LOS)
- UHF: 300-3000 MHz (LOS)
- SHF: 3-30 GHz (LOS, microwave)
- EHF: >30 GHz

---

## ISRO Key Points
- Ground wave: low freq, follows earth
- Sky wave: HF ionosphere reflection, MUF
- Space wave/LOS: high freq
- MUF = f_crit/cos(theta)
- Radio horizon ~ 4/3 longer than optical
- Fading: multipath causes variability
