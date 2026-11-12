# Run with: pytest test_signup.py
# Requires Python 3.9+, pytest, and a running Mailpit (SMTP on 1025, API on 8025).
import json
import os
import re
import smtplib
import time
import urllib.parse
import urllib.request
from email.message import EmailMessage

import pytest

MAILPIT_API = os.environ.get("MAILPIT_API", "http://localhost:8025/api/v1")


def api(method, path):
    req = urllib.request.Request(f"{MAILPIT_API}{path}", method=method)
    with urllib.request.urlopen(req, timeout=5) as res:
        body = res.read()
        return json.loads(body) if res.headers.get_content_type() == "application/json" else body


def send_signup_email(to):
    """Stand-in for your app's code that sends a sign-up email."""
    msg = EmailMessage()
    msg["From"] = "App <noreply@example.com>"
    msg["To"] = to
    msg["Subject"] = "Confirm your email"
    msg.set_content("Confirm your account: https://app.example.com/confirm?token=abc123")
    with smtplib.SMTP("localhost", 1025) as smtp:
        smtp.send_message(msg)


def wait_for_message(query, timeout=5.0):
    """Poll the search API until a matching message arrives."""
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        result = api("GET", "/search?query=" + urllib.parse.quote(query))
        if result["messages_count"] > 0:
            return result["messages"][0]
        time.sleep(0.2)
    raise AssertionError(f'No message matched "{query}" within {timeout} s')


@pytest.fixture(autouse=True)
def empty_mailbox():
    api("DELETE", "/messages")


def test_signup_sends_confirmation_link():
    send_signup_email("new-user@example.com")

    summary = wait_for_message('to:new-user@example.com subject:"Confirm your email"')
    message = api("GET", f"/message/{summary['ID']}")

    assert message["From"]["Address"] == "noreply@example.com"
    assert re.search(r"https://app\.example\.com/confirm\?token=\w+", message["Text"])
