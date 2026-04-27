import logging
from datetime import datetime
from typing import Dict, Any
from collection_pipeline.models import DebtorRawData
from collection_pipeline.agents.analyst import AnalystAgent
from collection_pipeline.agents.strategist import StrategyAgent
from collection_pipeline.agents.scriptwriter import ScriptWriterAgent
from collection_pipeline.agents.compliance import ComplianceAgent
from collection_pipeline.utils.compliance_rules import FZ230Checker

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CollectionPipeline:
    def __init__(self, mock_mode: bool = False):
        self.mock_mode = mock_mode
        if not mock_mode:
            self.analyst = AnalystAgent()
            self.strategist = StrategyAgent()
            self.scriptwriter = ScriptWriterAgent()
            self.compliance = ComplianceAgent()
    def run(self, debtor: DebtorRawData, calls_today: int = 0, calls_month: int = 0) -> Dict[str, Any]:
        if self.mock_mode:
            return {"status": "completed (mock)", "final_script": {"main": "Mock script"}, "compliance_check": {"is_compliant": True}}
        try:
            check = FZ230Checker.validate_debtor_interaction(debtor.debtor_id, calls_today, calls_month)
            if not check["allowed"]: return {"status": "blocked", "reason": check["reason"]}
            profile = self.analyst.analyze(debtor)
            strategy = self.strategist.generate_strategy(profile)
            script = self.scriptwriter.generate_script(profile, strategy)
            compliance = self.compliance.validate_script(script)
            if not compliance["is_compliant"]: return {"status": "failed_compliance", "issues": compliance["issues"]}
            return {"status": "completed", "final_script": {"main": script.main_speech}}
        except Exception as e:
            return {"status": "error", "error": str(e)}