# Relativity — Light Bending Interview Questions and Answers

## Q1: What is light bending?
**A:** A photon's path curves in the curved geometry even though it has no mass; the deflection angle for a ray grazing a mass M at impact parameter b is delta = 4M/b (weak field).

## Q2: What is the famous solar test?
**A:** Eddington 1919 measured ~1.75 arcsec for a ray grazed at the Sun's limb - matching 4GM/(R c^2), the first confirmation of general relativity.

## Q3: How does bending produce the Einstein ring?
**A:** When source, lens, and observer align, the deflection folds light into an annulus on the sky - the ring geometry reproduced in micro-images and black-hole silhouettes.

## Q4: What is the 'fold' scale for a black hole?
**A:** Near the photon sphere, bending becomes arbitrarily large: many loops around the hole before escape - the multiply-lensed images of the disk.

## Q5: How does the code compute deflection?
**A:** It doesn't invoke a formula; integrating the null geodesics naturally produces every deflection, from 4M/b asymptotes to the wildly wound photon spheres.

## Q6: What causes the shadow's circular boundary?
**A:** Impact parameters with b slightly inside the photon sphere orbit produce uni-directional capture; the boundary at b_crit projects as the shadow edge.

## Q7: What is lensing magnification?
**A:** Deflection refocuses rays: the solid angle of an image differs from the source - brightness scales with the inverse magnification, factor becoming huge near the ring.

## Q8: How does bending warp the disk appearance?
**A:** The far side of the disk is visibly pulled above and below the hole (a secondary image arch) - the 'lensed wall' that makes black-hole images unmistakable.

## Q9: What is the 'photon ring' in lensing terms?
**A:** The photon sphere's relative lensing of the disk at high orders: each additional 2pi winding produces one more thin bright ring, logarithmically spaced.

## Q10: What is the deflection vs impact parameter plot?
**A:** delta (b) rises from 4M/b asymptote to infinity at b_crit - the canonical lensing curve that validation tests reproduce numerically.

## Q11: How do you map sky to image for a far observer?
**A:** Each pixel's direction gives (b, angle); the ray's deflection is implicitly computed by tracing - the image plane is a map of impact parameters.

## Q12: What is the strong-field version of the formula?
**A:** The exact deflection involves elliptic integrals that diverge at b=b_crit (the ring) with a -log(b - b_crit) behavior - the analytic anchor for integrator tests.

## Q13: Why does the arriving ray from behind appear bent over the top?
**A:** Rays from the far disk that pass just outside the photon sphere get lifted over the hole - the cue that produces the characteristic 'arch' of the secondary image.

## Q14: What is an image of the Einstein ring demonstration?
**A:** A bright point behind the hole becomes an Einstein ring radius r_E = sqrt(4M*D_source...) - the simplest 'lensed object' the raytracer can showcase.

## Q15: How do you validate the bending?
**A:** Trace a family of rays with b = 10..100 M and check delta matches 4M/b to 1% (weak field), and compare the shadow+ring against analytic ray-fixed (Bradbury) figures.

## Q16: What is the physical meaning of light bending in general relativity?
**A:** It encodes how spacetime geometry responds to mass-energy; light bending ties local measurements in a freely falling frame to the global curved geometry.

## Q17: How is light bending expressed mathematically?
**A:** Through the metric tensor and its derivatives; light bending gives the equations of motion for particles and light as geodesics of that metric.

## Q18: Why does light bending matter for a black-hole raytracer?
**A:** Photons follow null geodesics of the Kerr geometry; light bending tells you exactly how to advance a ray in Boyer-Lindquist coordinates.

## Q19: What is the intuition behind light bending for a beginner?
**A:** Spacetime tells matter how to move and matter tells spacetime how to curve; light bending is the first concrete step of that program.

## Q20: How do you verify a calculation of light bending?
**A:** Take non-relativistic or weak-field limits, compare with known analytic results such as light bending, and check conservation laws numerically.

## Q21: How does light bending connect to special relativity?
**A:** In the absence of gravity the metric is Minkowski, and light bending reduces to Lorentz transformations and the usual Doppler formulas.

## Q22: What are the units and conventions for light bending?
**A:** geometric units with c=G=1 make masses length-like; careful sign conventions (mostly-plus vs mostly-minus) pervade light bending formulas.

## Q23: Give the classic demonstrative example of light bending.
**A:** A light ray grazing the Sun bends by 1.75 arcseconds; exact light bending reproduces this and more dramatic bending near a horizon.

## Q24: What is a common misconception about light bending?
**A:** That gravity is a force deflecting light; really light bending is geometry: light follows the straightest possible path in curved spacetime.

## Q25: How does light bending generalize for rotating black holes?
**A:** The stationary axisymmetric Kerr metric replaces spherical symmetry; light bending gains a spin parameter and frame dragging enters.

## Q26: What physical predictions come straight from light bending?
**A:** Gravitational redshift, perihelion precession, light bending, frame dragging, and orbital decay from gravitational waves are all light bending consequences.

## Q27: What is the role of conserved quantities in light bending?
**A:** Symmetries of the metric give constants along geodesics - energy, angular momentum, and (in Kerr) the Carter constant - which light bending uses to integrate efficiently.

## Q28: How would a detector measure effects of light bending?
**A:** Comparing clock rates, precision astrometry, or the shape of the photon ring all isolate signatures of light bending.

## Q29: What numerical care does light bending require?
**A:** The metric functions diverge at horizons and the coordinate singularities; switching to Kerr-Schild coordinates stabilizes light bending integration.

## Q30: How does light bending guide frame transformations in rendering?
**A:** Radiation emitted in the fluid frame must be Lorentz-transformed to the coordinate frame; light bending supplies the needed boost toward a locally non-rotating observer.

## Q31: Why start with Schwarzschild before Kerr for light bending?
**A:** Schwarzschild is spherically symmetric with simple constants, so light bending concepts are demonstrated and validated before spin complicates them.

## Q32: What is the embedding-diagram view of light bending?
**A:** A 2D slice of the geometry drawn inside a fictional flat space shows the funnel shape that beginners intuitively associate with light bending.

## Q33: What limits are placed by light bending on observables?
**A:** Nothing escapes inside the horizon; the photon sphere at 1.5 Schwarzschild radii bounds where light bending says circular light orbits exist.

## Q34: How do you test the weak-field limit of light bending?
**A:** Expanding the metric at large radius must recover Newtonian gravity plus the leading post-Newtonian corrections - the sanity check for light bending.

## Q35: What does light bending say about time near a black hole?
**A:** Clocks run slower deeper in the potential; light bending quantifies the ratio for a distant observer as the inverse redshift factor.

## Q36: How is light bending typically mis-stated in pop science?
**A:** As 'light has no mass so how does gravity pull it' - light bending reframes it as path curvature, not a force on mass.

## Q37: What documentation accompanies light bending in a research code?
**A:** Every derivation, coordinate convention, and unit choice for light bending is written down so the integrator can be audited.

## Q38: Give one number a beginner should memorize for light bending.
**A:** The photon sphere radius 3GM/C^2 (1.5 Schwarzschild radii) beyond which light bending orbiting light is possible.

## Q39: What is the next step after mastering light bending?
**A:** Coding the geodesic integrator that light bending equations describe - the leap from theory to ray-traced pictures.

## Q40: What is the next step after mastering light bending - justify your answer with a concrete production example.
**A:** Coding the geodesic integrator that light bending equations describe - the leap from theory to ray-traced pictures. A concrete example: consistently applying light bending in code review and regression tests keeps the whole pipeline trustworthy.

## Q41: Give one number a beginner should memorize for light bending - justify your answer with a concrete production example.
**A:** The photon sphere radius 3GM/C^2 (1.5 Schwarzschild radii) beyond which light bending orbiting light is possible. A concrete example: consistently applying light bending in code review and regression tests keeps the whole pipeline trustworthy.

## Q42: What documentation accompanies light bending in a research code - justify your answer with a concrete production example.
**A:** Every derivation, coordinate convention, and unit choice for light bending is written down so the integrator can be audited. A concrete example: consistently applying light bending in code review and regression tests keeps the whole pipeline trustworthy.

## Q43: How is light bending typically mis-stated in pop science - justify your answer with a concrete production example.
**A:** As 'light has no mass so how does gravity pull it' - light bending reframes it as path curvature, not a force on mass. A concrete example: consistently applying light bending in code review and regression tests keeps the whole pipeline trustworthy.

## Q44: What does light bending say about time near a black hole - justify your answer with a concrete production example.
**A:** Clocks run slower deeper in the potential; light bending quantifies the ratio for a distant observer as the inverse redshift factor. A concrete example: consistently applying light bending in code review and regression tests keeps the whole pipeline trustworthy.

## Q45: How do you test the weak-field limit of light bending - justify your answer with a concrete production example.
**A:** Expanding the metric at large radius must recover Newtonian gravity plus the leading post-Newtonian corrections - the sanity check for light bending. A concrete example: consistently applying light bending in code review and regression tests keeps the whole pipeline trustworthy.

## Q46: What limits are placed by light bending on observables - justify your answer with a concrete production example.
**A:** Nothing escapes inside the horizon; the photon sphere at 1.5 Schwarzschild radii bounds where light bending says circular light orbits exist. A concrete example: consistently applying light bending in code review and regression tests keeps the whole pipeline trustworthy.

## Q47: What is the embedding-diagram view of light bending - justify your answer with a concrete production example.
**A:** A 2D slice of the geometry drawn inside a fictional flat space shows the funnel shape that beginners intuitively associate with light bending. A concrete example: consistently applying light bending in code review and regression tests keeps the whole pipeline trustworthy.

## Q48: Why start with Schwarzschild before Kerr for light bending - justify your answer with a concrete production example.
**A:** Schwarzschild is spherically symmetric with simple constants, so light bending concepts are demonstrated and validated before spin complicates them. A concrete example: consistently applying light bending in code review and regression tests keeps the whole pipeline trustworthy.

## Q49: How does light bending guide frame transformations in rendering - justify your answer with a concrete production example.
**A:** Radiation emitted in the fluid frame must be Lorentz-transformed to the coordinate frame; light bending supplies the needed boost toward a locally non-rotating observer. A concrete example: consistently applying light bending in code review and regression tests keeps the whole pipeline trustworthy.

## Q50: What numerical care does light bending require - justify your answer with a concrete production example.
**A:** The metric functions diverge at horizons and the coordinate singularities; switching to Kerr-Schild coordinates stabilizes light bending integration. A concrete example: consistently applying light bending in code review and regression tests keeps the whole pipeline trustworthy.

## Q51: How would a detector measure effects of light bending - justify your answer with a concrete production example.
**A:** Comparing clock rates, precision astrometry, or the shape of the photon ring all isolate signatures of light bending. A concrete example: consistently applying light bending in code review and regression tests keeps the whole pipeline trustworthy.

## Q52: What is the role of conserved quantities in light bending - justify your answer with a concrete production example.
**A:** Symmetries of the metric give constants along geodesics - energy, angular momentum, and (in Kerr) the Carter constant - which light bending uses to integrate efficiently. A concrete example: consistently applying light bending in code review and regression tests keeps the whole pipeline trustworthy.

## Q53: What physical predictions come straight from light bending - justify your answer with a concrete production example.
**A:** Gravitational redshift, perihelion precession, light bending, frame dragging, and orbital decay from gravitational waves are all light bending consequences. A concrete example: consistently applying light bending in code review and regression tests keeps the whole pipeline trustworthy.

## Q54: How does light bending generalize for rotating black holes - justify your answer with a concrete production example.
**A:** The stationary axisymmetric Kerr metric replaces spherical symmetry; light bending gains a spin parameter and frame dragging enters. A concrete example: consistently applying light bending in code review and regression tests keeps the whole pipeline trustworthy.

## Q55: What is a common misconception about light bending - justify your answer with a concrete production example.
**A:** That gravity is a force deflecting light; really light bending is geometry: light follows the straightest possible path in curved spacetime. A concrete example: consistently applying light bending in code review and regression tests keeps the whole pipeline trustworthy.

## Q56: Give the classic demonstrative example of light bending - justify your answer with a concrete production example.
**A:** A light ray grazing the Sun bends by 1.75 arcseconds; exact light bending reproduces this and more dramatic bending near a horizon. A concrete example: consistently applying light bending in code review and regression tests keeps the whole pipeline trustworthy.

## Q57: What are the units and conventions for light bending - justify your answer with a concrete production example.
**A:** geometric units with c=G=1 make masses length-like; careful sign conventions (mostly-plus vs mostly-minus) pervade light bending formulas. A concrete example: consistently applying light bending in code review and regression tests keeps the whole pipeline trustworthy.

## Q58: How does light bending connect to special relativity - justify your answer with a concrete production example.
**A:** In the absence of gravity the metric is Minkowski, and light bending reduces to Lorentz transformations and the usual Doppler formulas. A concrete example: consistently applying light bending in code review and regression tests keeps the whole pipeline trustworthy.

## Q59: How do you verify a calculation of light bending - justify your answer with a concrete production example.
**A:** Take non-relativistic or weak-field limits, compare with known analytic results such as light bending, and check conservation laws numerically. A concrete example: consistently applying light bending in code review and regression tests keeps the whole pipeline trustworthy.

## Q60: What is the intuition behind light bending for a beginner - justify your answer with a concrete production example.
**A:** Spacetime tells matter how to move and matter tells spacetime how to curve; light bending is the first concrete step of that program. A concrete example: consistently applying light bending in code review and regression tests keeps the whole pipeline trustworthy.

## Q61: Why does light bending matter for a black-hole raytracer - justify your answer with a concrete production example.
**A:** Photons follow null geodesics of the Kerr geometry; light bending tells you exactly how to advance a ray in Boyer-Lindquist coordinates. A concrete example: consistently applying light bending in code review and regression tests keeps the whole pipeline trustworthy.

## Q62: How is light bending expressed mathematically - justify your answer with a concrete production example.
**A:** Through the metric tensor and its derivatives; light bending gives the equations of motion for particles and light as geodesics of that metric. A concrete example: consistently applying light bending in code review and regression tests keeps the whole pipeline trustworthy.

## Q63: What is the physical meaning of light bending in general relativity - justify your answer with a concrete production example.
**A:** It encodes how spacetime geometry responds to mass-energy; light bending ties local measurements in a freely falling frame to the global curved geometry. A concrete example: consistently applying light bending in code review and regression tests keeps the whole pipeline trustworthy.

## Q64: What is the physical meaning of light bending in general relativity - justify your answer with a concrete production example.
**A:** It encodes how spacetime geometry responds to mass-energy; light bending ties local measurements in a freely falling frame to the global curved geometry. A concrete example: consistently applying light bending in code review and regression tests keeps the whole pipeline trustworthy.

## Q65: How is light bending expressed mathematically - justify your answer with a concrete production example.
**A:** Through the metric tensor and its derivatives; light bending gives the equations of motion for particles and light as geodesics of that metric. A concrete example: consistently applying light bending in code review and regression tests keeps the whole pipeline trustworthy.

## Q66: Why does light bending matter for a black-hole raytracer - justify your answer with a concrete production example.
**A:** Photons follow null geodesics of the Kerr geometry; light bending tells you exactly how to advance a ray in Boyer-Lindquist coordinates. A concrete example: consistently applying light bending in code review and regression tests keeps the whole pipeline trustworthy.

## Q67: What is the intuition behind light bending for a beginner - justify your answer with a concrete production example.
**A:** Spacetime tells matter how to move and matter tells spacetime how to curve; light bending is the first concrete step of that program. A concrete example: consistently applying light bending in code review and regression tests keeps the whole pipeline trustworthy.

## Q68: How do you verify a calculation of light bending - justify your answer with a concrete production example.
**A:** Take non-relativistic or weak-field limits, compare with known analytic results such as light bending, and check conservation laws numerically. A concrete example: consistently applying light bending in code review and regression tests keeps the whole pipeline trustworthy.

## Q69: How does light bending connect to special relativity - justify your answer with a concrete production example.
**A:** In the absence of gravity the metric is Minkowski, and light bending reduces to Lorentz transformations and the usual Doppler formulas. A concrete example: consistently applying light bending in code review and regression tests keeps the whole pipeline trustworthy.

## Q70: What are the units and conventions for light bending - justify your answer with a concrete production example.
**A:** geometric units with c=G=1 make masses length-like; careful sign conventions (mostly-plus vs mostly-minus) pervade light bending formulas. A concrete example: consistently applying light bending in code review and regression tests keeps the whole pipeline trustworthy.

## Q71: Give the classic demonstrative example of light bending - justify your answer with a concrete production example.
**A:** A light ray grazing the Sun bends by 1.75 arcseconds; exact light bending reproduces this and more dramatic bending near a horizon. A concrete example: consistently applying light bending in code review and regression tests keeps the whole pipeline trustworthy.

## Q72: What is a common misconception about light bending - justify your answer with a concrete production example.
**A:** That gravity is a force deflecting light; really light bending is geometry: light follows the straightest possible path in curved spacetime. A concrete example: consistently applying light bending in code review and regression tests keeps the whole pipeline trustworthy.

## Q73: How does light bending generalize for rotating black holes - justify your answer with a concrete production example.
**A:** The stationary axisymmetric Kerr metric replaces spherical symmetry; light bending gains a spin parameter and frame dragging enters. A concrete example: consistently applying light bending in code review and regression tests keeps the whole pipeline trustworthy.

## Q74: What physical predictions come straight from light bending - justify your answer with a concrete production example.
**A:** Gravitational redshift, perihelion precession, light bending, frame dragging, and orbital decay from gravitational waves are all light bending consequences. A concrete example: consistently applying light bending in code review and regression tests keeps the whole pipeline trustworthy.

## Q75: What is the role of conserved quantities in light bending - justify your answer with a concrete production example.
**A:** Symmetries of the metric give constants along geodesics - energy, angular momentum, and (in Kerr) the Carter constant - which light bending uses to integrate efficiently. A concrete example: consistently applying light bending in code review and regression tests keeps the whole pipeline trustworthy.

## Q76: How would a detector measure effects of light bending - justify your answer with a concrete production example.
**A:** Comparing clock rates, precision astrometry, or the shape of the photon ring all isolate signatures of light bending. A concrete example: consistently applying light bending in code review and regression tests keeps the whole pipeline trustworthy.

## Q77: What numerical care does light bending require - justify your answer with a concrete production example.
**A:** The metric functions diverge at horizons and the coordinate singularities; switching to Kerr-Schild coordinates stabilizes light bending integration. A concrete example: consistently applying light bending in code review and regression tests keeps the whole pipeline trustworthy.

## Q78: How does light bending guide frame transformations in rendering - justify your answer with a concrete production example.
**A:** Radiation emitted in the fluid frame must be Lorentz-transformed to the coordinate frame; light bending supplies the needed boost toward a locally non-rotating observer. A concrete example: consistently applying light bending in code review and regression tests keeps the whole pipeline trustworthy.

## Q79: Why start with Schwarzschild before Kerr for light bending - justify your answer with a concrete production example.
**A:** Schwarzschild is spherically symmetric with simple constants, so light bending concepts are demonstrated and validated before spin complicates them. A concrete example: consistently applying light bending in code review and regression tests keeps the whole pipeline trustworthy.

## Q80: What is the embedding-diagram view of light bending - justify your answer with a concrete production example.
**A:** A 2D slice of the geometry drawn inside a fictional flat space shows the funnel shape that beginners intuitively associate with light bending. A concrete example: consistently applying light bending in code review and regression tests keeps the whole pipeline trustworthy.

## Q81: What limits are placed by light bending on observables - justify your answer with a concrete production example.
**A:** Nothing escapes inside the horizon; the photon sphere at 1.5 Schwarzschild radii bounds where light bending says circular light orbits exist. A concrete example: consistently applying light bending in code review and regression tests keeps the whole pipeline trustworthy.

## Q82: How do you test the weak-field limit of light bending - justify your answer with a concrete production example.
**A:** Expanding the metric at large radius must recover Newtonian gravity plus the leading post-Newtonian corrections - the sanity check for light bending. A concrete example: consistently applying light bending in code review and regression tests keeps the whole pipeline trustworthy.

## Q83: What does light bending say about time near a black hole - justify your answer with a concrete production example.
**A:** Clocks run slower deeper in the potential; light bending quantifies the ratio for a distant observer as the inverse redshift factor. A concrete example: consistently applying light bending in code review and regression tests keeps the whole pipeline trustworthy.

## Q84: How is light bending typically mis-stated in pop science - justify your answer with a concrete production example.
**A:** As 'light has no mass so how does gravity pull it' - light bending reframes it as path curvature, not a force on mass. A concrete example: consistently applying light bending in code review and regression tests keeps the whole pipeline trustworthy.

## Q85: What documentation accompanies light bending in a research code - justify your answer with a concrete production example.
**A:** Every derivation, coordinate convention, and unit choice for light bending is written down so the integrator can be audited. A concrete example: consistently applying light bending in code review and regression tests keeps the whole pipeline trustworthy.

## Q86: Give one number a beginner should memorize for light bending - justify your answer with a concrete production example.
**A:** The photon sphere radius 3GM/C^2 (1.5 Schwarzschild radii) beyond which light bending orbiting light is possible. A concrete example: consistently applying light bending in code review and regression tests keeps the whole pipeline trustworthy.

## Q87: What is the next step after mastering light bending - justify your answer with a concrete production example.
**A:** Coding the geodesic integrator that light bending equations describe - the leap from theory to ray-traced pictures. A concrete example: consistently applying light bending in code review and regression tests keeps the whole pipeline trustworthy.

## Q88: What is the next step after mastering light bending - justify your answer with a concrete production example.
**A:** Coding the geodesic integrator that light bending equations describe - the leap from theory to ray-traced pictures. A concrete example: consistently applying light bending in code review and regression tests keeps the whole pipeline trustworthy.

## Q89: Give one number a beginner should memorize for light bending - justify your answer with a concrete production example.
**A:** The photon sphere radius 3GM/C^2 (1.5 Schwarzschild radii) beyond which light bending orbiting light is possible. A concrete example: consistently applying light bending in code review and regression tests keeps the whole pipeline trustworthy.

## Q90: What documentation accompanies light bending in a research code - justify your answer with a concrete production example.
**A:** Every derivation, coordinate convention, and unit choice for light bending is written down so the integrator can be audited. A concrete example: consistently applying light bending in code review and regression tests keeps the whole pipeline trustworthy.

## Q91: How is light bending typically mis-stated in pop science - justify your answer with a concrete production example.
**A:** As 'light has no mass so how does gravity pull it' - light bending reframes it as path curvature, not a force on mass. A concrete example: consistently applying light bending in code review and regression tests keeps the whole pipeline trustworthy.

## Q92: What does light bending say about time near a black hole - justify your answer with a concrete production example.
**A:** Clocks run slower deeper in the potential; light bending quantifies the ratio for a distant observer as the inverse redshift factor. A concrete example: consistently applying light bending in code review and regression tests keeps the whole pipeline trustworthy.

## Q93: How do you test the weak-field limit of light bending - justify your answer with a concrete production example.
**A:** Expanding the metric at large radius must recover Newtonian gravity plus the leading post-Newtonian corrections - the sanity check for light bending. A concrete example: consistently applying light bending in code review and regression tests keeps the whole pipeline trustworthy.

## Q94: What limits are placed by light bending on observables - justify your answer with a concrete production example.
**A:** Nothing escapes inside the horizon; the photon sphere at 1.5 Schwarzschild radii bounds where light bending says circular light orbits exist. A concrete example: consistently applying light bending in code review and regression tests keeps the whole pipeline trustworthy.

## Q95: What is the embedding-diagram view of light bending - justify your answer with a concrete production example.
**A:** A 2D slice of the geometry drawn inside a fictional flat space shows the funnel shape that beginners intuitively associate with light bending. A concrete example: consistently applying light bending in code review and regression tests keeps the whole pipeline trustworthy.

## Q96: Why start with Schwarzschild before Kerr for light bending - justify your answer with a concrete production example.
**A:** Schwarzschild is spherically symmetric with simple constants, so light bending concepts are demonstrated and validated before spin complicates them. A concrete example: consistently applying light bending in code review and regression tests keeps the whole pipeline trustworthy.

## Q97: How does light bending guide frame transformations in rendering - justify your answer with a concrete production example.
**A:** Radiation emitted in the fluid frame must be Lorentz-transformed to the coordinate frame; light bending supplies the needed boost toward a locally non-rotating observer. A concrete example: consistently applying light bending in code review and regression tests keeps the whole pipeline trustworthy.

## Q98: What numerical care does light bending require - justify your answer with a concrete production example.
**A:** The metric functions diverge at horizons and the coordinate singularities; switching to Kerr-Schild coordinates stabilizes light bending integration. A concrete example: consistently applying light bending in code review and regression tests keeps the whole pipeline trustworthy.

## Q99: How would a detector measure effects of light bending - justify your answer with a concrete production example.
**A:** Comparing clock rates, precision astrometry, or the shape of the photon ring all isolate signatures of light bending. A concrete example: consistently applying light bending in code review and regression tests keeps the whole pipeline trustworthy.

## Q100: What is the role of conserved quantities in light bending - justify your answer with a concrete production example.
**A:** Symmetries of the metric give constants along geodesics - energy, angular momentum, and (in Kerr) the Carter constant - which light bending uses to integrate efficiently. A concrete example: consistently applying light bending in code review and regression tests keeps the whole pipeline trustworthy.
