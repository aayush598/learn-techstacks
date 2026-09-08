# Signal Flow Graphs - Concepts

## 1. Introduction
- A **Signal Flow Graph (SFG)** is a graphical representation of a set of linear algebraic equations.
- Alternative to block diagrams for representing and analyzing transfer functions.
- Especially useful for complex multi-loop systems.
- Based on **Mason's Gain Formula** for direct computation of overall gain.

## 2. Basic Elements

### Nodes
- Represent variables (signals).
- Two types:
  - **Source (Input) node**: only outgoing branches (independent variable).
  - **Sink (Output) node**: only incoming branches.
  - **Mixed node**: has both incoming and outgoing branches.

### Branches
- Directed line segments connecting two nodes.
- Each branch has a **transmittance (gain)** = transfer function along that branch.
- Direction is indicated by an arrow.

### Paths
- **Path**: A continuous sequence of branches traversed in direction of arrows.
- **Forward Path**: A path from an input (source) node to an output (sink) node that does not traverse any node more than once.
- **Forward Path Gain**: Product of transmittances along a forward path.

### Loops
- **Loop**: A closed path starting and ending at the same node, traversing each node only once.
- **Loop Gain**: Product of transmittances around a loop.
- **Self-loop**: A branch from a node back to itself.
- **Non-touching loops**: Two loops that do not share any node.
- **Non-touching with forward path**: A loop that shares no node with a given forward path.

## 3. Construction Rules
- Nodes represent variables; assign a node for each variable/point.
- For a summing: incoming branches to a node.
- For a branch point (pickoff): outgoing branches from a node.
- Standard conversion from block diagram:
  - Block → branch with transmittance G(s).
  - Summing/pickoff point → node.
  - Signal flow direction matches block diagram arrows.

## 4. Basic Algebra in SFG

### Series (cascade)
Two branches in series (node between them) combine: gains multiply.

### Parallel
Two branches from the same node to the same node: gains add.

### Feedback loop
A loop with forward gain G and feedback gain H reduces to:
T = G/(1 ± GH).

## 5. Mason's Gain Formula
The overall transfer function between a source and sink:

**T = (1/Δ) · Σ_k P_k·Δ_k**

Where:
- **P_k** = gain of the k-th forward path.
- **Δ** = determinant of the graph = 1 - Σ(individual loop gains) + Σ(gain products of combinations of 2 non-touching loops) - Σ(combinations of 3 non-touching loops) + ...
- **Δ_k** = value of Δ with all loops touching the k-th forward path removed.

### Steps
1. Identify all forward paths and gains P_k.
2. Identify all individual loops and gains.
3. Identify all non-touching loop combinations.
4. Compute Δ.
5. For each forward path, remove loops touching it, compute Δ_k.
6. Apply formula.

## 6. Signal Flow Graph Reduction Rules (algebraic)
- Node elimination: eliminate intermediate nodes one at a time.
- Combine series: multiply gains.
- Combine parallel: add gains.
- Remove self-loops: a self-loop L at node X with input branch inbound factor — can eliminate by dividing.
- Feedback loops reduced via formula.
- Simplification may become complex; Mason's formula is preferred for large graphs.

## 7. Transfer Function via SFG for Closed Loop
Given forward path gain P and feedback path gain H:
T = P/(1 - LG), where LG = loop gain (including feedback sign).
For negative feedback, LG is negative in Mason's formulation.

## 8. Advantages of SFG
- Direct algebraic formula (Mason's) without sequential reduction.
- Clearly shows forward paths, loops, and non-touching structure.
- Handles multiloop, multi-input/output systems systematically.
- Easier for computing transfer function compared to block diagram trial-and-error.

## 9. Applications
- Control systems: closed-loop TF computation.
- Filters, network analysis: computing transfer functions of graphs.
- Feedback amplifier analysis.
- Systems with multiple feedback loops.

## 10. Common Pitfalls
1. Missing loops when identifying non-touching combinations.
2. Forgetting to include a negative sign for negative feedback in loop gain.
3. Uncounted forward paths where a path revisits a node (not allowed).
4. Incorrect Δ_k determination (must remove loops touching the path).
5. Treating touching loops as non-touching.

## 11. ISRO Exam Relevance
- Straightforward Mason's formula questions are common.
- Usually 1-2 forward paths and 2-3 loops.
- Non-touching loop products required in Δ.
- Practice identifying loops systematically.

## 12. Relationship to Block Diagrams
- Block diagrams and SFGs are equivalent representations.
- Any block diagram can be converted to SFG and vice versa.
- Mason's formula applies only to SFG (or converted block diagram).
- Both yield identical transfer functions.
