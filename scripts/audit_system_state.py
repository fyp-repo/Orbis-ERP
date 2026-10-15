# Audit script for OrbisERP System State
import frappe

def run():
    print("=" * 80)
    print("  ORBIS ERP - DEEP AUDIT OF SYSTEM STATE")
    print("=" * 80)

    # 1. Users and Assigned Roles
    print("\n[1] Active Users & Roles:")
    users = frappe.get_all("User", filters={"enabled": 1}, fields=["name", "email", "first_name", "last_name"])
    for u in users:
        if u["name"] == "Guest":
            continue
        roles = [r.role for r in frappe.get_all("Has Role", filters={"parent": u["name"]}, fields=["role"])]
        roles = [r for r in roles if r not in ["All", "Guest"]]
        print(f"  User: {u['name']:<35} Roles ({len(roles)}): {roles[:5]}")

    # 2. Workspaces
    print("\n[2] All Workspaces in tabWorkspace:")
    ws_list = frappe.get_all("Workspace", fields=["name", "title", "is_hidden", "public", "module", "sequence_id"], order_by="sequence_id asc, name asc")
    for w in ws_list:
        roles = [r.role for r in frappe.get_all("Has Role", filters={"parent": w["name"], "parenttype": "Workspace"}, fields=["role"])]
        print(f"  {w['name']:<25} | hidden={w['is_hidden']} | public={w['public']} | seq={w['sequence_id']} | roles={roles}")

    # 3. Desktop Icons
    print("\n[3] Desktop Icons:")
    di_list = frappe.get_all("Desktop Icon", fields=["name", "label", "hidden", "app", "sidebar"], order_by="name asc")
    for d in di_list:
        print(f"  {d['name']:<25} | hidden={d['hidden']} | app={d['app']} | sidebar={d['sidebar']}")

    # 4. Employees & Linked Users
    print("\n[4] Employees & Linked Users:")
    emp_count = frappe.db.count("Employee")
    print(f"  Total Employees in DB: {emp_count}")
    if emp_count > 0:
        employees = frappe.get_all("Employee", fields=["name", "employee_name", "user_id", "department", "designation", "status"])
        for e in employees:
            print(f"  Employee: {e.name:<15} Name: {e.employee_name:<20} User: {str(e.user_id):<30} Dept: {str(e.department):<20} Desig: {str(e.designation)}")

    # 5. Branding / System Settings
    print("\n[5] System Settings & Branding:")
    sys_settings = frappe.get_single("System Settings")
    web_settings = frappe.get_single("Website Settings")
    print(f"  System Settings app_name: {getattr(sys_settings, 'app_name', 'N/A')}")
    print(f"  Website Settings app_name: {getattr(web_settings, 'app_name', 'N/A')}")
    print(f"  Website Settings app_logo: {getattr(web_settings, 'app_logo', 'N/A')}")
    print(f"  Website Settings banner_image: {getattr(web_settings, 'banner_image', 'N/A')}")

    print("\n" + "=" * 80)
    print("  AUDIT COMPLETED")
    print("=" * 80)

if __name__ == "__main__":
    frappe.init(site="frontend", sites_path="/home/frappe/frappe-bench/sites")
    frappe.connect()
    run()
    frappe.destroy()
