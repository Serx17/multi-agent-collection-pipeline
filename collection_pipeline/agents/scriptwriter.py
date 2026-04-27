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
        Ты — профессиональный оператор коллекторского агентства РФ.
        Напиши скрипт разговора, СТРОГО соблюдая ФЗ-230.

        ВАЖНО: Запрещены угрозы, унижения, давление и ложь.
        Даже если стратегия 'firm_demand' или тон 'strict', оставайся в рамках закона и делового этикета.

        Контекст:
        - Должник: {profile.debtor_id}
        - Тон: {strategy.tone_of_voice} (трактуй 'strict' как 'настойчивый и официальный', а не грубый)
        - Стратегия: {strategy.strategy_name}
        - Аргументы: {', '.join(strategy.key_arguments)}

        Верни СТРОГО JSON:
        {{
            "opening_phrase": "Вежливое приветствие...",
            "main_speech": "Суть звонка...",
            "objection_handling": "Ответ на 'нет денег'...",
            "closing_call_to_action": "Призыв к действию..."
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