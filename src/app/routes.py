from fastapi import APIRouter

router = APIRouter()


@router.get("/get-health")
async def health_check():
    return {"message": "app is runnings"}
