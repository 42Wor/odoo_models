# 04 - Pre-shipment Docs

---

## 1. Overview
This is the fourth step in the shipping process. It is all about paperwork. Before the cargo can be loaded onto a ship or cleared by customs, we must collect and verify several official documents. 

In this stage, the system acts as a **Checklist**. We ensure that the Commercial Invoice, Packing List, and other required certificates are uploaded and correct. If the paperwork is wrong, the shipment will be stopped at the port, and the customer might face heavy fines from the FBR (Federal Board of Revenue).

---

## 2. Odoo Technical Mapping
* **Base Model:** `freight.shipment` (The Job Order hub)
* **Document Model:** `ir.attachment` (Standard Odoo files) linked to a custom `freight.document.checklist` model.
* **Dependencies:** `document` (Odoo's document management app).

---

## 3. Core Entities Involved
This stage uses three main data entities:

1. **Customer (`res.partner`):** They provide the Commercial Invoice and Packing List.
2. **Authorized Bank (`res.partner`):** The bank issues the **E-Form** (now digital via PSW). This is a mandatory document in Pakistan for all exports and imports.
3. **Chamber of Commerce (`res.partner`):** They issue the **Certificate of Origin (COO)**, which proves where the goods were made.

---

## 4. Data Dictionary (Document Checklist)

The system tracks the status of each document. A document can be **Missing**, **Uploaded**, or **Verified**.

| Document Name | Technical Name | Required? | Description | Example Data |
| :--- | :--- | :--- | :--- | :--- |
| **Comm. Invoice** | `doc_ci` | **Yes** | Shows the value of the goods. | `INV-ALKARAM-99` |
| **Packing List** | `doc_pl` | **Yes** | Shows weight, boxes, and sizes. | `PL-ALKARAM-99` |
| **HS Code** | `x_hs_code` | **Yes** | The 8-digit code for the product type. | `5205.1100` (Cotton Yarn) |
| **Bank E-Form** | `doc_eform` | **Yes** | Digital bank approval via PSW. | `E-2026-BANK123` |
| **Cert. of Origin** | `doc_coo` | Optional | Proves goods are from Pakistan. | `KCCI-COO-556` |
| **Insurance Cert** | `doc_ins` | Optional | Proof the cargo is insured. | `EFU-INS-778` |

---

## 5. Real-World Example Scenario (Mock Data)

Here is an example of the Document Checklist for our textile shipment:

* **Job Order:** `JO-2026-00456`
* **HS Code Verified:** `5205.1100` (Cotton Yarn - 0% Duty)
* **Commercial Invoice:** `Uploaded & Verified` (Total Value: $25,000)
* **Packing List:** `Uploaded` (Total Weight: 18,000 KGs)
* **Bank E-Form:** `Verified via PSW API`
* **Certificate of Origin:** `Missing` (System sends a reminder to the customer)
* **Status:** `Waiting for Documents`

---

## 6. Business Rules & Automations

### A. HS Code Verification (Customs Protection)
* **Trigger:** When the HS Code is entered.
* **Logic:** The system checks the code against the official Pakistan Customs Tariff.
* **Action:** It displays the expected duty rates. If the code is invalid or high-risk, it flags the shipment for a "Manager Review" to prevent fines later.

### B. Value Mismatch Alert (Finance Protection)
* **Trigger:** When the Commercial Invoice is uploaded and the value is typed in.
* **Logic:** The system compares the Invoice Value ($25,000) to the original Quote Value ($24,800).
* **Action:** If the difference is more than 5%, the system triggers a warning. This ensures we are billing the customer correctly based on the actual goods being shipped.

### C. The "Gatekeeper" Rule (Workflow Control)
* **Trigger:** When the user tries to move to Stage 05 (GD Filing).
* **Logic:** The system checks if all "Mandatory" documents are marked as **Verified**.
* **Action:** The system **blocks** the user from moving forward if the Invoice, Packing List, or E-Form is missing. You cannot file customs without these.

---

## 7. User Roles & Access Rights

| Role | Access Level | Permissions |
| :--- | :--- | :--- |
| **Operations Exec** | User: Own Documents | Uploads files and marks them as "Uploaded". Cannot mark them as "Verified". |
| **Operations Manager** | User: All Documents | Reviews the uploaded files. They are the only ones who can click "Verified" to unlock the next stage. |
| **Customer** | Portal Access | Can log in to the Odoo Portal to upload their own Invoice and Packing List directly. |

> **Audit Trail:** Every time a document is uploaded or deleted, Odoo records the user's name and the time. This is critical if a document is lost or if the wrong version is sent to customs.

---

## 8. Next Steps / Workflow Transition
Once the checklist is 100% complete and verified:
1. The Operations Manager clicks **"Ready for Filing"**.
2. The system moves to **Stage 05: [GD Filing](05-GD-Filing.md)**.
3. The data is now ready to be sent to the **Clearing Agent** to file the Goods Declaration (GD) on the government's WeBOC/PSW system.