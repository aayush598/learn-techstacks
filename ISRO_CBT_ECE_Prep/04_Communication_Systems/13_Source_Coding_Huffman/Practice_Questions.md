# Source Coding / Huffman - Practice Questions

---

### Q1. (Easy) Huffman coding is used for:
(A) Lossless source compression  (B) Error correction  (C) Modulation  (D) Encryption

**Answer: (A) Lossless source coding (compression)**

---

### Q2. (Moderate) Huffman code property:
(A) Prefix-free (no code is prefix of another)  (B) Fixed length  (C) Adds redundancy  (D) Corrupts

**Answer: (A) Prefix-free - instantaneously decodable**

---

### Q3. (Moderate) Huffman assigns shorter codes to:
(A) More probable symbols  (B) Less probable  (C) Random  (D) Longest first

**Answer: (A) Shorter codes to frequent (higher-probability) symbols**

---

### Q4. (Moderate) Average code length L:
(A) sum p_i * l_i  (B) sum l_i  (C) max l_i  (D) min l_i

**Answer: (A) L = Σ p_i l_i (weighted by probability)**

---

### Q5. (Moderate) Huffman inefficiency: avg length relative to entropy:
(A) L >= H (within 1 bit)  (B) L < H  (C) L = 0  (D) L large only

**Answer: (A) H <= L < H+1 (optimal, at most 1 bit above entropy)**

---

### Q6. (Moderate) Shannon-Fano vs Huffman:
(A) Huffman optimal (better)  (B) Same  (C) Shannon better  (D) None

**Answer: (A) Huffman is optimal (minimum redundancy) prefix code**

---

### Q7. (Moderate) Prefix-free means decoding is:
(A) Unambiguous/instantaneous  (B) Needs lookahead only  (C) Impossible  (D) Lossy

**Answer: (A) Uniquely & instantaneously decodable (no ambiguity)**

---

### Q8. (Moderate) If symbols equally likely, Huffman length:
(A) Near log2 N (uniform)  (B) All very short  (C) Varies wildly  (D) Zero

**Answer: (A) ~log2 N each when equiprobable (no compression vs fixed)**

---

### Q9. (Moderate) Compression reduces:
(A) Bits needed (redundancy)  (B) Information  (C) Accuracy  (D) Entropy below info

**Answer: (A) Reduces redundant bits - preserves information (lossless)**

---

### Q10. (Moderate) Huffman tree built by:
(A) Merging two smallest probabilities  (B) Two largest  (C) Random  (D) Only one symbol

**Answer: (A) Repeatedly merge two lowest-probability symbols**
