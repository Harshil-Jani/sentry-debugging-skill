# Sentry Debugging Skill

> Be a product engineer and unblock your teams by debugging production issues even faster with this skill running alongside your code.

A [Claude Code](https://docs.anthropic.com/en/docs/claude-code) skill that connects to Sentry's API to fetch, analyze, and debug production errors — right from your terminal. Instead of context-switching between your editor and Sentry's dashboard, let Claude investigate issues, parse stack traces, and suggest fixes while you stay in flow.

## What It Does

- **Fetches unresolved issues** from your Sentry projects with filtering by frequency, user, error type, or time range
- **Analyzes stack traces** and cross-references them against your local codebase to pinpoint root causes
- **Reads breadcrumbs and context** (browser, OS, user info, request data) to help reproduce issues
- **Suggests fixes** with code changes and rationale based on the error data and your source code

## Quick Start

**Install the skill in 2 commands:**

```bash
# 1. Clone into your Claude Code skills directory
git clone https://github.com/Harshil-Jani/sentry-debugging-skill.git ~/.claude/skills/sentry-debugging-skill

# 2. Export your Sentry token (add to your shell profile to persist)
export SENTRY_AUTH_TOKEN="your-token-here"
```

That's it. Claude Code will automatically pick up the skill.

## Generating a Sentry Personal Token

You need a **read-only** personal API token from Sentry. Here's how:

1. Go to **Settings > Account > API > Personal Tokens** in your Sentry dashboard
2. Click **Create New Token**
3. Give it only **read** permissions:
   - `project:read`
   - `event:read`
   - `issue:read`
4. Copy the generated token

![Sentry Personal Token Setup](assets/sentry-personal-token.png)

> **Security note:** Only grant read scopes. This skill never needs to modify your Sentry data.

## Configuration

Set these environment variables (add them to your `.bashrc` / `.zshrc`):

```bash
export SENTRY_AUTH_TOKEN="your-token-here"   # Required
export SENTRY_ORG="your-org-slug"             # Optional default org
export SENTRY_PROJECT="your-project-slug"     # Optional default project
```

## Usage

Once the skill is active, Claude will automatically use it when you ask things like:

- *"Check Sentry for recent errors"*
- *"What's causing crashes in production?"*
- *"Debug the TypeError users are reporting"*
- *"Investigate errors in the checkout service"*

You can also use the Python helper directly:

```bash
# List unresolved issues from the last 24 hours
python sentry_debug.py issues --org myorg --project myproject

# Get full event details for an issue
python sentry_debug.py event 12345

# Extract a clean stacktrace
python sentry_debug.py stacktrace 12345
```

## Debugging Patterns

The skill supports several investigation patterns:

- **High-frequency errors** — sort by event count to tackle the noisiest issues first
- **User-reported issues** — filter by user email or ID
- **Error type filtering** — narrow down by `TypeError`, `500` status codes, etc.
- **Time-based investigation** — scope to the last hour, day, or a custom date range

## Files

| File | Description |
|------|-------------|
| `SKILL.md` | Skill metadata and description for Claude Code |
| `sentry-debugger.skill` | Core skill definition with workflows and debugging patterns |
| `sentry-api.md` | Sentry API reference (endpoints, query syntax, response structures) |
| `sentry_debug.py` | Standalone Python CLI for fetching Sentry data |

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
