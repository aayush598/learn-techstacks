# Information Theory - Practice Questions

---

### Q1. (Easy) Information in event with probability p:
(A) I = log2(1/p)  (B) I = p  (C) I = 1/p  (D) I = log(p)

**Answer: (A) I = log2(1/p) bits (less probable = more info)**

---

### Q2. (Moderate) Entropy H of source with symbol probabilities:
(A) -sum p log2 p  (B) sum p  (C) max p  (D) log N

**Answer: (A) H = -Σ p_i log2 p_i bits/symbol**

---

### Q3. (Moderate) Entropy of binary source p and 1-p:
(A) H = -p log p - (1-p)log(1-p)  (B) 1  (C) p  (D) p^2

**Answer: (A) Binary entropy H(p) = -p log2 p - (1-p) log2(1-p)**

---

### Q4. (Moderate) Max entropy of N equiprobable symbols:
(A) log2 N  (B) 1  (C) N  (D) 0

**Answer: (A) Hmax = log2 N bits (equally likely)**

---

### Q5. (Moderate) Channel capacity C (Shannon, bandwidth B, SNR):
(A) C = B log2(1 + SNR)  (B) C = B/SNR  (C) C = B SNR  (D) C = 2B

**Answer: (A) C = B log2(1 + SNR) bits/s**

---

### Q6. (Moderate) Doubling bandwidth roughly:
(A) Increases C logarithmically (not linear)  (B) Doubles C  (C) Halves  (D) No change

**Answer: (A) Capacity grows ~log - doubling B does NOT double C (log dependence)**

---

### Q7. (Moderate) Source coding (Huffman) aims to:
(A) Reduce redundancy (avg code length ~ entropy)  (B) Increase bits  (C) Add noise  (D) Encrypt

**Answer: (A) Lossless compression - minimize avg length approaching entropy**

---

### Q8. (Moderate) Huffman code is:
(A) Prefix-free (uniquely decodable), optimal  (B) Fixed length only  (C) Not decodable  (D) Noisy

**Answer: (A) Prefix-free variable-length optimal source code**

---

### Q9. (Moderate) Redundancy of source:
(A) (Hmax - H)/Hmax  (B) H  (C) Hmax+H  (D) 1-H

**Answer: (A) Redundancy = 1 - H/Hmax**

---

### Q10. (Moderate) Theorem: error-free transmission possible if rate:
(A) R < C (capacity)  (B) R > C  (C) R = 2C  (D) any R

**Answer: (A) Shannon: reliable (arbitrarily low error) if R < C**
