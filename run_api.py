import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",   # app is the FastAPI instance inside app/main.py
        host="0.0.0.0",
        port=8000,
        reload=True       # auto-reload for dev; disable in production
    )


#  uvicorn app.main:app --reload --port 8000