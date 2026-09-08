# Data Acquisition - Practice Questions

## Q1. (ISRO Pattern)
A signal has maximum frequency 5 kHz. The minimum sampling rate according to Nyquist theorem is:
- (A) 5 kHz
- (B) 10 kHz
- (C) 20 kHz
- (D) 50 kHz
**Answer: (B)** fs >= 2 x 5kHz = 10 kHz

## Q2.
The SNR of an ideal 12-bit ADC for a full-scale sinusoid is:
- (A) 74 dB
- (B) 72 dB
- (C) 48 dB
- (D) 96 dB
**Answer: (A)** SNR = 6.02 x 12 + 1.76 = 74 dB

## Q3.
An anti-aliasing filter is placed:
- (A) After the ADC
- (B) Before the ADC
- (C) After the signal conditioning
- (D) In the digital domain
**Answer: (B)**

## Q4.
If a 2 kHz signal is sampled at 3 kHz, the aliased frequency is:
- (A) 1 kHz
- (B) 2 kHz
- (C) 5 kHz
- (D) 3 kHz
**Answer: (A)** f_alias = |3k - 2k| = 1 kHz

## Q5.
Sample and hold circuit is used to:
- (A) Increase sampling rate
- (B) Hold voltage constant during ADC conversion
- (C) Filter the signal
- (D) Amplify the signal
**Answer: (B)**

## Q6.
For 16-bit ADC with 10V full scale, the LSB is approximately:
- (A) 0.153 mV
- (B) 1.53 mV
- (C) 15.3 mV
- (D) 0.015 mV
**Answer: (A)** LSB = 10/65536 = 0.153 mV

## Q7.
Oversampling improves SNR by:
- (A) 6 dB per doubling
- (B) 3 dB per doubling
- (C) 1 dB per doubling
- (D) 12 dB per doubling
**Answer: (B)**

## Q8.
A 100 kSPS ADC is multiplexed across 8 channels. Each channel gets:
- (A) 100 kSPS
- (B) 800 kSPS
- (C) 12.5 kSPS
- (D) 50 kSPS
**Answer: (C)** 100/8 = 12.5 kSPS per channel

## Q9.
Quantization error is:
- (A) +/- 1 LSB
- (B) +/- 1/2 LSB
- (C) +/- 2 LSB
- (D) 0 LSB
**Answer: (B)**

## Q10.
The practical sampling rate is usually:
- (A) Exactly 2 x fmax
- (B) 5-10 x fmax
- (C) 0.5 x fmax
- (D) Equal to fmax
**Answer: (B)**

## Q11.
A 10-bit ADC has quantization levels of:
- (A) 1024
- (B) 1000
- (C) 256
- (D) 2048
**Answer: (A)** 2^10 = 1024

## Q12.
Droop in sample and hold is caused by:
- (A) Capacitor charging
- (B) Capacitor leakage current
- (C) Switch resistance
- (D) ADC conversion
**Answer: (B)**

## Q13.
ENOB of an ADC with actual SNR of 70 dB is approximately:
- (A) 12 bits
- (B) 11 bits
- (C) 10 bits
- (D) 14 bits
**Answer: (B)** ENOB = (70-1.76)/6.02 = 11.3 -> 11 bits

## Q14.
Aliasing can be prevented by:
- (A) Increasing signal frequency
- (B) Using anti-aliasing filter before sampling
- (C) Sampling at higher voltage
- (D) Using more bits in ADC
**Answer: (B)**

## Q15.
The Nyquist frequency is:
- (A) fmax
- (B) fs
- (C) fs/2
- (D) 2*fs
**Answer: (C)**

---
**ISRO Tip:** Nyquist (fs >= 2*fmax), quantization SNR (6.02n + 1.76 dB), and anti-aliasing filter placement are the most tested DAQ concepts.
