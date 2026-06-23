# Changelog

## 0.1.6+codex.20260623094606 - 2026-06-23

### Changed

- Reworked the cognitive-adaptation skill from a fixed output contract into adaptive rules with progressive disclosure.
- Kept the required backbone short: plain-language conclusion, step-by-step breakdown, and short paragraphs.
- Made terminology breakdown, examples, analogies, evidence layering, and action items conditional on the user's current sticking point.
- Updated the router context to require reading the skill without reintroducing fixed templates or old hardening language.
- Replaced the legacy global prompt with the same adaptive component-selection model used by the skill.

### Removed

- Removed the visible activation phrase requirement.
- Removed the fixed "你现在该记住什么" memory section.
- Removed forced examples for every core concept.
- Removed the hard requirement to check both official and community sources for local plugin/file inspections.

### Added

- Added adaptive-output contract tests to prevent regressions back to hard templates.
- Added a 10-case benchmark suite covering known terms, unfamiliar terms, short judgments, debug explanations, code identifiers, abstract concepts, pure action prompts, evidence layering, review explanations, and longer rule-design prompts.

### Verified

- `pytest .codex-plugin/tests -q` passes.
- `quick_validate.py` reports the skill as valid.
- The plugin was reinstalled locally as `cognitive-adaptation@personal` version `0.1.6+codex.20260623094606`.
- Final benchmark run completed all 10 cases with no timeouts and no banned follow-up phrases in final outputs.
