import React, { forwardRef } from 'react';
import { cva } from 'class-variance-authority';
import cn from './cn.js';

// Button com variantes avançadas
const buttonVariants = cva(
  "inline-flex items-center justify-center whitespace-nowrap rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50",
  {
    variants: {
      variant: {
        default: "bg-primary text-primary-foreground hover:bg-primary/90",
        destructive: "bg-destructive text-destructive-foreground hover:bg-destructive/90",
        outline: "border border-input bg-background hover:bg-accent hover:text-accent-foreground",
        secondary: "bg-secondary text-secondary-foreground hover:bg-secondary/80",
        ghost: "hover:bg-accent hover:text-accent-foreground",
        link: "text-primary underline-offset-4 hover:underline",
        gradient: "bg-gradient-to-r from-primary to-primary/80 text-primary-foreground hover:from-primary/90 hover:to-primary/70 shadow-lg hover:shadow-xl",
        glass: "bg-white/10 backdrop-blur-md border border-white/20 text-white hover:bg-white/20",
      },
      size: {
        default: "h-10 px-4 py-2",
        sm: "h-9 rounded-md px-3",
        lg: "h-11 rounded-md px-8",
        xl: "h-12 rounded-lg px-10 text-base",
        icon: "h-10 w-10",
      },
    },
    defaultVariants: {
      variant: "default",
      size: "default",
    },
  }
);

export const Button = forwardRef(({ 
  className, 
  variant, 
  size, 
  children, 
  loading = false,
  leftIcon,
  rightIcon,
  ...props 
}, ref) => {
  return (
    <button
      className={cn(buttonVariants({ variant, size, className }))}
      ref={ref}
      disabled={loading}
      {...props}
    >
      {loading && (
        <svg className="mr-2 h-4 w-4 animate-spin" fill="none" viewBox="0 0 24 24">
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

Button.displayName = "Button";

// Card moderno com glassmorphism
const cardVariants = cva(
  "rounded-xl border bg-card text-card-foreground shadow-sm transition-all duration-300 hover:shadow-md",
  {
    variants: {
      variant: {
        default: "bg-white border-border",
        glass: "bg-white/80 backdrop-blur-md border-white/20",
        gradient: "bg-gradient-to-br from-white to-gray-50 border-border",
        elevated: "bg-white border-border shadow-lg hover:shadow-xl",
      },
      padding: {
        none: "",
        sm: "p-4",
        default: "p-6",
        lg: "p-8",
      },
    },
    defaultVariants: {
      variant: "default",
      padding: "default",
    },
  }
);

export const Card = forwardRef(({ className, variant, padding, children, ...props }, ref) => (
  <div ref={ref} className={cn(cardVariants({ variant, padding, className }))} {...props}>
    {children}
  </div>
));

Card.displayName = "Card";

// Input moderno com animações
const inputVariants = cva(
  "flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50 transition-all duration-200",
  {
    variants: {
      variant: {
        default: "border-input",
        ghost: "border-transparent bg-transparent",
        filled: "bg-muted border-muted",
      },
      size: {
        default: "h-10",
        sm: "h-8 text-xs",
        lg: "h-12 text-base",
      },
    },
    defaultVariants: {
      variant: "default",
      size: "default",
    },
  }
);

export const Input = forwardRef(({ 
  className, 
  variant, 
  size, 
  type = "text", 
  leftIcon,
  rightIcon,
  error,
  label,
  helperText,
  ...props 
}, ref) => {
  const inputId = React.useId();
  
  return (
    <div className="space-y-2">
      {label && (
        <label 
          htmlFor={inputId}
          className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
        >
          {label}
        </label>
      )}
      <div className="relative">
        {leftIcon && (
          <div className="absolute left-3 top-1/2 transform -translate-y-1/2 text-muted-foreground">
            {leftIcon}
          </div>
        )}
        <input
          id={inputId}
          type={type}
          className={cn(
            inputVariants({ variant, size }),
            leftIcon && "pl-10",
            rightIcon && "pr-10",
            error && "border-destructive focus-visible:ring-destructive",
            className
          )}
          ref={ref}
          aria-invalid={error ? "true" : "false"}
          aria-describedby={error ? `${inputId}-error` : helperText ? `${inputId}-helper` : undefined}
          {...props}
        />
        {rightIcon && (
          <div className="absolute right-3 top-1/2 transform -translate-y-1/2 text-muted-foreground">
            {rightIcon}
          </div>
        )}
      </div>
      {error && (
        <p id={`${inputId}-error`} className="text-sm text-destructive" role="alert">
          {error}
        </p>
      )}
      {helperText && !error && (
        <p id={`${inputId}-helper`} className="text-sm text-muted-foreground">
          {helperText}
        </p>
      )}
    </div>
  );
});

Input.displayName = "Input";

// Badge moderno
const badgeVariants = cva(
  "inline-flex items-center rounded-full border px-2.5 py-0.5 text-xs font-semibold transition-colors focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2",
  {
    variants: {
      variant: {
        default: "border-transparent bg-primary text-primary-foreground hover:bg-primary/80",
        secondary: "border-transparent bg-secondary text-secondary-foreground hover:bg-secondary/80",
        destructive: "border-transparent bg-destructive text-destructive-foreground hover:bg-destructive/80",
        outline: "text-foreground",
        success: "border-transparent bg-green-500 text-white hover:bg-green-600",
        warning: "border-transparent bg-yellow-500 text-white hover:bg-yellow-600",
        info: "border-transparent bg-blue-500 text-white hover:bg-blue-600",
      },
    },
    defaultVariants: {
      variant: "default",
    },
  }
);

export const Badge = forwardRef(({ className, variant, ...props }, ref) => {
  return (
    <div ref={ref} className={cn(badgeVariants({ variant }), className)} {...props} />
  );
});

Badge.displayName = "Badge";

// Skeleton loading
export const Skeleton = forwardRef(({ className, ...props }, ref) => (
  <div
    ref={ref}
    className={cn("animate-pulse rounded-md bg-muted", className)}
    {...props}
  />
));

Skeleton.displayName = "Skeleton";

// Separator
export const Separator = forwardRef(({ 
  className, 
  orientation = "horizontal", 
  decorative = true, 
  ...props 
}, ref) => (
  <div
    ref={ref}
    role={decorative ? "none" : "separator"}
    aria-orientation={orientation}
    className={cn(
      "shrink-0 bg-border",
      orientation === "horizontal" ? "h-[1px] w-full" : "h-full w-[1px]",
      className
    )}
    {...props}
  />
));

Separator.displayName = "Separator";

// Alert moderno
const alertVariants = cva(
  "relative w-full rounded-lg border p-4 [&>svg~*]:pl-7 [&>svg+div]:translate-y-[-3px] [&>svg]:absolute [&>svg]:left-4 [&>svg]:top-4 [&>svg]:text-foreground",
  {
    variants: {
      variant: {
        default: "bg-background text-foreground",
        destructive: "border-destructive/50 text-destructive dark:border-destructive [&>svg]:text-destructive",
        success: "border-green-500/50 text-green-700 bg-green-50 dark:bg-green-950 [&>svg]:text-green-600",
        warning: "border-yellow-500/50 text-yellow-700 bg-yellow-50 dark:bg-yellow-950 [&>svg]:text-yellow-600",
        info: "border-blue-500/50 text-blue-700 bg-blue-50 dark:bg-blue-950 [&>svg]:text-blue-600",
      },
    },
    defaultVariants: {
      variant: "default",
    },
  }
);

export const Alert = forwardRef(({ className, variant, children, ...props }, ref) => (
  <div ref={ref} role="alert" className={cn(alertVariants({ variant }), className)} {...props}>
    {children}
  </div>
));

Alert.displayName = "Alert";

// Progress bar
export const Progress = forwardRef(({ className, value, max = 100, ...props }, ref) => (
  <div
    ref={ref}
    className={cn("relative h-2 w-full overflow-hidden rounded-full bg-secondary", className)}
    {...props}
  >
    <div
      className="h-full w-full flex-1 bg-primary transition-all duration-300 ease-in-out"
      style={{ transform: `translateX(-${100 - (value || 0)}%)` }}
    />
  </div>
));

Progress.displayName = "Progress";

// Avatar
export const Avatar = forwardRef(({ className, src, alt, fallback, ...props }, ref) => (
  <div
    ref={ref}
    className={cn("relative flex h-10 w-10 shrink-0 overflow-hidden rounded-full", className)}
    {...props}
  >
    {src ? (
      <img src={src} alt={alt} className="aspect-square h-full w-full object-cover" />
    ) : (
      <div className="flex h-full w-full items-center justify-center bg-muted text-sm font-medium">
        {fallback}
      </div>
    )}
  </div>
));

Avatar.displayName = "Avatar";

// Tooltip
export const Tooltip = forwardRef(({ 
  children, 
  content, 
  side = "top", 
  className,
  ...props 
}, ref) => {
  const [isVisible, setIsVisible] = React.useState(false);
  
  return (
    <div
      ref={ref}
      className="relative inline-block"
      onMouseEnter={() => setIsVisible(true)}
      onMouseLeave={() => setIsVisible(false)}
      {...props}
    >
      {children}
      {isVisible && content && (
        <div
          className={cn(
            "absolute z-50 overflow-hidden rounded-md border bg-popover px-3 py-1.5 text-sm text-popover-foreground shadow-md animate-in fade-in-0 zoom-in-95",
            side === "top" && "bottom-full left-1/2 -translate-x-1/2 mb-2",
            side === "bottom" && "top-full left-1/2 -translate-x-1/2 mt-2",
            side === "left" && "right-full top-1/2 -translate-y-1/2 mr-2",
            side === "right" && "left-full top-1/2 -translate-y-1/2 ml-2",
            className
          )}
        >
          {content}
          <div
            className={cn(
              "absolute h-2 w-2 rotate-45 bg-popover border",
              side === "top" && "top-full left-1/2 -translate-x-1/2 -mt-1",
              side === "bottom" && "bottom-full left-1/2 -translate-x-1/2 -mb-1",
              side === "left" && "left-full top-1/2 -translate-y-1/2 -ml-1",
              side === "right" && "right-full top-1/2 -translate-y-1/2 -mr-1"
            )}
          />
        </div>
      )}
    </div>
  );
});

Tooltip.displayName = "Tooltip";

// Dropdown Menu
export const DropdownMenu = forwardRef(({ 
  children, 
  trigger, 
  items, 
  className,
  ...props 
}, ref) => {
  const [isOpen, setIsOpen] = React.useState(false);
  
  React.useEffect(() => {
    const handleClickOutside = (event) => {
      if (ref.current && !ref.current.contains(event.target)) {
        setIsOpen(false);
      }
    };
    
    if (isOpen) {
      document.addEventListener('mousedown', handleClickOutside);
    }
    
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, [isOpen, ref]);
  
  return (
    <div ref={ref} className="relative inline-block" {...props}>
      <div onClick={() => setIsOpen(!isOpen)}>
        {trigger}
      </div>
      {isOpen && (
        <div className={cn(
          "absolute z-50 min-w-[8rem] overflow-hidden rounded-md border bg-popover p-1 text-popover-foreground shadow-md animate-in fade-in-0 zoom-in-95",
          className
        )}>
          {items.map((item, index) => (
            <div
              key={index}
              className="relative flex cursor-default select-none items-center rounded-sm px-2 py-1.5 text-sm outline-none transition-colors hover:bg-accent hover:text-accent-foreground"
              onClick={() => {
                item.onClick?.();
                setIsOpen(false);
              }}
            >
              {item.icon && <span className="mr-2">{item.icon}</span>}
              {item.label}
            </div>
          ))}
        </div>
      )}
    </div>
  );
});

DropdownMenu.displayName = "DropdownMenu";
