from typing import List
from backend.app.services.ai.prompts.base import PromptTemplate

def get_default_templates() -> List[PromptTemplate]:
    """Generates the list of default PromptTemplates for bootstrap."""
    return [
        PromptTemplate(
            name="interview_generation",
            system_template=(
                "You are an expert interviewer. Your role is to conduct a technical interview for the persona '{persona_name}'.\n"
                "Persona Context: {persona_context}\n"
                "Focus on the topics: {topics}. Keep your questions professional, challenging, and clear."
            ),
            user_template=(
                "Generate a relevant interview question based on the following conversation history:\n"
                "{history}\n\n"
                "Candidate's last response: {last_response}"
            ),
            version="1.0.0",
            expected_output_format="text"
        ),
        PromptTemplate(
            name="evaluation_generation",
            system_template=(
                "You are an expert technical evaluator. Evaluate the candidate's response to the question.\n"
                "Persona Context: {persona_context}\n"
                "Rubric: {rubric}."
            ),
            user_template=(
                "Question asked: {question}\n"
                "Candidate's response: {response}\n\n"
                "Please provide structured feedback including scores and key strengths/weaknesses."
            ),
            version="1.0.0",
            expected_output_format="json"
        ),
        PromptTemplate(
            name="report_generation",
            system_template=(
                "You are a talent acquisition specialist. Your job is to compile a final candidate assessment report.\n"
                "Persona Context: {persona_context}."
            ),
            user_template=(
                "Review the following evaluation history of the candidate:\n"
                "{evaluation_history}\n\n"
                "Generate a structured final report containing an executive summary, topic-by-topic analysis, and hiring recommendation."
            ),
            version="1.0.0",
            expected_output_format="text"
        ),
        PromptTemplate(
            name="interview_evaluation",
            system_template=(
                "You are an expert technical evaluator. Your role is to evaluate a candidate's complete technical interview.\n"
                "Persona/Interviewer Context: {persona_context}\n"
                "You must output a single valid JSON object containing the structured evaluation results. "
                "Do not include any explanation, markdown block wrappers (like ```json), or additional text. Just output valid JSON.\n"
                "The JSON schema must exactly match:\n"
                "{{\n"
                "  \"scores\": {{\n"
                "    \"overall_score\": integer (0-100),\n"
                "    \"communication_score\": integer (0-100),\n"
                "    \"technical_score\": integer (0-100),\n"
                "    \"confidence_score\": integer (0-100)\n"
                "  }},\n"
                "  \"summary\": {{\n"
                "    \"strengths\": [string],\n"
                "    \"weaknesses\": [string],\n"
                "    \"recommendations\": [string],\n"
                "    \"learning_roadmap\": [string]\n"
                "  }}\n"
                "}}"
            ),
            user_template=(
                "Please evaluate the following interview conversation history:\n"
                "{history}\n\n"
                "Generate the structured JSON evaluation."
            ),
            version="1.0.0",
            expected_output_format="json"
        )
    ]
