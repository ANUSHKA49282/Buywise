# backend/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from forecast import get_forecast
from substitute import get_substitute

app = FastAPI()

# Allow frontend (optional)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "FlowCart API is running"}

@app.get("/forecast")
def forecast():
    return get_forecast()

@app.post("/substitute")
def substitute_endpoint(query: dict):
    return get_substitute(query["product"])
