'use client';

import { motion } from 'motion/react';
import { ChartLine, CloudArrowUp, Microphone, Robot, TestTube } from '@phosphor-icons/react';

const SERVICES = [
  {
    icon: Robot,
    title: 'Agentic AI Systems',
    description: 'Autonomous agents that handle real business workflows',
  },
  {
    icon: ChartLine,
    title: 'Multimodal AI Platforms',
    description: 'Systems that work across text, voice, vision, and data',
  },
  {
    icon: TestTube,
    title: 'AI Evaluation Frameworks',
    description: 'Testing and validation for production AI',
  },
  {
    icon: CloudArrowUp,
    title: 'Enterprise-Grade Deployment',
    description: 'Scalable, reliable AI infrastructure',
  },
  {
    icon: Microphone,
    title: 'Voice AI Solutions',
    description: 'Conversational AI for customer service and sales',
  },
];

export function ServicesSlide() {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
      className="services-slide"
    >
      <h2 className="mb-6 text-2xl font-semibold">Our Services</h2>
      <div className="services-grid">
        {SERVICES.map((service, index) => {
          const Icon = service.icon;
          return (
            <motion.div
              key={service.title}
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ delay: index * 0.08, duration: 0.2 }}
              className="service-card"
            >
              <Icon size={32} weight="duotone" className="text-primary mb-3" />
              <h3 className="mb-2 font-semibold">{service.title}</h3>
              <p className="text-muted-foreground text-sm">{service.description}</p>
            </motion.div>
          );
        })}
      </div>
    </motion.div>
  );
}
