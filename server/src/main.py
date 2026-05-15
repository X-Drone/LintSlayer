# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core import settings
from infra.persist import db
from infra.persist import Base
from infra.web.api.router import router

app = FastAPI(debug=settings.debug)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Try to create tables on startup, this will not do anything if the tables already exist
Base.metadata.create_all(bind=db.engine)

# Include API routes
app.include_router(router)
