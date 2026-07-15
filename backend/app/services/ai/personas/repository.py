from typing import Dict, List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import select

from backend.app.services.ai.personas.models import Persona as PersonaSchema, PersonaType
from backend.app.services.ai.personas.exceptions import PersonaNotFoundError, InvalidPersonaError
from app.models.persona import Persona as PersonaORM

from pydantic import ValidationError

class PersonaRepository:
    """Hybrid repository for storing and looking up interviewer personas.
    
    Supports database persistence via SQLAlchemy Session if provided, otherwise
    falls back to a read-only in-memory static dictionary for testing.
    """
    
    def __init__(self, db: Optional[Session] = None, raw_list: Optional[List[PersonaSchema]] = None) -> None:
        """Initializes the repository.
        
        Args:
            db: Optional database Session.
            raw_list: Optional custom list of personas to bootstrap (mainly for in-memory testing).
        """
        self.db = db
        self._personas: Dict[PersonaType, PersonaSchema] = {}
        if not self.db:
            self._bootstrap_personas(raw_list)

    def _bootstrap_personas(self, raw_list: Optional[List[PersonaSchema]] = None) -> None:
        """Pre-loads the interviewer personas into memory and performs strict bootstrap validation."""
        if raw_list is None:
            raw_list = [
                PersonaSchema(
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
                PersonaSchema(
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
                PersonaSchema(
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
                PersonaSchema(
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
                PersonaSchema(
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
                if persona.id in seen_ids:
                    raise InvalidPersonaError(f"Duplicate persona ID detected: {persona.id}")
                seen_ids.add(persona.id)

                if not persona.name or not persona.name.strip():
                    raise InvalidPersonaError(f"Persona '{persona.id}' has an empty or whitespace name.")

                if not persona.focus_areas:
                    raise InvalidPersonaError(f"Persona '{persona.id}' has empty focus_areas list.")
                for idx, fa in enumerate(persona.focus_areas):
                    if not fa or not fa.strip():
                        raise InvalidPersonaError(f"Persona '{persona.id}' contains an empty focus_area at index {idx}.")

                if not persona.system_context or not persona.system_context.strip():
                    raise InvalidPersonaError(f"Persona '{persona.id}' has an empty or whitespace system_context.")

                self._personas[persona.id] = persona
        except ValidationError as e:
            raise InvalidPersonaError(f"Validation error during bootstrapping: {str(e)}", original_error=e) from e

    def get_persona(self, id: str | PersonaType, user_id: Optional[UUID] = None) -> PersonaSchema:
        """Retrieves a persona by ID, filtered by user_id if DB is active."""
        if not id:
            raise ValueError("ID cannot be empty")

        id_str = id.value if isinstance(id, PersonaType) else str(id)

        if self.db:
            # Query from database with user_id filter
            stmt = select(PersonaORM).where(PersonaORM.id == id_str)
            if user_id:
                stmt = stmt.where(PersonaORM.user_id == user_id)
            
            db_persona = self.db.execute(stmt).scalar_one_or_none()
            if not db_persona:
                raise PersonaNotFoundError(f"Persona with ID '{id}' was not found for user '{user_id}'.")
            
            # Safely parse persona_id as string or PersonaType enum
            try:
                p_id = PersonaType(db_persona.id)
            except ValueError:
                p_id = db_persona.id

            return PersonaSchema(
                id=p_id,
                name=db_persona.name,
                role=db_persona.role,
                description=db_persona.description,
                interview_style=db_persona.interview_style,
                supported_difficulty_levels=db_persona.supported_difficulty_levels,
                focus_areas=db_persona.focus_areas,
                system_context=db_persona.system_context,
            )
        else:
            if isinstance(id, PersonaType):
                p_type = id
            else:
                try:
                    p_type = PersonaType(id)
                except ValueError:
                    p_type = id
            
            if p_type not in self._personas:
                raise PersonaNotFoundError(f"Persona with ID '{id}' was not found.")
            return self._personas[p_type]

    def list_personas(self, user_id: Optional[UUID] = None) -> List[PersonaSchema]:
        """Lists personas. Filters by user_id if DB is active."""
        if self.db:
            stmt = select(PersonaORM)
            if user_id:
                stmt = stmt.where(PersonaORM.user_id == user_id)
            db_personas = self.db.execute(stmt).scalars().all()
            
            res = []
            for p in db_personas:
                try:
                    p_id = PersonaType(p.id)
                except ValueError:
                    p_id = p.id
                res.append(
                    PersonaSchema(
                        id=p_id,
                        name=p.name,
                        role=p.role,
                        description=p.description,
                        interview_style=p.interview_style,
                        supported_difficulty_levels=p.supported_difficulty_levels,
                        focus_areas=p.focus_areas,
                        system_context=p.system_context,
                    )
                )
            return res
        else:
            return list(self._personas.values())

    def exists(self, id: str | PersonaType, user_id: Optional[UUID] = None) -> bool:
        """Checks if a persona ID exists."""
        if not id:
            return False
        try:
            self.get_persona(id, user_id)
            return True
        except PersonaNotFoundError:
            return False

    def create_persona(self, user_id: UUID, schema: PersonaSchema) -> PersonaSchema:
        """Saves a new persona to the database."""
        if not self.db:
            p_type = PersonaType(schema.id) if isinstance(schema.id, str) else schema.id
            self._personas[p_type] = schema
            return schema

        db_persona = PersonaORM(
            id=schema.id.value if hasattr(schema.id, 'value') else str(schema.id),
            user_id=user_id,
            name=schema.name,
            role=schema.role,
            description=schema.description,
            interview_style=schema.interview_style,
            supported_difficulty_levels=schema.supported_difficulty_levels,
            focus_areas=schema.focus_areas,
            system_context=schema.system_context,
        )
        self.db.add(db_persona)
        self.db.commit()
        self.db.refresh(db_persona)
        return schema

    def update_persona(self, user_id: UUID, id: str | PersonaType, schema: PersonaSchema) -> PersonaSchema:
        """Updates a persona in the database."""
        id_str = id.value if isinstance(id, PersonaType) else str(id)
        if not self.db:
            p_type = PersonaType(id) if not isinstance(id, PersonaType) else id
            self._personas[p_type] = schema
            return schema

        stmt = select(PersonaORM).where(PersonaORM.id == id_str, PersonaORM.user_id == user_id)
        db_persona = self.db.execute(stmt).scalar_one_or_none()
        if not db_persona:
            raise PersonaNotFoundError(f"Persona with ID '{id}' was not found.")

        db_persona.name = schema.name
        db_persona.role = schema.role
        db_persona.description = schema.description
        db_persona.interview_style = schema.interview_style
        db_persona.supported_difficulty_levels = schema.supported_difficulty_levels
        db_persona.focus_areas = schema.focus_areas
        db_persona.system_context = schema.system_context

        self.db.commit()
        return schema

    def delete_persona(self, user_id: UUID, id: str | PersonaType) -> None:
        """Deletes a persona from the database."""
        id_str = id.value if isinstance(id, PersonaType) else str(id)
        if not self.db:
            p_type = PersonaType(id) if not isinstance(id, PersonaType) else id
            if p_type in self._personas:
                del self._personas[p_type]
                return
            raise PersonaNotFoundError(f"Persona with ID '{id}' was not found.")

        stmt = select(PersonaORM).where(PersonaORM.id == id_str, PersonaORM.user_id == user_id)
        db_persona = self.db.execute(stmt).scalar_one_or_none()
        if not db_persona:
            raise PersonaNotFoundError(f"Persona with ID '{id}' was not found.")

        self.db.delete(db_persona)
        self.db.commit()
