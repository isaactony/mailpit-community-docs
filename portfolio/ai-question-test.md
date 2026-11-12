# AI question test: method and results

## Method

- **Questions:** 10 real user problems, taken from the most common topics in Mailpit's GitHub issues and discussions. One question (IMAP) asks about something Mailpit doesn't support, to check whether the AI makes things up.
- **Corpus:** the Markdown export of all 31 pages, the 26 generated API pages, and `skill.md`. That's 58 files, the same content an AI tool gets through MCP or `.md` URLs.
- **Answering model:** a separate Claude Sonnet agent, told to answer only from the docs, cite files, give a confidence level, and say when something isn't documented. It was told not to use its prior knowledge of Mailpit.
- **Grading:** each answer was checked against behavior observed by running Mailpit v1.33.1, and graded **Correct**, **Correct but low confidence** (right answer, but the docs made the AI infer or hedge), or **Wrong**.

## Round 1

| # | Question (source) | Grade | Notes |
| :-- | :-- | :-- | :-- |
| 1 | Laravel in Compose: `Connection could not be established with host localhost:1025` (Docker networking, the most common issue topic) | Correct but low confidence | Right fix (`mailpit` service name), but the troubleshooting page never named `MAIL_HOST`, so the AI mapped it itself. |
| 2 | Emails gone after restarting containers (#328, discussions) | Correct | `MP_DATABASE` plus a volume, the 500 limit, the typo warning, NFS |
| 3 | nginx sub-path: `404`, then `403` on delete (#137, #170, #639) | Correct | Both causes and both fixes |
| 4 | Node.js: assert a password-reset email and extract the link (#166) | Correct | Adapted the sign-up example. Noted that Text vs HTML extraction wasn't discussed. |
| 5 | `--smtp-auth-file` and Mailpit won't start | Correct | Quoted the exact startup error and gave three options |
| 6 | Webhook fires for only some emails in a burst | Correct | Skipped, not queued. `--webhook-limit 0` or the websocket. |
| 7 | Release a captured email to Gmail (#277) | Correct but low confidence | The example `allowed-recipients` would block Gmail, and there was no Gmail example. |
| 8 | Bcc recipient not found with `to:` | Correct | `addressed:` or `bcc:`. This came from a mistake caught during testing. |
| 9 | Make Mailpit reject email to test retries | Correct | Chaos, with 4xx vs 5xx guidance |
| 10 | Thunderbird over IMAP? (#730, #587) | Correct but low confidence | Didn't make anything up and pointed to POP3, but couldn't say IMAP was unsupported, because the docs didn't say it. |

**Round 1 result:** 10 of 10 correct, 0 wrong, 3 correct but low confidence.

## Fixes after round 1

| Finding | Fix |
| :-- | :-- |
| Q1: framework setting names missing where the error is diagnosed | Added a framework-by-framework host table (`MAIL_HOST`, `MAILER_DSN`, `EMAIL_HOST`, and others) to the connection-refused page and the skill |
| Q7: example blocks Gmail, no Gmail walkthrough | Added a note on `allowed-recipients` and a Gmail relay example with app passwords |
| Q10: IMAP not mentioned | Checked the CLI and GitHub (maintainer declined IMAP in #730), then added an FAQ entry with POP3 setup and a skill rule |
| `MP_SMTP_AUTH` vs `MP_SMTP_AUTH_FILE` easy to confuse | Reworded the troubleshooting cause to name both |
| Link extraction from HTML-only email not covered | Added guidance on Text vs HTML and the link-check endpoint |

## Round 2

A fresh agent, with no memory of round 1, retested the three low-confidence questions on the fixed docs.

| # | Question | Grade | Notes |
| :-- | :-- | :-- | :-- |
| 1 | Laravel in Compose, exact `.env` change | Correct, high confidence | `MAIL_HOST=mailpit`, plus `php artisan config:clear`. Two pages agree. |
| 7 | Release to Gmail | Correct, high confidence | Complete Gmail relay config with an app password, a matching `allowed-recipients`, and `override-from` |
| 10 | IMAP in Thunderbird | Correct, high confidence | "No", citing the maintainer's decision, with POP3 setup |

**Round 2 result:** 3 of 3 correct with high confidence.

One more finding in round 2: copying the Laravel snippet unchanged reproduces the Docker error, because it uses `localhost`. The snippet now has an inline comment pointing to the service name.

## Overall

| | Round 1 | Round 2 |
| :-- | :-- | :-- |
| Correct answers | 10 / 10 | 3 / 3 retested |
| Low-confidence answers | 3 | 0 |
| Made-up flags, endpoints, or features | 0 | 0 |

### Backlog: gaps the agent noted that didn't cause wrong answers

- Publishing POP3 port `1110` in Docker isn't shown.
- Deliverability of released email (SPF, DKIM, spam folders) isn't covered.
- An HTTPS sub-path example for nginx (the current one is port 80).
