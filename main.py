import uvicorn
from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.middleware.cors import CORSMiddleware  # Імпортуємо Middleware
from starlette.responses import JSONResponse
from slowapi.errors import RateLimitExceeded
from sqlalchemy.orm import Session
from sqlalchemy import text
from src.db.session import get_db
from src.api.contact_api import router as contact_router
from src.api import auth, users
from src.api.users import limiter
from src.config.app_config import settings

app = FastAPI(title="Contacts API")
app.state.limiter = limiter

# --- CORS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS_LIST,  # Список дозволених джерел
    allow_credentials=True,  # Дозволити передачу Cookies та Authorization headers
    allow_methods=["*"],  # Дозволити всі методи (GET, POST, PUT, DELETE тощо)
    allow_headers=["*"],  # Дозволити всі заголовки
)
# -------------------------


@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
        content={"error": "Перевищено ліміт запитів. Спробуйте пізніше."},
    )


app.include_router(contact_router, prefix="/api")
app.include_router(auth.router, prefix="/api")
app.include_router(users.router, prefix="/api")


@app.get("/")
def root():
    return {"message": "Welcome to Contacts API. Go to /docs for Swagger UI."}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
