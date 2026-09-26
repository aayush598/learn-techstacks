# Numerical Methods — Termination Criteria Interview Questions and Answers

## Q1: What are the termination criteria for a ray?
**A:** Four exits: HIT (reached the emission surface), CAPTURE (crossed the horizon), MISS (left the bounding domain), and BUDGET (step count exceeded) - each mapped to a pixel contribution.

## Q2: What is the HIT condition?
**A:** The ray crosses the disk/emission surface (e.g., z=0 crossing for a thin disk, or a volume emissivity threshold); refined by the bracketing/bisection finder.

## Q3: What is the CAPTURE condition?
**A:** r <= r+ (chart-dependent) with an inward component; the pixel is black (shadow) - the geometry's own cutoff.

## Q4: What is the MISS condition?
**A:** r > r_out (far boundary, e.g., 2000 M) with decreasing contribution; the pixel gets sky or the far-field integral's end.

## Q5: What is the BUDGET condition?
**A:** A safety cap on steps per ray (e.g., 50k) to bound worst-case cost near the ring - rare and flagged rather than silently truncating.

## Q6: How do you detect the disk HIT accurately?
**A:** Bracket the sign change of (z - 0) or (r - r_disk) between geodesic steps, then bisect/refine to sub-pixel accuracy without extra ODE work.

## Q7: Why have termination at all?
**A:** Without it, winding rays near the photon sphere integrate forever; explicit criteria convert 'hard to integrate' into 'correctly sampled boundary'.

## Q8: How do you guarantee no ray 'gets stuck'?
**A:** Along with BUDGET, monitor affine-parameter progress delta-lambda-per-step; if it shrinks below a floor while H>0, force a step and report it.

## Q9: What do you record on termination?
**A:** Hit (position, redshift, accumulated I/Stokes), capture (flagged), miss (sky direction or zero), and any budget warnings - the event record per pixel.

## Q10: How do termination criteria affect quality?
**A:** A too-tight BUDGET near the ring truncates winding rays -> faint outer 'echoes' of the ring - set the cap high enough that truncations stay < 1% of pixels.

## Q11: What is the interplay with supersampling?
**A:** Rays terminate independently; pixel value averages over terminating statuses - a mix of HIT/MISS at a boundary pixel is the natural blend.

## Q12: How do you validate termination?
**A:** Trace the analytic shadow: terminate exactly at b = b_crit boundary rays must land in the expected pixel class (capture vs miss) within pixel tolerance.

## Q13: What is the far-field sky termination?
**A:** r_out chosen far enough that the residual deflection is negligible (< 0.1 pixel); verified by doubling r_out and checking pixel colors unchanged.

## Q14: What is the summary?
**A:** Termination criteria are the ray's contract: hit/capture/miss/budget, each precisely defined and validated, turning infinite geodesics into finite rendering.

## Q15: Why is termination criteria central to geodesic ray tracing?
**A:** The ray trajectory is the solution of an ODE system; termination criteria decides how accurately and cheaply that solution is advanced per pixel.

## Q16: What does termination criteria have to guarantee for correctness?
**A:** Convergence to the analytic geodesic as tolerances shrink and stability across the whole domain - termination criteria failures appear as image artifacts.

## Q17: How is termination criteria chosen for a GPU kernel?
**A:** The scheme must be fixed-step or cheaply adaptive, register-light, and deterministic so termination criteria runs identically on a million parallel threads.

## Q18: What is the typical default integrator for termination criteria?
**A:** Fourth-order Runge-Kutta for its good accuracy-to-cost ratio, upgraded to embedded RK45 when adaptive error control is needed.

## Q19: How does termination criteria handle adaptive step sizes?
**A:** Estimate the local error with two approximations (e.g., RK4 vs RK5), halve/double the step, and maintain a tolerance - classic termination criteria practice.

## Q20: What happens to termination criteria near singularities?
**A:** Steps must shrink dramatically around coordinate and curvature singularities; termination criteria avoids runaway cost by terminating captured rays early.

## Q21: How do you compute the interpolation needed by termination criteria?
**A:** For grid fields, termination criteria uses multilinear interpolation with the cell coordinates; for analytic metrics none is needed at all.

## Q22: What is the role of the affine parameter in termination criteria?
**A:** The parameter governs how fast the state evolves; termination criteria integrates physical time and space the same way, avoiding division-by-zero at turning points.

## Q23: What are the error diagnostics for termination criteria?
**A:** Per-step local error, drift of conserved quantities, and final-impact parameter; termination criteria code monitors all three during development.

## Q24: How does termination criteria achieve determinism?
**A:** Fixed order of operations and epsilon-stable reductions; termination criteria output is identical across runs and across GPUs when the scheme is fixed.

## Q25: What limits real-time termination criteria?
**A:** The integrator cost per ray and rays per frame; termination criteria optimization typically targets the step-evaluation loop which dominates runtime.

## Q26: How is termination criteria verified against analytic results?
**A:** Schwarzschild light deflection, photon orbits, and precession rates have closed forms; termination criteria reproduces them as regression tests.

## Q27: What safeguards protect termination criteria from silent NaN?
**A:** Bounded step sizes, magnitude checks on state, and fail-fast on invalid intermediate values so termination criteria never writes a corrupted frame.

## Q28: How does termination criteria interact with precision?
**A:** Double precision shrinks accumulated error for long grazing trajectories but halves GPU throughput; termination criteria picks the least precision that passes validation.

## Q29: What makes termination criteria hard to debug?
**A:** A single bad step corrupts a whole trajectory; termination criteria debugging isolates by replaying one ray with logging forced on.

## Q30: How do you interpret termination criteria convergence plots?
**A:** Error versus step size on a log-log plot should follow the scheme's order; a discrepancy in termination criteria signals a bug in the step equations.

## Q31: What is the cost model for termination criteria?
**A:** Each step costs a fixed number of metric evaluations; termination criteria budget = evaluations-per-step times steps-per-ray times rays-per-frame.

## Q32: How does termination criteria handle termination for escaped rays?
**A:** An outer radius wall: once the ray exits the computational domain, termination criteria passes control to the background sky mapping.

## Q33: What is the recommended first step in implementing termination criteria?
**A:** Get Euler working on analytic Schwarzschild, then upgrade to RK4 with conserved-quantity drift as the acceptance metric - termination criteria then grows feature by feature.

## Q34: How does termination criteria ensure the photon sphere region is handled?
**A:** Tighter adaptive tolerances and more steps there, since orbits near the sphere are the most error-sensitive structures in termination criteria.

## Q35: What should the interpolation order be for termination criteria?
**A:** Start bilinear/trilinear; cubic reduces imprinting of the simulation cells but costs more - termination criteria validates visually before investing.

## Q36: What are the common failure modes of termination criteria?
**A:** Runaway step growth, step shrink to zero, conserved-quantity drift, and oscillation between grid cells - each has a diagnostic for termination criteria.

## Q37: How is termination criteria benchmarked on hardware?
**A:** Steps per second per thread times active threads measures throughput; termination criteria compares integrators under identical scene settings.

## Q38: What documentation should termination criteria carry?
**A:** The governing ODEs, step-size policy, tolerance defaults, and the known-good parameter set are the minimum termination criteria documentation.

## Q39: What documentation should termination criteria carry - justify your answer with a concrete production example.
**A:** The governing ODEs, step-size policy, tolerance defaults, and the known-good parameter set are the minimum termination criteria documentation. A concrete example: consistently applying termination criteria in code review and regression tests keeps the whole pipeline trustworthy.

## Q40: How is termination criteria benchmarked on hardware - justify your answer with a concrete production example.
**A:** Steps per second per thread times active threads measures throughput; termination criteria compares integrators under identical scene settings. A concrete example: consistently applying termination criteria in code review and regression tests keeps the whole pipeline trustworthy.

## Q41: What are the common failure modes of termination criteria - justify your answer with a concrete production example.
**A:** Runaway step growth, step shrink to zero, conserved-quantity drift, and oscillation between grid cells - each has a diagnostic for termination criteria. A concrete example: consistently applying termination criteria in code review and regression tests keeps the whole pipeline trustworthy.

## Q42: What should the interpolation order be for termination criteria - justify your answer with a concrete production example.
**A:** Start bilinear/trilinear; cubic reduces imprinting of the simulation cells but costs more - termination criteria validates visually before investing. A concrete example: consistently applying termination criteria in code review and regression tests keeps the whole pipeline trustworthy.

## Q43: How does termination criteria ensure the photon sphere region is handled - justify your answer with a concrete production example.
**A:** Tighter adaptive tolerances and more steps there, since orbits near the sphere are the most error-sensitive structures in termination criteria. A concrete example: consistently applying termination criteria in code review and regression tests keeps the whole pipeline trustworthy.

## Q44: What is the recommended first step in implementing termination criteria - justify your answer with a concrete production example.
**A:** Get Euler working on analytic Schwarzschild, then upgrade to RK4 with conserved-quantity drift as the acceptance metric - termination criteria then grows feature by feature. A concrete example: consistently applying termination criteria in code review and regression tests keeps the whole pipeline trustworthy.

## Q45: How does termination criteria handle termination for escaped rays - justify your answer with a concrete production example.
**A:** An outer radius wall: once the ray exits the computational domain, termination criteria passes control to the background sky mapping. A concrete example: consistently applying termination criteria in code review and regression tests keeps the whole pipeline trustworthy.

## Q46: What is the cost model for termination criteria - justify your answer with a concrete production example.
**A:** Each step costs a fixed number of metric evaluations; termination criteria budget = evaluations-per-step times steps-per-ray times rays-per-frame. A concrete example: consistently applying termination criteria in code review and regression tests keeps the whole pipeline trustworthy.

## Q47: How do you interpret termination criteria convergence plots - justify your answer with a concrete production example.
**A:** Error versus step size on a log-log plot should follow the scheme's order; a discrepancy in termination criteria signals a bug in the step equations. A concrete example: consistently applying termination criteria in code review and regression tests keeps the whole pipeline trustworthy.

## Q48: What makes termination criteria hard to debug - justify your answer with a concrete production example.
**A:** A single bad step corrupts a whole trajectory; termination criteria debugging isolates by replaying one ray with logging forced on. A concrete example: consistently applying termination criteria in code review and regression tests keeps the whole pipeline trustworthy.

## Q49: How does termination criteria interact with precision - justify your answer with a concrete production example.
**A:** Double precision shrinks accumulated error for long grazing trajectories but halves GPU throughput; termination criteria picks the least precision that passes validation. A concrete example: consistently applying termination criteria in code review and regression tests keeps the whole pipeline trustworthy.

## Q50: What safeguards protect termination criteria from silent NaN - justify your answer with a concrete production example.
**A:** Bounded step sizes, magnitude checks on state, and fail-fast on invalid intermediate values so termination criteria never writes a corrupted frame. A concrete example: consistently applying termination criteria in code review and regression tests keeps the whole pipeline trustworthy.

## Q51: How is termination criteria verified against analytic results - justify your answer with a concrete production example.
**A:** Schwarzschild light deflection, photon orbits, and precession rates have closed forms; termination criteria reproduces them as regression tests. A concrete example: consistently applying termination criteria in code review and regression tests keeps the whole pipeline trustworthy.

## Q52: What limits real-time termination criteria - justify your answer with a concrete production example.
**A:** The integrator cost per ray and rays per frame; termination criteria optimization typically targets the step-evaluation loop which dominates runtime. A concrete example: consistently applying termination criteria in code review and regression tests keeps the whole pipeline trustworthy.

## Q53: How does termination criteria achieve determinism - justify your answer with a concrete production example.
**A:** Fixed order of operations and epsilon-stable reductions; termination criteria output is identical across runs and across GPUs when the scheme is fixed. A concrete example: consistently applying termination criteria in code review and regression tests keeps the whole pipeline trustworthy.

## Q54: What are the error diagnostics for termination criteria - justify your answer with a concrete production example.
**A:** Per-step local error, drift of conserved quantities, and final-impact parameter; termination criteria code monitors all three during development. A concrete example: consistently applying termination criteria in code review and regression tests keeps the whole pipeline trustworthy.

## Q55: What is the role of the affine parameter in termination criteria - justify your answer with a concrete production example.
**A:** The parameter governs how fast the state evolves; termination criteria integrates physical time and space the same way, avoiding division-by-zero at turning points. A concrete example: consistently applying termination criteria in code review and regression tests keeps the whole pipeline trustworthy.

## Q56: How do you compute the interpolation needed by termination criteria - justify your answer with a concrete production example.
**A:** For grid fields, termination criteria uses multilinear interpolation with the cell coordinates; for analytic metrics none is needed at all. A concrete example: consistently applying termination criteria in code review and regression tests keeps the whole pipeline trustworthy.

## Q57: What happens to termination criteria near singularities - justify your answer with a concrete production example.
**A:** Steps must shrink dramatically around coordinate and curvature singularities; termination criteria avoids runaway cost by terminating captured rays early. A concrete example: consistently applying termination criteria in code review and regression tests keeps the whole pipeline trustworthy.

## Q58: How does termination criteria handle adaptive step sizes - justify your answer with a concrete production example.
**A:** Estimate the local error with two approximations (e.g., RK4 vs RK5), halve/double the step, and maintain a tolerance - classic termination criteria practice. A concrete example: consistently applying termination criteria in code review and regression tests keeps the whole pipeline trustworthy.

## Q59: What is the typical default integrator for termination criteria - justify your answer with a concrete production example.
**A:** Fourth-order Runge-Kutta for its good accuracy-to-cost ratio, upgraded to embedded RK45 when adaptive error control is needed. A concrete example: consistently applying termination criteria in code review and regression tests keeps the whole pipeline trustworthy.

## Q60: How is termination criteria chosen for a GPU kernel - justify your answer with a concrete production example.
**A:** The scheme must be fixed-step or cheaply adaptive, register-light, and deterministic so termination criteria runs identically on a million parallel threads. A concrete example: consistently applying termination criteria in code review and regression tests keeps the whole pipeline trustworthy.

## Q61: What does termination criteria have to guarantee for correctness - justify your answer with a concrete production example.
**A:** Convergence to the analytic geodesic as tolerances shrink and stability across the whole domain - termination criteria failures appear as image artifacts. A concrete example: consistently applying termination criteria in code review and regression tests keeps the whole pipeline trustworthy.

## Q62: Why is termination criteria central to geodesic ray tracing - justify your answer with a concrete production example.
**A:** The ray trajectory is the solution of an ODE system; termination criteria decides how accurately and cheaply that solution is advanced per pixel. A concrete example: consistently applying termination criteria in code review and regression tests keeps the whole pipeline trustworthy.

## Q63: Why is termination criteria central to geodesic ray tracing - justify your answer with a concrete production example.
**A:** The ray trajectory is the solution of an ODE system; termination criteria decides how accurately and cheaply that solution is advanced per pixel. A concrete example: consistently applying termination criteria in code review and regression tests keeps the whole pipeline trustworthy.

## Q64: What does termination criteria have to guarantee for correctness - justify your answer with a concrete production example.
**A:** Convergence to the analytic geodesic as tolerances shrink and stability across the whole domain - termination criteria failures appear as image artifacts. A concrete example: consistently applying termination criteria in code review and regression tests keeps the whole pipeline trustworthy.

## Q65: How is termination criteria chosen for a GPU kernel - justify your answer with a concrete production example.
**A:** The scheme must be fixed-step or cheaply adaptive, register-light, and deterministic so termination criteria runs identically on a million parallel threads. A concrete example: consistently applying termination criteria in code review and regression tests keeps the whole pipeline trustworthy.

## Q66: What is the typical default integrator for termination criteria - justify your answer with a concrete production example.
**A:** Fourth-order Runge-Kutta for its good accuracy-to-cost ratio, upgraded to embedded RK45 when adaptive error control is needed. A concrete example: consistently applying termination criteria in code review and regression tests keeps the whole pipeline trustworthy.

## Q67: How does termination criteria handle adaptive step sizes - justify your answer with a concrete production example.
**A:** Estimate the local error with two approximations (e.g., RK4 vs RK5), halve/double the step, and maintain a tolerance - classic termination criteria practice. A concrete example: consistently applying termination criteria in code review and regression tests keeps the whole pipeline trustworthy.

## Q68: What happens to termination criteria near singularities - justify your answer with a concrete production example.
**A:** Steps must shrink dramatically around coordinate and curvature singularities; termination criteria avoids runaway cost by terminating captured rays early. A concrete example: consistently applying termination criteria in code review and regression tests keeps the whole pipeline trustworthy.

## Q69: How do you compute the interpolation needed by termination criteria - justify your answer with a concrete production example.
**A:** For grid fields, termination criteria uses multilinear interpolation with the cell coordinates; for analytic metrics none is needed at all. A concrete example: consistently applying termination criteria in code review and regression tests keeps the whole pipeline trustworthy.

## Q70: What is the role of the affine parameter in termination criteria - justify your answer with a concrete production example.
**A:** The parameter governs how fast the state evolves; termination criteria integrates physical time and space the same way, avoiding division-by-zero at turning points. A concrete example: consistently applying termination criteria in code review and regression tests keeps the whole pipeline trustworthy.

## Q71: What are the error diagnostics for termination criteria - justify your answer with a concrete production example.
**A:** Per-step local error, drift of conserved quantities, and final-impact parameter; termination criteria code monitors all three during development. A concrete example: consistently applying termination criteria in code review and regression tests keeps the whole pipeline trustworthy.

## Q72: How does termination criteria achieve determinism - justify your answer with a concrete production example.
**A:** Fixed order of operations and epsilon-stable reductions; termination criteria output is identical across runs and across GPUs when the scheme is fixed. A concrete example: consistently applying termination criteria in code review and regression tests keeps the whole pipeline trustworthy.

## Q73: What limits real-time termination criteria - justify your answer with a concrete production example.
**A:** The integrator cost per ray and rays per frame; termination criteria optimization typically targets the step-evaluation loop which dominates runtime. A concrete example: consistently applying termination criteria in code review and regression tests keeps the whole pipeline trustworthy.

## Q74: How is termination criteria verified against analytic results - justify your answer with a concrete production example.
**A:** Schwarzschild light deflection, photon orbits, and precession rates have closed forms; termination criteria reproduces them as regression tests. A concrete example: consistently applying termination criteria in code review and regression tests keeps the whole pipeline trustworthy.

## Q75: What safeguards protect termination criteria from silent NaN - justify your answer with a concrete production example.
**A:** Bounded step sizes, magnitude checks on state, and fail-fast on invalid intermediate values so termination criteria never writes a corrupted frame. A concrete example: consistently applying termination criteria in code review and regression tests keeps the whole pipeline trustworthy.

## Q76: How does termination criteria interact with precision - justify your answer with a concrete production example.
**A:** Double precision shrinks accumulated error for long grazing trajectories but halves GPU throughput; termination criteria picks the least precision that passes validation. A concrete example: consistently applying termination criteria in code review and regression tests keeps the whole pipeline trustworthy.

## Q77: What makes termination criteria hard to debug - justify your answer with a concrete production example.
**A:** A single bad step corrupts a whole trajectory; termination criteria debugging isolates by replaying one ray with logging forced on. A concrete example: consistently applying termination criteria in code review and regression tests keeps the whole pipeline trustworthy.

## Q78: How do you interpret termination criteria convergence plots - justify your answer with a concrete production example.
**A:** Error versus step size on a log-log plot should follow the scheme's order; a discrepancy in termination criteria signals a bug in the step equations. A concrete example: consistently applying termination criteria in code review and regression tests keeps the whole pipeline trustworthy.

## Q79: What is the cost model for termination criteria - justify your answer with a concrete production example.
**A:** Each step costs a fixed number of metric evaluations; termination criteria budget = evaluations-per-step times steps-per-ray times rays-per-frame. A concrete example: consistently applying termination criteria in code review and regression tests keeps the whole pipeline trustworthy.

## Q80: How does termination criteria handle termination for escaped rays - justify your answer with a concrete production example.
**A:** An outer radius wall: once the ray exits the computational domain, termination criteria passes control to the background sky mapping. A concrete example: consistently applying termination criteria in code review and regression tests keeps the whole pipeline trustworthy.

## Q81: What is the recommended first step in implementing termination criteria - justify your answer with a concrete production example.
**A:** Get Euler working on analytic Schwarzschild, then upgrade to RK4 with conserved-quantity drift as the acceptance metric - termination criteria then grows feature by feature. A concrete example: consistently applying termination criteria in code review and regression tests keeps the whole pipeline trustworthy.

## Q82: How does termination criteria ensure the photon sphere region is handled - justify your answer with a concrete production example.
**A:** Tighter adaptive tolerances and more steps there, since orbits near the sphere are the most error-sensitive structures in termination criteria. A concrete example: consistently applying termination criteria in code review and regression tests keeps the whole pipeline trustworthy.

## Q83: What should the interpolation order be for termination criteria - justify your answer with a concrete production example.
**A:** Start bilinear/trilinear; cubic reduces imprinting of the simulation cells but costs more - termination criteria validates visually before investing. A concrete example: consistently applying termination criteria in code review and regression tests keeps the whole pipeline trustworthy.

## Q84: What are the common failure modes of termination criteria - justify your answer with a concrete production example.
**A:** Runaway step growth, step shrink to zero, conserved-quantity drift, and oscillation between grid cells - each has a diagnostic for termination criteria. A concrete example: consistently applying termination criteria in code review and regression tests keeps the whole pipeline trustworthy.

## Q85: How is termination criteria benchmarked on hardware - justify your answer with a concrete production example.
**A:** Steps per second per thread times active threads measures throughput; termination criteria compares integrators under identical scene settings. A concrete example: consistently applying termination criteria in code review and regression tests keeps the whole pipeline trustworthy.

## Q86: What documentation should termination criteria carry - justify your answer with a concrete production example.
**A:** The governing ODEs, step-size policy, tolerance defaults, and the known-good parameter set are the minimum termination criteria documentation. A concrete example: consistently applying termination criteria in code review and regression tests keeps the whole pipeline trustworthy.

## Q87: What documentation should termination criteria carry - justify your answer with a concrete production example.
**A:** The governing ODEs, step-size policy, tolerance defaults, and the known-good parameter set are the minimum termination criteria documentation. A concrete example: consistently applying termination criteria in code review and regression tests keeps the whole pipeline trustworthy.

## Q88: How is termination criteria benchmarked on hardware - justify your answer with a concrete production example.
**A:** Steps per second per thread times active threads measures throughput; termination criteria compares integrators under identical scene settings. A concrete example: consistently applying termination criteria in code review and regression tests keeps the whole pipeline trustworthy.

## Q89: What are the common failure modes of termination criteria - justify your answer with a concrete production example.
**A:** Runaway step growth, step shrink to zero, conserved-quantity drift, and oscillation between grid cells - each has a diagnostic for termination criteria. A concrete example: consistently applying termination criteria in code review and regression tests keeps the whole pipeline trustworthy.

## Q90: What should the interpolation order be for termination criteria - justify your answer with a concrete production example.
**A:** Start bilinear/trilinear; cubic reduces imprinting of the simulation cells but costs more - termination criteria validates visually before investing. A concrete example: consistently applying termination criteria in code review and regression tests keeps the whole pipeline trustworthy.

## Q91: How does termination criteria ensure the photon sphere region is handled - justify your answer with a concrete production example.
**A:** Tighter adaptive tolerances and more steps there, since orbits near the sphere are the most error-sensitive structures in termination criteria. A concrete example: consistently applying termination criteria in code review and regression tests keeps the whole pipeline trustworthy.

## Q92: What is the recommended first step in implementing termination criteria - justify your answer with a concrete production example.
**A:** Get Euler working on analytic Schwarzschild, then upgrade to RK4 with conserved-quantity drift as the acceptance metric - termination criteria then grows feature by feature. A concrete example: consistently applying termination criteria in code review and regression tests keeps the whole pipeline trustworthy.

## Q93: How does termination criteria handle termination for escaped rays - justify your answer with a concrete production example.
**A:** An outer radius wall: once the ray exits the computational domain, termination criteria passes control to the background sky mapping. A concrete example: consistently applying termination criteria in code review and regression tests keeps the whole pipeline trustworthy.

## Q94: What is the cost model for termination criteria - justify your answer with a concrete production example.
**A:** Each step costs a fixed number of metric evaluations; termination criteria budget = evaluations-per-step times steps-per-ray times rays-per-frame. A concrete example: consistently applying termination criteria in code review and regression tests keeps the whole pipeline trustworthy.

## Q95: How do you interpret termination criteria convergence plots - justify your answer with a concrete production example.
**A:** Error versus step size on a log-log plot should follow the scheme's order; a discrepancy in termination criteria signals a bug in the step equations. A concrete example: consistently applying termination criteria in code review and regression tests keeps the whole pipeline trustworthy.

## Q96: What makes termination criteria hard to debug - justify your answer with a concrete production example.
**A:** A single bad step corrupts a whole trajectory; termination criteria debugging isolates by replaying one ray with logging forced on. A concrete example: consistently applying termination criteria in code review and regression tests keeps the whole pipeline trustworthy.

## Q97: How does termination criteria interact with precision - justify your answer with a concrete production example.
**A:** Double precision shrinks accumulated error for long grazing trajectories but halves GPU throughput; termination criteria picks the least precision that passes validation. A concrete example: consistently applying termination criteria in code review and regression tests keeps the whole pipeline trustworthy.

## Q98: What safeguards protect termination criteria from silent NaN - justify your answer with a concrete production example.
**A:** Bounded step sizes, magnitude checks on state, and fail-fast on invalid intermediate values so termination criteria never writes a corrupted frame. A concrete example: consistently applying termination criteria in code review and regression tests keeps the whole pipeline trustworthy.

## Q99: How is termination criteria verified against analytic results - justify your answer with a concrete production example.
**A:** Schwarzschild light deflection, photon orbits, and precession rates have closed forms; termination criteria reproduces them as regression tests. A concrete example: consistently applying termination criteria in code review and regression tests keeps the whole pipeline trustworthy.

## Q100: What limits real-time termination criteria - justify your answer with a concrete production example.
**A:** The integrator cost per ray and rays per frame; termination criteria optimization typically targets the step-evaluation loop which dominates runtime. A concrete example: consistently applying termination criteria in code review and regression tests keeps the whole pipeline trustworthy.
