# OrbisERP – Car Manufacturing ERP Setup Report

**Company:** Orbis Car Manufacturing (Pvt.) Ltd.  
**Abbreviation:** OCM  
**Country:** Pakistan  
**Currency:** PKR  
**Industry:** Automobile Manufacturing  
**System/Project Name:** OrbisERP  
**Site URL:** http://localhost:8080  

---

## 1. Executive Summary

The ERPNext instance has been transformed from default/demo data into a realistic, internally consistent automobile manufacturing ERP environment designed for the **Voice-Controlled Secure ERP Final Year Project (FYP)**.

All old demo companies (`OrbisERP`, `OrbisERP (Demo)`), old customers, suppliers, demo users (`heerc838@gmail.com`), demo items, demo warehouses, and transactions were removed cleanly using Frappe/ERPNext supported mechanisms without modifying or truncating core tables.

The Administrator account remains intact and active for system management and troubleshooting.

---

## 2. Organization Structure & Departments

The primary company is **Orbis Car Manufacturing (Pvt.) Ltd.** (`OCM`).

All 10 required departments have been created and assigned:
1. **Sales**
2. **Purchasing**
3. **Inventory / Stock**
4. **Manufacturing / Production**
5. **Shop Floor / Production Operations**
6. **Quality Control**
7. **Delivery / Logistics**
8. **Accounts / Finance**
9. **Human Resources**
10. **System Administration**

---

## 3. Warehouses

Configured under `Orbis Car Manufacturing (Pvt.) Ltd.`:
- **Raw Material Warehouse - OCM**: Stores Steel, Aluminium, Rubber, Glass, Paint, Consumables.
- **Components Warehouse - OCM**: Stores Engines, Batteries, Brakes, Seats, Electrical components, Steering, Suspension.
- **Production Store - OCM**: Materials staged for issue to production lines.
- **Work In Progress Warehouse - OCM**: Active production and partially assembled cars.
- **Quality Hold Warehouse - OCM**: Quarantined items, failed inspections, rework units (contains failed Orbis E1 Electric components).
- **Finished Goods Warehouse - OCM**: Completed, quality-approved automobiles ready for customer delivery.
- **Spare Parts Warehouse - OCM**: Replacement assemblies and service parts.

---

## 4. Exactly 10 Project Users & Credentials

Each project user is configured with a unique email using the common Gmail inbox `forw8007@gmail.com` with `+alias` addresses. Passwords are encrypted using Frappe's native bcrypt hash.

| # | Employee Name | Role | Department | ERPNext Email / User ID | Configured Password |
|---|---------------|------|------------|-------------------------|---------------------|
| 1 | **Ali Khan** | Sales Manager | Sales | `forw8007+salesmanager@gmail.com` | `Orbis@Sales123` |
| 2 | **Ahmed Raza** | Purchase Manager | Purchasing | `forw8007+purchasemanager@gmail.com` | `Orbis@Purchase123` |
| 3 | **Usman Ali** | Stock Manager | Inventory / Stock | `forw8007+stockmanager@gmail.com` | `Orbis@Stock123` |
| 4 | **Hassan Malik** | Manufacturing Manager | Manufacturing / Production | `forw8007+manufacturingmanager@gmail.com` | `Orbis@Manufacturing123` |
| 5 | **Hamza Ahmed** | Shop Floor User | Shop Floor / Production Operations | `forw8007+flooruser1@gmail.com` | `Orbis@Floor123` |
| 6 | **Bilal Khan** | Shop Floor User | Shop Floor / Production Operations | `forw8007+flooruser2@gmail.com` | `Orbis@Floor123` |
| 7 | **Sara Ahmed** | Quality Manager | Quality Control | `forw8007+qualitymanager@gmail.com` | `Orbis@Quality123` |
| 8 | **Usman Shah** | Delivery Manager | Delivery / Logistics | `forw8007+deliverymanager@gmail.com` | `Orbis@Delivery123` |
| 9 | **Ayesha Khan** | Accounts Manager | Accounts / Finance | `forw8007+accountsmanager@gmail.com` | `Orbis@Accounts123` |
| 10 | **Fatima Ali** | HR Manager | Human Resources | `forw8007+hrmanager@gmail.com` | `Orbis@HR123` |

> [!NOTE]
> System Administrator remains separate (`Administrator`) with unrestricted administration privileges. Regular users have strict RBAC without System Manager or Administrator privileges.

---

## 5. Master Data

### 5.1 Item Groups
13 item groups organized hierarchically:
- `Finished Cars`
- `Raw Materials` (`Metals`, `Rubber Components`, `Glass Components`, `Electrical Components`, `Battery Components`, `Consumables`)
- `Manufactured Components` (`Engine Components`, `Interior Components`, `Safety Components`)
- `Spare Parts`

### 5.2 Finished Car Products
1. **Orbis O1 Sedan**: Stock Item, Standard Selling Rate: PKR 6,500,000
2. **Orbis X1 SUV**: Stock Item, Standard Selling Rate: PKR 11,500,000
3. **Orbis E1 Electric**: Stock Item, Standard Selling Rate: PKR 14,000,000

### 5.3 Suppliers (10 Automobile Suppliers)
1. Pakistan Steel Suppliers (Raw Material)
2. Orbis Auto Components (Components)
3. Pak Rubber Industries (Raw Material)
4. National Glass Components (Components)
5. Pak Battery Solutions (Electrical)
6. Auto Electrical Supplies (Electrical)
7. Prime Tyres Pakistan (Components)
8. Industrial Paint Suppliers (Raw Material)
9. Auto Interior Materials (Raw Material)
10. Engineering Components Ltd. (Mechanical)

### 5.4 Customers / Dealers (8 Auto Dealers)
1. Ahmed Motors
2. Karachi Auto Dealers
3. Lahore Motors
4. Islamabad Auto Gallery
5. Pak Wheels Dealership
6. Multan Auto Center
7. Faisalabad Motors
8. Rawalpindi Auto Traders

### 5.5 Workstations & Operations
- **Workstations (9):** Body Assembly Station, Engine Assembly Station, Mechanical Assembly Station, Electrical Assembly Station, Interior Assembly Station, Painting Station, Final Assembly Station, Quality Inspection Station, Testing Station.
- **Operations (18):** Body Assembly, Engine Installation, Transmission Installation, Suspension Installation, Brake Installation, Electrical Installation, Interior Installation, Glass Installation, Wheel Installation, Battery Installation, Painting, Final Assembly, Quality Inspection, Final Testing, Motor Installation, Charging System Installation, Electrical System Testing.

### 5.6 Bills of Materials (BOMs)
All submitted and active:
- `BOM-Orbis O1 Sedan-001` (22 items, 13 operations)
- `BOM-Orbis X1 SUV-001` (22 items, 13 operations)
- `BOM-Orbis E1 Electric-001` (19 items, 14 operations)

---

## 6. Business Workflow & Connected Transactions

The complete cycle demonstrates end-to-end integration:

```text
Material Request
      ↓
Purchase Orders (9 Orders)
      ↓
Purchase Receipts (Raw Materials & Components Stocked)
      ↓
Work Orders (Sedan, SUV, EV)
      ↓
Stock Transfers to WIP
      ↓
Manufacture to Finished Goods
      ↓
Quality Inspections (Passed: Sedan & SUV | Failed: EV -> Quality Hold)
      ↓
Customer Quotation & Sales Order
      ↓
Delivery Notes
      ↓
Sales Invoices
      ↓
Payment Entries (Full GAAP Double-Entry GL Ledger)
```

### Specific Highlights:
- **Work Orders:**
  - `MFG-WO-2026-00001`: 5 × Orbis O1 Sedan (Produced into Finished Goods)
  - `MFG-WO-2026-00002`: 3 × Orbis X1 SUV (Produced into Finished Goods)
  - `MFG-WO-2026-00003`: 2 × Orbis E1 Electric (Transferred to WIP, Quarantined)
- **Quality Inspections:**
  - `MAT-QA-2026-00001` (Orbis O1 Sedan): **Accepted (PASS)**
  - `MAT-QA-2026-00002` (Orbis X1 SUV): **Accepted (PASS)**
  - `MAT-QA-2026-00003` (Orbis E1 Electric): **Rejected (FAIL)** — Reason: *Electrical system issue detected: High voltage BMS communication timeout on bus 2. Quarantined in Quality Hold Warehouse for rework.*
- **Deliveries & Invoices:**
  - Delivery to **Ahmed Motors**: 2 × Orbis O1 Sedan (`MAT-DN-2026-00001`), Invoiced (`ACC-SINV-2026-00001`, PKR 13,000,000), Paid via Payment Entry (`ACC-PAY-2026-00003`).
  - Delivery to **Lahore Motors**: 1 × Orbis X1 SUV (`MAT-DN-2026-00002`), Invoiced (`ACC-SINV-2026-00002`, PKR 11,500,000), Paid via Payment Entry (`ACC-PAY-2026-00004`).
- **Finished Goods Stock:**
  - Remaining ready-to-sell inventory in `Finished Goods Warehouse - OCM`: 3 × Orbis O1 Sedan, 2 × Orbis X1 SUV.

---

## 7. Master & Manufacturing Validation Suite

The automated test suite executed comprehensive checks covering Company, System, Cleanup, Masters, Users, RBAC, Manufacturing, Quality, Deliveries, and Accounting:

**Master Suite Score: 31 / 31 Checks Passed (100.0%)**

---

## 8. Role-Based Access Control (RBAC) & Permission Boundaries

The permission configuration strictly enforces the Principle of Least Privilege across all 10 business users using native ERPNext `Custom DocPerm` records:

| User | Department | Designated Role | Allowed DocTypes | Denied DocTypes |
|---|---|---|---|---|
| **Ali Khan** | Sales | Sales Manager | Customer (R/W/C), Lead (R/W/C), Opportunity (R/W/C), Quotation (R/W/C/S), Sales Order (R/W/C/S), Sales Invoice (R), Delivery Note (R), Item (R), BOM (R) | Work Order (C), Employee (C), Payment Entry (C), Delivery Note (C), PO (C), User (C), Roles (C), System Settings (W) |
| **Ahmed Raza** | Purchasing | Purchase Manager | Supplier (R/W/C), Material Request (R/W/C/S), RFQ (R/W/C/S), Purchase Order (R/W/C/S), Purchase Receipt (R/W/C/S), Item (R), Stock Entry (R) | Sales Order (C), Work Order (C), BOM (C), Quality Inspection (C), Payment Entry (C), Employee (C), User (C), Roles (C) |
| **Usman Ali** | Inventory / Stock | Stock Manager | Item (R/W/C), Warehouse (R/W/C), Stock Entry (R/W/C/S), Stock Reconciliation (R/W/C/S), Batch (R/W/C), Serial No (R/W/C), Purchase Receipt (R), Delivery Note (R) | User (C), Employee (C), Roles (C), Accounting Config, System Settings (W), Work Order (C) |
| **Hassan Malik** | Manufacturing / Production | Manufacturing Manager | BOM (R/W/C/S), Work Order (R/W/C/S), Job Card (R/W/C/S), Operation (R/W/C), Workstation (R/W/C), Production Plan (R/W/C/S), Stock Entry (R/W/C/S), Item (R), Warehouse (R) | Employee (C), User (C), Roles (C), HR Config, Accounting Config, System Settings (W) |
| **Hamza Ahmed** | Shop Floor / Operations | Shop Floor User | Job Card (R/W/C/S), Work Order (R), BOM (R), Operation (R), Workstation (R), Item (R), Stock Entry (R/W/C/S) | Work Order (C/W/S), BOM (W/C/S), Customer (C), Supplier (C), Sales Order (C), Purchase Order (C), Employee (C), User (C) |
| **Bilal Khan** | Shop Floor / Operations | Shop Floor User | Job Card (R/W/C/S), Work Order (R), BOM (R), Operation (R), Workstation (R), Item (R), Stock Entry (R/W/C/S) | Work Order (C/W/S), BOM (W/C/S), Customer (C), Supplier (C), Sales Order (C), Purchase Order (C), Employee (C), User (C) |
| **Sara Ahmed** | Quality Control | Quality Manager | Quality Inspection (R/W/C/S/Cancel), Quality Inspection Template (R/W/C), Quality Inspection Parameter (R/W/C), Item (R), Work Order (R), Job Card (R), Batch (R), Serial No (R) | Purchase Order (C), Sales Order (C), Work Order (C), Employee (C), User (C), Roles (C), System Settings (W) |
| **Usman Shah** | Delivery / Logistics | Delivery Manager | Delivery Note (R/W/C/S), Delivery Trip (R/W/C/S), Sales Order (R), Customer (R), Item (R), Warehouse (R) | Purchase Order (C), Work Order (C), BOM (C), Employee (C), Payment Entry (C), User (C), Roles (C), System Settings (W) |
| **Ayesha Khan** | Accounts / Finance | Accounts Manager | Sales Invoice (R/W/C/S), Purchase Invoice (R/W/C/S), Payment Entry (R/W/C/S), Journal Entry (R/W/C/S), GL Entry (R), Account (R), Taxes (R), Budget (R/W/C) | Work Order (C), BOM (C), Employee (C), User (C), Roles (C), System Settings (W) |
| **Fatima Ali** | Human Resources | HR Manager | Employee (R/W/C), Department (R), Designation (R/W/C), Timesheet (R/W/C/S), Holiday List (R/W/C) | User (C/W/Delete), Roles (C/W/Assign), Role Permissions (W), User Permissions (W), System Settings (W), API Keys |
| **Administrator** | System Administration | Administrator | Unrestricted Root Access across all DocTypes, Users, Roles, and System Configuration | None |

---

## 9. Workspace & Module Visibility Configuration

Workspaces are strictly filtered via role assignments so each user sees only their departmental workspace on the Desk:

- **Sales Manager:** `Selling` (all other modules hidden)
- **Purchase Manager:** `Buying`
- **Stock Manager:** `Stock`
- **Manufacturing Manager:** `Manufacturing`, `Stock`, `Projects`
- **Shop Floor Users:** `Manufacturing`, limited `Stock`
- **Quality Manager:** `Quality`, `Manufacturing`, `Stock`
- **Delivery Manager:** `Selling`, `Stock`
- **Accounts Manager:** `Invoicing`, `Financial Reports`, `Buying`, `Selling`
- **HR Manager:** `Human Resources`
- **Administrative / Technical Workspaces:** (`ERPNext Settings`, `Users`, `Build`, `Integrations`, `Website`, `Subcontracting`, `Support`, `CRM`) restricted exclusively to `System Manager` and `Administrator`.

---

## 10. Projects, Tasks & Manufacturing Assets

### 10.1 Projects & Tasks
All projects assigned to `Orbis Car Manufacturing (Pvt.) Ltd.`:
1. **OCM O1 Sedan Production Project** (5 Tasks: Component Procurement, Prototype Assembly, Testing, Quality Approval, Production Readiness)
2. **OCM X1 SUV Production Improvement** (5 Tasks: Design Optimization, Chassis Reinforcement, Suspension Tuning, Production Line Setup, Quality Sign-Off)
3. **OCM E1 Electric Vehicle Development** (5 Tasks: Battery Pack Architecture, Electric Motor Integration, BMS Firmware Validation, Crash & HV Safety Testing, Pilot Production)

### 10.2 Manufacturing Machinery & Fixed Assets
Configured under category `Manufacturing Machinery` at `OCM Assembly Plant - Karachi`:
1. **CNC Body Cutting Machine** — Dept: `Manufacturing / Production - OCM` (PKR 4,500,000)
2. **Vehicle Paint Booth** — Dept: `Shop Floor / Production Operations - OCM` (PKR 8,000,000)
3. **Engine Assembly Machine** — Dept: `Manufacturing / Production - OCM` (PKR 6,500,000)
4. **Welding Station** — Dept: `Shop Floor / Production Operations - OCM` (PKR 3,200,000)
5. **Vehicle Testing Machine** — Dept: `Quality Control - OCM` (PKR 5,000,000)
6. **Battery Testing Equipment** — Dept: `Quality Control - OCM` (PKR 7,500,000)

---

## 11. Final System State & Verification Counts

| Record Type | Count | Status / Verification Note |
|---|---|---|
| **Company** | 1 | `Orbis Car Manufacturing (Pvt.) Ltd.` (OCM) — Default |
| **System Branding** | 1 | `OrbisERP` (Visible app name) |
| **Active Business Users** | 10 | Exactly 10 users with bcrypt hashed passwords |
| **Departments** | 21 | All 10 project departments + standard child departments |
| **Warehouses** | 12 | 7 manufacturing warehouses + transit/root trees |
| **Items** | 60 | 3 Finished Cars (OCM-CAR-O1/X1/E1), Assemblies, Raw Materials |
| **Customers / Dealers** | 8 | Automobile dealerships across Pakistan |
| **Suppliers** | 10 | Automobile raw material & component suppliers |
| **BOMs** | 3 | Multi-level submitted BOMs with operations & workstations |
| **Operations** | 18 | Automobile manufacturing & testing operations |
| **Workstations** | 9 | Factory assembly stations |
| **Work Orders** | 3 | 5 Sedan (Completed), 3 SUV (Completed), 2 EV (In Process) |
| **Job Cards** | 2 | Assigned to Shop Floor Users for EV assembly |
| **Quality Inspections** | 3 | 2 Passed (Sedan, SUV), 1 Failed & Quarantined (EV) |
| **Sales Orders** | 2 | Commercial dealership orders |
| **Purchase Orders** | 9 | Raw material & component orders |
| **Delivery Notes** | 2 | Completed vehicle deliveries |
| **Sales Invoices** | 2 | Submitted vehicle sales invoices |
| **Purchase Invoices** | 2 | Submitted material purchase invoices |
| **Payment Entries** | 4 | Inbound & outbound banking entries |
| **Journal Entries** | 1 | Factory petty cash bank transfer |
| **GL Entries** | 44 | Complete double-entry general ledger |
| **Employees** | 10 | Linked 1:1 with ERPNext business users & departments |
| **Timesheets** | 1 | Manufacturing Manager shop floor supervision |
| **Projects** | 3 | Sedan, SUV, and EV production projects |
| **Tasks** | 15 | Engineering and production tasks |
| **Assets** | 6 | Factory manufacturing machinery & testing equipment |

---

## 12. Automated Permission Boundary Test Results

Programmatic testing evaluated 33 permission boundary conditions directly against the Frappe engine:

```text
[✓] Ali Khan (Sales Mgr)         | ALLOWED | Customer             (create): True  == True  -> PASS
[✓] Ali Khan (Sales Mgr)         | ALLOWED | Quotation            (create): True  == True  -> PASS
[✓] Ali Khan (Sales Mgr)         | ALLOWED | Sales Order          (create): True  == True  -> PASS
[✓] Ali Khan (Sales Mgr)         | DENIED  | Work Order           (create): False == False -> PASS
[✓] Ali Khan (Sales Mgr)         | DENIED  | Employee             (create): False == False -> PASS
[✓] Ali Khan (Sales Mgr)         | DENIED  | Payment Entry        (create): False == False -> PASS
[✓] Ali Khan (Sales Mgr)         | DENIED  | Delivery Note        (create): False == False -> PASS
[✓] Ahmed Raza (Purchase Mgr)    | ALLOWED | Purchase Order       (create): True  == True  -> PASS
[✓] Ahmed Raza (Purchase Mgr)    | ALLOWED | Supplier             (create): True  == True  -> PASS
[✓] Ahmed Raza (Purchase Mgr)    | DENIED  | Sales Order          (create): False == False -> PASS
[✓] Ahmed Raza (Purchase Mgr)    | DENIED  | Work Order           (create): False == False -> PASS
[✓] Usman Ali (Stock Mgr)        | ALLOWED | Stock Entry          (create): True  == True  -> PASS
[✓] Usman Ali (Stock Mgr)        | ALLOWED | Item                 (create): True  == True  -> PASS
[✓] Usman Ali (Stock Mgr)        | DENIED  | User                 (create): False == False -> PASS
[✓] Usman Ali (Stock Mgr)        | DENIED  | Employee             (create): False == False -> PASS
[✓] Hassan Malik (Mfg Mgr)       | ALLOWED | Work Order           (create): True  == True  -> PASS
[✓] Hassan Malik (Mfg Mgr)       | ALLOWED | BOM                  (create): True  == True  -> PASS
[✓] Hassan Malik (Mfg Mgr)       | DENIED  | Employee             (create): False == False -> PASS
[✓] Hassan Malik (Mfg Mgr)       | DENIED  | User                 (create): False == False -> PASS
[✓] Hamza Ahmed (Shop Floor)     | ALLOWED | Job Card             (write) : True  == True  -> PASS
[✓] Hamza Ahmed (Shop Floor)     | DENIED  | Work Order           (create): False == False -> PASS
[✓] Hamza Ahmed (Shop Floor)     | DENIED  | BOM                  (write) : False == False -> PASS
[✓] Sara Ahmed (Quality Mgr)     | ALLOWED | Quality Inspection   (create): True  == True  -> PASS
[✓] Sara Ahmed (Quality Mgr)     | DENIED  | Purchase Order       (create): False == False -> PASS
[✓] Usman Shah (Delivery Mgr)    | ALLOWED | Delivery Note        (create): True  == True  -> PASS
[✓] Usman Shah (Delivery Mgr)    | DENIED  | Payment Entry        (create): False == False -> PASS
[✓] Ayesha Khan (Accounts Mgr)   | ALLOWED | Sales Invoice        (create): True  == True  -> PASS
[✓] Ayesha Khan (Accounts Mgr)   | ALLOWED | Payment Entry        (create): True  == True  -> PASS
[✓] Ayesha Khan (Accounts Mgr)   | DENIED  | Work Order           (create): False == False -> PASS
[✓] Fatima Ali (HR Mgr)          | ALLOWED | Employee             (create): True  == True  -> PASS
[✓] Fatima Ali (HR Mgr)          | DENIED  | User                 (create): False == False -> PASS
[✓] Fatima Ali (HR Mgr)          | DENIED  | Role                 (create): False == False -> PASS
[✓] Fatima Ali (HR Mgr)          | DENIED  | System Settings      (write) : False == False -> PASS

Final Boundary Test Score: 33 / 33 (100.0% Passed)
```

---

## 13. Voice-Controlled FYP Security Architecture

This ERPNext setup directly empowers the target Final Year Project architecture:

```text
Voice Input (Microphone)
       ↓
Speaker Verification (Biometric Auth)
       ↓
Identify ERPNext User (e.g., Ali Khan)
       ↓
Identify User Role (e.g., Sales Manager)
       ↓
Understand Voice Intent (e.g., "Create Sales Order for Ahmed Motors")
       ↓
Check ERPNext DocType Permissions (frappe.has_permission)
       ↓
Authorize or Deny (ERPNext is the final gatekeeper)
       ↓
Execute ERPNext Action via REST API
       ↓
Audit Log Recorded
```

**Key Security Invariant:** *Voice Identity Does NOT Equal Authorization*. The AI layer only identifies intent; ERPNext's role-based DocType permissions remain the ultimate authority.

---

## 14. Detailed Accounting & Finance Demo Data (Section 44 & 45)

### 14.1 Connected Sales Invoices
All sales invoices linked with `Pakistan Tax - OCM` (17% GST) and posted to `Debtors - OCM` and `Sales - OCM`:
1. **ACC-SINV-2026-00003** (Ahmed Motors):
   - Items: 2 × Orbis O1 Sedan, 1 × Orbis X1 SUV
   - Subtotal: PKR 24,500,000 | 17% GST: PKR 4,165,000 | **Grand Total: PKR 28,665,000**
   - Paid: PKR 18,665,000 via `ACC-PAY-2026-00005` | **Outstanding: PKR 10,000,000** (**Partly Paid**)
2. **ACC-SINV-2026-00004** (Lahore Motors):
   - Items: 2 × Orbis X1 SUV
   - Subtotal: PKR 23,000,000 | 17% GST: PKR 3,910,000 | **Grand Total: PKR 26,910,000**
   - Paid: PKR 26,910,000 via `ACC-PAY-2026-00006` | **Outstanding: PKR 0.00** (**Paid**)
3. **ACC-SINV-2026-00005** (Islamabad Auto Gallery):
   - Items: 1 × Orbis E1 Electric
   - Subtotal: PKR 14,000,000 | 17% GST: PKR 2,380,000 | **Grand Total: PKR 16,380,000**
   - **Outstanding: PKR 16,380,000** (**Unpaid**)

### 14.2 Connected Purchase Invoices
All purchase invoices linked with `Pakistan Tax - OCM` (17% GST) and posted to `Creditors - OCM` and `Cost of Goods Sold - OCM`:
1. **ACC-PINV-2026-00003** (Pakistan Steel Suppliers):
   - Items: 500 × Steel Sheet
   - Subtotal: PKR 7,500,000 | 17% GST: PKR 1,275,000 | **Grand Total: PKR 8,775,000**
   - Paid: PKR 8,775,000 via `ACC-PAY-2026-00007` | **Outstanding: PKR 0.00** (**Paid**)
2. **ACC-PINV-2026-00004** (Prime Tyres Pakistan):
   - Items: 200 × Tyres
   - Subtotal: PKR 3,600,000 | 17% GST: PKR 612,000 | **Grand Total: PKR 4,212,000**
   - Paid: PKR 2,212,000 via `ACC-PAY-2026-00008` | **Outstanding: PKR 2,000,000** (**Partly Paid**)
3. **ACC-PINV-2026-00005** (National Glass Components):
   - Items: 100 × Windshield Glass
   - Subtotal: PKR 2,500,000 | 17% GST: PKR 425,000 | **Grand Total: PKR 2,925,000**
   - **Outstanding: PKR 2,925,000** (**Unpaid**)

### 14.3 Payment Entries
- **Customer Payments (Receive):**
  - `ACC-PAY-2026-00005`: Ahmed Motors (PKR 18,665,000) -> Partial against `ACC-SINV-2026-00003`
  - `ACC-PAY-2026-00006`: Lahore Motors (PKR 26,910,000) -> Full against `ACC-SINV-2026-00004`
- **Supplier Payments (Pay):**
  - `ACC-PAY-2026-00007`: Pakistan Steel Suppliers (PKR 8,775,000) -> Full against `ACC-PINV-2026-00003`
  - `ACC-PAY-2026-00008`: Prime Tyres Pakistan (PKR 2,212,000) -> Partial against `ACC-PINV-2026-00004`

### 14.4 Journal Entries (General Ledger)
1. `ACC-JV-2026-00006`: Initial Shareholder Equity Injection (PKR 150,000,000 into `Habib Bank Limited - OCM` from `Capital Stock - OCM`)
2. `ACC-JV-2026-00002`: Factory Electricity Expense (PKR 550,000 to `Utility Expenses - OCM`)
3. `ACC-JV-2026-00003`: Factory Maintenance Expense (PKR 320,000 to `Office Maintenance Expenses - OCM`)
4. `ACC-JV-2026-00004`: Office Administrative Expense (PKR 180,000 to `Administrative Expenses - OCM`)
5. `ACC-JV-2026-00005`: Production Tooling Adjustment (PKR 140,000 to `Stock Adjustment - OCM`)
6. `ACC-JV-2026-00001`: Factory Petty Cash Bank Allocation (PKR 150,000 from Bank to Cash)

### 14.5 Annual Budgets (FY 2026-2027)
Configured under `Cost Center = Main - OCM` with equal monthly distribution:
1. `Cost of Goods Sold - OCM`: PKR 150,000,000 / year (Raw Materials & Manufacturing)
2. `Utility Expenses - OCM`: PKR 12,000,000 / year (Factory Electricity)
3. `Office Maintenance Expenses - OCM`: PKR 8,000,000 / year (Factory Maintenance)
4. `Administrative Expenses - OCM`: PKR 6,000,000 / year (Administration)
5. `Marketing Expenses - OCM`: PKR 5,000,000 / year (Marketing & Sales)
6. `Travel Expenses - OCM`: PKR 4,000,000 / year (Logistics & Distribution)

### 14.6 Financial Reports Verification Summary
All 9 ERPNext financial reports confirm live OCM accounting data:
- **General Ledger:** 80 GL Entries recorded | Status: **ACTIVE**
- **Accounts Receivable:** PKR 26,380,000 outstanding (Ahmed Motors + Islamabad Auto Gallery) | Status: **ACTIVE**
- **Accounts Payable:** PKR 4,925,000 outstanding (Prime Tyres + National Glass) | Status: **ACTIVE**
- **Trial Balance:** Total Debits = PKR 761,804,700 | Total Credits = PKR 761,804,700 | Status: **BALANCED (0.00 Difference)**
- **Profit and Loss:** Revenue = PKR 86,000,000 | Net Profit = PKR 75,912,050 | Status: **ACTIVE**
- **Balance Sheet:** Assets = PKR 297,180,050 | Liabilities = PKR 71,268,000 | Status: **ACTIVE**
- **Cash Flow / Bank Account:** Habib Bank Limited - OCM Balance = PKR 95,713,000.00 | Status: **ACTIVE**
- **Sales Register:** 5 submitted Sales Invoices | Status: **ACTIVE**
- **Purchase Register:** 5 submitted Purchase Invoices | Status: **ACTIVE**

---

## 15. Role-Based User Interface, Workspaces, Access Control & OCM Branding (Step 7)

### 15.1 Application Branding Configuration
All visible user-facing branding has been transformed from standard "ERPNext" to **OCM** / **OrbisERP** without altering core technical DocTypes or framework tables:
- **System Settings:** `app_name = "OCM"`
- **Navbar Settings:** `app_logo = "/files/ocm_logo.svg"` (sleek automotive badge with electric cyan accent & bold typography)
- **Website Settings:**
  - `app_name = "OCM - OrbisERP"`
  - `brand_html = "<b>OCM</b>"`
  - `app_logo = "/files/ocm_logo.svg"`
  - `banner_image = "/files/ocm_logo.svg"`
  - `favicon = "/files/ocm_favicon.svg"`
  - `copyright = "© 2026 Orbis Car Manufacturing (Pvt.) Ltd. (OCM)"`
- **Workspaces Renaming:** `ERPNext Settings` renamed to `OCM System Settings`

### 15.2 Default Workspace Lockdown
All 20 standard/default ERPNext workspaces (`Home`, `Selling`, `Buying`, `Stock`, `Manufacturing`, `Quality`, `Invoicing`, `Financial Reports`, `Projects`, `Assets`, `Subcontracting`, `Support`, `CRM`, `ERPNext Settings`, `Users`, `Build`, `Integrations`, `Website`, `Welcome Workspace`, `Human Resources`) have been strictly restricted to:
- `['System Manager', 'Administrator']`

Business users cannot view, click, or navigate to any standard workspaces.

### 15.3 Dedicated OCM Workspaces
Created 9 custom, dedicated workspaces with role-based visibility and streamlined card layouts:
1. **OCM Sales** (`Selling` module):
   - **Allowed Roles:** `Sales Manager`, `System Manager`, `Administrator`
   - **Cards:** Sales Operations (Customers, Leads, Opportunities, Quotations, Sales Orders, Sales Invoices [Read-Only], Delivery Notes [Read-Only], Vehicle Catalog [Read-Only]), Sales Reports (Sales Analytics, Sales Order Analysis, Sales Register, Customer Ledger Summary)
2. **OCM Purchasing** (`Buying` module):
   - **Allowed Roles:** `Purchase Manager`, `System Manager`, `Administrator`
   - **Cards:** Purchasing Operations (Suppliers, Material Requests, Request for Quotation, Purchase Orders, Purchase Receipts, Purchase Invoices, Raw Materials [Read-Only]), Procurement Reports (Purchase Analytics, Purchase Order Analysis, Purchase Register, Supplier Quotation Comparison)
3. **OCM Inventory** (`Stock` module):
   - **Allowed Roles:** `Stock Manager`, `System Manager`, `Administrator`
   - **Cards:** Stock Operations (Items, Item Groups, Warehouses, Stock Entry, Stock Reconciliation, Batches, Serial Numbers, Purchase Receipts, Delivery Notes), Inventory Reports (Stock Ledger, Stock Balance, Stock Analytics, Stock Projected Qty)
4. **OCM Manufacturing** (`Manufacturing` module):
   - **Allowed Roles:** `Manufacturing Manager`, `System Manager`, `Administrator`
   - **Cards:** Production Operations (BOM, Work Orders, Job Cards, Operations, Workstations, Production Plan, Manufacturing Stock Entry, Components & Materials, Warehouses), Production Reports (Work Order Summary, BOM Operations Time, Production Analytics)
5. **OCM Production** (`Manufacturing` module):
   - **Allowed Roles:** `Shop Floor User`, `System Manager`, `Administrator`
   - **Cards:** Shop Floor Operations (My Job Cards, Assigned Work Orders [Read-Only], Assembly Operations [Read-Only], Workstations [Read-Only], Production Material Transfer, Items [Read-Only])
6. **OCM Quality** (`Quality Management` module):
   - **Allowed Roles:** `Quality Manager`, `System Manager`, `Administrator`
   - **Cards:** Quality Control (Quality Inspections, Quality Inspection Templates, Quality Parameters, Work Orders [Read-Only], Job Cards [Read-Only], Items [Read-Only], Quality Hold Warehouse [Read-Only]), Quality Reports (Quality Inspection Summary)
7. **OCM Delivery** (`Selling` module):
   - **Allowed Roles:** `Delivery Manager`, `System Manager`, `Administrator`
   - **Cards:** Vehicle Logistics (Delivery Notes, Delivery Trips, Sales Orders [Read-Only], Dealership Customers [Read-Only], Finished Vehicles [Read-Only], Finished Goods Warehouse [Read-Only]), Delivery Reports (Delivered Vehicles To Be Billed, Delivery Note Trends)
8. **OCM Accounts** (`Accounts` module):
   - **Allowed Roles:** `Accounts Manager`, `System Manager`, `Administrator`
   - **Cards:** Financial Transactions (Sales Invoices, Purchase Invoices, Payment Entries, Journal Entries, Chart of Accounts [Read-Only], Annual Budgets, Customers [Read-Only], Suppliers [Read-Only]), Financial Reports (General Ledger, Trial Balance, P&L Statement, Balance Sheet, Cash Flow, Accounts Receivable, Accounts Payable, Sales Register, Purchase Register)
9. **OCM Human Resources** (`Setup` module):
   - **Allowed Roles:** `HR Manager`, `System Manager`, `Administrator`
   - **Cards:** Employee Management (Employees, Departments [Read-Only], Designations, Timesheets, Holiday Lists), HR Reports (Daily Timesheet Summary, Timesheet Billing Summary)

### 15.4 Workspace Visibility & Landing Verification Matrix
Validated live through `frappe.desk.desktop.get_workspaces()` for all 10 users:

| Business User | Email | Role | Visible Workspaces | Landing Workspace | Status |
|:---|:---|:---|:---|:---|:---:|
| Ali Khan | `forw8007+salesmanager@gmail.com` | Sales Manager | `['OCM Sales']` | OCM Sales | **PASS** |
| Ahmed Raza | `forw8007+purchasemanager@gmail.com` | Purchase Manager | `['OCM Purchasing']` | OCM Purchasing | **PASS** |
| Usman Ali | `forw8007+stockmanager@gmail.com` | Stock Manager | `['OCM Inventory']` | OCM Inventory | **PASS** |
| Hassan Malik | `forw8007+manufacturingmanager@gmail.com` | Manufacturing Manager | `['OCM Manufacturing']` | OCM Manufacturing | **PASS** |
| Hamza Ahmed | `forw8007+flooruser1@gmail.com` | Shop Floor User | `['OCM Production']` | OCM Production | **PASS** |
| Bilal Khan | `forw8007+flooruser2@gmail.com` | Shop Floor User | `['OCM Production']` | OCM Production | **PASS** |
| Sara Ahmed | `forw8007+qualitymanager@gmail.com` | Quality Manager | `['OCM Quality']` | OCM Quality | **PASS** |
| Usman Shah | `forw8007+deliverymanager@gmail.com` | Delivery Manager | `['OCM Delivery']` | OCM Delivery | **PASS** |
| Ayesha Khan | `forw8007+accountsmanager@gmail.com` | Accounts Manager | `['OCM Accounts']` | OCM Accounts | **PASS** |
| Fatima Ali | `forw8007+hrmanager@gmail.com` | HR Manager | `['OCM Human Resources']` | OCM Human Resources | **PASS** |
| Administrator | `Administrator` | System Root | **28 Workspaces** (All 9 OCM + All 19 System/Module Workspaces) | Complete Access | **PASS** |

### 15.5 Unauthorized Direct URL / API Access Prevention (42/42 Tests Passed)
Verified live backend authorization checks (`frappe.has_permission()`) ensuring that UI hiding is backed by rigid database-level security boundaries:

| User Role | Tested DocType | Action | Attempt Result | Enforcement | Status |
|:---|:---|:---|:---:|:---:|:---:|
| Sales Manager | Work Order | read | **Blocked** (`has_permission=False`) | Backend DocPerm | **PASS** |
| Sales Manager | BOM | read | **Blocked** (`has_permission=False`) | Backend DocPerm | **PASS** |
| Sales Manager | Employee | read | **Blocked** (`has_permission=False`) | Backend DocPerm | **PASS** |
| Sales Manager | Payment Entry | create | **Blocked** (`has_permission=False`) | Backend DocPerm | **PASS** |
| Sales Manager | User | create | **Blocked** (`has_permission=False`) | Backend DocPerm | **PASS** |
| Sales Manager | Role | create | **Blocked** (`has_permission=False`) | Backend DocPerm | **PASS** |
| Purchase Manager | Sales Order | create | **Blocked** (`has_permission=False`) | Backend DocPerm | **PASS** |
| Purchase Manager | Work Order | read | **Blocked** (`has_permission=False`) | Backend DocPerm | **PASS** |
| Purchase Manager | Employee | read | **Blocked** (`has_permission=False`) | Backend DocPerm | **PASS** |
| Purchase Manager | User | create | **Blocked** (`has_permission=False`) | Backend DocPerm | **PASS** |
| Stock Manager | User | create | **Blocked** (`has_permission=False`) | Backend DocPerm | **PASS** |
| Stock Manager | Role | create | **Blocked** (`has_permission=False`) | Backend DocPerm | **PASS** |
| Stock Manager | Employee | create | **Blocked** (`has_permission=False`) | Backend DocPerm | **PASS** |
| Stock Manager | Work Order | create | **Blocked** (`has_permission=False`) | Backend DocPerm | **PASS** |
| Manufacturing Manager | Employee | create | **Blocked** (`has_permission=False`) | Backend DocPerm | **PASS** |
| Manufacturing Manager | User | create | **Blocked** (`has_permission=False`) | Backend DocPerm | **PASS** |
| Manufacturing Manager | Role | create | **Blocked** (`has_permission=False`) | Backend DocPerm | **PASS** |
| Shop Floor User | Work Order | create | **Blocked** (`has_permission=False`) | Backend DocPerm | **PASS** |
| Shop Floor User | BOM | write | **Blocked** (`has_permission=False`) | Backend DocPerm | **PASS** |
| Shop Floor User | Customer | read | **Blocked** (`has_permission=False`) | Backend DocPerm | **PASS** |
| Shop Floor User | Sales Order | read | **Blocked** (`has_permission=False`) | Backend DocPerm | **PASS** |
| Shop Floor User | Purchase Order | read | **Blocked** (`has_permission=False`) | Backend DocPerm | **PASS** |
| Shop Floor User | Sales Invoice | read | **Blocked** (`has_permission=False`) | Backend DocPerm | **PASS** |
| Shop Floor User | Employee | create | **Blocked** (`has_permission=False`) | Backend DocPerm | **PASS** |
| Quality Manager | Purchase Order | create | **Blocked** (`has_permission=False`) | Backend DocPerm | **PASS** |
| Quality Manager | Sales Order | create | **Blocked** (`has_permission=False`) | Backend DocPerm | **PASS** |
| Quality Manager | Work Order | create | **Blocked** (`has_permission=False`) | Backend DocPerm | **PASS** |
| Quality Manager | Employee | read | **Blocked** (`has_permission=False`) | Backend DocPerm | **PASS** |
| Delivery Manager | Purchase Order | read | **Blocked** (`has_permission=False`) | Backend DocPerm | **PASS** |
| Delivery Manager | Work Order | read | **Blocked** (`has_permission=False`) | Backend DocPerm | **PASS** |
| Delivery Manager | BOM | read | **Blocked** (`has_permission=False`) | Backend DocPerm | **PASS** |
| Delivery Manager | Payment Entry | create | **Blocked** (`has_permission=False`) | Backend DocPerm | **PASS** |
| Accounts Manager | Work Order | create | **Blocked** (`has_permission=False`) | Backend DocPerm | **PASS** |
| Accounts Manager | BOM | create | **Blocked** (`has_permission=False`) | Backend DocPerm | **PASS** |
| Accounts Manager | Employee | create | **Blocked** (`has_permission=False`) | Backend DocPerm | **PASS** |
| Accounts Manager | User | create | **Blocked** (`has_permission=False`) | Backend DocPerm | **PASS** |
| HR Manager | User | create | **Blocked** (`has_permission=False`) | Backend DocPerm | **PASS** |
| HR Manager | Role | create | **Blocked** (`has_permission=False`) | Backend DocPerm | **PASS** |
| HR Manager | Role | write | **Blocked** (`has_permission=False`) | Backend DocPerm | **PASS** |
| HR Manager | Work Order | read | **Blocked** (`has_permission=False`) | Backend DocPerm | **PASS** |
| HR Manager | Sales Order | read | **Blocked** (`has_permission=False`) | Backend DocPerm | **PASS** |
| HR Manager | Purchase Order | read | **Blocked** (`has_permission=False`) | Backend DocPerm | **PASS** |

**Summary Security Score: 42 / 42 (100.0% Pass Rate)**

---

## 16. Strict OCM Role-Based Access, Visibility & Branding Fix (Step 8)

### 16.1 Root Cause Analysis of Previous Vulnerabilities
1. **Standard Role Permission Bleed:** Standard ERPNext roles `Desk User` and `Employee` contained default `DocPerm` granting read/write/create on Quality management records (`Quality Goal`, `Quality Review`, `Quality Action`, `Quality Meeting`, `Quality Procedure`, `Quality Feedback`, `Non Conformance`). Because business users held `Desk User` and `Employee`, these permissions allowed the Sales Manager to access the Quality module and create quality records.
2. **Desk Workspace Sidebar Auto-Discovery:** In modern Frappe desk, `bootinfo.workspace_sidebar_item` auto-discovered and rendered sidebars for every module containing at least one readable DocType. Because `Item` and `Customer` were readable by sales/purchasing/stock, sidebars for `Organization`, `Accounts Setup`, `Assets`, `Buying`, `Manufacturing`, `Projects`, `Quality`, `Stock`, `Subcontracting`, and `ERPNext Settings` were appearing in the sidebar navigation and app switcher.
3. **Sidebar Header Subtitle Branding:** The second line of the sidebar header was dynamically resolved from `frappe.boot.app_data[].app_title`, which defaulted to `"ERPNext"` for the erpnext app.
4. **Loading Screen Splash Identity:** The desk loading indicator rendered `/assets/erpnext/images/erpnext-logo.svg` which contained the generic ERPNext "E" logo.

### 16.2 Security & System Fixes Implemented
1. **Standard Role Auditing & Cleanup:**
   - Stripped the `Employee` role from all 9 non-HR users (`Sales Manager`, `Purchase Manager`, `Stock Manager`, `Manufacturing Manager`, `Shop Floor User 1 & 2`, `Quality Manager`, `Delivery Manager`, `Accounts Manager`).
   - Each business user now holds strictly their single required managerial/operator role (`Sales Manager`, `Purchase Manager`, etc.) plus implicit desk access.
2. **Server-Side Quality DocType Hardening:**
   - Deleted all broad standard permissions on all 10 Quality DocTypes (`Quality Inspection`, `Quality Inspection Template`, `Quality Inspection Parameter`, `Quality Goal`, `Quality Review`, `Quality Action`, `Quality Meeting`, `Quality Procedure`, `Quality Feedback`, `Non Conformance`).
   - Created strict `Custom DocPerm` exclusively assigning full permissions to `Quality Manager` and `System Manager`.
   - All 10 Quality DocTypes now return `has_permission('create') = False` and `has_permission('read') = False` for Sales Manager and all other non-Quality roles.
3. **Boot Session Role-Based Workspace & Sidebar Isolation:**
   - Hooked `ocm_boot_session(bootinfo)` into `apps/erpnext/erpnext/startup/boot.py:boot_session`.
   - Business users have their `bootinfo.workspaces['pages']`, `bootinfo.workspace_sidebar_item`, and `bootinfo.desktop_icons` strictly filtered at login.
   - Prohibited sidebars (`organization`, `accounting`, `assets`, `buying`, `manufacturing`, `projects`, `quality`, `stock`, `subcontracting`, `erpnext settings`, etc.) are eliminated from the user session.
   - For `Administrator` and `System Manager`, full unrestricted access to all 28 workspaces and all sidebars is preserved.
4. **Full OCM / OrbisERP Branding Transformation:**
   - **Sidebar Header Branding:** Set `app_title = "OCM"` in `bootinfo.app_data` and `apps/erpnext/erpnext/hooks.py`. The sidebar header now renders:
     ```
     Selling
     OCM
     ```
   - **Loading Screen Splash Identity:** Generated `/files/ocm_splash.svg` and updated static framework assets (`sites/assets/erpnext/images/erpnext-logo.svg`, `apps/erpnext/erpnext/public/images/erpnext-logo.svg`, etc.) so the loading screen displays the official OrbisERP / OCM badge instead of the generic ERPNext "E".
   - **Application Title:** Updated `System Settings.app_name` and `Website Settings.app_name` to `OCM | OrbisERP`.

### 16.3 Exact Permissions, Roles & Workspaces Changed Per User

| User | Email | Effective Roles | Allowed Workspaces & Sidebars | Prohibited & Blocked Modules / DocTypes |
|:---|:---|:---|:---|:---|
| **Ali Khan** | `forw8007+salesmanager@gmail.com` | `['Sales Manager', 'Desk User']` | **Workspace:** `OCM Sales`<br>**Sidebars:** `selling`, `crm` | **Blocked:** All 10 Quality DocTypes, `Work Order`, `BOM`, `Purchase Order`, `Payment Entry`, `Employee`, `User`, `Role` |
| **Ahmed Raza** | `forw8007+purchasemanager@gmail.com` | `['Purchase Manager', 'Desk User']` | **Workspace:** `OCM Purchasing`<br>**Sidebars:** `buying` | **Blocked:** `Sales Order`, `Work Order`, `BOM`, All Quality DocTypes, `Employee`, `User`, `Role` |
| **Usman Ali** | `forw8007+stockmanager@gmail.com` | `['Stock Manager', 'Desk User']` | **Workspace:** `OCM Inventory`<br>**Sidebars:** `stock` | **Blocked:** `Sales Order`, `Work Order`, `BOM`, All Quality DocTypes, `Employee`, `User`, `Role` |
| **Hassan Malik** | `forw8007+manufacturingmanager@gmail.com` | `['Manufacturing Manager', 'Desk User']` | **Workspace:** `OCM Manufacturing`<br>**Sidebars:** `manufacturing` | **Blocked:** `Sales Order` (create/write), `Purchase Order` (create), All Quality DocTypes, `Employee`, `User`, `Role` |
| **Hamza Ahmed** | `forw8007+flooruser1@gmail.com` | `['Shop Floor User', 'Desk User']` | **Workspace:** `OCM Production`<br>**Sidebars:** `ocm production` | **Blocked:** `Customer`, `Sales Order`, `Purchase Order`, `Sales Invoice`, `BOM` (create/write), `Work Order` (create), All Quality DocTypes, `Employee`, `User` |
| **Bilal Khan** | `forw8007+flooruser2@gmail.com` | `['Shop Floor User', 'Desk User']` | **Workspace:** `OCM Production`<br>**Sidebars:** `ocm production` | **Blocked:** Same as Shop Floor User 1 (Operator dashboard only) |
| **Sara Ahmed** | `forw8007+qualitymanager@gmail.com` | `['Quality Manager', 'Desk User']` | **Workspace:** `OCM Quality`<br>**Sidebars:** `quality`, `quality management` | **Allowed:** All 10 Quality DocTypes<br>**Blocked:** `Sales Order`, `Purchase Order`, `Work Order` (create), `Payment Entry`, `Employee`, `User` |
| **Usman Shah** | `forw8007+deliverymanager@gmail.com` | `['Delivery Manager', 'Desk User']` | **Workspace:** `OCM Delivery`<br>**Sidebars:** `delivery`, `selling` | **Blocked:** `Work Order`, `BOM`, `Purchase Order`, All Quality DocTypes, `Payment Entry`, `User` |
| **Ayesha Khan** | `forw8007+accountsmanager@gmail.com` | `['Accounts Manager', 'Desk User']` | **Workspace:** `OCM Accounts`<br>**Sidebars:** `accounts`, `invoicing`, `payments`, `financial reports` | **Blocked:** `Work Order`, `BOM`, All Quality DocTypes, `Employee` (create), `User`, `Role` |
| **Fatima Ali** | `forw8007+hrmanager@gmail.com` | `['HR Manager', 'Desk User']` | **Workspace:** `OCM Human Resources`<br>**Sidebars:** `human resources` | **Allowed:** `Employee`, `Designation`, `Timesheet`, `Holiday List`<br>**Blocked:** `Work Order`, `Sales Order`, `Purchase Order`, `User` (create/write), `Role` (create/write), System Settings |
| **Administrator** | `Administrator` | `['Administrator', 'System Manager']` | **All 28 Workspaces & All Sidebars** | **Unrestricted System Root Access** |

### 16.4 Acceptance Test Validation Results

#### Sales Manager Quality Security Boundary (Section 27 Mandatory Test)
- `Quality Inspection` -> Blocked = **True** (`has_permission('create') = False`)
- `Quality Inspection Template` -> Blocked = **True** (`has_permission('create') = False`)
- `Quality Inspection Parameter` -> Blocked = **True** (`has_permission('create') = False`)
- `Quality Goal` -> Blocked = **True** (`has_permission('create') = False`)
- `Quality Review` -> Blocked = **True** (`has_permission('create') = False`)
- `Quality Action` -> Blocked = **True** (`has_permission('create') = False`)
- `Quality Meeting` -> Blocked = **True** (`has_permission('create') = False`)
- `Quality Procedure` -> Blocked = **True** (`has_permission('create') = False`)
- `Quality Feedback` -> Blocked = **True** (`has_permission('create') = False`)
- `Non Conformance` -> Blocked = **True** (`has_permission('create') = False`)
- **Status: 10 / 10 QUALITY PERMISSION DENIAL CHECKS PASSED**

#### Sales Manager Home Screen & Sidebar Cleanliness (Section 14 & 15 Mandatory Test)
- Visible Workspaces: `['OCM Sales']`
- Visible Sidebars: `['selling', 'crm']`
- Leaked Sidebars (`organization`, `accounting`, `assets`, `buying`, `manufacturing`, `projects`, `quality`, `stock`, `subcontracting`, `erpnext settings`, `human resources`): **0 LEAKS (100% CLEAN)**
- Sidebar Identity: **`Selling \n OCM`** (Displays "OCM", not "ERPNext")

#### 10-User Access Matrix Status
- Ali Khan (Sales Manager): **PASS**
- Ahmed Raza (Purchase Manager): **PASS**
- Usman Ali (Stock Manager): **PASS**
- Hassan Malik (Manufacturing Manager): **PASS**
- Hamza Ahmed (Shop Floor User 1): **PASS**
- Bilal Khan (Shop Floor User 2): **PASS**
- Sara Ahmed (Quality Manager): **PASS**
- Usman Shah (Delivery Manager): **PASS**
- Ayesha Khan (Accounts Manager): **PASS**
- Fatima Ali (HR Manager): **PASS**
- Administrator (Root): **PASS (All 28 Workspaces Intact)**

---

### SECTION 17: OCM BRANDING & LOGO UNIFICATION DEPLOYMENT

#### 1. Source Image & High-Resolution Asset Generation
- **Source Graphic**: Futuristic glowing automotive badge (*"Orbis CAR MANUFACTURING - ERP -"*, 1024×1024 RGB JPEG).
- **Generated Assets**:
  - `/files/ocm_logo.png` (512×512 PNG, 304 KB, optimized) — Main application logo used on Navbar, Login Card, and Desk Header.
  - `/files/ocm_splash.png` (512×512 PNG, 304 KB, optimized) — Loading splash screen graphic.
  - `/files/ocm_favicon.png` (64×64 PNG, 8.4 KB) — Browser tab favicon and bookmark icon.
  - `/files/ocm_sidebar_icon.png` (128×128 PNG, 27.5 KB) — Sidebar icon representation.
  - `/files/ocm_logo.svg`, `/files/ocm_splash.svg`, `/files/ocm_favicon.svg` — SVG containers embedding high-resolution base64 PNG data for seamless legacy vector compatibility.

#### 2. Static Asset Overwrites Across Dual Containers (Backend & Nginx Frontend)
Because the Nginx frontend container (`frappe_docker-frontend-1`) serves static files directly from its image paths, all fallback image assets were updated and synchronized across both containers:
- `/assets/erpnext/images/erpnext-logo.png` & `.svg` -> **Updated with OCM Logo**
- `/assets/erpnext/images/erpnext-logo-blue.png` -> **Updated with OCM Logo**
- `/assets/frappe/images/frappe-framework-logo.png` & `.svg` -> **Updated with OCM Logo**
- `/assets/frappe/images/frappe-logo.png` & `frappe-comp-logo.svg` -> **Updated with OCM Logo**
- `/assets/erpnext/images/erpnext-favicon.svg` & `frappe-favicon.svg` -> **Updated with OCM Favicon**

#### 3. Sidebar "ERPNext" Text Replaced with "OCM"
- **Sidebar Subtitle (`.header-subtitle`)**:
  - Direct template update in `sidebar_header.html` sets `{%= frappe.app.sidebar.header_subtitle %}` to **`OCM`**.
  - Production Desk bundle (`desk.bundle.HAMU7ZDN.js`) patched across frontend and backend containers: all assignments to `header_subtitle` force **`"OCM"`**.
  - Session boot hook (`ocm_boot_session`) forces `parent_icon = "OCM"`, `app_title = "OCM"`, and `app = "OCM"` across all `desktop_icons`, `app_data`, and `workspace_sidebar_item`.
- **Sidebar Header Logo (`.header-logo`)**:
  - Replaced generic icon with `<img class="ocm-sidebar-logo" src="/files/ocm_logo.png">` with subtle neon blue glow (`box-shadow: 0 0 10px rgba(0, 195, 255, 0.45)`).

#### 4. Loading & Login Screen Branding
- **Loading / Splash Screen**:
  - `templates/includes/splash_screen.html` configured with `<img src="/files/ocm_splash.png">` styled with pulsing automotive glow animation (`@keyframes ocm-pulse`).
- **Login Screen**:
  - `apps/frappe/frappe/www/login.py` configured with `context["logo"] = "/files/ocm_logo.png"`.
  - Login card header displays the high-resolution glowing OCM badge with `filter: drop-shadow(0 0 16px rgba(0, 195, 255, 0.45))`.
  - Browser tab favicon displays `/files/ocm_favicon.png`.

#### 5. Persistent Runtime Guardian & CSS
- **`apps/erpnext/erpnext/public/js/ocm_branding.js`**:
  - Automatically hooked into `app_include_js` in `hooks.py`.
  - Runs continuous DOM checks and event listener hooks on `page-change` and route navigation to guarantee that `.header-subtitle` remains **`OCM`** and `.header-logo` displays the official emblem under all dynamic client-side transitions.
- **`apps/erpnext/erpnext/public/css/ocm_branding.css`**:
  - Automatically hooked into `app_include_css` in `hooks.py`.
  - Delivers futuristic automotive aesthetics with electric cyan glowing highlights matching OrbisERP design guidelines.

#### 6. Live Endpoint Verification Matrix
| Target Component | Endpoint / Element | Response / Value | Status |
| :--- | :--- | :--- | :--- |
| **Main Logo PNG** | `http://frontend:8080/files/ocm_logo.png` | HTTP 200 OK (304 KB PNG) | **PASS** |
| **Splash PNG** | `http://frontend:8080/files/ocm_splash.png` | HTTP 200 OK (304 KB PNG) | **PASS** |
| **Favicon PNG** | `http://frontend:8080/files/ocm_favicon.png` | HTTP 200 OK (8.4 KB PNG) | **PASS** |
| **Runtime JS** | `http://frontend:8080/assets/erpnext/js/ocm_branding.js` | HTTP 200 OK (2.0 KB JS) | **PASS** |
| **Runtime CSS** | `http://frontend:8080/assets/erpnext/css/ocm_branding.css` | HTTP 200 OK (1.7 KB CSS) | **PASS** |
| **Login Screen** | `http://frontend:8080/login` | `<img class="app-logo" src="/files/ocm_logo.png">` | **PASS** |
| **Login Favicon** | `http://frontend:8080/login` | `<link rel="icon" href="/files/ocm_favicon.png">` | **PASS** |
| **Loading Splash** | `desk.html` | `<img src="/files/ocm_splash.png">` | **PASS** |
| **Sidebar Subtitle** | Desk Header | `OCM` (Replaced "ERPNext") | **PASS** |
| **Sidebar Logo** | `.header-logo` | `/files/ocm_logo.png` | **PASS** |
| **Session Bootinfo** | All 10 Users + Admin | `app_title='OCM', parent_icon='OCM'` | **PASS** |

---

### SECTION 18: ORBISERP LOGIN SCREEN UI TRANSFORMATION (MOCKUP MATCH)

#### 1. Visual Design & Layout Architecture
The login screen interface was completely redesigned to strictly match the user-provided reference mockup (`media_1791466471924.png`):
- **Background**: Modern, clean off-white canvas (`#f8fafc`) with full viewport vertical and horizontal centering.
- **Top Brand Logo**:
  - Extracted the exact high-fidelity emblem (*"OrbisERP — Car Manufacturing ERP"*) with transparent background (`/files/orbis_login_logo.png`, 385×120 PNG).
  - Positioned centrally directly above the login card.
- **Login Card**:
  - Pure white container (`#ffffff`) with smooth rounded corners (`border-radius: 16px`), crisp border (`1px solid #e2e8f0`), and soft elevation shadow (`box-shadow: 0 4px 20px -2px rgba(0, 0, 0, 0.05)`).
  - Max width constrained to `440px`.
  - Header: Centered bold **"Sign In"** heading (`font-size: 22px; color: #0f172a;`) and subtitle *"Welcome! Please sign in to continue."* (`color: #64748b; font-size: 13.5px;`).
- **Input Fields**:
  - **Email**: Field label *"Email"*, envelope SVG stroke icon on the left, pill input box with placeholder `forw8007+salesmanager@gmail.com`.
  - **Password**: Field label *"Password"*, padlock SVG stroke icon on the left, masked bullet placeholder `••••••••••`, and interactive eye toggle SVG icon on the right.
  - **Forgot Password**: Right-aligned blue link *"Forgot password?"* (`#0284c7`) positioned directly beneath the password input.
- **Action Buttons**:
  - **Primary**: Deep dark navy button (`#0B132B`) displaying **"Continue &rarr;"** with smooth hover elevation and full-width border radius (`10px`).
  - **Secondary**: Light pill button (`#ffffff`, border `#e2e8f0`) displaying mail icon + *"Login with Email Link"*.
- **Distraction-Free**: Header navbars, breadcrumbs, footers, and signup prompts are completely hidden.

#### 2. Native Functional Architecture Preserved (Zero Functional Degradation)
To guarantee that 100% of ERPNext's native login capabilities, security checks, and session behaviors remain completely intact:
- Retained the exact standard Frappe form structure (`form.form-signin.form-login`), input identifiers (`#login_email`, `#login_password`), button classes (`btn`, `btn-sm`, `btn-primary`, `btn-block`, `btn-login`), and error banner containers (`.login-error-banner`).
- Preserved all standard sections (`for-login`, `for-email-login`, `for-forgot`, `for-login-with-email-link`, `for-signup`) to support forgot-password resets, email links, and LDAP authentication without breaking event handlers.
- Pure CSS styling and non-invasive top brand positioning were applied so that Frappe's client-side runtime script (`templates/includes/login/login.js`) executes with 100% accuracy.

#### 3. Live Functional Verification Matrix
| Test Case | Method / Target | Expected Behavior | Observed Result | Status |
| :--- | :--- | :--- | :--- | :--- |
| **DOM Element Structure** | `http://frontend:8080/login` | Form, inputs, error banners, and action buttons present | All standard IDs & classes mapped | **PASS** |
| **Admin Authentication** | POST `/api/method/login` | `{"message": "Logged In", "home_page": "desk"}` | HTTP 200 OK | **PASS** |
| **Business User Auth** | POST `/api/method/login` (`forw8007+salesmanager@gmail.com`) | Session cookie (`sid`) created, user logged in | HTTP 200 OK (`Ali Khan`) | **PASS** |
| **Desk Navigation** | GET `/desk` with session cookie | Desk loads successfully with user workspace | HTTP 200 OK (164 KB rendered) | **PASS** |
| **Invalid Credentials** | POST `/api/method/login` (bad password) | Return 401 with standard error payload | HTTP 401 (`Invalid credentials`) | **PASS** |







