from datetime import datetime, time
from typing import Tuple
class FZ230Checker:
    ALLOWED_CALL_START, ALLOWED_CALL_END = time(8,0), time(22,0)
    MAX_CALLS_PER_DAY, MAX_CALLS_PER_MONTH = 1, 4
    @staticmethod
    def is_call_time_allowed(current_time: datetime = None) -> Tuple[bool, str]:
        if not current_time: current_time = datetime.now()
        t = current_time.time()
        if t < FZ230Checker.ALLOWED_CALL_START or t > FZ230Checker.ALLOWED_CALL_END:
            return False, f"Звонок запрещен в {t}"
        return True, "OK"
    @staticmethod
    def check_frequency_limits(calls_today: int, calls_this_month: int) -> Tuple[bool, str]:
        if calls_today >= FZ230Checker.MAX_CALLS_PER_DAY: return False, "Лимит дня исчерпан"
        if calls_this_month >= FZ230Checker.MAX_CALLS_PER_MONTH: return False, "Лимит месяца исчерпан"
        return True, "OK"
    @staticmethod
    def validate_debtor_interaction(debtor_id: str, calls_today: int, calls_this_month: int) -> dict:
        ok1, msg1 = FZ230Checker.is_call_time_allowed()
        if not ok1: return {"allowed": False, "reason": msg1}
        ok2, msg2 = FZ230Checker.check_frequency_limits(calls_today, calls_this_month)
        if not ok2: return {"allowed": False, "reason": msg2}
        return {"allowed": True, "reason": "ФЗ-230 соблюден"}