# Basti Ki Pathshala Foundation — 100 Full Stack Interview Q&A

> Based on Basti Ki Pathshala Foundation — Full Stack Development Internship (NGO, HTML-focused, education for slum children)  > Candidate: Aayush Gid (Python/JS/React/Next.js/HTML/CSS/REST API background)

---

## 1. HTML & Web Fundamentals (Q1–Q15)

**Q1: What does HTML stand for and what is its role in web development?**  
A: HTML (HyperText Markup Language) is the standard markup language for structuring content on the web. It defines the skeleton of a page using elements like headings, paragraphs, links, and images that the browser renders.

**Q2: What is the difference between an element and a tag in HTML?**  
A: A tag is the markup written between angle brackets (e.g., `<p>`), while an element is the complete structure including the opening tag, content, and closing tag (e.g., `<p>Hello</p>`).

**Q3: Explain the structure of a basic HTML5 document.**  
A: A minimal HTML5 document has the doctype declaration, `html` root, `head` (with `meta` charset and `title`), and `body` with visible content:
```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Basti Ki Pathshala</title>
</head>
<body>
  <h1>Welcome</h1>
</body>
</html>
```

**Q4: What are semantic HTML elements and why are they important?**  
A: Semantic elements like `<header>`, `<nav>`, `<article>`, `<section>`, and `<footer>` describe their meaning. They improve accessibility for screen readers, boost SEO, and make the code more readable and maintainable.

**Q5: What is the difference between `<div>` and `<span>`?**  
A: `<div>` is a block-level element used to group large sections of content. `<span>` is an inline element used to wrap and style small pieces of text within a line.

**Q6: How do you create a hyperlink in HTML?**  
A: Use the anchor tag with an `href` attribute pointing to the destination URL:
```html
<a href="https://bastikipathshala.org">Visit Basti Ki Pathshala</a>
```

**Q7: What is the purpose of the `alt` attribute on images?**  
A: The `alt` attribute provides alternative text for screen readers and displays when an image fails to load, improving accessibility and SEO.

**Q8: How do you embed an image in an HTML page?**  
A: Use the `<img>` tag with `src` for the image path and `alt` for description:
```html
<img src="classroom.jpg" alt="Students learning in classroom" width="600">
```

**Q9: What are the main HTML heading levels and their hierarchy?**  
A: HTML has six heading levels from `<h1>` (most important, usually one per page) down to `<h6>` (least important). They form a document outline and hierarchy.

**Q10: What is the difference between `<ul>`, `<ol>`, and `<dl>`?**  
A: `<ul>` creates an unordered (bulleted) list, `<ol>` creates an ordered (numbered) list, and `<dl>` creates a description list with term/definition pairs.

**Q11: How do you create a table in HTML?**  
A: Use `<table>` with `<thead>`, `<tbody>`, `<tr>` for rows, `<th>` for headers, and `<td>` for data cells:
```html
<table>
  <thead><tr><th>Name</th><th>Role</th></tr></thead>
  <tbody><tr><td>Aayush</td><td>Intern</td></tr></tbody>
</table>
```

**Q12: What is the purpose of the `meta` viewport tag?**  
A: It controls how the page scales on different devices. The standard responsive tag is:
```html
<meta name="viewport" content="width=device-width, initial-scale=1.0">
```
Without it, mobile browsers may render the page at a desktop width.

**Q13: What are HTML entities and when do you use them?**  
A: HTML entities display reserved characters that have special meaning in HTML. For example, `&lt;` for `<`, `&gt;` for `>`, and `&amp;` for `&`. Use them when you need to display these characters as literal text.

**Q14: Explain the difference between `<head>` and `<body>`.**  
A: `<head>` contains metadata not displayed directly — title, character set, linked stylesheets, and scripts. `<body>` holds all visible content that users see and interact with.

**Q15: What is the `lang` attribute on the `<html>` tag and why does it matter?**  
A: The `lang` attribute specifies the document's language (e.g., `lang="en"`). It helps screen readers pronounce content correctly and helps search engines serve the right language version.

---

## 2. CSS & Styling Basics (Q16–Q26)

**Q16: What is CSS and how do you include it in an HTML page?**  
A: CSS (Cascading Style Sheets) controls the visual presentation. Include it via an external `<link>` tag, an internal `<style>` block, or inline `style` attributes. External stylesheets are preferred for reusability.

**Q17: Explain the CSS box model.**  
A: Every element consists of content, padding (space inside border), border, and margin (space outside border). Setting `box-sizing: border-box` makes width/height include padding and border, simplifying layout calculations.

**Q18: What is the difference between a class and an ID selector in CSS?**  
A: A class (`.classname`) can be applied to multiple elements and is reusable. An ID (`#idname`) must be unique per page and has higher specificity.

**Q19: How do you center a div both horizontally and vertically?**  
A: The simplest modern approach uses Flexbox:
```css
.container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
}
```

**Q20: What is the difference between `display: block`, `inline`, and `inline-block`?**  
A: `block` elements take full width and start on a new line. `inline` elements flow within text and ignore width/height. `inline-block` flows inline but respects width, height, and vertical margin/padding.

**Q21: How do you change fonts in CSS?**  
A: Use the `font-family` property with fallbacks. Google Fonts can be linked in the `<head>`:
```html
<link href="https://fonts.googleapis.com/css2?family=Roboto&display=swap" rel="stylesheet">
```
```css
body { font-family: 'Roboto', Arial, sans-serif; }
```

**Q22: What are CSS colors and how do you specify them?**  
A: Colors can be specified by name (`red`), hex (`#FF0000`), RGB (`rgb(255,0,0)`), RGBA (with transparency), or HSL. Hex and named colors are most common in simple projects.

**Q23: How do you add background images in CSS?**  
A: Use the `background-image` property along with `background-size` and `background-repeat`:
```css
.hero {
  background-image: url('classroom.jpg');
  background-size: cover;
  background-position: center;
}
```

**Q24: What is a CSS transition and how do you use one?**  
A: Transitions smoothly animate property changes over a duration. Useful for hover effects on buttons or links:
```css
.btn {
  background: #2563eb;
  transition: background 0.3s ease;
}
.btn:hover { background: #1d4ed8; }
```

**Q25: What is the difference between `position: relative`, `absolute`, `fixed`, and `sticky`?**  
A: `relative` offsets from the normal position. `absolute` positions relative to the nearest positioned ancestor. `fixed` positions relative to the viewport and stays on scroll. `sticky` toggles between relative and fixed based on scroll position.

**Q26: How do you make a website visually appealing for an NGO like Basti Ki Pathshala?**  
A: Use warm, approachable colors (oranges, greens), large readable fonts, plenty of whitespace, real photos of classrooms/students (with consent), clear calls-to-action like "Donate" or "Volunteer," and a clean, uncluttered layout that builds trust.

---

## 3. Responsive Design & Mobile-Friendly Websites (Q27–Q35)

**Q27: What is responsive web design and why is it important for an NGO?**  
A: Responsive design ensures a website looks and works well on all devices — phones, tablets, and desktops. For an NGO, many visitors will use budget Android phones, so mobile-first responsive design is essential.

**Q28: What is a mobile-first design approach?**  
A: Design and code for the smallest screen first, then use `min-width` media queries to add complexity for larger screens. This ensures core content is always accessible on low-bandwidth mobile connections.

**Q29: How do media queries work in CSS?**  
A: Media queries apply styles based on device characteristics like width:
```css
/* Mobile first — base styles for small screens */
.container { padding: 1rem; }

/* Tablet and up */
@media (min-width: 768px) {
  .container { padding: 2rem; max-width: 960px; margin: auto; }
}
```

**Q30: What is a fluid layout and how do you create one?**  
A: A fluid layout uses percentage-based widths instead of fixed pixels so elements resize with the viewport:
```css
.card { width: 100%; }
@media (min-width: 768px) { .card { width: 48%; } }
```

**Q31: How do you make images responsive in HTML/CSS?**  
A: Set `max-width: 100%` and `height: auto` on images so they never overflow their container:
```css
img { max-width: 100%; height: auto; }
```
This ensures images scale down gracefully on small screens.

**Q32: What is the CSS Grid layout and when should you use it?**  
A: CSS Grid is a two-dimensional layout system for arranging items in rows and columns. Use it for page-level layouts like a dashboard or photo gallery:
```css
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1rem;
}
```

**Q33: What is Flexbox and when is it preferred over Grid?**  
A: Flexbox is one-dimensional (row OR column) and ideal for aligning items within a single axis — navigation bars, card rows, centering content. Grid is better for complex two-dimensional layouts.

**Q34: Why might a phone show the desktop version of a site instead of mobile?**  
A: Usually because the `<meta name="viewport">` tag is missing. Without it, mobile browsers assume a ~980px viewport and zoom out to fit the full desktop page.

**Q35: How would you ensure a Basti Ki Pathshala website works on a cheap Android phone with a small screen?**  
A: Use mobile-first CSS, large touch targets (min 44px), readable font sizes (min 16px), compressed images (WebP format), minimal JavaScript, and test on real low-end devices. Avoid heavy animations and large background videos.

---

## 4. Web Accessibility & Best Practices (Q36–Q43)

**Q36: What is web accessibility and why does it matter for an education NGO?**  
A: Web accessibility means making websites usable by everyone, including people with disabilities. For an NGO serving slum communities, many users may share old devices, have low literacy, or use screen readers — accessible design ensures no one is excluded.

**Q37: What are ARIA roles and when should you use them?**  
A: ARIA (Accessible Rich Internet Applications) attributes add semantic meaning to elements that lack it. Use `role="button"` or `aria-label` when native HTML elements don't convey the purpose:
```html
<button aria-label="Donate now">❤️</button>
```

**Q38: How do you ensure color contrast is sufficient for readability?**  
A: Use tools like the WebAIM Contrast Checker. The WCAG AA standard requires a contrast ratio of at least 4.5:1 for normal text and 3:1 for large text. Avoid light gray text on white backgrounds.

**Q39: Why should you use proper heading hierarchy (h1 > h2 > h3)?**  
A: Screen readers use headings to navigate pages. Skipping levels (e.g., h1 directly to h3) confuses assistive technology users. A logical hierarchy also helps SEO by showing content structure.

**Q40: What is the purpose of the `title` attribute on a link?**  
A: The `title` attribute provides advisory information that typically shows as a tooltip on hover. It can add context but should not be the only way to convey information since it's not accessible to keyboard-only users.

**Q41: How do you make a form accessible?**  
A: Use `<label>` elements explicitly associated with inputs via `for`/`id`, group related fields with `<fieldset>` and `<legend>`, provide clear error messages, and ensure all inputs are keyboard-navigable:
```html
<label for="name">Your Name:</label>
<input type="text" id="name" name="name" required>
```

**Q42: What is the `tabindex` attribute and when should you use it?**  
A: `tabindex` controls the tab order of focusable elements. Use `tabindex="0"` to add a non-interactive element to the natural tab order, and `tabindex="-1"` to make something focusable via script but not tab. Avoid positive values.

**Q43: What is lazy loading and how do you implement it for images?**  
A: Lazy loading defers loading of off-screen images until the user scrolls near them, improving page speed. Add the `loading="lazy"` attribute:
```html
<img src="classroom.jpg" alt="Classroom" loading="lazy">
```

---

## 5. Forms & User Interaction (Q44–Q52)

**Q44: How do you create a contact form in HTML?**  
A: Use the `<form>` element with `method="POST"` and `action` pointing to a backend or email service. Include labeled inputs for name, email, and message:
```html
<form action="/contact" method="POST">
  <label for="name">Name</label>
  <input type="text" id="name" name="name" required>
  <label for="email">Email</label>
  <input type="email" id="email" name="email" required>
  <label for="msg">Message</label>
  <textarea id="msg" name="message" required></textarea>
  <button type="submit">Send</button>
</form>
```

**Q45: What input types does HTML5 provide?**  
A: HTML5 added types like `email`, `url`, `number`, `date`, `tel`, `search`, `color`, and `range`. These provide built-in validation and better mobile keyboards (e.g., numeric keypad for `number`).

**Q46: How do you validate a form without JavaScript?**  
A: Use HTML5 validation attributes: `required`, `type="email"`, `minlength`, `maxlength`, `pattern`, and `min`/`max` for numbers. The browser natively shows error messages for invalid inputs.

**Q47: What is the difference between `GET` and `POST` form methods?**  
A: `GET` appends form data to the URL (visible, limited size, good for search). `POST` sends data in the request body (hidden, no size limit, used for submissions that modify data like donations or registrations).

**Q48: How do you create a donation form for the NGO website?**  
A: Include fields for donor name, email, amount (radio buttons or input), and an optional message. Use `POST` method and a payment gateway integration. Keep it simple and trustworthy:
```html
<form action="/donate" method="POST">
  <input type="number" name="amount" min="10" placeholder="Amount (₹)" required>
  <input type="email" name="email" placeholder="Your Email" required>
  <button type="submit">Donate Now</button>
</form>
```

**Q49: What is the `<select>` element and how do you use it?**  
A: `<select>` creates a dropdown menu with `<option>` elements inside. Use it for fixed choices like state, category, or donation frequency:
```html
<select name="city" id="city">
  <option value="">Select City</option>
  <option value="delhi">Delhi</option>
  <option value="mumbai">Mumbai</option>
</select>
```

**Q50: How do you create a multi-step form?**  
A: Use multiple `<fieldset>` or `<div>` sections, showing one at a time with CSS (`display: none`) and JavaScript to toggle between steps. Each step has a "Next" and "Back" button.

**Q51: What is the `placeholder` attribute and should you rely on it?**  
A: Placeholder text appears inside an input field before the user types, giving a hint about expected input. It should supplement, not replace, `<label>` elements because placeholders disappear on focus and aren't always read by screen readers.

**Q52: How do you handle file uploads in an HTML form?**  
A: Use `<input type="file">`. Set `enctype="multipart/form-data"` on the form for the file data to be transmitted correctly:
```html
<form action="/upload" method="POST" enctype="multipart/form-data">
  <input type="file" name="photo" accept="image/*">
  <button type="submit">Upload</button>
</form>
```

---

## 6. JavaScript Basics for Web (Q53–Q60)

**Q53: What is JavaScript and how do you add it to an HTML page?**  
A: JavaScript adds interactivity to web pages. Include it via an inline `<script>` tag, an external `.js` file with `<script src="app.js">`, or a CDN link. Place it before `</body>` or use `defer`.

**Q54: How do you select an element in the DOM with JavaScript?**  
A: Use `document.getElementById()`, `document.querySelector()`, or `document.querySelectorAll()`:
```js
const heading = document.querySelector('h1');
const buttons = document.querySelectorAll('.btn');
```

**Q55: How do you add an event listener to a button?**  
A: Use `addEventListener` with the event type and callback:
```js
document.querySelector('#donateBtn').addEventListener('click', () => {
  alert('Thank you for your generosity!');
});
```

**Q56: What is the difference between `var`, `let`, and `const`?**  
A: `var` is function-scoped and hoisted. `let` is block-scoped and can be reassigned. `const` is block-scoped and cannot be reassigned (though objects/arrays can still be mutated). Always prefer `const` by default, `let` when reassignment is needed.

**Q57: How do you show a simple alert or confirmation in JavaScript?**  
A: Use `alert()` for a notification, `confirm()` for a yes/no prompt, and `prompt()` for user input:
```js
if (confirm('Are you sure you want to donate?')) {
  // proceed
}
```

**Q58: How do you validate a form using JavaScript before submission?**  
A: Listen for the `submit` event, check field values, and prevent default submission if invalid:
```js
form.addEventListener('submit', (e) => {
  if (!email.value.includes('@')) {
    e.preventDefault();
    alert('Please enter a valid email.');
  }
});
```

**Q59: What is the DOM in simple terms?**  
A: The DOM (Document Object Model) is the browser's representation of an HTML page as a tree of objects. JavaScript can read, add, modify, or delete elements and attributes through the DOM API.

**Q60: How do you dynamically change the content of an HTML element with JavaScript?**  
A: Use `.textContent` for plain text or `.innerHTML` for HTML content:
```js
document.querySelector('#counter').textContent = '50 students enrolled';
```

---

## 7. WordPress & CMS Basics (Q61–Q67)

**Q61: What is WordPress and why might an NGO use it?**  
A: WordPress is an open-source CMS that powers over 40% of websites. NGOs use it because it's free, easy for non-technical staff to update content (blog posts, events, donation pages), and has thousands of themes and plugins.

**Q62: What is the difference between WordPress.com and WordPress.org?**  
A: WordPress.org is self-hosted — you install it on your own server and have full control. WordPress.com is a hosted service by Automattic with free and paid plans but less customization.

**Q63: What is a WordPress theme and how does it work?**  
A: A theme controls the visual design and layout of a WordPress site. Activate a theme from Appearance > Themes and customize it through the Customizer. Many free themes work well for NGO websites.

**Q64: What are WordPress plugins and how do you use them?**  
A: Plugins add functionality — contact forms, SEO, donation tracking, image galleries. Install from Plugins > Add New. For an NGO, useful plugins include Contact Form 7, Yoast SEO, and WP Super Cache.

**Q65: How do you create a page in WordPress?**  
A: Go to Pages > Add New, add a title and content using the block editor (Gutenberg), and click Publish. Pages are for static content like "About Us" or "Donate," while posts are for blog entries.

**Q66: What is the WordPress block editor (Gutenberg)?**  
A: Gutenberg is WordPress's visual editor that uses content blocks (paragraphs, images, columns) instead of a plain text area. Each block can be styled individually, making it easy for non-technical users.

**Q67: What are the limitations of WordPress compared to custom HTML/CSS websites?**  
A: WordPress themes can be slower, harder to fully customize, and vulnerable to plugin conflicts or security issues. A custom HTML/CSS site gives complete control over performance and design but requires more technical skill to maintain.

---

## 8. Web Development for NGOs & Education (Q68–Q76)

**Q68: What are the key pages every NGO website should have?**  
A: Essential pages include: Home (mission & impact), About Us (team & story), Programs (what they do), Donate (with clear CTA), Contact (form & address), Blog/News (updates), and Volunteer (sign-up form).

**Q69: How should a donation page be designed for maximum conversions?**  
A: Keep it simple — predefined amount buttons (₹100, ₹500, ₹1000), a custom amount field, minimal form fields, trusted payment logos, a progress bar for campaigns, and a heartfelt story or photo above the fold.

**Q70: How can you use HTML to showcase an NGO's impact?**  
A: Use stat counters, testimonials in blockquotes, image galleries of activities, before/after comparisons, and embedded videos. Semantic HTML with proper `alt` text ensures these stories reach everyone.

**Q71: What kind of content should an education NGO website feature?**  
A: Student success stories, program outcomes (literacy rates, enrollment numbers), volunteer testimonials, photos from classrooms, upcoming events, and transparent financial reports showing how donations are used.

**Q72: Why is page speed important for an NGO website?**  
A: Many supporters browse on slow mobile connections in India. A fast-loading page reduces bounce rates and increases donations. Optimize images, use minimal JavaScript, leverage browser caching, and use a CDN.

**Q73: How do you make a website feel trustworthy for an NGO?**  
A: Display the government registration number, show real team photos (not stock images), include verified testimonials, provide transparent financial information, use HTTPS, and feature logos of partner organizations.

**Q74: What is SEO and why does it matter for an NGO?**  
A: SEO (Search Engine Optimization) helps the website appear in Google searches. For an NGO, good SEO means more visibility, more donations, and more volunteers finding the organization organically without ad spend.

**Q75: What basic SEO practices can you implement with HTML?**  
A: Use descriptive `<title>` tags, meta descriptions, semantic HTML headings, `alt` text on images, descriptive link text, clean URL structures, and a `robots.txt` file.

**Q76: How can you embed a Google Map on an NGO website?**  
A: Use an `<iframe>` from Google Maps:
```html
<iframe src="https://maps.google.com/maps?q=delhi&t=&z=13&ie=UTF8&iwloc=&output=embed"
  width="100%" height="300" style="border:0;" allowfullscreen loading="lazy">
</iframe>
```

---

## 9. UI/UX Collaboration & Design Principles (Q77–Q83)

**Q77: What is the difference between UI and UX design?**  
A: UI (User Interface) deals with the visual look — colors, typography, buttons. UX (User Experience) deals with how the site feels — navigation flow, ease of use, and overall satisfaction. Both are important for a good website.

**Q78: How do you collaborate with UI/UX designers as a developer?**  
A: Review mockups early, ask questions about interactions and edge cases, implement designs faithfully in HTML/CSS, provide feedback on technical feasibility, and iterate together. Use tools like Figma for design handoff.

**Q79: What is a call-to-action (CTA) and why is it important?**  
A: A CTA is a button or link that prompts a specific action — "Donate Now," "Volunteer Today," "Learn More." CTAs should be visually prominent, use action-oriented text, and be placed strategically on the page.

**Q80: What is visual hierarchy and how do you create it?**  
A: Visual hierarchy guides the eye to the most important elements first. Create it with size (larger = more important), color contrast, spacing, font weight, and placement (top-left gets more attention in left-to-right languages).

**Q81: What is whitespace and why is it important?**  
A: Whitespace (negative space) is the empty area around elements. It reduces clutter, improves readability, creates visual breathing room, and gives a professional, trustworthy feel — critical for an NGO website.

**Q82: What are wireframes and how do they help development?**  
A: Wireframes are low-fidelity layouts showing the structure and placement of elements without detailed design. They help developers understand the page layout, content hierarchy, and functionality before visual design begins.

**Q83: How do you ensure consistency across pages of a website?**  
A: Use a shared CSS file with common styles for typography, colors, button styles, and spacing. Create reusable HTML components (header, footer, navigation) and include them on every page. A style guide helps maintain consistency.

---

## 10. Debugging, Testing & Deployment (Q84–Q89)

**Q84: How do you debug HTML/CSS issues in a browser?**  
A: Right-click an element and select "Inspect" to open browser DevTools. Use the Elements tab to view and modify HTML/CSS live, the Console for JavaScript errors, and the Network tab to check for failed requests.

**Q85: What is the browser console and how do you use it for debugging?**  
A: The console (F12 > Console tab) shows JavaScript errors, warnings, and `console.log()` output. It's the first place to check when something isn't working on a page.

**Q86: What are common HTML/CSS mistakes beginners make?**  
A: Missing closing tags, missing `alt` attributes on images, not including the viewport meta tag, using `<div>` for everything instead of semantic elements, and not testing on mobile devices.

**Q87: How do you test a website on different devices and browsers?**  
A: Use browser DevTools device toolbar for responsive testing, BrowserStack or similar for cross-browser testing, and physically test on real devices when possible — especially low-end Android phones for Indian audiences.

**Q88: What is version control and why should you use Git?**  
A: Git tracks changes to code over time, allowing you to revert mistakes, collaborate with others, and maintain a history. Push code to GitHub for backup and team collaboration. Use meaningful commit messages.

**Q89: How do you deploy a static HTML website for free?**  
A: Use GitHub Pages (push to a `gh-pages` branch), Netlify (drag and drop or Git integration), or Vercel. For WordPress, use shared hosting providers like Hostinger or free tiers of cloud platforms.

---

## 11. Technology Research & Learning (Q90–Q94)

**Q90: How do you stay updated with emerging web technologies?**  
A: Follow MDN Web Docs, CSS-Tricks, freeCodeCamp, and web development YouTube channels. Read blogs from companies like Google and Mozilla. Experiment with new features in personal projects and contribute to open source.

**Q91: What is the difference between a static and dynamic website?**  
A: A static site serves the same pre-built HTML to every visitor (good for simple brochure sites). A dynamic site generates content on the server or client side (good for blogs, e-commerce, and CMS-driven sites like WordPress).

**Q92: What is an API in simple terms?**  
A: An API (Application Programming Interface) is a way for two software systems to communicate. For a website, it might fetch weather data, process payments, or pull social media feeds. It typically sends and receives JSON data.

**Q93: What is hosting and a domain name?**  
A: A domain name is the website's address (e.g., bastikipathshala.org). Hosting is the server where the website files live and are served from. You need both to make a website publicly accessible.

**Q94: What is HTTPS and why is it necessary?**  
A: HTTPS encrypts data between the browser and server, protecting user information. It's essential for any site with forms, donations, or login pages. Free SSL certificates are available from Let's Encrypt.

---

## 12. Behavioral & Motivation Questions (Q95–Q100)

**Q95: Why do you want to intern at Basti Ki Pathshala Foundation?**  
A: I believe technology can amplify the impact of education initiatives. Contributing my web development skills to help an NGO reach more children in slum areas aligns with my goal of using code for social good, even through a small but meaningful project.

**Q96: How do you handle working on a project with a tight deadline?**  
A: I prioritize tasks by impact, break work into smaller chunks, communicate blockers early, and focus on delivering core functionality first. For a 1-week sprint like this internship, I would deliver a clean, working prototype quickly and iterate.

**Q97: How would you explain a technical concept to a non-technical team member?**  
A: I use simple analogies, avoid jargon, show visual examples, and check for understanding. For instance, I'd explain a API as "like a waiter in a restaurant — you tell them what you want, they bring it from the kitchen."

**Q98: What makes you a good fit for a remote, part-time internship?**  
A: I have experience working remotely on projects like GuardrailZ and my AI agent development work. I'm self-disciplined, use Git for async collaboration, communicate clearly in written updates, and manage my time effectively alongside academics.

**Q99: How would you contribute to a team that has many interns (20 openings)?**  
A: I'd focus on clear communication, document my work so others can build on it, avoid duplicating efforts, and be flexible in taking on tasks where I can add the most value — whether that's HTML/CSS, debugging, or researching tools.

**Q100: What impact do you hope your work at Basti Ki Pathshala will have?**  
A: I hope to help build a clean, fast, mobile-friendly website that makes it easy for donors to contribute, parents to learn about programs, and volunteers to sign up — ultimately helping more children in underserved communities access quality education.
