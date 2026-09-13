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

## Q51: What is the importance of logpdf in scipy.stats?
**A:** logpdf computes the natural logarithm of the probability density function. It is numerically stable for extreme values where the density itself would underflow to zero. Use it for computing log-likelihoods in model fitting and for comparing probabilities in a log space.

## Q52: How do you create a custom continuous distribution in scipy.stats?
**A:** Subclass rv_continuous and implement the _pdf method, plus _cdf or support when needed. The framework provides default machinery for cdf, ppf, random sampling, and moments. Set the support with the support keyword if the distribution is bounded.

## Q53: What is a truncated normal distribution, and how do you work with it?
**A:** A truncated normal restricts the normal distribution to a range such as between a and b. scipy.stats.truncnorm represents it, and you pass the normalized bounds as a and b along with loc and scale. It is used when data is physically bounded, such as test scores or sensor readings.

## Q54: What is scipy.stats.expon used for?
**A:** expon models the exponential distribution, which describes time between events in a Poisson process. It has a single rate parameter encoded through loc and scale, with scale equal to the mean. The memoryless property means the remaining waiting time does not depend on the time already elapsed.

## Q55: How do you compute the correlation of ranks in scipy.stats?
**A:** Use spearmanr on two samples. It ranks the data and computes the Pearson correlation on the ranks, so it measures monotonic association and is robust to outliers. The result contains the correlation coefficient and a p-value for the null hypothesis of no association.

## Q56: What is scipy.stats.gmean used for?
**A:** gmean computes the geometric mean of a sample, which is the n-th root of the product of the values. It is appropriate for ratios, growth rates, and data that spans several orders of magnitude. Unlike the arithmetic mean, it is not distorted by large outliers.

## Q57: What is the difference between the mode and the median?
**A:** The mode is the most frequently occurring value, while the median is the middle value when data is sorted. scipy.stats.mode returns the modal value and its count, and the median is available in numpy and the scipy distributions. The mode is meaningful mainly for data with repeating values.

## Q58: How do you compute the variance and standard deviation with scipy?
**A:** scipy.stats.tstd computes the sample standard deviation using n minus 1 degrees of freedom by default. The tvar variant returns the sample variance. The std and var methods on distribution objects return the theoretical values of the underlying distribution.

## Q59: What is the interquartile range, and why is it useful?
**A:** The interquartile range, IQR, is the difference between the 75th and 25th percentiles, and scipy.stats.iqr computes it. It measures the spread of the middle half of the data and is robust to outliers. It is commonly used in box plots and in the outlier rule that flags values beyond 1.5 times the IQR.

## Q60: What is scipy.stats.zscore used for?
**A:** zscore standardizes a sample so that it has a mean of zero and a standard deviation of one. It returns how many standard deviations each value is from the mean. It is used to compare values across different scales and to flag outliers above a threshold such as 3.

## Q61: What is the Kruskal-Wallis test in scipy?
**A:** scipy.stats.kruskal performs the Kruskal-Wallis H test, the non-parametric alternative to one-way ANOVA. It compares the medians of two or more independent groups using ranks. It is preferred when the normality assumption for ANOVA is violated.

## Q62: What is the Mann-Whitney U test used for?
**A:** scipy.stats.mannwhitneyu tests whether two independent samples come from the same distribution. It is the non-parametric alternative to the two-sample t test and compares ranks rather than means. It is useful when the data is ordinal or not normally distributed.

## Q63: What is scipy.stats.wilcoxon used for?
**A:** wilcoxon performs the Wilcoxon signed-rank test for paired samples. It is the non-parametric alternative to the paired t test. It tests whether the distribution of differences between matched pairs is symmetric around zero.

## Q64: How do you test whether a sample is normally distributed?
**A:** Several options exist in scipy.stats. shapiro and normaltest test for normality directly. The Anderson-Darling test via anderson and the Kolmogorov-Smirnov test via kstest compare the sample against the normal distribution. No test proves normality, so combine the p-value with a visual histogram or a Q-Q plot.

## Q65: What is the Anderson-Darling test?
**A:** scipy.stats.anderson is a modification of the Kolmogorov-Smirnov test that gives more weight to the tails. It compares the empirical distribution against a reference distribution and returns the statistic and critical values for several significance levels. It is more sensitive than kstest for detecting deviations in the tails.

## Q66: What is a confidence interval for a population mean?
**A:** A confidence interval is a range that is likely to contain the true population mean with a stated probability, often 95 percent. For known variance use norm, and for unknown variance use the t distribution with the sample standard deviation. scipy.stats provides the interval method on frozen distributions for this purpose.

## Q67: How do you compute percentiles and quantiles in scipy.stats?
**A:** Use the ppf method of a distribution for theoretical quantiles, or numpy.percentile and numpy.quantile for empirical quantiles from data. scipy.stats also has functions such as scoreatpercentile. Quantiles and percentiles differ only in the scale, since a quantile of 0.5 equals the 50th percentile.

## Q68: What is scipy.stats.describe returned by the describe function?
**A:** describe returns a named tuple with nobs, minmax, mean, variance, skewness, and kurtosis. The minmax field holds the minimum and maximum values. It gives a quick summary of a data set without computing each statistic separately.

## Q69: How do you perform a one-sample t test in scipy?
**A:** Use scipy.stats.ttest_1samp with the sample array and the hypothesized population mean. It returns a test statistic and a two-tailed p-value. Set the alternative parameter to less or greater for one-sided hypotheses where supported.

## Q70: What is the difference between a one-tailed and a two-tailed test?
**A:** A two-tailed test checks whether a parameter is different from a target value in either direction. A one-tailed test checks only greater than or only less than. scipy.stats supports the alternative parameter in many tests, and the choice must be fixed before looking at the data.

## Q71: How do you simulate a normal distribution in scipy?
**A:** Call norm.rvs with a loc, scale, and size. For reproducibility pass random_state with a fixed seed. The same rvs method exists for every distribution in scipy.stats.

## Q72: What is a p-value, and how is it used in decision making?
**A:** A p-value is the probability of observing results at least as extreme as the sample, assuming the null hypothesis is true. A small p-value suggests that such results are unlikely under the null. The null hypothesis is typically rejected when the p-value is below the chosen significance level alpha.

## Q73: What is the difference between alpha and the p-value?
**A:** Alpha is the significance level chosen in advance, such as 0.05, and it sets the acceptable risk of a false rejection. The p-value is computed from the data and tells you how extreme the result is. Rejecting the null when the p-value is below alpha controls the rate of Type I errors.

## Q74: What are the errors in hypothesis testing called?
**A:** A Type I error rejects a true null hypothesis and has probability alpha. A Type II error fails to reject a false null hypothesis and relates to beta. The power of a test is one minus beta, the probability of correctly detecting a real effect.

## Q75: What is scipy.stats.sem used for?
**A:** sem computes the standard error of the mean, which is the sample standard deviation divided by the square root of the sample size. It measures how much the sample mean would vary across repeated samples. It is used directly when building confidence intervals.

## Q76: How do you measure the strength of agreement between two raters in scipy?
**A:** Use scipy.stats.cohen_kappa for inter-rater agreement on categorical judgments. It returns Cohen kappa, which accounts for agreement that happens by chance. Values near one indicate strong agreement.

## Q77: What is scipy.stats.entropy used for?
**A:** scipy.stats.entropy computes the Shannon entropy, or a relative entropy such as the Kullback-Leibler divergence when two arguments are given. The base parameter controls the logarithm base. Higher entropy values mean more uncertainty or randomness in the distribution.

## Q78: How do you work with the chi-squared distribution in scipy?
**A:** scipy.stats.chi2 represents the chi-squared distribution with a degrees-of-freedom parameter. It is used for goodness-of-fit tests, variance tests, and the distribution of the chi-squared test statistic. The ppf method provides critical values for confidence intervals on variance.

## Q79: What is scipy.stats.norm.fit and what does it return?
**A:** norm.fit estimates the parameters of a normal distribution from data using maximum likelihood. It returns the loc and scale values, which estimate the mean and the standard deviation. The fitted distribution can then be used for further probability calculations.

## Q80: How do you compare two independent group means when variances are unequal?
**A:** Use scipy.stats.ttest_ind with the equal_var parameter set to False. This applies the Welch test, which does not assume equal variances between groups. Welch t test is the safer default for real-world data.

## Q81: What is scipy.stats.f_oneway versus the Kruskal test?
**A:** f_oneway is the parametric one-way ANOVA based on the F distribution and assumes normally distributed groups. kruskal is its non-parametric rank-based alternative. Use ANOVA when assumptions hold, otherwise prefer kruskal.

## Q82: What is the geometric distribution in scipy.stats?
**A:** The geometric distribution models the number of trials until the first success in repeated independent trials. scipy.stats.geom provides its pmf and cdf among other methods. Each trial has a success probability p with mean one over p.

## Q83: How do you evaluate a probability density for many points efficiently?
**A:** The pdf and cdf methods accept array arguments directly, so pass the whole array instead of looping. For log-space work use logpdf and logcdf. These vectorized calls run in compiled code and are much faster than per-point functions.

## Q84: What is scipy.stats.binom and what does it do?
**A:** binom is the binomial distribution, which counts the number of successes in n fixed independent trials. Its parameters are n and p, and its methods include pmf, cdf, ppf, and rvs. It is the basis for proportion tests and coin-flip style probability problems.

## Q85: What does scipy.stats.poisson model?
**A:** poisson models the number of events occurring in a fixed interval given a constant average rate. Its single parameter mu is both the mean and the variance. It is used for call volumes, arrivals, and rare-event counting.

## Q86: How do you compute cumulative probabilities for discrete distributions?
**A:** Use the cdf method, which returns the probability of observing a value less than or equal to x. For the complementary upper tail use the survival function sf, which is one minus the cdf. The sf is numerically more stable for large values.

## Q87: What is the difference between pmf and pdf?
**A:** The pmf applies to discrete distributions and gives the exact probability of a single value. The pdf applies to continuous distributions and gives a density, not a probability, so it must be integrated over a range. scipy.stats uses pdf and pmf on their respective distribution types.

## Q88: How do you select a sample that reproduces a given distribution in scipy.stats?
**A:** Use the rvs method with the size argument, and fix random_state when reproducibility is needed. For inverse-transform sampling of a custom distribution, evaluate the ppf at uniform random values. This approach works for any distribution with a cdf.

## Q89: What is scipy.stats.gaussian_kde bandwidth?
**A:** The bandwidth controls the smoothness of the density estimate. scipy.stats.gaussian_kde selects a bandwidth automatically by Scott's rule by default, or Silverman's rule if requested. A small bandwidth fits the data closely, while a large bandwidth gives a smoother curve.

## Q90: How do you compute the covariance between two samples in scipy?
**A:** Use scipy.stats.covariance or numpy.cov for the covariance matrix. scipy.stats also provides cov with comparable behavior. The correlation coefficient normalizes the covariance to a range between negative one and one.

## Q91: What is scipy.stats.t for, and what is a degree of freedom?
**A:** scipy.stats.t is the Student t distribution used for testing means when the variance is unknown. The degrees of freedom typically equal the sample size minus one. As the degrees of freedom grow, the t distribution approaches the standard normal.

## Q92: What is the F distribution used for in scipy?
**A:** scipy.stats.f models the F distribution, which is the ratio of two scaled chi-squared variables. It is used in ANOVA for the ratio of between-group to within-group variance. The ppf provides critical values for comparing an F statistic.

## Q93: How do you perform a paired test with scipy.stats?
**A:** Use scipy.stats.ttest_rel for paired parametric data, or wilcoxon for the non-parametric paired case. Both expect two arrays of equal length with matched observations. The paired analysis removes subject-to-subject variation.

## Q94: What is the standard error of the proportion, and how do you compute it in scipy?
**A:** The standard error of a proportion is the square root of p times one minus p divided by n. Compute it directly with numpy and use norm.ppf for the critical value in a confidence interval. scipy.stats does not have a dedicated function for proportions.

## Q95: What is scipy.stats.beta used for?
**A:** beta is the beta distribution on the interval from zero to one. It is a flexible model for probabilities, proportions, and rates, and its parameters a and b shape the curve. In Bayesian analysis it is the conjugate prior for the binomial likelihood.

## Q96: What is scipy.stats.gamma used for?
**A:** gamma is the continuous gamma distribution, often used for waiting times and sums of exponential variables. Its shape parameter a and scale parameter control the distribution. It generalizes the exponential distribution when the shape is one.

## Q97: How do you compute relative entropy between two distributions?
**A:** Use scipy.stats.entropy with two probability arrays and base two to get the Kullback-Leibler divergence in bits. The divergence is non-negative and becomes zero when the distributions are identical. It is not symmetric, so the order of the arguments matters.

## Q98: What is scipy.stats.multivariate_normal used for?
**A:** multivariate_normal models a vector of jointly normal random variables with a mean vector and a covariance matrix. This is needed for portfolio modeling, Gaussian processes observations, and correlated features. Its methods accept arrays of points.

## Q99: How do you time-series test for randomness with scipy?
**A:** Use scipy.stats.lilliefors for normality on residuals, or the runs test via scipy.stats.runstest_1samp when available. For correlation in order, use scipy.stats.autocorrelation or lag correlation with numpy. Autocorrelation near zero supports randomness.

## Q100: What is a Q-Q plot and which scipy function creates it?
**A:** A Q-Q plot compares quantiles of the sample against quantiles of a reference distribution. scipy.stats.probplot creates the plot and also returns the fit parameters and a correlation coefficient. If the points lie close to a straight line, the distribution assumption is supported.
