# Tailwind CSS Interview Questions and Answers

## Q1: What is Tailwind CSS?
**A:** Tailwind CSS is a utility-first CSS framework that provides low-level utility classes for building custom designs directly in HTML. Instead of pre-built components, it offers composable utilities like `flex`, `pt-4`, `text-center`, and `rotate-90` that you combine to create any design.

## Q2: How does Tailwind differ from frameworks like Bootstrap or Material-UI?
**A:** Bootstrap provides pre-built components (buttons, cards, navbars) with opinionated styling. Tailwind provides utility classes (flex, padding, color) with no pre-built components — you compose custom designs from utilities. Bootstrap is component-first; Tailwind is utility-first.

## Q3: What is a utility-first approach?
**A:** Utility-first means using small, single-purpose CSS classes (e.g., `text-center`, `bg-blue-500`, `p-4`) to build designs directly in markup, rather than writing custom CSS. Each utility does one thing well, and combinations create complex styles without leaving your HTML.

## Q4: How do you install Tailwind CSS in a project?
**A:** Install via npm: `npm install -D tailwindcss @tailwindcss/cli`. Run `npx tailwindcss init` to create `tailwind.config.js`. Add `@import "tailwindcss"` to your main CSS file. Configure content paths in your config.

## Q5: How does Tailwind work with PostCSS?
**A:** Tailwind is a PostCSS plugin. It processes your CSS and generates utility classes based on your config. It's typically added to the PostCSS config along with autoprefixer. In v4, Tailwind uses Lightning CSS internally instead of PostCSS.

## Q6: What are utility classes?
**A:** Utility classes are small, single-purpose CSS classes like `m-4` (margin: 1rem), `text-lg` (font-size: 1.125rem), `flex` (display: flex), and `rounded-lg` (border-radius: 0.5rem). Each class maps to a single CSS rule.

## Q7: What is a Tailwind config file?
**A:** `tailwind.config.js` (v3) or `tailwind.config.ts` is where you customize Tailwind: extend/override colors, fonts, spacing, breakpoints, add plugins, and configure content paths. It defines your design system tokens.

## Q8: How do you customize colors in Tailwind?
**A:** In `tailwind.config.js`, extend the `colors` key:
```js
theme: { extend: { colors: { brand: { 500: '#3b82f6', 700: '#1d4ed8' } } } }
```
Then use `bg-brand-500` or `text-brand-700`.

## Q9: How do you add custom spacing values?
**A:** Extend `spacing` in the config:
```js
theme: { extend: { spacing: { '18': '4.5rem', '88': '22rem' } } }
```
Tailwind generates `p-18`, `m-18`, `w-88`, `h-18`, `gap-18`, etc.

## Q10: What is the Tailwind `@apply` directive?
**A:** `@apply` allows you to compose utility classes into custom CSS:
```css
.btn { @apply bg-blue-500 text-white px-4 py-2 rounded; }
```
This is useful for extracting repeated utility patterns, though Tailwind recommends keeping utilities in HTML when possible.

## Q11: What is the difference between Tailwind v3 and v4?
**A:** Tailwind v4 introduces CSS-first configuration (no JS config needed), uses Lightning CSS, native `@import`, `@theme` directive for in-CSS configuration, improved performance, and a smaller output. v3 uses a JavaScript config file and PostCSS.

## Q12: What are breakpoints in Tailwind?
**A:** Tailwind provides default responsive breakpoints: `sm` (640px), `md` (768px), `lg` (1024px), `xl` (1280px), `2xl` (1536px). Use prefix syntax: `md:flex` applies `display: flex` at 768px and above.

## Q13: How do you add custom breakpoints?
**A:** In the config, extend `screens`:
```js
theme: { extend: { screens: { '3xl': '1920px', 'xs': '480px' } } }
```
Custom breakpoints work with the same prefix syntax: `3xl:grid-cols-4`.

## Q14: How does the responsive prefix system work?
**A:** Prefix any utility with a breakpoint: `sm:`, `md:`, `lg:`, `xl:`, `2xl:`. The utility applies at that breakpoint and above. `md:flex` means `display: flex` from 768px onward. Multiple breakpoints can be combined for responsive designs.

## Q15: What are pseudo-class variants in Tailwind?
**A:** Variants for interactive states: `hover:`, `focus:`, `active:`, `disabled:`, `visited:`, `focus-visible:`, `focus-within:`, `group-hover:`, `peer-focus:`, etc. Example: `hover:bg-blue-700` darkens the background on hover.

## Q16: What are group and peer variants?
**A:** `group` allows styling a child based on parent state: parent has `group` class, child uses `group-hover:opacity-100`. `peer` styles a sibling based on another sibling's state: `peer-checked:bg-blue-500` for a label next to a checkbox.

## Q17: How do dark mode utilities work?
**A:** Use `dark:` prefix: `dark:bg-gray-900 dark:text-white`. Requires configuring `darkMode` in the config (`'class'` or `'media'`). With `class`, toggle dark mode by adding `dark` class to a parent element.

## Q18: How do you implement dark mode with Tailwind?
**A:** Set `darkMode: 'class'` in config. Add `dark` class to `<html>` or `<body>` (usually via JavaScript based on system preference or user toggle). Use `dark:` prefixed utilities: `bg-white dark:bg-gray-800`.

## Q19: What is the `container` class in Tailwind?
**A:** `.container` sets `max-width` based on the current breakpoint and auto-centers with `margin-inline: auto`. It's responsive by default. Customize max-widths by modifying `theme.container.center` or `theme.container.padding`.

## Q20: How do you center content with Tailwind?
**A:** Use `mx-auto` (horizontal auto margins), `flex justify-center items-center` (flexbox centering), or `grid place-items-center` (grid centering). For text, use `text-center`.

## Q21: How do you create a flex layout with Tailwind?
**A:** Use `flex` to enable flexbox. Combine with `flex-row`/`flex-col` for direction, `justify-center`/`justify-between` for main axis, `items-center`/`items-start` for cross axis, `flex-wrap` for wrapping, and `gap-*` for spacing.

## Q22: How do you create a grid layout?
**A:** Use `grid` to enable grid, `grid-cols-3` for three columns, `grid-rows-2` for two rows, `gap-4` for spacing, `col-span-2` for spanning columns, and `row-span-1` for spanning rows.

## Q23: What are Tailwind's spacing utilities?
**A:** Spacing utilities include `p-*` (padding), `m-*` (margin), `px-*` (padding x-axis), `py-*`, `pt-*`, `pb-*`, `pl-*`, `pr-*`, and similarly for margin. Also `space-x-*` (horizontal gap between children) and `space-y-*` (vertical gap).

## Q24: How does the spacing scale work?
**A:** Tailwind uses a 4px base unit. `p-1` = 4px (0.25rem), `p-2` = 8px (0.5rem), `p-4` = 16px (1rem). The scale goes from `0` (0) to `96` (24rem). Values are proportional: `p-2` is double `p-1`, `p-4` is double `p-2`.

## Q25: How do you set custom widths and heights?
**A:** Use `w-*` and `h-*`: `w-full` (100%), `w-screen` (100vw), `w-1/2` (50%), `w-64` (16rem), `h-auto`, `h-screen` (100vh). Min/max variants: `min-h-screen`, `max-w-4xl`. Arbitrary values: `w-[200px]`, `h-[30vh]`.

## Q26: What are arbitrary values in Tailwind?
**A:** Arbitrary values allow using values not in the default theme: `w-[200px]`, `text-[32px]`, `bg-[#1da1f2]`. Use square bracket syntax. Supports any CSS value: `top-[calc(100%-2rem)]`, `grid-cols-[1fr_2fr]`.

## Q27: How do you handle typography with Tailwind?
**A:** Use `font-sans`/`font-serif`/`font-mono` for font family, `text-*` for size (`text-lg`, `text-xl`, `text-3xl`), `font-*` for weight (`font-bold`, `font-medium`), `leading-*` for line height, `tracking-*` for letter spacing, and `text-*` for color.

## Q28: What Tailwind classes control text alignment?
**A:** `text-left`, `text-center`, `text-right`, `text-justify`. These map to `text-align`. Also `text-start` and `text-end` for logical properties.

## Q29: How do you truncate text with Tailwind?
**A:** Use `truncate` class which applies `overflow: hidden; text-overflow: ellipsis; white-space: nowrap;`. For multi-line truncation, use `line-clamp-2`, `line-clamp-3` (requires `@tailwindcss/line-clamp` or built-in in v3.3+).

## Q30: How do you handle line clamping?
**A:** Use `line-clamp-1` through `line-clamp-6+`. Truncates text at the specified number of lines with an ellipsis. Also `line-clamp-none` to disable. Built into Tailwind v3.3+.

## Q31: What are Tailwind's border utilities?
**A:** `border` (border-width: 1px), `border-2`, `border-4`, `border-t`, `border-b`, `border-l`, `border-r`, `border-x`, `border-y`. Color: `border-gray-300`, `border-red-500`. Style: `border-solid`, `border-dashed`, `border-dotted`, `border-none`.

## Q32: How do you handle border radius?
**A:** `rounded-none` (0), `rounded-sm` (0.125rem), `rounded` (0.25rem), `rounded-md` (0.375rem), `rounded-lg` (0.5rem), `rounded-xl`, `rounded-2xl`, `rounded-3xl`, `rounded-full` (50%). Per-corner: `rounded-t-lg`, `rounded-bl-md`.

## Q33: How do you create shadows with Tailwind?
**A:** Use `shadow-sm`, `shadow`, `shadow-md`, `shadow-lg`, `shadow-xl`, `shadow-2xl`, `shadow-inner`, `shadow-none`. Customize shadow colors with `shadow-blue-500/50`. Configure in `theme.extend.boxShadow`.

## Q34: How do you handle opacity in Tailwind?
**A:** Use `opacity-0` through `opacity-100` (step 5: 0, 5, 10, 20, 25, 30, 40, 50, 60, 70, 75, 80, 90, 95, 100). Apply to colors with slash notation: `bg-black/50` (50% opacity), `text-white/80`.

## Q35: How does Tailwind handle colors with opacity?
**A:** Use slash syntax: `bg-blue-500/50` for 50% opacity, `text-gray-900/75` for 75% opacity. The opacity applies to the color only, not the entire element. Works with all color utilities.

## Q36: What are Tailwind's transition utilities?
**A:** `transition` (enables transitions), `transition-all`, `transition-colors`, `transition-opacity`, `transition-shadow`, `transition-transform`. Control duration: `duration-300`, delay: `delay-150`, timing: `ease-in-out`, and property: `ease-linear`.

## Q37: How do you animate in Tailwind?
**A:** Use `animate-spin` (linear spin), `animate-ping` (pulse ring), `animate-pulse` (fade pulse), `animate-bounce` (bounce), or `animate-none`. Custom keyframes can be added via `theme.extend.animation` and `theme.extend.keyframes`.

## Q38: How do you create a custom keyframe animation in Tailwind?
**A:** In the config:
```js
theme: { extend: { keyframes: { wiggle: { '0%,100%': { transform: 'rotate(-3deg)' }, '50%': { transform: 'rotate(3deg)' } } }, animation: { wiggle: 'wiggle 1s ease-in-out infinite' } } }
```
Then use `animate-wiggle`.

## Q39: What are Tailwind's transform utilities?
**A:** `scale-*` (50-150), `scale-x-*`, `scale-y-*`, `rotate-*` (0 to 360 in steps), `translate-x-*`, `translate-y-*`, `skew-x-*`, `skew-y-*`, and `origin-*` for transform origin. Combine with `hover:scale-105` for hover effects.

## Q40: How do you handle transforms with Tailwind?
**A:** Apply transform utilities directly: `transform scale-110 rotate-45 translate-x-4`. Note: `transform` class is not needed in v3+ as transforms work standalone. Combine with state variants: `hover:scale-110 transition-transform`.

## Q41: How do you create a hover lift effect?
**A:** ```html
<div class="transition-all duration-300 hover:-translate-y-1 hover:shadow-lg">
  Content
</div>
```
The element lifts up with a shadow on hover.

## Q42: What are Tailwind's filter utilities?
**A:** `blur-sm` through `blur-3xl`, `brightness-50` through `brightness-200`, `contrast-50` through `contrast-200`, `grayscale`, `hue-rotate-*`, `invert`, `saturate-*`, `sepia`, `drop-shadow-*`. Apply with `filter` class (not needed in v3+).

## Q43: How do you use backdrop filters?
**A:** Use `backdrop-blur-sm`, `backdrop-brightness-50`, `backdrop-contrast-125`, `backdrop-grayscale`, `backdrop-hue-rotate-90`, `backdrop-invert`, `backdrop-opacity-50`, `backdrop-saturate-150`, `backdrop-sepia`. Creates a frosted glass effect.

## Q44: How do you create a glassmorphism effect with Tailwind?
**A:** Combine backdrop blur with semi-transparent background and border:
```html
<div class="bg-white/30 backdrop-blur-md border border-white/20 rounded-xl shadow-lg">
  Content
</div>
```

## Q45: How do you handle overflow with Tailwind?
**A:** `overflow-auto`, `overflow-hidden`, `overflow-visible`, `overflow-scroll`, `overflow-x-auto`, `overflow-y-scroll`, `overflow-clip`. Also `overscroll-auto`, `overscroll-contain`, `overscroll-none`.

## Q46: What are Tailwind's position utilities?
**A:** `static`, `fixed`, `absolute`, `relative`, `sticky`. Combined with inset utilities: `inset-0` (top/right/bottom/left: 0), `top-0`, `left-4`, `right-auto`, `bottom-2`. `z-*` for z-index (-50 to 50).

## Q47: How do you create a sticky header with Tailwind?
**A:** ```html
<header class="sticky top-0 z-50 bg-white shadow">
  Content
</header>
```
The header sticks to the top when scrolling.

## Q48: How do you handle z-index in Tailwind?
**A:** Use `z-0` through `z-50` plus `z-auto`. Custom values: `z-[100]`. Tailwind's scale covers common values. Negative: `-z-10`.

## Q49: How do you control aspect ratio?
**A:** Use `aspect-auto`, `aspect-square` (1:1), `aspect-video` (16:9), or arbitrary: `aspect-[4/3]`. Built into Tailwind v3+ via the aspect-ratio CSS property.

## Q50: How do you create responsive images with Tailwind?
**A:** `w-full h-auto` for responsive width, `max-w-full` to prevent overflow, `object-cover` for cropped backgrounds, `object-contain` for fitting, `object-center`/`object-top` for positioning.

## Q51: How do you hide elements in Tailwind?
**A:** `hidden` (display: none), `invisible` (visibility: hidden), `opacity-0` (transparent but takes space), `sr-only` (screen-reader only, visually hidden). Responsive: `md:hidden`, `block lg:hidden`.

## Q52: What is `sr-only` in Tailwind?
**A:** `sr-only` hides content visually but keeps it accessible to screen readers. Useful for providing context to assistive technology without visual clutter. Based on the common "visually hidden" pattern.

## Q53: How do you handle spacing between children?
**A:** Use `space-x-*` for horizontal spacing and `space-y-*` for vertical spacing between direct children. Alternatively, use `gap-*` with `flex` or `grid` layouts, which is often more intuitive.

## Q54: How do you create equal-width columns with Tailwind?
**A:** Use `grid grid-cols-3` for three equal columns. For flex: `flex [&>*]:flex-1` or use `flex-1` on each child. For auto-fill: `grid grid-cols-[repeat(auto-fill,minmax(200px,1fr))]`.

## Q55: How do you use Tailwind with CSS-in-JS (Styled Components)?
**A:** Use `tailwind.macro` or Twin Macro to use Tailwind classes within styled-components. Alternatively, use the `clsx` utility to conditionally apply classes in JSX without CSS-in-JS.

## Q56: How do you conditionally apply Tailwind classes?
**A:** Use `clsx()` or `cn()` (class-variance-authority) utility:
```jsx
<div className={cn('p-4 text-white', isActive && 'bg-blue-500', !isActive && 'bg-gray-500')} />
```

## Q57: What is `clsx` and why use it with Tailwind?
**A:** `clsx` is a tiny utility for conditionally constructing class strings. It handles falsy values, arrays, and objects. Essential for clean conditional Tailwind class composition. `cn()` from `class-variance-authority` is a popular alternative.

## Q58: How do you handle class conflicts in Tailwind?
**A:** Tailwind classes are just CSS classes — later classes in the same `class` attribute override earlier ones for the same property. Use this to your advantage: `className="text-red-500 text-blue-500"` results in blue text.

## Q59: How do you organize long class strings?
**A:** Use multi-line formatting, `clsx`/`cn` for conditionals, extract repeated patterns using `@apply` in CSS, or use component abstractions in React/Vue to encapsulate classes.

## Q60: What is the Tailwind CDN build?
**A:** The CDN script (`<script src="https://cdn.tailwindcss.com">`) lets you use Tailwind without a build step. It includes the full engine in the browser and supports some customization via `tailwind.config` in a script tag.

## Q61: What are the limitations of the Tailwind CDN build?
**A:** No custom config file, no purge (includes all classes, large file size), no `@apply`, no first-class `@layer`, limited customization, and is not recommended for production. Use the npm build for production.

## Q62: How does Tailwind's JIT (Just-In-Time) engine work?
**A:** Tailwind v3+ uses a JIT engine that generates CSS on-demand. It scans your content files for class names and generates only the CSS you actually use. This eliminates unused CSS and allows arbitrary values, variants, and zero-config custom styles.

## Q63: How do you purge unused CSS in Tailwind?
**A:** In v3+, JIT mode does this automatically by scanning `content` paths in config. In v2, you configure `purge` paths. Only classes found in your content files are included in the output.

## Q64: What content paths should you configure?
**A:** Point to files where you use Tailwind classes: HTML templates, JS/TSX/Vue/Svelte components, PHP files, etc. Example:
```js
content: ['./src/**/*.{js,jsx,ts,tsx}', './public/index.html']
```

## Q65: How do you optimize Tailwind for production?
**A:** Use JIT (default in v3+), configure content paths properly, enable CSS minification, purge unused styles, gzip CSS output, and use `--minify` flag with the CLI build.

## Q66: What are Tailwind plugins?
**A:** Plugins add custom utilities, components, or base styles. Official plugins: `@tailwindcss/typography` (Prose), `@tailwindcss/forms`, `@tailwindcss/aspect-ratio`, `@tailwindcss/container-queries`. Community plugins exist for animations, filters, etc.

## Q67: How do you create a Tailwind plugin?
**A:** Use `plugin()` function from Tailwind:
```js
const plugin = require('tailwindcss/plugin')
module.exports = { plugins: [ plugin(function({ addUtilities }) { addUtilities({ '.scrollbar-hide': { 'scrollbar-width': 'none' } }) }) ] }
```

## Q68: What is `@tailwindcss/typography`?
**A:** A plugin that provides `prose` classes for styling rich text content (articles, blog posts, documentation). `prose`, `prose-lg`, `prose-gray`, `prose-invert`, etc. Handles headings, lists, tables, blockquotes, and more.

## Q69: What is `@tailwindcss/forms`?
**A:** A plugin that resets form element styles to a consistent baseline, making them easy to customize with Tailwind utilities. Removes browser-specific styling from inputs, selects, checkboxes, radio buttons, and textareas.

## Q70: What is `@tailwindcss/container-queries`?
**A:** A plugin adding container query support: `@container` class, and size variants like `@sm:`, `@md:`, `@lg:`. Elements style based on their container size rather than the viewport. Requires `container-type: inline-size` on the container.

## Q71: How do you use Tailwind with React?
**A:** Install Tailwind, configure content paths to include `.tsx`/`.jsx` files, and use classes directly in JSX: `<div className="flex items-center gap-4 p-6 bg-white rounded-xl shadow">`. No special React integration required.

## Q72: How do you use Tailwind with Vue?
**A:** Same as React but with Vue's `class` binding: `<div :class="['flex', isActive ? 'bg-blue-500' : 'bg-gray-500']">`. Tailwind works with any framework since it's just CSS classes.

## Q73: What are the Tailwind directives?
**A:** `@tailwind base` (preflight styles), `@tailwind components` (component classes), `@tailwind utilities` (utility classes), `@tailwind variants` (responsive/hover variants). In v4, these are replaced with `@import "tailwindcss"`.

## Q74: What is Tailwind Preflight?
**A:** Preflight is Tailwind's base style reset (based on Modern Normalize). It removes browser inconsistencies: sets box-sizing to border-box, removes default margins, standardizes font rendering, and normalizes form elements.

## Q75: How do you disable Preflight?
**A:** Set `preflight: false` in the config (`corePlugins: { preflight: false }`). Useful when integrating Tailwind into an existing project with existing base styles.

## Q76: What are `@layer` directives used for?
**A:** `@layer base`, `@layer components`, `@layer utilities` organize custom CSS into Tailwind's cascade layers. Base for resets/fonts, components for component classes, utilities for custom utilities. Controls the override order.

## Q77: How do you add custom CSS that respects Tailwind's layer order?
**A:** Use `@layer` directives:
```css
@layer utilities { .text-shadow { text-shadow: 2px 2px 4px rgba(0,0,0,0.5); } }
```
This ensures your custom CSS is placed correctly in the cascade.

## Q78: How do you create a button component with Tailwind?
**A:** Combine utilities and extract if repeated:
```html
<button class="bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-4 rounded-lg transition-colors duration-200">
  Click me
</button>
```

## Q79: How do you create a card component?
**A:** ```html
<div class="bg-white rounded-xl shadow-lg overflow-hidden">
  <img class="w-full h-48 object-cover" src="..." />
  <div class="p-6">
    <h3 class="text-xl font-bold mb-2">Title</h3>
    <p class="text-gray-600">Content</p>
  </div>
</div>
```

## Q80: How do you create a responsive navigation bar?
**A:** ```html
<nav class="flex items-center justify-between p-4 bg-white shadow">
  <div class="text-xl font-bold">Logo</div>
  <div class="hidden md:flex gap-6">
    <a href="#">Home</a>
    <a href="#">About</a>
  </div>
  <button class="md:hidden">☰</button>
</nav>
```

## Q81: How do you create a modal with Tailwind?
**A:** ```html
<div class="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
  <div class="bg-white rounded-xl p-6 max-w-md w-full mx-4">
    <h2 class="text-xl font-bold mb-4">Modal Title</h2>
    <p class="mb-6">Content</p>
    <button class="bg-blue-600 text-white px-4 py-2 rounded">Close</button>
  </div>
</div>
```

## Q82: How do you create a dropdown menu with Tailwind?
**A:** Use `group` for hover-based visibility:
```html
<div class="relative group">
  <button>Menu</button>
  <div class="absolute hidden group-hover:block bg-white shadow-lg rounded mt-2">
    <a href="#" class="block px-4 py-2 hover:bg-gray-100">Item 1</a>
  </div>
</div>
```

## Q83: How do you use Tailwind with CSS Modules?
**A:** Use Tailwind classes as normal in your template. CSS Modules scope your custom CSS, not utility classes. Combine: `className={styles.card} + " p-4 bg-white"` with template literals or clsx.

## Q84: How do you handle custom fonts with Tailwind?
**A:** Add the font to your project (via Google Fonts, `@font-face`, or bundler). Extend the `fontFamily` in config:
```js
theme: { extend: { fontFamily: { heading: ['Playfair Display', 'serif'] } } }
```
Use `font-heading`.

## Q85: How do you handle gradients with Tailwind?
**A:** Use `bg-gradient-to-r`, `bg-gradient-to-b`, `bg-gradient-to-tl`, etc. Set colors: `from-blue-500 via-purple-500 to-pink-500`. Customize stops: `from-blue-500/50`. Arbitrary: `bg-[linear-gradient(45deg,red,blue)]`.

## Q86: How do you create a linear gradient background?
**A:** ```html
<div class="bg-gradient-to-r from-cyan-500 to-blue-500 p-8 rounded-lg">
  Gradient background
</div>
```

## Q87: How do you handle outline and ring utilities?
**A:** `outline-none` removes outline (use with visible focus ring for accessibility), `outline` adds outline, `outline-2` width, `outline-offset-2`. Rings: `ring-2 ring-blue-500 ring-offset-2` for focus indicators.

## Q88: How do you add a focus ring to inputs?
**A:** ```html
<input class="focus:outline-none focus:ring-2 focus:ring-blue-500 border border-gray-300 rounded px-3 py-2" />
```

## Q89: How do you use Tailwind with pseudo-elements?
**A:** Tailwind doesn't have utilities for `::before`/`::after`. Use arbitrary values with `before:` and `after:` variants (v3.1+): `before:content-['★'] before:text-yellow-400`. Or use `@apply` in CSS.

## Q90: How do you handle scrollbar styling with Tailwind?
**A:** No built-in scrollbar utilities. Use `@tailwindcss/scrollbar` community plugin, arbitrary CSS with `[&::-webkit-scrollbar]:w-2`, or the CSS `scrollbar-color` property.

## Q91: What are Tailwind CSS variables?
**A:** Tailwind exposes design tokens as CSS custom properties: `--tw-*` prefixes internally. In v3+, use the `theme()` function in CSS to reference config values: `color: theme('colors.blue.500')`. In v4, use `--color-blue-500` directly.

## Q92: How do you reference Tailwind theme values in CSS?
**A:** Use `theme()` function: `content: theme('content.none')`, `color: theme('colors.blue.500')`, `padding: theme('spacing.4')`. Works inside `@apply` and custom CSS.

## Q93: How do you use data attributes for styling?
**A:** Use bracket syntax: `data-[state=active]:bg-blue-500` applies when `data-state="active"`. Also `aria-*` variants: `aria-[current=page]:font-bold`.

## Q94: What are `has-*` variants?
**A:** Style an element based on its children: `has-[a]:underline` underlines a parent when it contains an `<a>` tag. `has-[:checked]:ring-2` adds ring when a child checkbox is checked.

## Q95: How do you handle RTL (right-to-left) support?
**A:** Use `rtl:` and `ltr:` variants: `pl-4 rtl:pr-4 rtl:pl-0`. Tailwind detects the `dir` attribute. Use logical properties when possible: `ps-4` (padding-inline-start) which automatically handles LTR/RTL.

## Q96: How do you debug Tailwind layouts?
**A:** Use `border-2 border-red-500` to visualize element boundaries, `outline-2 outline-red-500` as non-layout-shifting alternative, and browser DevTools to inspect computed styles and see which utilities are applied.

## Q97: How do you handle Tailwind in an existing project with existing CSS?
**A:** Use `prefix` option in config (`prefix: 'tw-'` generates `tw-flex`, `tw-p-4`), disable preflight, use `important: true` if needed, and gradually migrate by using utilities alongside existing styles.

## Q98: What is `screen()` in Tailwind?
**A:** `screen()` is used to reference a breakpoint in CSS: `@media screen(lg) { ... }`. Generates the correct media query for the named breakpoint. Used inside `@apply` and custom CSS.

## Q99: How do you create a custom variant?
**A:** Use `addVariant` in a plugin:
```js
plugin(function({ addVariant }) {
  addVariant('open', '&[data-open]');
  addVariant('not-first', '&:not(:first-child)');
})
```
Then use `open:bg-blue-500`, `not-first:mt-4`.

## Q100: What are the downsides of Tailwind CSS?
**A:** Long class strings in HTML (remedied by component extraction and `clsx`), learning curve for the utility class naming, initial setup for custom designs, CSS file size if not purging properly, and occasional frustration when a specific CSS property doesn't have a direct utility (using arbitrary values).
