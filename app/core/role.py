
from enum import StrEnum
from typing import List

class Role(StrEnum):
    STUDENT = "Etudiant"
    TEACHER = "Formateur"
    ADMIN = "Administrateur"

    @staticmethod
    def values() -> List[str]:
        return [role.value for role in Role]
    
    @staticmethod
    def names() -> List[str]:
        return [role.name for role in Role]