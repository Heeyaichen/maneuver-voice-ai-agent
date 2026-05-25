'use client';

import { AnimatePresence, motion } from 'motion/react';

interface LeadPanelProps {
  leadData: { [key: string]: string | null };
}

const FIELD_LABELS: { [key: string]: string } = {
  name: 'Name',
  company: 'Company',
  role: 'Role',
  problem: 'Challenge',
  business_metrics: 'Business Metrics',
  ai_context: 'AI Context',
  timeline: 'Timeline',
  budget: 'Budget',
  current_solutions: 'Current Solutions',
};

export function LeadPanel({ leadData }: LeadPanelProps) {
  const fields = Object.entries(leadData).filter(([, value]) => value);

  return (
    <motion.div
      initial={{ opacity: 0, x: 20 }}
      animate={{ opacity: 1, x: 0 }}
      className="lead-panel"
    >
      <h3 className="text-muted-foreground mb-3 text-sm font-semibold">Discovery Info</h3>
      <div className="space-y-2">
        <AnimatePresence mode="popLayout">
          {fields.map(([field, value]) => (
            <motion.div
              key={field}
              initial={{ opacity: 0, y: -10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.2 }}
              className="lead-field"
            >
              <div className="text-muted-foreground text-xs font-medium">
                {FIELD_LABELS[field] || field}
              </div>
              <div className="mt-0.5 text-sm">{value}</div>
            </motion.div>
          ))}
        </AnimatePresence>
      </div>
    </motion.div>
  );
}
