import test from 'node:test';
import assert from 'node:assert/strict';
import http from 'node:http';

import { createNotionRelayApp } from '../build/servers/notion-relay-server.js';

async function withServer(app, fn) {
  const server = http.createServer(app);
  await new Promise((resolve) => server.listen(0, resolve));
  const address = server.address();
  const port = typeof address === 'object' && address ? address.port : 0;
  try {
    await fn(port);
  } finally {
    await new Promise((resolve) => server.close(resolve));
  }
}

test('Notion Relay server health endpoint responds ok', async () => {
  const app = createNotionRelayApp({
    // Avoid side effects / FS writes during tests.
    enqueue: async () => {},
    allowUnauthenticatedWhenUnset: true
  });

  await withServer(app, async (port) => {
    const res = await fetch(`http://127.0.0.1:${port}/health`);
    assert.equal(res.status, 200);
    const body = await res.json();
    assert.deepEqual(body, { ok: true });
  });
});