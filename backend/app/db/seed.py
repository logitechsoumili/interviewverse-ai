"""Database seeding script for default users and platform personas."""

from __future__ import annotations

import logging
import uuid

from app.db.session import SessionLocal
from app.models.user import User as UserORM
from app.models.persona import Persona as PersonaORM
from backend.app.services.ai.personas.models import PersonaType

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

SYSTEM_USER_ID = uuid.UUID("00000000-0000-0000-0000-000000000000")


def seed_database() -> None:
    db = SessionLocal()
    try:
        logger.info("Starting database seeding...")

        # 1. Seed System User
        system_user = db.query(UserORM).filter(
            (UserORM.id == SYSTEM_USER_ID) | (UserORM.email == "system@interviewverse.ai")
        ).first()
        if not system_user:
            logger.info("Creating system user...")
            system_user = UserORM(
                id=SYSTEM_USER_ID,
                email="system@interviewverse.ai",
                full_name="System User",
                password_hash="disabled"
            )
            db.add(system_user)
            db.flush()
        else:
            logger.info("System user already exists.")
            if system_user.id != SYSTEM_USER_ID:
                logger.info(f"Updating system user ID from {system_user.id} to {SYSTEM_USER_ID}...")
                system_user.id = SYSTEM_USER_ID
                db.flush()

        # 2. Seed default personas
        default_personas = [
            PersonaORM(
                id=PersonaType.HR.value,
                user_id=SYSTEM_USER_ID,
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
            PersonaORM(
                id=PersonaType.SWE.value,
                user_id=SYSTEM_USER_ID,
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
            PersonaORM(
                id=PersonaType.MLE.value,
                user_id=SYSTEM_USER_ID,
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
            PersonaORM(
                id=PersonaType.PROFESSOR.value,
                user_id=SYSTEM_USER_ID,
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
            PersonaORM(
                id=PersonaType.INVESTOR.value,
                user_id=SYSTEM_USER_ID,
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

        for persona in default_personas:
            existing = db.query(PersonaORM).filter(PersonaORM.id == persona.id).first()

            if not existing:
                logger.info(f"Adding persona: {persona.name}")
                db.add(persona)
            else:
                logger.info(f"Persona already exists: {persona.name}. Updating details...")
                existing.name = persona.name
                existing.role = persona.role
                existing.description = persona.description
                existing.interview_style = persona.interview_style
                existing.supported_difficulty_levels = persona.supported_difficulty_levels
                existing.focus_areas = persona.focus_areas
                existing.system_context = persona.system_context
                existing.user_id = SYSTEM_USER_ID

        db.commit()
        logger.info("Database seeding successfully completed!")
    except Exception as e:
        db.rollback()
        logger.error(f"Seeding failed: {str(e)}")
        raise e
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
