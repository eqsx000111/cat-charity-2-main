from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import InvestableBase

REPR_TEMPLATE = '{base} name={name} description={description}'


class CharityProject(InvestableBase):
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)

    def __repr__(self):
        return REPR_TEMPLATE.format(
            base=super().__repr__(),
            name=self.name,
            description=self.description
        )
