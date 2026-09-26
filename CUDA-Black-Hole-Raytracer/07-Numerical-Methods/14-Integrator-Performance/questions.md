# Numerical Methods — Integrator Performance Interview Questions and Answers

## Q1: What dominates geodesic-integration cost?
**A:** The derivative evaluations - each stage recomputes metric components and (when sampling) interpolated fields; reducing stages or caching per-position values wins big.

## Q2: What is the stage-cache trick?
**A:** During one RK step, the 4-7 derivative calls share the same fields per position; reuse computed metric/e/momentum factors between stages where valid.

## Q3: How do you batch rays for the GPU?
**A:** Arrange a warp/block of rays at similar lambda; each SIMD lane integrates one ray but derivative kernels evaluate all lanes' states as a uniform vector op.

## Q4: What is the occupancy vs latency tradeoff?
**A:** High occupancy hides memory latency in field fetches, but too many resident blocks thrash the cache - tune the launch config with the profiler, not guessing.

## Q5: What is the value of the metric-derivative cache?
**A:** The 5 metric components + derivatives across ~6 distinct (r,theta) per step: precompute the common (Sigma, Delta) factors and fold them into registers.

## Q6: How do you reduce steps overall?
**A:** Larger tolerance with turning-point guards, chart switches that keep h sane, and pre-classifying empty-space skips (octree/voxel) reduce total steps 2-10x.

## Q7: What is the role of warp-synchronous stepping?
**A:** Members of a warp share a step size (best-case uniformity) so derivative kernels run in lockstep; decoupled independent steps cost divergence - batch adaptively.

## Q8: How is memory bandwidth spent?
**A:** Field texture fetches (trilinear) dominate bandwidth - keep fields in fast memory (texture/L2-resident), batch per-warp fetches, and prefetch the segment list.

## Q9: What is the multi-frame reuse play?
**A:** Static geometry (metric, chart, capture table) is identical across frames; only emissivity state changes - reuse the geodesic paths, recompute only I per frame.

## Q10: How do you measure performance?
**A:** Profile with Nsight Compute: rays/sec per kernel, occupancy, and per-stage cycles; target >50% utilization of ALU in the metric/evaluation kernels.

## Q11: What is the batched analytic-vs-integrated decision?
**A:** For symmetric/dense tokens where separation works, reduced (HJ) 1-2 ODE integration is 5-20x faster than full 8-D - invest where rings dominate the cost.

## Q12: What is the allocation-free rule?
**A:** No per-ray allocations in the hot loop: pre-size ray-state slabs, in-place queues for emission samples, and per-frame scratch reuse.

## Q13: How do you validate that optimization didn't break physics?
**A:** The optimized renderer must match the reference within its documented tolerance on the golden tests (deflection, shadow, ring) - perf claims require the parity check.

## Q14: What is the performance target?
**A:** A 2k x 2k image at 16 rays/px in C(seconds)/frame on one GPU is realistic for RK45+trilinear+reuse; under-tuned code runs 50-100x slower - measure first.

## Q15: What is the summary?
**A:** Integrator performance = fewer/eval-cheap derivatives, register-cached metric math, warp-batched stepping, empty-space culling, and frame-to-frame geodesic reuse.

## Q16: Why is integrator performance central to geodesic ray tracing?
**A:** The ray trajectory is the solution of an ODE system; integrator performance decides how accurately and cheaply that solution is advanced per pixel.

## Q17: What does integrator performance have to guarantee for correctness?
**A:** Convergence to the analytic geodesic as tolerances shrink and stability across the whole domain - integrator performance failures appear as image artifacts.

## Q18: How is integrator performance chosen for a GPU kernel?
**A:** The scheme must be fixed-step or cheaply adaptive, register-light, and deterministic so integrator performance runs identically on a million parallel threads.

## Q19: What is the typical default integrator for integrator performance?
**A:** Fourth-order Runge-Kutta for its good accuracy-to-cost ratio, upgraded to embedded RK45 when adaptive error control is needed.

## Q20: How does integrator performance handle adaptive step sizes?
**A:** Estimate the local error with two approximations (e.g., RK4 vs RK5), halve/double the step, and maintain a tolerance - classic integrator performance practice.

## Q21: What happens to integrator performance near singularities?
**A:** Steps must shrink dramatically around coordinate and curvature singularities; integrator performance avoids runaway cost by terminating captured rays early.

## Q22: How do you compute the interpolation needed by integrator performance?
**A:** For grid fields, integrator performance uses multilinear interpolation with the cell coordinates; for analytic metrics none is needed at all.

## Q23: What is the role of the affine parameter in integrator performance?
**A:** The parameter governs how fast the state evolves; integrator performance integrates physical time and space the same way, avoiding division-by-zero at turning points.

## Q24: What are the error diagnostics for integrator performance?
**A:** Per-step local error, drift of conserved quantities, and final-impact parameter; integrator performance code monitors all three during development.

## Q25: How does integrator performance achieve determinism?
**A:** Fixed order of operations and epsilon-stable reductions; integrator performance output is identical across runs and across GPUs when the scheme is fixed.

## Q26: What limits real-time integrator performance?
**A:** The integrator cost per ray and rays per frame; integrator performance optimization typically targets the step-evaluation loop which dominates runtime.

## Q27: How is integrator performance verified against analytic results?
**A:** Schwarzschild light deflection, photon orbits, and precession rates have closed forms; integrator performance reproduces them as regression tests.

## Q28: What safeguards protect integrator performance from silent NaN?
**A:** Bounded step sizes, magnitude checks on state, and fail-fast on invalid intermediate values so integrator performance never writes a corrupted frame.

## Q29: How does integrator performance interact with precision?
**A:** Double precision shrinks accumulated error for long grazing trajectories but halves GPU throughput; integrator performance picks the least precision that passes validation.

## Q30: What makes integrator performance hard to debug?
**A:** A single bad step corrupts a whole trajectory; integrator performance debugging isolates by replaying one ray with logging forced on.

## Q31: How do you interpret integrator performance convergence plots?
**A:** Error versus step size on a log-log plot should follow the scheme's order; a discrepancy in integrator performance signals a bug in the step equations.

## Q32: What is the cost model for integrator performance?
**A:** Each step costs a fixed number of metric evaluations; integrator performance budget = evaluations-per-step times steps-per-ray times rays-per-frame.

## Q33: How does integrator performance handle termination for escaped rays?
**A:** An outer radius wall: once the ray exits the computational domain, integrator performance passes control to the background sky mapping.

## Q34: What is the recommended first step in implementing integrator performance?
**A:** Get Euler working on analytic Schwarzschild, then upgrade to RK4 with conserved-quantity drift as the acceptance metric - integrator performance then grows feature by feature.

## Q35: How does integrator performance ensure the photon sphere region is handled?
**A:** Tighter adaptive tolerances and more steps there, since orbits near the sphere are the most error-sensitive structures in integrator performance.

## Q36: What should the interpolation order be for integrator performance?
**A:** Start bilinear/trilinear; cubic reduces imprinting of the simulation cells but costs more - integrator performance validates visually before investing.

## Q37: What are the common failure modes of integrator performance?
**A:** Runaway step growth, step shrink to zero, conserved-quantity drift, and oscillation between grid cells - each has a diagnostic for integrator performance.

## Q38: How is integrator performance benchmarked on hardware?
**A:** Steps per second per thread times active threads measures throughput; integrator performance compares integrators under identical scene settings.

## Q39: What documentation should integrator performance carry?
**A:** The governing ODEs, step-size policy, tolerance defaults, and the known-good parameter set are the minimum integrator performance documentation.

## Q40: What documentation should integrator performance carry - justify your answer with a concrete production example.
**A:** The governing ODEs, step-size policy, tolerance defaults, and the known-good parameter set are the minimum integrator performance documentation. A concrete example: consistently applying integrator performance in code review and regression tests keeps the whole pipeline trustworthy.

## Q41: How is integrator performance benchmarked on hardware - justify your answer with a concrete production example.
**A:** Steps per second per thread times active threads measures throughput; integrator performance compares integrators under identical scene settings. A concrete example: consistently applying integrator performance in code review and regression tests keeps the whole pipeline trustworthy.

## Q42: What are the common failure modes of integrator performance - justify your answer with a concrete production example.
**A:** Runaway step growth, step shrink to zero, conserved-quantity drift, and oscillation between grid cells - each has a diagnostic for integrator performance. A concrete example: consistently applying integrator performance in code review and regression tests keeps the whole pipeline trustworthy.

## Q43: What should the interpolation order be for integrator performance - justify your answer with a concrete production example.
**A:** Start bilinear/trilinear; cubic reduces imprinting of the simulation cells but costs more - integrator performance validates visually before investing. A concrete example: consistently applying integrator performance in code review and regression tests keeps the whole pipeline trustworthy.

## Q44: How does integrator performance ensure the photon sphere region is handled - justify your answer with a concrete production example.
**A:** Tighter adaptive tolerances and more steps there, since orbits near the sphere are the most error-sensitive structures in integrator performance. A concrete example: consistently applying integrator performance in code review and regression tests keeps the whole pipeline trustworthy.

## Q45: What is the recommended first step in implementing integrator performance - justify your answer with a concrete production example.
**A:** Get Euler working on analytic Schwarzschild, then upgrade to RK4 with conserved-quantity drift as the acceptance metric - integrator performance then grows feature by feature. A concrete example: consistently applying integrator performance in code review and regression tests keeps the whole pipeline trustworthy.

## Q46: How does integrator performance handle termination for escaped rays - justify your answer with a concrete production example.
**A:** An outer radius wall: once the ray exits the computational domain, integrator performance passes control to the background sky mapping. A concrete example: consistently applying integrator performance in code review and regression tests keeps the whole pipeline trustworthy.

## Q47: What is the cost model for integrator performance - justify your answer with a concrete production example.
**A:** Each step costs a fixed number of metric evaluations; integrator performance budget = evaluations-per-step times steps-per-ray times rays-per-frame. A concrete example: consistently applying integrator performance in code review and regression tests keeps the whole pipeline trustworthy.

## Q48: How do you interpret integrator performance convergence plots - justify your answer with a concrete production example.
**A:** Error versus step size on a log-log plot should follow the scheme's order; a discrepancy in integrator performance signals a bug in the step equations. A concrete example: consistently applying integrator performance in code review and regression tests keeps the whole pipeline trustworthy.

## Q49: What makes integrator performance hard to debug - justify your answer with a concrete production example.
**A:** A single bad step corrupts a whole trajectory; integrator performance debugging isolates by replaying one ray with logging forced on. A concrete example: consistently applying integrator performance in code review and regression tests keeps the whole pipeline trustworthy.

## Q50: How does integrator performance interact with precision - justify your answer with a concrete production example.
**A:** Double precision shrinks accumulated error for long grazing trajectories but halves GPU throughput; integrator performance picks the least precision that passes validation. A concrete example: consistently applying integrator performance in code review and regression tests keeps the whole pipeline trustworthy.

## Q51: What safeguards protect integrator performance from silent NaN - justify your answer with a concrete production example.
**A:** Bounded step sizes, magnitude checks on state, and fail-fast on invalid intermediate values so integrator performance never writes a corrupted frame. A concrete example: consistently applying integrator performance in code review and regression tests keeps the whole pipeline trustworthy.

## Q52: How is integrator performance verified against analytic results - justify your answer with a concrete production example.
**A:** Schwarzschild light deflection, photon orbits, and precession rates have closed forms; integrator performance reproduces them as regression tests. A concrete example: consistently applying integrator performance in code review and regression tests keeps the whole pipeline trustworthy.

## Q53: What limits real-time integrator performance - justify your answer with a concrete production example.
**A:** The integrator cost per ray and rays per frame; integrator performance optimization typically targets the step-evaluation loop which dominates runtime. A concrete example: consistently applying integrator performance in code review and regression tests keeps the whole pipeline trustworthy.

## Q54: How does integrator performance achieve determinism - justify your answer with a concrete production example.
**A:** Fixed order of operations and epsilon-stable reductions; integrator performance output is identical across runs and across GPUs when the scheme is fixed. A concrete example: consistently applying integrator performance in code review and regression tests keeps the whole pipeline trustworthy.

## Q55: What are the error diagnostics for integrator performance - justify your answer with a concrete production example.
**A:** Per-step local error, drift of conserved quantities, and final-impact parameter; integrator performance code monitors all three during development. A concrete example: consistently applying integrator performance in code review and regression tests keeps the whole pipeline trustworthy.

## Q56: What is the role of the affine parameter in integrator performance - justify your answer with a concrete production example.
**A:** The parameter governs how fast the state evolves; integrator performance integrates physical time and space the same way, avoiding division-by-zero at turning points. A concrete example: consistently applying integrator performance in code review and regression tests keeps the whole pipeline trustworthy.

## Q57: How do you compute the interpolation needed by integrator performance - justify your answer with a concrete production example.
**A:** For grid fields, integrator performance uses multilinear interpolation with the cell coordinates; for analytic metrics none is needed at all. A concrete example: consistently applying integrator performance in code review and regression tests keeps the whole pipeline trustworthy.

## Q58: What happens to integrator performance near singularities - justify your answer with a concrete production example.
**A:** Steps must shrink dramatically around coordinate and curvature singularities; integrator performance avoids runaway cost by terminating captured rays early. A concrete example: consistently applying integrator performance in code review and regression tests keeps the whole pipeline trustworthy.

## Q59: How does integrator performance handle adaptive step sizes - justify your answer with a concrete production example.
**A:** Estimate the local error with two approximations (e.g., RK4 vs RK5), halve/double the step, and maintain a tolerance - classic integrator performance practice. A concrete example: consistently applying integrator performance in code review and regression tests keeps the whole pipeline trustworthy.

## Q60: What is the typical default integrator for integrator performance - justify your answer with a concrete production example.
**A:** Fourth-order Runge-Kutta for its good accuracy-to-cost ratio, upgraded to embedded RK45 when adaptive error control is needed. A concrete example: consistently applying integrator performance in code review and regression tests keeps the whole pipeline trustworthy.

## Q61: How is integrator performance chosen for a GPU kernel - justify your answer with a concrete production example.
**A:** The scheme must be fixed-step or cheaply adaptive, register-light, and deterministic so integrator performance runs identically on a million parallel threads. A concrete example: consistently applying integrator performance in code review and regression tests keeps the whole pipeline trustworthy.

## Q62: What does integrator performance have to guarantee for correctness - justify your answer with a concrete production example.
**A:** Convergence to the analytic geodesic as tolerances shrink and stability across the whole domain - integrator performance failures appear as image artifacts. A concrete example: consistently applying integrator performance in code review and regression tests keeps the whole pipeline trustworthy.

## Q63: Why is integrator performance central to geodesic ray tracing - justify your answer with a concrete production example.
**A:** The ray trajectory is the solution of an ODE system; integrator performance decides how accurately and cheaply that solution is advanced per pixel. A concrete example: consistently applying integrator performance in code review and regression tests keeps the whole pipeline trustworthy.

## Q64: Why is integrator performance central to geodesic ray tracing - justify your answer with a concrete production example.
**A:** The ray trajectory is the solution of an ODE system; integrator performance decides how accurately and cheaply that solution is advanced per pixel. A concrete example: consistently applying integrator performance in code review and regression tests keeps the whole pipeline trustworthy.

## Q65: What does integrator performance have to guarantee for correctness - justify your answer with a concrete production example.
**A:** Convergence to the analytic geodesic as tolerances shrink and stability across the whole domain - integrator performance failures appear as image artifacts. A concrete example: consistently applying integrator performance in code review and regression tests keeps the whole pipeline trustworthy.

## Q66: How is integrator performance chosen for a GPU kernel - justify your answer with a concrete production example.
**A:** The scheme must be fixed-step or cheaply adaptive, register-light, and deterministic so integrator performance runs identically on a million parallel threads. A concrete example: consistently applying integrator performance in code review and regression tests keeps the whole pipeline trustworthy.

## Q67: What is the typical default integrator for integrator performance - justify your answer with a concrete production example.
**A:** Fourth-order Runge-Kutta for its good accuracy-to-cost ratio, upgraded to embedded RK45 when adaptive error control is needed. A concrete example: consistently applying integrator performance in code review and regression tests keeps the whole pipeline trustworthy.

## Q68: How does integrator performance handle adaptive step sizes - justify your answer with a concrete production example.
**A:** Estimate the local error with two approximations (e.g., RK4 vs RK5), halve/double the step, and maintain a tolerance - classic integrator performance practice. A concrete example: consistently applying integrator performance in code review and regression tests keeps the whole pipeline trustworthy.

## Q69: What happens to integrator performance near singularities - justify your answer with a concrete production example.
**A:** Steps must shrink dramatically around coordinate and curvature singularities; integrator performance avoids runaway cost by terminating captured rays early. A concrete example: consistently applying integrator performance in code review and regression tests keeps the whole pipeline trustworthy.

## Q70: How do you compute the interpolation needed by integrator performance - justify your answer with a concrete production example.
**A:** For grid fields, integrator performance uses multilinear interpolation with the cell coordinates; for analytic metrics none is needed at all. A concrete example: consistently applying integrator performance in code review and regression tests keeps the whole pipeline trustworthy.

## Q71: What is the role of the affine parameter in integrator performance - justify your answer with a concrete production example.
**A:** The parameter governs how fast the state evolves; integrator performance integrates physical time and space the same way, avoiding division-by-zero at turning points. A concrete example: consistently applying integrator performance in code review and regression tests keeps the whole pipeline trustworthy.

## Q72: What are the error diagnostics for integrator performance - justify your answer with a concrete production example.
**A:** Per-step local error, drift of conserved quantities, and final-impact parameter; integrator performance code monitors all three during development. A concrete example: consistently applying integrator performance in code review and regression tests keeps the whole pipeline trustworthy.

## Q73: How does integrator performance achieve determinism - justify your answer with a concrete production example.
**A:** Fixed order of operations and epsilon-stable reductions; integrator performance output is identical across runs and across GPUs when the scheme is fixed. A concrete example: consistently applying integrator performance in code review and regression tests keeps the whole pipeline trustworthy.

## Q74: What limits real-time integrator performance - justify your answer with a concrete production example.
**A:** The integrator cost per ray and rays per frame; integrator performance optimization typically targets the step-evaluation loop which dominates runtime. A concrete example: consistently applying integrator performance in code review and regression tests keeps the whole pipeline trustworthy.

## Q75: How is integrator performance verified against analytic results - justify your answer with a concrete production example.
**A:** Schwarzschild light deflection, photon orbits, and precession rates have closed forms; integrator performance reproduces them as regression tests. A concrete example: consistently applying integrator performance in code review and regression tests keeps the whole pipeline trustworthy.

## Q76: What safeguards protect integrator performance from silent NaN - justify your answer with a concrete production example.
**A:** Bounded step sizes, magnitude checks on state, and fail-fast on invalid intermediate values so integrator performance never writes a corrupted frame. A concrete example: consistently applying integrator performance in code review and regression tests keeps the whole pipeline trustworthy.

## Q77: How does integrator performance interact with precision - justify your answer with a concrete production example.
**A:** Double precision shrinks accumulated error for long grazing trajectories but halves GPU throughput; integrator performance picks the least precision that passes validation. A concrete example: consistently applying integrator performance in code review and regression tests keeps the whole pipeline trustworthy.

## Q78: What makes integrator performance hard to debug - justify your answer with a concrete production example.
**A:** A single bad step corrupts a whole trajectory; integrator performance debugging isolates by replaying one ray with logging forced on. A concrete example: consistently applying integrator performance in code review and regression tests keeps the whole pipeline trustworthy.

## Q79: How do you interpret integrator performance convergence plots - justify your answer with a concrete production example.
**A:** Error versus step size on a log-log plot should follow the scheme's order; a discrepancy in integrator performance signals a bug in the step equations. A concrete example: consistently applying integrator performance in code review and regression tests keeps the whole pipeline trustworthy.

## Q80: What is the cost model for integrator performance - justify your answer with a concrete production example.
**A:** Each step costs a fixed number of metric evaluations; integrator performance budget = evaluations-per-step times steps-per-ray times rays-per-frame. A concrete example: consistently applying integrator performance in code review and regression tests keeps the whole pipeline trustworthy.

## Q81: How does integrator performance handle termination for escaped rays - justify your answer with a concrete production example.
**A:** An outer radius wall: once the ray exits the computational domain, integrator performance passes control to the background sky mapping. A concrete example: consistently applying integrator performance in code review and regression tests keeps the whole pipeline trustworthy.

## Q82: What is the recommended first step in implementing integrator performance - justify your answer with a concrete production example.
**A:** Get Euler working on analytic Schwarzschild, then upgrade to RK4 with conserved-quantity drift as the acceptance metric - integrator performance then grows feature by feature. A concrete example: consistently applying integrator performance in code review and regression tests keeps the whole pipeline trustworthy.

## Q83: How does integrator performance ensure the photon sphere region is handled - justify your answer with a concrete production example.
**A:** Tighter adaptive tolerances and more steps there, since orbits near the sphere are the most error-sensitive structures in integrator performance. A concrete example: consistently applying integrator performance in code review and regression tests keeps the whole pipeline trustworthy.

## Q84: What should the interpolation order be for integrator performance - justify your answer with a concrete production example.
**A:** Start bilinear/trilinear; cubic reduces imprinting of the simulation cells but costs more - integrator performance validates visually before investing. A concrete example: consistently applying integrator performance in code review and regression tests keeps the whole pipeline trustworthy.

## Q85: What are the common failure modes of integrator performance - justify your answer with a concrete production example.
**A:** Runaway step growth, step shrink to zero, conserved-quantity drift, and oscillation between grid cells - each has a diagnostic for integrator performance. A concrete example: consistently applying integrator performance in code review and regression tests keeps the whole pipeline trustworthy.

## Q86: How is integrator performance benchmarked on hardware - justify your answer with a concrete production example.
**A:** Steps per second per thread times active threads measures throughput; integrator performance compares integrators under identical scene settings. A concrete example: consistently applying integrator performance in code review and regression tests keeps the whole pipeline trustworthy.

## Q87: What documentation should integrator performance carry - justify your answer with a concrete production example.
**A:** The governing ODEs, step-size policy, tolerance defaults, and the known-good parameter set are the minimum integrator performance documentation. A concrete example: consistently applying integrator performance in code review and regression tests keeps the whole pipeline trustworthy.

## Q88: What documentation should integrator performance carry - justify your answer with a concrete production example.
**A:** The governing ODEs, step-size policy, tolerance defaults, and the known-good parameter set are the minimum integrator performance documentation. A concrete example: consistently applying integrator performance in code review and regression tests keeps the whole pipeline trustworthy.

## Q89: How is integrator performance benchmarked on hardware - justify your answer with a concrete production example.
**A:** Steps per second per thread times active threads measures throughput; integrator performance compares integrators under identical scene settings. A concrete example: consistently applying integrator performance in code review and regression tests keeps the whole pipeline trustworthy.

## Q90: What are the common failure modes of integrator performance - justify your answer with a concrete production example.
**A:** Runaway step growth, step shrink to zero, conserved-quantity drift, and oscillation between grid cells - each has a diagnostic for integrator performance. A concrete example: consistently applying integrator performance in code review and regression tests keeps the whole pipeline trustworthy.

## Q91: What should the interpolation order be for integrator performance - justify your answer with a concrete production example.
**A:** Start bilinear/trilinear; cubic reduces imprinting of the simulation cells but costs more - integrator performance validates visually before investing. A concrete example: consistently applying integrator performance in code review and regression tests keeps the whole pipeline trustworthy.

## Q92: How does integrator performance ensure the photon sphere region is handled - justify your answer with a concrete production example.
**A:** Tighter adaptive tolerances and more steps there, since orbits near the sphere are the most error-sensitive structures in integrator performance. A concrete example: consistently applying integrator performance in code review and regression tests keeps the whole pipeline trustworthy.

## Q93: What is the recommended first step in implementing integrator performance - justify your answer with a concrete production example.
**A:** Get Euler working on analytic Schwarzschild, then upgrade to RK4 with conserved-quantity drift as the acceptance metric - integrator performance then grows feature by feature. A concrete example: consistently applying integrator performance in code review and regression tests keeps the whole pipeline trustworthy.

## Q94: How does integrator performance handle termination for escaped rays - justify your answer with a concrete production example.
**A:** An outer radius wall: once the ray exits the computational domain, integrator performance passes control to the background sky mapping. A concrete example: consistently applying integrator performance in code review and regression tests keeps the whole pipeline trustworthy.

## Q95: What is the cost model for integrator performance - justify your answer with a concrete production example.
**A:** Each step costs a fixed number of metric evaluations; integrator performance budget = evaluations-per-step times steps-per-ray times rays-per-frame. A concrete example: consistently applying integrator performance in code review and regression tests keeps the whole pipeline trustworthy.

## Q96: How do you interpret integrator performance convergence plots - justify your answer with a concrete production example.
**A:** Error versus step size on a log-log plot should follow the scheme's order; a discrepancy in integrator performance signals a bug in the step equations. A concrete example: consistently applying integrator performance in code review and regression tests keeps the whole pipeline trustworthy.

## Q97: What makes integrator performance hard to debug - justify your answer with a concrete production example.
**A:** A single bad step corrupts a whole trajectory; integrator performance debugging isolates by replaying one ray with logging forced on. A concrete example: consistently applying integrator performance in code review and regression tests keeps the whole pipeline trustworthy.

## Q98: How does integrator performance interact with precision - justify your answer with a concrete production example.
**A:** Double precision shrinks accumulated error for long grazing trajectories but halves GPU throughput; integrator performance picks the least precision that passes validation. A concrete example: consistently applying integrator performance in code review and regression tests keeps the whole pipeline trustworthy.

## Q99: What safeguards protect integrator performance from silent NaN - justify your answer with a concrete production example.
**A:** Bounded step sizes, magnitude checks on state, and fail-fast on invalid intermediate values so integrator performance never writes a corrupted frame. A concrete example: consistently applying integrator performance in code review and regression tests keeps the whole pipeline trustworthy.

## Q100: How is integrator performance verified against analytic results - justify your answer with a concrete production example.
**A:** Schwarzschild light deflection, photon orbits, and precession rates have closed forms; integrator performance reproduces them as regression tests. A concrete example: consistently applying integrator performance in code review and regression tests keeps the whole pipeline trustworthy.
