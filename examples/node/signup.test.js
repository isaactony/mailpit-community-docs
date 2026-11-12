// Run with: node --test signup.test.js
// Requires Node.js 18+ and a running Mailpit (SMTP on 1025, API on 8025).
const { test, before } = require("node:test");
const assert = require("node:assert");
const nodemailer = require("nodemailer");

const MAILPIT_API = process.env.MAILPIT_API || "http://localhost:8025/api/v1";
const smtp = nodemailer.createTransport({ host: "localhost", port: 1025, secure: false });

// Stand-in for your app's code that sends a sign-up email.
async function sendSignupEmail(to) {
  await smtp.sendMail({
    from: "App <noreply@example.com>",
    to,
    subject: "Confirm your email",
    text: "Confirm your account: https://app.example.com/confirm?token=abc123",
  });
}

// Poll the search API until a matching message arrives, or fail after the timeout.
async function waitForMessage(query, timeoutMs = 5000) {
  const deadline = Date.now() + timeoutMs;
  while (Date.now() < deadline) {
    const res = await fetch(`${MAILPIT_API}/search?query=${encodeURIComponent(query)}`);
    const body = await res.json();
    if (body.messages_count > 0) return body.messages[0];
    await new Promise((resolve) => setTimeout(resolve, 200));
  }
  throw new Error(`No message matched "${query}" within ${timeoutMs} ms`);
}

before(async () => {
  // Start every run with an empty mailbox.
  await fetch(`${MAILPIT_API}/messages`, { method: "DELETE" });
});

test("sign-up sends a confirmation email with a link", async () => {
  await sendSignupEmail("new-user@example.com");

  const summary = await waitForMessage('to:new-user@example.com subject:"Confirm your email"');
  const message = await (await fetch(`${MAILPIT_API}/message/${summary.ID}`)).json();

  assert.strictEqual(message.From.Address, "noreply@example.com");
  const link = message.Text.match(/https:\/\/app\.example\.com\/confirm\?token=\w+/);
  assert.ok(link, "confirmation link not found in the email body");
});
