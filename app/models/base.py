from datetime import datetime
from typing import Optional

from sqlalchemy import Boolean, CheckConstraint, DateTime, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base

REPR_TEMPLATE = (
    'base={base} full={full} invest={invest} closed={closed} '
    'create_date={create_date} close_date={close_date}'
)


class InvestableBase(Base):

    __abstract__ = True

    __table_args__ = (
        CheckConstraint(
            'full_amount > 0',
            name='check_full_amount_positive'
        ),
        CheckConstraint(
            '0 <= invested_amount <= full_amount',
            name='check_invested_amount_range'
        ),
    )

    full_amount: Mapped[int] = mapped_column(Integer, nullable=False)
    invested_amount: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False
    )
    fully_invested: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False
    )
    create_date: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )
    close_date: Mapped[Optional[datetime]] = mapped_column(
        DateTime,
        nullable=True
    )

    def recalculate_state(self) -> None:
        if self.invested_amount >= self.full_amount:
            self.fully_invested = True
            self.close_date = datetime.now()

    def __repr__(self):
        return REPR_TEMPLATE.format(
            base=super().__repr__(),
            full=self.full_amount,
            invest=self.invested_amount,
            closed=self.fully_invested,
            create_date=self.create_date,
            close_date=self.close_date
        )
