import uuid
from fastapi import APIRouter, Depends

from backend.app.services.ai.interview.service import InterviewService
from backend.app.services.ai.conversation.service import ConversationService
from backend.app.api.dependencies import get_interview_service, get_conversation_service
from backend.app.schemas.interviews import (
    StartInterviewRequest,
    StartInterviewResponse,
    SendMessageRequest,
    SendMessageResponse,
    CompleteInterviewResponse,
)

router = APIRouter(prefix="/api/v1/interviews", tags=["Interviews"])

@router.post("/start", response_model=StartInterviewResponse)
async def start_interview(
    request: StartInterviewRequest,
    service: InterviewService = Depends(get_interview_service),
) -> StartInterviewResponse:
    """Initiates a new technical interview session and returns the opening question."""
    interview_id = str(uuid.uuid4())
    
    turn_result = await service.start_interview(
        interview_id=interview_id,
        persona_id=request.persona_id,
        topics=request.topics,
        difficulty=request.difficulty,
    )
    
    return StartInterviewResponse(
        interview_id=interview_id,
        question=turn_result.question,
        question_number=1,
    )

@router.post("/{interview_id}/message", response_model=SendMessageResponse)
async def send_message(
    interview_id: str,
    request: SendMessageRequest,
    interview_service: InterviewService = Depends(get_interview_service),
    conversation_service: ConversationService = Depends(get_conversation_service),
) -> SendMessageResponse:
    """Processes candidate answer and returns the next AI follow-up question."""
    turn_result = await interview_service.process_response(
        interview_id=interview_id,
        candidate_response=request.message,
    )
    
    # Compute the current question number using interviewer turn count
    question_number = conversation_service.get_interviewer_turn_count(interview_id)
    
    return SendMessageResponse(
        question=turn_result.question,
        question_number=question_number,
    )

@router.post("/{interview_id}/complete", response_model=CompleteInterviewResponse)
def complete_interview(
    interview_id: str,
    service: InterviewService = Depends(get_interview_service),
) -> CompleteInterviewResponse:
    """Marks the interview as completed and deactivates its conversation session."""
    service.complete_interview(interview_id)
    return CompleteInterviewResponse(status="completed")
