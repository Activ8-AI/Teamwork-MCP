import fs from 'fs';
import path from 'path';
import crypto from 'crypto';
import logger from '../../utils/logger.js';
import createTask from '../tasks/createTask.js';
import enqueueHandoff from '../orchestration/enqueueHandoff.js';
import type { TaskRequest } from '../../models/TaskRequest.js';
import type { PayloadNullableTaskPriority } from '../../models/PayloadNullableTaskPriority.js';
import type { PayloadNullableDate } from '../../models/PayloadNullableDate.js';
import type { CompetitorDeltaInput, CompetitorDeltaRecord } from '../../models/CompetitorDelta.js';
import type { ClientCompetitorProfile, CompetitorDefinition } from '../../models/CompetitorProfile.js';

const COMP_INTEL_ROOT = path.resolve(process.cwd(), 'competitor-intel');
const BRIEFS_DIR = path.join(COMP_INTEL_ROOT, 'briefs');
const DELTA_LOG = path.join(COMP_INTEL_ROOT, 'deltas.jsonl');
const REFLEX_PIPELINE_FILE = path.resolve(process.cwd(), 'reflex', 'pipelines', 'competitor-deltas.jsonl');
const COMP_MAP_PATH = path.resolve(process.cwd(), 'codex-portal', 'client-intelligence', 'competitor-definition-map.json');

interface CompetitorMapFile {
  clients?: ClientCompetitorProfile[];
}

function ensureDirectory(target: string): void {
  if (!fs.existsSync(target)) {
    fs.mkdirSync(target, { recursive: true });
  }
}

function ensureFoundations() {
  ensureDirectory(COMP_INTEL_ROOT);
  ensureDirectory(BRIEFS_DIR);
  ensureDirectory(path.dirname(DELTA_LOG));
  ensureDirectory(path.dirname(REFLEX_PIPELINE_FILE));
}

export function getCompetitorDefinitionMap(): ClientCompetitorProfile[] {
  if (!fs.existsSync(COMP_MAP_PATH)) {
    logger.warn('Competitor Definition Map not found, returning empty set.');
    return [];
  }
  try {
    const raw = fs.readFileSync(COMP_MAP_PATH, 'utf8');
    const parsed = JSON.parse(raw) as CompetitorMapFile | ClientCompetitorProfile[];
    if (Array.isArray(parsed)) {
      return parsed;
    }
    return parsed.clients || [];
  } catch (error: any) {
    logger.error(`Failed to read Competitor Definition Map: ${error.message}`);
    return [];
  }
}

function findClient(clientId: string): ClientCompetitorProfile | undefined {
  return getCompetitorDefinitionMap().find((client) => client.clientId === clientId);
}

function findCompetitor(client: ClientCompetitorProfile | undefined, competitorId: string): CompetitorDefinition | undefined {
  return client?.competitors.find((competitor) => competitor.id === competitorId);
}

function normalizeConfidence(value?: number): number {
  const fallback = 0.72;
  if (value === undefined || Number.isNaN(value)) return fallback;
  return Math.max(0, Math.min(1, value));
}

function computeDueDate(severity: CompetitorDeltaInput['severity']): string {
  const days = severity === 'critical' || severity === 'high' ? 2 : severity === 'medium' ? 5 : 10;
  const due = new Date();
  due.setUTCDate(due.getUTCDate() + days);
  return due.toISOString().slice(0, 10);
}

function buildBrief(record: CompetitorDeltaRecord): string {
  const summaryLines = [
    `# Competitor Intelligence Brief — ${record.clientName || record.clientId}`,
    '',
    `- **Competitor:** ${record.competitorName || record.competitorId}`,
    `- **Signal Type:** ${record.signalType}`,
    `- **Severity:** ${record.severity || 'medium'}`,
    `- **Confidence Score:** ${(record.confidence ?? 0.72).toFixed(2)}`,
    `- **Custodian Hash:** ${record.custodianHash}`,
    `- **Watcher Agents:** ${record.watcherAgents.length > 0 ? record.watcherAgents.join(', ') : 'unassigned'}`,
    '',
    '## Summary',
    record.summary,
    '',
    '## Market Impact',
    record.marketImpact || 'TBD',
    '',
    '## Strategic Implication',
    record.strategicImplication || 'Pending Prime review.',
    '',
    '## Recommended Actions',
    ...(record.recommendedActions && record.recommendedActions.length
      ? record.recommendedActions.map((action, idx) => `${idx + 1}. ${action}`)
      : ['1. Pending charter review.']),
    '',
    '## Governance Notes',
    record.governanceNotes || 'Standard charter controls apply.',
    '',
    '## Evidence',
    record.evidenceUrl ? `- URL: ${record.evidenceUrl}` : '- URL: not provided',
    record.evidenceSnippet ? `- Snippet: ${record.evidenceSnippet}` : '',
    '',
    '## Metadata',
    '```json',
    JSON.stringify(record.metadata || {}, null, 2),
    '```',
  ];
  return summaryLines.filter(Boolean).join('\n');
}

function buildTaskPayload(record: CompetitorDeltaRecord): TaskRequest {
  const priority: PayloadNullableTaskPriority = {
    Set: true,
    Value: record.severity === 'critical' || record.severity === 'high' ? 'high' : 'medium',
  };

  const dueAt: PayloadNullableDate = { Set: true, Value: computeDueDate(record.severity) };
  const descriptionLines = [
    `**Signal Type:** ${record.signalType}`,
    `**Summary:** ${record.summary}`,
    record.marketImpact ? `**Market Impact:** ${record.marketImpact}` : undefined,
    record.strategicImplication ? `**Strategic Implication:** ${record.strategicImplication}` : undefined,
    record.recommendedActions?.length ? '**Recommended Actions:**' : undefined,
    ...(record.recommendedActions?.map((action) => `- ${action}`) || []),
    `**Severity:** ${record.severity || 'medium'} | **Confidence:** ${(record.confidence ?? 0.72).toFixed(2)}`,
    record.briefPath ? `**Brief:** ${record.briefPath}` : undefined,
    record.evidenceUrl ? `**Evidence:** ${record.evidenceUrl}` : undefined,
  ].filter(Boolean);

  return {
    task: {
      name: `Competitor delta — ${record.competitorName || record.competitorId} (${record.signalType})`,
      description: descriptionLines.join('\n'),
      priority,
      status: 'new',
      dueAt,
    },
  };
}

async function routeToTeamwork(record: CompetitorDeltaRecord, tasklistId?: string): Promise<void> {
  if (!tasklistId && !process.env.TEAMWORK_COMP_INTEL_TASKLIST_ID) {
    logger.info('No Teamwork tasklist configured for competitor intel; skipping task creation.');
    return;
  }
  const targetTasklistId = tasklistId || process.env.TEAMWORK_COMP_INTEL_TASKLIST_ID || '';
  try {
    const payload = buildTaskPayload(record);
    await createTask(String(targetTasklistId), payload);
    logger.info(`Created Teamwork task for competitor delta ${record.id}`);
  } catch (error: any) {
    logger.error(`Failed to create Teamwork task for competitor delta ${record.id}: ${error.message}`);
  }
}

async function persistRecord(record: CompetitorDeltaRecord, brief: string): Promise<void> {
  ensureFoundations();
  await Promise.all([
    fs.promises.appendFile(DELTA_LOG, JSON.stringify(record) + '\n', { encoding: 'utf8' }),
    fs.promises.writeFile(path.resolve(process.cwd(), record.briefPath), brief, { encoding: 'utf8' }),
    fs.promises.appendFile(REFLEX_PIPELINE_FILE, JSON.stringify(record) + '\n', { encoding: 'utf8' })
  ]);
}

async function routeToHandoff(record: CompetitorDeltaRecord, channel?: string): Promise<void> {
  try {
    await enqueueHandoff({
      title: `Competitor delta detected: ${record.competitorName || record.competitorId}`,
      description: record.summary,
      hypothesis: record.marketImpact || 'Requires evaluation',
      targets: [
        { name: 'NotionRelay', channel: channel || 'competitor-intelligence' },
        { name: 'PrimeAgent' },
        { name: 'ClaudeAgent' },
      ],
      context: {
        projectId: record.metadata?.projectId as number | undefined,
        entity: 'competitor-delta',
        metadata: {
          competitorId: record.competitorId,
          briefPath: record.briefPath,
          severity: record.severity,
        },
      },
      priority: record.severity === 'critical' || record.severity === 'high' ? 'high' : 'normal',
    });
  } catch (error: any) {
    logger.error(`Failed to enqueue handoff for competitor delta ${record.id}: ${error.message}`);
  }
}

export async function ingestCompetitorDelta(delta: CompetitorDeltaInput): Promise<CompetitorDeltaRecord> {
  const client = findClient(delta.clientId);
  const competitor = findCompetitor(client, delta.competitorId);

  const timestamp = new Date().toISOString();
  const custodianHash = crypto.createHash('sha256').update(`${delta.clientId}|${delta.competitorId}|${timestamp}|${delta.summary}`).digest('hex');

  const record: CompetitorDeltaRecord = {
    ...delta,
    id: delta.metadata?.deltaId ? String(delta.metadata.deltaId) : `comp_delta_${Date.now()}`,
    timestamp,
    clientName: client?.clientName,
    competitorName: competitor?.name,
    watcherAgents: competitor?.watcherAgents.map((agent) => agent.agent) || [],
    classification: {
      module: 'MAOS',
      plane: 'Intelligence Plane',
      track: 'Web Analysis Agents',
      portal: 'Client Portal',
    },
    custodianHash,
    confidence: normalizeConfidence(delta.confidence),
    briefPath: path.join('competitor-intel', 'briefs', `${delta.clientId.replace(/[^a-zA-Z0-9_-]/g, '_')}-${timestamp.replace(/[:.]/g, '-')}.md`),
  };

  const brief = buildBrief(record);
  persistRecord(record, brief);

  const errors: string[] = [];
  try {
    await routeToTeamwork(record, client?.teamworkTasklistId);
  } catch (error: any) {
    errors.push(`Teamwork routing failed: ${error?.message ?? error}`);
  }
  try {
    await routeToHandoff(record, client?.reflexChannel);
  } catch (error: any) {
    errors.push(`Handoff routing failed: ${error?.message ?? error}`);
  }

  return errors.length > 0 ? { ...record, warnings: errors } : record;
}

export default {
  ingestCompetitorDelta,
  getCompetitorDefinitionMap,
};
