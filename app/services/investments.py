from typing import Iterable

from app.protocols.investable import Investable


def invest(
        target: Investable,
        sources: Iterable[Investable]
) -> list[Investable]:
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
