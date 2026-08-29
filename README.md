# StoryLens AI 2.0 — Governed Decision Intelligence Platform
> **Accenture Innovation Challenge 2026 — Problem Track 3: BusinessIntelligence.ai**  
> **Team:** Dunhill (IIT Kanpur — Rahul Kumar Meena, Pranay Saini, Harshvardhan Singh Shekhawat)

---

## 💡 Executive Summary & Product Positioning

**StoryLens AI 2.0** is an **evidence-first, governed decision-intelligence engine** designed for enterprise executive decision-making. 

Unlike traditional LLM dashboards that generate quantitative estimates directly from prompts, StoryLens operates under a strict architectural principle:

> **"The LLM explains the investigation. It does not perform the investigation."**

StoryLens establishes an auditable enterprise loop:
$$\boxed{\text{Detect} \rightarrow \text{Investigate} \rightarrow \text{Challenge} \rightarrow \text{Decide} \rightarrow \text{Act} \rightarrow \text{Measure Outcome} \rightarrow \text{Learn}}$$

---

## 🌟 Key Features & Enterprise Differentiators

```
                          STORYLENS AI 2.0 ARCHITECTURE

Enterprise Data (SAP / WMS / CRM)
            │
            ▼
┌───────────────────────┐
│ Data Trust Layer      │  (Data Anomaly vs Business Incident Discriminator)
└───────────┬───────────┘
            ▼
┌───────────────────────┐
│ Governed Semantics    │  (Trusted Analytics Registry v3.2 & Semantic Drift)
└───────────┬───────────┘
            ▼
┌───────────────────────┐
│ Analytics Engine      │  (Price-Volume-Mix Waterfall & Difference-in-Differences)
└───────────┬───────────┘
            ▼
┌───────────────────────┐
│ Evidence Engine       │  (Falsification Engine & Evidence Confidence C-Score)
└───────────┬───────────┘
            ▼
┌───────────────────────┐
│ Decision Engine       │  (Monte-Carlo 500 Sampler & Constrained What-If Simulator)
└───────────┬───────────┘
            ▼
┌───────────────────────┐
│ C-Suite Action Brief  │  (Executive Brief, Autonomy Levels 0-4 & Approval SLA)
└───────────┬───────────┘
            ▼
┌───────────────────────┐
│ Closed-Loop Outcome   │  (+28 Day Observed Recovery & Prediction Error Tracking)
└───────────┬───────────┘
            ▼
┌───────────────────────┐
│ Decision Memory RAG   │  (Organizational Learning over Historical Decisions)
└───────────────────────┘
```

1. **Hypothesis Falsification Engine ("What would change my mind?")**:
   Explicitly details 3 conditions that would overturn the conclusion (e.g. *Competitor price drop > 12% = -18pp confidence impact*) and highlights **Next-Best-Evidence**.
2. **Monte-Carlo Decision Robustness (500 Trial Sampler)**:
   Runs 500 sampled scenarios across Demand ($\pm10\%$), Capacity, and Transport costs. Returns **87% Robustness Score**, P10 (`₹1.8M`), and P90 (`₹3.6M`).
3. **Closed-Loop Outcome Tracker (+28 Days)**:
   Compares predicted recovery (`₹3.03M`) vs actual observed recovery (`₹2.72M`, `-10.2%` error) to calibrate future simulation weights.
4. **Decision Lineage Log**:
   Full provenance audit ledger: `Signal -> Evidence Snapshot -> Driver -> Action -> Approval -> Execution -> Observed Outcome`.
5. **Data Pipeline Anomaly Discriminator**:
   Prevents false alarms by checking whether KPI drops are data ingestion failures (e.g. 19% drop in SAP records) vs true business incidents.
6. **Trusted Analytics Registry & Semantic Drift**:
   Signed, CFO-approved SQL queries (Finance v3.2) + alerts when contract definitions change.
7. **Decision Memory RAG**:
   Matches current incident against historical decision database (`INV-2026-0312-004`, 91% similarity) returning past resolution time & ROI.
8. **Executive C-Suite Decision Brief**:
   Downloadable brief summarizing Situation, Evidence, Decision Range (`₹2.6M–₹3.4M`), Decision Robustness (87%), Risk, SLA, and `[Approve] [Modify] [Reject]` controls.

---

## ⚡ Ground-Truth Evaluation Benchmark Results

Tested against a synthetic ground-truth benchmark suite of **42 seeded enterprise test incidents**:

```json
{
  "total_seeded_incidents": 42,
  "top1_driver_accuracy_pct": 85.7,
  "top3_driver_recall_pct": 95.2,
  "abstention_precision_pct": 88.9,
  "numeric_claim_fidelity_pct": 100.0,
  "unsupported_numeric_claims": 0,
  "data_anomaly_detection_accuracy_pct": 100.0,
  "monte_carlo_scenarios_tested": 500,
  "decision_robustness_score_pct": 87.0,
  "closed_loop_recovery_accuracy_pct": 89.8,
  "median_investigation_latency_ms": 153,
  "estimated_cost_per_insight_usd": 0.0021
}
```

---

## 🚀 Quickstart & Execution Instructions

### Prerequisites
- Python 3.9+
- Standard Library (`sqlite3`, `json`, `http.server`)

### One-Click Launch
```bash
python3 start.py
```
Open **`http://localhost:8080`** in your browser.

### Run Evaluation Suite
```bash
python3 storylens/evaluation/evaluate.py
```
