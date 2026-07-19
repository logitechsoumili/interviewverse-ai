export function BrandMark() {
  return (
    <div className="flex h-11 w-11 items-center justify-center rounded-xl border border-border bg-primary/10 text-primary">
      <svg
        aria-hidden="true"
        viewBox="0 0 24 24"
        className="h-6 w-6"
        fill="none"
      >
        <path
          d="M5 12.2L10.4 6.8L15.2 11.6L19 7.8"
          stroke="currentColor"
          strokeWidth="1.8"
          strokeLinecap="round"
          strokeLinejoin="round"
        />
        <path
          d="M19 7.8V12.2H14.6"
          stroke="currentColor"
          strokeWidth="1.8"
          strokeLinecap="round"
          strokeLinejoin="round"
        />
      </svg>
    </div>
  );
}
