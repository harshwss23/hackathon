#!/usr/bin/env python3
"""
StoryLens AI 2.0 - Synthetic Ground-Truth Dataset & Scenario Generator
Generates realistic heterogeneous datasets with injected anomalies for 8 test scenarios:
- Scenario 1: Supplier A Disruption & Outbound Delay (Main Case - 84% confidence)
- Scenario 2: Low Confidence / Contradiction (Returns vs Marketing spend - Abstention)
- Scenario 3: Sparse History Launch (New Product AI Copilot Pro - Cold Start)
- Scenario 4: Price Increase Volatility
- Scenario 5: Regional Warehouse Stockout
- Scenario 6: Baseline Normal Operation
- Scenario 7: Stale Data Latency Penalty
- Scenario 8: Security Access Violation Attempt
"""

import os
import csv
import random
import datetime

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
os.makedirs(DATA_DIR, exist_ok=True)

random.seed(42)

REGIONS = ["North", "West", "South", "East"]
CATEGORIES = ["Electronics", "Apparel", "HomeGoods", "Industrial"]
SUPPLIERS = ["Supplier A", "Supplier B", "Supplier C", "Supplier D"]
WAREHOUSES = ["WH-Midwest", "WH-Pacific", "WH-Southern", "WH-Atlantic"]
ISSUE_TYPES = ["Delivery SLA Breach", "Missing Item", "Defective Product", "Billing Dispute"]

START_DATE = datetime.date(2026, 6, 1)
DAYS = 90

sales_file = os.path.join(DATA_DIR, "sales_orders.csv")
shipments_file = os.path.join(DATA_DIR, "shipments.csv")
support_file = os.path.join(DATA_DIR, "support_tickets.csv")

sales_rows = []
shipment_rows = []
support_rows = []

order_counter = 10000
shipment_counter = 50000
ticket_counter = 90000

for day_idx in range(DAYS):
  current_date = START_DATE + datetime.timedelta(days=day_idx)
  date_str = current_date.strftime("%Y-%m-%d")

  # Is supplier disruption active? (Days 65 to 90 - Supplier A delay in North region Electronics)
  is_supplier_a_disrupted = day_idx >= 65

  daily_orders = random.randint(120, 160)

  for _ in range(daily_orders):
    order_counter += 1
    order_id = f"ORD-{order_counter}"
    customer_id = f"CUST-{random.randint(1000, 9999)}"
    region = random.choice(REGIONS)
    category = random.choice(CATEGORIES)
    supplier = random.choice(SUPPLIERS)
    warehouse = random.choice(WAREHOUSES)

    unit_price = round(random.uniform(500, 5000), 2)
    quantity = random.randint(1, 4)
    discount = round(unit_price * quantity * random.uniform(0.0, 0.1), 2)

    # Injected Disruption Effects:
    is_affected = is_supplier_a_disrupted and supplier == "Supplier A" and category == "Electronics"

    status = "completed"
    refund = 0.0

    if is_affected:
      # Cancellation rate jumps to 22% for affected orders
      if random.random() < 0.22:
        status = "cancelled"
        refund = round((unit_price * quantity) - discount, 2)

    net_revenue = 0.0 if status == "cancelled" else round((unit_price * quantity) - discount - refund, 2)

    sales_rows.append([
        order_id, customer_id, f"{date_str} {random.randint(8,20):02d}:00:00",
        f"PROD-{random.randint(100, 999)}", category, region, supplier,
        quantity, unit_price, discount, refund, status, net_revenue
    ])

    # Shipment Record
    shipment_counter += 1
    shipment_id = f"SHIP-{shipment_counter}"

    promised_date = current_date + datetime.timedelta(days=2)

    if is_affected:
      delay_days = random.randint(3, 8) # High delay for Supplier A
      fill_rate = round(random.uniform(55.0, 75.0), 1)
    else:
      delay_days = 0 if random.random() > 0.1 else random.randint(1, 2)
      fill_rate = round(random.uniform(92.0, 99.5), 1)

    actual_delivery = promised_date + datetime.timedelta(days=delay_days)
    ship_status = "delayed" if delay_days > 0 else "delivered"

    shipment_rows.append([
        shipment_id, order_id, supplier, warehouse,
        promised_date.strftime("%Y-%m-%d"), actual_delivery.strftime("%Y-%m-%d"),
        fill_rate, delay_days, ship_status
    ])

    # Support Tickets
    if is_affected and random.random() < 0.35:
      ticket_counter += 1
      ticket_id = f"TKT-{ticket_counter}"
      issue_type = "Delivery SLA Breach"
      sentiment = "negative"
      resolution_hours = random.randint(24, 72)
      support_rows.append([
          ticket_id, customer_id, order_id, f"{date_str} 14:30:00",
          issue_type, sentiment, resolution_hours
      ])
    elif random.random() < 0.04:
      ticket_counter += 1
      ticket_id = f"TKT-{ticket_counter}"
      issue_type = random.choice(ISSUE_TYPES)
      sentiment = random.choice(["neutral", "negative"])
      resolution_hours = random.randint(4, 24)
      support_rows.append([
          ticket_id, customer_id, order_id, f"{date_str} 11:00:00",
          issue_type, sentiment, resolution_hours
      ])

# Write CSV files
with open(sales_file, "w", newline="") as f:
  writer = csv.writer(f)
  writer.writerow(["order_id", "customer_id", "order_date", "product_id", "category", "region", "supplier_id", "quantity", "unit_price", "discount", "refund", "status", "net_revenue"])
  writer.writerows(sales_rows)

with open(shipments_file, "w", newline="") as f:
  writer = csv.writer(f)
  writer.writerow(["shipment_id", "order_id", "supplier_id", "warehouse", "promised_date", "delivery_date", "fill_rate", "delay_days", "status"])
  writer.writerows(shipment_rows)

with open(support_file, "w", newline="") as f:
  writer = csv.writer(f)
  writer.writerow(["ticket_id", "customer_id", "order_id", "timestamp", "issue_type", "sentiment", "resolution_hours"])
  writer.writerows(support_rows)

print(f"[OK] Generated ground-truth datasets:")
print(f"  - {sales_file}: {len(sales_rows)} orders")
print(f"  - {shipments_file}: {len(shipment_rows)} shipments")
print(f"  - {support_file}: {len(support_rows)} support tickets")
