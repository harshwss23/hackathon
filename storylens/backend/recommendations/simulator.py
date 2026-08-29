class ActionSimulator:
    def simulate_supplier_reallocation(self, reallocate_pct: float):
        """
        Simulates reallocating Supplier A volume (0% to 50%) to Supplier B & C.
        Capacity constraint: Supplier B max spare capacity = 32%.
        """
        reallocate_pct = max(0.0, min(50.0, float(reallocate_pct)))

        # Baseline metrics
        baseline_delay_rate = 18.2
        baseline_cancellation_rate = 14.1
        baseline_4week_revenue_loss_inr = 8100000.0

        # Constraint check: Supplier B max capacity = 32%
        is_constrained = reallocate_pct > 32.0
        warning_msg = None
        if is_constrained:
            warning_msg = "⚠️ Action Constraint Warning: Supplier B spare capacity limit (32.0%) exceeded! Additional volume requires secondary procurement authorization."

        effective_alloc = min(32.0, reallocate_pct) if is_constrained else reallocate_pct

        # Impact calculations
        projected_delay_rate = max(3.0, round(baseline_delay_rate - (effective_alloc * 0.45), 1))
        projected_cancellation_rate = max(2.5, round(baseline_cancellation_rate - (effective_alloc * 0.32), 1))
        projected_revenue_recovery_inr = round(baseline_4week_revenue_loss_inr * (effective_alloc / 50.0) * 0.85, 2)

        return {
            "reallocation_pct_requested": reallocate_pct,
            "reallocation_pct_effective": effective_alloc,
            "is_constrained": is_constrained,
            "constraint_warning": warning_msg,
            "baseline_delay_rate_pct": baseline_delay_rate,
            "projected_delay_rate_pct": projected_delay_rate,
            "baseline_cancellation_rate_pct": baseline_cancellation_rate,
            "projected_cancellation_rate_pct": projected_cancellation_rate,
            "projected_4week_revenue_recovery_inr": projected_revenue_recovery_inr,
            "confidence_level": "Medium-High"
        }

action_simulator = ActionSimulator()
