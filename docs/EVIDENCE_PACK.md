# Evidence Pack for MediNote VN

## Product boundary

MediNote VN creates a draft clinical note from a consultation. It does not diagnose, prescribe, or write autonomously to the EHR. A clinician must review and approve every note before it becomes part of the medical record.

## Current evidence status

| Asset | Status on 08/10/2026 | Owner | Deadline | Acceptance threshold |
| --- | --- | --- | --- | --- |
| Eval results | Not yet available | Nguyễn Thị Bảo Trang | 08/11/2026 | 300 de-identified Vietnamese consultations; 0 unsupported critical clinical facts; field-level accuracy at least 95%; major-edit rate at most 15% |
| Procurement Q&A and data-flow diagram | Draft below; architecture evidence still missing | Nguyễn Thị Bảo Trang | 25/10/2026 | Vendor list, retention, deletion, access control, incident contact, and exit/export procedure documented |
| Pilot report | Not yet available | Nguyễn Thị Bảo Trang | 10/01/2027 | At least 8,000 notes; completion at least 90%; GM at least 65%; median clinician review at most 3 minutes |

The thresholds are go/no-go criteria, not achieved results.

## Procurement Q&A draft

### 1. What happens when the model invents or omits clinical information?

The draft cannot be saved to the EHR without clinician approval. The product must show the transcript evidence behind each clinical section, log every clinician edit, and route low-confidence or failed audio to manual documentation. The pilot will report critical unsupported facts, field-level accuracy, major-edit rate, and median review time. Current limitation: no completed Vietnamese clinical eval exists yet, so the product remains pilot-only.

### 2. Is clinic or patient data used to train models?

The product policy will prohibit using clinic data for model training. OpenAI states that API inputs and outputs are not used for training by default unless the organization opts in. Before pilot launch, the team must disable all optional data sharing, execute the required vendor agreements, document sub-processors, encrypt data in transit and at rest, and record patient consent. Audio must be deleted after note generation and quality checks under the retention policy agreed with the clinic. Source: https://openai.com/enterprise-privacy/

### 3. What happens to our data if the startup closes or the contract ends?

The clinic must be able to export approved notes and audit metadata in JSON and PDF, with FHIR mapping where the target EHR supports it. The exit plan will define an export window, verification by the clinic, revocation of access, and deletion certification within 30 days. Current limitation: the export and deletion workflow has not yet been independently tested.

## Minimum viable evidence before a paid rollout

1. A signed data-processing agreement and a named security contact.
2. A data-flow diagram with sub-processors, storage location, retention, encryption, and deletion.
3. A Vietnamese eval report with the stated go/no-go thresholds and specialty slices.
4. A pilot report that separates attempted sessions from approved notes.
5. A clinician consent script, patient consent flow, incident response procedure, and tested export/deletion runbook.

