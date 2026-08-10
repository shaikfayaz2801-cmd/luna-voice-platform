import React from 'react';
import { motion } from 'framer-motion';

type VoiceState = 'idle' | 'listening' | 'processing' | 'speaking';

interface VoiceAvatarProps {
  state: VoiceState;
  size?: number;
}

const stateConfig: Record<VoiceState, { color: string; ringColor: string; label: string }> = {
  idle: {
    color: 'from-violet-600 to-indigo-700',
    ringColor: 'rgba(139,92,246,0.2)',
    label: 'Ready',
  },
  listening: {
    color: 'from-violet-500 to-purple-600',
    ringColor: 'rgba(139,92,246,0.5)',
    label: 'Listening...',
  },
  processing: {
    color: 'from-cyan-500 to-blue-600',
    ringColor: 'rgba(6,182,212,0.4)',
    label: 'Thinking...',
  },
  speaking: {
    color: 'from-cyan-400 to-violet-500',
    ringColor: 'rgba(6,182,212,0.5)',
    label: 'Speaking',
  },
};

const VoiceAvatar: React.FC<VoiceAvatarProps> = ({ state, size = 140 }) => {
  const config = stateConfig[state];

  return (
    <div className="relative flex items-center justify-center" style={{ width: size + 80, height: size + 80 }}>
      {/* Outer glow ring */}
      {['speaking', 'listening'].includes(state) && (
        <>
          <motion.div
            className="absolute rounded-full"
            style={{ width: size + 70, height: size + 70, border: `2px solid ${config.ringColor}` }}
            animate={{ scale: [1, 1.15, 1], opacity: [0.4, 0.8, 0.4] }}
            transition={{ duration: 2, repeat: Infinity, ease: 'easeInOut' }}
          />
          <motion.div
            className="absolute rounded-full"
            style={{ width: size + 40, height: size + 40, border: `2px solid ${config.ringColor}` }}
            animate={{ scale: [1, 1.1, 1], opacity: [0.6, 1, 0.6] }}
            transition={{ duration: 1.5, repeat: Infinity, ease: 'easeInOut', delay: 0.3 }}
          />
        </>
      )}

      {/* Processing spinner */}
      {state === 'processing' && (
        <motion.div
          className="absolute rounded-full border-2 border-transparent border-t-cyan-400"
          style={{ width: size + 20, height: size + 20 }}
          animate={{ rotate: 360 }}
          transition={{ duration: 1, repeat: Infinity, ease: 'linear' }}
        />
      )}

      {/* Avatar circle */}
      <motion.div
        className={`relative rounded-full bg-gradient-to-br ${config.color} flex items-center justify-center shadow-2xl cursor-pointer select-none`}
        style={{ width: size, height: size }}
        animate={
          state === 'speaking'
            ? { scale: [1, 1.04, 1], boxShadow: [`0 0 40px ${config.ringColor}`, `0 0 80px ${config.ringColor}`, `0 0 40px ${config.ringColor}`] }
            : state === 'listening'
            ? { scale: [1, 1.02, 1] }
            : { scale: 1 }
        }
        transition={{ duration: 1.2, repeat: Infinity, ease: 'easeInOut' }}
        whileHover={{ scale: 1.05 }}
        whileTap={{ scale: 0.97 }}
      >
        {/* Luna "L" letter */}
        <span
          className="font-bold text-white select-none"
          style={{ fontSize: size * 0.38, letterSpacing: '-0.02em', fontFamily: 'Inter, sans-serif' }}
        >
          L
        </span>

        {/* Shine overlay */}
        <div
          className="absolute inset-0 rounded-full opacity-20"
          style={{ background: 'linear-gradient(135deg, rgba(255,255,255,0.4) 0%, transparent 60%)' }}
        />
      </motion.div>
    </div>
  );
};

export default VoiceAvatar;
