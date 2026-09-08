# Engineering Mathematics - Complete Formula Sheet

## Linear Algebra
```
Determinant: det(A), det(AB) = det(A)*det(B)
Inverse: A^(-1) = adj(A)/det(A)
Rank: Maximum number of linearly independent rows/columns
Eigenvalue: det(A-lambda*I) = 0
Eigenvector: (A-lambda*I)*v = 0
Trace = Sum of eigenvalues
Determinant = Product of eigenvalues
Cayley-Hamilton: A satisfies its own characteristic equation
Similar matrices: B = P^(-1)*AP (same eigenvalues)
Singular matrix: det(A) = 0 (at least one eigenvalue = 0)
```

## Calculus
```
Chain rule: d/dx[f(g(x))] = f'(g(x))*g'(x)
Product rule: d/dx[f*g] = f'*g + f*g'
Integration by parts: integral u*dv = uv - integral v*du
Taylor series: f(x) = sum f^(n)(a)*(x-a)^n/n!
L'Hopital: lim f(x)/g(x) = lim f'(x)/g'(x) (if 0/0 or inf/inf)
```

## Differential Equations
```
First order linear: y' + P(x)*y = Q(x)
  IF = e^(integral P(x)dx)
  y = (1/IF)*(integral Q*IF dx + C)

Second order: ay'' + by' + cy = 0
  Characteristic: ar^2 + br + c = 0
  Roots r1, r2:
    Real distinct: y = C1*e^(r1*x) + C2*e^(r2*x)
    Real repeated: y = (C1+C2*x)*e^(r*x)
    Complex: y = e^(ax)*(C1*cos(bx)+C2*sin(bx))
```

## PDEs
```
Heat equation: du/dt = k*(d2u/dx2)
Wave equation: d2u/dt2 = c^2*(d2u/dx2)
Laplace: d2u/dx2 + d2u/dy2 = 0

Separation of variables: u(x,t) = X(x)*T(t)
For heat eq: X'' + lambda*X = 0, T' + k*lambda*T = 0
```

## Probability
```
Conditional: P(A|B) = P(A and B)/P(B)
Bayes: P(Ai|B) = P(B|Ai)*P(Ai)/Sum P(B|Aj)*P(Aj)
Total probability: P(B) = Sum P(B|Ai)*P(Ai)
Independence: P(A and B) = P(A)*P(B)
```

## Probability Distributions
```
Binomial: P(X=k) = C(n,k)*p^k*(1-p)^(n-k), mean=np, var=np(1-p)
Poisson: P(X=k) = e^(-lambda)*lambda^k/k!, mean=var=lambda
Uniform: f(x) = 1/(b-a), mean=(a+b)/2, var=(b-a)^2/12
Normal: f(x) = (1/(sigma*sqrt(2pi)))*e^(-(x-mu)^2/(2*sigma^2))
Exponential: f(x) = lambda*e^(-lambda*x), mean=1/lambda
```

## Complex Analysis
```
Cauchy-Riemann: du/dx = dv/dy, du/dy = -dv/dx
Residue theorem: integral f(z)dz = 2*pi*j*Sum(residues)
Residue at simple pole: Res = lim(z->z0) (z-z0)*f(z)
```
