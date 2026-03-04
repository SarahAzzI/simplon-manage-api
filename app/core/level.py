
from enum import StrEnum
from typing import List

class Level(StrEnum):
    BEGINNER = "débutant"
    INTERMEDIATE = "intermédiaire"
    ADVANCED = "avancé"

    @staticmethod
    def values() -> List[str]:
        return [level.value for level in Level]
    
    @staticmethod
    def names() -> List[str]:
        return [level.name for level in Level]