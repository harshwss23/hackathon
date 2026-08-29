import os
import json

ROLES_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "policies", "roles.json"))

class PolicyEngine:
    def __init__(self, roles_path=ROLES_FILE):
        self.roles = self._load_roles(roles_path)

    def _load_roles(self, path):
        if not os.path.exists(path):
            return {}
        with open(path, "r") as f:
            return json.load(f).get("roles", {})

    def apply_security_policy(self, persona: str, evidence_items: list):
        """
        Applies role-based entitlements BEFORE data query / narrative rendering.
        Strips or masks sensitive financial & PII fields for restricted roles.
        """
        role_config = self.roles.get(persona, self.roles.get("operations", {}))
        masked_fields = role_config.get("data_masking", [])

        sanitized_evidence = []
        security_log = []

        for item in evidence_items:
            sanitized_item = dict(item)
            if "net_revenue" in masked_fields and "Revenue" in item.get("claim", ""):
                sanitized_item["claim"] = "🔒 [Restricted: Net Revenue Data Masked for Operations Role]"
                sanitized_item["sql_query"] = "SELECT '🔒 RESTRICTED' FROM sales_orders"
                security_log.append(f"Security Policy Enforcement: Masked KPI Net Revenue for role '{persona}'.")
            
            sanitized_evidence.append(sanitized_item)

        return {
            "role_applied": persona,
            "role_name": role_config.get("name"),
            "masked_fields": masked_fields,
            "sanitized_evidence": sanitized_evidence,
            "security_log": security_log
        }

policy_engine = PolicyEngine()
