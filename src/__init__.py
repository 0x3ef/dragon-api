from fastapi import FastAPI
from src.classes.routes import dragon_class_router
from src.images.routes import images_router
from src.abilities.routes import abilities_router
from src.distributions.routes import distributions_router
from src.dragons.routes import dragons_router 
from .errors import register_all_errors
from .middleware import register_middleware 

version = "v1"
version_prefix = f"/api/{version}"

app = FastAPI(
        title="Dragon API",
    version=version,
)

register_all_errors(app)

register_middleware(app)


app.include_router(dragon_class_router,prefix=f"{version_prefix}/classes",tags=["classes"])
app.include_router(images_router,prefix=f"{version_prefix}/images",tags=["images"])
app.include_router(abilities_router,prefix=f"{version_prefix}/abilities",tags=["abilities"])
app.include_router(distributions_router,prefix=f"{version_prefix}/distributions",tags=["distributions"])
app.include_router(dragons_router,prefix=f"{version_prefix}/dragons",tags=["dragons"])
