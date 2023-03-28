# EPICS
## [Epic 1] Visualize code and notification
This epic contains all needed functions that allow users to obtain a ticket number and to show the status of the customer in the queue.

### Implementation

As initial part of the process, the epic must implement:

- Obtain a ticket number
- Calculate waiting time
- Notify status of user turn
- Show attended ticket

### US:

#### [US 1] Obtain a ticket number
As a Customer I need to get my ticket number. So that I can be attended to the queue line and get my service

##### Acceptance Criteria:

- When the user accesses a URL page(home/root of application), this will open a screen with my ticket number within the queue
- The format of the ticket number is: Qxxx (e.g. Q047).
- When the value Q999 is reached, the numbering restarts at Q001.
- If a ticket number is removed from the system, it cannot be re-assigned.-Each user can only have one ticket number at a time per queue.
- If the user can’t get a number ticket, then show him a feedback popup
- What is stored doesn’t contain personal information of the customers but as a cookie is used a notification pop-up must inform the customer.

Priority: High

#### [US 2] Calculate waiting time
As a customer I want to know how much time I need to wait until I will be attended so that I can better manage my time.

#### Acceptance Criteria:

- Waiting time shown in the main page of ticket number as remaining minutes
- The estimated waiting time = 𝐀𝐯𝐞𝐫𝐚𝐠𝐞 𝐚𝐭𝐭𝐞𝐧𝐭𝐢𝐨𝐧_𝐭𝐢𝐦𝐞 ∗ (nº of 𝐧𝐨_𝐚𝐭𝐭𝐞𝐧𝐝𝐞𝐝_𝐜𝐮𝐬𝐭𝐨𝐦𝐞𝐫𝐬 in queue before me)
- The Average attention_time = (The 𝐬𝐮𝐦 of 𝐚𝐭𝐭𝐞𝐧𝐭𝐢𝐨𝐧_𝐭𝐢𝐦𝐞 from the first attended customer until the last attended customer before me) / the number of the 𝐧𝐨_𝐚𝐭𝐭𝐞𝐧𝐝𝐞𝐝_𝐜𝐮𝐬𝐭𝐨𝐦𝐞𝐫𝐬 in queue before me.
- The attention_time is calculated as: The time between the moment the customer starts to be served and the moment the next customer is called
- The waiting_time cannot be shorter than a configured minimum waiting_time. If that happens, the waiting_time is set to that configured minimum waiting_time.

Priority: High

#### [US 3] Show the attended ticket
As a customer or owner/employee, I want to see the current customer who is being attended.

##### Acceptance Criteria:

- It’s shown in the main page of ticket number and also in the page of queue management
- In customer page, it must be displayed below the user’s ticket number
- The current customer is the one who has an acessCode with state at attending, as result of having NULL End_date and NOT NULL Start_date.
- You cannot have more than one attended customer in the same queue

Priority: High

#### [US 4] Notify status of user turn
As customer I want to be informed when it is the turn of the person who goes before me so that I don’t lose my turn.

##### Acceptance Criteria:

- When the current customer in the queue will be the next to be attended then a notification message is showed like “You are the next to attend”.
- The pop-up shown will contain two buttons that will be:
-   a) Leave queue
-   b) Delay number

Priority: Medium

## [Epic 2] Manage the queue
It contains all functions that permit to delay a ticket number and leave the queue.

### Implementation:

The user stories that define this are:

- Start queue
- Call next customer
- Close queue
- Show attended ticket
- Calculate total waiting customers
- Calculate remaining service time

### US:

#### [US 7] Start the queue

As an owner/employee, I want to start with the first number of the queue so that I can attend the first customer.

##### Acceptance Criteria:

- The owner should press “Start” button to initialize the queue
- “Start” Button located in the owner screen
- The first number active ticket number is attended

Priority: High

#### [US 8] Call the next customer

As an owner/employee, I want to be able to call the next customer so that I can know which ticket to attend.

##### Acceptance Criteria:

- When the user pushes the "Next" button, the displayed access code is updated to the access code of the new customer (if any). If there are no new customers, no code is displayed until there is a new code.
- The system must save:
- At the previous turn: Save the current time as end time
- At the new turn: Save the current time as start time
- The information for all non-attended customers (if any) gets updated.

Priority: High

#### [US 9] Close Queue

As an owner/employee, I want to be able to stop the queue at any moment so that news customers can not join the queue.

##### Acceptance criteria:

- The owner/employee of the queue can stop the queue by pressing the “Stop” button.
- The system will ask to confirm that he or she wants to stop the queue.
- The system stops the process that grants new ticket numbers to the customers that request to join the queue. They will be redirected to customer out page similar way as deleting his code (US6).

Priority: Low

#### [US 10] Calculate waiting tickets
As an owner/employee, I want to be able to see the total number of customers waiting, so that I can manage my queue efficiently.

##### Acceptance criteria:

- It will be show in the page of queue management
- The total number of customers waiting in the queue is calculated as the sum of all customers in the queue with waiting state, as result of null start date and null end date

Priority: Medium

#### [US 11] Calculate remaining service time

As an owner/employee, I want to be able to see how much time is needed to serve all customers that are waiting in the queue so that I can manage my queue efficiently.

##### Acceptance criteria:

- The total waiting time is calculated by multiply the average of attention_time by the total number of all customers that are waiting in the queue.

Priority: Medium
