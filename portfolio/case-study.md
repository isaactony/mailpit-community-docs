# Case study: task-based, AI-ready docs for Mailpit

**Project:** Unofficial community documentation for [Mailpit](https://github.com/axllent/mailpit), an open-source email testing tool with about 10,900 GitHub stars
**Role:** Technical writer and information architect
**Stack:** Mintlify, MDX, OpenAPI 3, Docker, GitHub Actions
**Scope:** 31 hand-written pages, 26 generated API pages, tested code examples with CI, a custom agent skill, and an AI question test

## The problem

Mailpit's official docs are accurate, but they're organized as a feature reference: Configuration, Usage, and Integration. Users arrive with tasks and problems instead: "How do I point Laravel at Mailpit?", "Why do my emails disappear?", "Why does my nginx proxy return 403?" Mailpit's GitHub issues show the same questions asked again and again.

The docs also weren't readable by AI tools: no `llms.txt`, no Markdown versions, and no page descriptions. The API reference was a Swagger 2.0 viewer.

## Research

1. **Docs audit.** I mapped all 49 official pages and checked them against my AI readiness checklist. There was no quickstart, no framework or CI guides, 4 troubleshooting entries, and none of the AI-readiness basics.
2. **User research from GitHub.** I reviewed about 400 issues and 60 discussions to find the most common problems. The top ones were Docker networking, lost messages after restarts, reverse-proxy errors, SMTP authentication and TLS, relay errors, and testing in CI. These became the guides and troubleshooting pages.
3. **Hands-on testing.** I installed Mailpit v1.33.1 and verified every fact by running it, rather than restating existing docs.

## What testing found

Running the software caught things a desk review would have missed, including one mistake in my own first draft:

| Finding | How it was found | What the docs now say |
| :-- | :-- | :-- |
| From a container, `localhost:1025` fails, while the service name and `host.docker.internal` work | Ran three containers with Docker Compose | A host lookup table on every page where the problem can occur |
| `to:` searches the To header only, so Bcc recipients aren't found | My own first draft recommended `to:`. The test failed. | Use `addressed:`, with a tip in the testing guide |
| `--webhook-limit N` means one webhook every N seconds, not N per second as the CLI help says. Extra webhooks are skipped. | Sent bursts of email with different limits | A warning callout and a correct option table |
| Misspelled `MP_` variables are ignored without a warning | Started Mailpit with a typo | Warnings on the storage and runtime-options pages |
| A proxy that changes `Host` causes `403` on `DELETE`. Without `--webroot`, the page returns `404`. | Ran nginx in Docker with and without the setting | Exact causes on the troubleshooting page |
| SMTP auth without TLS stops Mailpit with a specific error | Started Mailpit with a password file | The error quoted verbatim, so people searching for it find the page |
| The GitHub research summary said the relay uses STARTTLS by default. The official docs say it doesn't. | Checked against the official source | The default is documented as `false` |

## What I built

- **Information architecture:** Get started, Concepts, How-to guides (11), Reference, Troubleshooting by symptom, and Resources, plus an API tab.
- **Framework guide:** one page with Laravel, Symfony, Django, Rails, Node.js, Python, Spring Boot, and PHP settings in tabs.
- **Tested code:** Node.js and Python email-assertion tests that run in GitHub Actions against a real Mailpit container on every push.
- **API reference:** Mailpit's Swagger 2.0 file converted to OpenAPI 3, with cleaned tags, a `localhost` server, and `latest` documented on every ID parameter. The interactive "Try it" console is replaced with request examples, because a hosted docs site can't reach a reader's `localhost`.
- **AI readiness:** site-wide agent instructions with Mailpit's defaults and the Docker rule, a custom `skill.md` covering the pitfalls, a skill-install prompt, a contextual menu, `llms.txt`, and MCP.
- **Clear attribution:** an unofficial-docs banner, our own visual identity, credit to the MIT-licensed sources, and links to the official docs.

## Results: AI question test

A separate AI agent, using only these docs and told not to use its prior knowledge of Mailpit, answered 10 questions drawn from the most common GitHub issue topics. One question asked about a feature Mailpit doesn't have (IMAP).

| | Round 1 | Round 2 (after fixes) |
| :-- | :-- | :-- |
| Correct answers | 10 / 10 | 3 / 3 retested |
| Low-confidence answers | 3 | 0 |
| Made-up flags, endpoints, or features | 0 | 0 |

The three low-confidence answers each pointed to a specific content gap: framework setting names missing on the troubleshooting page, a release example whose recipient filter would block Gmail, and no statement that IMAP isn't supported. Each fix was a targeted content change, and the retest answered all three with high confidence.

Full results: [ai-question-test.md](ai-question-test.md).

**After deployment:** [MCP retrieval test and `mint score` results go here.]

## Quality checks

- `mint validate`: passed (strict build)
- `mint broken-links`: no broken links
- `mint a11y`: all colors pass, no issues in 31 pages
- All 31 pages export cleanly to Markdown, with no raw components left
- All code examples run against Mailpit v1.33.1

## What this shows

- **I start from users' real problems,** taken from issue trackers, not from the feature list.
- **I verify instead of rewording.** Testing found errors in the CLI help, in a research summary, and in my own draft.
- **I build docs that AI tools answer from correctly,** and I measure it.
