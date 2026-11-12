# Mailpit Community Docs

Created by **[Isaac Tony](https://github.com/isaactony)**, technical writer.

Unofficial, AI-ready documentation for [Mailpit](https://github.com/axllent/mailpit), the open-source email testing tool, built with [Mintlify](https://mintlify.com).

> Live site: https://mailpit-community-docs.mintlify.site
>
> Not affiliated with the Mailpit project. The official docs are at https://mailpit.axllent.org/docs/. These docs cover Mailpit v1.33.1.

## Why these docs exist

Mailpit's official docs are accurate and complete as a feature reference. These docs reorganize the same product around **tasks and problems**, based on what users ask in Mailpit's GitHub issues, and make it readable by AI tools:

| Official docs (v1.33) | These docs |
| :-- | :-- |
| Organized by feature (Configuration, Usage, Integration) | Organized by task type: Get started, Concepts, How-to guides, Reference, Troubleshooting |
| No quickstart | A five-minute quickstart |
| No framework guides | SMTP settings for Laravel, Symfony, Django, Rails, Node.js, Python, Spring Boot, and PHP |
| No CI or test-assertion guide | Tested Node.js and Python tests, plus a GitHub Actions workflow that runs them |
| 4 troubleshooting entries | 4 symptom-based troubleshooting pages built from GitHub issues |
| Swagger 2.0 viewer | OpenAPI 3 reference with 26 generated endpoint pages |
| No llms.txt, Markdown pages, or page descriptions | llms.txt, `.md` pages, agent instructions, a custom skill.md, and an MCP server |

## Everything was tested

- Every command, option, and API call was run against Mailpit v1.33.1.
- Docker networking (`localhost` vs service name vs `host.docker.internal`), the Compose health check, volume persistence, and an nginx sub-path proxy were tested with real containers.
- The test examples in `examples/` run in CI on every push: see `.github/workflows/test-examples.yml`.
- Testing found three behaviors that are easy to get wrong, now documented: the webhook rate limit skips messages, `to:` doesn't match Bcc recipients, and misspelled `MP_` variables are silently ignored.

## Run locally

```bash
npx mint@latest dev
```

## Checks

```bash
npx mint@latest validate
npx mint@latest broken-links
npx mint@latest a11y
```

## Structure

```text
docs.json                 Navigation, theme, contextual menu, agent instructions
skill.md                  Agent skill for coding assistants
index.mdx, quickstart.mdx, install.mdx, ai-tools.mdx
concepts/                 How Mailpit works, storage, tags, security
guides/                   11 task guides
reference/                Runtime options, search filters, commands
troubleshooting/          4 symptom-based pages
resources/                FAQ, glossary, about these docs
api-reference/            Overview, websocket, and openapi.json (converted from Mailpit's Swagger 2.0)
examples/                 Tested Node.js and Python code used in the docs
portfolio/                Case study and AI question test results (not published)
```

## License

The documentation text in this repository is written independently. Facts come from Mailpit's MIT-licensed documentation and source, its GitHub issues, and testing. The API spec is derived from Mailpit's MIT-licensed Swagger file.
