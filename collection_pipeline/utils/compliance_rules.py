from datetime import datetime, time
from typing import Tuple

class FZ230Checker:
    ALLOWED_CALL_START = time(8, 0)
    ALLOWED_CALL_END = time(22, 0)
    MAX_CALLS_PER_DAY = 1
    MAX_CALLS_PER_MONTH = 4

    @staticmethod
    def is_call_time_allowed(current_time: datetime = None) -> Tuple[bool, str]:
        if not current_time:
            current_time = datetime.now()
        t = current_time.time()
        if t < FZ230Checker.ALLOWED_CALL_START or t > FZ230Checker.ALLOWED_CALL_END:
            return False, f"Звонок запрещен в {t}. Разрешено 08:00-22:00."
        return True, "Время корректно."

    @staticmethod
    def check_frequency_limits(calls_today: int, calls_this_month: int) -> Tuple[bool, str]:
        if calls_today >= FZ230Checker.MAX_CALLS_PER_DAY:
            return False, f"Лимит звонков за сегодня исчерпан ({calls_today})."
        if calls_this_month >= FZ230Checker.MAX_CALLS_PER_MONTH:
            return False, f"Лимит звонков за месяц исчерпан ({calls_this_month})."
        return True, "Лимиты соблюдены."

    @staticmethod
    def validate_debtor_interaction(debtor_id: str, calls_today: int, calls_this_month: int) -> dict:
        is_time_ok, time_msg = FZ230Checker.is_call_time_allowed()
        if not is_time_ok:
            return {"allowed": False, "reason": time_msg}

        is_freq_ok, freq_msg = FZ230Checker.check_frequency_limits(calls_today, calls_this_month)
        if not is_freq_ok:
            return {"allowed": False, "reason": freq_msg}

        return {"allowed": True, "reason": "ФЗ-230 соблюден."}