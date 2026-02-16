#!/usr/bin/env node

import crypto from 'crypto';
import http from 'http';
import test from 'node:test';
import assert from 'node:assert/strict';

import { createNotionRelayApp } from '../build/servers/notion-relay-server.js';

function sign(body, secret) {
  return crypto.createHmac('sha256', secret).update(JSON.stringify(body)).digest('hex');
}

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

test('Notion relay webhook accepts valid signature (contract)', async () => {
  const secret = 'testsecret';
  const payload = {
    task_id: 'test-123',
    agent: 'Prime',
    action: 'Intake',
    timestamp: new Date('2026-01-01T00:00:00.000Z').toISOString(),
    version: 'v1.0'
  };

  const app = createNotionRelayApp({
    relaySecret: secret,
    allowUnauthenticatedWhenUnset: false,
    enqueue: async () => {}
  });

  await withServer(app, async (port) => {
    const sig = sign(payload, secret);
    const res = await fetch(`http://127.0.0.1:${port}/webhook/prime`, {
      method: 'POST',
      headers: {
        'content-type': 'application/json',
        'x-relay-signature': sig
      },
      body: JSON.stringify(payload)
    });
    assert.equal(res.status, 200);
    const body = await res.json();
    assert.deepEqual(body, { ok: true });
  });
});

test('Notion relay webhook rejects invalid signature', async () => {
  const secret = 'testsecret';
  const payload = { task_id: 'test-123', agent: 'Prime', action: 'Intake' };

  const app = createNotionRelayApp({
    relaySecret: secret,
    allowUnauthenticatedWhenUnset: false,
    enqueue: async () => {}
  });

  await withServer(app, async (port) => {
    const res = await fetch(`http://127.0.0.1:${port}/webhook/prime`, {
      method: 'POST',
      headers: {
        'content-type': 'application/json',
        'x-relay-signature': 'bad'
      },
      body: JSON.stringify(payload)
    });
    // timingSafeEqual throws when buffer lengths differ -> treated as a bad request
    assert.equal(res.status, 400);
    const body = await res.json();
    assert.equal(body.ok, false);
  });
});


test('Notion relay supports claude and notion webhook paths', async () => {
  const secret = 'testsecret';
  const payload = { task_id: 'test-456', action: 'Review' };

  const app = createNotionRelayApp({
    relaySecret: secret,
    allowUnauthenticatedWhenUnset: false,
    enqueue: async () => {}
  });

  await withServer(app, async (port) => {
    const sig = sign(payload, secret);

    const claudeRes = await fetch(`http://127.0.0.1:${port}/webhook/claude`, {
      method: 'POST',
      headers: {
        'content-type': 'application/json',
        'x-relay-signature': sig
      },
      body: JSON.stringify(payload)
    });
    assert.equal(claudeRes.status, 200);

    const notionRes = await fetch(`http://127.0.0.1:${port}/webhook/notion`, {
      method: 'POST',
      headers: {
        'content-type': 'application/json',
        'x-relay-signature': sig
      },
      body: JSON.stringify(payload)
    });
    assert.equal(notionRes.status, 200);
  });
});
