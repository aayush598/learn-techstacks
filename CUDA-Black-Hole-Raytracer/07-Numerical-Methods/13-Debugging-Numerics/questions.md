# Numerical Methods — Debugging Numerics Interview Questions and Answers

## Q1: What is the first debugging move for a geodesic integrator?
**A:** Reduce to M=0 (Minkowski): every geodesic must be a straight line - any bending here is a bug in the metric/initialization, not physics.

## Q2: What is the second test?
**A:** Static symmetric cases: a ray straight in/out of Schwarzschild, and the circular null orbit at r=3M - closed-form anchors for the metric+integration.

## Q3: How do you use conserved quantities to debug?
**A:** Plot E, L, Q (or H) along the ray; a sudden drift localizes the bad step (wrong Delta, wrong momentum update, chart switch glitch).

## Q4: What is the lopsided H test?
**A:** Always print H=p^2 at key points; monotonic/step-correlated H growth indicates either step-size or algebra drift - bisect step boundaries to find the offender.

## Q5: How do you isolate a bad field (emissivity) vs bad geodesic?
**A:** Render with emissivity=constant in a known region: if the image mismatches the analytic geometry, the geodesic geometry is at fault; else the field sampling.

## Q6: How do you inspect a specific pixel?
**A:** Save one ray's full (lambda, r, theta, p_r...) log to a CSV; compare turning points against the effective-potential analytic roots - pinpoint the discrepancy.

## Q7: What are unit tests worth in this domain?
**A:** Metric round-trips (BL<->KS), geodesic deflection, shadow boundary, Doppler factor, sampler reproduction - each is a tiny, order-independent regression test.

## Q8: What is the least-floating-point hint?
**A:** Recompile with -ffp-contract=off and the same FPU; if frames change, your algebra depends on fused-multiply-add order - standardize it.

## Q9: How do you spot grid/sampler bugs?
**A:** Render a field grayscale (e.g., just rho interpolated): sharp grid-cornered edges reveal axis mapping/octree errors mis-indexed by one cell.

## Q10: What is the golden 'M=1, a=0' baseline?
**A:** Schwarzschild must produce a perfectly circular shadow at 3 sqrt(3) M and ring at the photon-sphere bands - deviation = geometry bug.

## Q11: How do you debug the horizon crossing?
**A:** Log r - r+ per step near capture; a jagged sign pattern near the boundary means the bracket detection needs tuning, not the physics.

## Q12: What is the divergence-stuck pattern?
**A:** A ray whose step count hits BUDGET while oscillating in place near a turning point: add the min-step floor or localized error-clamp the controller.

## Q13: How do you compare against a reference CPU raytracer?
**A:** Integrate the identical ray in double precision with a high-tolerance CPU RK45; the GPU kernel must match within its documented tolerance - the parity test.

## Q14: What is the signature of a chart-mapping bug?
**A:** Smooth image everywhere except a hard azimuthal seam at phi = +- pi - the classic sign flip in the phi coordinate wrap.

## Q15: What is the summary?
**A:** Debugging numerically means: analytic anchors first, conserved-residual localization, per-pixel logs, unit regressions, and a fixed FP contract - systematic and fast.

## Q16: Why is debugging numerics central to geodesic ray tracing?
**A:** The ray trajectory is the solution of an ODE system; debugging numerics decides how accurately and cheaply that solution is advanced per pixel.

## Q17: What does debugging numerics have to guarantee for correctness?
**A:** Convergence to the analytic geodesic as tolerances shrink and stability across the whole domain - debugging numerics failures appear as image artifacts.

## Q18: How is debugging numerics chosen for a GPU kernel?
**A:** The scheme must be fixed-step or cheaply adaptive, register-light, and deterministic so debugging numerics runs identically on a million parallel threads.

## Q19: What is the typical default integrator for debugging numerics?
**A:** Fourth-order Runge-Kutta for its good accuracy-to-cost ratio, upgraded to embedded RK45 when adaptive error control is needed.

## Q20: How does debugging numerics handle adaptive step sizes?
**A:** Estimate the local error with two approximations (e.g., RK4 vs RK5), halve/double the step, and maintain a tolerance - classic debugging numerics practice.

## Q21: What happens to debugging numerics near singularities?
**A:** Steps must shrink dramatically around coordinate and curvature singularities; debugging numerics avoids runaway cost by terminating captured rays early.

## Q22: How do you compute the interpolation needed by debugging numerics?
**A:** For grid fields, debugging numerics uses multilinear interpolation with the cell coordinates; for analytic metrics none is needed at all.

## Q23: What is the role of the affine parameter in debugging numerics?
**A:** The parameter governs how fast the state evolves; debugging numerics integrates physical time and space the same way, avoiding division-by-zero at turning points.

## Q24: What are the error diagnostics for debugging numerics?
**A:** Per-step local error, drift of conserved quantities, and final-impact parameter; debugging numerics code monitors all three during development.

## Q25: How does debugging numerics achieve determinism?
**A:** Fixed order of operations and epsilon-stable reductions; debugging numerics output is identical across runs and across GPUs when the scheme is fixed.

## Q26: What limits real-time debugging numerics?
**A:** The integrator cost per ray and rays per frame; debugging numerics optimization typically targets the step-evaluation loop which dominates runtime.

## Q27: How is debugging numerics verified against analytic results?
**A:** Schwarzschild light deflection, photon orbits, and precession rates have closed forms; debugging numerics reproduces them as regression tests.

## Q28: What safeguards protect debugging numerics from silent NaN?
**A:** Bounded step sizes, magnitude checks on state, and fail-fast on invalid intermediate values so debugging numerics never writes a corrupted frame.

## Q29: How does debugging numerics interact with precision?
**A:** Double precision shrinks accumulated error for long grazing trajectories but halves GPU throughput; debugging numerics picks the least precision that passes validation.

## Q30: What makes debugging numerics hard to debug?
**A:** A single bad step corrupts a whole trajectory; debugging numerics debugging isolates by replaying one ray with logging forced on.

## Q31: How do you interpret debugging numerics convergence plots?
**A:** Error versus step size on a log-log plot should follow the scheme's order; a discrepancy in debugging numerics signals a bug in the step equations.

## Q32: What is the cost model for debugging numerics?
**A:** Each step costs a fixed number of metric evaluations; debugging numerics budget = evaluations-per-step times steps-per-ray times rays-per-frame.

## Q33: How does debugging numerics handle termination for escaped rays?
**A:** An outer radius wall: once the ray exits the computational domain, debugging numerics passes control to the background sky mapping.

## Q34: What is the recommended first step in implementing debugging numerics?
**A:** Get Euler working on analytic Schwarzschild, then upgrade to RK4 with conserved-quantity drift as the acceptance metric - debugging numerics then grows feature by feature.

## Q35: How does debugging numerics ensure the photon sphere region is handled?
**A:** Tighter adaptive tolerances and more steps there, since orbits near the sphere are the most error-sensitive structures in debugging numerics.

## Q36: What should the interpolation order be for debugging numerics?
**A:** Start bilinear/trilinear; cubic reduces imprinting of the simulation cells but costs more - debugging numerics validates visually before investing.

## Q37: What are the common failure modes of debugging numerics?
**A:** Runaway step growth, step shrink to zero, conserved-quantity drift, and oscillation between grid cells - each has a diagnostic for debugging numerics.

## Q38: How is debugging numerics benchmarked on hardware?
**A:** Steps per second per thread times active threads measures throughput; debugging numerics compares integrators under identical scene settings.

## Q39: What documentation should debugging numerics carry?
**A:** The governing ODEs, step-size policy, tolerance defaults, and the known-good parameter set are the minimum debugging numerics documentation.

## Q40: What documentation should debugging numerics carry - justify your answer with a concrete production example.
**A:** The governing ODEs, step-size policy, tolerance defaults, and the known-good parameter set are the minimum debugging numerics documentation. A concrete example: consistently applying debugging numerics in code review and regression tests keeps the whole pipeline trustworthy.

## Q41: How is debugging numerics benchmarked on hardware - justify your answer with a concrete production example.
**A:** Steps per second per thread times active threads measures throughput; debugging numerics compares integrators under identical scene settings. A concrete example: consistently applying debugging numerics in code review and regression tests keeps the whole pipeline trustworthy.

## Q42: What are the common failure modes of debugging numerics - justify your answer with a concrete production example.
**A:** Runaway step growth, step shrink to zero, conserved-quantity drift, and oscillation between grid cells - each has a diagnostic for debugging numerics. A concrete example: consistently applying debugging numerics in code review and regression tests keeps the whole pipeline trustworthy.

## Q43: What should the interpolation order be for debugging numerics - justify your answer with a concrete production example.
**A:** Start bilinear/trilinear; cubic reduces imprinting of the simulation cells but costs more - debugging numerics validates visually before investing. A concrete example: consistently applying debugging numerics in code review and regression tests keeps the whole pipeline trustworthy.

## Q44: How does debugging numerics ensure the photon sphere region is handled - justify your answer with a concrete production example.
**A:** Tighter adaptive tolerances and more steps there, since orbits near the sphere are the most error-sensitive structures in debugging numerics. A concrete example: consistently applying debugging numerics in code review and regression tests keeps the whole pipeline trustworthy.

## Q45: What is the recommended first step in implementing debugging numerics - justify your answer with a concrete production example.
**A:** Get Euler working on analytic Schwarzschild, then upgrade to RK4 with conserved-quantity drift as the acceptance metric - debugging numerics then grows feature by feature. A concrete example: consistently applying debugging numerics in code review and regression tests keeps the whole pipeline trustworthy.

## Q46: How does debugging numerics handle termination for escaped rays - justify your answer with a concrete production example.
**A:** An outer radius wall: once the ray exits the computational domain, debugging numerics passes control to the background sky mapping. A concrete example: consistently applying debugging numerics in code review and regression tests keeps the whole pipeline trustworthy.

## Q47: What is the cost model for debugging numerics - justify your answer with a concrete production example.
**A:** Each step costs a fixed number of metric evaluations; debugging numerics budget = evaluations-per-step times steps-per-ray times rays-per-frame. A concrete example: consistently applying debugging numerics in code review and regression tests keeps the whole pipeline trustworthy.

## Q48: How do you interpret debugging numerics convergence plots - justify your answer with a concrete production example.
**A:** Error versus step size on a log-log plot should follow the scheme's order; a discrepancy in debugging numerics signals a bug in the step equations. A concrete example: consistently applying debugging numerics in code review and regression tests keeps the whole pipeline trustworthy.

## Q49: What makes debugging numerics hard to debug - justify your answer with a concrete production example.
**A:** A single bad step corrupts a whole trajectory; debugging numerics debugging isolates by replaying one ray with logging forced on. A concrete example: consistently applying debugging numerics in code review and regression tests keeps the whole pipeline trustworthy.

## Q50: How does debugging numerics interact with precision - justify your answer with a concrete production example.
**A:** Double precision shrinks accumulated error for long grazing trajectories but halves GPU throughput; debugging numerics picks the least precision that passes validation. A concrete example: consistently applying debugging numerics in code review and regression tests keeps the whole pipeline trustworthy.

## Q51: What safeguards protect debugging numerics from silent NaN - justify your answer with a concrete production example.
**A:** Bounded step sizes, magnitude checks on state, and fail-fast on invalid intermediate values so debugging numerics never writes a corrupted frame. A concrete example: consistently applying debugging numerics in code review and regression tests keeps the whole pipeline trustworthy.

## Q52: How is debugging numerics verified against analytic results - justify your answer with a concrete production example.
**A:** Schwarzschild light deflection, photon orbits, and precession rates have closed forms; debugging numerics reproduces them as regression tests. A concrete example: consistently applying debugging numerics in code review and regression tests keeps the whole pipeline trustworthy.

## Q53: What limits real-time debugging numerics - justify your answer with a concrete production example.
**A:** The integrator cost per ray and rays per frame; debugging numerics optimization typically targets the step-evaluation loop which dominates runtime. A concrete example: consistently applying debugging numerics in code review and regression tests keeps the whole pipeline trustworthy.

## Q54: How does debugging numerics achieve determinism - justify your answer with a concrete production example.
**A:** Fixed order of operations and epsilon-stable reductions; debugging numerics output is identical across runs and across GPUs when the scheme is fixed. A concrete example: consistently applying debugging numerics in code review and regression tests keeps the whole pipeline trustworthy.

## Q55: What are the error diagnostics for debugging numerics - justify your answer with a concrete production example.
**A:** Per-step local error, drift of conserved quantities, and final-impact parameter; debugging numerics code monitors all three during development. A concrete example: consistently applying debugging numerics in code review and regression tests keeps the whole pipeline trustworthy.

## Q56: What is the role of the affine parameter in debugging numerics - justify your answer with a concrete production example.
**A:** The parameter governs how fast the state evolves; debugging numerics integrates physical time and space the same way, avoiding division-by-zero at turning points. A concrete example: consistently applying debugging numerics in code review and regression tests keeps the whole pipeline trustworthy.

## Q57: How do you compute the interpolation needed by debugging numerics - justify your answer with a concrete production example.
**A:** For grid fields, debugging numerics uses multilinear interpolation with the cell coordinates; for analytic metrics none is needed at all. A concrete example: consistently applying debugging numerics in code review and regression tests keeps the whole pipeline trustworthy.

## Q58: What happens to debugging numerics near singularities - justify your answer with a concrete production example.
**A:** Steps must shrink dramatically around coordinate and curvature singularities; debugging numerics avoids runaway cost by terminating captured rays early. A concrete example: consistently applying debugging numerics in code review and regression tests keeps the whole pipeline trustworthy.

## Q59: How does debugging numerics handle adaptive step sizes - justify your answer with a concrete production example.
**A:** Estimate the local error with two approximations (e.g., RK4 vs RK5), halve/double the step, and maintain a tolerance - classic debugging numerics practice. A concrete example: consistently applying debugging numerics in code review and regression tests keeps the whole pipeline trustworthy.

## Q60: What is the typical default integrator for debugging numerics - justify your answer with a concrete production example.
**A:** Fourth-order Runge-Kutta for its good accuracy-to-cost ratio, upgraded to embedded RK45 when adaptive error control is needed. A concrete example: consistently applying debugging numerics in code review and regression tests keeps the whole pipeline trustworthy.

## Q61: How is debugging numerics chosen for a GPU kernel - justify your answer with a concrete production example.
**A:** The scheme must be fixed-step or cheaply adaptive, register-light, and deterministic so debugging numerics runs identically on a million parallel threads. A concrete example: consistently applying debugging numerics in code review and regression tests keeps the whole pipeline trustworthy.

## Q62: What does debugging numerics have to guarantee for correctness - justify your answer with a concrete production example.
**A:** Convergence to the analytic geodesic as tolerances shrink and stability across the whole domain - debugging numerics failures appear as image artifacts. A concrete example: consistently applying debugging numerics in code review and regression tests keeps the whole pipeline trustworthy.

## Q63: Why is debugging numerics central to geodesic ray tracing - justify your answer with a concrete production example.
**A:** The ray trajectory is the solution of an ODE system; debugging numerics decides how accurately and cheaply that solution is advanced per pixel. A concrete example: consistently applying debugging numerics in code review and regression tests keeps the whole pipeline trustworthy.

## Q64: Why is debugging numerics central to geodesic ray tracing - justify your answer with a concrete production example.
**A:** The ray trajectory is the solution of an ODE system; debugging numerics decides how accurately and cheaply that solution is advanced per pixel. A concrete example: consistently applying debugging numerics in code review and regression tests keeps the whole pipeline trustworthy.

## Q65: What does debugging numerics have to guarantee for correctness - justify your answer with a concrete production example.
**A:** Convergence to the analytic geodesic as tolerances shrink and stability across the whole domain - debugging numerics failures appear as image artifacts. A concrete example: consistently applying debugging numerics in code review and regression tests keeps the whole pipeline trustworthy.

## Q66: How is debugging numerics chosen for a GPU kernel - justify your answer with a concrete production example.
**A:** The scheme must be fixed-step or cheaply adaptive, register-light, and deterministic so debugging numerics runs identically on a million parallel threads. A concrete example: consistently applying debugging numerics in code review and regression tests keeps the whole pipeline trustworthy.

## Q67: What is the typical default integrator for debugging numerics - justify your answer with a concrete production example.
**A:** Fourth-order Runge-Kutta for its good accuracy-to-cost ratio, upgraded to embedded RK45 when adaptive error control is needed. A concrete example: consistently applying debugging numerics in code review and regression tests keeps the whole pipeline trustworthy.

## Q68: How does debugging numerics handle adaptive step sizes - justify your answer with a concrete production example.
**A:** Estimate the local error with two approximations (e.g., RK4 vs RK5), halve/double the step, and maintain a tolerance - classic debugging numerics practice. A concrete example: consistently applying debugging numerics in code review and regression tests keeps the whole pipeline trustworthy.

## Q69: What happens to debugging numerics near singularities - justify your answer with a concrete production example.
**A:** Steps must shrink dramatically around coordinate and curvature singularities; debugging numerics avoids runaway cost by terminating captured rays early. A concrete example: consistently applying debugging numerics in code review and regression tests keeps the whole pipeline trustworthy.

## Q70: How do you compute the interpolation needed by debugging numerics - justify your answer with a concrete production example.
**A:** For grid fields, debugging numerics uses multilinear interpolation with the cell coordinates; for analytic metrics none is needed at all. A concrete example: consistently applying debugging numerics in code review and regression tests keeps the whole pipeline trustworthy.

## Q71: What is the role of the affine parameter in debugging numerics - justify your answer with a concrete production example.
**A:** The parameter governs how fast the state evolves; debugging numerics integrates physical time and space the same way, avoiding division-by-zero at turning points. A concrete example: consistently applying debugging numerics in code review and regression tests keeps the whole pipeline trustworthy.

## Q72: What are the error diagnostics for debugging numerics - justify your answer with a concrete production example.
**A:** Per-step local error, drift of conserved quantities, and final-impact parameter; debugging numerics code monitors all three during development. A concrete example: consistently applying debugging numerics in code review and regression tests keeps the whole pipeline trustworthy.

## Q73: How does debugging numerics achieve determinism - justify your answer with a concrete production example.
**A:** Fixed order of operations and epsilon-stable reductions; debugging numerics output is identical across runs and across GPUs when the scheme is fixed. A concrete example: consistently applying debugging numerics in code review and regression tests keeps the whole pipeline trustworthy.

## Q74: What limits real-time debugging numerics - justify your answer with a concrete production example.
**A:** The integrator cost per ray and rays per frame; debugging numerics optimization typically targets the step-evaluation loop which dominates runtime. A concrete example: consistently applying debugging numerics in code review and regression tests keeps the whole pipeline trustworthy.

## Q75: How is debugging numerics verified against analytic results - justify your answer with a concrete production example.
**A:** Schwarzschild light deflection, photon orbits, and precession rates have closed forms; debugging numerics reproduces them as regression tests. A concrete example: consistently applying debugging numerics in code review and regression tests keeps the whole pipeline trustworthy.

## Q76: What safeguards protect debugging numerics from silent NaN - justify your answer with a concrete production example.
**A:** Bounded step sizes, magnitude checks on state, and fail-fast on invalid intermediate values so debugging numerics never writes a corrupted frame. A concrete example: consistently applying debugging numerics in code review and regression tests keeps the whole pipeline trustworthy.

## Q77: How does debugging numerics interact with precision - justify your answer with a concrete production example.
**A:** Double precision shrinks accumulated error for long grazing trajectories but halves GPU throughput; debugging numerics picks the least precision that passes validation. A concrete example: consistently applying debugging numerics in code review and regression tests keeps the whole pipeline trustworthy.

## Q78: What makes debugging numerics hard to debug - justify your answer with a concrete production example.
**A:** A single bad step corrupts a whole trajectory; debugging numerics debugging isolates by replaying one ray with logging forced on. A concrete example: consistently applying debugging numerics in code review and regression tests keeps the whole pipeline trustworthy.

## Q79: How do you interpret debugging numerics convergence plots - justify your answer with a concrete production example.
**A:** Error versus step size on a log-log plot should follow the scheme's order; a discrepancy in debugging numerics signals a bug in the step equations. A concrete example: consistently applying debugging numerics in code review and regression tests keeps the whole pipeline trustworthy.

## Q80: What is the cost model for debugging numerics - justify your answer with a concrete production example.
**A:** Each step costs a fixed number of metric evaluations; debugging numerics budget = evaluations-per-step times steps-per-ray times rays-per-frame. A concrete example: consistently applying debugging numerics in code review and regression tests keeps the whole pipeline trustworthy.

## Q81: How does debugging numerics handle termination for escaped rays - justify your answer with a concrete production example.
**A:** An outer radius wall: once the ray exits the computational domain, debugging numerics passes control to the background sky mapping. A concrete example: consistently applying debugging numerics in code review and regression tests keeps the whole pipeline trustworthy.

## Q82: What is the recommended first step in implementing debugging numerics - justify your answer with a concrete production example.
**A:** Get Euler working on analytic Schwarzschild, then upgrade to RK4 with conserved-quantity drift as the acceptance metric - debugging numerics then grows feature by feature. A concrete example: consistently applying debugging numerics in code review and regression tests keeps the whole pipeline trustworthy.

## Q83: How does debugging numerics ensure the photon sphere region is handled - justify your answer with a concrete production example.
**A:** Tighter adaptive tolerances and more steps there, since orbits near the sphere are the most error-sensitive structures in debugging numerics. A concrete example: consistently applying debugging numerics in code review and regression tests keeps the whole pipeline trustworthy.

## Q84: What should the interpolation order be for debugging numerics - justify your answer with a concrete production example.
**A:** Start bilinear/trilinear; cubic reduces imprinting of the simulation cells but costs more - debugging numerics validates visually before investing. A concrete example: consistently applying debugging numerics in code review and regression tests keeps the whole pipeline trustworthy.

## Q85: What are the common failure modes of debugging numerics - justify your answer with a concrete production example.
**A:** Runaway step growth, step shrink to zero, conserved-quantity drift, and oscillation between grid cells - each has a diagnostic for debugging numerics. A concrete example: consistently applying debugging numerics in code review and regression tests keeps the whole pipeline trustworthy.

## Q86: How is debugging numerics benchmarked on hardware - justify your answer with a concrete production example.
**A:** Steps per second per thread times active threads measures throughput; debugging numerics compares integrators under identical scene settings. A concrete example: consistently applying debugging numerics in code review and regression tests keeps the whole pipeline trustworthy.

## Q87: What documentation should debugging numerics carry - justify your answer with a concrete production example.
**A:** The governing ODEs, step-size policy, tolerance defaults, and the known-good parameter set are the minimum debugging numerics documentation. A concrete example: consistently applying debugging numerics in code review and regression tests keeps the whole pipeline trustworthy.

## Q88: What documentation should debugging numerics carry - justify your answer with a concrete production example.
**A:** The governing ODEs, step-size policy, tolerance defaults, and the known-good parameter set are the minimum debugging numerics documentation. A concrete example: consistently applying debugging numerics in code review and regression tests keeps the whole pipeline trustworthy.

## Q89: How is debugging numerics benchmarked on hardware - justify your answer with a concrete production example.
**A:** Steps per second per thread times active threads measures throughput; debugging numerics compares integrators under identical scene settings. A concrete example: consistently applying debugging numerics in code review and regression tests keeps the whole pipeline trustworthy.

## Q90: What are the common failure modes of debugging numerics - justify your answer with a concrete production example.
**A:** Runaway step growth, step shrink to zero, conserved-quantity drift, and oscillation between grid cells - each has a diagnostic for debugging numerics. A concrete example: consistently applying debugging numerics in code review and regression tests keeps the whole pipeline trustworthy.

## Q91: What should the interpolation order be for debugging numerics - justify your answer with a concrete production example.
**A:** Start bilinear/trilinear; cubic reduces imprinting of the simulation cells but costs more - debugging numerics validates visually before investing. A concrete example: consistently applying debugging numerics in code review and regression tests keeps the whole pipeline trustworthy.

## Q92: How does debugging numerics ensure the photon sphere region is handled - justify your answer with a concrete production example.
**A:** Tighter adaptive tolerances and more steps there, since orbits near the sphere are the most error-sensitive structures in debugging numerics. A concrete example: consistently applying debugging numerics in code review and regression tests keeps the whole pipeline trustworthy.

## Q93: What is the recommended first step in implementing debugging numerics - justify your answer with a concrete production example.
**A:** Get Euler working on analytic Schwarzschild, then upgrade to RK4 with conserved-quantity drift as the acceptance metric - debugging numerics then grows feature by feature. A concrete example: consistently applying debugging numerics in code review and regression tests keeps the whole pipeline trustworthy.

## Q94: How does debugging numerics handle termination for escaped rays - justify your answer with a concrete production example.
**A:** An outer radius wall: once the ray exits the computational domain, debugging numerics passes control to the background sky mapping. A concrete example: consistently applying debugging numerics in code review and regression tests keeps the whole pipeline trustworthy.

## Q95: What is the cost model for debugging numerics - justify your answer with a concrete production example.
**A:** Each step costs a fixed number of metric evaluations; debugging numerics budget = evaluations-per-step times steps-per-ray times rays-per-frame. A concrete example: consistently applying debugging numerics in code review and regression tests keeps the whole pipeline trustworthy.

## Q96: How do you interpret debugging numerics convergence plots - justify your answer with a concrete production example.
**A:** Error versus step size on a log-log plot should follow the scheme's order; a discrepancy in debugging numerics signals a bug in the step equations. A concrete example: consistently applying debugging numerics in code review and regression tests keeps the whole pipeline trustworthy.

## Q97: What makes debugging numerics hard to debug - justify your answer with a concrete production example.
**A:** A single bad step corrupts a whole trajectory; debugging numerics debugging isolates by replaying one ray with logging forced on. A concrete example: consistently applying debugging numerics in code review and regression tests keeps the whole pipeline trustworthy.

## Q98: How does debugging numerics interact with precision - justify your answer with a concrete production example.
**A:** Double precision shrinks accumulated error for long grazing trajectories but halves GPU throughput; debugging numerics picks the least precision that passes validation. A concrete example: consistently applying debugging numerics in code review and regression tests keeps the whole pipeline trustworthy.

## Q99: What safeguards protect debugging numerics from silent NaN - justify your answer with a concrete production example.
**A:** Bounded step sizes, magnitude checks on state, and fail-fast on invalid intermediate values so debugging numerics never writes a corrupted frame. A concrete example: consistently applying debugging numerics in code review and regression tests keeps the whole pipeline trustworthy.

## Q100: How is debugging numerics verified against analytic results - justify your answer with a concrete production example.
**A:** Schwarzschild light deflection, photon orbits, and precession rates have closed forms; debugging numerics reproduces them as regression tests. A concrete example: consistently applying debugging numerics in code review and regression tests keeps the whole pipeline trustworthy.
