# LinkedIn CLI — Hermes Agent Setup

> **IMPORTANT: READ BEFORE PROCEEDING**
>
> This skill interacts with LinkedIn's unofficial API using cookie-based authentication. This is **not** an official LinkedIn product or API.
>
> **By proceeding, you acknowledge and agree that:**
> - You take full responsibility for any and all actions taken using this skill
> - This skill may violate LinkedIn's Terms of Service — use at your own risk
> - The developer(s) of this skill are **not responsible** for any account bans, data loss, security incidents, or other consequences arising from use of this skill
> - You are the sole controller of your LinkedIn account and any actions performed through it
> - You understand this skill involves scraping/intercepting LinkedIn's internal API calls
>
> **If you do not agree, type "exit" now and the setup will stop.**

---

## Step 1 — Consent

Do you agree to the above terms and take full responsibility for your actions?

Type **"yes"** to proceed or **"exit"** to cancel:

```
```

---

## Step 2 — Install the Skill

Once consent is given, the skill will be installed to `~/.hermes/skills/`:

```
```

---

## Step 3 — Cookie Authentication Setup

This skill requires your LinkedIn cookies to post on your behalf.

**Choose how you want to provide your cookies:**

**Option 1 — Manual .env file (RECOMMENDED, most secure)**
```
Create a file at ~/.hermes/linkedin-auth.env with these two lines:

export LINKEDIN_LI_AT="your_li_at_cookie_value"
export LINKEDIN_JSESSIONID="your_jsessionid_cookie_value"

To get these:
1. Open LinkedIn in Chrome/Firefox and log in
2. Press F12 → Application → Cookies → linkedin.com
3. Copy the "li_at" value
4. Copy the "JSESSIONID" value (may have "ajax:" prefix — include it)
5. Paste both into the file above
```

**Option 2 — Paste cookies into this chat (NOT RECOMMENDED)**
```
This is less secure — your cookies will appear in chat history.

If you still want to proceed, paste your cookies in this format:
LINKEDIN_LI_AT=your_li_at_value
LINKEDIN_JSESSIONID=your_jsessionid_value
```
*(Security warning: your cookies may be stored in logs, memory, or session history)*

**Option 3 — Browser auto-extract via CDP (NOT RECOMMENDED, security risk)**
```
This skill can attempt to extract cookies from your active LinkedIn browser session.
It will:
1. Check if you are logged into LinkedIn via Hermes's browser
2. If not logged in, ask you to log in manually
3. Extract the li_at and JSESSIONID cookies automatically

Security risk: This requires Hermes to have access to your browser session
and cookie storage. Only use on a trusted machine.

To proceed with Option 3, type "browser" below.
```

---

## Step 4 — Verify Authentication

After setting up your cookies, verify everything works:

```
PYTHONPATH=src /usr/bin/python3 -m linkedin_api.cli test
```

If you see **"Authentication: VALID"** — you're ready to post.

If you see **"Authentication: INVALID"** — your cookies may have expired. LinkedIn cookies typically expire after a few weeks. Re-extract fresh cookies from your browser.

---

## Step 5 — Post Your First Update

```
PYTHONPATH=src /usr/bin/python3 -m linkedin_api.cli post "Hello from LinkedIn CLI!"
```

To post to connections only:
```
PYTHONPATH=src /usr/bin/python3 -m linkedin_api.cli post --visibility CONNECTIONS "Team update"
```

For JSON output (useful for scripts):
```
PYTHONPATH=src /usr/bin/python3 -m linkedin_api.cli post --json "Your post here"
```

---

## Uninstall

To remove this skill:
```
rm -rf ~/.hermes/skills/social-media/linkedin-api-cli
rm ~/.hermes/linkedin-auth.env
```

---

## Troubleshooting

**"Authentication failed - cookies may be expired"**
→ LinkedIn cookies expire periodically. Re-extract fresh `li_at` and `JSESSIONID` from your browser (Step 2, Option 1).

**"TooManyRedirects" in curl_cffi**
→ Usually means your cookies are fully expired. Get fresh ones from your browser.

**Rate limiting**
→ LinkedIn has aggressive posting limits. Space out posts by at least 1-2 hours.
