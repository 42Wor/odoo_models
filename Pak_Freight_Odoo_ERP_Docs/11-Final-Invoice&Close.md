# 11 - Final Invoice & Close

---

## 1. Overview
This is the eleventh and **final step** in the shipping process. It is the **"Payday"** stage. The cargo has been delivered, and the POD is signed. Now, we do three things:
1. Send the final bill (Invoice) to the customer.
2. Pay our partners (Shipping lines, truckers, and agents).
3. Calculate exactly how much profit we made on this job.

Once the money is settled, we **Close** the Job Order. This locks the record forever so that no one can change the numbers later.

---

## 2. Odoo Technical Mapping
* **Base Model:** `account.move` (Odoo’s standard Invoice/Bill model).
* **Job State:** `state = closed` (Archived).
* **Dependencies:** `l10n_pk_einvoice` (The mandatory FBR e-invoicing system for Pakistan).

---

## 3. Core Entities Involved
This stage brings everyone together for the final settlement:

1. **Customer:** They receive the final invoice and pay the remaining balance.
2. **Vendors:** The Shipping Line, Transporter, and Clearing Agent who send us their bills.
3. **FBR (Federal Board of Revenue):** Every invoice must be reported to the FBR in real-time via their digital system.
4. **Sales Representative:** They receive their commission based on the final profit of the job.

---

## 4. Data Dictionary (Finance & Closing Fields)

We use these fields to see the final financial health of the shipment:

| Field Label | Technical Name | Field Type | Description | Example Data |
| :--- | :--- | :--- | :--- | :--- |
| **Final Invoice** | `x_invoice_id` | Many2one | The bill sent to the customer. | `INV-2026-0882` |
| **Total Revenue** | `x_total_revenue`| Monetary | Total money the customer owes us. | `PKR 550,000` |
| **Total Costs** | `x_total_costs` | Monetary | Total we must pay to vendors. | `PKR 470,000` |
| **Net Profit** | `x_net_profit` | Monetary | Revenue minus Costs. | `PKR 80,000` |
| **FBR QR Code** | `x_fbr_qr` | Image | Proof the invoice is registered. | `[QR Code Image]` |
| **Close Date** | `date_closed` | Date | When the job was archived. | `15-Jun-2026` |

---

## 5. Real-World Example Scenario (Mock Data)

Here is the final "Profit & Loss" for our textile shipment:

* **Job Order:** `JO-2026-00456`
* **Customer Bill:** `PKR 550,000` (Includes Freight + Handling + Taxes)
* **Vendor Bills:** 
    * *Shipping Line:* `PKR 380,000`
    * *Trucking:* `PKR 45,000`
    * *Clearing Agent:* `PKR 45,000`
* **Total Profit:** `PKR 80,000`
* **Sales Commission (5%):** `PKR 4,000`
* **Status:** `Closed & Locked`

---

## 6. Business Rules & Automations

### A. FBR E-Invoicing (Legal Requirement)
* **Trigger:** When the user clicks "Confirm Invoice."
* **Logic:** Pakistan law (SRO 1852) requires all freight invoices to be sent to the FBR digitally.
* **Action:** Odoo sends the data to the FBR system and receives a **QR Code**. This QR code is automatically printed on the customer's invoice. Without this, the invoice is not legal.

### B. The Profit Warning (Management Control)
* **Trigger:** Before the Job Order can be "Closed."
* **Logic:** We should never lose money on a shipment without knowing why.
* **Action:** If the `x_net_profit` is **Zero or Negative**, the system blocks the "Close" button. A Director must review the costs and type in a reason (e.g., "Agreed discount") to allow the job to close.

### C. The Hard Lock (Audit Protection)
* **Trigger:** When the status is changed to "Closed."
* **Logic:** Once a job is finished and the profit is calculated, no one should be able to change the data.
* **Action:** The system makes the entire Job Order **Read-Only**. No one (not even the manager) can change the weights, dates, or prices. This ensures our records are 100% safe for tax audits.

---

## 7. User Roles & Access Rights

| Role | Access Level | Permissions |
| :--- | :--- | :--- |
| **Finance Team** | Billing / Accounting | Creates the final invoice, records vendor bills, and verifies the FBR QR code. |
| **Sales Rep** | User: Own Documents | Can see their final profit and the commission they earned. Cannot edit the bills. |
| **Director** | Super User | The only person who can approve a "Loss-Making" job or re-open a closed job in an emergency. |

---

## 8. The End of the Journey
Congratulations! The shipment is now complete.
1. The customer has their goods.
2. The vendors are paid.
3. The company has its profit.
4. The data is safely stored in Odoo for future reports and FBR audits. 

**This concludes the 11-stage workflow for your Pakistan Freight Forwarding ERP.**