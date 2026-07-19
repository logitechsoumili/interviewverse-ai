"use client";

import { useMemo, useState } from "react";
import { useQueryClient } from "@tanstack/react-query";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { PersonaCard } from "@/features/personas/components/persona-card";
import { PersonaEmptyState } from "@/features/personas/components/persona-empty-state";
import { PersonaErrorState } from "@/features/personas/components/persona-error-state";
import { PersonaFilters } from "@/features/personas/components/persona-filters";
import { PersonaLoadingSkeleton } from "@/features/personas/components/persona-loading-skeleton";
import { enrichPersona, getPersonaRoleOptions } from "@/features/personas/utils";
import { getApiErrorMessage } from "@/lib/api-error";
import { queryKeys } from "@/lib/query-keys";
import { usePersonasQuery } from "@/features/personas/hooks/use-personas";
import type { PersonaListItem } from "@/features/personas/types";

function getDisplayPersonas(
  personas: PersonaListItem[],
  queryClient: ReturnType<typeof useQueryClient>
) {
  return personas.map((persona) => {
    const cachedDetail = queryClient.getQueryData(queryKeys.personas.detail(persona.id));
    return enrichPersona(persona, cachedDetail ?? null);
  });
}

export function PersonaListView() {
  const queryClient = useQueryClient();
  const personasQuery = usePersonasQuery();
  const [search, setSearch] = useState("");
  const [roleFilter, setRoleFilter] = useState("all");

  if (personasQuery.isLoading) {
    return <PersonaLoadingSkeleton />;
  }

  if (personasQuery.isError) {
    return (
      <PersonaErrorState
        message={getApiErrorMessage(personasQuery.error)}
        onRetry={() => void personasQuery.refetch()}
      />
    );
  }

  const personas = personasQuery.data ?? [];
  const displayPersonas = getDisplayPersonas(personas, queryClient);
  const roleOptions = getPersonaRoleOptions(personas);
  const searchTerm = search.trim().toLowerCase();

  const filteredPersonas = useMemo(() => {
    return displayPersonas.filter((persona) => {
      const matchesSearch =
        searchTerm.length === 0 ||
        persona.name.toLowerCase().includes(searchTerm) ||
        persona.role.toLowerCase().includes(searchTerm) ||
        persona.description.toLowerCase().includes(searchTerm) ||
        persona.expertise.some((item) => item.toLowerCase().includes(searchTerm));

      const matchesRole = roleFilter === "all" || persona.role === roleFilter;
      return matchesSearch && matchesRole;
    });
  }, [displayPersonas, roleFilter, searchTerm]);

  const hasNoPersonas = personas.length === 0;
  const hasNoMatches = !hasNoPersonas && filteredPersonas.length === 0;

  return (
    <div className="space-y-6">
      <Card className="border-border/80 bg-gradient-to-br from-surface via-surface to-background shadow-sm">
        <CardHeader className="space-y-4">
          <p className="text-xs font-semibold uppercase tracking-[0.3em] text-secondary">
            Personas
          </p>
          <div className="flex flex-wrap items-start justify-between gap-4">
            <div className="space-y-2">
              <CardTitle className="text-3xl tracking-tight">
                Interview personas for every session.
              </CardTitle>
              <p className="max-w-2xl text-sm leading-6 text-muted-foreground">
                Browse built-in and custom personas, inspect their interview style,
                and create new personas without leaving the dashboard.
              </p>
            </div>
            <Button asChild>
              <a href="/dashboard/personas/create">Create Persona</a>
            </Button>
          </div>
        </CardHeader>
        <CardContent className="flex flex-wrap gap-3 text-sm text-muted-foreground">
          <span>{personas.length} personas</span>
          <span>•</span>
          <span>{roleOptions.length} roles</span>
        </CardContent>
      </Card>

      <PersonaFilters
        search={search}
        role={roleFilter}
        roleOptions={roleOptions}
        onSearchChange={setSearch}
        onRoleChange={setRoleFilter}
      />

      {hasNoPersonas ? (
        <PersonaEmptyState
          title="No personas yet."
          description="Create your first persona to populate the library and start building interview presets."
        />
      ) : hasNoMatches ? (
        <PersonaEmptyState
          title="No matching personas."
          description="Try a different search term or clear the role filter to see more results."
          actionLabel="Clear Filters"
          actionHref="/dashboard/personas"
        />
      ) : (
        <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
          {filteredPersonas.map((persona) => (
            <PersonaCard key={persona.id} persona={persona} />
          ))}
        </div>
      )}
    </div>
  );
}
