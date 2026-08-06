from fastapi import FastAPI
from src.classes.routes import dragon_class_router
from .errors import register_all_errors

version = "v1"
version_prefix = f"/api/{version}"

app = FastAPI(
    title="Dragon API",
    version=version,
)

register_all_errors(app)

app.include_router(dragon_class_router,prefix=f"{version_prefix}/classes",tags=["classes"])
