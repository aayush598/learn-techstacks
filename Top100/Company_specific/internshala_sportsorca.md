# SportsOrca — 100 Full Stack Interview Q&A
> Based on SportsOrca — Full Stack Development Internship (WordPress CMS, sports publication, PHP/MySQL/JS)  > Candidate: Aayush Gid (JavaScript/React/MySQL/Next.js/HTML/CSS/attention-to-detail background)
---

## 1. WordPress & CMS Fundamentals (Q1–Q14)

**Q1: What is WordPress and why does SportsOrca use it for a sports publication?**  
A: WordPress is an open-source CMS powering ~43% of websites. It's ideal for sports publications because of its WYSIWYG editor, scheduled publishing, media library, category/tag taxonomy, SEO plugins, and theme ecosystem — enabling non-technical editors to publish articles quickly while developers customize via PHP/templates.

**Q2: What is the difference between WordPress.com and WordPress.org?**  
A: WordPress.org is self-hosted — you own the code, install themes/plugins freely, and have full control. WordPress.com is a hosted service with tiered plans; lower tiers restrict plugins and themes. SportsOrca likely uses WordPress.org (self-hosted) for full editorial and customization control.

**Q3: Explain the WordPress file/directory structure.**  
A: Key directories: `wp-admin/` (admin dashboard), `wp-includes/` (core libraries), `wp-content/` (themes, plugins, uploads). Key files: `wp-config.php` (DB credentials, salts), `functions.php` (theme hooks), `style.css` (theme metadata), `index.php` (main template). Understanding this is essential for locating where to fix issues.

**Q4: What are WordPress themes and how do child themes work?**  
A: A theme controls site appearance (templates, styles, layout). A child theme inherits a parent theme's functionality and lets you override templates/styles without modifying the parent — so updates don't wipe your changes. Create a child theme by adding a `style.css` with `Template: parent-theme-slug` and a `functions.php` that enqueues the parent stylesheet.

```css
/* style.css */
/*
 Theme Name:   SportsOrca Child
 Template:     flavor
*/
@import url("../flavor/style.css");
```

**Q5: What are WordPress plugins and how do they extend functionality?**  
A: Plugins are PHP packages that hook into WordPress actions/filters to add features (SEO, caching, forms). Install via `wp-content/plugins/`. Hooks: `add_action()` for events, `add_filter()` for modifying data. Example: Yoast SEO adds meta tags via `wp_head` action.

```php
add_action('wp_head', 'add_custom_meta');
function add_custom_meta() {
    echo '<meta name="description" content="Sports news...">';
}
```

**Q6: What is the WordPress Loop and why is it important?**  
A: The Loop is the core mechanism that iterates over posts/pages and renders content using template tags (`the_title()`, `the_content()`, `the_post_thumbnail()`). Every template file uses it. Understanding the Loop is critical for customizing how articles display on SportsOrca.

```php
if ( have_posts() ) {
    while ( have_posts() ) {
        the_post();
        the_title( '<h2>', '</h2>' );
        the_content();
    }
}
```

**Q7: What are WordPress custom post types and when would SportsOrca need them?**  
A: Custom post types (CPTs) extend beyond Posts/Pages. SportsOrca could use CPTs for "Teams", "Players", "Fixtures", or "Live Scores" — each with custom fields (meta boxes). Register with `register_post_type()` in `functions.php` or via a plugin like Custom Post Type UI.

```php
register_post_type('team', [
    'labels' => ['name' => 'Teams', 'singular_name' => 'Team'],
    'public' => true,
    'has_archive' => true,
    'supports' => ['title', 'editor', 'thumbnail'],
]);
```

**Q8: What is the WordPress REST API and how can a JavaScript developer leverage it?**  
A: The REST API exposes WordPress data as JSON at `/wp-json/wp/v2/posts`, `/wp-json/wp/v2/pages`, etc. A JS developer (like Aayush with React/Next.js) can build decoupled frontends, fetch content dynamically, or build interactive widgets — bridging WordPress backend with modern JS frontends.

```js
fetch('/wp-json/wp/v2/posts?per_page=5&categories=3')
  .then(res => res.json())
  .then(posts => posts.forEach(p => console.log(p.title.rendered)));
```

**Q9: What are WordPress taxonomies?**  
A: Taxonomies classify content. Built-in: Categories (hierarchical), Tags (flat). Custom taxonomies: "Leagues" (NFL, NBA), "Sports" (Football, Basketball), "Regions" (US, Europe). They power filtering, archives, and navigation on a sports publication site.

**Q10: How does WordPress handle user roles and permissions?**  
A: Default roles: Administrator (full access), Editor (publish/manage all posts), Author (own posts), Contributor (write but not publish), Subscriber (read only). SportsOrca would use Editor for senior staff and Author for junior writers. Managing roles prevents accidental content deletion.

**Q11: What is a WordPress widget and how do sidebars work?**  
A: Widgets are modular content blocks (recent posts, categories, ads) placed in widget-ready areas (sidebars, footers). Configure via Appearance → Widgets. SportsOrca might use widgets for "Trending Articles", "NFL Scores Sidebar", or "Newsletter Signup" in article sidebars.

**Q12: What is the difference between posts and pages in WordPress?**  
A: Posts are chronological, blog-style content with categories/tags (ideal for sports articles, news). Pages are static, non-documented (About Us, Contact, Privacy Policy). SportsOrca uses posts for articles and pages for About, Contact, Advertise, etc.

**Q13: How do WordPress permalinks work and why are they important for SEO?**  
A: Permalinks are URL structures for content. Settings → Permalinks. Best for SEO: "Post name" (`/slug/`) or custom structure (`/%category%/%postname%/`). SportsOrca should use `/%category%/%postname%/` so URLs read like `/nfl/chiefs-secure-playoff-spot/` — descriptive and keyword-rich.

**Q14: What is the WordPress admin dashboard and what are its key sections?**  
A: The admin dashboard (at `/wp-admin/`) includes: Dashboard (overview), Posts (write/manage articles), Media (image/video library), Pages (static content), Comments (moderation), Appearance (themes/widgets/menus), Plugins, Users, Settings, and Tools. This is the primary workspace for a CMS intern.

## 2. PHP & Server-Side Basics (Q15–Q24)

**Q15: What is PHP and why does WordPress use it?**  
A: PHP is a server-side scripting language that generates HTML dynamically. WordPress uses PHP because it runs on Apache/Nginx servers, integrates with MySQL, and has a vast ecosystem. PHP handles form processing, database queries, authentication, and template rendering before sending HTML to the browser.

**Q16: Write a basic PHP function that sanitizes user input for a WordPress comment form.**  
A: Use `sanitize_text_field()` for plain text and `wp_kses_post()` for HTML content. Never trust raw `$_POST` data.

```php
function process_comment() {
    $name  = sanitize_text_field($_POST['author_name']);
    $email = sanitize_email($_POST['author_email']);
    $body  = wp_kses_post($_POST['comment_body']);
    // Insert into database with $wpdb->insert()
}
```

**Q17: What are PHP hooks — actions and filters?**  
A: Actions (`do_action` / `add_action`) execute code at specific points (e.g., after a post saves). Filters (`apply_filters` / `add_filter`) modify data before it's returned (e.g., changing post content). They are WordPress's extensibility backbone — plugins and themes use them extensively.

```php
add_action('save_post', 'on_article_save', 10, 2);
function on_article_save($post_id, $post) {
    if ($post->post_type === 'post') {
        // Validate formatting, check typos, log the save
    }
}
```

**Q18: How do you connect to MySQL from PHP using WordPress's `$wpdb` class?**  
A: WordPress provides the global `$wpdb` object for database operations. It handles connection, escaping, and table prefixes automatically.

```php
global $wpdb;
$results = $wpdb->get_results(
    "SELECT * FROM {$wpdb->prefix}posts WHERE post_status = 'publish' AND post_type = 'post'"
);
foreach ($results as $row) {
    echo $row->post_title;
}
```

**Q19: What is the difference between `get_post_meta()` and custom fields in WordPress?**  
A: `get_post_meta($post_id, $key, $single)` retrieves metadata stored in the `wp_postmeta` table. The Custom Fields UI in the editor is a visual interface for the same data. SportsOrca could store "Team Name", "Match Score", "Author Twitter Handle" as post meta for each article.

```php
$team = get_post_meta($post->ID, 'team_name', true);
echo "Covering: " . esc_html($team);
```

**Q20: What are WordPress shortcodes and how do you create a custom one?**  
A: Shortcodes are macros like `[score team="Lakers" points="112"]` that output dynamic content. Register with `add_shortcode()`. SportsOrca could use shortcodes for embedded scoreboards, player stats, or ad placements within articles.

```php
add_shortcode('game_score', 'render_game_score');
function render_game_score($atts) {
    $atts = shortcode_atts(['team1' => '', 'team2' => '', 'score' => '0-0'], $atts);
    return '<div class="score-widget">' . esc_html($atts['team1']) . ' vs ' . esc_html($atts['team2']) . ' — ' . esc_html($atts['score']) . '</div>';
}
// Usage: [game_score team1="Chiefs" team2="Eagles" score="38-35"]
```

**Q21: How does PHP session management work and how does WordPress handle authentication differently?**  
A: PHP sessions use `session_start()` and `$_SESSION` superglobal. WordPress instead uses cookies with cryptographically signed auth (`logged_in_cookie`) and the `wp_users` table. Authentication is handled by `wp_authenticate()` and `wp_set_auth_cookie()`. You never need raw sessions in WordPress.

**Q22: What is `functions.php` and what can you put in it?**  
A: `functions.php` is a theme's bootstrap file — it runs on every page load. Use it to: enqueue scripts/styles, register menus/widgets, add shortcodes, hook into actions/filters, register custom post types. Treat it like a plugin embedded in the theme.

```php
function sportsorca_enqueue_scripts() {
    wp_enqueue_style('main-style', get_stylesheet_uri());
    wp_enqueue_script('custom-js', get_template_directory_uri() . '/js/custom.js', [], '1.0', true);
}
add_action('wp_enqueue_scripts', 'sportsorca_enqueue_scripts');
```

**Q23: What is the difference between `include`, `require`, `include_once`, and `require_once` in PHP?**  
A: `include`/`require` embed a file's PHP code. `require` throws a fatal error if the file is missing; `include` throws a warning and continues. `*_once` versions prevent duplicate inclusion. Use `require_once` for critical files (config, classes) and `include` for optional templates.

**Q24: How would you debug PHP code in WordPress during development?**  
A: Enable `WP_DEBUG` in `wp-config.php`: `define('WP_DEBUG', true); define('WP_DEBUG_LOG', true); define('WP_DEBUG_DISPLAY', false);`. Logs go to `wp-content/debug.log`. Also use `error_log()`, `var_dump()` for quick checks, and browser DevTools for front-end issues. For production, disable display but keep logging.

## 3. MySQL & Database Management (Q25–Q35)

**Q25: What is the WordPress database schema?**  
A: Core tables: `wp_posts` (posts, pages, revisions), `wp_postmeta` (custom fields), `wp_options` (settings), `wp_users` (user accounts), `wp_usermeta` (user metadata), `wp_comments` (comments), `wp_commentmeta`, `wp_terms`/`wp_termmeta`/`wp_term_taxonomy`/`wp_term_relationships` (taxonomies). Table prefix defaults to `wp_` but is configurable.

**Q26: Write a MySQL query to find the 5 most recent published articles on SportsOrca.**  
A: 

```sql
SELECT ID, post_title, post_date, post_author
FROM wp_posts
WHERE post_status = 'publish' AND post_type = 'post'
ORDER BY post_date DESC
LIMIT 5;
```

**Q27: What is the difference between `INNER JOIN`, `LEFT JOIN`, and `RIGHT JOIN`?**  
A: `INNER JOIN` returns only rows with matches in both tables. `LEFT JOIN` returns all rows from the left table and matching rows from the right (NULLs if no match). `RIGHT JOIN` is the inverse. For example, joining `wp_posts` with `wp_postmeta` using LEFT JOIN ensures all posts appear even without metadata.

```sql
SELECT p.post_title, pm.meta_value AS team_name
FROM wp_posts p
LEFT JOIN wp_postmeta pm ON p.ID = pm.post_id AND pm.meta_key = 'team_name'
WHERE p.post_status = 'publish';
```

**Q28: What are indexes in MySQL and why are they important for a sports publication site?**  
A: Indexes speed up read queries by creating a lookup structure (B-tree) on specified columns. SportsOrca should index `post_status`, `post_date`, `post_type` on `wp_posts` for fast article listing, and `meta_key`/`meta_value` on `wp_postmeta` for metadata queries. Trade-off: indexes slow down writes slightly.

```sql
CREATE INDEX idx_posts_status_date ON wp_posts (post_status, post_date);
CREATE INDEX idx_postmeta_key_value ON wp_postmeta (meta_key, meta_value(50));
```

**Q29: How do you prevent SQL injection in MySQL queries?**  
A: Always use prepared statements (parameterized queries). In WordPress, use `$wpdb->prepare()` which handles escaping. Never concatenate user input directly into SQL strings.

```php
// Safe
$results = $wpdb->get_results(
    $wpdb->prepare("SELECT * FROM wp_posts WHERE post_author = %d AND post_status = %s", $user_id, 'publish')
);

// Dangerous — never do this
$results = $wpdb->get_results("SELECT * FROM wp_posts WHERE post_author = $user_id");
```

**Q30: What is a MySQL transaction and when would you use one?**  
A: A transaction groups multiple queries that succeed or fail atomically (`BEGIN`, `COMMIT`, `ROLLBACK`). Use when updating related data that must stay consistent — e.g., updating a team's win count AND the standings table simultaneously. InnoDB engine required.

```sql
START TRANSACTION;
UPDATE teams SET wins = wins + 1 WHERE id = 1;
UPDATE standings SET points = points + 3 WHERE team_id = 1;
COMMIT;
```

**Q31: Explain the difference between `DELETE`, `TRUNCATE`, and `DROP` in MySQL.**  
A: `DELETE` removes rows one by one (can use WHERE, triggers events, logged). `TRUNCATE` removes all rows at once (faster, resets AUTO_INCREMENT, minimal logging). `DROP` removes the entire table structure and data. For cleaning test data during dev, `TRUNCATE` is efficient; `DROP` only when removing the table entirely.

**Q32: What is a WordPress database backup and how do you perform one?**  
A: Use a plugin (UpdraftPlus, WP-Clone) or manual `mysqldump`: `mysqldump -u root -p sportsorca_db > backup.sql`. For SportsOrca, schedule daily automated backups since the site publishes frequently. Always test restore procedures.

```bash
mysqldump -u wp_user -p sportsorca_db > sportsorca_$(date +%F).sql
```

**Q33: How do you optimize a slow WordPress MySQL query?**  
A: Steps: 1) Enable `SAVEQUERIES` in `wp-config.php` to log queries. 2) Use `EXPLAIN` to see the query plan and identify missing indexes. 3) Add appropriate indexes. 4) Rewrite inefficient queries (avoid `SELECT *`, reduce JOINs). 5) Consider object caching (Redis) for repeated queries. 6) Paginate long result sets.

```sql
EXPLAIN SELECT p.post_title FROM wp_posts p
LEFT JOIN wp_postmeta pm ON p.ID = pm.post_id
WHERE p.post_status = 'publish';
```

**Q34: What are WordPress transients and how do they reduce database load?**  
A: Transients store cached data in the database (or object cache) with an expiration. Use `set_transient()` / `get_transient()` to avoid repeated expensive queries. SportsOrca could cache "most viewed articles this week" or "NFL standings" to avoid recalculating on every page load.

```php
$standings = get_transient('nfl_standings');
if (false === $standings) {
    $standings = $wpdb->get_results("SELECT * FROM standings ORDER BY wins DESC");
    set_transient('nfl_standings', $standings, HOUR_IN_SECONDS);
}
```

**Q35: What is the difference between `wp_options` table and custom post meta?**  
A: `wp_options` stores site-wide settings (site name, permalink structure, plugin configs) — accessed via `get_option()`. Post meta stores per-post data (team name, match date) — accessed via `get_post_meta()`. Use `wp_options` for global settings and post meta for article-specific data.

## 4. JavaScript & Frontend Development (Q36–Q46)

**Q36: How is vanilla JavaScript different from React/Next.js, and how does WordPress use JS?**  
A: Vanilla JS manipulates the DOM directly. React/Next.js is a component-based framework with virtual DOM. WordPress uses vanilla JS in the admin (jQuery-based) and can use JS in themes for interactive elements (sliders, live scores, infinite scroll). As a React developer, Aayush can quickly adapt to WordPress's JS patterns since the core language is the same.

**Q37: Write a JavaScript snippet that dynamically loads the latest 3 SportsOrca articles using the WordPress REST API.**  
A: 

```js
async function loadLatestArticles() {
    const res = await fetch('/wp-json/wp/v2/posts?per_page=3&_embed');
    const posts = await res.json();
    const container = document.getElementById('latest-articles');
    posts.forEach(post => {
        const card = document.createElement('div');
        card.className = 'article-card';
        card.innerHTML = `
            <h3><a href="${post.link}">${post.title.rendered}</a></h3>
            <p>${post.excerpt.rendered}</p>
        `;
        container.appendChild(card);
    });
}
document.addEventListener('DOMContentLoaded', loadLatestArticles);
```

**Q38: What is event delegation and why is it useful in WordPress themes?**  
A: Event delegation attaches one listener to a parent element instead of individual children — useful when content loads dynamically (infinite scroll, AJAX filters). In WordPress, articles might load via AJAX pagination, so a delegated listener on the article container catches clicks on all cards without re-binding.

```js
document.querySelector('.articles-grid').addEventListener('click', (e) => {
    if (e.target.closest('.article-card')) {
        const id = e.target.closest('.article-card').dataset.id;
        openArticle(id);
    }
});
```

**Q39: Explain `fetch()` API vs jQuery AJAX — which should a WordPress theme use?**  
A: `fetch()` is modern, Promise-based, and native. jQuery AJAX is older, verbose, and adds a dependency. For new WordPress themes, use `fetch()` (or Axios). WordPress admin still uses jQuery, but front-end themes should prefer vanilla JS + fetch for performance.

```js
// Modern approach
const data = await fetch('/wp-json/wp/v2/posts').then(r => r.json());

// jQuery approach (legacy)
$.getJSON('/wp-json/wp/v2/posts', function(data) { ... });
```

**Q40: What is the difference between `let`, `const`, and `var`?**  
A: `var` is function-scoped, hoisted, can be redeclared. `let` is block-scoped, can be reassigned but not redeclared. `const` is block-scoped, cannot be reassigned or redeclared (objects/arrays can still be mutated). Use `const` by default, `let` when reassignment is needed, never `var`.

**Q41: How would you implement a live score ticker on SportsOrca using JavaScript?**  
A: Use `setInterval` + `fetch()` to poll an API (or WP REST endpoint) every 30 seconds, update the DOM with new scores. Use CSS transitions for smooth updates. Consider `WebSocket` for real-time if available.

```js
setInterval(async () => {
    const res = await fetch('/wp-json/sportsorca/v1/scores');
    const scores = await res.json();
    document.querySelectorAll('.ticker-item').forEach(el => {
        const game = scores.find(s => s.id === el.dataset.gameId);
        if (game) {
            el.querySelector('.score').textContent = `${game.team1} ${game.score1} - ${game.score2} ${game.team2}`;
        }
    });
}, 30000);
```

**Q42: What is a closure in JavaScript? Give a WordPress-relevant example.**  
A: A closure is a function that retains access to its outer scope's variables even after the outer function has returned. In WordPress, closures are used in jQuery and filter callbacks where you need to capture a variable value at definition time.

```js
function createArticleFilter(category) {
    return function(article) {
        return article.category === category; // `category` is captured via closure
    };
}
const nflFilter = createArticleFilter('NFL');
articles.filter(nflFilter); // returns only NFL articles
```

**Q43: Explain Promises and async/await. Why is this important for WordPress front-end development?**  
A: Promises represent future values; `async/await` makes asynchronous code readable. WordPress REST API calls, AJAX form submissions, and dynamic content loading are all async operations. Proper error handling with `try/catch` prevents silent failures.

```js
async function submitComment(postId, comment) {
    try {
        const res = await fetch('/wp-json/wp/v2/comments', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ post: postId, content: comment })
        });
        if (!res.ok) throw new Error('Comment failed');
        return await res.json();
    } catch (err) {
        console.error('Comment error:', err);
        showUserMessage('Failed to submit comment. Please try again.');
    }
}
```

**Q44: What is DOM manipulation and how does it differ from React's approach?**  
A: DOM manipulation directly modifies HTML elements via `document.getElementById()`, `element.innerHTML`, `element.appendChild()`. React uses a virtual DOM and declarative state — you update state, React diffs and applies minimal DOM changes. WordPress themes use direct DOM manipulation; React-based WP plugins might use React.

**Q45: How do you handle cross-origin requests (CORS) when fetching from the WordPress REST API?**  
A: CORS is needed when your JS frontend is on a different domain than the WordPress backend. In WordPress, add `Access-Control-Allow-Origin` headers via a plugin (CORS) or in `.htaccess`/nginx config. For same-origin (typical WordPress setup), CORS is not an issue.

```php
// In functions.php or a plugin
add_action('init', function() {
    header('Access-Control-Allow-Origin: https://sportsorca.com');
    header('Access-Control-Allow-Methods: GET, POST, OPTIONS');
});
```

**Q46: What is `localStorage` and how could SportsOrca use it?**  
A: `localStorage` stores key-value pairs in the browser (persists across sessions, no expiration). SportsOrca could use it to: remember user's preferred league filter, store recently viewed articles for a "Continue Reading" section, cache API responses to reduce requests, or save dark mode preference.

```js
// Save user preference
localStorage.setItem('preferredLeague', 'NFL');

// Retrieve on page load
const league = localStorage.getItem('preferredLeague') || 'All';
```

## 5. HTML, CSS & Responsive Design (Q47–Q57)

**Q47: What is semantic HTML and why does it matter for a sports publication?**  
A: Semantic HTML uses meaningful tags (`<article>`, `<header>`, `<nav>`, `<main>`, `<section>`, `<figure>`, `<time>`) instead of generic `<div>`. Benefits: better SEO (search engines understand structure), accessibility (screen readers), and maintainability. SportsOrca should use `<article>` for each sports story, `<time datetime="...">` for publication dates, and `<figure>/<figcaption>` for images with captions.

**Q48: Write the HTML structure for a sports article card.**  
A: 

```html
<article class="article-card" data-sport="nfl">
    <figure>
        <img src="/images/chiefs-win.webp" alt="Patrick Mahomes celebrates after Chiefs victory" loading="lazy">
        <figcaption>Chiefs secure playoff berth — Getty Images</figcaption>
    </figure>
    <div class="article-meta">
        <span class="category-tag">NFL</span>
        <time datetime="2026-01-15">Jan 15, 2026</time>
    </div>
    <h2><a href="/nfl/chiefs-secure-playoff-spot/">Chiefs Secure Playoff Spot with Dominant Win</a></h2>
    <p class="excerpt">Patrick Mahomes threw 4 touchdowns as Kansas City clinched the AFC West...</p>
    <span class="author">By Sarah Mitchell</span>
</article>
```

**Q49: What is CSS Flexbox and when would you use it in a WordPress theme?**  
A: Flexbox is a one-dimensional layout model for aligning items in a row or column. Use it for: navigation menus, article card grids, aligning author/date metadata, centering content. It's ideal for responsive layouts that need to adapt from desktop to mobile without complex float hacks.

```css
.article-grid {
    display: flex;
    flex-wrap: wrap;
    gap: 1.5rem;
}
.article-card {
    flex: 1 1 300px; /* grow, shrink, min-width */
    max-width: 400px;
}
```

**Q50: What is CSS Grid and how does it differ from Flexbox?**  
A: CSS Grid is two-dimensional (rows AND columns simultaneously). Flexbox is one-dimensional (row OR column). Use Grid for page layouts (sidebar + main content), article grid layouts with fixed columns, or complex magazine-style arrangements. Flexbox is better for individual component alignment.

```css
.page-layout {
    display: grid;
    grid-template-columns: 250px 1fr 200px;
    grid-template-areas: "sidebar main ads";
    gap: 2rem;
}
```

**Q51: How do CSS media queries work for mobile responsiveness?**  
A: Media queries apply styles based on device characteristics. SportsOrca articles must look good on phones, tablets, and desktops. Start with mobile-first: base styles for small screens, add `min-width` queries for larger screens.

```css
/* Mobile first */
.article-card { padding: 1rem; }

/* Tablet */
@media (min-width: 768px) {
    .article-grid { grid-template-columns: repeat(2, 1fr); }
    .article-card { padding: 1.5rem; }
}

/* Desktop */
@media (min-width: 1024px) {
    .article-grid { grid-template-columns: repeat(3, 1fr); }
}
```

**Q52: What is the CSS box model and why does `box-sizing: border-box` matter?**  
A: The box model is content → padding → border → margin. Default `content-box` adds padding/border to width. `border-box` includes padding/border in the declared width — essential for predictable layouts. Always set `*, *::before, *::after { box-sizing: border-box; }` at the top of your stylesheet.

**Q53: What is CSS specificity and how do you manage it in WordPress themes?**  
A: Specificity determines which CSS rule wins: inline styles (1000) > IDs (100) > classes (10) > elements (1). WordPress themes and plugins can conflict. Manage by: using BEM naming (`.article-card__title`), avoiding `!important`, using class selectors over element selectors, and enqueueing styles in correct order (theme after plugins).

**Q54: How do you optimize web fonts for a fast-loading sports site?**  
A: Use `font-display: swap` to avoid invisible text during load. Limit font weights (2-3 max). Self-host fonts instead of Google Fonts for privacy/speed. Use `unicode-range` subsets. Preload critical fonts with `<link rel="preload">`. SportsOrca should use one bold weight for headlines and one regular for body text.

```css
@font-face {
    font-family: 'SportsOrca Sans';
    src: url('/fonts/sportsorca-regular.woff2') format('woff2');
    font-display: swap;
    font-weight: 400;
    unicode-range: U+0000-00FF;
}
```

**Q55: What is CSS `position: sticky` and how can it improve a sports article layout?**  
A: `position: sticky` keeps an element in its normal flow until it reaches a scroll threshold, then fixes it in place. Use for: sticky navigation bars, sticky "Related Articles" sidebars, sticky "Back to Top" buttons, or sticky score tickers that remain visible while scrolling long articles.

```css
.score-ticker {
    position: sticky;
    top: 0;
    z-index: 100;
    background: #1a1a2e;
}
```

**Q56: What is the `:root` CSS pseudo-class and CSS custom properties?**  
A: `:root` targets the `<html>` element. CSS custom properties (variables) defined on `:root` are available globally. Use them for consistent theming across SportsOrca — colors, fonts, spacing. Update one variable to change the entire site's color scheme.

```css
:root {
    --primary: #1a73e8;
    --accent: #ff6b35;
    --text: #333;
    --bg: #fff;
    --font-heading: 'Inter', sans-serif;
    --spacing-md: 1.5rem;
}
.article-card { color: var(--text); border-left: 4px solid var(--accent); }
```

**Q57: How do you implement a dark mode toggle on a WordPress site?**  
A: Store preference in `localStorage`. Toggle a class on `<body>` (e.g., `.dark-mode`). Use CSS custom properties with a class override. Add a button that triggers the toggle via JS. Persist the choice across page loads.

```js
const toggle = document.getElementById('dark-toggle');
toggle.addEventListener('click', () => {
    document.body.classList.toggle('dark-mode');
    localStorage.setItem('theme', document.body.classList.contains('dark-mode') ? 'dark' : 'light');
});
// On page load
if (localStorage.getItem('theme') === 'dark') document.body.classList.add('dark-mode');
```

## 6. Content Proofreading & Attention to Detail (Q58–Q68)

**Q58: Describe your proofreading process for a sports article before publishing.**  
A: 1) Read the full article once for overall flow and meaning. 2) Re-read line by line checking grammar, spelling, and punctuation. 3) Verify all names (player, team, coach) are spelled correctly. 4) Check all statistics and scores against sources. 5) Verify image alt text and captions. 6) Preview on desktop and mobile. 7) Check all internal/external links. 8) Confirm categories/tags are correct.

**Q59: Identify the errors in this sentence: "The lakers defeated the celtics 112-98, lebron james scored 35 points and grabed 8 rebounds in the tuesday night matchup at crypto dot com arena."**  
A: Errors: 1) "lakers" → "Lakers" (proper noun), 2) "celtics" → "Celtics", 3) "lebron james" → "LeBron James", 4) "grabed" → "grabbed", 5) "tuesday" → "Tuesday", 6) "crypto dot com arena" → "Crypto.com Arena". Corrected: "The Lakers defeated the Celtics 112–98. LeBron James scored 35 points and grabbed 8 rebounds in the Tuesday night matchup at Crypto.com Arena."

**Q60: What are common typographical errors to watch for in sports content?**  
A: Common errors: player name misspellings (Djokovic vs Djoković), incorrect team abbreviations (LAC vs LAC for LA Clippers vs Los Angeles Chargers), wrong jersey numbers, outdated scores/stats, inconsistent date formats, apostrophe errors ("Chiefs'" vs "Chiefs"), confusing "its" vs "it's", comma splices in long sentences, inconsistent capitalization of league names.

**Q61: How do you verify statistics and scores in a sports article?**  
A: Cross-reference with official league APIs (NFL.com, NBA.com), trusted sources (ESPN, AP), or the team's official website. Note the source and date. Flag any stat that can't be verified. For live scores, use the official league's real-time data feed. Never publish unverified statistics.

**Q62: What is AP Style and why does it matter for a sports publication?**  
A: AP (Associated Press) Style is the standard for journalism. Key rules: titles before names (Coach Reid), no serial comma in simple lists (but SportsOrca may use Oxford comma for clarity), numeral rules (one through nine as words, 10+ as figures), date formats (Jan. 15, not January 15th), and age format (Mahomes is 30, not thirty). Consistency builds reader trust.

**Q63: How do you ensure consistency across multiple articles on the same topic?**  
A: Create a style guide/checklist: standard abbreviations (NFL, NBA, NHL), date/time format, score format (38–35 or 38-35), team name conventions (full name first mention, abbreviation after), photo credit format, and category/tag naming. Use WordPress's reusable blocks for recurring elements (score boxes, author bios).

**Q64: What is the difference between "effect" and "affect", "compliment" and "complement"?**  
A: Effect = noun (result/outcome); affect = verb (to influence). "The injury affected his performance." "The effect was significant." Compliment = praise; complement = to complete/enhance. "The coach complimented the defense." "The running game complemented the passing attack."

**Q65: How do you handle content that has been updated after initial publication?**  
A: Update the article with corrections, add an "Updated" timestamp and note explaining what changed. Use WordPress's revision history to track changes. If the update changes the article's meaning significantly, update the social media post and notify editors. Never silently change published content without documentation.

**Q66: What tools can assist with proofreading in WordPress?**  
A: Grammarly (browser extension for real-time checking), Yoast SEO (readability analysis), Hemingway Editor (complexity check), WordPress's built-in spellcheck, browser DevTools for HTML inspection, and custom regex search in the database for bulk typo fixes across multiple articles.

**Q67: How do you handle multi-author content inconsistencies on a sports publication?**  
A: 1) Establish a shared editorial style guide. 2) Use WordPress's "Edit Flow" or "CoSchedule" plugin for editorial workflow. 3) Standardize templates for different article types (game recaps, trade analyses, opinion pieces). 4) Run periodic audits using SQL queries to find formatting inconsistencies across authors' posts.

**Q68: Describe a situation where attention to detail prevented a significant error.**  
A: (Behavioral sample) While reviewing a game recap, I noticed the final score was listed as 35–28 but the article text described a "comeback victory" — the score order was reversed (the winning team's score should be listed first). Additionally, the player name was misspelled as "Mahommes" instead of "Mahomes". Catching these before publication maintained editorial credibility.

## 7. SEO, Media & Image Optimization (Q69–Q77)

**Q69: What is on-page SEO and how do you implement it in WordPress?**  
A: On-page SEO optimizes individual pages for search engines. Key elements: title tags (`<title>` and `<h1>` with target keyword), meta descriptions (155 chars, compelling summary), header hierarchy (H1→H2→H3), URL slug (keyword-rich, short), image alt text, internal linking, and content length (1000+ words for sports features). Use Yoast or Rank Math plugin for guidance.

**Q70: How do you optimize images for a sports publication website?**  
A: 1) Resize before upload (max 1920px width for full-width). 2) Compress (TinyPNG, ShortPixel plugin). 3) Use WebP format (30% smaller than JPEG, WordPress supports it natively). 4) Add descriptive alt text (SEO + accessibility). 5) Use `loading="lazy"` for below-fold images. 6) Use descriptive filenames (`chiefs-playoff-win.webp` not `IMG_2847.jpg`).

```html
<img src="/images/chiefs-playoff-win.webp"
     alt="Patrick Mahomes throws a touchdown pass against the Bills"
     width="800" height="450"
     loading="lazy">
```

**Q71: What is the `srcset` attribute and why is it important for responsive images?**  
A: `srcset` lets the browser choose the best image size based on the device's viewport. This prevents mobile phones from downloading massive desktop images. WordPress generates multiple sizes automatically — leverage them.

```html
<img src="/images/hero-800.jpg"
     srcset="/images/hero-400.jpg 400w, /images/hero-800.jpg 800w, /images/hero-1200.jpg 1200w"
     sizes="(max-width: 600px) 400px, (max-width: 1024px) 800px, 1200px"
     alt="NFL playoffs bracket">
```

**Q72: How do you create and optimize XML sitemaps in WordPress?**  
A: Install Yoast SEO or Google Site Kit — they auto-generate XML sitemaps at `/sitemap.xml`. Submit to Google Search Console. The sitemap should include: posts, pages, categories, author pages. Exclude: tags, media attachment pages, thin pages. Update automatically when new content is published.

**Q73: What are WordPress categories and tags, and how do they affect SEO?**  
A: Categories are hierarchical (NFL → AFC → Chiefs). Tags are flat (Mahomes, Playoffs, Touchdown). Categories create archive pages that rank for broad terms. Tags create niche pages. Use 5-10 categories max, descriptive tags. Avoid duplicate/circular taxonomy. Each should have unique descriptions to avoid thin content.

**Q74: What is schema markup and how does it apply to sports articles?**  
A: Schema markup (structured data) helps search engines understand content. For sports articles: `Article` schema (author, datePublished, headline), `SportsEvent` schema (teams, scores, venue), `BreadcrumbList` for navigation. Use Yoast or Schema Pro plugin. Enables rich snippets (star ratings, event dates) in search results.

**Q75: How do you handle SEO for a WordPress site with lots of duplicate content (e.g., articles appearing in multiple categories)?**  
A: 1) Use canonical URLs (`<link rel="canonical">`) — Yoast handles this automatically. 2) Assign one primary category per post. 3) Use `noindex` on tag archives if thin. 4) Avoid duplicate category/tag pages with similar content. 5) Use 301 redirects for changed URLs. 6) Set a preferred domain (www vs non-www).

**Q76: How do you optimize WordPress site speed for a content-heavy sports publication?**  
A: 1) Caching plugin (WP Super Cache or W3 Total Cache). 2) Image optimization (ShortPixel). 3) Minify CSS/JS (Autoptimize). 4) Use a CDN (Cloudflare). 5) Optimize MySQL queries (reduce autoloaded options). 6) Lazy load images and iframes. 7) Use lightweight theme. 8) Keep plugins minimal (audit regularly). Target: < 3 second load time, > 90 Lighthouse score.

**Q77: What is `robots.txt` and how should SportsOrca configure it?**  
A: `robots.txt` tells crawlers which pages to crawl/ignore. Place at site root. For SportsOrca:

```
User-agent: *
Allow: /
Disallow: /wp-admin/
Disallow: /wp-content/plugins/
Sitemap: https://sportsorca.com/sitemap.xml
```

This allows full crawling of articles while blocking admin areas and plugin directories.

## 8. Cross-Browser & Mobile Testing (Q78–Q84)

**Q78: Why is cross-browser testing important for a sports publication?**  
A: Readers access SportsOrca from diverse browsers (Chrome, Safari, Firefox, Edge) and devices. A broken layout on Safari mobile means losing iOS readers. Cross-browser testing ensures consistent experience: images load correctly, navigation works, interactive elements (live scores, video embeds) function, and typography renders properly across all platforms.

**Q79: What tools do you use for cross-browser and responsive testing?**  
A: Browser DevTools (Chrome, Firefox) device simulation for quick checks. BrowserStack/Sauce Labs for real device testing. Chrome DevTools Lighthouse for performance/accessibility audits. For WordPress specifically: test with different user roles (admin vs editor) and check both admin preview and front-end rendering.

**Q80: How do you test a WordPress page on mobile view without a physical device?**  
A: Use Chrome DevTools → Toggle Device Toolbar (Ctrl+Shift+M). Select preset devices (iPhone 14, iPad, Galaxy S23). Check: text readability, image scaling, navigation usability, touch targets (min 44×44px), tap targets not overlapping, and horizontal scrolling. Also test with Firefox Responsive Design Mode.

**Q81: What are common mobile layout issues in WordPress themes?**  
A: Common issues: 1) Horizontal overflow (fixed-width elements), 2) Text too small to read (< 16px), 3) Buttons/links too close together, 4) Images overflowing containers, 5) Navigation menu not collapsing to hamburger, 6) Tables overflowing on small screens, 7) Fixed headers covering content on scroll, 8) Video embeds not scaling.

```css
/* Common fix for overflow */
.article-content img { max-width: 100%; height: auto; }
.article-content table { display: block; overflow-x: auto; }
```

**Q82: What are media queries breakpoints and what are standard ones for SportsOrca?**  
A: Breakpoints are pixel widths where CSS changes layout. Standard: 480px (small phones), 768px (tablets), 1024px (small desktops/laptops), 1200px (large desktops). SportsOrca should add a breakpoint around 1400px for very wide displays. Always use `min-width` for mobile-first approach.

```css
/* SportsOrca breakpoints */
@media (min-width: 480px)  { /* large phone */ }
@media (min-width: 768px)  { /* tablet */ }
@media (min-width: 1024px) { /* desktop */ }
@media (min-width: 1200px) { /* large desktop */ }
```

**Q83: How do you test that a WordPress page displays correctly after making edits?**  
A: 1) Preview changes before publishing (WordPress Preview button). 2) Check admin view and front-end view. 3) Test on desktop and mobile (DevTools). 4) Clear cache (browser + any caching plugin) to see fresh version. 5) Check across Chrome, Firefox, Safari. 6) Verify images load, links work, formatting is correct. 7) Log out to see as a non-admin visitor.

**Q84: What is the viewport meta tag and why is it essential?**  
A: The viewport meta tag tells mobile browsers to use the device's screen width and set initial scale. Without it, mobile browsers render at desktop width and zoom out — making text unreadable. Every WordPress page must include this.

```html
<meta name="viewport" content="width=device-width, initial-scale=1.0">
```

WordPress includes this by default in modern themes, but always verify it's present when customizing templates.

## 9. Git, Tools & Development Workflow (Q85–Q90)

**Q85: How do you use Git in a WordPress development workflow?**  
A: 1) Version control theme files and custom plugins (not `wp-content/uploads`). 2) Use `.gitignore` to exclude `wp-config.php`, `uploads/`, `node_modules/`. 3) Branch for features: `git checkout -b feature/sports-score-widget`. 4) Commit with descriptive messages. 5) Pull requests for code review before merging. Tools: GitHub, GitLab, or Bitbucket.

**Q86: Write a `.gitignore` appropriate for a WordPress project.**  
A: 

```
# WordPress core (if using WP-CLI for core management)
wp-config.php
wp-content/uploads/
wp-content/cache/
wp-content/plugins/*
!wp-content/plugins/custom-plugin/
wp-content/themes/flavor/node_modules/

# Environment
.env
*.log

# OS
.DS_Store
Thumbs.db

# IDE
.idea/
.vscode/
```

**Q87: What is LocalWP (Local by Flywheel) and how does it help WordPress development?**  
A: LocalWP is a free local WordPress development environment. It spins up a local server (Apache/Nginx + MySQL + PHP) with one click. Features: SSL support, live links for sharing, database access, log viewing, and blueprint templates. Much faster than developing directly on a remote server.

**Q88: How would you deploy changes from local development to SportsOrca's production WordPress site?**  
A: 1) Push theme/plugin changes to Git repository. 2) On production, pull changes (or use CI/CD). 3) For content changes: make directly in WordPress admin (staging → production). 4) For theme updates: use staging site first, test, then push to production. 5) Always backup before deploying. 6) Use FTP/SFTP for file uploads if Git isn't set up on the server.

**Q89: What is WP-CLI and what are its common commands?**  
A: WP-CLI is the command-line interface for WordPress. Common commands: `wp core update`, `wp plugin install yoast-seo`, `wp post list --post_status=publish`, `wp db export backup.sql`, `wp theme activate flavor`, `wp user list`. Essential for batch operations, automation, and server management without the admin UI.

```bash
wp post list --post_type=post --post_status=publish --fields=ID,post_title,post_date --format=table
wp db query "SELECT COUNT(*) FROM wp_posts WHERE post_status='publish'"
```

**Q90: What is the difference between a staging site and a production site?**  
A: Production is the live public website. Staging is an identical copy used for testing changes safely. Before deploying new themes, plugins, or code changes: test on staging → verify everything works → deploy to production. This prevents breaking the live site. Many hosts (WP Engine, Kinsta) provide one-click staging.

## 10. Behavioral & SportsOrca-Specific (Q91–Q98)

**Q91: Why are you interested in a Full Stack Development Internship at SportsOrca?**  
A: SportsOrca combines my technical skills (JavaScript, React, MySQL) with a domain I'm passionate about. Sports publications require both technical precision (CMS management, responsive design) and editorial care (proofreading, content accuracy). This role lets me apply my attention to detail while learning WordPress — a platform powering millions of sites. The 3-month WFH structure aligns well with my current B.Tech schedule.

**Q92: How does your background in React/Next.js translate to WordPress development?**  
A: React/Next.js taught me component thinking, state management, and JavaScript fundamentals that directly apply to WordPress front-end work. The WordPress REST API is fetch-based like any modern API I've worked with. HTML/CSS skills transfer 100%. PHP is a new language but my experience with Python (FastAPI) and JavaScript means I understand server-side patterns, templating, and database interaction — PHP's learning curve is significantly lower for me.

**Q93: Describe your attention to detail process. How would you approach reviewing all pages on SportsOrca's website?**  
A: I would create a systematic checklist: 1) Crawl the full sitemap and list every page. 2) Check each page for: typos, broken links, image issues (alt text, sizing), formatting inconsistencies, and mobile responsiveness. 3) Document findings in a spreadsheet (page, issue type, severity, fix status). 4) Prioritize critical issues (broken content, typos in headlines) over cosmetic ones. 5) Fix in batches and re-verify. This methodical approach mirrors how I debug code — systematic, documented, and thorough.

**Q94: How do you handle working independently in a remote internship?**  
A: From my Agentic AI Internship (fully remote), I developed a routine: start each day with a task list, communicate progress daily via Slack/email, block focus hours for deep work (content review, coding), and proactively ask questions when stuck rather than spinning. I use tools like Notion for task tracking and Git for code versioning to stay organized and accountable.

**Q95: A sports article you're reviewing has the correct information but reads awkwardly. How do you handle it?**  
A: I'd rewrite for clarity while preserving the factual content and the original author's intent. For example: "The game was won by the team in a very good performance" → "The team delivered a dominant performance to secure the win." I'd flag the change in WordPress's revision notes so editors can review. The goal is improved readability without altering meaning or adding opinions.

**Q96: How do you prioritize tasks when you have multiple articles to review, a broken image on the homepage, and a formatting issue on mobile?**  
A: 1) Fix the broken homepage image first — it's high-visibility and likely quick. 2) Address the mobile formatting issue — affects a significant portion of users. 3) Process articles in deadline order — most time-sensitive first. Communicate with the team about the timeline for each item so expectations are aligned.

**Q97: What sports do you follow, and how does that knowledge benefit SportsOrca?**  
A: (Tailor to actual knowledge — sample answer) I follow NFL and NBA closely, with growing interest in soccer (Premier League). Understanding sports context means I can spot factual errors a non-fan wouldn't — wrong team names, outdated roster info, or misattributed statistics. It also helps with content categorization, tagging, and understanding what readers expect from quality sports journalism.

**Q98: Where do you see yourself after this 3-month internship?**  
A: I aim to leave SportsOrca with solid WordPress development skills, a proven ability to manage CMS content accurately, and a portfolio of contributions to a live sports publication. I'd like to have become proficient enough in WordPress/PHP to contribute independently, and ideally have built or improved a feature (like a custom score widget or content template) that adds lasting value to the site.

## 11. Scenario-Based & Problem Solving (Q99–Q100)

**Q99: You notice that after a WordPress update, the SportsOrca homepage layout is broken — the sidebar has shifted below the main content. Walk me through your debugging process.**  
A: 1) Check if it's a caching issue first — clear WP cache + browser cache. 2) Verify in Chrome DevTools which element is breaking the layout (inspect the grid/flex container). 3) Check if the theme's `style.css` or `functions.php` has conflicts with the new WordPress version. 4) Test with default theme (Twenty Twenty-Four) — if layout works, the issue is in the active theme. 5) Check plugin conflicts by deactivating plugins one by one. 6) If the issue is in the theme, inspect the CSS for specificity conflicts or deprecated functions. 7) Roll back theme changes via Git if version-controlled, or use the child theme to apply CSS fixes. 8) Test fix on staging before applying to production.

```css
/* Quick fix if it's a flex container issue */
.page-layout {
    display: flex;
    flex-wrap: nowrap; /* Prevent wrapping */
    gap: 2rem;
}
.main-content { flex: 1; min-width: 0; }
.sidebar { flex: 0 0 300px; }
```

**Q100: You're tasked with creating a new article template for "Game Recap" articles on SportsOrca. What would this template include and how would you implement it?**  
A: The template should include: 1) Hero image with game action shot and caption. 2) Game metadata block (teams, final score, venue, date, attendance). 3) Article body with proper heading hierarchy. 4) Key statistics sidebar (team stats comparison table). 5) Related games/articles section. 6) Social sharing buttons. 7) Comments section. 8) Author bio with byline.

Implementation in a WordPress child theme:

```php
<?php
/* Template Name: Game Recap */
get_header();
while (have_posts()) : the_post();
    $home = get_post_meta(get_the_ID(), 'home_team', true);
    $away = get_post_meta(get_the_ID(), 'away_team', true);
    $score = get_post_meta(get_the_ID(), 'final_score', true);
?>
<article class="game-recap">
    <div class="game-hero">
        <?php the_post_thumbnail('full', ['alt' => get_the_title()]); ?>
        <div class="score-overlay">
            <span class="away-team"><?= esc_html($away); ?></span>
            <span class="score"><?= esc_html($score); ?></span>
            <span class="home-team"><?= esc_html($home); ?></span>
        </div>
    </div>
    <header class="recap-header">
        <h1><?php the_title(); ?></h1>
        <div class="meta">
            <time datetime="<?= get_the_date('c'); ?>"><?= get_the_date('F j, Y'); ?></time>
            <span class="author">By <?php the_author(); ?></span>
        </div>
    </header>
    <div class="recap-body">
        <div class="main-column"><?php the_content(); ?></div>
        <aside class="stats-sidebar">
            <h3>Key Stats</h3>
            <?php get_template_part('template-parts/game-stats'); ?>
        </aside>
    </div>
    <?php get_template_part('template-parts/related-games'); ?>
</article>
<?php endwhile;
get_footer();
```
