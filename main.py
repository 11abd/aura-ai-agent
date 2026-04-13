from fastapi import FastAPI
from app.config.settings import settings
from app.utils.logger import setup_logger, get_logger
from app.api.routes import router

# Setup logging
setup_logger()
logger = get_logger(__name__)

# Initialize FastAPI app
app = FastAPI(title=settings.APP_NAME)


@app.on_event("startup")
def startup_event():
    logger.info("Starting AURA AI Agent...")


@app.get("/")
def health_check():
    return {"status": f"{settings.APP_NAME} is running 🚀"}

app.include_router(router)