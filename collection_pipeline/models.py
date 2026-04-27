from pydantic import BaseModel, Field
from typing import Optional, List, Literal
from datetime import date, datetime

# --- Модель входных данных (сырые данные из CRM) ---
class DebtorRawData(BaseModel):
    """Сырые данные о должнике из базы данных."""
    debtor_id: str = Field(..., description="Уникальный ID должника")
    full_name: str = Field(..., description="ФИО должника")
    debt_amount: float = Field(..., gt=0, description="Сумма долга в рублях")
    days_overdue: int = Field(..., ge=0, description="Количество дней просрочки")

    # Контакты
    phone_number: Optional[str] = Field(None, description="Номер телефона")
    email: Optional[str] = Field(None, description="Email адрес")

    # История
    last_payment_date: Optional[date] = Field(None, description="Дата последнего платежа")
    previous_contacts_count: int = Field(0, ge=0, description="Сколько раз уже связывались")

# --- Модель профиля (выход Агента 1: Аналитика) ---
class DebtorProfile(BaseModel):
    """Обогащенный профиль должника после анализа."""
    debtor_id: str
    risk_level: Literal["low", "medium", "high", "critical"] = Field(..., description="Уровень риска невозврата")
    recommended_channel: Literal["sms", "email", "phone_call", "legal_letter"] = Field(..., description="Предпочтительный канал связи")
    sentiment_score: float = Field(..., ge=-1.0, le=1.0, description="Оценка эмоционального состояния (от негатива к позитиву)")
    key_insights: List[str] = Field(default_factory=list, description="Ключевые инсайты для оператора")
    analysis_timestamp: datetime = Field(default_factory=datetime.now, description="Время анализа")