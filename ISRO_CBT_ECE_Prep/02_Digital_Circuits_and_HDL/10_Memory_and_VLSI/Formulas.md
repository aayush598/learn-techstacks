# Memory and VLSI - Formulas

## Memory Capacity
```
Capacity = depth x width (bits)
Address lines: depth = 2^A  (A = number of address lines)
Data lines = width
Example: 1Kx8 -> 2^10 x 8, 1024 locations, 8-bit data
Total bits = depth * width
```

## Common sizes
```
1K = 2^10, 1M = 2^20, 1G = 2^30
1 byte = 8 bits
64K x 8 = 65536 x 8 = 524288 bits = 64 KB
```

## Number of memory chips
```
No. of chips = Total memory / chip size
Example: 64KB using 16Kx8 chips -> 4 chips
(64K/16K = 4)
```

## Address decoding / chip select
```
Chip select from high-order address bits
Decoder (n inputs -> 2^n outputs) selects chip
Number of decoder outputs = number of chips
```

## CMOS Power
```
Dynamic power: P = C V^2 f   (C = capacitance, V = supply, f = freq)
Static/leakage: P = V * I_leak
Total dynamic dominates in normal operation
```

## CMOS Propagation delay
```
Delay ~ R_on * C_load  (RC)
Scaling: reduce V, C -> faster
```

## SRAM/DRAM
```
SRAM: 6T cell, no refresh
DRAM: 1T + 1C, refresh every ~15-64 ms (row refresh)
```

## Cache performance
```
Average access = Hit_time + Miss_rate * Miss_penalty
Effective access time = H*Tc + (1-H)*Tm
H = hit ratio, Tc = cache time, Tm = memory time
```

## VLSI integration levels
```
SSI: <10 gates, MSI: 10-100, LSI: 100-1000
VLSI: 1000-10^5, ULSI: >10^5
```

## AM & fan-out
```
Fan-out F = I_output_max / I_input_max (current-based)
For logic: number of loads drivable
```

## Quick Reference
| Quantity | Formula |
|----------|---------|
| Depth | 2^A |
| Total bits | depth x width |
| No. chips | total/chip |
| P_dynamic | C V^2 f |
| Avg access | H Tc + (1-H)Tm |
| DRAM refresh | every ~15ms |
