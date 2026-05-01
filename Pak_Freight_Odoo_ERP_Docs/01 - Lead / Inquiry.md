# 01 - Lead / Inquiry

---

## 1. Overview
This is the first step in the shipping process. It begins when a customer asks for a freight quote. Customers contact us via WhatsApp, email, or phone. We use this stage to collect cargo and routing details. We also record compliance data like the NTN. This information helps us calculate an accurate price.
---

## 2. Odoo Technical Mapping
* **Base Model:** `crm.lead`
* **Inheritance:** Custom module (e.g., `freight_crm_extension`) will inherit `crm.lead` to add freight-specific and Pakistan-specific compliance fields.
* **Dependencies:** `crm`, `contacts`, `hr`, `whatsapp` (Phase 2).

---

## 3. Core Entities Involved
This stage uses two main data entities:

1. **Customer (`res.partner`):** The importer or exporter. We must record their NTN for FBR compliance. We check their ATL status to see if they are a Filer or Non-Filer. We also check their credit limit and overdue invoices.
2. **Sales Representative (`hr.employee` / `res.users`):** The person who owns the lead. Their performance is tracked against monthly targets.

---

## 4. Data Dictionary (Custom Fields on `crm.lead`)

To successfully process a freight inquiry, the following custom fields must be added to the `crm.lead` form view. 

| Field Label | Technical Name | Field Type | Description / Validation | Example Data |
| :--- | :--- | :--- | :--- | :--- |
| **Customer** | `partner_id` | Many2one | Links to `res.partner`. | `Al-Karam Textiles Ltd` |
| **NTN Number** | `x_ntn_number` | Char | Fetched from partner. Format: 7 digits + 1 check digit. | `1234567-8` |
| **Mode of Transport** | `x_freight_mode` | Selection | `Sea FCL`, `Sea LCL`, `Air`, `Land`. | `Sea FCL` |
| **Cargo Type** | `x_cargo_type` | Char/Selection | e.g., Garments, Surgical Goods, Auto Parts. | `Cotton Yarn` |
| **Total Weight** | `x_weight_kg` | Float | Gross weight in Kilograms (KGs). | `24,500.00` |
| **Total Volume** | `x_volume_cbm` | Float | Volume in Cubic Meters (CBM). Critical for LCL. | `68.5` |
| **Origin** | `x_origin_id` | Many2one | Links to `freight.location`. | `Ningbo, China (CNNGB)` |
| **Destination** | `x_dest_id` | Many2one | Links to `freight.location`. | `Port Qasim / QICT (PKBQM)` |
| **Target Rate** | `x_target_rate` | Monetary | The price the customer is asking for (optional). | `$ 1,450.00 USD` |

---

## 5. Real-World Example Scenario (Mock Data)

Here is an example of a completed Lead record:

* **Lead Name:** `Inquiry - 2x40HC Ningbo to QICT - Al-Karam`
* **Customer:** `Al-Karam Textiles Ltd`
* **Customer NTN:** `4210123-8`
* **ATL Status:** `Active (Filer)` *(System notes: Apply standard 1% WHT on freight later)*
* **Credit Status:** `OK - Available Limit: PKR 2,500,000`
* **Mode:** `Sea FCL`
* **Container Requirement:** `2 x 40ft HC`
* **Cargo:** `Textile Machinery Parts`
* **Weight:** `18,000 KGs`
* **Volume:** `110 CBM`
* **Origin:** `Ningbo, China`
* **Destination:** `QICT, Karachi`
* **Sales Rep:** `Ali Khan`

---

## 6. Business Rules & Automations

### A. Credit Limit & Aging Check (Risk Control)
* **Trigger:** When `partner_id` is selected on the lead.
* **Logic:** The system checks the credit limit and any invoices older than 90 days.
* **Action:** A warning banner appears if the limit is exceeded or payments are late.
* **Lock:** Users cannot create a quote without a Manager's Approval PIN if a warning exists.

### B. Tax Status Inheritance (FBR Compliance)
* **Trigger:** When `partner_id` is selected.
* **Logic:** The system gets the ATL status from the customer profile.
* **Action:** This status is saved to the lead. It ensures the correct tax rate is applied to the final quote.

### C. WhatsApp Auto-Acknowledgment (Phase 2)
* **Trigger:** Creating a new lead.
* **Logic:** The system uses the WhatsApp API.
* **Action:** It sends an automatic message to the customer. It thanks them for the inquiry and promises a quote soon.

---

## 7. User Roles & Access Rights

| Role | Access Level | Permissions |
| :--- | :--- | :--- |
| **Sales Rep** | User: Own Documents Only | Can create, read, and edit their own leads. Cannot edit customer credit limits or NTN verification status. |
| **Sales Manager** | User: All Documents | Can view and reassign all leads. Can override credit limit warnings to allow quoting. |
| **Finance / Admin** | Master Data Manager | Manages `res.partner` financial fields (Credit Limit, ATL status). Read-only access to leads. |

> **Audit Trail:** We must enable Odoo tracking on the lead. The system must log every change to the mode, weight, or customer. This is required for internal audits.

---

## 8. Next Steps / Workflow Transition
After gathering rates and verifying the customer:
1. The user clicks **"Create Quotation"**.
2. The system moves to **Stage 02: Quotation**.
3. All data copies to the new quote automatically. This prevents typing errors.