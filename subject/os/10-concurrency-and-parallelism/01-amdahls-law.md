# Amdahl's Law & Gustafson's Law

## Amdahl's Law
- **Formula:** `Speedup = 1 / ((1 - P) + P / N)`
  - `P` = fraction of program that is parallelizable
  - `N` = number of processors/cores
- **Key insight:** speedup limited by serial portion, **not** core count

| Parallel % | 2 cores | 4 cores | 8 cores | ∞ cores |
|-------------|---------|---------|---------|---------|
| 50%         | 1.33×   | 1.60×   | 1.78×   | 2.00×   |
| 90%         | 1.82×   | 3.08×   | 4.44×   | 10.0×   |
| 95%         | 1.90×   | 3.48×   | 5.58×   | 20.0×   |
| 99%         | 1.98×   | 3.88×   | 7.48×   | 100×    |

- **Diminishing returns:** doubling cores yields <2× speedup
- **Implication:** optimize serial code first; parallel speedup caps quickly
- **Example:** 90% parallel → max 10× (even with 1M cores)

## Gustafson's Law (Scaled Speedup)
- **Formula:** `Speedup = P × N + (1 - P)`
  - Problem size grows with N; parallel work scales
- **Amdahl** = fixed problem size | **Gustafson** = fixed time
- **Reality check:** in practice, problem sizes grow with compute power
- Large-scale HPC tends to follow Gustafson more than Amdahl

## Worked Example
- Program: 20 hrs serial, 80 hrs parallel (can parallelize)
  - N=4: total = 20 + 80/4 = 40 hrs → speedup = 100/40 = 2.5×
  - N=∞: total = 20 hrs → max speedup = 5×
- **Takeaway:** even infinite parallelism can't fix serial bottlenecks

## Interview Tips
- *"If you can make the serial portion 2× faster, that's better than doubling cores"*
- Mention **Amdahl's Law** when discussing parallel scaling limits
- Contrast with **Gustafson** when problem size scales
