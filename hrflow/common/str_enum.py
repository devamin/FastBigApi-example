from __future__ import annotations

from enum import Enum, EnumMeta


class EnumWithContains(EnumMeta):
    def __contains__(cls, item):  # noqa: N805
        try:
            cls(item)
        except ValueError:
            return False
        return True


class StrEnum(str, Enum, metaclass=EnumWithContains):
    def __str__(self) -> str:
        return self.value

    def __eq__(self, other: str) -> bool:  # type: ignore
        return self.value == other

    def __hash__(self) -> int:
        return hash(self.value)
