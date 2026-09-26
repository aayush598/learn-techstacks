# Gr Ray Tracing — Null Geodesics Interview Questions and Answers

## Q1: What is a null geodesic?
**A:** A geodesic with zero interval, ds^2 = 0, the path of a massless particle (photon); its tangent is lightlike at every event.

## Q2: Why are all these effects described by null geodesics exclusively?
**A:** Light is massless, so only null rays matter for imaging; massive trajectories (disks, orbits) are used for emission but are timelike geodesics instead.

## Q3: What mathematical property makes null geodesics the basis?
**A:** They are the extrema of the geometric path length among null curves; the physical statement is Fermat's principle in curved spacetime.

## Q4: How is the null condition imposed on initial data?
**A:** The photon's 4-momentum must satisfy g_mu,nu p^mu p^nu = 0; code constructs this by normalizing the spatial direction with E.

## Q5: What does 'H=0' mean for the affine parameter?
**A:** The affine parameter for null geodesics is only defined up to scale; H=0 forbids proper time, but that's fine - lambda remains a valid integration coordinate.

## Q6: How do null geodesics specify the shadow?
**A:** Null rays with low impact parameter cross the horizon (capture); the boundary between capture and escape in image space is the shadow edge.

## Q7: What is the photon ring in null language?
**A:** The unstable null orbits at r ~ 3M: null geodesics that linger there wind many times, producing the bright rings in images.

## Q8: How do you numerically preserve nullness?
**A:** Use symplectic/geodesic-accurate integrators and check |2H| per step; adaptive schemes keep the residual at roundoff, preserving the null shell.

## Q9: What is the equivalence of null geodesics to bending?
**A:** Every bending angle, multiple image, and redshift is a consequence of one family of null equations - no separate lensing model needed.

## Q10: What happens to the null ray at the horizon?
**A:** In smooth coordinates it crosses r+ with finite lambda; in Boyer-Lindquist its t and r coordinate flip, so the capture check must use r < r+.

## Q11: What is the radial turning point for a null ray?
**A:** The closest approach r0 where rdot = 0; solving the effective equation for r0 as function of b and the angle determines deflection - the lens map.

## Q12: What is the 'impact parameter' - null geodesic dictionary?
**A:** b = L/E; every observable (deflection, shadow boundary, ring position) is a function of b - the fundamental scalar of null geometry.

## Q13: What is the self-similar ring structure?
**A:** Null geodesics that wind n half-turns produce images n orders fainter; the ratio of successive ring radii tends to the large-winding geometric limit e^(-2pi).

## Q14: How do you validate null geodesics?
**A:** Reproduce: deflection 4M/b (weak), circular orbit at r=3M (a=0), and the shadow boundary at b=3sqrt(3)M - the three canonical null tests.

## Q15: What does polarization/null coupling add?
**A:** Polarization is parallel-transported along the null ray (with the Faraday rotation in the GRMHD plasma); a fully physical code tracks the polarization basis along null geodesics.

## Q16: What does null geodesics concretely do inside the raytracer?
**A:** It advances photon trajectories in the curved spacetime, applying the equations of motion so each camera ray follows a true null geodesic.

## Q17: Why is null geodesics the heart of a black-hole visualizer?
**A:** Every visual signature - lensing, photon ring, shadow, redshift - emerges from exactly how null geodesics bends and time-shifts each ray.

## Q18: How is null geodesics implemented on the GPU?
**A:** As a numerical integration loop in device code with per-ray state in registers, stepping through null geodesics until the ray is captured or escapes.

## Q19: What are the two families of integration for null geodesics?
**A:** The direct geodesic integration of the equations of motion, and Hamilton-Jacobi reduced systems using conserved constants; null geodesics chooses per codebase.

## Q20: How do you validate null geodesics?
**A:** Reproduce the analytic Schwarzschild lensing angle, the photon ring, and the projected shadow shape measured against published figures.

## Q21: What is the typical step-size strategy in null geodesics?
**A:** Adaptive stepping that refines near the photon sphere and the horizon, where null geodesics gradients are steepest and error grows fastest.

## Q22: What state does the integrator track for null geodesics?
**A:** Position, four-momentum components, affine parameter, and accumulated redshift - null geodesics state vector is small enough to fit in registers.

## Q23: How does null geodesics handle captured photons?
**A:** It terminates integration at the horizon and records absorption; null geodesics distinguishes capture from scatter by the radial turning point.

## Q24: What role do conserved constants play in null geodesics?
**A:** They let you solve impact parameters analytically or prune impossible trajectories, dramatically speeding null geodesics for large image grids.

## Q25: Describe the numerical error budget of null geodesics.
**A:** Per-step truncation error and accumulated drift; null geodesics budgets a relative tolerance and verifies the final image is stable.

## Q26: How does null geodesics map the sky to the image plane?
**A:** Each image pixel defines an initial direction; null geodesics evolves that direction backward in time until it leaves the domain to a background sky or hits the disk.

## Q27: What is the most common bug in null geodesics?
**A:** A sign error in the equations of motion or a wrong coordinate transformation that produces plausible-but-wrong lensing; null geodesics needs golden-image regression tests.

## Q28: How do you parallelize null geodesics?
**A:** Every pixel is an independent null geodesics problem, so one thread per ray gives embarrassingly parallel behavior with no inter-thread communication.

## Q29: What determines the visual shadow size in null geodesics?
**A:** The photon sphere and horizon geometry: captured rays draw the shadow whose boundary in null geodesics is the photon ring.

## Q30: When do you need full Kerr null geodesics instead of Schwarzschild?
**A:** Whenever the disk's rotation and frame dragging matter - most real astrophysical images; null geodesics must support spin to be credible.

## Q31: What is the 'second/third image' vocabulary of null geodesics?
**A:** Light winding around the black hole produces multiple images; null geodesics naturally produces the primary, secondary, and higher-order photon ring.

## Q32: How does null geodesics produce the bright thin ring?
**A:** Rays that graze the photon sphere travel long path lengths through the brightest disk region, so averaged intensity peaks at the null geodesics critical impact parameter.

## Q33: How does null geodesics decide frequencies for render?
**A:** It integrates the redshift factor along the ray; null geodesics multiplies emitted frequency by it before applying the transfer equation.

## Q34: What modes does null geodesics render the accretion disk?
**A:** First as a geometric emitter grid, later using GRMHD data; null geodesics is agnostic to the source as long as it can query emissivity along the path.

## Q35: How is null geodesics performance quantified?
**A:** Mega-rays per second and time per frame; null geodesics usually spends its budget in the integration loop, so its step count is the key metric.

## Q36: What is the effect of camera position in null geodesics?
**A:** Face-on, edge-on, and plunging camera setups change the projected ring shape; null geodesics validates each against known renders.

## Q37: How does null geodesics incorporate the disk's fluid velocity?
**A:** Doppler and beaming appear when the emissivity frame is boosted; null geodesics applies that boost per photon ray path segment.

## Q38: What is the horizon-catching strategy in null geodesics?
**A:** Rather than refine forever, you flag a ray as captured once r drops below the horizon radius; null geodesics then terminates that lane.

## Q39: How should you commission null geodesics output?
**A:** Side-by-side with published stills of the same metric and camera to confirm lensing, ring, and shadow match within a few percent.

## Q40: How should you commission null geodesics output - justify your answer with a concrete production example.
**A:** Side-by-side with published stills of the same metric and camera to confirm lensing, ring, and shadow match within a few percent. A concrete example: consistently applying null geodesics in code review and regression tests keeps the whole pipeline trustworthy.

## Q41: What is the horizon-catching strategy in null geodesics - justify your answer with a concrete production example.
**A:** Rather than refine forever, you flag a ray as captured once r drops below the horizon radius; null geodesics then terminates that lane. A concrete example: consistently applying null geodesics in code review and regression tests keeps the whole pipeline trustworthy.

## Q42: How does null geodesics incorporate the disk's fluid velocity - justify your answer with a concrete production example.
**A:** Doppler and beaming appear when the emissivity frame is boosted; null geodesics applies that boost per photon ray path segment. A concrete example: consistently applying null geodesics in code review and regression tests keeps the whole pipeline trustworthy.

## Q43: What is the effect of camera position in null geodesics - justify your answer with a concrete production example.
**A:** Face-on, edge-on, and plunging camera setups change the projected ring shape; null geodesics validates each against known renders. A concrete example: consistently applying null geodesics in code review and regression tests keeps the whole pipeline trustworthy.

## Q44: How is null geodesics performance quantified - justify your answer with a concrete production example.
**A:** Mega-rays per second and time per frame; null geodesics usually spends its budget in the integration loop, so its step count is the key metric. A concrete example: consistently applying null geodesics in code review and regression tests keeps the whole pipeline trustworthy.

## Q45: What modes does null geodesics render the accretion disk - justify your answer with a concrete production example.
**A:** First as a geometric emitter grid, later using GRMHD data; null geodesics is agnostic to the source as long as it can query emissivity along the path. A concrete example: consistently applying null geodesics in code review and regression tests keeps the whole pipeline trustworthy.

## Q46: How does null geodesics decide frequencies for render - justify your answer with a concrete production example.
**A:** It integrates the redshift factor along the ray; null geodesics multiplies emitted frequency by it before applying the transfer equation. A concrete example: consistently applying null geodesics in code review and regression tests keeps the whole pipeline trustworthy.

## Q47: How does null geodesics produce the bright thin ring - justify your answer with a concrete production example.
**A:** Rays that graze the photon sphere travel long path lengths through the brightest disk region, so averaged intensity peaks at the null geodesics critical impact parameter. A concrete example: consistently applying null geodesics in code review and regression tests keeps the whole pipeline trustworthy.

## Q48: What is the 'second/third image' vocabulary of null geodesics - justify your answer with a concrete production example.
**A:** Light winding around the black hole produces multiple images; null geodesics naturally produces the primary, secondary, and higher-order photon ring. A concrete example: consistently applying null geodesics in code review and regression tests keeps the whole pipeline trustworthy.

## Q49: When do you need full Kerr null geodesics instead of Schwarzschild - justify your answer with a concrete production example.
**A:** Whenever the disk's rotation and frame dragging matter - most real astrophysical images; null geodesics must support spin to be credible. A concrete example: consistently applying null geodesics in code review and regression tests keeps the whole pipeline trustworthy.

## Q50: What determines the visual shadow size in null geodesics - justify your answer with a concrete production example.
**A:** The photon sphere and horizon geometry: captured rays draw the shadow whose boundary in null geodesics is the photon ring. A concrete example: consistently applying null geodesics in code review and regression tests keeps the whole pipeline trustworthy.

## Q51: How do you parallelize null geodesics - justify your answer with a concrete production example.
**A:** Every pixel is an independent null geodesics problem, so one thread per ray gives embarrassingly parallel behavior with no inter-thread communication. A concrete example: consistently applying null geodesics in code review and regression tests keeps the whole pipeline trustworthy.

## Q52: What is the most common bug in null geodesics - justify your answer with a concrete production example.
**A:** A sign error in the equations of motion or a wrong coordinate transformation that produces plausible-but-wrong lensing; null geodesics needs golden-image regression tests. A concrete example: consistently applying null geodesics in code review and regression tests keeps the whole pipeline trustworthy.

## Q53: How does null geodesics map the sky to the image plane - justify your answer with a concrete production example.
**A:** Each image pixel defines an initial direction; null geodesics evolves that direction backward in time until it leaves the domain to a background sky or hits the disk. A concrete example: consistently applying null geodesics in code review and regression tests keeps the whole pipeline trustworthy.

## Q54: Describe the numerical error budget of null geodesics - justify your answer with a concrete production example.
**A:** Per-step truncation error and accumulated drift; null geodesics budgets a relative tolerance and verifies the final image is stable. A concrete example: consistently applying null geodesics in code review and regression tests keeps the whole pipeline trustworthy.

## Q55: What role do conserved constants play in null geodesics - justify your answer with a concrete production example.
**A:** They let you solve impact parameters analytically or prune impossible trajectories, dramatically speeding null geodesics for large image grids. A concrete example: consistently applying null geodesics in code review and regression tests keeps the whole pipeline trustworthy.

## Q56: How does null geodesics handle captured photons - justify your answer with a concrete production example.
**A:** It terminates integration at the horizon and records absorption; null geodesics distinguishes capture from scatter by the radial turning point. A concrete example: consistently applying null geodesics in code review and regression tests keeps the whole pipeline trustworthy.

## Q57: What state does the integrator track for null geodesics - justify your answer with a concrete production example.
**A:** Position, four-momentum components, affine parameter, and accumulated redshift - null geodesics state vector is small enough to fit in registers. A concrete example: consistently applying null geodesics in code review and regression tests keeps the whole pipeline trustworthy.

## Q58: What is the typical step-size strategy in null geodesics - justify your answer with a concrete production example.
**A:** Adaptive stepping that refines near the photon sphere and the horizon, where null geodesics gradients are steepest and error grows fastest. A concrete example: consistently applying null geodesics in code review and regression tests keeps the whole pipeline trustworthy.

## Q59: How do you validate null geodesics - justify your answer with a concrete production example.
**A:** Reproduce the analytic Schwarzschild lensing angle, the photon ring, and the projected shadow shape measured against published figures. A concrete example: consistently applying null geodesics in code review and regression tests keeps the whole pipeline trustworthy.

## Q60: What are the two families of integration for null geodesics - justify your answer with a concrete production example.
**A:** The direct geodesic integration of the equations of motion, and Hamilton-Jacobi reduced systems using conserved constants; null geodesics chooses per codebase. A concrete example: consistently applying null geodesics in code review and regression tests keeps the whole pipeline trustworthy.

## Q61: How is null geodesics implemented on the GPU - justify your answer with a concrete production example.
**A:** As a numerical integration loop in device code with per-ray state in registers, stepping through null geodesics until the ray is captured or escapes. A concrete example: consistently applying null geodesics in code review and regression tests keeps the whole pipeline trustworthy.

## Q62: Why is null geodesics the heart of a black-hole visualizer - justify your answer with a concrete production example.
**A:** Every visual signature - lensing, photon ring, shadow, redshift - emerges from exactly how null geodesics bends and time-shifts each ray. A concrete example: consistently applying null geodesics in code review and regression tests keeps the whole pipeline trustworthy.

## Q63: What does null geodesics concretely do inside the raytracer - justify your answer with a concrete production example.
**A:** It advances photon trajectories in the curved spacetime, applying the equations of motion so each camera ray follows a true null geodesic. A concrete example: consistently applying null geodesics in code review and regression tests keeps the whole pipeline trustworthy.

## Q64: What does null geodesics concretely do inside the raytracer - justify your answer with a concrete production example.
**A:** It advances photon trajectories in the curved spacetime, applying the equations of motion so each camera ray follows a true null geodesic. A concrete example: consistently applying null geodesics in code review and regression tests keeps the whole pipeline trustworthy.

## Q65: Why is null geodesics the heart of a black-hole visualizer - justify your answer with a concrete production example.
**A:** Every visual signature - lensing, photon ring, shadow, redshift - emerges from exactly how null geodesics bends and time-shifts each ray. A concrete example: consistently applying null geodesics in code review and regression tests keeps the whole pipeline trustworthy.

## Q66: How is null geodesics implemented on the GPU - justify your answer with a concrete production example.
**A:** As a numerical integration loop in device code with per-ray state in registers, stepping through null geodesics until the ray is captured or escapes. A concrete example: consistently applying null geodesics in code review and regression tests keeps the whole pipeline trustworthy.

## Q67: What are the two families of integration for null geodesics - justify your answer with a concrete production example.
**A:** The direct geodesic integration of the equations of motion, and Hamilton-Jacobi reduced systems using conserved constants; null geodesics chooses per codebase. A concrete example: consistently applying null geodesics in code review and regression tests keeps the whole pipeline trustworthy.

## Q68: How do you validate null geodesics - justify your answer with a concrete production example.
**A:** Reproduce the analytic Schwarzschild lensing angle, the photon ring, and the projected shadow shape measured against published figures. A concrete example: consistently applying null geodesics in code review and regression tests keeps the whole pipeline trustworthy.

## Q69: What is the typical step-size strategy in null geodesics - justify your answer with a concrete production example.
**A:** Adaptive stepping that refines near the photon sphere and the horizon, where null geodesics gradients are steepest and error grows fastest. A concrete example: consistently applying null geodesics in code review and regression tests keeps the whole pipeline trustworthy.

## Q70: What state does the integrator track for null geodesics - justify your answer with a concrete production example.
**A:** Position, four-momentum components, affine parameter, and accumulated redshift - null geodesics state vector is small enough to fit in registers. A concrete example: consistently applying null geodesics in code review and regression tests keeps the whole pipeline trustworthy.

## Q71: How does null geodesics handle captured photons - justify your answer with a concrete production example.
**A:** It terminates integration at the horizon and records absorption; null geodesics distinguishes capture from scatter by the radial turning point. A concrete example: consistently applying null geodesics in code review and regression tests keeps the whole pipeline trustworthy.

## Q72: What role do conserved constants play in null geodesics - justify your answer with a concrete production example.
**A:** They let you solve impact parameters analytically or prune impossible trajectories, dramatically speeding null geodesics for large image grids. A concrete example: consistently applying null geodesics in code review and regression tests keeps the whole pipeline trustworthy.

## Q73: Describe the numerical error budget of null geodesics - justify your answer with a concrete production example.
**A:** Per-step truncation error and accumulated drift; null geodesics budgets a relative tolerance and verifies the final image is stable. A concrete example: consistently applying null geodesics in code review and regression tests keeps the whole pipeline trustworthy.

## Q74: How does null geodesics map the sky to the image plane - justify your answer with a concrete production example.
**A:** Each image pixel defines an initial direction; null geodesics evolves that direction backward in time until it leaves the domain to a background sky or hits the disk. A concrete example: consistently applying null geodesics in code review and regression tests keeps the whole pipeline trustworthy.

## Q75: What is the most common bug in null geodesics - justify your answer with a concrete production example.
**A:** A sign error in the equations of motion or a wrong coordinate transformation that produces plausible-but-wrong lensing; null geodesics needs golden-image regression tests. A concrete example: consistently applying null geodesics in code review and regression tests keeps the whole pipeline trustworthy.

## Q76: How do you parallelize null geodesics - justify your answer with a concrete production example.
**A:** Every pixel is an independent null geodesics problem, so one thread per ray gives embarrassingly parallel behavior with no inter-thread communication. A concrete example: consistently applying null geodesics in code review and regression tests keeps the whole pipeline trustworthy.

## Q77: What determines the visual shadow size in null geodesics - justify your answer with a concrete production example.
**A:** The photon sphere and horizon geometry: captured rays draw the shadow whose boundary in null geodesics is the photon ring. A concrete example: consistently applying null geodesics in code review and regression tests keeps the whole pipeline trustworthy.

## Q78: When do you need full Kerr null geodesics instead of Schwarzschild - justify your answer with a concrete production example.
**A:** Whenever the disk's rotation and frame dragging matter - most real astrophysical images; null geodesics must support spin to be credible. A concrete example: consistently applying null geodesics in code review and regression tests keeps the whole pipeline trustworthy.

## Q79: What is the 'second/third image' vocabulary of null geodesics - justify your answer with a concrete production example.
**A:** Light winding around the black hole produces multiple images; null geodesics naturally produces the primary, secondary, and higher-order photon ring. A concrete example: consistently applying null geodesics in code review and regression tests keeps the whole pipeline trustworthy.

## Q80: How does null geodesics produce the bright thin ring - justify your answer with a concrete production example.
**A:** Rays that graze the photon sphere travel long path lengths through the brightest disk region, so averaged intensity peaks at the null geodesics critical impact parameter. A concrete example: consistently applying null geodesics in code review and regression tests keeps the whole pipeline trustworthy.

## Q81: How does null geodesics decide frequencies for render - justify your answer with a concrete production example.
**A:** It integrates the redshift factor along the ray; null geodesics multiplies emitted frequency by it before applying the transfer equation. A concrete example: consistently applying null geodesics in code review and regression tests keeps the whole pipeline trustworthy.

## Q82: What modes does null geodesics render the accretion disk - justify your answer with a concrete production example.
**A:** First as a geometric emitter grid, later using GRMHD data; null geodesics is agnostic to the source as long as it can query emissivity along the path. A concrete example: consistently applying null geodesics in code review and regression tests keeps the whole pipeline trustworthy.

## Q83: How is null geodesics performance quantified - justify your answer with a concrete production example.
**A:** Mega-rays per second and time per frame; null geodesics usually spends its budget in the integration loop, so its step count is the key metric. A concrete example: consistently applying null geodesics in code review and regression tests keeps the whole pipeline trustworthy.

## Q84: What is the effect of camera position in null geodesics - justify your answer with a concrete production example.
**A:** Face-on, edge-on, and plunging camera setups change the projected ring shape; null geodesics validates each against known renders. A concrete example: consistently applying null geodesics in code review and regression tests keeps the whole pipeline trustworthy.

## Q85: How does null geodesics incorporate the disk's fluid velocity - justify your answer with a concrete production example.
**A:** Doppler and beaming appear when the emissivity frame is boosted; null geodesics applies that boost per photon ray path segment. A concrete example: consistently applying null geodesics in code review and regression tests keeps the whole pipeline trustworthy.

## Q86: What is the horizon-catching strategy in null geodesics - justify your answer with a concrete production example.
**A:** Rather than refine forever, you flag a ray as captured once r drops below the horizon radius; null geodesics then terminates that lane. A concrete example: consistently applying null geodesics in code review and regression tests keeps the whole pipeline trustworthy.

## Q87: How should you commission null geodesics output - justify your answer with a concrete production example.
**A:** Side-by-side with published stills of the same metric and camera to confirm lensing, ring, and shadow match within a few percent. A concrete example: consistently applying null geodesics in code review and regression tests keeps the whole pipeline trustworthy.

## Q88: How should you commission null geodesics output - justify your answer with a concrete production example.
**A:** Side-by-side with published stills of the same metric and camera to confirm lensing, ring, and shadow match within a few percent. A concrete example: consistently applying null geodesics in code review and regression tests keeps the whole pipeline trustworthy.

## Q89: What is the horizon-catching strategy in null geodesics - justify your answer with a concrete production example.
**A:** Rather than refine forever, you flag a ray as captured once r drops below the horizon radius; null geodesics then terminates that lane. A concrete example: consistently applying null geodesics in code review and regression tests keeps the whole pipeline trustworthy.

## Q90: How does null geodesics incorporate the disk's fluid velocity - justify your answer with a concrete production example.
**A:** Doppler and beaming appear when the emissivity frame is boosted; null geodesics applies that boost per photon ray path segment. A concrete example: consistently applying null geodesics in code review and regression tests keeps the whole pipeline trustworthy.

## Q91: What is the effect of camera position in null geodesics - justify your answer with a concrete production example.
**A:** Face-on, edge-on, and plunging camera setups change the projected ring shape; null geodesics validates each against known renders. A concrete example: consistently applying null geodesics in code review and regression tests keeps the whole pipeline trustworthy.

## Q92: How is null geodesics performance quantified - justify your answer with a concrete production example.
**A:** Mega-rays per second and time per frame; null geodesics usually spends its budget in the integration loop, so its step count is the key metric. A concrete example: consistently applying null geodesics in code review and regression tests keeps the whole pipeline trustworthy.

## Q93: What modes does null geodesics render the accretion disk - justify your answer with a concrete production example.
**A:** First as a geometric emitter grid, later using GRMHD data; null geodesics is agnostic to the source as long as it can query emissivity along the path. A concrete example: consistently applying null geodesics in code review and regression tests keeps the whole pipeline trustworthy.

## Q94: How does null geodesics decide frequencies for render - justify your answer with a concrete production example.
**A:** It integrates the redshift factor along the ray; null geodesics multiplies emitted frequency by it before applying the transfer equation. A concrete example: consistently applying null geodesics in code review and regression tests keeps the whole pipeline trustworthy.

## Q95: How does null geodesics produce the bright thin ring - justify your answer with a concrete production example.
**A:** Rays that graze the photon sphere travel long path lengths through the brightest disk region, so averaged intensity peaks at the null geodesics critical impact parameter. A concrete example: consistently applying null geodesics in code review and regression tests keeps the whole pipeline trustworthy.

## Q96: What is the 'second/third image' vocabulary of null geodesics - justify your answer with a concrete production example.
**A:** Light winding around the black hole produces multiple images; null geodesics naturally produces the primary, secondary, and higher-order photon ring. A concrete example: consistently applying null geodesics in code review and regression tests keeps the whole pipeline trustworthy.

## Q97: When do you need full Kerr null geodesics instead of Schwarzschild - justify your answer with a concrete production example.
**A:** Whenever the disk's rotation and frame dragging matter - most real astrophysical images; null geodesics must support spin to be credible. A concrete example: consistently applying null geodesics in code review and regression tests keeps the whole pipeline trustworthy.

## Q98: What determines the visual shadow size in null geodesics - justify your answer with a concrete production example.
**A:** The photon sphere and horizon geometry: captured rays draw the shadow whose boundary in null geodesics is the photon ring. A concrete example: consistently applying null geodesics in code review and regression tests keeps the whole pipeline trustworthy.

## Q99: How do you parallelize null geodesics - justify your answer with a concrete production example.
**A:** Every pixel is an independent null geodesics problem, so one thread per ray gives embarrassingly parallel behavior with no inter-thread communication. A concrete example: consistently applying null geodesics in code review and regression tests keeps the whole pipeline trustworthy.

## Q100: What is the most common bug in null geodesics - justify your answer with a concrete production example.
**A:** A sign error in the equations of motion or a wrong coordinate transformation that produces plausible-but-wrong lensing; null geodesics needs golden-image regression tests. A concrete example: consistently applying null geodesics in code review and regression tests keeps the whole pipeline trustworthy.
