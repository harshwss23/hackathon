/**
 * StoryLens AI - Governed KPI Semantic Contracts
 * Problem Track 3: BusinessIntelligence.ai
 * Team Dunhill - Accenture Innovation Challenge 2026
 */

export const kpiContracts = {
  "KPI_REV": {
    id: "KPI_REV",
    name: "Quarterly Revenue",
    category: "Financial Performance",
    definition: "Total net revenue generated across all enterprise product lines after returns & discounts.",
    formula: "SUM(Gross_Sales) - SUM(Returns) - SUM(Discounts)",
    sourceSystem: "SAP ERP Financials",
    refreshCadence: "Daily (00:00 UTC)",
    granularity: "Regional / Line of Business",
    thresholds: {
      target: "> +5% QoQ",
      warning: "-2% to -5% QoQ",
      critical: "< -5% QoQ"
    },
    lineage: {
      upstream: ["SAP_BSEG", "STRIPE_PAYMENTS"],
      downstream: ["KPI_EBITDA", "KPI_SHAREHOLDER_VAL"]
    },
    entitlement: "Executive",
    dataQualityScore: 0.99
  },

  "KPI_SHIP_DELAY": {
    id: "KPI_SHIP_DELAY",
    name: "Supplier Shipment Delay Rate",
    category: "Supply Chain & Operations",
    definition: "Percentage of outbound orders delayed past promised SLA delivery date due to component availability.",
    formula: "(Delayed_Shipments / Total_Outbound_Shipments) * 100",
    sourceSystem: "Manhattan WMS / SAP Logistics",
    refreshCadence: "Real-time Streaming (Kafka)",
    granularity: "Fulfillment Center / SKU",
    thresholds: {
      target: "< 3%",
      warning: "3% - 10%",
      critical: "> 10%"
    },
    lineage: {
      upstream: ["WMS_SHIP_LOGS", "SUPPLIER_EDI_856"],
      downstream: ["KPI_COMPLAINTS", "KPI_REV"]
    },
    entitlement: "Operations",
    dataQualityScore: 0.94
  },

  "KPI_COMPLAINTS": {
    id: "KPI_COMPLAINTS",
    name: "Customer Complaint Rate",
    category: "Customer Experience",
    definition: "Ratio of support tickets tagged under 'Delivery SLA Breach' or 'Missing Item' per 1,000 orders.",
    formula: "(SLA_Breach_Tickets / Total_Orders_Delivered) * 1000",
    sourceSystem: "Zendesk Enterprise CRM",
    refreshCadence: "Hourly Batch",
    granularity: "Customer Segment / Region",
    thresholds: {
      target: "< 15 per 1k",
      warning: "15 - 30 per 1k",
      critical: "> 30 per 1k"
    },
    lineage: {
      upstream: ["ZENDESK_TICKETS", "TWITTER_SENTIMENT_API"],
      downstream: ["KPI_RETENTION", "KPI_NPS"]
    },
    entitlement: "Operations",
    dataQualityScore: 0.91
  },

  "KPI_RETENTION": {
    id: "KPI_RETENTION",
    name: "Repeat Purchase Retention Rate",
    category: "Customer Lifetime Value",
    definition: "Percentage of existing cohort customers placing a repeat purchase within a 60-day window.",
    formula: "(Repeat_Buyers_Cohort / Total_Cohort_Buyers) * 100",
    sourceSystem: "Snowflake Customer 360",
    refreshCadence: "Weekly (Mon 02:00 UTC)",
    granularity: "Cohort / Channel",
    thresholds: {
      target: "> 65%",
      warning: "50% - 65%",
      critical: "< 50%"
    },
    lineage: {
      upstream: ["SNOWFLAKE_CUSTOMER_EVENTS", "SHOPIFY_ORDERS"],
      downstream: ["KPI_LTV", "KPI_REV"]
    },
    entitlement: "Executive",
    dataQualityScore: 0.96
  },

  "KPI_CAC": {
    id: "KPI_CAC",
    name: "Customer Acquisition Cost",
    category: "Marketing Efficiency",
    definition: "Total marketing & sales expenditure divided by new user acquisitions in given period.",
    formula: "(Total_Marketing_Spend + Sales_Costs) / New_Acquired_Customers",
    sourceSystem: "HubSpot & Google Ads Analytics",
    refreshCadence: "Daily (04:00 UTC)",
    granularity: "Campaign / Channel",
    thresholds: {
      target: "< $45",
      warning: "$45 - $65",
      critical: "> $65"
    },
    lineage: {
      upstream: ["META_ADS_API", "GOOGLE_ADS_API", "STRIPE_CUSTOMERS"],
      downstream: ["KPI_ROAS", "KPI_PAYBACK_MONTHS"]
    },
    entitlement: "Executive",
    dataQualityScore: 0.88
  }
};
