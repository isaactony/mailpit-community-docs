# Publish the Mailpit docs: your steps

Everything is built, tested, and committed locally. These steps need your GitHub and Mintlify accounts, so you do them. They take about 10 minutes.

## 1. Create the GitHub repo and push

From the `mailpit-docs` folder:

```bash
gh repo create isaactony/mailpit-community-docs --public --source . --push --description "Unofficial, AI-ready, task-based documentation for Mailpit (built with Mintlify). Not affiliated with the Mailpit project."
```

The push starts the **Test email examples** workflow (`.github/workflows/test-examples.yml`). It runs the Node.js and Python test examples from the docs against a real Mailpit container. Check that it passes in the repo's **Actions** tab. A green run proves the CI guide works.

## 2. Add the site in Mintlify

1. In the Mintlify dashboard, add a new project (or deployment) and connect the `mailpit-community-docs` repo. The docs are at the repo root.
2. Choose the subdomain `mailpit-community-docs` if it's available. The docs already use `https://mailpit-community-docs.mintlify.site`.

If your Mintlify plan allows only one site, either upgrade or replace the Hookferry site temporarily. Don't change the Hookferry repo.

## 3. If you got a different subdomain

Replace the placeholder URL everywhere, then commit and push:

```bash
grep -rl 'mailpit-community-docs.mintlify.site' --include='*.mdx' --include='*.md' . \
  | xargs sed -i '' 's#mailpit-community-docs.mintlify.site#<your-subdomain>.mintlify.site#g'
git commit -am "Use the live docs URL" && git push
```

## 4. Check the live AI features

| Check | Expected |
| :-- | :-- |
| `<site>/llms.txt` | 31 pages plus 26 API pages, each with a description |
| `<site>/quickstart.md` | Markdown with an "Agent Instructions" block |
| `<site>/skill.md` | The custom Mailpit skill from this repo |
| `<site>/mcp` | Responds to MCP clients. Test with `npx @modelcontextprotocol/inspector`. |
| Contextual menu on any page | Copy page, View as Markdown, ChatGPT, Claude, Perplexity, MCP options |

Then send me the live URL, and I'll run the MCP retrieval test against it, as I did for Hookferry.

## 5. Optional: contribute upstream

Several findings would improve the official docs and would make good pull requests to [axllent/mailpit-website](https://github.com/axllent/mailpit-website):

- A troubleshooting entry for `Connection refused` from inside Docker containers.
- A note that `to:` doesn't match Bcc recipients, and that `addressed:` does.
- A fix to the `--webhook-limit` CLI help text, which says "per second" while the behavior is "one every N seconds". That one belongs in [axllent/mailpit](https://github.com/axllent/mailpit).

Merged pull requests are public, verifiable proof for clients.
