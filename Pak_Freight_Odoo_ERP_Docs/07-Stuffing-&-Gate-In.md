# 07 - Stuffing & Gate-In

---

## 1. Overview
This is the seventh step in the shipping process. It is the "Physical" stage. For exports, this is when the goods are loaded into the container (**Stuffing**) and the container is delivered to the port (**Gate-In**). For imports, it tracks when the container is moved from the ship to the terminal or an off-dock yard.

In this stage, we record the physical identity of the shipment: the **Container Number** and the **Seal Number**. We also record the **VGM** (Verified Gross Mass), which is a legal requirement to prove the total weight of the container before it is loaded onto a ship.

---

## 2. Odoo Technical Mapping
* **Base Model:** `freight.shipment` (The Job Order hub)
* **Custom Model:** `freight.container` (To track individual container details)
* **Dependencies:** `stock` (if managing warehouse stuffing) or custom logistics fields.

---

## 3. Core Entities Involved
This stage uses three main data entities:

1. **Transporter (`res.partner`):** The trucking company that moves the container from the factory/warehouse to the port.
2. **Terminal (KICT / QICT / SAPT):** The specific area at the Karachi port where the container is stored before loading.
3. **Off-Dock Terminal (AICT / PSCS / MTO):** Private yards outside the main port where containers are often stuffed or stored to avoid port congestion.

---

## 4. Data Dictionary (Physical Tracking Fields)

The following details must be entered to track the physical container:

| Field Label | Technical Name | Field Type | Description | Example Data |
| :--- | :--- | :--- | :--- | :--- |
| **Container No.** | `x_container_no` | Char | The unique ID on the box. | `MSCU1234567` |
| **Seal Number** | `x_seal_no` | Char | The plastic/metal lock ID. | `PK123456` |
| **Container Size** | `x_size_id` | Selection | 20ft, 40ft, or 40ft High Cube. | `40ft HC` |
| **VGM Weight** | `x_vgm_weight` | Float | Total weight (Goods + Box). | `28,450 KGs` |
| **Gate-In Date** | `x_gate_in` | DateTime | When it entered the port. | `18-May-2026 14:00` |
| **Terminal Name** | `x_terminal_id` | Many2one | Where the container is sitting. | `QICT - Port Qasim` |

---

## 5. Real-World Example Scenario (Mock Data)

Here is an example of a container that has just reached the port:

* **Job Order:** `JO-2026-00456`
* **Container ID:** `MSCU1234567`
* **Seal ID:** `PK123456`
* **VGM Status:** `Submitted & Verified`
* **Transporter:** `Lucky Trucking Co.`
* **Gate-In Status:** `Completed at QICT`
* **System Note:** *Container is now inside the port. Ready for loading onto the vessel.*

---

## 6. Business Rules & Automations

### A. The VGM Requirement (Safety Rule)
* **Trigger:** Before the user can mark the shipment as "Gate-In."
* **Logic:** International law (SOLAS) says every container must have a verified weight (VGM).
* **Action:** Odoo **blocks** the Gate-In status if the `x_vgm_weight` field is empty. This prevents the ship from leaving without knowing the weight.

### B. Seal Number Lock (Security Control)
* **Trigger:** Once the Gate-In date is entered.
* **Logic:** Once a container is in the port, the seal should not be changed.
* **Action:** The system **locks** the `x_seal_no` field. If the seal is broken or changed, it must be reported as a "Security Incident" in the Odoo chatter.

### C. Off-Dock Transfer Alert (Location Tracking)
* **Trigger:** If the terminal is changed from a main port (QICT) to an off-dock (AICT).
* **Logic:** Off-dock terminals charge extra daily fees.
* **Action:** The system shows a **Yellow Warning**: *"Cargo moved to Off-Dock. Daily storage charges may increase. Please notify the customer."*

---

## 7. User Roles & Access Rights

| Role | Access Level | Permissions |
| :--- | :--- | :--- |
| **Operations Exec** | User: Own Documents | Enters the Container Number, Seal Number, and Gate-In time. |
| **Transporter** | External / App | Can use a mobile app to upload a photo of the "Gate-In Slip" directly to Odoo. |
| **Operations Manager** | User: All Documents | Verifies the VGM weight and ensures the container is at the correct terminal. |

> **Audit Trail:** Odoo tracks the time between "Stuffing" and "Gate-In." If it takes more than 24 hours, the system flags it as a "Delay," helping the manager see if the trucking company is slow.

---

## 8. Next Steps / Workflow Transition
Once the container is safely inside the port:
1. The system moves to **Stage 08: [B/L Issuance](08-BL-Issuance.md)**.
2. The shipping line confirms the container is on the ship.
3. We prepare the **Bill of Lading (B/L)**, which is the "Title Deed" or ownership document for the goods.