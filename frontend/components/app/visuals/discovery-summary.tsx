'use client';

import { motion } from 'motion/react';
import { CheckCircle } from '@phosphor-icons/react';

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

interface DiscoverySummaryProps {
  data: DiscoveryData;
}

export function DiscoverySummary({ data }: DiscoverySummaryProps) {
  const fields = [
    { label: 'Name', value: data.name },
    { label: 'Company', value: data.company },
    { label: 'Role', value: data.role },
    { label: 'Challenge', value: data.problem },
    { label: 'Business Metrics', value: data.business_metrics },
    { label: 'Timeline', value: data.timeline },
    { label: 'Budget', value: data.budget },
    { label: 'Current Solutions', value: data.current_solutions },
  ].filter((f) => f.value);

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ duration: 0.3 }}
      className="discovery-summary"
    >
      <div className="mb-4 flex items-center gap-2">
        <CheckCircle size={24} weight="fill" className="text-green-500" />
        <h2 className="text-xl font-semibold">Discovery Complete</h2>
      </div>

      <div className="summary-grid">
        {fields.map((field, index) => (
          <motion.div
            key={field.label}
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.05, duration: 0.2 }}
            className="summary-field"
          >
            <div className="text-muted-foreground text-sm font-medium">{field.label}</div>
            <div className="mt-1 text-base">{field.value}</div>
          </motion.div>
        ))}
      </div>

      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.4 }}
        className="bg-muted/50 mt-6 rounded-lg p-4"
      >
        <p className="text-muted-foreground text-sm">
          Thanks for sharing! We&apos;ll follow up within 24 hours to discuss next steps.
        </p>
      </motion.div>
    </motion.div>
  );
}
