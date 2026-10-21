# Framer Motion Interview Questions and Answers - Part 2

## Q1: How do you implement shared layout animations across different components using layoutId?
**A:** Use the `layoutId` prop to create shared layout animations between components. When two different components share the same `layoutId`, Framer Motion automatically animates between them when one unmounts and the other mounts. Wrap in <AnimatePresence> to enable exit animations. The `layoutId` creates a single animation identity across the component tree, so Framer Motion knows these represent the same UI element transitioning between states. This is the foundation of morphing layouts.

## Q2: How do you use the `layout` prop with layoutAnimation for smooth parent-child animations?
**A:** Adding `layout` to a motion component makes it automatically animate to its new position when layout changes due to re-renders. When a parent has `layout` and children change, the parent size animates smoothly. Use `transition={{ layout: { type: "spring", stiffness: 300, damping: 30 } }}` to customize the spring physics. Use `layout="position"` to only animate position for better performance, or `layout="size"` for dimensions only. The `layout` prop uses FLIP (First, Last, Invert, Play) technique internally.

## Q3: How do you implement drag with custom constraints and elastic boundaries?
**A:** Use `drag` prop with `dragConstraints` and `dragElastic`. `dragConstraints` defines boundaries as pixel values: `dragConstraints={{ left: 0, right: 300, top: 0, bottom: 300 }}`. `dragElastic` controls springy overshoot (0 = no elastic, 1 = max elastic): `dragElastic={0.2}` for subtle stretch. Use `dragMomentum={false}` to disable momentum scrolling. For custom bounds: use `dragConstraintsRef={ref}` with `useRef`. For spring-based constraints with resistance: use `dragTransition` to customize end-of-drag physics.

## Q4: How do you chain animations sequentially using transition delay and staggered children?
**A:** Use `staggerChildren` in parent variants: `variants={{ animate: { transition: { staggerChildren: 0.1, delayChildren: 0.3 } } }}`. For programmatic sequencing, use `useAnimate()`: `const [scope, animate] = useAnimate(); await animate(scope.current, { opacity: 0 }); await animate(scope.current, { x: 100 })`. This allows async/await style chaining of animations. For delay on a single element: `transition={{ duration: 0.5, delay: 1 }}`.

## Q5: How do you implement scroll-linked animations using useScroll and useTransform?
**A:** `useScroll()` returns `scrollY`, `scrollYProgress`, `scrollX`, `scrollXProgress`. `useTransform()` maps value ranges: `const scale = useTransform(scrollYProgress, [0, 1], [1, 0.5])`. For smoothness: `const smooth = useSpring(scrollYProgress, { stiffness: 100, damping: 30 })`. For element-specific progress: `useScroll({ target: articleRef, offset: ["start start", "end end"] })`. Combine with negative output ranges for parallax effects.

## Q6: How do you implement exit animations with AnimatePresence mode and custom keys?
**A:** <AnimatePresence mode="popLayout"> — mode options: "sync" (default), "popLayout" (exit element removed from layout flow), "wait" (exit before enter). Use `custom` prop for dynamic variants: `const variants = { enter: (dir) => ({ x: dir > 0 ? 300 : -300 }), exit: (dir) => ({ x: dir > 0 ? -300 : 300 }) }`. Use `onExitComplete` callback for side effects after all exit animations complete. The `key` prop must change to trigger re-animation.

## Q7: How do you create spring-based animations with custom physics parameters?
**A:** `transition={{ type: "spring", stiffness: 100, damping: 10, mass: 1 }}`. Higher stiffness = snappier. Higher damping = less bounce. Higher mass = heavier. For critical damping (no bounce): `damping >= 2 * sqrt(stiffness)`. For underdamped (bouncy): reduce damping. For overdamped (slow settle): increase damping. Use `velocity` for initial velocity: `transition={{ type: "spring", velocity: 1000 }}`. Spring feels more natural than tween in UI animations.

## Q8: How do you implement gesture-based interactions combining drag, hover, and tap?
**A:** Combine multiple gesture handlers: `<motion.div whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }} drag="x" dragConstraints={{ left: -100, right: 100 }} whileDrag={{ boxShadow: "0 10px 30px rgba(0,0,0,0.2)" }} onDragEnd={(_, info) => console.log(info.offset.x)} />`. `whileDrag` runs during drag. `whileHover` on hover. `whileTap` on press. Use `whileInView` for scroll-triggered animations.

## Q9: How do you use motion values directly with useMotionValue for high-performance animations?
**A:** `useMotionValue(0)` creates a thread-safe motion value that doesn't cause React re-renders. Use with `useSpring` and `useTransform` for derived values. Set imperatively: `x.set(100)` or `x.setWithVelocity(100, 500)`. Watch changes: `useMotionValueEvent(x, "change", (latest) => console.log(latest))`. Motion values can drive non-motion components. They are the building block for custom animations.

## Q10: How do you implement keyframe animations with multiple stops and custom timing?
**A:** Use arrays: `animate={{ x: [0, 100, 200, 100, 0], opacity: [1, 0.5, 1, 0.5, 1] }}`. For times: `transition={{ duration: 2, times: [0, 0.2, 0.5, 0.8, 1] }}`. For different easings per segment: `transition={{ ease: ["easeIn", "easeOut", "easeInOut", "linear"] }}`. For looping: `repeat: Infinity` with `repeatType: "loop" | "reverse" | "mirror"`. Keyframe arrays must all be the same length.

## Q11: How do you implement variants propagation with context-based overrides?
**A:** Parent sets `variants` and children inherit through the DOM tree. Children can override. Use `inherit={false}` to break inheritance. For dynamic variants, return a function: `const variants = { open: (custom) => ({ opacity: 1, x: custom }) }`. Pass via `custom={100}`. Variants propagate across AnimatePresence boundaries. For conditional: `animate={isOpen ? "open" : "closed"}`.

## Q12: How do you implement SVG path animations (draw on/draw off)?
**A:** Use `pathLength`, `pathSpacing`, `pathOffset`. Initial: `pathLength: 0`, animate to `pathLength: 1`: `<motion.path d="..." initial={{ pathLength: 0 }} animate={{ pathLength: 1 }} transition={{ duration: 2 }} />`. For draw off: animate from 1 to 0. For staggered multi-path: use `staggerChildren`. Works with circle, ellipse, line, path, polygon, polyline, rect. Path must be valid SVG without fill.

## Q13: How do you implement reduced motion accessibility?
**A:** Use `useReducedMotion()` hook: `const prefersReducedMotion = useReducedMotion()`. When true, disable animations. Wrap in `<MotionConfig reducedMotion="user">` for global setting. The `reducedMotion` prop accepts "always", "never", or "user". For critical context changes, still animate but remove decorative flourishes. Use CSS `@media (prefers-reduced-motion: reduce)` as fallback.

## Q14: How do you optimize performance for motion components in large lists?
**A:** Use `layoutDependency` to prevent unnecessary layout recalculations. Use `willChange="transform"` prop. Use `layoutScroll` for scrollable containers. For lists: `layout` on items with stable `key`. For drag: use `drag="x"` with `dragConstraints`. Avoid animating `width`/height — animate `scaleX`/scaleY instead. Use `useSpring` with `damping: 20`. For huge lists, use CSS transitions or virtualization.

## Q15: How do you implement AnimatePresence with custom callbacks for complex flows?
**A:** AnimatePresence lifecycle: `<AnimatePresence mode="wait" onExitComplete={() => console.log("done")}>`. Per element: `onAnimationStart` and `onAnimationComplete`. For pagination: trigger next page load in `onExitComplete`. For nested AnimatePresence, inner exits before outer. Use `initial={false}` to skip initial animation on mount. For waiting for specific children: use `uniqueKeys` prop.

## Q16: How do you implement drag with constraints based on element position and size?
**A:** `dragConstraints` as a function returning pixel values. `dragConstraintsRef={parentRef}` to constrain within parent. For grid snapping: `onDragEnd={(_, info) => { const snapX = Math.round(info.point.x / grid) * grid; x.set(snapX); }}`. For directional: `drag="x"` or `drag="y"`. For propagation within scrollable parents: `dragPropagation`. For inertial constraints: combine `dragMomentum` with `dragTransition={{ power: 0.2, timeConstant: 200 }}`.

## Q17: How do you use useSpring to smoothly interpolate rapidly changing values?
**A:** `useSpring` wraps a motion value: `const smoothX = useSpring(mouseX, { stiffness: 100, damping: 30 })`. This creates a lag effect. Combine with `useTransform`: `const rotateY = useTransform(smoothX, [0, window.innerWidth], [-10, 10])`. Zero damping creates infinite oscillation. High stiffness + high damping = near-instant response with no bounce. Essential for 3D parallax and cursor-follow effects.

## Q18: How do you implement viewport-based animations with whileInView?
**A:** `<motion.div initial={{ opacity: 0, y: 50 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true, amount: 0.3, margin: "-50px" }} />`. `viewport` options: `once` (animate once), `amount` (visible threshold 0-1), `margin` (IntersectionObserver root margin). For multiple thresholds: use `useInView()` hook. For staggered children: set `whileInView` on parent with `staggerChildren`.

## Q19: How do you implement animation composition with useAnimate?
**A:** `const [scope, animate] = useAnimate()`. Returns imperative pair. `await animate("li", { opacity: 1 }, { duration: 0.3 }); await animate(scope.current, { rotate: 360 }, { duration: 0.5 })`. Accepts CSS selector, motion value, or AnimationSequence. For sequences: `animate([["li", { opacity: 1 }, { duration: 0.3 }], [scope.current, { rotate: 360 }, { duration: 0.5 }]])`. Gives imperative control while keeping animation loop within Framer Motion.

## Q20: How do you implement gesture recognition for swipe-to-dismiss cards?
**A:** `const x = useMotionValue(0); const opacity = useTransform(x, [-200, 0, 200], [0, 1, 0]);` Set `drag="x"` with `dragConstraints={{ left: 0, right: 0 }}` and `dragElastic={0.7}`. On `onDragEnd`, if offset > 150, animate off screen; else snap back. Use `whileTap={{ scale: 0.95 }}` for press feedback. For stack: use `layoutId` and `<AnimatePresence>`. For undo: store dismissed item and animate back.

## Q21: How do you implement scroll-triggered progress bars?
**A:** `const { scrollYProgress } = useScroll(); const scaleX = useSpring(scrollYProgress, { stiffness: 100, damping: 30 }); return <motion.div style={{ position: "fixed", top: 0, height: "4px", transformOrigin: "0%", scaleX }} />`. For article-specific: `useScroll({ target: articleRef, offset: ["start start", "end end"] })`. For reading time: combine with `useTransform` for opacity gradient.

## Q22: How do you implement flip animations for reordered list items?
**A:** Use `layout` prop on list items with stable keys. When list reorders, items animate to new position: `<motion.li key={item.id} layout transition={{ type: "spring", stiffness: 300 }}>`. Wrap in `<AnimatePresence>` for enter/exit. For performance: `layout="position"` to skip size animation. For grid reorder: `layout` handles FLIP computation automatically.

## Q23: How do you implement 3D transforms with perspective and rotateX/rotateY?
**A:** `<motion.div whileHover={{ rotateX: 10, rotateY: 10, scale: 1.05 }} style={{ perspective: 1000 }}>`. For cursor-follow 3D tilt: convert mouse position to normalized coordinates and map to rotation via `useTransform`. Use `transformStyle: "preserve-3d"` for nested 3D children. `perspective` on parent for shared vanishing point.

## Q24: How do you implement AnimatePresence with route transitions in Next.js?
**A:** Wrap page with `<AnimatePresence mode="wait">` using `key={router.asPath}`. Each page: `initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -20 }}`. For shared layout animations: use `layoutId` on elements present in both pages. Use `<LayoutRouter>` for proper AnimatePresence with Next.js. Disable scroll restoration.

## Q25: How do you implement parallax scrolling with multiple layers at different speeds?
**A:** Use `useScroll` and `useTransform` per layer: `const y1 = useTransform(scrollY, [0, 1000], [0, -200]); const y2 = useTransform(scrollY, [0, 1000], [0, -100])`. Far background: slow, foreground: fast. For horizontal: `scrollX`. For mouse parallax: use mouse position. Smooth with `useSpring`. For image-only: animate `backgroundPosition` instead of y for better performance.

## Q26: How do you implement drag-to-reorder with Framer Motion?
**A:** Use `<Reorder.Group>`: `<Reorder.Group axis="y" values={items} onReorder={setItems}>{items.map(item => <Reorder.Item key={item.id} value={item}>{item.name}</Reorder.Item>)}</Reorder.Group>`. The `Reorder` component handles FLIP calculations, drag constraints, and position snapping automatically. Supports axis="x", "y", or "xy".

## Q27: How do you use MotionConfig to set global animation defaults?
**A:** `<MotionConfig transition={{ type: "spring", stiffness: 300, damping: 20 }} reducedMotion="user" nonce="random123"><App /></MotionConfig>`. Sets default transition, reduced motion policy, and CSP nonce. Override at any child level. Use `MotionConfigContext` to read config. For testing: `transition={{ duration: 0 }}` to disable all animations.

## Q28: How do you implement measuring element dimensions with useMotionValue?
**A:** Combine with ResizeObserver: `const width = useMotionValue(0); const ref = useCallback((node) => { if (node) { const observer = new ResizeObserver(([entry]) => { width.set(entry.contentRect.width); }); observer.observe(node); } }, [])`. Use measured values to drive other animations. For animating to specific height, `layout` prop is more efficient.

## Q29: How do you implement gesture-based drag with rotation (Tinder cards)?
**A:** `const rotate = useTransform(x, [-300, 0, 300], [-30, 0, 30]); const opacity = useTransform(x, [-300, -100, 0, 100, 300], [0, 1, 1, 1, 0]);` Set `drag="x"` with `dragConstraints={{ left: 0, right: 0 }}`. On drag end, swipe off screen if offset > threshold, or snap back. For stack: subsequent cards `scale: 0.95, y: 10`.

## Q30: How do you implement animation that responds to scroll velocity?
**A:** Calculate velocity from `scrollY`: `const velocity = useMotionValue(0); useMotionValueEvent(scrollY, "change", (latest) => { velocity.set((latest - prevY.get()) / 16); prevY.set(latest); })`. Map to animation: `const scale = useTransform(velocity, [-100, 0, 100], [1.2, 1, 1.2])`. Or use `useSpring` damping for implicit velocity. Fast scroll = more intensity.

## Q31: How do you implement useAnimationControls for complex orchestration?
**A:** `const controls = useAnimationControls(); const sequence = async () => { await controls.start({ scale: 1.5 }); await controls.start({ rotate: 90 }); await controls.start({ scale: 1, rotate: 0 }); }; return <motion.div animate={controls}>`. For staggering: `controls.start(i => ({ opacity: 1, transition: { delay: i * 0.1 } }))`. Use `controls.set()` for instant changes.

## Q32: How do you animate CSS custom properties with Framer Motion?
**A:** `<motion.div initial={{ "--x": "0px" }} animate={{ "--x": "100px" }} style={{ transform: "translateX(var(--x))" }} />`. Use for properties not directly supported (clip-path, background-position). Combine multiple CSS variables for complex animations. Cast for TypeScript: `animate={{ "--x": "100px" } as any}`.

## Q33: How do you implement overlapping entry animations with staggered timing?
**A:** Parent variants: `{ hidden: {}, visible: { transition: { staggerChildren: 0.15, delayChildren: 0.3 } } }`. Children: `{ hidden: { opacity: 0, y: 20 }, visible: { opacity: 1, y: 0 } }`. For overlap: stagger < child duration. For directional stagger: use `custom` with computed delays. For random stagger: use staggerRandom or custom function.

## Q34: How do you implement color and background-color animation?
**A:** `<motion.div animate={{ backgroundColor: "#ff0000", color: "#fff" }} />`. Supports hex, rgb, rgba, hsl, hsla, named colors. For gradients: animate CSS variables for stop positions. For backgroundPosition: use `backgroundPosition: "0% 50%"`. Prefer opacity and transform over color for performance.

## Q35: How do you implement custom easing curves (cubic bezier)?
**A:** `transition={{ ease: [0.17, 0.67, 0.83, 0.67], duration: 0.5 }}`. Common: elastic [0.68, -0.55, 0.27, 1.55], smooth [0.25, 0.1, 0.25, 1]. Per-property: `transition={{ x: { ease: [0.17, 0.67, 0.83, 0.67] }, opacity: { ease: "linear" } }}`. For stepped: use keyframes with array times.

## Q36: How do you animate elements based on scroll progress through a specific section?
**A:** `const { scrollYProgress } = useScroll({ target: sectionRef, offset: ["start end", "end start"] }); const opacity = useTransform(scrollYProgress, [0, 0.3, 0.7, 1], [0, 1, 1, 0])`. Offset defines when animation starts/ends relative to viewport. Use `container` for scroll within an element: `useScroll({ container: scrollRef })`.

## Q37: How do you implement a typewriter animation effect?
**A:** Use `useAnimate` with a character-by-character approach: `const [scope, animate] = useAnimate(); const typeText = async (text) => { for (let i = 0; i <= text.length; i++) { scope.current.textContent = text.slice(0, i); await animate(scope.current, { opacity: [0.5, 1] }, { duration: 0.05 }); } }`. For cursor blink: `animate(".cursor", { opacity: [1, 0] }, { duration: 0.5, repeat: Infinity })`. For multiple strings: chain with delays.

## Q38: How do you implement drag with momentum and friction?
**A:** `drag="x"` with `dragTransition={{ power: 0.1, timeConstant: 200, modifyTarget: (target) => Math.round(target / 100) * 100 }}`. `power` controls momentum strength (0 = no momentum, 1 = full). `timeConstant` controls how long momentum lasts. `modifyTarget` for grid snapping: `Math.round(target / snap) * snap`. Use `dragMomentum={false}` to disable.

## Q39: How do you implement scroll-triggered sticky headers with animation?
**A:** Use `useScroll` and `useTransform` on a fixed-position element: `const { scrollY } = useScroll(); const y = useTransform(scrollY, [headerHeight, headerHeight], [0, -headerHeight])`. For sticky with reveal: `const opacity = useTransform(scrollY, [0, 200], [0, 1])`. For parallax sticky: layer multiple `useTransform` values. Combine with `position: sticky` and `layout` for smooth transitions.

## Q40: How do you implement animated route transitions with shared element morphing?
**A:** Use `layoutId` on elements shared across routes. Define variants for page enter/exit. In Next.js: `<AnimatePresence mode="wait"> <motion.div key={router.asPath} variants={pageVariants} initial="initial" animate="animate" exit="exit"> <Component /> </motion.div> </AnimatePresence>`. Shared elements get `layoutId` like "card-image" and morph between pages.

## Q41: How do you implement animation interruption and restart patterns?
**A:** Use `controls.stop()` to stop current animation. For restart: `controls.set({ x: 0, opacity: 0 }); controls.start({ x: 100, opacity: 1 })`. For interruptible hover: `whileHover={{ scale: 1.1, transition: { type: "spring", stiffness: 400 } }}`. For sequence restart: store animation promise and cancel via AbortController. For repeat with reset: `repeatType: "loop"` with `repeat: Infinity`.

## Q42: How do you implement gesture-based 3D card tilt effect?
**A:** `const x = useMotionValue(0); const y = useMotionValue(0); const rotateX = useTransform(y, [-0.5, 0.5], [15, -15]); const rotateY = useTransform(x, [-0.5, 0.5], [-15, 15]);` On mouse move: normalize position relative to card bounds. On mouse leave: animate back to zero with spring. Use `whileHover={{ scale: 1.02 }}` for depth. The glow effect: `background` radial gradient following mouse position via CSS variables.

## Q43: How do you implement animation sequences with timings based on previous animation completion?
**A:** Use `useAnimate` with async/await: `const seq = async () => { await animate(el, { x: 100 }); await animate(el, { rotate: 180 }); await animate(el, { scale: 1.5 }); }`. For parallel: `Promise.all([animate(el, { x: 100 }), animate(el2, { opacity: 1 })])`. For sequences: `animate([[el, { x: 100 }], [el, { rotate: 180 }]], { duration: 0.5, ease: "easeInOut" })`.

## Q44: How do you implement scroll-triggered horizontal scroll sections?
**A:** `const { scrollYProgress } = useScroll(); const x = useTransform(scrollYProgress, [0, 1], [0, -(sections * 100 - 100) + "vw"]); return <motion.div style={{ x, display: "flex" }}>`. Each section is `100vw` wide. For sticky container: `position: sticky; top: 0; height: 100vh; overflow: hidden;`. For pin-based horizontal scroll: `useTransform` maps vertical scroll to horizontal translate.

## Q45: How do you implement a custom gesture recognizer using motion values?
**A:** Track gesture state with motion values: `const dx = useMotionValue(0); const dy = useMotionValue(0); const isDragging = useMotionValue(0);` Use `onPointerDown`, `onPointerMove`, `onPointerUp` to update values. `const rotate = useTransform(dx, [-200, 200], [-45, 45]); const scale = useTransform(isDragging, [0, 1], [1, 1.05])`. For multi-touch: track multiple pointers. This gives complete control beyond built-in gestures.

## Q46: How do you implement layout animations with AnimatePresence for modal transitions?
**A:** `<AnimatePresence> {isOpen && <motion.div initial={{ opacity: 0, scale: 0.9 }} animate={{ opacity: 1, scale: 1 }} exit={{ opacity: 0, scale: 0.9 }} transition={{ type: "spring", stiffness: 300 }}> <motion.div layoutId="modal">content</motion.div> </motion.div> } </AnimatePresence>`. Overlay: fade with backdrop blur. Modal: spring scale and slide. Use `layoutId` for content that morphs to/from a trigger element.

## Q47: How do you implement drag with velocity-based color changes?
**A:** `const x = useMotionValue(0); const color = useTransform(x, [-200, 0, 200], ["#ff4444", "#ffffff", "#44ff44"]); const boxShadow = useTransform(x, [-200, 0, 200], ["0 0 20px rgba(255,0,0,0.5)", "none", "0 0 20px rgba(0,255,0,0.5)"]);` Color changes as the user drags, providing visual feedback. Use `whileDrag` for immediate feedback.

## Q48: How do you implement nested scrolling with different animation speeds?
**A:** `const { scrollY: outerScroll } = useScroll(); const { scrollY: innerScroll } = useScroll({ container: innerRef }); const combined = useTransform([outerScroll, innerScroll], ([outer, inner]) => outer * 0.5 + inner);` Use `useScroll` with `container` for inner scrollable areas. Combine scroll values with `useTransform` accepting arrays. Each scroll contributes at different weights.

## Q49: How do you implement accordion/collapse animations with AnimatePresence and layout?
**A:** `<AnimatePresence initial={false}> {isOpen && <motion.section key="content" initial={{ height: 0, opacity: 0 }} animate={{ height: "auto", opacity: 1 }} exit={{ height: 0, opacity: 0 }} transition={{ duration: 0.3 }}>content</motion.section> } </AnimatePresence>`. For smooth height: use `layout` on the container. For icon rotation: `animate={{ rotate: isOpen ? 180 : 0 }}`. Use `overflow: hidden` on the animated container.

## Q50: How do you implement a custom useInView hook with IntersectionObserver options?
**A:** Framer Motion provides `useInView(ref, options)`: `const ref = useRef(null); const isInView = useInView(ref, { once: true, amount: 0.5, margin: "-50px" })`. `once`: only trigger once. `amount`: visible ratio (0-1). `margin`: root margin. Combine with `useAnimate`: `useEffect(() => { if (isInView) animate(ref.current, { opacity: 1, y: 0 }); }, [isInView])`.

## Q51: How do you implement drag with multiple axes and rotation?
**A:** `drag="x"` limits to one axis. For free drag: `drag` (equivalent to `drag="xy"`). To add rotation to free drag: `const rotateX = useTransform(y, [-200, 200], [10, -10]); const rotateY = useTransform(x, [-200, 200], [-10, 10])`. For 3D card with drag: combine `drag` with perspective transform. Use `whileDrag={{ scale: 1.05 }}`.

## Q52: How do you implement animated counter/number transitions?
**A:** `const count = useMotionValue(0); const rounded = useTransform(count, Math.round); useMotionValueEvent(count, "change", (latest) => setDisplay(Math.round(latest))); useEffect(() => { const controls = animate(count, target, { duration: 2, ease: "easeOut" }); return controls.stop; }, [target])`. Or use `useSpring: const count = useSpring(0, { stiffness: 100, damping: 30 }); useMotionValueEvent(count, "change", (v) => setDisplay(Math.floor(v)))`.

## Q53: How do you implement exit animations for elements in a filtered list?
**A:** Wrap in `<AnimatePresence>` with unique `key` on each item. `{items.filter(condition).map(item => <motion.div key={item.id} layout initial={{ opacity: 0, scale: 0.8 }} animate={{ opacity: 1, scale: 1 }} exit={{ opacity: 0, scale: 0.8, transition: { duration: 0.2 } }}>`. Use `layout` for remaining items to animate to new positions. `mode="popLayout"` removes exited items from flow immediately.

## Q54: How do you implement a custom transition using animate function with timing functions?
**A:** `const [scope, animate] = useAnimate(); animate(scope.current, { x: [0, 200, 0], rotate: [0, 360, 0] }, { duration: 3, ease: ["easeIn", "easeOut"], times: [0, 0.5, 1], repeat: Infinity, repeatDelay: 0.5 })`. Supports per-property easing arrays, custom timings, and repeat options. For spring: `{ type: "spring", stiffness: 300, damping: 10 }`.

## Q55: How do you implement an animated gradient background with motion?
**A:** Use CSS variables: `<motion.div initial={{ "--gradient-pos": "0%" }} animate={{ "--gradient-pos": "100%" }} transition={{ duration: 10, repeat: Infinity, repeatType: "reverse" }} style={{ background: "linear-gradient(var(--gradient-pos), #667eea, #764ba2)" }} />`. For multi-stop: animate multiple CSS variables. For hue rotation: animate CSS `filter: hue-rotate()` or use `—hue` CSS variable.

## Q56: How do you implement spring animations with configurable bounce and stiffness?
**A:** `transition={{ type: "spring", stiffness: 300, damping: 10, mass: 1, velocity: 2 }}`. For no bounce: `damping: 100`. For max bounce: `damping: 5, stiffness: 200`. For heavy object: `mass: 3`. For initial velocity: `velocity: 100` makes it start fast then decelerate. For rubber band: `stiffness: 500, damping: 5`. For snap: `stiffness: 1000, damping: 50`.

## Q57: How do you implement scroll-triggered reveal animations with different delays for children?
**A:** Parent: `whileInView={{ opacity: 1 }} viewport={{ once: true }}`. Children: use `variants` with `staggerChildren`. `const container = { hidden: {}, visible: { transition: { staggerChildren: 0.1 } } }`. Each child: `const item = { hidden: { opacity: 0, y: 20 }, visible: { opacity: 1, y: 0 } }`. For cascade from different directions: use `custom` to pass index.

## Q58: How do you implement a progress-based animation where user can seek through timeline?
**A:** `const progress = useMotionValue(0); const x = useTransform(progress, [0, 1], [0, 300]); const opacity = useTransform(progress, [0, 0.5, 1], [0, 1, 0]);` Link to input: `<input type="range" min={0} max={1} step={0.01} onChange={(e) => progress.set(parseFloat(e.target.value))} />`. Use spring for smoothing: `useSpring(progress, { stiffness: 100, damping: 20 })`.

## Q59: How do you implement tap gesture with ripple effect?
**A:** Track tap position: `const [ripples, setRipples] = useState([]); const handleTap = (e) => { const rect = e.target.getBoundingClientRect(); const x = e.clientX - rect.left; const y = e.clientY - rect.top; setRipples(prev => [...prev, { x, y, id: Date.now() }]); }`. Render ripples: `<AnimatePresence>{ripples.map(r => <motion.span key={r.id} initial={{ scale: 0, opacity: 1, x: r.x, y: r.y }} animate={{ scale: 4, opacity: 0 }} exit={{ opacity: 0 }} onAnimationComplete={() => setRipples(prev => prev.filter(p => p.id !== r.id))} />)}</AnimatePresence>`.

## Q60: How do you implement animated box shadows and glow effects?
**A:** Animate boxShadow directly: `<motion.div animate={{ boxShadow: "0 20px 40px rgba(0,0,0,0.3)" }}>`. For glow: `animate={{ boxShadow: "0 0 30px rgba(99,102,241,0.5), 0 0 60px rgba(99,102,241,0.2)" }}`. For performance, prefer `filter: drop-shadow()` over boxShadow when possible. For pulsing glow: `transition={{ duration: 2, repeat: Infinity, repeatType: "reverse" }}`.

## Q61: How do you implement a parallax effect on scroll with multiple overlapping elements?
**A:** Create layers: `const { scrollY } = useScroll(); const y1 = useTransform(scrollY, [0, 1000], [0, -300]); const y2 = useTransform(scrollY, [0, 1000], [0, -150]); const y3 = useTransform(scrollY, [0, 1000], [0, -50]);`. Layer with z-index and different translate speeds. For depth: `scale: useTransform(scrollY, [0, 1000], [1, 1.2])` for far elements. Use `position: fixed` for background layers.

## Q62: How do you implement a collapse/expand animation with smooth height transition?
**A:** `<motion.div animate={{ height: isOpen ? height : 0, opacity: isOpen ? 1 : 0 }} transition={{ type: "spring", stiffness: 300, damping: 30 }}>`. For auto height (unknown content size): use `layout` prop instead: `<motion.div layout>`. Or measure with ref and animate to measured height: `const contentRef = useRef(null); const height = isOpen ? contentRef.current?.scrollHeight : 0`.

## Q63: How do you implement drag with rotation based on drag velocity?
**A:** `const { scrollY } = useScroll(); // alternative`, but for drag: `const x = useMotionValue(0); const rotate = useTransform(x, [-300, 0, 300], [-45, 0, 45]);`. For velocity-based rotation: `onDrag={(_, info) => { const velX = info.velocity.x; velocityBasedRotation.set(velX * 0.1); }}`. Use `dragElastic={0.5}` for springy resistance.

## Q64: How do you implement variant-based animations with logical AND/OR conditions?
**A:** Combine conditions to determine variant name: `const variantName = isOpen ? (isHovered ? "openHovered" : "open") : (isHovered ? "closedHovered" : "closed")`. Define all four variants: `{ open: {}, openHovered: {}, closed: {}, closedHovered: {} }`. For simpler logic: use `animate={{ opacity: isOpen ? (isHovered ? 0.8 : 1) : 0, scale: isOpen ? 1 : 0.9 }}`.

## Q65: How do you implement a marquee/infinite scroll animation?
**A:** `const x = useMotionValue(0); useEffect(() => { const controls = animate(x, [-contentWidth, 0], { duration: 20, repeat: Infinity, ease: "linear" }); return controls.stop; }, []); return <motion.div style={{ x }}>`. Duplicate content for seamless loop: render content twice. For pause on hover: `whileHover={{ animationPlayState: "paused" }}` via CSS or `onMouseEnter={() => controls.pause()}`.

## Q66: How do you implement AnimatePresence with stacked modals?
**A:** Nest `<AnimatePresence>` for each modal level. Each modal: `initial={{ opacity: 0, scale: 0.9, y: 20 }} animate={{ opacity: 1, scale: 1, y: 0 }} exit={{ opacity: 0, scale: 0.9, y: 20 }}`. For backdrop: `<motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} onClick={onClose} />`. Stack: each subsequent modal has `z-index` incrementing and appears on top.

## Q67: How do you implement a scroll-based animation that reverses on scroll up?
**A:** Framer Motion automatically reverses when using `useScroll` and `useTransform` since they're bound to current scroll position. `const { scrollYProgress } = useScroll(); const opacity = useTransform(scrollYProgress, [0, 0.5, 1], [0, 1, 0])`. The animation naturally reverses when scrolling back up. No additional logic needed. Use `useSpring` for smooth interpolation.

## Q68: How do you implement drag with elastic snap-back animation?
**A:** `dragElastic={0.8}` allows stretching beyond constraints. `dragConstraints={{ left: 0, right: 500 }}`. When released, spring animates back to bounds. Custom snap-back: `onDragEnd={(_, info) => { animate(x, 0, { type: "spring", stiffness: 300, damping: 20, velocity: info.velocity.x }); }`. The velocity prop makes snap-back feel natural with momentum.

## Q69: How do you implement an animated page transition with direction awareness?
**A:** `const [[page, direction], setPage] = useState([0, 0]); const variants = { enter: (dir) => ({ x: dir > 0 ? 500 : -500, opacity: 0 }), center: { x: 0, opacity: 1 }, exit: (dir) => ({ x: dir > 0 ? -500 : 500, opacity: 0 }) }`. Wrap in `<AnimatePresence custom={direction}>`. Use `custom={direction}` on page content.

## Q70: How do you implement a drag-to-resize pattern?
**A:** `const width = useMotionValue(200); useMotionValueEvent(x, "change", (latest) => { width.set(Math.max(100, 200 + latest)); }); return <motion.div drag="x" dragConstraints={{ left: 0 }} onDragEnd={() => animate(x, 0)} style={{ width }}>`. For corner resize: combine horizontal and vertical drag values. For aspect ratio lock: compute height from width.

## Q71: How do you implement a spring-based progress indicator with bounce?
**A:** `const progress = useSpring(0, { stiffness: 200, damping: 15 }); useEffect(() => { progress.set(1); }, []); const scaleX = useTransform(progress, [0, 0.5, 1], [0, 1.02, 1]);`. The spring overshoots slightly at the end then settles. For indeterminate progress: `animate(progress, [0, 1], { duration: 2, repeat: Infinity, ease: "easeInOut" })`.

## Q72: How do you implement a shake animation for form validation errors?
**A:** `const controls = useAnimationControls(); const shake = async () => { await controls.start({ x: [0, -10, 10, -10, 10, -5, 5, 0], transition: { duration: 0.5 } }); }; return <motion.input animate={controls} onAnimationComplete={() => controls.set({ x: 0 })} />`. Trigger on error: `useEffect(() => { if (error) shake(); }, [error])`. Combine with color change: `animate={{ borderColor: error ? "#ff0000" : "#ccc" }}`.

## Q73: How do you implement a highlight/pulse animation on page load?
**A:** `<motion.div initial={{ backgroundColor: "#fef3c7" }} animate={{ backgroundColor: "transparent" }} transition={{ duration: 1.5, ease: "easeOut" }}>`. For pulse: `animate={{ scale: [1, 1.02, 1], opacity: [0.8, 1, 0.8] }} transition={{ duration: 2, repeat: Infinity }}`. For attention: `whileInView={{ scale: [1, 1.1, 1], transition: { duration: 0.5 } }}`.

## Q74: How do you implement a custom animation that uses requestAnimationFrame with motion values?
**A:** Motion values integrate with RAF: `const x = useMotionValue(0); useEffect(() => { let frame; const update = () => { x.set(x.get() + 1); frame = requestAnimationFrame(update); }; frame = requestAnimationFrame(update); return () => cancelAnimationFrame(frame); }, [])`. Use `typeof animate !== "undefined" &&` guard for SSR. For performance, prefer Framer Motion's built-in `animate` over manual RAF.

## Q75: How do you implement gesture-based sortable grid with Reorder?
**A:** `<Reorder.Group axis="xy" values={items} onReorder={setItems} style={{ display: "grid", gridTemplateColumns: "repeat(3, 1fr)" }}> {items.map(item => <Reorder.Item key={item.id} value={item}><motion.div layout whileDrag={{ scale: 1.05, boxShadow: "0 10px 30px rgba(0,0,0,0.2)" }} />)</Reorder.Item>} </Reorder.Group>`. `axis="xy"` enables both directions. Grid auto-layout via CSS. Items animate to new positions during reorder.

## Q76: How do you implement scroll-linked opacity fade for a sticky header?
**A:** `const { scrollY } = useScroll(); const headerOpacity = useTransform(scrollY, [0, 100], [0, 1]); const headerY = useTransform(scrollY, [0, 100], [-50, 0]); return <motion.header style={{ position: "fixed", top: 0, width: "100%", opacity: headerOpacity, y: headerY }}>`. For background blur: `backdropFilter: useTransform(scrollY, [0, 100], ["blur(0px)", "blur(10px)"])`.

## Q77: How do you implement an animation that follows the cursor with delay?
**A:** `const mouseX = useMotionValue(0); const mouseY = useMotionValue(0); const smoothX = useSpring(mouseX, { stiffness: 50, damping: 20 }); const smoothY = useSpring(mouseY, { stiffness: 50, damping: 20 });` On mouse move, set mouseX/mouseY to client coordinates. The spring creates delay for trailing effect. For glow trail: render multiple elements with increasing delay using `staggerChildren`.

## Q78: How do you implement a skeleton loader animation with shimmer effect?
**A:** `const shimmer = { background: "linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%)", backgroundSize: "200% 100%" }`. Animate backgroundPosition: `<motion.div animate={{ backgroundPosition: ["200% 0", "-200% 0"] }} transition={{ duration: 1.5, repeat: Infinity, ease: "linear" }} style={shimmer} />`. For each skeleton item, stagger the animation start.

## Q79: How do you implement a text reveal animation (word by word or character by character)?
**A:** Split text into words/characters, wrap each in `<motion.span>` with `display: inline-block`. Parent: `variants={{ hidden: {}, visible: { transition: { staggerChildren: 0.04 } } }}`. Child: `variants={{ hidden: { opacity: 0, y: 20, rotateX: -90 }, visible: { opacity: 1, y: 0, rotateX: 0 } }}`. Use `whileInView` to trigger on scroll.

## Q80: How do you implement a floating animation (hover/bob effect)?
**A:** `<motion.div animate={{ y: [0, -10, 0] }} transition={{ duration: 3, repeat: Infinity, ease: "easeInOut" }}>`. For multiple elements with different timing: vary the duration and delay per element. For organic float: `animate={{ y: [0, -8, 2, -5, 0], rotate: [0, -2, 1, -1, 0], transition: { duration: 4, repeat: Infinity, ease: "linear" } }}`. The rotation adds organic feel.

## Q81: How do you implement AnimatePresence with multiple children being added/removed dynamically?
**A:** Each child needs unique `key`. `<AnimatePresence> {items.map(item => <motion.div key={item.id} layout initial={{ opacity: 0, x: -20 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: 20 }}>{item.name}</motion.div>)} </AnimatePresence>`. `layout` animates siblings to new positions when items are added/removed. `mode="popLayout"` removes exiting item from layout flow immediately.

## Q82: How do you implement a pull-to-refresh gesture?
**A:** `const pullDistance = useMotionValue(0); const pullRotate = useTransform(pullDistance, [0, 100], [0, 180]); const opacity = useTransform(pullDistance, [0, 100], [0, 1]);` On drag down: `drag="y" dragConstraints={{ top: 0 }} onDrag={(_, info) => pullDistance.set(Math.max(0, info.offset.y))} onDragEnd={(_, info) => { if (info.offset.y > 100) { onRefresh(); animate(pullDistance, 0); } else { animate(pullDistance, 0); } }}`.

## Q83: How do you implement a morphing shape animation between two components?
**A:** Use `layoutId` for shape morphing. Both components must have same `layoutId`: `{isCircle ? <motion.div layoutId="shape" style={{ borderRadius: "50%" }} /> : <motion.div layoutId="shape" style={{ borderRadius: "0%" }} />}`. Wrap in `<AnimatePresence>` if components unmount/mount. For SVG morphing: use `d` attribute animation on `<motion.path>` with same number of path points.

## Q84: How do you implement a context menu with enter/exit animations?
**A:** `<AnimatePresence> {isOpen && <> <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} className="backdrop" onClick={onClose} /> <motion.div initial={{ opacity: 0, scale: 0.9, x: menuX, y: menuY }} animate={{ opacity: 1, scale: 1 }} exit={{ opacity: 0, scale: 0.9 }} style={{ position: "fixed", top: 0, left: 0 }}>menu items</motion.div> </>} </AnimatePresence>`. Stagger menu items with `staggerChildren`. For sub-menu: animate from parent menu item position.

## Q85: How do you implement a 3D carousel with motion components?
**A:** `const rotateY = useTransform(scrollX, [0, containerWidth], [0, 360]);` For each card: compute translateZ and rotateY based on index. `{items.map((item, i) => { const theta = (i / items.length) * 360; return <motion.div style={{ rotateY: theta, translateZ: 300 }} /> })}`. Use `transformStyle: "preserve-3d"` on parent. For drag rotation: `drag="x"` mapped to rotation.

## Q86: How do you implement a counting-up number animation that triggers on scroll?
**A:** `const [ref, inView] = useInView({ once: true }); const count = useMotionValue(0); const rounded = useTransform(count, (v) => Math.round(v)); useMotionValueEvent(rounded, "change", (v) => setDisplay(v)); useEffect(() => { if (inView) { const controls = animate(count, target, { duration: 2, ease: "easeOut" }); return controls.stop; } }, [inView])`. Use `display: "tabular-nums"` for stable width.

## Q87: How do you implement an animation timeline with staggered start times?
**A:** Use `useAnimate` with sequence: `animate([ [".el1", { opacity: 1 }, { duration: 0.5, at: 0 }], [".el2", { x: 100 }, { duration: 0.5, at: 0.2 }], [".el3", { scale: 1.2 }, { duration: 0.3, at: "-0.1" }], // overlap with previous ])`. The `at` property: number (absolute time), "+0.3" (relative after previous), "-0.1" (overlap).

## Q88: How do you implement a smooth scroll-to-top animation?
**A:** `const { scrollY } = useScroll(); const opacity = useTransform(scrollY, [0, 500], [0, 1]); const y = useTransform(scrollY, [0, 500], [20, 0]);` On click: `const handleClick = () => { window.scrollTo({ top: 0, behavior: "smooth" }); }`. For cross-browser: use `animate(document.documentElement, { scrollTop: 0 }, { duration: 0.5, ease: "easeInOut" })`.

## Q89: How do you implement a drag boundary that resists but doesn't constrain?
**A:** Use `dragTransition={{ power: 0, bounceStiffness: 500, bounceDamping: 50 }}`. `power: 0` means no momentum. The `bounceStiffness` and `bounceDamping` control how it snaps back. For soft resistance: `dragElastic={0.5}`. For infinite drag with resistance getting stronger: custom `onDrag` handler that applies increasing counter-force.

## Q90: How do you implement an animated tooltip with position tracking?
**A:** `const [coords, setCoords] = useState({ x: 0, y: 0 }); const handleHover = (e) => { const rect = e.target.getBoundingClientRect(); setCoords({ x: rect.left + rect.width / 2, y: rect.top }); }`. Tooltip: `<AnimatePresence> {isHovered && <motion.div initial={{ opacity: 0, scale: 0.8, y: -5 }} animate={{ opacity: 1, scale: 1, y: 0 }} exit={{ opacity: 0, scale: 0.8, y: -5 }} style={{ position: "fixed", left: coords.x, top: coords.y - 10 }} /> } </AnimatePresence>`. Use spring for smooth position changes.

## Q91: How do you implement an accordion with multiple open items?
**A:** `const [openItems, setOpenItems] = useState(new Set()); const toggle = (id) => { setOpenItems(prev => { const next = new Set(prev); next.has(id) ? next.delete(id) : next.add(id); return next; }); }`. Each item: `<motion.div animate={{ height: openItems.has(id) ? "auto" : 0, opacity: openItems.has(id) ? 1 : 0 }} transition={{ duration: 0.3 }}>`. For smooth auto height: use `layout` on content div.

## Q92: How do you implement a parallax effect within a specific section only?
**A:** `const ref = useRef(null); const { scrollYProgress } = useScroll({ target: ref, offset: ["start end", "end start"] }); const y = useTransform(scrollYProgress, [0, 1], ["-20%", "20%"]); return <section ref={ref}><motion.div style={{ y }}>content</motion.div></section>`. The parallax only activates while the section is in view. `offset` controls when animation starts/ends.

## Q93: How do you implement a sticky scroll section with fading content?
**A:** `<section style={{ height: "200vh", position: "relative" }}> <motion.div style={{ position: "sticky", top: 0, height: "100vh", display: "flex" }}> <motion.div style={{ opacity: useTransform(scrollYProgress, [0, 0.3, 0.7, 1], [0, 1, 1, 0]) }}>content</motion.div> </motion.div> </section>`. The section takes up viewport height, content stickies and fades through on scroll.

## Q94: How do you implement a custom useScroll with callbacks for scroll direction?
**A:** `const { scrollY } = useScroll(); const [direction, setDirection] = useState(0); useMotionValueEvent(scrollY, "change", (latest) => { const prev = prevRef.current; setDirection(latest > prev ? 1 : -1); prevRef.current = latest; })`. Use direction for: hide-on-scroll-down (nav bar), parallax direction, reveal animations. Combine with velocity for scroll speed detection.

## Q95: How do you implement a rotation dial/knob component?
**A:** `const angle = useMotionValue(0); const handlePan = (_, info) => { const newAngle = Math.atan2(info.point.y - center.y, info.point.x - center.x) * (180 / Math.PI); angle.set(newAngle); }`. Render: `<motion.div style={{ rotate: angle }}>`. For snapping: `const snapped = useTransform(angle, (v) => Math.round(v / snap) * snap)`. For min/max: `useTransform(angle, (v) => Math.min(360, Math.max(0, v)))`.

## Q96: How do you implement AnimatePresence with custom mounting/unmounting hooks?
**A:** `<AnimatePresence onExitComplete={() => console.log("All exits done")}> {items.map(item => <motion.div key={item.id} onAnimationStart={() => item.onMount?.()} onAnimationComplete={() => item.onAnimated?.()} exit={{ opacity: 0, transition: { duration: 0.2, onComplete: item.onUnmount } }} />)} </AnimatePresence>`. For cleanup: use `onAnimationComplete` on exit to trigger unmount logic.

## Q97: How do you implement a wavy/flag animation for text or shapes?
**A:** Multiple elements with staggered sine wave delay. For text: split into characters, each with `animate={{ y: [0, -10, 0] }} transition={{ duration: 2, repeat: Infinity, delay: i * 0.1, ease: "easeInOut" }}`. For continuous wave: `repeat: Infinity, repeatType: "mirror"`. For flag-like: horizontal stagger with `rotateZ: [0, 5, 0]`. Use `useMotionValue` for real-time sine calculation.

## Q98: How do you implement a progress-based pan gesture?
**A:** `const x = useMotionValue(0); const progress = useTransform(x, [0, maxWidth], [0, 1]); const handlePanEnd = () => { if (progress.get() > 0.5) { animate(x, maxWidth); onComplete(); } else { animate(x, 0); } }`. For step-based: `const step = useTransform(x, [0, maxWidth], [0, steps]); const currentStep = useTransform(step, Math.round)`. Use for stepper/tutorial UIs.

## Q99: How do you implement an animation that tracks element position relative to viewport center?
**A:** `const { scrollY } = useScroll(); const elY = useMotionValue(0); const ref = useCallback((node) => { if (node) { const observer = new ResizeObserver(() => { const rect = node.getBoundingClientRect(); elY.set(rect.top + rect.height / 2); }); observer.observe(node); } }, []); const distanceFromCenter = useTransform([scrollY, elY], ([scroll, elTop]) => Math.abs(elTop - window.innerHeight / 2));`. Map distance to opacity, scale, or blur.

## Q100: How do you implement a custom layout animation with the FLIP technique manually?
**A:** FLIP: First (record current rect), Last (record new rect after state change), Invert (calculate transform to go from last to first), Play (animate transform to zero). Implementation: `const ref = useRef(null); const firstRect = useRef(null); const updateLayout = () => { if (!ref.current) return; const lastRect = ref.current.getBoundingClientRect(); if (firstRect.current) { const dx = firstRect.current.left - lastRect.left; const dy = firstRect.current.top - lastRect.top; animate(ref.current, { x: [dx, 0], y: [dy, 0] }, { duration: 0.3, ease: "easeInOut" }); } firstRect.current = lastRect; }`. Framer Motion's `layout` prop does this automatically.
