from sqlalchemy.ext.asyncio import AsyncSession
from app.diagnosis.models.diagnosis_answer import DiagnosisAnswer
from sqlalchemy import insert, select

class DiagnosisAnswerRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_diagnosis_answer(self, diagnosis_answer_data: dict) -> DiagnosisAnswer | None:
        """
        create diagnosis answer
        args:
            diagnosis_answer_data: dict
        """
        try:
            stmt = insert(DiagnosisAnswer).values(diagnosis_answer_data).returning(DiagnosisAnswer)
            result = await self.session.execute(stmt)
            await self.session.commit()
            return result.scalar_one_or_none()
        except Exception as e:
            raise e

    async def get_diagnosis_answer_by_id(self, id: int) -> DiagnosisAnswer | None:
        """
        get diagnosis answer by id
        args:
            id: int
        """
        try:
            stmt = select(DiagnosisAnswer).where(DiagnosisAnswer.id == id)
            result = await self.session.execute(stmt)
            return result.scalar_one_or_none()
        except Exception as e:
            raise e