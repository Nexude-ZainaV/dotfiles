"""Next.js (App Router, 15/16) snippets: pages, layouts, route handlers,
server actions, loading/error files, metadata, data fetching and proxy."""

FAMILY = dict(
    key="nextjs",
    vscode="typescriptreact,typescript,javascriptreact,javascript",
    sublime="source.tsx, source.ts, source.jsx, source.js",
)

SNIPPETS = [
    ("npage", "Next.js page (server component)", r"""
// app/«1:dashboard»/page.tsx: Server Component by default (runs on the server, no JS shipped)
import type { Metadata } from "next";

export const metadata: Metadata = {
    title: "«2:Dashboard»",
    description: "«3:What this page is for»",
};

export default async function «4:Dashboard»Page() {
    // You can await data directly in a server component
    «0»
    return (
        <main className="mx-auto max-w-5xl p-4 md:p-8">
            <h1 className="text-2xl font-semibold md:text-3xl">«2»</h1>
        </main>
    );
}
""", {"template": True}),
    ("ndynamic", "Next.js dynamic route page", r"""
// app/«1:posts»/[«2:slug»]/page.tsx. Next 15+: params is a Promise, so await it.
import { notFound } from "next/navigation";

type Props = { params: Promise<{ «2»: string }> };

export default async function «3:Post»Page({ params }: Props) {
    const { «2» } = await params;
    const item = await «4:getBySlug»(«2»);
    if (!item) notFound();   // renders not-found.tsx and returns a 404
    «0»
    return <article>{item.title}</article>;
}
""", {"template": True}),
    ("nlayout", "Next.js layout", r"""
// app/layout.tsx: wraps every page beneath it and persists between navigations
import type { Metadata, Viewport } from "next";
import "./globals.css";

export const metadata: Metadata = {
    title: { default: "«1:My App»", template: "%s | «1»" },
    description: "«2:Short description for search and social previews»",
};

// Responsive: width=device-width so mobile browsers do not zoom out a desktop layout
export const viewport: Viewport = { width: "device-width", initialScale: 1 };

export default function RootLayout({ children }: { children: React.ReactNode }) {
    return (
        <html lang="en">
            <body className="min-h-dvh antialiased">«0»{children}</body>
        </html>
    );
}
""", {"template": True}),
    ("nclient", "Next.js client component", r"""
"use client";
// "use client" marks the boundary: this file and its imports ship to the browser.
// Needed for state, effects, event handlers and browser APIs. Keep these small.
import { useState } from "react";

export function «1:Counter»() {
    const [count, setCount] = useState(0);
    return (
        <button type="button" onClick={() => setCount((c) => c + 1)}>
            «0»Clicked {count} times
        </button>
    );
}
""", {"template": True}),
    ("nroute", "Next.js route handler (API)", r"""
// app/api/«1:items»/route.ts: REST endpoint. Export one function per HTTP method.
import { NextResponse, type NextRequest } from "next/server";
import { z } from "zod";

// Validate input at the boundary: never trust the request body
const Create«2:Item» = z.object({
    «3:name»: z.string().min(1).max(100),
});

export async function GET(request: NextRequest) {
    const page = Number(request.nextUrl.searchParams.get("page") ?? "1");
    «0»
    return NextResponse.json({ page, items: [] });
}

export async function POST(request: NextRequest) {
    const parsed = Create«2».safeParse(await request.json().catch(() => null));
    if (!parsed.success) {
        return NextResponse.json({ error: parsed.error.flatten() }, { status: 400 });
    }
    return NextResponse.json({ ok: true, data: parsed.data }, { status: 201 });
}
""", {"template": True}),
    ("naction", "Next.js server action", r"""
"use server";
// Server actions run on the server but can be called from a <form action={...}>.
// Always validate and authorize here: they are public HTTP endpoints under the hood.
import { revalidatePath } from "next/cache";
import { z } from "zod";

const Schema = z.object({ «1:title»: z.string().min(1) });

export async function «2:createPost»(formData: FormData) {
    const parsed = Schema.safeParse({ «1»: formData.get("«1»") });
    if (!parsed.success) return { error: "«3:Title is required»" };
    «0»
    revalidatePath("/«4:posts»");   // refresh cached pages that show this data
    return { ok: true };
}
"""),
    ("nloading", "Next.js loading.tsx", r"""
// loading.tsx: shown instantly while the page's server data loads (a Suspense fallback)
export default function Loading() {
    return (
        <div role="status" aria-live="polite" className="animate-pulse p-8">
            «0»Loading...
        </div>
    );
}
""", {"template": True}),
    ("nerror", "Next.js error.tsx", r"""
"use client";
// error.tsx must be a client component. It catches errors thrown while rendering this segment.
export default function Error({ error, reset }: { error: Error & { digest?: string }; reset: () => void }) {
    return (
        <div role="alert" className="p-8">
            <h2>Something went wrong.</h2>
            <button type="button" onClick={() => reset()}>Try again</button>
            «0»
        </div>
    );
}
""", {"template": True}),
    ("nmeta", "generateMetadata", r"""
// Dynamic SEO metadata per page (title, description, Open Graph)
export async function generateMetadata({ params }: { params: Promise<{ «1:slug»: string }> }) {
    const { «1» } = await params;
    const item = await «2:getBySlug»(«1»);
    return {
        title: item?.title ?? "Not found",
        description: item?.summary,
        openGraph: { images: item?.image ? [item.image] : [] },
    };
}«0»
"""),
    ("nfetch", "Server-side fetch with caching", r"""
// In server components, fetch results can be cached and revalidated on a timer
const res = await fetch("«1:https://api.example.com/items»", {
    next: { revalidate: «2:60» },   // seconds; use cache: "no-store" for always-fresh data
});
if (!res.ok) throw new Error(`Failed to load: ${res.status}`);
const «3:items» = await res.json();«0»
"""),
    ("nproxy", "Next.js proxy (middleware)", r"""
// proxy.ts at the project root (Next.js 16+; called middleware.ts in older versions).
// Runs before a request is routed: redirects, rewrites, auth gates, headers.
import { NextResponse, type NextRequest } from "next/server";

export function proxy(request: NextRequest) {
    const token = request.cookies.get("«1:session»")?.value;
    if (!token) {
        return NextResponse.redirect(new URL("/«2:login»", request.url));
    }
    «0»
    return NextResponse.next();
}

// Only run on the paths that need it
export const config = { matcher: ["/«3:dashboard»/:path*"] };
""", {"template": True}),
    ("nimg", "next/image responsive", r"""
import Image from "next/image";

{/* sizes tells the browser which width to download at each breakpoint */}
<Image
    src="«1:/hero.jpg»"
    alt="«2:Describe the image for screen readers»"
    width={«3:1200»}
    height={«4:630»}
    sizes="(min-width: 1024px) 960px, 100vw"
    priority«0»
/>
"""),
]
