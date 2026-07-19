import { Toaster as Sonner, type ToasterProps } from "sonner";

export function Toaster(props: ToasterProps) {
  return (
    <Sonner
      theme="dark"
      position="top-right"
      expand
      closeButton
      className="toaster group"
      toastOptions={{
        classNames: {
          toast:
            "group toast rounded-2xl border border-border/80 bg-surface/95 text-foreground shadow-xl shadow-black/20 backdrop-blur-xl",
          title: "text-sm font-medium",
          description: "text-sm text-muted-foreground",
          actionButton:
            "rounded-full bg-primary text-primary-foreground hover:bg-primary/90",
          cancelButton:
            "rounded-full bg-muted text-muted-foreground hover:bg-muted/80",
          closeButton:
            "rounded-full border border-border/70 bg-background/70 text-muted-foreground hover:bg-accent hover:text-foreground",
        },
      }}
      {...props}
    />
  );
}
