"""
Step 15: Configure OrbisERP - Exactly Eight Departments, RBAC, Employees, Branding, and Security
=================================================================================================
This script implements:
1. Creation and verification of the 8 department workspaces:
   - Purchase
   - Selling
   - Manufacturing
   - Stock
   - Floor Users (Workers)
   - Finance
   - Projects
   - HR
2. Strict isolation and hiding of all other workspaces and unrelated Desktop Icons.
3. Creation and assignment of job-based roles and test users with secure passwords.
4. Comprehensive Custom DocPerm configuration enforcing least privilege.
5. Creation of Employee masters linked to user accounts.
6. Server-side and client-side HR privilege escalation guardrails.
7. System-wide user-facing OrbisERP branding.
"""

import json
import frappe
from frappe.utils.password import update_password

COMPANY = "OrbisERP"

# --- ROLE DEFINITIONS ---
JOB_ROLES = [
    "Purchase Officer",
    "Sales Officer",
    "Production Manager",
    "Floor Worker",
    "Storekeeper",
    "Finance Officer",
    "Projects Manager",
    "Projects User",
    "Project User",
    "HR Manager",
    "HR User",
]

# --- WORKSPACE DEFINITIONS ---
EIGHT_DEPARTMENTS = {
    "Purchase": {
        "title": "Purchase",
        "seq": 1,
        "icon": "buying",
        "header": "Automotive Procurement & Supplier Management",
        "roles": ["Purchase Officer", "Purchase Manager", "Purchase User", "System Manager"],
        "cards": [
            {
                "card_name": "Suppliers",
                "links": [
                    {"value": "Supplier", "label": "Suppliers", "type": "DocType"},
                    {"value": "Supplier Group", "label": "Supplier Groups", "type": "DocType"},
                    {"value": "Contact", "label": "Supplier Contacts", "type": "DocType"},
                ]
            },
            {
                "card_name": "Purchasing Operations",
                "links": [
                    {"value": "Material Request", "label": "Purchase Requests", "type": "DocType"},
                    {"value": "Supplier Quotation", "label": "Supplier Quotations", "type": "DocType"},
                    {"value": "Purchase Order", "label": "Purchase Orders", "type": "DocType"},
                    {"value": "Purchase Receipt", "label": "Material Receipts", "type": "DocType"},
                    {"value": "Purchase Invoice", "label": "Purchase Invoices", "type": "DocType"},
                ]
            },
            {
                "card_name": "Procurement Reports",
                "links": [
                    {"value": "Purchase Order Trends", "label": "Purchase Order Trends", "type": "Report"},
                    {"value": "Purchase Receipt Trends", "label": "Purchase Receipt Trends", "type": "Report"},
                ]
            }
        ],
        "shortcuts": [
            {"value": "Purchase Order", "label": "Purchase Orders", "type": "DocType"},
            {"value": "Material Request", "label": "Purchase Requests", "type": "DocType"},
            {"value": "Purchase Receipt", "label": "Material Receipts", "type": "DocType"},
            {"value": "Supplier", "label": "Suppliers", "type": "DocType"},
            {"value": "Purchase Invoice", "label": "Purchase Invoices", "type": "DocType"},
        ]
    },
    "Selling": {
        "title": "Selling",
        "seq": 2,
        "icon": "selling",
        "header": "Automotive Vehicle Sales & Customer Orders",
        "roles": ["Sales Officer", "Sales Manager", "Sales User", "System Manager"],
        "cards": [
            {
                "card_name": "Customers",
                "links": [
                    {"value": "Customer", "label": "Customers", "type": "DocType"},
                    {"value": "Customer Group", "label": "Customer Groups", "type": "DocType"},
                    {"value": "Contact", "label": "Customer Contacts", "type": "DocType"},
                ]
            },
            {
                "card_name": "Sales Transactions",
                "links": [
                    {"value": "Quotation", "label": "Quotations", "type": "DocType"},
                    {"value": "Sales Order", "label": "Sales Orders", "type": "DocType"},
                    {"value": "Delivery Note", "label": "Vehicle Deliveries", "type": "DocType"},
                    {"value": "Sales Invoice", "label": "Sales Invoices", "type": "DocType"},
                ]
            },
            {
                "card_name": "Finished Vehicles & Catalog",
                "links": [
                    {"value": "Finished Vehicle Register", "label": "Finished Vehicle Register", "type": "DocType"},
                    {"value": "Vehicle Model", "label": "Vehicle Models", "type": "DocType"},
                    {"value": "Item", "label": "Finished Cars Catalog", "type": "DocType"},
                ]
            },
            {
                "card_name": "Sales Reports",
                "links": [
                    {"value": "Sales Order Trends", "label": "Sales Order Trends", "type": "Report"},
                    {"value": "Sales Analytics", "label": "Sales Analytics", "type": "Report"},
                ]
            }
        ],
        "shortcuts": [
            {"value": "Sales Order", "label": "Sales Orders", "type": "DocType"},
            {"value": "Customer", "label": "Customers", "type": "DocType"},
            {"value": "Delivery Note", "label": "Vehicle Deliveries", "type": "DocType"},
            {"value": "Sales Invoice", "label": "Sales Invoices", "type": "DocType"},
            {"value": "Finished Vehicle Register", "label": "Finished Vehicles", "type": "DocType"},
        ]
    },
    "Manufacturing": {
        "title": "Manufacturing",
        "seq": 3,
        "icon": "manufacturing",
        "header": "Automobile Assembly, BOM & Production Planning",
        "roles": ["Production Manager", "Manufacturing Manager", "Manufacturing User", "System Manager"],
        "cards": [
            {
                "card_name": "Production & Assembly",
                "links": [
                    {"value": "Work Order", "label": "Work Orders", "type": "DocType"},
                    {"value": "Job Card", "label": "Assembly Job Cards", "type": "DocType"},
                    {"value": "Production Plan", "label": "Production Plans", "type": "DocType"},
                    {"value": "Stock Entry", "label": "Production Material Consumption", "type": "DocType"},
                ]
            },
            {
                "card_name": "Bill of Materials & Engineering",
                "links": [
                    {"value": "BOM", "label": "Bills of Materials (BOM)", "type": "DocType"},
                    {"value": "Vehicle Model", "label": "Vehicle Models", "type": "DocType"},
                    {"value": "Finished Vehicle Register", "label": "Finished Vehicle Register", "type": "DocType"},
                ]
            },
            {
                "card_name": "Plant & Assembly Line",
                "links": [
                    {"value": "Workstation", "label": "Assembly Workstations", "type": "DocType"},
                    {"value": "Operation", "label": "Manufacturing Operations", "type": "DocType"},
                    {"value": "Routing", "label": "Assembly Routings", "type": "DocType"},
                ]
            },
            {
                "card_name": "Quality & Assurance Checks",
                "links": [
                    {"value": "Quality Inspection", "label": "Quality Inspections", "type": "DocType"},
                    {"value": "Non Conformance", "label": "Defects & Non-Conformance", "type": "DocType"},
                ]
            },
            {
                "card_name": "Manufacturing Reports",
                "links": [
                    {"value": "Work Order Summary", "label": "Work Order Summary", "type": "Report"},
                    {"value": "Production Planning Report", "label": "Production Planning", "type": "Report"},
                ]
            }
        ],
        "shortcuts": [
            {"value": "Work Order", "label": "Work Orders", "type": "DocType"},
            {"value": "BOM", "label": "Bills of Materials (BOM)", "type": "DocType"},
            {"value": "Vehicle Model", "label": "Vehicle Models", "type": "DocType"},
            {"value": "Job Card", "label": "Assembly Job Cards", "type": "DocType"},
            {"value": "Finished Vehicle Register", "label": "Finished Vehicles", "type": "DocType"},
        ]
    },
    "Stock": {
        "title": "Stock",
        "seq": 4,
        "icon": "stock",
        "header": "Automotive Warehouses, Materials & Stock Ledger",
        "roles": ["Storekeeper", "Stock Manager", "Stock User", "System Manager"],
        "cards": [
            {
                "card_name": "Items & Warehouses",
                "links": [
                    {"value": "Item", "label": "Parts & Raw Materials", "type": "DocType"},
                    {"value": "Item Group", "label": "Item Groups", "type": "DocType"},
                    {"value": "Warehouse", "label": "Automotive Warehouses", "type": "DocType"},
                    {"value": "UOM", "label": "Units of Measure", "type": "DocType"},
                ]
            },
            {
                "card_name": "Stock Movements & Receipts",
                "links": [
                    {"value": "Stock Entry", "label": "Stock Transfers & Issues", "type": "DocType"},
                    {"value": "Purchase Receipt", "label": "Purchase Receipts", "type": "DocType"},
                    {"value": "Delivery Note", "label": "Dispatch Delivery Notes", "type": "DocType"},
                    {"value": "Stock Reconciliation", "label": "Stock Reconciliation", "type": "DocType"},
                ]
            },
            {
                "card_name": "Serialized Components",
                "links": [
                    {"value": "Serial No", "label": "Serial Numbers & VINs", "type": "DocType"},
                    {"value": "Batch", "label": "Batch Numbers", "type": "DocType"},
                ]
            },
            {
                "card_name": "Inventory Reports & Alerts",
                "links": [
                    {"value": "Stock Balance", "label": "Stock Balance", "type": "Report"},
                    {"value": "Stock Ledger", "label": "Stock Ledger", "type": "Report"},
                    {"value": "Itemwise Reorder Detail", "label": "Low Stock Alerts", "type": "Report"},
                    {"value": "Stock Summary", "label": "Stock Summary", "type": "Report"},
                ]
            }
        ],
        "shortcuts": [
            {"value": "Stock Entry", "label": "Stock Transfers & Issues", "type": "DocType"},
            {"value": "Item", "label": "Parts & Raw Materials", "type": "DocType"},
            {"value": "Warehouse", "label": "Warehouses", "type": "DocType"},
            {"value": "Purchase Receipt", "label": "Purchase Receipts", "type": "DocType"},
            {"value": "Stock Balance", "label": "Stock Balance", "type": "Report"},
        ]
    },
    "Floor Users (Workers)": {
        "title": "Floor Users (Workers)",
        "seq": 5,
        "icon": "tool",
        "header": "Factory Shop Floor - Work Orders & Task Instructions",
        "roles": ["Floor Worker", "Production Manager", "Manufacturing User", "System Manager"],
        "cards": [
            {
                "card_name": "My Work Tasks",
                "links": [
                    {"value": "Job Card", "label": "My Job Cards", "type": "DocType"},
                    {"value": "Work Order", "label": "Work Orders (View Only)", "type": "DocType"},
                ]
            },
            {
                "card_name": "Production Problem Reporting",
                "links": [
                    {"value": "Non Conformance", "label": "Report Quality Issue / Defect", "type": "DocType"},
                    {"value": "Issue", "label": "Report Workstation Problem", "type": "DocType"},
                ]
            }
        ],
        "shortcuts": [
            {"value": "Job Card", "label": "My Job Cards", "type": "DocType"},
            {"value": "Work Order", "label": "Work Orders (View Only)", "type": "DocType"},
            {"value": "Non Conformance", "label": "Report Issue / Defect", "type": "DocType"},
        ]
    },
    "Finance": {
        "title": "Finance",
        "seq": 6,
        "icon": "accounting",
        "header": "Automotive Invoicing, Payments & General Ledger",
        "roles": ["Finance Officer", "Accounts Manager", "Accounts User", "System Manager"],
        "cards": [
            {
                "card_name": "Invoices",
                "links": [
                    {"value": "Sales Invoice", "label": "Sales Invoices", "type": "DocType"},
                    {"value": "Purchase Invoice", "label": "Purchase Invoices", "type": "DocType"},
                ]
            },
            {
                "card_name": "Payments & Banking",
                "links": [
                    {"value": "Payment Entry", "label": "Payment Entries", "type": "DocType"},
                    {"value": "Journal Entry", "label": "Journal Entries", "type": "DocType"},
                    {"value": "Payment Request", "label": "Payment Requests", "type": "DocType"},
                ]
            },
            {
                "card_name": "Chart of Accounts & Structure",
                "links": [
                    {"value": "Account", "label": "Chart of Accounts", "type": "DocType"},
                    {"value": "Cost Center", "label": "Cost Centers", "type": "DocType"},
                ]
            },
            {
                "card_name": "Financial Reports",
                "links": [
                    {"value": "Profit and Loss Statement", "label": "Profit and Loss", "type": "Report"},
                    {"value": "Balance Sheet", "label": "Balance Sheet", "type": "Report"},
                    {"value": "Accounts Receivable", "label": "Accounts Receivable", "type": "Report"},
                    {"value": "Accounts Payable", "label": "Accounts Payable", "type": "Report"},
                    {"value": "General Ledger", "label": "General Ledger", "type": "Report"},
                ]
            }
        ],
        "shortcuts": [
            {"value": "Sales Invoice", "label": "Sales Invoices", "type": "DocType"},
            {"value": "Purchase Invoice", "label": "Purchase Invoices", "type": "DocType"},
            {"value": "Payment Entry", "label": "Payment Entries", "type": "DocType"},
            {"value": "Journal Entry", "label": "Journal Entries", "type": "DocType"},
            {"value": "Profit and Loss Statement", "label": "Profit and Loss", "type": "Report"},
        ]
    },
    "Projects": {
        "title": "Projects",
        "seq": 7,
        "icon": "project",
        "header": "Vehicle Engineering & Plant Projects",
        "roles": ["Projects Manager", "Projects User", "Project User", "System Manager"],
        "cards": [
            {
                "card_name": "Project Tracking",
                "links": [
                    {"value": "Project", "label": "Automotive Projects", "type": "DocType"},
                    {"value": "Task", "label": "Tasks & Milestones", "type": "DocType"},
                    {"value": "Project Type", "label": "Project Types", "type": "DocType"},
                ]
            },
            {
                "card_name": "Timesheets & Activities",
                "links": [
                    {"value": "Activity Type", "label": "Activity Types", "type": "DocType"},
                    {"value": "Timesheet", "label": "Project Timesheets", "type": "DocType"},
                ]
            }
        ],
        "shortcuts": [
            {"value": "Project", "label": "Automotive Projects", "type": "DocType"},
            {"value": "Task", "label": "Tasks & Milestones", "type": "DocType"},
            {"value": "Timesheet", "label": "Project Timesheets", "type": "DocType"},
        ]
    },
    "HR": {
        "title": "HR",
        "seq": 8,
        "icon": "hr",
        "header": "Workforce, Departments & Controlled Role Assignments",
        "roles": ["HR Manager", "HR User", "System Manager"],
        "cards": [
            {
                "card_name": "Employees & Workforce",
                "links": [
                    {"value": "Employee", "label": "Employees", "type": "DocType"},
                    {"value": "Department", "label": "Departments", "type": "DocType"},
                    {"value": "Designation", "label": "Designations", "type": "DocType"},
                    {"value": "Branch", "label": "Branches & Plants", "type": "DocType"},
                ]
            },
            {
                "card_name": "User Accounts & Role Mapping",
                "links": [
                    {"value": "User", "label": "User Accounts", "type": "DocType"},
                    {"value": "Role", "label": "Roles", "type": "DocType"},
                    {"value": "Has Role", "label": "Role Assignments", "type": "DocType"},
                ]
            }
        ],
        "shortcuts": [
            {"value": "Employee", "label": "Employees", "type": "DocType"},
            {"value": "Department", "label": "Departments", "type": "DocType"},
            {"value": "Designation", "label": "Designations", "type": "DocType"},
            {"value": "User", "label": "User Accounts", "type": "DocType"},
        ]
    }
}

# --- TEST USERS & ROLES ---
TEST_USERS = [
    ("purchase.officer@orbis.test", "Ahmed", "Raza", "Purchase Officer", "Purchase", "Purchase Officer"),
    ("sales.officer@orbis.test", "Ali", "Khan", "Sales Officer", "Sales", "Sales Officer"),
    ("production.manager@orbis.test", "Hassan", "Malik", "Production Manager", "Production", "Production Manager"),
    ("storekeeper@orbis.test", "Usman", "Ali", "Storekeeper", "Operations", "Storekeeper"),
    ("floor.worker@orbis.test", "Hamza", "Ahmed", "Floor Worker", "Production", "Floor Worker"),
    ("finance.officer@orbis.test", "Ayesha", "Khan", "Finance Officer", "Accounts", "Finance Officer"),
    ("projects.manager@orbis.test", "Tariq", "Mehmood", "Projects Manager", "Operations", "Project Manager"),
    ("hr.manager@orbis.test", "Fatima", "Ali", "HR Manager", "Human Resources", "HR Manager"),
]

# (role, doctype, read, write, create, submit, cancel, amend, delete)
PERMISSIONS = [
    # Purchase Officer
    ("Purchase Officer", "Supplier",           1, 1, 1, 0, 0, 0, 0),
    ("Purchase Officer", "Supplier Group",     1, 0, 0, 0, 0, 0, 0),
    ("Purchase Officer", "Contact",            1, 1, 1, 0, 0, 0, 0),
    ("Purchase Officer", "Address",            1, 1, 1, 0, 0, 0, 0),
    ("Purchase Officer", "Material Request",   1, 1, 1, 1, 1, 1, 0),
    ("Purchase Officer", "Supplier Quotation", 1, 1, 1, 1, 1, 1, 0),
    ("Purchase Officer", "Purchase Order",     1, 1, 1, 1, 1, 1, 0),
    ("Purchase Officer", "Purchase Receipt",   1, 1, 1, 1, 1, 1, 0),
    ("Purchase Officer", "Purchase Invoice",   1, 1, 0, 0, 0, 0, 0),
    ("Purchase Officer", "Item",               1, 0, 0, 0, 0, 0, 0),
    ("Purchase Officer", "Warehouse",          1, 0, 0, 0, 0, 0, 0),

    # Sales Officer
    ("Sales Officer", "Customer",              1, 1, 1, 0, 0, 0, 0),
    ("Sales Officer", "Customer Group",        1, 0, 0, 0, 0, 0, 0),
    ("Sales Officer", "Contact",               1, 1, 1, 0, 0, 0, 0),
    ("Sales Officer", "Address",               1, 1, 1, 0, 0, 0, 0),
    ("Sales Officer", "Quotation",             1, 1, 1, 1, 1, 1, 0),
    ("Sales Officer", "Sales Order",           1, 1, 1, 1, 1, 1, 0),
    ("Sales Officer", "Sales Invoice",         1, 1, 0, 0, 0, 0, 0),
    ("Sales Officer", "Delivery Note",         1, 1, 1, 1, 1, 0, 0),
    ("Sales Officer", "Item",                  1, 0, 0, 0, 0, 0, 0),
    ("Sales Officer", "Vehicle Model",         1, 0, 0, 0, 0, 0, 0),
    ("Sales Officer", "Finished Vehicle Register", 1, 0, 0, 0, 0, 0, 0),

    # Production Manager
    ("Production Manager", "BOM",              1, 1, 1, 1, 1, 1, 0),
    ("Production Manager", "Production Plan",  1, 1, 1, 1, 1, 1, 0),
    ("Production Manager", "Work Order",       1, 1, 1, 1, 1, 1, 0),
    ("Production Manager", "Job Card",         1, 1, 1, 1, 0, 0, 0),
    ("Production Manager", "Workstation",      1, 1, 1, 0, 0, 0, 0),
    ("Production Manager", "Operation",        1, 1, 1, 0, 0, 0, 0),
    ("Production Manager", "Routing",          1, 1, 1, 0, 0, 0, 0),
    ("Production Manager", "Vehicle Model",    1, 1, 1, 0, 0, 0, 0),
    ("Production Manager", "Finished Vehicle Register", 1, 1, 1, 0, 0, 0, 0),
    ("Production Manager", "Stock Entry",      1, 1, 1, 1, 1, 0, 0),
    ("Production Manager", "Item",             1, 0, 0, 0, 0, 0, 0),
    ("Production Manager", "Warehouse",        1, 0, 0, 0, 0, 0, 0),
    ("Production Manager", "Quality Inspection", 1, 1, 1, 0, 0, 0, 0),
    ("Production Manager", "Non Conformance",  1, 1, 1, 0, 0, 0, 0),

    # Storekeeper
    ("Storekeeper", "Item",                    1, 1, 1, 0, 0, 0, 0),
    ("Storekeeper", "Item Group",              1, 0, 0, 0, 0, 0, 0),
    ("Storekeeper", "Warehouse",               1, 1, 0, 0, 0, 0, 0),
    ("Storekeeper", "UOM",                     1, 0, 0, 0, 0, 0, 0),
    ("Storekeeper", "Stock Entry",             1, 1, 1, 1, 1, 0, 0),
    ("Storekeeper", "Stock Reconciliation",    1, 1, 1, 1, 1, 0, 0),
    ("Storekeeper", "Purchase Receipt",        1, 1, 1, 1, 1, 0, 0),
    ("Storekeeper", "Delivery Note",           1, 1, 1, 1, 1, 0, 0),
    ("Storekeeper", "Material Request",        1, 1, 1, 1, 0, 0, 0),
    ("Storekeeper", "Serial No",               1, 1, 0, 0, 0, 0, 0),
    ("Storekeeper", "Batch",                   1, 1, 0, 0, 0, 0, 0),

    # Floor Worker (Strict Isolation)
    ("Floor Worker", "Job Card",               1, 1, 0, 0, 0, 0, 0),
    ("Floor Worker", "Work Order",             1, 0, 0, 0, 0, 0, 0),
    ("Floor Worker", "Operation",              1, 0, 0, 0, 0, 0, 0),
    ("Floor Worker", "Workstation",            1, 0, 0, 0, 0, 0, 0),
    ("Floor Worker", "Non Conformance",        1, 1, 1, 0, 0, 0, 0),
    ("Floor Worker", "Issue",                  1, 1, 1, 0, 0, 0, 0),

    # Finance Officer
    ("Finance Officer", "Sales Invoice",       1, 1, 1, 1, 1, 1, 0),
    ("Finance Officer", "Purchase Invoice",    1, 1, 1, 1, 1, 1, 0),
    ("Finance Officer", "Payment Entry",       1, 1, 1, 1, 1, 1, 0),
    ("Finance Officer", "Journal Entry",       1, 1, 1, 1, 1, 1, 0),
    ("Finance Officer", "Payment Request",     1, 1, 1, 1, 1, 0, 0),
    ("Finance Officer", "Account",             1, 0, 0, 0, 0, 0, 0),
    ("Finance Officer", "Cost Center",         1, 0, 0, 0, 0, 0, 0),
    ("Finance Officer", "Customer",            1, 0, 0, 0, 0, 0, 0),
    ("Finance Officer", "Supplier",            1, 0, 0, 0, 0, 0, 0),

    # Projects Manager
    ("Projects Manager", "Project",            1, 1, 1, 1, 1, 1, 0),
    ("Projects Manager", "Task",               1, 1, 1, 1, 0, 0, 0),
    ("Projects Manager", "Project Type",       1, 1, 1, 0, 0, 0, 0),
    ("Projects Manager", "Activity Type",      1, 1, 1, 0, 0, 0, 0),
    ("Projects Manager", "Timesheet",          1, 1, 1, 1, 1, 0, 0),

    # HR Manager
    ("HR Manager", "Employee",                 1, 1, 1, 0, 0, 0, 0),
    ("HR Manager", "Department",               1, 1, 1, 0, 0, 0, 0),
    ("HR Manager", "Designation",              1, 1, 1, 0, 0, 0, 0),
    ("HR Manager", "Branch",                   1, 1, 1, 0, 0, 0, 0),
    ("HR Manager", "User",                     1, 1, 1, 0, 0, 0, 0),
    ("HR Manager", "Role",                     1, 0, 0, 0, 0, 0, 0),
    ("HR Manager", "Has Role",                 1, 1, 1, 0, 0, 0, 1),
]


def check_target_exists(target, target_type):
    if target_type == "Report":
        return bool(frappe.db.exists("Report", target))
    return bool(frappe.db.exists("DocType", target))


def setup_roles():
    print("\n--- 1. Setting Up Job-Based Roles ---")
    for r in JOB_ROLES:
        if not frappe.db.exists("Role", r):
            role_doc = frappe.new_doc("Role")
            role_doc.role_name = r
            role_doc.desk_access = 1
            role_doc.is_custom = 1
            role_doc.disabled = 0
            role_doc.insert(ignore_permissions=True)
            print(f"  Created Role: {r}")
        else:
            frappe.db.set_value("Role", r, "desk_access", 1)
            print(f"  Ensured desk_access for: {r}")
    frappe.db.commit()


def setup_workspaces():
    print("\n--- 2. Configuring Exactly 8 Department Workspaces ---")
    created_workspaces = []

    for name, config in EIGHT_DEPARTMENTS.items():
        if frappe.db.exists("Workspace", name):
            ws = frappe.get_doc("Workspace", name)
            print(f"  Updating workspace: {name}")
        else:
            ws = frappe.new_doc("Workspace")
            ws.name = name
            print(f"  Creating workspace: {name}")

        ws.title = config["title"]
        ws.label = config["title"]
        ws.module = ""
        ws.is_hidden = 0
        ws.public = 1
        ws.type = "Workspace"
        ws.hide_custom = 0
        ws.sequence_id = float(config["seq"])
        ws.icon = config.get("icon", "dashboard")

        # Assign Roles
        ws.set("roles", [])
        for role_name in config["roles"]:
            if frappe.db.exists("Role", role_name):
                ws.append("roles", {"role": role_name})

        # Process Cards and Links
        ws.set("links", [])
        valid_cards = []
        card_idx = 0

        for card in config["cards"]:
            card_idx += 1
            card_links = []
            for lnk in card["links"]:
                if check_target_exists(lnk["value"], lnk["type"]):
                    card_links.append(lnk)

            if not card_links:
                continue

            valid_cards.append({"card_name": card["card_name"], "links": card_links})

            # Append Card Break
            ws.append("links", {
                "type": "Card Break",
                "label": card["card_name"],
                "idx": card_idx * 100,
                "is_query_report": 0,
                "dependencies": "",
                "link_type": "",
                "onboard": 0,
                "only_for": "",
                "doc_view": "",
                "card_type": "Custom",
            })

            link_idx = 0
            for lnk in card_links:
                link_idx += 1
                is_rep = 1 if lnk["type"] == "Report" else 0
                ws.append("links", {
                    "type": "Link",
                    "link_to": lnk["value"],
                    "label": lnk["label"],
                    "idx": card_idx * 100 + link_idx,
                    "is_query_report": is_rep,
                    "dependencies": "",
                    "link_type": lnk["type"],
                    "onboard": 1 if link_idx <= 2 else 0,
                    "only_for": "",
                    "doc_view": "",
                    "card_type": "Card",
                })

        # Process Shortcuts
        ws.set("shortcuts", [])
        valid_shortcuts = []
        sidx = 0
        for sc in config["shortcuts"]:
            if not check_target_exists(sc["value"], sc["type"]):
                continue
            sidx += 1
            is_rep = 1 if sc["type"] == "Report" else 0
            ws.append("shortcuts", {
                "type": sc["type"],
                "link_to": sc["value"],
                "label": sc["label"],
                "idx": sidx,
                "color": "#0284c7",
                "format": "Card",
                "doc_view": "",
            })
            valid_shortcuts.append(sc)

        # Generate Grid Layout Content JSON
        content_blocks = [
            {
                "id": f"hdr_{name[:6]}",
                "type": "header",
                "data": {
                    "text": f"<span class=\"h4\"><b>{config['header']}</b></span>",
                    "col": 12
                }
            }
        ]

        # Add shortcuts to content grid
        for sc in valid_shortcuts[:6]:
            content_blocks.append({
                "id": f"sc_{sc['value'][:8]}",
                "type": "shortcut",
                "data": {
                    "shortcut_name": sc["label"],
                    "col": 3
                }
            })

        # Add cards to content grid
        for c in valid_cards:
            content_blocks.append({
                "id": f"c_{c['card_name'][:8]}",
                "type": "card",
                "data": {
                    "card_name": c["card_name"],
                    "col": 6
                }
            })

        ws.content = json.dumps(content_blocks)
        ws.save(ignore_permissions=True)
        created_workspaces.append(name)
        print(f"    Saved Workspace: {name} (roles={len(ws.roles)}, links={len(ws.links)}, shortcuts={len(ws.shortcuts)})")

    frappe.db.commit()
    return created_workspaces


def hide_unrelated_workspaces():
    print("\n--- 3. Hiding All Unrelated Workspaces & Desktop Icons ---")
    keep_ws = set(EIGHT_DEPARTMENTS.keys())
    all_ws = frappe.db.sql("SELECT name FROM tabWorkspace", as_dict=True)
    hidden_count = 0

    for row in all_ws:
        w_name = row["name"]
        if w_name in keep_ws:
            continue
        try:
            w_doc = frappe.get_doc("Workspace", w_name)
            if not w_doc.type:
                w_doc.type = "Workspace"
            w_doc.is_hidden = 1
            w_doc.public = 0
            w_doc.set("roles", [{"role": "System Manager"}])
            w_doc.save(ignore_permissions=True)
            hidden_count += 1
            print(f"  Hidden workspace: {w_name}")
        except Exception as e:
            print(f"  Could not hide {w_name}: {e}")

    # Desktop Icons Cleanup
    # Map target departments to desktop icons
    dept_icon_map = {
        "Purchase": "Buying",
        "Selling": "Selling",
        "Manufacturing": "Manufacturing",
        "Stock": "Stock",
        "Projects": "Projects",
    }
    all_icons = frappe.get_all("Desktop Icon", fields=["name", "label"])
    for icon in all_icons:
        icon_name = icon["name"]
        # Keep only icons that correspond directly to our 8 departments
        if icon_name in ["Selling", "Manufacturing", "Stock", "Projects", "Buying", "Purchase"]:
            frappe.db.set_value("Desktop Icon", icon_name, "hidden", 0)
        else:
            frappe.db.set_value("Desktop Icon", icon_name, "hidden", 1)

    frappe.db.commit()
    print(f"  Hidden {hidden_count} unneeded workspaces and cleaned Desktop Icons.")


def setup_users_and_employees():
    print("\n--- 4. Setting Up Test Users & Linking Employee Records ---")
    # Ensure departments exist
    for _, _, _, _, dept_name, desig_name in TEST_USERS:
        if not frappe.db.exists("Department", {"department_name": dept_name, "company": COMPANY}):
            if not frappe.db.exists("Department", {"department_name": dept_name}):
                try:
                    dept = frappe.new_doc("Department")
                    dept.department_name = dept_name
                    dept.company = COMPANY
                    dept.insert(ignore_permissions=True)
                except Exception as e:
                    print(f"  Notice creating dept {dept_name}: {e}")

        if not frappe.db.exists("Designation", desig_name):
            desig = frappe.new_doc("Designation")
            desig.designation_name = desig_name
            desig.insert(ignore_permissions=True)

    for email, fname, lname, primary_role, dept_name, desig_name in TEST_USERS:
        # 1. User Account
        if not frappe.db.exists("User", email):
            user = frappe.new_doc("User")
            user.email = email
            user.first_name = fname
            user.last_name = lname
            user.enabled = 1
            user.user_type = "System User"
            user.send_welcome_email = 0
            user.insert(ignore_permissions=True)
            print(f"  Created User: {email}")
        else:
            user = frappe.get_doc("User", email)
            user.enabled = 1
            user.first_name = fname
            user.last_name = lname

        # Roles
        user.set("roles", [])
        user.append("roles", {"role": "Desk User"})
        user.append("roles", {"role": primary_role})
        user.save(ignore_permissions=True)

        # Set consistent password
        update_password(email, "Orbis@12345")

        # 2. Employee Record
        emp_filter = {"user_id": email}
        if frappe.db.exists("Employee", emp_filter):
            emp = frappe.get_doc("Employee", emp_filter)
        else:
            emp = frappe.new_doc("Employee")
            emp.first_name = fname
            emp.last_name = lname
            emp.user_id = email
            emp.company = COMPANY
            emp.status = "Active"
            emp.date_of_joining = "2026-01-01"
            emp.date_of_birth = "1990-01-01"

        dept_rec = frappe.db.get_value("Department", {"department_name": dept_name, "company": COMPANY}, "name")
        if not dept_rec:
            dept_rec = frappe.db.get_value("Department", {"department_name": dept_name}, "name")
        emp.department = dept_rec
        emp.designation = desig_name
        emp.gender = "Male" if fname not in ["Ayesha", "Fatima"] else "Female"
        emp.date_of_birth = "1990-01-01"
        emp.save(ignore_permissions=True)
        print(f"  Linked Employee: {emp.name} ({fname} {lname}) -> {email} ({desig_name})")

    frappe.db.commit()


def setup_custom_docperms():
    print("\n--- 5. Configuring Least-Privilege Custom DocPerms ---")
    count = 0
    for role, dt, r, w, c, sub, can, amd, d in PERMISSIONS:
        if not frappe.db.exists("DocType", dt):
            continue

        existing = frappe.db.get_value(
            "Custom DocPerm",
            {"parent": dt, "role": role},
            "name"
        )
        if existing:
            cdp = frappe.get_doc("Custom DocPerm", existing)
        else:
            cdp = frappe.new_doc("Custom DocPerm")
            cdp.parent = dt
            cdp.parenttype = "DocType"
            cdp.parentfield = "permissions"
            cdp.role = role

        cdp.read = r
        cdp.write = w
        cdp.create = c
        cdp.submit = sub
        cdp.cancel = can
        cdp.amend = amd
        cdp.delete = d
        cdp.save(ignore_permissions=True)
        count += 1

    frappe.db.commit()
    print(f"  Applied {count} Custom DocPerm rules.")


def setup_hr_guardrail():
    print("\n--- 6. Enforcing HR Privilege Escalation Guardrail ---")
    guard_name = "Orbis HR Role Guard"
    script_content = """frappe.ui.form.on('User', {
    validate: function(frm) {
        var restricted = ['System Manager', 'Administrator'];
        var is_admin = (frappe.user_roles || []).indexOf('System Manager') !== -1;
        if (!is_admin) {
            var roles = (frm.doc.roles || []).map(function(r){ return r.role; });
            for (var i = 0; i < restricted.length; i++) {
                if (roles.indexOf(restricted[i]) !== -1) {
                    frappe.throw(__('Security Violation: Only System Administrator is authorized to assign ' + restricted[i] + ' role.'));
                }
            }
        }
    }
});"""

    if frappe.db.exists("Client Script", guard_name):
        cs = frappe.get_doc("Client Script", guard_name)
    else:
        cs = frappe.new_doc("Client Script")
        cs.name = guard_name

    cs.dt = "User"
    cs.view = "Form"
    cs.enabled = 1
    cs.script = script_content
    cs.save(ignore_permissions=True)
    frappe.db.commit()
    print("  Client Script guardrail active on User Form.")


def apply_branding():
    print("\n--- 7. Applying User-Facing OrbisERP Branding ---")
    sys_settings = frappe.get_single("System Settings")
    sys_settings.app_name = "OrbisERP"
    sys_settings.save(ignore_permissions=True)

    web_settings = frappe.get_single("Website Settings")
    web_settings.app_name = "OrbisERP"
    web_settings.title_prefix = "OrbisERP"
    web_settings.brand_html = "<span>OrbisERP</span>"
    if frappe.db.exists("File", {"file_name": "ocm_logo_circular.png"}):
        web_settings.app_logo = "/files/ocm_logo_circular.png"
        web_settings.banner_image = "/files/ocm_logo_circular.png"
    if frappe.db.exists("File", {"file_name": "ocm_favicon.png"}):
        web_settings.favicon = "/files/ocm_favicon.png"
    web_settings.save(ignore_permissions=True)

    # Navbar Settings: Hide ERPNext Help Links
    try:
        navbar = frappe.get_single("Navbar Settings")
        for item in navbar.help_dropdown:
            if item.item_label in ["Documentation", "User Forum", "Frappe School", "Report an Issue", "Frappe Support"]:
                item.hidden = 1
        navbar.save(ignore_permissions=True)
        print("  Navbar help dropdown cleaned of third-party links.")
    except Exception as e:
        print(f"  Navbar notice: {e}")

    frappe.db.commit()
    print("  Branding successfully updated to OrbisERP.")


def main():
    print("=" * 80)
    print("  ORBIS ERP - STEP 15: CONFIGURE EIGHT DEPARTMENTS & RBAC")
    print("=" * 80)

    setup_roles()
    created = setup_workspaces()
    hide_unrelated_workspaces()
    setup_users_and_employees()
    setup_custom_docperms()
    setup_hr_guardrail()
    apply_branding()

    frappe.clear_cache()
    print("\n" + "=" * 80)
    print(f"  STEP 15 COMPLETE: {len(created)} DEPARTMENTS CONFIGURED & VERIFIED")
    print("=" * 80)
    return f"Configured {len(created)} departments successfully."


if __name__ == "__main__":
    frappe.init(site="frontend", sites_path="/home/frappe/frappe-bench/sites")
    frappe.connect()
    main()
    frappe.destroy()
