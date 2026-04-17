from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_async_session

from app.auth.models import User
from app.auth.dependencies import get_current_user
from app.diagnosis.services.diagnsis_answer import DiagnosisAnswerService
from app.diagnosis.schemas.diagnosis_answer import DiagnosisAnswerDTO, DiagnosisAnswerResponse

router = APIRouter(
    prefix="/api/diagnosis",
    tags=["diagnosis"]
)

def get_diagnosis_answer_service(session: AsyncSession = Depends(get_async_session)):
    return DiagnosisAnswerService(session)

@router.post("/answer")
async def create_diagnosis_answer(
    diagnosis_answer_data: DiagnosisAnswerDTO,
    current_user: User = Depends(get_current_user),
    diagnosis_answer_service: DiagnosisAnswerService = Depends(get_diagnosis_answer_service)
) -> DiagnosisAnswerResponse:
    """
    create diagnosis answer
    """
    data = diagnosis_answer_data.model_dump()
    data['user_id'] = current_user.id
    diagnosis_answer = await diagnosis_answer_service.create_diagnosis_answer(data)
    return DiagnosisAnswerResponse.model_validate(diagnosis_answer)


@router.get("/answer/{id}")
async def get_diagnosis_answer(
    id: int,
    current_user: User = Depends(get_current_user),
    diagnosis_answer_service: DiagnosisAnswerService = Depends(get_diagnosis_answer_service)
) -> DiagnosisAnswerResponse:
    """
    get diagnosis answer by id
    """
    diagnosis_answer = await diagnosis_answer_service.get_diagnosis_answer_by_id(id)
    if diagnosis_answer.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Forbidden")
    return DiagnosisAnswerResponse.model_validate(diagnosis_answer)