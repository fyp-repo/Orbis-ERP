import os
import sys
import json
import base64
import re
from PIL import Image

def run_branding_setup():
    print("=" * 70)
    print("STARTING OCM BRANDING CONFIGURATION (STEP 9)")
    print("=" * 70)

    import frappe
    frappe.init(site="frontend")
    frappe.connect()

    bench_root = "/home/frappe/frappe-bench"
    site_files_dir = frappe.get_site_path("public", "files")
    os.makedirs(site_files_dir, exist_ok=True)

    src_logo = "/tmp/ocm_source_logo.jpg"
    if not os.path.exists(src_logo):
        print(f"ERROR: Source logo not found at {src_logo}")
        return False

    # -------------------------------------------------------------
    # 1. GENERATE HIGH-QUALITY PNG & SVG ASSETS
    # -------------------------------------------------------------
    print("\n[1/7] Generating high-resolution PNG & SVG assets from provided logo...")
    im = Image.open(src_logo)

    # 1.1 Main Logo (512x512 PNG)
    im_logo = im.copy()
    im_logo.thumbnail((512, 512), Image.Resampling.LANCZOS)
    logo_path = os.path.join(site_files_dir, "ocm_logo.png")
    im_logo.save(logo_path, format="PNG", optimize=True)

    # 1.2 Splash Logo (512x512 PNG)
    splash_path = os.path.join(site_files_dir, "ocm_splash.png")
    im_logo.save(splash_path, format="PNG", optimize=True)

    # 1.3 Favicon (64x64 PNG)
    im_fav = im.copy()
    im_fav.thumbnail((64, 64), Image.Resampling.LANCZOS)
    fav_path = os.path.join(site_files_dir, "ocm_favicon.png")
    im_fav.save(fav_path, format="PNG", optimize=True)

    # 1.4 Sidebar Icon (128x128 PNG)
    im_sb = im.copy()
    im_sb.thumbnail((128, 128), Image.Resampling.LANCZOS)
    sb_path = os.path.join(site_files_dir, "ocm_sidebar_icon.png")
    im_sb.save(sb_path, format="PNG", optimize=True)

    # 1.5 Generate SVG embedding base64-encoded PNG for SVG fallbacks
    with open(logo_path, "rb") as f:
        b64_logo = base64.b64encode(f.read()).decode("utf-8")
    with open(fav_path, "rb") as f:
        b64_fav = base64.b64encode(f.read()).decode("utf-8")

    svg_logo_content = f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 512 512" width="512" height="512">
  <image width="512" height="512" xlink:href="data:image/png;base64,{b64_logo}"/>
</svg>'''

    svg_fav_content = f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 64 64" width="64" height="64">
  <image width="64" height="64" xlink:href="data:image/png;base64,{b64_fav}"/>
</svg>'''

    with open(os.path.join(site_files_dir, "ocm_logo.svg"), "w", encoding="utf-8") as f:
        f.write(svg_logo_content)
    with open(os.path.join(site_files_dir, "ocm_splash.svg"), "w", encoding="utf-8") as f:
        f.write(svg_logo_content)
    with open(os.path.join(site_files_dir, "ocm_favicon.svg"), "w", encoding="utf-8") as f:
        f.write(svg_fav_content)

    # 1.6 Overwrite standard static assets in apps and sites
    static_targets_png = [
        os.path.join(bench_root, "apps/erpnext/erpnext/public/images/erpnext-logo.png"),
        os.path.join(bench_root, "apps/erpnext/erpnext/public/images/erpnext-logo-blue.png"),
        os.path.join(bench_root, "apps/frappe/frappe/public/images/frappe-framework-logo.png"),
        os.path.join(bench_root, "apps/frappe/frappe/public/images/frappe-logo.png"),
    ]
    for p in static_targets_png:
        try:
            os.makedirs(os.path.dirname(p), exist_ok=True)
            im_logo.save(p, format="PNG", optimize=True)
            print(f"  Updated static PNG: {p}")
        except Exception as e:
            print(f"  Note: {p}: {e}")

    static_targets_svg = [
        os.path.join(bench_root, "apps/erpnext/erpnext/public/images/erpnext-logo.svg"),
        os.path.join(bench_root, "apps/frappe/frappe/public/images/frappe-framework-logo.svg"),
        os.path.join(bench_root, "apps/frappe/frappe/public/images/frappe-comp-logo.svg"),
    ]
    for p in static_targets_svg:
        try:
            os.makedirs(os.path.dirname(p), exist_ok=True)
            with open(p, "w", encoding="utf-8") as f:
                f.write(svg_logo_content)
            print(f"  Updated static SVG: {p}")
        except Exception as e:
            print(f"  Note: {p}: {e}")

    static_favicons = [
        os.path.join(bench_root, "apps/erpnext/erpnext/public/images/erpnext-favicon.svg"),
        os.path.join(bench_root, "apps/frappe/frappe/public/images/frappe-favicon.svg"),
    ]
    for p in static_favicons:
        try:
            os.makedirs(os.path.dirname(p), exist_ok=True)
            with open(p, "w", encoding="utf-8") as f:
                f.write(svg_fav_content)
            print(f"  Updated static Favicon: {p}")
        except Exception as e:
            print(f"  Note: {p}: {e}")

    print("  All logo image assets created successfully.")

    # -------------------------------------------------------------
    # 2. UPDATE DATABASE SETTINGS (System, Website, Navbar)
    # -------------------------------------------------------------
    print("\n[2/7] Updating Database Settings...")

    # 2.1 System Settings
    sys_settings = frappe.get_single("System Settings")
    sys_settings.app_name = "OCM | OrbisERP"
    sys_settings.save(ignore_permissions=True)

    # 2.2 Website Settings
    if frappe.db.exists("DocType", "Website Settings"):
        web_settings = frappe.get_single("Website Settings")
        web_settings.app_name = "OCM | OrbisERP"
        web_settings.app_logo = "/files/ocm_logo.png"
        web_settings.banner_image = "/files/ocm_logo.png"
        web_settings.favicon = "/files/ocm_favicon.png"
        web_settings.splash_image = "/files/ocm_splash.png"
        web_settings.brand_html = "<b>OCM</b>"
        web_settings.copyright = "© 2026 Orbis Car Manufacturing (Pvt.) Ltd. (OCM)"
        web_settings.save(ignore_permissions=True)

    # 2.3 Navbar Settings
    if frappe.db.exists("DocType", "Navbar Settings"):
        navbar = frappe.get_single("Navbar Settings")
        navbar.app_logo = "/files/ocm_logo.png"
        navbar.save(ignore_permissions=True)

    # 2.4 ERPNext Settings Workspace title
    if frappe.db.exists("Workspace", "ERPNext Settings"):
        es_ws = frappe.get_doc("Workspace", "ERPNext Settings")
        es_ws.title = "OCM System Settings"
        es_ws.label = "OCM System Settings"
        es_ws.save(ignore_permissions=True)

    frappe.db.commit()
    print("  Database Settings saved: app_name='OCM | OrbisERP', app_logo='/files/ocm_logo.png'.")

    # -------------------------------------------------------------
    # 3. UPDATE SPLASH SCREEN & LOGIN TEMPLATES
    # -------------------------------------------------------------
    print("\n[3/7] Updating Splash Screen and Login Screen Templates...")

    # 3.1 Splash screen HTML
    splash_template = os.path.join(bench_root, "apps/frappe/frappe/templates/includes/splash_screen.html")
    if os.path.exists(splash_template):
        splash_html = """<div class="centered splash">
	<img src="{{ splash_image or '/files/ocm_splash.png' }}"
		style="width: auto; max-width: 220px; filter: drop-shadow(0 0 25px rgba(0, 195, 255, 0.45));">
</div>
"""
        with open(splash_template, "w", encoding="utf-8") as f:
            f.write(splash_html)
        print("  Updated splash_screen.html with glowing OCM logo.")

    # 3.2 Login template
    login_py = os.path.join(bench_root, "apps/frappe/frappe/www/login.py")
    if os.path.exists(login_py):
        with open(login_py, "r", encoding="utf-8") as f:
            l_code = f.read()
        l_code = l_code.replace('context["logo"] = get_app_logo()', 'context["logo"] = "/files/ocm_logo.png"')
        with open(login_py, "w", encoding="utf-8") as f:
            f.write(l_code)
        print("  Updated login.py to serve '/files/ocm_logo.png'.")

    # 3.3 Desk HTML
    desk_html = os.path.join(bench_root, "apps/frappe/frappe/www/desk.html")
    if os.path.exists(desk_html):
        with open(desk_html, "r", encoding="utf-8") as f:
            d_code = f.read()
        d_code = d_code.replace(
            'href="{{ favicon or "/assets/frappe/images/frappe-favicon.svg" }}"',
            'href="{{ favicon or "/files/ocm_favicon.png" }}"'
        )
        with open(desk_html, "w", encoding="utf-8") as f:
            f.write(d_code)
        print("  Updated desk.html favicon reference.")

    # -------------------------------------------------------------
    # 4. HOOKS.PY AND STARTUP/BOOT.PY ENFORCEMENT
    # -------------------------------------------------------------
    print("\n[4/7] Updating hooks.py and startup/boot.py...")

    hooks_file = os.path.join(bench_root, "apps/erpnext/erpnext/hooks.py")
    if os.path.exists(hooks_file):
        with open(hooks_file, "r", encoding="utf-8") as f:
            content = f.read()

        content = content.replace('app_title = "ERPNext"', 'app_title = "OCM"')
        content = content.replace('app_logo_url = "/assets/erpnext/images/erpnext-logo.svg"', 'app_logo_url = "/files/ocm_logo.png"')
        content = content.replace('app_logo_url = "/files/ocm_logo.svg"', 'app_logo_url = "/files/ocm_logo.png"')
        content = content.replace('"favicon": "/assets/erpnext/images/erpnext-favicon.svg"', '"favicon": "/files/ocm_favicon.png"')
        content = content.replace('"favicon": "/files/ocm_favicon.svg"', '"favicon": "/files/ocm_favicon.png"')
        content = content.replace('"splash_image": "/assets/erpnext/images/erpnext-logo.svg"', '"splash_image": "/files/ocm_splash.png"')
        content = content.replace('"splash_image": "/files/ocm_splash.svg"', '"splash_image": "/files/ocm_splash.png"')

        # Ensure our custom ocm_branding.js and ocm_branding.css are registered in app_include_js / css
        if 'ocm_branding.js' not in content:
            content = content.replace(
                'app_include_js = "erpnext.bundle.js"',
                'app_include_js = ["erpnext.bundle.js", "/assets/erpnext/js/ocm_branding.js"]'
            )
        if 'ocm_branding.css' not in content:
            content = content.replace(
                'app_include_css = "erpnext.bundle.css"',
                'app_include_css = ["erpnext.bundle.css", "/assets/erpnext/css/ocm_branding.css"]'
            )

        with open(hooks_file, "w", encoding="utf-8") as f:
            f.write(content)
        print("  Updated apps/erpnext/erpnext/hooks.py.")

    boot_file = os.path.join(bench_root, "apps/erpnext/erpnext/startup/boot.py")
    if os.path.exists(boot_file):
        with open(boot_file, "r", encoding="utf-8") as f:
            boot_code = f.read()

        # Update ocm_boot_session definition
        target_ocm_boot = """
def ocm_boot_session(bootinfo):
	\"\"\"Enforce OCM branding, logo, and role-based workspace/sidebar isolation.\"\"\"
	bootinfo.sysdefaults["app_name"] = "OCM | OrbisERP"
	if "navbar_settings" in bootinfo:
		bootinfo.navbar_settings.app_logo = "/files/ocm_logo.png"

	for app in bootinfo.get("app_data", []):
		app["app_title"] = "OCM"
		app["app_logo_url"] = "/files/ocm_logo.png"

	for icon in bootinfo.get("desktop_icons", []):
		if icon.get("parent_icon") in ["ERPNext", "erpnext", None, ""]:
			icon["parent_icon"] = "OCM"
		if icon.get("label") == "ERPNext":
			icon["label"] = "OCM"
		icon["logo_url"] = "/files/ocm_logo.png"

	for k, v in bootinfo.get("workspace_sidebar_item", {}).items():
		if isinstance(v, dict):
			v["app"] = "OCM"
			v["header_icon"] = "/files/ocm_logo.png"

	user = frappe.session.user
	if not user or user in ["Guest", "Administrator"] or "System Manager" in frappe.get_roles(user):
		return

	user_roles = set(frappe.get_roles(user))
	role_map = {
		"Sales Manager": {
			"workspaces": ["OCM Sales"],
			"sidebars": ["selling", "crm", "ocm sales"]
		},
		"Purchase Manager": {
			"workspaces": ["OCM Purchasing"],
			"sidebars": ["buying", "ocm purchasing"]
		},
		"Stock Manager": {
			"workspaces": ["OCM Inventory"],
			"sidebars": ["stock", "ocm inventory"]
		},
		"Manufacturing Manager": {
			"workspaces": ["OCM Manufacturing"],
			"sidebars": ["manufacturing", "ocm manufacturing"]
		},
		"Shop Floor User": {
			"workspaces": ["OCM Production"],
			"sidebars": ["ocm production"]
		},
		"Quality Manager": {
			"workspaces": ["OCM Quality"],
			"sidebars": ["quality", "quality management", "ocm quality"]
		},
		"Delivery Manager": {
			"workspaces": ["OCM Delivery"],
			"sidebars": ["delivery", "selling", "ocm delivery"]
		},
		"Accounts Manager": {
			"workspaces": ["OCM Accounts"],
			"sidebars": ["accounts", "accounting", "invoicing", "payments", "financial reports", "ocm accounts"]
		},
		"HR Manager": {
			"workspaces": ["OCM Human Resources"],
			"sidebars": ["human resources", "ocm human resources"]
		}
	}

	allowed_ws = set()
	allowed_sb = set()
	for r, conf in role_map.items():
		if r in user_roles:
			allowed_ws.update(conf["workspaces"])
			allowed_sb.update(conf["sidebars"])

	if not allowed_ws:
		return

	if "workspaces" in bootinfo and "pages" in bootinfo["workspaces"]:
		bootinfo["workspaces"]["pages"] = [
			w for w in bootinfo["workspaces"]["pages"]
			if w.get("name") in allowed_ws
		]

	if "workspace_sidebar_item" in bootinfo:
		bootinfo["workspace_sidebar_item"] = {
			k: v for k, v in bootinfo["workspace_sidebar_item"].items()
			if k in allowed_sb
		}

	if "desktop_icons" in bootinfo:
		bootinfo["desktop_icons"] = [
			icon for icon in bootinfo["desktop_icons"]
			if icon.get("label") in allowed_ws or icon.get("label", "").lower() in allowed_sb
		]
"""
        # If ocm_boot_session already exists, replace it cleanly; otherwise append
        if "def ocm_boot_session(bootinfo):" in boot_code:
            # Cut from def ocm_boot_session to end
            idx = boot_code.find("def ocm_boot_session(bootinfo):")
            boot_code = boot_code[:idx].rstrip() + "\n" + target_ocm_boot
        else:
            boot_code = boot_code.rstrip() + "\n" + target_ocm_boot

        with open(boot_file, "w", encoding="utf-8") as f:
            f.write(boot_code)
        print("  Updated apps/erpnext/erpnext/startup/boot.py with comprehensive OCM bootinfo branding.")

    # -------------------------------------------------------------
    # 5. SIDEBAR TEMPLATES & CLIENT-SIDE DESK BUNDLE PATCHING
    # -------------------------------------------------------------
    print("\n[5/7] Patching Sidebar Templates and Desk Bundle...")

    # 5.1 sidebar_header.html template
    sb_header_html = os.path.join(bench_root, "apps/frappe/frappe/public/js/frappe/ui/sidebar/sidebar_header.html")
    if os.path.exists(sb_header_html):
        new_sb_header = """<a class="sidebar-header" style="text-decoration: none; width: auto;">
<div class="sidebar-item-icon" style="background-color: transparent;">
    <div class="header-logo">
        <img class="ocm-sidebar-logo" src="/files/ocm_logo.png" style="width: 28px; height: 28px; object-fit: contain; border-radius: 6px; box-shadow: 0 0 10px rgba(0, 195, 255, 0.45);">
    </div>
</div>
<div class="title-container">
    <div class="sidebar-item-label header-title" data-name-style="{%=frappe.boot.app_name_style%}">
            {%= __(workspace_title) %}
    </div>
    <div class="sidebar-item-label header-subtitle">
        OCM
    </div>
</div>
<button class="btn-reset drop-icon show-in-edit-mode">
    <svg class="icon icon-sm" style="display: block;margin:auto;" aria-hidden="true">
        <use class="" href="#icon-chevron-down"></use>
    </svg>
</button>
</a>
"""
        with open(sb_header_html, "w", encoding="utf-8") as f:
            f.write(new_sb_header)
        print("  Updated apps/frappe/frappe/public/js/frappe/ui/sidebar/sidebar_header.html.")

    # 5.2 Patch production desk bundle in apps & sites
    desk_bundles = [
        os.path.join(bench_root, "apps/frappe/frappe/public/dist/js/desk.bundle.HAMU7ZDN.js"),
        os.path.join(bench_root, "sites/assets/frappe/dist/js/desk.bundle.HAMU7ZDN.js"),
    ]
    for db_path in desk_bundles:
        if os.path.exists(db_path):
            with open(db_path, "r", encoding="utf-8") as f:
                b_code = f.read()

            # Replace subtitle interpolation
            b_code = b_code.replace(
                "{%= frappe.app.sidebar.header_subtitle %}",
                "OCM"
            )
            # Replace choose_app_name assignments
            b_code = b_code.replace(
                "this.header_subtitle=t.app_title",
                'this.header_subtitle="OCM"'
            )
            b_code = b_code.replace(
                "this.header_subtitle=s",
                'this.header_subtitle="OCM"'
            )
            b_code = b_code.replace(
                "this.header_subtitle=e.parent_icon",
                'this.header_subtitle="OCM"'
            )
            b_code = b_code.replace(
                "this.app_logo_url=t.app_logo_url",
                'this.app_logo_url="/files/ocm_logo.png"'
            )

            with open(db_path, "w", encoding="utf-8") as f:
                f.write(b_code)
            print(f"  Patched production desk bundle: {db_path}")

    # -------------------------------------------------------------
    # 6. CREATE RUNTIME BRANDING SCRIPT & CSS FOR 100% PERSISTENCE
    # -------------------------------------------------------------
    print("\n[6/7] Creating OCM Runtime Script & Premium Automotive CSS...")

    js_dir = os.path.join(bench_root, "apps/erpnext/erpnext/public/js")
    css_dir = os.path.join(bench_root, "apps/erpnext/erpnext/public/css")
    os.makedirs(js_dir, exist_ok=True)
    os.makedirs(css_dir, exist_ok=True)

    ocm_js = """// OCM / OrbisERP Persistent Branding Script
(function() {
    function applyOcmBranding() {
        // 1. Sidebar Header Subtitle
        document.querySelectorAll('.header-subtitle').forEach(function(el) {
            if (el.textContent.trim() !== 'OCM') {
                el.textContent = 'OCM';
            }
        });

        // 2. Sidebar Header Logo
        document.querySelectorAll('.header-logo').forEach(function(el) {
            if (!el.querySelector('img.ocm-sidebar-logo')) {
                el.innerHTML = '<img class="ocm-sidebar-logo" src="/files/ocm_logo.png" alt="OCM">';
            }
        });

        // 3. Navbar Logo & Title
        document.querySelectorAll('.navbar-brand .app-logo, .navbar .app-logo').forEach(function(img) {
            if (img.getAttribute('src') !== '/files/ocm_logo.png') {
                img.setAttribute('src', '/files/ocm_logo.png');
            }
        });
        document.querySelectorAll('.navbar-brand .app-title').forEach(function(el) {
            el.textContent = 'OCM';
        });

        // 4. Override Sidebar prototypes if initialized
        if (window.frappe && frappe.ui && frappe.ui.Sidebar) {
            frappe.ui.Sidebar.prototype.choose_app_name = function() {
                this.header_subtitle = "OCM";
                this.app_logo_url = "/files/ocm_logo.png";
            };
        }
        if (window.frappe && frappe.ui && frappe.ui.SidebarHeader) {
            frappe.ui.SidebarHeader.prototype.set_header_icon = function() {
                this.header_icon = '<img class="ocm-sidebar-logo" src="/files/ocm_logo.png" alt="OCM">';
            };
        }
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', applyOcmBranding);
    } else {
        applyOcmBranding();
    }

    // Interval & Event Listeners
    setInterval(applyOcmBranding, 800);
    window.addEventListener('load', applyOcmBranding);
    if (window.$) {
        $(document).on('page-change', applyOcmBranding);
    }
})();
"""
    with open(os.path.join(js_dir, "ocm_branding.js"), "w", encoding="utf-8") as f:
        f.write(ocm_js)
    print("  Created apps/erpnext/erpnext/public/js/ocm_branding.js.")

    ocm_css = """/* OCM / OrbisERP Futuristic Automotive Branding CSS */
.header-logo .ocm-sidebar-logo,
.ocm-sidebar-logo {
    width: 28px !important;
    height: 28px !important;
    max-width: 28px !important;
    max-height: 28px !important;
    object-fit: contain !important;
    border-radius: 6px !important;
    filter: drop-shadow(0 0 6px rgba(0, 195, 255, 0.5)) !important;
    display: block !important;
}

.header-subtitle {
    font-size: 11px !important;
    font-weight: 700 !important;
    letter-spacing: 1px !important;
    color: #0284C7 !important;
    text-transform: uppercase !important;
}

.sidebar-header .sidebar-item-icon {
    background-color: transparent !important;
}

/* Loading Splash Screen */
.centered.splash img {
    max-width: 220px !important;
    width: auto !important;
    filter: drop-shadow(0 0 30px rgba(0, 195, 255, 0.6)) !important;
    animation: ocm-pulse 2.5s infinite ease-in-out;
}

@keyframes ocm-pulse {
    0% { transform: scale(0.98); filter: drop-shadow(0 0 20px rgba(0, 195, 255, 0.4)); }
    50% { transform: scale(1.02); filter: drop-shadow(0 0 35px rgba(0, 195, 255, 0.75)); }
    100% { transform: scale(0.98); filter: drop-shadow(0 0 20px rgba(0, 195, 255, 0.4)); }
}

/* Login Screen Card */
.page-card-head .app-logo {
    max-height: 85px !important;
    width: auto !important;
    object-fit: contain !important;
    margin: 0 auto 15px auto !important;
    display: block !important;
    filter: drop-shadow(0 0 16px rgba(0, 195, 255, 0.45)) !important;
}

/* Navbar Logo */
.navbar-brand img,
.navbar .app-logo {
    max-height: 28px !important;
    width: auto !important;
    filter: drop-shadow(0 0 6px rgba(0, 195, 255, 0.4)) !important;
}
"""
    with open(os.path.join(css_dir, "ocm_branding.css"), "w", encoding="utf-8") as f:
        f.write(ocm_css)
    print("  Created apps/erpnext/erpnext/public/css/ocm_branding.css.")

    # -------------------------------------------------------------
    # 7. FLUSH BENCH AND SITE CACHES
    # -------------------------------------------------------------
    print("\n[7/7] Clearing site cache and reloading...")
    frappe.clear_cache()
    frappe.destroy()

    print("\n" + "=" * 70)
    print("OCM BRANDING CONFIGURATION COMPLETED SUCCESSFULLY!")
    print("=" * 70)
    return True

if __name__ == "__main__":
    success = run_branding_setup()
    sys.exit(0 if success else 1)
