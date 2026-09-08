# Digital Circuits - Memory Tricks

## Number System Mnemonics
- **Binary** = **B**ase 2 = **B**irth of all digital
- **Hexadecimal** = **H**ex = **H**uman-friendly binary (4 bits each)
- **Octal** = **O**ctal = **O**lder than hex (3 bits each)

## K-Map Gray Code Memory
- Columns must be: **00, 01, 11, 10** (one-bit changes only)
- Mnemonic: "**00 01 11 10**" - "Oh-Oh, Oh-One, One-One, One-Zero"
- NEVER: 00, 01, 10, 11 (two bits change at once - WRONG)

## De Morgan's Laws Memory
- **NOR = bubbled AND**: (A+B)' = A'.B'
- **NAND = bubbled OR**: (A.B)' = A'+B'
- Visualize: Push bubble through, change gate type (AND<->OR)

## Flip-Flop Mnemonics
- **D Flip-Flop**: D = Delay (output follows input after clock)
- **T Flip-Flop**: T = Toggle (T=1 flips, T=0 holds)
- **SR Flip-Flop**: S = Set (Q=1), R = Reset (Q=0)
- **JK Flip-Flop**: J = jump, K = kill (J sets, K resets, both toggle)

## FSM State Assignment Trick
- Use **Gray code** for state assignment
- Only 1 bit changes between adjacent states
- Reduces logic complexity

## VHDL Memory Tricks
- **Signal** = **S**low (gets value after delta delay)
- **Variable** = **V**ery fast (gets value immediately)
- **Process** = **P**er clock (sequential code)
- **Concurrent** = **C**ompeting (all statements execute simultaneously)

## ADC Ranking Memory
- **Flash** = **F**astest (but most expensive)
- **SAR** = **S**uccessive = **S**equential approximation (moderate speed)
- **Dual Slope** = **D**ead slow but most accurate

## Metastability Mnemonic
- "**Meta** = **Messy**" (output is in a mess between 0 and 1)
- **2-FF synchronizer** = "**Two** heads are better than **one**" (two FFs prevent metastability better than one)
