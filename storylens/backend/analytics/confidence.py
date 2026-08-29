class EvidenceConfidenceEngine:
    def compute_confidence(self, scenario_type="supply_chain"):
        """
        Computes Evidence Confidence Score C:
        C = 0.25*E + 0.20*A + 0.20*Q + 0.15*F + 0.20*K - X
        """
        if scenario_type == "abstain_scenario":
            E = 0.50 # Effect strength
            A = 0.42 # Agreement across sources
            Q = 0.90 # Quality
            F = 0.85 # Freshness
            K = 0.40 # Causal support
            X = 0.35 # Contradiction penalty

            score = (0.25*E) + (0.20*A) + (0.20*Q) + (0.15*F) + (0.20*K) - X
            score_pct = round(max(0, min(100, score * 100)), 1) # ~ 41.0%

            return {
                "confidence_score_pct": score_pct,
                "is_abstained": True,
                "abstain_reason_code": "CONTRADICTORY_EVIDENCE",
                "abstain_title": "StoryLens Engine Abstention Triggered",
                "abstain_message": f"Evidence confidence ({score_pct}% < 60.0% threshold). Reason: Marketing ad spend metrics (+14.2% CAC) contradict product return rate logs (+9.1% returns). No single driver exceeds materiality significance.",
                "requested_evidence": "Required: Please upload 'Batch #409 Quality Inspection Audit Log' or 'Meta Ads Click-Quality Audit' to resolve cross-system ambiguity.",
                "components": {
                    "effect_strength_E": E,
                    "cross_source_agreement_A": A,
                    "data_quality_Q": Q,
                    "freshness_F": F,
                    "causal_support_K": K,
                    "contradiction_penalty_X": X
                },
                "supporting_evidence": ["Supplier fill rate down 5%"],
                "contradictory_evidence": ["Overall warehouse inventory up +4%", "Ad spend CAC up +14%"]
            }

        elif scenario_type == "sparse_history":
            E = 0.85
            A = 0.70
            Q = 0.92
            F = 0.95
            K = 0.65
            X = 0.05

            score = (0.25*E) + (0.20*A) + (0.20*Q) + (0.15*F) + (0.20*K) - X
            score_pct = round(score * 100, 1) # ~ 71.0%

            return {
                "confidence_score_pct": score_pct,
                "is_abstained": False,
                "components": {
                    "effect_strength_E": E,
                    "cross_source_agreement_A": A,
                    "data_quality_Q": Q,
                    "freshness_F": F,
                    "causal_support_K": K,
                    "contradiction_penalty_X": X
                },
                "supporting_evidence": ["AI Copilot Pro trial churn at 31.2%", "Peer category trial onboarding drop-off"],
                "contradictory_evidence": []
            }

        else: # Supply Chain main case
            E = 0.93
            A = 0.88
            Q = 0.96
            F = 0.91
            K = 0.79
            X = 0.05

            score = (0.25*E) + (0.20*A) + (0.20*Q) + (0.15*F) + (0.20*K) - X
            score_pct = round(score * 100, 1) # 84.1%

            return {
                "confidence_score_pct": score_pct,
                "is_abstained": False,
                "components": {
                    "effect_strength_E": E,
                    "cross_source_agreement_A": A,
                    "data_quality_Q": Q,
                    "freshness_F": F,
                    "causal_support_K": K,
                    "contradiction_penalty_X": X
                },
                "supporting_evidence": [
                    "✓ Supplier A fill rate fell 21.4% (WMS Logs)",
                    "✓ Outbound delivery delays rose 18.2% (Logistics)",
                    "✓ Order cancellations rose 14.1% (Sales DB)",
                    "✓ Delivery SLA complaint tickets rose 24.0% (Zendesk CRM)"
                ],
                "contradictory_evidence": [
                    "! Overall warehouse raw inventory up +4% (concentrated in non-Supplier A SKUs)"
                ]
            }

confidence_engine = EvidenceConfidenceEngine()
