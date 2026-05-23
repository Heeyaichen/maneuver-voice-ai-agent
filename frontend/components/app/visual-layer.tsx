'use client';

import { useEffect, useState } from 'react';
import { useLocalParticipant } from '@livekit/components-react';
import { ServicesSlide } from './visuals/services-slide';
import { ProcessDiagram } from './visuals/process-diagram';
import { LeadPanel } from './visuals/lead-panel';
import { DiscoverySummary } from './visuals/discovery-summary';
import { AgentState } from './visuals/agent-state';

type VisualMode = 'idle' | 'services' | 'process' | 'summary';

interface LeadData {
  [key: string]: string | null;
}

interface DiscoveryData {
  timestamp: string;
  name: string | null;
  company: string | null;
  role: string | null;
  problem: string | null;
  business_metrics: string | null;
  ai_context: string | null;
  timeline: string | null;
  budget: string | null;
  current_solutions: string | null;
  additional_notes: string[];
}

export function VisualLayer() {
  const { localParticipant } = useLocalParticipant();
  const [visualMode, setVisualMode] = useState<VisualMode>('idle');
  const [leadData, setLeadData] = useState<LeadData>({});
  const [discoveryData, setDiscoveryData] = useState<DiscoveryData | null>(null);

  useEffect(() => {
    if (!localParticipant) return;

    // Register RPC method handlers
    localParticipant.registerRpcMethod(
      'updateLeadField',
      async (data: string) => {
        try {
          const { field, value } = JSON.parse(data);
          console.log('[RPC] updateLeadField:', field, value);
          
          // Optimistic rendering - update immediately
          setLeadData((prev) => ({
            ...prev,
            [field]: value,
          }));
          
          return JSON.stringify({ success: true });
        } catch (error) {
          console.error('[RPC] updateLeadField error:', error);
          return JSON.stringify({ success: false, error: String(error) });
        }
      }
    );

    localParticipant.registerRpcMethod(
      'showServicesSlide',
      async () => {
        console.log('[RPC] showServicesSlide');
        setVisualMode('services');
        return JSON.stringify({ success: true });
      }
    );

    localParticipant.registerRpcMethod(
      'showProcessDiagram',
      async () => {
        console.log('[RPC] showProcessDiagram');
        setVisualMode('process');
        return JSON.stringify({ success: true });
      }
    );

    localParticipant.registerRpcMethod(
      'showDiscoverySummary',
      async (data: string) => {
        try {
          const summary = JSON.parse(data);
          console.log('[RPC] showDiscoverySummary:', summary);
          setDiscoveryData(summary);
          setVisualMode('summary');
          return JSON.stringify({ success: true });
        } catch (error) {
          console.error('[RPC] showDiscoverySummary error:', error);
          return JSON.stringify({ success: false, error: String(error) });
        }
      }
    );

    return () => {
      // Cleanup RPC handlers
      localParticipant.unregisterRpcMethod('updateLeadField');
      localParticipant.unregisterRpcMethod('showServicesSlide');
      localParticipant.unregisterRpcMethod('showProcessDiagram');
      localParticipant.unregisterRpcMethod('showDiscoverySummary');
    };
  }, [localParticipant]);

  return (
    <div className="visual-layer-container">
      {/* Agent State Indicator */}
      <AgentState />

      {/* Lead Panel - Always visible during conversation */}
      {Object.keys(leadData).length > 0 && visualMode !== 'summary' && (
        <LeadPanel leadData={leadData} />
      )}

      {/* Dynamic Visual Content */}
      <div className="visual-content">
        {visualMode === 'services' && <ServicesSlide />}
        {visualMode === 'process' && <ProcessDiagram />}
        {visualMode === 'summary' && discoveryData && (
          <DiscoverySummary data={discoveryData} />
        )}
      </div>
    </div>
  );
}
