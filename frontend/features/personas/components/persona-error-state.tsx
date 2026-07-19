"use client";

import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

type PersonaErrorStateProps = {
  message: string;
  onRetry: () => void;
};

export function PersonaErrorState({ message, onRetry }: PersonaErrorStateProps) {
  return (
    <Card className="border-border/80 bg-surface/90 shadow-sm">
      <CardHeader>
        <CardTitle className="text-lg">Unable to load personas</CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        <p className="max-w-2xl text-sm leading-6 text-muted-foreground">{message}</p>
        <Button type="button" onClick={onRetry}>
          Try Again
        </Button>
      </CardContent>
    </Card>
  );
}
