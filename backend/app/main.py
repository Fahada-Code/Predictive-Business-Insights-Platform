from fastapi import FastAPI

app = FastAPI(title="Predictive Business Insights Platform")

@app.get("/")
def root():
    return {"status": "Backend is running"}
