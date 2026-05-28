/**
 * BlueOcean Crawler Proxy - Cloudflare Worker
 * CORS reverse proxy with anti-bot bypass for blue-ocean product selection tool
 */

// ⚠️ 部署前必须改成你自己的随机字符串 (推荐: openssl rand -hex 24)
// 留空 '' 表示不验证 token (任何人可调用,不推荐生产用)
const SECRET_TOKEN = '';
const DEFAULT_UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36';
const ALLOWED_HOSTS = [];

addEventListener('fetch', event => {
  event.respondWith(handle(event.request));
});

async function handle(request) {
  if (request.method === 'OPTIONS') {
    return new Response(null, { headers: corsHeaders() });
  }

  const url = new URL(request.url);
  const target = url.searchParams.get('url');

  if (!target) {
    return json({
      service: 'BlueOcean Crawler Proxy',
      version: '1.0',
      usage: 'GET /?url=<TARGET_URL>[&token=<TOKEN>]',
      examples: [
        '/?url=https://weibo-trending-hot-search.vercel.app/api',
        '/?url=https://www.zhihu.com/api/v4/search/top_search',
        '/?url=https://api.bilibili.com/x/web-interface/popular?ps=20',
      ],
      ok: true,
      timestamp: new Date().toISOString()
    });
  }

  if (SECRET_TOKEN) {
    const provided = url.searchParams.get('token') || request.headers.get('X-Proxy-Token');
    if (provided !== SECRET_TOKEN) return json({ error: 'Invalid token' }, 401);
  }

  let targetUrl;
  try { targetUrl = new URL(target); }
  catch (e) { return json({ error: 'Invalid url: ' + e.message }, 400); }

  if (!/^https?:$/.test(targetUrl.protocol)) {
    return json({ error: 'Only http(s) allowed' }, 400);
  }
  if (ALLOWED_HOSTS.length && !ALLOWED_HOSTS.some(h => targetUrl.hostname.endsWith(h))) {
    return json({ error: 'Host not allowed' }, 403);
  }

  const headers = new Headers(request.headers);
  headers.delete('host');
  headers.delete('origin');
  headers.delete('referer');
  headers.delete('cf-connecting-ip');
  headers.delete('cf-ipcountry');
  headers.delete('cf-ray');
  headers.delete('cf-visitor');
  headers.delete('x-forwarded-for');
  headers.delete('x-forwarded-proto');
  headers.delete('x-real-ip');

  if (!headers.get('user-agent') || headers.get('user-agent').includes('Cloudflare')) {
    headers.set('user-agent', DEFAULT_UA);
  }
  headers.set('referer', targetUrl.origin + '/');

  const init = {
    method: request.method,
    headers,
    redirect: 'follow'
  };
  if (request.method !== 'GET' && request.method !== 'HEAD') {
    init.body = await request.arrayBuffer();
  }

  try {
    const upstream = await fetch(targetUrl.toString(), init);
    const respHeaders = new Headers(upstream.headers);
    Object.entries(corsHeaders()).forEach(([k, v]) => respHeaders.set(k, v));
    respHeaders.delete('content-security-policy');
    respHeaders.delete('content-security-policy-report-only');
    respHeaders.delete('x-frame-options');
    respHeaders.delete('strict-transport-security');
    respHeaders.set('x-proxy-by', 'BlueOcean-Worker');
    return new Response(upstream.body, {
      status: upstream.status,
      statusText: upstream.statusText,
      headers: respHeaders
    });
  } catch (e) {
    return json({ error: 'Upstream fetch failed: ' + e.message, target: targetUrl.toString() }, 502);
  }
}

function corsHeaders() {
  return {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
    'Access-Control-Allow-Headers': '*',
    'Access-Control-Expose-Headers': '*',
    'Access-Control-Max-Age': '86400'
  };
}

function json(obj, status = 200) {
  return new Response(JSON.stringify(obj, null, 2), {
    status,
    headers: { 'Content-Type': 'application/json; charset=utf-8', ...corsHeaders() }
  });
}
