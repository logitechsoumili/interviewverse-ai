import { http } from "@/services/http";
import type {
  PersonaCreateRequest,
  PersonaDetail,
  PersonaListItem,
} from "@/features/personas/types";

export async function fetchPersonas(): Promise<PersonaListItem[]> {
  const { data } = await http.get<PersonaListItem[]>("/personas");
  return data;
}

export async function createPersona(
  payload: PersonaCreateRequest
): Promise<PersonaDetail> {
  const { data } = await http.post<PersonaDetail>("/personas", payload);
  return data;
}
