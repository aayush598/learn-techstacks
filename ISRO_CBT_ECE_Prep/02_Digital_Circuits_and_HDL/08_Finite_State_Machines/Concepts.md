# Finite State Machines - Concepts

## Moore Machine
- Output depends ONLY on current state
- Output associated with each state
- Slower (output changes after state transition)
- More states needed for same function
- Output = f(current state)

## Mealy Machine
- Output depends on current state AND current input
- Output associated with each transition
- Faster (output changes with input)
- Fewer states needed for same function
- Output = f(current state, input)

### Key Difference:
- Moore: Output = g(State)
- Mealy: Output = g(State, Input)
- Mealy can have glitches (output changes asynchronously with input)

---

## FSM Design Steps
1. **State Diagram:** Draw state bubble diagram with transitions
2. **State Table:** Create table with present state, input, next state, output
3. **State Assignment:** Assign binary codes to states
4. **Flip-Flop Excitation:** Determine required FF inputs
5. **K-Maps:** Minimize next-state and output logic
6. **Implementation:** Draw circuit

---

## State Reduction
- Two states are equivalent if:
  - They produce same output for all input sequences
  - They can be merged into one state
- Implication table method for finding equivalent states
- Reduces number of flip-flops needed

---

## Common ISRO FSM Problems
- **Sequence Detector:** Detect specific bit pattern (e.g., 101, 1101)
- **101 Sequence Detector:**
  - States: S0 (reset), S1 (got 1), S2 (got 10), S3 (got 101 = detected)
  - Mealy: 4 states, output on transition
  - Moore: 4 states, output in state S3

---

## ISRO Key Points
- Moore: Output depends on state only (no glitches)
- Mealy: Output depends on state + input (can glitch)
- State reduction using implication table
- Sequence detector is most common ISRO FSM question
- Mealy machine needs fewer states than Moore for same function
