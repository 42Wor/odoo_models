# 06 - Customs Clearance

---

## 1. Overview
This is the sixth step in the shipping process. Now that the GD is filed, we wait for Pakistan Customs to review it. The government uses a "Risk Engine" to decide how closely they want to check our cargo. 

The cargo is assigned to one of three **Channels**: Green, Yellow, or Red. Our goal in this stage is to pay the required duties (taxes) and get the "Out of Charge" (OOC) note, which is the official permission to move the cargo out of the port.

---

## 2. Odoo Technical Mapping
* **Base Model:** `freight.shipment` (The Job Order hub)
* **Custom Model:** `freight.declaration.status` (To track the movement through customs channels)
* **Dependencies:** `account` (to record the duty payments to the government).

---

## 3. Core Entities Involved
This stage uses three main data entities:

1. **FBR / Customs Appraiser:** The government officer who reviews the documents (for Yellow Channel) and decides if the value of the goods is correct.
2. **Customs Examiner:** The officer who physically opens the container (for Red Channel) to count the items.
3. **1Bill / 1Link:** The electronic payment system used in Pakistan to pay customs duties and taxes.

---

## 4. Data Dictionary (Clearance Fields)

We track the progress of the clearance using these fields:

| Field Label | Technical Name | Field Type | Description | Example Data |
| :--- | :--- | :--- | :--- | :--- |
| **Channel** | `x_channel` | Selection | The path assigned by the system. | `Yellow Channel` |
| **Duty Amount** | `x_duty_total` | Monetary | Total taxes (CD, ST, ACD, RD). | `PKR 450,000` |
| **Payment Status** | `x_payment_status`| Selection | Has the duty been paid? | `Paid` |
| **PSID Number** | `x_psid_no` | Char | The ID used to pay the duty. | `100023456789` |
| **Examination Date**| `x_exam_date` | Date | When the physical check happened. | `14-May-2026` |
| **Out of Charge** | `x_ooc_date` | Date | The date the cargo was released. | `16-May-2026` |

---

## 5. Real-World Example Scenario (Mock Data)

Here is an example of a shipment going through the **Yellow Channel**:

* **Job Order:** `JO-2026-00456`
* **Assigned Channel:** `Yellow` (Document Review)
* **Appraiser Note:** *"Value accepted. Please pay duties."*
* **Total Duties:** `PKR 450,000`
* **Payment Method:** `1Bill (Online)`
* **Status:** `Duties Paid - Awaiting Release`
* **Final Release:** `Out of Charge (OOC) Granted`

---

## 6. Business Rules & Automations

### A. The Channel Dashboard (Operations Control)
* **Trigger:** When the `x_channel` is selected.
* **Logic:** The system categorizes the shipment on the main dashboard.
* **Action:** 
    * **Green:** Moves to "Ready for Delivery" immediately.
    * **Yellow:** Flags for "Document Review" (usually takes 1-2 days).
    * **Red:** Flags for "Physical Examination" (usually takes 3-7 days).

### B. Duty Payment Verification (Finance Control)
* **Trigger:** When the user marks duties as "Paid."
* **Logic:** The system requires the user to upload the **Duty Challan** (receipt) and enter the **PSID Number**.
* **Action:** It notifies the Finance team to verify that the money has left the company bank account.

### C. Examination Alert (Risk Management)
* **Trigger:** If a shipment is assigned to the **Red Channel**.
* **Logic:** Red channel means the container will be opened. This increases the risk of damage or theft.
* **Action:** The system sends an automatic WhatsApp to the customer: *"Your shipment has been marked for physical examination by Customs. This may add 3-5 days to the delivery time."*

---

## 7. User Roles & Access Rights

| Role | Access Level | Permissions |
| :--- | :--- | :--- |
| **Clearing Agent** | External / Portal | Updates the Channel status and enters the Examination Date. |
| **Finance Team** | Billing / Receipts | Enters the final Duty Amount and verifies the payment. |
| **Operations Exec** | User: Own Documents | Monitors the status to coordinate the truck for delivery. |

> **Audit Trail:** Odoo records exactly how long the shipment stayed in each channel. If a shipment stays in "Yellow" for more than 3 days, the system highlights it in **Red** so the manager can call the agent.

---

## 8. Next Steps / Workflow Transition
Once the "Out of Charge" (OOC) is granted:
1. The system moves to **Stage 07: Stuffing & Gate-In**.
2. The cargo is now legally free. We coordinate with the **Transporter** to pick up the goods from the port or terminal.
3. We prepare the **Delivery Order (DO)**.