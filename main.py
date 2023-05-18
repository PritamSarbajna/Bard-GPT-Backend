from fastapi import FastAPI
from routes.bardgpt_routes import bardgpt_api_router

app = FastAPI()

app.include_router(bardgpt_api_router)
