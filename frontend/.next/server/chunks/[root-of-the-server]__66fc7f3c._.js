module.exports = {

"[project]/.next-internal/server/app/api/agents/route/actions.js [app-rsc] (server actions loader, ecmascript)": ((__turbopack_context__) => {

var { m: module, e: exports } = __turbopack_context__;
{
}}),
"[externals]/next/dist/compiled/next-server/app-route-turbo.runtime.dev.js [external] (next/dist/compiled/next-server/app-route-turbo.runtime.dev.js, cjs)": ((__turbopack_context__) => {

var { m: module, e: exports } = __turbopack_context__;
{
const mod = __turbopack_context__.x("next/dist/compiled/next-server/app-route-turbo.runtime.dev.js", () => require("next/dist/compiled/next-server/app-route-turbo.runtime.dev.js"));

module.exports = mod;
}}),
"[externals]/next/dist/compiled/next-server/app-page-turbo.runtime.dev.js [external] (next/dist/compiled/next-server/app-page-turbo.runtime.dev.js, cjs)": ((__turbopack_context__) => {

var { m: module, e: exports } = __turbopack_context__;
{
const mod = __turbopack_context__.x("next/dist/compiled/next-server/app-page-turbo.runtime.dev.js", () => require("next/dist/compiled/next-server/app-page-turbo.runtime.dev.js"));

module.exports = mod;
}}),
"[externals]/next/dist/server/app-render/work-unit-async-storage.external.js [external] (next/dist/server/app-render/work-unit-async-storage.external.js, cjs)": ((__turbopack_context__) => {

var { m: module, e: exports } = __turbopack_context__;
{
const mod = __turbopack_context__.x("next/dist/server/app-render/work-unit-async-storage.external.js", () => require("next/dist/server/app-render/work-unit-async-storage.external.js"));

module.exports = mod;
}}),
"[externals]/next/dist/server/app-render/work-async-storage.external.js [external] (next/dist/server/app-render/work-async-storage.external.js, cjs)": ((__turbopack_context__) => {

var { m: module, e: exports } = __turbopack_context__;
{
const mod = __turbopack_context__.x("next/dist/server/app-render/work-async-storage.external.js", () => require("next/dist/server/app-render/work-async-storage.external.js"));

module.exports = mod;
}}),
"[externals]/next/dist/shared/lib/no-fallback-error.external.js [external] (next/dist/shared/lib/no-fallback-error.external.js, cjs)": ((__turbopack_context__) => {

var { m: module, e: exports } = __turbopack_context__;
{
const mod = __turbopack_context__.x("next/dist/shared/lib/no-fallback-error.external.js", () => require("next/dist/shared/lib/no-fallback-error.external.js"));

module.exports = mod;
}}),
"[project]/src/app/api/agents/route.ts [app-route] (ecmascript)": ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s({
    "GET": ()=>GET
});
async function GET() {
    try {
        const isLocal = ("TURBOPACK compile-time value", "local") === 'local';
        const apiUrl = ("TURBOPACK compile-time truthy", 1) ? process.env.VALUE_CANVAS_API_URL_LOCAL : "TURBOPACK unreachable";
        // Add timeout with AbortController
        const controller = new AbortController();
        const timeoutId = setTimeout(()=>controller.abort(), 5000); // 5 second timeout
        const response = await fetch(`${apiUrl}/info`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                ...process.env.VALUE_CANVAS_API_TOKEN && {
                    'Authorization': `Bearer ${process.env.VALUE_CANVAS_API_TOKEN}`
                }
            },
            signal: controller.signal
        });
        clearTimeout(timeoutId);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        // Filter to only return founder-buddy agent
        if (data.agents && Array.isArray(data.agents)) {
            data.agents = data.agents.filter((agent)=>agent.key === 'founder-buddy');
        }
        return Response.json(data);
    } catch (error) {
        console.error('Failed to fetch agents:', error);
        // Fallback - only founder-buddy agent
        const fallbackAgents = {
            agents: [
                {
                    key: 'founder-buddy',
                    description: 'A Founder Buddy agent that helps entrepreneurs validate and refine their startup ideas through structured conversations about mission, idea, team traction, and investment plan'
                }
            ]
        };
        return Response.json(fallbackAgents);
    }
}
}),

};

//# sourceMappingURL=%5Broot-of-the-server%5D__66fc7f3c._.js.map