"use client";

import * as React from 'react';
import { cn } from '@/lib/utils';

interface CheckboxProps extends React.ComponentPropsWithoutRef<'button'> {
  checked: boolean;
  onCheckedChange: (checked: boolean) => void;
}

const Checkbox = React.forwardRef<HTMLButtonElement, CheckboxProps>(
  ({ className, checked, onCheckedChange, ...props }, ref) => {
    return (
      <button
        type="button"
        className={cn(
          'peer h-5 w-5 shrink-0 rounded-sm border border-primary ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50',
          checked ? 'bg-primary text-primary-foreground' : 'bg-transparent',
          className
        )}
        aria-checked={checked}
        role="checkbox"
        onClick={() => onCheckedChange(!checked)}
        ref={ref}
        {...props}
      >
        {checked && (
          <div className="flex items-center justify-center text-current">
            <svg viewBox="0 0 16 16" fill="currentColor" className="h-4 w-4">
              <path d="M12.207 4.793a1 1 0 010 1.414l-5 5a1 1 0 01-1.414 0l-2-2a1 1 0 011.414-1.414L6.5 9.086l4.293-4.293a1 1 0 011.414 0z" />
            </svg>
          </div>
        )}
      </button>
    );
  }
);

Checkbox.displayName = 'Checkbox';

export { Checkbox };
