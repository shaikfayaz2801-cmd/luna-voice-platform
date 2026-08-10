import React, { useRef, useEffect } from 'react';
import { motion } from 'framer-motion';

interface VoiceVisualizerProps {
  isActive: boolean;
  audioLevel?: number; // 0-1
  mode: 'listening' | 'speaking' | 'idle';
}

const VoiceVisualizer: React.FC<VoiceVisualizerProps> = ({
  isActive,
  audioLevel = 0,
  mode,
}) => {
  const BAR_COUNT = 32;

  const getBarHeight = (index: number, level: number): number => {
    if (!isActive || mode === 'idle') return 4;
    const center = BAR_COUNT / 2;
    const distFromCenter = Math.abs(index - center) / center;
    const base = mode === 'speaking' ? 0.5 : 0.3;
    const wave = Math.sin((index / BAR_COUNT) * Math.PI * 3 + Date.now() / 200) * 0.3;
    return Math.max(4, (base + wave + level * 0.4) * (1 - distFromCenter * 0.5) * 80);
  };

  const colorMap = {
    listening: '#8b5cf6',
    speaking: '#06b6d4',
    idle: '#334155',
  };

  return (
    <div className="flex items-center justify-center gap-[3px] h-20 w-full">
      {Array.from({ length: BAR_COUNT }, (_, i) => (
        <motion.div
          key={i}
          className="rounded-full"
          style={{
            width: 3,
            backgroundColor: colorMap[mode],
            opacity: isActive ? 0.85 : 0.3,
          }}
          animate={{
            height: isActive
              ? [
                  getBarHeight(i, audioLevel),
                  getBarHeight(i, audioLevel * 1.2),
                  getBarHeight(i, audioLevel * 0.8),
                ]
              : 4,
            opacity: isActive ? [0.6, 1, 0.7] : 0.3,
          }}
          transition={{
            duration: isActive ? 0.4 + (i % 5) * 0.08 : 0.3,
            repeat: isActive ? Infinity : 0,
            repeatType: 'mirror',
            ease: 'easeInOut',
            delay: i * 0.02,
          }}
        />
      ))}
    </div>
  );
};

export default VoiceVisualizer;
