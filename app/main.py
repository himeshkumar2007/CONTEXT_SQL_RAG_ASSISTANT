from fastapi import FastAPI
from app.routes import router
import uvicorn
import logging

app = FastAPI(
    title="Smart SQL + KB Assistant",
    description="API for answering SQL queries and KB questions",
    version="1.0.0"
)

# Include routes
app.include_router(router)

# Optional: configure logging
logging.basicConfig(level=logging.INFO)

# For running directly
if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
