# Signals and Systems - Memory Tricks

## Transform Pairs Quick Memory
- **e^(-at)u(t) <-> 1/(s+a)** - "**exponential decay maps to simple pole**"

## Laplace Transform Memory
- **Ramp <-> 1/s^2** (like integration adds 1/s each time)
- **Delta <-> 1** (identity)
- **Unit step <-> 1/s** (integration)
- **Initial value**: x(0+) = lim s*X(s) - "**s times s**" (multiply by s, let s go to infinity)

## Z-Transform Memory
- **a^n <-> z/(z-a)** - "**a to the n, z over z minus a**"
- **Unit step <-> z/(z-1)** (like a=1)

## FFT Memory
- **N=1024: stages = 10** (log2(1024) = 10)
- **Butterflies = (N/2)*log2(N)** - "**Half N times log N**"
- For 1024: (1024/2)*10 = 5120 butterflies

## System Properties Quick Check
- **Causal**: h(t) = 0 for t<0 - "**No future requirement**"
- **Stable**: integral|h| < inf - "**Bounded response from bounded input**"

## Fourier Series Memory
- **Parseval's**: (1/T)integral|x|^2 = sum|cn|^2 - "**Power in time = power in frequency**"
- **Half-wave symmetry**: only odd harmonics - "**Half = Odd**"

## Convolution Identity Trick
- **x * delta = x** - "**Identity element transfers input directly**"
- Think of delta as the "1" of convolution

## DTFT Memory
- **DTFT is always periodic** (period 2pi) - "**Discrete in time, periodic in frequency**"
- **DFT is sampled DTFT** - "**Sampling in frequency like sampling in time**"
