#!/usr/bin/env python3
"""
Simple script to populate Snowflake Ontology database with sample data
"""

import snowflake.connector
import os
import json
from datetime import datetime

# Get Snowflake connection parameters from environment
conn = snowflake.connector.connect(
    account=os.getenv('SNOWFLAKE_ACCOUNT'),
    user=os.getenv('SNOWFLAKE_USER'),
    password=os.getenv('SNOWFLAKE_PASSWORD'),
    warehouse=os.getenv('SNOWFLAKE_WAREHOUSE', 'COMPUTE_WH'),
    database='ONTOLOGY_DB',
    schema='PUBLIC'
)

cursor = conn.cursor()

print("🗑️  Clearing existing data...")
cursor.execute("DELETE FROM WORKFLOW_EXECUTIONS")
cursor.execute("DELETE FROM WORKFLOW_DEFINITIONS")
cursor.execute("DELETE FROM ENTITY_STATES")
cursor.execute("DELETE FROM RELATIONSHIPS")
cursor.execute("DELETE FROM ENTITIES")

print("👥 Inserting customers...")
customers = [
    ('cust-001', 'Acme Corporation', {"industry": "Technology", "size": "Enterprise", "annual_revenue": 50000000, "employees": 5000, "country": "US", "email": "contact@acme.com", "health_score": 85, "tier": "Platinum"}, ["enterprise", "technology", "active", "high_value", "platinum"]),
    ('cust-002', 'Global Industries Inc', {"industry": "Manufacturing", "size": "Enterprise", "annual_revenue": 75000000, "employees": 8000, "country": "US", "health_score": 92, "tier": "Platinum"}, ["enterprise", "manufacturing", "active", "high_value", "platinum"]),
    ('cust-003', 'TechStart Solutions', {"industry": "Technology", "size": "Mid-Market", "annual_revenue": 15000000, "employees": 500, "country": "US", "health_score": 78, "tier": "Gold"}, ["mid_market", "technology", "active", "gold"]),
    ('cust-004', 'Retail Masters LLC', {"industry": "Retail", "size": "Mid-Market", "annual_revenue": 20000000, "employees": 1200, "country": "US", "health_score": 65, "tier": "Silver"}, ["mid_market", "retail", "active", "silver", "at_risk"]),
    ('cust-005', 'FinServe Partners', {"industry": "Financial Services", "size": "Enterprise", "annual_revenue": 100000000, "employees": 3000, "country": "UK", "health_score": 88, "tier": "Platinum"}, ["enterprise", "financial_services", "active", "high_value", "platinum", "international"]),
]

for entity_id, label, properties, tags in customers:
    cursor.execute(
        "INSERT INTO ENTITIES (ENTITY_ID, ENTITY_TYPE, LABEL, PROPERTIES, TAGS, CREATED_AT, UPDATED_AT) SELECT %s, %s, %s, PARSE_JSON(%s), PARSE_JSON(%s), CURRENT_TIMESTAMP(), CURRENT_TIMESTAMP()",
        (entity_id, 'CUSTOMER', label, json.dumps(properties), json.dumps(tags))
    )

print("🏦 Inserting accounts...")
accounts = [
    ('acct-001', 'Acme Main Account', {"account_number": "ACC-10001", "balance": 250000, "credit_limit": 500000, "status": "active", "payment_terms": "Net 30"}, ["main_account", "active", "high_balance"]),
    ('acct-002', 'Acme Dev Account', {"account_number": "ACC-10002", "balance": 75000, "credit_limit": 100000, "status": "active", "payment_terms": "Net 15"}, ["dev_account", "active"]),
    ('acct-003', 'Global Industries Account', {"account_number": "ACC-10003", "balance": 450000, "credit_limit": 1000000, "status": "active", "payment_terms": "Net 45"}, ["main_account", "active", "high_balance", "vip"]),
    ('acct-004', 'TechStart Account', {"account_number": "ACC-10004", "balance": 35000, "credit_limit": 50000, "status": "active", "payment_terms": "Net 30"}, ["main_account", "active"]),
]

for entity_id, label, properties, tags in accounts:
    cursor.execute(
        "INSERT INTO ENTITIES (ENTITY_ID, ENTITY_TYPE, LABEL, PROPERTIES, TAGS, CREATED_AT, UPDATED_AT) SELECT %s, %s, %s, PARSE_JSON(%s), PARSE_JSON(%s), CURRENT_TIMESTAMP(), CURRENT_TIMESTAMP()",
        (entity_id, 'ACCOUNT', label, json.dumps(properties), json.dumps(tags))
    )

print("📦 Inserting products...")
products = [
    ('prod-001', 'Enterprise Platform License', {"sku": "EPL-1000", "price": 50000, "category": "Software", "license_type": "Annual", "max_users": 1000}, ["software", "enterprise", "subscription", "flagship"]),
    ('prod-002', 'Analytics Module', {"sku": "AM-500", "price": 15000, "category": "Software", "license_type": "Annual", "max_users": 500}, ["software", "analytics", "addon", "popular"]),
    ('prod-003', 'API Integration Pack', {"sku": "API-100", "price": 10000, "category": "Software", "license_type": "Annual", "api_calls": 1000000}, ["software", "integration", "addon"]),
    ('prod-004', 'Professional Services - Implementation', {"sku": "PS-IMPL", "price": 25000, "category": "Services", "duration_weeks": 8, "team_size": 3}, ["services", "implementation", "consulting"]),
    ('prod-005', 'Premium Support', {"sku": "SUP-PREM", "price": 12000, "category": "Support", "sla": "4 hours", "availability": "24/7"}, ["support", "premium", "subscription"]),
]

for entity_id, label, properties, tags in products:
    cursor.execute(
        "INSERT INTO ENTITIES (ENTITY_ID, ENTITY_TYPE, LABEL, PROPERTIES, TAGS, CREATED_AT, UPDATED_AT) SELECT %s, %s, %s, PARSE_JSON(%s), PARSE_JSON(%s), CURRENT_TIMESTAMP(), CURRENT_TIMESTAMP()",
        (entity_id, 'PRODUCT', label, json.dumps(properties), json.dumps(tags))
    )

print("📋 Inserting orders...")
orders = [
    ('order-001', 'Order #1001', {"order_number": "ORD-1001", "order_date": "2024-01-15", "total_amount": 100000, "status": "completed", "payment_status": "paid"}, ["completed", "paid", "large_order"]),
    ('order-002', 'Order #1002', {"order_number": "ORD-1002", "order_date": "2024-02-20", "total_amount": 25000, "status": "completed", "payment_status": "paid"}, ["completed", "paid"]),
    ('order-003', 'Order #1003', {"order_number": "ORD-1003", "order_date": "2024-03-10", "total_amount": 150000, "status": "processing", "payment_status": "pending"}, ["processing", "pending", "large_order"]),
]

for entity_id, label, properties, tags in orders:
    cursor.execute(
        "INSERT INTO ENTITIES (ENTITY_ID, ENTITY_TYPE, LABEL, PROPERTIES, TAGS, CREATED_AT, UPDATED_AT) SELECT %s, %s, %s, PARSE_JSON(%s), PARSE_JSON(%s), CURRENT_TIMESTAMP(), CURRENT_TIMESTAMP()",
        (entity_id, 'ORDER', label, json.dumps(properties), json.dumps(tags))
    )

print("👨‍💼 Inserting employees...")
employees = [
    ('emp-001', 'John Smith', {"employee_id": "EMP-001", "title": "Account Executive", "department": "Sales", "email": "john.smith@company.com", "hire_date": "2020-01-15"}, ["sales", "account_executive", "senior"]),
    ('emp-002', 'Sarah Johnson', {"employee_id": "EMP-002", "title": "Customer Success Manager", "department": "Customer Success", "email": "sarah.johnson@company.com", "hire_date": "2019-06-01"}, ["customer_success", "manager"]),
    ('emp-003', 'Mike Chen', {"employee_id": "EMP-003", "title": "Solutions Architect", "department": "Engineering", "email": "mike.chen@company.com", "hire_date": "2021-03-15"}, ["engineering", "architect", "technical"]),
]

for entity_id, label, properties, tags in employees:
    cursor.execute(
        "INSERT INTO ENTITIES (ENTITY_ID, ENTITY_TYPE, LABEL, PROPERTIES, TAGS, CREATED_AT, UPDATED_AT) SELECT %s, %s, %s, PARSE_JSON(%s), PARSE_JSON(%s), CURRENT_TIMESTAMP(), CURRENT_TIMESTAMP()",
        (entity_id, 'EMPLOYEE', label, json.dumps(properties), json.dumps(tags))
    )

print("🔗 Inserting relationships...")
relationships = [
    ('rel-001', 'cust-001', 'OWNS', 'acct-001', {"relationship_type": "primary", "since": "2020-01-15"}),
    ('rel-002', 'cust-001', 'OWNS', 'acct-002', {"relationship_type": "secondary", "since": "2021-06-01"}),
    ('rel-003', 'cust-002', 'OWNS', 'acct-003', {"relationship_type": "primary", "since": "2019-03-20"}),
    ('rel-004', 'cust-003', 'OWNS', 'acct-004', {"relationship_type": "primary", "since": "2021-06-10"}),
    ('rel-005', 'acct-001', 'PLACED', 'order-001', {"order_date": "2024-01-15"}),
    ('rel-006', 'acct-002', 'PLACED', 'order-002', {"order_date": "2024-02-20"}),
    ('rel-007', 'acct-003', 'PLACED', 'order-003', {"order_date": "2024-03-10"}),
    ('rel-008', 'order-001', 'INCLUDES', 'prod-001', {"quantity": 1, "unit_price": 50000, "line_total": 50000}),
    ('rel-009', 'order-001', 'INCLUDES', 'prod-002', {"quantity": 1, "unit_price": 15000, "line_total": 15000}),
    ('rel-010', 'order-001', 'INCLUDES', 'prod-004', {"quantity": 1, "unit_price": 25000, "line_total": 25000}),
    ('rel-011', 'order-002', 'INCLUDES', 'prod-005', {"quantity": 1, "unit_price": 12000, "line_total": 12000}),
    ('rel-012', 'order-003', 'INCLUDES', 'prod-001', {"quantity": 2, "unit_price": 50000, "line_total": 100000}),
    ('rel-013', 'order-003', 'INCLUDES', 'prod-003', {"quantity": 1, "unit_price": 10000, "line_total": 10000}),
    ('rel-014', 'emp-001', 'MANAGES', 'cust-001', {"role": "Account Executive", "since": "2020-01-15"}),
    ('rel-015', 'emp-001', 'MANAGES', 'cust-003', {"role": "Account Executive", "since": "2021-06-10"}),
    ('rel-016', 'emp-002', 'MANAGES', 'cust-002', {"role": "Customer Success Manager", "since": "2019-03-20"}),
]

for rel_id, subject_id, predicate, object_id, properties in relationships:
    cursor.execute(
        "INSERT INTO RELATIONSHIPS (RELATIONSHIP_ID, SUBJECT_ID, PREDICATE, OBJECT_ID, PROPERTIES, CREATED_AT) SELECT %s, %s, %s, %s, PARSE_JSON(%s), CURRENT_TIMESTAMP()",
        (rel_id, subject_id, predicate, object_id, json.dumps(properties))
    )

print("📊 Inserting entity states...")
states = [
    ('state-001', 'cust-001', 'ACTIVE', {"health_score": 85, "last_contact": "2024-03-15"}),
    ('state-002', 'cust-002', 'ACTIVE', {"health_score": 92, "last_contact": "2024-03-10"}),
    ('state-003', 'cust-003', 'ACTIVE', {"health_score": 78, "last_contact": "2024-02-28"}),
    ('state-004', 'cust-004', 'AT_RISK', {"health_score": 65, "last_contact": "2024-01-15", "reason": "Low engagement"}),
]

for state_id, entity_id, state, properties in states:
    cursor.execute(
        "INSERT INTO ENTITY_STATES (STATE_ID, ENTITY_ID, STATE, PROPERTIES, CREATED_AT) SELECT %s, %s, %s, PARSE_JSON(%s), CURRENT_TIMESTAMP()",
        (state_id, entity_id, state, json.dumps(properties))
    )

print("⚙️  Inserting workflow definitions...")
workflows = [
    ('wf-001', 'Customer At-Risk Alert', 'Notify account managers when customer state changes to AT_RISK', 'entity_type=CUSTOMER AND current_state=AT_RISK', 'NOTIFICATION', {"message": "Customer {{entity_label}} is now at risk", "severity": "HIGH", "recipients": ["account_managers"], "channels": ["email", "slack"]}),
    ('wf-002', 'New Order Processing', 'Process new orders automatically', 'entity_type=ORDER AND action=CREATE', 'SQL', {"query": "UPDATE ENTITIES SET PROPERTIES = OBJECT_INSERT(PROPERTIES, 'processed', TRUE) WHERE ENTITY_ID = '{{entity_id}}'", "database": "ONTOLOGY_DB", "schema": "PUBLIC"}),
    ('wf-003', 'Large Order Notification', 'Notify sales team of large orders', 'entity_type=ORDER AND properties:total_amount>100000', 'EMAIL', {"to": ["sales@company.com"], "subject": "Large Order Alert: {{entity_label}}", "body": "A large order has been placed. Total: ${{properties:total_amount}}", "from": "notifications@company.com"}),
    ('wf-004', 'Customer Onboarding', 'Trigger onboarding workflow for new customers', 'entity_type=CUSTOMER AND action=CREATE', 'STATE_TRANSITION', {"from_state": None, "to_state": "ONBOARDING", "reason": "New customer created"}),
    ('wf-005', 'Tag High Value Customers', 'Automatically tag high-value customers', 'entity_type=CUSTOMER AND properties:annual_revenue>50000000', 'TAG_MANAGEMENT', {"action": "ADD", "tags": ["high_value", "vip"]}),
]

for wf_id, name, description, trigger, action_type, config in workflows:
    cursor.execute(
        "INSERT INTO WORKFLOW_DEFINITIONS (WORKFLOW_ID, NAME, DESCRIPTION, TRIGGER_CONDITION, ACTION_TYPE, ACTION_CONFIG, ENABLED, CREATED_AT) SELECT %s, %s, %s, %s, %s, PARSE_JSON(%s), TRUE, CURRENT_TIMESTAMP()",
        (wf_id, name, description, trigger, action_type, json.dumps(config))
    )

# Get counts
print("\n✅ Data population complete!")
print("\n📊 Summary:")
cursor.execute("SELECT COUNT(*) FROM ENTITIES WHERE ENTITY_TYPE = 'CUSTOMER'")
print(f"   Customers: {cursor.fetchone()[0]}")
cursor.execute("SELECT COUNT(*) FROM ENTITIES WHERE ENTITY_TYPE = 'ACCOUNT'")
print(f"   Accounts: {cursor.fetchone()[0]}")
cursor.execute("SELECT COUNT(*) FROM ENTITIES WHERE ENTITY_TYPE = 'PRODUCT'")
print(f"   Products: {cursor.fetchone()[0]}")
cursor.execute("SELECT COUNT(*) FROM ENTITIES WHERE ENTITY_TYPE = 'ORDER'")
print(f"   Orders: {cursor.fetchone()[0]}")
cursor.execute("SELECT COUNT(*) FROM ENTITIES WHERE ENTITY_TYPE = 'EMPLOYEE'")
print(f"   Employees: {cursor.fetchone()[0]}")
cursor.execute("SELECT COUNT(*) FROM RELATIONSHIPS")
print(f"   Relationships: {cursor.fetchone()[0]}")
cursor.execute("SELECT COUNT(*) FROM ENTITY_STATES")
print(f"   States: {cursor.fetchone()[0]}")
cursor.execute("SELECT COUNT(*) FROM WORKFLOW_DEFINITIONS")
print(f"   Workflows: {cursor.fetchone()[0]}")

conn.commit()
cursor.close()
conn.close()

print("\n🎉 All done! Your Snowflake Ontology is now populated with sample data.")
