# TDM and FDM Multiplexing - Formulas

## FDM Bandwidth
```
Total BW = Sum(channel BW) + Sum(guard bands)
         = N*BW_signal + (N-1)*BW_guard
FDM uses guard band to prevent adjacent channel crosstalk
```

## TDM Frame
```
Frame duration = 1/fs (if sampling at fs)
Slot duration = frame duration / N = 1/(N*fs)
TDM bit rate = N * channel bit rate
```

## T1 Carrier
```
Frames: 24 channels x 8 bits = 192 bits + 1 framing = 193 bits
Frame rate: 8000/sec
Bit rate = 193 x 8000 = 1.544 Mbps
Per channel: 64 kbps
Framing bit alternates pattern for sync
```

## E1 Carrier
```
32 time slots x 8 bits = 256 bits/frame
Frame rate: 8000/sec
Bit rate = 256 x 8000 = 2.048 Mbps
30 traffic channels + 1 sync + 1 signaling
```

## TDM Data Rate Calculation
```
If each of N channels has bit rate Rb:
  TDM output rate = N * Rb
If channels sampled at fs with n bits per sample:
  Rb = fs * n per channel
  TDM rate = N * Rb
```

## Example Calculations
```
4 channels, each 8-bit sampled at 8 kHz:
  Per channel: 64 kbps
  TDM rate: 4 * 64k = 256 kbps
```
```
5 channels of 2kHz each FDM with 100Hz guard:
  BW = 5*2000 + 4*100 = 10000 + 400 = 10400 Hz
```

## Time Slot Utilization
```
ASCII 8 data bits + 1 start + 1 stop (async)
Efficiency = 8/10 = 80% (async)
Synchronous (no frame overhead excluded): 100%
```

## Quick Reference
| Value | Formula |
|-------|---------|
| T1 bit rate | 1.544 Mbps |
| E1 bit rate | 2.048 Mbps |
| Voice channel | 64 kbps |
| T1 frame | 193 bits |
| E1 frame | 256 bits |
| Frame rate | 8000/s |
| FDM BW | N*BW_sig + (N-1)*guard |
| TDM rate | N * Rb |
