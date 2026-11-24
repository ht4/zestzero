from pathlib import Path
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.assurance import snapshot

app=FastAPI(title='ZestZero laboratory')
@app.get('/api/results')
def results():
    return snapshot()

app.mount('/',StaticFiles(directory=Path(__file__).resolve().parents[1]/'site',html=True),name='site')
