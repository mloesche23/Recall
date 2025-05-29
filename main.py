import app
from fastapi import FastAPI
import requests
import json
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or "*" to allow all during development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return FileResponse("static/index.html")


@app.get("/nba/scores")
async def getNBAScoresLive():
    url = "https://site.api.espn.com/apis/site/v2/sports/basketball/nba/scoreboard"
    response = requests.get(f"{url}")
    data = response.json()

    games = []
    for event in data.get("events", []):
        competition = event["competitions"][0]
        teams = competition["competitors"]
        game_data = {
            "home": teams[0]["team"]["displayName"],
            "homeScore": teams[0].get("score"),
            "away": teams[1]["team"]["displayName"],
            "awayScore": teams[1].get("score"),
            "status": event["status"]["type"]["description"],
            "startTime": competition["date"]
        }
        games.append(game_data)

    return {"games": games}

@app.get("/mlb/scores")
async def getMLBscoresLive():
    url = "https://site.api.espn.com/apis/site/v2/sports/baseball/mlb/scoreboard"
    response = requests.get(f"{url}")
    data = response.json()

    games = []
    for event in data.get("events", []):
        competition = event["competitions"][0]
        teams = competition["competitors"]
        game_data = {
            "home": teams[0]["team"]["displayName"],
            "homeScore": teams[0].get("score"),
            "away": teams[1]["team"]["displayName"],
            "awayScore": teams[1].get("score"),
            "status": event["status"]["type"]["description"],
            "startTime": competition["date"]
        }
        games.append(game_data)

    return {"games": games}