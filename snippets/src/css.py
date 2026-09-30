"""CSS snippets focused on responsive design: breakpoint/device reference,
mobile-first media queries, container queries, fluid type, layout primitives,
user-preference queries, and starter files."""

FAMILY = dict(key="css", vscode="css,scss,less", sublime="source.css, source.scss, source.less")

DEVICE_TABLE = r"""
/* ============================================================
   Breakpoint reference (mobile-first, Tailwind-compatible)
   ------------------------------------------------------------
   base   0-639px   phones portrait    iPhone SE 375x667, iPhone 15 393x852,
                                       Pixel 8 412x915, Galaxy S24 360x780
   sm   >= 640px    phones landscape / small tablets
   md   >= 768px    tablets portrait   iPad Mini 768x1024, iPad 820x1180
   lg   >= 1024px   tablets landscape, small laptops   iPad Pro 1024x1366
   xl   >= 1280px   laptops            1280x800, 1366x768, 1440x900
   2xl  >= 1536px   desktops           1536x864, 1920x1080, 2560x1440
   Design for content, not devices: add a breakpoint where the layout breaks.
   ============================================================ */
"""

SNIPPETS = [
    ("bp", "Breakpoint and device reference", DEVICE_TABLE + "«0»"),
    ("mq", "Mobile-first media query set", DEVICE_TABLE + r"""
/* Base styles (no query) target phones. Each min-width query ADDS to them. */
«1:.selector» {
    «0»
}

@media (min-width: 640px) {   /* sm: large phones landscape */
    «1» { }
}

@media (min-width: 768px) {   /* md: tablets portrait */
    «1» { }
}

@media (min-width: 1024px) {  /* lg: tablets landscape, small laptops */
    «1» { }
}

@media (min-width: 1280px) {  /* xl: laptops and desktops */
    «1» { }
}

@media (min-width: 1536px) {  /* 2xl: large desktops */
    «1» { }
}
"""),
    ("mqmax", "Desktop-first media query set", r"""
/* Desktop-first: base styles target large screens, max-width queries override downward.
   Mobile-first (min-width) is usually preferred; use this when retrofitting a desktop site. */
«1:.selector» { «0» }

@media (max-width: 1279.98px) { «1» { } }   /* below xl: laptops */
@media (max-width: 1023.98px) { «1» { } }   /* below lg: tablets */
@media (max-width: 767.98px)  { «1» { } }   /* below md: phones  */
/* .98 avoids a 1px overlap with min-width queries at the exact breakpoint */
"""),
    ("mqmd", "Media query: tablet and up", r"""
@media (min-width: 768px) {   /* md: iPad Mini portrait (768px) and wider */
    «0»
}
"""),
    ("mqlg", "Media query: laptop and up", r"""
@media (min-width: 1024px) {  /* lg: iPad Pro / small laptops and wider */
    «0»
}
"""),
    ("mqrange", "Media query: range syntax", r"""
/* Media Queries Level 4 range syntax (all modern browsers): reads like maths */
@media («1:768px» <= width < «2:1024px») {   /* tablets only */
    «0»
}
"""),
    ("mqpointer", "Media query: touch vs mouse", r"""
/* Target the input device, not the screen size */
@media (hover: hover) and (pointer: fine) {   /* mouse / trackpad */
    «1:.card»:hover { «0» }
}
@media (pointer: coarse) {                     /* touch: bigger tap targets (44x44px minimum) */
    button, a { min-height: 44px; }
}
"""),
    ("mqmotion", "Media query: reduced motion", r"""
/* Respect users who turned on "reduce motion" in their OS (vestibular disorders) */
@media (prefers-reduced-motion: reduce) {
    *, *::before, *::after {
        animation-duration: 0.01ms !important;
        animation-iteration-count: 1 !important;
        transition-duration: 0.01ms !important;
        scroll-behavior: auto !important;
    }
}«0»
"""),
    ("mqdark", "Media query: dark mode", r"""
/* Follow the OS colour scheme through custom properties */
:root {
    --bg: #ffffff;
    --fg: #1a1a1a;
}
@media (prefers-color-scheme: dark) {
    :root {
        --bg: #111418;
        --fg: #e8eaed;
    }
}
body { background: var(--bg); color: var(--fg); }«0»
"""),
    ("mqorient", "Media query: orientation", r"""
/* Orientation: useful for full-screen layouts like games and galleries */
@media (orientation: landscape) and (max-height: 500px) {   /* phone held sideways */
    «0»
}
"""),
    ("cq", "Container query", r"""
/* Container queries: a component responds to ITS container's width, not the viewport,
   so the same card works in a sidebar and in the main column. */
.«1:card»-wrap {
    container-type: inline-size;
    container-name: «1»;
}

@container «1» (min-width: «2:420px») {
    .«1» {
        display: grid;
        grid-template-columns: 160px 1fr;
        «0»
    }
}
"""),
    ("clamp", "Fluid typography with clamp()", r"""
/* clamp(MIN, PREFERRED, MAX): scales with the viewport, never below MIN or above MAX.
   rem-based min/max keep user font-size preferences working. */
«1:h1» {
    font-size: clamp(«2:1.75rem», «3:1.2rem + 2.5vw», «4:3rem»);«0»
}
"""),
    ("grid", "Responsive grid (no media queries)", r"""
/* auto-fit + minmax: as many columns as fit, each at least «1:16rem» wide.
   The grid reflows from 1 column on phones to 3-4 on desktop by itself. */
.«2:grid» {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(min(«1», 100%), 1fr));
    gap: «3:1.5rem»;«0»
}
"""),
    ("flexc", "Flex center / row that wraps", r"""
/* Center anything horizontally and vertically */
.«1:center» {
    display: flex;
    align-items: center;
    justify-content: center;
}

/* A row that wraps onto new lines on small screens */
.«2:row» {
    display: flex;
    flex-wrap: wrap;
    gap: «3:1rem»;«0»
}
"""),
    ("container", "Responsive page container", r"""
/* Centered, readable max width with side padding that grows on larger screens */
.«1:container» {
    width: min(100% - 2rem, «2:72rem»);
    margin-inline: auto;«0»
}
"""),
    ("vh", "Full-height section (mobile safe)", r"""
/* 100vh is taller than the visible area on mobile (the URL bar). dvh tracks the real height. */
.«1:hero» {
    min-height: 100vh;   /* fallback for old browsers */
    min-height: 100dvh;«0»
}
"""),
    ("srtext", "Visually hidden (screen-reader only)", r"""
/* Hidden visually but still read by screen readers (never use display:none for this) */
.visually-hidden {
    position: absolute !important;
    width: 1px;
    height: 1px;
    padding: 0;
    margin: -1px;
    overflow: hidden;
    clip-path: inset(50%);
    white-space: nowrap;
    border: 0;
}«0»
"""),
    ("tokens", "Design tokens (:root custom properties)", r"""
/* Design tokens: change the look of the whole site from one place */
:root {
    --color-primary: «1:#2563eb»;
    --color-text: #1f2937;
    --color-muted: #6b7280;
    --radius: «2:0.5rem»;
    --space-1: 0.25rem;
    --space-2: 0.5rem;
    --space-4: 1rem;
    --space-8: 2rem;
    --font-sans: system-ui, -apple-system, "Segoe UI", Roboto, sans-serif;
    --shadow: 0 1px 3px rgb(0 0 0 / 0.12);«0»
}
"""),
    ("reset", "Modern CSS reset file", r"""
/* reset.css: a small modern reset. Import before your own styles. */
*, *::before, *::after { box-sizing: border-box; }   /* width includes padding and border */
* { margin: 0; }
html { -webkit-text-size-adjust: 100%; text-size-adjust: 100%; }
body { min-height: 100dvh; line-height: 1.5; -webkit-font-smoothing: antialiased; }
img, picture, video, canvas, svg { display: block; max-width: 100%; }   /* media never overflows */
input, button, textarea, select { font: inherit; }                       /* forms use the page font */
p, h1, h2, h3, h4, h5, h6 { overflow-wrap: break-word; }
:focus-visible { outline: 2px solid currentColor; outline-offset: 2px; } /* keyboard focus stays visible */
«0»
""", {"template": True}),
    ("respfile", "Responsive stylesheet starter", DEVICE_TABLE + r"""
@import url("reset.css");

:root {
    --max-width: «1:72rem»;
    --gutter: clamp(1rem, 4vw, 2rem);
}

.container { width: min(100% - 2 * var(--gutter), var(--max-width)); margin-inline: auto; }

/* ---- base: phones ---- */
.layout { display: grid; gap: var(--gutter); }

/* ---- md: tablets ---- */
@media (min-width: 768px) {
    .layout { grid-template-columns: 1fr 1fr; }
}

/* ---- lg: laptops ---- */
@media (min-width: 1024px) {
    .layout { grid-template-columns: 240px 1fr; }
}
«0»
""", {"template": True}),
]
