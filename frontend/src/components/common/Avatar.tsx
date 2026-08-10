import React from 'react';
import { clsx } from 'clsx';

interface AvatarProps {
  src?: string | null;
  name?: string;
  size?: 'xs' | 'sm' | 'md' | 'lg' | 'xl';
  isLuna?: boolean;
  className?: string;
}

const sizeMap = {
  xs: 'w-6 h-6 text-xs',
  sm: 'w-8 h-8 text-sm',
  md: 'w-10 h-10 text-base',
  lg: 'w-12 h-12 text-lg',
  xl: 'w-16 h-16 text-xl',
};

function getInitials(name?: string): string {
  if (!name) return 'U';
  const parts = name.trim().split(' ');
  if (parts.length >= 2) return (parts[0][0] + parts[1][0]).toUpperCase();
  return parts[0][0].toUpperCase();
}

const Avatar: React.FC<AvatarProps> = ({
  src,
  name,
  size = 'md',
  isLuna = false,
  className,
}) => {
  if (isLuna) {
    return (
      <div
        className={clsx(
          sizeMap[size],
          'rounded-full bg-gradient-to-br from-violet-500 to-cyan-500 flex items-center justify-center font-bold text-white shadow-lg shadow-violet-500/30 flex-shrink-0',
          className
        )}
      >
        <span style={{ fontSize: '42%' }}>L</span>
      </div>
    );
  }

  if (src) {
    return (
      <img
        src={src}
        alt={name || 'User'}
        className={clsx(sizeMap[size], 'rounded-full object-cover flex-shrink-0', className)}
      />
    );
  }

  return (
    <div
      className={clsx(
        sizeMap[size],
        'rounded-full bg-gradient-to-br from-violet-600 to-indigo-700 flex items-center justify-center font-semibold text-white flex-shrink-0',
        className
      )}
    >
      {getInitials(name)}
    </div>
  );
};

export default Avatar;
