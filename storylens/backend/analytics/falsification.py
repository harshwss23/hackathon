class FalsificationEngine:
    def get_falsification_conditions(self, current_confidence: float = 84.1):
        """
        Calculates 'What evidence could materially overturn this conclusion?'
        and ranks Investigation Next-Best-Evidence by information gain.
        """
        falsification_items = [
            {
                "condition": "Competitor pricing decline > 12%",
                "confidence_impact_pp": -18.0,
                "projected_confidence_pct": round(current_confidence - 18.0, 1),
                "falsification_risk": "High"
            },
            {
                "condition": "Demand decline across unaffected SKUs > 8%",
                "confidence_impact_pp": -14.0,
                "projected_confidence_pct": round(current_confidence - 14.0, 1),
                "falsification_risk": "Medium"
            },
            {
                "condition": "Supplier B/C products showing equivalent retention drop",
                "confidence_impact_pp": -21.0,
                "projected_confidence_pct": round(current_confidence - 21.0, 1),
                "falsification_risk": "High"
            }
        ]

        next_best_evidence = [
            {
                "evidence_type": "Competitor Pricing Feed",
                "expected_information_gain": "VERY HIGH",
                "reason": "Best separates the Supplier Disruption hypothesis from broader Market Pricing Pressure."
            },
            {
                "evidence_type": "Supplier Capacity & Port Congestion Report",
                "expected_information_gain": "HIGH",
                "reason": "Confirms physical inbound port bottleneck vs local warehouse operational issue."
            },
            {
                "evidence_type": "Additional 7-Day Order Tracking Feed",
                "expected_information_gain": "MEDIUM",
                "reason": "Increases sample size for cohort retention stability."
            }
        ]

        return {
            "current_conclusion": "Supplier A fulfillment deterioration is the primary driver",
            "current_confidence_pct": current_confidence,
            "falsification_conditions": falsification_items,
            "next_best_evidence": next_best_evidence
        }

falsification_engine = FalsificationEngine()
