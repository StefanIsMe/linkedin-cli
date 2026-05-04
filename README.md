# LinkedIn CLI

Unofficial LinkedIn CLI client for posting to LinkedIn via cookie-based authentication.

**⚠️ Warning:** This is not an official LinkedIn product or API. Using this tool may violate LinkedIn's Terms of Service. The developer is not responsible for any account bans or other consequences. Use at your own risk.

---

## Features

- Post text updates to LinkedIn from the command line
- Public posts or connections-only visibility
- JSON output for scripting
- Cookie-based authentication (li_at + JSESSIONID)

---

## Prerequisites

- Python 3.10+
- `curl_cffi` library

Install dependencies:

```bash
pip install curl_cffi
```

---

## Installation

### Option 1 — Clone and Install

```bash
git clone https://github.com/YOUR_USERNAME/linkedin-cli.git
cd linkedin-cli
pip install -e .
```

### Option 2 — Hermes Agent Skill

See [SETUP.md](SETUP.md) for the interactive setup process.

---

## Authentication Setup

### Step 1 — Get Your Cookies

1. Open [LinkedIn](https://www.linkedin.com) in Chrome or Firefox and log in
2. Press **F12** to open Developer Tools
3. Go to **Application** (Chrome) or **Storage** (Firefox)
4. Click **Cookies** → `https://www.linkedin.com`
5. Copy the value of **`li_at`**
6. Copy the value of **`JSESSIONID`** (may have `ajax:` prefix — include it)

### Step 2 — Save Cookies

Create a file at `~/.hermes/linkedin-auth.env`:

```bash
export LINKEDIN_LI_AT="your_li_at_cookie_value"
export LINKEDIN_JSESSIONID="your_jsessionid_cookie_value"
```

Or use the `.env.example` file:

```bash
cp .env.example ~/.hermes/linkedin-auth.env
# Then edit the file and paste your cookies
```

### Step 3 — Verify

```bash
python3 -m linkedin_api.cli test
```

You should see `Authentication: VALID`.

---

## Usage

### Command Line

```bash
# Simple public post
python3 -m linkedin_api.cli post "Hello LinkedIn!"

# Connections only
python3 -m linkedin_api.cli post --visibility CONNECTIONS "Team update"

# JSON output
python3 -m linkedin_api.cli post --json "Check this out!"

# Test auth
python3 -m linkedin_api.cli test
```

### Python API

```python
import sys
sys.path.insert(0, "/path/to/linkedin-cli/src")

from linkedin_api.client import LinkedInClient, load_auth_from_env

li_at, jsessionid = load_auth_from_env()
client = LinkedInClient(li_at, jsessionid)
result = client.post("Hello from Python!")

if result.success:
    print(f"Posted: {result.share_url}")
else:
    print(f"Failed: {result.error}")
```

---

## Cookie Refresh

LinkedIn cookies expire periodically (usually every few weeks). When authentication starts failing:

1. Go back to LinkedIn in your browser
2. Make sure you're still logged in
3. Refresh the cookies in DevTools (F12 → Application → Cookies)
4. Copy the new `li_at` and `JSESSIONID` values
5. Update `~/.hermes/linkedin-auth.env`

---

## Rate Limiting

LinkedIn has aggressive posting limits. Space out posts by at least 1-2 hours between posts to avoid account restrictions.

---

## Security Notes

- **Never share your cookies.** They give full account access.
- Store cookies only in `~/.hermes/linkedin-auth.env` — not in scripts or chat.
- Cookies in chat history can be exposed — prefer the manual `.env` file approach.
- Browser auto-extract via CDP is convenient but gives Hermes access to all your browser cookies.

---

## Troubleshooting

### "Authentication: INVALID" or "cookies may be expired"
→ Cookies are expired. Get fresh ones from your browser (see Step 1 above).

### `ModuleNotFoundError: No module named 'curl_cffi'`
→ Run `pip install curl_cffi`

### `TooManyRedirects` error
→ Usually means cookies are fully expired and LinkedIn is redirecting the auth check.

### 409 Duplicate Detection
→ LinkedIn flagged your post as a duplicate. Change the text and try again.

---

## License

MIT — see [LICENSE](LICENSE)
