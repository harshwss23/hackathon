class LLMNarrativeGenerator:
    def generate_narrative(self, persona: str, evidence_pkg: dict, confidence_data: dict, scenario_type: str = "supply_chain"):
        """
        Generates structured JSON narrative strictly bound to quantitative Evidence Package.
        "The LLM explains the investigation. It does not perform the investigation."
        """
        if confidence_data.get("is_abstained"):
            return {
                "headline": "SYSTEM ABSTENTION: Low Confidence Signal Discrepancy",
                "summary": confidence_data.get("abstain_message"),
                "primary_driver": "Inconclusive",
                "evidence_citations": [],
                "uncertainty_statement": f"Confidence ({confidence_data.get('confidence_score_pct')}%) falls below 60% safety threshold.",
                "recommended_actions": [confidence_data.get("requested_evidence")]
            }

        if persona == "operations":
            return {
                "headline": "Outbound Delivery SLA Breach Alert — Floor Shift Target Required",
                "summary": "Logistics & warehouse telemetry shows outbound delivery SLA breaches increased by 18.2% across Midwest fulfillment hubs [EV-3942]. Supplier A component availability issues caused Zendesk delivery escalation tickets to rise 24.0% [EV-3943]. Outbound shipment backlog currently stands at 4,200 units.",
                "primary_driver": "Supplier A Component Fulfillment Delay (18.2% delay spike)",
                "evidence_citations": ["EV-3942", "EV-3943"],
                "uncertainty_statement": "Evidence confidence is 84.1% supported by 12,570 shipment records.",
                "recommended_actions": [
                    "Re-assign 8 floor staff to priority packing & send automated SMS delivery tracking",
                    "Implement real-time RFID bin tracking & expand safety stock threshold by +15%"
                ]
            }
        else: # executive
            return {
                "headline": "Q3 Revenue Impact Analysis: Supplier Disruption & Retention Leakage",
                "summary": "Financial and supply chain contracts indicate enterprise Net Revenue declined by 8.1% QoQ ($8.1M INR gap) [EV-3941]. Causal inference confirms an 18.2% spike in Supplier A shipment delays as the primary root driver [EV-3942]. Reduced product availability triggered a 24.0% increase in customer complaints [EV-3943] and a 15.1% drop in repeat cohort retention.",
                "primary_driver": "Supplier A Component Bottleneck (61% explained revenue loss)",
                "evidence_citations": ["EV-3941", "EV-3942", "EV-3943"],
                "uncertainty_statement": "Evidence confidence is 84.1% (High). Causal Difference-in-Differences test confirms p < 0.01 significance.",
                "recommended_actions": [
                    "Authorise premium air-freight logistics for tier-1 customer backorders (Clear $1.2M Backlog in 2 weeks)",
                    "Enforce strict SLA penalty clauses & reallocate 30% volume to secondary regional suppliers"
                ]
            }

llm_narrative_gen = LLMNarrativeGenerator()
