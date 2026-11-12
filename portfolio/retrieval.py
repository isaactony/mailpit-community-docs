"""Send each test question to the live docs MCP search tool and check where the answer page ranks.

Run with: python3 retrieval.py
"""
import json
import re
import urllib.request

MCP = "https://mailpit-community-docs.mintlify.site/mcp"
TOOL = "search_mailpit_community_docs"
HEADERS = {"Content-Type": "application/json", "Accept": "application/json, text/event-stream"}

# (question, regex of page paths that answer it)
TESTS = [
    ("Laravel in Docker Compose: Connection could not be established with host localhost:1025",
     r"troubleshooting/cant-connect-to-smtp|guides/send-email-from-your-app|guides/docker-compose"),
    ("all my emails in Mailpit are gone every time I restart my Docker containers",
     r"guides/keep-messages-after-restart|concepts/message-storage|resources/faq"),
    ("Mailpit behind nginx at /mailpit/ page 404 and deleting messages returns 403",
     r"troubleshooting/blank-page-or-403-behind-proxy|guides/reverse-proxy"),
    ("check in a Node.js test that a password reset email was sent and extract the link",
     r"guides/assert-email-in-tests"),
    ("Mailpit won't start after adding --smtp-auth-file",
     r"troubleshooting/smtp-auth-and-tls-errors|guides/protect-with-password-and-https"),
    ("webhook only fires for some emails when many arrive at once",
     r"guides/webhooks"),
    ("send a captured email to my real Gmail inbox",
     r"guides/release-to-a-real-smtp-server"),
    ("search to:bob@example.com doesn't find an email where bob was BCC",
     r"reference/search-filters|guides/assert-email-in-tests"),
    ("make Mailpit reject emails to test my app's retry logic",
     r"guides/simulate-smtp-failures"),
    ("connect Thunderbird to Mailpit over IMAP",
     r"resources/faq"),
]


def rpc(body, session=None):
    headers = dict(HEADERS)
    if session:
        headers["Mcp-Session-Id"] = session
    req = urllib.request.Request(MCP, json.dumps(body).encode(), headers)
    with urllib.request.urlopen(req, timeout=30) as res:
        raw = res.read().decode()
        data = [line[5:].strip() for line in raw.splitlines() if line.startswith("data:")]
        return res.headers.get("mcp-session-id"), json.loads(data[-1] if data else raw)


session, _ = rpc({"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {
    "protocolVersion": "2025-06-18", "capabilities": {}, "clientInfo": {"name": "retrieval-test", "version": "1"}}})

found = 0
for i, (question, want) in enumerate(TESTS, 1):
    _, res = rpc({"jsonrpc": "2.0", "id": 10 + i, "method": "tools/call",
                  "params": {"name": TOOL, "arguments": {"query": question}}}, session)
    text = " ".join(c.get("text", "") for c in res.get("result", {}).get("content", []))
    paths = []
    for path in re.findall(r"mintlify\.(?:site|app)/([a-z0-9/\-]+)", text):
        if path not in paths:
            paths.append(path)
    rank = next((n for n, p in enumerate(paths, 1) if re.fullmatch(want, p)), None)
    ok = rank is not None and rank <= 3
    found += ok
    print(f"{i:>2}. {'PASS' if ok else 'MISS'} rank={rank} top3={paths[:3]}")

print(f"\n{found}/{len(TESTS)} questions had an answer page in the top 3 results")
