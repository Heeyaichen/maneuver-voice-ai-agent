'use client';

import { useAgentState } from '@livekit/components-react';
import { motion } from 'motion/react';
import { Microphone, Brain, SpeakerHigh } from '@phosphor-icons/react';

export function AgentState() {
  const agentState = useAgentState();

  const stateConfig = {
    listening: {
      icon: Microphone,
      label: 'Listening',
      color: 'text-blue-500',
    },
    thinking: {
      icon: Brain,
      label: 'Thinking',
      color: 'text-purple-500',
    },
    speaking: {
      icon: SpeakerHigh,
      label: 'Speaking',
      color: 'text-green-500',
    },
  };

  const config = stateConfig[agentState as keyof typeof stateConfig];
  if (!config) return null;

  const Icon = config.icon;

  return (
    <motion.div
      initial={{ opacity: 0, y: -10 }}
      animate={{ opacity: 1, y: 0 }}
      className="agent-state-indicator"
    >
      <Icon size={16} weight="fill" className={config.color} />
      <span className="text-sm font-medium">{config.label}</span>
    </motion.div>
  );
}
