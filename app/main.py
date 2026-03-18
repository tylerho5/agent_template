import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.middleware import ErrorHandlerMiddleware
from app.api.routes import router
from app.config import get_settings


def create_app() -> FastAPI:
    settings = get_settings()

    logging.basicConfig(
        level=settings.log_level,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )

    app = FastAPI(title="AI Agent Template")

    # Middleware (order matters — outermost first)
    app.add_middleware(ErrorHandlerMiddleware)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins.split(","),
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(router)
    return app


app = create_app()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
