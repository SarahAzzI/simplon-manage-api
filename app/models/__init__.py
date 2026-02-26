from app.models.user import User                    # ← fichier user.py de votre collègue
from app.models.formation import Formation
from app.models.session import SessionFormation      # ← VOTRE model
from app.models.inscription import Inscription

__all__ = ["User", "Formation", "SessionFormation", "Inscription"]