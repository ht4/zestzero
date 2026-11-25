from pathlib import Path
from fastapi import FastAPI
from typing import Literal
from app.playground import simulate
from fastapi.staticfiles import StaticFiles
from app.assurance import snapshot

app=FastAPI(title='ZestZero laboratory')
@app.get('/api/results')
def results():
    return snapshot()

@app.get('/api/playground')
def playground(version: Literal['baseline','corrected'], user: Literal['analyst-a','analyst-b','reviewer','unknown'], topic: Literal['notice','pricing','budget','public'], operation: Literal['document','summary','revoked']):
    return simulate(version,user,topic,operation)

app.mount('/', StaticFiles(directory=Path(__file__).resolve().parents[1]/'site',html=True),name='site')
