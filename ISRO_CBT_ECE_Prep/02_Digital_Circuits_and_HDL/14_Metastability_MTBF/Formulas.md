# Metastability and MTBF - Formulas

## MTBF Formula (Single Flip-Flop)
```
MTBF = e^(Tsetup / tau) / (fclk * fdata * T0)

where:
  Tsetup = setup time of flip-flop
  tau = metastability time constant (propagation delay parameter)
  fclk = sampling clock frequency
  fdata = input data transition frequency
  T0 = measurement time constant (device specific)
```

## MTBF with Two-Stage Synchronizer
```
MTBF_2FF = (e^(Tclk / tau) / (fdata * T0))

where Tclk = 1/fclk (clock period)
```

## Key Relationships
```
MTBF increases exponentially with:
  - Increasing Tsetup (better FF)
  - Decreasing tau (faster FF)
  - Decreasing fclk (slower clock)
  - Decreasing fdata (fewer data transitions)

MTBF_2FF >> MTBF_1FF (exponentially better)
```

## Setup and Hold Time Window
```
Data must be stable during:
  [Tclk - Tsetup, Thold] before clock edge
  (Setup time before, Hold time after)

Violation occurs if data changes in this window
```

## Metastability Resolution Time
```
Tresolve = tau * ln(Vdd / (2 * Delta_V))

where:
  Delta_V = acceptable voltage uncertainty
  Vdd = supply voltage
  tau = time constant
```

## Quick Reference Table
| Parameter | Effect on MTBF | Direction |
|-----------|---------------|-----------|
| fclk ↑ | MTBF ↓ | Worse |
| fdata ↑ | MTBF ↓ | Worse |
| Tsetup ↑ | MTBF ↑ | Better |
| tau ↓ | MTBF ↑ | Better |
| More FF stages | MTBF ↑↑↑ | Much better |

## Two-FF Synchronizer Design Rule
```
Tclk > Tresolve (clock period must be > resolution time)
Typical: Tclk >= 3 * Tsetup for practical MTBF
```
