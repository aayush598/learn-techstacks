# State Space - Practice Questions

## Section A: Conceptual

**Q1.** Write the standard state and output equations for an LTI system.
**A1.** ẋ = Ax + Bu; y = Cx + Du.

**Q2.** What are the dimensions of A, B, C, D?
**A2.** A: n×n, B: n×r, C: m×n, D: m×r.

**Q3.** What is the state transition matrix and its Laplace relation?
**A3.** Φ(t) = e^{At} = L⁻¹{(sI−A)⁻¹}.

**Q4.** When is a system controllable?
**A4.** When its controllability matrix Q_c=[B AB ... A^{n-1}B] has full rank n.

## Section B: Transfer Function from State Space

**Q5.** A = [[0,1],[−2,−3]], B = [[0],[1]], C = [1,0], D=0. Find G(s).
**A5.** det(sI−A)= det[[s,−1],[2,s+3]] = s(s+3)+2 = s²+3s+2.
adj(sI−A) = [[s+3,1],[−2,s]].
C(sI−A)⁻¹B = [1,0]·(1/det)[[s+3,1],[−2,s]]·[[0],[1]] = (1/det)[1,0]·[[1],[s]] = (1/det)[1] = 1/(s²+3s+2).

**Q6.** Given A=[[0,1],[−a₀,−a₁]], find characteristic equation.
**A6.** det(sI−A)=s²+a₁s+a₀=0.

**Q7.** A system has A = [[0,1],[−6,−5]]. Find poles.
**A7.** s²+5s+6=0 → (s+2)(s+3) → poles −2,−3.

## Section C: State Transition Matrix

**Q8.** Find e^{At} for A = [[0,1],[0,0]].
**A8.** (sI−A)⁻¹ = 1/s²·[[s,1],[0,s]]. e^{At} = [[1,t],[0,1]].

**Q9.** Find e^{At} for A = [[−3,0],[0,−2]].
**A9.** Diagonal: e^{At} = [[e^{−3t},0],[0,e^{−2t}]].

**Q10.** For A=[[0,ω],[−ω,0]], state transition matrix.
**A10.** e^{At} = [[cosωt, sinωt],[−sinωt, cosωt]].

## Section D: Controllability

**Q11.** A=[[0,1],[−2,−3]], B=[[0],[1]]. Controllable?
**A11.** Q_c=[B AB]=[[0,1],[1,−3]]. det=0·(−3)−1·1=−1≠0 → controllable.

**Q12.** A=[[0,1],[−2,−3]], B=[[1],[0]]. Controllable?
**A12.** Q_c=[B AB], AB=[[0],[−2]]. Q_c=[[1,0],[0,−2]]. det=−2≠0 → controllable.

**Q13.** A=[[1,2],[3,4]], B=[[1],[2]]. Controllable?
**A13.** AB=[[1+4],[3+8]]=[[5],[11]]. Q_c=[[1,5],[2,11]]. det=11−10=1≠0 → controllable.

## Section E: Observability

**Q14.** A=[[0,1],[−2,−3]], C=[1,1]. Observable?
**A14.** Q_o=[[C],[CA]]. CA=[1,1]·[[0,1],[−2,−3]] = [0−2,1−3]=[−2,−2]. Q_o=[[1,1],[−2,−2]]. det=1(−2)−1(−2)=0 → NOT observable.

**Q15.** A=[[0,1],[−2,−3]], C=[1,0]. Observable?
**A15.** CA=[1,0]·[[0,1],[−2,−3]]=[0,1]. Q_o=[[1,0],[0,1]]. det=1≠0 → observable.

**Q16.** A system with A=[[−1,0],[0,−3]], C=[1,0]. Observable?
**A16.** CA=[−1,0]. Q_o=[[1,0],[−1,0]]. det=0 → NOT observable (state x₂ invisible in output).

## Section F: Canonical Forms

**Q17.** G(s)=(s+3)/(s²+4s+7). Write controllable canonical form.
**A17.** a₀=7,a₁=4; b₀=3,b₁=1,b₂=0. A=[[0,1],[−7,−4]], B=[[0],[1]], C=[3,1], D=0.

**Q18.** Write observable canonical form for G(s)= (2s+1)/(s²+5s+6).
**A18.** A=[[0,−6],[1,−5]], B=[1,2]ᵀ, C=[0,1]. (Using b values adjusted.)

**Q19.** For G(s)=1/(s²+3s+2), give diagonal form.
**A19.** Poles −1,−2. A=diag(−1,−2). (B, C from partial fractions.)

## Section G: ISRO-Style

**Q20.** Given ẋ=Ax+Bu with A=[[−2,0],[0,−1]], is the system asymptotically stable?
**A20.** Eigenvalues −2,−1 both negative → asymptotically stable.

**Q21.** A=[[0,1],[−ω_n²,−2ζω_n]]. Identify the corresponding second-order system.
**A21.** Characteristic equation det(sI−A)=s²+2ζω_n s+ω_n². Standard second-order system.

**Q22.** A matrix A=[[-3,1],[1,-3]]. Find eigenvalues.
**A22.** det[[s+3,-1],[-1,s+3]]=(s+3)²−1=s²+6s+8=(s+2)(s+4). Eigenvalues −2,−4.

**Q23.** For A=[[0,1],[−2,−3]], B=[[1],[1]], determine if controllable.
**A23.** AB=[[1],[−2−3·1]]... AB=[[1],[−2·1−3·1]]=[[1],[−5]]. Q_c=[[1,1],[1,−5]]. det=(−5)−1=−6≠0 → controllable.

**Q24.** Using the relation G(s)=C(sI−A)⁻¹B+D, when is D nonzero important?
**A24.** When there is direct feedthrough from input to output (e.g., derivatives in numerator equal to denominator degree).

**Q25.** How many state variables does a 4th-order transfer function require?
**A25.** 4 (equal to the order).

## Common Mistakes
1. Wrong dimension ordering in Q_c and Q_o.
2. Inverting (sI−A) instead of (sI−A) for TF.
3. Forgetting the minus signs in companion matrices.
4. Confusing controllability and observability matrices/tests.
5. Applying final value / stability tests to states without checking eigenvalues.
