from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud.charity_project import charity_project_crud
from app.crud.donation import donation_crud
from app.models.user import User
from app.schemas.donation import DonationCreate, DonationDB, DonationResponse
from app.services.investments import invest

router = APIRouter()
SessionDep = Annotated[AsyncSession, Depends(get_async_session)]
CurrentUserDep = Annotated[User, Depends(current_user)]


@router.get(
    '/',
    response_model=list[DonationDB],
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)]
)
async def get_donations(session: SessionDep):
    return await donation_crud.get_multi(session)


@router.post(
    '/',
    response_model=DonationResponse,
    response_model_exclude_none=True
)
async def create_donation(
    donation: DonationCreate,
    session: SessionDep,
    user: CurrentUserDep
):
    donation = await donation_crud.create(donation, session, user)
    session.add_all(
        invest(
            target=donation,
            sources=await charity_project_crud.get_open(session)
        )
    )
    await session.commit()
    await session.refresh(donation)
    return donation


@router.get('/my', response_model=list[DonationResponse])
async def get_my_donation(
    session: SessionDep,
    user: CurrentUserDep
):
    return await donation_crud.get_by_user(session=session, user=user)
