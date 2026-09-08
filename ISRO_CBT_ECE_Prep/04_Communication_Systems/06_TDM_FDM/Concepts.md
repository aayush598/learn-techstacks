# TDM and FDM Multiplexing - Concepts

## Multiplexing
- Combining multiple signals over one communication channel
- Three main types: FDM, TDM, and mixed

## FDM (Frequency Division Multiplexing)
- Each signal assigned a distinct frequency band
- Signal translated (modulated) to its assigned band
- Guard bands prevent adjacent channel interference
- Simultaneous transmission
- Used in: AM/FM radio, TV, telephone broadband

### FDM Components:
1. Modulators shift each baseband to its carrier
2. Band-pass filters restrict each channel to its band
3. Summed for transmission
4. At receiver: BPF separates, demodulator recovers

### FDM Bandwidth
```
Total BW = N*(signal BW) + (N-1)*guard band
```
- Example: 30 channels of 4kHz each, 100Hz guard -> 30*4000 + 29*100 = 122,900
- Guard band quality: adjacent channel crosstalk reduction

## TDM (Time Division Multiplexing)
- Each signal gets a time slot (recurring cycle)
- Samples interleaved in time
- Synchronous TDM: fixed slots, no addressing needed
- Used in: telephone (T1/E1), PCM systems

### TDM Frame Structure
```
Frame = N time slots (one per channel)
Slot duration = frame duration / N
Data rate: R = N * channel bit rate (for equal channels)
```

### T1 Carrier
```
24 channels * 8 bits = 192 bits + 1 framing bit = 193 bits/frame
Frame rate: 8000 frames/sec
Bit rate: 193 * 8000 = 1.544 Mbps
Each channel: 64 kbps (8 bits * 8kHz)
```

### E1 Carrier
```
32 slots * 8 bits = 256 bits/frame
Frame rate: 8000
Bit rate: 2.048 Mbps
- Slot 0: framing/sync
- Slot 16: signaling
- Slots 1-15, 17-31: 30 voice channels
```

## TDM vs FDM Comparison
| Feature | FDM | TDM |
|---------|-----|-----|
| Sharing | Frequency | Time |
| Synchronization | Not needed | Essential |
| Filters | BPF required | Not needed |
| Crosstalk | Guard bands | Timing errors |
| Analog use | Common | Rare (mostly digital) |
| Data efficiency | Lower | Higher |

## Statistical TDM
- Slots allocated dynamically to active channels
- More efficient for bursty traffic
- Needs addressing (packet-like)

## WDM (Wavelength Division Multiplexing)
- Optical analog of FDM
- Different wavelengths (colors) on optical fiber
- DWDM: dense, many wavelengths
- Used for fiber optic long-haul

## Synchronization in TDM
- Framing bit; high/low alarm
- Clock recovery at receiver
- Bit timing and frame timing both needed
- Slip: sampling timing offset

---

## ISRO Key Points
- T1 = 1.544 Mbps, E1 = 2.048 Mbps - MOST TESTED
- FDM needs guard band, TDM doesn't use BPF
- FDM simultaneous, TDM sequential
- Guard band: prevent crosstalk in FDM
- TDM is digital-friendly, FDM analog
