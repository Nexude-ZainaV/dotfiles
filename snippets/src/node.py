"""Node.js snippets: Express server/router/middleware, built-in modules,
environment config, events, CLI scripts and the built-in test runner."""

FAMILY = dict(key="node", vscode="javascript,typescript", sublime="source.js, source.ts")

SNIPPETS = [
    ("express", "Express server", r"""
// server.js: Express app with the usual production middleware
import express from "express";
import helmet from "helmet";
import cors from "cors";

const app = express();
const PORT = Number(process.env.PORT) || «1:3000»;

app.use(helmet());                          // secure HTTP headers
app.use(cors({ origin: process.env.CORS_ORIGIN?.split(",") ?? false }));
app.use(express.json({ limit: "100kb" }));  // parse JSON bodies, cap the size

app.get("/health", (_req, res) => res.json({ status: "ok" }));
«0»

// 404 for anything not matched above
app.use((_req, res) => res.status(404).json({ error: "Not found" }));

// Error handler: 4 arguments is what marks it as one
app.use((err, _req, res, _next) => {
    console.error(err);
    res.status(err.status ?? 500).json({ error: err.expose ? err.message : "Internal error" });
});

app.listen(PORT, () => console.log(`listening on http://localhost:${PORT}`));
""", {"template": True}),
    ("router", "Express router", r"""
// routes/«1:items».js: group related endpoints, mount with app.use("/api/«1»", router)
import { Router } from "express";

const router = Router();

router.get("/", async (req, res) => {
    res.json([]);
});

router.get("/:id", async (req, res) => {
    const id = Number(req.params.id);
    if (!Number.isInteger(id)) return res.status(400).json({ error: "id must be an integer" });
    «0»
    res.status(404).json({ error: "Not found" });
});

router.post("/", async (req, res) => {
    res.status(201).json(req.body);
});

export default router;
""", {"template": True}),
    ("mw", "Express middleware", r"""
// Middleware: (req, res, next). Call next() to continue, or send a response to stop.
export function «1:requestLogger»(req, res, next) {
    const start = performance.now();
    res.on("finish", () => {
        const ms = (performance.now() - start).toFixed(1);
        console.log(`${req.method} ${req.originalUrl} ${res.statusCode} ${ms}ms`);
    });
    «0»
    next();
}
"""),
    ("errmw", "Express error handler", r"""
// Error-handling middleware is recognised by its 4 parameters; register it LAST
export function errorHandler(err, req, res, _next) {
    const status = err.status ?? 500;
    if (status >= 500) console.error(err);   // log server faults, not client mistakes
    res.status(status).json({ error: status >= 500 ? "Internal server error" : err.message });«0»
}
"""),
    ("readfile", "fs/promises read and write", r"""
import { readFile, writeFile, mkdir } from "node:fs/promises";
import path from "node:path";

// Promise-based fs: never block the event loop with the *Sync versions in a server
const «1:file» = path.join(import.meta.dirname, "«2:data.json»");
const «3:data» = JSON.parse(await readFile(«1», "utf8"));
await mkdir(path.dirname(«1»), { recursive: true });
await writeFile(«1», JSON.stringify(«3», null, 2) + "\n");«0»
"""),
    ("env", "Validated environment config", r"""
// config.js: read env vars once, validate at startup, fail fast with a clear message
import "dotenv/config";

function required(name) {
    const value = process.env[name];
    if (!value) throw new Error(`Missing required environment variable: ${name}`);
    return value;
}

export const config = {
    port: Number(process.env.PORT ?? «1:3000»),
    databaseUrl: required("«2:DATABASE_URL»"),
    nodeEnv: process.env.NODE_ENV ?? "development",
};«0»
""", {"template": True}),
    ("httpserver", "node:http server (no framework)", r"""
import { createServer } from "node:http";

// Plain Node HTTP server: what Express is built on
const server = createServer((req, res) => {
    if (req.method === "GET" && req.url === "/«1:health»") {
        res.writeHead(200, { "Content-Type": "application/json" });
        return res.end(JSON.stringify({ status: "ok" }));
    }
    «0»
    res.writeHead(404).end();
});

server.listen(«2:3000»);
"""),
    ("emitter", "EventEmitter", r"""
import { EventEmitter } from "node:events";

// Publish/subscribe inside one process
const «1:bus» = new EventEmitter();
«1».on("«2:order:created»", (payload) => {
    «0»
});
«1».emit("«2»", { id: 1 });
"""),
    ("cli", "CLI script with parseArgs", r"""
#!/usr/bin/env node
// CLI entry point using the built-in argument parser (no dependency needed)
import { parseArgs } from "node:util";

const { values, positionals } = parseArgs({
    options: {
        «1:output»: { type: "string", short: "o" },
        verbose: { type: "boolean", short: "v", default: false },
    },
    allowPositionals: true,
});

async function main() {
    «0»
}

main().catch((err) => {
    console.error(err.message);
    process.exitCode = 1;   // set, do not call process.exit(), so pending output flushes
});
""", {"template": True}),
    ("ntest", "node:test test file", r"""
// Built-in test runner: `node --test` (no Jest or Mocha required)
import { describe, it } from "node:test";
import assert from "node:assert/strict";
import { «1:add» } from "../src/«2:math».js";

describe("«1»", () => {
    it("«3:adds two numbers»", () => {
        assert.equal(«1»(2, 3), 5);
    });«0»
});
""", {"template": True}),
]
