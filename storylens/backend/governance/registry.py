class AnalyticsRegistry:
    def get_verified_registry(self):
        """
        Trusted Analytics Registry containing CFO/Finance approved signed SQL queries.
        """
        return {
            "verified_analytics": [
                {
                    "metric_id": "net_revenue",
                    "name": "Net Revenue",
                    "approved_sql": "SELECT SUM(price * quantity - discount - refund) FROM sales_orders WHERE status != 'cancelled'",
                    "owner": "Finance Analytics",
                    "verified_by": "CFO Data Office",
                    "version": "v3.2",
                    "last_validated": "2026-08-27",
                    "status": "TRUSTED"
                },
                {
                    "metric_id": "on_time_delivery",
                    "name": "On-Time Delivery Rate",
                    "approved_sql": "SELECT (COUNT(CASE WHEN delay_days <= 0 THEN 1 END) / COUNT(*)) * 100 FROM shipments",
                    "owner": "Logistics Operations",
                    "verified_by": "VP Supply Chain",
                    "version": "v2.1",
                    "last_validated": "2026-08-20",
                    "status": "TRUSTED"
                }
            ]
        }

    def check_semantic_drift(self):
        """
        Detects if KPI definitions changed (e.g. Net Revenue v3.1 to v3.2).
        """
        return {
            "drift_detected": True,
            "metric_id": "net_revenue",
            "previous_version": "v3.1 (Revenue = sales - refunds)",
            "current_version": "v3.2 (Revenue = sales - refunds - promotional_credits)",
            "historical_comparability_impact": "-1.7% variance on Apr-Aug 2026 historical baseline",
            "recommended_action": "Recompute 90-day seasonal baseline under v3.2 semantic contract."
        }

analytics_registry = AnalyticsRegistry()
