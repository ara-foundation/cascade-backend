from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class RootResponse(BaseModel):
    message: str

@app.get("/", response_model=RootResponse)
async def root():
    return {"message": "CascadeFund API"}
