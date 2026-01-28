export type CompetitorSignalType =
  | 'pricing'
  | 'product'
  | 'campaign'
  | 'seo'
  | 'ppc'
  | 'social'
  | 'sentiment'
  | 'partnership'
  | 'talent'
  | 'regulatory'
  | 'other';

export interface CompetitorDeltaInput {
  clientId: string;
  competitorId: string;
  signalType: CompetitorSignalType;
  summary: string;
  evidenceUrl?: string;
  evidenceSnippet?: string;
  severity?: 'info' | 'low' | 'medium' | 'high' | 'critical';
  marketImpact?: string;
  strategicImplication?: string;
  recommendedActions?: string[];
  governanceNotes?: string;
  confidence?: number;
  metadata?: Record<string, unknown>;
  tags?: string[];
  revenueImpact?: number;
  actionOwner?: string;
}

export interface CompetitorDeltaRecord extends CompetitorDeltaInput {
  id: string;
  timestamp: string;
  clientName?: string;
  competitorName?: string;
  classification: {
    module: 'MAOS';
    plane: 'Intelligence Plane';
    track: 'Web Analysis Agents';
    portal: 'Client Portal';
  };
  watcherAgents: string[];
  briefPath: string;
  custodianHash: string;
  warnings?: string[];
}