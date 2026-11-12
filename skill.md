---
name: mailpit
description: Catch, inspect, and test email in development and CI with Mailpit, the open-source fake SMTP server with a web UI and REST API. Use when configuring an app to send email locally, running Mailpit in Docker or Docker Compose, asserting email content in automated tests, or troubleshooting connection refused, missing emails, reverse-proxy 403 errors, or SMTP auth and TLS errors.
license: MIT
compatibility: Written for Mailpit v1.33. Mailpit runs as a single binary on macOS, Linux, and Windows, or as the axllent/mailpit Docker image.
metadata:
  author: Isaac Tony
  version: "1.33"
  docs: https://mailpit-community-docs.mintlify.site
  official-docs: https://mailpit.axllent.org/docs/
---

# Mailpit

Mailpit captures email. Apps send to its SMTP server, and it stores each message and shows it in a web UI and a REST API. It never delivers email to real recipients unless a relay is explicitly configured.

These are unofficial community docs. Full docs: https://mailpit-community-docs.mintlify.site. Page index: https://mailpit-community-docs.mintlify.site/llms.txt.

## Defaults to assume

| Setting | Default |
| :-- | :-- |
| SMTP | port `1025`, all interfaces, no auth, no TLS |
| Web UI and API | `http://localhost:8025`, API under `/api/v1` |
| Storage | temporary, deleted when Mailpit stops |
| Messages kept | newest 500 |
| Max message size | 50 MB, max 100 recipients |

Every flag has an `MP_` environment variable, for example `--max` → `MP_MAX_MESSAGES`, `--database` → `MP_DATABASE`, `--smtp` → `MP_SMTP_BIND_ADDR`, `--listen` → `MP_UI_BIND_ADDR`. Unknown env vars are silently ignored, so check spelling.

## Before you act

- Ask or check where the app runs (host, Docker, Compose, CI) before choosing the SMTP host.
- Never invent flags. Run `mailpit --help` or check the docs.

## Choose the SMTP host

| App runs | Mailpit runs | Host |
| :-- | :-- | :-- |
| On the machine | On the machine, or Docker with `-p 1025:1025` | `localhost:1025` |
| Compose service | Same Compose project | `mailpit:1025` (service name) |
| Container | On the machine | `host.docker.internal:1025` (Linux: add `extra_hosts: ["host.docker.internal:host-gateway"]`) |

`localhost` inside a container is the container itself and gives `Connection refused`.

## Common tasks

Run: `docker run -d --name mailpit -p 8025:8025 -p 1025:1025 axllent/mailpit` or `brew install mailpit && mailpit`.

Keep messages: `--database /data/mailpit.db` (`MP_DATABASE`), plus a Docker volume on `/data`.

Read the newest message: `curl -s http://localhost:8025/api/v1/message/latest`. `latest` works anywhere an ID is expected.

Test pattern: `DELETE /api/v1/messages` (no body = delete all) → trigger email → poll `GET /api/v1/search?query=<url-encoded query>` until `messages_count > 0` → `GET /api/v1/message/<ID>` and assert on `From`, `To`, `Subject`, `Text`, `HTML`.

Search: `to:`, `from:`, `subject:"…"`, `addressed:`, `tag:`, `is:unread`, `has:attachment`, `before:yyyy/mm/dd`, `after:yyyy/mm/dd`, `!` negates. `to:` searches the To header only. Use `addressed:` to also match Bcc and envelope recipients.

CI (GitHub Actions): service container `axllent/mailpit:v1.33` with ports `1025:1025` and `8025:8025`, then wait on `curl -sf http://localhost:8025/readyz`.

Health check: `mailpit readyz` (exit 0 ready, 1 not). In Compose: `test: ["CMD", "/mailpit", "readyz"]`.

Send over HTTP: `POST /api/v1/send` with JSON `{"From":{"Email":…},"To":[{"Email":…}],"Subject":…,"Text":…}`. `From` is required.

## Rules that are easy to get wrong

- **Webhooks** (`--webhook-url`) are limited to one every `--webhook-limit` seconds (default 1). Extra messages are skipped, not queued, and failures aren't retried. Use `--webhook-limit 0` or the `/api/events` websocket to see every message.
- **SMTP auth** (`--smtp-auth-file`) needs a TLS cert, or Mailpit refuses to start. For local tests use `--smtp-auth-allow-insecure` or `--smtp-auth-accept-any`.
- **Reverse proxy:** preserve the `Host` header (nginx `proxy_set_header Host $http_host;`, Apache `ProxyPreserveHost On`), proxy websockets, and set `--webroot /path/` for sub-paths. Otherwise you get `403` on PUT/DELETE or `404` pages.
- **Release** needs a relay: `--smtp-relay-config relay.yaml` or `MP_SMTP_RELAY_HOST`. Without one, release returns `400 … error connecting to :0`.
- **Chaos** must be enabled at startup (`--enable-chaos` or `MP_ENABLE_CHAOS=true`). Then `PUT /api/v1/chaos` with `{"Recipient":{"ErrorCode":451,"Probability":100}}`.
- `MP_DATA_FILE` is the deprecated name for `MP_DATABASE`.
- `/view/<ID>.html` returns 404 when the message has no HTML part. Use `.txt`.
- **No IMAP.** Mailpit has never supported IMAP. Mail clients can use POP3 on port 1110, which starts only with `--pop3-auth-file`.
- Framework host settings: Laravel `MAIL_HOST`, Symfony `MAILER_DSN=smtp://host:1025`, Django `EMAIL_HOST`, Rails `smtp_settings[:address]`, Nodemailer `host`, Spring `spring.mail.host`.

## Troubleshooting map

| Symptom | Page |
| :-- | :-- |
| Connection refused on 1025 | https://mailpit-community-docs.mintlify.site/troubleshooting/cant-connect-to-smtp.md |
| Sent but not in Mailpit | https://mailpit-community-docs.mintlify.site/troubleshooting/emails-dont-appear.md |
| Blank page or 403 behind proxy | https://mailpit-community-docs.mintlify.site/troubleshooting/blank-page-or-403-behind-proxy.md |
| 530, 535, STARTTLS, or certificate errors | https://mailpit-community-docs.mintlify.site/troubleshooting/smtp-auth-and-tls-errors.md |
