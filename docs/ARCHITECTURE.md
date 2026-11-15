# Claude AEO Architecture

Claude AEO splits App Store & Play Store optimization into three deterministic-first layers:

1. **Deterministic Verification (`scripts/` + `data/`)**: Exact character counting, space-waste detection in iOS keyword fields, duplicate token checking, and Android Vitals bad-behavior gate verification.
2. **Modular Sub-Skills (`skills/aeo-*/SKILL.md`)**: Focused playbooks loaded on demand so context stays lean.
3. **Parallel Sub-Agents (`agents/aeo-*.md`)**: Specialized personas invoked concurrently during `/aeo audit`.
