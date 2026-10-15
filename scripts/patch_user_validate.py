user_py_path = "/home/frappe/frappe-bench/apps/frappe/frappe/core/doctype/user/user.py"
with open(user_py_path, "r", encoding="utf-8") as f:
    content = f.read()

target = "self.validate_user_image()"
replacement = """self.validate_user_image()
\t\ttry:
\t\t\timport erpnext.orbis_security as sec
\t\t\tsec.validate_user_roles(self)
\t\texcept ImportError:
\t\t\tpass"""

if target in content and "sec.validate_user_roles(self)" not in content:
    content = content.replace(target, replacement, 1)
    with open(user_py_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("User.validate successfully updated with orbis_security check!")
else:
    print("Already updated or target not found.")
