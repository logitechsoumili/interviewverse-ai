import uuid
from fastapi import APIRouter, Depends, HTTPException, status

from backend.app.services.ai.interview.service import InterviewService
from backend.app.services.ai.conversation.service import ConversationService
from typing import List
from backend.app.api.dependencies import get_interview_service, get_conversation_service, get_current_user
from backend.app.schemas.interviews import (
    StartInterviewRequest,
    StartInterviewResponse,
    SendMessageRequest,
    SendMessageResponse,
    CompleteInterviewResponse,
    InterviewListItemSchema,
    InterviewDetailResponse,
    InterviewMetadataSchema,
    ConversationSummaryTurnSchema,
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

@router.get("", response_model=List[InterviewListItemSchema])
def get_interviews(
    service: InterviewService = Depends(get_interview_service),
    current_user: User = Depends(get_current_user),
) -> List[InterviewListItemSchema]:
    """Retrieves all interview sessions for the current user."""
    sessions = service.list_interviews(user_id=current_user.id)
    return [
        InterviewListItemSchema(
            id=s.interview_id,
            status=s.status.value,
            persona=s.persona_id.value if hasattr(s.persona_id, 'value') else str(s.persona_id),
            created_at=s.created_at,
            completed_at=s.completed_at,
        )
        for s in sessions
    ]

@router.get("/{interview_id}", response_model=InterviewDetailResponse)
def get_interview(
    interview_id: str,
    interview_service: InterviewService = Depends(get_interview_service),
    conversation_service: ConversationService = Depends(get_conversation_service),
    current_user: User = Depends(get_current_user),
) -> InterviewDetailResponse:
    """Retrieves metadata and chronological conversation turns for a specific interview session."""
    try:
        session = interview_service.get_interview(interview_id, user_id=current_user.id)
    except InterviewNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Interview was not found."
        )

    conv_session = conversation_service.repository.get_session(interview_id)
    turns = [
        ConversationSummaryTurnSchema(
            role=t.role.value if hasattr(t.role, 'value') else str(t.role),
            content=t.content,
            timestamp=t.timestamp,
        )
        for t in conv_session.turns
    ]

    return InterviewDetailResponse(
        metadata=InterviewMetadataSchema(
            topics=session.topics,
            difficulty=session.difficulty,
            persona_id=session.persona_id.value if hasattr(session.persona_id, 'value') else str(session.persona_id),
            created_at=session.created_at,
            completed_at=session.completed_at,
        ),
        conversation_summary=turns,
        status=session.status.value,
    )
