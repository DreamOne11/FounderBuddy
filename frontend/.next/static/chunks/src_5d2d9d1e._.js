(globalThis.TURBOPACK = globalThis.TURBOPACK || []).push([typeof document === "object" ? document.currentScript : undefined, {

"[project]/src/components/ConfigPanel.tsx [app-client] (ecmascript)": ((__turbopack_context__) => {
"use strict";

var { k: __turbopack_refresh__, m: module } = __turbopack_context__;
{
__turbopack_context__.s({
    "default": ()=>ConfigPanel
});
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/next/dist/compiled/react/jsx-dev-runtime.js [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/next/dist/compiled/react/index.js [app-client] (ecmascript)");
;
var _s = __turbopack_context__.k.signature();
'use client';
;
function ConfigPanel(param) {
    let { selectedAgent, userId, mode, threadId, onAgentChange, onUserIdChange, onModeChange, onClose } = param;
    var _agents_find;
    _s();
    const [agents, setAgents] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useState"])([]);
    const [userIdInput, setUserIdInput] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useState"])(userId.toString());
    const [loading, setLoading] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useState"])(true);
    (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useEffect"])({
        "ConfigPanel.useEffect": ()=>{
            fetchAgents();
        }
    }["ConfigPanel.useEffect"], []); // eslint-disable-line react-hooks/exhaustive-deps
    (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useEffect"])({
        "ConfigPanel.useEffect": ()=>{
            setUserIdInput(userId.toString());
        }
    }["ConfigPanel.useEffect"], [
        userId
    ]);
    const fetchAgents = async ()=>{
        try {
            const response = await fetch('/api/agents');
            const data = await response.json();
            const transformedAgents = (data.agents || []).map((agent)=>({
                    id: agent.key,
                    name: getAgentName(agent.key),
                    description: agent.description
                }));
            // Filter to only show founder-buddy agent
            const filteredAgents = transformedAgents.filter((agent)=>agent.id === 'founder-buddy');
            setAgents(filteredAgents);
            // Auto-select founder-buddy if not already selected
            if (filteredAgents.length > 0 && !selectedAgent) {
                onAgentChange('founder-buddy');
            }
        } catch (error) {
            console.error('Failed to fetch agents:', error);
            // Fallback - only founder-buddy
            setAgents([
                {
                    id: 'founder-buddy',
                    name: 'Founder Buddy',
                    description: 'Validate and refine your startup idea'
                }
            ]);
            // Auto-select founder-buddy if not already selected
            if (!selectedAgent) {
                onAgentChange('founder-buddy');
            }
        } finally{
            setLoading(false);
        }
    };
    const getAgentName = (key)=>{
        const names = {
            'founder-buddy': 'Founder Buddy'
        };
        return names[key] || key;
    };
    const handleUserIdSubmit = ()=>{
        const numericUserId = parseInt(userIdInput, 10);
        if (isNaN(numericUserId) || numericUserId <= 0) {
            alert('Please enter a valid positive integer');
            return;
        }
        onUserIdChange(numericUserId);
    };
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
        style: {
            width: onClose ? '400px' : '320px',
            maxHeight: onClose ? '90vh' : '100vh',
            backgroundColor: 'white',
            borderRight: onClose ? 'none' : '1px solid #e2e8f0',
            borderRadius: onClose ? '12px' : '0',
            boxShadow: onClose ? '0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)' : 'none',
            display: 'flex',
            flexDirection: 'column',
            overflow: 'hidden',
            position: 'relative'
        },
        children: [
            onClose && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                onClick: onClose,
                style: {
                    position: 'absolute',
                    top: '16px',
                    right: '16px',
                    width: '32px',
                    height: '32px',
                    borderRadius: '50%',
                    backgroundColor: '#f1f5f9',
                    border: 'none',
                    color: '#64748b',
                    fontSize: '18px',
                    cursor: 'pointer',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    zIndex: 10,
                    transition: 'all 0.2s ease'
                },
                onMouseEnter: (e)=>{
                    e.currentTarget.style.backgroundColor = '#e2e8f0';
                    e.currentTarget.style.color = '#1e293b';
                },
                onMouseLeave: (e)=>{
                    e.currentTarget.style.backgroundColor = '#f1f5f9';
                    e.currentTarget.style.color = '#64748b';
                },
                title: "Close",
                children: "✕"
            }, void 0, false, {
                fileName: "[project]/src/components/ConfigPanel.tsx",
                lineNumber: 111,
                columnNumber: 9
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                style: {
                    padding: '20px',
                    flex: '0 0 auto',
                    borderBottom: '1px solid #e2e8f0'
                },
                children: [
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                        children: [
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("h2", {
                                style: {
                                    fontSize: '18px',
                                    fontWeight: 'bold',
                                    color: '#1e293b',
                                    marginBottom: '8px'
                                },
                                children: "Configuration"
                            }, void 0, false, {
                                fileName: "[project]/src/components/ConfigPanel.tsx",
                                lineNumber: 152,
                                columnNumber: 9
                            }, this),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                                style: {
                                    fontSize: '12px',
                                    color: '#64748b'
                                },
                                children: "Configure your chat settings"
                            }, void 0, false, {
                                fileName: "[project]/src/components/ConfigPanel.tsx",
                                lineNumber: 160,
                                columnNumber: 9
                            }, this)
                        ]
                    }, void 0, true, {
                        fileName: "[project]/src/components/ConfigPanel.tsx",
                        lineNumber: 151,
                        columnNumber: 9
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                        children: [
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("label", {
                                style: {
                                    fontSize: '14px',
                                    fontWeight: '500',
                                    color: '#374151',
                                    marginBottom: '8px',
                                    display: 'block'
                                },
                                children: "Agent"
                            }, void 0, false, {
                                fileName: "[project]/src/components/ConfigPanel.tsx",
                                lineNumber: 170,
                                columnNumber: 9
                            }, this),
                            loading ? /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                style: {
                                    color: '#64748b',
                                    fontSize: '12px'
                                },
                                children: "Loading agents..."
                            }, void 0, false, {
                                fileName: "[project]/src/components/ConfigPanel.tsx",
                                lineNumber: 180,
                                columnNumber: 11
                            }, this) : agents.length === 1 ? // If only one agent, show it as read-only
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                style: {
                                    width: '100%',
                                    padding: '8px 12px',
                                    border: '1px solid #d1d5db',
                                    borderRadius: '6px',
                                    fontSize: '14px',
                                    backgroundColor: '#f8fafc',
                                    color: '#64748b'
                                },
                                children: agents[0].name
                            }, void 0, false, {
                                fileName: "[project]/src/components/ConfigPanel.tsx",
                                lineNumber: 183,
                                columnNumber: 11
                            }, this) : /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("select", {
                                value: selectedAgent,
                                onChange: (e)=>onAgentChange(e.target.value),
                                style: {
                                    width: '100%',
                                    padding: '8px 12px',
                                    border: '1px solid #d1d5db',
                                    borderRadius: '6px',
                                    fontSize: '14px',
                                    backgroundColor: 'white'
                                },
                                children: [
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("option", {
                                        value: "",
                                        children: "Select an agent"
                                    }, void 0, false, {
                                        fileName: "[project]/src/components/ConfigPanel.tsx",
                                        lineNumber: 207,
                                        columnNumber: 13
                                    }, this),
                                    agents.map((agent)=>/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("option", {
                                            value: agent.id,
                                            children: agent.name
                                        }, agent.id, false, {
                                            fileName: "[project]/src/components/ConfigPanel.tsx",
                                            lineNumber: 209,
                                            columnNumber: 15
                                        }, this))
                                ]
                            }, void 0, true, {
                                fileName: "[project]/src/components/ConfigPanel.tsx",
                                lineNumber: 195,
                                columnNumber: 11
                            }, this),
                            selectedAgent && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                style: {
                                    marginTop: '8px',
                                    padding: '8px',
                                    backgroundColor: '#f8fafc',
                                    borderRadius: '4px',
                                    fontSize: '12px',
                                    color: '#475569'
                                },
                                children: (_agents_find = agents.find((a)=>a.id === selectedAgent)) === null || _agents_find === void 0 ? void 0 : _agents_find.description
                            }, void 0, false, {
                                fileName: "[project]/src/components/ConfigPanel.tsx",
                                lineNumber: 216,
                                columnNumber: 11
                            }, this)
                        ]
                    }, void 0, true, {
                        fileName: "[project]/src/components/ConfigPanel.tsx",
                        lineNumber: 169,
                        columnNumber: 7
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                        children: [
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("label", {
                                style: {
                                    fontSize: '14px',
                                    fontWeight: '500',
                                    color: '#374151',
                                    marginBottom: '8px',
                                    display: 'block'
                                },
                                children: "User ID"
                            }, void 0, false, {
                                fileName: "[project]/src/components/ConfigPanel.tsx",
                                lineNumber: 231,
                                columnNumber: 9
                            }, this),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                style: {
                                    display: 'flex',
                                    gap: '8px'
                                },
                                children: [
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("input", {
                                        type: "number",
                                        value: userIdInput,
                                        onChange: (e)=>setUserIdInput(e.target.value),
                                        placeholder: "Enter user ID",
                                        min: "1",
                                        step: "1",
                                        style: {
                                            flex: 1,
                                            padding: '8px 12px',
                                            border: '1px solid #d1d5db',
                                            borderRadius: '6px',
                                            fontSize: '14px'
                                        }
                                    }, void 0, false, {
                                        fileName: "[project]/src/components/ConfigPanel.tsx",
                                        lineNumber: 241,
                                        columnNumber: 11
                                    }, this),
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                                        onClick: handleUserIdSubmit,
                                        disabled: userIdInput === userId.toString(),
                                        style: {
                                            padding: '8px 12px',
                                            backgroundColor: userIdInput === userId.toString() ? '#9ca3af' : '#3b82f6',
                                            color: 'white',
                                            border: 'none',
                                            borderRadius: '6px',
                                            fontSize: '12px',
                                            cursor: userIdInput === userId.toString() ? 'not-allowed' : 'pointer'
                                        },
                                        children: "Set"
                                    }, void 0, false, {
                                        fileName: "[project]/src/components/ConfigPanel.tsx",
                                        lineNumber: 256,
                                        columnNumber: 11
                                    }, this)
                                ]
                            }, void 0, true, {
                                fileName: "[project]/src/components/ConfigPanel.tsx",
                                lineNumber: 240,
                                columnNumber: 9
                            }, this)
                        ]
                    }, void 0, true, {
                        fileName: "[project]/src/components/ConfigPanel.tsx",
                        lineNumber: 230,
                        columnNumber: 7
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                        children: [
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("label", {
                                style: {
                                    fontSize: '14px',
                                    fontWeight: '500',
                                    color: '#374151',
                                    marginBottom: '8px',
                                    display: 'block'
                                },
                                children: "Response Mode"
                            }, void 0, false, {
                                fileName: "[project]/src/components/ConfigPanel.tsx",
                                lineNumber: 276,
                                columnNumber: 9
                            }, this),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                style: {
                                    display: 'flex',
                                    gap: '8px'
                                },
                                children: [
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                                        onClick: ()=>onModeChange('invoke'),
                                        style: {
                                            flex: 1,
                                            padding: '8px 12px',
                                            backgroundColor: mode === 'invoke' ? '#3b82f6' : '#f1f5f9',
                                            color: mode === 'invoke' ? 'white' : '#64748b',
                                            border: '1px solid #e2e8f0',
                                            borderRadius: '6px',
                                            fontSize: '12px',
                                            cursor: 'pointer'
                                        },
                                        children: "Invoke"
                                    }, void 0, false, {
                                        fileName: "[project]/src/components/ConfigPanel.tsx",
                                        lineNumber: 286,
                                        columnNumber: 11
                                    }, this),
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                                        onClick: ()=>onModeChange('stream'),
                                        style: {
                                            flex: 1,
                                            padding: '8px 12px',
                                            backgroundColor: mode === 'stream' ? '#3b82f6' : '#f1f5f9',
                                            color: mode === 'stream' ? 'white' : '#64748b',
                                            border: '1px solid #e2e8f0',
                                            borderRadius: '6px',
                                            fontSize: '12px',
                                            cursor: 'pointer'
                                        },
                                        children: "Stream"
                                    }, void 0, false, {
                                        fileName: "[project]/src/components/ConfigPanel.tsx",
                                        lineNumber: 301,
                                        columnNumber: 11
                                    }, this)
                                ]
                            }, void 0, true, {
                                fileName: "[project]/src/components/ConfigPanel.tsx",
                                lineNumber: 285,
                                columnNumber: 9
                            }, this),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                style: {
                                    marginTop: '8px',
                                    fontSize: '11px',
                                    color: '#64748b'
                                },
                                children: mode === 'invoke' ? 'Get complete response at once' : 'Get real-time streaming response'
                            }, void 0, false, {
                                fileName: "[project]/src/components/ConfigPanel.tsx",
                                lineNumber: 317,
                                columnNumber: 9
                            }, this)
                        ]
                    }, void 0, true, {
                        fileName: "[project]/src/components/ConfigPanel.tsx",
                        lineNumber: 275,
                        columnNumber: 7
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                        style: {
                            padding: '12px',
                            backgroundColor: '#f0f9ff',
                            borderRadius: '8px',
                            border: '1px solid #0ea5e9',
                            marginTop: '16px'
                        },
                        children: [
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                style: {
                                    fontSize: '12px',
                                    fontWeight: '500',
                                    color: '#0369a1',
                                    marginBottom: '8px'
                                },
                                children: "Current Settings"
                            }, void 0, false, {
                                fileName: "[project]/src/components/ConfigPanel.tsx",
                                lineNumber: 334,
                                columnNumber: 11
                            }, this),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                style: {
                                    fontSize: '11px',
                                    color: '#0369a1',
                                    lineHeight: '1.4'
                                },
                                children: [
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                        children: [
                                            "Agent: ",
                                            selectedAgent ? getAgentName(selectedAgent) : 'None'
                                        ]
                                    }, void 0, true, {
                                        fileName: "[project]/src/components/ConfigPanel.tsx",
                                        lineNumber: 338,
                                        columnNumber: 13
                                    }, this),
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                        children: [
                                            "User ID: ",
                                            userId
                                        ]
                                    }, void 0, true, {
                                        fileName: "[project]/src/components/ConfigPanel.tsx",
                                        lineNumber: 339,
                                        columnNumber: 13
                                    }, this),
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                        children: [
                                            "Mode: ",
                                            mode === 'invoke' ? 'Invoke' : 'Stream'
                                        ]
                                    }, void 0, true, {
                                        fileName: "[project]/src/components/ConfigPanel.tsx",
                                        lineNumber: 340,
                                        columnNumber: 13
                                    }, this)
                                ]
                            }, void 0, true, {
                                fileName: "[project]/src/components/ConfigPanel.tsx",
                                lineNumber: 337,
                                columnNumber: 11
                            }, this)
                        ]
                    }, void 0, true, {
                        fileName: "[project]/src/components/ConfigPanel.tsx",
                        lineNumber: 327,
                        columnNumber: 9
                    }, this)
                ]
            }, void 0, true, {
                fileName: "[project]/src/components/ConfigPanel.tsx",
                lineNumber: 146,
                columnNumber: 7
            }, this)
        ]
    }, void 0, true, {
        fileName: "[project]/src/components/ConfigPanel.tsx",
        lineNumber: 97,
        columnNumber: 5
    }, this);
}
_s(ConfigPanel, "yW/b1rP9vXumTgTwvhzBm6KOZKw=");
_c = ConfigPanel;
var _c;
__turbopack_context__.k.register(_c, "ConfigPanel");
if (typeof globalThis.$RefreshHelpers$ === 'object' && globalThis.$RefreshHelpers !== null) {
    __turbopack_context__.k.registerExports(module, globalThis.$RefreshHelpers$);
}
}}),
"[project]/src/utils/conversationStorage.ts [app-client] (ecmascript)": ((__turbopack_context__) => {
"use strict";

var { k: __turbopack_refresh__, m: module } = __turbopack_context__;
{
__turbopack_context__.s({
    "conversationStorage": ()=>conversationStorage
});
const STORAGE_KEY = 'dent_conversations';
const MAX_CONVERSATIONS = 50;
const conversationStorage = {
    getAll () {
        try {
            const data = localStorage.getItem(STORAGE_KEY);
            return data ? JSON.parse(data) : [];
        } catch (error) {
            console.error('Error loading conversations:', error);
            return [];
        }
    },
    save (conversation) {
        try {
            const conversations = this.getAll();
            const existingIndex = conversations.findIndex((c)=>c.threadId === conversation.threadId);
            if (existingIndex >= 0) {
                conversations[existingIndex] = {
                    ...conversations[existingIndex],
                    ...conversation,
                    lastUpdatedAt: new Date().toISOString()
                };
            } else {
                conversations.unshift(conversation);
                if (conversations.length > MAX_CONVERSATIONS) {
                    conversations.pop();
                }
            }
            // Remove sorting to maintain creation order
            // Only sort when initially loading from storage
            localStorage.setItem(STORAGE_KEY, JSON.stringify(conversations));
        } catch (error) {
            console.error('Error saving conversation:', error);
        }
    },
    get (threadId) {
        try {
            const conversations = this.getAll();
            return conversations.find((c)=>c.threadId === threadId) || null;
        } catch (error) {
            console.error('Error getting conversation:', error);
            return null;
        }
    },
    delete (threadId) {
        try {
            const conversations = this.getAll();
            const filtered = conversations.filter((c)=>c.threadId !== threadId);
            localStorage.setItem(STORAGE_KEY, JSON.stringify(filtered));
        } catch (error) {
            console.error('Error deleting conversation:', error);
        }
    },
    clear () {
        try {
            localStorage.removeItem(STORAGE_KEY);
        } catch (error) {
            console.error('Error clearing conversations:', error);
        }
    },
    generateTitle (messages) {
        const firstUserMessage = messages.find((m)=>m.role === 'user');
        if (!firstUserMessage) return 'New Conversation';
        const content = firstUserMessage.content;
        const maxLength = 50;
        if (content.length <= maxLength) return content;
        return content.substring(0, maxLength) + '...';
    },
    formatDate (dateString) {
        const date = new Date(dateString);
        const now = new Date();
        const diffMs = now.getTime() - date.getTime();
        const diffMins = Math.floor(diffMs / 60000);
        const diffHours = Math.floor(diffMs / 3600000);
        const diffDays = Math.floor(diffMs / 86400000);
        if (diffMins < 1) return 'Just now';
        if (diffMins < 60) return "".concat(diffMins, " ").concat(diffMins === 1 ? 'minute' : 'minutes', " ago");
        if (diffHours < 24) return "".concat(diffHours, " ").concat(diffHours === 1 ? 'hour' : 'hours', " ago");
        if (diffDays < 7) return "".concat(diffDays, " ").concat(diffDays === 1 ? 'day' : 'days', " ago");
        return date.toLocaleDateString('en-US', {
            month: 'short',
            day: 'numeric',
            year: date.getFullYear() !== now.getFullYear() ? 'numeric' : undefined
        });
    }
};
if (typeof globalThis.$RefreshHelpers$ === 'object' && globalThis.$RefreshHelpers !== null) {
    __turbopack_context__.k.registerExports(module, globalThis.$RefreshHelpers$);
}
}}),
"[project]/src/components/ChatArea.tsx [app-client] (ecmascript)": ((__turbopack_context__) => {
"use strict";

var { k: __turbopack_refresh__, m: module } = __turbopack_context__;
{
__turbopack_context__.s({
    "default": ()=>ChatArea
});
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/next/dist/compiled/react/jsx-dev-runtime.js [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$styled$2d$jsx$2f$style$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/styled-jsx/style.js [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/next/dist/compiled/react/index.js [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$react$2d$markdown$2f$lib$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__$3c$export__Markdown__as__default$3e$__ = __turbopack_context__.i("[project]/node_modules/react-markdown/lib/index.js [app-client] (ecmascript) <export Markdown as default>");
var __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$utils$2f$conversationStorage$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/src/utils/conversationStorage.ts [app-client] (ecmascript)");
;
var _s = __turbopack_context__.k.signature();
'use client';
;
;
;
;
function ChatArea(param) {
    let { selectedAgent, userId, mode, threadId, loadedMessages, currentSection, onThreadIdChange, onSectionUpdate, progressSidebar } = param;
    _s();
    const [messages, setMessages] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useState"])([]);
    const [input, setInput] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useState"])('');
    const [isLoading, setIsLoading] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useState"])(false);
    const [streamingContent, setStreamingContent] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useState"])('');
    const [copiedMessageId, setCopiedMessageId] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useState"])(null);
    const [copiedAll, setCopiedAll] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useState"])(false);
    const [isGeneratingLLM, setIsGeneratingLLM] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useState"])(false);
    const [isAutoMode, setIsAutoMode] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useState"])(false);
    const messagesEndRef = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useRef"])(null);
    const inputRef = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useRef"])(null);
    const autoModeRef = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useRef"])(false);
    (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useEffect"])({
        "ChatArea.useEffect": ()=>{
            var _messagesEndRef_current;
            (_messagesEndRef_current = messagesEndRef.current) === null || _messagesEndRef_current === void 0 ? void 0 : _messagesEndRef_current.scrollIntoView({
                behavior: 'smooth'
            });
        }
    }["ChatArea.useEffect"], [
        messages,
        isLoading
    ]);
    (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useEffect"])({
        "ChatArea.useEffect": ()=>{
            if (!isLoading) {
                var _inputRef_current;
                (_inputRef_current = inputRef.current) === null || _inputRef_current === void 0 ? void 0 : _inputRef_current.focus();
            }
        }
    }["ChatArea.useEffect"], [
        isLoading
    ]);
    // Add keyboard shortcut for auto-reply (Ctrl+G or Cmd+G)
    (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useEffect"])({
        "ChatArea.useEffect": ()=>{
            const handleKeyDown = {
                "ChatArea.useEffect.handleKeyDown": (e)=>{
                    if ((e.ctrlKey || e.metaKey) && e.key === 'g') {
                        e.preventDefault();
                        handleAutoReply();
                    }
                }
            }["ChatArea.useEffect.handleKeyDown"];
            window.addEventListener('keydown', handleKeyDown);
            return ({
                "ChatArea.useEffect": ()=>window.removeEventListener('keydown', handleKeyDown)
            })["ChatArea.useEffect"];
        // eslint-disable-next-line react-hooks/exhaustive-deps
        }
    }["ChatArea.useEffect"], [
        messages,
        selectedAgent,
        userId,
        isLoading,
        isGeneratingLLM,
        currentSection
    ]);
    // Reset messages when threadId is null (reset button clicked)
    (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useEffect"])({
        "ChatArea.useEffect": ()=>{
            if (threadId === null) {
                setMessages([]);
                setInput('');
                setStreamingContent('');
                setIsLoading(false);
                setIsAutoMode(false);
                autoModeRef.current = false;
            }
        }
    }["ChatArea.useEffect"], [
        threadId
    ]);
    // Load messages when conversation is selected
    (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useEffect"])({
        "ChatArea.useEffect": ()=>{
            if (loadedMessages && loadedMessages.length > 0) {
                setMessages(loadedMessages);
            }
        }
    }["ChatArea.useEffect"], [
        loadedMessages,
        threadId
    ]);
    // Save conversation to localStorage when messages or threadId changes
    (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useEffect"])({
        "ChatArea.useEffect": ()=>{
            if (threadId && messages.length > 0) {
                const conversation = {
                    threadId,
                    agentType: selectedAgent,
                    userId,
                    createdAt: new Date().toISOString(),
                    lastUpdatedAt: new Date().toISOString(),
                    messages,
                    title: __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$utils$2f$conversationStorage$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["conversationStorage"].generateTitle(messages),
                    currentSection: currentSection || undefined
                };
                __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$utils$2f$conversationStorage$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["conversationStorage"].save(conversation);
            }
        }
    }["ChatArea.useEffect"], [
        messages,
        threadId,
        selectedAgent,
        userId,
        currentSection
    ]);
    // Sync autoModeRef with isAutoMode state
    (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useEffect"])({
        "ChatArea.useEffect": ()=>{
            autoModeRef.current = isAutoMode;
        }
    }["ChatArea.useEffect"], [
        isAutoMode
    ]);
    // Auto conversation trigger
    (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useEffect"])({
        "ChatArea.useEffect": ()=>{
            if (isAutoMode && !isLoading && !isGeneratingLLM && messages.length > 0) {
                const lastMessage = messages[messages.length - 1];
                // Only trigger if the last message is from assistant and has content
                if (lastMessage.role === 'assistant' && lastMessage.content && lastMessage.content.trim() !== '') {
                    // Small delay to ensure stream is fully closed
                    const timer = setTimeout({
                        "ChatArea.useEffect.timer": ()=>{
                            if (autoModeRef.current && !isLoading && !isGeneratingLLM) {
                                handleAutoReply(true);
                            }
                        }
                    }["ChatArea.useEffect.timer"], 100);
                    return ({
                        "ChatArea.useEffect": ()=>clearTimeout(timer)
                    })["ChatArea.useEffect"];
                }
            }
        // eslint-disable-next-line react-hooks/exhaustive-deps
        }
    }["ChatArea.useEffect"], [
        messages,
        isAutoMode,
        isLoading,
        isGeneratingLLM
    ]);
    const getAgentName = (agentId)=>{
        const names = {
            'value-canvas': 'Value Canvas Agent',
            'social-pitch': 'Social Pitch Agent',
            'mission-pitch': 'Mission Pitch Agent',
            'special-report': 'Special Report Agent',
            'founder-buddy': 'Founder Buddy'
        };
        return names[agentId] || 'AI Agent';
    };
    const getPlaceholderText = (agentId)=>{
        const placeholders = {
            'value-canvas': 'Try: "I want to create my value canvas"',
            'social-pitch': 'Try: "I want to create my social pitch"',
            'mission-pitch': 'Try: "I want to discover my mission pitch"',
            'special-report': 'Try: "Help me create a business report"',
            'founder-buddy': 'Try: "I want to validate my startup idea"'
        };
        return placeholders[agentId] || 'Type your message...';
    };
    // Extract send message logic
    const handleSendMessage = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useCallback"])({
        "ChatArea.useCallback[handleSendMessage]": async (messageContent)=>{
            if (!messageContent.trim() || isLoading || !selectedAgent || !userId) return;
            const userMessage = {
                id: Date.now().toString() + '-user',
                role: 'user',
                content: messageContent.trim()
            };
            setMessages({
                "ChatArea.useCallback[handleSendMessage]": (prev)=>[
                        ...prev,
                        userMessage
                    ]
            }["ChatArea.useCallback[handleSendMessage]"]);
            setInput('');
            setIsLoading(true);
            try {
                var _response_body;
                const requestPayload = {
                    messages: [
                        {
                            role: 'user',
                            content: userMessage.content
                        }
                    ],
                    userId: userId,
                    threadId: threadId,
                    mode: mode,
                    agentId: selectedAgent
                };
                const response = await fetch('/api/chat', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(requestPayload)
                });
                if (!response.ok) {
                    throw new Error("HTTP error! status: ".concat(response.status));
                }
                // Handle invoke mode
                if (mode === 'invoke') {
                    const invokeData = await response.json();
                    const assistantMessage = {
                        id: Date.now().toString() + '-assistant',
                        role: 'assistant',
                        content: invokeData.content
                    };
                    setMessages({
                        "ChatArea.useCallback[handleSendMessage]": (prev)=>[
                                ...prev,
                                assistantMessage
                            ]
                    }["ChatArea.useCallback[handleSendMessage]"]);
                    if (invokeData.threadId && !threadId) {
                        onThreadIdChange(invokeData.threadId);
                    }
                    if (invokeData.section) {
                        onSectionUpdate(invokeData.section);
                    }
                    setIsLoading(false);
                    return;
                }
                // Handle streaming mode
                const reader = (_response_body = response.body) === null || _response_body === void 0 ? void 0 : _response_body.getReader();
                const decoder = new TextDecoder();
                if (!reader) {
                    throw new Error('No response body reader available');
                }
                const tempAssistantMessage = {
                    id: Date.now().toString() + '-assistant',
                    role: 'assistant',
                    content: ''
                };
                setMessages({
                    "ChatArea.useCallback[handleSendMessage]": (prev)=>[
                            ...prev,
                            tempAssistantMessage
                        ]
                }["ChatArea.useCallback[handleSendMessage]"]);
                setStreamingContent('');
                try {
                    while(true){
                        const { done, value } = await reader.read();
                        if (done) break;
                        const chunk = decoder.decode(value, {
                            stream: true
                        });
                        const lines = chunk.split('\n');
                        for (const line of lines){
                            if (line.startsWith('data: ')) {
                                const data = line.slice(6);
                                if (data === '[DONE]') {
                                    // Stream is complete
                                    setIsLoading(false);
                                    setStreamingContent('');
                                    return;
                                }
                                try {
                                    const parsed = JSON.parse(data);
                                    if (parsed.type === 'token') {
                                        // Accumulate tokens for streaming display - no filtering
                                        setStreamingContent({
                                            "ChatArea.useCallback[handleSendMessage]": (prev)=>{
                                                const newContent = prev + parsed.content;
                                                setMessages({
                                                    "ChatArea.useCallback[handleSendMessage]": (prevMessages)=>prevMessages.map({
                                                            "ChatArea.useCallback[handleSendMessage]": (msg)=>msg.id === tempAssistantMessage.id ? {
                                                                    ...msg,
                                                                    content: newContent
                                                                } : msg
                                                        }["ChatArea.useCallback[handleSendMessage]"])
                                                }["ChatArea.useCallback[handleSendMessage]"]);
                                                return newContent;
                                            }
                                        }["ChatArea.useCallback[handleSendMessage]"]);
                                    } else if (parsed.type === 'metadata') {
                                        // Handle metadata event - extract thread_id
                                        if (parsed.content && parsed.content.thread_id && !threadId) {
                                            onThreadIdChange(parsed.content.thread_id);
                                        }
                                    } else if (parsed.type === 'message') {
                                    // Skip duplicate message events - content is already handled via tokens
                                    // The backend sends these but we don't need to process them
                                    } else if (parsed.type === 'section') {
                                        onSectionUpdate(parsed.content);
                                    } else if (parsed.type === 'final_response') {
                                        // Handle final response if needed
                                        if (parsed.threadId && !threadId) {
                                            onThreadIdChange(parsed.threadId);
                                        }
                                        if (parsed.section) {
                                            onSectionUpdate(parsed.section);
                                        }
                                        setMessages({
                                            "ChatArea.useCallback[handleSendMessage]": (prevMessages)=>prevMessages.map({
                                                    "ChatArea.useCallback[handleSendMessage]": (msg)=>msg.id === tempAssistantMessage.id ? {
                                                            ...msg,
                                                            content: parsed.content
                                                        } : msg
                                                }["ChatArea.useCallback[handleSendMessage]"])
                                        }["ChatArea.useCallback[handleSendMessage]"]);
                                    }
                                } catch (e) {
                                    console.error('Parse error:', e);
                                }
                            }
                        }
                    }
                } finally{
                    reader.releaseLock();
                    // Ensure loading is set to false when stream ends
                    setIsLoading(false);
                }
            } catch (error) {
                console.error('Error:', error);
                const errorMessage = {
                    id: Date.now().toString() + '-error',
                    role: 'assistant',
                    content: "Sorry, an error occurred while connecting to ".concat(getAgentName(selectedAgent), ". Please try again.")
                };
                setMessages({
                    "ChatArea.useCallback[handleSendMessage]": (prev)=>[
                            ...prev,
                            errorMessage
                        ]
                }["ChatArea.useCallback[handleSendMessage]"]);
                setIsLoading(false);
                // Stop auto mode on error
                if (isAutoMode) {
                    setIsAutoMode(false);
                }
            }
        }
    }["ChatArea.useCallback[handleSendMessage]"], [
        isLoading,
        selectedAgent,
        userId,
        threadId,
        mode,
        onThreadIdChange,
        onSectionUpdate,
        isAutoMode
    ]);
    const handleAutoReply = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useCallback"])({
        "ChatArea.useCallback[handleAutoReply]": async function() {
            let autoSend = arguments.length > 0 && arguments[0] !== void 0 ? arguments[0] : false;
            if (isLoading || isGeneratingLLM || !selectedAgent || !userId) return;
            setIsGeneratingLLM(true);
            try {
                // Call LLM API to generate response
                const response = await fetch('/api/llm-generate', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        messages: messages,
                        agentType: selectedAgent,
                        currentSection: (currentSection === null || currentSection === void 0 ? void 0 : currentSection.name) || null
                    })
                });
                if (!response.ok) {
                    throw new Error('Failed to generate LLM response');
                }
                const data = await response.json();
                if (autoSend) {
                    // Auto send the message
                    await handleSendMessage(data.message);
                } else {
                    // Set the generated message in the input for preview
                    setInput(data.message);
                    // Focus the input field so user can review/edit before sending
                    setTimeout({
                        "ChatArea.useCallback[handleAutoReply]": ()=>{
                            var _inputRef_current;
                            (_inputRef_current = inputRef.current) === null || _inputRef_current === void 0 ? void 0 : _inputRef_current.focus();
                        }
                    }["ChatArea.useCallback[handleAutoReply]"], 100);
                }
            } catch (error) {
                console.error('Error generating LLM response:', error);
                if (!autoSend) {
                    // Fallback message only for manual mode
                    setInput('Yes, let\'s continue.');
                }
            } finally{
                setIsGeneratingLLM(false);
            }
        }
    }["ChatArea.useCallback[handleAutoReply]"], [
        isLoading,
        isGeneratingLLM,
        selectedAgent,
        userId,
        messages,
        currentSection,
        handleSendMessage
    ]);
    const handleSubmit = async (e)=>{
        e.preventDefault();
        await handleSendMessage(input);
    };
    const canSendMessage = selectedAgent && userId && input.trim() && !isLoading && !isAutoMode;
    const copyToClipboard = async (text, messageId)=>{
        try {
            await navigator.clipboard.writeText(text);
            if (messageId) {
                setCopiedMessageId(messageId);
                setTimeout(()=>setCopiedMessageId(null), 1500);
            }
        } catch (err) {
            console.error('Failed to copy text: ', err);
        }
    };
    const copyAllConversation = async ()=>{
        const conversationText = messages.map((msg)=>{
            const role = msg.role === 'user' ? '👤 用户' : "🤖 ".concat(getAgentName(selectedAgent));
            return "".concat(role, ":\n").concat(msg.content);
        }).join('\n\n' + '='.repeat(50) + '\n\n');
        await copyToClipboard(conversationText);
        setCopiedAll(true);
        setTimeout(()=>setCopiedAll(false), 1500);
    };
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
        style: {
            flex: 1,
            display: 'flex',
            flexDirection: 'column',
            height: '100vh'
        },
        className: "jsx-a0e8a0cfa24aa12",
        children: [
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                style: {
                    padding: '16px 24px',
                    borderBottom: '1px solid #e2e8f0',
                    backgroundColor: 'white',
                    display: 'flex',
                    justifyContent: 'space-between',
                    alignItems: 'center',
                    gap: '16px'
                },
                className: "jsx-a0e8a0cfa24aa12",
                children: [
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                        style: {
                            flex: 1
                        },
                        className: "jsx-a0e8a0cfa24aa12",
                        children: [
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("h1", {
                                style: {
                                    fontSize: '20px',
                                    fontWeight: 'bold',
                                    color: '#1e293b',
                                    margin: 0,
                                    display: 'flex',
                                    alignItems: 'center',
                                    gap: '8px'
                                },
                                className: "jsx-a0e8a0cfa24aa12",
                                children: [
                                    selectedAgent ? getAgentName(selectedAgent) : 'Select an Agent',
                                    isAutoMode && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                        style: {
                                            fontSize: '12px',
                                            padding: '2px 8px',
                                            backgroundColor: '#dc2626',
                                            color: 'white',
                                            borderRadius: '4px',
                                            fontWeight: 'normal',
                                            animation: 'pulse 2s infinite'
                                        },
                                        className: "jsx-a0e8a0cfa24aa12",
                                        children: "AUTO MODE"
                                    }, void 0, false, {
                                        fileName: "[project]/src/components/ChatArea.tsx",
                                        lineNumber: 430,
                                        columnNumber: 16
                                    }, this)
                                ]
                            }, void 0, true, {
                                fileName: "[project]/src/components/ChatArea.tsx",
                                lineNumber: 419,
                                columnNumber: 12
                            }, this),
                            selectedAgent && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                                style: {
                                    fontSize: '12px',
                                    color: '#64748b',
                                    margin: '4px 0 0 0'
                                },
                                className: "jsx-a0e8a0cfa24aa12",
                                children: [
                                    selectedAgent === 'value-canvas' && 'Create powerful marketing frameworks',
                                    selectedAgent === 'social-pitch' && 'Craft compelling social pitches',
                                    selectedAgent === 'mission-pitch' && 'Discover your purpose and vision',
                                    selectedAgent === 'special-report' && 'Comprehensive business reports and analysis',
                                    selectedAgent === 'founder-buddy' && 'Validate and refine your startup idea'
                                ]
                            }, void 0, true, {
                                fileName: "[project]/src/components/ChatArea.tsx",
                                lineNumber: 444,
                                columnNumber: 14
                            }, this)
                        ]
                    }, void 0, true, {
                        fileName: "[project]/src/components/ChatArea.tsx",
                        lineNumber: 418,
                        columnNumber: 10
                    }, this),
                    progressSidebar,
                    messages.length > 0 && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                        onClick: copyAllConversation,
                        style: {
                            padding: '8px 12px',
                            backgroundColor: copiedAll ? '#059669' : '#10b981',
                            color: 'white',
                            border: 'none',
                            borderRadius: '6px',
                            fontSize: '12px',
                            cursor: 'pointer',
                            display: 'flex',
                            alignItems: 'center',
                            gap: '4px',
                            transition: 'all 0.2s ease',
                            transform: copiedAll ? 'scale(1.05)' : 'scale(1)',
                            whiteSpace: 'nowrap'
                        },
                        title: copiedAll ? "Copied all messages!" : "Copy all conversation",
                        className: "jsx-a0e8a0cfa24aa12",
                        children: copiedAll ? '✓ Copied!' : '📋 Copy All'
                    }, void 0, false, {
                        fileName: "[project]/src/components/ChatArea.tsx",
                        lineNumber: 461,
                        columnNumber: 12
                    }, this)
                ]
            }, void 0, true, {
                fileName: "[project]/src/components/ChatArea.tsx",
                lineNumber: 409,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                style: {
                    flex: 1,
                    overflowY: 'auto',
                    padding: '24px',
                    backgroundColor: '#f8fafc'
                },
                className: "jsx-a0e8a0cfa24aa12",
                children: !selectedAgent ? /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                    style: {
                        textAlign: 'center',
                        paddingTop: '100px',
                        color: '#64748b'
                    },
                    className: "jsx-a0e8a0cfa24aa12",
                    children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                        style: {
                            fontSize: '16px',
                            marginBottom: '8px'
                        },
                        className: "jsx-a0e8a0cfa24aa12",
                        children: "👈 Please select an agent from the left panel to start chatting"
                    }, void 0, false, {
                        fileName: "[project]/src/components/ChatArea.tsx",
                        lineNumber: 498,
                        columnNumber: 13
                    }, this)
                }, void 0, false, {
                    fileName: "[project]/src/components/ChatArea.tsx",
                    lineNumber: 493,
                    columnNumber: 11
                }, this) : messages.length === 0 ? /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                    style: {
                        textAlign: 'center',
                        paddingTop: '100px',
                        color: '#64748b'
                    },
                    className: "jsx-a0e8a0cfa24aa12",
                    children: [
                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                            style: {
                                fontSize: '16px',
                                marginBottom: '8px'
                            },
                            className: "jsx-a0e8a0cfa24aa12",
                            children: [
                                "🚀 Start your conversation with ",
                                getAgentName(selectedAgent)
                            ]
                        }, void 0, true, {
                            fileName: "[project]/src/components/ChatArea.tsx",
                            lineNumber: 508,
                            columnNumber: 13
                        }, this),
                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                            style: {
                                fontSize: '12px'
                            },
                            className: "jsx-a0e8a0cfa24aa12",
                            children: getPlaceholderText(selectedAgent)
                        }, void 0, false, {
                            fileName: "[project]/src/components/ChatArea.tsx",
                            lineNumber: 511,
                            columnNumber: 13
                        }, this)
                    ]
                }, void 0, true, {
                    fileName: "[project]/src/components/ChatArea.tsx",
                    lineNumber: 503,
                    columnNumber: 11
                }, this) : /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                    style: {
                        display: 'flex',
                        flexDirection: 'column',
                        gap: '16px'
                    },
                    className: "jsx-a0e8a0cfa24aa12",
                    children: [
                        messages.map((message)=>/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                style: {
                                    display: 'flex',
                                    justifyContent: message.role === 'user' ? 'flex-end' : 'flex-start'
                                },
                                className: "jsx-a0e8a0cfa24aa12",
                                children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                    style: {
                                        maxWidth: '70%',
                                        padding: '12px 16px',
                                        borderRadius: '12px',
                                        backgroundColor: message.role === 'user' ? '#3b82f6' : '#ffffff',
                                        color: message.role === 'user' ? 'white' : '#1e293b',
                                        boxShadow: '0 1px 3px rgba(0,0,0,0.1)',
                                        position: 'relative'
                                    },
                                    className: "jsx-a0e8a0cfa24aa12",
                                    children: [
                                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                            style: {
                                                fontSize: '10px',
                                                fontWeight: '500',
                                                marginBottom: '4px',
                                                opacity: 0.7
                                            },
                                            className: "jsx-a0e8a0cfa24aa12",
                                            children: message.role === 'user' ? 'You' : getAgentName(selectedAgent)
                                        }, void 0, false, {
                                            fileName: "[project]/src/components/ChatArea.tsx",
                                            lineNumber: 531,
                                            columnNumber: 19
                                        }, this),
                                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                            style: {
                                                fontSize: '14px',
                                                lineHeight: '1.5',
                                                whiteSpace: message.role === 'user' ? 'pre-wrap' : 'normal'
                                            },
                                            className: "jsx-a0e8a0cfa24aa12",
                                            children: message.role === 'assistant' ? /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$react$2d$markdown$2f$lib$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__$3c$export__Markdown__as__default$3e$__["default"], {
                                                components: {
                                                    p: (param)=>{
                                                        let { children } = param;
                                                        return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                                                            style: {
                                                                margin: '0 0 8px 0'
                                                            },
                                                            className: "jsx-a0e8a0cfa24aa12",
                                                            children: children
                                                        }, void 0, false, {
                                                            fileName: "[project]/src/components/ChatArea.tsx",
                                                            lineNumber: 547,
                                                            columnNumber: 48
                                                        }, void 0);
                                                    },
                                                    h1: (param)=>{
                                                        let { children } = param;
                                                        return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("h1", {
                                                            style: {
                                                                margin: '0 0 12px 0',
                                                                fontSize: '18px',
                                                                fontWeight: 'bold'
                                                            },
                                                            className: "jsx-a0e8a0cfa24aa12",
                                                            children: children
                                                        }, void 0, false, {
                                                            fileName: "[project]/src/components/ChatArea.tsx",
                                                            lineNumber: 548,
                                                            columnNumber: 49
                                                        }, void 0);
                                                    },
                                                    h2: (param)=>{
                                                        let { children } = param;
                                                        return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("h2", {
                                                            style: {
                                                                margin: '0 0 10px 0',
                                                                fontSize: '16px',
                                                                fontWeight: 'bold'
                                                            },
                                                            className: "jsx-a0e8a0cfa24aa12",
                                                            children: children
                                                        }, void 0, false, {
                                                            fileName: "[project]/src/components/ChatArea.tsx",
                                                            lineNumber: 549,
                                                            columnNumber: 49
                                                        }, void 0);
                                                    },
                                                    h3: (param)=>{
                                                        let { children } = param;
                                                        return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("h3", {
                                                            style: {
                                                                margin: '0 0 8px 0',
                                                                fontSize: '15px',
                                                                fontWeight: 'bold'
                                                            },
                                                            className: "jsx-a0e8a0cfa24aa12",
                                                            children: children
                                                        }, void 0, false, {
                                                            fileName: "[project]/src/components/ChatArea.tsx",
                                                            lineNumber: 550,
                                                            columnNumber: 49
                                                        }, void 0);
                                                    },
                                                    ul: (param)=>{
                                                        let { children } = param;
                                                        return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("ul", {
                                                            style: {
                                                                margin: '0 0 8px 0',
                                                                paddingLeft: '16px'
                                                            },
                                                            className: "jsx-a0e8a0cfa24aa12",
                                                            children: children
                                                        }, void 0, false, {
                                                            fileName: "[project]/src/components/ChatArea.tsx",
                                                            lineNumber: 551,
                                                            columnNumber: 49
                                                        }, void 0);
                                                    },
                                                    ol: (param)=>{
                                                        let { children } = param;
                                                        return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("ol", {
                                                            style: {
                                                                margin: '0 0 8px 0',
                                                                paddingLeft: '16px'
                                                            },
                                                            className: "jsx-a0e8a0cfa24aa12",
                                                            children: children
                                                        }, void 0, false, {
                                                            fileName: "[project]/src/components/ChatArea.tsx",
                                                            lineNumber: 552,
                                                            columnNumber: 49
                                                        }, void 0);
                                                    },
                                                    li: (param)=>{
                                                        let { children } = param;
                                                        return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("li", {
                                                            style: {
                                                                margin: '2px 0'
                                                            },
                                                            className: "jsx-a0e8a0cfa24aa12",
                                                            children: children
                                                        }, void 0, false, {
                                                            fileName: "[project]/src/components/ChatArea.tsx",
                                                            lineNumber: 553,
                                                            columnNumber: 49
                                                        }, void 0);
                                                    },
                                                    strong: (param)=>{
                                                        let { children } = param;
                                                        return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("strong", {
                                                            style: {
                                                                fontWeight: 'bold'
                                                            },
                                                            className: "jsx-a0e8a0cfa24aa12",
                                                            children: children
                                                        }, void 0, false, {
                                                            fileName: "[project]/src/components/ChatArea.tsx",
                                                            lineNumber: 554,
                                                            columnNumber: 53
                                                        }, void 0);
                                                    },
                                                    em: (param)=>{
                                                        let { children } = param;
                                                        return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("em", {
                                                            style: {
                                                                fontStyle: 'italic'
                                                            },
                                                            className: "jsx-a0e8a0cfa24aa12",
                                                            children: children
                                                        }, void 0, false, {
                                                            fileName: "[project]/src/components/ChatArea.tsx",
                                                            lineNumber: 555,
                                                            columnNumber: 49
                                                        }, void 0);
                                                    },
                                                    code: (param)=>{
                                                        let { children } = param;
                                                        return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("code", {
                                                            style: {
                                                                backgroundColor: '#f1f5f9',
                                                                padding: '2px 4px',
                                                                borderRadius: '3px',
                                                                fontSize: '13px',
                                                                fontFamily: 'monospace'
                                                            },
                                                            className: "jsx-a0e8a0cfa24aa12",
                                                            children: children
                                                        }, void 0, false, {
                                                            fileName: "[project]/src/components/ChatArea.tsx",
                                                            lineNumber: 556,
                                                            columnNumber: 51
                                                        }, void 0);
                                                    },
                                                    pre: (param)=>{
                                                        let { children } = param;
                                                        return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("pre", {
                                                            style: {
                                                                backgroundColor: '#f1f5f9',
                                                                padding: '8px',
                                                                borderRadius: '6px',
                                                                overflow: 'auto',
                                                                margin: '8px 0'
                                                            },
                                                            className: "jsx-a0e8a0cfa24aa12",
                                                            children: children
                                                        }, void 0, false, {
                                                            fileName: "[project]/src/components/ChatArea.tsx",
                                                            lineNumber: 563,
                                                            columnNumber: 50
                                                        }, void 0);
                                                    },
                                                    blockquote: (param)=>{
                                                        let { children } = param;
                                                        return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("blockquote", {
                                                            style: {
                                                                borderLeft: '3px solid #cbd5e1',
                                                                paddingLeft: '12px',
                                                                margin: '8px 0',
                                                                fontStyle: 'italic'
                                                            },
                                                            className: "jsx-a0e8a0cfa24aa12",
                                                            children: children
                                                        }, void 0, false, {
                                                            fileName: "[project]/src/components/ChatArea.tsx",
                                                            lineNumber: 570,
                                                            columnNumber: 57
                                                        }, void 0);
                                                    }
                                                },
                                                children: message.content
                                            }, void 0, false, {
                                                fileName: "[project]/src/components/ChatArea.tsx",
                                                lineNumber: 545,
                                                columnNumber: 23
                                            }, this) : message.content
                                        }, void 0, false, {
                                            fileName: "[project]/src/components/ChatArea.tsx",
                                            lineNumber: 539,
                                            columnNumber: 19
                                        }, this),
                                        message.role === 'assistant' && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                                            onClick: ()=>copyToClipboard(message.content, message.id),
                                            style: {
                                                position: 'absolute',
                                                top: '8px',
                                                right: '8px',
                                                width: '24px',
                                                height: '24px',
                                                border: 'none',
                                                borderRadius: '4px',
                                                backgroundColor: copiedMessageId === message.id ? '#10b981' : '#f1f5f9',
                                                color: copiedMessageId === message.id ? 'white' : '#64748b',
                                                cursor: 'pointer',
                                                fontSize: '12px',
                                                display: 'flex',
                                                alignItems: 'center',
                                                justifyContent: 'center',
                                                opacity: 0.7,
                                                transition: 'all 0.2s ease',
                                                transform: copiedMessageId === message.id ? 'scale(1.1)' : 'scale(1)'
                                            },
                                            onMouseEnter: (e)=>e.currentTarget.style.opacity = '1',
                                            onMouseLeave: (e)=>e.currentTarget.style.opacity = '0.7',
                                            title: copiedMessageId === message.id ? "Copied!" : "Copy message",
                                            className: "jsx-a0e8a0cfa24aa12",
                                            children: copiedMessageId === message.id ? '✓' : '📋'
                                        }, void 0, false, {
                                            fileName: "[project]/src/components/ChatArea.tsx",
                                            lineNumber: 585,
                                            columnNumber: 21
                                        }, this)
                                    ]
                                }, void 0, true, {
                                    fileName: "[project]/src/components/ChatArea.tsx",
                                    lineNumber: 522,
                                    columnNumber: 17
                                }, this)
                            }, message.id, false, {
                                fileName: "[project]/src/components/ChatArea.tsx",
                                lineNumber: 518,
                                columnNumber: 15
                            }, this)),
                        isLoading && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                            style: {
                                display: 'flex',
                                justifyContent: 'flex-start'
                            },
                            className: "jsx-a0e8a0cfa24aa12",
                            children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                style: {
                                    maxWidth: '70%',
                                    padding: '12px 16px',
                                    borderRadius: '12px',
                                    backgroundColor: '#ffffff',
                                    color: '#1e293b',
                                    boxShadow: '0 1px 3px rgba(0,0,0,0.1)'
                                },
                                className: "jsx-a0e8a0cfa24aa12",
                                children: [
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                        style: {
                                            fontSize: '10px',
                                            fontWeight: '500',
                                            marginBottom: '4px',
                                            opacity: 0.7
                                        },
                                        className: "jsx-a0e8a0cfa24aa12",
                                        children: getAgentName(selectedAgent)
                                    }, void 0, false, {
                                        fileName: "[project]/src/components/ChatArea.tsx",
                                        lineNumber: 627,
                                        columnNumber: 19
                                    }, this),
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                        style: {
                                            fontSize: '14px',
                                            color: '#64748b',
                                            display: 'flex',
                                            alignItems: 'center',
                                            gap: '8px'
                                        },
                                        className: "jsx-a0e8a0cfa24aa12",
                                        children: [
                                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                                style: {
                                                    width: '16px',
                                                    height: '16px',
                                                    border: '2px solid #f3f4f6',
                                                    borderTop: '2px solid #3b82f6',
                                                    borderRadius: '50%',
                                                    animation: 'spin 1s linear infinite'
                                                },
                                                className: "jsx-a0e8a0cfa24aa12"
                                            }, void 0, false, {
                                                fileName: "[project]/src/components/ChatArea.tsx",
                                                lineNumber: 642,
                                                columnNumber: 21
                                            }, this),
                                            mode === 'stream' ? 'Thinking...' : 'Processing...'
                                        ]
                                    }, void 0, true, {
                                        fileName: "[project]/src/components/ChatArea.tsx",
                                        lineNumber: 635,
                                        columnNumber: 19
                                    }, this)
                                ]
                            }, void 0, true, {
                                fileName: "[project]/src/components/ChatArea.tsx",
                                lineNumber: 619,
                                columnNumber: 17
                            }, this)
                        }, void 0, false, {
                            fileName: "[project]/src/components/ChatArea.tsx",
                            lineNumber: 618,
                            columnNumber: 15
                        }, this),
                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                            ref: messagesEndRef,
                            className: "jsx-a0e8a0cfa24aa12"
                        }, void 0, false, {
                            fileName: "[project]/src/components/ChatArea.tsx",
                            lineNumber: 656,
                            columnNumber: 13
                        }, this)
                    ]
                }, void 0, true, {
                    fileName: "[project]/src/components/ChatArea.tsx",
                    lineNumber: 516,
                    columnNumber: 11
                }, this)
            }, void 0, false, {
                fileName: "[project]/src/components/ChatArea.tsx",
                lineNumber: 486,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                style: {
                    padding: '16px 24px',
                    backgroundColor: 'white',
                    borderTop: '1px solid #e2e8f0'
                },
                className: "jsx-a0e8a0cfa24aa12",
                children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("form", {
                    onSubmit: handleSubmit,
                    style: {
                        display: 'flex',
                        gap: '12px'
                    },
                    className: "jsx-a0e8a0cfa24aa12",
                    children: [
                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("input", {
                            ref: inputRef,
                            type: "text",
                            value: input,
                            onChange: (e)=>setInput(e.target.value),
                            placeholder: isAutoMode ? 'Auto conversation in progress...' : selectedAgent ? getPlaceholderText(selectedAgent) : 'Select an agent first...',
                            disabled: !selectedAgent || !userId || isGeneratingLLM || isAutoMode,
                            style: {
                                flex: 1,
                                padding: '12px 16px',
                                border: '1px solid #d1d5db',
                                borderRadius: '8px',
                                fontSize: '14px',
                                outline: 'none',
                                backgroundColor: isAutoMode ? '#f9fafb' : 'white',
                                cursor: isAutoMode ? 'not-allowed' : 'text'
                            },
                            className: "jsx-a0e8a0cfa24aa12"
                        }, void 0, false, {
                            fileName: "[project]/src/components/ChatArea.tsx",
                            lineNumber: 668,
                            columnNumber: 11
                        }, this),
                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                            type: "button",
                            onClick: ()=>handleAutoReply(false),
                            disabled: !selectedAgent || !userId || isLoading || isGeneratingLLM || isAutoMode,
                            style: {
                                padding: '12px 20px',
                                backgroundColor: isGeneratingLLM ? '#fbbf24' : !selectedAgent || !userId || isLoading || isAutoMode ? '#d1d5db' : '#10b981',
                                color: 'white',
                                borderRadius: '8px',
                                border: 'none',
                                fontSize: '14px',
                                cursor: !selectedAgent || !userId || isLoading || isGeneratingLLM || isAutoMode ? 'not-allowed' : 'pointer',
                                fontWeight: '500',
                                display: 'flex',
                                alignItems: 'center',
                                gap: '6px',
                                transition: 'all 0.2s ease'
                            },
                            title: "Generate response using AI (for testing)",
                            className: "jsx-a0e8a0cfa24aa12",
                            children: isGeneratingLLM ? /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["Fragment"], {
                                children: [
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                        style: {
                                            width: '14px',
                                            height: '14px',
                                            border: '2px solid rgba(255, 255, 255, 0.3)',
                                            borderTop: '2px solid white',
                                            borderRadius: '50%',
                                            animation: 'spin 0.8s linear infinite'
                                        },
                                        className: "jsx-a0e8a0cfa24aa12"
                                    }, void 0, false, {
                                        fileName: "[project]/src/components/ChatArea.tsx",
                                        lineNumber: 712,
                                        columnNumber: 17
                                    }, this),
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                        className: "jsx-a0e8a0cfa24aa12",
                                        children: "Generating..."
                                    }, void 0, false, {
                                        fileName: "[project]/src/components/ChatArea.tsx",
                                        lineNumber: 720,
                                        columnNumber: 17
                                    }, this)
                                ]
                            }, void 0, true) : /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["Fragment"], {
                                children: [
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                        className: "jsx-a0e8a0cfa24aa12",
                                        children: "🤖"
                                    }, void 0, false, {
                                        fileName: "[project]/src/components/ChatArea.tsx",
                                        lineNumber: 724,
                                        columnNumber: 17
                                    }, this),
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                        className: "jsx-a0e8a0cfa24aa12",
                                        children: "Auto Reply"
                                    }, void 0, false, {
                                        fileName: "[project]/src/components/ChatArea.tsx",
                                        lineNumber: 725,
                                        columnNumber: 17
                                    }, this)
                                ]
                            }, void 0, true)
                        }, void 0, false, {
                            fileName: "[project]/src/components/ChatArea.tsx",
                            lineNumber: 686,
                            columnNumber: 11
                        }, this),
                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                            type: "button",
                            onClick: ()=>{
                                if (isAutoMode) {
                                    setIsAutoMode(false);
                                    // If generating LLM, stop it immediately
                                    if (isGeneratingLLM) {
                                        setIsGeneratingLLM(false);
                                    }
                                } else {
                                    setIsAutoMode(true);
                                    // Start the conversation if no messages yet
                                    if (messages.length === 0) {
                                        handleAutoReply(true);
                                    }
                                }
                            },
                            disabled: !selectedAgent || !userId || !isAutoMode && (isLoading || isGeneratingLLM),
                            style: {
                                padding: '12px 20px',
                                backgroundColor: isAutoMode ? '#dc2626' : !selectedAgent || !userId || isLoading || isGeneratingLLM ? '#d1d5db' : '#8b5cf6',
                                color: 'white',
                                borderRadius: '8px',
                                border: 'none',
                                fontSize: '14px',
                                cursor: !selectedAgent || !userId || !isAutoMode && (isLoading || isGeneratingLLM) ? 'not-allowed' : 'pointer',
                                fontWeight: '500',
                                display: 'flex',
                                alignItems: 'center',
                                gap: '6px',
                                transition: 'all 0.2s ease'
                            },
                            title: isAutoMode ? "Stop auto conversation" : "Start auto conversation",
                            className: "jsx-a0e8a0cfa24aa12",
                            children: isAutoMode ? /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["Fragment"], {
                                children: [
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                        className: "jsx-a0e8a0cfa24aa12",
                                        children: "⏹️"
                                    }, void 0, false, {
                                        fileName: "[project]/src/components/ChatArea.tsx",
                                        lineNumber: 769,
                                        columnNumber: 17
                                    }, this),
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                        className: "jsx-a0e8a0cfa24aa12",
                                        children: "Stop Auto"
                                    }, void 0, false, {
                                        fileName: "[project]/src/components/ChatArea.tsx",
                                        lineNumber: 770,
                                        columnNumber: 17
                                    }, this)
                                ]
                            }, void 0, true) : /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["Fragment"], {
                                children: [
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                        className: "jsx-a0e8a0cfa24aa12",
                                        children: "▶️"
                                    }, void 0, false, {
                                        fileName: "[project]/src/components/ChatArea.tsx",
                                        lineNumber: 774,
                                        columnNumber: 17
                                    }, this),
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                        className: "jsx-a0e8a0cfa24aa12",
                                        children: "Start Auto"
                                    }, void 0, false, {
                                        fileName: "[project]/src/components/ChatArea.tsx",
                                        lineNumber: 775,
                                        columnNumber: 17
                                    }, this)
                                ]
                            }, void 0, true)
                        }, void 0, false, {
                            fileName: "[project]/src/components/ChatArea.tsx",
                            lineNumber: 729,
                            columnNumber: 11
                        }, this),
                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                            type: "submit",
                            disabled: !canSendMessage,
                            style: {
                                padding: '12px 24px',
                                backgroundColor: canSendMessage ? '#3b82f6' : '#9ca3af',
                                color: 'white',
                                borderRadius: '8px',
                                border: 'none',
                                fontSize: '14px',
                                cursor: canSendMessage ? 'pointer' : 'not-allowed',
                                fontWeight: '500'
                            },
                            className: "jsx-a0e8a0cfa24aa12",
                            children: "Send"
                        }, void 0, false, {
                            fileName: "[project]/src/components/ChatArea.tsx",
                            lineNumber: 779,
                            columnNumber: 11
                        }, this)
                    ]
                }, void 0, true, {
                    fileName: "[project]/src/components/ChatArea.tsx",
                    lineNumber: 667,
                    columnNumber: 9
                }, this)
            }, void 0, false, {
                fileName: "[project]/src/components/ChatArea.tsx",
                lineNumber: 662,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$styled$2d$jsx$2f$style$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["default"], {
                id: "a0e8a0cfa24aa12",
                children: "@keyframes spin{0%{transform:rotate(0)}to{transform:rotate(360deg)}}@keyframes pulse{0%,to{opacity:1}50%{opacity:.5}}"
            }, void 0, false, void 0, this)
        ]
    }, void 0, true, {
        fileName: "[project]/src/components/ChatArea.tsx",
        lineNumber: 402,
        columnNumber: 5
    }, this);
}
_s(ChatArea, "IzkAFwxp5P4Dwarc6OpI9XVuBS4=");
_c = ChatArea;
var _c;
__turbopack_context__.k.register(_c, "ChatArea");
if (typeof globalThis.$RefreshHelpers$ === 'object' && globalThis.$RefreshHelpers !== null) {
    __turbopack_context__.k.registerExports(module, globalThis.$RefreshHelpers$);
}
}}),
"[project]/src/components/ProgressSidebar.tsx [app-client] (ecmascript)": ((__turbopack_context__) => {
"use strict";

var { k: __turbopack_refresh__, m: module } = __turbopack_context__;
{
__turbopack_context__.s({
    "default": ()=>ProgressSidebar
});
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/next/dist/compiled/react/jsx-dev-runtime.js [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/next/dist/compiled/react/index.js [app-client] (ecmascript)");
;
var _s = __turbopack_context__.k.signature();
'use client';
;
// Define all sections for founder-buddy
const FOUNDER_BUDDY_SECTIONS = [
    {
        id: 'mission',
        name: 'Mission',
        displayName: 'Mission'
    },
    {
        id: 'idea',
        name: 'Idea',
        displayName: 'Idea'
    },
    {
        id: 'team_traction',
        name: 'Team & Traction',
        displayName: 'Team & Traction'
    },
    {
        id: 'invest_plan',
        name: 'Investment Plan',
        displayName: 'Investment Plan'
    }
];
function ProgressSidebar(param) {
    let { currentSection, selectedAgent } = param;
    _s();
    const [isOpen, setIsOpen] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useState"])(false);
    const getSectionTitle = (agentId)=>{
        if (agentId === 'value-canvas') return 'Current Section';
        if (agentId === 'social-pitch') return 'Current Component';
        if (agentId === 'mission-pitch') return 'Current Stage';
        if (agentId === 'special-report') return 'Current Section';
        return 'Progress';
    };
    // Get status for a section
    const getSectionStatus = (sectionId)=>{
        if (!currentSection) return 'pending';
        // Match by section name (case-insensitive)
        const currentSectionName = currentSection.name.toLowerCase();
        const sectionName = sectionId.toLowerCase();
        // Check if this is the current section
        if (currentSectionName.includes(sectionName) || sectionName.includes(currentSectionName)) {
            if (currentSection.status === 'completed' || currentSection.status === 'done') {
                return 'completed';
            }
            return 'in_progress';
        }
        // Check if sections before this one are completed
        const currentIndex = FOUNDER_BUDDY_SECTIONS.findIndex((s)=>currentSectionName.includes(s.id) || currentSectionName.includes(s.name.toLowerCase()));
        const sectionIndex = FOUNDER_BUDDY_SECTIONS.findIndex((s)=>s.id === sectionId);
        if (currentIndex > sectionIndex) {
            return 'completed';
        }
        return 'pending';
    };
    // Get display name for current section
    const getCurrentSectionDisplayName = ()=>{
        if (!currentSection) return 'Select a section';
        // Try to match with our defined sections
        const matched = FOUNDER_BUDDY_SECTIONS.find((s)=>currentSection.name.toLowerCase().includes(s.id) || currentSection.name.toLowerCase().includes(s.name.toLowerCase()));
        return matched ? matched.displayName : currentSection.name;
    };
    const getStatusColor = (status)=>{
        switch(status){
            case 'completed':
            case 'done':
                return '#10b981'; // green
            case 'in_progress':
                return '#6366f1'; // purple
            default:
                return '#94a3b8'; // gray
        }
    };
    const getStatusText = (status)=>{
        switch(status){
            case 'completed':
            case 'done':
                return 'Done';
            case 'in_progress':
                return 'In Progress';
            default:
                return 'Pending';
        }
    };
    // Only show dropdown for founder-buddy
    if (selectedAgent !== 'founder-buddy') {
        return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
            style: {
                display: 'flex',
                gap: '12px',
                alignItems: 'center'
            },
            children: [
                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                    style: {
                        fontSize: '12px',
                        fontWeight: '600',
                        color: '#64748b',
                        whiteSpace: 'nowrap'
                    },
                    children: [
                        getSectionTitle(selectedAgent),
                        ":"
                    ]
                }, void 0, true, {
                    fileName: "[project]/src/components/ProgressSidebar.tsx",
                    lineNumber: 109,
                    columnNumber: 9
                }, this),
                currentSection ? /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                    style: {
                        display: 'flex',
                        gap: '8px',
                        alignItems: 'center'
                    },
                    children: [
                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                            style: {
                                padding: '6px 12px',
                                backgroundColor: '#f8fafc',
                                borderRadius: '6px',
                                border: '1px solid #e2e8f0',
                                fontSize: '12px',
                                color: '#1e293b',
                                fontWeight: '500'
                            },
                            children: [
                                "#",
                                currentSection.database_id
                            ]
                        }, void 0, true, {
                            fileName: "[project]/src/components/ProgressSidebar.tsx",
                            lineNumber: 120,
                            columnNumber: 13
                        }, this),
                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                            style: {
                                padding: '6px 12px',
                                backgroundColor: '#f8fafc',
                                borderRadius: '6px',
                                border: '1px solid #e2e8f0',
                                fontSize: '12px',
                                color: '#1e293b',
                                fontWeight: '500'
                            },
                            children: currentSection.name
                        }, void 0, false, {
                            fileName: "[project]/src/components/ProgressSidebar.tsx",
                            lineNumber: 132,
                            columnNumber: 13
                        }, this),
                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                            style: {
                                padding: '6px 12px',
                                backgroundColor: '#f8fafc',
                                borderRadius: '6px',
                                border: '1px solid #e2e8f0',
                                fontSize: '12px',
                                fontWeight: '500',
                                color: currentSection.status === 'pending' ? '#f59e0b' : currentSection.status === 'completed' ? '#10b981' : '#6366f1',
                                display: 'flex',
                                alignItems: 'center',
                                gap: '4px'
                            },
                            children: [
                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                    style: {
                                        width: '6px',
                                        height: '6px',
                                        borderRadius: '50%',
                                        backgroundColor: currentSection.status === 'pending' ? '#f59e0b' : currentSection.status === 'completed' ? '#10b981' : '#6366f1'
                                    }
                                }, void 0, false, {
                                    fileName: "[project]/src/components/ProgressSidebar.tsx",
                                    lineNumber: 157,
                                    columnNumber: 15
                                }, this),
                                currentSection.status.charAt(0).toUpperCase() + currentSection.status.slice(1)
                            ]
                        }, void 0, true, {
                            fileName: "[project]/src/components/ProgressSidebar.tsx",
                            lineNumber: 144,
                            columnNumber: 13
                        }, this)
                    ]
                }, void 0, true, {
                    fileName: "[project]/src/components/ProgressSidebar.tsx",
                    lineNumber: 119,
                    columnNumber: 11
                }, this) : /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                    style: {
                        fontSize: '12px',
                        color: '#94a3b8',
                        fontStyle: 'italic'
                    },
                    children: selectedAgent ? 'Start a conversation to see progress' : 'Select an agent to begin'
                }, void 0, false, {
                    fileName: "[project]/src/components/ProgressSidebar.tsx",
                    lineNumber: 168,
                    columnNumber: 11
                }, this)
            ]
        }, void 0, true, {
            fileName: "[project]/src/components/ProgressSidebar.tsx",
            lineNumber: 104,
            columnNumber: 7
        }, this);
    }
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
        style: {
            display: 'flex',
            gap: '12px',
            alignItems: 'center',
            position: 'relative'
        },
        children: [
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                style: {
                    fontSize: '12px',
                    fontWeight: '600',
                    color: '#64748b',
                    whiteSpace: 'nowrap'
                },
                children: [
                    getSectionTitle(selectedAgent),
                    ":"
                ]
            }, void 0, true, {
                fileName: "[project]/src/components/ProgressSidebar.tsx",
                lineNumber: 187,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                style: {
                    position: 'relative',
                    minWidth: '200px'
                },
                children: [
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                        onClick: ()=>setIsOpen(!isOpen),
                        style: {
                            width: '100%',
                            padding: '8px 12px',
                            backgroundColor: '#f8fafc',
                            border: '1px solid #e2e8f0',
                            borderRadius: '6px',
                            fontSize: '12px',
                            color: '#1e293b',
                            fontWeight: '500',
                            cursor: 'pointer',
                            display: 'flex',
                            alignItems: 'center',
                            justifyContent: 'space-between',
                            gap: '8px',
                            transition: 'all 0.2s ease'
                        },
                        onMouseEnter: (e)=>{
                            e.currentTarget.style.backgroundColor = '#f1f5f9';
                            e.currentTarget.style.borderColor = '#cbd5e1';
                        },
                        onMouseLeave: (e)=>{
                            if (!isOpen) {
                                e.currentTarget.style.backgroundColor = '#f8fafc';
                                e.currentTarget.style.borderColor = '#e2e8f0';
                            }
                        },
                        children: [
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                style: {
                                    display: 'flex',
                                    alignItems: 'center',
                                    gap: '8px',
                                    flex: 1
                                },
                                children: currentSection ? /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["Fragment"], {
                                    children: [
                                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                            style: {
                                                width: '6px',
                                                height: '6px',
                                                borderRadius: '50%',
                                                backgroundColor: getStatusColor(currentSection.status)
                                            }
                                        }, void 0, false, {
                                            fileName: "[project]/src/components/ProgressSidebar.tsx",
                                            lineNumber: 229,
                                            columnNumber: 17
                                        }, this),
                                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                            children: getCurrentSectionDisplayName()
                                        }, void 0, false, {
                                            fileName: "[project]/src/components/ProgressSidebar.tsx",
                                            lineNumber: 235,
                                            columnNumber: 17
                                        }, this),
                                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                            style: {
                                                fontSize: '10px',
                                                color: '#94a3b8',
                                                marginLeft: 'auto'
                                            },
                                            children: getStatusText(currentSection.status)
                                        }, void 0, false, {
                                            fileName: "[project]/src/components/ProgressSidebar.tsx",
                                            lineNumber: 236,
                                            columnNumber: 17
                                        }, this)
                                    ]
                                }, void 0, true) : /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                    style: {
                                        color: '#94a3b8'
                                    },
                                    children: "Select a section"
                                }, void 0, false, {
                                    fileName: "[project]/src/components/ProgressSidebar.tsx",
                                    lineNumber: 245,
                                    columnNumber: 15
                                }, this)
                            }, void 0, false, {
                                fileName: "[project]/src/components/ProgressSidebar.tsx",
                                lineNumber: 226,
                                columnNumber: 11
                            }, this),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                style: {
                                    fontSize: '10px',
                                    color: '#64748b',
                                    transform: isOpen ? 'rotate(180deg)' : 'rotate(0deg)',
                                    transition: 'transform 0.2s ease'
                                },
                                children: "▼"
                            }, void 0, false, {
                                fileName: "[project]/src/components/ProgressSidebar.tsx",
                                lineNumber: 248,
                                columnNumber: 11
                            }, this)
                        ]
                    }, void 0, true, {
                        fileName: "[project]/src/components/ProgressSidebar.tsx",
                        lineNumber: 197,
                        columnNumber: 9
                    }, this),
                    isOpen && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["Fragment"], {
                        children: [
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                onClick: ()=>setIsOpen(false),
                                style: {
                                    position: 'fixed',
                                    top: 0,
                                    left: 0,
                                    right: 0,
                                    bottom: 0,
                                    zIndex: 998
                                }
                            }, void 0, false, {
                                fileName: "[project]/src/components/ProgressSidebar.tsx",
                                lineNumber: 258,
                                columnNumber: 13
                            }, this),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                style: {
                                    position: 'absolute',
                                    top: '100%',
                                    left: 0,
                                    right: 0,
                                    marginTop: '4px',
                                    backgroundColor: 'white',
                                    border: '1px solid #e2e8f0',
                                    borderRadius: '6px',
                                    boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)',
                                    zIndex: 999,
                                    overflow: 'hidden',
                                    maxHeight: '300px',
                                    overflowY: 'auto'
                                },
                                children: FOUNDER_BUDDY_SECTIONS.map((section)=>{
                                    const status = getSectionStatus(section.id);
                                    const isCurrent = currentSection && (currentSection.name.toLowerCase().includes(section.id) || currentSection.name.toLowerCase().includes(section.name.toLowerCase()));
                                    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                        onClick: ()=>{
                                            setIsOpen(false);
                                        // Could add navigation logic here if needed
                                        },
                                        style: {
                                            padding: '10px 12px',
                                            cursor: 'pointer',
                                            backgroundColor: isCurrent ? '#f0f9ff' : 'white',
                                            borderLeft: isCurrent ? '3px solid #6366f1' : '3px solid transparent',
                                            display: 'flex',
                                            alignItems: 'center',
                                            justifyContent: 'space-between',
                                            gap: '8px',
                                            transition: 'background-color 0.15s ease'
                                        },
                                        onMouseEnter: (e)=>{
                                            e.currentTarget.style.backgroundColor = '#f8fafc';
                                        },
                                        onMouseLeave: (e)=>{
                                            e.currentTarget.style.backgroundColor = isCurrent ? '#f0f9ff' : 'white';
                                        },
                                        children: [
                                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                                style: {
                                                    display: 'flex',
                                                    alignItems: 'center',
                                                    gap: '8px',
                                                    flex: 1
                                                },
                                                children: [
                                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                                        style: {
                                                            width: '6px',
                                                            height: '6px',
                                                            borderRadius: '50%',
                                                            backgroundColor: getStatusColor(status)
                                                        }
                                                    }, void 0, false, {
                                                        fileName: "[project]/src/components/ProgressSidebar.tsx",
                                                        lineNumber: 317,
                                                        columnNumber: 23
                                                    }, this),
                                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                                        style: {
                                                            fontSize: '12px',
                                                            fontWeight: isCurrent ? '600' : '500',
                                                            color: '#1e293b'
                                                        },
                                                        children: section.displayName
                                                    }, void 0, false, {
                                                        fileName: "[project]/src/components/ProgressSidebar.tsx",
                                                        lineNumber: 323,
                                                        columnNumber: 23
                                                    }, this)
                                                ]
                                            }, void 0, true, {
                                                fileName: "[project]/src/components/ProgressSidebar.tsx",
                                                lineNumber: 316,
                                                columnNumber: 21
                                            }, this),
                                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                                style: {
                                                    fontSize: '10px',
                                                    color: getStatusColor(status),
                                                    fontWeight: '500'
                                                },
                                                children: getStatusText(status)
                                            }, void 0, false, {
                                                fileName: "[project]/src/components/ProgressSidebar.tsx",
                                                lineNumber: 331,
                                                columnNumber: 21
                                            }, this)
                                        ]
                                    }, section.id, true, {
                                        fileName: "[project]/src/components/ProgressSidebar.tsx",
                                        lineNumber: 292,
                                        columnNumber: 19
                                    }, this);
                                })
                            }, void 0, false, {
                                fileName: "[project]/src/components/ProgressSidebar.tsx",
                                lineNumber: 269,
                                columnNumber: 13
                            }, this)
                        ]
                    }, void 0, true)
                ]
            }, void 0, true, {
                fileName: "[project]/src/components/ProgressSidebar.tsx",
                lineNumber: 196,
                columnNumber: 7
            }, this)
        ]
    }, void 0, true, {
        fileName: "[project]/src/components/ProgressSidebar.tsx",
        lineNumber: 181,
        columnNumber: 5
    }, this);
}
_s(ProgressSidebar, "+sus0Lb0ewKHdwiUhiTAJFoFyQ0=");
_c = ProgressSidebar;
var _c;
__turbopack_context__.k.register(_c, "ProgressSidebar");
if (typeof globalThis.$RefreshHelpers$ === 'object' && globalThis.$RefreshHelpers !== null) {
    __turbopack_context__.k.registerExports(module, globalThis.$RefreshHelpers$);
}
}}),
"[project]/src/components/ConversationHistory.tsx [app-client] (ecmascript)": ((__turbopack_context__) => {
"use strict";

var { k: __turbopack_refresh__, m: module } = __turbopack_context__;
{
__turbopack_context__.s({
    "default": ()=>ConversationHistory
});
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/next/dist/compiled/react/jsx-dev-runtime.js [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/next/dist/compiled/react/index.js [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$utils$2f$conversationStorage$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/src/utils/conversationStorage.ts [app-client] (ecmascript)");
;
var _s = __turbopack_context__.k.signature();
'use client';
;
;
const agentIcons = {
    'value-canvas': '💎',
    'mission-pitch': '🎯',
    'signature-pitch': '✍️',
    'social-pitch': '🌐',
    'special-report': '📊'
};
function ConversationHistory(param) {
    let { currentThreadId, selectedAgent, onSelectConversation, onDeleteConversation } = param;
    _s();
    const [conversations, setConversations] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useState"])([]);
    const [filter, setFilter] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useState"])('all');
    const [showFilters, setShowFilters] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useState"])(false);
    (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useEffect"])({
        "ConversationHistory.useEffect": ()=>{
            loadConversations();
            const interval = setInterval(loadConversations, 5000);
            return ({
                "ConversationHistory.useEffect": ()=>clearInterval(interval)
            })["ConversationHistory.useEffect"];
        }
    }["ConversationHistory.useEffect"], []);
    const loadConversations = ()=>{
        const allConversations = __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$utils$2f$conversationStorage$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["conversationStorage"].getAll();
        setConversations(allConversations);
    };
    const handleDelete = (e, threadId)=>{
        e.stopPropagation();
        if (confirm('Delete this conversation?')) {
            __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$utils$2f$conversationStorage$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["conversationStorage"].delete(threadId);
            loadConversations();
            if (onDeleteConversation) {
                onDeleteConversation(threadId);
            }
        }
    };
    const handleClearAll = ()=>{
        if (confirm('Delete all conversation history?')) {
            __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$utils$2f$conversationStorage$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["conversationStorage"].clear();
            loadConversations();
        }
    };
    const handleNewConversation = ()=>{
        window.location.reload();
    };
    const filteredConversations = conversations.filter((conv)=>{
        return filter === 'all' || conv.agentType === filter;
    });
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
        style: {
            height: '100%',
            display: 'flex',
            flexDirection: 'column',
            backgroundColor: '#f8fafc'
        },
        children: [
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                style: {
                    padding: '16px',
                    backgroundColor: 'white',
                    borderBottom: '1px solid #e2e8f0'
                },
                children: [
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                        style: {
                            display: 'flex',
                            justifyContent: 'space-between',
                            alignItems: 'center',
                            marginBottom: '12px'
                        },
                        children: [
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("h3", {
                                style: {
                                    margin: 0,
                                    fontSize: '14px',
                                    fontWeight: 600,
                                    color: '#1e293b'
                                },
                                children: "Conversations"
                            }, void 0, false, {
                                fileName: "[project]/src/components/ConversationHistory.tsx",
                                lineNumber: 87,
                                columnNumber: 11
                            }, this),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                style: {
                                    display: 'flex',
                                    gap: '4px'
                                },
                                children: [
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                                        onClick: ()=>setShowFilters(!showFilters),
                                        style: {
                                            padding: '4px 8px',
                                            fontSize: '11px',
                                            color: '#64748b',
                                            background: 'white',
                                            border: '1px solid #e2e8f0',
                                            borderRadius: '4px',
                                            cursor: 'pointer'
                                        },
                                        title: "Filter conversations",
                                        children: "🔽 Filter"
                                    }, void 0, false, {
                                        fileName: "[project]/src/components/ConversationHistory.tsx",
                                        lineNumber: 96,
                                        columnNumber: 13
                                    }, this),
                                    conversations.length > 0 && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                                        onClick: handleClearAll,
                                        style: {
                                            padding: '4px 8px',
                                            fontSize: '11px',
                                            color: '#ef4444',
                                            background: 'white',
                                            border: '1px solid #fecaca',
                                            borderRadius: '4px',
                                            cursor: 'pointer'
                                        },
                                        title: "Clear all conversations",
                                        children: "Clear"
                                    }, void 0, false, {
                                        fileName: "[project]/src/components/ConversationHistory.tsx",
                                        lineNumber: 112,
                                        columnNumber: 15
                                    }, this)
                                ]
                            }, void 0, true, {
                                fileName: "[project]/src/components/ConversationHistory.tsx",
                                lineNumber: 95,
                                columnNumber: 11
                            }, this)
                        ]
                    }, void 0, true, {
                        fileName: "[project]/src/components/ConversationHistory.tsx",
                        lineNumber: 81,
                        columnNumber: 9
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                        onClick: handleNewConversation,
                        style: {
                            width: '100%',
                            padding: '10px',
                            backgroundColor: '#3b82f6',
                            color: 'white',
                            border: 'none',
                            borderRadius: '6px',
                            fontSize: '13px',
                            fontWeight: 500,
                            cursor: 'pointer',
                            display: 'flex',
                            alignItems: 'center',
                            justifyContent: 'center',
                            gap: '6px'
                        },
                        children: [
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                style: {
                                    fontSize: '16px'
                                },
                                children: "+"
                            }, void 0, false, {
                                fileName: "[project]/src/components/ConversationHistory.tsx",
                                lineNumber: 150,
                                columnNumber: 11
                            }, this),
                            "New Conversation"
                        ]
                    }, void 0, true, {
                        fileName: "[project]/src/components/ConversationHistory.tsx",
                        lineNumber: 132,
                        columnNumber: 9
                    }, this),
                    showFilters && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                        style: {
                            marginTop: '12px',
                            display: 'flex',
                            gap: '4px',
                            flexWrap: 'wrap'
                        },
                        children: [
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                                onClick: ()=>setFilter('all'),
                                style: {
                                    padding: '4px 10px',
                                    fontSize: '11px',
                                    background: filter === 'all' ? '#3b82f6' : 'white',
                                    color: filter === 'all' ? 'white' : '#64748b',
                                    border: "1px solid ".concat(filter === 'all' ? '#3b82f6' : '#e2e8f0'),
                                    borderRadius: '12px',
                                    cursor: 'pointer'
                                },
                                children: [
                                    "All (",
                                    conversations.length,
                                    ")"
                                ]
                            }, void 0, true, {
                                fileName: "[project]/src/components/ConversationHistory.tsx",
                                lineNumber: 162,
                                columnNumber: 13
                            }, this),
                            Object.entries(agentIcons).map((param)=>{
                                let [agent, icon] = param;
                                const count = conversations.filter((c)=>c.agentType === agent).length;
                                if (count === 0) return null;
                                return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                                    onClick: ()=>setFilter(agent),
                                    style: {
                                        padding: '4px 10px',
                                        fontSize: '11px',
                                        background: filter === agent ? '#3b82f6' : 'white',
                                        color: filter === agent ? 'white' : '#64748b',
                                        border: "1px solid ".concat(filter === agent ? '#3b82f6' : '#e2e8f0'),
                                        borderRadius: '12px',
                                        cursor: 'pointer'
                                    },
                                    children: [
                                        icon,
                                        " (",
                                        count,
                                        ")"
                                    ]
                                }, agent, true, {
                                    fileName: "[project]/src/components/ConversationHistory.tsx",
                                    lineNumber: 180,
                                    columnNumber: 17
                                }, this);
                            })
                        ]
                    }, void 0, true, {
                        fileName: "[project]/src/components/ConversationHistory.tsx",
                        lineNumber: 156,
                        columnNumber: 11
                    }, this)
                ]
            }, void 0, true, {
                fileName: "[project]/src/components/ConversationHistory.tsx",
                lineNumber: 76,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                style: {
                    flex: 1,
                    overflowY: 'auto',
                    padding: '12px'
                },
                children: filteredConversations.length === 0 ? /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                    style: {
                        textAlign: 'center',
                        color: '#94a3b8',
                        padding: '32px 16px',
                        fontSize: '13px'
                    },
                    children: conversations.length === 0 ? 'No conversations yet. Start a new conversation above.' : 'No conversations match the selected filter.'
                }, void 0, false, {
                    fileName: "[project]/src/components/ConversationHistory.tsx",
                    lineNumber: 208,
                    columnNumber: 11
                }, this) : /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                    style: {
                        display: 'flex',
                        flexDirection: 'column',
                        gap: '8px'
                    },
                    children: filteredConversations.map((conv)=>/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                            onClick: ()=>onSelectConversation(conv),
                            style: {
                                padding: '12px',
                                background: currentThreadId === conv.threadId ? 'linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%)' : 'white',
                                border: currentThreadId === conv.threadId ? '2px solid #6366f1' : '1px solid #e2e8f0',
                                borderRadius: '10px',
                                cursor: 'pointer',
                                transition: 'all 0.2s',
                                position: 'relative',
                                boxShadow: currentThreadId === conv.threadId ? '0 10px 25px -5px rgba(99, 102, 241, 0.3)' : '0 1px 2px 0 rgba(0, 0, 0, 0.05)'
                            },
                            onMouseEnter: (e)=>{
                                if (currentThreadId !== conv.threadId) {
                                    e.currentTarget.style.transform = 'translateY(-2px)';
                                    e.currentTarget.style.boxShadow = '0 4px 6px -1px rgba(0, 0, 0, 0.1)';
                                }
                            },
                            onMouseLeave: (e)=>{
                                if (currentThreadId !== conv.threadId) {
                                    e.currentTarget.style.transform = 'translateY(0)';
                                    e.currentTarget.style.boxShadow = '0 1px 2px 0 rgba(0, 0, 0, 0.05)';
                                }
                            },
                            children: [
                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                    style: {
                                        display: 'flex',
                                        justifyContent: 'space-between',
                                        alignItems: 'flex-start',
                                        marginBottom: '6px'
                                    },
                                    children: [
                                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                            style: {
                                                display: 'flex',
                                                alignItems: 'center',
                                                gap: '8px',
                                                flex: 1
                                            },
                                            children: [
                                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                                    style: {
                                                        fontSize: '16px',
                                                        filter: currentThreadId === conv.threadId ? 'grayscale(0) brightness(1.2)' : 'none'
                                                    },
                                                    children: agentIcons[conv.agentType] || '💬'
                                                }, void 0, false, {
                                                    fileName: "[project]/src/components/ConversationHistory.tsx",
                                                    lineNumber: 269,
                                                    columnNumber: 21
                                                }, this),
                                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                                    style: {
                                                        flex: 1
                                                    },
                                                    children: [
                                                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                                            style: {
                                                                fontSize: '13px',
                                                                fontWeight: 500,
                                                                color: currentThreadId === conv.threadId ? 'white' : '#1e293b',
                                                                marginBottom: '2px',
                                                                overflow: 'hidden',
                                                                textOverflow: 'ellipsis',
                                                                whiteSpace: 'nowrap'
                                                            },
                                                            children: conv.title || 'New Conversation'
                                                        }, void 0, false, {
                                                            fileName: "[project]/src/components/ConversationHistory.tsx",
                                                            lineNumber: 276,
                                                            columnNumber: 23
                                                        }, this),
                                                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                                            style: {
                                                                fontSize: '11px',
                                                                color: currentThreadId === conv.threadId ? 'rgba(255,255,255,0.8)' : '#64748b'
                                                            },
                                                            children: __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$utils$2f$conversationStorage$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["conversationStorage"].formatDate(conv.lastUpdatedAt)
                                                        }, void 0, false, {
                                                            fileName: "[project]/src/components/ConversationHistory.tsx",
                                                            lineNumber: 287,
                                                            columnNumber: 23
                                                        }, this)
                                                    ]
                                                }, void 0, true, {
                                                    fileName: "[project]/src/components/ConversationHistory.tsx",
                                                    lineNumber: 275,
                                                    columnNumber: 21
                                                }, this)
                                            ]
                                        }, void 0, true, {
                                            fileName: "[project]/src/components/ConversationHistory.tsx",
                                            lineNumber: 263,
                                            columnNumber: 19
                                        }, this),
                                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                                            onClick: (e)=>handleDelete(e, conv.threadId),
                                            className: "delete-btn",
                                            style: {
                                                padding: '2px 6px',
                                                fontSize: '12px',
                                                color: currentThreadId === conv.threadId ? 'rgba(255,255,255,0.9)' : '#6b7280',
                                                background: currentThreadId === conv.threadId ? 'rgba(255,255,255,0.15)' : 'rgba(239, 68, 68, 0.05)',
                                                border: currentThreadId === conv.threadId ? '1px solid rgba(255,255,255,0.2)' : '1px solid rgba(239, 68, 68, 0.1)',
                                                cursor: 'pointer',
                                                opacity: 0.7,
                                                transition: 'all 0.2s',
                                                borderRadius: '6px',
                                                fontWeight: '500'
                                            },
                                            onMouseEnter: (e)=>{
                                                e.currentTarget.style.opacity = '1';
                                                e.currentTarget.style.background = currentThreadId === conv.threadId ? 'rgba(255,255,255,0.25)' : 'rgba(239, 68, 68, 0.15)';
                                                e.currentTarget.style.color = currentThreadId === conv.threadId ? 'white' : '#dc2626';
                                                e.currentTarget.style.borderColor = currentThreadId === conv.threadId ? 'rgba(255,255,255,0.3)' : 'rgba(239, 68, 68, 0.3)';
                                            },
                                            onMouseLeave: (e)=>{
                                                e.currentTarget.style.opacity = '0.7';
                                                e.currentTarget.style.background = currentThreadId === conv.threadId ? 'rgba(255,255,255,0.15)' : 'rgba(239, 68, 68, 0.05)';
                                                e.currentTarget.style.color = currentThreadId === conv.threadId ? 'rgba(255,255,255,0.9)' : '#6b7280';
                                                e.currentTarget.style.borderColor = currentThreadId === conv.threadId ? 'rgba(255,255,255,0.2)' : 'rgba(239, 68, 68, 0.1)';
                                            },
                                            title: "Delete conversation",
                                            children: "✕"
                                        }, void 0, false, {
                                            fileName: "[project]/src/components/ConversationHistory.tsx",
                                            lineNumber: 295,
                                            columnNumber: 19
                                        }, this)
                                    ]
                                }, void 0, true, {
                                    fileName: "[project]/src/components/ConversationHistory.tsx",
                                    lineNumber: 257,
                                    columnNumber: 17
                                }, this),
                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                    style: {
                                        fontSize: '11px',
                                        color: currentThreadId === conv.threadId ? 'rgba(255,255,255,0.9)' : '#94a3b8',
                                        display: 'flex',
                                        alignItems: 'center',
                                        gap: '8px',
                                        flexWrap: 'wrap'
                                    },
                                    children: [
                                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                            children: [
                                                conv.messages.length,
                                                " messages"
                                            ]
                                        }, void 0, true, {
                                            fileName: "[project]/src/components/ConversationHistory.tsx",
                                            lineNumber: 351,
                                            columnNumber: 19
                                        }, this),
                                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                            children: "•"
                                        }, void 0, false, {
                                            fileName: "[project]/src/components/ConversationHistory.tsx",
                                            lineNumber: 352,
                                            columnNumber: 19
                                        }, this),
                                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                            children: conv.agentType.split('-').map((w)=>w[0].toUpperCase() + w.slice(1)).join(' ')
                                        }, void 0, false, {
                                            fileName: "[project]/src/components/ConversationHistory.tsx",
                                            lineNumber: 353,
                                            columnNumber: 19
                                        }, this),
                                        conv.currentSection && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["Fragment"], {
                                            children: [
                                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                                    children: "•"
                                                }, void 0, false, {
                                                    fileName: "[project]/src/components/ConversationHistory.tsx",
                                                    lineNumber: 356,
                                                    columnNumber: 23
                                                }, this),
                                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                                    style: {
                                                        backgroundColor: currentThreadId === conv.threadId ? 'rgba(255,255,255,0.2)' : '#f3f4f6',
                                                        color: currentThreadId === conv.threadId ? 'white' : '#6b7280',
                                                        padding: '2px 6px',
                                                        borderRadius: '4px',
                                                        fontSize: '10px',
                                                        fontWeight: '600',
                                                        border: currentThreadId === conv.threadId ? '1px solid rgba(255,255,255,0.3)' : '1px solid #e5e7eb'
                                                    },
                                                    children: [
                                                        "📍 ",
                                                        conv.currentSection.name
                                                    ]
                                                }, void 0, true, {
                                                    fileName: "[project]/src/components/ConversationHistory.tsx",
                                                    lineNumber: 357,
                                                    columnNumber: 23
                                                }, this)
                                            ]
                                        }, void 0, true)
                                    ]
                                }, void 0, true, {
                                    fileName: "[project]/src/components/ConversationHistory.tsx",
                                    lineNumber: 343,
                                    columnNumber: 17
                                }, this)
                            ]
                        }, conv.threadId, true, {
                            fileName: "[project]/src/components/ConversationHistory.tsx",
                            lineNumber: 225,
                            columnNumber: 15
                        }, this))
                }, void 0, false, {
                    fileName: "[project]/src/components/ConversationHistory.tsx",
                    lineNumber: 219,
                    columnNumber: 11
                }, this)
            }, void 0, false, {
                fileName: "[project]/src/components/ConversationHistory.tsx",
                lineNumber: 202,
                columnNumber: 7
            }, this)
        ]
    }, void 0, true, {
        fileName: "[project]/src/components/ConversationHistory.tsx",
        lineNumber: 69,
        columnNumber: 5
    }, this);
}
_s(ConversationHistory, "vCwnHRy/sMHa8dn/+6fQzMot4qw=");
_c = ConversationHistory;
var _c;
__turbopack_context__.k.register(_c, "ConversationHistory");
if (typeof globalThis.$RefreshHelpers$ === 'object' && globalThis.$RefreshHelpers !== null) {
    __turbopack_context__.k.registerExports(module, globalThis.$RefreshHelpers$);
}
}}),
"[project]/src/components/SectionDisplayPanel.tsx [app-client] (ecmascript)": ((__turbopack_context__) => {
"use strict";

var { k: __turbopack_refresh__, m: module } = __turbopack_context__;
{
__turbopack_context__.s({
    "default": ()=>SectionDisplayPanel
});
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/next/dist/compiled/react/jsx-dev-runtime.js [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$styled$2d$jsx$2f$style$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/styled-jsx/style.js [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/next/dist/compiled/react/index.js [app-client] (ecmascript)");
;
var _s = __turbopack_context__.k.signature();
'use client';
;
;
const SECTION_DISPLAY_NAMES = {
    // Value Canvas sections
    45: 'Initial Interview',
    46: 'Ideal Customer Persona (ICP)',
    47: 'ICP Stress Test',
    48: 'The Pain',
    49: 'The Deep Fear',
    50: 'The Payoffs',
    51: 'Pain-Payoff Symmetry',
    52: 'Signature Method',
    53: 'The Mistakes',
    54: 'The Prize',
    // Concept Pitch sections
    9001: 'Summary Confirmation',
    9002: 'Pitch Generation',
    9003: 'Pitch Selection',
    9004: 'Refinement'
};
const REFINE_STYLES = {
    'concise': 'Make the content more concise and to the point',
    'detailed': 'Add more details and explanations to make it comprehensive',
    'professional': 'Rewrite in a more professional and formal tone',
    'engaging': 'Make it more engaging and compelling for the reader',
    'simple': 'Simplify the language to make it easier to understand'
};
function SectionDisplayPanel(param) {
    let { userId, selectedAgent, currentSection, threadId } = param;
    _s();
    const [sections, setSections] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useState"])([]);
    const [loading, setLoading] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useState"])(false);
    const [error, setError] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useState"])(null);
    const [selectedSectionId, setSelectedSectionId] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useState"])(null);
    const [sectionContent, setSectionContent] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useState"])(null);
    const [loadingContent, setLoadingContent] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useState"])(false);
    const [showRefineModal, setShowRefineModal] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useState"])(false);
    const [refineLoading, setRefineLoading] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useState"])(false);
    const [refinedContent, setRefinedContent] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useState"])(null);
    const [selectedStyle, setSelectedStyle] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useState"])('');
    (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useEffect"])({
        "SectionDisplayPanel.useEffect": ()=>{
            if (userId && (selectedAgent === 'value-canvas' || selectedAgent === 'concept-pitch')) {
                fetchSections();
            }
        // eslint-disable-next-line react-hooks/exhaustive-deps
        }
    }["SectionDisplayPanel.useEffect"], [
        userId,
        selectedAgent,
        currentSection
    ]);
    const fetchSections = async ()=>{
        setLoading(true);
        setError(null);
        try {
            var _data_data;
            // For Concept Pitch, use mock sections since they're not in DentApp yet
            if (selectedAgent === 'concept-pitch') {
                const mockSections = [
                    {
                        section_id: 9001,
                        section_name: 'Summary Confirmation',
                        is_completed: false,
                        has_content: false,
                        current_version: 1,
                        ai_interaction_count: 0
                    },
                    {
                        section_id: 9002,
                        section_name: 'Pitch Generation',
                        is_completed: false,
                        has_content: false,
                        current_version: 1,
                        ai_interaction_count: 0
                    },
                    {
                        section_id: 9003,
                        section_name: 'Pitch Selection',
                        is_completed: false,
                        has_content: false,
                        current_version: 1,
                        ai_interaction_count: 0
                    },
                    {
                        section_id: 9004,
                        section_name: 'Refinement',
                        is_completed: false,
                        has_content: false,
                        current_version: 1,
                        ai_interaction_count: 0
                    }
                ];
                setSections(mockSections);
                setLoading(false);
                return;
            }
            // For Value Canvas, fetch from DentApp API
            const response = await fetch('/api/sections', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    userId: userId,
                    action: 'get-all-sections'
                })
            });
            if (!response.ok) {
                throw new Error('Failed to fetch sections');
            }
            const data = await response.json();
            if (data.success && ((_data_data = data.data) === null || _data_data === void 0 ? void 0 : _data_data.sections)) {
                setSections(data.data.sections);
            } else {
                throw new Error(data.message || 'Invalid response format');
            }
        } catch (err) {
            setError(err instanceof Error ? err.message : 'Unknown error');
            console.error('Error fetching sections:', err);
        } finally{
            setLoading(false);
        }
    };
    const fetchSectionContent = async (sectionId)=>{
        setLoadingContent(true);
        setSectionContent(null);
        try {
            // For Concept Pitch, show placeholder message (no DentApp integration yet)
            if (selectedAgent === 'concept-pitch') {
                setSectionContent({
                    content: {
                        text: 'Concept Pitch sections are currently in development.\n\nSection content will be available once DentApp API integration is complete.'
                    },
                    is_completed: false,
                    current_version: 1,
                    created_at: new Date().toISOString(),
                    updated_at: new Date().toISOString()
                });
                setLoadingContent(false);
                return;
            }
            // For Value Canvas, fetch from DentApp API
            const response = await fetch('/api/sections', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    userId: userId,
                    action: 'get-section-content',
                    sectionId: sectionId
                })
            });
            if (!response.ok) {
                throw new Error('Failed to fetch section content');
            }
            const data = await response.json();
            if (data.success && data.data) {
                setSectionContent(data.data);
            }
        } catch (err) {
            console.error('Error fetching section content:', err);
            setError('Failed to load section content');
        } finally{
            setLoadingContent(false);
        }
    };
    const handleSectionChange = (sectionId)=>{
        const id = parseInt(sectionId);
        setSelectedSectionId(id);
        if (id) {
            fetchSectionContent(id);
        }
    };
    const getSelectedSection = ()=>{
        return sections.find((s)=>s.section_id === selectedSectionId);
    };
    const handleRefineClick = ()=>{
        setShowRefineModal(true);
        setRefinedContent(null);
        setSelectedStyle('');
    };
    const handleRefineExecute = async ()=>{
        if (!selectedStyle || !selectedSectionId || !threadId) {
            alert('Please select a refine style and ensure you have an active conversation');
            return;
        }
        setRefineLoading(true);
        try {
            var _data_data;
            const response = await fetch('/api/sections', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    userId: userId,
                    threadId: threadId,
                    action: 'refine-section',
                    sectionId: selectedSectionId,
                    refinementPrompt: REFINE_STYLES[selectedStyle]
                })
            });
            if (!response.ok) {
                throw new Error('Failed to refine section');
            }
            const data = await response.json();
            if (data.success && ((_data_data = data.data) === null || _data_data === void 0 ? void 0 : _data_data.refined_content)) {
                setRefinedContent(data.data.refined_content.text);
            } else {
                throw new Error(data.message || 'Invalid response format');
            }
        } catch (err) {
            console.error('Error refining section:', err);
            alert('Failed to refine section: ' + (err instanceof Error ? err.message : 'Unknown error'));
        } finally{
            setRefineLoading(false);
        }
    };
    const handleReplaceContent = async ()=>{
        if (!refinedContent || !selectedSectionId || !threadId) return;
        try {
            // 1. Update database
            const updateResponse = await fetch('/api/sections', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    userId: userId,
                    action: 'update-section-content',
                    sectionId: selectedSectionId,
                    content: refinedContent
                })
            });
            if (!updateResponse.ok) {
                throw new Error('Failed to update section in database');
            }
            // 2. Sync LangGraph state
            const syncResponse = await fetch('/api/sections', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    userId: userId,
                    threadId: threadId,
                    action: 'sync-section',
                    sectionId: selectedSectionId
                })
            });
            if (!syncResponse.ok) {
                throw new Error('Failed to sync LangGraph state');
            }
            // 3. Refresh displayed content
            await fetchSectionContent(selectedSectionId);
            setShowRefineModal(false);
            setRefinedContent(null);
            setSelectedStyle('');
        } catch (err) {
            console.error('Error replacing content:', err);
            alert('Failed to replace content: ' + (err instanceof Error ? err.message : 'Unknown error'));
        }
    };
    if (selectedAgent !== 'value-canvas' && selectedAgent !== 'concept-pitch') {
        return null;
    }
    const selectedSection = getSelectedSection();
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
        style: {
            width: '500px',
            height: '100vh',
            backgroundColor: 'white',
            borderLeft: '1px solid #e2e8f0',
            display: 'flex',
            flexDirection: 'column',
            overflow: 'hidden'
        },
        className: "jsx-a18a11d9e8e85108",
        children: [
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                style: {
                    padding: '16px 20px',
                    borderBottom: '1px solid #e2e8f0',
                    backgroundColor: '#ffffff'
                },
                className: "jsx-a18a11d9e8e85108",
                children: [
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                        style: {
                            marginBottom: '16px'
                        },
                        className: "jsx-a18a11d9e8e85108",
                        children: [
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("h2", {
                                style: {
                                    fontSize: '18px',
                                    fontWeight: '700',
                                    color: '#1e293b',
                                    margin: '0 0 4px 0'
                                },
                                className: "jsx-a18a11d9e8e85108",
                                children: "📄 Section Viewer"
                            }, void 0, false, {
                                fileName: "[project]/src/components/SectionDisplayPanel.tsx",
                                lineNumber: 292,
                                columnNumber: 11
                            }, this),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                                style: {
                                    fontSize: '12px',
                                    color: '#64748b',
                                    margin: 0
                                },
                                className: "jsx-a18a11d9e8e85108",
                                children: [
                                    "User #",
                                    userId
                                ]
                            }, void 0, true, {
                                fileName: "[project]/src/components/SectionDisplayPanel.tsx",
                                lineNumber: 300,
                                columnNumber: 11
                            }, this)
                        ]
                    }, void 0, true, {
                        fileName: "[project]/src/components/SectionDisplayPanel.tsx",
                        lineNumber: 291,
                        columnNumber: 9
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                        style: {
                            display: 'flex',
                            gap: '8px'
                        },
                        className: "jsx-a18a11d9e8e85108",
                        children: [
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("select", {
                                value: selectedSectionId || '',
                                onChange: (e)=>handleSectionChange(e.target.value),
                                disabled: loading || sections.length === 0,
                                style: {
                                    flex: 1,
                                    padding: '10px 12px',
                                    border: '2px solid #e2e8f0',
                                    borderRadius: '8px',
                                    fontSize: '13px',
                                    fontWeight: '500',
                                    color: '#1e293b',
                                    backgroundColor: 'white',
                                    cursor: 'pointer',
                                    outline: 'none',
                                    transition: 'all 0.2s ease'
                                },
                                onFocus: (e)=>e.currentTarget.style.borderColor = '#6366f1',
                                onBlur: (e)=>e.currentTarget.style.borderColor = '#e2e8f0',
                                className: "jsx-a18a11d9e8e85108",
                                children: [
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("option", {
                                        value: "",
                                        className: "jsx-a18a11d9e8e85108",
                                        children: "Select a section to view"
                                    }, void 0, false, {
                                        fileName: "[project]/src/components/SectionDisplayPanel.tsx",
                                        lineNumber: 331,
                                        columnNumber: 13
                                    }, this),
                                    sections.map((section)=>/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("option", {
                                            value: section.section_id,
                                            className: "jsx-a18a11d9e8e85108",
                                            children: [
                                                "#",
                                                section.section_id,
                                                " - ",
                                                SECTION_DISPLAY_NAMES[section.section_id],
                                                section.is_completed ? ' ✓' : '',
                                                "(v",
                                                section.current_version,
                                                ")"
                                            ]
                                        }, section.section_id, true, {
                                            fileName: "[project]/src/components/SectionDisplayPanel.tsx",
                                            lineNumber: 333,
                                            columnNumber: 15
                                        }, this))
                                ]
                            }, void 0, true, {
                                fileName: "[project]/src/components/SectionDisplayPanel.tsx",
                                lineNumber: 311,
                                columnNumber: 11
                            }, this),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                                onClick: fetchSections,
                                disabled: loading,
                                style: {
                                    padding: '10px 14px',
                                    backgroundColor: loading ? '#e2e8f0' : '#6366f1',
                                    color: loading ? '#94a3b8' : 'white',
                                    border: 'none',
                                    borderRadius: '8px',
                                    fontSize: '16px',
                                    cursor: loading ? 'not-allowed' : 'pointer',
                                    transition: 'all 0.2s ease'
                                },
                                onMouseEnter: (e)=>!loading && (e.currentTarget.style.backgroundColor = '#4f46e5'),
                                onMouseLeave: (e)=>!loading && (e.currentTarget.style.backgroundColor = '#6366f1'),
                                title: "Refresh sections",
                                className: "jsx-a18a11d9e8e85108",
                                children: "🔄"
                            }, void 0, false, {
                                fileName: "[project]/src/components/SectionDisplayPanel.tsx",
                                lineNumber: 341,
                                columnNumber: 11
                            }, this)
                        ]
                    }, void 0, true, {
                        fileName: "[project]/src/components/SectionDisplayPanel.tsx",
                        lineNumber: 310,
                        columnNumber: 9
                    }, this)
                ]
            }, void 0, true, {
                fileName: "[project]/src/components/SectionDisplayPanel.tsx",
                lineNumber: 286,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                style: {
                    flex: 1,
                    overflowY: 'auto',
                    backgroundColor: '#f8fafc'
                },
                className: "jsx-a18a11d9e8e85108",
                children: [
                    error && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                        style: {
                            margin: '20px',
                            padding: '16px',
                            backgroundColor: '#fee2e2',
                            borderRadius: '8px',
                            fontSize: '13px',
                            color: '#991b1b',
                            border: '1px solid #fecaca'
                        },
                        className: "jsx-a18a11d9e8e85108",
                        children: [
                            "❌ ",
                            error
                        ]
                    }, void 0, true, {
                        fileName: "[project]/src/components/SectionDisplayPanel.tsx",
                        lineNumber: 370,
                        columnNumber: 11
                    }, this),
                    loading && sections.length === 0 ? /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                        style: {
                            display: 'flex',
                            flexDirection: 'column',
                            alignItems: 'center',
                            justifyContent: 'center',
                            padding: '60px 20px',
                            color: '#64748b'
                        },
                        className: "jsx-a18a11d9e8e85108",
                        children: [
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                style: {
                                    width: '40px',
                                    height: '40px',
                                    border: '3px solid #e2e8f0',
                                    borderTop: '3px solid #6366f1',
                                    borderRadius: '50%',
                                    animation: 'spin 1s linear infinite',
                                    marginBottom: '16px'
                                },
                                className: "jsx-a18a11d9e8e85108"
                            }, void 0, false, {
                                fileName: "[project]/src/components/SectionDisplayPanel.tsx",
                                lineNumber: 392,
                                columnNumber: 13
                            }, this),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                                style: {
                                    fontSize: '13px',
                                    margin: 0
                                },
                                className: "jsx-a18a11d9e8e85108",
                                children: "Loading sections..."
                            }, void 0, false, {
                                fileName: "[project]/src/components/SectionDisplayPanel.tsx",
                                lineNumber: 401,
                                columnNumber: 13
                            }, this)
                        ]
                    }, void 0, true, {
                        fileName: "[project]/src/components/SectionDisplayPanel.tsx",
                        lineNumber: 384,
                        columnNumber: 11
                    }, this) : !selectedSectionId ? /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                        style: {
                            display: 'flex',
                            flexDirection: 'column',
                            alignItems: 'center',
                            justifyContent: 'center',
                            padding: '60px 20px',
                            color: '#94a3b8',
                            textAlign: 'center'
                        },
                        className: "jsx-a18a11d9e8e85108",
                        children: [
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                style: {
                                    fontSize: '48px',
                                    marginBottom: '16px'
                                },
                                className: "jsx-a18a11d9e8e85108",
                                children: "📋"
                            }, void 0, false, {
                                fileName: "[project]/src/components/SectionDisplayPanel.tsx",
                                lineNumber: 413,
                                columnNumber: 13
                            }, this),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                                style: {
                                    fontSize: '14px',
                                    fontWeight: '500',
                                    color: '#64748b',
                                    margin: '0 0 8px 0'
                                },
                                className: "jsx-a18a11d9e8e85108",
                                children: "Select a section to view"
                            }, void 0, false, {
                                fileName: "[project]/src/components/SectionDisplayPanel.tsx",
                                lineNumber: 414,
                                columnNumber: 13
                            }, this),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                                style: {
                                    fontSize: '12px',
                                    margin: 0
                                },
                                className: "jsx-a18a11d9e8e85108",
                                children: "Choose from the dropdown above to see section content"
                            }, void 0, false, {
                                fileName: "[project]/src/components/SectionDisplayPanel.tsx",
                                lineNumber: 417,
                                columnNumber: 13
                            }, this)
                        ]
                    }, void 0, true, {
                        fileName: "[project]/src/components/SectionDisplayPanel.tsx",
                        lineNumber: 404,
                        columnNumber: 11
                    }, this) : loadingContent ? /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                        style: {
                            display: 'flex',
                            flexDirection: 'column',
                            alignItems: 'center',
                            justifyContent: 'center',
                            padding: '60px 20px',
                            color: '#64748b'
                        },
                        className: "jsx-a18a11d9e8e85108",
                        children: [
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                style: {
                                    width: '40px',
                                    height: '40px',
                                    border: '3px solid #e2e8f0',
                                    borderTop: '3px solid #6366f1',
                                    borderRadius: '50%',
                                    animation: 'spin 1s linear infinite',
                                    marginBottom: '16px'
                                },
                                className: "jsx-a18a11d9e8e85108"
                            }, void 0, false, {
                                fileName: "[project]/src/components/SectionDisplayPanel.tsx",
                                lineNumber: 430,
                                columnNumber: 13
                            }, this),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                                style: {
                                    fontSize: '13px',
                                    margin: 0
                                },
                                className: "jsx-a18a11d9e8e85108",
                                children: "Loading content..."
                            }, void 0, false, {
                                fileName: "[project]/src/components/SectionDisplayPanel.tsx",
                                lineNumber: 439,
                                columnNumber: 13
                            }, this)
                        ]
                    }, void 0, true, {
                        fileName: "[project]/src/components/SectionDisplayPanel.tsx",
                        lineNumber: 422,
                        columnNumber: 11
                    }, this) : sectionContent ? /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                        style: {
                            padding: '20px'
                        },
                        className: "jsx-a18a11d9e8e85108",
                        children: [
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                style: {
                                    backgroundColor: 'white',
                                    borderRadius: '12px',
                                    padding: '16px',
                                    marginBottom: '16px',
                                    border: '1px solid #e2e8f0',
                                    boxShadow: '0 1px 3px rgba(0,0,0,0.05)'
                                },
                                className: "jsx-a18a11d9e8e85108",
                                children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                    style: {
                                        display: 'flex',
                                        alignItems: 'flex-start',
                                        gap: '12px',
                                        marginBottom: '12px'
                                    },
                                    className: "jsx-a18a11d9e8e85108",
                                    children: [
                                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                            style: {
                                                width: '40px',
                                                height: '40px',
                                                borderRadius: '8px',
                                                backgroundColor: (selectedSection === null || selectedSection === void 0 ? void 0 : selectedSection.is_completed) ? '#dcfce7' : '#f1f5f9',
                                                display: 'flex',
                                                alignItems: 'center',
                                                justifyContent: 'center',
                                                fontSize: '20px',
                                                flexShrink: 0
                                            },
                                            className: "jsx-a18a11d9e8e85108",
                                            children: (selectedSection === null || selectedSection === void 0 ? void 0 : selectedSection.is_completed) ? '✓' : '📝'
                                        }, void 0, false, {
                                            fileName: "[project]/src/components/SectionDisplayPanel.tsx",
                                            lineNumber: 453,
                                            columnNumber: 17
                                        }, this),
                                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                            style: {
                                                flex: 1
                                            },
                                            className: "jsx-a18a11d9e8e85108",
                                            children: [
                                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("h3", {
                                                    style: {
                                                        fontSize: '15px',
                                                        fontWeight: '700',
                                                        color: '#1e293b',
                                                        margin: '0 0 4px 0'
                                                    },
                                                    className: "jsx-a18a11d9e8e85108",
                                                    children: selectedSection && SECTION_DISPLAY_NAMES[selectedSection.section_id]
                                                }, void 0, false, {
                                                    fileName: "[project]/src/components/SectionDisplayPanel.tsx",
                                                    lineNumber: 467,
                                                    columnNumber: 19
                                                }, this),
                                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                                    style: {
                                                        fontSize: '11px',
                                                        color: '#64748b',
                                                        display: 'flex',
                                                        gap: '12px',
                                                        flexWrap: 'wrap'
                                                    },
                                                    className: "jsx-a18a11d9e8e85108",
                                                    children: [
                                                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                                            style: {
                                                                backgroundColor: '#f1f5f9',
                                                                padding: '2px 8px',
                                                                borderRadius: '4px',
                                                                fontWeight: '500'
                                                            },
                                                            className: "jsx-a18a11d9e8e85108",
                                                            children: [
                                                                "Section #",
                                                                selectedSectionId
                                                            ]
                                                        }, void 0, true, {
                                                            fileName: "[project]/src/components/SectionDisplayPanel.tsx",
                                                            lineNumber: 482,
                                                            columnNumber: 21
                                                        }, this),
                                                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                                            className: "jsx-a18a11d9e8e85108",
                                                            children: [
                                                                "Version ",
                                                                sectionContent.current_version
                                                            ]
                                                        }, void 0, true, {
                                                            fileName: "[project]/src/components/SectionDisplayPanel.tsx",
                                                            lineNumber: 490,
                                                            columnNumber: 21
                                                        }, this),
                                                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                                            className: "jsx-a18a11d9e8e85108",
                                                            children: "•"
                                                        }, void 0, false, {
                                                            fileName: "[project]/src/components/SectionDisplayPanel.tsx",
                                                            lineNumber: 491,
                                                            columnNumber: 21
                                                        }, this),
                                                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                                            className: "jsx-a18a11d9e8e85108",
                                                            children: [
                                                                (selectedSection === null || selectedSection === void 0 ? void 0 : selectedSection.ai_interaction_count) || 0,
                                                                " interactions"
                                                            ]
                                                        }, void 0, true, {
                                                            fileName: "[project]/src/components/SectionDisplayPanel.tsx",
                                                            lineNumber: 492,
                                                            columnNumber: 21
                                                        }, this)
                                                    ]
                                                }, void 0, true, {
                                                    fileName: "[project]/src/components/SectionDisplayPanel.tsx",
                                                    lineNumber: 475,
                                                    columnNumber: 19
                                                }, this)
                                            ]
                                        }, void 0, true, {
                                            fileName: "[project]/src/components/SectionDisplayPanel.tsx",
                                            lineNumber: 466,
                                            columnNumber: 17
                                        }, this),
                                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                            style: {
                                                padding: '4px 10px',
                                                borderRadius: '12px',
                                                backgroundColor: (selectedSection === null || selectedSection === void 0 ? void 0 : selectedSection.is_completed) ? '#dcfce7' : '#fef3c7',
                                                color: (selectedSection === null || selectedSection === void 0 ? void 0 : selectedSection.is_completed) ? '#166534' : '#92400e',
                                                fontSize: '11px',
                                                fontWeight: '600'
                                            },
                                            className: "jsx-a18a11d9e8e85108",
                                            children: (selectedSection === null || selectedSection === void 0 ? void 0 : selectedSection.is_completed) ? 'Completed' : 'In Progress'
                                        }, void 0, false, {
                                            fileName: "[project]/src/components/SectionDisplayPanel.tsx",
                                            lineNumber: 495,
                                            columnNumber: 17
                                        }, this)
                                    ]
                                }, void 0, true, {
                                    fileName: "[project]/src/components/SectionDisplayPanel.tsx",
                                    lineNumber: 452,
                                    columnNumber: 15
                                }, this)
                            }, void 0, false, {
                                fileName: "[project]/src/components/SectionDisplayPanel.tsx",
                                lineNumber: 444,
                                columnNumber: 13
                            }, this),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                style: {
                                    backgroundColor: 'white',
                                    borderRadius: '12px',
                                    padding: '20px',
                                    border: '1px solid #e2e8f0',
                                    boxShadow: '0 1px 3px rgba(0,0,0,0.05)'
                                },
                                className: "jsx-a18a11d9e8e85108",
                                children: [
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                        style: {
                                            display: 'flex',
                                            justifyContent: 'space-between',
                                            alignItems: 'center',
                                            marginBottom: '12px'
                                        },
                                        className: "jsx-a18a11d9e8e85108",
                                        children: [
                                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                                style: {
                                                    fontSize: '12px',
                                                    fontWeight: '600',
                                                    color: '#64748b',
                                                    textTransform: 'uppercase',
                                                    letterSpacing: '0.5px'
                                                },
                                                className: "jsx-a18a11d9e8e85108",
                                                children: "Content"
                                            }, void 0, false, {
                                                fileName: "[project]/src/components/SectionDisplayPanel.tsx",
                                                lineNumber: 522,
                                                columnNumber: 17
                                            }, this),
                                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                                                onClick: handleRefineClick,
                                                disabled: !threadId || !(sectionContent === null || sectionContent === void 0 ? void 0 : sectionContent.content.text),
                                                style: {
                                                    padding: '6px 12px',
                                                    backgroundColor: !threadId || !(sectionContent === null || sectionContent === void 0 ? void 0 : sectionContent.content.text) ? '#e2e8f0' : '#8b5cf6',
                                                    color: !threadId || !(sectionContent === null || sectionContent === void 0 ? void 0 : sectionContent.content.text) ? '#94a3b8' : 'white',
                                                    border: 'none',
                                                    borderRadius: '6px',
                                                    fontSize: '12px',
                                                    fontWeight: '600',
                                                    cursor: !threadId || !(sectionContent === null || sectionContent === void 0 ? void 0 : sectionContent.content.text) ? 'not-allowed' : 'pointer',
                                                    display: 'flex',
                                                    alignItems: 'center',
                                                    gap: '4px',
                                                    transition: 'all 0.2s ease'
                                                },
                                                onMouseEnter: (e)=>{
                                                    if (threadId && (sectionContent === null || sectionContent === void 0 ? void 0 : sectionContent.content.text)) {
                                                        e.currentTarget.style.backgroundColor = '#7c3aed';
                                                    }
                                                },
                                                onMouseLeave: (e)=>{
                                                    if (threadId && (sectionContent === null || sectionContent === void 0 ? void 0 : sectionContent.content.text)) {
                                                        e.currentTarget.style.backgroundColor = '#8b5cf6';
                                                    }
                                                },
                                                title: !threadId ? 'Active conversation required' : 'Refine this section with AI',
                                                className: "jsx-a18a11d9e8e85108",
                                                children: "✨ Refine"
                                            }, void 0, false, {
                                                fileName: "[project]/src/components/SectionDisplayPanel.tsx",
                                                lineNumber: 531,
                                                columnNumber: 17
                                            }, this)
                                        ]
                                    }, void 0, true, {
                                        fileName: "[project]/src/components/SectionDisplayPanel.tsx",
                                        lineNumber: 516,
                                        columnNumber: 15
                                    }, this),
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                        style: {
                                            fontSize: '13px',
                                            lineHeight: '1.7',
                                            color: '#1e293b',
                                            whiteSpace: 'pre-wrap',
                                            backgroundColor: '#f8fafc',
                                            padding: '16px',
                                            borderRadius: '8px',
                                            border: '1px solid #e2e8f0',
                                            minHeight: '200px',
                                            maxHeight: '500px',
                                            overflowY: 'auto'
                                        },
                                        className: "jsx-a18a11d9e8e85108",
                                        children: sectionContent.content.text || /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                            style: {
                                                color: '#94a3b8',
                                                fontStyle: 'italic'
                                            },
                                            className: "jsx-a18a11d9e8e85108",
                                            children: "No content available for this section"
                                        }, void 0, false, {
                                            fileName: "[project]/src/components/SectionDisplayPanel.tsx",
                                            lineNumber: 577,
                                            columnNumber: 19
                                        }, this)
                                    }, void 0, false, {
                                        fileName: "[project]/src/components/SectionDisplayPanel.tsx",
                                        lineNumber: 563,
                                        columnNumber: 15
                                    }, this),
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                        style: {
                                            marginTop: '16px',
                                            paddingTop: '16px',
                                            borderTop: '1px solid #e2e8f0',
                                            display: 'flex',
                                            gap: '16px',
                                            flexWrap: 'wrap',
                                            fontSize: '11px',
                                            color: '#64748b'
                                        },
                                        className: "jsx-a18a11d9e8e85108",
                                        children: [
                                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                                className: "jsx-a18a11d9e8e85108",
                                                children: [
                                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                                        style: {
                                                            fontWeight: '600'
                                                        },
                                                        className: "jsx-a18a11d9e8e85108",
                                                        children: "Created:"
                                                    }, void 0, false, {
                                                        fileName: "[project]/src/components/SectionDisplayPanel.tsx",
                                                        lineNumber: 595,
                                                        columnNumber: 19
                                                    }, this),
                                                    ' ',
                                                    new Date(sectionContent.created_at).toLocaleString()
                                                ]
                                            }, void 0, true, {
                                                fileName: "[project]/src/components/SectionDisplayPanel.tsx",
                                                lineNumber: 594,
                                                columnNumber: 17
                                            }, this),
                                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                                className: "jsx-a18a11d9e8e85108",
                                                children: [
                                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                                        style: {
                                                            fontWeight: '600'
                                                        },
                                                        className: "jsx-a18a11d9e8e85108",
                                                        children: "Updated:"
                                                    }, void 0, false, {
                                                        fileName: "[project]/src/components/SectionDisplayPanel.tsx",
                                                        lineNumber: 599,
                                                        columnNumber: 19
                                                    }, this),
                                                    ' ',
                                                    new Date(sectionContent.updated_at).toLocaleString()
                                                ]
                                            }, void 0, true, {
                                                fileName: "[project]/src/components/SectionDisplayPanel.tsx",
                                                lineNumber: 598,
                                                columnNumber: 17
                                            }, this)
                                        ]
                                    }, void 0, true, {
                                        fileName: "[project]/src/components/SectionDisplayPanel.tsx",
                                        lineNumber: 584,
                                        columnNumber: 15
                                    }, this)
                                ]
                            }, void 0, true, {
                                fileName: "[project]/src/components/SectionDisplayPanel.tsx",
                                lineNumber: 509,
                                columnNumber: 13
                            }, this)
                        ]
                    }, void 0, true, {
                        fileName: "[project]/src/components/SectionDisplayPanel.tsx",
                        lineNumber: 442,
                        columnNumber: 11
                    }, this) : /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                        style: {
                            display: 'flex',
                            flexDirection: 'column',
                            alignItems: 'center',
                            justifyContent: 'center',
                            padding: '60px 20px',
                            color: '#94a3b8',
                            textAlign: 'center'
                        },
                        className: "jsx-a18a11d9e8e85108",
                        children: [
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                style: {
                                    fontSize: '48px',
                                    marginBottom: '16px'
                                },
                                className: "jsx-a18a11d9e8e85108",
                                children: "⚠️"
                            }, void 0, false, {
                                fileName: "[project]/src/components/SectionDisplayPanel.tsx",
                                lineNumber: 615,
                                columnNumber: 13
                            }, this),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                                style: {
                                    fontSize: '14px',
                                    fontWeight: '500',
                                    color: '#64748b',
                                    margin: 0
                                },
                                className: "jsx-a18a11d9e8e85108",
                                children: "Failed to load content"
                            }, void 0, false, {
                                fileName: "[project]/src/components/SectionDisplayPanel.tsx",
                                lineNumber: 616,
                                columnNumber: 13
                            }, this)
                        ]
                    }, void 0, true, {
                        fileName: "[project]/src/components/SectionDisplayPanel.tsx",
                        lineNumber: 606,
                        columnNumber: 11
                    }, this)
                ]
            }, void 0, true, {
                fileName: "[project]/src/components/SectionDisplayPanel.tsx",
                lineNumber: 364,
                columnNumber: 7
            }, this),
            showRefineModal && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["Fragment"], {
                children: [
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                        onClick: ()=>setShowRefineModal(false),
                        style: {
                            position: 'fixed',
                            top: 0,
                            left: 0,
                            right: 0,
                            bottom: 0,
                            backgroundColor: 'rgba(0, 0, 0, 0.5)',
                            zIndex: 1000,
                            animation: 'fadeIn 0.2s ease'
                        },
                        className: "jsx-a18a11d9e8e85108"
                    }, void 0, false, {
                        fileName: "[project]/src/components/SectionDisplayPanel.tsx",
                        lineNumber: 626,
                        columnNumber: 11
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                        style: {
                            position: 'fixed',
                            top: '50%',
                            left: '50%',
                            transform: 'translate(-50%, -50%)',
                            width: '90%',
                            maxWidth: '1000px',
                            maxHeight: '90vh',
                            backgroundColor: 'white',
                            borderRadius: '16px',
                            boxShadow: '0 25px 50px -12px rgba(0, 0, 0, 0.25)',
                            zIndex: 1001,
                            display: 'flex',
                            flexDirection: 'column',
                            overflow: 'hidden',
                            animation: 'slideIn 0.3s ease'
                        },
                        className: "jsx-a18a11d9e8e85108",
                        children: [
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                style: {
                                    padding: '24px',
                                    borderBottom: '1px solid #e2e8f0',
                                    display: 'flex',
                                    justifyContent: 'space-between',
                                    alignItems: 'center'
                                },
                                className: "jsx-a18a11d9e8e85108",
                                children: [
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                        className: "jsx-a18a11d9e8e85108",
                                        children: [
                                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("h3", {
                                                style: {
                                                    fontSize: '20px',
                                                    fontWeight: '700',
                                                    color: '#1e293b',
                                                    margin: '0 0 4px 0'
                                                },
                                                className: "jsx-a18a11d9e8e85108",
                                                children: "✨ Refine Section Content"
                                            }, void 0, false, {
                                                fileName: "[project]/src/components/SectionDisplayPanel.tsx",
                                                lineNumber: 665,
                                                columnNumber: 17
                                            }, this),
                                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                                                style: {
                                                    fontSize: '13px',
                                                    color: '#64748b',
                                                    margin: '0 0 4px 0'
                                                },
                                                className: "jsx-a18a11d9e8e85108",
                                                children: selectedSection && SECTION_DISPLAY_NAMES[selectedSection.section_id]
                                            }, void 0, false, {
                                                fileName: "[project]/src/components/SectionDisplayPanel.tsx",
                                                lineNumber: 673,
                                                columnNumber: 17
                                            }, this),
                                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                                                style: {
                                                    fontSize: '11px',
                                                    color: '#8b5cf6',
                                                    margin: 0,
                                                    fontWeight: '500',
                                                    display: 'flex',
                                                    alignItems: 'center',
                                                    gap: '4px'
                                                },
                                                className: "jsx-a18a11d9e8e85108",
                                                children: [
                                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                                        className: "jsx-a18a11d9e8e85108",
                                                        children: "🔗 Thread:"
                                                    }, void 0, false, {
                                                        fileName: "[project]/src/components/SectionDisplayPanel.tsx",
                                                        lineNumber: 689,
                                                        columnNumber: 19
                                                    }, this),
                                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("code", {
                                                        style: {
                                                            backgroundColor: '#f5f3ff',
                                                            padding: '2px 6px',
                                                            borderRadius: '4px',
                                                            fontSize: '10px',
                                                            fontFamily: 'monospace'
                                                        },
                                                        className: "jsx-a18a11d9e8e85108",
                                                        children: threadId
                                                    }, void 0, false, {
                                                        fileName: "[project]/src/components/SectionDisplayPanel.tsx",
                                                        lineNumber: 690,
                                                        columnNumber: 19
                                                    }, this)
                                                ]
                                            }, void 0, true, {
                                                fileName: "[project]/src/components/SectionDisplayPanel.tsx",
                                                lineNumber: 680,
                                                columnNumber: 17
                                            }, this)
                                        ]
                                    }, void 0, true, {
                                        fileName: "[project]/src/components/SectionDisplayPanel.tsx",
                                        lineNumber: 664,
                                        columnNumber: 15
                                    }, this),
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                                        onClick: ()=>setShowRefineModal(false),
                                        style: {
                                            width: '36px',
                                            height: '36px',
                                            borderRadius: '50%',
                                            backgroundColor: '#f1f5f9',
                                            border: 'none',
                                            color: '#64748b',
                                            fontSize: '20px',
                                            cursor: 'pointer',
                                            display: 'flex',
                                            alignItems: 'center',
                                            justifyContent: 'center',
                                            transition: 'all 0.2s ease'
                                        },
                                        onMouseEnter: (e)=>{
                                            e.currentTarget.style.backgroundColor = '#e2e8f0';
                                            e.currentTarget.style.color = '#1e293b';
                                        },
                                        onMouseLeave: (e)=>{
                                            e.currentTarget.style.backgroundColor = '#f1f5f9';
                                            e.currentTarget.style.color = '#64748b';
                                        },
                                        className: "jsx-a18a11d9e8e85108",
                                        children: "✕"
                                    }, void 0, false, {
                                        fileName: "[project]/src/components/SectionDisplayPanel.tsx",
                                        lineNumber: 701,
                                        columnNumber: 15
                                    }, this)
                                ]
                            }, void 0, true, {
                                fileName: "[project]/src/components/SectionDisplayPanel.tsx",
                                lineNumber: 657,
                                columnNumber: 13
                            }, this),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                style: {
                                    flex: 1,
                                    overflowY: 'auto',
                                    padding: '24px'
                                },
                                className: "jsx-a18a11d9e8e85108",
                                children: [
                                    !refinedContent && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                        style: {
                                            marginBottom: '24px'
                                        },
                                        className: "jsx-a18a11d9e8e85108",
                                        children: [
                                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("label", {
                                                style: {
                                                    display: 'block',
                                                    fontSize: '14px',
                                                    fontWeight: '600',
                                                    color: '#1e293b',
                                                    marginBottom: '8px'
                                                },
                                                className: "jsx-a18a11d9e8e85108",
                                                children: "Select Refine Style"
                                            }, void 0, false, {
                                                fileName: "[project]/src/components/SectionDisplayPanel.tsx",
                                                lineNumber: 739,
                                                columnNumber: 19
                                            }, this),
                                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("select", {
                                                value: selectedStyle,
                                                onChange: (e)=>setSelectedStyle(e.target.value),
                                                disabled: refineLoading,
                                                style: {
                                                    width: '100%',
                                                    padding: '10px 12px',
                                                    border: '2px solid #e2e8f0',
                                                    borderRadius: '8px',
                                                    fontSize: '14px',
                                                    color: '#1e293b',
                                                    backgroundColor: 'white',
                                                    cursor: refineLoading ? 'not-allowed' : 'pointer'
                                                },
                                                className: "jsx-a18a11d9e8e85108",
                                                children: [
                                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("option", {
                                                        value: "",
                                                        className: "jsx-a18a11d9e8e85108",
                                                        children: "Choose a style..."
                                                    }, void 0, false, {
                                                        fileName: "[project]/src/components/SectionDisplayPanel.tsx",
                                                        lineNumber: 763,
                                                        columnNumber: 21
                                                    }, this),
                                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("option", {
                                                        value: "concise",
                                                        className: "jsx-a18a11d9e8e85108",
                                                        children: "✂️ More Concise"
                                                    }, void 0, false, {
                                                        fileName: "[project]/src/components/SectionDisplayPanel.tsx",
                                                        lineNumber: 764,
                                                        columnNumber: 21
                                                    }, this),
                                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("option", {
                                                        value: "detailed",
                                                        className: "jsx-a18a11d9e8e85108",
                                                        children: "📝 More Detailed"
                                                    }, void 0, false, {
                                                        fileName: "[project]/src/components/SectionDisplayPanel.tsx",
                                                        lineNumber: 765,
                                                        columnNumber: 21
                                                    }, this),
                                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("option", {
                                                        value: "professional",
                                                        className: "jsx-a18a11d9e8e85108",
                                                        children: "💼 More Professional"
                                                    }, void 0, false, {
                                                        fileName: "[project]/src/components/SectionDisplayPanel.tsx",
                                                        lineNumber: 766,
                                                        columnNumber: 21
                                                    }, this),
                                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("option", {
                                                        value: "engaging",
                                                        className: "jsx-a18a11d9e8e85108",
                                                        children: "🎯 More Engaging"
                                                    }, void 0, false, {
                                                        fileName: "[project]/src/components/SectionDisplayPanel.tsx",
                                                        lineNumber: 767,
                                                        columnNumber: 21
                                                    }, this),
                                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("option", {
                                                        value: "simple",
                                                        className: "jsx-a18a11d9e8e85108",
                                                        children: "💡 Simpler Language"
                                                    }, void 0, false, {
                                                        fileName: "[project]/src/components/SectionDisplayPanel.tsx",
                                                        lineNumber: 768,
                                                        columnNumber: 21
                                                    }, this)
                                                ]
                                            }, void 0, true, {
                                                fileName: "[project]/src/components/SectionDisplayPanel.tsx",
                                                lineNumber: 748,
                                                columnNumber: 19
                                            }, this),
                                            selectedStyle && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                                                style: {
                                                    marginTop: '8px',
                                                    fontSize: '12px',
                                                    color: '#64748b',
                                                    fontStyle: 'italic'
                                                },
                                                className: "jsx-a18a11d9e8e85108",
                                                children: REFINE_STYLES[selectedStyle]
                                            }, void 0, false, {
                                                fileName: "[project]/src/components/SectionDisplayPanel.tsx",
                                                lineNumber: 771,
                                                columnNumber: 21
                                            }, this)
                                        ]
                                    }, void 0, true, {
                                        fileName: "[project]/src/components/SectionDisplayPanel.tsx",
                                        lineNumber: 738,
                                        columnNumber: 17
                                    }, this),
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                        style: {
                                            marginBottom: refinedContent ? '16px' : '0'
                                        },
                                        className: "jsx-a18a11d9e8e85108",
                                        children: [
                                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                                style: {
                                                    fontSize: '12px',
                                                    fontWeight: '600',
                                                    color: '#64748b',
                                                    marginBottom: '8px',
                                                    textTransform: 'uppercase',
                                                    letterSpacing: '0.5px'
                                                },
                                                className: "jsx-a18a11d9e8e85108",
                                                children: refinedContent ? 'Original Content' : 'Current Content'
                                            }, void 0, false, {
                                                fileName: "[project]/src/components/SectionDisplayPanel.tsx",
                                                lineNumber: 785,
                                                columnNumber: 17
                                            }, this),
                                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                                style: {
                                                    padding: '16px',
                                                    backgroundColor: '#f8fafc',
                                                    borderRadius: '8px',
                                                    border: '1px solid #e2e8f0',
                                                    fontSize: '13px',
                                                    lineHeight: '1.7',
                                                    color: '#1e293b',
                                                    whiteSpace: 'pre-wrap',
                                                    maxHeight: refinedContent ? '300px' : '400px',
                                                    overflowY: 'auto'
                                                },
                                                className: "jsx-a18a11d9e8e85108",
                                                children: (sectionContent === null || sectionContent === void 0 ? void 0 : sectionContent.content.text) || 'No content'
                                            }, void 0, false, {
                                                fileName: "[project]/src/components/SectionDisplayPanel.tsx",
                                                lineNumber: 795,
                                                columnNumber: 17
                                            }, this)
                                        ]
                                    }, void 0, true, {
                                        fileName: "[project]/src/components/SectionDisplayPanel.tsx",
                                        lineNumber: 784,
                                        columnNumber: 15
                                    }, this),
                                    refinedContent && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                        className: "jsx-a18a11d9e8e85108",
                                        children: [
                                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                                style: {
                                                    fontSize: '12px',
                                                    fontWeight: '600',
                                                    color: '#8b5cf6',
                                                    marginBottom: '8px',
                                                    textTransform: 'uppercase',
                                                    letterSpacing: '0.5px'
                                                },
                                                className: "jsx-a18a11d9e8e85108",
                                                children: "✨ Refined Content"
                                            }, void 0, false, {
                                                fileName: "[project]/src/components/SectionDisplayPanel.tsx",
                                                lineNumber: 814,
                                                columnNumber: 19
                                            }, this),
                                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                                style: {
                                                    padding: '16px',
                                                    backgroundColor: '#faf5ff',
                                                    borderRadius: '8px',
                                                    border: '2px solid #8b5cf6',
                                                    fontSize: '13px',
                                                    lineHeight: '1.7',
                                                    color: '#1e293b',
                                                    whiteSpace: 'pre-wrap',
                                                    maxHeight: '300px',
                                                    overflowY: 'auto'
                                                },
                                                className: "jsx-a18a11d9e8e85108",
                                                children: refinedContent
                                            }, void 0, false, {
                                                fileName: "[project]/src/components/SectionDisplayPanel.tsx",
                                                lineNumber: 824,
                                                columnNumber: 19
                                            }, this)
                                        ]
                                    }, void 0, true, {
                                        fileName: "[project]/src/components/SectionDisplayPanel.tsx",
                                        lineNumber: 813,
                                        columnNumber: 17
                                    }, this),
                                    refineLoading && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                        style: {
                                            display: 'flex',
                                            flexDirection: 'column',
                                            alignItems: 'center',
                                            justifyContent: 'center',
                                            padding: '40px',
                                            color: '#64748b'
                                        },
                                        className: "jsx-a18a11d9e8e85108",
                                        children: [
                                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                                style: {
                                                    width: '40px',
                                                    height: '40px',
                                                    border: '3px solid #e2e8f0',
                                                    borderTop: '3px solid #8b5cf6',
                                                    borderRadius: '50%',
                                                    animation: 'spin 1s linear infinite',
                                                    marginBottom: '16px'
                                                },
                                                className: "jsx-a18a11d9e8e85108"
                                            }, void 0, false, {
                                                fileName: "[project]/src/components/SectionDisplayPanel.tsx",
                                                lineNumber: 851,
                                                columnNumber: 19
                                            }, this),
                                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                                                style: {
                                                    fontSize: '14px',
                                                    margin: 0
                                                },
                                                className: "jsx-a18a11d9e8e85108",
                                                children: "Refining content..."
                                            }, void 0, false, {
                                                fileName: "[project]/src/components/SectionDisplayPanel.tsx",
                                                lineNumber: 860,
                                                columnNumber: 19
                                            }, this)
                                        ]
                                    }, void 0, true, {
                                        fileName: "[project]/src/components/SectionDisplayPanel.tsx",
                                        lineNumber: 843,
                                        columnNumber: 17
                                    }, this)
                                ]
                            }, void 0, true, {
                                fileName: "[project]/src/components/SectionDisplayPanel.tsx",
                                lineNumber: 731,
                                columnNumber: 13
                            }, this),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                style: {
                                    padding: '20px 24px',
                                    borderTop: '1px solid #e2e8f0',
                                    display: 'flex',
                                    justifyContent: 'flex-end',
                                    gap: '12px'
                                },
                                className: "jsx-a18a11d9e8e85108",
                                children: [
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                                        onClick: ()=>{
                                            setShowRefineModal(false);
                                            setRefinedContent(null);
                                            setSelectedStyle('');
                                        },
                                        style: {
                                            padding: '10px 20px',
                                            backgroundColor: '#f1f5f9',
                                            color: '#64748b',
                                            border: 'none',
                                            borderRadius: '8px',
                                            fontSize: '14px',
                                            fontWeight: '600',
                                            cursor: 'pointer',
                                            transition: 'all 0.2s ease'
                                        },
                                        onMouseEnter: (e)=>e.currentTarget.style.backgroundColor = '#e2e8f0',
                                        onMouseLeave: (e)=>e.currentTarget.style.backgroundColor = '#f1f5f9',
                                        className: "jsx-a18a11d9e8e85108",
                                        children: "Cancel"
                                    }, void 0, false, {
                                        fileName: "[project]/src/components/SectionDisplayPanel.tsx",
                                        lineNumber: 873,
                                        columnNumber: 15
                                    }, this),
                                    !refinedContent ? /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                                        onClick: handleRefineExecute,
                                        disabled: !selectedStyle || refineLoading,
                                        style: {
                                            padding: '10px 20px',
                                            backgroundColor: !selectedStyle || refineLoading ? '#e2e8f0' : '#8b5cf6',
                                            color: !selectedStyle || refineLoading ? '#94a3b8' : 'white',
                                            border: 'none',
                                            borderRadius: '8px',
                                            fontSize: '14px',
                                            fontWeight: '600',
                                            cursor: !selectedStyle || refineLoading ? 'not-allowed' : 'pointer',
                                            transition: 'all 0.2s ease'
                                        },
                                        onMouseEnter: (e)=>{
                                            if (selectedStyle && !refineLoading) {
                                                e.currentTarget.style.backgroundColor = '#7c3aed';
                                            }
                                        },
                                        onMouseLeave: (e)=>{
                                            if (selectedStyle && !refineLoading) {
                                                e.currentTarget.style.backgroundColor = '#8b5cf6';
                                            }
                                        },
                                        className: "jsx-a18a11d9e8e85108",
                                        children: "✨ Refine"
                                    }, void 0, false, {
                                        fileName: "[project]/src/components/SectionDisplayPanel.tsx",
                                        lineNumber: 896,
                                        columnNumber: 17
                                    }, this) : /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                                        onClick: handleReplaceContent,
                                        style: {
                                            padding: '10px 20px',
                                            backgroundColor: '#10b981',
                                            color: 'white',
                                            border: 'none',
                                            borderRadius: '8px',
                                            fontSize: '14px',
                                            fontWeight: '600',
                                            cursor: 'pointer',
                                            transition: 'all 0.2s ease'
                                        },
                                        onMouseEnter: (e)=>e.currentTarget.style.backgroundColor = '#059669',
                                        onMouseLeave: (e)=>e.currentTarget.style.backgroundColor = '#10b981',
                                        className: "jsx-a18a11d9e8e85108",
                                        children: "✓ Replace Content"
                                    }, void 0, false, {
                                        fileName: "[project]/src/components/SectionDisplayPanel.tsx",
                                        lineNumber: 924,
                                        columnNumber: 17
                                    }, this)
                                ]
                            }, void 0, true, {
                                fileName: "[project]/src/components/SectionDisplayPanel.tsx",
                                lineNumber: 866,
                                columnNumber: 13
                            }, this)
                        ]
                    }, void 0, true, {
                        fileName: "[project]/src/components/SectionDisplayPanel.tsx",
                        lineNumber: 639,
                        columnNumber: 11
                    }, this)
                ]
            }, void 0, true),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$styled$2d$jsx$2f$style$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["default"], {
                id: "a18a11d9e8e85108",
                children: "@keyframes spin{0%{transform:rotate(0)}to{transform:rotate(360deg)}}@keyframes fadeIn{0%{opacity:0}to{opacity:1}}@keyframes slideIn{0%{opacity:0;transform:translate(-50%,-45%)}to{opacity:1;transform:translate(-50%,-50%)}}"
            }, void 0, false, void 0, this)
        ]
    }, void 0, true, {
        fileName: "[project]/src/components/SectionDisplayPanel.tsx",
        lineNumber: 276,
        columnNumber: 5
    }, this);
}
_s(SectionDisplayPanel, "AvTQiu20rPmIEOaOWIiUhwCcxvM=");
_c = SectionDisplayPanel;
var _c;
__turbopack_context__.k.register(_c, "SectionDisplayPanel");
if (typeof globalThis.$RefreshHelpers$ === 'object' && globalThis.$RefreshHelpers !== null) {
    __turbopack_context__.k.registerExports(module, globalThis.$RefreshHelpers$);
}
}}),
"[project]/src/app/page.tsx [app-client] (ecmascript)": ((__turbopack_context__) => {
"use strict";

var { k: __turbopack_refresh__, m: module } = __turbopack_context__;
{
__turbopack_context__.s({
    "default": ()=>Chat
});
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/next/dist/compiled/react/jsx-dev-runtime.js [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$styled$2d$jsx$2f$style$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/styled-jsx/style.js [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/next/dist/compiled/react/index.js [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$components$2f$ConfigPanel$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/src/components/ConfigPanel.tsx [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$components$2f$ChatArea$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/src/components/ChatArea.tsx [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$components$2f$ProgressSidebar$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/src/components/ProgressSidebar.tsx [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$components$2f$ConversationHistory$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/src/components/ConversationHistory.tsx [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$components$2f$SectionDisplayPanel$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/src/components/SectionDisplayPanel.tsx [app-client] (ecmascript)");
;
var _s = __turbopack_context__.k.signature();
'use client';
;
;
;
;
;
;
;
function Chat() {
    _s();
    const [selectedAgent, setSelectedAgent] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useState"])('founder-buddy');
    const [userId, setUserId] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useState"])(12);
    const [mode, setMode] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useState"])('stream');
    const [threadId, setThreadId] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useState"])(null);
    const [currentSection, setCurrentSection] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useState"])(null);
    const [loadedMessages, setLoadedMessages] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useState"])([]);
    const [isConfigOpen, setIsConfigOpen] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useState"])(false);
    const handleAgentChange = (agentId)=>{
        setSelectedAgent(agentId);
        // Reset conversation when agent changes
        setThreadId(null);
        setCurrentSection(null);
    };
    const handleUserIdChange = (newUserId)=>{
        setUserId(newUserId);
    };
    const handleModeChange = (newMode)=>{
        setMode(newMode);
    };
    const handleThreadIdChange = (newThreadId)=>{
        setThreadId(newThreadId);
    };
    const handleSectionUpdate = (section)=>{
        setCurrentSection(section);
    };
    const handleLoadConversation = (conversation)=>{
        setThreadId(conversation.threadId);
        setSelectedAgent(conversation.agentType);
        setUserId(conversation.userId);
        setLoadedMessages(conversation.messages);
        // Restore section state if available
        if (conversation.currentSection) {
            setCurrentSection(conversation.currentSection);
        } else {
            setCurrentSection(null);
        }
    };
    const handleDeleteConversation = (deletedThreadId)=>{
        if (threadId === deletedThreadId) {
            setThreadId(null);
            setLoadedMessages([]);
            setCurrentSection(null);
        }
    };
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
        style: {
            display: 'flex',
            height: '100vh',
            fontFamily: 'system-ui, -apple-system, sans-serif',
            position: 'relative'
        },
        className: "jsx-d9461ce327477151",
        children: [
            isConfigOpen && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["Fragment"], {
                children: [
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                        onClick: ()=>setIsConfigOpen(false),
                        style: {
                            position: 'fixed',
                            top: 0,
                            left: 0,
                            right: 0,
                            bottom: 0,
                            backgroundColor: 'rgba(0, 0, 0, 0.5)',
                            zIndex: 200,
                            animation: 'fadeIn 0.2s ease'
                        },
                        className: "jsx-d9461ce327477151"
                    }, void 0, false, {
                        fileName: "[project]/src/app/page.tsx",
                        lineNumber: 83,
                        columnNumber: 11
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                        style: {
                            position: 'fixed',
                            top: '50%',
                            left: '50%',
                            transform: 'translate(-50%, -50%)',
                            zIndex: 201,
                            animation: 'slideIn 0.3s ease'
                        },
                        className: "jsx-d9461ce327477151",
                        children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$components$2f$ConfigPanel$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__["default"], {
                            selectedAgent: selectedAgent,
                            userId: userId,
                            mode: mode,
                            threadId: threadId,
                            onAgentChange: handleAgentChange,
                            onUserIdChange: handleUserIdChange,
                            onModeChange: handleModeChange,
                            onClose: ()=>setIsConfigOpen(false)
                        }, void 0, false, {
                            fileName: "[project]/src/app/page.tsx",
                            lineNumber: 104,
                            columnNumber: 13
                        }, this)
                    }, void 0, false, {
                        fileName: "[project]/src/app/page.tsx",
                        lineNumber: 96,
                        columnNumber: 11
                    }, this)
                ]
            }, void 0, true),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                style: {
                    width: '280px',
                    height: '100vh',
                    backgroundColor: '#f8fafc',
                    borderRight: '1px solid #e2e8f0',
                    display: 'flex',
                    flexDirection: 'column',
                    overflow: 'hidden'
                },
                className: "jsx-d9461ce327477151",
                children: [
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                        style: {
                            padding: '16px',
                            borderBottom: '1px solid #e2e8f0'
                        },
                        className: "jsx-d9461ce327477151",
                        children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                            onClick: ()=>setIsConfigOpen(true),
                            style: {
                                width: '100%',
                                padding: '10px 16px',
                                backgroundColor: '#6366f1',
                                color: 'white',
                                border: 'none',
                                borderRadius: '8px',
                                fontSize: '14px',
                                cursor: 'pointer',
                                display: 'flex',
                                alignItems: 'center',
                                justifyContent: 'center',
                                gap: '8px',
                                transition: 'all 0.2s ease',
                                fontWeight: '600'
                            },
                            onMouseEnter: (e)=>{
                                e.currentTarget.style.backgroundColor = '#4f46e5';
                                e.currentTarget.style.transform = 'translateY(-1px)';
                                e.currentTarget.style.boxShadow = '0 4px 6px rgba(0, 0, 0, 0.1)';
                            },
                            onMouseLeave: (e)=>{
                                e.currentTarget.style.backgroundColor = '#6366f1';
                                e.currentTarget.style.transform = 'translateY(0)';
                                e.currentTarget.style.boxShadow = 'none';
                            },
                            title: "Open Settings",
                            className: "jsx-d9461ce327477151",
                            children: [
                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                    style: {
                                        fontSize: '16px'
                                    },
                                    className: "jsx-d9461ce327477151",
                                    children: "⚙"
                                }, void 0, false, {
                                    fileName: "[project]/src/app/page.tsx",
                                    lineNumber: 160,
                                    columnNumber: 13
                                }, this),
                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                    className: "jsx-d9461ce327477151",
                                    children: "Settings"
                                }, void 0, false, {
                                    fileName: "[project]/src/app/page.tsx",
                                    lineNumber: 161,
                                    columnNumber: 13
                                }, this)
                            ]
                        }, void 0, true, {
                            fileName: "[project]/src/app/page.tsx",
                            lineNumber: 130,
                            columnNumber: 11
                        }, this)
                    }, void 0, false, {
                        fileName: "[project]/src/app/page.tsx",
                        lineNumber: 129,
                        columnNumber: 9
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                        style: {
                            flex: 1,
                            overflow: 'hidden',
                            display: 'flex',
                            flexDirection: 'column'
                        },
                        className: "jsx-d9461ce327477151",
                        children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$components$2f$ConversationHistory$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__["default"], {
                            currentThreadId: threadId,
                            selectedAgent: selectedAgent,
                            onSelectConversation: handleLoadConversation,
                            onDeleteConversation: handleDeleteConversation
                        }, void 0, false, {
                            fileName: "[project]/src/app/page.tsx",
                            lineNumber: 167,
                            columnNumber: 11
                        }, this)
                    }, void 0, false, {
                        fileName: "[project]/src/app/page.tsx",
                        lineNumber: 166,
                        columnNumber: 9
                    }, this)
                ]
            }, void 0, true, {
                fileName: "[project]/src/app/page.tsx",
                lineNumber: 119,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$components$2f$ChatArea$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__["default"], {
                selectedAgent: selectedAgent,
                userId: userId,
                mode: mode,
                threadId: threadId,
                loadedMessages: loadedMessages,
                currentSection: currentSection,
                onThreadIdChange: handleThreadIdChange,
                onSectionUpdate: handleSectionUpdate,
                progressSidebar: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$components$2f$ProgressSidebar$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__["default"], {
                    currentSection: currentSection,
                    selectedAgent: selectedAgent
                }, void 0, false, {
                    fileName: "[project]/src/app/page.tsx",
                    lineNumber: 186,
                    columnNumber: 11
                }, void 0)
            }, void 0, false, {
                fileName: "[project]/src/app/page.tsx",
                lineNumber: 176,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$components$2f$SectionDisplayPanel$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__["default"], {
                userId: userId,
                selectedAgent: selectedAgent,
                currentSection: currentSection,
                threadId: threadId
            }, void 0, false, {
                fileName: "[project]/src/app/page.tsx",
                lineNumber: 194,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$styled$2d$jsx$2f$style$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["default"], {
                id: "d9461ce327477151",
                children: "@keyframes fadeIn{0%{opacity:0}to{opacity:1}}@keyframes slideIn{0%{opacity:0;transform:translate(-50%,-45%)}to{opacity:1;transform:translate(-50%,-50%)}}"
            }, void 0, false, void 0, this)
        ]
    }, void 0, true, {
        fileName: "[project]/src/app/page.tsx",
        lineNumber: 73,
        columnNumber: 5
    }, this);
}
_s(Chat, "wfhEzVxJEWK2GotGMUTSNZrkgzc=");
_c = Chat;
var _c;
__turbopack_context__.k.register(_c, "Chat");
if (typeof globalThis.$RefreshHelpers$ === 'object' && globalThis.$RefreshHelpers !== null) {
    __turbopack_context__.k.registerExports(module, globalThis.$RefreshHelpers$);
}
}}),
}]);

//# sourceMappingURL=src_5d2d9d1e._.js.map