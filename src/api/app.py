"""
Aplicación principal de FastAPI para GymFit Agent.
Expone el núcleo funcional como servicios web REST con documentación OpenAPI y Dashboard Interactivo.
"""
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from src.api.routers.equipment import router as equipment_router
from src.api.routers.events import router as events_router
from src.api.routers.profile import router as profile_router
from src.api.routers.routine import router as routine_router
from src.api.routers.session import router as session_router
from src.api.routers.variability import router as variability_router


def montar_estaticos(
    app: FastAPI,
    static_dir: Path | None = None,
    exercises_dir: Path | None = None,
) -> None:
    """Monta directorios de archivos estáticos (/static y opcionalmente /exercise-images).

    Rutas calculadas relativas a __file__.
    /exercise-images/ solo se monta si el directorio data/external/free-exercise-db/exercises/ existe.
    Si no existe, la app arranca igual sin esa ruta.
    """
    base_api_dir = Path(__file__).resolve().parent
    resolved_static_dir = static_dir or (base_api_dir / "static")
    resolved_static_dir.mkdir(parents=True, exist_ok=True)
    app.mount("/static", StaticFiles(directory=str(resolved_static_dir)), name="static")

    resolved_exercises_dir = exercises_dir or (
        base_api_dir.parent.parent / "data" / "external" / "free-exercise-db" / "exercises"
    )
    if resolved_exercises_dir.exists() and resolved_exercises_dir.is_dir():
        app.mount(
            "/exercise-images",
            StaticFiles(directory=str(resolved_exercises_dir)),
            name="exercise-images",
        )


def create_app(
    static_dir: Path | None = None,
    exercises_dir: Path | None = None,
) -> FastAPI:
    """Fábrica pura para crear y configurar la aplicación FastAPI."""
    app = FastAPI(
        title="GymFit Agent API",
        description=(
            "API REST para el agente de IA agéntica GymFit. "
            "Implementa principios de Programación Funcional: inmutabilidad, "
            "filtrado bicondicional de catálogos y Event Sourcing."
        ),
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
    )

    # Configurar CORS para permitir peticiones desde React Native / Expo / Web
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Montar directorios estáticos (/static y opcionalmente /exercise-images)
    montar_estaticos(app, static_dir=static_dir, exercises_dir=exercises_dir)

    # Registrar enrutadores modulares
    app.include_router(profile_router)
    app.include_router(equipment_router)
    app.include_router(routine_router)
    app.include_router(session_router)
    app.include_router(variability_router)
    app.include_router(events_router)

    default_index = Path(__file__).resolve().parent / "static" / "index.html"
    index_file = (
        (static_dir / "index.html")
        if (static_dir and (static_dir / "index.html").exists())
        else default_index
    )

    @app.get("/dashboard", response_class=FileResponse, tags=["Interfaz Interactiva"])
    def get_dashboard() -> FileResponse:
        """Renderiza el dashboard interactivo de prueba para GymFit Agent."""
        return FileResponse(index_file)

    @app.get("/", response_class=FileResponse, tags=["General"])
    def root() -> FileResponse:
        """Página principal: muestra el dashboard interactivo."""
        return FileResponse(index_file)

    @app.get("/health", tags=["General"])
    def health_check() -> dict:
        return {"status": "healthy"}

    return app


app = create_app()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.api.app:app", host="0.0.0.0", port=8000, reload=True)
