from sqlalchemy.ext.asyncio import AsyncSession
from app.diagnosis.repositories.diagnosis_answer import DiagnosisAnswerRepository
from app.diagnosis.models.diagnosis_answer import DiagnosisAnswer

class DiagnosisAnswerService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.diagnosis_answer_repository = DiagnosisAnswerRepository(session)

    async def create_diagnosis_answer(self, diagnosis_answer_data: dict) -> DiagnosisAnswer | None:
        """
        create diagnosis answer
        args:
            diagnosis_answer_data: dict
        """
        diagnosis_answer = await self.diagnosis_answer_repository.create_diagnosis_answer(diagnosis_answer_data)
        if not diagnosis_answer:
            raise ValueError("failed to create diagnosis answer")
        return diagnosis_answer

    async def get_diagnosis_answer_by_id(self, id: int) -> DiagnosisAnswer | None:
        """
        get diagnosis answer by id
        args:
            id: int
        """
        diagnosis_answer = await self.diagnosis_answer_repository.get_diagnosis_answer_by_id(id)
        if not diagnosis_answer:
            raise ValueError("diagnosis answer not found")
        return diagnosis_answer