'use client';

import { motion, AnimatePresence } from 'motion/react';

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
  const fields = Object.entries(leadData).filter(([_, value]) => value);

  return (
    <motion.div
      initial={{ opacity: 0, x: 20 }}
      animate={{ opacity: 1, x: 0 }}
      className="lead-panel"
    >
      <h3 className="text-sm font-semibold mb-3 text-muted-foreground">
        Discovery Info
      </h3>
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
              <div className="text-xs font-medium text-muted-foreground">
                {FIELD_LABELS[field] || field}
              </div>
              <div className="text-sm mt-0.5">{value}</div>
            </motion.div>
          ))}
        </AnimatePresence>
      </div>
    </motion.div>
  );
}
