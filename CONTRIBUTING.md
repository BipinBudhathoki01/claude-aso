# Contributing

Open an issue or send a focused pull request. Include the runtime, operating system, exact command, and redacted input for bugs.

New here? Read the [first contribution discussion](https://github.com/BipinBudhathoki01/claude-aso/discussions/2), browse [good first issues](https://github.com/BipinBudhathoki01/claude-aso/labels/good%20first%20issue), or pick a [help wanted task](https://github.com/BipinBudhathoki01/claude-aso/labels/help%20wanted). Use [Q&A](https://github.com/BipinBudhathoki01/claude-aso/discussions/categories/q-a) for usage questions and [Ideas](https://github.com/BipinBudhathoki01/claude-aso/discussions/categories/ideas) for proposals.

## Your first pull request

1. Choose an issue and comment if you plan to work on it. Discuss large changes before implementation.
2. Fork the repository, clone your fork, and create a branch such as `docs/improve-install-guide`.
3. Make one focused change. Use fictional or fully anonymized examples; do not include private app audits.
4. Run checks appropriate to the change. For helper or installer changes, run `python -m unittest discover -s tests -v`. For documentation-only changes, verify the links and instructions you changed.
5. Push the branch to your fork and open a pull request against this repository's `main` branch.
6. Explain the problem and resulting behavior, link the issue, and report the checks actually run. Use `Closes #NUMBER` when the PR resolves an issue.

Small documentation improvements and reproducible compatibility reports are welcome. A contribution does not need a new agent or feature.

## Development guidance

Use Python 3.10+. Helpers use only the standard library. Run `python -m unittest discover -s tests -v` before submitting script changes. CI also checks plugin manifests, bundled paths, skill frontmatter, and installers.

Keep model-provider choices in the user's AI runtime. Do not add mandatory API credentials, telemetry, a hosted service, or automatic store publishing. Keep deterministic validation separate from model recommendations.

For store guidance, cite an official source and record the verification date in `docs/SOURCES.md`. Label uncertain indexing behavior as hypotheses. Add regression coverage for script fixes. Keep secrets and private app data out of examples and issues.

For a specialist, add a focused `skills/aso-*/SKILL.md` with `name` and `description` frontmatter and document routing. Keep numeric constraints in `data/store-limits.json`.

Contributions are licensed under the repository's MIT license.
