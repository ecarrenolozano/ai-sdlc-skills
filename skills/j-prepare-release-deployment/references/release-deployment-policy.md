# Release Deployment Policy

## Discovery First

Classify the current release model before proposing changes:

- `Package-only`: the repository builds a package but does not deploy it.
- `Local executable`: users run the app from a checkout or installed package.
- `Local container`: Docker or Podman builds a local runtime only.
- `Internal deployment`: deployment target is private and approved.
- `Hosted deployment`: public or network-accessible runtime is approved.
- `Unknown`: release or deployment policy is not approved.

If the model is `Unknown`, ask for or route the missing decision. Do not infer hosting from the existence of a web framework, Dockerfile, workflow, or build command.

## Version And Lockfile

Change versions only when the proposal identifies:

- current version;
- target version;
- versioning rule or human decision;
- files to update;
- lockfile command and validation command.

Use lockfile updates only for deliberate dependency or metadata changes. Do not update lockfiles as incidental churn.

Use repository-approved semantic version tooling for version updates. When `bump-my-version` is configured, use it to apply patch/minor/major bumps instead of manual version editing.

Record the exact command used (for example, `uv run bump-my-version bump patch`) in release preparation evidence.

## Containers

Container work is allowed only when it supports the approved release model. Prefer local build/run verification before registry publishing. Treat public ports, bind addresses, secrets, volumes, and network exposure as architecture-sensitive decisions.

Support Docker or Podman commands according to the repository's existing convention. Do not require both unless the user asks for both.

## CI And Workflows

CI release workflow changes must use the same checks documented for local development when possible. Do not add deployment secrets, package registry credentials, GitHub release publishing, or environment promotions without explicit approval.

## Documentation

Release/deployment docs should describe the approved artifact, commands, constraints, and known limitations. They should not document unsupported hosting paths as if they are approved.
