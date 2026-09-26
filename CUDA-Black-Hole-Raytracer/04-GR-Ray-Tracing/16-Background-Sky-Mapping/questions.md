# Gr Ray Tracing — Background Sky Mapping Interview Questions and Answers

## Q1: What is the background sky?
**A:** The celestial sphere of distant stars/galaxies mapped to each pixel via ray propagation; an essential realism layer and a tool to expose lensing.

## Q2: How do you map a sky to a pixel?
**A:** The ray's initial direction gives the sky coordinate (equatorial/azimuthal angles); the far-field deflection maps arrival to emission direction - 'where did this photon come from'.

## Q3: What is the 'sky map' transform?
**A:** A map from image pixel (x,y) to source direction (theta_src, phi_src); for weak lensing it's nearly identity, near the hole it's wildly wrapped - visualized as star trails.

## Q4: How do stars look near the shadow?
**A:** Sources near the ring wrap multiple times - stars appear as winding arcs/smirches; the realistic starfield is the best intuitive lensing demo.

## Q5: How do you attach a sky texture?
**A:** Sample a cubemap/panorama from the far-field direction of a MISS ray; capture-mode rays get sky color, hit-mode rays get disk emission.

## Q6: What credit does the sky give to the geometry?
**A:** A uniform-grid starfield rotated by the lens, when compared to the analytic deflection map, validates the far-field behavior of the integrator.

## Q7: How do you render a static background (no disk)?
**A:** Classic: rays miss -> sky; capture -> black shadow. The resulting 'shadow-in-stars' image is the textbook demonstration of the code.

## Q8: What is the isocenter of the sky magnification pattern?
**A:** Just outside the shadow, sky regions are magnified (star trails expand); inside they're hidden - the map shows the classic Einstein-ring annulus of stars.

## Q9: How do you handle very distant sources with lenses?
**A:** The single deflection picture is enough: each star = one source ray; the code launches per-pixel rays and maps them - no extra lens equation needed.

## Q10: What does high-L imaging give?
**A:** The map wraps: sources at angles many M/D behind the hole appear at multiple image positions (the 'rail' of the photon ring in star maps).

## Q11: What is the practical texture format?
**A:** Equirectangular 4096x2048 or cubemap; sampling at far-field theta/phi in float precision keeps aliasing away from the critical lines.

## Q12: How do you add a CMB-like large-scale background?
**A:** Use a gridded background sphere; the code maps all rays to it - providing the robust far-field anchor for ray-direction bookkeeping.

## Q13: What is the visual paradox (ring of stars vs shadow)?
**A:** The star trails form a ring at r_E just outside the shadow, AGREEING with the analytic Einstein ring; the shadow remains black - a self-checking display.

## Q14: How does supersampling help the sky?
**A:** Stars are point-like: without supersampling they alias. Multi-ray per pixel plus motion blur smears star arcs appropriately - a feature, not a bug.

## Q15: What is the golden end-to-end test?
**A:** Render 'shadow-on-starfield': compare the sky-mapped star positions analytically across a grid; any star displaced outside its analytic deflection = smash-bug.

## Q16: What does background sky mapping concretely do inside the raytracer?
**A:** It advances photon trajectories in the curved spacetime, applying the equations of motion so each camera ray follows a true null geodesic.

## Q17: Why is background sky mapping the heart of a black-hole visualizer?
**A:** Every visual signature - lensing, photon ring, shadow, redshift - emerges from exactly how background sky mapping bends and time-shifts each ray.

## Q18: How is background sky mapping implemented on the GPU?
**A:** As a numerical integration loop in device code with per-ray state in registers, stepping through background sky mapping until the ray is captured or escapes.

## Q19: What are the two families of integration for background sky mapping?
**A:** The direct geodesic integration of the equations of motion, and Hamilton-Jacobi reduced systems using conserved constants; background sky mapping chooses per codebase.

## Q20: How do you validate background sky mapping?
**A:** Reproduce the analytic Schwarzschild lensing angle, the photon ring, and the projected shadow shape measured against published figures.

## Q21: What is the typical step-size strategy in background sky mapping?
**A:** Adaptive stepping that refines near the photon sphere and the horizon, where background sky mapping gradients are steepest and error grows fastest.

## Q22: What state does the integrator track for background sky mapping?
**A:** Position, four-momentum components, affine parameter, and accumulated redshift - background sky mapping state vector is small enough to fit in registers.

## Q23: How does background sky mapping handle captured photons?
**A:** It terminates integration at the horizon and records absorption; background sky mapping distinguishes capture from scatter by the radial turning point.

## Q24: What role do conserved constants play in background sky mapping?
**A:** They let you solve impact parameters analytically or prune impossible trajectories, dramatically speeding background sky mapping for large image grids.

## Q25: Describe the numerical error budget of background sky mapping.
**A:** Per-step truncation error and accumulated drift; background sky mapping budgets a relative tolerance and verifies the final image is stable.

## Q26: How does background sky mapping map the sky to the image plane?
**A:** Each image pixel defines an initial direction; background sky mapping evolves that direction backward in time until it leaves the domain to a background sky or hits the disk.

## Q27: What is the most common bug in background sky mapping?
**A:** A sign error in the equations of motion or a wrong coordinate transformation that produces plausible-but-wrong lensing; background sky mapping needs golden-image regression tests.

## Q28: How do you parallelize background sky mapping?
**A:** Every pixel is an independent background sky mapping problem, so one thread per ray gives embarrassingly parallel behavior with no inter-thread communication.

## Q29: What determines the visual shadow size in background sky mapping?
**A:** The photon sphere and horizon geometry: captured rays draw the shadow whose boundary in background sky mapping is the photon ring.

## Q30: When do you need full Kerr background sky mapping instead of Schwarzschild?
**A:** Whenever the disk's rotation and frame dragging matter - most real astrophysical images; background sky mapping must support spin to be credible.

## Q31: What is the 'second/third image' vocabulary of background sky mapping?
**A:** Light winding around the black hole produces multiple images; background sky mapping naturally produces the primary, secondary, and higher-order photon ring.

## Q32: How does background sky mapping produce the bright thin ring?
**A:** Rays that graze the photon sphere travel long path lengths through the brightest disk region, so averaged intensity peaks at the background sky mapping critical impact parameter.

## Q33: How does background sky mapping decide frequencies for render?
**A:** It integrates the redshift factor along the ray; background sky mapping multiplies emitted frequency by it before applying the transfer equation.

## Q34: What modes does background sky mapping render the accretion disk?
**A:** First as a geometric emitter grid, later using GRMHD data; background sky mapping is agnostic to the source as long as it can query emissivity along the path.

## Q35: How is background sky mapping performance quantified?
**A:** Mega-rays per second and time per frame; background sky mapping usually spends its budget in the integration loop, so its step count is the key metric.

## Q36: What is the effect of camera position in background sky mapping?
**A:** Face-on, edge-on, and plunging camera setups change the projected ring shape; background sky mapping validates each against known renders.

## Q37: How does background sky mapping incorporate the disk's fluid velocity?
**A:** Doppler and beaming appear when the emissivity frame is boosted; background sky mapping applies that boost per photon ray path segment.

## Q38: What is the horizon-catching strategy in background sky mapping?
**A:** Rather than refine forever, you flag a ray as captured once r drops below the horizon radius; background sky mapping then terminates that lane.

## Q39: How should you commission background sky mapping output?
**A:** Side-by-side with published stills of the same metric and camera to confirm lensing, ring, and shadow match within a few percent.

## Q40: How should you commission background sky mapping output - justify your answer with a concrete production example.
**A:** Side-by-side with published stills of the same metric and camera to confirm lensing, ring, and shadow match within a few percent. A concrete example: consistently applying background sky mapping in code review and regression tests keeps the whole pipeline trustworthy.

## Q41: What is the horizon-catching strategy in background sky mapping - justify your answer with a concrete production example.
**A:** Rather than refine forever, you flag a ray as captured once r drops below the horizon radius; background sky mapping then terminates that lane. A concrete example: consistently applying background sky mapping in code review and regression tests keeps the whole pipeline trustworthy.

## Q42: How does background sky mapping incorporate the disk's fluid velocity - justify your answer with a concrete production example.
**A:** Doppler and beaming appear when the emissivity frame is boosted; background sky mapping applies that boost per photon ray path segment. A concrete example: consistently applying background sky mapping in code review and regression tests keeps the whole pipeline trustworthy.

## Q43: What is the effect of camera position in background sky mapping - justify your answer with a concrete production example.
**A:** Face-on, edge-on, and plunging camera setups change the projected ring shape; background sky mapping validates each against known renders. A concrete example: consistently applying background sky mapping in code review and regression tests keeps the whole pipeline trustworthy.

## Q44: How is background sky mapping performance quantified - justify your answer with a concrete production example.
**A:** Mega-rays per second and time per frame; background sky mapping usually spends its budget in the integration loop, so its step count is the key metric. A concrete example: consistently applying background sky mapping in code review and regression tests keeps the whole pipeline trustworthy.

## Q45: What modes does background sky mapping render the accretion disk - justify your answer with a concrete production example.
**A:** First as a geometric emitter grid, later using GRMHD data; background sky mapping is agnostic to the source as long as it can query emissivity along the path. A concrete example: consistently applying background sky mapping in code review and regression tests keeps the whole pipeline trustworthy.

## Q46: How does background sky mapping decide frequencies for render - justify your answer with a concrete production example.
**A:** It integrates the redshift factor along the ray; background sky mapping multiplies emitted frequency by it before applying the transfer equation. A concrete example: consistently applying background sky mapping in code review and regression tests keeps the whole pipeline trustworthy.

## Q47: How does background sky mapping produce the bright thin ring - justify your answer with a concrete production example.
**A:** Rays that graze the photon sphere travel long path lengths through the brightest disk region, so averaged intensity peaks at the background sky mapping critical impact parameter. A concrete example: consistently applying background sky mapping in code review and regression tests keeps the whole pipeline trustworthy.

## Q48: What is the 'second/third image' vocabulary of background sky mapping - justify your answer with a concrete production example.
**A:** Light winding around the black hole produces multiple images; background sky mapping naturally produces the primary, secondary, and higher-order photon ring. A concrete example: consistently applying background sky mapping in code review and regression tests keeps the whole pipeline trustworthy.

## Q49: When do you need full Kerr background sky mapping instead of Schwarzschild - justify your answer with a concrete production example.
**A:** Whenever the disk's rotation and frame dragging matter - most real astrophysical images; background sky mapping must support spin to be credible. A concrete example: consistently applying background sky mapping in code review and regression tests keeps the whole pipeline trustworthy.

## Q50: What determines the visual shadow size in background sky mapping - justify your answer with a concrete production example.
**A:** The photon sphere and horizon geometry: captured rays draw the shadow whose boundary in background sky mapping is the photon ring. A concrete example: consistently applying background sky mapping in code review and regression tests keeps the whole pipeline trustworthy.

## Q51: How do you parallelize background sky mapping - justify your answer with a concrete production example.
**A:** Every pixel is an independent background sky mapping problem, so one thread per ray gives embarrassingly parallel behavior with no inter-thread communication. A concrete example: consistently applying background sky mapping in code review and regression tests keeps the whole pipeline trustworthy.

## Q52: What is the most common bug in background sky mapping - justify your answer with a concrete production example.
**A:** A sign error in the equations of motion or a wrong coordinate transformation that produces plausible-but-wrong lensing; background sky mapping needs golden-image regression tests. A concrete example: consistently applying background sky mapping in code review and regression tests keeps the whole pipeline trustworthy.

## Q53: How does background sky mapping map the sky to the image plane - justify your answer with a concrete production example.
**A:** Each image pixel defines an initial direction; background sky mapping evolves that direction backward in time until it leaves the domain to a background sky or hits the disk. A concrete example: consistently applying background sky mapping in code review and regression tests keeps the whole pipeline trustworthy.

## Q54: Describe the numerical error budget of background sky mapping - justify your answer with a concrete production example.
**A:** Per-step truncation error and accumulated drift; background sky mapping budgets a relative tolerance and verifies the final image is stable. A concrete example: consistently applying background sky mapping in code review and regression tests keeps the whole pipeline trustworthy.

## Q55: What role do conserved constants play in background sky mapping - justify your answer with a concrete production example.
**A:** They let you solve impact parameters analytically or prune impossible trajectories, dramatically speeding background sky mapping for large image grids. A concrete example: consistently applying background sky mapping in code review and regression tests keeps the whole pipeline trustworthy.

## Q56: How does background sky mapping handle captured photons - justify your answer with a concrete production example.
**A:** It terminates integration at the horizon and records absorption; background sky mapping distinguishes capture from scatter by the radial turning point. A concrete example: consistently applying background sky mapping in code review and regression tests keeps the whole pipeline trustworthy.

## Q57: What state does the integrator track for background sky mapping - justify your answer with a concrete production example.
**A:** Position, four-momentum components, affine parameter, and accumulated redshift - background sky mapping state vector is small enough to fit in registers. A concrete example: consistently applying background sky mapping in code review and regression tests keeps the whole pipeline trustworthy.

## Q58: What is the typical step-size strategy in background sky mapping - justify your answer with a concrete production example.
**A:** Adaptive stepping that refines near the photon sphere and the horizon, where background sky mapping gradients are steepest and error grows fastest. A concrete example: consistently applying background sky mapping in code review and regression tests keeps the whole pipeline trustworthy.

## Q59: How do you validate background sky mapping - justify your answer with a concrete production example.
**A:** Reproduce the analytic Schwarzschild lensing angle, the photon ring, and the projected shadow shape measured against published figures. A concrete example: consistently applying background sky mapping in code review and regression tests keeps the whole pipeline trustworthy.

## Q60: What are the two families of integration for background sky mapping - justify your answer with a concrete production example.
**A:** The direct geodesic integration of the equations of motion, and Hamilton-Jacobi reduced systems using conserved constants; background sky mapping chooses per codebase. A concrete example: consistently applying background sky mapping in code review and regression tests keeps the whole pipeline trustworthy.

## Q61: How is background sky mapping implemented on the GPU - justify your answer with a concrete production example.
**A:** As a numerical integration loop in device code with per-ray state in registers, stepping through background sky mapping until the ray is captured or escapes. A concrete example: consistently applying background sky mapping in code review and regression tests keeps the whole pipeline trustworthy.

## Q62: Why is background sky mapping the heart of a black-hole visualizer - justify your answer with a concrete production example.
**A:** Every visual signature - lensing, photon ring, shadow, redshift - emerges from exactly how background sky mapping bends and time-shifts each ray. A concrete example: consistently applying background sky mapping in code review and regression tests keeps the whole pipeline trustworthy.

## Q63: What does background sky mapping concretely do inside the raytracer - justify your answer with a concrete production example.
**A:** It advances photon trajectories in the curved spacetime, applying the equations of motion so each camera ray follows a true null geodesic. A concrete example: consistently applying background sky mapping in code review and regression tests keeps the whole pipeline trustworthy.

## Q64: What does background sky mapping concretely do inside the raytracer - justify your answer with a concrete production example.
**A:** It advances photon trajectories in the curved spacetime, applying the equations of motion so each camera ray follows a true null geodesic. A concrete example: consistently applying background sky mapping in code review and regression tests keeps the whole pipeline trustworthy.

## Q65: Why is background sky mapping the heart of a black-hole visualizer - justify your answer with a concrete production example.
**A:** Every visual signature - lensing, photon ring, shadow, redshift - emerges from exactly how background sky mapping bends and time-shifts each ray. A concrete example: consistently applying background sky mapping in code review and regression tests keeps the whole pipeline trustworthy.

## Q66: How is background sky mapping implemented on the GPU - justify your answer with a concrete production example.
**A:** As a numerical integration loop in device code with per-ray state in registers, stepping through background sky mapping until the ray is captured or escapes. A concrete example: consistently applying background sky mapping in code review and regression tests keeps the whole pipeline trustworthy.

## Q67: What are the two families of integration for background sky mapping - justify your answer with a concrete production example.
**A:** The direct geodesic integration of the equations of motion, and Hamilton-Jacobi reduced systems using conserved constants; background sky mapping chooses per codebase. A concrete example: consistently applying background sky mapping in code review and regression tests keeps the whole pipeline trustworthy.

## Q68: How do you validate background sky mapping - justify your answer with a concrete production example.
**A:** Reproduce the analytic Schwarzschild lensing angle, the photon ring, and the projected shadow shape measured against published figures. A concrete example: consistently applying background sky mapping in code review and regression tests keeps the whole pipeline trustworthy.

## Q69: What is the typical step-size strategy in background sky mapping - justify your answer with a concrete production example.
**A:** Adaptive stepping that refines near the photon sphere and the horizon, where background sky mapping gradients are steepest and error grows fastest. A concrete example: consistently applying background sky mapping in code review and regression tests keeps the whole pipeline trustworthy.

## Q70: What state does the integrator track for background sky mapping - justify your answer with a concrete production example.
**A:** Position, four-momentum components, affine parameter, and accumulated redshift - background sky mapping state vector is small enough to fit in registers. A concrete example: consistently applying background sky mapping in code review and regression tests keeps the whole pipeline trustworthy.

## Q71: How does background sky mapping handle captured photons - justify your answer with a concrete production example.
**A:** It terminates integration at the horizon and records absorption; background sky mapping distinguishes capture from scatter by the radial turning point. A concrete example: consistently applying background sky mapping in code review and regression tests keeps the whole pipeline trustworthy.

## Q72: What role do conserved constants play in background sky mapping - justify your answer with a concrete production example.
**A:** They let you solve impact parameters analytically or prune impossible trajectories, dramatically speeding background sky mapping for large image grids. A concrete example: consistently applying background sky mapping in code review and regression tests keeps the whole pipeline trustworthy.

## Q73: Describe the numerical error budget of background sky mapping - justify your answer with a concrete production example.
**A:** Per-step truncation error and accumulated drift; background sky mapping budgets a relative tolerance and verifies the final image is stable. A concrete example: consistently applying background sky mapping in code review and regression tests keeps the whole pipeline trustworthy.

## Q74: How does background sky mapping map the sky to the image plane - justify your answer with a concrete production example.
**A:** Each image pixel defines an initial direction; background sky mapping evolves that direction backward in time until it leaves the domain to a background sky or hits the disk. A concrete example: consistently applying background sky mapping in code review and regression tests keeps the whole pipeline trustworthy.

## Q75: What is the most common bug in background sky mapping - justify your answer with a concrete production example.
**A:** A sign error in the equations of motion or a wrong coordinate transformation that produces plausible-but-wrong lensing; background sky mapping needs golden-image regression tests. A concrete example: consistently applying background sky mapping in code review and regression tests keeps the whole pipeline trustworthy.

## Q76: How do you parallelize background sky mapping - justify your answer with a concrete production example.
**A:** Every pixel is an independent background sky mapping problem, so one thread per ray gives embarrassingly parallel behavior with no inter-thread communication. A concrete example: consistently applying background sky mapping in code review and regression tests keeps the whole pipeline trustworthy.

## Q77: What determines the visual shadow size in background sky mapping - justify your answer with a concrete production example.
**A:** The photon sphere and horizon geometry: captured rays draw the shadow whose boundary in background sky mapping is the photon ring. A concrete example: consistently applying background sky mapping in code review and regression tests keeps the whole pipeline trustworthy.

## Q78: When do you need full Kerr background sky mapping instead of Schwarzschild - justify your answer with a concrete production example.
**A:** Whenever the disk's rotation and frame dragging matter - most real astrophysical images; background sky mapping must support spin to be credible. A concrete example: consistently applying background sky mapping in code review and regression tests keeps the whole pipeline trustworthy.

## Q79: What is the 'second/third image' vocabulary of background sky mapping - justify your answer with a concrete production example.
**A:** Light winding around the black hole produces multiple images; background sky mapping naturally produces the primary, secondary, and higher-order photon ring. A concrete example: consistently applying background sky mapping in code review and regression tests keeps the whole pipeline trustworthy.

## Q80: How does background sky mapping produce the bright thin ring - justify your answer with a concrete production example.
**A:** Rays that graze the photon sphere travel long path lengths through the brightest disk region, so averaged intensity peaks at the background sky mapping critical impact parameter. A concrete example: consistently applying background sky mapping in code review and regression tests keeps the whole pipeline trustworthy.

## Q81: How does background sky mapping decide frequencies for render - justify your answer with a concrete production example.
**A:** It integrates the redshift factor along the ray; background sky mapping multiplies emitted frequency by it before applying the transfer equation. A concrete example: consistently applying background sky mapping in code review and regression tests keeps the whole pipeline trustworthy.

## Q82: What modes does background sky mapping render the accretion disk - justify your answer with a concrete production example.
**A:** First as a geometric emitter grid, later using GRMHD data; background sky mapping is agnostic to the source as long as it can query emissivity along the path. A concrete example: consistently applying background sky mapping in code review and regression tests keeps the whole pipeline trustworthy.

## Q83: How is background sky mapping performance quantified - justify your answer with a concrete production example.
**A:** Mega-rays per second and time per frame; background sky mapping usually spends its budget in the integration loop, so its step count is the key metric. A concrete example: consistently applying background sky mapping in code review and regression tests keeps the whole pipeline trustworthy.

## Q84: What is the effect of camera position in background sky mapping - justify your answer with a concrete production example.
**A:** Face-on, edge-on, and plunging camera setups change the projected ring shape; background sky mapping validates each against known renders. A concrete example: consistently applying background sky mapping in code review and regression tests keeps the whole pipeline trustworthy.

## Q85: How does background sky mapping incorporate the disk's fluid velocity - justify your answer with a concrete production example.
**A:** Doppler and beaming appear when the emissivity frame is boosted; background sky mapping applies that boost per photon ray path segment. A concrete example: consistently applying background sky mapping in code review and regression tests keeps the whole pipeline trustworthy.

## Q86: What is the horizon-catching strategy in background sky mapping - justify your answer with a concrete production example.
**A:** Rather than refine forever, you flag a ray as captured once r drops below the horizon radius; background sky mapping then terminates that lane. A concrete example: consistently applying background sky mapping in code review and regression tests keeps the whole pipeline trustworthy.

## Q87: How should you commission background sky mapping output - justify your answer with a concrete production example.
**A:** Side-by-side with published stills of the same metric and camera to confirm lensing, ring, and shadow match within a few percent. A concrete example: consistently applying background sky mapping in code review and regression tests keeps the whole pipeline trustworthy.

## Q88: How should you commission background sky mapping output - justify your answer with a concrete production example.
**A:** Side-by-side with published stills of the same metric and camera to confirm lensing, ring, and shadow match within a few percent. A concrete example: consistently applying background sky mapping in code review and regression tests keeps the whole pipeline trustworthy.

## Q89: What is the horizon-catching strategy in background sky mapping - justify your answer with a concrete production example.
**A:** Rather than refine forever, you flag a ray as captured once r drops below the horizon radius; background sky mapping then terminates that lane. A concrete example: consistently applying background sky mapping in code review and regression tests keeps the whole pipeline trustworthy.

## Q90: How does background sky mapping incorporate the disk's fluid velocity - justify your answer with a concrete production example.
**A:** Doppler and beaming appear when the emissivity frame is boosted; background sky mapping applies that boost per photon ray path segment. A concrete example: consistently applying background sky mapping in code review and regression tests keeps the whole pipeline trustworthy.

## Q91: What is the effect of camera position in background sky mapping - justify your answer with a concrete production example.
**A:** Face-on, edge-on, and plunging camera setups change the projected ring shape; background sky mapping validates each against known renders. A concrete example: consistently applying background sky mapping in code review and regression tests keeps the whole pipeline trustworthy.

## Q92: How is background sky mapping performance quantified - justify your answer with a concrete production example.
**A:** Mega-rays per second and time per frame; background sky mapping usually spends its budget in the integration loop, so its step count is the key metric. A concrete example: consistently applying background sky mapping in code review and regression tests keeps the whole pipeline trustworthy.

## Q93: What modes does background sky mapping render the accretion disk - justify your answer with a concrete production example.
**A:** First as a geometric emitter grid, later using GRMHD data; background sky mapping is agnostic to the source as long as it can query emissivity along the path. A concrete example: consistently applying background sky mapping in code review and regression tests keeps the whole pipeline trustworthy.

## Q94: How does background sky mapping decide frequencies for render - justify your answer with a concrete production example.
**A:** It integrates the redshift factor along the ray; background sky mapping multiplies emitted frequency by it before applying the transfer equation. A concrete example: consistently applying background sky mapping in code review and regression tests keeps the whole pipeline trustworthy.

## Q95: How does background sky mapping produce the bright thin ring - justify your answer with a concrete production example.
**A:** Rays that graze the photon sphere travel long path lengths through the brightest disk region, so averaged intensity peaks at the background sky mapping critical impact parameter. A concrete example: consistently applying background sky mapping in code review and regression tests keeps the whole pipeline trustworthy.

## Q96: What is the 'second/third image' vocabulary of background sky mapping - justify your answer with a concrete production example.
**A:** Light winding around the black hole produces multiple images; background sky mapping naturally produces the primary, secondary, and higher-order photon ring. A concrete example: consistently applying background sky mapping in code review and regression tests keeps the whole pipeline trustworthy.

## Q97: When do you need full Kerr background sky mapping instead of Schwarzschild - justify your answer with a concrete production example.
**A:** Whenever the disk's rotation and frame dragging matter - most real astrophysical images; background sky mapping must support spin to be credible. A concrete example: consistently applying background sky mapping in code review and regression tests keeps the whole pipeline trustworthy.

## Q98: What determines the visual shadow size in background sky mapping - justify your answer with a concrete production example.
**A:** The photon sphere and horizon geometry: captured rays draw the shadow whose boundary in background sky mapping is the photon ring. A concrete example: consistently applying background sky mapping in code review and regression tests keeps the whole pipeline trustworthy.

## Q99: How do you parallelize background sky mapping - justify your answer with a concrete production example.
**A:** Every pixel is an independent background sky mapping problem, so one thread per ray gives embarrassingly parallel behavior with no inter-thread communication. A concrete example: consistently applying background sky mapping in code review and regression tests keeps the whole pipeline trustworthy.

## Q100: What is the most common bug in background sky mapping - justify your answer with a concrete production example.
**A:** A sign error in the equations of motion or a wrong coordinate transformation that produces plausible-but-wrong lensing; background sky mapping needs golden-image regression tests. A concrete example: consistently applying background sky mapping in code review and regression tests keeps the whole pipeline trustworthy.
