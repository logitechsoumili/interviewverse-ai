export default function RootLoading() {
  return (
    <div className="flex min-h-screen flex-col items-center justify-center bg-background px-6">
      <div className="relative flex h-20 w-20 items-center justify-center">
        {/* Outer glowing ring */}
        <div className="absolute inset-0 rounded-full border border-primary/20 bg-primary/5 blur-md animate-pulse" />
        {/* Inner rotating gradient spinner */}
        <div className="h-12 w-12 animate-spin rounded-full border-2 border-t-primary border-r-secondary border-b-transparent border-l-transparent" />
      </div>
      <p className="mt-6 text-xs font-semibold tracking-[0.25em] text-muted-foreground uppercase animate-pulse">
        Loading Workspace
      </p>
    </div>
  );
}
