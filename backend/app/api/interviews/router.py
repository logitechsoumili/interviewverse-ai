import uuid
from fastapi import APIRouter, Depends, HTTPException, status

from backend.app.services.ai.interview.service import InterviewService
from backend.app.services.ai.conversation.service import ConversationService
from backend.app.api.dependencies import get_interview_service, get_conversation_service, get_current_user
from backend.app.schemas.interviews import (
    StartInterviewRequest,
    StartInterviewResponse,
    SendMessageRequest,
    SendMessageResponse,
    CompleteInterviewResponse,
)
from backend.app.services.ai.interview.exceptions import (
    InterviewNotFoundError,
    InterviewAlreadyCompletedError,
    InterviewError,
    InterviewGenerationError,
)
from app.models.user import User

router = APIRouter(prefix="/api/v1/interviews", tags=["Interviews"])

@router.post("/start", response_model=StartInterviewResponse)
async def start_interview(
    request: StartInterviewRequest,
    service: InterviewService = Depends(get_interview_service),
    current_user: User = Depends(get_current_user),
) -> StartInterviewResponse:
    """Initiates a new technical interview session and returns the opening question."""
    interview_id = str(uuid.uuid4())
    
    turn_result = await service.start_interview(
        interview_id=interview_id,
        persona_id=request.persona_id,
        topics=request.topics,
        difficulty=request.difficulty,
        user_id=current_user.id,
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
    current_user: User = Depends(get_current_user),
) -> SendMessageResponse:
    """Processes candidate answer and returns the next AI follow-up question."""
    try:
        turn_result = await interview_service.process_response(
            interview_id=interview_id,
            candidate_response=request.message,
            user_id=current_user.id,
        )
    except InterviewNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Interview was not found."
        )
    except InterviewAlreadyCompletedError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Interview is completed."
        )
    except InterviewGenerationError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
    except InterviewError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
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
    current_user: User = Depends(get_current_user),
) -> CompleteInterviewResponse:
    """Marks the interview as completed and deactivates its conversation session."""
    try:
        service.complete_interview(interview_id, user_id=current_user.id)
    except InterviewNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Interview was not found."
        )
    except InterviewAlreadyCompletedError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Interview is completed."
        )
    return CompleteInterviewResponse(status="completed")
