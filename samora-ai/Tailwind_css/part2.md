# Tailwind CSS Interview Questions and Answers - Part 2

## Q1: How do you configure a custom theme with extended colors and custom spacing?
**A:** In `tailwind.config.js`: `theme: { extend: { colors: { brand: { 50: '#eff6ff', 100: '#dbeafe', 500: '#3b82f6', 900: '#1e3a5f' } }, spacing: { '18': '4.5rem', '88': '22rem' } } }`. The `extend` key merges with defaults. To override entirely, use `theme: { colors: { ... } }` without extend. Use generated classes: `bg-brand-500`, `mt-18`, `w-88`. For nested color objects, Tailwind generates depth-based names like `brand-light`.

## Q2: How do you create custom plugins for reusable utility patterns?
**A:** `plugins: [ plugin(function({ addUtilities, addComponents, addBase, addVariant, theme, e }) { addUtilities({ '.text-shadow': { textShadow: '2px 2px 4px rgba(0,0,0,0.5)' }, '.text-shadow-md': { textShadow: '4px 4px 8px rgba(0,0,0,0.5)' } }) }), plugin(require('@tailwindcss/forms')) ]`. Use `addUtilities` for utilities, `addComponents` for component classes, `addBase` for base styles, `addVariant` for custom variants like `@supports` or `group-*`.

## Q3: How do you use arbitrary values with bracket syntax?
**A:** Use square brackets for one-off values: `w-[237px]`, `bg-[#1da1f1]`, `text-[calc(100vh-4rem)]`, `grid-cols-[1fr_2fr_1fr]`, `top-[-5px]`, `p-[13px_24px]`. For complex values with spaces: `grid-cols-[repeat(3,minmax(0,1fr))]`. For CSS functions: `w-[clamp(200px,50%,400px)]`. The JIT engine generates these on-demand. For theme values: use `theme('spacing.4')` or `theme(colors.red.500)` for referencing config values.

## Q4: How do you implement responsive design strategies beyond breakpoints?
**A:** Use container queries (via plugin): `@container (min-width: 400px) { .card { flex-direction: row } }`. The `@tailwindcss/container-queries` plugin provides `@sm:`, `@md:`, `@lg:` variants. For element-query-like behavior: use `resize` prop with overflow. For responsive typography: `text-[clamp(1rem,2.5vw,2rem)]`. For responsive grids: `grid-template-columns: repeat(auto-fill, minmax(250px, 1fr))` via arbitrary value `grid-cols-[repeat(auto-fill,minmax(250px,1fr))]`. For responsive order: `order-1 md:order-3`.

## Q5: How do you implement dark mode with the class strategy vs media strategy?
**A:** `darkMode: 'class'` (toggle via JS) vs `darkMode: 'media'` (respects OS setting). Class strategy: `<html class="dark">`, toggle with `document.documentElement.classList.toggle('dark')`. For persistence: store in localStorage. For media strategy: `@media (prefers-color-scheme: dark)` auto-detects. Use `dark:bg-gray-900 dark:text-white`. For mixed: class on specific sections only. For system + manual override: detect media query, allow toggle to override, store preference.

## Q6: How does the JIT (Just-In-Time) engine work internally?
**A:** Tailwind v3+ uses a JIT engine that generates styles on-demand. It scans your source files (configurable via `content` paths) for class names using regex, generates only those utilities, and outputs a single CSS file. The engine parses class patterns like `md:dark:hover:bg-blue-500` into their constituent variants and utilities. It uses a cache system for incremental rebuilds. For development, it watches files and rebuilds only changed classes. The engine resolves arbitrary values `[value]` at build time.

## Q7: How do you create custom variants with plugins?
**A:** `addVariant('optional', '&:optional'); addVariant('open', '&[open]'); addVariant('group-open', ':merge(.group)[open] &'); addVariant('children', '& > *'); addVariant('not-first', '&:not(:first-child)'); addVariant('rtl', '[dir="rtl"] &'); addVariant('inert', '&[inert]');`. Usage: `optional:border-gray-300`, `group-open:block`, `rtl:text-right`. For complex selectors: `addVariant('important', '&!important')` but use `!` prefix instead. For media queries: `addVariant('portrait', '@media (orientation: portrait) { & }')`.

## Q8: What are the pros and cons of the `@apply` directive?
**A:** Pros: reuse utility patterns, reduce HTML repetition, migration from utility-first to component approach. Cons: increases CSS bundle size (defeats JIT optimization), creates specificity issues (nested `@apply` can't use `@screen`), makes debugging harder (no direct HTML class reference), can't use variants with `@apply` (no `@apply hover:bg-red`), fragile with style overrides. Better approaches: component extraction via React/Vue components, or using `@layer components` for semantic class names.

## Q9: How do you implement container queries with Tailwind?
**A:** Install `@tailwindcss/container-queries` plugin. Use `@container` class on parent. Variants: `@sm:`, `@md:`, `@lg:`, `@xl:`. Apply to children: `@md:flex-row @md:text-lg`. Define container types: `container-type: inline-size` via `@container` class. Custom container names: `@container [sidebar]`. For breakpoints: default container breakpoints match screen breakpoints (640px, 768px, etc.). Customize in config: `theme: { containers: { xs: '300px' } }`.

## Q10: How do you create component extraction patterns without `@apply`?
**A:** Extract shared patterns into reusable components. React: `const Button = ({ variant, children }) => <button className={`px-4 py-2 rounded font-medium ${variant === 'primary' ? 'bg-blue-500 text-white' : 'bg-gray-200 text-gray-800'}`}>{children}</button>`. For complex: use `clsx`/`cn` utilities. For design system: create a `Button` component with props mapping to Tailwind classes. For server-side: Blade components (Laravel), template partials. Avoid `@apply` for components that are already extracted.

## Q11: How do you integrate Tailwind with CSS-in-JS libraries (styled-components, Emotion)?
**A:** Use `tailwind.macro` or `tw` macro: `const Button = styled.button` ${tw`bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded`} ``. For Emotion: `css={tw`bg-blue-500`}`. Alternative: use `clsx` with Tailwind classes in template literals. For `@emotion/styled`: `const Div = styled.div` composes: ${tw`p-4`} & { customProp: 'value' } ``. Best practice: use `cva` (class-variance-authority) with Tailwind for variant-based components.

## Q12: How do you optimize Tailwind CSS build size for production?
**A:** Configure `content` paths precisely: `content: ['./src/**/*.{js,jsx,ts,tsx}', './pages/**/*.{js,jsx,ts,tsx}']`. Avoid broad patterns like `./src/**/*` that scan node_modules. Use `safelist` for dynamically constructed classes: `safelist: ['bg-red-500', 'text-center']`. Use `blocklist` to remove unused classes: `blocklist: ['*red*', '*blue*']`. Set `purge: { enabled: true }` (v2). For v3: configure `content` properly and JIT handles purge. Remove unused fonts/icons.

## Q13: How do you create custom color palettes with opacity support?
**A:** `colors: { primary: { 50: '#eff6ff', 100: '#dbeafe', 200: '#bfdbfe', 300: '#93c5fd', 400: '#60a5fa', 500: '#3b82f6', 600: '#2563eb', 700: '#1d4ed8', 800: '#1e40af', 900: '#1e3a8a', 950: '#172554' } }`. Opacity modifiers work automatically: `bg-primary-500/50` (50% opacity). For custom opacity levels: they use the default opacity scale. For flat colors without shades: `brand: '#ff0000'` generates arbitrary opacity via `bg-brand/50`. Use `withOpacity` helper function for dynamic opacity in older configs.

## Q14: How do you use screen-specific variants for advanced responsive behavior?
**A:** Default breakpoints: `sm:640px, md:768px, lg:1024px, xl:1280px, 2xl:1536px`. Custom: `screens: { tablet: '768px', laptop: '1024px', desktop: '1280px' }`. For ranges: `max-md:bg-red` (below md). For specific: `max-sm:only:flex-col` (only on small screens). For orientation: `landscape:flex-row`, `portrait:flex-col`. For print: `print:hidden`. For custom media: `addVariant('tall', '@media (min-height: 800px) { & }')`.

## Q15: How do you use `group-hover` and `peer` modifiers for parent/sibling styling?
**A:** `group` parent + `group-hover:child-class`: `<div class="group"> <p class="group-hover:text-blue-500">child</p> </div>`. Nested groups: `group/nav` + `group-hover/nav:text-blue`. Named groups: `group/inner` `group-hover/inner:scale-105`. Peer: `<input class="peer" /> <label class="peer-focus:text-blue-500 peer-invalid:text-red-500">Label</label>`. Peer variants: `peer-hover:`, `peer-focus:`, `peer-disabled:`, `peer-required:`. Multiple peers: `peer/invalid` + `peer-invalid/invalid:block`.

## Q16: How do you use the forms plugin for form styling?
**A:** `npm install @tailwindcss/forms`. Add to plugins. Resets browser-default form styles. Classes: `form-input`, `form-textarea`, `form-select`, `form-checkbox`, `form-radio`, `form-multiselect`. Customize via `theme: { forms: { input: { borderRadius: '8px' } } }`. For checkbox: `form-checkbox h-4 w-4 text-blue-600`. For radio: `form-radio`. For rounded select: `form-select rounded-lg`. For sized inputs: combine with sizing utilities.

## Q17: How do you use the typography plugin (Prose)?
**A:** `npm install @tailwindcss/typography`. Add to plugins. Use `prose` class for rich text formatting. Modifiers: `prose-sm`, `prose-lg`, `prose-xl`, `prose-2xl`. Color modifiers: `prose-blue`, `prose-gray`. For custom: `theme: { typography: { DEFAULT: { css: { a: { color: '#3b82f6', '&:hover': { color: '#2563eb' } } } } } }`. For dark mode: `prose dark:prose-invert`. For unstyled: `prose prose-p:my-2`. Disable specific elements: `prose-no-li`.

## Q18: How do you create and use custom animation utilities?
**A:** Define in config: `animation: { 'spin-slow': 'spin 3s linear infinite', 'ping-slow': 'ping 2s cubic-bezier(0, 0, 0.2, 1) infinite', 'slide-up': 'slideUp 0.3s ease-out', 'fade-in': 'fadeIn 0.5s ease-out' }`. Keyframes: `keyframes: { slideUp: { '0%': { transform: 'translateY(10px)', opacity: '0' }, '100%': { transform: 'translateY(0)', opacity: '1' } } }`. Use: `animate-slide-up`. For staggered: combine with `animation-delay` arbitrary value.

## Q19: How do you use Tailwind with CSS Modules?
**A:** Import: `import styles from './Button.module.css'`. Composition: `.btn { @apply px-4 py-2 rounded; }` in CSS Module. For dynamic classes: `className={${styles.btn} ${active ? styles.active : ''}}`. For complex: use `clsx` with CSS Module objects. For globals: use `global:bg-blue-500` or configure `important: true` with prefix. For Next.js: CSS Modules work out of the box with Tailwind. For Vite: configure `vite.config.js` CSS modules option.

## Q20: How do you implement dark mode with custom color tokens?
**A:** Define in config: `colors: { light: { bg: '#ffffff', text: '#1a1a2e' }, dark: { bg: '#1a1a2e', text: '#e0e0e0' } }`. Use: `bg-light-bg dark:bg-dark-bg text-light-text dark:text-dark-text`. For semantic naming: `brand-bg: '#fff'` and dark override. For complex: use CSS variables: `:root { --bg: #fff } .dark { --bg: #1a1a2e }`. Then `bg-[var(--bg)]`. For component-level dark mode: add `dark` class to specific section.

## Q21: How do you use the `safelist` and `blocklist` configuration options?
**A:** `safelist: ['bg-red-500', { pattern: /bg-(red|green|blue)-(100|200|300)/, variants: ['hover', 'focus'] }]`. Safelist prevents purging. Blocklist: `blocklist: ['container', 'space-x-*']` removes classes. For dynamic classes from API: use pattern safelist. For i18n: safelist `text-left` and `text-right`. For all colors: `pattern: /bg-(red|green|blue|yellow|purple|indigo)-(100|200|300|400|500)/`.

## Q22: How do you implement `@apply` with responsive and pseudo-class variants?
**A:** `@apply` CANNOT use variants directly. Workaround: `@media (min-width: 768px) { .card { @apply flex-row; } }`. Or: `@layer components { .btn { @apply px-4 py-2; } }` with separate hover class: `.btn-primary { @apply bg-blue-500; } .btn-primary:hover { @apply bg-blue-600; }`. Best practice: use the component class directly in HTML with variants instead of `@apply`. Only use `@apply` for base structural styles.

## Q23: How do you configure Tailwind for a design system with branded components?
**A:** Create a design tokens file: `const tokens = { color: { primary: '#0070f3', secondary: '#0070f3' } }`. Import into config: `colors: { ...tokens.color }`. For component classes: `plugins: [ plugin(({ addComponents }) => { addComponents({ '.btn-primary': { '@apply bg-primary text-white px-4 py-2 rounded': {} } }) }) ]`. For consistency: use CSS custom properties for runtime theming. Document with Storybook.

## Q24: How do you implement min-height screen minus header using arbitrary values?
**A:** `min-h-[calc(100vh-4rem)]` or `min-h-[calc(100dvh-4rem)]` (for mobile address bar). For dynamic header heights: use CSS variables: `--header-height: 4rem; min-height: calc(100vh - var(--header-height))`. For sticky footer pattern: `flex flex-col min-h-screen` and `flex-1` on main content. For grid layout: `grid-template-rows: auto 1fr auto` via `grid-rows-[auto_1fr_auto]`.

## Q25: How do you use the `important` option in Tailwind?
**A:** `important: true` adds `!important` to all utilities. `important: '#app'` scopes to selector: `.card { ... }` becomes `#app .card { ... }`. Use for: overriding third-party styles (CMS, WordPress), integration with legacy CSS. Avoid for: new projects, component libraries. Alternative: use `!` prefix on individual classes: `!text-white !bg-blue-500`. The `!` prefix is more targeted and doesn't affect the whole utility set.

## Q26: How do you implement sticky/fixed headers with Tailwind?
**A:** `sticky top-0 z-50 bg-white shadow-md`. For smooth transition: `transition-shadow duration-300`. For blur effect: `backdrop-blur-md bg-white/80`. For shrinking on scroll: combine with JS to toggle classes. For multiple sticky elements: each needs its own `top-X` class. For sticky header with padding: `top-4`. For full-width: `w-full`. For compatibility: `sticky` doesn't work in some table contexts; use `position: sticky` on thead cells.

## Q27: How do you implement complex grid layouts with Tailwind?
**A:** `grid grid-cols-[200px_1fr_200px] grid-rows-[auto_1fr_auto] gap-4`. For named areas: `grid-areas-[header_main_sidebar]` (via arbitrary). For auto-fill: `grid-cols-[repeat(auto-fill,minmax(250px,1fr))]`. For masonry: Tailwind doesn't support native masonry; use columns: `columns-3 gap-4`. For subgrid: `grid-cols-subgrid`. For explicit placement: `col-span-2 col-start-1 row-span-2 row-start-1`. For responsive grid: `grid-cols-1 md:grid-cols-2 lg:grid-cols-3`.

## Q28: How do you implement container queries with arbitrary container names?
**A:** `<div class="@container [container-name:sidebar]"> <div class="@md:block hidden">content</div> </div>`. For multiple containers: name each uniquely. Responsive to container width, not viewport. Use `@xs:`, `@sm:`, `@md:`, `@lg:`, `@xl:`, `@2xl:`. For custom container breakpoints: `theme: { containers: { narrow: '400px', wide: '800px' } }`. Then use `@narrow:flex-col`. Always define `container-type: inline-size` variant.

## Q29: How do you implement CSS Houdini integration with Tailwind?
**A:** Register custom properties: `CSS.registerProperty({ name: '--color-1', syntax: '<color>', initialValue: '#fff', inherits: false })`. Use with Tailwind arbitrary values: `bg-[var(--color-1)]`. For paint worklets: create utility `.paint-ripple { background: paint(ripple) }`. For custom layout: use the `@tailwindcss/container-queries` as a Houdini-like approach. For progressive enhancement: use Houdini with Tailwind fallbacks.

## Q30: How do you use Tailwind with server-side rendering (Next.js, Nuxt, Remix)?
**A:** Next.js: `postcss.config.js` includes `tailwindcss` and `autoprefixer`. Import `globals.css` in layout. No SSR issues since Tailwind is CSS-only. For dynamic classes: construct className strings safely. For Remix: same PostCSS setup. For Nuxt: `@nuxtjs/tailwindcss` module. For performance: enable JIT for production. For CDN: use Play CDN for prototyping: `<script src="https://cdn.tailwindcss.com"></script>`.

## Q31: How do you create a custom `screens` breakpoint that uses `max-width` queries?
**A:** `screens: { 'max-sm': { max: '639px' }, 'max-md': { max: '767px' }, 'max-lg': { max: '1023px' }, 'max-xl': { max: '1279px' } }`. Or use `@media (max-width: theme('screens.md'))` in custom CSS. For range: `screens: { 'md-max': { max: '1023px' }, 'md-min': { min: '768px' } }`. For custom orientation: `screens: { 'tall': { raw: '(min-height: 800px)' } }`. Using raw queries gives full control over the generated `@media` rule.

## Q32: How do you implement a theme switcher (not just dark/light)?
**A:** Define multiple themes in config: `colors: { theme: { blue: { bg: '#e0f2fe', text: '#1e3a5f' }, green: { bg: '#d1fae5', text: '#065f46' }, purple: { bg: '#f3e8ff', text: '#4c1d95' } } }`. Add theme class to html: `class="theme-blue"` or `class="theme-green"`. Use: `bg-theme-bg text-theme-text`. For CSS variables: `:root { --bg: var(--theme-bg) } .theme-blue { --theme-bg: #e0f2fe }`. Match Tailwind classes via arbitrary values: `bg-[var(--bg)]`.

## Q33: How do you use Tailwind with PostCSS plugins like autoprefixer and cssnano?
**A:** `postcss.config.js: { plugins: { tailwindcss: {}, autoprefixer: {}, cssnano: process.env.NODE_ENV === 'production' ? { preset: 'default' } : {} } }`. Order matters: tailwindcss first, then autoprefixer, then cssnano. For custom PostCSS: add before tailwind for syntax plugins. For CSS imports: `postcss-import` must be before tailwindcss. For nesting: `postcss-nesting` or `tailwindcss/nesting` plugin.

## Q34: How do you implement safe area insets (notch, status bar) with Tailwind?
**A:** Arbitrary values: `pt-[env(safe-area-inset-top)] pb-[env(safe-area-inset-bottom)] pl-[env(safe-area-inset-left)] pr-[env(safe-area-inset-right)]`. For reusable: `addUtilities({ '.safe-top': { paddingTop: 'env(safe-area-inset-top)' } })`. For viewport-fit: add `viewport-fit=cover` to meta tag. For constant env: older iOS uses `constant()` — combine: `padding-top: env(safe-area-inset-top, constant(safe-area-inset-top))`.

## Q35: How do you implement scrollbar styling with Tailwind?
**A:** Custom plugin: `addUtilities({ '.scrollbar-thin': { scrollbarWidth: 'thin', scrollbarColor: '#888 #f1f1f1' }, '.scrollbar-thumb': { '&::-webkit-scrollbar-thumb': { background: '#888', borderRadius: '4px' } } })`. For hiding: `.scrollbar-hide { -ms-overflow-style: none; scrollbar-width: none; &::-webkit-scrollbar { display: none } }`. Use with variants: `hover:scrollbar-thin`. For custom colors: use arbitrary values with CSS custom properties.

## Q36: How do you implement text truncation with custom line counts?
**A:** Single line: `truncate` (overflow hidden, text-overflow ellipsis, white-space nowrap). Multi-line: `line-clamp-2`, `line-clamp-3`, etc. (from `@tailwindcss/line-clamp`). In v3.3+: built-in. Arbitrary: `line-clamp-[7]`. For fallback: `overflow-hidden text-ellipsis display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical`. For responsive: `line-clamp-3 md:line-clamp-none`.

## Q37: How do you implement print-specific styles with Tailwind?
**A:** `print:hidden` hides elements on print. `print:block` shows only on print. `print:text-black` for ink-saving. `print:shadow-none` removes decorative effects. `print:break-inside-avoid` prevents page breaks. `print:!text-sm` reduces font size. For print-only content: `hidden print:block`. For screen-only: `print:hidden`. Custom variant: `addVariant('print', '@media print { & }')`.

## Q38: How do you implement `:has()` selector support in Tailwind?
**A:** Tailwind v3.4+ supports `has-*` variants: `has-[input]:bg-blue-50` (if parent has input child), `group-has-[:invalid]:border-red-500`, `has-[:checked]:ring-2`. Usage: `<div class="has-[:checked]:bg-blue-100"><input type="checkbox" /></div>`. For complex: `has-[>button]:flex`. For empty detection: `<div class="has-[:empty]:hidden">`. Browser support: Chrome 105+, Firefox 121+, Safari 15.4+. For fallback: JavaScript-based detection.

## Q39: How do you use the `@config` directive in CSS files?
**A:** `@config "./tailwind.admin.config.js";` in CSS file loads a different config for that file. Useful for: multiple themes, admin vs frontend, different design systems. The config is relative to the CSS file. Combine with `@tailwind base/components/utilities`. For multi-config: import different CSS files per route/layout. For sharing: base config extends common config.

## Q40: How do you implement dynamic class names with clsx/twMerge?
**A:** `npm install clsx tailwind-merge`. `import { twMerge } from 'tailwind-merge'; import { clsx } from 'clsx'; function cn(...inputs) { return twMerge(clsx(inputs)); }`. Usage: `<div className={cn('px-4 py-2', isActive && 'bg-blue-500', variant === 'primary' ? 'text-white' : 'text-gray-800')}>`. twMerge resolves conflicts (last class wins). clsx handles conditional merging. For performance: memoize complex class strings.

## Q41: How do you build a custom button component with variants using Tailwind?
**A:** Using `cva` (class-variance-authority): `const button = cva(['px-4', 'py-2', 'rounded', 'font-medium'], { variants: { variant: { primary: 'bg-blue-500 text-white hover:bg-blue-600', secondary: 'bg-gray-200 text-gray-800 hover:bg-gray-300', danger: 'bg-red-500 text-white hover:bg-red-600' }, size: { sm: 'text-sm px-3 py-1', md: 'text-base px-4 py-2', lg: 'text-lg px-6 py-3' } }, defaultVariants: { variant: 'primary', size: 'md' } })`. Usage: `className={button({ variant, size })}`. For state: add `disabled:opacity-50` to base.

## Q42: How do you implement a responsive nav bar with mobile hamburger?
**A:** `<nav class="flex items-center justify-between p-4"> <div class="hidden md:flex space-x-4"> nav links </div> <button class="md:hidden" onclick="toggleMenu()"> hamburger icon </button> <div id="mobile-menu" class="hidden mobile-menu-open:flex flex-col md:hidden"> mobile links </div> </nav>`. Use `peer` approach: `<input type="checkbox" class="peer hidden" id="menu-toggle" /><label for="menu-toggle" class="md:hidden">☰</label><div class="hidden peer-checked:block md:flex">menu</div>`.

## Q43: How do you use Tailwind with CSS Grid named areas?
**A:** HTML: `<div class="grid grid-cols-[1fr_300px] grid-rows-[auto_1fr_auto] gap-4" style="grid-template-areas: 'header header' 'main sidebar' 'footer footer'"> <div style="grid-area: header">Header</div> <div style="grid-area: main">Main</div> <div style="grid-area: sidebar">Sidebar</div> <div style="grid-area: footer">Footer</div> </div>`. For Tailwind utility approach: `col-span-2` for full-width header/footer. For named areas via arbitrary: `grid-areas-[header_header/sidebar_main/footer_footer]` (v3.4+).

## Q44: How do you implement aspect ratio containers (e.g., 16:9 video)?
**A:** `aspect-video` (16:9), `aspect-square` (1:1), `aspect-[4/3]` (custom). Before v2: `<div class="relative pb-[56.25%]"><iframe class="absolute inset-0 w-full h-full" /></div>`. With built-in: `<div class="aspect-video"><iframe class="w-full h-full" /></div>`. For responsive aspect ratio: `aspect-[4/3] md:aspect-video`. For portrait: `aspect-[3/4]`. For object fit: `object-cover object-center`.

## Q45: How do you implement a loading skeleton with Tailwind?
**A:** `<div class="animate-pulse space-y-4"> <div class="h-4 bg-gray-200 rounded w-3/4"></div> <div class="h-4 bg-gray-200 rounded"></div> <div class="h-4 bg-gray-200 rounded w-5/6"></div> <div class="h-20 bg-gray-200 rounded"></div> </div>`. For shimmer effect: `bg-gradient-to-r from-gray-200 via-gray-100 to-gray-200 bg-[length:200%_100%] animate-shimmer` with custom keyframe: `shimmer: { '0%': { backgroundPosition: '200% 0' }, '100%': { backgroundPosition: '-200% 0' } }`. For avatar: `rounded-full h-12 w-12 bg-gray-200`.

## Q46: How do you implement drag-and-drop visual feedback with Tailwind?
**A:** `<div class="drag-over:border-blue-500 drag-over:bg-blue-50 border-2 border-dashed border-gray-300 transition-colors" onDragOver={(e) => { e.preventDefault(); e.currentTarget.classList.add('drag-over'); }} onDragLeave={(e) => e.currentTarget.classList.remove('drag-over')} onDrop={handleDrop}>Drop zone</div>`. With `addVariant`: `addVariant('drag-over', '&.drag-over')`. For dragging item: `opacity-50 cursor-grab active:cursor-grabbing`. For prohibited: `cursor-not-allowed opacity-30`.

## Q47: How do you implement text gradient with Tailwind?
**A:** `<span class="bg-gradient-to-r from-blue-500 to-purple-600 bg-clip-text text-transparent font-bold">Gradient Text</span>`. For multiple stops: `from-blue-500 via-purple-500 to-pink-500`. For direction: `bg-gradient-to-br`. For animated gradient: add `animate-gradient` with keyframe: `gradient: { '0%, 100%': { backgroundPosition: '0% 50%' }, '50%': { backgroundPosition: '100% 50%' } }`. Set `backgroundSize: '200% 200%'`. For accessibility: provide a solid color fallback.

## Q48: How do you implement a breadcrumb navigation with Tailwind?
**A:** `<nav aria-label="Breadcrumb" class="flex items-center space-x-2 text-sm text-gray-500"> <a href="/" class="hover:text-gray-700">Home</a> <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" /></svg> <a href="/category" class="hover:text-gray-700">Category</a> <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">...</svg> <span class="text-gray-900 font-medium">Current</span> </nav>`. For collapse on mobile: `hidden md:flex`. For structured data: add `itemscope itemtype="https://schema.org/BreadcrumbList"`.

## Q49: How do you implement scroll-triggered animations with Tailwind only?
**A:** Combine `group` with IntersectionObserver via custom variant: `addVariant('in-view', '&[data-in-view]')`. JS: `observer.observe(el); el.dataset.inView = isIntersecting ? '' : undefined`. Use: `<div data-in-view class="opacity-0 in-view:opacity-100 in-view:translate-y-0 translate-y-4 transition-all duration-700">`. For staggered: `delay-[calc(var(--index)*100ms)]` with inline `style="--index: 1"`. For CSS-only: use `@keyframes` and `animation-timeline`.

## Q50: How do you optimize fonts with Tailwind's font-family utilities?
**A:** Config: `fontFamily: { sans: ['Inter var', 'system-ui', 'sans-serif'], display: ['Cabinet Grotesk', 'system-ui', 'sans-serif'] }`. Use: `font-sans font-display`. For variable fonts: `font-weight: 100..900` works with Tailwind's font-weight scale. For font subsetting: `font-display: swap` in `@font-face`. For performance: preload fonts, use `font-family` with local/system fallbacks. For icons: `fontFamily: { icons: ['Material Icons'] }` with `font-icons`.

## Q51: How do you implement a multi-column layout with Tailwind?
**A:** `columns-3 gap-8` creates CSS columns. `break-inside-avoid-column` prevents item splitting. `column-count` variants: `columns-1 md:columns-2 lg:columns-3`. For column gaps: `gap-4` doesn't work — use `space-y-4` for items. For column rules: add custom: `.columns-3 { column-rule: 1px solid #e5e7eb; column-gap: 2rem; }`. For masonry-like: `columns-[250px]` sets ideal width. For balanced: `column-fill: balance` via arbitrary. For three-column text: `columns-3 [column-rule:1px_solid_#e5e7eb]`. Note: columns flow top-to-bottom, then next column.

## Q52: How do you use `content-visibility` and `contain` with Tailwind?
**A:** `content-visibility: auto` defers rendering of off-screen elements. Utility: `content-visibility-[auto] contain-intrinsic-size-[500px]`. Use on long lists, comments, repeated sections. CSS: `contain: content` limits layout/paint/style containment. For images: `content-visibility: auto` with `contain-intrinsic-size: 300px` prevents layout shift. For lazy sections: `content-visibility-[auto] [contain-intrinsic-size:auto_500px]`. Combine with `@media (prefers-reduced-data: reduce)`.

## Q53: How do you implement backdrop blur and transparency effects?
**A:** `backdrop-blur-sm bg-white/30` creates glassmorphism. Variants: `backdrop-blur-none/sm/md/lg/xl/2xl/3xl`. For frosted glass: `bg-white/10 backdrop-blur-md border border-white/20 shadow-lg`. For navbar: `sticky top-0 bg-white/80 backdrop-blur-md`. For modal: `bg-black/50 backdrop-blur-sm`. For custom blur: `backdrop-blur-[2px]`. For performance: avoid `backdrop-blur` on large areas in scrollable containers.

## Q54: How do you implement sticky headers with scroll shadow?
**A:** `<header class="sticky top-0 z-50 transition-shadow" id="header">`. JS: `window.addEventListener('scroll', () => { header.classList.toggle('shadow-md', window.scrollY > 0) })`. Or with pure CSS: not possible with Tailwind alone (no `has()` based on scroll). For CSS-only: use `position: sticky; @supports (animation-timeline: scroll()) { animation: show-shadow; animation-timeline: scroll(); }`. For Tailwind: use a small JS snippet or Alpine.js.

## Q55: How do you implement a table with sticky headers and zebra striping?
**A:** `<div class="overflow-x-auto max-h-[500px]"> <table class="w-full text-left"> <thead class="sticky top-0 z-10"> <tr class="bg-gray-50"> <th class="px-4 py-2 font-medium">Header</th> </tr> </thead> <tbody> <tr class="even:bg-gray-50 hover:bg-gray-100 transition-colors"> <td class="px-4 py-2">Cell</td> </tr> </tbody> </table> </div>`. For responsive: horizontal scroll on mobile. For sortable: add cursor-pointer on headers. For dense: `px-2 py-1 text-sm`. For bordered: `border border-gray-200 divide-y divide-gray-200`.

## Q56: How do you implement a modal/dialog with Tailwind?
**A:** `<div class="fixed inset-0 z-50 flex items-center justify-center"> <div class="fixed inset-0 bg-black/50 backdrop-blur-sm"></div> <div class="relative bg-white rounded-xl shadow-2xl max-w-lg w-full mx-4 p-6 max-h-[90vh] overflow-y-auto"> <button class="absolute top-4 right-4 text-gray-400 hover:text-gray-600">&times;</button> <h2 class="text-xl font-semibold mb-4">Title</h2> <p class="text-gray-600 mb-6">Content</p> <div class="flex justify-end space-x-3"> <button class="px-4 py-2 text-gray-700 hover:bg-gray-100 rounded">Cancel</button> <button class="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600">Confirm</button> </div> </div> </div>`. For slide-up: `animate-slide-up` custom animation.

## Q57: How do you implement an accessible skip-to-content link with Tailwind?
**A:** `<a href="#main-content" class="sr-only focus:not-sr-only focus:absolute focus:top-4 focus:left-4 focus:z-50 focus:px-4 focus:py-2 focus:bg-white focus:text-blue-600 focus:rounded focus:shadow-lg">Skip to content</a>`. The `sr-only` class visually hides content while keeping it accessible to screen readers. `focus:not-sr-only` makes it visible when focused. For focus-visible: `focus-visible:ring-2 focus-visible:ring-blue-500`. For reduced motion: `motion-safe:transition`.

## Q58: How do you use Tailwind's `size-*` utility?
**A:** `size-4` sets both width and height to 1rem. `size-8` = 2rem. `size-12` = 3rem (avatar size). `size-full` = 100% × 100%. `size-[50px]` arbitrary. Use for: icons, avatars, buttons, checkboxes. For responsive: `size-8 md:size-12`. For icons inside buttons: `<button class="p-2"><svg class="size-5" /></button>`. For squares: `<div class="size-16 bg-blue-500 rounded-lg"></div>`. Avoid for non-square elements.

## Q59: How do you implement dialog/overlay with backdrop using Tailwind?
**A:** Use the native `<dialog>` element with Tailwind: `<dialog id="modal" class="backdrop:bg-black/50 open:flex rounded-xl shadow-2xl p-0 w-full max-w-md"> <form method="dialog" class="p-6"> <h2 class="text-lg font-semibold">Title</h2> <button class="absolute top-4 right-4 text-gray-400">&times;</button> </form> </dialog>`. Style backdrop: `backdrop:bg-black/50` is a native CSS pseudo-element. For animation: `@starting-style` for entry animation. For close: `dialog.close()`.

## Q60: How do you use Tailwind in environment-agnostic (isomorphic) contexts?
**A:** For CSS-in-JS on server: use `tw` from `@emotion/css` or `styled-components/macro`. For static generation: extract classes at build-time. For email: use `inline-tailwind` library to inline styles. For canvas/SVG: Tailwind classes on SVG elements work in browser (not server). For React Native: use `nativewind`. For web components: import generated CSS. For PDF generation: use `@react-pdf/renderer` with custom theme.

## Q61: How do you implement a button group with separator lines?
**A:** `<div class="inline-flex rounded-lg overflow-hidden border border-gray-300 divide-x divide-gray-300"> <button class="px-4 py-2 bg-white hover:bg-gray-50 text-sm font-medium text-gray-700 transition-colors">Left</button> <button class="px-4 py-2 bg-white hover:bg-gray-50 text-sm font-medium text-gray-700 transition-colors">Middle</button> <button class="px-4 py-2 bg-white hover:bg-gray-50 text-sm font-medium text-gray-700 transition-colors">Right</button> </div>`. For vertical: `flex-col divide-x-0 divide-y`. For active state: `bg-blue-50 text-blue-600`. For segmented control: `even:border-x` for alternating borders.

## Q62: How do you implement auto-fit and auto-fill grid behavior?
**A:** `grid-cols-[repeat(auto-fill,minmax(250px,1fr))]` creates as many 250px-min columns as fit. `auto-fill` keeps empty tracks; `auto-fit` collapses them. Difference: `auto-fill` creates empty grid columns; `auto-fit` collapses empty tracks to 0. Use `auto-fit` when you want items to stretch. Use `auto-fill` when you want consistent grid geometry. For responsive: `grid-cols-[repeat(auto-fill,minmax(250px,1fr))]` is responsive without media queries.

## Q63: How do you implement logical properties (margin-inline, padding-block) with Tailwind?
**A:** `ms-4` (margin-inline-start), `me-4` (margin-inline-end), `ps-4` (padding-inline-start), `pe-4`. `mt-4` translates to `margin-block-start`. `mb-4` = `margin-block-end`. For RTL support: `ms` and `me` auto-flip. For LTR: `ml-4` works too but doesn't flip. For start/end: `items-start`, `items-end` are logical-aware. For border: `border-s-2`, `border-e-2`. Prefer logical properties for internationalized apps.

## Q64: How do you implement `inset` shorthand with Tailwind?
**A:** `inset-0` = `top:0; right:0; bottom:0; left:0`. `inset-x-0` = left+right. `inset-y-0` = top+bottom. `inset-4` = 1rem on all sides. `inset-x-4` = 1rem left/right. `inset-[10px]` arbitrary. Use for: absolutely positioned full-size overlays, sticky elements, background covers. For negative: `-inset-1` (outset for shadows). For responsive: `inset-0 md:inset-auto`. Combined with `absolute` or `fixed`.

## Q65: How do you use `transform-gpu` and `transform-cpu` for hardware acceleration?
**A:** `transform-gpu` enables GPU-accelerated transforms (forces `translate3d`/`scale3d`). Use on elements with heavy animations: `transform-gpu hover:scale-105 transition-transform duration-300`. `transform-cpu` uses CPU. For `will-change-transform`: use `will-change-transform` utility. For performance: apply `transform-gpu` only to animated elements. For Safari: GPU acceleration reduces flickering. For 3D transforms: `transform-gpu` is automatic.

## Q66: How do you implement subgrid in Tailwind CSS?
**A:** Subgrid allows children to align with parent grid tracks. Use `grid-cols-subgrid grid-rows-subgrid` on a child that is also a grid. Example: `<div class="grid grid-cols-3 gap-4"> <div class="grid grid-cols-subgrid gap-4 col-span-3"> <div class="col-start-1">item</div> <div class="col-start-3">item</div> </div> </div>`. The `.grid-cols-subgrid` class makes the child inherit the parent's column tracks. Browser support: Firefox 71+, Safari 16+, Chrome 117+.

## Q67: How do you implement `field-sizing` for auto-growing textareas?
**A:** CSS `field-sizing: content` makes textarea/contenteditable grow with content. Tailwind arbitrary: `[field-sizing:content]`. Combine with `resize-none` to prevent manual resize. For min/max height: `min-h-[40px] max-h-[200px]`. For auto-grow with JS: synchronize scrollHeight. For `contenteditable`: `<div contenteditable class="[field-sizing:content] min-h-[40px] border rounded p-2">`. Browser support: Chrome 123+. Fallback: JavaScript-based auto-resize.

## Q68: How do you implement masonry layout with Tailwind without plugins?
**A:** CSS columns approach: `<div class="columns-2 md:columns-3 gap-4 space-y-4"> <div class="break-inside-avoid bg-white rounded-lg shadow p-4">item of any height</div> <div class="break-inside-avoid bg-white rounded-lg shadow p-4">taller item</div> <div class="break-inside-avoid bg-white rounded-lg shadow p-4">short</div> </div>`. `columns-2` creates 2-column masonry. `break-inside-avoid` prevents items splitting across columns. `space-y-4` adds vertical gap. Note: items flow top-to-bottom, left-to-right (not left-to-right, top-to-bottom like classic masonry). For correct ordering: use a grid-based JS masonry.

## Q69: How do you implement auto-height textareas with Tailwind?
**A:** `<textarea class="w-full border rounded-lg p-3 resize-none overflow-hidden [field-sizing:content] min-h-[40px] max-h-[300px]" placeholder="Type here..." onInput={e => { e.target.style.height = 'auto'; e.target.style.height = e.target.scrollHeight + 'px'; }} />`. The JS approach resets height to auto, then sets to scrollHeight. For `field-sizing:content`: no JS needed but limited browser support. For React: use `useRef` and `useEffect`. For Vue: `v-textarea-auto-grow` directive.

## Q70: How do you implement view transitions API with Tailwind?
**A:** Enable view transitions: `view-transition-old-root`, `view-transition-new-root`. Tailwind classes on elements with `view-transition-name` via arbitrary: `[view-transition-name:card-1]`. For cross-fade: `::view-transition-old(root) { animation: fade-out 0.3s; }`. For custom: `[view-transition-name:hero]` on shared elements. For SPA: wrap router transitions. For MPA: `@view-transition { navigation: auto; }` in CSS.

## Q71: How do you implement `scroll-timeline` based animations with Tailwind?
**A:** CSS scroll-timeline: `@keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }` then `animation: fadeIn linear; animation-timeline: scroll();`. Tailwind classes: `[animation-timeline:scroll()]`. For view-timeline: `[animation-timeline:view()] [animation-range:entry_0%_entry_100%]`. For element-based: `scroll-timeline-name: --section-scroll; scroll-timeline-axis: block`. Use for: parallax, reading progress, reveal animations without JS. Browser support: Chrome 115+, limited.

## Q72: How do you create a custom `@utility` in Tailwind v4?
**A:** Tailwind v4 introduces `@utility` for custom utilities in CSS: `@utility text-balance { text-wrap: balance; }`. Usage: `<p class="text-balance">`. For responsive: `@utility content-auto { content-visibility: auto; contain-intrinsic-size: 500px; }`. For complex: `@utility scrollbar-thin { scrollbar-width: thin; scrollbar-color: oklch(0.7 0 0) transparent; }`. This is the v4 replacement for some plugin use cases. Apply: any project that uses `@import "tailwindcss"`.

## Q73: How do you implement a custom `@theme` directive in Tailwind v4?
**A:** In Tailwind v4: `@theme { --color-brand: #0070f3; --font-display: 'Inter', sans-serif; --spacing-18: 4.5rem; --breakpoint-xs: 30rem; }`. This replaces the `tailwind.config.js` theme extension. Use: `bg-brand font-display mt-18 xs:flex-col`. For overrides: `@theme { --color-blue-500: #3b82f6; }`. For dark: `@variant dark (@media (prefers-color-scheme: dark) { & { --color-brand: #60a5fa; } })`. This is the cornerstone of Tailwind v4's CSS-first config.

## Q74: How do you use `@import` in Tailwind v4 for modular CSS?
**A:** Tailwind v4 uses `@import "tailwindcss"` to load the framework. Module CSS files: `@import "components/button.css"`. For layers: `@import "tailwindcss/theme" layer(theme); @import "tailwindcss/preflight" layer(base); @import "tailwindcss/utilities" layer(utilities);`. For third-party: `@import "swiper/css" layer(vendor);`. For conditional: `@import "print.css" print;`. This replaces the `@tailwind` directives from v3.

## Q75: How do you implement `@variant` in Tailwind v4 for custom states?
**A:** `@variant hover (&:hover) { .btn { @apply bg-blue-600; } }`. `@variant group-hover (.group:hover &) { .child { @apply opacity-100; } }`. `@variant portrait (@media (orientation: portrait) { & { @apply flex-col; } })`. `@variant supports-grid (@supports (display: grid) { & { @apply grid; } })`. In Tailwind v4, variants are defined in CSS rather than JS config. Use `@variant` for custom pseudo-classes and media queries.

## Q76: How do you use `@apply` in Tailwind v4 with `@variant`?
**A:** In v4, `@apply` works inside `@variant` blocks: `@variant hover { .btn-primary { @apply bg-blue-600 shadow-lg; } }`. For dark mode: `@variant dark { .card { @apply bg-gray-800 text-white; } }`. For responsive: `@variant lg (@media (width >= 1024px) { .nav { @apply flex; } })`. Supports nesting: `.btn { @apply px-4 py-2; @variant hover { @apply bg-blue-600; } }`. This makes component styling more self-contained.

## Q77: How do you implement the `@starting-style` rule with Tailwind?
**A:** `@starting-style` animates elements from their initial state when first displayed. Tailwind arbitrary: `[@starting-style]:opacity-0`. For native dialog: `dialog[open] { @starting-style { opacity: 0; } }`. For popover: `[popover]:popover-open { @starting-style { opacity: 0; scale: 0.9; } }`. For transitions: `opacity-0 transition-opacity duration-300 [@starting-style]:opacity-0`. This eliminates the need for `enter` animations in JS frameworks for native elements.

## Q78: How do you implement CSS layers (`@layer`) with Tailwind?
**A:** `@layer base { h1 { @apply text-3xl font-bold; } }`. `@layer components { .card { @apply bg-white rounded-xl shadow p-6; } }`. `@layer utilities { .text-shadow { text-shadow: 2px 2px 4px rgba(0,0,0,0.1); } }`. Layer order: base < components < utilities. This controls specificity and override order. For third-party overrides: wrap in `@layer utilities` at the end. For Tailwind v4: `@layer` works with `@import "tailwindcss"`.

## Q79: How do you implement progressive enhancement with `@supports` in Tailwind?
**A:** `@supports (display: grid) { .grid-layout { @apply grid grid-cols-3 gap-4; } }`. Or via variant: `addVariant('supports-grid', '@supports (display: grid) { & }')`. For container queries: `@supports (container-type: inline-size) { .card-container { @apply @container; } }`. For `has()`: `@supports selector(:has(*)) { ... }`. In HTML: `<div class="flex flex-wrap supports-grid:grid supports-grid:grid-cols-3">`. This ensures basic layout works everywhere, enhanced layout where supported.

## Q80: How do you implement custom `@media` queries beyond breakpoints?
**A:** Tailwind arbitrary: `[@media_(prefers-contrast:more)]:border-2`, `[@media_(prefers-reduced-transparency:reduce)]:bg-opacity-100`, `[@media_(inverted-colors:inverted)]:brightness-0.8`. For prefers-contrast: `[@media_(prefers-contrast:more)]:border-2`. For pointer type: `[@media_(pointer:fine)]:cursor-default`. For hover capability: `[@media_(hover:hover)]:hover:bg-blue-600`. For scripting: `[@media_(scripting:enabled)]:hidden`. For dark: `[@media_(prefers-color-scheme:dark)]`. Combine variants for complex queries.

## Q81: How do you implement Tailwind with Shadow DOM (web components)?
**A:** Shadow DOM encapsulates styles. Solutions: 1) Use `@layer` and `@import` inside shadow root. 2) Use `constructable stylesheets`: `const sheet = new CSSStyleSheet(); sheet.replaceSync(tailwindOutput); shadowRoot.adoptedStyleSheets = [sheet]`. 3) Use `lightningcss` to compile Tailwind per component. 4) Use `tailwindcss-webcomponent` tool. For scoped: Tailwind v4's `@scope` approach. For `@scope`: `@scope (.card) { @apply; }`. The key challenge: global preflight doesn't apply in shadow DOM.

## Q82: How do you implement `@scope` in Tailwind for style scoping?
**A:** Tailwind v4 supports CSS `@scope`: `@scope (.card) { :scope { @apply bg-white rounded-xl; } .title { @apply text-lg font-bold; } }`. This scopes styles to `.card` and its descendants. Use for: component isolation, avoiding nested selector conflicts. For donut scope (exclude inner): `@scope (.card) to (.ignore) { .inner { @apply hidden; } }`. For Tailwind v3: no built-in support — use CSS modules or web components.

## Q83: How do you implement `text-wrap: pretty` and `text-wrap: balance` with Tailwind?
**A:** `text-balance` (Tailwind v3.4+): `text-wrap: balance` for balanced headlines. `text-pretty`: `text-wrap: pretty` for orphan prevention. Example: `<h1 class="text-balance text-4xl font-bold">Long headline that wraps across multiple lines evenly</h1>`. `<p class="text-pretty">Paragraph text that avoids single orphaned words on the last line</p>`. For arbitrary: `[text-wrap:stable]`. These improve typography without JS. Browser support: Chrome 114+, Safari 17.5+, Firefox 121+.

## Q84: How do you implement `:user-valid` and `:user-invalid` pseudo-classes?
**A:** `:user-valid`/`:user-invalid` only apply after user interaction (unlike `:valid`/`:invalid` which apply immediately). Tailwind: `user-valid:border-green-500 user-invalid:border-red-500`. Example: `<input type="email" required class="border-2 border-gray-300 user-valid:border-green-500 user-invalid:border-red-500 user-invalid:bg-red-50" />`. `:user-invalid` triggers after first blur or submission attempt. `:user-valid` triggers when data meets constraints. Prevents initial flash of validation styles.

## Q85: How do you implement scroll-driven animations (scroll-timeline)?
**A:** CSS scroll-timeline: `<div class="[animation-timeline:scroll()] [animation-range:0_100%]">`. For view progress: `[view-timeline-name:--card] [animation-timeline:--card]`. Combine with custom animation: `@keyframes reveal { from { opacity: 0; scale: 0.8; } to { opacity: 1; scale: 1; } }`. Then `<div class="animate-[reveak_linear_both] [animation-timeline:scroll()]">`. For range: `animation-range: entry 0% contain 100%`. This replaces many IntersectionObserver use cases.

## Q86: How do you implement `container-type` variants for element queries?
**A:** `<div class="@container [container-type:inline-size]"> <div class="@md:flex-col @lg:flex-row">...</div> </div>`. Define container via `@container` class. Container query variants: `@xs:`, `@sm:`, `@md:`, `@lg:`, `@xl:`, `@2xl:`. For custom name: `<div class="@container [container-name:sidebar]">`. Use `@md:flex @md:flex-row` to change layout based on container width. This enables truly reusable responsive components.

## Q87: How do you implement aspect-ratio independent of width/height?
**A:** `aspect-[4/3]` forces 4:3 ratio. `aspect-[1/1]` = square. `aspect-[9/16]` = portrait phone. For intrinsic ratio from content: use `aspect-auto`. For responsive: `aspect-video md:aspect-square`. For grid items: `aspect-square` maintains squares in responsive grid. For images: `object-cover aspect-square`. For dynamic: `aspect-[var(--ratio)]` with CSS variable. The `aspect-ratio` property works for any element (not just replaced elements).

## Q88: How do you implement `overscroll-behavior` with Tailwind?
**A:** `overscroll-contain` prevents scroll chaining (scroll boundary stops at element). `overscroll-auto` default. `overscroll-none` disables overscroll. Use: `<div class="h-96 overflow-y-auto overscroll-contain">scrollable content</div>`. For modals: `overscroll-contain` prevents background page scrolling. For sidebars: `overscroll-none` prevents pull-to-refresh. For macOS rubber-banding: `overscroll-none` disables elastic overflow.

## Q89: How do you implement `scroll-snap` with Tailwind?
**A:** `snap-x snap-mandatory` for horizontal scroll. `snap-start snap-center snap-end` for alignment. `<div class="flex overflow-x-auto snap-x snap-mandatory"> <div class="min-w-[300px] snap-start">slide 1</div> <div class="min-w-[300px] snap-start">slide 2</div> </div>`. Variants: `snap-y` (vertical), `snap-both`. `snap-proximity` (less strict). `snap-always` vs `snap-normal` (motion-ok). Styling: `scrollbar-hide` for carousels. For pagination dots: JS to track active slide.

## Q90: How do you implement color scheme detection for form controls?
**A:** `color-scheme: dark` makes native form controls (scrollbars, inputs, select menus) render with dark theme. Tailwind: `[color-scheme:dark]`. Use on `<html>` or specific containers: `<div class="[color-scheme:dark]"> <input type="date" /> <select><option>Dark select</option></select> </div>`. For auto: `[color-scheme:light_dark]`. This affects: scrollbar colors, input backgrounds, select dropdowns, date pickers. Combine with `dark:` variants.

## Q91: How do you implement accent color on form controls?
**A:** `accent-pink-500` sets the accent color for checkboxes, radios, range, and progress elements. `<input type="checkbox" class="accent-pink-500" />`. `<input type="range" class="accent-blue-600" />`. `<progress class="accent-green-500" value="70" max="100"></progress>`. Variables: `[accent-color:var(--brand)]`. Note: accent color only affects the interactive color, not the entire element. For full custom styling, use the forms plugin.

## Q92: How do you implement forced-color-adjust for high contrast mode?
**A:** `forced-color-adjust-none` preserves custom colors in Windows High Contrast Mode. `forced-color-adjust-auto` lets browser adjust. Use: `<div class="forced-color-adjust-none" style="background: #0070f3; color: white;">branded element</div>`. For forced colors detection: `@media (forced-colors: active) { .card { border: 2px solid ButtonText; } }`. For accessibility: ensure sufficient contrast even in forced colors mode.

## Q93: How do you implement `touch-action` CSS property with Tailwind?
**A:** `touch-action: manipulation` disables double-tap zoom (300ms delay fix on mobile). Tailwind: `[touch-action:manipulation]`. Use on interactive elements: `<button class="[touch-action:manipulation] active:scale-95 transition-transform">tap me</button>`. Other values: `touch-action: none` (disable all gestures), `touch-action: pan-x` (horizontal scroll only), `touch-action: pinch-zoom` (zoom only). For game: `touch-action: none` prevents browser gestures.

## Q94: How do you use Tailwind with CSS `@container` style queries?
**A:** Container style queries query computed style values (not yet widely supported). Future syntax: `@container style(--theme: dark) { .card { background: #333; } }`. Tailwind: no direct support. Workaround: use class-based theming. For future: Tailwind v4 may support `@container style(...)` via custom variants. For now, use `class="dark:bg-gray-800"` instead of container style queries.

## Q95: How do you implement `anchor()` positioning API with Tailwind?
**A:** CSS Anchor Positioning: `<div id="anchor" class="relative">anchor</div> <div class="fixed [position-anchor:--anchor] [top:anchor(bottom)] [left:anchor(center)] [translate:-50%_8px]">tooltip</div>`. The anchor element: `[anchor-name:--anchor]`. Target: `position-anchor: --anchor`. Use fallback: `@position-try --bottom { ..., inset-area: bottom }`. For popover: `[popover]`: `<div popover class="[position-anchor:--btn] [inset-area:top]">`. Browser support: Chrome 125+.

## Q96: How do you implement `interpolate-size` for CSS transitions on auto height?
**A:** `interpolate-size: allow-keywords` enables CSS transitions to/from `auto`, `fit-content`, `min-content`, `max-content`. Tailwind: `[interpolate-size:allow-keywords]`. Use: `<div class="[interpolate-size:allow-keywords] transition-[height] duration-300 h-0 hover:h-auto">`. Without this, `transition: height` doesn't work with `auto`. Works with `grid-template-rows`, `width`, etc. Browser support: Chrome 129+. Fallback: `max-height` approach with large value.

## Q97: How do you implement `@page` rules for print with Tailwind?
**A:** `@page { size: A4; margin: 2cm; }`. Tailwind: no direct `@page` directive. Use custom CSS: `@page { @apply; }` doesn't work. Instead, add in your CSS: `@page { size: A4 landscape; margin: 1in; }`. For page breaks: `page-break-before: always`, `page-break-after: avoid`. `.print-landscape { size: landscape; }` in a `@media print` block. For headers/footers: use `position: running` CSS with `@top-center` etc.

## Q98: How do you implement `initial-letter` property for drop caps?
**A:** `initial-letter: 2` creates a drop cap of 2 lines. Tailwind: `[initial-letter:2]`. `<p><span class="float-left text-5xl font-bold leading-none mr-2 [initial-letter:3]">H</span>ere is the start of the paragraph.</p>`. Values: number (lines tall), or number and sink (e.g., `3 2`). Browser support: Safari only (limited). Alternative: `first-letter:text-5xl first-letter:font-bold first-letter:float-left first-letter:leading-none first-letter:mr-2 first-letter:text-blue-600`.

## Q99: How do you implement `text-spacing-trim` for CJK typography?
**A:** `text-spacing-trim: trim-start` removes extra spacing before CJK punctuation. Tailwind: `[text-spacing-trim:trim-start]`. Other values: `trim-both`, `space-all`, `space-first`. Use with CJK fonts: `<div class="[text-spacing-trim:trim-both] text-lg font-cjk">「引号」や句読点の前後の余白を詰める</div>`. For mixed CJK/Latin: `text-spacing-trim: trim-both`. Browser support: limited — use with progressive enhancement.

## Q100: How do you build a complete design system documentation with Tailwind?
**A:** 1) Config: define colors, typography scale, spacing, breakpoints in config. 2) Implement: create reusable component classes via plugins (not `@apply` for components). 3) Document: use Storybook with Tailwind classes displayed alongside. 4) Variants: use `cva` for component variants. 5) Tokens: use `tailwind.config` as the single source of truth. 6) Theme: implement `light`/`dark` tokens via CSS variables + Tailwind. 7) Accessibility: ensure all utilities have accessible contrast. 8) Testing: visual regression tests for utility combinations. 9) Export: generate design token JSON from config for use in Figma/design tools. 10) Distribute: publish as npm package with plugin.
