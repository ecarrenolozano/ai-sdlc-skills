# Inception Sources

This directory preserves the original information received about the project before that information is clarified, interpreted, or converted into formal project documentation.

Files in this directory are source evidence.

## Typical Sources

Examples include:

* Informal project requests.
* Requester or stakeholder emails.
* Meeting notes.
* Interview transcripts.
* Existing-system descriptions.
* Business or scientific background documents.
* Corrections or additional information supplied later.
* Links or references to external source material.

Use meaningful filenames that communicate where the information originated, for example:

```text
informal_project_request.md
requester_email_2026-07-23.md
kickoff_meeting_notes.md
stakeholder_interview_transcript.md
existing_system_overview.md
```

## Preservation Rules

Preserve every source in its original form whenever possible.

Do not:

* Rewrite a source to improve its wording.
* Replace a source with a summary.
* Add generated conclusions to a source.
* Modify an old source when new information arrives.
* Treat an interpretation as original evidence.
* Store generated workflow artifacts in this directory.

When additional documentary evidence arrives, preserve it as a new source file.

For example:

```text
requester_email_2026-07-23.md
requester_correction_2026-07-25.md
```

Do not modify the first email to incorporate the later correction.

## Chat-Based Clarifications

When a stakeholder provides an answer directly through chat and no independent document exists, record the answer in:

```text
../clarified_project_request.md
```

Include the respondent and the impact of the answer.

A separate source file is not required for every direct chat response.

## External Sources

When a source cannot be stored locally, preserve an explicit reference to it.

Record enough information to identify the source, such as:

* Document title.
* URL or system location.
* Owner or author.
* Relevant date.
* Access limitations.

Do not claim to have preserved a source locally when only an external reference exists.

## Generated Artifacts

The clarified interpretation of these sources belongs in:

```text
../clarified_project_request.md
```

The approved general project foundation belongs in:

```text
../project_context.md
```

Neither file belongs inside `sources/`.

## Scope

This directory is not a general-purpose data repository.

Do not store unrelated files or large technical assets here, such as:

* Images or videos.
* Large datasets.
* Application binaries.
* Generated results.
* Build artifacts.

Store those resources in an appropriate project data, documentation, or external storage location.
