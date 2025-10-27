import React, { forwardRef } from 'react';
import { designTokens, semanticTokens } from './tokens';

// Componente Button base
export const Button = forwardRef(({
  children,
  variant = 'primary',
  size = 'md',
  disabled = false,
  loading = false,
  leftIcon,
  rightIcon,
  className = '',
  ...props
}, ref) => {
  const baseClasses = 'inline-flex items-center justify-center font-medium rounded-lg transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed';
  
  const variants = {
    primary: 'bg-primary-600 hover:bg-primary-700 text-white focus:ring-primary-500',
    secondary: 'bg-neutral-200 hover:bg-neutral-300 text-neutral-800 focus:ring-neutral-500',
    outline: 'border border-neutral-300 hover:bg-neutral-50 text-neutral-700 focus:ring-primary-500',
    ghost: 'hover:bg-neutral-100 text-neutral-700 focus:ring-primary-500',
    danger: 'bg-error-600 hover:bg-error-700 text-white focus:ring-error-500',
    success: 'bg-success-600 hover:bg-success-700 text-white focus:ring-success-500',
  };

  const sizes = {
    xs: 'px-2 py-1 text-xs',
    sm: 'px-3 py-1.5 text-sm',
    md: 'px-4 py-2 text-sm',
    lg: 'px-6 py-3 text-base',
    xl: 'px-8 py-4 text-lg',
  };

  const classes = `${baseClasses} ${variants[variant]} ${sizes[size]} ${className}`;

  return (
    <button
      ref={ref}
      className={classes}
      disabled={disabled || loading}
      aria-disabled={disabled || loading}
      {...props}
    >
      {loading && (
        <svg className="animate-spin -ml-1 mr-2 h-4 w-4" fill="none" viewBox="0 0 24 24">
          <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
          <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
        </svg>
      )}
      {leftIcon && !loading && <span className="mr-2">{leftIcon}</span>}
      {children}
      {rightIcon && !loading && <span className="ml-2">{rightIcon}</span>}
    </button>
  );
});

Button.displayName = 'Button';

// Componente Input base
export const Input = forwardRef(({
  label,
  error,
  helperText,
  leftIcon,
  rightIcon,
  className = '',
  ...props
}, ref) => {
  const inputClasses = `
    w-full px-3 py-2 border rounded-lg transition-colors duration-200
    focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent
    disabled:bg-neutral-100 disabled:cursor-not-allowed
    ${error ? 'border-error-300 focus:ring-error-500' : 'border-neutral-300'}
    ${leftIcon ? 'pl-10' : ''}
    ${rightIcon ? 'pr-10' : ''}
    ${className}
  `;

  return (
    <div className="space-y-1">
      {label && (
        <label className="block text-sm font-medium text-neutral-700">
          {label}
        </label>
      )}
      <div className="relative">
        {leftIcon && (
          <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
            <span className="text-neutral-400">{leftIcon}</span>
          </div>
        )}
        <input
          ref={ref}
          className={inputClasses}
          aria-invalid={error ? 'true' : 'false'}
          aria-describedby={error ? `${props.id}-error` : helperText ? `${props.id}-helper` : undefined}
          {...props}
        />
        {rightIcon && (
          <div className="absolute inset-y-0 right-0 pr-3 flex items-center pointer-events-none">
            <span className="text-neutral-400">{rightIcon}</span>
          </div>
        )}
      </div>
      {error && (
        <p id={`${props.id}-error`} className="text-sm text-error-600" role="alert">
          {error}
        </p>
      )}
      {helperText && !error && (
        <p id={`${props.id}-helper`} className="text-sm text-neutral-500">
          {helperText}
        </p>
      )}
    </div>
  );
});

Input.displayName = 'Input';

// Componente Card base
export const Card = forwardRef(({
  children,
  padding = 'md',
  shadow = 'sm',
  className = '',
  ...props
}, ref) => {
  const paddingClasses = {
    none: '',
    sm: 'p-4',
    md: 'p-6',
    lg: 'p-8',
  };

  const shadowClasses = {
    none: '',
    sm: 'shadow-sm',
    md: 'shadow-md',
    lg: 'shadow-lg',
  };

  const classes = `
    bg-white rounded-lg border border-neutral-200
    ${paddingClasses[padding]}
    ${shadowClasses[shadow]}
    ${className}
  `;

  return (
    <div ref={ref} className={classes} {...props}>
      {children}
    </div>
  );
});

Card.displayName = 'Card';

// Componente Badge
export const Badge = forwardRef(({
  children,
  variant = 'neutral',
  size = 'sm',
  className = '',
  ...props
}, ref) => {
  const baseClasses = 'inline-flex items-center font-medium rounded-full';
  
  const variants = {
    neutral: 'bg-neutral-100 text-neutral-800',
    primary: 'bg-primary-100 text-primary-800',
    success: 'bg-success-100 text-success-800',
    warning: 'bg-warning-100 text-warning-800',
    error: 'bg-error-100 text-error-800',
  };

  const sizes = {
    xs: 'px-2 py-0.5 text-xs',
    sm: 'px-2.5 py-0.5 text-xs',
    md: 'px-3 py-1 text-sm',
  };

  const classes = `${baseClasses} ${variants[variant]} ${sizes[size]} ${className}`;

  return (
    <span ref={ref} className={classes} {...props}>
      {children}
    </span>
  );
});

Badge.displayName = 'Badge';

// Componente Loading Spinner
export const Spinner = ({ size = 'md', className = '' }) => {
  const sizes = {
    xs: 'h-3 w-3',
    sm: 'h-4 w-4',
    md: 'h-6 w-6',
    lg: 'h-8 w-8',
    xl: 'h-12 w-12',
  };

  return (
    <svg
      className={`animate-spin text-primary-600 ${sizes[size]} ${className}`}
      fill="none"
      viewBox="0 0 24 24"
      role="status"
      aria-label="Carregando"
    >
      <circle
        className="opacity-25"
        cx="12"
        cy="12"
        r="10"
        stroke="currentColor"
        strokeWidth="4"
      />
      <path
        className="opacity-75"
        fill="currentColor"
        d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
      />
    </svg>
  );
};

// Componente Alert
export const Alert = forwardRef(({
  children,
  variant = 'info',
  title,
  className = '',
  ...props
}, ref) => {
  const variants = {
    info: 'bg-primary-50 border-primary-200 text-primary-800',
    success: 'bg-success-50 border-success-200 text-success-800',
    warning: 'bg-warning-50 border-warning-200 text-warning-800',
    error: 'bg-error-50 border-error-200 text-error-800',
  };

  const icons = {
    info: 'ℹ️',
    success: '✅',
    warning: '⚠️',
    error: '❌',
  };

  const classes = `
    border rounded-lg p-4
    ${variants[variant]}
    ${className}
  `;

  return (
    <div ref={ref} className={classes} role="alert" {...props}>
      <div className="flex">
        <div className="flex-shrink-0">
          <span className="text-lg">{icons[variant]}</span>
        </div>
        <div className="ml-3">
          {title && (
            <h3 className="text-sm font-medium mb-1">
              {title}
            </h3>
          )}
          <div className="text-sm">
            {children}
          </div>
        </div>
      </div>
    </div>
  );
});

Alert.displayName = 'Alert';

