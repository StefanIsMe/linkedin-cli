# LinkedIn CLI

An unofficial LinkedIn command-line interface for posting, scheduling, and managing LinkedIn content directly from your terminal. Built for integration with Hermes Agent, but works standalone too.

> **Status:** Active development. LinkedIn cookie-based auth — no official API needed.

---

## Features

- Post text updates to your LinkedIn feed
- Post to specific visibility (PUBLIC or CONNECTIONS)
- JSON output for scripting and automation
- Cookie-based authentication (no OAuth, no app registration)
- Works as a standalone CLI or as a Hermes Agent skill
- Auth validation before every operation

---

## Prerequisites

- Python 3.9+
- `curl_cffi` library (automatically installed with the skill)
- A LinkedIn account with valid session cookies

---

## Install

**Paste the following into your Hermes Agent to have Hermes install the skill on your behalf:**

---

> **Skill Install Instructions**
>
> Audit the following URL and follow each step in order:
> https://github.com/StefanIsMe/linkedin-cli/blob/main/SETUP.md
>
> Follow every step in SETUP.md exactly as written, in order. The user may have already installed this skill previously — if the skill already exists at `~/.hermes/skills/social-media/linkedin-api-cli/`, check whether any files are missing or outdated compared to the repository, and update them. After installing or updating the skill, verify it works by running the auth test from Step 4 of SETUP.md.

---

## Quick Start

**1. Add your LinkedIn cookies:**

Create `~/.hermes/linkedin-auth.env`:

```bash
export LINKEDIN_LI_AT="your_li_at_cookie"
export LINKEDIN_JSESSIONID="your_jsessionid_cookie"
```

Get cookies from Chrome: F12 → Application → Cookies → linkedin.com

**2. Test authentication:**

```bash
PYTHONPATH=~/.hermes/skills/social-media/linkedin-api-cli/src \
  python3 -m linkedin_api.cli test
```

**3. Post an update:**

```bash
PYTHONPATH=~/.hermes/skills/social-media/linkedin-api-cli/src \
  python3 -m linkedin_api.cli post "Hello from LinkedIn CLI!"
```

Post to connections only:

```bash
PYTHONPATH=~/.hermes/skills/social-media/linkedin-api-cli/src \
  python3 -m linkedin_api.cli post --visibility CONNECTIONS "Team update"
```

JSON output:

```bash
PYTHONPATH=~/.hermes/skills/social-media/linkedin-api-cli/src \
  python3 -m linkedin_api.cli post --json "Your post here"
```

---

## Visibility Options

| Flag | Effect |
|------|--------|
| `--visibility PUBLIC` | Visible to anyone (default) |
| `--visibility CONNECTIONS` | Visible to 1st-degree connections only |

---

## Cookie Setup

LinkedIn session cookies typically expire after a few weeks. When authentication starts failing:

1. Open linkedin.com in Chrome
2. F12 → Application → Cookies → linkedin.com
3. Copy fresh values for `li_at` and `JSESSIONID`
4. Update `~/.hermes/linkedin-auth.env`
5. Re-run the auth test

---

## Uninstall

```bash
rm -rf ~/.hermes/skills/social-media/linkedin-api-cli
rm ~/.hermes/linkedin-auth.env
```

---

## Troubleshooting

**"Authentication: INVALID"**
→ Cookies have expired. Get fresh `li_at` and `JSESSIONID` from your browser.

**"TooManyRedirects"**
→ Usually means cookies are fully expired or LinkedIn is blocking the request. Try fresh cookies.

**"Authentication failed - too many requests"**
→ LinkedIn rate-limits posting. Wait 1-2 hours between posts.

---

## License

MIT — see [LICENSE](LICENSE)
