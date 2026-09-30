"""HTML snippets: responsive boilerplate, semantic layout, accessible nav/forms,
responsive images, dialog, and a form that submits with AJAX."""

FAMILY = dict(key="html", vscode="html,php", sublime="text.html")

SNIPPETS = [
    ("html5", "HTML5 responsive page", r"""
<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <!-- Responsive: without this, phones render a zoomed-out desktop page -->
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>«1:Page title»</title>
    <meta name="description" content="«2:150-160 characters that appear under the title in search results»">

    <!-- Open Graph: the preview card when the link is shared -->
    <meta property="og:title" content="«1»">
    <meta property="og:description" content="«2»">
    <meta property="og:image" content="«3:/og-image.png»">

    <link rel="icon" href="/favicon.svg" type="image/svg+xml">
    <link rel="stylesheet" href="«4:css/styles.css»">
    <!-- defer: download in parallel, run after the HTML is parsed -->
    <script src="«5:js/main.js»" defer></script>
</head>
<body>
    <a class="skip-link" href="#main">Skip to content</a>
    <header></header>
    <main id="main">
        «0»
    </main>
    <footer></footer>
</body>
</html>
""", {"template": True}),
    ("vp", "viewport meta", r"""
<!-- Required for responsive layouts on mobile -->
<meta name="viewport" content="width=device-width, initial-scale=1">«0»
"""),
    ("layout", "Semantic page layout", r"""
<!-- Semantic landmarks let screen readers jump straight to each region -->
<header class="site-header">
    <nav aria-label="Main">«1»</nav>
</header>
<main id="main">
    <section aria-labelledby="«2:intro»-title">
        <h1 id="«2»-title">«3:Heading»</h1>
        «0»
    </section>
</main>
<aside aria-label="Related"></aside>
<footer class="site-footer"></footer>
"""),
    ("nav", "Responsive nav with toggle", r"""
<!-- Mobile: button toggles the menu. Desktop: CSS shows the list and hides the button. -->
<nav class="nav" aria-label="Main">
    <a class="nav__brand" href="/">«1:Brand»</a>
    <button class="nav__toggle" type="button" aria-expanded="false" aria-controls="nav-menu">
        <span class="visually-hidden">Menu</span>☰
    </button>
    <ul class="nav__menu" id="nav-menu">
        <li><a href="/" aria-current="page">Home</a></li>
        <li><a href="/«2:about»">«3:About»</a></li>
        «0»
    </ul>
</nav>
<script>
    // Keep aria-expanded in sync so assistive tech announces the menu state
    const toggle = document.querySelector(".nav__toggle");
    toggle.addEventListener("click", () => {
        const open = toggle.getAttribute("aria-expanded") === "true";
        toggle.setAttribute("aria-expanded", String(!open));
        document.getElementById("nav-menu").classList.toggle("is-open", !open);
    });
</script>
"""),
    ("form", "Accessible form", r"""
<!-- Every input has a <label for>; required + type give free browser validation -->
<form action="«1:/contact»" method="post" novalidate>
    <div class="field">
        <label for="«2:email»">Email</label>
        <input id="«2»" name="«2»" type="email" autocomplete="email" required>
    </div>
    <div class="field">
        <label for="«3:message»">Message</label>
        <textarea id="«3»" name="«3»" rows="5" required></textarea>
    </div>
    <button type="submit">«4:Send»</button>
    <p class="form-status" role="status" aria-live="polite"></p>
    «0»
</form>
"""),
    ("ajaxform", "Form submitted with AJAX (fetch)", r"""
<form id="«1:signup»-form" action="«2:/api/signup»" method="post">
    <label for="«1»-email">Email</label>
    <input id="«1»-email" name="email" type="email" required>
    <button type="submit">Sign up</button>
    <p class="form-status" role="status" aria-live="polite"></p>
</form>
<script>
    // Works without JS (normal POST); with JS it submits in place and reports status
    const form = document.getElementById("«1»-form");
    const status = form.querySelector(".form-status");
    form.addEventListener("submit", async (event) => {
        event.preventDefault();
        status.textContent = "Sending...";
        try {
            const res = await fetch(form.action, { method: "POST", body: new FormData(form) });
            if (!res.ok) throw new Error(`HTTP ${res.status}`);
            status.textContent = "«3:Thanks, you're signed up!»";
            form.reset();
        } catch (err) {
            status.textContent = "Something went wrong. Please try again.";
        }
    });«0»
</script>
"""),
    ("img", "Responsive image (srcset + sizes)", r"""
<!-- srcset lists files by width; sizes tells the browser how wide the image will display,
     so a phone downloads the 480w file and a desktop the 1200w one. -->
<img
    src="«1:photo»-800.jpg"
    srcset="«1»-480.jpg 480w, «1»-800.jpg 800w, «1»-1200.jpg 1200w"
    sizes="(min-width: 1024px) 800px, 100vw"
    width="800" height="533"
    alt="«2:Describe what the image shows»"
    loading="lazy" decoding="async">«0»
"""),
    ("pic", "Art-directed <picture>", r"""
<!-- <picture>: a different crop per screen size (art direction) plus modern formats -->
<picture>
    <source media="(min-width: 1024px)" srcset="«1:hero»-wide.avif" type="image/avif">
    <source media="(min-width: 1024px)" srcset="«1»-wide.jpg">
    <source srcset="«1»-square.avif" type="image/avif">
    <img src="«1»-square.jpg" alt="«2:Describe the image»" width="800" height="800">
</picture>«0»
"""),
    ("table", "Accessible data table", r"""
<!-- caption + th scope let screen readers announce which header each cell belongs to -->
<div class="table-wrap" role="region" aria-label="«1:Orders»" tabindex="0">  <!-- scrolls on small screens -->
    <table>
        <caption>«1»</caption>
        <thead>
            <tr><th scope="col">«2:Name»</th><th scope="col">«3:Total»</th></tr>
        </thead>
        <tbody>
            <tr><td>«0»</td><td></td></tr>
        </tbody>
    </table>
</div>
"""),
    ("card", "Content card", r"""
<article class="card">
    <img class="card__media" src="«1:image.jpg»" alt="" width="400" height="225" loading="lazy">
    <div class="card__body">
        <h3 class="card__title"><a href="«2:#»">«3:Card title»</a></h3>
        <p>«4:Short summary of the content.»</p>
        «0»
    </div>
</article>
"""),
    ("dialog", "Native <dialog> modal", r"""
<!-- Native <dialog>: focus trapping, Esc to close and a backdrop come built in -->
<button type="button" onclick="document.getElementById('«1:confirm»').showModal()">«2:Open»</button>
<dialog id="«1»" aria-labelledby="«1»-title">
    <h2 id="«1»-title">«3:Are you sure?»</h2>
    <form method="dialog">   <!-- method="dialog" closes it and sets returnValue -->
        <button value="cancel">Cancel</button>
        <button value="confirm">Confirm</button>
    </form>
    «0»
</dialog>
"""),
]
