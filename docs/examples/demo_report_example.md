# TraceOps Evidence Demo Report

This report uses fake demo data and keeps source provenance visible for review.

## Input Summary

- Role description: `data/demo_evidence/sample_role_description.md`
- Evidence sources loaded: 4
- Requirements reviewed: 6

## Evidence Sources

- `data/demo_evidence/firmware_log_review_notes.md`
- `data/demo_evidence/python_automation_notes.md`
- `data/demo_evidence/unsupported_claim_examples.md`
- `data/demo_evidence/validation_station_notes.md`

## Decision Summary

- Supported claims: 3
- Partial claims: 1
- Unsupported claims: 2

## Supported Claims
- **Supported: Python automation for validation workflows**
  - Rationale: Supported by demo evidence with source provenance.
  - Sources:
    - `data/demo_evidence/python_automation_notes.md`
- **Supported: Telemetry log review and evidence summaries**
  - Rationale: Supported by demo evidence with source provenance.
  - Sources:
    - `data/demo_evidence/firmware_log_review_notes.md`
- **Supported: Validation station bring-up and fixture lane debugging**
  - Rationale: Supported by demo evidence with source provenance.
  - Sources:
    - `data/demo_evidence/validation_station_notes.md`

## Partial Claims
- **Partial: Repeatable failure documentation and operator handoff**
  - Rationale: Some requirement terms appear in demo evidence, but no single source supports the full requirement.
  - Sources:
    - `data/demo_evidence/firmware_log_review_notes.md`
    - `data/demo_evidence/python_automation_notes.md`
    - `data/demo_evidence/validation_station_notes.md`

## Unsupported Claims
- **Unsupported: Production database ownership**
  - Rationale: No matching demo evidence was found.
  - Sources: No source evidence found.
- **Unsupported: Production firmware ownership**
  - Rationale: No matching demo evidence was found.
  - Sources: No source evidence found.

## Review Notes

- Supported claims have direct source evidence and source paths.
- Partial claims have at least one weak or incomplete source.
- Unsupported claims remain visible and are not promoted.

## Source Provenance

All source paths are repo-relative and use forward slashes.
