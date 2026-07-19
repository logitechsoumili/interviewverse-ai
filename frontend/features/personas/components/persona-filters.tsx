"use client";

import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";

type PersonaFiltersProps = {
  search: string;
  role: string;
  roleOptions: string[];
  onSearchChange: (value: string) => void;
  onRoleChange: (value: string) => void;
};

export function PersonaFilters({
  search,
  role,
  roleOptions,
  onSearchChange,
  onRoleChange,
}: PersonaFiltersProps) {
  return (
    <div className="grid gap-4 rounded-2xl border border-border/80 bg-surface/90 p-4 shadow-sm md:grid-cols-[minmax(0,1.5fr)_260px]">
      <div className="space-y-2">
        <Label htmlFor="persona-search">Search personas</Label>
        <Input
          id="persona-search"
          value={search}
          onChange={(event) => onSearchChange(event.target.value)}
          placeholder="Search by name, role, or description"
        />
      </div>

      <div className="space-y-2">
        <Label htmlFor="role-filter">Role filter</Label>
        <select
          id="role-filter"
          value={role}
          onChange={(event) => onRoleChange(event.target.value)}
          className="flex h-11 w-full rounded-md border border-border/80 bg-background/70 px-3 py-2 text-sm text-foreground shadow-sm transition-all duration-200 ease-out focus-visible:outline-none focus-visible:border-primary/60 focus-visible:bg-background focus-visible:ring-2 focus-visible:ring-ring/30 motion-reduce:transition-none"
        >
          <option value="all">All roles</option>
          {roleOptions.map((roleOption) => (
            <option key={roleOption} value={roleOption}>
              {roleOption}
            </option>
          ))}
        </select>
      </div>
    </div>
  );
}
