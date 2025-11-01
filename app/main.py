from fastapi import FastAPI
from app.api.routes import router as api_router
from app.api.routes import router as public_router
from app.api.routes_etl import router as etl_router
from app.api.routes_metrics import router as metrics_router
from app.ui.routes_dashboard import router as dashboard_router
from app.api.routes_scheduler import router as scheduler_router

app = FastAPI(title="SpaceTracker")
app.include_router(api_router, prefix="/api")
app.include_router(public_router, prefix="/public")
app.include_router(etl_router)
app.include_router(metrics_router)
app.include_router(dashboard_router)
app.include_router(scheduler_router, prefix="/scheduler")
