from app.router.auth import auth_router
from app.router.stocks import stocks_router
from fastapi import FastAPI
from app.core.settings import settings
from scalar_fastapi import get_scalar_api_reference

app = FastAPI(title=settings.APP_NAME, version=settings.VERSION)

app.include_router(auth_router)
app.include_router(stocks_router)


@app.get("/scalar")
def get_scalar():
    return get_scalar_api_reference(openapi_url=app.openapi_url, title=app.title)
