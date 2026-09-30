"""JavaScript / TypeScript snippets shared by .js .ts .jsx .tsx: control flow,
functions, timers, async, AJAX (fetch, XHR, jQuery, axios) and responsive JS."""

FAMILY = dict(
    key="js",
    vscode="javascript,typescript,javascriptreact,typescriptreact",
    sublime="source.js, source.ts, source.jsx, source.tsx",
)

SNIPPETS = [
    ("imp", "Import block (ordered)", r"""
// Import order (industry convention, enforced by eslint-plugin-import / Biome):
// 1. Node built-ins  2. external packages  3. internal aliases (@/...)  4. relative  5. styles
import { «1:readFile» } from "node:«2:fs/promises»";

import «3:React» from "«4:react»";

import { «5:helper» } from "@/«6:lib/helper»";

import { «7:thing» } from "./«8:thing»";
«0»
"""),
    ("module", "ES module file", r"""
/**
 * «1:module-name».js
 * «2:What this module is responsible for.»
 */

// ---- constants ----
const «3:DEFAULT_LIMIT» = «4:20»;

// ---- public API ----
export function «5:doWork»(«6:input») {
    «0»
}
""", {"template": True}),
    ("if", "if statement", r"""
// if: runs when the condition is truthy (not false, 0, "", null, undefined, NaN)
if («1:condition») {
    «0»
}
"""),
    ("ife", "if / else", r"""
// if / else: exactly one branch runs
if («1:condition») {
    «2»
} else {
    «0»
}
"""),
    ("elif", "else-if chain", r"""
// else-if chain: first truthy branch wins; order from most to least specific
if («1:status» === «2:"success"») {
    «3»
} else if («1» === «4:"pending"») {
    «5»
} else {
    «0»
}
"""),
    ("ifn", "Nested if vs guard clauses", r"""
// Nested if: the inner check only runs when the outer one passed
if («1:user») {
    if («1».«2:isActive») {
        «0»
    }
}
// Cleaner alternative (guard clauses):  if (!«1») return;  if (!«1».«2») return;
// Or optional chaining:                 if («1»?.«2») { ... }
"""),
    ("tern", "Ternary / nullish / optional chaining", r"""
// ternary: condition ? whenTrue : whenFalse (an expression, so it can be assigned)
const «1:label» = «2:count» > 0 ? «3:"has items"» : «4:"empty"»;
// ?? falls back only on null/undefined (unlike ||, which also replaces 0 and "")
const «5:name» = «6:input»?.«7:name» ?? «8:"anonymous"»;«0»
"""),
    ("sw", "switch statement", r"""
// switch uses strict equality (===). Forgetting `break` falls into the next case.
switch («1:action».type) {
    case «2:"add"»:
        «3»
        break;
    case «4:"remove"»:
        «5»
        break;
    default:
        «0»
}
"""),
    ("for", "for loop", r"""
// Classic for: use when you need the index or to step by more than 1
for (let «1:i» = 0; «1» < «2:items».length; «1»++) {
    «0»
}
"""),
    ("forof", "for...of loop", r"""
// for...of: iterates VALUES of arrays, strings, Maps, Sets (works with await/break)
for (const «1:item» of «2:items») {
    «0»
}
"""),
    ("forin", "for...in loop", r"""
// for...in: iterates object KEYS. Prefer Object.entries(obj) for key + value.
for (const [«1:key», «2:value»] of Object.entries(«3:obj»)) {
    «0»
}
"""),
    ("fore", "forEach", r"""
// forEach: cannot break early or await; use for...of when you need either
«1:items».forEach((«2:item», «3:index») => {
    «0»
});
"""),
    ("while", "while loop", r"""
// while: checks before each pass; make sure something changes the condition
while («1:condition») {
    «0»
}
"""),
    ("dowhile", "do-while loop", r"""
// do-while: body runs at least once
do {
    «0»
} while («1:condition»);
"""),
    ("try", "try / catch / finally", r"""
// catch receives `unknown` in TS: narrow before using it
try {
    «1»
} catch (err) {
    console.error("«2:operation failed»:", err instanceof Error ? err.message : err);
} finally {
    «0»
}
"""),
    ("fn", "function with JSDoc", r"""
/**
 * «2:What the function does.»
 * @param {«3:string»} «4:value» «5:what it means»
 * @returns {«6:boolean»} «7:what comes back»
 */
function «1:name»(«4») {
    «0»
}
"""),
    ("afn", "arrow function", r"""
// Arrow functions keep the outer `this`; implicit return when the body is one expression
const «1:name» = («2:args») => {
    «0»
};
"""),
    ("asyncfn", "async function", r"""
// async functions always return a Promise; await pauses only this function, not the page
async function «1:loadData»(«2:id») {
    «0»
}
"""),
    ("cls", "class", r"""
// class: # fields are truly private (not reachable from outside)
class «1:Name» {
    #«2:value»;

    constructor(«2») {
        this.#«2» = «2»;
    }

    get «2»() {
        return this.#«2»;
    }
    «0»
}
"""),
    ("destr", "destructuring", r"""
// Destructuring with defaults and renaming
const { «1:id», «2:name»: «3:displayName», «4:role» = «5:"user"» } = «6:obj»;
const [«7:first», ...«8:rest»] = «9:list»;«0»
"""),
    ("mfr", "map / filter / reduce", r"""
// Chain: filter (keep), map (transform), reduce (combine to one value)
const «1:total» = «2:orders»
    .filter((o) => o.«3:paid»)
    .map((o) => o.«4:amount»)
    .reduce((sum, amount) => sum + amount, 0);«0»
"""),
    ("timeout", "setTimeout with cancel", r"""
// setTimeout runs once after the delay; keep the id so you can cancel it
const «1:timerId» = setTimeout(() => {
    «0»
}, «2:1000»);   // milliseconds
// clearTimeout(«1»);  // cancel before it fires (e.g. component unmount)
"""),
    ("interval", "setInterval with cancel", r"""
// setInterval repeats every N ms until cleared. Always clear it, or it leaks.
const «1:intervalId» = setInterval(() => {
    «0»
}, «2:1000»);
// clearInterval(«1»);
"""),
    ("sleep", "sleep / delay promise", r"""
// Promise-based delay: `await sleep(500)` inside an async function
const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));«0»
"""),
    ("debounce", "debounce", r"""
// debounce: wait until calls stop for `wait` ms, then run once (search boxes, resize)
function debounce(fn, wait = «1:300») {
    let timer;
    return (...args) => {
        clearTimeout(timer);
        timer = setTimeout(() => fn(...args), wait);
    };
}«0»
"""),
    ("throttle", "throttle", r"""
// throttle: run at most once per `limit` ms (scroll and mousemove handlers)
function throttle(fn, limit = «1:200») {
    let waiting = false;
    return (...args) => {
        if (waiting) return;
        fn(...args);
        waiting = true;
        setTimeout(() => (waiting = false), limit);
    };
}«0»
"""),
    ("pall", "Promise.all / allSettled", r"""
// Promise.all fails fast on the first rejection; allSettled waits for every result
const [«1:users», «2:posts»] = await Promise.all([«3:getUsers»(), «4:getPosts»()]);
const results = await Promise.allSettled([«5:taskA»(), «6:taskB»()]);
const failed = results.filter((r) => r.status === "rejected");«0»
"""),
    ("fetchget", "AJAX: fetch GET (JSON)", r"""
// fetch only rejects on NETWORK errors. HTTP 404/500 still resolve: check res.ok.
async function «1:getData»() {
    const res = await fetch(«2:"/api/items"», {
        headers: { Accept: "application/json" },
    });
    if (!res.ok) {
        throw new Error(`Request failed: ${res.status} ${res.statusText}`);
    }
    return res.json();
}«0»
"""),
    ("fetchpost", "AJAX: fetch POST (JSON)", r"""
// POST JSON: set Content-Type and stringify the body yourself
async function «1:createItem»(«2:payload») {
    const res = await fetch(«3:"/api/items"», {
        method: "POST",
        headers: { "Content-Type": "application/json", Accept: "application/json" },
        body: JSON.stringify(«2»),
    });
    if (!res.ok) {
        const detail = await res.text();
        throw new Error(`POST failed (${res.status}): ${detail}`);
    }
    return res.json();
}«0»
"""),
    ("fetchtimeout", "AJAX: fetch with timeout / abort", r"""
// AbortSignal.timeout cancels slow requests. Use an AbortController to cancel manually
// (e.g. when the user types again or a React component unmounts).
async function «1:getWithTimeout»(url, ms = «2:8000») {
    try {
        const res = await fetch(url, { signal: AbortSignal.timeout(ms) });
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        return await res.json();
    } catch (err) {
        if (err.name === "TimeoutError") throw new Error(`Timed out after ${ms} ms`);
        throw err;
    }
}«0»
"""),
    ("fetchform", "AJAX: submit a form with fetch", r"""
// Progressive enhancement: the form still works without JS; with JS it submits in place
const «1:form» = document.querySelector(«2:"#contact-form"»);
«1».addEventListener("submit", async (event) => {
    event.preventDefault();
    const button = «1».querySelector("[type=submit]");
    button.disabled = true;   // prevent double submits
    try {
        const res = await fetch(«1».action, { method: «1».method, body: new FormData(«1») });
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        «1».reset();
        «0»
    } catch (err) {
        console.error(err);
    } finally {
        button.disabled = false;
    }
});
"""),
    ("xhr", "AJAX: XMLHttpRequest (legacy)", r"""
// XMLHttpRequest: the original AJAX API. You will meet it in older codebases.
const xhr = new XMLHttpRequest();
xhr.open(«1:"GET"», «2:"/api/items"»);
xhr.responseType = "json";
xhr.onload = () => {
    if (xhr.status >= 200 && xhr.status < 300) {
        «0»console.log(xhr.response);
    } else {
        console.error(`HTTP ${xhr.status}`);
    }
};
xhr.onerror = () => console.error("network error");
xhr.send();
"""),
    ("jqajax", "AJAX: jQuery $.ajax", r"""
// jQuery AJAX (common in WordPress/legacy PHP sites). dataType "json" parses the reply.
$.ajax({
    url: «1:"/api/items"»,
    method: «2:"POST"»,
    contentType: "application/json",
    data: JSON.stringify(«3:payload»),
    dataType: "json",
})
    .done((data) => {
        «0»
    })
    .fail((xhr, status, error) => console.error(status, error));
"""),
    ("axios", "AJAX: axios instance", r"""
import axios from "axios";

// One configured instance per API: base URL, timeout and auth in one place
export const «1:api» = axios.create({
    baseURL: «2:"https://api.example.com"»,
    timeout: «3:10000»,
});

// Interceptors run before every request / after every response
«1».interceptors.request.use((config) => {
    const token = localStorage.getItem("token");
    if (token) config.headers.Authorization = `Bearer ${token}`;
    return config;
});
«1».interceptors.response.use(
    (res) => res,
    (err) => Promise.reject(err.response?.data ?? err),
);«0»
"""),
    ("mq", "Responsive: matchMedia breakpoints", r"""
// Mobile-first breakpoints (same values as Tailwind): mirror your CSS in JS
const BREAKPOINTS = {
    sm: "(min-width: 640px)",   // large phones landscape
    md: "(min-width: 768px)",   // tablets portrait (iPad Mini 768x1024)
    lg: "(min-width: 1024px)",  // tablets landscape / small laptops
    xl: "(min-width: 1280px)",  // laptops and desktops
};

const «1:mql» = window.matchMedia(BREAKPOINTS.«2:md»);
const «3:onChange» = (e) => {
    // e.matches is true when the viewport is at or above the breakpoint
    «0»
};
«1».addEventListener("change", «3»);
«3»(«1»);   // run once for the current size
"""),
    ("clog", "labelled console.log", r"""
console.log("«1:label»:", «2:value»);«0»
"""),
]
