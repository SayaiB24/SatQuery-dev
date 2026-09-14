# SatQuery AI — Hackathon Development Plan

## Project

**Project ID:** SIH26167  
**Project:** SatQuery AI — An Interactive Vision-Language Assistant for Multimodal Remote Sensing Image Analysis through Text Queries  
**Target:** Hackathon-ready interactive web prototype with dummy models first, while preserving the architecture and contracts required for future real model integration.

---

## 1. Purpose of This Development Plan

This document is the implementation roadmap for building the SatQuery AI prototype.

The three project documents are the primary source of truth:

1. `SIH26167 — SatQuery AI` Problem Statement
2. `SatQuery_AI_Final_Synthesized_Solution.md`
3. `SatQuery_AI_SPDD.md`

The Problem Statement defines the required capabilities and evaluation scope.

The Final Synthesized Solution defines the selected architectural principles and the major technical decisions.

The SPDD defines the build-ready component contracts, API structures, frontend requirements, validation rules, specialist interfaces, evidence model, confidence logic, deployment approach, and testing strategy.

**Do not redesign the project independently when implementing this plan.**

---

# 2. Product Goal

Build a polished interactive web application in which a user can:

- Upload one or two remote-sensing images.
- Enter a natural-language query.
- Let the system determine the appropriate analytical task.
- Validate whether the uploaded inputs are compatible with that task.
- Route the request to the appropriate specialist workflow.
- Run a dummy specialist implementation initially.
- Produce structured evidence.
- Verify the evidence.
- Generate a High / Medium / Low confidence result.
- Display an auditable execution trace.
- Return a grounded textual answer with visual evidence.
- Download a PDF / JSON report.

The prototype must look and behave like the intended final SatQuery AI system even though the first implementation uses deterministic dummy models.

---

# 3. Core Product Philosophy

The implementation must preserve the following principles from the selected solution:

## 3.1 Validate Before Execute

The Compatibility Validator is a first-class stage.

It must determine whether the query can actually be answered from the supplied image configuration before specialist execution begins.

Invalid or unsatisfiable requests should produce a polished rejection state with a human-readable explanation.

## 3.2 Typed / Deterministic Orchestration

Do not use a free-form runtime model-selection mechanism.

The Query Interpreter converts the user query into a structured task specification.

The Specialist Router then uses a fixed, testable routing table to select the specialist workflow.

## 3.3 Evidence Before Final Answer

Specialists should produce structured evidence.

The verifier evaluates the collected evidence before the final answer is shown.

## 3.4 Confidence Must Be Explainable

Use:

- High
- Medium
- Low

with a short rationale.

Do not present a meaningless raw probability as if it were calibrated truth.

## 3.5 Dummy Models Must Be Replaceable

Every dummy specialist must expose the same logical interface and output structure that a future real specialist will use.

The frontend must never depend on whether the backend is using a dummy or real model.

---

# 4. Supported User Input

The UI and backend must support the following input modes.

## 4.1 Single Image

One:

- Optical / multispectral image
- SAR image

Possible tasks:

- VQA
- Captioning / scene description
- Text-guided grounding

## 4.2 Optical + SAR Pair

Two co-registered images:

- Optical / multispectral
- SAR

Possible task:

- Optical-SAR joint analysis / fusion

## 4.3 Bi-Temporal Pair

Two spatially corresponding observations from different times.

Possible tasks:

- Change description
- Change-VQA
- Change + grounding

## 4.4 Supported Formats

Support:

- GeoTIFF
- TIFF
- PNG / JPEG for benchmark/demo scenarios

The implementation should preserve the distinction between georeferenced raster inputs and ordinary image files.

---

# 5. Target User Journey

The primary flow is:

```text
User Input
    |
    v
Query Interpreter
    |
    v
Compatibility Validator
    |
    v
Specialist Router
    |
    +-------------------------------+
    |               |               |
    v               v               v
   VQA          Grounding       Change-VQA
    |               |               |
    +---------------+---------------+
                    |
                    v
              Fusion Pipeline
                    |
                    v
             Evidence Verifier
                    |
                    v
             Confidence Scorer
                    |
                    v
              Trace Emitter
                    |
                    v
             Response Composer
                    |
                    v
       Answer + Visual Evidence
       + Confidence + Trace + Report
```

For compound workflows:

```text
Fusion -> Change-VQA
```

or:

```text
Change-VQA -> Grounding
```

as required by the selected task.

---

# 6. Recommended Application Structure

## 6.1 Frontend

Recommended:

- React
- TypeScript
- Tailwind CSS or equivalent styling system
- Vite
- Leaflet or equivalent lightweight map layer where georeferencing is available

Main routes:

```text
/
  Landing / Home

/analyze
  Upload & Query

/processing
  Agent execution / progress

/results
  Results Dashboard
```

A separate route for processing is optional if the interaction is implemented as a modal/full-screen state, but the application must visibly show the stages being executed.

## 6.2 Backend

Recommended:

- Python
- FastAPI
- Pydantic

Logical services:

```text
api_gateway
orchestrator
query_interpreter
compatibility_validator
specialist_router
vqa_caption_specialist
grounding_specialist
change_vqa_specialist
fusion_pipeline
verifier_node
confidence_scorer
trace_emitter
response_composer
report_service
storage
```

## 6.3 Model Layer

Initial implementation:

```text
dummy_vqa_caption
dummy_grounding
dummy_change_vqa
dummy_fusion
```

Future implementation:

```text
real_vqa_caption
real_grounding
real_change_vqa
real_fusion
```

The orchestrator should not care which implementation is active.

---

# 7. Frontend Product Plan

## 7.1 Landing Page

Purpose:

Explain the product in a few seconds.

Must contain:

- SatQuery AI branding
- Short description
- Start Analysis CTA
- Multimodal Analysis
- Agentic Intelligence
- Evidence Grounding
- Confidence / Trace / Reporting

Do not overload the page with technical documentation.

---

# 8. Upload & Query Page

This is the primary user interaction page.

## Components

### Image Upload Area

Support:

- Image 1
- Optional Image 2
- Drag and drop
- File picker
- Remove / replace
- Preview
- File metadata summary

### Metadata Summary

Display when available:

- Format
- Modality
- Resolution / GSD
- CRS
- Acquisition date
- Image dimensions

For the dummy demo, metadata may be inferred from file properties or demo configuration.

### Natural Language Query

Use a large query input box.

Example queries:

```text
Describe the land-cover and major objects visible in this image.

Highlight the water body referred to in the query.

What changed between these two dates, and where did the change occur?

Use the optical and SAR images together to identify built-up and water-covered regions.

Has the built-up area increased, decreased, or remained unchanged?
```

### Capability Hint Panel

Show:

- VQA
- Captioning
- Grounding
- Change Analysis
- Optical-SAR Fusion
- Compound Analysis

The hint panel should make it clear which capabilities the current input configuration can support.

---

# 9. Processing / Agent View

The processing state is an important part of the hackathon demo.

Display observable execution steps:

```text
1. Query received
2. Query interpreted
3. Input compatibility checked
4. Specialist workflow selected
5. Specialist execution
6. Evidence verification
7. Confidence estimation
8. Response composition
```

Each step should have:

- Pending
- Running
- Completed
- Rejected
- Failed

Do not expose hidden chain-of-thought or internal reasoning.

Only show observable system operations, tools, parameters, outputs, and status.

---

# 10. Results Dashboard

The Results page is the most important demo screen.

Use a clear two-column layout.

## Left / Main Area

### Answer

Display:

- Final answer
- Short explanation

### Visual Evidence

Display:

- Original image
- Annotated image
- Bounding boxes
- Change mask where available
- Evidence regions
- Overlay toggles

For grounding, if multiple candidate regions are returned, show all plausible candidates rather than only a silent top-1 result.

## Right / Supporting Area

### Confidence

Display:

```text
HIGH
Geometric and cross-tool checks passed.
```

or:

```text
MEDIUM
Confidence reduced due to ambiguity.
```

or:

```text
LOW
Deterministic quantity check disagrees with
the specialist result.
```

### Task Information

Display:

- Selected task
- Image count
- Modalities
- Temporal relationship if applicable

### Verification

Show:

- Geometric consistency
- Cross-tool agreement
- Quantity validation

### Execution Trace

Make the trace collapsible.

Display:

- Step number
- Component
- Specialist / adapter
- Parameters where relevant
- Runtime
- Output summary

### Reports

Buttons:

- Download PDF
- Download JSON

---

# 11. Rejection State

A rejection is not a generic error toast.

It must be a dedicated polished state.

Example:

```text
INPUT COMPATIBILITY CHECK

Change analysis cannot be performed.

Detected:
Image 1 → Optical
Image 2 → SAR

Required:
Two spatially corresponding observations
from the same modality for temporal change analysis.

Suggested action:
Use T1 + T2 images for change analysis,
or ask an Optical-SAR analysis question.
```

This is a key demo feature.

---

# 12. Specialist Architecture

## 12.1 VQA / Captioning Specialist

Dummy implementation must accept:

- One image
- Query
- Mode

Modes:

- VQA
- Caption

Return:

```json
{
  "answerText": "string",
  "answerType": "open_ended | binary | mcq",
  "boundingBoxesIfAny": [],
  "rawTokenConfidence": 0.0
}
```

---

## 12.2 Grounding Specialist

Accept:

- One optical / multispectral image
- Referring expression

Return:

```json
{
  "boxes": [],
  "isAmbiguous": false,
  "candidateCount": 1
}
```

The dummy implementation should be able to return:

- one candidate
- multiple plausible candidates

for demonstration of ambiguity handling.

---

## 12.3 Change-VQA Specialist

Accept:

- Image T1
- Image T2
- Query

Return:

```json
{
  "answerText": "string",
  "changeMaskAvailable": true,
  "changeMaskRef": "string | null",
  "quantityFlag": false,
  "deterministicPixelCount": null
}
```

For quantity-style queries, populate deterministic cross-check information so that the verifier can demonstrate discrepancy handling.

---

## 12.4 Fusion Pipeline

The prototype should preserve the structured fusion concept:

```text
Optical image
     |
     v
Independent evidence extraction
     |
     +------------------+
                        |
SAR image               |
     |                  |
     v                  |
Independent evidence ---+
            |
            v
   Complementarity
       Detection
            |
            v
      Evidence Fusion
            |
            v
      Verbalization
```

Initially, the complementarity detector can be deterministic / rule-based.

Its interface should remain replaceable by the future learned detector.

---

# 13. Query Interpreter

The Query Interpreter converts natural language into a structured TaskSpec.

Example:

```text
User:
"Has the built-up area increased?"

↓

TaskSpec:
taskType = change_vqa
requiresTwoImages = true
```

Supported task types should include:

```text
single_vqa
single_caption
single_grounding
change_vqa
change_description
change_and_grounding
fusion
fusion_then_change
```

If the dummy interpreter cannot confidently map an input, it should return an ambiguous state or request clarification rather than inventing an unsupported task.

---

# 14. Compatibility Validator

This component should be deterministic.

Checks should include:

- Image count
- Modality
- Format
- CRS
- Temporal relationship
- Spatial overlap
- Required metadata
- Other specialist preconditions

Examples:

### Valid

```text
1 Optical image
+
VQA query
=
PASS
```

### Invalid

```text
1 image
+
change query
=
REJECT
```

### Invalid

```text
Optical + SAR
+
same-modality temporal change query
=
REJECT
```

### Valid

```text
Optical + SAR
+
Optical-SAR analysis query
=
PASS
```

---

# 15. Specialist Router

The router should be a deterministic mapping.

```text
single_vqa
    -> vqa_caption_specialist

single_caption
    -> vqa_caption_specialist

single_grounding
    -> grounding_specialist

change_vqa
    -> change_vqa_specialist

change_description
    -> change_vqa_specialist

change_and_grounding
    -> change_vqa_specialist
    -> grounding_specialist

fusion
    -> fusion_pipeline

fusion_then_change
    -> fusion_pipeline
    -> change_vqa_specialist
```

The router must not invent runtime task names.

---

# 16. Evidence Model

All specialists should contribute to a structured evidence ledger.

Conceptually:

```text
EvidenceLedger
|
+-- specialist outputs
+-- bounding boxes
+-- masks
+-- region tags
+-- deterministic counts
+-- geometry validity
+-- agreement flag
+-- discrepancy flags
```

This ledger feeds:

```text
Verifier
   |
   v
Confidence
   |
   v
Response Composer
```

---

# 17. Verification

The verifier must perform observable checks.

## 17.1 Geometric Checks

Examples:

- Bounding boxes inside image bounds
- Change region inside valid overlap
- Valid oriented-box angle

## 17.2 Cross-Tool Agreement

Where independent evidence sources exist:

- compare results
- identify agreement / disagreement

## 17.3 Quantity Validation

For quantity-style change questions:

- compare model answer-derived quantity with deterministic evidence
- flag material discrepancies

The verifier annotates the evidence; it does not silently rewrite the model answer.

---

# 18. Confidence System

Initial MVP:

```text
If geometry fails:
    LOW

Else if quantity discrepancy:
    LOW

Else if known ambiguous / weak query:
    MEDIUM

Else:
    MEDIUM
```

Optional future enhancement:

- decoupled perception confidence
- reasoning confidence
- calibration

The prototype should prioritize the simple auditable confidence path.

---

# 19. Execution Trace

Every important operation must generate a trace entry.

Example:

```json
{
  "stepIndex": 3,
  "component": "specialist_router",
  "adapterIdOrVersion": null,
  "parametersUsed": {
    "taskType": "change_vqa"
  },
  "wallClockMs": 20,
  "outputSummary": "Selected change_vqa_specialist"
}
```

The frontend should render this as a timeline.

---

# 20. Report Generation

Generate two formats.

## PDF

Must include:

- SatQuery AI title
- Session ID
- Query
- Input information
- Detected task
- Final answer
- Evidence image(s)
- Confidence
- Confidence rationale
- Verification results
- Execution trace

## JSON

Return the structured AnalyzeResponse / session information.

The report should contain the same information displayed on the Results page.

---

# 21. Technology Stack

## Frontend

- React
- TypeScript
- Vite
- Tailwind CSS or equivalent
- Leaflet for georeferenced map presentation where appropriate

## Backend

- Python
- FastAPI
- Pydantic

## Image / Raster Handling

- Rasterio / GDAL
- Pillow
- NumPy where required

## AI / Future Model Layer

- PyTorch
- Hugging Face Transformers
- PEFT / LoRA

## Storage

Prototype:

- Local file storage
- SQLite

Future / scalable:

- PostgreSQL
- MinIO or equivalent object storage

## Reports

- HTML template
- PDF renderer
- JSON export

## Deployment

- Docker
- Docker Compose

The first prototype should remain lightweight and hackathon-focused.

---

# 22. Dummy Model Design

The dummy models must be deterministic enough for a live demo.

Do not return random text.

Create a small Scenario Engine.

## Scenario A — VQA

Input:

One optical image

Query:

"Describe the land-cover and major objects visible in this image."

Expected prototype response:

```text
The scene contains a mixture of built-up,
vegetated and open land-cover regions.
```

---

## Scenario B — Grounding

Input:

One optical image

Query:

"Highlight the water body referred to in the query."

Expected:

- Answer text
- One or more bounding boxes
- Annotated image

---

## Scenario C — Change

Input:

T1 + T2

Query:

"What changed between these two dates, and where did the change occur?"

Expected:

- Change description
- Change region / mask
- Evidence image
- Confidence

---

## Scenario D — Optical-SAR Fusion

Input:

Optical + SAR

Query:

"Use the optical and SAR images together to identify built-up and water-covered regions."

Expected:

- Optical evidence
- SAR evidence
- Complementarity result
- Combined answer

---

## Scenario E — Compound Workflow

Input:

Optical + SAR

Query:

"Use the optical and SAR images together to identify built-up areas, then determine whether the built-up area increased."

Expected execution:

```text
Query Interpreter
      ↓
Validator
      ↓
Fusion
      ↓
Change-VQA
      ↓
Verifier
      ↓
Confidence
      ↓
Grounded Response
```

---

# 23. Development Phases

## Phase 0 — Document Study & Technical Planning

### Objective

Understand the three source documents and freeze the implementation plan.

### Deliverables

- architecture
- repository structure
- page structure
- API contract plan
- dummy model strategy
- phase plan

### Exit Criteria

Team can explain:

- what the PS requires
- what the synthesized solution adds
- what the SPDD specifies

No application code is required yet.

---

# Phase 1 — Frontend Foundation

### Objective

Build the visual product shell.

### Implement

- Landing page
- Upload & Query
- Results page skeleton
- Header / branding
- Image upload
- Image preview
- Query box
- Example queries
- Capability hints
- Loading state
- Results layout

### Exit Criteria

All frontend routes work.

No major console errors.

No backend is required yet.

---

# Phase 2 — FastAPI Backend and Contracts

### Objective

Establish the backend foundation.

### Implement

- FastAPI application
- Pydantic schemas
- `/v1/analyze`
- `/v1/session/{sessionId}`
- `/v1/session/{sessionId}/report`
- `/v1/health`
- `/v1/registry`

### Exit Criteria

Frontend can send an analyze request and receive a structurally valid AnalyzeResponse.

---

# Phase 3 — Agentic Orchestration

### Objective

Implement the complete logical pipeline using dummy services.

### Implement

```text
Interpreter
→ Validator
→ Router
→ Specialist
→ Verifier
→ Confidence
→ Trace
→ Response
```

### Exit Criteria

At least one end-to-end request works through the complete pipeline.

---

# Phase 4 — Scenario-Aware Dummy Specialists

### Objective

Make dummy outputs visually and logically meaningful.

### Implement

- VQA
- Caption
- Grounding
- Change-VQA
- Fusion
- Compound fusion + change

### Exit Criteria

All five demo scenarios produce deterministic, structured results.

---

# Phase 5 — Evidence & Results Dashboard

### Objective

Connect real-looking analysis outputs to the UI.

### Implement

- Annotated images
- Bounding boxes
- Change regions
- Optical/SAR comparison
- Evidence cards
- Confidence
- Verification results
- Trace panel

### Exit Criteria

A judge can understand exactly what the system analyzed and why the answer was produced.

---

# Phase 6 — Compatibility & Rejection Demo

### Objective

Make validation a visible differentiator.

### Implement

- Input compatibility checks
- Human-readable rejection state
- Suggested corrective action
- Validation trace

### Exit Criteria

Invalid combinations fail gracefully without crashing.

---

# Phase 7 — Reports & Demo Polish

### Objective

Make the application hackathon-presentation ready.

### Implement

- PDF report
- JSON export
- loading animations
- transitions
- empty states
- proper failures
- responsive layout
- professional visual styling
- demo mode

### Exit Criteria

A complete live demo can be run without manual backend manipulation.

---

# Phase 8 — Integration & Validation

### Objective

Perform a full end-to-end readiness pass.

### Test

- single VQA
- caption
- grounding
- change analysis
- optical-SAR fusion
- compound fusion + change
- invalid input rejection
- confidence
- execution trace
- PDF
- JSON

### Exit Criteria

All critical demo paths work from the browser.

---

# 24. Recommended Demo Mode

Create a visible:

**Demo Scenarios**

section.

Possible buttons:

```text
[ Scene Understanding ]
[ Grounding ]
[ Change Detection ]
[ Optical + SAR ]
[ Fusion → Change ]
[ Validation / Rejection ]
```

Selecting a scenario should pre-load the appropriate demo images and query.

This guarantees repeatable live demonstrations.

---

# 25. Repository Structure

Use a structure similar to:

```text
satquery-ai/
|
├── frontend/
│   ├── src/
│   │   ├── pages/
│   │   │   ├── Home.tsx
│   │   │   ├── UploadQuery.tsx
│   │   │   ├── Processing.tsx
│   │   │   └── Results.tsx
│   │   ├── components/
│   │   │   ├── ImageUploader.tsx
│   │   │   ├── QueryInput.tsx
│   │   │   ├── EvidenceViewer.tsx
│   │   │   ├── ConfidenceBadge.tsx
│   │   │   ├── ExecutionTracePanel.tsx
│   │   │   ├── ValidationMessage.tsx
│   │   │   └── ReportDownload.tsx
│   │   ├── services/
│   │   │   └── api.ts
│   │   └── types/
│   │       └── satquery.ts
│   └── ...
|
├── backend/
│   ├── api_gateway/
│   ├── orchestrator/
│   │   ├── query_interpreter.py
│   │   ├── compatibility_validator.py
│   │   ├── specialist_router.py
│   │   ├── verifier_node.py
│   │   ├── confidence_scorer.py
│   │   ├── trace_emitter.py
│   │   └── response_composer.py
│   ├── specialists/
│   │   ├── vqa_caption.py
│   │   ├── grounding.py
│   │   ├── change_vqa.py
│   │   └── dummy_scenarios.py
│   ├── fusion_pipeline/
│   │   ├── evidence_extraction.py
│   │   ├── complementarity_detector.py
│   │   └── verbalizer.py
│   ├── reports/
│   └── storage/
|
├── demo_data/
│   ├── optical/
│   ├── sar/
│   └── temporal/
|
├── tests/
│   ├── unit/
│   └── integration/
|
├── docker-compose.yml
├── README.md
└── docs/
```

This is a prototype-oriented adaptation of the component structure already defined in the SPDD.

---

# 26. API Contract Principle

The most important integration rule is:

```text
Frontend
   |
   | AnalyzeRequest
   v
Backend
   |
   | AnalyzeResponse
   v
Frontend
```

The frontend should not make assumptions such as:

```text
if task == dummy_change_model
```

Instead, it should consume the standard response:

```text
answerText
evidence
confidence
executionTrace
reportUrl
rejected
rejectionReason
```

This ensures real models can replace dummy models later without redesigning the frontend.

---

# 27. Future Real-Model Integration

After the dummy system is stable, integrate real models one specialist at a time.

Order:

```text
1. Real VQA / Caption
2. Real Grounding
3. Real Change-VQA
4. Real Evidence / Change overlays
5. Real Optical-SAR complementarity detector
6. Real fusion verbalization
```

Keep the orchestrator, API contracts, evidence model, verification layer and UI unchanged whenever possible.

---

# 28. Real Remote-Sensing Model Direction

The source documents specify:

- BigEarthNet.txt for remote-sensing adaptation
- VRSBench for captioning / grounding / VQA evaluation
- RSVQA for single-image VQA cross-check
- CDVQA for multitemporal change VQA
- Shared frozen visual + language backbone
- Task-specific LoRA adaptation

The SPDD further defines task-specific adapters and a Change-Enhancing Module for Change-VQA.

Real-model integration should follow those contracts rather than replacing the architecture with an unrelated end-to-end model.

---

# 29. Domain-Gap Awareness

The implementation must keep the Sentinel → Cartosat/RISAT domain gap visible in the technical architecture.

Future preprocessing hooks should support:

- GSD normalization
- radiometric / histogram adaptation
- SAR speckle-noise characteristics
- cross-sensor robustness testing

Do not claim that dummy-model performance proves domain robustness.

---

# 30. Hackathon Scope Guardrails

Do not allow the project to expand into unnecessary infrastructure during the prototype phase.

Explicitly defer:

- Kubernetes autoscaling
- production-grade MLOps
- Triton/TensorRT optimization
- vector database / historical recall
- QGIS plugin
- end-to-end generative optical-SAR fusion trained from scratch

The goal is a strong, complete, demonstrable MVP.

---

# 31. Testing Strategy

Every phase must have tests appropriate to that phase.

## Unit Tests

Test:

- query task mapping
- validation rules
- routing
- evidence schema
- confidence logic
- trace generation
- report generation

## Integration Tests

Test:

```text
Upload
→ Analyze
→ Result
```

for every supported task.

## Demo Tests

Before presentation, verify:

- malformed input rejection
- ambiguous grounding
- quantity discrepancy / Low confidence
- compound workflow trace
- report parity
- clean startup

---

# 32. Definition of Done

The prototype is considered ready when a fresh user can:

1. Open SatQuery AI.
2. Upload one or two images.
3. Enter a natural-language query.
4. Submit the request.
5. Watch the observable agent workflow.
6. See task and validation results.
7. See a relevant dummy specialist execute.
8. See visual evidence.
9. See confidence and rationale.
10. Open the execution trace.
11. Download a PDF report.
12. Try an invalid request and receive a polished rejection.

No manual edits to backend data should be required during the live demo.

---

# 33. Antigravity Execution Rules

Antigravity must follow these rules during implementation:

1. Work one phase at a time.
2. Do not start the next phase automatically.
3. Treat the three `.md` documents as source-of-truth references.
4. Preserve documented API contracts.
5. Preserve task names and routing semantics.
6. Keep dummy models isolated from orchestration.
7. Keep the frontend model-agnostic.
8. Do not expose hidden chain-of-thought.
9. Only expose observable execution steps.
10. Prefer simple, testable implementations for the hackathon.
11. Do not add speculative enterprise infrastructure.
12. After each phase:
   - run the application
   - run relevant tests
   - fix errors
   - summarize files changed
   - summarize what works
   - summarize remaining work
   - stop and wait for the next phase.

---

# 34. Master Development Sequence

```text
PHASE 0
Understand + Freeze Plan
        ↓
PHASE 1
Frontend Foundation
        ↓
PHASE 2
FastAPI + Contracts
        ↓
PHASE 3
Agentic Orchestration
        ↓
PHASE 4
Scenario-Aware Dummy Models
        ↓
PHASE 5
Evidence + Results Dashboard
        ↓
PHASE 6
Validation + Rejection
        ↓
PHASE 7
Reports + Demo Polish
        ↓
PHASE 8
Full Integration + Testing
        ↓
REAL MODEL INTEGRATION
```

---

# 35. Final Product Definition

The prototype should communicate one simple idea:

> **SatQuery AI transforms a natural-language question and satellite imagery into a verified, evidence-grounded and auditable answer.**

The application is successful when the judge can visually see:

```text
ASK
  ↓
UNDERSTAND
  ↓
VALIDATE
  ↓
ROUTE
  ↓
ANALYZE
  ↓
VERIFY
  ↓
EXPLAIN
```

without needing to understand the internal ML implementation to appreciate the agentic system.

