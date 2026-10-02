"""
Aplicación principal de FastAPI para GymFit Agent.
Expone el núcleo funcional como servicios web REST con documentación OpenAPI y Dashboard Interactivo.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from src.api.dashboard_html import DASHBOARD_HTML
from src.api.routers.equipment import router as equipment_router
from src.api.routers.events import router as events_router
from src.api.routers.profile import router as profile_router
from src.api.routers.routine import router as routine_router
from src.api.routers.session import router as session_router
from src.api.routers.variability import router as variability_router


def create_app() -> FastAPI:
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

    # Registrar enrutadores modulares
    app.include_router(profile_router)
    app.include_router(equipment_router)
    app.include_router(routine_router)
    app.include_router(session_router)
    app.include_router(variability_router)
    app.include_router(events_router)

    @app.get("/dashboard", response_class=HTMLResponse, tags=["Interfaz Interactiva"])
    def get_dashboard() -> HTMLResponse:
        """Renderiza el dashboard interactivo de prueba para GymFit Agent."""
        return HTMLResponse(content=DASHBOARD_HTML)

    @app.get("/", response_class=HTMLResponse, tags=["General"])
    def root() -> HTMLResponse:
        """Página principal: muestra el dashboard interactivo."""
        return HTMLResponse(content=DASHBOARD_HTML)

    @app.get("/health", tags=["General"])
    def health_check() -> dict:
        return {"status": "healthy"}

    return app


app = create_app()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.api.app:app", host="0.0.0.0", port=8000, reload=True)
