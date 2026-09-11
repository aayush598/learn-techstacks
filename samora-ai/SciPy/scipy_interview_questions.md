# SciPy — 100 Interview Q&A

---

## Q1: What is SciPy?
**A:** SciPy is an open-source Python library for scientific and technical computing. It builds on NumPy and adds high-level functions for optimization, linear algebra, integration, statistics, sparse matrices, signal processing, image processing, and interpolation.

## Q2: What is the difference between NumPy and SciPy?
**A:** NumPy provides fast N-dimensional array objects, basic linear algebra, Fourier transforms, and random number generation. SciPy builds on top of NumPy and adds specialized scientific tools such as optimizers, integrators, statistical tests, sparse matrices, and signal filters. NumPy is the foundation, and SciPy is the toolbox that uses it.

## Q3: How is SciPy related to LAPACK and BLAS?
**A:** SciPy routines, especially those in the linear algebra module, are built on top of optimized Fortran libraries called LAPACK and BLAS. These libraries provide highly tuned implementations of matrix operations, which is why SciPy linear algebra can be much faster than naive Python loops.

## Q4: What are the main submodules of SciPy?
**A:** The main submodules are optimize, linalg, integrate, stats, sparse, interpolate, signal, fft, ndimage, cluster, special, constants, spatial, and io. Each one handles a distinct area such as optimization, linear algebra, numerical integration, statistics, or signal processing.

## Q5: How do you check the installed version of SciPy?
**A:** Run import scipy and then print(scipy.__version__). You can also check the version from the terminal with pip list or pip show scipy.

## Q6: What is the recommended way to import SciPy submodules?
**A:** Import each submodule explicitly, for example from scipy import optimize, linalg, integrate, or stats. Avoid importing the entire scipy package because it is large, and most functions live in specific submodules.

## Q7: Does SciPy work without NumPy?
**A:** No. SciPy depends on NumPy, and its data structures are NumPy arrays. You must install NumPy before SciPy because all SciPy functions expect NumPy array inputs.

## Q8: What is the scipy.optimize module used for?
**A:** The optimize module provides tools for finding the minimum of a function, solving nonlinear equations, fitting curves to data, and solving linear programming problems. Common functions are minimize, fsolve, curve_fit, linprog, and least_squares.

## Q9: What is scipy.optimize.minimize, and how do you call it?
**A:** minimize finds the minimum of a scalar or vector function. You call it with a function f(x), an initial guess x0, and optional method and bounds. For example, result equals minimize(f, x0), where result.fun holds the minimum value and result.x holds the optimum point.

## Q10: Is scipy.optimize.minimize guaranteed to find the global minimum?
**A:** No. Most methods in minimize are local optimizers, so they can converge to a local minimum that is not the global one. To search for a global minimum, you can run the optimizer from many different starting points or use differential_evolution.

## Q11: What is scipy.optimize.fsolve?
**A:** fsolve finds the roots of a system of nonlinear equations. You give it a function f(x) and an initial guess, and it returns the x values where f(x) is approximately zero. It uses iterative methods such as Newton or secant, so it needs a reasonably good initial guess.

## Q12: What is the difference between fsolve and root?
**A:** root is a more general root-finding function that supports several solvers, including ones that use Jacobian information, and it returns detailed results. fsolve is a simpler wrapper and is often easier to use for small problems.

## Q13: How do you fit a curve to data in SciPy?
**A:** You use scipy.optimize.curve_fit. It takes a model function, the independent data x, and the observed y data, and it returns the best-fit parameters and their covariance. You can also provide an initial guess through the p0 argument and bounds through the bounds argument.

## Q14: What does curve_fit return?
**A:** curve_fit returns two outputs. The first is an array of the best-fit parameter values. The second is a covariance matrix, and the square roots of its diagonal entries give the standard errors of the parameters.

## Q15: What is scipy.optimize.linprog?
**A:** linprog solves linear programming problems, where the objective function and all constraints are linear. You supply the cost vector c, the inequality constraint matrices and vectors, and optional bounds, and it returns the optimal solution and the objective value.

## Q16: What is scipy.optimize.least_squares used for?
**A:** least_squares solves nonlinear least-squares problems. It is commonly used for curve fitting and for solving systems where the sum of squared residuals is minimized. It supports bounds on the variables and several algorithms such as lm, trf, and dogbox.

## Q17: What optimization methods are available in minimize?
**A:** minimize supports many methods. Common ones are Nelder-Mead for derivative-free problems, BFGS for smooth problems, L-BFGS-B for large problems with bounds, SLSQP for constrained problems, and trust-constr for general constraints.

## Q18: When should you use L-BFGS-B?
**A:** Use L-BFGS-B when the optimization problem has many variables and you want bound constraints. It uses limited memory, so it works well even when the Hessian matrix would be too large to store.

## Q19: When should you use SLSQP?
**A:** Use SLSQP when the problem has equality or inequality constraints. It supports both linear and nonlinear constraints and handles bounded variables, which makes it a common choice for constrained optimization.

## Q20: How do you specify constraints in minimize?
**A:** You pass a constraints argument as a list of dictionaries. Each dictionary has a type key set to eq for equality or ineq for inequality, and a fun key that holds the constraint function. You can also add a jac key that provides the derivative of the constraint.

## Q21: What is differential_evolution?
**A:** differential_evolution is a global optimizer in scipy.optimize. Instead of relying on one starting point, it maintains a population of candidate solutions and evolves them over generations. It is useful for non-smooth or multimodal problems where local optimizers may get stuck.

## Q22: What is scipy.optimize.minimize_scalar used for?
**A:** minimize_scalar finds the minimum of a function of a single variable. You can give it a bracket, a bound, or just a starting point. It is convenient for quick one-dimensional optimizations.

## Q23: Why is the initial guess important for fsolve and minimize?
**A:** Iterative solvers start from the initial guess and move downhill. A poor guess can lead to divergence, a different root, or a local minimum. Always try multiple starting points and check the success flag and the residuals in the result object.

## Q24: What is scipy.integrate.quad?
**A:** quad computes the definite integral of a one-dimensional function using an adaptive Gauss-Kronrod method. It takes a function and the lower and upper limits, and it returns the integral value and an estimate of the absolute error.

## Q25: What is scipy.integrate.solve_ivp?
**A:** solve_ivp solves an initial-value problem for a system of ordinary differential equations. You provide a right-hand-side function, a time span, and initial conditions. It supports many methods, with RK45 as the default, plus options for dense output and event detection.

## Q26: What is the difference between odeint and solve_ivp?
**A:** solve_ivp is the modern and recommended interface for initial-value problems, with many methods and advanced options such as events and dense output. odeint is an older, simpler interface that is still available. For new code, prefer solve_ivp.

## Q27: What does the RK45 method mean in solve_ivp?
**A:** RK45 is an adaptive Runge-Kutta method. It uses a fourth-order and fifth-order pair to estimate the local error at each step, and it automatically adjusts the step size to keep the error within tolerance. The 45 describes the two orders of accuracy used.

## Q28: How do you compute multiple integrals in SciPy?
**A:** Use scipy.integrate.dblquad for double integrals and nquad for general nested integrals. The integration order is important in the argument order of the inner limits, so check the documentation for which variable is integrated first.

## Q29: How do you integrate data given as sample points instead of a function?
**A:** Use scipy.integrate.simpson for Simpson rule integration and cumulative_trapezoid for cumulative integration of sampled data. These functions accept arrays of y values and optional sample positions x.

## Q30: Can quad handle infinite integration limits?
**A:** Yes. Pass math.inf or negative infinity as the bound. quad transforms the integration internally and can handle improper integrals such as a normal distribution integrated from negative infinity to positive infinity.

## Q31: What do the two return values of quad mean?
**A:** quad returns a tuple. The first value is the estimate of the integral, and the second value is an upper bound on the absolute error of that estimate. Small error values indicate a reliable result.

## Q32: What is scipy.integrate.quad_vec?
**A:** quad_vec evaluates a vector-valued function with a single pass of adaptive quadrature. It is much faster than calling quad once for every output component when the integrand returns many values at once, for example a function that returns an array over frequency.

## Q33: What are distribution objects in scipy.stats?
**A:** scipy.stats provides dozens of probability distributions, for example norm for the normal, t for the Student t, chi2 for chi-squared, poisson, and expon. Each distribution object has methods such as pdf, cdf, ppf, and rvs.

## Q34: What do pdf, cdf, and ppf mean?
**A:** pdf is the probability density function value at a point. cdf gives the cumulative probability up to a point. ppf is the inverse of the cdf, also called the quantile function, so ppf(p) returns the value below which a fraction p of the distribution lies.

## Q35: How do you draw random samples from a distribution?
**A:** Use the rvs method with a size argument, for example norm.rvs(size equals 100). For reproducible results, pass the random_state parameter with a fixed integer or numpy RandomState object.

## Q36: What does the fit method do?
**A:** The fit method estimates the parameters of a distribution by maximum likelihood estimation. Given an array of data, it returns the parameter values that make the observed data most probable. For the normal distribution, this gives the sample mean and standard deviation.

## Q37: What is a frozen distribution?
**A:** A frozen distribution fixes the parameters of a distribution once, for example norm(loc equals 0, scale equals 1). The frozen object can then be reused for pdf, cdf, ppf, and rvs calls without passing the parameters again, which is faster and cleaner.

## Q38: What descriptive statistics does scipy.stats provide?
**A:** The describe function returns count, mean, variance, skewness, and kurtosis. Separate functions include gmean for geometric mean, hmean for harmonic mean, iqr for interquartile range, mode for the most frequent value, and moment for raw or central moments.

## Q39: What are skewness and kurtosis?
**A:** Skewness measures the asymmetry of a distribution. Positive skew means a longer right tail. Kurtosis measures how heavy the tails are compared to a normal distribution. scipy.stats can compute both per column or per sample.

## Q40: How do you interpret a p-value?
**A:** A p-value is the probability of observing a result at least as extreme as the one you got, assuming the null hypothesis is true. A common rule is to reject the null hypothesis when the p-value is below a chosen significance level such as 0.05.

## Q41: What is the difference between ttest_ind and ttest_rel?
**A:** ttest_ind compares the means of two independent groups with the two-sample Student t test. ttest_rel compares two related or paired measurements, for example the same subjects before and after treatment. The paired version accounts for the correlation between pairs.

## Q42: What is the difference between pearsonr and spearmanr?
**A:** pearsonr measures the strength of a linear relationship between two variables, and it requires roughly normally distributed numeric data. spearmanr measures a monotonic relationship using ranks, so it is robust to outliers and does not assume linearity. Both return a correlation coefficient and a p-value.

## Q43: What does scipy.stats.linregress do?
**A:** linregress performs simple linear regression on two numeric arrays. It returns the slope, intercept, correlation coefficient r, p-value, and standard error of the slope. It is the quick tool for fitting a straight line to two variables.

## Q44: What is scipy.stats.chi2_contingency used for?
**A:** chi2_contingency performs a chi-squared test of independence on a contingency table of counts. It tests whether two categorical variables are related. It returns the test statistic, p-value, degrees of freedom, and the expected counts under independence.

## Q45: What does scipy.stats.f_oneway do?
**A:** f_oneway performs a one-way analysis of variance, known as ANOVA. It tests whether the means of two or more independent groups are equal. It returns an F statistic and a p-value. It is the parametric extension of the two-sample t test to several groups.

## Q46: What do kstest and shapiro do?
**A:** kstest is the Kolmogorov-Smirnov one-sample test, which compares a sample against a reference distribution and measures the largest difference between the empirical and theoretical cumulative distributions. shapiro tests for normality and is most reliable for smaller sample sizes.

## Q47: What is the difference between a Type I and Type II error?
**A:** A Type I error rejects the null hypothesis when it is actually true, a false positive, and its probability is the significance level alpha. A Type II error fails to reject the null hypothesis when it is false, a false negative, and its probability relates to the power of the test.

## Q48: How do you compute a confidence interval in scipy.stats?
**A:** Use the interval method on a frozen distribution. For example, for a 95 percent interval on the standard normal, call norm.interval(0.95). For t-based intervals, use t.interval with the appropriate degrees of freedom and scale.

## Q49: What is scipy.stats.gaussian_kde?
**A:** gaussian_kde estimates a smooth probability density from a sample using kernel density estimation with Gaussian kernels. You can evaluate the density at any points and also sample new points from the estimated distribution. The bandwidth is chosen automatically by default.

## Q50: What is scipy.stats.probplot used for?
**A:** probplot creates a probability plot, often a Q-Q plot, that compares sample quantiles against the quantiles of a reference distribution. If the points fall roughly on a straight line, the sample approximately follows the reference distribution. It also returns the correlation coefficient as a fit-quality measure.
