#!/bin/bash
cd /home/frappe/frappe-bench/sites
/home/frappe/frappe-bench/env/bin/python - << 'EOF'
import sys
sys.path.insert(0, '/home/frappe/frappe-bench/apps/frappe')
sys.path.insert(0, '/home/frappe/frappe-bench/apps/erpnext')
import frappe

frappe.init(site='frontend', sites_path='/home/frappe/frappe-bench/sites')
frappe.connect()

print("=== WORKSPACES ===")
ws = frappe.db.sql("SELECT name, title, is_hidden, public FROM tabWorkspace ORDER BY name", as_dict=True)
for w in ws:
    print(f"  {w['name']:<25} | hidden={w['is_hidden']} | public={w['public']}")

print("\n=== USERS & ROLES ===")
users = frappe.db.sql("SELECT name, first_name FROM tabUser WHERE enabled=1 ORDER BY name", as_dict=True)
for u in users:
    roles = frappe.get_all("Has Role", filters={"parent": u["name"], "parenttype": "User"}, pluck="role")
    filtered_roles = [r for r in roles if r not in ("All", "Guest")]
    print(f"  {u['name']:<35} -> {filtered_roles}")

frappe.destroy()
EOF

