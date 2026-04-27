import json
from google import genai
from google.colab import userdata
from collection_pipeline.models import DebtorRawData, DebtorProfile

class AnalystAgent:
    def __init__(self, model_name="gemini-2.5-flash"):
        # Инициализируем клиент с ключом из секретов
        self.client = genai.Client(api_key=userdata.get('GEMINI_API_KEY'))
        self.model_name = model_name

    def analyze(self, debtor: DebtorRawData) -> DebtorProfile:
        prompt = f"""
        Ты — опытный специалист по взысканию задолженности.
        Проанализируй данные должника и верни СТРОГО JSON.

        Данные:
        - ФИО: {debtor.full_name}
        - Долг: {debtor.debt_amount} руб.
        - Просрочка: {debtor.days_overdue} дн.
        - Телефон: {'Есть' if debtor.phone_number else 'Нет'}
        - Email: {'Есть' if debtor.email else 'Нет'}
        - Контакты: {debtor.previous_contacts_count} раз.

        Правила:
        1. Риск (risk_level): 'low' (<30д), 'medium' (30-90д), 'high' (>90д), 'critical' (>180д).
        2. Канал (recommended_channel): 'phone_call', 'email', 'sms', 'legal_letter'.
        3. Инсайты (key_insights): 2-3 тезиса на русском.

        Формат JSON:
        {{
            "risk_level": "...",
            "recommended_channel": "...",
            "sentiment_score": 0.0,
            "key_insights": ["...", "..."]
        }}
        """

        # Отправляем запрос через новый SDK
        response = self.client.models.generate_content(
            model=self.model_name,
            contents=prompt
        )

        raw_text = response.text

        # Очистка от markdown
        if "```json" in raw_text:
            raw_text = raw_text.split("```json")[1].split("```")[0]
        elif "```" in raw_text:
            raw_text = raw_text.split("```")[1].split("```")[0]

        data = json.loads(raw_text.strip())

        # Добавляем ID должника, которого нет в ответе LLM
        profile_data = {"debtor_id": debtor.debtor_id, **data}
        return DebtorProfile(**profile_data)