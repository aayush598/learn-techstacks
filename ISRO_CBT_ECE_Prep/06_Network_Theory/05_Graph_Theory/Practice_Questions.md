# Graph Theory and Network Topology - Practice Questions

## Instructions
Each question has one correct option. A connected network with `n` nodes and `b` branches has `n−1` independent node equations and `b−n+1` independent loops.

## Questions

### Q1. Number of tree branches [Easy]
A connected network has 5 nodes. A tree contains how many independent branches?

A. 3  
B. 4  
C. 5  
D. 6

**Answer:** B  
**Explanation:** A spanning tree has `n−1=5−1=4` branches.

### Q2. Number of independent loops [Easy]
A connected planar network has 8 nodes and 14 branches. The number of independent loops is:

A. 5  
B. 6  
C. 7  
D. 8

**Answer:** C  
**Explanation:** Independent loops `=b−n+1=14−8+1=7`.

### Q3. Nodal conductance matrix [Medium]
Node 1 connects to ground through conductances `G1` and `G3`, and node 1 connects to node 2 through `G2`. With no injected current, the coefficient matrix in nodal analysis is:

A. `[[G1+G3, 0], [0, G2]]`  
B. `[[G1+G2, −G2], [−G2, G2+G3]]`  
C. `[[G1, G2], [G2, G3]]`  
D. `[[1/G1+1/G3, 1/G2], [1/G2, 1/G2]]`

**Answer:** B  
**Explanation:** Self-conductances appear on the diagonal and mutual conductances appear off-diagonal with a negative sign.

### Q4. Rank of incidence matrix [Easy]
For a connected network with 6 nodes, the rank of a reduced incidence matrix is:

A. 1  
B. 5  
C. 6  
D. 7

**Answer:** B  
**Explanation:** A reduced incidence matrix has rank `n−1=5`.

### Q5. Fundamental tie sets [Medium]
A connected graph has 7 nodes and 12 branches. The number of fundamental tie sets equals:

A. 4  
B. 5  
C. 6  
D. 7

**Answer:** C  
**Explanation:** One tie set is selected per independent loop, so the number is `12−7+1=6`.

### Q6. Complete graph branches [Easy]
How many branches are in a complete graph with 5 nodes?

A. 5  
B. 8  
C. 10  
D. 12

**Answer:** C  
**Explanation:** `K_n` has `n(n−1)/2` edges; for `n=5`, the count is `5×4/2=10`.

### Q7. Spanning trees of K4 [Medium]
How many distinct spanning trees does the complete graph `K4` have?

A. 4  
B. 8  
C. 12  
D. 16

**Answer:** D  
**Explanation:** Cayley's formula gives `n^(n−2)=4²=16` spanning trees for `K4`.

### Q8. Planar graph bound [Medium]
A simple connected planar graph with 5 vertices can have at most how many edges?

A. 6  
B. 8  
C. 9  
D. 10

**Answer:** C  
**Explanation:** For a simple planar graph, `E_max=3V−6=3×5−6=9` for `V≥3`.

### Q9. Graph reciprocity [Easy]
For the associated 2×2 Z-parameter matrix, reciprocity requires:

A. `Z11=Z22` only  
B. `Z12=Z21`  
C. `Z11+Z22=0`  
D. `Z12Z21=0`

**Answer:** B  
**Explanation:** The off-diagonal transfer impedances must be equal for a reciprocal network.

### Q10. Minimal connected graph [Easy]
What is the minimum number of branches needed to connect 8 distinct nodes into one connected network?

A. 6  
B. 7  
C. 8  
D. 9

**Answer:** B  
**Explanation:** A connected network needs at least `n−1=7` branches, which is exactly the number in a tree.

## Answer Key
1. B  
2. C  
3. B  
4. B  
5. C  
6. C  
7. D  
8. C  
9. B  
10. B
