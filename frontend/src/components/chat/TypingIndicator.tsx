import React from 'react';
import { motion } from 'framer-motion';

const TypingIndicator: React.FC = () => {
  return (
    <div className="flex items-end gap-3 px-2">
      {/* Luna avatar */}
      <div className="w-8 h-8 rounded-full bg-gradient-to-br from-violet-500 to-cyan-500 flex items-center justify-center text-white text-xs font-bold flex-shrink-0 shadow-lg shadow-violet-500/20">
        L
      </div>

      {/* Bubble */}
      <motion.div
        className="flex items-center gap-1.5 px-4 py-3 rounded-2xl rounded-bl-sm bg-white/5 border border-white/10 backdrop-blur-sm"
        initial={{ opacity: 0, y: 8, scale: 0.95 }}
        animate={{ opacity: 1, y: 0, scale: 1 }}
        exit={{ opacity: 0, scale: 0.95 }}
        transition={{ type: 'spring', damping: 20, stiffness: 300 }}
      >
        {[0, 1, 2].map((i) => (
          <motion.span
            key={i}
            className="block w-2 h-2 rounded-full bg-violet-400"
            animate={{
              y: [0, -6, 0],
              opacity: [0.5, 1, 0.5],
            }}
            transition={{
              duration: 0.8,
              repeat: Infinity,
              delay: i * 0.15,
              ease: 'easeInOut',
            }}
          />
        ))}
      </motion.div>
    </div>
  );
};

export default TypingIndicator;
