# Audit script for OrbisERP: 8 Departments customization
import frappe

def audit():
    print("=" * 80)
    print("  ORBIS ERP - PHASE 1 AUDIT: 8 DEPARTMENTS & SYSTEM STATUS")
    print("=" * 80)

    # 1. Apps
    print("\n[1] Installed Apps:")
    installed_apps = frappe.get_installed_apps()
    print("   Installed:", installed_apps)

    # 2. Workspaces
    print("\n[2] All Workspaces in tabWorkspace:")
    all_ws = frappe.db.sql("SELECT name, title, is_hidden, public, module FROM tabWorkspace ORDER BY name", as_dict=True)
    visible_ws = []
    hidden_ws = []
    for w in all_ws:
        if (not w["is_hidden"]) and w["public"]:
            visible_ws.append(w["name"])
        else:
            hidden_ws.append(w["name"])
    print(f"   Total workspaces: {len(all_ws)}")
    print(f"   Visible ({len(visible_ws)}): {visible_ws}")
    print(f"   Hidden ({len(hidden_ws)}): {[w for w in hidden_ws[:15]]} ... (truncated)")

    # 3. Check DocTypes for each of the 8 Departments
    departments_doctypes = {
        "Purchase": ["Supplier", "Supplier Group", "Material Request", "Supplier Quotation", "Purchase Order", "Purchase Receipt", "Purchase Invoice"],
        "Selling": ["Customer", "Customer Group", "Quotation", "Sales Order", "Delivery Note", "Sales Invoice"],
        "Manufacturing": ["BOM", "Work Order", "Job Card", "Operation", "Workstation", "Production Plan", "Routing", "Vehicle Model"],
        "Stock": ["Item", "Item Group", "Warehouse", "Stock Entry", "Stock Reconciliation", "UOM", "Batch", "Serial No"],
        "Floor Users (Workers)": ["Job Card", "Work Order", "Issue", "Non Conformance"],
        "Finance": ["Purchase Invoice", "Sales Invoice", "Payment Entry", "Journal Entry", "Account", "Cost Center", "Payment Request"],
        "Projects": ["Project", "Task", "Project Type", "Activity Type", "Timesheet"],
        "HR": ["Employee", "Department", "Designation", "Employment Type", "Branch", "User", "Role", "Has Role"]
    }

    print("\n[3] Checking Essential DocTypes for 8 Departments:")
    for dept, dt_list in departments_doctypes.items():
        print(f"\n   --- Department: {dept} ---")
        for dt in dt_list:
            exists = frappe.db.exists("DocType", dt)
            count = 0
            if exists:
                try:
                    count = frappe.db.count(dt)
                except Exception:
                    count = "N/A"
            print(f"     DocType: {dt:<25} Exists: {bool(exists):<6} Count: {count}")

    # 4. Check Roles
    print("\n[4] Department-Related Roles in System:")
    target_roles = [
        "System Manager", "Administrator",
        "Purchase Officer", "Purchase User", "Purchase Manager",
        "Sales Officer", "Sales User", "Sales Manager",
        "Production Manager", "Manufacturing User", "Manufacturing Manager",
        "Storekeeper", "Stock User", "Stock Manager",
        "Floor Worker",
        "Finance Officer", "Accounts User", "Accounts Manager",
        "Project User", "Projects User", "Projects Manager",
        "HR Manager", "HR User"
    ]
    for r in target_roles:
        exists = frappe.db.exists("Role", r)
        print(f"     Role: {r:<25} Exists: {bool(exists)}")

    # 5. Check Test Users
    print("\n[5] Users & Assigned Roles:")
    users = frappe.db.sql("SELECT name, email, enabled, full_name FROM tabUser WHERE enabled=1 ORDER BY name", as_dict=True)
    for u in users:
        if u["name"] in ["Administrator", "Guest"] or "orbis" in u["name"] or "test" in u["name"]:
            roles = [r.role for r in frappe.get_all("Has Role", filters={"parent": u["name"]}, fields=["role"])]
            print(f"     User: {u['name']:<30} Roles: {roles}")

    # 6. Check Branding / Settings
    print("\n[6] System & Website Settings:")
    try:
        sys_settings = frappe.get_single("System Settings")
        print(f"     System Settings app_name: {getattr(sys_settings, 'app_name', 'N/A')}")
    except Exception as e:
        print(f"     System Settings error: {e}")

    try:
        web_settings = frappe.get_single("Website Settings")
        print(f"     Website Settings app_name: {getattr(web_settings, 'app_name', 'N/A')}")
        print(f"     Website Settings app_logo: {getattr(web_settings, 'app_logo', 'N/A')}")
        print(f"     Website Settings banner_image: {getattr(web_settings, 'banner_image', 'N/A')}")
    except Exception as e:
        print(f"     Website Settings error: {e}")

    # 7. Check Client Scripts & Hooks
    print("\n[7] Custom / Client Scripts:")
    cs_list = frappe.get_all("Client Script", fields=["name", "dt", "enabled"])
    for cs in cs_list:
        print(f"     Client Script: {cs.name} on {cs.dt} (enabled: {cs.enabled})")

    print("\n" + "=" * 80)
    print("  AUDIT COMPLETE")
    print("=" * 80)

if __name__ == "__main__":
    frappe.init(site="frontend", sites_path="/home/frappe/frappe-bench/sites")
    frappe.connect()
    audit()
    frappe.destroy()
