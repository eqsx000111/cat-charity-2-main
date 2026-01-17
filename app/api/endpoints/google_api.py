from aiogoogle import Aiogoogle
from aiogoogle.excs import AiogoogleError, HTTPError
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.google_client import get_service
from app.crud.charity_project import charity_project_crud
from app.services.google_api import (
    create_spreadsheets,
    set_user_permissions,
    update_spreadsheets_value
)

router = APIRouter()


@router.post(
    '/'
)
async def get_report(
    session: AsyncSession = Depends(get_async_session),
    wrapper_services: Aiogoogle = Depends(get_service)
):
    projects = await charity_project_crud.get_projects_by_completion_rate(
        session
    )
    spreadsheet_id, spreadsheet_url = await create_spreadsheets(
        wrapper_services
    )
    await set_user_permissions(spreadsheet_id, wrapper_services)
    try:
        await update_spreadsheets_value(
            spreadsheet_id=spreadsheet_id,
            projects=projects,
            wrapper_services=wrapper_services
        )
    except AiogoogleError as error:
        raise HTTPError(error)
    return spreadsheet_url
