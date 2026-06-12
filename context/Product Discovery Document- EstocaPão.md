# **📋 Product Discovery Document: EstocaPão — Eliminating Inventory Friction & Revenue Leakage**

**Role:** Project Owner

**Objective:** Investigate, map, and deeply understand the customer's core pain points before designing any technical implementation.

**Context:** EstocaPão — A CLI-based inventory management system designed to eliminate human error through memory-resident CRUD operations and robust data validation pipelines.

## **🏛️ Project Metadata**

* **Client / Segment:** Artisanal Bakeries (Boulangerie & Pastry Segment)  
* **Date of Creation:** June 12, 2026  
* **Lead Product Owner:** Kalyel Nunes Laurindo / Project Owner  
* **Document Version:** v1.0

## **1\. 🎯 Core Problem (The Macro Pain)**

**Artisanal bakery owners and frontline staff** spend approximately *1 hour per day manually tracking ingredient levels and shelf-life expiration dates* using **illegible, grease-stained paper logs** during closing handovers. This analog process leads to *catastrophic stockouts of key ingredients (e.g., specialty flour and yeast) right before peak morning baking cycles, generates direct financial loss from unmonitored ingredient spoilage, and inflicts severe operational stress on the kitchen staff due to a complete lack of inventory predictability*.

## **2\. 👥 Target Audience: Segments, Micro-Pains & Empathy Mapping**

### **👤 Head Baker / Owner (Direct & Indirect Beneficiary)**

* **Segment / Department:** Production Operations & Business Management  
* **Micro-Pains (Specific Drains):** Discovering critical ingredient shortages minutes before the 3:00 AM baking cycle; complete lack of data-driven purchasing triggers.  
* **Emotional State / Sentiment:** Chronic anxiety regarding fulfillment windows and persistent fear of revenue loss during peak morning sales.

### **👤 Counter Staff / Frontline Clerk (Direct User)**

* **Segment / Department:** Front-of-House Operations & Daily Handovers  
* **Micro-Pains (Specific Drains):** Logging inventory events on vulnerable paper slips that get torn, misplaced, or covered in flour; wasting valuable shift-end time trying to decipher handwritten notes from prior shifts.  
* **Emotional State / Sentiment:** Burnout due to repetitive manual labor and high cognitive load during closing handovers.

## **3\. 🛠️ Current Workarounds (The "Gambiarras")**

* **Workaround 1: The "Nail & Clipboard" Wall Log**  
  * ⚡ **Risk Profile: Critical.** Zero data durability. Logs are frequently damaged by water, grease, or flour, making historical audits or waste tracking impossible.  
* **Workaround 2: The "We're Out\!" WhatsApp Group Chat**  
  * ⚡ **Risk Profile: High.** Highly unstructured, ephemeral communication. Photo updates of empty shelves get buried in chat history, leading to missed purchasing orders by the owner.

## **4\. 🚨 Cost of Inaction (COI)**

* **🔴 Operational Overhead (Productivity Bottleneck):** Unplanned downtime in the baking queue, causing staff idle time and severe inventory delays.  
* **🔴 Quality & Consistency Degradation:** Unintentional use of expired or suboptimal ingredients, degrading the signature quality of artisanal goods and increasing product discard rates.  
* **🔴 Compliance & Food Safety Liability:** Major regulatory exposure (health inspections) due to a complete absence of lot-level tracking and expiration audit trails.

## **5\. 🔄 As-Is User Journey (The Friction Map)**

\[Trigger: Weekly vendor delivery or shift handover\]  
       │  
       ▼  
 1\. \[Receiving: Clerk manually checks deliveries against paper invoices\]  
       │  
       ▼  
 2\. \[CRITICAL BOTTLENECK: Baker starts the night shift and finds expired/spoiled ingredients\] \<-- 🚨 Leakage\!  
       │  
       ▼  
 3\. \[Emergency Run: Baker calls the owner at 4:30 AM to buy retail-priced flour\]  
       │  
       ▼  
\[Outcome: Delayed morning bake, empty display cases at 6:00 AM, compromised margins\]

📝 **Step-by-Step Breakdown:**

1. **Step 1 (Manual Intake & Sorting):** The frontline clerk receives physical boxes from suppliers. Verification is based on a printed invoice sheet, ticking off quantities with a pencil. Expiration dates are rarely cross-checked systematically.  
2. **Step 2 (The Midnight Production Bottleneck):** The Head Baker starts the dough preparation at 3:00 AM. When reaching for 20kg of premium flour, they discover that the remaining bags in the pantry are unusable due to moisture contamination or expired shelf-life.  
3. **Step 3 (The Emergency Patch):** Out of options, the baker wakes up the business owner via urgent phone calls. The owner has to drive to a local supermarket to buy flour at standard retail price, absorbing a massive markup.  
4. **The Ultimate Failure:** The 6:00 AM baking batch is significantly delayed. Commuters find empty display shelves during peak breakfast hours, causing immediate customer churn and margin erosion on the high-cost retail ingredients.

## **6\. 💰 Financial Quantification of the Pain**

### **📊 Metric Formulas:**

* **Wasted Labor Cost (Overhead):**  
  ![][image1]  
* **Emergency Procurement Premium:**  
  ![][image2]

### **📈 Cost of Inaction (COI) Matrix**

| Impact Metric | Baseline Metric | Unit of Measure | Estimated Monthly Cost of Inaction (COI) |
| :---- | :---- | :---- | :---- |
| **Wasted Labor** | 30 | Hours / Month (per FTE) | Loss of **$900.00/month** in pure overhead from manual closures (Formula: ![][image3]). |
| **Shrinkage & Spoilage** | 5% | Monthly perishable discard rate | Direct loss of **$600.00/month** in high-value ingredients (milk, eggs, butter) expiring unmonitored. |
| **Emergency Procurements** | 4 | Retail-price emergency runs / Month | **$450.00/month** in margin erosion due to buying key supplies at local retail markup (\~40% premium). |
| **Revenue Leakage** | 8 | Delayed morning bakes / Month | Estimated loss of **$1,200.00/month** in high-margin breakfast sales due to empty shelves during opening hours (06:00 \- 07:00). |

* **💸 Total Cost of Inaction (COI):** **$3,150.00 / month** (or **$37,800.00 / year**).

## **7\. 🌱 Root Cause Analysis (The 5 Whys)**

### **🔍 Uncovering the Structural Core of Inventory Leakage**

1. **Why do production delays and food waste continue to happen?**  
   * 🗣️ *Response:* Because stock counts and expiration tracking fail consistently at the shift transitions.  
2. **Why do stock counts and expiration tracking fail?**  
   * 🗣️ *Response:* Because they rely entirely on vulnerable, grease-stained paper logs on the kitchen floor.  
3. **Why does the kitchen rely on manual paper tracking?**  
   * 🗣️ *Response:* Because staff lack a streamlined interface and validation rules to prevent data entry errors and trigger low-stock alerts.  
4. **Why are there no automated validation rules or low-stock alerts?**  
   * 🗣️ *Response:* Because the bakery lacks a lightweight, digital inventory management tool tailored to frontline kitchen workflows.  
5. **Why has this tool not been built? (The Structural Root Cause)**  
   * 🗣️ *Response:* **Root Cause:** Absence of a standardized inventory control process backed by a highly accessible data entry system with built-in input validations to eliminate human error prior to closing handovers.

## **8\. 🚧 Scope Boundaries & Constraints**

* 🟢 **In-Scope (The Core Product MVP):**  
  * High-performance, in-memory CRUD operations for baking ingredients (Create, Read, Update quantities, and Delete stale/damaged stock records).  
  * Strict CLI-level input validation (block negative quantities, enforce standard date formats, reject historical expiration dates).  
  * Out-of-the-box console warnings for critical events (e.g., "Low Stock" warning, "Expired/Soon to Expire" notices).  
* ❌ **Out-of-Scope (Future Iterations):**  
  * Persistent database integration (SQL/NoSQL) to keep the MVP highly performant and focused on memory structures.  
  * Graphical User Interface (GUI), web, or mobile app development.  
  * Point of Sale (POS) operations, cash drawer management, and tax/invoice generation.
  * **Sprint 2 Roadmap:** Language selection menu (PT-BR / EN), auto-deduction based on recipe formulations (Baking Recipes Engine), batch acquisition costs and loss dashboard, CSV/PDF printable reports export, and off-site cloud sync backups.

## **9\. 🔍 Operational Escalation & Blockers**

* **Current Help Channels:** Informal WhatsApp messages or emergency calls; manual retrieval of physical, stapled vendor invoices to verify received batch expiration dates.  
* **Key Resolution Blockers:**  
  * **Lack of Real-Time Autonomy:** Bakers cannot anticipate shortages without physically opening bags, delaying decisions.  
  * **Outdated Documentation:** Lack of historical records prevents the team from tracking vendor quality, leading to repeat losses from bad supplier batches.

## **🎯 10\. Jobs To Be Done (JTBD)**

### **⚙️ Functional Needs**

* **Core Job:** Complete shift closures with 100% accurate, audited, and error-free inventory records in under 5 minutes.  
* **Supporting Requirements:**  
  * Prevent human error during fast-paced manual entry at the CLI level.  
  * Flag expired ingredients instantly, safeguarding production quality.

### **❤️ Emotional & Social Needs**

* **Personal (Emotional):** Experience peace of mind during early morning bakes, knowing ingredients are fresh and fully accounted for.  
* **Social (Team Recognition):** Be recognized by ownership as a highly efficient, reliable operations professional rather than an unorganized clerk.

### **📌 Field Notes & Observations**

### **💡 Real-World Evidence**

Contextual observations and raw user quotes gathered from the field:

* *🗣️ User Quote (Head Baker):* "My chest gets tight every single morning before I open the fridge to check the fresh yeast. If it's spoiled, our production for the day is dead."  
* *🗣️ User Quote (Clerk):* "The paper log is always sticky. Half the time I can't tell if the guy before me wrote a '5' or a '9'."  
* *📸 Physical Evidence:* — Clipboard located next to the prep station, heavily stained with grease and flour, making multiple historical entries completely unreadable.

## **🏁 Transition Checklist (Definition of Done)**

* \[x\] **Evidence Validation:** Macro pain backed by a solid $3,150.00/month cost of inaction and direct user interviews.  
* \[x\] **Boundary Consensus:** Technical stakeholders agree on keeping the MVP scoped to a clean memory-resident CLI application.  
* \[x\] **Root Cause Alignment:** The product target matches the root cause: building strong input validation layers inside the data entry process.  
* \[x\] **Impact Clarity:** A potential $37.800,00 annual saving provides a clear business justification to start engineering.

[image1]: <data:image/png;base64,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>

[image2]: <data:image/png;base64,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>

[image3]: <data:image/png;base64,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>