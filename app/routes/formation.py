from fastapi import APIRouter

router = APIRouter(prefix="/formations", tags=["Formations"])

@router.get("/")
def get_formations():
    return []
