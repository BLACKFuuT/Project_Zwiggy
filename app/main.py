from fastapi import FastAPI

app = FastAPI(title="Smart Order Platform")


@app.get("/health")
async def health_check():
    return {"status": "ok"}