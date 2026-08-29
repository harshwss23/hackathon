class EvidenceLedger:
    def get_evidence_package(self):
        """
        Generates structured Evidence Package with unique Evidence IDs and SQL citations.
        """
        return {
            "evidence_items": [
                {
                    "evidence_id": "EV-3941",
                    "claim": "Net Revenue declined 8.1% QoQ ($8.1M INR revenue gap)",
                    "source_table": "sales_orders",
                    "sql_query": "SELECT SUM(net_revenue) FROM sales_orders WHERE order_date >= '2026-08-01'",
                    "time_window": "2026-08-01 -> 2026-08-28",
                    "row_count": 12570,
                    "freshness_minutes": 7,
                    "quality_score": 0.99
                },
                {
                    "evidence_id": "EV-3942",
                    "claim": "Supplier A fill rate fell 21.4% and outbound delivery delays increased 18.2%",
                    "source_table": "shipments",
                    "sql_query": "SELECT supplier_id, AVG(fill_rate), AVG(delay_days) FROM shipments GROUP BY supplier_id",
                    "time_window": "2026-08-01 -> 2026-08-28",
                    "row_count": 12570,
                    "freshness_minutes": 53,
                    "quality_score": 0.94
                },
                {
                    "evidence_id": "EV-3943",
                    "claim": "Customer complaint tickets for SLA breach increased 24.0%",
                    "source_table": "support_tickets",
                    "sql_query": "SELECT COUNT(*) FROM support_tickets WHERE issue_type = 'Delivery SLA Breach'",
                    "time_window": "2026-08-01 -> 2026-08-28",
                    "row_count": 542,
                    "freshness_minutes": 2,
                    "quality_score": 0.91
                }
            ]
        }

evidence_ledger = EvidenceLedger()
