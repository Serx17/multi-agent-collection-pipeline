import json
from google import genai
from google.colab import userdata
from collection_pipeline.models import DebtorRawData, DebtorProfile
class AnalystAgent:
    def __init__(self, model_name="gemini-2.5-flash"):
        self.client = genai.Client(api_key=userdata.get('GEMINI_API_KEY'))
        self.model_name = model_name
    def analyze(self, debtor: DebtorRawData) -> DebtorProfile:
        prompt = f"Проанализируй должника {debtor.full_name}. Верни JSON: risk_level, recommended_channel, sentiment_score, key_insights"
        response = self.client.models.generate_content(model=self.model_name, contents=prompt)
        raw = response.text
        if "```json" in raw: raw = raw.split("```json")[1].split("```")[0]
        data = json.loads(raw.strip())
        return DebtorProfile(debtor_id=debtor.debtor_id, **data)