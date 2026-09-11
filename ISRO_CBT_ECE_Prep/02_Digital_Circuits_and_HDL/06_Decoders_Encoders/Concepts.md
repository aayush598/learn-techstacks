# Decoders and Encoders - Concepts

## Decoder
- n inputs -> up to 2^n outputs (one active at a time)
- Activated output = binary value of inputs
- 2-to-4, 3-to-8, 4-to-16 decoders
- Used to select one of many lines (address decoding)

### 2-to-4 Decoder
```
Inputs A,B -> Outputs Y0..Y3
Y0 = A'B', Y1 = A'B, Y2 = AB', Y3 = AB
Only output corresponding to input code is HIGH (with enable)
```

## Encoder
- 2^n inputs -> n outputs (inverse of decoder)
- One active input -> binary code on outputs
- 4-to-2, 8-to-3 encoders
- Problem: if multiple inputs active, ambiguous output

### 4-to-2 Encoder
```
Inputs D0-D3 -> Outputs A,B
A = D1 + D3, B = D2 + D3 (which input is active)
```

## Priority Encoder
- Solves multiple-active ambiguity
- Encodes HIGHEST-priority active input
- 4-to-2 priority encoder: priority D3>D2>D1>D0
- Additional valid/output flag (V) when any input active
- Used in interrupt controllers

### 4-to-2 Priority (priority D3 highest)
```
V = D0+D1+D2+D3 (any active)
A = D2 D3' + D3
B = D1 D3' + D2 D3' ... (with prior tie)
```

## Decoder with Enable
```
Enable active-low typically: only decode when enabled
Inactive: all outputs off
Used to build larger decoders / address decode
Example: 3-to-8 from 2-to-4 + enable logic
```

## Decoder as Demux/Function generator
```
Decoder + OR gates can realize any Boolean function
Each minterm available on a decoder output
Function F = OR of decoder outputs for minterms of F
(Alternative to K-map-based logic)
```

## Applications
```
- Memory address decoding (select RAM/ROM chips)
- Seven-segment display drive
- Multiplexer/demultiplexer building
- Function implementation
- Binary-to-Gray, code conversion
```

## Encoder vs Decoder
| Feature | Decoder | Encoder |
|---------|---------|---------|
| Inputs | n | 2^n |
| Outputs | 2^n | n |
| Function | code -> one line | line -> code |
| Priority | - | priority option |
| Direction | source to select | sensing to code |

---

## ISRO Key Points
- Decoder: n to 2^n
- Encoder: 2^n to n
- Priority encoder: handles multiple, highest priority
- Decoder outputs = minterms (useful for logic)
- Enable bit for cascading
- Decoder + OR = universal function generator
