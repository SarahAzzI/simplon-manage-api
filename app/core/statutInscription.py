from enum import StrEnum
from typing import List


class StatutInscription(StrEnum):
    EN_ATTENTE = "en_attente"
    CONFIRME = "confirmé"
    ANNULE = "annulé"
    TERMINE = "terminé"
    

    @staticmethod
    def values() -> List[str]:
        return [statutInscription.value for statutInscription in StatutInscription]
    
    @staticmethod
    def names() -> List[str]:
        return [statutInscription.name for statutInscription in StatutInscription]