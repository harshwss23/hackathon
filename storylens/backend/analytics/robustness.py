import random

class MonteCarloRobustnessEngine:
    def run_robustness_simulation(self, reallocate_pct: float = 22.0, num_trials: int = 500):
        """
        Runs 500 sampled scenarios across:
        - Demand (-10% to +10%)
        - Supplier B SLA (88% to 96%)
        - Supplier B capacity (20% to 35%)
        - Transport cost (Base to +15%)
        """
        random.seed(42)
        beneficial_count = 0
        recoveries = []

        for _ in range(num_trials):
            demand_var = random.uniform(-0.10, 0.10)
            supplier_b_sla = random.uniform(0.88, 0.96)
            supplier_b_cap = random.uniform(20.0, 35.0)
            transport_cost_var = random.uniform(0.0, 0.15)

            # Calculate trial recovery
            effective_vol = min(reallocate_pct, supplier_b_cap)
            recovery_inr = (8100000.0 * (effective_vol / 50.0) * supplier_b_sla) * (1.0 + demand_var) - (transport_cost_var * 200000.0)

            if recovery_inr > 500000.0:
                beneficial_count += 1
            
            recoveries.append(recovery_inr)

        recoveries.sort()

        robustness_pct = round((beneficial_count / num_trials) * 100.0, 1)
        p10 = round(recoveries[int(num_trials * 0.10)], 2)
        p50 = round(recoveries[int(num_trials * 0.50)], 2)
        p90 = round(recoveries[int(num_trials * 0.90)], 2)
        downside_risk = round(max(0, 1000000.0 - p10), 2)

        return {
            "num_scenarios_simulated": num_trials,
            "robustness_score_pct": robustness_pct,
            "recommendation_beneficial_pct": robustness_pct,
            "p10_recovery_inr": p10,
            "p50_median_recovery_inr": p50,
            "p90_recovery_inr": p90,
            "downside_risk_inr": downside_risk,
            "interpretation": f"Recommendation remains beneficial in {robustness_pct}% of 500 sampled scenarios (P50 Median Recovery: ₹{p50/1e6:.2f}M, P10: ₹{p10/1e6:.2f}M, P90: ₹{p90/1e6:.2f}M)."
        }

robustness_engine = MonteCarloRobustnessEngine()
