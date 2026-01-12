from sqlalchemy import ForeignKey, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import ProjectDonationBase

REPR_TEMPLATE = '{base} comment={comment}'


class Donation(ProjectDonationBase):
    comment: Mapped[str] = mapped_column(Text, nullable=True)
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('user.id', name='fk_donation_user_id_user'),
        nullable=True
    )

    def __repr__(self):
        base = super().__repr__()
        return REPR_TEMPLATE.format(base=base, comment=self.comment)
