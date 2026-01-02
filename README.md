# Licenscope

Licenscope is a Python tool for monitoring license and entitlement expiration across multiple platforms. It loads license data from files or URLs, parses records, and sends notifications for automation and monitoring workflows.

## Features
- Config-driven sources, parsers, and notifications
- File, HTTP URL, and TLS certificate sources with optional auth, headers, and request bodies
- Regex, Jinja2, and JSON parsers
- Notification hooks for Slack, Opsgenie, and PagerDuty (currently stub outputs)

## Quick start
1. Create a config file (default: `licenscope.toml`).
2. Run the CLI.

```bash
cp templates/gitlab.toml licenscope.toml
python main.py -c licenscope.toml
```

## Configuration
Licenscope uses TOML. The top-level keys are `default_timezone`, `sources`, and `notifications`.

```toml
default_timezone = "UTC"

[[sources]]
kind = "file"
parser = "regex"
options = { path = "licenses/jira.txt", system = "jira" }
parser_options = { pattern = "(?P<system>\\w+) expires (?P<expires_at>\\d{4}-\\d{2}-\\d{2}T\\d{2}:\\d{2}:\\d{2})" }

[[sources]]
kind = "url"
parser = "jinja"
options = { url = "https://example/api/license", system = "confluence", method = "GET", headers = { "X-API-Key" = "abc123" } }
parser_options = { template = "{\"system\": \"{{ system }}\", \"expires_at\": \"{{ payload.expires_at }}\"}" }
auth = { type = "token", token = "abc123" }

[[sources]]
kind = "url"
parser = "json"
options = { url = "https://example/api/license", system = "cortex-xdr" }
parser_options = { key = ".reply.pro_cloud_expiration", date_formats = ["%b %d %Y %H:%M:%S"] }

[[sources]]
kind = "certificate"
parser = "json"
options = { host = "example.com", port = 443 }
parser_options = { key = "." }

[[notifications]]
kind = "slack"
options = { webhook_url = "https://hooks.slack.com/..." }
```

### Sources
- `file`: `options = { path = "...", system = "..." }`
- `url`: `options = { url = "...", system = "...", method = "GET", headers = { "Header-Name" = "value" }, body = "..." }`, optional `auth = { type = "basic" | "token", ... }`
- `certificate`: `options = { host = "...", port = 443, system = "...", server_name = "...", timeout = 10 }`. For deeper certificate analysis and management, consider [ssleek](https://ssleek.com/).

### Parsers
- `regex`: expects a named group `expires_at` in a supported datetime format. Optional `system` group overrides the source context. Any group prefixed with `meta_` is placed into record metadata.
- `jinja`: renders the template with `payload` plus source context, then parses JSON. Output can be a single object or list of objects with `expires_at` in a supported datetime format.
- `json`: reads a JSON payload and resolves a dotted path to an expiration value (example: `.reply.pro_cloud_expiration`). If the resolved value is a list, one record is emitted per element. If an element is an object, it must include `expires_at`.

The `json` parser supports optional `date_formats` (list of `strptime` patterns) and `timestamp_unit` (`auto`, `seconds`, `milliseconds`). It strips ordinal suffixes like `19th` to support dates such as `Dec 19th 2025 23:59:59`.

### Notifications
- `slack`, `opsgenie`, `pagerduty`

Note: notification implementations currently print a stub message to stdout so you can validate wiring.

## Templates
Sample TOML configurations live in `templates/` and focus on URL-based APIs with the `json` parser. Copy one into `licenscope.toml` and update placeholders like `FQDN_HERE` and `TOKEN_HERE`.

Available templates:
- `templates/cortex.toml`
- `templates/certificate.toml`
- `templates/gitlab.toml`
- `templates/nexus.toml`
- `templates/sonarqube.toml`

## Installation
This project targets Python 3.14+.

```bash
uv venv
source .venv/bin/activate
uv pip install -e .
```

If you use the Jinja parser, install `jinja2`:

```bash
uv pip install jinja2
```

## CLI

```bash
python main.py --config licenscope.toml
```

The CLI defaults to `licenscope.toml` when `--config` is not provided.
Logs are colorized by default when running in a TTY. Disable colors with `--no-color` or set a verbosity level with `--log-level DEBUG`.

## License
Apache2. See `LICENSE`.
