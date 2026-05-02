# 08 - B/L Issuance

---

## 1. Overview
This is the eighth step in the shipping process. It is the **"Ownership"** stage. Now that the ship has left the port, we issue the **Bill of Lading (B/L)**. 

Think of the B/L as a "Title Deed" or a "Property Receipt." Whoever holds the original B/L legally owns the goods. The shipping line gives us a **Master B/L (MBL)**, and we give our customer a **House B/L (HBL)**. Without this document, the customer cannot collect their cargo at the destination.

---

## 2. Odoo Technical Mapping
* **Base Model:** `freight.shipment` (The Job Order hub)
* **Custom Model:** `freight.bl` (To generate and store HBL or Air Waybill details)
* **Dependencies:** `base_setup` (to manage company logos and signatures on the PDF).

---

## 3. Core Entities Involved
This stage uses three main data entities:

1. **Shipping Line / Airline:** They issue the **Master B/L (MBL)** to us once the ship sails.
2. **Shipper:** The person sending the goods (usually our customer).
3. **Consignee:** The person receiving the goods at the destination. Their name must be exactly correct on the B/L.

---

## 4. Data Dictionary (B/L Fields)

The following details are printed on the official B/L document:

| Field Label | Technical Name | Field Type | Description | Example Data |
| :--- | :--- | :--- | :--- | :--- |
| **HBL Number** | `x_hbl_no` | Char | Our unique B/L reference. | `HBL-KHI-2026-0456` |
| **B/L Type** | `x_bl_type` | Selection | Original, Telex Release, or Waybill. | `Original` |
| **Issue Date** | `x_issue_date` | Date | When the B/L was signed. | `20-May-2026` |
| **Freight Status** | `x_freight_status`| Selection | Is the freight "Prepaid" or "Collect"? | `Prepaid` |
| **Place of Issue** | `x_issue_place` | Char | Usually the city of departure. | `Karachi, Pakistan` |
| **No. of Originals**| `x_originals_count`| Integer | Usually 3 originals are printed. | `3` |

---

## 5. Real-World Example Scenario (Mock Data)

Here is an example of a House B/L generated in Odoo:

* **Job Order:** `JO-2026-00456`
* **HBL Number:** `HBL-KHI-2026-0456`
* **Shipper:** `Al-Karam Textiles Ltd`
* **Consignee:** `Global Fashion UK Ltd`
* **Notify Party:** `Same as Consignee`
* **B/L Type:** `Original` (3 Paper copies printed)
* **Status:** `Issued & Dispatched to Client`

---

## 6. Business Rules & Automations

### A. The Matching Rule (Compliance Control)
* **Trigger:** Before the B/L can be "Validated."
* **Logic:** The weight, number of packages, and description on the B/L **must match** the GD (Stage 05) and the Packing List (Stage 04).
* **Action:** Odoo shows a **Red Warning** if the B/L weight is different from the GD weight. This prevents legal trouble at the destination port.

### B. The Payment Block (Financial Control)
* **Trigger:** When the user clicks "Print Original B/L."
* **Logic:** We should not give the customer the "Title Deed" if they haven't paid us.
* **Action:** The system **blocks printing** if the customer has an "Overdue Balance" or if the "Advance Payment" wasn't received. A Manager must override this.

### C. Telex Release Automation (Workflow Control)
* **Trigger:** If the B/L Type is set to "Telex Release."
* **Logic:** A Telex Release means no paper B/L is needed; it's all digital.
* **Action:** The system automatically adds a **"TELEX RELEASED"** watermark to the PDF and sends a secure email to the agent at the destination port.

---

## 7. User Roles & Access Rights

| Role | Access Level | Permissions |
| :--- | :--- | :--- |
| **Operations Exec** | User: Own Documents | Types the B/L details and generates the "Draft B/L" for the customer to check. |
| **Operations Manager** | User: All Documents | Reviews the draft and clicks "Final Issue." This generates the official HBL number. |
| **Finance Team** | Billing / Receipts | Confirms if the customer has paid before the B/L is released. |

---

## 8. Next Steps / Workflow Transition
Now that the customer has their ownership documents:
1. The system moves to **Stage 09: Transit Tracking**.
2. The ship is now at sea. We monitor its location.
3. We send "Status Updates" to the customer so they know when the ship will arrive.