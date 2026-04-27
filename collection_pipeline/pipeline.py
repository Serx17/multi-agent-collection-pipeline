import logging
from datetime import datetime
from typing import Dict, Any

from collection_pipeline.models import DebtorRawData, DebtorProfile, CollectionStrategy, CallScript
from collection_pipeline.agents.analyst import AnalystAgent
from collection_pipeline.agents.strategist import StrategyAgent
from collection_pipeline.agents.scriptwriter import ScriptWriterAgent
from collection_pipeline.agents.compliance import ComplianceAgent
from collection_pipeline.utils.compliance_rules import FZ230Checker

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class CollectionPipeline:
    def __init__(self, mock_mode: bool = False):
        logger.info("🚀 Инициализация пайплайна взыскания...")
        self.mock_mode = mock_mode
        if not mock_mode:
            self.analyst = AnalystAgent()
            self.strategist = StrategyAgent()
            self.scriptwriter = ScriptWriterAgent()
            self.compliance = ComplianceAgent()

    def run(self, debtor: DebtorRawData, calls_today: int = 0, calls_month: int = 0) -> Dict[str, Any]:
        start_time = datetime.now()
        report = {
            "debtor_id": debtor.debtor_id,
            "status": "started",
            "steps": [],
            "final_script": None,
            "compliance_check": None
        }

        # === MOCK MODE: Возвращаем тестовые данные без API ===
        if self.mock_mode:
            logger.info("🎭 Запуск в режиме эмуляции (mock_mode)...")
            return {
                "debtor_id": debtor.debtor_id,
                "status": "completed (mock)",
                "steps": [
                    {"step": "fz230_check", "status": "passed"},
                    {"step": "analysis", "risk": "medium"},
                    {"step": "strategy", "name": "soft_reminder"}
                ],
                "final_script": {
                    "opening": f"Добрый день, {debtor.full_name}. Это [Агентство] по вопросу задолженности.",
                    "main": f"Напоминаем о задолженности {debtor.debt_amount} руб. Просим связаться с нами.",
                    "objection": "Понимаем ваши обстоятельства. Давайте обсудим варианты решения.",
                    "closing": "Ждем вашего звонка до конца дня. Спасибо."
                },
                "compliance_check": {"is_compliant": True, "issues": []}
            }

        try:
            # 1. Pre-check: ФЗ-230
            logger.info(f"🛡️ Проверка ограничений для {debtor.debtor_id}...")
            check_result = FZ230Checker.validate_debtor_interaction(
                debtor.debtor_id, calls_today, calls_month
            )

            if not check_result["allowed"]:
                report["status"] = "blocked_by_fz230"
                report["reason"] = check_result["reason"]
                logger.warning(f"⛔ Пайплайн остановлен: {check_result['reason']}")
                return report

            report["steps"].append({"step": "fz230_check", "status": "passed"})

            # 2. Agent 1: Анализ
            logger.info("🕵️‍♂️ Запуск Analyst...")
            profile = self.analyst.analyze(debtor)
            report["steps"].append({"step": "analysis", "risk": profile.risk_level})

            # 3. Agent 2: Стратегия
            logger.info("🧠 Запуск Strategist...")
            strategy = self.strategist.generate_strategy(profile)
            report["steps"].append({"step": "strategy", "name": strategy.strategy_name})

            # 4. Agent 3: Скрипт
            logger.info("📝 Запуск ScriptWriter...")
            script = self.scriptwriter.generate_script(profile, strategy)

            # 5. Agent 4: Комплаенс
            logger.info("⚖️ Запуск Compliance Check...")
            compliance_result = self.compliance.validate_script(script)
            report["compliance_check"] = compliance_result

            if not compliance_result["is_compliant"]:
                report["status"] = "failed_compliance"
                report["issues"] = compliance_result["issues"]
                logger.error(f"❌ Скрипт отклонен комплаенсом: {compliance_result['issues']}")
                return report

            # Успех
            report["status"] = "completed"
            report["final_script"] = {
                "opening": script.opening_phrase,
                "main": script.main_speech,
                "objection": script.objection_handling,
                "closing": script.closing_call_to_action
            }

            duration = (datetime.now() - start_time).total_seconds()
            logger.info(f"✅ Пайплайн завершен за {duration:.2f} сек.")

        except Exception as e:
            report["status"] = "error"
            report["error"] = str(e)
            logger.error(f"💥 Критическая ошибка пайплайна: {e}")

        return report