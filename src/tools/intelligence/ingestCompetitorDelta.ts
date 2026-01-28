import logger from "../../utils/logger.js";
import teamworkService from "../../services/index.js";
import type { CompetitorDeltaInput } from "../../models/CompetitorDelta.js";

export const ingestCompetitorDeltaDefinition = {
  name: "ingestCompetitorDelta",
  description: "Install a competitor intelligence delta into the MAOS Intelligence Plane. Generates a charter brief, triggers Reflex pipelines, and creates Teamwork action tasks when configured.",
  inputSchema: {
    type: "object",
    required: ["clientId", "competitorId", "signalType", "summary"],
    properties: {
      clientId: {
        type: "string",
        description: "Client identifier that maps to the Competitor Definition Map.",
      },
      competitorId: {
        type: "string",
        description: "Competitor identifier under the selected client.",
      },
      signalType: {
        type: "string",
        description: "Type of external signal that was detected.",
        enum: ["pricing", "product", "campaign", "seo", "ppc", "social", "sentiment", "partnership", "talent", "regulatory", "other"],
      },
      summary: {
        type: "string",
        description: "Two to three sentence synopsis of the detected move.",
      },
      evidenceUrl: {
        type: "string",
        description: "Source URL validating the signal.",
      },
      evidenceSnippet: {
        type: "string",
        description: "Quoted excerpt or data point from the source.",
      },
      severity: {
        type: "string",
        enum: ["info", "low", "medium", "high", "critical"],
        description: "Operational severity to drive Reflex priority.",
      },
      marketImpact: {
        type: "string",
        description: "Describe anticipated category or revenue impact.",
      },
      strategicImplication: {
        type: "string",
        description: "Why this matters for the client’s positioning.",
      },
      recommendedActions: {
        type: "array",
        items: { type: "string" },
        description: "Actionable directives that should be pushed into Teamwork.",
      },
      governanceNotes: {
        type: "string",
        description: "Controls, risk notes, or TAO references.",
      },
      confidence: {
        type: "number",
        minimum: 0,
        maximum: 1,
        description: "Confidence score (0-1). Defaults to 0.72 if omitted.",
      },
      metadata: {
        type: "object",
        description: "Additional structured context (e.g., projectId, channel, scraping batch).",
        additionalProperties: true,
      },
      tags: {
        type: "array",
        items: { type: "string" },
        description: "Optional tags used for Portal filtering.",
      },
      revenueImpact: {
        type: "number",
        description: "Estimated revenue delta in USD.",
      },
      actionOwner: {
        type: "string",
        description: "Primary owner or team expected to respond.",
      },
    },
  },
  annotations: {
    title: "Competitor Intelligence Delta Intake",
    readOnlyHint: false,
    destructiveHint: false,
    idempotentHint: false,
    openWorldHint: true,
  },
};

export async function handleIngestCompetitorDelta(input: CompetitorDeltaInput) {
  try {
    const record = await teamworkService.ingestCompetitorDelta(input);
    return {
      content: [
        {
          type: "text",
          text: JSON.stringify(record, null, 2),
        },
      ],
    };
  } catch (error: any) {
    logger.error(`ingestCompetitorDelta tool failed: ${error.message}`);
    return {
      content: [
        {
          type: "text",
          text: `Failed to ingest competitor delta: ${error.message}`,
        },
      ],
    };
  }
}
