hooks_path = "/home/frappe/frappe-bench/apps/erpnext/erpnext/hooks.py"
with open(hooks_path, "r", encoding="utf-8") as f:
    content = f.read()

target = '"validate": "erpnext.setup.doctype.employee.employee.validate_employee_role",'
replacement = '"validate": [\n\t\t\t"erpnext.setup.doctype.employee.employee.validate_employee_role",\n\t\t\t"erpnext.orbis_security.validate_user_roles",\n\t\t],'

if target in content:
    content = content.replace(target, replacement, 1)
    with open(hooks_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("Successfully added validate_user_roles to User validate list in hooks.py")
elif "erpnext.orbis_security.validate_user_roles" in content:
    print("validate_user_roles already present")
else:
    print("Target not found")
