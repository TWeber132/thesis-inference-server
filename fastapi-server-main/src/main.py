# main.py
from fastapi import FastAPI, Request, HTTPException
from starlette.responses import JSONResponse

from routes.process_routes import router as process_router
from routes.results import router as results_router

# Create the FastAPI app
app = FastAPI()
# Include the routers
app.include_router(process_router)
app.include_router(results_router)


# Define the exception handlers
@app.exception_handler(Exception)
async def validation_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500, content={"message": "Unexpected error.", "detail": str(exc)}
    )


@app.exception_handler(HTTPException)
async def validation_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500, content={"message": "Unexpected error.", "detail": str(exc)}
    )


# Define the health check endpoint
@app.get("/health")
def health_check():
    return {"status": "ok"}
