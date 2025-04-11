from fastapi import FastAPI
import requests
from fastapi.middleware.cors import CORSMiddleware

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

@app.get("/get_ipl_live")
def get_ipl_live(match_id: str):
    url = f"https://api.cricapi.com/v1/match_scorecard?apikey={CRICKETDATA_API_KEY}&id={match_id}"
    response = requests.get(url)
    data = response.json()

    if not data.get("status") == "success":
        return {"error": "Match data not available or invalid match ID."}

    match_info = data["data"]
    return {
        "match_id": match_id,
        "toss_winner": match_info.get("tossWinner"),
        "toss_decision": match_info.get("tossDecision"),
        "status": match_info.get("status"),
        "venue": match_info.get("venue"),
        "team1": match_info.get("teamInfo")[0].get("name"),
        "team2": match_info.get("teamInfo")[1].get("name"),
        "playing_xi": {
            "team1": match_info.get("teamInfo")[0].get("players", []),
            "team2": match_info.get("teamInfo")[1].get("players", [])
        }
    }
