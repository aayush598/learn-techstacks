# Channel Coding and Error Control - Concepts

## Need for Channel Coding
- Add redundant bits to detect/correct transmission errors
- Trade bandwidth for reliability
- Fundamental: Shannon says coding can approach capacity

## Error Detection vs Correction
- Detection: know an error occurred (retransmit)
- Correction: locate AND fix error automatically (FEC)
- FEC (Forward Error Correction): used when retransmission impractical

## Block Codes
- Message divided into blocks of k bits
- Each block encoded to n bits (n > k): (n,k) code
- Code rate: R = k/n (information fraction)

### Hamming Distance
```
d_min = minimum Hamming distance between any two codewords
Error detection capability: can detect up to (d_min - 1) errors
Error correction capability: can correct up to floor((d_min-1)/2) errors
```

## Hamming (7,4) Code
- k=4 message bits, n=7 codeword (3 parity bits)
- d_min = 3
- Corrects 1 error, detects 2 errors
- Parity check matrix H, generator matrix G
- Codeword c = m*G, syndrome s = r*H^T

## Generator & Parity Check
```
G (k x n): generates codewords c = m G
H ((n-k) x n): parity check, valid codewords satisfy H c^T = 0
Syndrome: s = H r^T = H e^T (depends only on error e)
If s = 0: no (detectable) error
```

## Linear Block Codes
- Codewords form a vector space (linear combination property)
- Systematic code: first k bits are original message, rest parity
- Hamming codes: all single-error-correcting with minimal redundancy

## Convolutional Codes
- Continuous encoding with memory (shift register)
- Constraint length K: number of input bits affecting output
- Rate R = k/n
- Decoded with **Viterbi algorithm** (maximum-likelihood sequence)
- No fixed block structure
- Used in: satellite, deep space, cellular

## Cyclic Codes
- Shift of a codeword is also a codeword
- Polynomial representation (CRC uses this)
- Efficient encoders (shift registers)
- Ex: CRC (Cyclic Redundancy Check) for error detection

## BCH / Reed-Solomon
- BCH: powerful multiple-error-correcting block codes
- Reed-Solomon: non-binary, corrects bursts of errors
- Used in: CDs/DVDs, QR codes, space communication

## ARQ (Automatic Repeat reQuest)
- Error detection + retransmission
- Stop-and-wait, Go-back-N, Selective repeat
- Uses feedback channel

## Interleaving
- Spreads burst errors across time
- Converts burst errors into random errors (easier to correct)
- Used with FEC codes

---

## ISRO Key Points
- d_min relation to detection/correction - most tested
- Hamming (7,4): corrects 1, detects 2
- Code rate R = k/n
- Syndrome s = H r^T, s=0 no error
- Convolutional: Viterbi decoder
