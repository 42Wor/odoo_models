# 10 - Delivery & POD

---

## 1. Overview
This is the tenth step in the shipping process. It is the **"Final Mile"** stage. The cargo has arrived at the port and is cleared by customs. Now, we move the goods from the port to the customer’s warehouse.

The most important part of this stage is the **POD (Proof of Delivery)**. This is a document signed by the customer confirming they received the goods in good condition. In our Odoo system, uploading the POD is the "Key" that unlocks the final invoice.

---

## 2. Odoo Technical Mapping
* **Base Model:** `freight.shipment` (The Job Order hub)
* **Custom Model:** `freight.delivery` (To track truck and driver details)
* **Dependencies:** `stock.picking` (Odoo’s delivery system) and `mobile` (for the driver app).

---

## 3. Core Entities Involved
This stage uses three main data entities:

1. **Transporter:** The trucking company providing the vehicle.
2. **Driver:** The specific person driving the truck. We must record their **CNIC (ID Card Number)** for security.
3. **Consignee:** The customer receiving the goods. They must sign the POD.

---

## 4. Data Dictionary (Delivery Fields)

We record these details to ensure the cargo reaches the right place safely:

| Field Label | Technical Name | Field Type | Description | Example Data |
| :--- | :--- | :--- | :--- | :--- |
| **DO Number** | `x_do_no` | Char | Delivery Order ID. | `DO-KHI-2026-099` |
| **Truck Number** | `x_truck_no` | Char | The license plate of the truck. | `ABC-123-KHI` |
| **Driver Name** | `x_driver_name` | Char | Name of the person driving. | `Ahmed Ali` |
| **Driver CNIC** | `x_driver_cnic` | Char | Pakistani National ID Number. | `42101-1234567-1` |
| **Delivery Date** | `x_delivery_date`| DateTime | When the goods reached the warehouse. | `08-Jun-2026 11:30` |
| **POD Upload** | `x_pod_file` | Binary | A photo or scan of the signed POD. | `pod_signed.jpg` |

---

## 5. Real-World Example Scenario (Mock Data)

Here is an example of a completed delivery:

* **Job Order:** `JO-2026-00456`
* **Delivery Order:** `DO-KHI-2026-099`
* **Truck:** `ABC-123-KHI` (Flatbed Trailer)
* **Driver:** `Ahmed Ali (CNIC: 42101-1234567-1)`
* **Status:** `Delivered`
* **POD Status:** `Uploaded & Verified`
* **Condition:** `Clean (No damages reported)`

---

## 6. Business Rules & Automations

### A. Driver Security Check (Safety Control)
* **Trigger:** Before the truck leaves the port.
* **Logic:** We must ensure the driver is who they say they are to prevent cargo theft.
* **Action:** Odoo requires the **Driver CNIC** and a photo of the **Truck License Plate**. If these are missing, the system will not generate the Delivery Order (DO).

### B. The POD Unlock Rule (Financial Control)
* **Trigger:** When the user tries to create the Final Invoice.
* **Logic:** We should not ask the customer for the final payment until we prove we delivered the goods.
* **Action:** The system **blocks the Final Invoice** until a file is uploaded into the `x_pod_file` field. Once uploaded, the "Create Invoice" button becomes active.

### C. Damage Reporting (Quality Control)
* **Trigger:** If the driver clicks "Cargo Damaged" in the mobile app.
* **Logic:** We need to start an insurance claim immediately.
* **Action:** Odoo sends an **Instant Alert** to the Operations Manager and the Insurance team. It also prevents the Job Order from being "Closed" until the damage claim is reviewed.

---

## 7. User Roles & Access Rights

| Role | Access Level | Permissions |
| :--- | :--- | :--- |
| **Driver** | Mobile App | Can see the delivery address. Can take a photo of the signed POD and upload it directly. |
| **Operations Exec** | User: Own Documents | Assigns the Transporter and Truck. Verifies that the POD photo is clear and readable. |
| **Customer** | Portal Access | Receives an automatic WhatsApp: *"Your cargo has been delivered. Please view your signed POD here [Link]."* |

---

## 8. Next Steps / Workflow Transition
Now that the goods are safely with the customer:
1. The system moves to **Stage 11: [Final Invoice & Close](11-Final-Invoice&Close.md)**.
2. We calculate the final profit for the job.
3. We collect the remaining balance from the customer and pay our vendors (shipping lines, truckers).