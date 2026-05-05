#  Multi-Agent Collection Pipeline

> **AI-powered debt collection system with FZ-230 compliance checks**  
> *End-to-end решение для автоматизации взыскания задолженности с соблюдением российского законодательства*

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![Gemini API](https://img.shields.io/badge/Gemini-API-green?logo=google)
![Pydantic](https://img.shields.io/badge/Pydantic-v2-E92063?logo=python)
![Status](https://img.shields.io/badge/Status-MVP-orange)

---

##  Executive Summary

| Параметр | Значение |
|----------|----------|
| **Цель** | Автоматизация взыскания с сохранением юридической безопасности и операционной эффективности |
| **Архитектура** | Мультиагентная система с оркестрацией, типизированными интерфейсами и валидацией |
| **Регуляторика** | Полное соответствие ФЗ-230 (РФ) через детерминированный код + LLM-комплаенс |
| **Stack** | Python 3.10+, Pydantic v2, Google Gemini API (`google-genai`), Google Colab |
| **Режимы** | `Production` (с API) / `Demo` (mock mode без затрат на токены) |

> 💡 **Уникальное ценностное предложение**:  
> Проект объединяет 14 лет опыта в банковском секторе, взыскании и юриспруденции с современными практиками AI-разработки. Это не просто промпт-инженеринг, а архитектурно выверенное решение с четким разделением ответственности между LLM и детерминированным кодом.

---

##  Об авторе

Сергей Антоненко | AI Solutions Architect
🏦 10+ лет в банковском секторе: операционное управление, колл-центры, омниканальные стратегии
⚖️ 6 лет юридического опыта: взыскание долгов, медиация, судебное сопровождение, ФССП
🎓 Высшее юридическое образование + курсы по аналитике данных и тестированию ПО
🤖 Практический опыт: NLP/ML-проекты, Telegram-боты, интеграции с нейросетями, vibe-coding


> *"Я создаю AI-решения, которые работают не только технически, но и юридически безопасно — потому что понимаю бизнес-контекст изнутри."*

🔗 [GitHub](https://github.com/Serx17) | 📧 [Связаться](mailto:alice@example.com)

---


## ️ Архитектура системы

### Высокоуровневая схема потока данных


┌─────────────────────────────────────────────────────┐
│ DebtorRawData │
│ (сырые данные из CRM: долг, просрочка, контакты) │
└────────────────┬────────────────────────────────────
│
▼
─────────────────────────────────────────────────────┐
│ FZ230Checker (Pre-flight Check) │
│ • Время звонков: 08:00–22:00 │
│ • Лимиты: ≤1 звонка/день, ≤4/месяц │
│ • Детерминированная логика (НЕ LLM) │
└───────┬──────────────────────┬──────────────────────┘
│ │
[Blocked] [Allowed]
│ │
▼ ▼
───────────────┐ ┌─────────────────────────────┐
│ Return early │ │ AnalystAgent │
│ with reason │ │ • Оценка риска │
└───────────────┘ │ • Выбор канала связи │
│ • Sentiment-анализ │
└────────┬────────────────────
│
▼
┌─────────────────────────────┐
│ StrategistAgent │
│ • Выбор стратегии и тона │
└────────────────────────────┘
│
▼
┌─────────────────────────────┐
│ ScriptWriterAgent │
│ • Генерация текста скрипта │
────────┬────────────────────┘
│
▼
┌─────────────────────────────┐
│ ComplianceAgent │
│ • Пост-генерационная проверка│
│ • Детекция нарушений ФЗ-230 │
└────────┬────────────────────┘
│
┌────────────┴────────────┐
▼ ▼
[Approved] [Rejected]
│ │
▼ ▼
┌─────────────────────┐ ┌─────────────────────────
│ Final CallScript │ │ Audit Log + │
│ + Timestamp │ │ Notification to human │
└─────────────────────┘ └─────────────────────────┘


### Компоненты проекта

| Модуль | Файл | Ответственность | Ключевые технологии |
|--------|------|-----------------|-------------------|
| **Модели данных** | `models.py` | Типизированные схемы Pydantic для всех сущностей | Pydantic v2, Python type hints |
| **Агент: Аналитик** | `agents/analyst.py` | Оценка риска, выбор канала, sentiment-анализ | Gemini API, prompt engineering |
| **Агент: Стратег** | `agents/strategist.py` | Выбор стратегии и тона на основе профиля | Rule-based + LLM hybrid |
| **Агент: Скриптер** | `agents/scriptwriter.py` | Генерация персонализированного текста | Text generation, tone control |
| **Агент: Комплаенс** | `agents/compliance.py` | Валидация скрипта на соответствие ФЗ-230 | LLM-as-a-judge pattern |
| **Утилиты ФЗ-230** | `utils/compliance_rules.py` | Детерминированные проверки времени и лимитов | Pure Python, no external deps |
| **Оркестратор** | `pipeline.py` | Управление потоком, обработка ошибок, логирование | Design Pattern: Pipeline/Chain |
| **Демо-ноутбук** | `notebooks/01_setup_and_architecture.ipynb` | Интерактивная демонстрация для работодателя | Google Colab, mock mode |

---

## ⚙️ Ключевые архитектурные решения

### 1. Разделение ответственности: LLM ↔ Code

```python
# ❌ НЕПРАВИЛЬНО: доверять регуляторику нейросети
prompt = "Проверь, можно ли звонить должнику сейчас, по ФЗ-230"

# ✅ ПРАВИЛЬНО: детерминированная проверка в коде
from collection_pipeline.utils.compliance_rules import FZ230Checker

result = FZ230Checker.validate_debtor_interaction(
    debtor_id="D-123", calls_today=0, calls_this_month=2
)
if not result["allowed"]:
    return {"status": "blocked", "reason": result["reason"]}

Почему это важно: 100% надежность, экономия токенов, юридическая безопасность, скорость проверки (мкс vs сек).
2. Типизированные интерфейсы между агентами

class DebtorProfile(BaseModel):
    debtor_id: str
    risk_level: Literal["low", "medium", "high", "critical"]
    recommended_channel: Literal["sms", "email", "phone_call", "legal_letter"]
    sentiment_score: float = Field(ge=-1.0, le=1.0)
    key_insights: List[str]

Преимущества: Раннее обнаружение ошибок, автодокументация, упрощенное тестирование, безопасный рефакторинг.
3. Mock Mode для демо и CI/CD

class CollectionPipeline:
    def __init__(self, mock_mode: bool = False):
        self.mock_mode = mock_mode
        if not mock_mode:
            self.analyst = AnalystAgent()
            # ...
    
    def run(self, debtor: DebtorRawData) -> dict:
        if self.mock_mode:
            return {"status": "completed (mock)", "final_script": {"main": "Mock script text"}}
        # ... реальная логика с вызовами API

Use cases: Демонстрация на собеседовании без интернета, юнит-тесты без затрат на токены, быстрая отладка.
4. Обработка ошибок и логирование

try:
    profile = self.analyst.analyze(debtor)
    strategy = self.strategist.generate_strategy(profile)
except ValidationError as e:
    logger.error(f"Data validation failed: {e.errors()}")
    return {"status": "error", "error": "invalid_data"}
except Exception as e:
    logger.exception("Unexpected error in pipeline")
    return {"status": "error", "error": str(e)}

🚀 Быстрый старт

Вариант 1: Локальный запуск

git clone https://github.com/Serx17/multi-agent-collection-pipeline.git
cd multi-agent-collection-pipeline
pip install -r requirements.txt
python -m collection_pipeline.main --mock

Вариант 2: Интеграция в код

from collection_pipeline.pipeline import CollectionPipeline
from collection_pipeline.models import DebtorRawData

pipeline = CollectionPipeline(mock_mode=False)
debtor = DebtorRawData(
    debtor_id="D-2024-001", full_name="Петров П.П.",
    debt_amount=75000.00, days_overdue=62, phone_number="+79991234567"
)
result = pipeline.run(debtor, calls_today=0, calls_month=2)

📊 Примеры работы
Кейс 1: Успешный сценарий

{
  "status": "completed",
  "steps": [
    {"step": "fz230_check", "status": "passed"},
    {"step": "analysis", "risk": "medium", "channel": "phone_call"},
    {"step": "strategy", "name": "soft_reminder", "tone": "neutral"},
    {"step": "compliance", "is_compliant": true}
  ],
  "final_script": {
    "opening": "Добрый день, Алексей. Это [Агентство], напоминаем о задолженности...",
    "main": "На текущий момент сумма задолженности составляет 50 000 рублей...",
    "objection_handling": "Понимаем, что обстоятельства могут быть разными...",
    "closing": "Просим связаться с нами до конца недели..."
  }
}

Кейс 2: Блокировка по ФЗ-230

{
  "status": "blocked_by_fz230",
  "reason": "Звонок запрещен в 23:30:00. Разрешено с 08:00 до 22:00."
}

Кейс 3: Отклонение комплаенсом

{
  "status": "failed_compliance",
  "issues": [
    "Психологическое давление: фраза 'у вас не останется выбора' может трактоваться как угроза",
    "Раскрытие информации: упоминание места работы должника без согласия"
  ]
}

🔐 Безопасность и соответствие ФЗ-230
Требование закона
Реализация в проекте
Звонки только 08:00–22:00
FZ230Checker.is_call_time_allowed()
≤1 звонка в день, ≤4 в месяц
FZ230Checker.check_frequency_limits()
Запрет на угрозы и унижения
ComplianceAgent + промпт-инструкции
Запрет на раскрытие данных третьим лицам
Валидация в ScriptWriterAgent + пост-чек
Секреты и ключи
.env / Colab Secrets, исключены из Git через .gitignore
⚠️ Важно: Проект является демонстрационным прототипом. Для промышленного использования требуется аудит юристом и интеграция с CRM/системой учета согласий.
📈 Метрики и Roadmap
Метрика
Целевое значение
Как измеряется
Время выполнения
< 30 сек
datetime в pipeline.py
Успешность генерации
> 95%
Логирование статусов
Точность compliance
100%*
Детерминированный код + тесты
Стоимость запуска
~$0.0003–0.001
Мониторинг токенов Gemini API
*При условии корректных входных данных
🗺️ Roadmap
✅ v1.0 MVP: Мультиагентная архитектура, Pydantic, FZ-230, Mock Mode
🔄 v1.1: Интеграция с Telegram-ботом, кэширование LLM, экспорт в CRM
💡 v2.0: Адаптивное обучение, голосовые боты, предиктивная аналитика возврата


