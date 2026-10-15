# Step 14b: Fix Workspace Link Types and Re-Build All 9 Department Workspaces
# =============================================================================
# Fixes from step14 run:
# 1. Frappe v16 workspace links must use type="Link" (not "DocType")
# 2. Removes non-existent report/doctype links that caused save errors
# 3. Re-saves all 9 workspaces correctly, then re-hides all others
#
# Idempotent - safe to re-run.

import frappe

# Only DocTypes/Reports confirmed to exist in standard ERPNext installs
WORKSPACES = {
    "Purchase": {
        "roles": ["Purchase Officer", "Purchase Manager", "Purchase User", "Purchase Master Manager"],
        "cards": [
            {"card_name": "Suppliers", "links": [
                {"type": "Link", "value": "Supplier",        "label": "Suppliers",        "is_report": 0},
                {"type": "Link", "value": "Supplier Group",  "label": "Supplier Groups",  "is_report": 0},
                {"type": "Link", "value": "Contact",         "label": "Contacts",         "is_report": 0},
            ]},
            {"card_name": "Procurement", "links": [
                {"type": "Link", "value": "Material Request",   "label": "Material Requests",   "is_report": 0},
                {"type": "Link", "value": "Supplier Quotation", "label": "Supplier Quotations", "is_report": 0},
                {"type": "Link", "value": "Purchase Order",     "label": "Purchase Orders",     "is_report": 0},
                {"type": "Link", "value": "Purchase Receipt",   "label": "Purchase Receipts",   "is_report": 0},
                {"type": "Link", "value": "Purchase Invoice",   "label": "Purchase Invoices",   "is_report": 0},
            ]},
            {"card_name": "Reports", "links": [
                {"type": "Link", "value": "Purchase Order Trends",   "label": "Purchase Order Trends",   "is_report": 1},
                {"type": "Link", "value": "Purchase Receipt Trends", "label": "Purchase Receipt Trends", "is_report": 1},
            ]},
        ],
    },
    "Selling": {
        "roles": ["Sales Officer", "Sales Manager", "Sales User", "Sales Master Manager"],
        "cards": [
            {"card_name": "Customers", "links": [
                {"type": "Link", "value": "Customer",       "label": "Customers",       "is_report": 0},
                {"type": "Link", "value": "Customer Group", "label": "Customer Groups", "is_report": 0},
                {"type": "Link", "value": "Contact",        "label": "Contacts",        "is_report": 0},
            ]},
            {"card_name": "Sales Transactions", "links": [
                {"type": "Link", "value": "Quotation",     "label": "Quotations",     "is_report": 0},
                {"type": "Link", "value": "Sales Order",   "label": "Sales Orders",   "is_report": 0},
                {"type": "Link", "value": "Sales Invoice", "label": "Sales Invoices", "is_report": 0},
                {"type": "Link", "value": "Delivery Note", "label": "Delivery Notes", "is_report": 0},
            ]},
            {"card_name": "Reports", "links": [
                {"type": "Link", "value": "Sales Order Trends", "label": "Sales Order Trends", "is_report": 1},
                {"type": "Link", "value": "Quotation Trends",   "label": "Quotation Trends",   "is_report": 1},
                {"type": "Link", "value": "Sales Analytics",    "label": "Sales Analytics",    "is_report": 1},
            ]},
        ],
    },
    "HR": {
        "roles": ["HR Manager", "HR User"],
        "cards": [
            {"card_name": "Employees", "links": [
                {"type": "Link", "value": "Employee",    "label": "Employees",    "is_report": 0},
                {"type": "Link", "value": "Department",  "label": "Departments",  "is_report": 0},
                {"type": "Link", "value": "Designation", "label": "Designations", "is_report": 0},
            ]},
            {"card_name": "User and Access Management", "links": [
                {"type": "Link", "value": "User",     "label": "Users",            "is_report": 0},
                {"type": "Link", "value": "Role",     "label": "Roles",            "is_report": 0},
                {"type": "Link", "value": "Has Role", "label": "Role Assignments", "is_report": 0},
            ]},
        ],
    },
    "Manufacturing": {
        "roles": ["Production Manager", "Manufacturing Manager", "Manufacturing User"],
        "cards": [
            {"card_name": "Planning", "links": [
                {"type": "Link", "value": "BOM",             "label": "Bill of Materials (BOM)", "is_report": 0},
                {"type": "Link", "value": "Production Plan", "label": "Production Plans",        "is_report": 0},
                {"type": "Link", "value": "Work Order",      "label": "Work Orders",             "is_report": 0},
                {"type": "Link", "value": "Job Card",        "label": "Job Cards",               "is_report": 0},
            ]},
            {"card_name": "Assembly Setup", "links": [
                {"type": "Link", "value": "Workstation",   "label": "Workstations",   "is_report": 0},
                {"type": "Link", "value": "Operation",     "label": "Operations",     "is_report": 0},
                {"type": "Link", "value": "Routing",       "label": "Routings",       "is_report": 0},
                {"type": "Link", "value": "Vehicle Model", "label": "Vehicle Models", "is_report": 0},
            ]},
            {"card_name": "Reports", "links": [
                {"type": "Link", "value": "Work Order Summary",      "label": "Work Order Summary",  "is_report": 1},
                {"type": "Link", "value": "Production Planning Report", "label": "Production Planning", "is_report": 1},
            ]},
        ],
    },
    "Stock": {
        "roles": ["Storekeeper", "Stock Manager", "Stock User", "Item Manager"],
        "cards": [
            {"card_name": "Items and Warehouses", "links": [
                {"type": "Link", "value": "Item",      "label": "Items",             "is_report": 0},
                {"type": "Link", "value": "Item Group","label": "Item Groups",       "is_report": 0},
                {"type": "Link", "value": "Warehouse", "label": "Warehouses",        "is_report": 0},
                {"type": "Link", "value": "UOM",       "label": "Units of Measure",  "is_report": 0},
            ]},
            {"card_name": "Stock Transactions", "links": [
                {"type": "Link", "value": "Stock Entry",          "label": "Stock Entries",         "is_report": 0},
                {"type": "Link", "value": "Purchase Receipt",     "label": "Purchase Receipts",     "is_report": 0},
                {"type": "Link", "value": "Delivery Note",        "label": "Delivery Notes",        "is_report": 0},
                {"type": "Link", "value": "Stock Reconciliation", "label": "Stock Reconciliation",  "is_report": 0},
            ]},
            {"card_name": "Reports", "links": [
                {"type": "Link", "value": "Stock Balance", "label": "Stock Balance", "is_report": 1},
                {"type": "Link", "value": "Stock Ledger",  "label": "Stock Ledger",  "is_report": 1},
            ]},
        ],
    },
    "Floor User (Workers)": {
        "roles": ["Floor Worker", "Manufacturing User"],
        "cards": [
            {"card_name": "My Work", "links": [
                {"type": "Link", "value": "Job Card",   "label": "My Job Cards",           "is_report": 0},
                {"type": "Link", "value": "Work Order", "label": "Work Orders (View Only)","is_report": 0},
            ]},
            {"card_name": "Report Issues", "links": [
                {"type": "Link", "value": "Non Conformance", "label": "Report Quality Issue or Defect", "is_report": 0},
            ]},
        ],
    },
    "Delivery": {
        "roles": ["Delivery Officer", "Delivery Manager", "Delivery User"],
        "cards": [
            {"card_name": "Dispatch", "links": [
                {"type": "Link", "value": "Delivery Note", "label": "Delivery Notes",    "is_report": 0},
                {"type": "Link", "value": "Delivery Trip", "label": "Delivery Trips",    "is_report": 0},
                {"type": "Link", "value": "Sales Order",   "label": "Sales Orders (View)","is_report": 0},
                {"type": "Link", "value": "Packing Slip",  "label": "Packing Slips",     "is_report": 0},
            ]},
            {"card_name": "Finished Vehicles", "links": [
                {"type": "Link", "value": "Finished Vehicle Register", "label": "Finished Vehicle Register", "is_report": 0},
                {"type": "Link", "value": "Serial No",                 "label": "Serial Numbers",           "is_report": 0},
            ]},
            {"card_name": "Reports", "links": [
                {"type": "Link", "value": "Delivery Note Trends", "label": "Delivery Trends", "is_report": 1},
            ]},
        ],
    },
    "Finance": {
        "roles": ["Finance Officer", "Accounts Manager", "Accounts User"],
        "cards": [
            {"card_name": "Invoices", "links": [
                {"type": "Link", "value": "Sales Invoice",    "label": "Sales Invoices",    "is_report": 0},
                {"type": "Link", "value": "Purchase Invoice", "label": "Purchase Invoices", "is_report": 0},
            ]},
            {"card_name": "Payments", "links": [
                {"type": "Link", "value": "Payment Entry",   "label": "Payment Entries",  "is_report": 0},
                {"type": "Link", "value": "Journal Entry",   "label": "Journal Entries",  "is_report": 0},
                {"type": "Link", "value": "Payment Request", "label": "Payment Requests", "is_report": 0},
            ]},
            {"card_name": "Accounting", "links": [
                {"type": "Link", "value": "Account",      "label": "Accounts",      "is_report": 0},
                {"type": "Link", "value": "Cost Center",  "label": "Cost Centers",  "is_report": 0},
            ]},
            {"card_name": "Reports", "links": [
                {"type": "Link", "value": "Profit and Loss Statement", "label": "Profit and Loss",   "is_report": 1},
                {"type": "Link", "value": "Balance Sheet",             "label": "Balance Sheet",     "is_report": 1},
                {"type": "Link", "value": "Accounts Receivable",       "label": "Accounts Receivable","is_report": 1},
                {"type": "Link", "value": "Accounts Payable",          "label": "Accounts Payable",  "is_report": 1},
            ]},
        ],
    },
    "Quality": {
        "roles": ["Quality Inspector", "Quality Manager"],
        "cards": [
            {"card_name": "Inspections", "links": [
                {"type": "Link", "value": "Quality Inspection",           "label": "Quality Inspections",     "is_report": 0},
                {"type": "Link", "value": "Quality Inspection Template",  "label": "Inspection Templates",    "is_report": 0},
                {"type": "Link", "value": "Quality Inspection Parameter", "label": "Inspection Parameters",   "is_report": 0},
            ]},
            {"card_name": "Defects and Actions", "links": [
                {"type": "Link", "value": "Non Conformance", "label": "Non-Conformances and Defects", "is_report": 0},
                {"type": "Link", "value": "Quality Action",  "label": "Corrective Actions",           "is_report": 0},
                {"type": "Link", "value": "Quality Review",  "label": "Quality Reviews",              "is_report": 0},
            ]},
            {"card_name": "Reports", "links": [
                {"type": "Link", "value": "Quality Inspection Summary", "label": "Inspection Summary", "is_report": 1},
            ]},
        ],
    },
}


def check_link_exists(link_value, is_report):
    """Return True only if the target DocType or Report name exists in the DB."""
    if is_report:
        return bool(frappe.db.exists("Report", link_value))
    else:
        return bool(frappe.db.exists("DocType", link_value))


def rebuild_workspaces():
    print("\n=== Rebuilding 9 Department Workspaces (Fixed Link Types) ===")
    success = []
    failed = []

    for ws_name, ws_def in WORKSPACES.items():
        print("\n  Processing: " + ws_name)

        if frappe.db.exists("Workspace", ws_name):
            ws = frappe.get_doc("Workspace", ws_name)
        else:
            ws = frappe.new_doc("Workspace")
            ws.name = ws_name
            ws.label = ws_name

        ws.label = ws_name
        ws.title = ws_name
        ws.module = ""
        ws.is_hidden = 0
        ws.public = 1
        ws.type = "Workspace"
        ws.hide_custom = 0

        # Roles
        ws.set("roles", [])
        ws.append("roles", {"role": "System Manager"})
        for role in ws_def["roles"]:
            if frappe.db.exists("Role", role):
                ws.append("roles", {"role": role})

        # Links - validate each target before adding
        ws.set("links", [])
        card_idx = 0
        skipped_links = []
        for card in ws_def["cards"]:
            card_idx += 1
            valid_links = []
            for lnk in card["links"]:
                if check_link_exists(lnk["value"], lnk["is_report"]):
                    valid_links.append(lnk)
                else:
                    skipped_links.append(lnk["value"])

            if not valid_links:
                continue

            # Card Break header
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
            for lnk in valid_links:
                link_idx += 1
                ws.append("links", {
                    "type": "Link",
                    "link_to": lnk["value"],
                    "label": lnk["label"],
                    "idx": card_idx * 100 + link_idx,
                    "is_query_report": lnk["is_report"],
                    "dependencies": "",
                    "link_type": "Report" if lnk["is_report"] else "DocType",
                    "onboard": 1 if link_idx <= 2 else 0,
                    "only_for": "",
                    "doc_view": "",
                    "card_type": "Card",
                })

        if skipped_links:
            print("    Skipped missing targets: " + str(skipped_links))

        # Shortcuts (first 6 valid links)
        ws.set("shortcuts", [])
        sidx = 0
        for card in ws_def["cards"]:
            for lnk in card["links"]:
                if sidx >= 6:
                    break
                if not check_link_exists(lnk["value"], lnk["is_report"]):
                    continue
                sidx += 1
                ws.append("shortcuts", {
                    "type": "Link",
                    "link_to": lnk["value"],
                    "label": lnk["label"],
                    "idx": sidx,
                    "is_query_report": lnk["is_report"],
                    "color": "#2490EF",
                    "format": "Card",
                    "doc_view": "",
                })
            if sidx >= 6:
                break

        try:
            ws.save(ignore_permissions=True)
            print("    SAVED: roles=" + str(len(ws.roles)) + " links=" + str(len(ws.links)))
            success.append(ws_name)
        except Exception as e:
            print("    ERROR: " + str(e))
            failed.append(ws_name)

    frappe.db.commit()
    print("\n  Successfully saved: " + str(success))
    if failed:
        print("  FAILED: " + str(failed))
    return success, failed


def hide_other_workspaces():
    print("\n=== Hiding Non-Department Workspaces ===")
    keep = set(WORKSPACES.keys())
    all_ws = frappe.db.sql("SELECT name FROM tabWorkspace", as_dict=True)
    count = 0
    for row in all_ws:
        name = row["name"]
        if name in keep:
            continue
        try:
            ws = frappe.get_doc("Workspace", name)
            if not ws.type:
                ws.type = "Workspace"
            ws.is_hidden = 1
            ws.public = 0
            ws.set("roles", [{"role": "System Manager"}])
            ws.save(ignore_permissions=True)
            print("  Hidden: " + name)
            count += 1
        except Exception as e:
            print("  Could not hide " + name + ": " + str(e))
    frappe.db.commit()
    print("  Total hidden: " + str(count))


def validate():
    print("\n=== Validation ===")
    ws_data = frappe.db.sql("SELECT name, is_hidden, public FROM tabWorkspace ORDER BY name", as_dict=True)
    visible = []
    hidden = []
    for w in ws_data:
        if (not w["is_hidden"]) and w["public"]:
            visible.append(w["name"])
        else:
            hidden.append(w["name"])

    print("\n  VISIBLE workspaces (" + str(len(visible)) + "):")
    for v in visible:
        flag = " <-- EXPECTED" if v in WORKSPACES else " <-- UNEXPECTED"
        print("    VISIBLE: " + v + flag)

    missing = [ws for ws in WORKSPACES if ws not in visible]
    if missing:
        print("\n  MISSING from visible: " + str(missing))
    else:
        print("\n  All 9 department workspaces are visible.")

    print("\n  Hidden workspaces (" + str(len(hidden)) + "): " + str(hidden))
    return visible, hidden


def run():
    print("=" * 70)
    print("  STEP 14b: FIX WORKSPACE LINK TYPES")
    print("=" * 70)
    success, failed = rebuild_workspaces()
    hide_other_workspaces()
    visible, hidden = validate()
    frappe.clear_cache()
    print("\n" + "=" * 70)
    print("  STEP 14b COMPLETE")
    print("  Workspaces saved OK: " + str(len(success)))
    print("  Workspaces failed:   " + str(len(failed)))
    print("  Visible in UI:       " + str(len(visible)))
    print("=" * 70)
    return "Step 14b - Fix Workspaces: DONE (" + str(len(success)) + "/9 saved)"

if __name__ == '__main__':
    frappe.init(site='frontend', sites_path='/home/frappe/frappe-bench/sites')
    frappe.connect()
    run()
    frappe.destroy()
