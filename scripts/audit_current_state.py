"""
Audit current OrbisERP system state - workspaces, users, roles, branding
"""
import frappe


def run():
    print("=" * 80)
    print("  ORBIS ERP - CURRENT SYSTEM STATE AUDIT")
    print("=" * 80)

    # 1. Workspaces
    print("\n[1] All Workspaces:")
    ws_list = frappe.db.sql(
        "SELECT name, title, is_hidden, public, sequence_id FROM tabWorkspace ORDER BY sequence_id, name",
        as_dict=True
    )
    for w in ws_list:
        roles = frappe.db.sql(
            "SELECT role FROM `tabHas Role` WHERE parent=%s AND parenttype='Workspace'",
            w["name"], as_dict=True
        )
        role_names = [r["role"] for r in roles]
        print(f"  [{w['name']}] hidden={w['is_hidden']} public={w['public']} seq={w['sequence_id']} roles={role_names}")

    # 2. Users
    print("\n[2] Active Users & Roles:")
    users = frappe.get_all("User", filters={"enabled": 1}, fields=["name", "email", "first_name"])
    for u in users:
        if u["name"] in ("Guest",):
            continue
        roles = frappe.db.sql(
            "SELECT role FROM `tabHas Role` WHERE parent=%s AND parenttype='User'",
            u["name"], as_dict=True
        )
        role_names = [r["role"] for r in roles if r["role"] not in ("All", "Guest")]
        print(f"  {u['name']:<40} roles={role_names}")

    # 3. Custom DocPerms count
    print("\n[3] Custom DocPerms:")
    cdp_count = frappe.db.count("Custom DocPerm")
    print(f"  Total Custom DocPerm records: {cdp_count}")

    # 4. Branding
    print("\n[4] Branding:")
    try:
        sys_s = frappe.get_single("System Settings")
        print(f"  System Settings app_name: {getattr(sys_s, 'app_name', 'N/A')}")
    except Exception as e:
        print(f"  System Settings error: {e}")
    try:
        web_s = frappe.get_single("Website Settings")
        print(f"  Website Settings app_name: {getattr(web_s, 'app_name', 'N/A')}")
        print(f"  Website Settings favicon: {getattr(web_s, 'favicon', 'N/A')}")
    except Exception as e:
        print(f"  Website Settings error: {e}")

    # 5. Check key DocTypes exist
    print("\n[5] Key DocType Checks:")
    key_doctypes = [
        "Purchase Order", "Purchase Receipt", "Purchase Invoice",
        "Sales Order", "Sales Invoice", "Delivery Note",
        "Work Order", "BOM", "Job Card", "Production Plan",
        "Stock Entry", "Item", "Warehouse",
        "Payment Entry", "Journal Entry", "Account",
        "Project", "Task", "Employee", "Department",
        "Vehicle Model", "Finished Vehicle Register", "Non Conformance",
    ]
    for dt in key_doctypes:
        exists = frappe.db.exists("DocType", dt)
        print(f"  {'[OK]' if exists else '[MISSING]'} {dt}")

    # 6. Check hooks.py for branding patches
    print("\n[6] Checking ERPNext hooks.py for OCM patches:")
    try:
        with open("/home/frappe/frappe-bench/apps/erpnext/erpnext/hooks.py", "r") as f:
            hooks_content = f.read()
        has_ocm_js = "ocm_branding.js" in hooks_content
        has_ocm_css = "ocm_branding.css" in hooks_content
        has_boot_hook = "ocm_boot_session" in hooks_content or "boot_session" in hooks_content
        print(f"  OCM branding JS hook: {'YES' if has_ocm_js else 'NO'}")
        print(f"  OCM branding CSS hook: {'YES' if has_ocm_css else 'NO'}")
        print(f"  Boot session hook: {'YES' if has_boot_hook else 'NO'}")
    except Exception as e:
        print(f"  Could not read hooks.py: {e}")

    # 7. Check client scripts
    print("\n[7] Active Client Scripts:")
    scripts = frappe.get_all("Client Script", filters={"enabled": 1}, fields=["name", "dt", "view"])
    for s in scripts:
        print(f"  {s['name']} | dt={s['dt']} view={s['view']}")

    print("\n" + "=" * 80)
    print("  AUDIT COMPLETE")
    print("=" * 80)


if __name__ == "__main__":
    frappe.init(site="frontend", sites_path="/home/frappe/frappe-bench/sites")
    frappe.connect()
    run()
    frappe.destroy()
