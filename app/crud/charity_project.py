from typing import Optional

from sqlalchemy import extract, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.charity_project import CharityProject


class CRUDCharityProject(CRUDBase):

    async def get_project_id_by_name(
        self,
        project_name: str,
        session: AsyncSession
    ) -> Optional[int]:
        return (await session.execute(
            select(CharityProject.id)
            .where(CharityProject.name == project_name)
        )).scalars().first()

    async def get_projects_by_completion_rate(
        session: AsyncSession
    ) -> list[CharityProject]:
        close_days = (
            extract('year', CharityProject.close_date) * 365 +
            extract('month', CharityProject.close_date) * 30 +
            extract('day', CharityProject.close_date)
        )
        create_days = (
            extract('year', CharityProject.create_date) * 365 +
            extract('month', CharityProject.create_date) * 30 +
            extract('day', CharityProject.create_date)
        )
        completion_time = close_days - create_days
        stmt = (
            select(CharityProject)
            .where(CharityProject.close_date.isnot(None))
            .order_by(completion_time)
        )
        result = await session.execute(stmt)
        return result.scalars().all()


charity_project_crud = CRUDCharityProject(CharityProject)
