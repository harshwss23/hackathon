import os
import json
from storylens.backend.db_engine import db_engine

CONTRACTS_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "contracts", "kpis.json"))

class ContractValidator:
    def __init__(self, contracts_path=CONTRACTS_FILE):
        self.contracts_path = contracts_path
        self.contracts = self._load_contracts()
        self.validation_errors = self._validate_contracts_on_startup()

    def _load_contracts(self):
        if not os.path.exists(self.contracts_path):
            return {}
        with open(self.contracts_path, "r") as f:
            data = json.load(f)
            return data.get("kpis", {})

    def _validate_contracts_on_startup(self):
        errors = []
        for kpi_id, kpi in self.contracts.items():
            lineage = kpi.get("lineage", [])
            for ref in lineage:
                table_name = ref.split(".")[0]
                if table_name not in ["sales", "logistics", "support", "customer"]:
                    errors.append(f"KPI {kpi_id} references invalid source: {ref}")
        return errors

    def get_contract(self, kpi_id: str):
        return self.contracts.get(kpi_id)

    def get_all_contracts(self):
        return self.contracts

contract_validator = ContractValidator()
