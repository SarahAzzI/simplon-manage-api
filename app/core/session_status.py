from enum import StrEnum
from typing import List


class SessionStatus(StrEnum):
    PLANNED = "planifiée"
    IN_PROGRESS = "en_cours"
    COMPLETED = "terminée"
    CANCELLED = "annulée"

    @staticmethod
    def values() -> List[str]:
        return [status.value for status in SessionStatus]

    @staticmethod
    def names() -> List[str]:
        return [status.name for status in SessionStatus]
