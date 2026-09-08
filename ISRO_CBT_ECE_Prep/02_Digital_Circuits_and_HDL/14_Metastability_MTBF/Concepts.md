# Metastability and MTBF - Concepts

## Metastability
- When a flip-flop samples an input that violates setup or hold time
- Output enters an unstable state between 0 and 1
- May stay metastable for unpredictable duration
- Eventually settles to 0 or 1 (unpredictable which)

## Setup and Hold Time Violations
- **Setup time (Ts):** Data must be stable BEFORE clock edge
- **Hold time (Th):** Data must be stable AFTER clock edge
- If data changes within [Th, Ts] window before clock: metastability possible

## MTBF (Mean Time Between Failures)
```
MTBF = (1/fclk) * e^(Tsetup/tau) / (fdata * T0)
where:
  fclk = clock frequency
  fdata = data transition rate
  Tsetup = required setup time
  tau = flip-flop time constant
  T0 = test duration parameter
```

## Two-Flip-Flop Synchronizer
- First FF: May go metastable
- Second FF: Samples after one clock period (allows time for settling)
- Dramatically increases MTBF
- Not 100% guaranteed but practically sufficient

### MTBF with 2-FF Synchronizer:
```
MTBF_2FF = (1/fclk) * e^(Tsetup/tau) / (fdata * T0) * e^(Tclk/tau)
approximately: MTBF_2FF = MTBF_1FF * e^(Tclk/tau)
```

---

## Clock Domain Crossing
- When signals cross from one clock domain to another
- Metastability is unavoidable without synchronization
- Solution: Use 2 or 3 flip-flop synchronizers
- For multi-bit signals: use handshaking or FIFO

## ISRO Key Points
- Metastability occurs when setup/hold time violated
- Two-FF synchronizer dramatically increases MTBF
- MTBF formula: exponential with Tsetup/tau
- More synchronizer stages = higher MTBF but more latency
- Cannot be eliminated, only made extremely rare
