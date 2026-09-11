# TDM and FDM - Practice Questions

---

### Q1. (Easy) FDM multiplexing:
(A) Different carriers/frequencies in parallel  (B) Time slots  (C) Codes  (D) Phase

**Answer: (A) Frequency Division - allocate distinct frequency bands per channel**

---

### Q2. (Moderate) TDM multiplexing:
(A) Time slots per channel on same freq  (B) Separate freq  (C) Codes  (D) Amplitude

**Answer: (A) Time Division - interleave samples of channels in time slots**

---

### Q3. (Moderate) TDM requires:
(A) Synchronization (frame sync)  (B) Separate antennas  (C) Filters only  (D) No clock

**Answer: (A) Synchronization to identify channel slots (framing)**

---

### Q4. (Moderate) In TDM with N channels each sampled at fs, total bit rate:
(A) N * fs * bits/sample  (B) fs  (C) N  (D) N*fs

**Answer: (A) Bit rate = N (channels) * fs * b (bits per sample)**

---

### Q5. (Moderate) FDM needs to prevent:
(A) Adjacent channel interference (guard bands)  (B) Timing  (C) Sync  (D) Clock

**Answer: (A) Guard bands between channels to avoid crosstalk**

---

### Q6. (Moderate) Advantage of TDM over FDM (digital):
(A) Handles digital data efficiently (no crosstalk issues)  (B) More power  (C) Simpler filter  (D) No clock

**Answer: (A) Digital TDM - efficient, digital data, PCM compatible**

---

### Q7. (Moderate) Which needs a carrier per channel?
(A) FDM  (B) TDM  (C) Both  (D) Neither

**Answer: (A) FDM - each channel on separate carrier frequency**

---

### Q8. (Moderate) FDM demodulation requires:
(A) Bandpass filters + coherent/sync detection  (B) Only clock  (C) Only switch  (D) Delay

**Answer: (A) Filter each band + demodulate (selective filtering)**

---

### Q9. (Moderate) For TDM of N analog channels through PCM:
(A) Total rate = N * fs * bits  (B) Only fs  (C) Only N*fs  (D) N^2

**Answer: (A) Combined (TDM + PCM) rate = N * fs * b**

---

### Q10. (Moderate) E1 (European) TDM frame structure:
(A) 32 channels (30 voice + sync + sig)  (B) 24  (C) 8  (D) 64

**Answer: (A) E1 = 32 slots (30 voice + 2 overhead); T1 = 24 voice channels**
