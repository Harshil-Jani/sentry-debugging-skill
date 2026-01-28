# Sentry Debugging Skill

> Be a product engineer and unblock your teams by debugging production issues even faster with this skill running alongside your code.

A [Claude Code](https://docs.anthropic.com/en/docs/claude-code) skill that connects to Sentry's API to fetch, analyze, and debug production errors — right from your terminal. Instead of context-switching between your editor and Sentry's dashboard, let Claude investigate issues, parse stack traces, and suggest fixes while you stay in flow.

## What It Does

- **Fetches unresolved issues** from your Sentry projects with filtering by frequency, user, error type, or time range
- **Analyzes stack traces** and cross-references them against your local codebase to pinpoint root causes
- **Reads breadcrumbs and context** (browser, OS, user info, request data) to help reproduce issues
- **Suggests fixes** with code changes and rationale based on the error data and your source code

## Prerequisites

- A [Sentry](https://sentry.io) account with API access
- An auth token with scopes: `project:read`, `event:read`, `issue:read`
- Your organization and project slugs

## Setup

1. **Set your Sentry auth token:**

   ```bash
   export SENTRY_AUTH_TOKEN="your-token-here"
   export SENTRY_ORG="your-org-slug"
   export SENTRY_PROJECT="your-project-slug"
   ```

2. **Install the skill** in your Claude Code project:

   Copy the skill files into your project's `.claude/skills/` directory or reference them from your Claude Code configuration.

## Files

| File | Description |
|------|-------------|
| `SKILL.md` | Skill metadata and description for Claude Code |
| `sentry-debugger.skill` | Core skill definition with workflows and debugging patterns |
| `sentry-api.md` | Sentry API reference (endpoints, query syntax, response structures) |
| `sentry_debug.py` | Standalone Python CLI for fetching Sentry data |

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

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
