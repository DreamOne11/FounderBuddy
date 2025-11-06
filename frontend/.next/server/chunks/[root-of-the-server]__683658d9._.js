module.exports = {

"[project]/.next-internal/server/app/api/chat/route/actions.js [app-rsc] (server actions loader, ecmascript)": ((__turbopack_context__) => {

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
"[project]/src/app/api/chat/route.ts [app-route] (ecmascript)": ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s({
    "POST": ()=>POST
});
const logApiCall = (phase, data, level = 'INFO')=>{
    const timestamp = new Date().toISOString();
    const logLevel = ("TURBOPACK compile-time truthy", 1) ? 'DEBUG' : "TURBOPACK unreachable";
    // 在生产环境中，只记录ERROR和WARN级别的日志，除非明确启用DEBUG
    if ("TURBOPACK compile-time falsy", 0) //TURBOPACK unreachable
    ;
    const logPrefix = level === 'ERROR' ? '🔴' : level === 'WARN' ? '🟡' : '🔵';
    console.log(`\n${logPrefix} === API CALL LOG [${level}] [${phase}] - ${timestamp} ===`);
    console.log(JSON.stringify(data, null, 2));
    console.log('=====================================\n');
};
async function POST(req) {
    const requestStartTime = Date.now();
    try {
        const { messages, userId, threadId, mode = 'stream', agentId = 'value-canvas' } = await req.json();
        const latestMessage = messages[messages.length - 1]?.content || '';
        // 详细的请求开始日志
        logApiCall('REQUEST_START', {
            timestamp: new Date().toISOString(),
            requestId: `req_${requestStartTime}`,
            requestHeaders: Object.fromEntries(req.headers.entries()),
            requestUrl: req.url,
            requestMethod: req.method,
            input: {
                userId: userId,
                threadId: threadId,
                agentId: agentId,
                messageCount: messages.length,
                latestMessage: latestMessage,
                allMessages: messages
            },
            environment: {
                nodeEnv: ("TURBOPACK compile-time value", "development"),
                apiEnv: ("TURBOPACK compile-time value", "local"),
                hasAuthToken: !!process.env.VALUE_CANVAS_API_TOKEN
            }
        });
        // Validate and ensure userId is an integer
        const validateUserId = (id)=>{
            if (id === null || id === undefined) {
                throw new Error('user_id is required and must be provided');
            }
            const numericId = Number(id);
            if (!Number.isInteger(numericId) || numericId <= 0) {
                throw new Error('user_id must be a positive integer');
            }
            return numericId;
        };
        const finalUserId = validateUserId(userId);
        const requestBody = {
            message: latestMessage,
            user_id: finalUserId
        };
        // 只有stream模式才需要stream_tokens
        if (mode === 'stream') {
            requestBody.stream_tokens = true;
        }
        if (threadId) {
            requestBody.thread_id = threadId;
        }
        const isLocal = ("TURBOPACK compile-time value", "local") === 'local';
        const apiUrl = ("TURBOPACK compile-time truthy", 1) ? process.env.VALUE_CANVAS_API_URL_LOCAL : "TURBOPACK unreachable";
        const endpoint = mode === 'stream' ? 'stream' : 'invoke';
        const fullApiUrl = `${apiUrl}/${agentId}/${endpoint}`;
        // 详细的外部API请求日志
        logApiCall('EXTERNAL_API_REQUEST', {
            timestamp: new Date().toISOString(),
            requestId: `req_${requestStartTime}`,
            externalApi: {
                url: fullApiUrl,
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    hasAuthToken: !!process.env.VALUE_CANVAS_API_TOKEN
                },
                body: requestBody
            },
            processedData: {
                originalUserId: userId,
                finalUserId: finalUserId,
                originalThreadId: threadId,
                messageLength: latestMessage.length,
                isLocal: isLocal
            }
        });
        const response = await fetch(fullApiUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                ...process.env.VALUE_CANVAS_API_TOKEN && {
                    'Authorization': `Bearer ${process.env.VALUE_CANVAS_API_TOKEN}`
                }
            },
            body: JSON.stringify(requestBody)
        });
        // 详细的外部API响应日志
        const responseTime = Date.now() - requestStartTime;
        logApiCall('EXTERNAL_API_RESPONSE', {
            timestamp: new Date().toISOString(),
            requestId: `req_${requestStartTime}`,
            response: {
                status: response.status,
                statusText: response.statusText,
                headers: Object.fromEntries(response.headers.entries()),
                ok: response.ok
            },
            performance: {
                responseTime: `${responseTime}ms`,
                startTime: requestStartTime
            }
        });
        if (!response.ok) {
            const errorText = await response.text();
            logApiCall('API_ERROR', {
                timestamp: new Date().toISOString(),
                requestId: `req_${requestStartTime}`,
                error: {
                    status: response.status,
                    statusText: response.statusText,
                    errorText: errorText,
                    responseTime: `${responseTime}ms`
                }
            }, 'ERROR');
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        // 处理invoke模式的同步响应
        if (mode === 'invoke') {
            const invokeResponse = await response.json();
            logApiCall('INVOKE_SUCCESS', {
                timestamp: new Date().toISOString(),
                requestId: `req_${requestStartTime}`,
                response: {
                    contentLength: invokeResponse.output?.content?.length || 0,
                    threadId: invokeResponse.thread_id,
                    userId: invokeResponse.user_id
                }
            });
            return Response.json({
                content: invokeResponse.output?.content || '',
                threadId: invokeResponse.thread_id,
                userId: invokeResponse.user_id,
                section: invokeResponse.output?.custom_data?.section || null,
                mode: 'invoke'
            });
        }
        // 返回流式响应
        const encoder = new TextEncoder();
        let finalContent = '';
        let finalThreadId = null;
        let finalUserId_response = null;
        let finalSection = null;
        let chunkCount = 0;
        let tokenCount = 0;
        let lastActivityTime = Date.now();
        const stream = new ReadableStream({
            async start (controller) {
                const reader = response.body?.getReader();
                const decoder = new TextDecoder();
                const STREAM_TIMEOUT = 30000; // 30秒超时
                let timeoutId = null;
                let isClosed = false; // 添加标志防止重复关闭
                // 安全地写入数据
                const safeEnqueue = (data)=>{
                    if (!isClosed) {
                        try {
                            controller.enqueue(data);
                        } catch (e) {
                            console.warn('Failed to enqueue data:', e);
                        }
                    }
                };
                // 安全地关闭流
                const safeClose = ()=>{
                    if (!isClosed) {
                        isClosed = true;
                        if (timeoutId) clearTimeout(timeoutId);
                        try {
                            controller.close();
                        } catch (e) {
                            console.warn('Failed to close controller:', e);
                        }
                    }
                };
                // 设置流超时监控
                const resetTimeout = ()=>{
                    if (timeoutId) clearTimeout(timeoutId);
                    if (!isClosed) {
                        timeoutId = setTimeout(()=>{
                            logApiCall('STREAM_TIMEOUT', {
                                timestamp: new Date().toISOString(),
                                requestId: `req_${requestStartTime}`,
                                timeoutInfo: {
                                    timeoutDuration: STREAM_TIMEOUT,
                                    lastActivityTime: new Date(lastActivityTime).toISOString(),
                                    chunkCount: chunkCount,
                                    tokenCount: tokenCount,
                                    inactiveTime: `${Date.now() - lastActivityTime}ms`
                                }
                            }, 'ERROR');
                            if (!isClosed) {
                                controller.error(new Error('Stream timeout - no data received for 30 seconds'));
                                isClosed = true;
                            }
                        }, STREAM_TIMEOUT);
                    }
                };
                resetTimeout();
                logApiCall('STREAM_READER_INIT', {
                    timestamp: new Date().toISOString(),
                    requestId: `req_${requestStartTime}`,
                    streamSetup: {
                        hasReader: !!reader,
                        responseBodyExists: !!response.body,
                        timeoutConfigured: STREAM_TIMEOUT
                    }
                });
                if (!reader) {
                    logApiCall('STREAM_ERROR', {
                        timestamp: new Date().toISOString(),
                        requestId: `req_${requestStartTime}`,
                        error: {
                            type: 'NO_READER',
                            message: 'No reader available from response body'
                        }
                    }, 'ERROR');
                    safeClose();
                    return;
                }
                try {
                    while(true){
                        const readStart = Date.now();
                        const { done, value } = await reader.read();
                        const readTime = Date.now() - readStart;
                        if (done) {
                            logApiCall('STREAM_COMPLETE', {
                                timestamp: new Date().toISOString(),
                                requestId: `req_${requestStartTime}`,
                                streamStats: {
                                    totalChunks: chunkCount,
                                    totalTokens: tokenCount,
                                    finalContentLength: finalContent.length,
                                    totalStreamTime: `${Date.now() - requestStartTime}ms`,
                                    lastActivityTime: new Date(lastActivityTime).toISOString()
                                }
                            });
                            break;
                        }
                        chunkCount++;
                        lastActivityTime = Date.now();
                        resetTimeout(); // 重置超时计时器
                        const chunk = decoder.decode(value, {
                            stream: true
                        });
                        const lines = chunk.split('\n');
                        logApiCall('STREAM_CHUNK_RECEIVED', {
                            timestamp: new Date().toISOString(),
                            requestId: `req_${requestStartTime}`,
                            chunkData: {
                                chunkNumber: chunkCount,
                                chunkSize: value?.length || 0,
                                readTime: `${readTime}ms`,
                                linesCount: lines.length,
                                rawChunk: chunk.substring(0, 200) + (chunk.length > 200 ? '...' : ''),
                                chunkLength: chunk.length
                            }
                        });
                        for (const line of lines){
                            if (line.startsWith('data: ')) {
                                const data = line.slice(6);
                                if (data === '[DONE]') {
                                    // 发送最终的完整响应数据
                                    const finalResponseData = {
                                        type: 'final_response',
                                        content: finalContent,
                                        threadId: finalThreadId,
                                        userId: finalUserId_response || finalUserId,
                                        section: finalSection
                                    };
                                    logApiCall('STREAM_SENDING_FINAL', {
                                        timestamp: new Date().toISOString(),
                                        requestId: `req_${requestStartTime}`,
                                        finalData: {
                                            contentLength: finalContent.length,
                                            threadId: finalThreadId,
                                            userId: finalUserId_response || finalUserId,
                                            hasSection: !!finalSection,
                                            totalTokens: tokenCount,
                                            totalChunks: chunkCount
                                        }
                                    });
                                    safeEnqueue(encoder.encode(`data: ${JSON.stringify(finalResponseData)}\n\n`));
                                    safeEnqueue(encoder.encode('data: [DONE]\n\n'));
                                    safeClose();
                                    return;
                                }
                                try {
                                    const parsed = JSON.parse(data);
                                    logApiCall('STREAM_DATA_PARSED', {
                                        timestamp: new Date().toISOString(),
                                        requestId: `req_${requestStartTime}`,
                                        parsedData: {
                                            type: parsed.type,
                                            contentLength: parsed.content?.length || 0,
                                            hasRunId: !!parsed.content?.run_id,
                                            hasCustomData: !!parsed.content?.custom_data,
                                            rawDataSample: data.substring(0, 100) + (data.length > 100 ? '...' : '')
                                        }
                                    });
                                    // 处理不同类型的流式数据
                                    if (parsed.type === 'token') {
                                        tokenCount++;
                                        finalContent += parsed.content;
                                    } else if (parsed.type === 'message') {
                                        finalContent = parsed.content.content || finalContent;
                                        if (parsed.content.run_id) {
                                            finalThreadId = parsed.content.run_id;
                                        }
                                        if (parsed.content.custom_data) {
                                            finalSection = parsed.content.custom_data.section;
                                            finalUserId_response = parsed.content.custom_data.user_id;
                                        }
                                    } else if (parsed.type === 'section') {
                                        finalSection = parsed.content;
                                    }
                                    // 转发流式数据
                                    safeEnqueue(encoder.encode(`data: ${JSON.stringify(parsed)}\n\n`));
                                } catch (e) {
                                    logApiCall('STREAM_PARSE_ERROR', {
                                        timestamp: new Date().toISOString(),
                                        requestId: `req_${requestStartTime}`,
                                        parseError: {
                                            error: e instanceof Error ? e.message : 'Unknown parse error',
                                            rawData: data,
                                            chunkNumber: chunkCount,
                                            lineNumber: lines.indexOf(line)
                                        }
                                    }, 'WARN');
                                    console.error('解析流数据失败:', e, data);
                                }
                            }
                        }
                    }
                } catch (error) {
                    logApiCall('STREAM_PROCESSING_ERROR', {
                        timestamp: new Date().toISOString(),
                        requestId: `req_${requestStartTime}`,
                        streamError: {
                            error: error instanceof Error ? error.message : 'Unknown stream error',
                            stack: error instanceof Error ? error.stack : undefined,
                            chunkCount: chunkCount,
                            tokenCount: tokenCount,
                            lastActivityTime: new Date(lastActivityTime).toISOString(),
                            streamDuration: `${Date.now() - requestStartTime}ms`
                        }
                    }, 'ERROR');
                    console.error('Stream processing error:', error);
                    if (!isClosed) {
                        controller.error(error);
                        isClosed = true;
                    }
                    if (timeoutId) clearTimeout(timeoutId);
                }
            }
        });
        logApiCall('STREAM_START', {
            timestamp: new Date().toISOString(),
            requestId: `req_${requestStartTime}`,
            streamSetup: {
                responseHeaders: Object.fromEntries(response.headers.entries())
            }
        });
        return new Response(stream, {
            headers: {
                'Content-Type': 'text/event-stream',
                'Cache-Control': 'no-cache',
                'Connection': 'keep-alive'
            }
        });
    } catch (error) {
        const errorResponseTime = Date.now() - requestStartTime;
        logApiCall('REQUEST_ERROR', {
            timestamp: new Date().toISOString(),
            requestId: `req_${requestStartTime}`,
            error: {
                message: error instanceof Error ? error.message : 'Unknown error',
                stack: error instanceof Error ? error.stack : undefined,
                type: error?.constructor?.name || 'Unknown'
            },
            performance: {
                errorResponseTime: `${errorResponseTime}ms`,
                requestStartTime: requestStartTime,
                errorTime: Date.now()
            }
        }, 'ERROR');
        return new Response(JSON.stringify({
            content: `Error: ${error instanceof Error ? error.message : 'Unknown error'}`,
            threadId: null,
            userId: null
        }), {
            status: 500,
            headers: {
                'Content-Type': 'application/json'
            }
        });
    }
}
}),

};

//# sourceMappingURL=%5Broot-of-the-server%5D__683658d9._.js.map