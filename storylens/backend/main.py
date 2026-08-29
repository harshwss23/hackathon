import os
import sys
import time
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from storylens.backend.db_engine import db_engine
from storylens.backend.semantic.contracts import contract_validator
from storylens.backend.semantic.reconciliation import reconciliation_engine
from storylens.backend.analytics.materiality import materiality_engine
from storylens.backend.analytics.anomaly import anomaly_detector
from storylens.backend.analytics.contribution import contribution_engine
from storylens.backend.analytics.causal import causal_engine
from storylens.backend.analytics.confidence import confidence_engine
from storylens.backend.analytics.robustness import robustness_engine
from storylens.backend.analytics.falsification import falsification_engine
from storylens.backend.evidence.ledger import evidence_ledger
from storylens.backend.evidence.outcome import outcome_tracker
from storylens.backend.recommendations.simulator import action_simulator
from storylens.backend.narrative.llm import llm_narrative_gen
from storylens.backend.narrative.verifier import claim_verifier
from storylens.backend.governance.policy import policy_engine
from storylens.backend.governance.registry import analytics_registry
from storylens.backend.governance.data_anomaly import data_discriminator
from storylens.backend.memory.decision_memory import decision_memory
from storylens.backend.telemetry.metrics import telemetry_tracker

def handle_investigate(scenario_id: str = "supply_chain", persona: str = "executive"):
    start_time = time.time()

    data_incident_check = data_discriminator.evaluate_incident_type(scenario_id)
    sources_reconciliation = reconciliation_engine.get_source_freshness_and_quality()

    anomaly_result = anomaly_detector.detect_anomalies([-2.0, -1.5, 0.0, -2.4, -5.1, -7.2, -8.4, -8.4])
    materiality_result = materiality_engine.calculate_materiality(
        statistical_surprise=anomaly_result["robust_zscore"],
        business_impact_usd=8100000.0,
        persistence_ratio=0.85
    )

    decomp_result = contribution_engine.decompose_revenue_gap()
    tree_result = contribution_engine.get_hierarchical_contribution_tree()
    causal_result = causal_engine.compute_difference_in_differences("Supplier A")
    confidence_data = confidence_engine.compute_confidence(scenario_id)

    raw_evidence_pkg = evidence_ledger.get_evidence_package()
    security_result = policy_engine.apply_security_policy(persona, raw_evidence_pkg["evidence_items"])

    narrative_result = llm_narrative_gen.generate_narrative(
        persona=persona,
        evidence_pkg={"evidence_items": security_result["sanitized_evidence"]},
        confidence_data=confidence_data,
        scenario_type=scenario_id
    )

    verifier_result = claim_verifier.verify_narrative_claims(
        narrative_text=narrative_result.get("summary", ""),
        evidence_items=raw_evidence_pkg["evidence_items"]
    )

    falsification_data = falsification_engine.get_falsification_conditions(confidence_data.get("confidence_score_pct", 84.1))
    robustness_data = robustness_engine.run_robustness_simulation(22.0, 500)
    outcome_data = outcome_tracker.get_closed_loop_outcome()
    lineage_data = outcome_tracker.get_decision_lineage()
    memory_data = decision_memory.find_similar_historical_incidents()
    registry_data = analytics_registry.get_verified_registry()
    drift_data = analytics_registry.check_semantic_drift()

    telemetry_result = telemetry_tracker.get_telemetry(start_time, scenario_id)

    return {
        "scenario_id": scenario_id,
        "persona": persona,
        "data_incident_check": data_incident_check,
        "sources_reconciliation": sources_reconciliation,
        "materiality": materiality_result,
        "anomaly": anomaly_result,
        "decomposition": decomp_result,
        "contribution_tree": tree_result,
        "causal_support": causal_result,
        "confidence": confidence_data,
        "falsification": falsification_data,
        "robustness": robustness_data,
        "closed_loop_outcome": outcome_data,
        "decision_lineage": lineage_data,
        "decision_memory": memory_data,
        "analytics_registry": registry_data,
        "semantic_drift": drift_data,
        "security": {
            "role_name": security_result["role_name"],
            "masked_fields": security_result["masked_fields"],
            "security_log": security_result["security_log"]
        },
        "evidence_package": security_result["sanitized_evidence"],
        "narrative": narrative_result,
        "claim_verifier": verifier_result,
        "telemetry": telemetry_result
    }

def handle_simulate(reallocate_pct: float):
    sim = action_simulator.simulate_supplier_reallocation(reallocate_pct)
    mc = robustness_engine.run_robustness_simulation(reallocate_pct, 500)
    sim["monte_carlo_robustness"] = mc
    return sim
