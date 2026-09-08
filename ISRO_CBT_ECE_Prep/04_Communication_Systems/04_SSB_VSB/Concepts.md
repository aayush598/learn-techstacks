# SSB-SC and VSB - Concepts

## SSB (Single Sideband Suppressed Carrier)
- Only ONE sideband transmitted (LSB or USB)
- Carrier suppressed
- Bandwidth: HALF of AM/DSB (just fm not 2*fm)
- Power: only ~Pc*mu^2/4 (or the single sideband power) - very efficient
- Requires coherent detection (no carrier to envelope-detect)

## Generation Methods
1. **Filter method**: AM/DSB then BPF to select one sideband
   - Sharp filter needed if fm small (difficulty)
2. **Phase-shift method**: 
   - Based on Hilbert transform relationship between sidebands
   - s_SSB(t) = m(t)cos(wc t) -/+ mh(t) sin(wc t)
   - mh(t) = Hilbert transform of m(t)
3. **Weaver method** (third, less common): mixing in stages

## SSB Signal (upper sideband)
```
s_USB(t) = (1/2)[m(t) cos wc t - mh(t) sin wc t]
s_LSB(t) = (1/2)[m(t) cos wc t + mh(t) sin wc t]
mh(t) = Hilbert transform of m(t) (90-degree phase shift)
```

## SSB Demodulation
- Coherent detection required (multiplication by local carrier)
- Output: m(t)/2 (with LPF)
- Coherent requires frequency/phase lock

## VSB (Vestigial Sideband)
- Sends one full sideband + a "vestige" of the other
- Bandwidth: between fm and 2fm (roughly fm + vestige)
- Standard for TV video (compatible with envelope detection)
- Compromise: SSB's saving + manageable filter

## SSB Advantages
1. Half bandwidth (fm vs 2fm)
2. Most power efficient (no carrier, one sideband only)
3. Less susceptible to selective fading (for HF)

## SSB Disadvantages
1. Complex / expensive (coherent detection, sharp filters)
2. Cannot use simple envelope detector
3. Precise frequency synchronization needed

## Applications
- SSB: HF amateur radio, two-way voice, point-to-point HF
- VSB: Broadcast TV video (analog), some cable systems
- DSB/AM: AM broadcast radio (because envelope detection simple)

## Comparison Table
| Feature | AM | DSB-SC | SSB | VSB |
|---------|----|--------|-----|-----|
| BW | 2fm | 2fm | fm | ~fm+vestige |
| Power eff | low (33%) | high | highest | high |
| Carrier | Yes | No | No | partial |
| Detection | envelope | coherent | coherent | envelope(ok) |
| Complexity | low | med | high | med |

---

## ISRO Key Points
- SSB: bandwidth fm, NEEDS coherent detection
- SSB from DSB by suppressing one sideband + carrier
- Hilbert transform: 90 degree phase relation
- VSB used in TV broadcast
- SSB most bandwidth & power efficient of AM family
