import uvicorn
from fastapi import FastAPI, Depends, HTTPException, status 
from sqlalchemy.orm import Session
from sqlalchemy import text
from src.db.session import get_db
from src.api.contact_api import router as contact_router
from src.api import auth, users

app = FastAPI(title="Contacts API")

app.include_router(contact_router, prefix="/api")
app.include_router(auth.router, prefix="/api")
app.include_router(users.router, prefix="/api")


# @app.get("/healthcheck")
# def healthcheck(db: Session = Depends(get_db)):
#     try:
#         result = db.execute(text("SELECT 1")).fetchone()

#         if result is not None:
#             return {
#                 "status": "ok",
#                 "database": "connected",
#                 "message": "API and Database are working correctly",
#             }

#         raise Exception("Database returned no result")

#     except Exception as e:
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail=f"Database connection error: {str(e)}",
#         )


@app.get("/")
def root():
    return {"message": "Welcome to Contacts API. Go to /docs for Swagger UI."}

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)
