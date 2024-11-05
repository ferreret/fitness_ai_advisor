import json
import os
from typing import Optional

import requests
from dotenv import load_dotenv
from langflow.load import run_flow_from_json

load_dotenv()

BASE_API_URL = "https://api.langflow.astra.datastax.com"
LANGFLOW_ID = "a954ef92-1d9b-459e-aa9a-98f97904473a"
APPLICATION_TOKEN = os.getenv("LANGFLOW_TOKEN")


def dict_to_string(obj, level=0):
    strings = []
    indent = "  " * level

    if isinstance(obj, dict):
        for key, value in obj.items():
            if isinstance(value, (dict, list)):
                nested_string = dict_to_string(value, level + 1)
                strings.append(f"{indent}{key}: {nested_string}")
            else:
                strings.append(f"{indent}{key}: {value}")
    elif isinstance(obj, list):
        for idx, item in enumerate(obj):
            nested_string = dict_to_string(item, level + 1)
            strings.append(f"{indent}Item {idx + 1}: {nested_string}")
    else:
        strings.append(f"{indent}{obj}")

    return ", ".join(strings)


def ask_ai(profile, question):

    TWEAKS = {
        "TextInput-ER4IY": {
            "input_value": question,
        },
        "TextInput-NvPw3": {
            "input_value": dict_to_string(profile),
        },
    }

    result = run_flow_from_json(
        flow="AskAIV2.json",
        input_value="message",
        session_id="",
        fallback_to_env_vars=True,
        tweaks=TWEAKS,
    )

    return result[0].outputs[0].results["text"].data["text"]


def get_macros(profile, goals):
    TWEAKS = {
        "TextInput-M2SWb": {
            "input_value": ", ".join(goals),
        },
        "TextInput-1S1jj": {
            "input_value": dict_to_string(profile),
        },
    }
    return run_flow("", tweaks=TWEAKS, application_token=APPLICATION_TOKEN)


def run_flow(
    message: str,
    output_type: str = "chat",
    input_type: str = "chat",
    tweaks: Optional[dict] = None,
    application_token: Optional[str] = None,
) -> dict:

    api_url = f"{BASE_API_URL}/lf/{LANGFLOW_ID}/api/v1/run/macros"

    payload = {
        "input_value": message,
        "output_type": output_type,
        "input_type": input_type,
    }
    headers = None
    if tweaks:
        payload["tweaks"] = tweaks
    if application_token:
        headers = {
            "Authorization": "Bearer " + application_token,
            "Content-Type": "application/json",
        }
    response = requests.post(api_url, json=payload, headers=headers)
    return json.loads(
        response.json()["outputs"][0]["outputs"][0]["results"]["text"]["data"]["text"]
    )
