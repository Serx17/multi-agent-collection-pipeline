import json
from google import genai
from google.colab import userdata
from collection_pipeline.models import DebtorProfile, CollectionStrategy, CallScript

class ScriptWriterAgent:
    def __init__(self, model_name="gemini-2.5-flash"):
        self.client = genai.Client(api_key=userdata.get('GEMINI_API_KEY'))
        self.model_name = model_name

    def generate_script(self, profile: DebtorProfile, strategy: CollectionStrategy) -> CallScript:
        prompt = f"""
        Ты — профессиональный тренер по холодным звонкам и переговорам.
        Напиши скрипт разговора для оператора коллекторского агентства.

        Контекст:
        - Должник: {profile.debtor_id}
        - Тон голоса: {strategy.tone_of_voice}
        - Стратегия: {strategy.strategy_name}
        - Ключевые аргументы: {', '.join(strategy.key_arguments)}
        - Инсайты о должнике: {', '.join(profile.key_insights)}

        Требования:
        1. Соблюдай тон ({strategy.tone_of_voice}).
        2. Используй аргументы из стратегии.
        3. Будь краток и убедителен.
        4. Язык: Русский.

        Верни СТРОГО JSON:
        {{
            "opening_phrase": "...",
            "main_speech": "...",
            "objection_handling": "...",
            "closing_call_to_action": "..."
        }}
        """

        response = self.client.models.generate_content(
            model=self.model_name,
            contents=prompt
        )

        raw_text = response.text
        if "```json" in raw_text:
            raw_text = raw_text.split("```json")[1].split("```")[0]

        data = json.loads(raw_text.strip())
        return CallScript(**data)