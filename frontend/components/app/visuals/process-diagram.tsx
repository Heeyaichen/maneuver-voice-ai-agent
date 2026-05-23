'use client';

import { motion } from 'motion/react';
import { ArrowRight } from '@phosphor-icons/react';

const PROCESS_STEPS = [
  {
    number: 1,
    title: 'Discovery',
    duration: '30 min',
    description: 'Understand your business metrics and AI opportunity',
  },
  {
    number: 2,
    title: 'Technical Audit',
    duration: '1 week',
    description: 'Review current systems, data, and readiness',
  },
  {
    number: 3,
    title: 'Implementation',
    duration: '2-4 weeks',
    description: 'Build and deploy AI solution',
  },
  {
    number: 4,
    title: 'Handoff',
    duration: 'Ongoing',
    description: 'Your team owns it, we support as needed',
  },
];

export function ProcessDiagram() {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
      className="process-diagram"
    >
      <h2 className="text-2xl font-semibold mb-6">Our Process</h2>
      <div className="process-steps">
        {PROCESS_STEPS.map((step, index) => (
          <div key={step.number} className="flex items-center">
            <motion.div
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: index * 0.15, duration: 0.3 }}
              className="process-step"
            >
              <div className="step-number">{step.number}</div>
              <div className="step-content">
                <h3 className="font-semibold">{step.title}</h3>
                <div className="text-xs text-muted-foreground mb-1">{step.duration}</div>
                <p className="text-sm text-muted-foreground">{step.description}</p>
              </div>
            </motion.div>
            {index < PROCESS_STEPS.length - 1 && (
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: index * 0.15 + 0.1 }}
                className="mx-4"
              >
                <ArrowRight size={24} className="text-muted-foreground" />
              </motion.div>
            )}
          </div>
        ))}
      </div>
    </motion.div>
  );
}
