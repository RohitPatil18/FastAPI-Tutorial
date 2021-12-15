
import time

from fastapi import FastAPI, status, Request, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from core.exceptions import AuthenticationFailed
from core.dependencies import check_session

from auth.router import router as auth_router
from basic.router import router as basic_router
from products.router import products_router, categories_router
from projects.router import router as projects_router
from users.router import router as users_router


app = FastAPI(
    title="FastAPI Tutorial",
    description="Simple app created while learning FastAPI.",
    version="0.0.1",
    docs_url="/swagger",

    dependencies=[Depends(check_session)],
)


@app.exception_handler(AuthenticationFailed)
async def authentication_failed_handler(
    request: Request,
    exc: AuthenticationFailed
):
    return JSONResponse(
        status_code=exc.code,
        content={"message": exc.message}
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=jsonable_encoder({"detail": exc.errors()}),
    )

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

app.include_router(auth_router)
app.include_router(basic_router)
app.include_router(categories_router)
app.include_router(products_router)
app.include_router(projects_router)
app.include_router(users_router)