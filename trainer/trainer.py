# Fast API RESTful API for training and fine tuning the model

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

from trainer import Trainer

app = FastAPI()

# Allow CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

trainer = Trainer()

@app.post("/train")
async def train(file: UploadFile = File(...)):
    return trainer.train(file)

@app.post("/fine-tune")
async def fine_tune(file: UploadFile = File(...)):
    return trainer.fine_tune(file)

@app.get("/update")
async def download():
    return FileResponse(trainer.download())