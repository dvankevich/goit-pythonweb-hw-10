from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
import logging
from src.db.session import get_db

logger = logging.getLogger(__name__)
router = APIRouter(tags=["system"])


@router.get("/healthcheck")
async def healthcheck(db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(text("SELECT 1"))
        if result.scalar() == 1:
            return {"status": "ok", "database": "connected"}
        raise Exception("Database unexpected result")
    except Exception as e:
        logger.error(f"Healthcheck failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database connection error",
        )
