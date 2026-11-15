# 00-MASTER-ACTION-PLAN — {{APP_NAME}}

- **Play Package ID**: `{{PLAY_PACKAGE_ID}}`
- **App Store ID**: `{{IOS_APP_ID}}`
- **Target Launch / Release Date**: {{LAUNCH_DATE}}

## Phase 1: Research & Competitor Gaps
- Primary Keywords: {{TARGET_KEYWORDS}}
- Competitor Positioning Notes: Identify unclaimed high-intent terms in Title & Subtitle.

## Phase 2: Copy-Paste Metadata
- Google Play Title (30): `{{PLAY_TITLE}}`
- Google Play Short Description (80): `{{PLAY_SHORT}}`
- Apple App Store Name (30): `{{IOS_NAME}}`
- Apple App Store Subtitle (30): `{{IOS_SUBTITLE}}`
- Apple App Store Keywords (100): `{{IOS_KEYWORDS}}`

## Phase 3: A/B Testing Plan
- Test Surface: First 3 Screenshots / Icon / Short Description
- Run duration computed via `scripts/ab_test_planner.py`

## Phase 4: Pre-Launch Validation & Vitals Gate
- Android Crash Rate <= 1.09% (current: {{CRASH_RATE}}%)
- Android ANR Rate <= 0.47% (current: {{ANR_RATE}}%)

## Phase 5: Ongoing Review & AI Discovery (GEO) Loop
- Weekly review clustering + ARC replies <= 350 chars on Play Store
- Maintain `SoftwareApplication` JSON-LD on canonical domain
