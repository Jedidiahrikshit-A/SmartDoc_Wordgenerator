import { beforeEach, describe, expect, it, vi } from 'vitest';
import { api } from './api';

describe('SmartDocAI API client', () => {
  beforeEach(() => {
    vi.restoreAllMocks();
    global.fetch = vi.fn((path) => Promise.resolve({
      ok: path === '/api/health',
      headers: { get: () => 'application/json' },
      json: async () => path === '/api/health' ? { ok: true, service: 'smartdocai' } : { error: { message: 'Unauthorized' } },
    }));
  });

  it('returns the JSON payload for a healthy API', async () => {
    await expect(api.get('/api/health')).resolves.toEqual({ ok: true, service: 'smartdocai' });
    expect(fetch).toHaveBeenCalledWith('/api/health', expect.objectContaining({ credentials: 'include' }));
  });

  it('surfaces structured API errors', async () => {
    await expect(api.get('/api/private')).rejects.toThrow('Unauthorized');
  });
});
