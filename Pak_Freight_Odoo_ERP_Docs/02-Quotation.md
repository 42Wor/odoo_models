# 02 - Quotation

---

## 1. Overview
This is the second step in the shipping process. It begins after we have collected the customer's requirements in the Lead stage. In this stage, we calculate our costs (buying rate from the shipping line) and add our profit margin to create a selling price. We then generate a PDF quote and send it to the customer. Quotes are usually valid for 3 to 7 days because shipping prices change quickly.

example for pdf [freight-quotation](freight-quotation-form.pdf)

---

## 2. Odoo Technical Mapping
* **Base Model:** `sale.order` (or a custom `freight.quote` model)
* **Inheritance:** Custom module (e.g., `freight_quote_extension`) will inherit `sale.order` to add freight-specific pricing, buying rates, and FX (foreign exchange) tracking.
* **Dependencies:** `sale`, `crm`, `currency` (for USD to PKR conversion).

---

## 3. Core Entities Involved
This stage uses three main data entities:

1. **Customer (`res.partner`):** The person receiving the quote. Their tax status (Filer/Non-Filer) determines the tax added to the quote.
2. **Shipping Line / Airline (`res.partner`):** The carrier (like Maersk or Emirates) that gives us the base buying rate for the container or air freight.
3. **Sales Representative (`hr.employee` / `res.users`):** The person who builds the quote, sets the profit margin, and sends the PDF to the customer.

---

## 4. Data Dictionary (Custom Fields on `sale.order`)

To successfully build a freight quote, the following custom fields must be added to the quotation form view.

| Field Label | Technical Name | Field Type | Description / Validation | Example Data |
| :--- | :--- | :--- | :--- | :--- |
| **Lead Reference** | `opportunity_id` | Many2one | Links back to the original Lead. | `Inquiry - 2x40HC Ningbo` |
| **Validity Date** | `validity_date` | Date | The date the quote expires. | `15-Oct-2025` |
| **Buying Rate** | `x_buy_rate` | Monetary | Our cost from the shipping line. | `$ 1,200.00 USD` |
| **Selling Rate** | `x_sell_rate` | Monetary | The price we charge the customer. | `$ 1,350.00 USD` |
| **Profit Margin** | `x_margin` | Monetary | Auto-calculated (Sell - Buy). | `$ 150.00 USD` |
| **Exchange Rate** | `x_fx_rate` | Float | The USD to PKR rate on that day. | `278.50` |
| **WHT Amount** | `x_wht_amount` | Monetary | Withholding tax based on ATL status. | `PKR 3,759` (1% Filer) |
| **Quote Version** | `x_quote_version` | Integer | Tracks revisions (v1, v2, v3). | `v2` |

---

## 5. Real-World Example Scenario (Mock Data)

Here is an example of a completed Quotation record:

* **Quote Number:** `QT-2025-00123`
* **Customer:** `Al-Karam Textiles Ltd`
* **Validity:** `3 Days (Expires Oct 15)`
* **Carrier:** `COSCO Shipping`
* **Buying Rate:** `$ 1,200 USD`
* **Selling Rate:** `$ 1,350 USD`
* **Exchange Rate:** `1 USD = 278.50 PKR`
* **Total in PKR:** `PKR 375,975`
* **WHT (1% Filer):** `Applied automatically`
* **Version:** `v1`
* **Status:** `Sent to Customer`

---

## 6. Business Rules & Automations

### A. FX Rate Snapshot (Finance Protection)
* **Trigger:** When the quote is created.
* **Logic:** The system fetches today's USD to PKR exchange rate.
* **Action:** It locks this specific exchange rate into the quote. This protects our profit margin if the currency value changes tomorrow.

### B. Quote Versioning (Audit Control)
* **Trigger:** When a customer asks for a discount and the Sales Rep changes the price.
* **Logic:** Instead of deleting the old price, the system saves the new price as "Version 2" (v2).
* **Action:** It keeps a history of all versions. We can always see exactly which version the customer finally accepted.

### C. Soft Lock (Risk Control)
* **Trigger:** When the quote is marked as "Sent".
* **Logic:** The system locks the routing details (Origin, Destination, Mode).
* **Action:** The Sales Rep cannot change the ports or the container size without creating a new version.
* **Lock:** A Manager's Approval PIN is required to unlock and edit a sent quote.

---

## 7. User Roles & Access Rights

| Role | Access Level | Permissions |
| :--- | :--- | :--- |
| **Sales Rep** | User: Own Documents Only | Can create and send quotes. Cannot approve discounts that drop the profit margin below the company minimum. |
| **Sales Manager** | User: All Documents | Can view all quotes. Can approve low-margin quotes and unlock "Soft Locks". |
| **Finance / Admin** | Master Data Manager | Manages the daily FX (exchange) rates and tax rules. Cannot create quotes. |

> **Audit Trail:** We must enable Odoo tracking on the quote. The system must log every change to the Selling Rate, Buying Rate, and Profit Margin. If a price is lowered, the system records who lowered it and when.

---

## 8. Next Steps / Workflow Transition
After the customer reviews the PDF quote:
1. The customer agrees to the price.
2. The user clicks **"Confirm Booking"**.
3. The system moves to **Stage 03: Booking**.
4. A central Job Order number (e.g., `JO-2025-XXXX`) is automatically created, and the space is booked with the shipping line.