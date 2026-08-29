class MaterialityEngine:
    def calculate_materiality(self, statistical_surprise: float, business_impact_usd: float, persistence_ratio: float):
        """
        Calculates Materiality Score M = 0.4 * StatisticalSurprise + 0.4 * BusinessImpact + 0.2 * Persistence
        Normalized to 0.0 - 1.0 range.
        """
        norm_surprise = min(1.0, max(0.0, abs(statistical_surprise) / 4.0))
        norm_impact = min(1.0, max(0.0, abs(business_impact_usd) / 10000000.0))
        norm_persistence = min(1.0, max(0.0, persistence_ratio))

        materiality_score = (0.4 * norm_surprise) + (0.4 * norm_impact) + (0.2 * norm_persistence)
        
        priority = "Low"
        if materiality_score >= 0.75:
            priority = "Critical"
        elif materiality_score >= 0.50:
            priority = "High"
        elif materiality_score >= 0.30:
            priority = "Medium"

        return {
            "materiality_score": round(materiality_score, 2),
            "priority": priority,
            "components": {
                "statistical_surprise_score": round(norm_surprise, 2),
                "business_impact_score": round(norm_impact, 2),
                "persistence_score": round(norm_persistence, 2)
            }
        }

materiality_engine = MaterialityEngine()
