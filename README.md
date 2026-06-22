# Cognitive Adaptation

Cognitive Adaptation is a personal Codex plugin that injects a small router context on each `UserPromptSubmit` event. The router tells the model when to load the bundled `cognitive-adaptation` skill for explanation, research, teaching, code walkthrough, review explanation, and debug explanation tasks.

The plugin is intentionally small:

- the hook reads and discards the incoming hook payload;
- the hook emits a static router context from `.codex-plugin/prompts/router-context.md`;
- the skill file defines the actual answer contract in `skills/cognitive-adaptation/SKILL.md`;
- no external service is called by the hook.

## Why This Exists

The goal is to make explanation-heavy answers easier to follow. When the router matches an explanation-style task, the model should first load the skill and then answer with a visible activation phrase, a plain-language conclusion, term explanations, step-by-step reasoning, examples, and a short memory checklist.

## Repository Layout

```text
cognitive-adaptation/
  .codex-plugin/
    plugin.json
    prompts/
      router-context.md
    tests/
      test_user_prompt_submit_hook.py
  hooks/
    hooks.json
    run-hook.cmd
    user-prompt-submit
  skills/
    cognitive-adaptation/
      SKILL.md
```

## Verification

Run the hook tests:

```bash
python -m pytest .codex-plugin/tests -q
```

Manually inspect the hook output:

```bash
printf '{"prompt":"调研一下 UserPromptSubmit 是什么"}' | ./hooks/user-prompt-submit
```

## Privacy And Terms

- Privacy policy: [PRIVACY.md](PRIVACY.md)
- Terms of service: [TERMS.md](TERMS.md)

