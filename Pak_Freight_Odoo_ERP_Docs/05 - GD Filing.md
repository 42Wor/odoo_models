# 05 - GD Filing

---

## 1. Overview
This is the fifth step in the shipping process and is often called the **"Point of No Return."** In this stage, the Clearing Agent files the official **Goods Declaration (GD)** with Pakistan Customs using the government's WeBOC or PSW system. 

This is a legal declaration of what is being shipped, how much it weighs, and what it is worth. Once this is filed, the government assigns a unique **GD Number**. In our Odoo system, entering this number triggers a "Hard Lock" to ensure our records match the government records exactly.

---

## 2. Odoo Technical Mapping
* **Base Model:** `freight.shipment` (The Job Order hub)
* **Custom Model:** `freight.declaration` (To track the specific customs filing details)
* **Dependencies:** `psw_integration` (Phase 2 API) or manual entry for Phase 1.

---

## 3. Core Entities Involved
This stage uses three main data entities:

1. **Clearing Agent (`res.partner`):** A licensed professional who has the authority to file the GD on behalf of the customer.
2. **Pakistan Customs / FBR:** The government body that receives the filing and decides if the cargo is allowed to enter or leave the country.
3. **PSW / WeBOC:** The official government software portals where the GD is actually typed and submitted.

---

## 4. Data Dictionary (Customs Filing Fields)

When the GD is filed, the following information must be recorded in Odoo:

| Field Label | Technical Name | Field Type | Description | Example Data |
| :--- | :--- | :--- | :--- | :--- |
| **GD Number** | `x_gd_number` | Char | The official ID from Customs. | `KAPE-HC-2026-123456` |
| **Filing Date** | `x_gd_date` | Date | The date the GD was submitted. | `12-May-2026` |
| **Declared Value** | `x_declared_value`| Monetary | The total value reported to FBR. | `$ 25,000.00` |
| **Net Weight** | `x_net_weight` | Float | The actual weight of the goods. | `17,850 KGs` |
| **NTN Verified** | `x_ntn_status` | Boolean | Confirms the NTN matches the GD. | `True` |
| **Agent Name** | `x_agent_id` | Many2one | The specific agent who filed it. | `FastTrack Clearing Ltd` |

---

## 5. Real-World Example Scenario (Mock Data)

Here is an example of a Job Order that has just been filed:

* **Job Order:** `JO-2026-00456`
* **GD Number:** `KAPE-HC-2026-123456`
* **Filing Status:** `Submitted`
* **Declared Value:** `$ 25,000.00`
* **Clearing Agent:** `FastTrack Clearing Ltd`
* **System Note:** *GD Lock is now ACTIVE. Invoice and Cargo details are read-only.*

---

## 6. Business Rules & Automations

### A. The GD LOCK (Critical Control)
* **Trigger:** When the `x_gd_number` is saved in Odoo.
* **Logic:** The system assumes the legal filing is finished.
* **Action:** Odoo immediately **locks** the following fields: Customer Name, HS Code, Cargo Weight, and Invoice Value. 
* **Why:** If you change these in Odoo but not in the government system, you will fail a government audit. Only a **Director** can unlock this with a special override.

### B. NTN Consistency Check (Compliance)
* **Trigger:** Before saving the GD Number.
* **Logic:** The system checks if the NTN on the Job Order matches the NTN registered on the customer's profile.
* **Action:** If they don't match, the system shows a **Red Alert**. Filing with the wrong NTN can lead to the cargo being seized by customs.

### C. Amendment Alert (Workflow Control)
* **Trigger:** If a user tries to change a locked field.
* **Logic:** The system detects the GD Lock is active.
* **Action:** It forces the user to create an **"Amendment Request."** This records *why* the change is needed (e.g., "Typo in weight") and requires a manager's signature.

---

## 7. User Roles & Access Rights

| Role | Access Level | Permissions |
| :--- | :--- | :--- |
| **Clearing Agent** | External / Portal | Can enter the GD Number and Filing Date. Cannot see the company's profit margins. |
| **Operations Exec** | User: Own Documents | Can view the GD details. Cannot edit any fields once the GD Lock is active. |
| **Director / Admin** | Super User | The only person who can "Unlock" a GD to fix a major mistake. |

> **Audit Trail:** Every GD filing is logged. If a GD is amended, Odoo keeps the old version and the new version so you can show the history to a customs officer if they ask.

---

## 8. Next Steps / Workflow Transition
Now that the government has our paperwork:
1. The system moves to **Stage 06: Customs Clearance**.
2. We wait for the government's "Risk Engine" to assign a channel (**Green, Yellow, or Red**).
3. The Clearing Agent monitors the status to see if the cargo needs a physical inspection.