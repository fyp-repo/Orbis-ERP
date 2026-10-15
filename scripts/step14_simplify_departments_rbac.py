# Step 14: Simplify Orbis ERP - 9 Departments, Job-Based Roles and RBAC
# ======================================================================
# Objectives:
# A. Create 9 custom job-based roles (idempotent).
# B. Build exactly 9 public department workspaces with curated cards.
# C. Hide ALL other workspaces from non-Admin navigation.
# D. Configure server-side Custom DocPerm for every role.
# E. Create one demo test user per department role for validation.
# F. Enforce HR security guardrail (HR Manager cannot assign System Manager).
#
# Constraints:
# - No DocTypes, tables, or existing business records are deleted.
# - All changes are idempotent - re-running is harmless.
# - Administrator / System Manager permissions are never restricted.

import frappe

JOB_ROLES = [
    "Purchase Officer",
    "Sales Officer",
    "Production Manager",
    "Floor Worker",
    "Storekeeper",
    "Delivery Officer",
    "Finance Officer",
    "Quality Inspector",
]

WORKSPACES = {
    "Purchase": {
        "roles": ["Purchase Officer", "Purchase Manager", "Purchase User", "Purchase Master Manager"],
        "cards": [
            {"card_name": "Suppliers", "links": [
                {"type": "DocType", "value": "Supplier", "label": "Suppliers"},
                {"type": "DocType", "value": "Supplier Group", "label": "Supplier Groups"},
                {"type": "DocType", "value": "Contact", "label": "Contacts"},
            ]},
            {"card_name": "Procurement", "links": [
                {"type": "DocType", "value": "Material Request", "label": "Material Requests"},
                {"type": "DocType", "value": "Supplier Quotation", "label": "Supplier Quotations"},
                {"type": "DocType", "value": "Purchase Order", "label": "Purchase Orders"},
                {"type": "DocType", "value": "Purchase Receipt", "label": "Purchase Receipts"},
                {"type": "DocType", "value": "Purchase Invoice", "label": "Purchase Invoices"},
            ]},
            {"card_name": "Reports", "links": [
                {"type": "Report", "value": "Purchase Order Trends", "label": "Purchase Order Trends"},
                {"type": "Report", "value": "Requested Items To Be Ordered", "label": "Requested Items"},
                {"type": "Report", "value": "Purchase Receipt Trends", "label": "Purchase Receipt Trends"},
            ]},
        ],
    },
    "Selling": {
        "roles": ["Sales Officer", "Sales Manager", "Sales User", "Sales Master Manager"],
        "cards": [
            {"card_name": "Customers", "links": [
                {"type": "DocType", "value": "Customer", "label": "Customers"},
                {"type": "DocType", "value": "Customer Group", "label": "Customer Groups"},
                {"type": "DocType", "value": "Contact", "label": "Contacts"},
            ]},
            {"card_name": "Sales Transactions", "links": [
                {"type": "DocType", "value": "Quotation", "label": "Quotations"},
                {"type": "DocType", "value": "Sales Order", "label": "Sales Orders"},
                {"type": "DocType", "value": "Sales Invoice", "label": "Sales Invoices"},
                {"type": "DocType", "value": "Delivery Note", "label": "Delivery Notes"},
            ]},
            {"card_name": "Reports", "links": [
                {"type": "Report", "value": "Sales Order Trends", "label": "Sales Order Trends"},
                {"type": "Report", "value": "Quotation Trends", "label": "Quotation Trends"},
                {"type": "Report", "value": "Sales Analytics", "label": "Sales Analytics"},
            ]},
        ],
    },
    "HR": {
        "roles": ["HR Manager", "HR User"],
        "cards": [
            {"card_name": "Employees", "links": [
                {"type": "DocType", "value": "Employee", "label": "Employees"},
                {"type": "DocType", "value": "Department", "label": "Departments"},
                {"type": "DocType", "value": "Designation", "label": "Designations"},
                {"type": "DocType", "value": "Employee Grade", "label": "Employee Grades"},
            ]},
            {"card_name": "User and Access Management", "links": [
                {"type": "DocType", "value": "User", "label": "Users"},
                {"type": "DocType", "value": "Role", "label": "Roles"},
                {"type": "DocType", "value": "Has Role", "label": "Role Assignments"},
            ]},
            {"card_name": "Reports", "links": [
                {"type": "Report", "value": "Employee Birthday", "label": "Employee Birthdays"},
                {"type": "Report", "value": "Headcount Report", "label": "Headcount Report"},
            ]},
        ],
    },
    "Manufacturing": {
        "roles": ["Production Manager", "Manufacturing Manager", "Manufacturing User"],
        "cards": [
            {"card_name": "Planning", "links": [
                {"type": "DocType", "value": "BOM", "label": "Bill of Materials (BOM)"},
                {"type": "DocType", "value": "Production Plan", "label": "Production Plans"},
                {"type": "DocType", "value": "Work Order", "label": "Work Orders"},
                {"type": "DocType", "value": "Job Card", "label": "Job Cards"},
            ]},
            {"card_name": "Assembly Setup", "links": [
                {"type": "DocType", "value": "Workstation", "label": "Workstations"},
                {"type": "DocType", "value": "Operation", "label": "Operations"},
                {"type": "DocType", "value": "Routing", "label": "Routings"},
                {"type": "DocType", "value": "Vehicle Model", "label": "Vehicle Models"},
            ]},
            {"card_name": "Reports", "links": [
                {"type": "Report", "value": "Work Order Summary", "label": "Work Order Summary"},
                {"type": "Report", "value": "Production Planning Report", "label": "Production Planning"},
                {"type": "Report", "value": "BOM Stock Report", "label": "BOM Stock Report"},
            ]},
        ],
    },
    "Stock": {
        "roles": ["Storekeeper", "Stock Manager", "Stock User", "Item Manager"],
        "cards": [
            {"card_name": "Items and Warehouses", "links": [
                {"type": "DocType", "value": "Item", "label": "Items"},
                {"type": "DocType", "value": "Item Group", "label": "Item Groups"},
                {"type": "DocType", "value": "Warehouse", "label": "Warehouses"},
                {"type": "DocType", "value": "UOM", "label": "Units of Measure"},
            ]},
            {"card_name": "Stock Transactions", "links": [
                {"type": "DocType", "value": "Stock Entry", "label": "Stock Entries"},
                {"type": "DocType", "value": "Purchase Receipt", "label": "Purchase Receipts"},
                {"type": "DocType", "value": "Delivery Note", "label": "Delivery Notes"},
                {"type": "DocType", "value": "Stock Reconciliation", "label": "Stock Reconciliation"},
            ]},
            {"card_name": "Reports", "links": [
                {"type": "Report", "value": "Stock Balance", "label": "Stock Balance"},
                {"type": "Report", "value": "Stock Ledger", "label": "Stock Ledger"},
                {"type": "Report", "value": "Itemwise Reorder Detail", "label": "Reorder Alerts"},
                {"type": "Report", "value": "Stock Summary", "label": "Stock Summary"},
            ]},
        ],
    },
    "Floor User (Workers)": {
        "roles": ["Floor Worker", "Manufacturing User"],
        "cards": [
            {"card_name": "My Work", "links": [
                {"type": "DocType", "value": "Job Card", "label": "My Job Cards"},
                {"type": "DocType", "value": "Work Order", "label": "Work Orders (View Only)"},
            ]},
            {"card_name": "Report Issues", "links": [
                {"type": "DocType", "value": "Non Conformance", "label": "Report Quality Issue or Defect"},
            ]},
        ],
    },
    "Delivery": {
        "roles": ["Delivery Officer", "Delivery Manager", "Delivery User"],
        "cards": [
            {"card_name": "Dispatch", "links": [
                {"type": "DocType", "value": "Delivery Note", "label": "Delivery Notes"},
                {"type": "DocType", "value": "Delivery Trip", "label": "Delivery Trips"},
                {"type": "DocType", "value": "Sales Order", "label": "Sales Orders (View)"},
                {"type": "DocType", "value": "Packing Slip", "label": "Packing Slips"},
            ]},
            {"card_name": "Finished Vehicles", "links": [
                {"type": "DocType", "value": "Finished Vehicle Register", "label": "Finished Vehicle Register"},
                {"type": "DocType", "value": "Serial No", "label": "Serial Numbers"},
            ]},
            {"card_name": "Reports", "links": [
                {"type": "Report", "value": "Delivery Note Trends", "label": "Delivery Trends"},
            ]},
        ],
    },
    "Finance": {
        "roles": ["Finance Officer", "Accounts Manager", "Accounts User"],
        "cards": [
            {"card_name": "Invoices", "links": [
                {"type": "DocType", "value": "Sales Invoice", "label": "Sales Invoices"},
                {"type": "DocType", "value": "Purchase Invoice", "label": "Purchase Invoices"},
            ]},
            {"card_name": "Payments", "links": [
                {"type": "DocType", "value": "Payment Entry", "label": "Payment Entries"},
                {"type": "DocType", "value": "Journal Entry", "label": "Journal Entries"},
                {"type": "DocType", "value": "Payment Request", "label": "Payment Requests"},
            ]},
            {"card_name": "Accounting", "links": [
                {"type": "DocType", "value": "Chart of Accounts", "label": "Chart of Accounts"},
                {"type": "DocType", "value": "Cost Center", "label": "Cost Centers"},
                {"type": "DocType", "value": "Account", "label": "Accounts"},
            ]},
            {"card_name": "Reports", "links": [
                {"type": "Report", "value": "Profit and Loss Statement", "label": "Profit and Loss"},
                {"type": "Report", "value": "Balance Sheet", "label": "Balance Sheet"},
                {"type": "Report", "value": "Accounts Receivable", "label": "Accounts Receivable"},
                {"type": "Report", "value": "Accounts Payable", "label": "Accounts Payable"},
            ]},
        ],
    },
    "Quality": {
        "roles": ["Quality Inspector", "Quality Manager"],
        "cards": [
            {"card_name": "Inspections", "links": [
                {"type": "DocType", "value": "Quality Inspection", "label": "Quality Inspections"},
                {"type": "DocType", "value": "Quality Inspection Template", "label": "Inspection Templates"},
                {"type": "DocType", "value": "Quality Inspection Parameter", "label": "Inspection Parameters"},
            ]},
            {"card_name": "Defects and Actions", "links": [
                {"type": "DocType", "value": "Non Conformance", "label": "Non-Conformances / Defects"},
                {"type": "DocType", "value": "Quality Action", "label": "Corrective Actions"},
                {"type": "DocType", "value": "Quality Review", "label": "Quality Reviews"},
            ]},
            {"card_name": "Reports", "links": [
                {"type": "Report", "value": "Quality Inspection Summary", "label": "Inspection Summary"},
            ]},
        ],
    },
}

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
    ("Sales Officer", "Lead",                  1, 1, 1, 0, 0, 0, 0),
    ("Sales Officer", "Quotation",             1, 1, 1, 1, 1, 1, 0),
    ("Sales Officer", "Sales Order",           1, 1, 1, 1, 1, 1, 0),
    ("Sales Officer", "Sales Invoice",         1, 1, 0, 0, 0, 0, 0),
    ("Sales Officer", "Delivery Note",         1, 0, 0, 0, 0, 0, 0),
    ("Sales Officer", "Item",                  1, 0, 0, 0, 0, 0, 0),
    ("Sales Officer", "Price List",            1, 0, 0, 0, 0, 0, 0),
    ("Sales Officer", "Item Price",            1, 0, 0, 0, 0, 0, 0),
    # HR Manager
    ("HR Manager", "Employee",                 1, 1, 1, 0, 0, 0, 0),
    ("HR Manager", "Department",               1, 1, 1, 0, 0, 0, 0),
    ("HR Manager", "Designation",              1, 1, 1, 0, 0, 0, 0),
    ("HR Manager", "Employee Grade",           1, 1, 1, 0, 0, 0, 0),
    ("HR Manager", "Branch",                   1, 1, 1, 0, 0, 0, 0),
    ("HR Manager", "User",                     1, 1, 1, 0, 0, 0, 0),
    ("HR Manager", "Role",                     1, 0, 0, 0, 0, 0, 0),
    ("HR Manager", "Has Role",                 1, 1, 1, 0, 0, 0, 1),
    ("HR Manager", "Leave Type",               1, 0, 0, 0, 0, 0, 0),
    # Production Manager
    ("Production Manager", "BOM",              1, 1, 1, 1, 1, 1, 0),
    ("Production Manager", "Production Plan",  1, 1, 1, 1, 1, 1, 0),
    ("Production Manager", "Work Order",       1, 1, 1, 1, 1, 1, 0),
    ("Production Manager", "Job Card",         1, 1, 1, 1, 0, 0, 0),
    ("Production Manager", "Workstation",      1, 1, 1, 0, 0, 0, 0),
    ("Production Manager", "Operation",        1, 1, 1, 0, 0, 0, 0),
    ("Production Manager", "Routing",          1, 1, 1, 0, 0, 0, 0),
    ("Production Manager", "Item",             1, 0, 0, 0, 0, 0, 0),
    ("Production Manager", "Warehouse",        1, 0, 0, 0, 0, 0, 0),
    ("Production Manager", "Vehicle Model",    1, 1, 1, 0, 0, 0, 0),
    ("Production Manager", "Stock Entry",      1, 1, 1, 1, 1, 0, 0),
    ("Production Manager", "Quality Inspection", 1, 0, 0, 0, 0, 0, 0),
    # Floor Worker - strict isolation
    ("Floor Worker", "Job Card",               1, 1, 0, 0, 0, 0, 0),
    ("Floor Worker", "Work Order",             1, 0, 0, 0, 0, 0, 0),
    ("Floor Worker", "Workstation",            1, 0, 0, 0, 0, 0, 0),
    ("Floor Worker", "Operation",              1, 0, 0, 0, 0, 0, 0),
    ("Floor Worker", "Non Conformance",        1, 1, 1, 0, 0, 0, 0),
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
    ("Storekeeper", "Packing Slip",            1, 1, 1, 0, 0, 0, 0),
    ("Storekeeper", "Serial No",               1, 1, 0, 0, 0, 0, 0),
    ("Storekeeper", "Batch",                   1, 1, 0, 0, 0, 0, 0),
    # Delivery Officer
    ("Delivery Officer", "Delivery Note",      1, 1, 1, 1, 1, 1, 0),
    ("Delivery Officer", "Delivery Trip",      1, 1, 1, 0, 0, 0, 0),
    ("Delivery Officer", "Sales Order",        1, 0, 0, 0, 0, 0, 0),
    ("Delivery Officer", "Packing Slip",       1, 1, 1, 0, 0, 0, 0),
    ("Delivery Officer", "Finished Vehicle Register", 1, 1, 0, 0, 0, 0, 0),
    ("Delivery Officer", "Serial No",          1, 0, 0, 0, 0, 0, 0),
    ("Delivery Officer", "Customer",           1, 0, 0, 0, 0, 0, 0),
    ("Delivery Officer", "Address",            1, 0, 0, 0, 0, 0, 0),
    # Finance Officer
    ("Finance Officer", "Sales Invoice",       1, 1, 1, 1, 1, 1, 0),
    ("Finance Officer", "Purchase Invoice",    1, 1, 1, 1, 1, 1, 0),
    ("Finance Officer", "Payment Entry",       1, 1, 1, 1, 1, 1, 0),
    ("Finance Officer", "Journal Entry",       1, 1, 1, 1, 1, 1, 0),
    ("Finance Officer", "Payment Request",     1, 1, 1, 1, 1, 0, 0),
    ("Finance Officer", "Account",             1, 0, 0, 0, 0, 0, 0),
    ("Finance Officer", "Chart of Accounts",   1, 0, 0, 0, 0, 0, 0),
    ("Finance Officer", "Cost Center",         1, 0, 0, 0, 0, 0, 0),
    ("Finance Officer", "Currency",            1, 0, 0, 0, 0, 0, 0),
    ("Finance Officer", "Customer",            1, 0, 0, 0, 0, 0, 0),
    ("Finance Officer", "Supplier",            1, 0, 0, 0, 0, 0, 0),
    # Quality Inspector
    ("Quality Inspector", "Quality Inspection",           1, 1, 1, 1, 1, 0, 0),
    ("Quality Inspector", "Quality Inspection Template",  1, 1, 1, 0, 0, 0, 0),
    ("Quality Inspector", "Quality Inspection Parameter", 1, 1, 1, 0, 0, 0, 0),
    ("Quality Inspector", "Non Conformance",              1, 1, 1, 1, 0, 0, 0),
    ("Quality Inspector", "Quality Action",               1, 1, 1, 0, 0, 0, 0),
    ("Quality Inspector", "Quality Review",               1, 1, 1, 0, 0, 0, 0),
    ("Quality Inspector", "Item",                         1, 0, 0, 0, 0, 0, 0),
    ("Quality Inspector", "Work Order",                   1, 0, 0, 0, 0, 0, 0),
    ("Quality Inspector", "Purchase Receipt",             1, 0, 0, 0, 0, 0, 0),
    ("Quality Inspector", "Finished Vehicle Register",    1, 1, 0, 0, 0, 0, 0),
]

# (email, first_name, last_name, role)
TEST_USERS = [
    ("purchase.officer@orbis.test",   "Omar",   "Purchase",   "Purchase Officer"),
    ("sales.officer@orbis.test",      "Sara",   "Sales",      "Sales Officer"),
    ("hr.manager@orbis.test",         "Hina",   "HR",         "HR Manager"),
    ("production.manager@orbis.test", "Pavlov", "Production", "Production Manager"),
    ("floor.worker@orbis.test",       "Farhan", "Floor",      "Floor Worker"),
    ("storekeeper@orbis.test",        "Saad",   "Store",      "Storekeeper"),
    ("delivery.officer@orbis.test",   "Dana",   "Delivery",   "Delivery Officer"),
    ("finance.officer@orbis.test",    "Faraz",  "Finance",    "Finance Officer"),
    ("quality.inspector@orbis.test",  "Qamar",  "Quality",    "Quality Inspector"),
]


def step_a_create_roles():
    print("\n=== STEP A: Creating Job-Based Roles ===")
    created = []
    for role_name in JOB_ROLES:
        if not frappe.db.exists("Role", role_name):
            role_doc = frappe.get_doc({
                "doctype": "Role",
                "role_name": role_name,
                "desk_access": 1,
                "is_custom": 1,
                "disabled": 0,
            })
            role_doc.insert(ignore_permissions=True)
            created.append(role_name)
            print("  Created role: " + role_name)
        else:
            frappe.db.set_value("Role", role_name, "desk_access", 1)
            print("  Role exists (desk_access ensured): " + role_name)

    if frappe.db.exists("Role", "HR Manager"):
        frappe.db.set_value("Role", "HR Manager", "desk_access", 1)
        print("  HR Manager desk_access ensured.")

    frappe.db.commit()
    print("  Created " + str(len(created)) + " new roles.")
    return created


def step_b_build_workspaces():
    print("\n=== STEP B: Building 9 Department Workspaces ===")
    for ws_name, ws_def in WORKSPACES.items():
        print("\n  Processing workspace: " + ws_name)
        if frappe.db.exists("Workspace", ws_name):
            ws = frappe.get_doc("Workspace", ws_name)
            print("    Updating existing workspace")
        else:
            ws = frappe.new_doc("Workspace")
            ws.name = ws_name
            ws.label = ws_name
            print("    Creating new workspace")

        ws.label = ws_name
        ws.title = ws_name
        ws.module = ""
        ws.is_hidden = 0
        ws.public = 1
        ws.type = "Workspace"
        ws.hide_custom = 0

        ws.set("roles", [])
        ws.append("roles", {"role": "System Manager"})
        for role in ws_def["roles"]:
            if frappe.db.exists("Role", role):
                ws.append("roles", {"role": role})
            else:
                print("    Role not found, skipping: " + role)

        ws.set("links", [])
        card_idx = 0
        for card in ws_def["cards"]:
            card_idx += 1
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
            for lnk in card["links"]:
                link_idx += 1
                ws.append("links", {
                    "type": lnk["type"],
                    "link_to": lnk["value"],
                    "label": lnk["label"],
                    "idx": card_idx * 100 + link_idx,
                    "is_query_report": 1 if lnk["type"] == "Report" else 0,
                    "dependencies": "",
                    "link_type": lnk["type"],
                    "onboard": 1 if link_idx <= 2 else 0,
                    "only_for": "",
                    "doc_view": "",
                    "card_type": "Card",
                })

        ws.set("shortcuts", [])
        sidx = 0
        for card in ws_def["cards"]:
            for lnk in card["links"]:
                if sidx >= 6:
                    break
                sidx += 1
                ws.append("shortcuts", {
                    "type": lnk["type"],
                    "link_to": lnk["value"],
                    "label": lnk["label"],
                    "idx": sidx,
                    "is_query_report": 1 if lnk["type"] == "Report" else 0,
                    "color": "#2490EF",
                    "format": "Card",
                    "doc_view": "",
                })
            if sidx >= 6:
                break

        try:
            ws.save(ignore_permissions=True)
            print("    Saved: " + ws_name + " (roles: " + str(len(ws.roles)) + ", links: " + str(len(ws.links)) + ")")
        except Exception as e:
            print("    ERROR saving " + ws_name + ": " + str(e))

    frappe.db.commit()


def step_c_hide_other_workspaces():
    print("\n=== STEP C: Hiding Non-Department Workspaces ===")
    all_ws = frappe.db.sql("SELECT name FROM tabWorkspace", as_dict=True)
    keep_visible = set(WORKSPACES.keys())
    hidden_count = 0
    for row in all_ws:
        ws_name = row["name"]
        if ws_name in keep_visible:
            continue
        try:
            ws = frappe.get_doc("Workspace", ws_name)
            if not ws.type:
                ws.type = "Workspace"
            ws.is_hidden = 1
            ws.public = 0
            ws.set("roles", [{"role": "System Manager"}])
            ws.save(ignore_permissions=True)
            print("  Hidden: " + ws_name)
            hidden_count += 1
        except Exception as e:
            print("  Could not hide " + ws_name + ": " + str(e))
    frappe.db.commit()
    print("  Total hidden: " + str(hidden_count))


def step_d_configure_permissions():
    print("\n=== STEP D: Configuring Custom DocPerm (Server-Side) ===")
    created = 0
    updated = 0
    for perm_tuple in PERMISSIONS:
        role, doctype, read, write, create, submit, cancel, amend, delete = perm_tuple
        if not frappe.db.exists("DocType", doctype):
            print("  DocType not found, skipping: " + doctype)
            continue
        existing = frappe.db.get_value(
            "Custom DocPerm",
            {"parent": doctype, "role": role, "permlevel": 0},
            "name"
        )
        perm_values = {
            "parent": doctype, "role": role, "permlevel": 0,
            "read": read, "write": write, "create": create,
            "submit": submit, "cancel": cancel, "amend": amend,
            "delete": delete, "report": read, "export": read,
            "import": 0, "share": read, "print": read, "email": read,
        }
        if existing:
            frappe.db.set_value("Custom DocPerm", existing, perm_values)
            updated += 1
        else:
            cdp = frappe.get_doc({
                "doctype": "Custom DocPerm",
                "parenttype": "DocType",
                "parentfield": "permissions",
            })
            for k, v in perm_values.items():
                setattr(cdp, k, v)
            cdp.insert(ignore_permissions=True)
            created += 1
    frappe.db.commit()
    print("  Custom DocPerm: " + str(created) + " created, " + str(updated) + " updated")
    try:
        frappe.clear_cache()
        print("  Cache cleared.")
    except Exception as e:
        print("  Cache clear warning: " + str(e))


def step_e_floor_worker_isolation():
    print("\n=== STEP E: Verifying Floor Worker Isolation ===")
    blocked = [
        "Sales Invoice", "Purchase Invoice", "Payment Entry",
        "Journal Entry", "Employee", "User", "Purchase Order",
        "Quotation", "Sales Order", "Customer", "Supplier",
        "Account", "Chart of Accounts",
    ]
    issues = []
    for dt in blocked:
        row = frappe.db.get_value(
            "Custom DocPerm",
            {"parent": dt, "role": "Floor Worker", "permlevel": 0},
            ["name", "read"],
            as_dict=True,
        )
        if row and row.get("read"):
            issues.append(dt)
    if issues:
        print("  ISSUE - Floor Worker has read access to: " + str(issues))
    else:
        print("  OK - Floor Worker correctly isolated from restricted DocTypes.")
    return issues


def step_f_hr_security_guardrail():
    print("\n=== STEP F: HR Manager Security Guardrail ===")
    existing = frappe.db.get_value(
        "Custom DocPerm",
        {"parent": "Role", "role": "HR Manager", "permlevel": 0},
        "name"
    )
    if existing:
        frappe.db.set_value("Custom DocPerm", existing, {
            "read": 1, "write": 0, "create": 0, "delete": 0
        })
        print("  HR Manager Role DocPerm: read-only enforced.")
    else:
        cdp = frappe.get_doc({"doctype": "Custom DocPerm", "parenttype": "DocType", "parentfield": "permissions"})
        cdp.parent = "Role"
        cdp.role = "HR Manager"
        cdp.permlevel = 0
        cdp.read = 1
        cdp.write = 0
        cdp.create = 0
        cdp.submit = 0
        cdp.cancel = 0
        cdp.amend = 0
        cdp.delete = 0
        cdp.insert(ignore_permissions=True)
        print("  HR Manager Role DocPerm created: read-only.")

    script_name = "Orbis HR Role Guard"
    script_code = (
        "frappe.ui.form.on('User', {"
        "validate: function(frm) {"
        "var restricted = ['System Manager', 'Administrator'];"
        "var is_admin = (frappe.user_roles || []).indexOf('System Manager') !== -1;"
        "if (!is_admin) {"
        "var roles = (frm.doc.roles || []).map(function(r){return r.role;});"
        "for (var i = 0; i < restricted.length; i++) {"
        "if (roles.indexOf(restricted[i]) !== -1) {"
        "frappe.throw('You are not authorised to assign the ' + restricted[i] + ' role.');"
        "}}}}});"
    )
    if frappe.db.exists("Client Script", script_name):
        cs = frappe.get_doc("Client Script", script_name)
        cs.script = script_code
        cs.enabled = 1
        cs.save(ignore_permissions=True)
        print("  Client Script updated: " + script_name)
    else:
        cs = frappe.get_doc({
            "doctype": "Client Script",
            "name": script_name,
            "dt": "User",
            "view": "Form",
            "script": script_code,
            "enabled": 1,
        })
        cs.insert(ignore_permissions=True)
        print("  Client Script created: " + script_name)

    frappe.db.commit()
    print("  HR security guardrail applied.")


def step_g_create_test_users():
    print("\n=== STEP G: Creating Demo Test Users ===")
    created_count = 0
    skipped_count = 0
    for email, first_name, last_name, role in TEST_USERS:
        if frappe.db.exists("User", email):
            skipped_count += 1
            existing_roles = [r.role for r in frappe.get_doc("User", email).roles]
            if role not in existing_roles:
                usr = frappe.get_doc("User", email)
                usr.append("roles", {"role": role})
                if "Desk User" not in existing_roles:
                    usr.append("roles", {"role": "Desk User"})
                usr.save(ignore_permissions=True)
                print("  User exists, added role " + role + ": " + email)
            else:
                print("  User exists (role OK): " + email)
            continue
        try:
            usr = frappe.get_doc({
                "doctype": "User",
                "email": email,
                "first_name": first_name,
                "last_name": last_name,
                "enabled": 1,
                "new_password": "Orbis@2026",
                "send_welcome_email": 0,
                "user_type": "System User",
                "roles": [{"role": "Desk User"}, {"role": role}],
            })
            usr.insert(ignore_permissions=True)
            created_count += 1
            print("  Created user: " + email + " | Role: " + role)
        except Exception as e:
            print("  ERROR creating user " + email + ": " + str(e))
    frappe.db.commit()
    print("  Users created: " + str(created_count) + ", skipped: " + str(skipped_count))


def step_h_validate():
    print("\n=== STEP H: Validation Report ===")

    ws_data = frappe.db.sql("SELECT name, is_hidden, public FROM tabWorkspace ORDER BY name", as_dict=True)
    print("\n  [Workspaces]")
    for w in ws_data:
        visible = (not w["is_hidden"]) and w["public"]
        status = "VISIBLE" if visible else "hidden "
        print("    " + status + ": " + w["name"])

    print("\n  [Custom DocPerm by Role]")
    cdp_summary = frappe.db.sql(
        "SELECT role, COUNT(*) as cnt FROM `tabCustom DocPerm` GROUP BY role ORDER BY role",
        as_dict=True
    )
    for row in cdp_summary:
        print("    " + str(row["role"]) + ": " + str(row["cnt"]) + " rules")

    print("\n  [Test Users]")
    for email, first_name, last_name, role in TEST_USERS:
        exists = frappe.db.exists("User", email)
        has_role = False
        if exists:
            has_role = role in [r.role for r in frappe.get_doc("User", email).roles]
        status = "OK     " if (exists and has_role) else "MISSING"
        print("    " + status + " " + email + " | Role: " + role)

    print("\n  [Floor Worker Isolation]")
    blocked = ["Sales Invoice", "Purchase Invoice", "Payment Entry", "Employee", "User", "Purchase Order", "Supplier"]
    clean = True
    for dt in blocked:
        has_perm = frappe.db.get_value(
            "Custom DocPerm",
            {"parent": dt, "role": "Floor Worker", "permlevel": 0, "read": 1},
            "name"
        )
        if has_perm:
            print("    ISSUE: Floor Worker has read on: " + dt)
            clean = False
    if clean:
        print("    OK - Floor Worker correctly isolated.")

    print("\n  [HR Manager Role Write Access]")
    hr_perm = frappe.db.get_value(
        "Custom DocPerm",
        {"parent": "Role", "role": "HR Manager", "permlevel": 0},
        ["read", "write"],
        as_dict=True
    )
    if hr_perm:
        if hr_perm.get("write"):
            print("    ISSUE: HR Manager has WRITE access to Role!")
        else:
            print("    OK - HR Manager has read-only access to Role.")
    else:
        print("    WARNING: No Custom DocPerm for HR Manager on Role.")

    return "Validation complete"


def run():
    print("=" * 70)
    print("  STEP 14: ORBIS ERP - 9 DEPARTMENTS, JOB ROLES AND RBAC")
    print("=" * 70)
    step_a_create_roles()
    step_b_build_workspaces()
    step_c_hide_other_workspaces()
    step_d_configure_permissions()
    step_e_floor_worker_isolation()
    step_f_hr_security_guardrail()
    step_g_create_test_users()
    step_h_validate()
    print("\n" + "=" * 70)
    print("  STEP 14 COMPLETE")
    print("=" * 70)
    return "Step 14 - Simplify Departments and RBAC: DONE"

if __name__ == '__main__':
    frappe.init(site='frontend', sites_path='/home/frappe/frappe-bench/sites')
    frappe.connect()
    run()
    frappe.destroy()
