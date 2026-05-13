# Framer Motion Interview Questions and Answers

## Q1: What is Framer Motion?
**A:** Framer Motion is a production-ready animation library for React. It provides declarative APIs for creating animations, gestures, and layout transitions using motion components and a powerful animation system built on top of CSS transforms and the Web Animations API.

## Q2: How does Framer Motion differ from CSS animations?
**A:** Framer Motion offers declarative React-friendly APIs, automatic spring physics, gesture handling (drag, hover, tap), AnimatePresence for mount/unmount animations, layout animations with FLIP, SVG animation support, and imperative animation controls — none of which are natively available with CSS alone.

## Q3: What is a `motion` component?
**A:** A `motion` component is a Framer Motion-enhanced version of a regular HTML/SVG element. For example, `motion.div`, `motion.button`, `motion.svg`. These components accept animation props like `animate`, `initial`, `exit`, `whileHover`, `whileTap`, etc.

## Q4: What are the core animation props in Framer Motion?
**A:** The core props are: `initial` (starting state), `animate` (target state), `exit` (exit state for AnimatePresence), `whileHover` (state on hover), `whileTap` (state on click), `whileFocus`, `whileDrag`, `whileInView` (state when in viewport), and `transition` (animation configuration).

## Q5: How do you define a simple fade-in animation?
**A:** ```jsx
<motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
  Hello
</motion.div>
```
The element starts invisible and fades in over the default transition duration.

## Q6: What is the `transition` prop?
**A:** The `transition` prop configures animation parameters like duration, delay, easing, and type. Example: `transition={{ duration: 0.5, ease: 'easeInOut', delay: 0.2 }}`. It can also define spring physics with `type: 'spring'`.

## Q7: What is a spring animation in Framer Motion?
**A:** A spring animation simulates physical spring motion. Configured with `type: 'spring'` and parameters like `stiffness` (how rigid), `damping` (how much bounce decays), and `mass` (heaviness). Springs feel more natural than CSS transitions.

## Q8: What is `AnimatePresence`?
**A:** `AnimatePresence` enables animation of components being removed from the React tree. It wraps a conditional render and triggers the `exit` animation before unmounting. It also handles entering children's animations.

## Q9: How do you animate a component entering and leaving?
**A:** Wrap the conditional with `<AnimatePresence>`, and add `initial`, `animate`, and `exit` props:
```jsx
<AnimatePresence>
  {isVisible && (
    <motion.div
      initial={{ opacity: 0, x: -100 }}
      animate={{ opacity: 1, x: 0 }}
      exit={{ opacity: 0, x: 100 }}
    />
  )}
</AnimatePresence>
```

## Q10: What is `layout` animation?
**A:** The `layout` prop on a motion component enables automatic animation when the component's layout changes (position, size). Framer Motion uses the FLIP technique (First, Last, Invert, Play) to smoothly animate layout changes without manual calculations.

## Q11: What does `layoutId` do?
**A:** `layoutId` is used to animate between different components that represent the same visual element across renders. When components with the same `layoutId` appear in different parts of the tree, Framer Motion animates the transition smoothly (e.g., list item expanding to a detail view).

## Q12: How do you animate between different components sharing a layoutId?
**A:** Assign the same `layoutId` to both components. When one unmounts and the other mounts, Framer Motion animates the transformation. Commonly used with `<AnimatePresence>` for shared layout animations.

## Q13: What gesture handlers does Framer Motion support?
**A:** Framer Motion supports `whileHover`, `whileTap`, `whileFocus`, `whileDrag`, and `whileInView`. These are declared as props that accept animation variants or style objects.

## Q14: How do you implement drag in Framer Motion?
**A:** Add the `drag` prop to a motion component: `drag="x"` (constrain to x-axis), `drag="y"` (y-axis), or `drag={true}` (free). Use `dragConstraints` to limit drag bounds and `onDragEnd` for callbacks.

## Q15: What are `dragConstraints`?
**A:** `dragConstraints` define the boundaries for dragging. Can be set to `{ left, right, top, bottom }` pixel values, or a ref to a parent element whose bounding box serves as the constraint area.

## Q16: How do you implement a draggable modal?
**A:** Use `drag` for the panning area, `dragConstraints` set to the modal container ref, `dragElastic` for resistance at edges, and `onDragEnd` with velocity checks to implement dismiss-by-swipe behavior.

## Q17: What is `whileInView`?
**A:** `whileInView` defines animations that trigger when the element scrolls into the viewport. Works with the Intersection Observer API behind the scenes. Use `viewport` prop to configure margins, amount, and whether animation triggers once.

## Q18: How do you configure intersection detection with `viewport` prop?
**A:** The `viewport` prop configures scroll-based animation: `viewport={{ once: true, amount: 0.5, margin: '-50px' }}`. `once: true` plays the animation only the first time. `amount` is the percentage visible (0-1). `margin` works like CSS margin.

## Q19: What are variants in Framer Motion?
**A:** Variants are named sets of animation states defined in an object. They reduce repetition and enable orchestrating animations across parent/child components. A variant object has keys like `hidden`, `visible`, `exit` with corresponding style values.

## Q20: How do you use variants for staggered children animations?
**A:** Define a parent variant with `staggerChildren: 0.1` in the `transition`. Children define their own variants. The parent controls the timing of each child's animation:
```jsx
const container = { hidden: {}, show: { transition: { staggerChildren: 0.1 } } };
const item = { hidden: { opacity: 0 }, show: { opacity: 1 } };
```

## Q21: What is the `variants` prop used for?
**A:** The `variants` prop receives a variants object. Components use variant label strings in `initial`, `animate`, etc., instead of style objects: `animate="visible"`. This enables cleaner code and parent-child coordination.

## Q22: How do you animate SVG elements with Framer Motion?
**A:** Use `motion.path`, `motion.circle`, `motion.svg`, etc. Animate `pathLength`, `pathSpacing`, and `pathOffset` for line drawing effects. Framer Motion also animates SVG-specific attributes like `d`, `viewBox`, and `transform`.

## Q23: How do you animate a path drawing effect?
**A:** ```jsx
<motion.path
  initial={{ pathLength: 0 }}
  animate={{ pathLength: 1 }}
  transition={{ duration: 2 }}
/>
```
Initially the path is invisible, then it draws over 2 seconds.

## Q24: What is `useAnimation`?
**A:** `useAnimation` returns an animation controller with methods like `start()`, `stop()`, and `set()`. Use it to trigger animations imperatively (in response to events or async logic) rather than declaratively via props.

## Q25: How do you sequence animations with `useAnimation`?
**A:** ```jsx
const controls = useAnimation();
await controls.start({ x: 100 });
await controls.start({ y: 100 });
await controls.start({ opacity: 0 });
```
Each `start()` returns a promise that resolves when the animation completes.

## Q26: How do you chain animations using variants?
**A:** Use variant transitions with `delay` or `staggerChildren`. For sequential child animations, set `staggerChildren` in the parent's animate transition. For sequencing within a single motion component, use `transition` with `delay`.

## Q27: What is `useScroll`?
**A:** `useScroll()` tracks the page or element scroll position. Returns motion values: `scrollX`, `scrollY`, `scrollXProgress` (0-1), `scrollYProgress`. These motion values can drive other animations.

## Q28: What is `useTransform`?
**A:** `useTransform` maps one motion value (input range) to another (output range). For example, map `scrollYProgress` (0-1) to `opacity` (1-0) for parallax effects. Supports clamping, easing, and interpolation.

## Q29: How do you create a parallax scroll effect?
**A:** ```jsx
const { scrollYProgress } = useScroll();
const y = useTransform(scrollYProgress, [0, 1], [0, 200]);
return <motion.div style={{ y }} />;
```
The element moves at a different speed than the scroll.

## Q30: What is `useMotionValue`?
**A:** `useMotionValue` creates a reactive motion value that tracks a numeric or string value and updates animations efficiently. Unlike React state, updating a motion value does not trigger re-renders, making it ideal for high-frequency updates.

## Q31: What is the difference between `useMotionValue` and `useState` for animations?
**A:** `useMotionValue` does not cause re-renders when updated, making it performant for animations driven by events like scroll or mouse move. React `useState` causes re-renders and is not suitable for frame-by-frame animation updates.

## Q32: How do you use `useSpring`?
**A:** `useSpring` creates a motion value that springs to its target value: `const x = useSpring(0)`. When you set `x.set(100)`, it animates smoothly using spring physics instead of jumping to the value.

## Q33: What is `useVelocity`?
**A:** `useVelocity` extracts the current velocity (rate of change) of a motion value. Useful for detecting how fast a user is dragging or scrolling, enabling physics-based interactions.

## Q34: How do you animate CSS variables with Framer Motion?
**A:** Animate custom CSS properties using `style={{ '--custom-var': value }}` on a motion component. Framer Motion interpolates numeric values and colors in custom properties.

## Q35: How do you apply keyframe animations?
**A:** Pass an array of values to `animate` props: `animate={{ x: [0, 100, 50, 200] }}`. The element animates through each value in sequence. Control timing with `transition={{ times: [0, 0.25, 0.5, 1] }}`.

## Q36: What are supported easing functions?
**A:** Framer Motion supports named easings (`ease`, `easeIn`, `easeOut`, `easeInOut`, `linear`, `anticipate`, `backIn`, `backOut`, `backInOut`, `circIn`, `circOut`, `circInOut`), cubic bezier (`[0.17, 0.67, 0.83, 0.67]`), and spring physics.

## Q37: How do you use Framer Motion with React Server Components?
**A:** Framer Motion is a client-side library that uses browser APIs. Import it in files with `'use client'` directive or separate client components from server components. Motion components cannot run on the server.

## Q38: What is `motion.create`?
**A:** `motion.create` is an API to create custom motion components from any React component or DOM element. Useful for integrating with design system components: `const MotionButton = motion.create(Button)`.

## Q39: How do you animate responsive values?
**A:** Use `useMediaQuery` (from a custom hook) to detect breakpoints and conditionally set animation values. Or use CSS variables with `useTransform` to create responsive animations.

## Q40: How do you pause and resume animations?
**A:** Use `useAnimation` controls: `controls.stop()` to pause, `controls.start()` to resume. Or set `initial={false}` to prevent initial animation and control all animations imperatively.

## Q41: How can Framer Motion improve perceived performance?
**A:** Framer Motion runs animations on the compositor thread (using `will-change` and CSS transforms) rather than the main thread. This prevents animations from blocking JavaScript execution, resulting in smoother 60fps animations.

## Q42: What happens if React re-renders during an animation?
**A:** Framer Motion is optimized to handle re-renders. Motion values persist across renders. Layout animations use refs to track DOM positions. However, frequent re-renders can cause visual glitches — use `useMotionValue` to avoid unnecessary re-renders.

## Q43: How do you handle reduced motion preferences?
**A:** Use `useReducedMotion()` hook which returns `true` if the user prefers reduced motion. Conditionally disable animations: `const shouldReduceMotion = useReducedMotion(); animate={shouldReduceMotion ? {} : { x: 100 }}`.

## Q44: What is `useReducedMotion`?
**A:** A hook that reads the user's `prefers-reduced-motion` OS/browser setting. Returns `true` when animations should be minimized for accessibility. Always respect this for inclusive design.

## Q45: How do you create a toast notification system with Framer Motion?
**A:** Map toasts to `<AnimatePresence>` with custom `exit` animations (slide out, fade out). Use `layout` prop for smooth reflow when toasts are removed. Use `positionTransition` (legacy) or `layout` for automatic repositioning.

## Q46: How do you animate a page transition in Next.js?
**A:** Wrap `<Component>` with `<AnimatePresence>` and `motion.div` around each page. Use the `router.pathname` as the `key` prop to trigger exit/enter animations on route change.

## Q47: How do you handle route change animations in Next.js?
**A:** ```jsx
<AnimatePresence mode="wait">
  <motion.div key={router.route} initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}>
    <Component {...pageProps} />
  </motion.div>
</AnimatePresence>
```
The `mode="wait"` ensures exit completes before enter starts.

## Q48: What is the `mode` prop on AnimatePresence?
**A:** `mode` controls how entering/exiting children coexist: `"sync"` (default, both animate simultaneously), `"wait"` (exit completes before enter starts), `"popLayout"` (exiting elements pop out of layout flow).

## Q49: How do you handle form input animations?
**A:** Use `layout` for smooth label transitions (placeholder floating labels). Use `whileFocus` for focus ring animations. Animate `scale` and `borderColor` on focus/blur. Use `onChange` with `animate` for validation shake animations.

## Q50: How do you shake an element on validation error?
**A:** ```jsx
<motion.div animate={hasError ? { x: [0, -10, 10, -10, 10, 0] } : {}}>
  <input ... />
</motion.div>
```
A keyframe array creates the shaking effect when `hasError` is true.

## Q51: What is the `onAnimationComplete` callback?
**A:** A prop that fires when an animation finishes. Receives the definition that completed. Useful for chaining: navigate after an exit animation completes, or trigger state changes.

## Q52: How do you animate between different components? (shared layout animation)
**A:** Use `layoutId`. Two different components (e.g., `<Card>` and `<Detail>`) with the same `layoutId` and wrapping `<AnimatePresence>` will animate smoothly between each other, creating a morphing effect.

## Q53: How do you create a morphing effect between two components?
**A:** Both components must have matching `layoutId` and be children of `<AnimatePresence>`. Framer Motion animates the position, size, and shape differences automatically. Combine with `borderRadius` animation for smoother morphs.

## Q54: How do you animate children independently with variants?
**A:** Parent variant defines `staggerChildren: 0.1` and `delayChildren: 0.3`. Each child has its own variant. Children animate in sequence (staggered) and optionally delayed from parent.

## Q55: How do you animate lists with add/remove operations?
**A:** Each list item uses `layout` prop to animate position changes. Wrap the list in `<AnimatePresence>` for exit animations. Assign unique `key`s. New items get `initial` + `animate`, removed items get `exit`.

## Q56: How do you animate a progress bar?
**A:** ```jsx
<motion.div
  initial={{ width: 0 }}
  animate={{ width: `${progress}%` }}
  transition={{ duration: 0.5, ease: 'easeOut' }}
/>
```
The progress bar animates from 0 to the target percentage.

## Q57: How do you animate a counter from one number to another?
**A:** Use `useMotionValue` and `useTransform` with `useSpring`. Or use the `animate` function directly:
```jsx
const count = useMotionValue(0);
const rounded = useTransform(count, Math.round);
// in useEffect: const controls = animate(count, 100, { duration: 2 });
```

## Q58: What is the `animate` function (not prop)?
**A:** `animate()` is an imperative function that animates a motion value to a target. Returns a `PlaybackControls` object with `stop()` and `.then()`:. Useful for one-off or programmatic animations outside of JSX.

## Q59: How do you animate colors with Framer Motion?
**A:** Motion components support animating `backgroundColor`, `color`, `borderColor`, etc., with hex, rgb, rgba, or hsl values. Framer Motion automatically interpolates between color formats.

## Q60: How do you animate gradients?
**A:** Animate `background` with gradient values. Framer Motion animates gradient angles and color stops. For complex gradient animations, use `backgroundImage` with motion values: `style={{ backgroundImage: `linear-gradient(${angle}deg, ${color1}, ${color2})` }}`.

## Q61: How do you handle animation callbacks like `onUpdate`?
**A:** Use `onUpdate(latest)` prop on motion components to receive the current animated value on each frame. For motion values, use `motionValue.on('change', callback)`.

## Q62: What is `onDragStart`, `onDrag`, and `onDragEnd`?
**A:** Lifecycle callbacks for drag gestures. `onDragStart` fires when drag begins. `onDrag` fires on every pointer move during drag. `onDragEnd` fires when drag ends, providing info about velocity and offset.

## Q63: How do you implement a swipe-to-dismiss card?
**A:** ```jsx
<motion.div
  drag="x"
  dragConstraints={{ left: 0, right: 0 }}
  onDragEnd={(_, info) => {
    if (Math.abs(info.offset.x) > 100) removeItem();
  }}
  animate={{ x: 0 }}
  exit={{ x: -300, opacity: 0 }}
/>
```
Combines drag gesture, exit animation, and AnimatePresence.

## Q64: How do you animate based on scroll progress?
**A:** Use `useScroll()` to get scroll progress, `useTransform()` to map progress to animation values, and pass through `style` prop:
```jsx
const { scrollYProgress } = useScroll();
const scale = useTransform(scrollYProgress, [0, 1], [1, 1.5]);
<motion.div style={{ scale }} />
```

## Q65: What is `useInView`?
**A:** A hook alternative to `whileInView`. Returns a ref and boolean: `const [ref, inView] = useInView({ once: true })`. Use `inView` to trigger animations imperatively via `useAnimation`.

## Q66: How do you create a FlipCard animation?
**A:** Animate `rotateY` from 0 to 180 on the card container. Apply `backfaceVisibility: 'hidden'` on both sides. Use `whileHover` or click state to toggle the rotation. The back side has `rotateY: 180` initially.

## Q67: How do you animate a modal backdrop?
**A:** Fade the backdrop with `animate={{ opacity: 1 }}` and `exit={{ opacity: 0 }}`. Add scale animation for the modal content. Use `<AnimatePresence>` conditional on `isOpen`.

## Q68: What is `MotionConfig`?
**A:** `MotionConfig` is a context provider that sets default transition options for all descendant motion components. Example: `<MotionConfig transition={{ type: 'spring', duration: 0.3 }}>`.

## Q69: How do you set global transition defaults?
**A:** Use `<MotionConfig transition={{ type: 'spring', stiffness: 300, damping: 30 }}>` at the app root. All motion components inside inherit these defaults unless overridden locally.

## Q70: How do you create a particle effect with Framer Motion?
**A:** Generate an array of particles, render each as a `motion.div` with random `initial` and `animate` positions. Use `staggerChildren` for varied timing. Animate `opacity`, `scale`, and `y` for float-up effects.

## Q71: How do you animate along a path?
**A:** Use `motion.path` with `pathLength`, or use CSS `offset-path` with Framer Motion animating `offset-distance`. For custom paths, create an SVG path and animate a circle's `cx`/`cy` using calculated positions from `getPointAtLength()`.

## Q72: How do you create a hover card effect?
**A:** Use `whileHover={{ scale: 1.05, boxShadow: '0 10px 30px rgba(0,0,0,0.2)' }}` with `transition={{ type: 'spring', stiffness: 300 }}`. Combine with `whileTap` for click feedback.

## Q73: How do you create an accordion animation?
**A:** Animate `height` (using `overflow: hidden`) or use `layout` on the content div. For smooth height animation, animate from 0 to `auto` — Framer Motion supports `height: 'auto'` in the animate prop since it internally calculates the value.

## Q74: How do you animate a carousel/slider?
**A:** Use `animate={{ x: -currentIndex * slideWidth }}` on the track container with `drag="x"` and `dragConstraints` for swipe support. Use `AnimatePresence` with `mode="popLayout"` for slide transitions.

## Q75: How do you handle animation performance?
**A:** Framer Motion automatically uses GPU-accelerated properties (transform, opacity). For performance: prefer `transform` over `width/height/top/left`, use `layoutId` instead of position calculations, avoid animating too many elements simultaneously, and use `willChange` sparingly.

## Q76: What properties are GPU-accelerated in Framer Motion?
**A:** `transform` (translate, scale, rotate, skew) and `opacity` are compositor-only and GPU-accelerated. Animating `width`, `height`, `top`, `left`, `margin`, `padding` triggers layout thrashing and is not GPU-accelerated.

## Q77: How do you debug Framer Motion animations?
**A:** Use React DevTools to inspect motion component props. Enable Framer Motion's logging with `window.__MOTION_DEV_TOOLS__`. Check the browser's Animation panel in DevTools. Use `onUpdate` logging for frame-by-frame values.

## Q78: How do you animate with CSS variables?
**A:** Set CSS variables in `style` prop and animate using Framer Motion: `style={{ '--x': x }}` where `x` is a motion value. Use `var(--x)` in your CSS. Framer Motion interpolates the variable values.

## Q79: How do you animate `filter` properties?
**A:** Framer Motion supports animating CSS filter functions: `animate={{ filter: ['blur(10px)', 'blur(0px)'] }}` for a blur-in effect. Supports `blur`, `brightness`, `contrast`, `grayscale`, `hue-rotate`, `saturate`, `sepia`, `invert`, and `drop-shadow`.

## Q80: How do you animate `clip-path`?
**A:** Animate `clipPath` as a string: `animate={{ clipPath: ['circle(0%)', 'circle(100%)'] }}`. Framer Motion interpolates compatible clip-path formats. Alternatively, use `layout` for reveal animations.

## Q81: How do you create a text reveal animation?
**A:** Split text into characters or words, render each as a `motion.span`, and use `staggerChildren` with a parent variant. Animate `y` from 20 to 0 and `opacity` from 0 to 1. Wrap in `overflow: hidden`.

## Q82: How do you animate an element from display:none?
**A:** Framer Motion handles this via `<AnimatePresence>=`. When an element is conditionally rendered, AnimatePresence allows animating its entrance. Use `initial={{ opacity: 0, height: 0 }}` and `animate={{ opacity: 1, height: 'auto' }}`.

## Q83: What is the `custom` prop in variants?
**A:** The `custom` prop passes data to variant functions. Variants can be functions: `hidden: (i) => ({ opacity: 0, x: -i * 20 })`. The `custom` prop provides the argument (e.g., `custom={index}`).

## Q84: How do you handle 3D transforms?
**A:** Add `style={{ perspective: 1000 }}` to the parent. Animate `rotateX`, `rotateY`, `rotateZ`, `translateZ`, and `scaleZ` on children. Framer Motion supports all 3D transform properties.

## Q85: How do you create a stagger animation for dynamic lists?
**A:** Use parent variant with `staggerChildren: 0.05` and `delayChildren: 0.1`. Each list item has its own `hidden`/`visible` variants. Set `custom={index}` for per-item delay if needed.

## Q86: How do you use `useCycle`?
**A:** `useCycle` cycles through an array of values on each call:
```jsx
const [x, cycleX] = useCycle(0, 100, 200);
return <motion.div animate={{ x }} onClick={() => cycleX()} />;
```
Each click moves to the next value in the array.

## Q87: What is `useMotionTemplate`?
**A:** `useMotionTemplate` creates a motion value from a string template containing other motion values: `const gradient = useMotionTemplate`linear-gradient(45deg, ${color1}, ${color2})``. Updates efficiently when motion values change.

## Q88: How do you animate an element along a scroll-linked timeline?
**A:** Use `useScroll()` and `useTransform()` to map scroll progress to animation values. For example, map `scrollYProgress` (0-1) to `scale` (1-0.5) and `rotate` (0-360) for a scroll-driven rotation and shrink.

## Q89: How do you implement infinite looping animation?
**A:** Use `transition={{ repeat: Infinity, duration: 2, ease: 'linear' }}` with `animate` that returns to the original value or cycles. For example, a loading spinner: `animate={{ rotate: 360 }}` with infinite repeat.

## Q90: How do you randomize animation properties?
**A:** Use `Math.random()` in variant functions or when constructing animation objects. For example: `animate={{ x: Math.random() * 500, y: Math.random() * 500 }}`. Use `custom` prop and functions for variant-based randomization.

## Q91: What is `AnimatePresence`'s `onExitComplete` prop?
**A:** A callback that fires when all exit animations have completed. Useful for cleanup, removing items from state, or triggering navigation after an exit animation.

## Q92: How do you create a background parallax effect?
**A:** ```jsx
const { scrollY } = useScroll();
const y = useTransform(scrollY, [0, 1000], [0, -200]);
return <motion.div style={{ y }} />;
```
The background moves slower than the foreground, creating depth.

## Q93: How do you animate `grid` templates?
**A:** Use `layout` on grid items for smooth reordering. Animate `gridTemplateColumns` and `gridTemplateRows` as strings — Framer Motion interpolates compatible values.

## Q94: How do you create a reveal-on-scroll section?
**A:** Use `whileInView={{ opacity: 1, y: 0 }}` with `initial={{ opacity: 0, y: 50 }}` and `viewport={{ once: true, amount: 0.2 }}`. The section animates when 20% visible in the viewport.

## Q95: How do you create a cursor follower?
**A:** Track mouse position with `mousemove` event listener and set motion values: `const x = useMotionValue(0);` then update in the listener. Use `useSpring` for smooth following. Apply to a motion div with `style={{ x, y }}`.

## Q96: How do you handle animation conflicts with CSS classes?
**A:** Framer Motion sets inline styles which override CSS. Use `style` prop for baseline styles. Avoid CSS transitions on elements using motion components. Let Framer Motion manage all animation styles.

## Q97: How do you implement gesture-based password input?
**A:** Use `whileFocus` for scaling on focus. Animate `borderColor` for validation states. Use layout for floating label animations. Combine spring transitions for natural input interactions.

## Q98: How do you animate a notification badge count?
**A:** ```jsx
<motion.span key={count} initial={{ scale: 0.5, opacity: 0 }}
  animate={{ scale: 1, opacity: 1 }} exit={{ scale: 1.5, opacity: 0 }}>
  {count}
</motion.span>
```
The badge animates on each count change.

## Q99: How do you create a staggered sidebar menu?
**A:** Parent menu variant uses `staggerChildren: 0.05`. Each menu item variant uses `x: -20` to `x: 0` and `opacity: 0` to `1`. Animate the parent when the sidebar opens. Use `custom={index}` for non-uniform delays.

## Q100: What are the limitations of Framer Motion?
**A:** Framer Motion is client-side only (no SSR by default), adds bundle size (~30KB gzipped), does not support some CSS properties (background-size gradient interpolation), complex chained animations can be tricky, and heavy simultaneous animations can still drop frames on low-end devices. It also requires React 18+.
