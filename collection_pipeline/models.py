from pydantic import BaseModel, Field
from typing import Optional, List, Literal
from datetime import date, datetime

class DebtorRawData(BaseModel):
    debtor_id: str
    full_name: str
    debt_amount: float
    days_overdue: int
    phone_number: Optional[str] = None
    email: Optional[str] = None
    last_payment_date: Optional[date] = None
    previous_contacts_count: int = 0

class DebtorProfile(BaseModel):
    debtor_id: str
    risk_level: Literal["low", "medium", "high", "critical"]
    recommended_channel: Literal["sms", "email", "phone_call", "legal_letter"]
    sentiment_score: float
    key_insights: List[str] = []
    analysis_timestamp: datetime = Field(default_factory=datetime.now)

class CollectionStrategy(BaseModel):
    strategy_name: Literal["soft_reminder", "firm_demand", "negotiation", "legal_threat"]
    tone_of_voice: Literal["friendly", "neutral", "strict", "aggressive"]
    key_arguments: List[str]
    next_step_deadline: str

class CallScript(BaseModel):
    opening_phrase: str
    main_speech: str
    objection_handling: str
    closing_call_to_action: str