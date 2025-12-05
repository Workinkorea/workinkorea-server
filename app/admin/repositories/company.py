from sqlalchemy import select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.auth.models import Company


"""
모델들은 걍 기존에 있던거 쓰면 되서 굳이 안만들었음
"""


class AdminCompanyRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all_companies(self, skip: int = 0, limit: int = 100) -> list[Company]:
        """
        회사 목록 페이지네이션으로 가져옴
        args:
            skip: int
            limit: int
        returns:
            list[Company]
        raises:
            Exception
        """
        try:
            stmt = select(Company).options(
                selectinload(Company.company_profile),
                selectinload(Company.company_users)
            ).offset(skip).limit(limit)
            result = await self.session.execute(stmt)
            return result.scalars().all()
        except Exception as e:
            raise e

    async def get_company_by_id(self, company_id: int) -> Company | None:
        """
        회사 아이디로 하나만 가져옴
        args:
            company_id: int
        returns:
            Company | None
        raises:
            Exception
        """
        try:
            stmt = select(Company).options(
                selectinload(Company.company_profile),
                selectinload(Company.company_users)
            ).where(Company.id == company_id)
            result = await self.session.execute(stmt)
            return result.scalar_one_or_none()
        except Exception as e:
            raise e

    async def update_company(self, company_id: int, company_data: dict) -> Company | None:
        """
        회사 수정하기
        args:
            company_id: int
            company_data: dict
        returns:
            Company | None
        raises:
            Exception
        """
        try:
            stmt = update(Company).where(Company.id == company_id).values(company_data).returning(Company)
            result = await self.session.execute(stmt)
            await self.session.commit()
            return result.scalar_one_or_none()
        except Exception as e:
            raise e

    async def delete_company(self, company: Company) -> bool:
        """
        회사 삭제하기
        args:
            company: Company
        returns:
            bool
        raises:
            Exception
        """
        try:
            await self.session.delete(company)
            await self.session.commit()
            return True
        except Exception as e:
            raise e
