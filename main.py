from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi import FastAPI, Query, Request

from db import Database
from models import SlotRequest , BookRequest

app = FastAPI()
templates = Jinja2Templates(directory="templates")
db = Database()

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/slots")
def post_slots(payload: SlotRequest):
    db.add_slots(payload.users)
    return {"message" : "Slots added"}

@app.get("/suggest")
def get_suggestion(duration: int = Query(..., description="Duration in minutes for the slot suggestion")):
    return [[s["start"], s["end"]] for s in db.suggest_slots(duration)[:3]]

@app.post("/book")
def book_slot(payload: BookRequest):
    db.book_slot(payload)
    return {"message": "Slot booked successfully"}

@app.get("/calendar/{userId}")
def get_calendar(userId: int):
    return db.get_user_calendar(userId)
