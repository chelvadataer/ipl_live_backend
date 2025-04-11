from fastapi import FastAPI
import requests
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

app = FastAPI()

# Replace with your real API key from cricketdata.org
CRICKETDATA_API_KEY = "8a33d409-9392-4c8f-9820-de47e0d46745"

# Optional: Allow cross-origin access if you're using this from a frontend/chatbot
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return JSONResponse(content={"message": "🎯 DT CREATOR API is live! Ready to serve Dream11 IPL data."})

@app.get("/get_ipl_live")
def get_ipl_live(match_id: str):
    url = f"https://api.cricapi.com/v1/match_scorecard?apikey={CRICKETDATA_API_KEY}&id={match_id}"
    response = requests.get(url)
    data = response.json()

    if not data.get("status") == "success":
        return {"error": "Match data not available or invalid match ID."}

    match_info = data.get("data", {})

    team1_info = match_info.get("teamInfo", [{}])[0]
    team2_info = match_info.get("teamInfo", [{}])[1] if len(match_info.get("teamInfo", [])) > 1 else {}

    return {
        "match_id": match_id,
        "toss_winner": match_info.get("tossWinner"),
        "toss_decision": match_info.get("tossDecision"),
        "status": match_info.get("status"),
        "venue": match_info.get("venue"),
        "team1": team1_info.get("name", "N/A"),
        "team2": team2_info.get("name", "N/A"),
        "playing_xi": {
            "team1": team1_info.get("players", []),
            "team2": team2_info.get("players", [])
        }
    }

@app.get("/list_ipl_matches")
def list_ipl_matches():
    url = f"https://api.cricapi.com/v1/currentMatches?apikey={CRICKETDATA_API_KEY}"
    response = requests.get(url)
    data = response.json()

    if not data.get("status") == "success":
        return {"error": "Unable to fetch matches"}

    ipl_matches = []
    ipl_teams = {
        "Mumbai Indians", "Chennai Super Kings", "Royal Challengers Bengaluru",
        "Delhi Capitals", "Punjab Kings", "Rajasthan Royals",
        "Kolkata Knight Riders", "Sunrisers Hyderabad", "Lucknow Super Giants",
        "Gujarat Titans"
    }

    for match in data["data"]:
        if set(match["teams"]) & ipl_teams:
            ipl_matches.append({
                "match_id": match["id"],
                "name": match["name"],
                "teams": match["teams"],
                "status": match["status"],
                "venue": match["venue"],
                "date": match["date"],
                "match_type": match["matchType"]
            })

    return {"matches": ipl_matches}
