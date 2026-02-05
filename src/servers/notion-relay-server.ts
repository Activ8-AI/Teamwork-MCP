import express from 'express';
import crypto from 'crypto';
import http from 'http';
import { pathToFileURL } from 'url';
import logger from '../utils/logger.js';
import { enqueueHandoff as defaultEnqueueHandoff } from '../services/orchestration/enqueueHandoff.js';

export type NotionRelayEnqueue = typeof defaultEnqueueHandoff;

export interface NotionRelayAppOptions {
  relayToken?: string;
  relaySecret?: string;
  /**
   * If true, requests are allowed when neither RELAY_SECRET nor RELAY_TOKEN is configured.
   * Defaults to true (development-friendly), but can be set false in tests/production hardening.
   */
  allowUnauthenticatedWhenUnset?: boolean;
  /**
   * Dependency injection for tests.
   */
  enqueue?: NotionRelayEnqueue;
}

export function createNotionRelayApp(options: NotionRelayAppOptions = {}) {
  const app = express();
  app.use(express.json());

  const token = options.relayToken ?? process.env.RELAY_TOKEN;
  const secret = options.relaySecret ?? process.env.RELAY_SECRET;
  const allowUnauthenticatedWhenUnset =
    options.allowUnauthenticatedWhenUnset ?? true;
  const enqueue = options.enqueue ?? defaultEnqueueHandoff;

  const verifyRequest: express.RequestHandler = (req, res, next) => {
    const headerSig = (req.header('x-relay-signature') || '').trim();
    const headerTok = (req.header('x-relay-token') || '').trim();

    if (secret) {
      try {
        const payload = JSON.stringify(req.body || {});
        const h = crypto.createHmac('sha256', secret).update(payload).digest('hex');
        if (crypto.timingSafeEqual(Buffer.from(h), Buffer.from(headerSig || ''))) {
          next();
          return;
        }
        logger.warn('Signature verification failed');
        res.status(401).json({ ok: false, error: 'invalid signature' });
        return;
      } catch (e: any) {
        logger.error(e.message);
        res.status(400).json({ ok: false, error: 'bad request' });
        return;
      }
    } else if (token) {
      if (headerTok && token && crypto.timingSafeEqual(Buffer.from(headerTok), Buffer.from(token))) {
        next();
        return;
      }
      logger.warn('Token verification failed');
      res.status(401).json({ ok: false, error: 'invalid token' });
      return;
    }

    if (!allowUnauthenticatedWhenUnset) {
      res.status(500).json({ ok: false, error: 'relay auth not configured' });
      return;
    }

    logger.warn('No RELAY_SECRET or RELAY_TOKEN configured; allowing request (development).');
    next();
  };

app.get('/health', (_req, res) => {
  res.json({ ok: true });
});

function toTargets(agent: string) {
  const name = (agent || '').toLowerCase();
  if (name.includes('prime')) return [{ name: 'PrimeAgent' }];
  if (name.includes('claw') || name.includes('clau')) return [{ name: 'ClaudeAgent' }];
  return [{ name: 'NotionRelay' }];
}

app.post('/webhook/prime', verifyRequest, async (req, res) => {
  try {
    const payload = req.body || {};
    await enqueue({
      title: payload.task || payload.task_id || 'Prime Intake',
      description: `Stage: ${payload.action || 'Intake'}`,
      targets: toTargets('prime')
    });
    res.json({ ok: true });
  } catch (e: any) {
    logger.error(e.message);
    res.status(500).json({ ok: false, error: e.message });
  }
});

async function handleClaudeWebhook(req: express.Request, res: express.Response) {
  try {
    const payload = req.body || {};
    await enqueue({
      title: payload.task || payload.task_id || 'Claude In-Flight',
      description: `Stage: ${payload.action || 'In-Flight'}`,
      targets: toTargets('claude')
    });
    res.json({ ok: true });
  } catch (e: any) {
    logger.error(e.message);
    res.status(500).json({ ok: false, error: e.message });
  }
}

async function handleNotionWebhook(req: express.Request, res: express.Response) {
  try {
    const payload = req.body || {};
    await enqueue({
      title: payload.task || payload.task_id || 'Notion Review',
      description: `Stage: ${payload.action || 'Review'}`,
      targets: [{ name: 'NotionRelay' }]
    });
    res.json({ ok: true });
  } catch (e: any) {
    logger.error(e.message);
    res.status(500).json({ ok: false, error: e.message });
  }
}

app.post('/webhook/claude', verifyRequest, handleClaudeWebhook);
// Backward compatible alias.
app.post('/webhook/clawed', verifyRequest, handleClaudeWebhook);

app.post('/webhook/notion', verifyRequest, handleNotionWebhook);
// Backward compatible alias.
app.post('/webhook/ancillary', verifyRequest, handleNotionWebhook);

  return app;
}

export interface NotionRelayServerOptions extends NotionRelayAppOptions {
  port?: number;
}

export function startNotionRelayServer(options: NotionRelayServerOptions = {}) {
  const app = createNotionRelayApp(options);
  const port = options.port ?? (process.env.PORT ? Number(process.env.PORT) : 8787);
  const server = http.createServer(app);

  server.listen(port, () => {
    logger.info(`Notion Relay server listening on :${port}`);
  });

  return { app, server, port };
}

// Default export for callers that just want an Express app instance.
export default createNotionRelayApp();

// If invoked directly (e.g. `node build/servers/notion-relay-server.js`), start the server.
if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) {
  startNotionRelayServer();
}
