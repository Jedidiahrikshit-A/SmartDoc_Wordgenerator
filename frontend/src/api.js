const jsonHeaders = { 'Content-Type': 'application/json' };

function cookie(name) {
  return document.cookie.split('; ').find((part) => part.startsWith(`${name}=`))?.split('=')[1] || '';
}

export async function ensureCsrf() {
  await fetch('/api/auth/csrf', { credentials: 'include' });
}

async function request(path, options = {}) {
  const method = options.method || 'GET';
  if (['POST', 'PUT', 'PATCH', 'DELETE'].includes(method)) await ensureCsrf();
  const headers = { ...(options.body instanceof FormData ? {} : jsonHeaders), ...(options.headers || {}) };
  if (method !== 'GET') headers['X-CSRF-Token'] = decodeURIComponent(cookie('csrf_token'));
  const response = await fetch(path, { ...options, method, headers, credentials: 'include' });
  const contentType = response.headers.get('content-type') || '';
  const payload = contentType.includes('application/json') ? await response.json() : await response.blob();
  if (!response.ok) throw new Error(payload?.error?.message || 'Something went wrong.');
  return payload;
}

export const api = {
  get: (path) => request(path),
  post: (path, body) => request(path, { method: 'POST', body: body instanceof FormData ? body : JSON.stringify(body) }),
  put: (path, body) => request(path, { method: 'PUT', body: JSON.stringify(body) }),
  delete: (path) => request(path, { method: 'DELETE' }),
  download: async (path) => {
    const response = await fetch(path, { credentials: 'include' });
    if (!response.ok) { const data = await response.json().catch(() => ({})); throw new Error(data?.error?.message || 'Download failed.'); }
    return { blob: await response.blob(), disposition: response.headers.get('content-disposition') || '' };
  }
};
