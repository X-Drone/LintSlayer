from fastapi import APIRouter
from infra.persist import db
from .project import router as shit_router
# from .shit import router as shit_router

router = APIRouter()

router.include_router(shit_router, prefix="/projects")
# router.include_router(shit_router, prefix="/shit")

@router.get("/health")
def health_check():
    return {"status": "healthy", "debug": db.engine.url if hasattr(db.engine, 'url') else str(db.engine)}
