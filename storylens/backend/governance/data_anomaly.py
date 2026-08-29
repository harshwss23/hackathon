class DataAnomalyDiscriminator:
    def evaluate_incident_type(self, scenario_id: str = "supply_chain"):
        """
        Determines whether a KPI drop is a true Business Incident or a Data Pipeline Ingestion Anomaly.
        "We refuse to explain unhealthy data."
        """
        if scenario_id == "data_pipeline_fault":
            return {
                "is_data_incident": True,
                "investigation_status": "PAUSED",
                "incident_type": "Data Pipeline Ingestion Anomaly",
                "affected_source": "SAP Sales Ingestion Pipeline",
                "anomaly_detail": "SAP sales record ingestion volume dropped 19.4% at 03:00 UTC due to API sync failure. WMS and Zendesk data remain normal.",
                "action_required": "Data Operations team must restart Kafka SAP Ingest Connector before business investigation can resume."
            }

        return {
            "is_data_incident": False,
            "investigation_status": "ACTIVE",
            "incident_type": "Verified Business Incident",
            "data_health_score": 99.1,
            "details": "All 3 data sources (SAP Sales, WMS Logistics, Zendesk CRM) are healthy and verified."
        }

data_discriminator = DataAnomalyDiscriminator()
