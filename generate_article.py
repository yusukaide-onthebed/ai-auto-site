import os
import json
import urllib.request

API_KEY = os.environ["GEMINI_API_KEY"]

url = "https://generativelanguage.googleapis.com/v1beta/models"

request = urllib.request.Request(
    url,
    headers={
        "x-goog-api-key": API_KEY
    },
    method="GET"
)

with urllib.request.urlopen(request) as response:
    result = json.loads(response.read().decode("utf-8"))

print("利用可能なモデル一覧:")

for model in result.get("models", []):
    actions = model.get("supportedGenerationMethods", [])

    if "generateContent" in actions:
        print(model["name"])
