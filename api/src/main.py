from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse
import sys
import os

# Add the src directory to the sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))
from src.models.birthchart import BirthChart
from src.service.predictions import get_all_predictions

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/")
def index(request:Request):
    return templates.TemplateResponse("index.html", request=request)



    
@app.post("/birthchart")
def birthchart(birthchart:BirthChart):
    print(birthchart)
    year=1990
    month=9
    day=10
    _tob_text="02:05:00"
    birth_place = 'Delhi, India'
    result = get_all_predictions(day, month, year, _tob_text, birth_place)
    return JSONResponse({"result": result})

@app.get("/test")
def test():
    return {"status": "ok"}