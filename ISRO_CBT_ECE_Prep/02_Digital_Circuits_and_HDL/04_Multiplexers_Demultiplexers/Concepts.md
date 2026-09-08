# Multiplexers and Demultiplexers - Concepts

## Multiplexer (MUX) - Data Selector
- Selects one of many input lines and forwards to single output
- 2^n inputs, n select lines, 1 output
- Also called data selector

### Common MUX Sizes:
| MUX | Inputs | Select Lines | Enable |
|-----|--------|-------------|--------|
| 2:1 | 2 | 1 | Optional |
| 4:1 | 4 | 2 | Optional |
| 8:1 | 8 | 3 | Optional |
| 16:1 | 16 | 4 | Optional |

### MUX as Universal Logic Element
- Any n-variable Boolean function can be implemented using 2^(n-1):1 MUX
- For 3 variables: 4:1 MUX needed (2 select lines, remaining variable on inputs)
- For 4 variables: 8:1 MUX needed

### Function Implementation Using MUX
**Method:** 
1. Write truth table
2. Connect variables to select lines
3. Based on select line combination, connect appropriate input (0, 1, variable, or complement)

### Example: Implement f(A,B,C) = Sigma m(1,3,5,7) using 4:1 MUX
- Connect A,B to select lines S1,S0
- For AB=00: output should be 0 (no minterms 0,1... wait, m1=001)
- Need to re-examine based on truth table

---

## Demultiplexer (DEMUX) - Data Distributor
- Takes single input and routes to one of many outputs
- 1 input, n select lines, 2^n outputs
- Inverse operation of MUX

### DEMUX Applications:
- Data distribution
- Serial to parallel conversion
- 7-segment decoder (special case)

---

## Decoder
- n input lines, 2^n output lines
- Only one output is active (HIGH or LOW) at a time
- Used for memory address decoding, 7-segment display

### Common Decoders:
- 2-to-4 decoder (2 inputs, 4 outputs)
- 3-to-8 decoder (3 inputs, 8 outputs)
- BCD to 7-segment decoder (4 inputs, 7 outputs)

### Decoder as Logic Function Implementer:
- Any n-variable SOP function can be implemented using n-to-2^n decoder + OR gate
- Connect variables to decoder inputs, OR together minterm outputs

---

## ISRO Key Points
- MUX with n select lines can implement any function of (n+1) variables
- 4:1 MUX implements any 3-variable function
- 8:1 MUX implements any 4-variable function
- Decoder + OR = SOP implementation
- MUX is more flexible than decoder for function implementation
