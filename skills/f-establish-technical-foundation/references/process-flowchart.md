# Process Flowchart

The numbered nodes correspond to the workflow in `SKILL.md`.

```mermaid
flowchart TD
    S01[1. Locate repository root] --> S02[2. Read approved inputs]
    S02 --> S03{3. Architecture and repository preparation complete?}
    S03 -- No --> H01[Route to the owning earlier skill]
    S03 -- Yes --> S04[4. Check active-increment foundation scope]
    S04 --> S05[5. Inspect repository foundation]
    S05 --> S06[6. Run read-only inspector]
    S06 --> S07[7. Identify missing or contradictory elements]
    S07 --> S08{8. Product or architecture conflict?}
    S08 -- Yes --> H01
    S08 -- No --> S09[9. Define smallest viable foundation]
    S09 --> S10[10. Define pytest and technical smoke tests]
    S10 --> S11[11. Define commands, CI, and documentation]
    S11 --> S12[12. Present exact proposal and wait]
    S12 --> A01{Approved?}
    A01 -- No --> S12
    A01 -- Yes --> S13[13. Re-read affected state]
    S13 --> S14[14. Apply approved foundation changes]
    S14 --> S15[15. Run repository checks and validator]
    S15 --> V01{Validation passes?}
    V01 -- No --> S16[16. Fix foundation defects]
    S16 --> S15
    V01 -- Yes --> S17[17. Review final diff]
    S17 --> S18[18. Set Pending Approval and request acceptance]
    S18 --> A02{Accepted?}
    A02 -- Corrections --> S14
    A02 -- Yes --> S19[19. Set Complete and hand off]
```
