"""Quick DB inspection script."""
import frappe

def run():
    lines = []

    ws = frappe.db.sql('SELECT name, is_hidden, public FROM tabWorkspace ORDER BY name', as_dict=True)
    lines.append('=== WORKSPACES ===')
    for w in ws:
        lines.append(f"  {w['name']} | hidden={w['is_hidden']} | public={w['public']}")

    roles = frappe.db.sql('SELECT name, desk_access FROM tabRole ORDER BY name', as_dict=True)
    lines.append('\n=== ROLES ===')
    for r in roles:
        lines.append(f"  {r['name']} | desk_access={r['desk_access']}")

    cdp_tbl = 'tabCustom DocPerm'
    cdp = frappe.db.sql(f'SELECT COUNT(*) as cnt FROM `{cdp_tbl}`', as_dict=True)
    lines.append(f"\n=== Custom DocPerm count: {cdp[0]['cnt']} ===")

    users = frappe.db.sql('SELECT name, enabled FROM tabUser ORDER BY name', as_dict=True)
    lines.append('\n=== USERS ===')
    for u in users:
        lines.append(f"  {u['name']} | enabled={u['enabled']}")

    result = '\n'.join(lines)
    print(result)
    return result

if __name__ == '__main__':
    frappe.init(site='frontend', sites_path='/home/frappe/frappe-bench/sites')
    frappe.connect()
    run()
    frappe.destroy()

