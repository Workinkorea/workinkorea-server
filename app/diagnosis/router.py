from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_async_session

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
    diagnosis_answer_service: DiagnosisAnswerService = Depends(get_diagnosis_answer_service)
) -> DiagnosisAnswerResponse:
    """
    create diagnosis answer
    """
    diagnosis_answer = await diagnosis_answer_service.create_diagnosis_answer(diagnosis_answer_data.model_dump())
    return DiagnosisAnswerResponse.model_validate(diagnosis_answer)


@router.get("/answer/{id}")
async def get_diagnosis_answer(
    id: int,
    diagnosis_answer_service: DiagnosisAnswerService = Depends(get_diagnosis_answer_service)
) -> DiagnosisAnswerResponse:
    """
    get diagnosis answer by id
    """
    diagnosis_answer = await diagnosis_answer_service.get_diagnosis_answer_by_id(id)
    return DiagnosisAnswerResponse.model_validate(diagnosis_answer)