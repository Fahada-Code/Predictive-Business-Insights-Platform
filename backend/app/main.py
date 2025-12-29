from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import forecast

app = FastAPI(title="Predictive Business Insights Platform")

# Configure CORS
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:3000", # In case they use nextjs/default vite
    "*" # For dev simplicity
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register Routers
app.include_router(forecast.router)

@app.get("/")
def root():
    return {"status": "Backend is running"}
