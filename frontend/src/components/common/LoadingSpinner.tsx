import React from 'react';
import { motion } from 'framer-motion';
import { clsx } from 'clsx';

interface LoadingSpinnerProps {
  size?: 'sm' | 'md' | 'lg';
  color?: 'violet' | 'cyan' | 'white';
  label?: string;
  fullScreen?: boolean;
}

const sizeMap = { sm: 16, md: 28, lg: 48 };

const colorMap = {
  violet: '#8b5cf6',
  cyan: '#06b6d4',
  white: '#ffffff',
};

const LoadingSpinner: React.FC<LoadingSpinnerProps> = ({
  size = 'md',
  color = 'violet',
  label,
  fullScreen = false,
}) => {
  const px = sizeMap[size];
  const stroke = colorMap[color];

  const spinner = (
    <div className="flex flex-col items-center gap-3">
      <motion.svg
        width={px}
        height={px}
        viewBox="0 0 24 24"
        fill="none"
        animate={{ rotate: 360 }}
        transition={{ duration: 0.9, repeat: Infinity, ease: 'linear' }}
      >
        <circle
          cx="12" cy="12" r="10"
          stroke={stroke}
          strokeWidth="2.5"
          strokeOpacity="0.2"
        />
        <path
          d="M12 2 A10 10 0 0 1 22 12"
          stroke={stroke}
          strokeWidth="2.5"
          strokeLinecap="round"
        />
      </motion.svg>
      {label && <p className="text-sm text-slate-400">{label}</p>}
    </div>
  );

  if (fullScreen) {
    return (
      <div className="fixed inset-0 z-50 flex items-center justify-center bg-[#0a0a14]">
        {spinner}
      </div>
    );
  }

  return spinner;
};

export default LoadingSpinner;
