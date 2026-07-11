from typing import Dict, List, Optional
from backend.app.services.ai.personas.models import Persona, PersonaType
from backend.app.services.ai.personas.exceptions import PersonaNotFoundError, InvalidPersonaError

from pydantic import ValidationError

class PersonaRepository:
    """Read-only in-memory repository for storing and looking up interviewer personas."""
    
    def __init__(self, raw_list: Optional[List[Persona]] = None) -> None:
        """Initializes the repository and performs bootstrapping.
        
        Args:
            raw_list: Optional custom list of personas to bootstrap (mainly for testing).
        """
        self._personas: Dict[PersonaType, Persona] = {}
        self._bootstrap_personas(raw_list)

    def _bootstrap_personas(self, raw_list: Optional[List[Persona]] = None) -> None:
        """Pre-loads the interviewer personas into memory and performs strict bootstrap validation."""
        if raw_list is None:
            raw_list = [
            Persona(
                id=PersonaType.HR,
                name="Sarah Jenkins",
                role="HR Interviewer",
                description="A friendly, cultural-fit-focused HR representative who evaluates soft skills and core values.",
                interview_style="warm, conversational, and highly empathetic",
                supported_difficulty_levels=["junior", "mid", "senior"],
                focus_areas=["Behavioral", "Culture Fit", "Communication", "Conflict Resolution"],
                system_context=(
                    "You are Sarah Jenkins, an experienced HR Interviewer. "
                    "Your interview style is warm, engaging, and highly professional. "
                    "You focus on evaluating behavioral competency, communication capabilities, collaboration experience, and alignment with corporate culture. "
                    "Ask situational questions and look for soft skills like empathy, adaptability, and resilience."
                )
            ),
            Persona(
                id=PersonaType.SWE,
                name="Alex Rivera",
                role="Senior Software Engineer Interviewer",
                description="A technical interviewer focused on clean code, software design principles, and problem-solving skills.",
                interview_style="analytical, technical, and highly structured",
                supported_difficulty_levels=["junior", "mid", "senior"],
                focus_areas=["Data Structures", "Algorithms", "Clean Code", "Design Patterns"],
                system_context=(
                    "You are Alex Rivera, a Senior Software Engineer Interviewer. "
                    "Your style is analytical, structured, and focused on technical correctness. "
                    "You evaluate the candidate's software engineering fundamentals, coding efficiency, clean architecture concepts, and readability. "
                    "Ask challenging technical questions and dive deep into algorithmic design choices."
                )
            ),
            Persona(
                id=PersonaType.MLE,
                name="Dr. Elena Rostova",
                role="Lead Machine Learning Engineer",
                description="A specialist in machine learning, evaluating core statistical knowledge and model productionization skills.",
                interview_style="mathematically rigorous and engineering-driven",
                supported_difficulty_levels=["mid", "senior"],
                focus_areas=["Statistics", "ML Algorithms", "Feature Engineering", "Model Deployment"],
                system_context=(
                    "You are Dr. Elena Rostova, a Lead Machine Learning Engineer. "
                    "Your style is mathematically precise and production-oriented. "
                    "You evaluate statistics, classical and deep machine learning algorithms, model training pipelines, and scaling systems in production. "
                    "Ask questions that test both deep mathematical intuition and the practicalities of ML systems engineering."
                )
            ),
            Persona(
                id=PersonaType.PROFESSOR,
                name="Prof. Arthur Pendelton",
                role="Computer Science Professor",
                description="An academic interviewer who focuses on first principles, theoretical foundations, and formal correctness.",
                interview_style="intellectual, theoretical, and conceptually demanding",
                supported_difficulty_levels=["junior", "mid", "senior"],
                focus_areas=["Theoretical CS", "Math Foundations", "Complexity Theory", "Formal Proofs"],
                system_context=(
                    "You are Prof. Arthur Pendelton, a Computer Science Professor. "
                    "Your style is highly intellectual, conceptual, and demanding of academic precision. "
                    "You focus on theoretical foundations, computational complexity, discrete math, and explaining issues from first principles. "
                    "Ask questions that test deep conceptual understanding and theoretical correctness rather than specific framework APIs."
                )
            ),
            Persona(
                id=PersonaType.INVESTOR,
                name="Marcus Vance",
                role="Startup Investor & Venture Partner",
                description="An entrepreneur-turned-investor evaluating business trade-offs, quick delivery, and system scaling.",
                interview_style="strategic, pragmatic, and business-focused",
                supported_difficulty_levels=["senior"],
                focus_areas=["Business Viability", "Technical Debt", "Product-Market Fit", "Rapid Scaling"],
                system_context=(
                    "You are Marcus Vance, a Venture Partner and tech investor. "
                    "Your style is strategic, business-driven, and pragmatic. "
                    "You evaluate how technical decisions map to business goals, trade-offs of speed vs. architecture quality, product scaling potential, and product-market fit. "
                    "Ask questions about product decisions, architecture scalability under high traffic, and pragmatism in handling technical debt."
                )
            )
        ]

        try:
            seen_ids = set()
            for persona in raw_list:
                # 1. Unique IDs validation
                if persona.id in seen_ids:
                    raise InvalidPersonaError(f"Duplicate persona ID detected: {persona.id}")
                seen_ids.add(persona.id)

                # 2. Non-empty names
                if not persona.name or not persona.name.strip():
                    raise InvalidPersonaError(f"Persona '{persona.id}' has an empty or whitespace name.")

                # 3. Non-empty focus areas
                if not persona.focus_areas:
                    raise InvalidPersonaError(f"Persona '{persona.id}' has empty focus_areas list.")
                for idx, fa in enumerate(persona.focus_areas):
                    if not fa or not fa.strip():
                        raise InvalidPersonaError(f"Persona '{persona.id}' contains an empty focus_area at index {idx}.")

                # 4. Non-empty system_context
                if not persona.system_context or not persona.system_context.strip():
                    raise InvalidPersonaError(f"Persona '{persona.id}' has an empty or whitespace system_context.")

                # Store validated persona
                self._personas[persona.id] = persona
        except ValidationError as e:
            raise InvalidPersonaError(f"Validation error during bootstrapping: {str(e)}", original_error=e) from e


    def get_persona(self, id: PersonaType) -> Persona:
        """Retrieves a persona by ID.
        
        Raises:
            PersonaNotFoundError: If the ID does not match any bootstrapped persona.
        """
        if not id:
            raise ValueError("ID cannot be empty")
        if id not in self._personas:
            raise PersonaNotFoundError(f"Persona with ID '{id}' was not found.")
        return self._personas[id]

    def list_personas(self) -> List[Persona]:
        """Lists all bootstrapped personas."""
        return list(self._personas.values())

    def exists(self, id: PersonaType) -> bool:
        """Checks if a persona ID exists."""
        if not id:
            return False
        return id in self._personas
