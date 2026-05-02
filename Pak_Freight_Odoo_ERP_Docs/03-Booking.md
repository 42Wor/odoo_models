


# 03 - Booking

---

## 1. Overview
This is the third step in the shipping process. It begins after the customer accepts our Quotation. In this stage, we officially book space on a ship or airplane with the carrier (like Maersk or Emirates). 

The system creates a central **Job Order (JO)**. This Job Order becomes the "hub" for everything else—all documents, invoices, and tracking will be linked to this JO. We also collect an advance payment (usually 30-50%) from the customer and start tracking the "Free Time" to avoid expensive demurrage penalties at the port.




| Document Name | Odoo Field/Link | Type | Description |
| :--- | :--- | :--- | :--- |
| **Carrier Booking Note** | `x_carrier_note_ids` | File (PDF) | The "ticket" for the container. |
| **Booking Confirmation** | `x_internal_bc_ids` | File (PDF) | Our summary sent to the client. |
| **Payment Receipt** | `x_payment_receipt` | File (PDF/Image) | Proof of the bank transfer (IBFT). |
| **VGM Instructions** | `x_vgm_draft` | File (PDF) | Weight details (needed for sea freight). |

---

## 2. Odoo Technical Mapping
* **Base Model:** `freight.shipment` (Custom core model)
* **State:** `state = booked`
* **Dependencies:** `sale` (to link the quote), `account` (to log the advance payment), `freight` (custom module).

---

## 3. Core Entities Involved
This stage uses four main data entities:

1. **Job Order (`freight.shipment`):** The central record for the entire shipment. It connects the customer, the cargo, the money, and the documents.
2. **Shipping Line / Airline (`res.partner`):** The carrier we are buying space from.
3. **Vessel / Flight (`freight.vessel`):** The specific ship and voyage number, or the flight number carrying the cargo.
4. **Container (`freight.container`):** The physical box (for sea freight). We record the size (20ft/40ft) and the allowed free days.

---

## 4. Data Dictionary (Custom Fields on `freight.shipment`)

To successfully manage a booking, the following fields are used on the Job Order form:

| Field Label | Technical Name | Field Type | Description / Validation | Example Data |
| :--- | :--- | :--- | :--- | :--- |
| **Job Order No.** | `name` | Char | Auto-generated central ID. | `JO-2026-00456` |
| **Quote Reference** | `quote_id` | Many2one | Links back to the accepted Quote. | `QT-2026-00123` |
| **Carrier Booking Ref** | `x_carrier_ref` | Char | The official booking number from the shipping line. | `COSU123456789` |
| **Vessel & Voyage** | `x_vessel_id` | Many2one | The ship carrying the cargo. | `COSCO STAR v.045W` |
| **ETD (Departure)** | `x_etd` | Date | Estimated Time of Departure. | `10-May-2026` |
| **ETA (Arrival)** | `x_eta` | Date | Estimated Time of Arrival. | `05-Jun-2026` |
| **Advance Payment** | `x_advance_amount` | Monetary | The 30-50% deposit paid by the customer. | `PKR 150,000` |
| **Free Days** | `x_free_days` | Integer | Number of days before port demurrage charges begin. | `14` |

---

## 5. Real-World Example Scenario (Mock Data)

Here is an example of a completed Booking (Job Order) record:

* **Job Order:** `JO-2026-00456`
* **Customer:** `Al-Karam Textiles Ltd`
* **Carrier:** `COSCO Shipping`
* **Carrier Booking Ref:** `COSU123456789`
* **Vessel / Voyage:** `COSCO STAR v.045W`
* **ETD (Ningbo):** `10-May-2026`
* **ETA (QICT):** `05-Jun-2026`
* **Advance Received:** `PKR 150,000 (Paid via IBFT)`
* **Container Size:** `2 x 40ft HC`
* **Free Time:** `14 Days`
* **Status:** `Booked`

---

## 6. Business Rules & Automations

### A. Job Order Hub Creation (Data Flow)
* **Trigger:** When the Quote is confirmed.
* **Logic:** The system automatically creates the `freight.shipment` (Job Order) record.
* **Action:** It copies the customer name, NTN, weight, volume, and ports from the Quote directly into the Job Order. Nobody has to type this information again.

### B. Advance Payment & Soft Lock (Risk Control)
* **Trigger:** When the booking is confirmed with the carrier.
* **Logic:** The system checks if the 30-50% advance payment has been logged by the Finance team.
* **Action:** Once the advance is received, a **Soft Lock** activates. The customer name, routing, and rates are frozen. 
* **Lock:** Operations staff cannot change these core details without a Manager's Approval PIN.

### C. Demurrage Countdown (Risk Alert)
* **Trigger:** When the ETA and Free Days are entered.
* **Logic:** The system calculates the exact date when expensive port penalties (demurrage) will start.
* **Action:** It schedules automatic WhatsApp and email alerts for T-3, T-2, and T-1 days before the free time expires, warning the team and the customer to hurry up.

---

## 7. User Roles & Access Rights

| Role | Access Level | Permissions |
| :--- | :--- | :--- |
| **Operations Exec** | User: Own Documents | Enters the Carrier Booking Reference, Vessel details, ETD, and ETA. Cannot change the pricing. |
| **Finance Team** | Billing / Receipts | Logs the advance payment into the system. This action triggers the Soft Lock. |
| **Operations Manager** | User: All Documents | Can view all Job Orders. Can use their PIN to unlock the Soft Lock if a major change is needed (like a vessel delay). |

> **Audit Trail:** The system logs exactly when the booking was confirmed and when the advance payment was received. Any changes to the ETD or ETA are recorded in the history log with the user's name.

---

## 8. Next Steps / Workflow Transition
Now that the space is booked and the ship is scheduled:
1. The Operations team moves to **Stage 04: [Pre-shipment](04-Pre-shipment.md)**.
2. The system generates a checklist of required paperwork (Commercial Invoice, Packing List, Certificate of Origin, Bank E-Form).
3. The customer must upload these documents before the cargo can be loaded or cleared through customs.