import React, { InputHTMLAttributes, forwardRef } from 'react';
import clsx from 'clsx';

interface InputProps extends InputHTMLAttributes<HTMLInputElement> {
  label: string;
  error?: string;
}

export const Input = forwardRef<HTMLInputElement, InputProps>(
  ({ label, error, className, id, ...props }, ref) => {
    const inputId = id || label.replace(/\s+/g, '-').toLowerCase();

    return (
      <div className="flex flex-col w-full relative">
        <div className="relative group">
          <input
            id={inputId}
            ref={ref}
            placeholder=" "
            className={clsx(
              "peer w-full bg-white/5 border border-white/10 rounded-xl px-4 pt-6 pb-2 text-white placeholder-transparent focus:outline-none focus:border-primary-DEFAULT focus:ring-1 focus:ring-primary-DEFAULT transition-all duration-200",
              error && "border-red-500 focus:border-red-500 focus:ring-red-500",
              className
            )}
            {...props}
          />
          <label
            htmlFor={inputId}
            className={clsx(
              "absolute left-4 top-2 text-xs text-slate-400 transition-all duration-200 pointer-events-none peer-placeholder-shown:text-base peer-placeholder-shown:top-4 peer-focus:top-2 peer-focus:text-xs",
              error ? "text-red-400 peer-focus:text-red-400" : "peer-focus:text-primary-DEFAULT"
            )}
          >
            {label}
          </label>
        </div>
        {error && (
          <span className="text-xs text-red-400 mt-1 ml-1">{error}</span>
        )}
      </div>
    );
  }
);

Input.displayName = 'Input';
