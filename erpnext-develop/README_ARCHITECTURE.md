# ERPNext (Develop Branch / v17) — Complete Architecture & Developer Guide

Welcome to the comprehensive technical documentation and guide for **ERPNext** (Develop Branch). This repository contains the source code for the world's leading open-source Enterprise Resource Planning (ERP) platform, built on top of the **Frappe Framework**.

---

## 📑 Table of Contents
1. [Overview & What ERPNext Is](#-overview--what-erpnext-is)
2. [High-Level Architecture & How It Works](#-high-level-architecture--how-it-works)
3. [Complete Folder Structure](#-complete-folder-structure)
4. [File & Directory Breakdown](#-file--directory-breakdown)
   - [Root Configuration Files](#root-configuration-files)
   - [The Modern Banking Frontend (`banking/`)](#the-modern-banking-frontend-banking)
   - [ERPNext Core Python Package (`erpnext/`)](#erpnext-core-python-package-erpnext)
   - [All 39 Functional & Core Modules](#all-39-functional--core-modules)
   - [DocType Internal Anatomy](#doctype-internal-anatomy)
5. [How to Run ERPNext](#-how-to-run-erpnext)
   - [Prerequisites & System Requirements](#prerequisites--system-requirements)
   - [Method 1: Docker (Fastest & Windows-Friendly)](#method-1-docker-quickest-and-recommended-for-windows)
   - [Method 2: Frappe Bench on WSL2 / Linux (Full Development)](#method-2-frappe-bench-on-wsl2--linux-native-dev)
   - [Method 3: Running the Banking React/Vite SPA](#method-3-running-the-banking-reactvite-spa)
6. [Essential Bench Commands Reference](#-essential-bench-commands-reference)

---

## 🌟 Overview & What ERPNext Is

**ERPNext** is a 100% open-source, full-featured enterprise management system designed for businesses of all scales. It encompasses:
- **Financial Accounting & Double-Entry Bookkeeping**
- **Inventory & Warehouse Management (Stock)**
- **Sales & Customer Relationship Management (CRM)**
- **Procurement & Purchase Cycle (Buying)**
- **Manufacturing & Material Requirement Planning (MRP)**
- **Subcontracting & Quality Control**
- **Asset Lifecycle Management**
- **Project Tracking & Timesheets**
- **Point of Sale (POS), Telephony, and Third-Party Integrations**
- **Modern Banking SPA (React 19, Vite, Tailwind CSS)**

---

## 🏗 High-Level Architecture & How It Works

ERPNext is not a traditional standalone Django, Flask, or Express app where you run `python app.py`. Instead, it is an **application module built on the Frappe Framework**.

```
┌─────────────────────────────────────────────────────────────────┐
│                     Client Layer / Browsers                     │
│  ┌────────────────────────┐         ┌────────────────────────┐  │
│  │   Frappe Desk (JS/UI)  │         │   Banking SPA (React)  │  │
│  └───────────┬────────────┘         └───────────┬────────────┘  │
└──────────────┼──────────────────────────────────┼───────────────┘
               │ HTTP / REST / RPC                │
┌──────────────▼──────────────────────────────────▼───────────────┐
│                        Frappe Framework                         │
│  ┌────────────────────┐ ┌───────────────────┐ ┌──────────────┐  │
│  │  DocType Engine    │ │ Event Hooks / Bus │ │ REST API GW  │  │
│  └─────────┬──────────┘ └─────────┬─────────┘ └───────┬──────┘  │
└────────────┼──────────────────────┼───────────────────┼─────────┘
             │                      │                   │
┌────────────▼──────────────────────▼───────────────────▼─────────┐
│                     ERPNext Business Logic                      │
│  ┌────────────┐  ┌────────────┐  ┌─────────────┐  ┌──────────┐  │
│  │  Accounts  │  │   Stock    │  │   Selling   │  │  Buying  │  │
│  └─────┬──────┘  └─────┬──────┘  └──────┬──────┘  └────┬─────┘  │
│        │               │                │              │        │
│  ┌─────▼───────────────▼────────────────▼──────────────▼─────┐  │
│  │    ERPNext Controllers (taxes_and_totals, status_updater) │  │
│  └─────────────────────────────┬─────────────────────────────┘  │
└────────────────────────────────┼────────────────────────────────┘
                                 │
┌────────────────────────────────▼────────────────────────────────┐
│                        Data & Storage                           │
│   ┌───────────────────────────┐   ┌──────────────────────────┐  │
│   │ MariaDB 10.6+ / Postgres  │   │  Redis (Cache & Queues)  │  │
│   └───────────────────────────┘   └──────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

### 1. The DocType (Document Type) Paradigm
In ERPNext, virtually everything is a **DocType** (schema, metadata, model, and view all in one):
- When a DocType is created, Frappe creates a MariaDB/Postgres database table (e.g. `tabSales Invoice`).
- Business logic is written in a Python class inheriting from `frappe.model.document.Document` or ERPNext base controllers (e.g., `AccountsController`).
- Client-side validation, triggers, and UI interactions are handled via Desk JavaScript (`sales_invoice.js`).

### 2. Transaction Flow & Immutable Ledgers
ERPNext enforces GAAP-compliant double-entry accounting and strict inventory valuation:
1. **Draft State (`docstatus = 0`)**: Editable, no financial or stock impact.
2. **Submitted State (`docstatus = 1`)**: Immutable transaction. Generates:
   - **General Ledger Entries (`tabGL Entry`)** for debits and credits.
   - **Stock Ledger Entries (`tabStock Ledger Entry`)** updating FIFO or Moving Average valuations.
   - **Payment Ledgers** tracking outstanding customer and supplier balances.
3. **Cancelled State (`docstatus = 2`)**: Reversal entries are created. Past transactions are never deleted from history.

### 3. Cross-Document Linking & Status Updater
Using controllers like `erpnext/controllers/status_updater.py`, documents synchronize automatically:
- `Material Request` ➔ `Purchase Order` ➔ `Purchase Receipt` ➔ `Purchase Invoice`
- `Quotation` ➔ `Sales Order` ➔ `Delivery Note` ➔ `Sales Invoice` ➔ `Payment Entry`
Quantities, billed amounts, and delivery percentages are automatically recalculated across linked records.

### 4. Background Workers & Reactive Queues
- **Redis Queue (`rq`)**: Long operations (such as bulk inventory valuation reposting, invoice generation, mass emails) run asynchronously across `short`, `default`, and `long` worker queues.
- **Bench Scheduler**: Executes recurring cron tasks defined in `erpnext/hooks.py` (e.g. daily exchange rate syncs, recurring subscriptions, depreciation entries).

---

## 📂 Complete Folder Structure

Below is the directory tree of the repository:

```
erpnext-develop/
├── erpnext-develop/                     # Primary repository root
│   │
│   ├── .github/                         # GitHub configurations and CI/CD pipelines
│   │   ├── helper/                      # CI helper scripts and test setups
│   │   ├── ISSUE_TEMPLATE/              # Bug report and feature request templates
│   │   ├── workflows/                   # GitHub Actions (tests, linters, docker, releases)
│   │   ├── CONTRIBUTING.md              # Community contribution guide
│   │   ├── labeler.yml                  # PR auto-labeling rules
│   │   ├── POSTGRES_COMPATIBILITY.md    # Guide for PostgreSQL database compatibility
│   │   ├── PULL_REQUEST_TEMPLATE.md     # PR checklist template
│   │   ├── release.yml                  # Release workflow definition
│   │   ├── stale.yml                    # Auto-close stale issues/PRs
│   │   └── try-on-f-cloud-button.svg    # Badge asset
│   │
│   ├── .greptile/                       # AI Code Review and Indexing configuration
│   │   └── config.json
│   │
│   ├── banking/                         # Modern React 19 + TypeScript + Vite Banking SPA
│   │   ├── src/                         # React application source code
│   │   │   ├── components/              # UI components (Radix UI, TanStack, Command palette)
│   │   │   ├── hooks/                   # Custom React hooks
│   │   │   ├── lib/                     # Utilities, API client (frappe-react-sdk)
│   │   │   ├── pages/                   # Banking views (Reconciliation, Statements, Rules)
│   │   │   ├── styles/                  # Tailwind CSS styling
│   │   │   └── types/                   # TypeScript interfaces and DocType models
│   │   ├── index.html                   # HTML entry point for the Vite app
│   │   ├── package.json                 # Node dependencies for Banking SPA
│   │   ├── proxyOptions.ts              # Vite reverse proxy configuration to Frappe backend
│   │   ├── tsconfig.json                # TypeScript project configuration
│   │   ├── vite.config.ts               # Vite build and development server config
│   │   └── yarn.lock                    # Locked frontend dependencies
│   │
│   ├── erpnext/                         # Core Python Application Package
│   │   ├── __init__.py                  # Version declaration & app init
│   │   ├── hooks.py                     # Frappe integration hooks (routes, cron, doc_events)
│   │   ├── modules.txt                  # Master list of all registered business modules
│   │   ├── patches.txt                  # Schema & data migration patch sequence
│   │   ├── exceptions.py                # Global ERPNext custom exception classes
│   │   ├── deprecation_dumpster.py      # Backward compatibility adapter for legacy methods
│   │   │
│   │   ├── accounts/                    # General Ledger, Invoicing, Taxes, Currency, Payments
│   │   ├── assets/                      # Fixed Asset Register, Depreciation, Asset Repairs
│   │   ├── bulk_transaction/            # Bulk processing for Sales/Purchase Orders
│   │   ├── buying/                      # Procurement, Purchase Orders, Supplier Quotations
│   │   ├── change_log/                  # Release notes and system change logs
│   │   ├── commands/                    # Custom bench CLI commands for ERPNext
│   │   ├── communication/               # Email and messaging integrations
│   │   ├── config/                      # Module desktop icons and legacy configs
│   │   ├── controllers/                 # Base classes, taxes engine, and status recalculators
│   │   ├── crm/                         # Leads, Opportunities, Campaigns, Newsletters
│   │   ├── desktop_icon/                # Desk workspace icons
│   │   ├── dock/                        # Navigation sidebar and dock configurations
│   │   ├── domains/                     # Domain-specific presets (Services, Manufacturing, Retail)
│   │   ├── edi/                         # Electronic Data Interchange & Code Lists
│   │   ├── erpnext_integrations/        # Plaid, Google Maps, Exotel, Payment Gateways
│   │   ├── gettext/                     # PO/MO translation catalog extraction
│   │   ├── locale/                      # Multi-language translation files
│   │   ├── maintenance/                 # Maintenance Schedules and Support Visits
│   │   ├── manufacturing/               # Bill of Materials (BOM), Work Orders, Job Cards
│   │   ├── patches/                     # Version-by-version database migration scripts
│   │   ├── portal/                      # Customer & Supplier self-service web portal
│   │   ├── projects/                    # Project budgeting, Tasks, Gantt charts, Timesheets
│   │   ├── public/                      # Static web assets (JS bundles, SCSS, icons, sounds)
│   │   ├── quality_management/          # Quality Goals, Procedures, Reviews, Inspections
│   │   ├── regional/                    # Country-specific compliance (UAE, Italy, USA, etc.)
│   │   ├── report_center/               # Centralized analytics & BI dashboard configs
│   │   ├── selling/                     # Sales Orders, Quotations, Customers, Pricing Rules
│   │   ├── setup/                       # Setup Wizard, Company defaults, Chart of Accounts
│   │   ├── shopping_cart/               # Public e-commerce portal and cart logic
│   │   ├── startup/                     # Boot session payload, notifications, filters
│   │   ├── stock/                       # Inventory, Batches, Serials, Warehouses, Stock Entry
│   │   ├── subcontracting/              # Subcontracted purchase & outward material supply
│   │   ├── support/                     # Issue tickets, Service Level Agreements (SLAs)
│   │   ├── telephony/                   # Call logs, Incoming call popups, telephony mediums
│   │   ├── templates/                   # Jinja templates (emails, print formats, web pages)
│   │   ├── tests/                       # Global test runners and mock utilities
│   │   ├── utilities/                   # Transaction helpers, barcode scanning, activations
│   │   ├── workspace_sidebar/           # Desk sidebar navigation structures
│   │   └── www/                         # Public website routes & portal entry points
│   │
│   ├── semgrep/                         # Custom Semgrep static security analysis rules
│   ├── .coderabbit.yml                  # AI Code review bot configuration
│   ├── .editorconfig                    # Text editor indentation and encoding standards
│   ├── .eslintrc                        # JavaScript & Vue linting rules
│   ├── .flake8                          # Python Flake8 linter configuration
│   ├── .git-blame-ignore-revs           # Git revisions ignored during git blame
│   ├── .gitignore                       # Git ignored files pattern list
│   ├── .mergify.yml                     # Mergify automation rules for PRs
│   ├── .pre-commit-config.yaml          # Pre-commit hook definitions (Ruff, ESLint, Prettier)
│   ├── .releaserc                       # Semantic release configuration
│   ├── .semgrepignore                   # Semgrep ignore rules
│   ├── CODEOWNERS                       # GitHub code ownership definition
│   ├── CODE_OF_CONDUCT.md               # Community code of conduct
│   ├── README.md                        # Official GitHub README
│   ├── SECURITY.md                      # Security vulnerability reporting guidelines
│   ├── TRADEMARK_POLICY.md              # Frappe trademark usage guidelines
│   ├── attributions.md                  # Third-party open source attributions
│   ├── babel_extractors.csv             # Babel extraction rules for i18n
│   ├── codecov.yml                      # Code coverage rules
│   ├── commitlint.config.js             # Commit message convention configuration
│   ├── crowdin.yml                      # Crowdin localization integration config
│   ├── license.txt                      # GNU General Public License v3
│   ├── package.json                     # Frontend scripts (`dev`, `build`, `postinstall`)
│   ├── pyproject.toml                   # Python build metadata, dependencies, Ruff rules
│   ├── sider.yml                        # Sider code analyzer config
│   ├── sponsors.md                      # Financial sponsors acknowledgments
│   └── yarn.lock                        # Yarn root lockfile
```

---

## 🔍 File & Directory Breakdown

### Root Configuration Files

| File | Purpose |
| :--- | :--- |
| `pyproject.toml` | **The Core Python Project Definition (PEP 517/621)**. Specifies Python version requirements (`>=3.14`), dependencies (`plaid-python`, `pdfplumber`, `rapidfuzz`, `mt-940`, `holidays`), build system (`flit_core`), and configuration for the **Ruff** linter/formatter. Also defines Bench asset compilation rules. |
| `package.json` | **Root Node.js Configuration**. Maps scripts for the frontend: `"postinstall"`, `"dev": "cd banking && yarn dev"`, and `"build": "cd banking && yarn build"`. |
| `.pre-commit-config.yaml` | Automates code formatting and hygiene before git commits (Ruff, Prettier, ESLint, trailing whitespace, copyright checks). |
| `hooks.py` (in `erpnext/`) | **The Central Nerve Center of ERPNext**. Tells the Frappe framework about all ERPNext hooks, including route rules, DocType event triggers, cron jobs, portal settings, and boot session augmentations. |
| `patches.txt` (in `erpnext/`) | Contains an ordered list of Python migration scripts. When `bench migrate` runs, it executes any newly added patches in sequence to ensure database schemas and existing data migrate cleanly between versions. |
| `modules.txt` (in `erpnext/`) | Lists all 21 core business modules that ERPNext registers with Frappe's module system. |

---

### The Modern Banking Frontend (`banking/`)

Located in `banking/`, this is a decoupled, modern Single-Page Application (SPA) introduced in ERPNext v17:
- **Frameworks**: React 19, TypeScript 5.9, Vite 8, Tailwind CSS v4.
- **State Management**: Jotai (atomic state) and TanStack Virtual/Table for rendering thousands of bank transactions smoothly.
- **Communication**: Uses `frappe-react-sdk` to call Frappe's backend REST APIs and Whitelisted methods.
- **Build Output**: Compiles into `erpnext/public/banking` and embeds its entry point into `erpnext/www/banking.html`.

---

### ERPNext Core Python Package (`erpnext/`)

#### 1. Core Technical Subsystems
- **`controllers/`**: Houses base classes used across the system:
  - `accounts_controller.py`: Validates general ledger entries, exchange rates, payment terms, and invoice tax calculations.
  - `stock_controller.py`: Validates stock movements, serial/batch assignments, and stock ledger entries.
  - `buying_controller.py` & `selling_controller.py`: Base logic for purchasing and sales documents.
  - `taxes_and_totals.py`: Calculation engine for sales/purchase taxes, discounts, shipping rules, and inclusive taxes.
  - `status_updater.py`: Synchronizes status and fulfillment metrics across interconnected parent-child documents.
- **`startup/`**:
  - `boot.py`: Modifies `frappe.boot` data sent to the browser when a user logs in (default company, active currency, user permissions).
  - `notifications.py`: Computes unread counter badges shown in the Frappe Desk navigation bar.
- **`setup/`**: Handles initialization:
  - `setup_wizard/`: The wizard that runs immediately after a site is created to configure company details, fiscal year, and chart of accounts.
  - `install.py`: Database initialization hooks executed when installing the app (`after_install`).
- **`patches/`**: Directory containing hundreds of migration scripts categorized by version (`v11_0`, `v12_0`, `v13_0`, `v14_0`, `v15_0`, `v16_0`, `v17_0`).
- **`public/`**: Static assets served under `/assets/erpnext/`:
  - `js/`: Client scripts bundled into `erpnext.bundle.js` (e.g. POS cashier interface, transaction shortcuts, dialogs).
  - `scss/`: Style source files compiled into CSS.
  - `images/` & `icons/`: Logos, DocType icons, and favicon assets.
- **`www/`**: Public web pages rendered via Frappe's Jinja web engine:
  - `all-products/`, `shop-by-category/`: Public e-commerce product catalogs.
  - `book-appointment/`: Public appointment scheduler.
  - `banking.py` / `banking.html`: Host page for the Banking React application.

---

### All 39 Functional & Core Modules

| Module Directory | Core Functionality & Included DocTypes |
| :--- | :--- |
| **`accounts`** | General Ledger, Chart of Accounts, Sales/Purchase Invoices, Payment Entries, Journal Entries, Bank Reconciliation, Cost Centers, Budgeting, Tax Templates. |
| **`stock`** | Inventory management, Item Master, Warehouses, Stock Entry, Delivery Note, Purchase Receipt, Serial Numbers, Batch Numbers, Landed Cost Vouchers. |
| **`selling`** | Customer Master, Quotations, Sales Orders, Blanket Orders, Pricing Rules, Product Bundles, Customer Groups, Sales Partners. |
| **`buying`** | Supplier Master, Material Requests, Request for Quotation (RFQ), Supplier Quotations, Purchase Orders. |
| **`manufacturing`** | Bill of Materials (BOM), Work Orders, Production Plans, Job Cards, Workstations, Routing, Operations. |
| **`assets`** | Fixed Assets, Asset Depreciation Schedules, Asset Value Adjustments, Asset Maintenance, Asset Scrapping. |
| **`projects`** | Projects, Tasks, Gantt Chart representations, Timesheets, Activity Types, Project Costing & Profitability. |
| **`crm`** | Leads, Opportunities, Customer Campaigns, Email Newsletters, Communication Mediums. |
| **`subcontracting`** | Subcontracting Orders, Subcontracting Inward Receipts, Raw Material Supply Tracking. |
| **`support`** | Customer Support Tickets (Issues), Service Level Agreements (SLAs), Warranty Claims, Issue Types. |
| **`quality_management`**| Quality Goals, Quality Procedures, Quality Inspections, Quality Action Records. |
| **`maintenance`** | Maintenance Visits, Maintenance Schedules, Equipment Warranty Tracking. |
| **`bulk_transaction`** | Background queuing and bulk processing tools for mass-creating or submitting documents. |
| **`telephony`** | Call logs, Incoming call notifications, integration with Exotel/Twilio voice gateways. |
| **`communication`** | Document-level email threads, comments, and unified inbox sync. |
| **`edi`** | Electronic Data Interchange schema mappings, Code Lists, and Common Codes for B2B electronic document exchanges. |
| **`regional`** | Country-specific tax regulations, e-invoicing schemas, and tax reports (e.g. Italy, United States, UAE, South Africa, Australia). |
| **`erpnext_integrations`**| Plaid Bank Feeds, Google Maps distance/matrix calculation, SMS gateways, Payment gateways. |
| **`portal`** | Web Portal for customers/suppliers to view orders, download PDF invoices, and review account balances. |
| **`shopping_cart`** | Online store checkout, pricing rules for web users, payment gateway integration. |
| **`utilities`** | Barcode utilities, dynamic activation helpers, SMS center, quick search tools. |
| **`workspace_sidebar`** | Defines modern Frappe v16/v17 sidebar menus and dock icons for each domain. |
| **`report_center`** | Consolidated financial and analytical report index. |
| **`domains`** | Industry-specific setups (Distribution, Manufacturing, Retail, Services). |

---

### DocType Internal Anatomy

Every folder inside a module's `doctype/` directory (e.g. `erpnext/accounts/doctype/sales_invoice/`) follows a standardized Frappe pattern:

```
sales_invoice/
├── sales_invoice.json          # Schema: field definitions, options, permissions, triggers
├── sales_invoice.py            # Backend Python Class: calculations, validations, hooks
├── sales_invoice.js            # Frontend JavaScript: form events, dynamic field filtering
├── sales_invoice_list.js       # List View script: color indicators, custom buttons
├── sales_invoice_dashboard.py  # Linked Documents: relations to Payments, Delivery Notes
├── test_sales_invoice.py       # Automated unit tests using FrappeTestCase
└── test_records.json           # Fixture data used during testing
```

---

## 🚀 How to Run ERPNext

ERPNext requires a Unix-like environment (Linux or macOS) to run its full backend stack because dependencies like Redis unix sockets, Gunicorn, Python `rq`, and specific system daemons do not natively support Windows directly.

On **Windows**, there are two primary development paths:
1. **Docker Compose** (*Recommended for instant evaluation, demo, or isolated testing*)
2. **WSL2 (Windows Subsystem for Linux)** (*Recommended for full code editing, running unit tests, and active development*)

---

### Prerequisites & System Requirements

- **Memory**: Minimum 4 GB RAM (8 GB+ recommended).
- **Python**: Python 3.12 or 3.14 (develop branch specifies `requires-python = ">=3.14"` or 3.12+ in modern bench environments).
- **Node.js**: Node 20 or 22 LTS, and Yarn (`npm install -g yarn`).
- **Database**: MariaDB 10.6+ (configured with `character-set-server = utf8mb4` and `collation-server = utf8mb4_unicode_ci`) or PostgreSQL 14+.
- **In-Memory Store**: Redis (Redis Server 6+).

---

### Method 1: Docker (Quickest and Recommended for Windows)

The Frappe community maintains official Docker images through [`frappe_docker`](https://github.com/frappe/frappe_docker).

#### Step 1: Install Prerequisites
1. Install [Docker Desktop for Windows](https://docs.docker.com/desktop/install/windows-install/) (ensure WSL2 backend is enabled).

#### Step 2: Clone and Launch Frappe Docker Demo
In PowerShell or your terminal:

```powershell
# Clone the official docker repo
git clone https://github.com/frappe/frappe_docker.git
cd frappe_docker

# Start the quick evaluation stack
docker compose -f pwd.yml up -d
```

#### Step 3: Access ERPNext
- Wait 2–3 minutes while the `create-site` container automatically initializes the MariaDB database, runs migrations, and creates your site.
- Open your browser at: **`http://localhost:8080`**
- **Default Credentials**:
  - **Username**: `Administrator`
  - **Password**: `admin`

---

### Method 2: Frappe Bench on WSL2 / Linux (Native Dev)

To develop, customize, or modify the Python/JS code in this repository directly, use **Frappe Bench** inside WSL2 (Ubuntu 22.04 or 24.04).

#### Step 1: Open WSL2 Terminal
If WSL2 is not installed, open PowerShell as Administrator and run:
```powershell
wsl --install -d Ubuntu
```
Restart your computer if prompted, then open Ubuntu.

#### Step 2: Install System Dependencies in Ubuntu
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y git python3-dev python3-pip python3-venv \
    mariadb-server mariadb-client redis-server \
    curl xvfb libfontconfig wkhtmltopdf

# Install Node.js 20 & Yarn
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt install -y nodejs
sudo npm install -g yarn
```

#### Step 3: Configure MariaDB for Frappe
Edit the MariaDB configuration:
```bash
sudo nano /etc/mysql/mariadb.conf.d/50-server.cnf
```
Add the following lines under the `[mysqld]` section:
```ini
[mysqld]
character-set-client-handshake = FALSE
character-set-server = utf8mb4
collation-server = utf8mb4_unicode_ci

[mysql]
default-character-set = utf8mb4
```
Restart MariaDB:
```bash
sudo service mariadb restart
sudo service redis-server start
```

#### Step 4: Install Frappe Bench CLI
```bash
pip3 install frappe-bench --break-system-packages
```

#### Step 5: Initialize Bench Environment
```bash
# Create a new bench with Frappe Framework (develop or version-16)
bench init --frappe-branch develop frappe-bench
cd frappe-bench
```

#### Step 6: Link or Fetch ERPNext
You can either clone ERPNext from GitHub or link this local folder into your bench:
```bash
# Option A: Get directly via git
bench get-app erpnext --branch develop

# Option B: Use this local repository
# Copy or symlink this folder to: frappe-bench/apps/erpnext
# Then install its dependencies:
bench setup requirements
```

#### Step 7: Create a Site and Install ERPNext
```bash
# 1. Create a new local site
bench new-site erpnext.local --admin-password admin

# 2. Install the ERPNext application onto the site
bench --site erpnext.local install-app erpnext

# 3. Set the site as default
bench use erpnext.local
```

#### Step 8: Start the Bench Server
```bash
bench start
```
- Open your browser at **`http://localhost:8000`**.
- Log in with `Administrator` and your admin password.
- Complete the Setup Wizard to begin using ERPNext.

---

### Method 3: Running the Banking React/Vite SPA

The new Banking module has its own independent development server with Hot Module Replacement (HMR).

1. Navigate to the `banking` directory:
   ```bash
   cd banking
   ```
2. Install frontend dependencies:
   ```bash
   yarn install
   ```
3. Start the Vite development server:
   ```bash
   yarn dev
   ```
   *Note: Ensure your Frappe/ERPNext backend is running on `http://localhost:8000`. The Vite server uses `proxyOptions.ts` to automatically route API calls (`/api/method/...`) to your local ERPNext backend.*
4. Build for production:
   ```bash
   yarn build
   ```
   *This compiles the assets into `erpnext/public/banking` and copies the entry point to `erpnext/www/banking.html`.*

---

## 🛠 Essential Bench Commands Reference

| Command | Action |
| :--- | :--- |
| `bench start` | Boots all local development processes (web server, worker queues, redis, socketio). |
| `bench new-site <site-name>` | Creates a fresh database and site container. |
| `bench --site <site-name> install-app erpnext` | Installs ERPNext and runs initial migrations (`after_install`). |
| `bench --site <site-name> migrate` | Runs new patches from `patches.txt` and synchronizes DocType schemas. |
| `bench --site <site-name> console` | Opens an interactive IPython shell connected to the site database. |
| `bench build` | Compiles JS and CSS bundles for Frappe and ERPNext. |
| `bench --site <site-name> run-tests --app erpnext` | Runs the automated test suite for ERPNext. |
| `bench --site <site-name> reset-perms` | Resets standard DocType user permissions to default. |
| `bench --site <site-name> clear-cache` | Flushes Redis cache and resets session variables. |

---

## 🤝 Community & Support
- **Official Documentation**: [https://docs.erpnext.com](https://docs.erpnext.com)
- **Community Forum**: [https://discuss.frappe.io](https://discuss.frappe.io)
- **Frappe School**: [https://frappe.school](https://frappe.school)
- **Source Code**: [https://github.com/frappe/erpnext](https://github.com/frappe/erpnext)
