# Gr Ray Tracing — Photon Sphere Interview Questions and Answers

## Q1: What is the photon sphere?
**A:** The surface where null circular orbits exist - for Schwarzschild at r=3M; in Kerr there are prograde and retrograde photon orbits at different radii.

## Q2: Why is the orbit unstable?
**A:** The effective potential has a maximum there - radially, V_r(r) is a maximum; small perturbations rocket the photon inward or outward (the ring is a razor).

## Q3: What does it do in images?
**A:** Photons skimming the sphere wind many times, piling up near the boundary of the shadow - producing the characteristically bright, sharp ring.

## Q4: What is the prograde vs retrograde radius?
**A:** r_ph,prog < 3M < r_ph,retro for Kerr with a>0; the difference sets the asymmetric ring shape (crescent/D) - a spin probe.

## Q5: What is the analytic radius?
**A:** r_ph = 2M (1 + cos(2/3 arccos(+-|a|/M))) - the upper sign for prograde, lower for retrograde; verify against both limits (3M at a=0, ~M/(2) at a=M prograde) - code-check.

## Q6: How does the sphere relate to the shadow?
**A:** The shadow boundary consists of impact parameters that wind asymptotically to the sphere (b = b_crit(prog) and b_crit(retro)); the sphere IS the shadow's edge-set.

## Q7: How many images does the ring produce?
**A:** The sphere encodes an infinite ladder of winding angles; each multiple of the angle gives one more faint copy of the source on the ring - log-spaced.

## Q8: What is the total magnification near the ring?
**A:** As impact parameter approaches b_crit the ray's winding and travel time diverge, magnifying the source's intensity by factors of ~e^pi per loop.

## Q9: How do you ensure numeric capture of ring photons?
**A:** Those rays spend long affine time near r ~ r_ph; adaptive stepping and fine pixel scanning make the ring resolution robust (supersample the boundary).

## Q10: What is the caustic at the photon ring?
**A:** A caustic: the focus of the lens detaches; the ring's intensity divergence is the null-lensing caustic analogue to gravitational microlensing peaks.

## Q11: What is the ring's radial scaling?
**A:** Successive ring images shrink by a factor ~e^(-2pi) approximately, giving the self-similar 'onion' observable banding in high-res images.

## Q12: What does the sphere do to photon time delay?
**A:** Rays near b_crit linger near 3M for a long affine time; the delay produces the 'late-time' red/infrared limbs of the ring.

## Q13: How does the sphere interplay with the disk?
**A:** Disk emission just inside/outside the sphere gets bent the most; the innermost ring samples emission from the entire disk silhouetted through multipass bending.

## Q14: What is the validation of the sphere?
**A:** Launch rays from r0=3M (a=0) with tangential momentum; they must stay at constant r for the whole integration - the golden null test.

## Q15: What is the practical renderer's ring recipe?
**A:** Trace fine impact-parameter sampling around b_crit plus supersample and clamp count - the ring is cheap to expose, hard to hide, easy to sharpen later.

## Q16: What does photon sphere concretely do inside the raytracer?
**A:** It advances photon trajectories in the curved spacetime, applying the equations of motion so each camera ray follows a true null geodesic.

## Q17: Why is photon sphere the heart of a black-hole visualizer?
**A:** Every visual signature - lensing, photon ring, shadow, redshift - emerges from exactly how photon sphere bends and time-shifts each ray.

## Q18: How is photon sphere implemented on the GPU?
**A:** As a numerical integration loop in device code with per-ray state in registers, stepping through photon sphere until the ray is captured or escapes.

## Q19: What are the two families of integration for photon sphere?
**A:** The direct geodesic integration of the equations of motion, and Hamilton-Jacobi reduced systems using conserved constants; photon sphere chooses per codebase.

## Q20: How do you validate photon sphere?
**A:** Reproduce the analytic Schwarzschild lensing angle, the photon ring, and the projected shadow shape measured against published figures.

## Q21: What is the typical step-size strategy in photon sphere?
**A:** Adaptive stepping that refines near the photon sphere and the horizon, where photon sphere gradients are steepest and error grows fastest.

## Q22: What state does the integrator track for photon sphere?
**A:** Position, four-momentum components, affine parameter, and accumulated redshift - photon sphere state vector is small enough to fit in registers.

## Q23: How does photon sphere handle captured photons?
**A:** It terminates integration at the horizon and records absorption; photon sphere distinguishes capture from scatter by the radial turning point.

## Q24: What role do conserved constants play in photon sphere?
**A:** They let you solve impact parameters analytically or prune impossible trajectories, dramatically speeding photon sphere for large image grids.

## Q25: Describe the numerical error budget of photon sphere.
**A:** Per-step truncation error and accumulated drift; photon sphere budgets a relative tolerance and verifies the final image is stable.

## Q26: How does photon sphere map the sky to the image plane?
**A:** Each image pixel defines an initial direction; photon sphere evolves that direction backward in time until it leaves the domain to a background sky or hits the disk.

## Q27: What is the most common bug in photon sphere?
**A:** A sign error in the equations of motion or a wrong coordinate transformation that produces plausible-but-wrong lensing; photon sphere needs golden-image regression tests.

## Q28: How do you parallelize photon sphere?
**A:** Every pixel is an independent photon sphere problem, so one thread per ray gives embarrassingly parallel behavior with no inter-thread communication.

## Q29: What determines the visual shadow size in photon sphere?
**A:** The photon sphere and horizon geometry: captured rays draw the shadow whose boundary in photon sphere is the photon ring.

## Q30: When do you need full Kerr photon sphere instead of Schwarzschild?
**A:** Whenever the disk's rotation and frame dragging matter - most real astrophysical images; photon sphere must support spin to be credible.

## Q31: What is the 'second/third image' vocabulary of photon sphere?
**A:** Light winding around the black hole produces multiple images; photon sphere naturally produces the primary, secondary, and higher-order photon ring.

## Q32: How does photon sphere produce the bright thin ring?
**A:** Rays that graze the photon sphere travel long path lengths through the brightest disk region, so averaged intensity peaks at the photon sphere critical impact parameter.

## Q33: How does photon sphere decide frequencies for render?
**A:** It integrates the redshift factor along the ray; photon sphere multiplies emitted frequency by it before applying the transfer equation.

## Q34: What modes does photon sphere render the accretion disk?
**A:** First as a geometric emitter grid, later using GRMHD data; photon sphere is agnostic to the source as long as it can query emissivity along the path.

## Q35: How is photon sphere performance quantified?
**A:** Mega-rays per second and time per frame; photon sphere usually spends its budget in the integration loop, so its step count is the key metric.

## Q36: What is the effect of camera position in photon sphere?
**A:** Face-on, edge-on, and plunging camera setups change the projected ring shape; photon sphere validates each against known renders.

## Q37: How does photon sphere incorporate the disk's fluid velocity?
**A:** Doppler and beaming appear when the emissivity frame is boosted; photon sphere applies that boost per photon ray path segment.

## Q38: What is the horizon-catching strategy in photon sphere?
**A:** Rather than refine forever, you flag a ray as captured once r drops below the horizon radius; photon sphere then terminates that lane.

## Q39: How should you commission photon sphere output?
**A:** Side-by-side with published stills of the same metric and camera to confirm lensing, ring, and shadow match within a few percent.

## Q40: How should you commission photon sphere output - justify your answer with a concrete production example.
**A:** Side-by-side with published stills of the same metric and camera to confirm lensing, ring, and shadow match within a few percent. A concrete example: consistently applying photon sphere in code review and regression tests keeps the whole pipeline trustworthy.

## Q41: What is the horizon-catching strategy in photon sphere - justify your answer with a concrete production example.
**A:** Rather than refine forever, you flag a ray as captured once r drops below the horizon radius; photon sphere then terminates that lane. A concrete example: consistently applying photon sphere in code review and regression tests keeps the whole pipeline trustworthy.

## Q42: How does photon sphere incorporate the disk's fluid velocity - justify your answer with a concrete production example.
**A:** Doppler and beaming appear when the emissivity frame is boosted; photon sphere applies that boost per photon ray path segment. A concrete example: consistently applying photon sphere in code review and regression tests keeps the whole pipeline trustworthy.

## Q43: What is the effect of camera position in photon sphere - justify your answer with a concrete production example.
**A:** Face-on, edge-on, and plunging camera setups change the projected ring shape; photon sphere validates each against known renders. A concrete example: consistently applying photon sphere in code review and regression tests keeps the whole pipeline trustworthy.

## Q44: How is photon sphere performance quantified - justify your answer with a concrete production example.
**A:** Mega-rays per second and time per frame; photon sphere usually spends its budget in the integration loop, so its step count is the key metric. A concrete example: consistently applying photon sphere in code review and regression tests keeps the whole pipeline trustworthy.

## Q45: What modes does photon sphere render the accretion disk - justify your answer with a concrete production example.
**A:** First as a geometric emitter grid, later using GRMHD data; photon sphere is agnostic to the source as long as it can query emissivity along the path. A concrete example: consistently applying photon sphere in code review and regression tests keeps the whole pipeline trustworthy.

## Q46: How does photon sphere decide frequencies for render - justify your answer with a concrete production example.
**A:** It integrates the redshift factor along the ray; photon sphere multiplies emitted frequency by it before applying the transfer equation. A concrete example: consistently applying photon sphere in code review and regression tests keeps the whole pipeline trustworthy.

## Q47: How does photon sphere produce the bright thin ring - justify your answer with a concrete production example.
**A:** Rays that graze the photon sphere travel long path lengths through the brightest disk region, so averaged intensity peaks at the photon sphere critical impact parameter. A concrete example: consistently applying photon sphere in code review and regression tests keeps the whole pipeline trustworthy.

## Q48: What is the 'second/third image' vocabulary of photon sphere - justify your answer with a concrete production example.
**A:** Light winding around the black hole produces multiple images; photon sphere naturally produces the primary, secondary, and higher-order photon ring. A concrete example: consistently applying photon sphere in code review and regression tests keeps the whole pipeline trustworthy.

## Q49: When do you need full Kerr photon sphere instead of Schwarzschild - justify your answer with a concrete production example.
**A:** Whenever the disk's rotation and frame dragging matter - most real astrophysical images; photon sphere must support spin to be credible. A concrete example: consistently applying photon sphere in code review and regression tests keeps the whole pipeline trustworthy.

## Q50: What determines the visual shadow size in photon sphere - justify your answer with a concrete production example.
**A:** The photon sphere and horizon geometry: captured rays draw the shadow whose boundary in photon sphere is the photon ring. A concrete example: consistently applying photon sphere in code review and regression tests keeps the whole pipeline trustworthy.

## Q51: How do you parallelize photon sphere - justify your answer with a concrete production example.
**A:** Every pixel is an independent photon sphere problem, so one thread per ray gives embarrassingly parallel behavior with no inter-thread communication. A concrete example: consistently applying photon sphere in code review and regression tests keeps the whole pipeline trustworthy.

## Q52: What is the most common bug in photon sphere - justify your answer with a concrete production example.
**A:** A sign error in the equations of motion or a wrong coordinate transformation that produces plausible-but-wrong lensing; photon sphere needs golden-image regression tests. A concrete example: consistently applying photon sphere in code review and regression tests keeps the whole pipeline trustworthy.

## Q53: How does photon sphere map the sky to the image plane - justify your answer with a concrete production example.
**A:** Each image pixel defines an initial direction; photon sphere evolves that direction backward in time until it leaves the domain to a background sky or hits the disk. A concrete example: consistently applying photon sphere in code review and regression tests keeps the whole pipeline trustworthy.

## Q54: Describe the numerical error budget of photon sphere - justify your answer with a concrete production example.
**A:** Per-step truncation error and accumulated drift; photon sphere budgets a relative tolerance and verifies the final image is stable. A concrete example: consistently applying photon sphere in code review and regression tests keeps the whole pipeline trustworthy.

## Q55: What role do conserved constants play in photon sphere - justify your answer with a concrete production example.
**A:** They let you solve impact parameters analytically or prune impossible trajectories, dramatically speeding photon sphere for large image grids. A concrete example: consistently applying photon sphere in code review and regression tests keeps the whole pipeline trustworthy.

## Q56: How does photon sphere handle captured photons - justify your answer with a concrete production example.
**A:** It terminates integration at the horizon and records absorption; photon sphere distinguishes capture from scatter by the radial turning point. A concrete example: consistently applying photon sphere in code review and regression tests keeps the whole pipeline trustworthy.

## Q57: What state does the integrator track for photon sphere - justify your answer with a concrete production example.
**A:** Position, four-momentum components, affine parameter, and accumulated redshift - photon sphere state vector is small enough to fit in registers. A concrete example: consistently applying photon sphere in code review and regression tests keeps the whole pipeline trustworthy.

## Q58: What is the typical step-size strategy in photon sphere - justify your answer with a concrete production example.
**A:** Adaptive stepping that refines near the photon sphere and the horizon, where photon sphere gradients are steepest and error grows fastest. A concrete example: consistently applying photon sphere in code review and regression tests keeps the whole pipeline trustworthy.

## Q59: How do you validate photon sphere - justify your answer with a concrete production example.
**A:** Reproduce the analytic Schwarzschild lensing angle, the photon ring, and the projected shadow shape measured against published figures. A concrete example: consistently applying photon sphere in code review and regression tests keeps the whole pipeline trustworthy.

## Q60: What are the two families of integration for photon sphere - justify your answer with a concrete production example.
**A:** The direct geodesic integration of the equations of motion, and Hamilton-Jacobi reduced systems using conserved constants; photon sphere chooses per codebase. A concrete example: consistently applying photon sphere in code review and regression tests keeps the whole pipeline trustworthy.

## Q61: How is photon sphere implemented on the GPU - justify your answer with a concrete production example.
**A:** As a numerical integration loop in device code with per-ray state in registers, stepping through photon sphere until the ray is captured or escapes. A concrete example: consistently applying photon sphere in code review and regression tests keeps the whole pipeline trustworthy.

## Q62: Why is photon sphere the heart of a black-hole visualizer - justify your answer with a concrete production example.
**A:** Every visual signature - lensing, photon ring, shadow, redshift - emerges from exactly how photon sphere bends and time-shifts each ray. A concrete example: consistently applying photon sphere in code review and regression tests keeps the whole pipeline trustworthy.

## Q63: What does photon sphere concretely do inside the raytracer - justify your answer with a concrete production example.
**A:** It advances photon trajectories in the curved spacetime, applying the equations of motion so each camera ray follows a true null geodesic. A concrete example: consistently applying photon sphere in code review and regression tests keeps the whole pipeline trustworthy.

## Q64: What does photon sphere concretely do inside the raytracer - justify your answer with a concrete production example.
**A:** It advances photon trajectories in the curved spacetime, applying the equations of motion so each camera ray follows a true null geodesic. A concrete example: consistently applying photon sphere in code review and regression tests keeps the whole pipeline trustworthy.

## Q65: Why is photon sphere the heart of a black-hole visualizer - justify your answer with a concrete production example.
**A:** Every visual signature - lensing, photon ring, shadow, redshift - emerges from exactly how photon sphere bends and time-shifts each ray. A concrete example: consistently applying photon sphere in code review and regression tests keeps the whole pipeline trustworthy.

## Q66: How is photon sphere implemented on the GPU - justify your answer with a concrete production example.
**A:** As a numerical integration loop in device code with per-ray state in registers, stepping through photon sphere until the ray is captured or escapes. A concrete example: consistently applying photon sphere in code review and regression tests keeps the whole pipeline trustworthy.

## Q67: What are the two families of integration for photon sphere - justify your answer with a concrete production example.
**A:** The direct geodesic integration of the equations of motion, and Hamilton-Jacobi reduced systems using conserved constants; photon sphere chooses per codebase. A concrete example: consistently applying photon sphere in code review and regression tests keeps the whole pipeline trustworthy.

## Q68: How do you validate photon sphere - justify your answer with a concrete production example.
**A:** Reproduce the analytic Schwarzschild lensing angle, the photon ring, and the projected shadow shape measured against published figures. A concrete example: consistently applying photon sphere in code review and regression tests keeps the whole pipeline trustworthy.

## Q69: What is the typical step-size strategy in photon sphere - justify your answer with a concrete production example.
**A:** Adaptive stepping that refines near the photon sphere and the horizon, where photon sphere gradients are steepest and error grows fastest. A concrete example: consistently applying photon sphere in code review and regression tests keeps the whole pipeline trustworthy.

## Q70: What state does the integrator track for photon sphere - justify your answer with a concrete production example.
**A:** Position, four-momentum components, affine parameter, and accumulated redshift - photon sphere state vector is small enough to fit in registers. A concrete example: consistently applying photon sphere in code review and regression tests keeps the whole pipeline trustworthy.

## Q71: How does photon sphere handle captured photons - justify your answer with a concrete production example.
**A:** It terminates integration at the horizon and records absorption; photon sphere distinguishes capture from scatter by the radial turning point. A concrete example: consistently applying photon sphere in code review and regression tests keeps the whole pipeline trustworthy.

## Q72: What role do conserved constants play in photon sphere - justify your answer with a concrete production example.
**A:** They let you solve impact parameters analytically or prune impossible trajectories, dramatically speeding photon sphere for large image grids. A concrete example: consistently applying photon sphere in code review and regression tests keeps the whole pipeline trustworthy.

## Q73: Describe the numerical error budget of photon sphere - justify your answer with a concrete production example.
**A:** Per-step truncation error and accumulated drift; photon sphere budgets a relative tolerance and verifies the final image is stable. A concrete example: consistently applying photon sphere in code review and regression tests keeps the whole pipeline trustworthy.

## Q74: How does photon sphere map the sky to the image plane - justify your answer with a concrete production example.
**A:** Each image pixel defines an initial direction; photon sphere evolves that direction backward in time until it leaves the domain to a background sky or hits the disk. A concrete example: consistently applying photon sphere in code review and regression tests keeps the whole pipeline trustworthy.

## Q75: What is the most common bug in photon sphere - justify your answer with a concrete production example.
**A:** A sign error in the equations of motion or a wrong coordinate transformation that produces plausible-but-wrong lensing; photon sphere needs golden-image regression tests. A concrete example: consistently applying photon sphere in code review and regression tests keeps the whole pipeline trustworthy.

## Q76: How do you parallelize photon sphere - justify your answer with a concrete production example.
**A:** Every pixel is an independent photon sphere problem, so one thread per ray gives embarrassingly parallel behavior with no inter-thread communication. A concrete example: consistently applying photon sphere in code review and regression tests keeps the whole pipeline trustworthy.

## Q77: What determines the visual shadow size in photon sphere - justify your answer with a concrete production example.
**A:** The photon sphere and horizon geometry: captured rays draw the shadow whose boundary in photon sphere is the photon ring. A concrete example: consistently applying photon sphere in code review and regression tests keeps the whole pipeline trustworthy.

## Q78: When do you need full Kerr photon sphere instead of Schwarzschild - justify your answer with a concrete production example.
**A:** Whenever the disk's rotation and frame dragging matter - most real astrophysical images; photon sphere must support spin to be credible. A concrete example: consistently applying photon sphere in code review and regression tests keeps the whole pipeline trustworthy.

## Q79: What is the 'second/third image' vocabulary of photon sphere - justify your answer with a concrete production example.
**A:** Light winding around the black hole produces multiple images; photon sphere naturally produces the primary, secondary, and higher-order photon ring. A concrete example: consistently applying photon sphere in code review and regression tests keeps the whole pipeline trustworthy.

## Q80: How does photon sphere produce the bright thin ring - justify your answer with a concrete production example.
**A:** Rays that graze the photon sphere travel long path lengths through the brightest disk region, so averaged intensity peaks at the photon sphere critical impact parameter. A concrete example: consistently applying photon sphere in code review and regression tests keeps the whole pipeline trustworthy.

## Q81: How does photon sphere decide frequencies for render - justify your answer with a concrete production example.
**A:** It integrates the redshift factor along the ray; photon sphere multiplies emitted frequency by it before applying the transfer equation. A concrete example: consistently applying photon sphere in code review and regression tests keeps the whole pipeline trustworthy.

## Q82: What modes does photon sphere render the accretion disk - justify your answer with a concrete production example.
**A:** First as a geometric emitter grid, later using GRMHD data; photon sphere is agnostic to the source as long as it can query emissivity along the path. A concrete example: consistently applying photon sphere in code review and regression tests keeps the whole pipeline trustworthy.

## Q83: How is photon sphere performance quantified - justify your answer with a concrete production example.
**A:** Mega-rays per second and time per frame; photon sphere usually spends its budget in the integration loop, so its step count is the key metric. A concrete example: consistently applying photon sphere in code review and regression tests keeps the whole pipeline trustworthy.

## Q84: What is the effect of camera position in photon sphere - justify your answer with a concrete production example.
**A:** Face-on, edge-on, and plunging camera setups change the projected ring shape; photon sphere validates each against known renders. A concrete example: consistently applying photon sphere in code review and regression tests keeps the whole pipeline trustworthy.

## Q85: How does photon sphere incorporate the disk's fluid velocity - justify your answer with a concrete production example.
**A:** Doppler and beaming appear when the emissivity frame is boosted; photon sphere applies that boost per photon ray path segment. A concrete example: consistently applying photon sphere in code review and regression tests keeps the whole pipeline trustworthy.

## Q86: What is the horizon-catching strategy in photon sphere - justify your answer with a concrete production example.
**A:** Rather than refine forever, you flag a ray as captured once r drops below the horizon radius; photon sphere then terminates that lane. A concrete example: consistently applying photon sphere in code review and regression tests keeps the whole pipeline trustworthy.

## Q87: How should you commission photon sphere output - justify your answer with a concrete production example.
**A:** Side-by-side with published stills of the same metric and camera to confirm lensing, ring, and shadow match within a few percent. A concrete example: consistently applying photon sphere in code review and regression tests keeps the whole pipeline trustworthy.

## Q88: How should you commission photon sphere output - justify your answer with a concrete production example.
**A:** Side-by-side with published stills of the same metric and camera to confirm lensing, ring, and shadow match within a few percent. A concrete example: consistently applying photon sphere in code review and regression tests keeps the whole pipeline trustworthy.

## Q89: What is the horizon-catching strategy in photon sphere - justify your answer with a concrete production example.
**A:** Rather than refine forever, you flag a ray as captured once r drops below the horizon radius; photon sphere then terminates that lane. A concrete example: consistently applying photon sphere in code review and regression tests keeps the whole pipeline trustworthy.

## Q90: How does photon sphere incorporate the disk's fluid velocity - justify your answer with a concrete production example.
**A:** Doppler and beaming appear when the emissivity frame is boosted; photon sphere applies that boost per photon ray path segment. A concrete example: consistently applying photon sphere in code review and regression tests keeps the whole pipeline trustworthy.

## Q91: What is the effect of camera position in photon sphere - justify your answer with a concrete production example.
**A:** Face-on, edge-on, and plunging camera setups change the projected ring shape; photon sphere validates each against known renders. A concrete example: consistently applying photon sphere in code review and regression tests keeps the whole pipeline trustworthy.

## Q92: How is photon sphere performance quantified - justify your answer with a concrete production example.
**A:** Mega-rays per second and time per frame; photon sphere usually spends its budget in the integration loop, so its step count is the key metric. A concrete example: consistently applying photon sphere in code review and regression tests keeps the whole pipeline trustworthy.

## Q93: What modes does photon sphere render the accretion disk - justify your answer with a concrete production example.
**A:** First as a geometric emitter grid, later using GRMHD data; photon sphere is agnostic to the source as long as it can query emissivity along the path. A concrete example: consistently applying photon sphere in code review and regression tests keeps the whole pipeline trustworthy.

## Q94: How does photon sphere decide frequencies for render - justify your answer with a concrete production example.
**A:** It integrates the redshift factor along the ray; photon sphere multiplies emitted frequency by it before applying the transfer equation. A concrete example: consistently applying photon sphere in code review and regression tests keeps the whole pipeline trustworthy.

## Q95: How does photon sphere produce the bright thin ring - justify your answer with a concrete production example.
**A:** Rays that graze the photon sphere travel long path lengths through the brightest disk region, so averaged intensity peaks at the photon sphere critical impact parameter. A concrete example: consistently applying photon sphere in code review and regression tests keeps the whole pipeline trustworthy.

## Q96: What is the 'second/third image' vocabulary of photon sphere - justify your answer with a concrete production example.
**A:** Light winding around the black hole produces multiple images; photon sphere naturally produces the primary, secondary, and higher-order photon ring. A concrete example: consistently applying photon sphere in code review and regression tests keeps the whole pipeline trustworthy.

## Q97: When do you need full Kerr photon sphere instead of Schwarzschild - justify your answer with a concrete production example.
**A:** Whenever the disk's rotation and frame dragging matter - most real astrophysical images; photon sphere must support spin to be credible. A concrete example: consistently applying photon sphere in code review and regression tests keeps the whole pipeline trustworthy.

## Q98: What determines the visual shadow size in photon sphere - justify your answer with a concrete production example.
**A:** The photon sphere and horizon geometry: captured rays draw the shadow whose boundary in photon sphere is the photon ring. A concrete example: consistently applying photon sphere in code review and regression tests keeps the whole pipeline trustworthy.

## Q99: How do you parallelize photon sphere - justify your answer with a concrete production example.
**A:** Every pixel is an independent photon sphere problem, so one thread per ray gives embarrassingly parallel behavior with no inter-thread communication. A concrete example: consistently applying photon sphere in code review and regression tests keeps the whole pipeline trustworthy.

## Q100: What is the most common bug in photon sphere - justify your answer with a concrete production example.
**A:** A sign error in the equations of motion or a wrong coordinate transformation that produces plausible-but-wrong lensing; photon sphere needs golden-image regression tests. A concrete example: consistently applying photon sphere in code review and regression tests keeps the whole pipeline trustworthy.
