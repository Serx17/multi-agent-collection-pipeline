import json
from google import genai
from google.colab import userdata
from collection_pipeline.models import DebtorProfile, CollectionStrategy, CallScript
class ScriptWriterAgent:
    def __init__(self, model_name="gemini-2.5-flash"):
        self.client = genai.Client(api_key=userdata.get('GEMINI_API_KEY'))
        self.model_name = model_name
    def generate_script(self, profile: DebtorProfile, strategy: CollectionStrategy) -> CallScript:
        prompt = f"Напиши скрипт (тон: {strategy.tone_of_voice}) по стратегии {strategy.strategy_name}. Соблюдай ФЗ-230. Верни JSON: opening_phrase, main_speech, objection_handling, closing_call_to_action"
        response = self.client.models.generate_content(model=self.model_name, contents=prompt)
        raw = response.text
        if "```json" in raw: raw = raw.split("```json")[1].split("```")[0]
        return CallScript(**json.loads(raw.strip()))