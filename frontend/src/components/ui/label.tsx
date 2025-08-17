"use client";

import * as React from "react";
import { Slot } from "@radix-ui/react-slot";

// Basitleştirilmiş Label, sadece temel HTML label'ı gibi davranır
// ve Radix veya CVA bağımlılıklarını kullanmaz.
const Label = React.forwardRef<
  HTMLLabelElement,
  React.LabelHTMLAttributes<HTMLLabelElement>
>(({ className, ...props }, ref) => {
  return (
    <label
      ref={ref}
      className={`text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70 ${className}`}
      {...props}
    />
  );
});
Label.displayName = "Label";

export { Label };
