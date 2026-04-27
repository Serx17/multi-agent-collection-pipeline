import json
from google import genai
from google.colab import userdata
from collection_pipeline.models import DebtorProfile, CollectionStrategy
class StrategyAgent:
    def __init__(self, model_name="gemini-2.5-flash"):
        self.client = genai.Client(api_key=userdata.get('GEMINI_API_KEY'))
        self.model_name = model_name
    def generate_strategy(self, profile: DebtorProfile) -> CollectionStrategy:
        prompt = f"Выбери стратегию для риска {profile.risk_level}. Верни JSON: strategy_name, tone_of_voice, key_arguments, next_step_deadline"
        response = self.client.models.generate_content(model=self.model_name, contents=prompt)
        raw = response.text
        if "```json" in raw: raw = raw.split("```json")[1].split("```")[0]
        return CollectionStrategy(**json.loads(raw.strip()))