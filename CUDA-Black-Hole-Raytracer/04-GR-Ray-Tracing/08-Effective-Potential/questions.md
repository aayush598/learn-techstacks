# Gr Ray Tracing — Effective Potential Interview Questions and Answers

## Q1: What is the effective potential for radial motion?
**A:** For fixed (E, L, Q) the null condition reduces to rdot^2 = V_r(r); the allowed radial range is where V_r >= 0 - the potential determines the orbit's envelope.

## Q2: What is V_r for Kerr (Boyer-Lindquist)?
**A:** The full expression containing Delta and Sigma splits into a rational form; its boundary V_r=0 and critical points drive turning points and circular orbits.

## Q3: What is the effective potential for the theta motion?
**A:** The companion theta-potential fixes cottheta^2 bounds from Q; theta-motion is normalizable given Q in a bounded interval.

## Q4: What are turning points?
**A:** Radii where V_r = 0 (rdot=0) - the closest-approach r0 and possibly an outer bound; the ray bounces between these extremes.

## Q5: What is a circular (photon) orbit?
**A:** Where V_r has a critical point (V_r = V_r' = 0): a degenerate root - the photon sphere for given (E, Q, a), unstable in radial direction.

## Q6: How does the potential encode capture?
**A:** If no turning point exists for r > r+ consistent with V_r >= 0, the ray plunges to the horizon - capture is precisely 'no outgoing turning point'.

## Q7: How do you compute the shadow from the potential?
**A:** Scan the image plane (b, gamma); for each, solve V_r for turning points; those lacking escaping turning points fall in the shadow.

## Q8: What is the photon-sphere equation from the potential?
**A:** The double root condition V_r(r) = V_r'(r) = 0 yields r_ph and the critical b_ph - the hidden benefit of potential analysis.

## Q9: What does the potential say about multiple images?
**A:** Nested turning-point structures give multiple radial extrema - the source of the rays that wrap several layers of image.

## Q10: How is the potential used to seed the integrator?
**A:** Initial rdot computed from V_r directly; turning points predicted analytically so the integrator passes smoothly through r0 without sign flips.

## Q11: What is a wavefront/family sweep in potential language?
**A:** For fixed E, scanning L traces the potential family; the shadow boundary is where the potential maxima equal the incoming b - the nude surface.

## Q12: How do you validate the potential?
**A:** Move particles r flat: integrate and assert rdot from V_r matches the integration's own rdot; at photon sphere, V=0 with V'=0 reproduces r_ph=3M (a=0).

## Q13: What is the energy vs impact parameter relation?
**A:** Scaled by E, everything depends on b and the polar angle gamma (via Q), so V_r is effectively a two-parameter family - the lens map's territory.

## Q14: What caution about units?
**A:** Potential formulas assume geometric units; mixing in G/c yields absolute turns - code keeps the pure M=1 forms and scales radii at I/O only.

## Q15: Why is the potential the right mental model?
**A:** It reduces the black hole's lensing to 1-D classical mechanics - the intuition of hills/valleys that makes capture, rings, and shadow all feel immediate.

## Q16: What does effective potential concretely do inside the raytracer?
**A:** It advances photon trajectories in the curved spacetime, applying the equations of motion so each camera ray follows a true null geodesic.

## Q17: Why is effective potential the heart of a black-hole visualizer?
**A:** Every visual signature - lensing, photon ring, shadow, redshift - emerges from exactly how effective potential bends and time-shifts each ray.

## Q18: How is effective potential implemented on the GPU?
**A:** As a numerical integration loop in device code with per-ray state in registers, stepping through effective potential until the ray is captured or escapes.

## Q19: What are the two families of integration for effective potential?
**A:** The direct geodesic integration of the equations of motion, and Hamilton-Jacobi reduced systems using conserved constants; effective potential chooses per codebase.

## Q20: How do you validate effective potential?
**A:** Reproduce the analytic Schwarzschild lensing angle, the photon ring, and the projected shadow shape measured against published figures.

## Q21: What is the typical step-size strategy in effective potential?
**A:** Adaptive stepping that refines near the photon sphere and the horizon, where effective potential gradients are steepest and error grows fastest.

## Q22: What state does the integrator track for effective potential?
**A:** Position, four-momentum components, affine parameter, and accumulated redshift - effective potential state vector is small enough to fit in registers.

## Q23: How does effective potential handle captured photons?
**A:** It terminates integration at the horizon and records absorption; effective potential distinguishes capture from scatter by the radial turning point.

## Q24: What role do conserved constants play in effective potential?
**A:** They let you solve impact parameters analytically or prune impossible trajectories, dramatically speeding effective potential for large image grids.

## Q25: Describe the numerical error budget of effective potential.
**A:** Per-step truncation error and accumulated drift; effective potential budgets a relative tolerance and verifies the final image is stable.

## Q26: How does effective potential map the sky to the image plane?
**A:** Each image pixel defines an initial direction; effective potential evolves that direction backward in time until it leaves the domain to a background sky or hits the disk.

## Q27: What is the most common bug in effective potential?
**A:** A sign error in the equations of motion or a wrong coordinate transformation that produces plausible-but-wrong lensing; effective potential needs golden-image regression tests.

## Q28: How do you parallelize effective potential?
**A:** Every pixel is an independent effective potential problem, so one thread per ray gives embarrassingly parallel behavior with no inter-thread communication.

## Q29: What determines the visual shadow size in effective potential?
**A:** The photon sphere and horizon geometry: captured rays draw the shadow whose boundary in effective potential is the photon ring.

## Q30: When do you need full Kerr effective potential instead of Schwarzschild?
**A:** Whenever the disk's rotation and frame dragging matter - most real astrophysical images; effective potential must support spin to be credible.

## Q31: What is the 'second/third image' vocabulary of effective potential?
**A:** Light winding around the black hole produces multiple images; effective potential naturally produces the primary, secondary, and higher-order photon ring.

## Q32: How does effective potential produce the bright thin ring?
**A:** Rays that graze the photon sphere travel long path lengths through the brightest disk region, so averaged intensity peaks at the effective potential critical impact parameter.

## Q33: How does effective potential decide frequencies for render?
**A:** It integrates the redshift factor along the ray; effective potential multiplies emitted frequency by it before applying the transfer equation.

## Q34: What modes does effective potential render the accretion disk?
**A:** First as a geometric emitter grid, later using GRMHD data; effective potential is agnostic to the source as long as it can query emissivity along the path.

## Q35: How is effective potential performance quantified?
**A:** Mega-rays per second and time per frame; effective potential usually spends its budget in the integration loop, so its step count is the key metric.

## Q36: What is the effect of camera position in effective potential?
**A:** Face-on, edge-on, and plunging camera setups change the projected ring shape; effective potential validates each against known renders.

## Q37: How does effective potential incorporate the disk's fluid velocity?
**A:** Doppler and beaming appear when the emissivity frame is boosted; effective potential applies that boost per photon ray path segment.

## Q38: What is the horizon-catching strategy in effective potential?
**A:** Rather than refine forever, you flag a ray as captured once r drops below the horizon radius; effective potential then terminates that lane.

## Q39: How should you commission effective potential output?
**A:** Side-by-side with published stills of the same metric and camera to confirm lensing, ring, and shadow match within a few percent.

## Q40: How should you commission effective potential output - justify your answer with a concrete production example.
**A:** Side-by-side with published stills of the same metric and camera to confirm lensing, ring, and shadow match within a few percent. A concrete example: consistently applying effective potential in code review and regression tests keeps the whole pipeline trustworthy.

## Q41: What is the horizon-catching strategy in effective potential - justify your answer with a concrete production example.
**A:** Rather than refine forever, you flag a ray as captured once r drops below the horizon radius; effective potential then terminates that lane. A concrete example: consistently applying effective potential in code review and regression tests keeps the whole pipeline trustworthy.

## Q42: How does effective potential incorporate the disk's fluid velocity - justify your answer with a concrete production example.
**A:** Doppler and beaming appear when the emissivity frame is boosted; effective potential applies that boost per photon ray path segment. A concrete example: consistently applying effective potential in code review and regression tests keeps the whole pipeline trustworthy.

## Q43: What is the effect of camera position in effective potential - justify your answer with a concrete production example.
**A:** Face-on, edge-on, and plunging camera setups change the projected ring shape; effective potential validates each against known renders. A concrete example: consistently applying effective potential in code review and regression tests keeps the whole pipeline trustworthy.

## Q44: How is effective potential performance quantified - justify your answer with a concrete production example.
**A:** Mega-rays per second and time per frame; effective potential usually spends its budget in the integration loop, so its step count is the key metric. A concrete example: consistently applying effective potential in code review and regression tests keeps the whole pipeline trustworthy.

## Q45: What modes does effective potential render the accretion disk - justify your answer with a concrete production example.
**A:** First as a geometric emitter grid, later using GRMHD data; effective potential is agnostic to the source as long as it can query emissivity along the path. A concrete example: consistently applying effective potential in code review and regression tests keeps the whole pipeline trustworthy.

## Q46: How does effective potential decide frequencies for render - justify your answer with a concrete production example.
**A:** It integrates the redshift factor along the ray; effective potential multiplies emitted frequency by it before applying the transfer equation. A concrete example: consistently applying effective potential in code review and regression tests keeps the whole pipeline trustworthy.

## Q47: How does effective potential produce the bright thin ring - justify your answer with a concrete production example.
**A:** Rays that graze the photon sphere travel long path lengths through the brightest disk region, so averaged intensity peaks at the effective potential critical impact parameter. A concrete example: consistently applying effective potential in code review and regression tests keeps the whole pipeline trustworthy.

## Q48: What is the 'second/third image' vocabulary of effective potential - justify your answer with a concrete production example.
**A:** Light winding around the black hole produces multiple images; effective potential naturally produces the primary, secondary, and higher-order photon ring. A concrete example: consistently applying effective potential in code review and regression tests keeps the whole pipeline trustworthy.

## Q49: When do you need full Kerr effective potential instead of Schwarzschild - justify your answer with a concrete production example.
**A:** Whenever the disk's rotation and frame dragging matter - most real astrophysical images; effective potential must support spin to be credible. A concrete example: consistently applying effective potential in code review and regression tests keeps the whole pipeline trustworthy.

## Q50: What determines the visual shadow size in effective potential - justify your answer with a concrete production example.
**A:** The photon sphere and horizon geometry: captured rays draw the shadow whose boundary in effective potential is the photon ring. A concrete example: consistently applying effective potential in code review and regression tests keeps the whole pipeline trustworthy.

## Q51: How do you parallelize effective potential - justify your answer with a concrete production example.
**A:** Every pixel is an independent effective potential problem, so one thread per ray gives embarrassingly parallel behavior with no inter-thread communication. A concrete example: consistently applying effective potential in code review and regression tests keeps the whole pipeline trustworthy.

## Q52: What is the most common bug in effective potential - justify your answer with a concrete production example.
**A:** A sign error in the equations of motion or a wrong coordinate transformation that produces plausible-but-wrong lensing; effective potential needs golden-image regression tests. A concrete example: consistently applying effective potential in code review and regression tests keeps the whole pipeline trustworthy.

## Q53: How does effective potential map the sky to the image plane - justify your answer with a concrete production example.
**A:** Each image pixel defines an initial direction; effective potential evolves that direction backward in time until it leaves the domain to a background sky or hits the disk. A concrete example: consistently applying effective potential in code review and regression tests keeps the whole pipeline trustworthy.

## Q54: Describe the numerical error budget of effective potential - justify your answer with a concrete production example.
**A:** Per-step truncation error and accumulated drift; effective potential budgets a relative tolerance and verifies the final image is stable. A concrete example: consistently applying effective potential in code review and regression tests keeps the whole pipeline trustworthy.

## Q55: What role do conserved constants play in effective potential - justify your answer with a concrete production example.
**A:** They let you solve impact parameters analytically or prune impossible trajectories, dramatically speeding effective potential for large image grids. A concrete example: consistently applying effective potential in code review and regression tests keeps the whole pipeline trustworthy.

## Q56: How does effective potential handle captured photons - justify your answer with a concrete production example.
**A:** It terminates integration at the horizon and records absorption; effective potential distinguishes capture from scatter by the radial turning point. A concrete example: consistently applying effective potential in code review and regression tests keeps the whole pipeline trustworthy.

## Q57: What state does the integrator track for effective potential - justify your answer with a concrete production example.
**A:** Position, four-momentum components, affine parameter, and accumulated redshift - effective potential state vector is small enough to fit in registers. A concrete example: consistently applying effective potential in code review and regression tests keeps the whole pipeline trustworthy.

## Q58: What is the typical step-size strategy in effective potential - justify your answer with a concrete production example.
**A:** Adaptive stepping that refines near the photon sphere and the horizon, where effective potential gradients are steepest and error grows fastest. A concrete example: consistently applying effective potential in code review and regression tests keeps the whole pipeline trustworthy.

## Q59: How do you validate effective potential - justify your answer with a concrete production example.
**A:** Reproduce the analytic Schwarzschild lensing angle, the photon ring, and the projected shadow shape measured against published figures. A concrete example: consistently applying effective potential in code review and regression tests keeps the whole pipeline trustworthy.

## Q60: What are the two families of integration for effective potential - justify your answer with a concrete production example.
**A:** The direct geodesic integration of the equations of motion, and Hamilton-Jacobi reduced systems using conserved constants; effective potential chooses per codebase. A concrete example: consistently applying effective potential in code review and regression tests keeps the whole pipeline trustworthy.

## Q61: How is effective potential implemented on the GPU - justify your answer with a concrete production example.
**A:** As a numerical integration loop in device code with per-ray state in registers, stepping through effective potential until the ray is captured or escapes. A concrete example: consistently applying effective potential in code review and regression tests keeps the whole pipeline trustworthy.

## Q62: Why is effective potential the heart of a black-hole visualizer - justify your answer with a concrete production example.
**A:** Every visual signature - lensing, photon ring, shadow, redshift - emerges from exactly how effective potential bends and time-shifts each ray. A concrete example: consistently applying effective potential in code review and regression tests keeps the whole pipeline trustworthy.

## Q63: What does effective potential concretely do inside the raytracer - justify your answer with a concrete production example.
**A:** It advances photon trajectories in the curved spacetime, applying the equations of motion so each camera ray follows a true null geodesic. A concrete example: consistently applying effective potential in code review and regression tests keeps the whole pipeline trustworthy.

## Q64: What does effective potential concretely do inside the raytracer - justify your answer with a concrete production example.
**A:** It advances photon trajectories in the curved spacetime, applying the equations of motion so each camera ray follows a true null geodesic. A concrete example: consistently applying effective potential in code review and regression tests keeps the whole pipeline trustworthy.

## Q65: Why is effective potential the heart of a black-hole visualizer - justify your answer with a concrete production example.
**A:** Every visual signature - lensing, photon ring, shadow, redshift - emerges from exactly how effective potential bends and time-shifts each ray. A concrete example: consistently applying effective potential in code review and regression tests keeps the whole pipeline trustworthy.

## Q66: How is effective potential implemented on the GPU - justify your answer with a concrete production example.
**A:** As a numerical integration loop in device code with per-ray state in registers, stepping through effective potential until the ray is captured or escapes. A concrete example: consistently applying effective potential in code review and regression tests keeps the whole pipeline trustworthy.

## Q67: What are the two families of integration for effective potential - justify your answer with a concrete production example.
**A:** The direct geodesic integration of the equations of motion, and Hamilton-Jacobi reduced systems using conserved constants; effective potential chooses per codebase. A concrete example: consistently applying effective potential in code review and regression tests keeps the whole pipeline trustworthy.

## Q68: How do you validate effective potential - justify your answer with a concrete production example.
**A:** Reproduce the analytic Schwarzschild lensing angle, the photon ring, and the projected shadow shape measured against published figures. A concrete example: consistently applying effective potential in code review and regression tests keeps the whole pipeline trustworthy.

## Q69: What is the typical step-size strategy in effective potential - justify your answer with a concrete production example.
**A:** Adaptive stepping that refines near the photon sphere and the horizon, where effective potential gradients are steepest and error grows fastest. A concrete example: consistently applying effective potential in code review and regression tests keeps the whole pipeline trustworthy.

## Q70: What state does the integrator track for effective potential - justify your answer with a concrete production example.
**A:** Position, four-momentum components, affine parameter, and accumulated redshift - effective potential state vector is small enough to fit in registers. A concrete example: consistently applying effective potential in code review and regression tests keeps the whole pipeline trustworthy.

## Q71: How does effective potential handle captured photons - justify your answer with a concrete production example.
**A:** It terminates integration at the horizon and records absorption; effective potential distinguishes capture from scatter by the radial turning point. A concrete example: consistently applying effective potential in code review and regression tests keeps the whole pipeline trustworthy.

## Q72: What role do conserved constants play in effective potential - justify your answer with a concrete production example.
**A:** They let you solve impact parameters analytically or prune impossible trajectories, dramatically speeding effective potential for large image grids. A concrete example: consistently applying effective potential in code review and regression tests keeps the whole pipeline trustworthy.

## Q73: Describe the numerical error budget of effective potential - justify your answer with a concrete production example.
**A:** Per-step truncation error and accumulated drift; effective potential budgets a relative tolerance and verifies the final image is stable. A concrete example: consistently applying effective potential in code review and regression tests keeps the whole pipeline trustworthy.

## Q74: How does effective potential map the sky to the image plane - justify your answer with a concrete production example.
**A:** Each image pixel defines an initial direction; effective potential evolves that direction backward in time until it leaves the domain to a background sky or hits the disk. A concrete example: consistently applying effective potential in code review and regression tests keeps the whole pipeline trustworthy.

## Q75: What is the most common bug in effective potential - justify your answer with a concrete production example.
**A:** A sign error in the equations of motion or a wrong coordinate transformation that produces plausible-but-wrong lensing; effective potential needs golden-image regression tests. A concrete example: consistently applying effective potential in code review and regression tests keeps the whole pipeline trustworthy.

## Q76: How do you parallelize effective potential - justify your answer with a concrete production example.
**A:** Every pixel is an independent effective potential problem, so one thread per ray gives embarrassingly parallel behavior with no inter-thread communication. A concrete example: consistently applying effective potential in code review and regression tests keeps the whole pipeline trustworthy.

## Q77: What determines the visual shadow size in effective potential - justify your answer with a concrete production example.
**A:** The photon sphere and horizon geometry: captured rays draw the shadow whose boundary in effective potential is the photon ring. A concrete example: consistently applying effective potential in code review and regression tests keeps the whole pipeline trustworthy.

## Q78: When do you need full Kerr effective potential instead of Schwarzschild - justify your answer with a concrete production example.
**A:** Whenever the disk's rotation and frame dragging matter - most real astrophysical images; effective potential must support spin to be credible. A concrete example: consistently applying effective potential in code review and regression tests keeps the whole pipeline trustworthy.

## Q79: What is the 'second/third image' vocabulary of effective potential - justify your answer with a concrete production example.
**A:** Light winding around the black hole produces multiple images; effective potential naturally produces the primary, secondary, and higher-order photon ring. A concrete example: consistently applying effective potential in code review and regression tests keeps the whole pipeline trustworthy.

## Q80: How does effective potential produce the bright thin ring - justify your answer with a concrete production example.
**A:** Rays that graze the photon sphere travel long path lengths through the brightest disk region, so averaged intensity peaks at the effective potential critical impact parameter. A concrete example: consistently applying effective potential in code review and regression tests keeps the whole pipeline trustworthy.

## Q81: How does effective potential decide frequencies for render - justify your answer with a concrete production example.
**A:** It integrates the redshift factor along the ray; effective potential multiplies emitted frequency by it before applying the transfer equation. A concrete example: consistently applying effective potential in code review and regression tests keeps the whole pipeline trustworthy.

## Q82: What modes does effective potential render the accretion disk - justify your answer with a concrete production example.
**A:** First as a geometric emitter grid, later using GRMHD data; effective potential is agnostic to the source as long as it can query emissivity along the path. A concrete example: consistently applying effective potential in code review and regression tests keeps the whole pipeline trustworthy.

## Q83: How is effective potential performance quantified - justify your answer with a concrete production example.
**A:** Mega-rays per second and time per frame; effective potential usually spends its budget in the integration loop, so its step count is the key metric. A concrete example: consistently applying effective potential in code review and regression tests keeps the whole pipeline trustworthy.

## Q84: What is the effect of camera position in effective potential - justify your answer with a concrete production example.
**A:** Face-on, edge-on, and plunging camera setups change the projected ring shape; effective potential validates each against known renders. A concrete example: consistently applying effective potential in code review and regression tests keeps the whole pipeline trustworthy.

## Q85: How does effective potential incorporate the disk's fluid velocity - justify your answer with a concrete production example.
**A:** Doppler and beaming appear when the emissivity frame is boosted; effective potential applies that boost per photon ray path segment. A concrete example: consistently applying effective potential in code review and regression tests keeps the whole pipeline trustworthy.

## Q86: What is the horizon-catching strategy in effective potential - justify your answer with a concrete production example.
**A:** Rather than refine forever, you flag a ray as captured once r drops below the horizon radius; effective potential then terminates that lane. A concrete example: consistently applying effective potential in code review and regression tests keeps the whole pipeline trustworthy.

## Q87: How should you commission effective potential output - justify your answer with a concrete production example.
**A:** Side-by-side with published stills of the same metric and camera to confirm lensing, ring, and shadow match within a few percent. A concrete example: consistently applying effective potential in code review and regression tests keeps the whole pipeline trustworthy.

## Q88: How should you commission effective potential output - justify your answer with a concrete production example.
**A:** Side-by-side with published stills of the same metric and camera to confirm lensing, ring, and shadow match within a few percent. A concrete example: consistently applying effective potential in code review and regression tests keeps the whole pipeline trustworthy.

## Q89: What is the horizon-catching strategy in effective potential - justify your answer with a concrete production example.
**A:** Rather than refine forever, you flag a ray as captured once r drops below the horizon radius; effective potential then terminates that lane. A concrete example: consistently applying effective potential in code review and regression tests keeps the whole pipeline trustworthy.

## Q90: How does effective potential incorporate the disk's fluid velocity - justify your answer with a concrete production example.
**A:** Doppler and beaming appear when the emissivity frame is boosted; effective potential applies that boost per photon ray path segment. A concrete example: consistently applying effective potential in code review and regression tests keeps the whole pipeline trustworthy.

## Q91: What is the effect of camera position in effective potential - justify your answer with a concrete production example.
**A:** Face-on, edge-on, and plunging camera setups change the projected ring shape; effective potential validates each against known renders. A concrete example: consistently applying effective potential in code review and regression tests keeps the whole pipeline trustworthy.

## Q92: How is effective potential performance quantified - justify your answer with a concrete production example.
**A:** Mega-rays per second and time per frame; effective potential usually spends its budget in the integration loop, so its step count is the key metric. A concrete example: consistently applying effective potential in code review and regression tests keeps the whole pipeline trustworthy.

## Q93: What modes does effective potential render the accretion disk - justify your answer with a concrete production example.
**A:** First as a geometric emitter grid, later using GRMHD data; effective potential is agnostic to the source as long as it can query emissivity along the path. A concrete example: consistently applying effective potential in code review and regression tests keeps the whole pipeline trustworthy.

## Q94: How does effective potential decide frequencies for render - justify your answer with a concrete production example.
**A:** It integrates the redshift factor along the ray; effective potential multiplies emitted frequency by it before applying the transfer equation. A concrete example: consistently applying effective potential in code review and regression tests keeps the whole pipeline trustworthy.

## Q95: How does effective potential produce the bright thin ring - justify your answer with a concrete production example.
**A:** Rays that graze the photon sphere travel long path lengths through the brightest disk region, so averaged intensity peaks at the effective potential critical impact parameter. A concrete example: consistently applying effective potential in code review and regression tests keeps the whole pipeline trustworthy.

## Q96: What is the 'second/third image' vocabulary of effective potential - justify your answer with a concrete production example.
**A:** Light winding around the black hole produces multiple images; effective potential naturally produces the primary, secondary, and higher-order photon ring. A concrete example: consistently applying effective potential in code review and regression tests keeps the whole pipeline trustworthy.

## Q97: When do you need full Kerr effective potential instead of Schwarzschild - justify your answer with a concrete production example.
**A:** Whenever the disk's rotation and frame dragging matter - most real astrophysical images; effective potential must support spin to be credible. A concrete example: consistently applying effective potential in code review and regression tests keeps the whole pipeline trustworthy.

## Q98: What determines the visual shadow size in effective potential - justify your answer with a concrete production example.
**A:** The photon sphere and horizon geometry: captured rays draw the shadow whose boundary in effective potential is the photon ring. A concrete example: consistently applying effective potential in code review and regression tests keeps the whole pipeline trustworthy.

## Q99: How do you parallelize effective potential - justify your answer with a concrete production example.
**A:** Every pixel is an independent effective potential problem, so one thread per ray gives embarrassingly parallel behavior with no inter-thread communication. A concrete example: consistently applying effective potential in code review and regression tests keeps the whole pipeline trustworthy.

## Q100: What is the most common bug in effective potential - justify your answer with a concrete production example.
**A:** A sign error in the equations of motion or a wrong coordinate transformation that produces plausible-but-wrong lensing; effective potential needs golden-image regression tests. A concrete example: consistently applying effective potential in code review and regression tests keeps the whole pipeline trustworthy.
