import json
from google import genai
from google.colab import userdata
from collection_pipeline.models import CallScript

class ComplianceAgent:
    def __init__(self, model_name="gemini-2.5-flash"):
        self.client = genai.Client(api_key=userdata.get('GEMINI_API_KEY'))
        self.model_name = model_name

    def validate_script(self, script: CallScript) -> dict:
        full_text = f"{script.opening_phrase} {script.main_speech} {script.objection_handling} {script.closing_call_to_action}"

        prompt = f"""
        Ты — юрист-комплаенс в коллекторском агентстве РФ.
        Проверь текст скрипта на соответствие ФЗ-230.

        Текст скрипта:
        "{full_text}"

        Критические нарушения:
        1. Угрозы насилия или порчи имущества.
        2. Психологическое давление и унижение.
        3. Введение в заблуждение.
        4. Раскрытие информации третьим лицам без согласия.

        Верни СТРОГО JSON:
        {{
            "is_compliant": true/false,
            "issues": ["нарушение 1", "нарушение 2"]
        }}
        Если нарушений нет, issues должен быть пустым списком [].
        """

        response = self.client.models.generate_content(
            model=self.model_name,
            contents=prompt
        )

        raw_text = response.text
        if "```json" in raw_text:
            raw_text = raw_text.split("```json")[1].split("```")[0]

        data = json.loads(raw_text.strip())
        return data