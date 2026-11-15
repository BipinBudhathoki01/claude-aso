# Claude ASO Architecture

Claude ASO splits App Store & Play Store optimization into three deterministic-first layers:

1. **Deterministic Verification (`scripts/` + `data/`)**: Exact character counting, space-waste detection in iOS keyword fields, duplicate token checking, and Android Vitals bad-behavior gate verification.
2. **Modular Sub-Skills (`skills/aso-*/SKILL.md`)**: Focused playbooks loaded on demand so context stays lean.
3. **Specialist Checklists (`agents/aso-*.md`)**: Delegate concurrently when the host supports it; otherwise apply sequentially.

The host supplies the model, tool access, permissions, and billing. No web app, model server, or extra API key is included. Instructions cannot grant capabilities the host does not provide. The public iTunes helpers are read-only; authenticated store integrations are future extension guidance.
