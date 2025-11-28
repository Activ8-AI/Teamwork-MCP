export interface CompetitorAsset {
  type: 'website' | 'pricing' | 'blog' | 'adLibrary' | 'social' | 'seo' | 'ppc' | 'press' | 'product' | 'other';
  url: string;
  cadence?: string;
  notes?: string;
}

export interface CompetitorWatcherAssignment {
  agent: string;
  responsibilities: string[];
  triggers?: string[];
  outputs?: string[];
}

export interface CompetitorDefinition {
  id: string;
  name: string;
  aliases?: string[];
  segment: string;
  watchlist: CompetitorAsset[];
  watcherAgents: CompetitorWatcherAssignment[];
  keywords?: string[];
  revenueTier?: 'seed' | 'growth' | 'enterprise';
  notes?: string;
}

export interface ClientCompetitorProfile {
  clientId: string;
  clientName: string;
  industry: string;
  tier: 'tier1' | 'tier2' | 'tier3';
  portalSlug: string;
  teamworkTasklistId?: string;
  reflexChannel?: string;
  notionPageId?: string;
  guardian?: string;
  riskOwner?: string;
  competitors: CompetitorDefinition[];
  alerts?: Array<{
    type: string;
    threshold: string;
    severity: 'info' | 'yellow' | 'red';
  }>;
  dataSources?: Record<string, string>;
  portalViews?: Array<{
    tab: string;
    description: string;
    widgets: string[];
  }>;
}
