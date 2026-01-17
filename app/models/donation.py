from sqlalchemy import ForeignKey, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import InvestableBase

REPR_TEMPLATE = '{base} comment={comment}'


class Donation(InvestableBase):
    comment: Mapped[str] = mapped_column(Text, nullable=True)
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('user.id', name='fk_donation_user_id_user'),
        nullable=True
    )

    def __repr__(self):
        return REPR_TEMPLATE.format(
            base=super().__repr__(),
            comment=self.comment
        )
