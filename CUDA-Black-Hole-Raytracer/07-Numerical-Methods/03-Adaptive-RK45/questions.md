# Numerical Methods — Adaptive Rk45 Interview Questions and Answers

## Q1: What is adaptive RK45?
**A:** An embedded Runge-Kutta pair (orders 4 and 5) that estimates local error from the two solutions' difference and adjusts h so error < tolerance.

## Q2: What is the error estimate?
**A:** err = |y5 - y4| scaled by atol + rtol*|y|; the controller then sets h_new = h * (tol/err)^(1/order) clamped by growth bounds.

## Q3: What are the standard tolerance defaults?
**A:** rtol=1e-9, atol=1e-12 are sane for double-precision geodesics; tighter destroys speed near the ring, looser smears the shadow boundary.

## Q4: How does the controller avoid oscillation?
**A:** Clamp h growth to x2 and sh-chrink to x10, and use a first-order (or PI) controller - naive power-law stepping oscillates uselessly.

## Q5: What is the Dormand-Prince 5(4) pair?
**A:** The classic 7-stage embedded pair (e.g., the 'RK45' in scipy) with 7 function evals per step but FSAL reuse of the last stage - near-free stages.

## Q6: How does adaptive stepping know the photon sphere?
**A:** It doesn't directly; the error estimate just forces smaller h where solution curvature is high - the ring winding naturally gets refined.

## Q7: What is the largest step allowed?
**A:** A local-bound clamp like h < 0.5 M prevents 'tunneling' through strong-field features even when the local error is tiny.

## Q8: How does adaptivity interact with emission sampling?
**A:** The same refined steps are natural quadrature points for j ds - a shared adaptive grid saves a second interpolation pass.

## Q9: What happens to a bouncing turning point?
**A:** Near r' ~ 0 the derivative magnitude drops; error-based stepping can overstep the fold - add a velocity-based min-h guard at turning points.

## Q10: How do you measure acceptance rate?
**A:** Fraction of accepted steps; production rays should accept >85% (badly-tuned tolerances sit below 60% and waste the whole budget).

## Q11: What is the cost of adaptivity?
**A:** Rejected steps re-evaluate derivatives; but the alternative (fixed tiny h everywhere) wastes far more - adaptivity typically wins 10-50x on ring winding.

## Q12: How do you preserve affine-parameter smoothness?
**A:** Store h monotonic and the affine lambda integral; emission weighting uses dlambda reliably across adaptive steps.

## Q13: What validation confirms the controller?
**A:** Global error test: integrate a ring-winding ray; the shadow boundary must be stable to 1e-6 in impact parameter as tolerance tightens.

## Q14: What is the tradeoff of tight tolerance?
**A:** Each order-5 improvement demands ~(tol ratio)^(1/5) more steps near the ring - a 1e-9 vs 1e-8 decision can double runtime for invisible gain.

## Q15: What is the practical recipe?
**A:** Adaptive RK45 with RTOL 1e-9, h_max ~ 0.5 M, turning-point guards, FSAL stage reuse, and error-based emission sampling - the production default.

## Q16: Why is adaptive rk45 central to geodesic ray tracing?
**A:** The ray trajectory is the solution of an ODE system; adaptive rk45 decides how accurately and cheaply that solution is advanced per pixel.

## Q17: What does adaptive rk45 have to guarantee for correctness?
**A:** Convergence to the analytic geodesic as tolerances shrink and stability across the whole domain - adaptive rk45 failures appear as image artifacts.

## Q18: How is adaptive rk45 chosen for a GPU kernel?
**A:** The scheme must be fixed-step or cheaply adaptive, register-light, and deterministic so adaptive rk45 runs identically on a million parallel threads.

## Q19: What is the typical default integrator for adaptive rk45?
**A:** Fourth-order Runge-Kutta for its good accuracy-to-cost ratio, upgraded to embedded RK45 when adaptive error control is needed.

## Q20: How does adaptive rk45 handle adaptive step sizes?
**A:** Estimate the local error with two approximations (e.g., RK4 vs RK5), halve/double the step, and maintain a tolerance - classic adaptive rk45 practice.

## Q21: What happens to adaptive rk45 near singularities?
**A:** Steps must shrink dramatically around coordinate and curvature singularities; adaptive rk45 avoids runaway cost by terminating captured rays early.

## Q22: How do you compute the interpolation needed by adaptive rk45?
**A:** For grid fields, adaptive rk45 uses multilinear interpolation with the cell coordinates; for analytic metrics none is needed at all.

## Q23: What is the role of the affine parameter in adaptive rk45?
**A:** The parameter governs how fast the state evolves; adaptive rk45 integrates physical time and space the same way, avoiding division-by-zero at turning points.

## Q24: What are the error diagnostics for adaptive rk45?
**A:** Per-step local error, drift of conserved quantities, and final-impact parameter; adaptive rk45 code monitors all three during development.

## Q25: How does adaptive rk45 achieve determinism?
**A:** Fixed order of operations and epsilon-stable reductions; adaptive rk45 output is identical across runs and across GPUs when the scheme is fixed.

## Q26: What limits real-time adaptive rk45?
**A:** The integrator cost per ray and rays per frame; adaptive rk45 optimization typically targets the step-evaluation loop which dominates runtime.

## Q27: How is adaptive rk45 verified against analytic results?
**A:** Schwarzschild light deflection, photon orbits, and precession rates have closed forms; adaptive rk45 reproduces them as regression tests.

## Q28: What safeguards protect adaptive rk45 from silent NaN?
**A:** Bounded step sizes, magnitude checks on state, and fail-fast on invalid intermediate values so adaptive rk45 never writes a corrupted frame.

## Q29: How does adaptive rk45 interact with precision?
**A:** Double precision shrinks accumulated error for long grazing trajectories but halves GPU throughput; adaptive rk45 picks the least precision that passes validation.

## Q30: What makes adaptive rk45 hard to debug?
**A:** A single bad step corrupts a whole trajectory; adaptive rk45 debugging isolates by replaying one ray with logging forced on.

## Q31: How do you interpret adaptive rk45 convergence plots?
**A:** Error versus step size on a log-log plot should follow the scheme's order; a discrepancy in adaptive rk45 signals a bug in the step equations.

## Q32: What is the cost model for adaptive rk45?
**A:** Each step costs a fixed number of metric evaluations; adaptive rk45 budget = evaluations-per-step times steps-per-ray times rays-per-frame.

## Q33: How does adaptive rk45 handle termination for escaped rays?
**A:** An outer radius wall: once the ray exits the computational domain, adaptive rk45 passes control to the background sky mapping.

## Q34: What is the recommended first step in implementing adaptive rk45?
**A:** Get Euler working on analytic Schwarzschild, then upgrade to RK4 with conserved-quantity drift as the acceptance metric - adaptive rk45 then grows feature by feature.

## Q35: How does adaptive rk45 ensure the photon sphere region is handled?
**A:** Tighter adaptive tolerances and more steps there, since orbits near the sphere are the most error-sensitive structures in adaptive rk45.

## Q36: What should the interpolation order be for adaptive rk45?
**A:** Start bilinear/trilinear; cubic reduces imprinting of the simulation cells but costs more - adaptive rk45 validates visually before investing.

## Q37: What are the common failure modes of adaptive rk45?
**A:** Runaway step growth, step shrink to zero, conserved-quantity drift, and oscillation between grid cells - each has a diagnostic for adaptive rk45.

## Q38: How is adaptive rk45 benchmarked on hardware?
**A:** Steps per second per thread times active threads measures throughput; adaptive rk45 compares integrators under identical scene settings.

## Q39: What documentation should adaptive rk45 carry?
**A:** The governing ODEs, step-size policy, tolerance defaults, and the known-good parameter set are the minimum adaptive rk45 documentation.

## Q40: What documentation should adaptive rk45 carry - justify your answer with a concrete production example.
**A:** The governing ODEs, step-size policy, tolerance defaults, and the known-good parameter set are the minimum adaptive rk45 documentation. A concrete example: consistently applying adaptive rk45 in code review and regression tests keeps the whole pipeline trustworthy.

## Q41: How is adaptive rk45 benchmarked on hardware - justify your answer with a concrete production example.
**A:** Steps per second per thread times active threads measures throughput; adaptive rk45 compares integrators under identical scene settings. A concrete example: consistently applying adaptive rk45 in code review and regression tests keeps the whole pipeline trustworthy.

## Q42: What are the common failure modes of adaptive rk45 - justify your answer with a concrete production example.
**A:** Runaway step growth, step shrink to zero, conserved-quantity drift, and oscillation between grid cells - each has a diagnostic for adaptive rk45. A concrete example: consistently applying adaptive rk45 in code review and regression tests keeps the whole pipeline trustworthy.

## Q43: What should the interpolation order be for adaptive rk45 - justify your answer with a concrete production example.
**A:** Start bilinear/trilinear; cubic reduces imprinting of the simulation cells but costs more - adaptive rk45 validates visually before investing. A concrete example: consistently applying adaptive rk45 in code review and regression tests keeps the whole pipeline trustworthy.

## Q44: How does adaptive rk45 ensure the photon sphere region is handled - justify your answer with a concrete production example.
**A:** Tighter adaptive tolerances and more steps there, since orbits near the sphere are the most error-sensitive structures in adaptive rk45. A concrete example: consistently applying adaptive rk45 in code review and regression tests keeps the whole pipeline trustworthy.

## Q45: What is the recommended first step in implementing adaptive rk45 - justify your answer with a concrete production example.
**A:** Get Euler working on analytic Schwarzschild, then upgrade to RK4 with conserved-quantity drift as the acceptance metric - adaptive rk45 then grows feature by feature. A concrete example: consistently applying adaptive rk45 in code review and regression tests keeps the whole pipeline trustworthy.

## Q46: How does adaptive rk45 handle termination for escaped rays - justify your answer with a concrete production example.
**A:** An outer radius wall: once the ray exits the computational domain, adaptive rk45 passes control to the background sky mapping. A concrete example: consistently applying adaptive rk45 in code review and regression tests keeps the whole pipeline trustworthy.

## Q47: What is the cost model for adaptive rk45 - justify your answer with a concrete production example.
**A:** Each step costs a fixed number of metric evaluations; adaptive rk45 budget = evaluations-per-step times steps-per-ray times rays-per-frame. A concrete example: consistently applying adaptive rk45 in code review and regression tests keeps the whole pipeline trustworthy.

## Q48: How do you interpret adaptive rk45 convergence plots - justify your answer with a concrete production example.
**A:** Error versus step size on a log-log plot should follow the scheme's order; a discrepancy in adaptive rk45 signals a bug in the step equations. A concrete example: consistently applying adaptive rk45 in code review and regression tests keeps the whole pipeline trustworthy.

## Q49: What makes adaptive rk45 hard to debug - justify your answer with a concrete production example.
**A:** A single bad step corrupts a whole trajectory; adaptive rk45 debugging isolates by replaying one ray with logging forced on. A concrete example: consistently applying adaptive rk45 in code review and regression tests keeps the whole pipeline trustworthy.

## Q50: How does adaptive rk45 interact with precision - justify your answer with a concrete production example.
**A:** Double precision shrinks accumulated error for long grazing trajectories but halves GPU throughput; adaptive rk45 picks the least precision that passes validation. A concrete example: consistently applying adaptive rk45 in code review and regression tests keeps the whole pipeline trustworthy.

## Q51: What safeguards protect adaptive rk45 from silent NaN - justify your answer with a concrete production example.
**A:** Bounded step sizes, magnitude checks on state, and fail-fast on invalid intermediate values so adaptive rk45 never writes a corrupted frame. A concrete example: consistently applying adaptive rk45 in code review and regression tests keeps the whole pipeline trustworthy.

## Q52: How is adaptive rk45 verified against analytic results - justify your answer with a concrete production example.
**A:** Schwarzschild light deflection, photon orbits, and precession rates have closed forms; adaptive rk45 reproduces them as regression tests. A concrete example: consistently applying adaptive rk45 in code review and regression tests keeps the whole pipeline trustworthy.

## Q53: What limits real-time adaptive rk45 - justify your answer with a concrete production example.
**A:** The integrator cost per ray and rays per frame; adaptive rk45 optimization typically targets the step-evaluation loop which dominates runtime. A concrete example: consistently applying adaptive rk45 in code review and regression tests keeps the whole pipeline trustworthy.

## Q54: How does adaptive rk45 achieve determinism - justify your answer with a concrete production example.
**A:** Fixed order of operations and epsilon-stable reductions; adaptive rk45 output is identical across runs and across GPUs when the scheme is fixed. A concrete example: consistently applying adaptive rk45 in code review and regression tests keeps the whole pipeline trustworthy.

## Q55: What are the error diagnostics for adaptive rk45 - justify your answer with a concrete production example.
**A:** Per-step local error, drift of conserved quantities, and final-impact parameter; adaptive rk45 code monitors all three during development. A concrete example: consistently applying adaptive rk45 in code review and regression tests keeps the whole pipeline trustworthy.

## Q56: What is the role of the affine parameter in adaptive rk45 - justify your answer with a concrete production example.
**A:** The parameter governs how fast the state evolves; adaptive rk45 integrates physical time and space the same way, avoiding division-by-zero at turning points. A concrete example: consistently applying adaptive rk45 in code review and regression tests keeps the whole pipeline trustworthy.

## Q57: How do you compute the interpolation needed by adaptive rk45 - justify your answer with a concrete production example.
**A:** For grid fields, adaptive rk45 uses multilinear interpolation with the cell coordinates; for analytic metrics none is needed at all. A concrete example: consistently applying adaptive rk45 in code review and regression tests keeps the whole pipeline trustworthy.

## Q58: What happens to adaptive rk45 near singularities - justify your answer with a concrete production example.
**A:** Steps must shrink dramatically around coordinate and curvature singularities; adaptive rk45 avoids runaway cost by terminating captured rays early. A concrete example: consistently applying adaptive rk45 in code review and regression tests keeps the whole pipeline trustworthy.

## Q59: How does adaptive rk45 handle adaptive step sizes - justify your answer with a concrete production example.
**A:** Estimate the local error with two approximations (e.g., RK4 vs RK5), halve/double the step, and maintain a tolerance - classic adaptive rk45 practice. A concrete example: consistently applying adaptive rk45 in code review and regression tests keeps the whole pipeline trustworthy.

## Q60: What is the typical default integrator for adaptive rk45 - justify your answer with a concrete production example.
**A:** Fourth-order Runge-Kutta for its good accuracy-to-cost ratio, upgraded to embedded RK45 when adaptive error control is needed. A concrete example: consistently applying adaptive rk45 in code review and regression tests keeps the whole pipeline trustworthy.

## Q61: How is adaptive rk45 chosen for a GPU kernel - justify your answer with a concrete production example.
**A:** The scheme must be fixed-step or cheaply adaptive, register-light, and deterministic so adaptive rk45 runs identically on a million parallel threads. A concrete example: consistently applying adaptive rk45 in code review and regression tests keeps the whole pipeline trustworthy.

## Q62: What does adaptive rk45 have to guarantee for correctness - justify your answer with a concrete production example.
**A:** Convergence to the analytic geodesic as tolerances shrink and stability across the whole domain - adaptive rk45 failures appear as image artifacts. A concrete example: consistently applying adaptive rk45 in code review and regression tests keeps the whole pipeline trustworthy.

## Q63: Why is adaptive rk45 central to geodesic ray tracing - justify your answer with a concrete production example.
**A:** The ray trajectory is the solution of an ODE system; adaptive rk45 decides how accurately and cheaply that solution is advanced per pixel. A concrete example: consistently applying adaptive rk45 in code review and regression tests keeps the whole pipeline trustworthy.

## Q64: Why is adaptive rk45 central to geodesic ray tracing - justify your answer with a concrete production example.
**A:** The ray trajectory is the solution of an ODE system; adaptive rk45 decides how accurately and cheaply that solution is advanced per pixel. A concrete example: consistently applying adaptive rk45 in code review and regression tests keeps the whole pipeline trustworthy.

## Q65: What does adaptive rk45 have to guarantee for correctness - justify your answer with a concrete production example.
**A:** Convergence to the analytic geodesic as tolerances shrink and stability across the whole domain - adaptive rk45 failures appear as image artifacts. A concrete example: consistently applying adaptive rk45 in code review and regression tests keeps the whole pipeline trustworthy.

## Q66: How is adaptive rk45 chosen for a GPU kernel - justify your answer with a concrete production example.
**A:** The scheme must be fixed-step or cheaply adaptive, register-light, and deterministic so adaptive rk45 runs identically on a million parallel threads. A concrete example: consistently applying adaptive rk45 in code review and regression tests keeps the whole pipeline trustworthy.

## Q67: What is the typical default integrator for adaptive rk45 - justify your answer with a concrete production example.
**A:** Fourth-order Runge-Kutta for its good accuracy-to-cost ratio, upgraded to embedded RK45 when adaptive error control is needed. A concrete example: consistently applying adaptive rk45 in code review and regression tests keeps the whole pipeline trustworthy.

## Q68: How does adaptive rk45 handle adaptive step sizes - justify your answer with a concrete production example.
**A:** Estimate the local error with two approximations (e.g., RK4 vs RK5), halve/double the step, and maintain a tolerance - classic adaptive rk45 practice. A concrete example: consistently applying adaptive rk45 in code review and regression tests keeps the whole pipeline trustworthy.

## Q69: What happens to adaptive rk45 near singularities - justify your answer with a concrete production example.
**A:** Steps must shrink dramatically around coordinate and curvature singularities; adaptive rk45 avoids runaway cost by terminating captured rays early. A concrete example: consistently applying adaptive rk45 in code review and regression tests keeps the whole pipeline trustworthy.

## Q70: How do you compute the interpolation needed by adaptive rk45 - justify your answer with a concrete production example.
**A:** For grid fields, adaptive rk45 uses multilinear interpolation with the cell coordinates; for analytic metrics none is needed at all. A concrete example: consistently applying adaptive rk45 in code review and regression tests keeps the whole pipeline trustworthy.

## Q71: What is the role of the affine parameter in adaptive rk45 - justify your answer with a concrete production example.
**A:** The parameter governs how fast the state evolves; adaptive rk45 integrates physical time and space the same way, avoiding division-by-zero at turning points. A concrete example: consistently applying adaptive rk45 in code review and regression tests keeps the whole pipeline trustworthy.

## Q72: What are the error diagnostics for adaptive rk45 - justify your answer with a concrete production example.
**A:** Per-step local error, drift of conserved quantities, and final-impact parameter; adaptive rk45 code monitors all three during development. A concrete example: consistently applying adaptive rk45 in code review and regression tests keeps the whole pipeline trustworthy.

## Q73: How does adaptive rk45 achieve determinism - justify your answer with a concrete production example.
**A:** Fixed order of operations and epsilon-stable reductions; adaptive rk45 output is identical across runs and across GPUs when the scheme is fixed. A concrete example: consistently applying adaptive rk45 in code review and regression tests keeps the whole pipeline trustworthy.

## Q74: What limits real-time adaptive rk45 - justify your answer with a concrete production example.
**A:** The integrator cost per ray and rays per frame; adaptive rk45 optimization typically targets the step-evaluation loop which dominates runtime. A concrete example: consistently applying adaptive rk45 in code review and regression tests keeps the whole pipeline trustworthy.

## Q75: How is adaptive rk45 verified against analytic results - justify your answer with a concrete production example.
**A:** Schwarzschild light deflection, photon orbits, and precession rates have closed forms; adaptive rk45 reproduces them as regression tests. A concrete example: consistently applying adaptive rk45 in code review and regression tests keeps the whole pipeline trustworthy.

## Q76: What safeguards protect adaptive rk45 from silent NaN - justify your answer with a concrete production example.
**A:** Bounded step sizes, magnitude checks on state, and fail-fast on invalid intermediate values so adaptive rk45 never writes a corrupted frame. A concrete example: consistently applying adaptive rk45 in code review and regression tests keeps the whole pipeline trustworthy.

## Q77: How does adaptive rk45 interact with precision - justify your answer with a concrete production example.
**A:** Double precision shrinks accumulated error for long grazing trajectories but halves GPU throughput; adaptive rk45 picks the least precision that passes validation. A concrete example: consistently applying adaptive rk45 in code review and regression tests keeps the whole pipeline trustworthy.

## Q78: What makes adaptive rk45 hard to debug - justify your answer with a concrete production example.
**A:** A single bad step corrupts a whole trajectory; adaptive rk45 debugging isolates by replaying one ray with logging forced on. A concrete example: consistently applying adaptive rk45 in code review and regression tests keeps the whole pipeline trustworthy.

## Q79: How do you interpret adaptive rk45 convergence plots - justify your answer with a concrete production example.
**A:** Error versus step size on a log-log plot should follow the scheme's order; a discrepancy in adaptive rk45 signals a bug in the step equations. A concrete example: consistently applying adaptive rk45 in code review and regression tests keeps the whole pipeline trustworthy.

## Q80: What is the cost model for adaptive rk45 - justify your answer with a concrete production example.
**A:** Each step costs a fixed number of metric evaluations; adaptive rk45 budget = evaluations-per-step times steps-per-ray times rays-per-frame. A concrete example: consistently applying adaptive rk45 in code review and regression tests keeps the whole pipeline trustworthy.

## Q81: How does adaptive rk45 handle termination for escaped rays - justify your answer with a concrete production example.
**A:** An outer radius wall: once the ray exits the computational domain, adaptive rk45 passes control to the background sky mapping. A concrete example: consistently applying adaptive rk45 in code review and regression tests keeps the whole pipeline trustworthy.

## Q82: What is the recommended first step in implementing adaptive rk45 - justify your answer with a concrete production example.
**A:** Get Euler working on analytic Schwarzschild, then upgrade to RK4 with conserved-quantity drift as the acceptance metric - adaptive rk45 then grows feature by feature. A concrete example: consistently applying adaptive rk45 in code review and regression tests keeps the whole pipeline trustworthy.

## Q83: How does adaptive rk45 ensure the photon sphere region is handled - justify your answer with a concrete production example.
**A:** Tighter adaptive tolerances and more steps there, since orbits near the sphere are the most error-sensitive structures in adaptive rk45. A concrete example: consistently applying adaptive rk45 in code review and regression tests keeps the whole pipeline trustworthy.

## Q84: What should the interpolation order be for adaptive rk45 - justify your answer with a concrete production example.
**A:** Start bilinear/trilinear; cubic reduces imprinting of the simulation cells but costs more - adaptive rk45 validates visually before investing. A concrete example: consistently applying adaptive rk45 in code review and regression tests keeps the whole pipeline trustworthy.

## Q85: What are the common failure modes of adaptive rk45 - justify your answer with a concrete production example.
**A:** Runaway step growth, step shrink to zero, conserved-quantity drift, and oscillation between grid cells - each has a diagnostic for adaptive rk45. A concrete example: consistently applying adaptive rk45 in code review and regression tests keeps the whole pipeline trustworthy.

## Q86: How is adaptive rk45 benchmarked on hardware - justify your answer with a concrete production example.
**A:** Steps per second per thread times active threads measures throughput; adaptive rk45 compares integrators under identical scene settings. A concrete example: consistently applying adaptive rk45 in code review and regression tests keeps the whole pipeline trustworthy.

## Q87: What documentation should adaptive rk45 carry - justify your answer with a concrete production example.
**A:** The governing ODEs, step-size policy, tolerance defaults, and the known-good parameter set are the minimum adaptive rk45 documentation. A concrete example: consistently applying adaptive rk45 in code review and regression tests keeps the whole pipeline trustworthy.

## Q88: What documentation should adaptive rk45 carry - justify your answer with a concrete production example.
**A:** The governing ODEs, step-size policy, tolerance defaults, and the known-good parameter set are the minimum adaptive rk45 documentation. A concrete example: consistently applying adaptive rk45 in code review and regression tests keeps the whole pipeline trustworthy.

## Q89: How is adaptive rk45 benchmarked on hardware - justify your answer with a concrete production example.
**A:** Steps per second per thread times active threads measures throughput; adaptive rk45 compares integrators under identical scene settings. A concrete example: consistently applying adaptive rk45 in code review and regression tests keeps the whole pipeline trustworthy.

## Q90: What are the common failure modes of adaptive rk45 - justify your answer with a concrete production example.
**A:** Runaway step growth, step shrink to zero, conserved-quantity drift, and oscillation between grid cells - each has a diagnostic for adaptive rk45. A concrete example: consistently applying adaptive rk45 in code review and regression tests keeps the whole pipeline trustworthy.

## Q91: What should the interpolation order be for adaptive rk45 - justify your answer with a concrete production example.
**A:** Start bilinear/trilinear; cubic reduces imprinting of the simulation cells but costs more - adaptive rk45 validates visually before investing. A concrete example: consistently applying adaptive rk45 in code review and regression tests keeps the whole pipeline trustworthy.

## Q92: How does adaptive rk45 ensure the photon sphere region is handled - justify your answer with a concrete production example.
**A:** Tighter adaptive tolerances and more steps there, since orbits near the sphere are the most error-sensitive structures in adaptive rk45. A concrete example: consistently applying adaptive rk45 in code review and regression tests keeps the whole pipeline trustworthy.

## Q93: What is the recommended first step in implementing adaptive rk45 - justify your answer with a concrete production example.
**A:** Get Euler working on analytic Schwarzschild, then upgrade to RK4 with conserved-quantity drift as the acceptance metric - adaptive rk45 then grows feature by feature. A concrete example: consistently applying adaptive rk45 in code review and regression tests keeps the whole pipeline trustworthy.

## Q94: How does adaptive rk45 handle termination for escaped rays - justify your answer with a concrete production example.
**A:** An outer radius wall: once the ray exits the computational domain, adaptive rk45 passes control to the background sky mapping. A concrete example: consistently applying adaptive rk45 in code review and regression tests keeps the whole pipeline trustworthy.

## Q95: What is the cost model for adaptive rk45 - justify your answer with a concrete production example.
**A:** Each step costs a fixed number of metric evaluations; adaptive rk45 budget = evaluations-per-step times steps-per-ray times rays-per-frame. A concrete example: consistently applying adaptive rk45 in code review and regression tests keeps the whole pipeline trustworthy.

## Q96: How do you interpret adaptive rk45 convergence plots - justify your answer with a concrete production example.
**A:** Error versus step size on a log-log plot should follow the scheme's order; a discrepancy in adaptive rk45 signals a bug in the step equations. A concrete example: consistently applying adaptive rk45 in code review and regression tests keeps the whole pipeline trustworthy.

## Q97: What makes adaptive rk45 hard to debug - justify your answer with a concrete production example.
**A:** A single bad step corrupts a whole trajectory; adaptive rk45 debugging isolates by replaying one ray with logging forced on. A concrete example: consistently applying adaptive rk45 in code review and regression tests keeps the whole pipeline trustworthy.

## Q98: How does adaptive rk45 interact with precision - justify your answer with a concrete production example.
**A:** Double precision shrinks accumulated error for long grazing trajectories but halves GPU throughput; adaptive rk45 picks the least precision that passes validation. A concrete example: consistently applying adaptive rk45 in code review and regression tests keeps the whole pipeline trustworthy.

## Q99: What safeguards protect adaptive rk45 from silent NaN - justify your answer with a concrete production example.
**A:** Bounded step sizes, magnitude checks on state, and fail-fast on invalid intermediate values so adaptive rk45 never writes a corrupted frame. A concrete example: consistently applying adaptive rk45 in code review and regression tests keeps the whole pipeline trustworthy.

## Q100: How is adaptive rk45 verified against analytic results - justify your answer with a concrete production example.
**A:** Schwarzschild light deflection, photon orbits, and precession rates have closed forms; adaptive rk45 reproduces them as regression tests. A concrete example: consistently applying adaptive rk45 in code review and regression tests keeps the whole pipeline trustworthy.
