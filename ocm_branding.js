// OCM / OrbisERP Futuristic Automotive Branding & Collapsible Sidebar Script
(function() {
    'use strict';

    function isCollapsed() {
        if (window.frappe && frappe.app && frappe.app.sidebar) {
            return !frappe.app.sidebar.sidebar_expanded;
        }
        return localStorage.getItem('sidebar-expanded') === 'false';
    }

    function syncSidebarClasses(expanded) {
        if (expanded) {
            document.body.classList.remove('ocm-sidebar-collapsed');
            document.body.classList.add('ocm-sidebar-expanded');
            const btn = document.querySelector('.ocm-header-toggle-btn svg');
            if (btn) btn.style.transform = 'rotate(0deg)';
        } else {
            document.body.classList.add('ocm-sidebar-collapsed');
            document.body.classList.remove('ocm-sidebar-expanded');
            const btn = document.querySelector('.ocm-header-toggle-btn svg');
            if (btn) btn.style.transform = 'rotate(180deg)';
        }
    }

    function toggleSidebar(e) {
        if (e) {
            e.preventDefault();
            e.stopPropagation();
        }
        if (window.frappe && frappe.app && frappe.app.sidebar) {
            frappe.app.sidebar.toggle_width();
            syncSidebarClasses(frappe.app.sidebar.sidebar_expanded);
        }
    }

    function setupSidebarHeader() {
        const header = document.querySelector('.sidebar-header');
        if (!header) return;

        // Ensure circular OCM logo
        const logoImg = header.querySelector('.ocm-sidebar-logo');
        if (!logoImg) {
            const logoContainer = header.querySelector('.header-logo');
            if (logoContainer) {
                logoContainer.innerHTML = '<img class="ocm-sidebar-logo" src="/files/ocm_logo_circular.png" alt="OCM">';
            }
        } else if (logoImg.getAttribute('src') !== '/files/ocm_logo_circular.png') {
            logoImg.setAttribute('src', '/files/ocm_logo_circular.png');
        }

        // Subtitle OCM
        const subtitle = header.querySelector('.header-subtitle');
        if (subtitle && subtitle.textContent.trim() !== 'OCM') {
            subtitle.textContent = 'OCM';
        }

        // Add header collapse toggle button if missing
        if (!header.querySelector('.ocm-header-toggle-btn')) {
            const toggleBtn = document.createElement('div');
            toggleBtn.className = 'ocm-header-toggle-btn';
            toggleBtn.setAttribute('title', 'Toggle Sidebar');
            toggleBtn.setAttribute('aria-label', 'Toggle Sidebar');
            toggleBtn.innerHTML = `
                <svg viewBox="0 0 24 24" width="16" height="16" stroke="currentColor" stroke-width="2.5" fill="none" stroke-linecap="round" stroke-linejoin="round">
                    <polyline points="11 17 6 12 11 7"></polyline>
                    <polyline points="18 17 13 12 18 7"></polyline>
                </svg>
            `;
            const titleContainer = header.querySelector('.title-container');
            if (titleContainer) {
                titleContainer.after(toggleBtn);
            } else {
                header.appendChild(toggleBtn);
            }
        }

        // Bind click event once
        if (!header.dataset.ocmBound) {
            header.dataset.ocmBound = 'true';
            header.addEventListener('click', function(e) {
                // If clicking app switcher dropdown items, let default work
                if (e.target.closest('.sidebar-header-menu, .dropdown-menu-item')) {
                    return;
                }

                // If currently collapsed, clicking anywhere on header expands it
                if (isCollapsed()) {
                    toggleSidebar(e);
                    return;
                }

                // If currently expanded, clicking logo, icon, or toggle button collapses it
                if (e.target.closest('.sidebar-item-icon, .header-logo, .ocm-sidebar-logo, .ocm-header-toggle-btn')) {
                    toggleSidebar(e);
                    return;
                }
            });
        }
    }

    function applyOcmBranding() {
        setupSidebarHeader();

        // Navbar logo & title
        document.querySelectorAll('.navbar-brand .app-logo, .navbar .app-logo').forEach(function(img) {
            if (img.getAttribute('src') !== '/files/ocm_logo_circular.png') {
                img.setAttribute('src', '/files/ocm_logo_circular.png');
            }
        });
        document.querySelectorAll('.navbar-brand .app-title').forEach(function(el) {
            if (el.textContent.trim() !== 'OCM') {
                el.textContent = 'OCM';
            }
        });

        // Sync initial sidebar state
        const savedExpanded = localStorage.getItem('sidebar-expanded');
        if (savedExpanded !== null) {
            syncSidebarClasses(savedExpanded !== 'false');
        } else if (window.frappe && frappe.app && frappe.app.sidebar) {
            syncSidebarClasses(frappe.app.sidebar.sidebar_expanded);
        }
    }

    // Event listeners
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', applyOcmBranding);
    } else {
        applyOcmBranding();
    }

    window.addEventListener('load', applyOcmBranding);
    setInterval(applyOcmBranding, 1000);

    if (window.$) {
        $(document).on('sidebar-expand', function(e, data) {
            syncSidebarClasses(data.sidebar_expand);
        });
        $(document).on('page-change', function() {
            setTimeout(applyOcmBranding, 150);
        });
    }
})();
