# Scenario Examples

## 9.1 IT Service Management Scenarios

### Scenario: Major Incident Response

> **User:** "We just had a full outage of our ERP system. 500 users affected. How do I handle this in ServiceNow?"

**Expert:**
> **Major Incident Procedure:**
>
> 1. **Create Major Incident Record**
>    - Category: `major_incident`
>    - Impact: `1 - Enterprise`
>    - Urgency: `1 - Critical`
>    - Check "Major Incident" checkbox → auto-assigns to MIM (Major Incident Manager)
>
> 2. **Notify Stakeholders via Flow Designer**
>    ```
>    Trigger: MI created
>        ├─ Email: IT Leadership (role: itil_admin)
>        ├─ Teams/Slack: #it-major-incidents channel
>        └─ Page: On-call manager via PagerDuty spoke
>    ```
>
> 3. **Create Child Incidents per Affected Area**
>    - Network → child incident
>    - Database → child incident
>    - Application → child incident
>    - Link via `parent_incident` field
>
> 4. **War Room Collaboration**
>    - Use `incident.chat` field for real-time notes
>    - Post updates every 15 minutes
>    - Update `known_error` in Knowledge Base
>
> 5. **Resolution & Post-Incident Review**
>    - Create PIR (Post Incident Review) task
>    - Link to problem record for root cause analysis
>    - Document lessons learned

### Scenario: Cireson Integration for ITSM

> **User:** "We're using Cireson for our ITSM portal. How do we sync ServiceNow incidents?"

**Expert:**
> **Cireson-Servicenow Integration Setup:**
>
> 1. Install Cireson SCSM Connector on ServiceNow MID Server
> 2. Configure connector: Source `incident` table → Target SCSM `System.WorkItem.Incident`
> 3. Field mapping:
>    ```
>    SN.short_description → SCSM.Title
>    SN.caller_id.email → SCSM.AffectedUser.Email
>    SN.assignment_group → SCSM.TierQueue
>    SN.state → SCSM.Status (map: 1→New, 2→Active, 3→Awaiting, 6→Resolved, 7→Closed)
>    ```
> 4. Enable change request sync for SC requests
> 5. Schedule: Real-time sync via MID Server polling every 5 minutes

## 9.2 HR & Finance Workflows

### Scenario: Employee Onboarding via HR Service Management

> **User:** "How do I automate the employee onboarding request flow from Workday to ServiceNow?"

**Expert:**
> **Onboarding Flow:**
>
> ```
> Workday HCM → Integration Hub REST spoke → ServiceNow HR Service
>                                                       │
>                                           ┌───────────┼───────────┐
>                                    Provision AD   Setup Laptop   Assign Badge
>                                        │              │              │
>                                    Task created   Task created   Task created
>                                        │              │              │
>                                        └──────────────┼──────────────┘
>                                                       │
>                                              All tasks complete
>                                                       │
>                                              Onboarding Complete task
>                                                       │
>                                              Notify HR Manager
> ```
>
> 1. **Workday Integration:** REST import set from Workday Worker API
> 2. **Trigger:** New `sys_user` record with `u_employee_type=onboarding`
> 3. **Flow Designer:** Create parallel tasks for IT, Security, Facilities
> 4. **Deadline:** Each task SLA = start_date - 5 business days
> 5. **Completion:** Task group `All complete` → triggers welcome email

### Scenario: Expense Report Approval

> **User:** "Set up an expense report approval that routes based on amount thresholds."

**Expert:**
> **Approval Routing Logic:**
>
> ```javascript
> // Before Business Rule on expense_report
> (function executeRule(current, previous) {
    
>     var amount = current.amount.getDecimalValue();
>     var user = current.requested_by;
>     var dept = user.department;
>     
>     if (amount <= 500) {
>         current.approval = 'direct_manager';
>         current.u_approver = user.manager;
>     } else if (amount <= 5000) {
>         current.approval = 'dept_head';
>         current.u_approver = dept.dept_head;
>     } else {
>         current.approval = 'finance_director';
>         current.u_approver = 'finance_director_group';
>     }
>     
>     current.state = 'pending_approval';
    
> })(current, previous);
> ```

## 9.3 Support Ticketing Workflows

### Scenario: Automated Ticket Routing via NLP

> **User:** "We get thousands of tickets a day. How can we auto-categorize and route them?"

**Expert:**
> **Intelligent Routing with Now Assist:**
>
> 1. Enable `com.snc.knowledge.intelligence` plugin
> 2. Train model on 6+ months of historical tickets
> 3. Configure prediction:
>    ```
>    Predict: Category (from 50 historical categories)
>    Predict: Assignment Group (from incident.cmdb_ci + description)
>    Predict: Priority (based on keywords + user impact tier)
>    ```
> 4. Confidence threshold: ≥ 80% → auto-assign; < 80% → queue review
> 5. Human-in-the-loop: Agent can override → feedback loop improves model
>
> **Fallback Rule Engine:**
> ```
> if (short_description.contains('password')) → Assignment: IAM Team
> if (category == 'Hardware' && subcategory == 'Laptop') → Assignment: Hardware Ops
> if (caller.department == 'Finance') → Assignment: Finance IT Support
> ```

### Scenario: Customer Service Management (CSM) Entitlement Check

> **User:** "We want to check product entitlements before opening a support case."

**Expert:**
> **Entitlement Check Flow:**
>
> ```
> Customer submits case via CSM Portal
>         │
>         ├─ Flow: Look up entitlement
>         │   GET /api/crm/entitlements?customer_id={caller_id}
>         │
>         ├─ Response: { product: "Enterprise Suite", status: "active", tier: "Premium" }
>         │
>         ├─ If active → Create case, assign to Premium Support queue, SLA: 2 hours
>         └─ If expired → 
>              Case created with note: "Your entitlement expired on {date}"
>              Redirect to renewal offer page
>              Route to Sales queue
> ```

### Scenario: SLA Breach Notification

> **User:** "How do I set up proactive SLA breach notifications at 75% and 90%?"

**Expert:**
> **SLA Breach Warning Flow:**
>
> 1. Configure SLA Definition with breach warning schedule:
>    ```properties
>    # System Property: SLA warning thresholds
>    com.snc.sla.warning.percentage=75,90
>    com.snc.sla.notification.recipients=assigned_to,assignment_group.manager
>    ```
> 2. **Flow Designer** trigger: `SLA Milestone Warning Event`
>    ```
>    Event: sla.marker.warning
>        │
>        ├─ Condition: milestone.name == "Response Time"
>        │   │
>        │   ├─ If percentage >= 75 AND < 90:
>        │   │   └── Email to assigned_to: "Approaching SLA breach in {remaining} minutes"
>        │   │
>        │   └─ If percentage >= 90:
>        │       └── Email + Push notification
>        │       └── Escalate to assignment_group.manager
>        │       └── Add work note: "SLA breach imminent - escalated at 90%"
>    ```
> 3. SLA Breach Event: `sla.marker.breach` → notify leadership + create audit log
