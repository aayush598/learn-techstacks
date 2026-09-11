# FFT Algorithms - Practice Questions

---

### Q1. (Easy) FFT is:
(A) Fast algorithm to compute DFT (O(N log N))  (B) Slower  (C) Analog  (D) Not DFT

**Answer: (A) Fast Fourier Transform - efficient DFT computation, O(N log N)**

---

### Q2. (Moderate) Direct DFT complexity:
(A) O(N^2)  (B) O(N log N)  (C) O(N)  (D) O(log N)

**Answer: (A) Direct DFT = O(N^2); FFT reduces to O(N log N)**

---

### Q3. (Moderate) Radix-2 FFT requires N:
(A) Power of 2  (B) Any integer  (C) Prime  (D) Odd

**Answer: (A) Radix-2 requires N = 2^k (power of two)**

---

### Q4. (Moderate) Number of stages in radix-2 FFT for N points:
(A) log2 N  (B) N  (C) N/2  (D) 2N

**Answer: (A) log2 N stages**

---

### Q5. (Moderate) Number of complex multiplications in radix-2 FFT:
(A) (N/2) log2 N  (B) N log N  (C) N^2  (D) N

**Answer: (A) ~(N/2) log2 N complex multiplications**

---

### Q6. (Moderate) Twiddle factor WN:
(A) e^{-j 2π/N}  (B) e^{j2π}  (C) 1  (D) j

**Answer: (A) WN = e^{-j2π/N} (rotates by 2π/N)**

---

### Q7. (Moderate) 1024-point radix-2 FFT stages:
(A) 10  (B) 512  (C) 1024  (D) 32

**Solution:** log2(1024) = 10
**Answer: (A) 10 stages**

---

### Q8. (Moderate) IFFT vs FFT difference:
(A) Conjugate twiddle + scale by 1/N  (B) None  (C) Only 2N  (D) sign only

**Answer: (A) IFFT uses e^{+j2π/N} and 1/N scaling**

---

### Q9. (Moderate) Decimation-in-time (DIT) reorders input in:
(A) Bit-reversed order  (B) Natural  (C) Descending  (D) Random

**Answer: (A) DIT - input in bit-reversed order, output natural**

---

### Q10. (Moderate) Frequency resolution of N-point DFT fs:
(A) fs/N  (B) fs*N  (C) N  (D) 1/N

**Answer: (A) Frequency resolution = fs/N (bin spacing)**
