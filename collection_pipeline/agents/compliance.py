import json
from google import genai
from google.colab import userdata
from collection_pipeline.models import CallScript
class ComplianceAgent:
    def __init__(self, model_name="gemini-2.5-flash"):
        self.client = genai.Client(api_key=userdata.get('GEMINI_API_KEY'))
        self.model_name = model_name
    def validate_script(self, script: CallScript) -> dict:
        prompt = f"Проверь текст на нарушения ФЗ-230. Верни JSON: is_compliant (bool), issues (list)"
        response = self.client.models.generate_content(model=self.model_name, contents=prompt)
        raw = response.text
        if "```json" in raw: raw = raw.split("```json")[1].split("```")[0]
        return json.loads(raw.strip())