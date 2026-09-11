# Channel Coding - Practice Questions

---

### Q1. (Easy) Purpose of channel coding (error correction):
(A) Detect/correct errors due to noise  (B) Compress  (C) Encrypt  (D) Modulate

**Answer: (A) Detect & correct transmission errors (add redundancy)**

---

### Q2. (Moderate) Hamming code (7,4):
(A) 4 data bits + 3 parity = 7  (B) 7 data  (C) 4 parity  (D) 11 data

**Answer: (A) (7,4): 7 total, 4 data, 3 parity; can correct single bit error**

---

### Q3. (Moderate) Minimum Hamming distance dmin for correcting t errors:
(A) dmin >= 2t+1  (B) dmin >= t  (C) dmin = t  (D) dmin >= 2t

**Answer: (A) dmin >= 2t + 1 to correct t errors**

---

### Q4. (Moderate) To detect s errors:
(A) dmin >= s+1  (B) dmin >= s  (C) dmin >= 2s  (D) dmin = s

**Answer: (A) dmin >= s + 1 to detect s errors**

---

### Q5. (Moderate) Parity bit detects:
(A) Odd number of errors only  (B) Corrects  (C) Even errors  (D) All errors

**Answer: (A) Single even-parity detects odd number of bit errors (not even)**

---

### Q6. (Moderate) Code rate R:
(A) k/n (data/total)  (B) n/k  (C) k*n  (D) n+k

**Answer: (A) R = k/n - fraction of useful (data) bits**

---

### Q7. (Moderate) Convolutional codes process:
(A) Bitstream with memory (sliding window)  (B) Fixed blocks only  (C) No redundancy  (D) Analog

**Answer: (A) Convolutional - code depends on current + previous input bits (state)**

---

### Q8. (Moderate) Viterbi decoding used for:
(A) Convolutional codes (ML sequence)  (B) Only hamming  (C) Only CRC  (D) Only parity

**Answer: (A) Viterbi - maximum likelihood decoding of convolutional codes**

---

### Q9. (Moderate) Cyclic redundancy check (CRC) detects:
(A) Burst errors (good at bursts)  (B) Only single  (C) Corrects all  (D) Nothing

**Answer: (A) CRC - excellent burst error detection, no correction**

---

### Q10. (Moderate) Hamming (7,4) code word length and correct:
(A) 7 bits, corrects 1 error  (B) 4 bits  (C) 11  (D) corrects 2

**Answer: (A) 7-bit codeword, corrects single bit (dmin=3)**
