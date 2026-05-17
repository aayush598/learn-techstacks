## 8. Tailwind CSS (241–260)

241. What is Tailwind CSS?
     T**Answer:** Tailwind CSS is a utility-first CSS framework that provides low-level utility classes for building custom designs directly in HTML/JSX. Instead of pre-built components, it offers classes like `flex`, `pt-4`, `text-center`, and `bg-blue-500` for composable styling.

242. Why use utility-first CSS?
     U**Answer:** Utility-first CSS offers faster prototyping, smaller CSS bundles (unused styles are purged), consistent design through a constrained design system, no context switching between files, and predictable styles without specificity wars.

243. Explain responsive utilities.
     R**Answer:** Responsive utilities use breakpoint prefixes like `sm:`, `md:`, `lg:`, `xl:`, and `2xl:` to apply styles at specific viewport widths. Example: `text-base md:text-lg lg:text-xl` scales text size across screen sizes with mobile-first design.

244. What are Tailwind breakpoints?
     D**Answer:** Default breakpoints: `sm` (640px), `md` (768px), `lg` (1024px), `xl` (1280px), `2xl` (1536px). They follow a mobile-first approach where unprefixed utilities apply at all sizes, and prefixed utilities override at the given breakpoint and above.

245. Explain dark mode handling.
     D**Answer:** Dark mode is enabled via the `dark:` variant when `darkMode: 'class'` is configured in `tailwind.config.js`. Toggling a `dark` class on a parent element switches styles, with `dark:bg-gray-900 dark:text-white` providing theme-aware styles.

246. What is JIT compilation?
     J**Answer:** Just-In-Time (JIT) compilation generates CSS on-demand as you write classes, eliminating unused styles and reducing build times. It also enables arbitrary values, custom variants, and generates exactly the CSS you use with zero bloat.

247. Explain Tailwind configuration.
     T**Answer:** The `tailwind.config.js` file customizes design tokens: colors, spacing, fonts, breakpoints, and plugins. It extends or overrides the default theme using `extend` for additive changes and direct properties for complete overrides.

248. What are plugins in Tailwind?
     P**Answer:** Plugins extend Tailwind with custom utilities, components, variants, or base styles using `plugin()` from Tailwind. Official plugins include `@tailwindcss/forms`, `@tailwindcss/typography`, `@tailwindcss/aspect-ratio`, and `@tailwindcss/container-queries`.

249. Explain component extraction.
     C**Answer:** Component extraction extracts repeated utility patterns into reusable components using frameworks (React components) or `@apply` directive in CSS. It reduces duplication while maintaining utility-first benefits — prefer framework components over `@apply`.

250. How do you avoid class duplication?
     A**Answer:** Avoid duplication by extracting repeated utility groups into reusable React/Vue components, using `@apply` sparingly, leveraging editor multi-cursor, using class management libraries like `clsx` or `tailwind-merge`, and composing with template literals.

251. Explain arbitrary values.
     A**Answer:** Arbitrary values use square bracket syntax for one-off values not in the design system: `w-[32rem]`, `top-[calc(100%-2rem)]`, `bg-[#1da1f1]`. They bypass the theme while retaining responsive variants and JIT compilation benefits.

252. What are variants in Tailwind?
     V**Answer:** Variants are conditional prefixes that apply utilities in specific states or conditions: `hover:`, `focus:`, `active:`, `disabled:`, `first:`, `last:`, `odd:`, `even:`, `group-hover:`, `peer:`, and custom variants for different scenarios.

253. Explain Tailwind optimization.
     O**Answer:** Optimize by purging unused CSS (automatic with JIT), keeping the config lean, using the JIT engine for small builds, leveraging Tree-shaking, and configuring `content` paths precisely to capture all template files.

254. How does purging work?
     P**Answer:** Purging scans configured content paths for class names and removes unused CSS from the build output. With JIT mode, only classes found in source files generate CSS, resulting in tiny production bundles (typically < 10KB gzipped).

255. Explain accessibility in UI design.
     A**Answer:** Accessibility ensures UIs work for all users including those with disabilities. Practices include semantic HTML, proper color contrast, keyboard navigation, ARIA labels, focus indicators, screen reader support, and respecting `prefers-reduced-motion`.

256. What are common Tailwind pitfalls?
     C**Answer:** Common pitfalls include long unreadable class strings, overusing `@apply` (losing utility benefits), inconsistent spacing from arbitrary values, forgetting purge configuration (large bundles), and mixing Tailwind with other CSS approaches causing conflicts.

257. Explain design systems with Tailwind.
     T**Answer:** Tailwind's configuration-driven design system enforces consistency through centralized tokens for colors, fonts, spacing, and breakpoints. Teams extend the theme to match brand guidelines, creating a shared design language across components and projects.

258. How do you handle animations?
     A**Answer:** Animations use utility classes like `animate-spin`, `animate-ping`, and `animate-pulse`, or custom keyframes defined in `tailwind.config.js`. The `transition-*` utilities handle property transitions, and `duration-*`, `ease-*` configure animation timing.

259. Explain Tailwind with Next.js.
     T**Answer:** Tailwind integrates with Next.js by adding `@tailwind` directives in CSS and including Next.js file paths in `content`. It works seamlessly with both Server and Client Components, App Router, and supports JIT compilation for fast development.

260. How do you scale Tailwind projects?
     S**Answer:** Scale by establishing a shared design system with consistent tokens, enforcing linting with `eslint-plugin-tailwindcss`, creating reusable component libraries, using design tokens across teams, and maintaining a style guide with documented patterns.
