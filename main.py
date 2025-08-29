from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from contextlib import asynccontextmanager
import os

# Import routers
from app.api import auth, patients, doctors, users, emergency, laboratory, radiology
from app.api import pharmacy, financial, hr, reports, warehouse, dashboard
from app.core.config import get_settings
from app.database.connection import init_db

settings = get_settings()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await init_db()
    yield
    # Shutdown
    pass

# Create FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Comprehensive Hospital Management System with bilingual support",
    lifespan=lifespan,
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
)

# Add middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if settings.DEBUG else ["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["localhost", "127.0.0.1", "*"] if settings.DEBUG else ["yourdomain.com"]
)

# Mount static files
if not os.path.exists("app/static"):
    os.makedirs("app/static")
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Setup templates
templates = Jinja2Templates(directory="app/templates")

# Include API routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(users.router, prefix="/api/users", tags=["User Management"])
app.include_router(patients.router, prefix="/api/patients", tags=["Patient Management"])
app.include_router(doctors.router, prefix="/api/doctors", tags=["Doctor Management"])
app.include_router(emergency.router, prefix="/api/emergency", tags=["Emergency Department"])
app.include_router(laboratory.router, prefix="/api/laboratory", tags=["Laboratory"])
app.include_router(radiology.router, prefix="/api/radiology", tags=["Radiology"])
app.include_router(pharmacy.router, prefix="/api/pharmacy", tags=["Pharmacy"])
app.include_router(financial.router, prefix="/api/financial", tags=["Financial Management"])
app.include_router(hr.router, prefix="/api/hr", tags=["Human Resources"])
app.include_router(reports.router, prefix="/api/reports", tags=["Reports"])
app.include_router(warehouse.router, prefix="/api/warehouse", tags=["Warehouse"])
app.include_router(dashboard.router, prefix="/api/dashboard", tags=["Dashboard"])

# Root endpoint
@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request, "title": "HMS Dashboard"})

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "app": settings.APP_NAME, "version": settings.APP_VERSION}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower()
    )