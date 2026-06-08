from fastapi import FastAPI

app = FastAPI(title="AI-App-Compiler API")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/api/hello")
def hello():
    return {"message": "Hello from backend"}
