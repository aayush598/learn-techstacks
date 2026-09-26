# Numerical Methods — Voxel Traversal Interview Questions and Answers

## Q1: What is voxel traversal?
**A:** Efficiently walking a ray through a uniform 3D grid, visiting exactly the cells it passes - used for grid-space ray intersection and AMR sampling.

## Q2: What is the classic algorithm?
**A:** The Amanatides-Woo (DDA-style) marching algorithm: per-axis slab stepping with boundary crossing at exactly one axis per step - O(cells crossed), not O(grid cells).

## Q3: Describe the DDA/Amanatides-Woo traversal.
**A:** From a cube, compute t_next for the next crossing along each axis via tMax update (t_cross = (boundary - pos)/dir), then step to the smallest tMax - a 3-branch loop.

## Q4: What is a 'voxel' in the raytracer?
**A:** A GRMHD grid cell (e.g., uniform in (log r, theta, phi) or physical space cells) holding interpolated field values; the ray samples along it.

## Q5: Why traverse voxels explicitly?
**A:** It gives a FREE ordered list of cells for emission accumulation, cull-by-cell skipping of empty regions, and exact cell-entry/exit for the transfer integral.

## Q6: How does traversal handle the horizon recap?
**A:** Cell-boundary axis touches determine the ray's step endpoints - the capture/disc crossing is detected when a cell face coincides with r = r+ or z = 0.

## Q7: What are empty-cell skips?
**A:** Cells below a density/emissivity threshold are skipped in two of traversal or a per-cell opacity test - real cost saving in the outer vacuum.

## Q8: How is traversal different from stepping the geodesic?
**A:** Geodesic stepping advances in affine parameter (curved path); voxel traversal assumes (nearly) straight segments between adaptive geodesic points.

## Q9: What is the hybrid pattern?
**A:** Adaptive geodesic steps produce a polyline in field space; each geodesic segment is then voxel-traversed for the quadrature - combining both worlds.

## Q10: What is the cost model?
**A:** One cell visit per cell crossed: O(n_cells) work regardless of grid size - a massive win vs brute-force 'check every cell' for large 3D grids.

## Q11: How do you handle the log-r grid in traversal?
**A:** Traversal works in CELL-INDEX space: map each point to (i,j,k), step indexes, and convert back to physical coordinates for field sampling - no metric distortion issues.

## Q12: What are the boundary cases?
**A:** Ray outside the grid (skip/adjust t-entry), ray parallel to an axis (infinite tMax - guard), and empty-cell skips near floors (avoid sub-step ghosting).

## Q13: What validation tests traversal?
**A:** Compare cell-sequence output vs a brute-force 'all cells intersected' check for random rays on a small known grid - sequences must match exactly.

## Q14: How is traversal vectorized?
**A:** Independent rays traverse independently (batch of rays in SIMD lanes); the branch-heavy per-cell loop tolerates warp divergence thanks to short remainder.

## Q15: What is the summary?
**A:** Voxel traversal gives ordered, cheap cell visits along the ray - the efficient bridge between curved geodesics and the gridded GRMHD fields.

## Q16: Why is voxel traversal central to geodesic ray tracing?
**A:** The ray trajectory is the solution of an ODE system; voxel traversal decides how accurately and cheaply that solution is advanced per pixel.

## Q17: What does voxel traversal have to guarantee for correctness?
**A:** Convergence to the analytic geodesic as tolerances shrink and stability across the whole domain - voxel traversal failures appear as image artifacts.

## Q18: How is voxel traversal chosen for a GPU kernel?
**A:** The scheme must be fixed-step or cheaply adaptive, register-light, and deterministic so voxel traversal runs identically on a million parallel threads.

## Q19: What is the typical default integrator for voxel traversal?
**A:** Fourth-order Runge-Kutta for its good accuracy-to-cost ratio, upgraded to embedded RK45 when adaptive error control is needed.

## Q20: How does voxel traversal handle adaptive step sizes?
**A:** Estimate the local error with two approximations (e.g., RK4 vs RK5), halve/double the step, and maintain a tolerance - classic voxel traversal practice.

## Q21: What happens to voxel traversal near singularities?
**A:** Steps must shrink dramatically around coordinate and curvature singularities; voxel traversal avoids runaway cost by terminating captured rays early.

## Q22: How do you compute the interpolation needed by voxel traversal?
**A:** For grid fields, voxel traversal uses multilinear interpolation with the cell coordinates; for analytic metrics none is needed at all.

## Q23: What is the role of the affine parameter in voxel traversal?
**A:** The parameter governs how fast the state evolves; voxel traversal integrates physical time and space the same way, avoiding division-by-zero at turning points.

## Q24: What are the error diagnostics for voxel traversal?
**A:** Per-step local error, drift of conserved quantities, and final-impact parameter; voxel traversal code monitors all three during development.

## Q25: How does voxel traversal achieve determinism?
**A:** Fixed order of operations and epsilon-stable reductions; voxel traversal output is identical across runs and across GPUs when the scheme is fixed.

## Q26: What limits real-time voxel traversal?
**A:** The integrator cost per ray and rays per frame; voxel traversal optimization typically targets the step-evaluation loop which dominates runtime.

## Q27: How is voxel traversal verified against analytic results?
**A:** Schwarzschild light deflection, photon orbits, and precession rates have closed forms; voxel traversal reproduces them as regression tests.

## Q28: What safeguards protect voxel traversal from silent NaN?
**A:** Bounded step sizes, magnitude checks on state, and fail-fast on invalid intermediate values so voxel traversal never writes a corrupted frame.

## Q29: How does voxel traversal interact with precision?
**A:** Double precision shrinks accumulated error for long grazing trajectories but halves GPU throughput; voxel traversal picks the least precision that passes validation.

## Q30: What makes voxel traversal hard to debug?
**A:** A single bad step corrupts a whole trajectory; voxel traversal debugging isolates by replaying one ray with logging forced on.

## Q31: How do you interpret voxel traversal convergence plots?
**A:** Error versus step size on a log-log plot should follow the scheme's order; a discrepancy in voxel traversal signals a bug in the step equations.

## Q32: What is the cost model for voxel traversal?
**A:** Each step costs a fixed number of metric evaluations; voxel traversal budget = evaluations-per-step times steps-per-ray times rays-per-frame.

## Q33: How does voxel traversal handle termination for escaped rays?
**A:** An outer radius wall: once the ray exits the computational domain, voxel traversal passes control to the background sky mapping.

## Q34: What is the recommended first step in implementing voxel traversal?
**A:** Get Euler working on analytic Schwarzschild, then upgrade to RK4 with conserved-quantity drift as the acceptance metric - voxel traversal then grows feature by feature.

## Q35: How does voxel traversal ensure the photon sphere region is handled?
**A:** Tighter adaptive tolerances and more steps there, since orbits near the sphere are the most error-sensitive structures in voxel traversal.

## Q36: What should the interpolation order be for voxel traversal?
**A:** Start bilinear/trilinear; cubic reduces imprinting of the simulation cells but costs more - voxel traversal validates visually before investing.

## Q37: What are the common failure modes of voxel traversal?
**A:** Runaway step growth, step shrink to zero, conserved-quantity drift, and oscillation between grid cells - each has a diagnostic for voxel traversal.

## Q38: How is voxel traversal benchmarked on hardware?
**A:** Steps per second per thread times active threads measures throughput; voxel traversal compares integrators under identical scene settings.

## Q39: What documentation should voxel traversal carry?
**A:** The governing ODEs, step-size policy, tolerance defaults, and the known-good parameter set are the minimum voxel traversal documentation.

## Q40: What documentation should voxel traversal carry - justify your answer with a concrete production example.
**A:** The governing ODEs, step-size policy, tolerance defaults, and the known-good parameter set are the minimum voxel traversal documentation. A concrete example: consistently applying voxel traversal in code review and regression tests keeps the whole pipeline trustworthy.

## Q41: How is voxel traversal benchmarked on hardware - justify your answer with a concrete production example.
**A:** Steps per second per thread times active threads measures throughput; voxel traversal compares integrators under identical scene settings. A concrete example: consistently applying voxel traversal in code review and regression tests keeps the whole pipeline trustworthy.

## Q42: What are the common failure modes of voxel traversal - justify your answer with a concrete production example.
**A:** Runaway step growth, step shrink to zero, conserved-quantity drift, and oscillation between grid cells - each has a diagnostic for voxel traversal. A concrete example: consistently applying voxel traversal in code review and regression tests keeps the whole pipeline trustworthy.

## Q43: What should the interpolation order be for voxel traversal - justify your answer with a concrete production example.
**A:** Start bilinear/trilinear; cubic reduces imprinting of the simulation cells but costs more - voxel traversal validates visually before investing. A concrete example: consistently applying voxel traversal in code review and regression tests keeps the whole pipeline trustworthy.

## Q44: How does voxel traversal ensure the photon sphere region is handled - justify your answer with a concrete production example.
**A:** Tighter adaptive tolerances and more steps there, since orbits near the sphere are the most error-sensitive structures in voxel traversal. A concrete example: consistently applying voxel traversal in code review and regression tests keeps the whole pipeline trustworthy.

## Q45: What is the recommended first step in implementing voxel traversal - justify your answer with a concrete production example.
**A:** Get Euler working on analytic Schwarzschild, then upgrade to RK4 with conserved-quantity drift as the acceptance metric - voxel traversal then grows feature by feature. A concrete example: consistently applying voxel traversal in code review and regression tests keeps the whole pipeline trustworthy.

## Q46: How does voxel traversal handle termination for escaped rays - justify your answer with a concrete production example.
**A:** An outer radius wall: once the ray exits the computational domain, voxel traversal passes control to the background sky mapping. A concrete example: consistently applying voxel traversal in code review and regression tests keeps the whole pipeline trustworthy.

## Q47: What is the cost model for voxel traversal - justify your answer with a concrete production example.
**A:** Each step costs a fixed number of metric evaluations; voxel traversal budget = evaluations-per-step times steps-per-ray times rays-per-frame. A concrete example: consistently applying voxel traversal in code review and regression tests keeps the whole pipeline trustworthy.

## Q48: How do you interpret voxel traversal convergence plots - justify your answer with a concrete production example.
**A:** Error versus step size on a log-log plot should follow the scheme's order; a discrepancy in voxel traversal signals a bug in the step equations. A concrete example: consistently applying voxel traversal in code review and regression tests keeps the whole pipeline trustworthy.

## Q49: What makes voxel traversal hard to debug - justify your answer with a concrete production example.
**A:** A single bad step corrupts a whole trajectory; voxel traversal debugging isolates by replaying one ray with logging forced on. A concrete example: consistently applying voxel traversal in code review and regression tests keeps the whole pipeline trustworthy.

## Q50: How does voxel traversal interact with precision - justify your answer with a concrete production example.
**A:** Double precision shrinks accumulated error for long grazing trajectories but halves GPU throughput; voxel traversal picks the least precision that passes validation. A concrete example: consistently applying voxel traversal in code review and regression tests keeps the whole pipeline trustworthy.

## Q51: What safeguards protect voxel traversal from silent NaN - justify your answer with a concrete production example.
**A:** Bounded step sizes, magnitude checks on state, and fail-fast on invalid intermediate values so voxel traversal never writes a corrupted frame. A concrete example: consistently applying voxel traversal in code review and regression tests keeps the whole pipeline trustworthy.

## Q52: How is voxel traversal verified against analytic results - justify your answer with a concrete production example.
**A:** Schwarzschild light deflection, photon orbits, and precession rates have closed forms; voxel traversal reproduces them as regression tests. A concrete example: consistently applying voxel traversal in code review and regression tests keeps the whole pipeline trustworthy.

## Q53: What limits real-time voxel traversal - justify your answer with a concrete production example.
**A:** The integrator cost per ray and rays per frame; voxel traversal optimization typically targets the step-evaluation loop which dominates runtime. A concrete example: consistently applying voxel traversal in code review and regression tests keeps the whole pipeline trustworthy.

## Q54: How does voxel traversal achieve determinism - justify your answer with a concrete production example.
**A:** Fixed order of operations and epsilon-stable reductions; voxel traversal output is identical across runs and across GPUs when the scheme is fixed. A concrete example: consistently applying voxel traversal in code review and regression tests keeps the whole pipeline trustworthy.

## Q55: What are the error diagnostics for voxel traversal - justify your answer with a concrete production example.
**A:** Per-step local error, drift of conserved quantities, and final-impact parameter; voxel traversal code monitors all three during development. A concrete example: consistently applying voxel traversal in code review and regression tests keeps the whole pipeline trustworthy.

## Q56: What is the role of the affine parameter in voxel traversal - justify your answer with a concrete production example.
**A:** The parameter governs how fast the state evolves; voxel traversal integrates physical time and space the same way, avoiding division-by-zero at turning points. A concrete example: consistently applying voxel traversal in code review and regression tests keeps the whole pipeline trustworthy.

## Q57: How do you compute the interpolation needed by voxel traversal - justify your answer with a concrete production example.
**A:** For grid fields, voxel traversal uses multilinear interpolation with the cell coordinates; for analytic metrics none is needed at all. A concrete example: consistently applying voxel traversal in code review and regression tests keeps the whole pipeline trustworthy.

## Q58: What happens to voxel traversal near singularities - justify your answer with a concrete production example.
**A:** Steps must shrink dramatically around coordinate and curvature singularities; voxel traversal avoids runaway cost by terminating captured rays early. A concrete example: consistently applying voxel traversal in code review and regression tests keeps the whole pipeline trustworthy.

## Q59: How does voxel traversal handle adaptive step sizes - justify your answer with a concrete production example.
**A:** Estimate the local error with two approximations (e.g., RK4 vs RK5), halve/double the step, and maintain a tolerance - classic voxel traversal practice. A concrete example: consistently applying voxel traversal in code review and regression tests keeps the whole pipeline trustworthy.

## Q60: What is the typical default integrator for voxel traversal - justify your answer with a concrete production example.
**A:** Fourth-order Runge-Kutta for its good accuracy-to-cost ratio, upgraded to embedded RK45 when adaptive error control is needed. A concrete example: consistently applying voxel traversal in code review and regression tests keeps the whole pipeline trustworthy.

## Q61: How is voxel traversal chosen for a GPU kernel - justify your answer with a concrete production example.
**A:** The scheme must be fixed-step or cheaply adaptive, register-light, and deterministic so voxel traversal runs identically on a million parallel threads. A concrete example: consistently applying voxel traversal in code review and regression tests keeps the whole pipeline trustworthy.

## Q62: What does voxel traversal have to guarantee for correctness - justify your answer with a concrete production example.
**A:** Convergence to the analytic geodesic as tolerances shrink and stability across the whole domain - voxel traversal failures appear as image artifacts. A concrete example: consistently applying voxel traversal in code review and regression tests keeps the whole pipeline trustworthy.

## Q63: Why is voxel traversal central to geodesic ray tracing - justify your answer with a concrete production example.
**A:** The ray trajectory is the solution of an ODE system; voxel traversal decides how accurately and cheaply that solution is advanced per pixel. A concrete example: consistently applying voxel traversal in code review and regression tests keeps the whole pipeline trustworthy.

## Q64: Why is voxel traversal central to geodesic ray tracing - justify your answer with a concrete production example.
**A:** The ray trajectory is the solution of an ODE system; voxel traversal decides how accurately and cheaply that solution is advanced per pixel. A concrete example: consistently applying voxel traversal in code review and regression tests keeps the whole pipeline trustworthy.

## Q65: What does voxel traversal have to guarantee for correctness - justify your answer with a concrete production example.
**A:** Convergence to the analytic geodesic as tolerances shrink and stability across the whole domain - voxel traversal failures appear as image artifacts. A concrete example: consistently applying voxel traversal in code review and regression tests keeps the whole pipeline trustworthy.

## Q66: How is voxel traversal chosen for a GPU kernel - justify your answer with a concrete production example.
**A:** The scheme must be fixed-step or cheaply adaptive, register-light, and deterministic so voxel traversal runs identically on a million parallel threads. A concrete example: consistently applying voxel traversal in code review and regression tests keeps the whole pipeline trustworthy.

## Q67: What is the typical default integrator for voxel traversal - justify your answer with a concrete production example.
**A:** Fourth-order Runge-Kutta for its good accuracy-to-cost ratio, upgraded to embedded RK45 when adaptive error control is needed. A concrete example: consistently applying voxel traversal in code review and regression tests keeps the whole pipeline trustworthy.

## Q68: How does voxel traversal handle adaptive step sizes - justify your answer with a concrete production example.
**A:** Estimate the local error with two approximations (e.g., RK4 vs RK5), halve/double the step, and maintain a tolerance - classic voxel traversal practice. A concrete example: consistently applying voxel traversal in code review and regression tests keeps the whole pipeline trustworthy.

## Q69: What happens to voxel traversal near singularities - justify your answer with a concrete production example.
**A:** Steps must shrink dramatically around coordinate and curvature singularities; voxel traversal avoids runaway cost by terminating captured rays early. A concrete example: consistently applying voxel traversal in code review and regression tests keeps the whole pipeline trustworthy.

## Q70: How do you compute the interpolation needed by voxel traversal - justify your answer with a concrete production example.
**A:** For grid fields, voxel traversal uses multilinear interpolation with the cell coordinates; for analytic metrics none is needed at all. A concrete example: consistently applying voxel traversal in code review and regression tests keeps the whole pipeline trustworthy.

## Q71: What is the role of the affine parameter in voxel traversal - justify your answer with a concrete production example.
**A:** The parameter governs how fast the state evolves; voxel traversal integrates physical time and space the same way, avoiding division-by-zero at turning points. A concrete example: consistently applying voxel traversal in code review and regression tests keeps the whole pipeline trustworthy.

## Q72: What are the error diagnostics for voxel traversal - justify your answer with a concrete production example.
**A:** Per-step local error, drift of conserved quantities, and final-impact parameter; voxel traversal code monitors all three during development. A concrete example: consistently applying voxel traversal in code review and regression tests keeps the whole pipeline trustworthy.

## Q73: How does voxel traversal achieve determinism - justify your answer with a concrete production example.
**A:** Fixed order of operations and epsilon-stable reductions; voxel traversal output is identical across runs and across GPUs when the scheme is fixed. A concrete example: consistently applying voxel traversal in code review and regression tests keeps the whole pipeline trustworthy.

## Q74: What limits real-time voxel traversal - justify your answer with a concrete production example.
**A:** The integrator cost per ray and rays per frame; voxel traversal optimization typically targets the step-evaluation loop which dominates runtime. A concrete example: consistently applying voxel traversal in code review and regression tests keeps the whole pipeline trustworthy.

## Q75: How is voxel traversal verified against analytic results - justify your answer with a concrete production example.
**A:** Schwarzschild light deflection, photon orbits, and precession rates have closed forms; voxel traversal reproduces them as regression tests. A concrete example: consistently applying voxel traversal in code review and regression tests keeps the whole pipeline trustworthy.

## Q76: What safeguards protect voxel traversal from silent NaN - justify your answer with a concrete production example.
**A:** Bounded step sizes, magnitude checks on state, and fail-fast on invalid intermediate values so voxel traversal never writes a corrupted frame. A concrete example: consistently applying voxel traversal in code review and regression tests keeps the whole pipeline trustworthy.

## Q77: How does voxel traversal interact with precision - justify your answer with a concrete production example.
**A:** Double precision shrinks accumulated error for long grazing trajectories but halves GPU throughput; voxel traversal picks the least precision that passes validation. A concrete example: consistently applying voxel traversal in code review and regression tests keeps the whole pipeline trustworthy.

## Q78: What makes voxel traversal hard to debug - justify your answer with a concrete production example.
**A:** A single bad step corrupts a whole trajectory; voxel traversal debugging isolates by replaying one ray with logging forced on. A concrete example: consistently applying voxel traversal in code review and regression tests keeps the whole pipeline trustworthy.

## Q79: How do you interpret voxel traversal convergence plots - justify your answer with a concrete production example.
**A:** Error versus step size on a log-log plot should follow the scheme's order; a discrepancy in voxel traversal signals a bug in the step equations. A concrete example: consistently applying voxel traversal in code review and regression tests keeps the whole pipeline trustworthy.

## Q80: What is the cost model for voxel traversal - justify your answer with a concrete production example.
**A:** Each step costs a fixed number of metric evaluations; voxel traversal budget = evaluations-per-step times steps-per-ray times rays-per-frame. A concrete example: consistently applying voxel traversal in code review and regression tests keeps the whole pipeline trustworthy.

## Q81: How does voxel traversal handle termination for escaped rays - justify your answer with a concrete production example.
**A:** An outer radius wall: once the ray exits the computational domain, voxel traversal passes control to the background sky mapping. A concrete example: consistently applying voxel traversal in code review and regression tests keeps the whole pipeline trustworthy.

## Q82: What is the recommended first step in implementing voxel traversal - justify your answer with a concrete production example.
**A:** Get Euler working on analytic Schwarzschild, then upgrade to RK4 with conserved-quantity drift as the acceptance metric - voxel traversal then grows feature by feature. A concrete example: consistently applying voxel traversal in code review and regression tests keeps the whole pipeline trustworthy.

## Q83: How does voxel traversal ensure the photon sphere region is handled - justify your answer with a concrete production example.
**A:** Tighter adaptive tolerances and more steps there, since orbits near the sphere are the most error-sensitive structures in voxel traversal. A concrete example: consistently applying voxel traversal in code review and regression tests keeps the whole pipeline trustworthy.

## Q84: What should the interpolation order be for voxel traversal - justify your answer with a concrete production example.
**A:** Start bilinear/trilinear; cubic reduces imprinting of the simulation cells but costs more - voxel traversal validates visually before investing. A concrete example: consistently applying voxel traversal in code review and regression tests keeps the whole pipeline trustworthy.

## Q85: What are the common failure modes of voxel traversal - justify your answer with a concrete production example.
**A:** Runaway step growth, step shrink to zero, conserved-quantity drift, and oscillation between grid cells - each has a diagnostic for voxel traversal. A concrete example: consistently applying voxel traversal in code review and regression tests keeps the whole pipeline trustworthy.

## Q86: How is voxel traversal benchmarked on hardware - justify your answer with a concrete production example.
**A:** Steps per second per thread times active threads measures throughput; voxel traversal compares integrators under identical scene settings. A concrete example: consistently applying voxel traversal in code review and regression tests keeps the whole pipeline trustworthy.

## Q87: What documentation should voxel traversal carry - justify your answer with a concrete production example.
**A:** The governing ODEs, step-size policy, tolerance defaults, and the known-good parameter set are the minimum voxel traversal documentation. A concrete example: consistently applying voxel traversal in code review and regression tests keeps the whole pipeline trustworthy.

## Q88: What documentation should voxel traversal carry - justify your answer with a concrete production example.
**A:** The governing ODEs, step-size policy, tolerance defaults, and the known-good parameter set are the minimum voxel traversal documentation. A concrete example: consistently applying voxel traversal in code review and regression tests keeps the whole pipeline trustworthy.

## Q89: How is voxel traversal benchmarked on hardware - justify your answer with a concrete production example.
**A:** Steps per second per thread times active threads measures throughput; voxel traversal compares integrators under identical scene settings. A concrete example: consistently applying voxel traversal in code review and regression tests keeps the whole pipeline trustworthy.

## Q90: What are the common failure modes of voxel traversal - justify your answer with a concrete production example.
**A:** Runaway step growth, step shrink to zero, conserved-quantity drift, and oscillation between grid cells - each has a diagnostic for voxel traversal. A concrete example: consistently applying voxel traversal in code review and regression tests keeps the whole pipeline trustworthy.

## Q91: What should the interpolation order be for voxel traversal - justify your answer with a concrete production example.
**A:** Start bilinear/trilinear; cubic reduces imprinting of the simulation cells but costs more - voxel traversal validates visually before investing. A concrete example: consistently applying voxel traversal in code review and regression tests keeps the whole pipeline trustworthy.

## Q92: How does voxel traversal ensure the photon sphere region is handled - justify your answer with a concrete production example.
**A:** Tighter adaptive tolerances and more steps there, since orbits near the sphere are the most error-sensitive structures in voxel traversal. A concrete example: consistently applying voxel traversal in code review and regression tests keeps the whole pipeline trustworthy.

## Q93: What is the recommended first step in implementing voxel traversal - justify your answer with a concrete production example.
**A:** Get Euler working on analytic Schwarzschild, then upgrade to RK4 with conserved-quantity drift as the acceptance metric - voxel traversal then grows feature by feature. A concrete example: consistently applying voxel traversal in code review and regression tests keeps the whole pipeline trustworthy.

## Q94: How does voxel traversal handle termination for escaped rays - justify your answer with a concrete production example.
**A:** An outer radius wall: once the ray exits the computational domain, voxel traversal passes control to the background sky mapping. A concrete example: consistently applying voxel traversal in code review and regression tests keeps the whole pipeline trustworthy.

## Q95: What is the cost model for voxel traversal - justify your answer with a concrete production example.
**A:** Each step costs a fixed number of metric evaluations; voxel traversal budget = evaluations-per-step times steps-per-ray times rays-per-frame. A concrete example: consistently applying voxel traversal in code review and regression tests keeps the whole pipeline trustworthy.

## Q96: How do you interpret voxel traversal convergence plots - justify your answer with a concrete production example.
**A:** Error versus step size on a log-log plot should follow the scheme's order; a discrepancy in voxel traversal signals a bug in the step equations. A concrete example: consistently applying voxel traversal in code review and regression tests keeps the whole pipeline trustworthy.

## Q97: What makes voxel traversal hard to debug - justify your answer with a concrete production example.
**A:** A single bad step corrupts a whole trajectory; voxel traversal debugging isolates by replaying one ray with logging forced on. A concrete example: consistently applying voxel traversal in code review and regression tests keeps the whole pipeline trustworthy.

## Q98: How does voxel traversal interact with precision - justify your answer with a concrete production example.
**A:** Double precision shrinks accumulated error for long grazing trajectories but halves GPU throughput; voxel traversal picks the least precision that passes validation. A concrete example: consistently applying voxel traversal in code review and regression tests keeps the whole pipeline trustworthy.

## Q99: What safeguards protect voxel traversal from silent NaN - justify your answer with a concrete production example.
**A:** Bounded step sizes, magnitude checks on state, and fail-fast on invalid intermediate values so voxel traversal never writes a corrupted frame. A concrete example: consistently applying voxel traversal in code review and regression tests keeps the whole pipeline trustworthy.

## Q100: How is voxel traversal verified against analytic results - justify your answer with a concrete production example.
**A:** Schwarzschild light deflection, photon orbits, and precession rates have closed forms; voxel traversal reproduces them as regression tests. A concrete example: consistently applying voxel traversal in code review and regression tests keeps the whole pipeline trustworthy.
