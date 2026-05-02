# 09 - Transit Tracking

---

## 1. Overview
This is the ninth step in the shipping process. It is the **"Waiting"** stage. The ship or airplane is now moving toward the destination. 

Our job is to watch the shipment. We need to know exactly where it is so we can tell the customer when it will arrive. If the ship is delayed by a storm or port congestion, we must update the **ETA (Estimated Time of Arrival)** in Odoo immediately.

---

## 2. Odoo Technical Mapping
* **Base Model:** `freight.shipment` (The Job Order hub)
* **Tracking Model:** `freight.tracking.line` (To record location history)
* **Dependencies:** `google_maps` (to show the ship's position) or API links to Marine Traffic.

---

## 3. Core Entities Involved
This stage uses three main data entities:

1. **Shipping Line / Airline:** They provide the "Live Tracking" data on their websites.
2. **Transshipment Port:** A middle-stop port (like **Colombo** or **Jebel Ali**) where the container might be moved to a different ship.
3. **Customer:** They are waiting for their goods. They want regular updates.

---

## 4. Data Dictionary (Tracking Fields)

We use these fields to keep the customer informed:

| Field Label | Technical Name | Field Type | Description | Example Data |
| :--- | :--- | :--- | :--- | :--- |
| **Current Status** | `x_transit_status` | Selection | At Sea, In Port, or Transshipped. | `At Sea` |
| **Last Known Port**| `x_last_port` | Char | The last place the ship stopped. | `Colombo, Sri Lanka` |
| **New ETA** | `x_new_eta` | Date | The updated arrival date. | `07-Jun-2026` |
| **Delay Reason** | `x_delay_reason` | Selection | Weather, Congestion, or Engine Issue. | `Port Congestion` |
| **Vessel Position**| `x_lat_long` | Char | GPS coordinates of the ship. | `6.9271° N, 79.8612° E` |

---

## 5. Real-World Example Scenario (Mock Data)

Here is an example of a shipment being tracked:

* **Job Order:** `JO-2026-00456`
* **Vessel:** `COSCO STAR`
* **Current Location:** `Indian Ocean (Near Sri Lanka)`
* **Original ETA:** `05-Jun-2026`
* **Revised ETA:** `07-Jun-2026` (2 days late)
* **Reason:** `Heavy Monsoon Rains in Colombo`
* **Status Update:** `Sent to Customer via WhatsApp`

---

## 6. Business Rules & Automations

### A. The ETA Change Alert (Customer Service)
* **Trigger:** When the `x_new_eta` is changed by more than 24 hours.
* **Logic:** Customers hate surprises. They need to plan their warehouse space.
* **Action:** Odoo automatically sends a **WhatsApp/Email** to the customer: *"Dear Customer, your shipment JO-00456 is delayed by 2 days due to port congestion. New arrival date is June 7."*

### B. Transshipment Monitor (Risk Control)
* **Trigger:** When the ship reaches a middle port (like Colombo).
* **Logic:** Containers often get "stuck" at middle ports for weeks.
* **Action:** If the container stays at a transshipment port for more than **5 days**, Odoo flags the Job Order in **Purple** on the dashboard. This tells the manager to call the shipping line.

### C. Demurrage Pre-Alert (Financial Protection)
* **Trigger:** 3 days before the ship arrives at the final port.
* **Logic:** We need to remind the customer to prepare the final payment so we can clear the cargo quickly.
* **Action:** The system sends a **"T-Minus 3 Days"** alert. This helps avoid expensive demurrage fees that start the moment the container touches the ground.

---

## 7. User Roles & Access Rights

| Role | Access Level | Permissions |
| :--- | :--- | :--- |
| **Operations Exec** | User: Own Documents | Checks the shipping line website daily and updates the ETA and Location in Odoo. |
| **Customer** | Portal Access | Can log in to the Odoo Portal to see a **Live Map** of where their cargo is. |
| **Operations Manager** | User: All Documents | Reviews the "Delayed Shipments" report to help solve problems with the carriers. |

---

## 8. Next Steps / Workflow Transition
Once the ship finally arrives at the destination port (Karachi):
1. The system moves to **Stage 10: [Delivery & POD](10-Delivery&POD.md)**.
2. The container is unloaded from the ship.
3. We send the truck to pick up the goods and deliver them to the customer's door.