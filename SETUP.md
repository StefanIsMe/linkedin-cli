# LinkedIn CLI — Setup Guide

> **IMPORTANT: READ BEFORE PROCEEDING**
>
> This skill uses cookie-based authentication to interact with LinkedIn's unofficial API. This is **not** an official LinkedIn product or API.
>
> **By proceeding, you agree that:**
> - You take full responsibility for all actions performed using this skill
> - This skill may violate LinkedIn's Terms of Service — use at your own risk
> - The developer(s) are **not responsible** for account bans, data loss, or other consequences
> - You are the sole controller of your LinkedIn account
>
> **If you do not agree, type "exit" now.**

---

## Step 1 — Consent

Before continuing, confirm you agree to the above terms.

Type **"yes"** to proceed or **"exit"** to cancel.

---

## Step 2 — Create Directory Structure

Run this in terminal:

```
terminal(command="mkdir -p ~/.hermes/skills/social-media/linkedin-api-cli/src/linkedin_api && echo \"directories created\"")
```

---

## Step 3 — Download SKILL.md

Download the skill definition file:

```
terminal(command="curl -fsSL https://raw.githubusercontent.com/StefanIsMe/linkedin-cli/main/SKILL.md -o ~/.hermes/skills/social-media/linkedin-api-cli/SKILL.md && echo \"SKILL.md downloaded\"")
```

---

## Step 4 — Download Source Files

Download all Python source files:

```
terminal(command="cd ~/.hermes/skills/social-media/linkedin-api-cli && for f in __init__.py __main__.py client.py cli.py auth.py; do curl -fsSL \"https://raw.githubusercontent.com/StefanIsMe/linkedin-cli/main/src/linkedin_api/$f\" -o \"src/linkedin_api/$f\" && echo \"downloaded: $f\"; done")
```

---

## Step 5 — Install Dependency

Install `curl_cffi` — required for API requests:

```
terminal(command="pip install curl_cffi 2>&1 | tail -3")
```

---

## Step 6 — Cookie Authentication Setup

**Choose ONE of the three options below:**

### Option A — Manual .env file (RECOMMENDED)

Create the auth file:

```
terminal(command="cat > ~/.hermes/linkedin-auth.env << 'EOF'\nexport LINKEDIN_LI_AT=\"YOUR_LI_AT_COOKIE\"\nexport LINKEDIN_JSESSIONID=\"YOUR_JSESSIONID_COOKIE\"\nEOF\necho \"linkedin-auth.env created\"")
```

**To get your cookies:**
1. Open linkedin.com in Chrome and log in
2. Press F12 → Application → Cookies → linkedin.com
3. Copy the `li_at` value
4. Copy the `JSESSIONID` value (may have `ajax:` prefix — include it)
5. Edit `~/.hermes/linkedin-auth.env` and replace the placeholder values with your actual cookies

### Option B — Paste cookies into chat (NOT RECOMMENDED)

If you want to paste cookies directly, format them as:

```
LINKEDIN_LI_AT=your_li_at_value
LINKEDIN_JSESSIONID=your_jsessionid_value
```

Then run:

```
terminal(command="cat > ~/.hermes/linkedin-auth.env << 'EOF'\nexport LINKEDIN_LI_AT=\"PASTE_LI_AT_HERE\"\nexport LINKEDIN_JSESSIONID=\"PASTE_JSESSIONID_HERE\"\nEOF")
```

**Security warning:** Cookies appear in chat history. Use Option A instead.

### Option C — Browser auto-extract via CDP (NOT RECOMMENDED)

If Hermes has an active Chrome CDP session connected to your LinkedIn browser:

1. Navigate browser to linkedin.com and confirm you are logged in
2. Run CDP to extract cookies:

```
browser_cdp(method="Storage.getCookies", params={})
```

3. Find `li_at` and `JSESSIONID` in the returned cookies
4. Write them to the auth file:

```
terminal(command="cat > ~/.hermes/linkedin-auth.env << 'EOF'\nexport LINKEDIN_LI_AT=\"EXTRACTED_LI_AT\"\nexport LINKEDIN_JSESSIONID=\"EXTRACTED_JSESSIONID\"\nEOF")
```

**Security warning:** This requires Hermes to access your browser session. Only use on a trusted machine.

---

## Step 7 — Verify Authentication

Run the auth test:

```
terminal(command="PYTHONPATH=~/.hermes/skills/social-media/linkedin-api-cli/src python3 -m linkedin_api.cli test")
```

- If you see **"Authentication: VALID"** — cookies are working, proceed to Step 8
- If you see **"Authentication: INVALID"** — cookies are expired or incorrect. Get fresh cookies from your browser and update the .env file

---

## Step 8 — Post Your First Update

Test with a simple post:

```
terminal(command="PYTHONPATH=~/.hermes/skills/social-media/linkedin-api-cli/src python3 -m linkedin_api.cli post \"Hello from LinkedIn CLI!\"")
```

To post to connections only:

```
terminal(command="PYTHONPATH=~/.hermes/skills/social-media/linkedin-api-cli/src python3 -m linkedin_api.cli post --visibility CONNECTIONS \"Team update\"")
```

For JSON output:

```
terminal(command="PYTHONPATH=~/.hermes/skills/social-media/linkedin-api-cli/src python3 -m linkedin_api.cli post --json \"Your post here\"")
```

---

## Cookie Refresh

LinkedIn cookies typically expire every few weeks. When authentication starts failing:

1. Open linkedin.com in Chrome
2. F12 → Application → Cookies → linkedin.com
3. Copy fresh `li_at` and `JSESSIONID` values
4. Edit `~/.hermes/linkedin-auth.env` with the new values
5. Re-run Step 7 to verify

---

## Uninstall

```
terminal(command="rm -rf ~/.hermes/skills/social-media/linkedin-api-cli ~/.hermes/linkedin-auth.env && echo \"uninstalled\"")
```

---

## Troubleshooting

| Error | Cause | Fix |
|-------|-------|-----|
| "Authentication: INVALID" | Cookies expired | Get fresh cookies from browser |
| "TooManyRedirects" | Cookies expired or LinkedIn blocking | Try fresh cookies |
| "Authentication failed - too many requests" | LinkedIn rate limiting | Wait 1-2 hours between posts |
| File not found on import | Source files not downloaded | Re-run Steps 3 and 4 |
