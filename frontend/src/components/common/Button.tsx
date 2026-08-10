import React, { ButtonHTMLAttributes, forwardRef } from 'react';
import clsx from 'clsx';
import { Loader2 } from 'lucide-react';

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'ghost' | 'danger';
  size?: 'sm' | 'md' | 'lg';
  isLoading?: boolean;
}

export const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  ({ children, variant = 'primary', size = 'md', isLoading, className, disabled, ...props }, ref) => {
    
    const variants = {
      primary: "bg-primary-DEFAULT hover:bg-primary-DEFAULT/80 text-white shadow-[0_0_15px_rgba(139,92,246,0.3)] hover:shadow-[0_0_20px_rgba(139,92,246,0.5)] border border-white/10",
      secondary: "bg-white/10 hover:bg-white/20 text-white border border-white/10",
      ghost: "bg-transparent hover:bg-white/10 text-slate-300 hover:text-white",
      danger: "bg-red-500/20 hover:bg-red-500/30 text-red-400 border border-red-500/30 hover:shadow-[0_0_15px_rgba(248,113,113,0.3)]"
    };

    const sizes = {
      sm: "px-3 py-1.5 text-sm",
      md: "px-4 py-2",
      lg: "px-6 py-3 text-lg font-medium"
    };

    return (
      <button
        ref={ref}
        disabled={disabled || isLoading}
        className={clsx(
          "relative inline-flex items-center justify-center rounded-xl transition-all duration-200 overflow-hidden outline-none focus:ring-2 focus:ring-primary-DEFAULT focus:ring-offset-2 focus:ring-offset-background",
          variants[variant],
          sizes[size],
          (disabled || isLoading) && "opacity-60 cursor-not-allowed hover:shadow-none hover:bg-opacity-100",
          className
        )}
        {...props}
      >
        {isLoading && <Loader2 className="w-4 h-4 mr-2 animate-spin" />}
        <span className="relative z-10 flex items-center justify-center">{children}</span>
      </button>
    );
  }
);

Button.displayName = 'Button';
