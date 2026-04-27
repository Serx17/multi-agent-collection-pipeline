import json
from google import genai
from google.colab import userdata
from collection_pipeline.models import DebtorProfile, CollectionStrategy

class StrategyAgent:
    def __init__(self, model_name="gemini-2.5-flash"):
        self.client = genai.Client(api_key=userdata.get('GEMINI_API_KEY'))
        self.model_name = model_name

    def generate_strategy(self, profile: DebtorProfile) -> CollectionStrategy:
        prompt = f"""
        Ты — старший стратег отдела взыскания.
        На основе профиля должника выбери стратегию взаимодействия.

        Профиль должника:
        - Риск: {profile.risk_level}
        - Канал: {profile.recommended_channel}
        - Инсайты: {', '.join(profile.key_insights)}
        - Sentiment: {profile.sentiment_score}

        Правила выбора стратегии:
        1. Если риск 'low' или 'medium' -> 'soft_reminder', тон 'friendly' или 'neutral'.
        2. Если риск 'high' и sentiment низкий -> 'firm_demand', тон 'strict'.
        3. Если риск 'critical' -> 'legal_threat', тон 'aggressive'.
        4. Если долг большой, но клиент идет на контакт -> 'negotiation'.

        Верни СТРОГО JSON:
        {{
            "strategy_name": "...",
            "tone_of_voice": "...",
            "key_arguments": ["аргумент 1", "аргумент 2"],
            "next_step_deadline": "..."
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
        return CollectionStrategy(**data)