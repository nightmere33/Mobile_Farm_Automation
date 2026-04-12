# Mobile Automation Project Roadmap

This document organizes the proposed build plan for a multi-device Android automation system with a face-photo intake flow, client data management, and an operator dashboard. It also includes a recommended build order, technology stack, milestone plan, and practical resources for implementation.

## Core direction

The recommended first step is to prove the automation on **one real Android phone** before building the full Windows control app, because Appium's Android setup depends on the UiAutomator2 driver and this proof-of-concept is the fastest way to validate whether the target app flow is stable under automation.[cite:46][cite:56] Appium also supports parallel Android sessions across multiple devices when each session uses a separate device identifier and unique ports, which supports the long-term goal of scaling to many devices.[cite:40][cite:43]

## Recommended build order

| Phase | What to build | Why it comes now |
|---|---|---|
| 1 | One-device automation proof | Validates the hardest technical risk first: whether the booking flow can actually be automated on a real Android device.[cite:46][cite:49] |
| 2 | Minimal Django dashboard + API | Gives staff a structured way to enter client records and store booking-ready data after the automation path is proven.[cite:51][cite:57] |
| 3 | Database-backed single-device worker | Confirms the automation can pull real client records from the server and complete a full run end-to-end.[cite:51][cite:60] |
| 4 | Windows operator app | Should sit on top of already-proven automation and APIs, not be built first.[cite:52][cite:55] |
| 5 | Parallel multi-device execution | Appium supports parallel Android sessions when each device has its own `udid` and unique port configuration.[cite:40][cite:43] |
| 6 | Cloud devices, retries, queueing | Final scaling layer after the local model works reliably.[cite:40][cite:55] |

## System architecture

### Client-facing layer

The existing Android face-photo app can remain the intake tool for collecting face images that are then stored on the server for later use in the booking workflow. The next client-facing build should be a small Django dashboard or form workflow so staff can enter passport and identity data in a structured way and push it to the database for later assignment to devices.[cite:51][cite:57]

### Automation layer

Appium with the UiAutomator2 driver is the recommended Android automation stack because UiAutomator2 is Appium's current Android driver for modern Android versions, and Appium Inspector can be used to inspect elements and selectors in the target app.[cite:46][cite:47] ADB should be used as the device transport layer because it can target a specific connected device by serial and works for both USB and TCP/IP-connected phones.[cite:36][cite:39]

### Operator layer

The desktop control application can be built in **C# WPF on .NET 8** after the automation proof and API are stable, because it is best treated as an orchestration layer rather than the first thing to build. Its initial responsibilities should be listing devices, starting jobs, stopping jobs, showing status, and assigning one client record to one device worker at a time.[cite:33][cite:40]

## Recommended technology stack

| Area | Recommended technology | Notes |
|---|---|---|
| Android automation | Appium 2 + UiAutomator2 | Standard Android automation path for real-device control.[cite:46][cite:47] |
| Device inspection | Appium Inspector | Useful for identifying selectors and validating screen structure.[cite:48][cite:49] |
| Device transport | ADB | Supports targeted device commands by serial for multiple devices.[cite:36][cite:39] |
| Desktop control | C# WPF (.NET 8) | Good fit for a Windows operator console and ADB/Appium orchestration.[cite:33] |
| Backend | Django + Django REST Framework | Suitable for admin dashboard, API, authentication, and data entry workflows.[cite:51][cite:57] |
| Database | PostgreSQL or MySQL | Either is suitable for client records, task queue, logs, and booking results. |
| Queueing | Database-backed queue first, then Redis/Celery if needed | Start simple and upgrade only after throughput needs justify it. |
| Cloud device layer | Only after local proof | Remote scaling should come after one-device and two-device validation.[cite:40][cite:55] |

## What to build first

### Phase 1: Automation proof on one device

This is the immediate next milestone. Install Appium, install the UiAutomator2 driver, connect one Android phone by USB, and use Appium Inspector to inspect the target app screens and capture usable selectors.[cite:46][cite:47][cite:49] The goal is to prove that the target booking flow can launch, accept typed data, move through screens, and reach the photo/liveness stage on a real phone.[cite:48][cite:59]

**Deliverables for Phase 1**
- ADB sees the phone.
- Appium session starts successfully.
- The target app opens.
- The script fills text fields.
- The script clicks through the next steps.
- The team documents what happens at the photo/liveness step.[cite:46][cite:49][cite:59]

### Phase 2: Minimal dashboard and API

Only after Phase 1 is viable should the Django dashboard be built. A minimal MVP should focus on storing the exact data the worker needs: client identity, passport details, face-photo path, appointment status, attempt count, and logs.[cite:51][cite:57] This keeps the admin layer small and aligned with the validated automation flow rather than building a large dashboard before the risky part is proven.[cite:54][cite:60]

**Suggested Django models**
- `Client`
- `ClientDocument`
- `ClientPhoto`
- `BookingJob`
- `Device`
- `JobLog`
- `Operator`

### Phase 3: One-device end-to-end worker

In this phase, the script should stop using hardcoded test data and instead pull one real client record from the database, run the booking flow, and write the result back to the server. This validates the full loop: dashboard to database to automation worker to result logging.[cite:51][cite:60]

### Phase 4: Windows operator app

The Windows application should be built only after the backend API and one-device automation are stable. Its first version should be intentionally small and should mainly orchestrate workers rather than implement all features at once.[cite:52][cite:55]

**Version 1 modules**
- Device list panel
- Connect/disconnect panel
- Start/stop job controls
- Current job status table
- Simple logs view
- API configuration panel

### Phase 5: Parallel execution

Appium supports parallel sessions when each device is configured with a unique `udid` and separate per-session ports such as `systemPort`, so the next step after one-device success is to scale to two devices and then more.[cite:40][cite:43] Each device should process only one job at a time, and the server should lock the record so no second worker picks the same client record concurrently.[cite:40][cite:43]

## Exact step-by-step roadmap

### Week 1: Validate the core risk

1. Install Node.js, Appium 2, Android SDK tools, Java, and Appium Inspector.[cite:46][cite:48]
2. Install the UiAutomator2 driver in Appium.[cite:46][cite:47]
3. Connect one Android phone via USB and confirm `adb devices` can see it.[cite:36][cite:39]
4. Open the target app and inspect the screens with Appium Inspector.[cite:48][cite:49]
5. Write one short automation script that opens the app and fills a few fields.[cite:46][cite:59]
6. Continue until the script reaches the photo/liveness screen and document what blocks or succeeds there.[cite:48][cite:59]

### Week 2: Build the smallest useful backend

1. Create the Django project.
2. Add authentication for internal operators.
3. Create models for clients, photos, jobs, devices, and logs.
4. Build forms so staff can add one client at a time.
5. Expose a simple API endpoint for the automation worker to fetch the next pending job.
6. Add an endpoint for posting back success, failure, and logs.

### Week 3: Connect automation to real data

1. Replace hardcoded test data with database-driven input.
2. Have the worker fetch one pending job.
3. Run the booking flow with the stored client data.
4. Upload logs and final status back to the server.
5. Add retry counts and failure reasons.

### Week 4: Build the first Windows app

1. Create a WPF app shell.
2. Add a device discovery screen using ADB.
3. Show connected device IDs and online/offline state.
4. Add a button to launch one worker on one selected device.
5. Show live logs and current job state.
6. Add settings for API base URL, Appium server URL, and timeouts.

### Week 5: Scale to two devices

1. Start two Appium sessions in parallel with separate device IDs and unique ports.[cite:40][cite:43]
2. Add record locking in the backend.
3. Confirm each device takes a different client.
4. Measure success rate and timing.
5. Fix stability issues before adding more devices.

## Practical project structure

```text
project-root/
├── backend/
│   ├── django_project/
│   ├── apps/
│   │   ├── clients/
│   │   ├── jobs/
│   │   ├── devices/
│   │   └── logs/
│   └── requirements.txt
├── automation/
│   ├── appium_worker/
│   ├── selectors/
│   ├── flows/
│   └── config/
├── desktop/
│   ├── OperatorApp.sln
│   └── OperatorApp/
├── docs/
└── assets/
```

## Suggested API endpoints

| Endpoint | Method | Purpose |
|---|---|---|
| `/api/jobs/next/` | POST | Reserve and return the next pending job for one device |
| `/api/jobs/{id}/status/` | POST | Update running, failed, or success state |
| `/api/jobs/{id}/logs/` | POST | Upload logs during execution |
| `/api/devices/heartbeat/` | POST | Update online status for each desktop-connected device |
| `/api/clients/` | GET/POST | Manage client records |
| `/api/photos/` | POST | Upload or register client face photo |

## Minimum database design

| Table | Purpose |
|---|---|
| `clients` | Identity and passport information |
| `client_photos` | Face image path, metadata, validation result |
| `booking_jobs` | Client-to-booking task assignment and state |
| `devices` | Device serial, type, status, last heartbeat |
| `job_logs` | Execution trail, timestamps, failure reasons |
| `operators` | Internal user accounts |

## Key engineering rules

- One device should run one client job at a time to keep execution predictable.[cite:40][cite:43]
- Start with one phone, then two, then scale further only after stability metrics are acceptable.[cite:40][cite:55]
- Keep selectors and automation flow logic separate so UI changes are easier to fix.[cite:48][cite:49]
- Build monitoring from the start: timestamps, screenshots on failure, and device-level logs improve debugging significantly.[cite:48][cite:59]
- Treat the Windows app as an orchestration shell, not as the source of business logic. Business rules should live in the backend and worker layers.

## Cursor and Claude Pro usage plan

Cursor and Claude Pro can accelerate implementation if they are used in a structured way. They are most useful for scaffolding, refactoring, writing repetitive code, summarizing logs, and drafting API or UI boilerplate. They should not replace direct testing on the device, because the core risk is practical automation reliability rather than code generation quality.

### Best use of Cursor
- Generate Django models, serializers, and admin screens.
- Refactor Appium helper methods.
- Build C# WPF MVVM boilerplate.
- Generate API client classes.
- Help organize project folders and naming.

### Best use of Claude Pro
- Review architecture decisions.
- Help think through worker lifecycle and queue logic.
- Produce documentation, SOPs, and troubleshooting checklists.
- Analyze long logs and suggest fixes.

### Best practice with both
- Ask them for small, testable pieces.
- Paste exact error output when asking for fixes.
- Keep a real architecture document and do not let the codebase become AI-generated chaos.

## Installation checklist for the immediate next session

### On the automation PC
- Node.js
- Java JDK
- Android platform tools (ADB)
- Android SDK
- Appium 2
- UiAutomator2 driver
- Appium Inspector[cite:46][cite:48]

### On the Android device
- Developer options enabled
- USB debugging enabled
- Stable cable and trusted PC pairing
- Test build of the target environment ready

## Immediate next actions

1. Set up Appium and UiAutomator2 on the PC.[cite:46][cite:47]
2. Connect one phone and verify ADB sees it.[cite:36][cite:39]
3. Inspect the target app screens in Appium Inspector.[cite:48][cite:49]
4. Write the first proof-of-concept automation for one device.[cite:46][cite:59]
5. Decide on viability only after testing the photo/liveness step.[cite:48][cite:59]
6. Build the Django dashboard only after this proof is acceptable.[cite:51][cite:57]

## Resources

| Resource | Purpose |
|---|---|
| Appium UiAutomator2 Quickstart | Driver install and Android setup.[cite:46] |
| Appium UiAutomator2 GitHub repo | Driver details and reference implementation notes.[cite:47] |
| Appium Inspector guides | Screen inspection and selector discovery.[cite:48][cite:49] |
| Appium parallel testing docs | Multi-device execution design.[cite:40] |
| ADB multi-device usage references | Device selection and targeted commands.[cite:36][cite:39] |

## Final recommendation

The correct build order is: **prove one-device automation first, then build the Django dashboard and API, then connect the worker to real data, then build the Windows operator app, and only then scale to multi-device execution**.[cite:46][cite:49][cite:51][cite:55] This order minimizes wasted time, validates the real technical risks early, and gives a much better foundation for using Cursor and Claude Pro effectively across the project.[cite:57][cite:60]
