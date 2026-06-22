# Privacy Policy

Last updated: 2026-06-23

This plugin is a local Codex plugin intended for personal use.

## What The Hook Receives

The `UserPromptSubmit` hook may receive the normal Codex hook payload through standard input. That payload can include the current user prompt and other hook metadata provided by Codex.

## What The Hook Does With That Data

The hook reads and discards the incoming payload. It does not parse, classify, store, log, transmit, or upload the payload.

The hook returns a static router context from `.codex-plugin/prompts/router-context.md`.

## External Services

The hook does not call external services. It does not call language models, analytics services, databases, telemetry endpoints, or third-party APIs.

## Local Files

The plugin reads its own local prompt file so it can return the router context. It does not intentionally read user documents, shell history, environment files, API key files, or unrelated workspace files.

## Secrets

Do not place secrets, API keys, passwords, or private tokens in this repository. The plugin does not need any secret to run.

## Changes

If the plugin later adds logging, network calls, telemetry, model calls, or persistent storage, this policy should be updated before that version is shared.

