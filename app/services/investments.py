from typing import Iterable

from app.models.base import InvestableBase


def invest(
        target: InvestableBase,
        sources: Iterable[InvestableBase]
) -> list[InvestableBase]:
    modified = []
    for source in sources:
        modified.append(source)
        invested_amount = min(
            target.full_amount - target.invested_amount,
            source.full_amount - source.invested_amount
        )
        for obj in (target, source):
            obj.invested_amount += invested_amount
            obj.recalculate_state()
        if target.fully_invested:
            break
    return modified
