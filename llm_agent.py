from dotenv import load_dotenv
from google import genai
import json
load_dotenv()
from config import DECISIONS, SYSTEM_PROMPT, RESPONSE_SCHEMA
from typing import Dict

client = genai.Client()

def get_llm_decision(game_state: Dict, sim: Dict, risk: str) -> Dict:
    input = {
        "game_state": game_state,
        "simulation_results": sim,
        "risk_level": risk
    }

    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=json.dumps(input),
        config={
            "system_instruction": SYSTEM_PROMPT,
            "response_json_schema": RESPONSE_SCHEMA
        }
    )

    out = json.loads(response.text)

    if out["decision"] not in DECISIONS:
        raise ValueError(f"Invalid decision: {out["deicision"]}")
    if not (0.0 <= float(out["confidence"]) <= 1.0):
        raise ValueError(f"Invalid confidence score: {out["confidence"]}")
    
    return out