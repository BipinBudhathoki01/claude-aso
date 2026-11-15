# Contributing

Open an issue or send a focused pull request. Include the runtime, operating system, exact command, and redacted input for bugs.

Use Python 3.10+. Helpers use only the standard library. Run `python -m unittest discover -s tests -v` before submitting script changes. CI also checks plugin manifests, bundled paths, skill frontmatter, and installers.

Keep model-provider choices in the user's AI runtime. Do not add mandatory API credentials, telemetry, a hosted service, or automatic store publishing. Keep deterministic validation separate from model recommendations.

For store guidance, cite an official source and record the verification date in `docs/SOURCES.md`. Label uncertain indexing behavior as hypotheses. Add regression coverage for script fixes. Keep secrets and private app data out of examples and issues.

For a specialist, add a focused `skills/aso-*/SKILL.md` with `name` and `description` frontmatter and document routing. Keep numeric constraints in `data/store-limits.json`.

Contributions are licensed under the repository's MIT license.
