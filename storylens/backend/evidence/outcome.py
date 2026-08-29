class OutcomeTracker:
    def get_closed_loop_outcome(self, incident_id: str = "INV-2026-0829-017"):
        """
        Compares predicted recommendation outcomes vs actual observed outcomes after +28 days.
        """
        return {
            "incident_id": incident_id,
            "decision_date": "2026-08-30 10:42 UTC",
            "action_executed": "Shift 22% Supplier A outbound volume to Supplier B",
            "actor": "Operations Lead (Approved)",
            "predicted_outcomes": {
                "delivery_delay_rate_pct": 8.3,
                "cancellation_rate_pct": 7.1,
                "revenue_recovery_inr": 3030000.0
            },
            "actual_observed_outcomes_28d": {
                "delivery_delay_rate_pct": 9.1,
                "cancellation_rate_pct": 7.8,
                "revenue_recovery_inr": 2720000.0
            },
            "variance": {
                "revenue_prediction_error_pct": -10.2,
                "delay_prediction_error_pp": +0.8,
                "cancellation_prediction_error_pp": +0.7
            },
            "outcome_status": "SUCCESSFUL (Revenue recovered within 10.2% tolerance window)",
            "feedback_loop_calibration": "Supplier B transfer capacity multiplier calibrated from 0.85 -> 0.76 for future simulations."
        }

    def get_decision_lineage(self, incident_id: str = "INV-2026-0829-017"):
        """
        Full provenance log tracking data, logic, decision, action, and observed outcome.
        """
        return {
            "incident_id": incident_id,
            "lineage_events": [
                { "event": "Signal Detection", "actor": "StoryLens Engine", "detail": "Revenue anomaly -8.1% detected (M=0.91)", "snapshot": "DS-08F1", "timestamp": "2026-08-29 16:40" },
                { "event": "Evidence Reconciliation", "actor": "Reconciliation Engine", "detail": "3 sources reconciled (99.1% data quality)", "snapshot": "DS-08F1", "timestamp": "2026-08-29 16:41" },
                { "event": "Causal Verification", "actor": "Analytics Engine", "detail": "DID test confirms Supplier A -6.0 pp causal effect (p < 0.01)", "snapshot": "DS-08F1", "timestamp": "2026-08-29 16:42" },
                { "event": "Analyst Review", "actor": "BI Analyst", "detail": "Accepted Supplier A primary driver ranking (84% confidence)", "snapshot": "DS-08F1", "timestamp": "2026-08-29 16:44" },
                { "event": "Decision Approval", "actor": "Operations Lead", "detail": "Approved 22% volume reallocation to Supplier B (ACT-108)", "snapshot": "ACT-108", "timestamp": "2026-08-30 10:42" },
                { "event": "Outcome Evaluation", "actor": "StoryLens Engine", "detail": "₹2.72M recovered (+28 days). Prediction error: -10.2%. Status: Successful.", "snapshot": "DS-08F9", "timestamp": "2026-09-27 10:42" }
            ]
        }

outcome_tracker = OutcomeTracker()
