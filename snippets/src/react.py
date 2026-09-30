"""React (19) snippets for .jsx/.tsx: components, hooks, forms, responsive hook, tests."""

FAMILY = dict(
    key="react",
    vscode="javascriptreact,typescriptreact",
    sublime="source.jsx, source.tsx, source.js, source.ts",
)

SNIPPETS = [
    ("rfc", "React component (TSX)", r"""
// «1:Card».tsx: one component per file, named after the file (PascalCase)
type «1»Props = {
    «2:title»: string;
    children?: React.ReactNode;
};

export function «1»({ «2», children }: «1»Props) {
    return (
        <section className="«3:card»">
            <h2>{«2»}</h2>
            {children}
            «0»
        </section>
    );
}
""", {"template": True}),
    ("rfcs", "Component with state + effect", r"""
import { useEffect, useState } from "react";

// State holds what the UI shows; effects sync with things outside React (APIs, timers)
export function «1:UserList»() {
    const [«2:items», set«3:Items»] = useState<«4:string»[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const controller = new AbortController();   // cancel the request on unmount
        fetch("«5:/api/users»", { signal: controller.signal })
            .then((res) => {
                if (!res.ok) throw new Error(`HTTP ${res.status}`);
                return res.json();
            })
            .then(set«3»)
            .catch((err) => {
                if (err.name !== "AbortError") setError(err.message);
            })
            .finally(() => setLoading(false));
        return () => controller.abort();
    }, []);   // [] = run once after the first render

    if (loading) return <p>Loading...</p>;
    if (error) return <p role="alert">Error: {error}</p>;
    return (
        <ul>
            {«2».map((item) => (
                <li key={item}>{item}</li>   // key must be stable and unique
            ))}
            «0»
        </ul>
    );
}
""", {"template": True}),
    ("us", "useState", r"""
// useState: [value, setter]. Use the updater form when the new value depends on the old.
const [«1:count», set«2:Count»] = useState<«3:number»>(«4:0»);
// set«2»((prev) => prev + 1);«0»
"""),
    ("ue", "useEffect with cleanup", r"""
// useEffect: runs after render. Return a cleanup to undo subscriptions, timers, listeners.
useEffect(() => {
    «1»
    return () => {
        «2»
    };
}, [«3:dependency»]);   // re-runs when a dependency changes«0»
"""),
    ("uref", "useRef", r"""
// useRef: a mutable box that survives renders without causing one (DOM nodes, timer ids)
const «1:inputRef» = useRef<«2:HTMLInputElement»>(null);
// <input ref={«1»} />  then  «1».current?.focus();«0»
"""),
    ("umemo", "useMemo / useCallback", r"""
// useMemo caches a computed VALUE, useCallback caches a FUNCTION, both between renders.
// Only reach for them when profiling shows a cost, or a child relies on stable props.
const «1:sorted» = useMemo(() => [...«2:items»].sort(), [«2»]);
const «3:handleClick» = useCallback(() => {
    «0»
}, []);
"""),
    ("ured", "useReducer", r"""
// useReducer: when several state values change together, or next state follows rules
type State = { «1:count»: number };
type Action = { type: "increment" } | { type: "decrement" } | { type: "reset" };

function reducer(state: State, action: Action): State {
    switch (action.type) {
        case "increment":
            return { «1»: state.«1» + 1 };
        case "decrement":
            return { «1»: state.«1» - 1 };
        case "reset":
            return { «1»: 0 };
    }
}

const [state, dispatch] = useReducer(reducer, { «1»: 0 });«0»
"""),
    ("uctx", "Context + provider + hook", r"""
import { createContext, useContext, useState } from "react";

// Context: share a value with a whole subtree without passing props at every level
type «1:Theme»ContextValue = { «2:theme»: string; set«3:Theme»: (t: string) => void };

const «1»Context = createContext<«1»ContextValue | null>(null);

export function «1»Provider({ children }: { children: React.ReactNode }) {
    const [«2», set«3»] = useState("«4:light»");
    return <«1»Context.Provider value={{ «2», set«3» }}>{children}</«1»Context.Provider>;
}

// Custom hook: throws a clear error if used outside the provider
export function use«1»() {
    const ctx = useContext(«1»Context);
    if (!ctx) throw new Error("use«1» must be used inside <«1»Provider>");
    return ctx;
}«0»
""", {"template": True}),
    ("hookfetch", "Custom hook: useFetch", r"""
import { useEffect, useState } from "react";

// A custom hook is a function starting with `use` that reuses stateful logic
export function useFetch<T>(url: string) {
    const [data, setData] = useState<T | null>(null);
    const [error, setError] = useState<string | null>(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const controller = new AbortController();
        setLoading(true);
        fetch(url, { signal: controller.signal })
            .then((res) => {
                if (!res.ok) throw new Error(`HTTP ${res.status}`);
                return res.json() as Promise<T>;
            })
            .then(setData)
            .catch((err) => err.name !== "AbortError" && setError(err.message))
            .finally(() => setLoading(false));
        return () => controller.abort();   // a new url cancels the old request
    }, [url]);

    return { data, error, loading };
}«0»
""", {"template": True}),
    ("umq", "Responsive: useMediaQuery hook", r"""
import { useSyncExternalStore } from "react";

// Subscribes to a CSS media query. Breakpoints match Tailwind: sm 640, md 768, lg 1024, xl 1280.
export function useMediaQuery(query: string): boolean {
    return useSyncExternalStore(
        (onChange) => {
            const mql = window.matchMedia(query);
            mql.addEventListener("change", onChange);
            return () => mql.removeEventListener("change", onChange);
        },
        () => window.matchMedia(query).matches,
        () => false,   // server render: assume mobile-first (no match)
    );
}

// const isDesktop = useMediaQuery("(min-width: «1:1024»px)");«0»
"""),
    ("cond", "Conditional rendering", r"""
{/* && renders the right side only when the left is truthy. Careful: {0 && x} renders "0". */}
{«1:isLoggedIn» && <«2:Dashboard» />}
{/* ternary for either/or */}
{«3:loading» ? <p>Loading...</p> : <«4:Content» />}«0»
"""),
    ("listmap", "Render a list", r"""
{/* Every list item needs a stable, unique key (an id, never the array index if items reorder) */}
<ul>
    {«1:items».map((«2:item») => (
        <li key={«2».«3:id»}>{«2».«4:name»}</li>
    ))}
</ul>«0»
"""),
    ("form", "Controlled form", r"""
// Controlled inputs: React state is the single source of truth for each field
const [values, setValues] = useState({ «1:email»: "", «2:password»: "" });

function handleChange(e: React.ChangeEvent<HTMLInputElement>) {
    setValues((v) => ({ ...v, [e.target.name]: e.target.value }));
}

function handleSubmit(e: React.FormEvent) {
    e.preventDefault();   // stop the full-page reload
    «0»
}

// <form onSubmit={handleSubmit}>
//     <label htmlFor="«1»">Email</label>
//     <input id="«1»" name="«1»" type="email" value={values.«1»} onChange={handleChange} required />
// </form>
"""),
    ("rtest", "React Testing Library test", r"""
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, expect, it } from "vitest";
import { «1:Counter» } from "./«1»";

// Test what the user sees and does, not implementation details
describe("«1»", () => {
    it("«2:increments when clicked»", async () => {
        render(<«1» />);
        await userEvent.click(screen.getByRole("button", { name: /«3:increment»/i }));
        expect(screen.getByText(«4:"1"»)).toBeInTheDocument();
    });«0»
});
""", {"template": True}),
]
