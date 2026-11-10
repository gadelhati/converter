
import uvicorn
from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.config import settings
from app.routers import conversion, health, pages


APP_DIR = Path(__file__).resolve().parent

app = FastAPI(
    title="Conversor de RTF para HTML",
    version="1.0.0",
)

app.mount(
    "/static",
    StaticFiles(directory=APP_DIR / "static"),
    name="static",
)

app.include_router(pages.router)
app.include_router(health.router)
app.include_router(conversion.router)


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        root_path=settings.root_path,
        reload=settings.reload,
    )
