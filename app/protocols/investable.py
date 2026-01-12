from typing import Protocol


class Investable(Protocol):
    full_amount: int
    invested_amount: int
    fully_invested: bool

    def recalculate_state(self) -> None:
        ...
