# LinkedIn CLI — Setup Guide

---

## SECTION A — CONSENT GATE

**For the AI agent:** Before executing any setup step, present the following to the user and wait for their explicit response. Do NOT proceed past this point until the user types "yes".

**Present to user:**

> **IMPORTANT — READ BEFORE PROCEEDING**
>
> This skill uses cookie-based authentication with LinkedIn's unofficial API. This is not an official LinkedIn product.
>
> By proceeding, you agree that:
> - You take full responsibility for all actions using this skill
> - This may violate LinkedIn's Terms of Service — use at your own risk
> - The developer(s) are not responsible for account bans, data loss, or other consequences
>
> Type **"yes"** to proceed or **"exit"** to cancel.

---

## SECTION B — PREREQUISITES CHECK

**For the AI agent:** Execute each check silently. Report only if something is missing or below minimum version.

### B.1 — Check Python version (minimum: 3.9)
```
terminal(command="python3 --version 2>&1")
```
Parse output: if version string contains a number less than 3.9, abort and tell the user to upgrade Python.

### B.2 — Check pip is available
```
terminal(command="pip --version 2>&1")
```
Abort if pip not found.

### B.3 — Check curl is available
```
terminal(command="curl --version 2>&1 | head -1")
```
Abort if curl not found.

### B.4 — Check if skill is already installed
```
terminal(command="ls ~/.hermes/skills/social-media/linkedin-api-cli/SKILL.md 2>/dev/null && echo \"INSTALLED\" || echo \"NOT_INSTALLED\"")
```
Store result as `SKILL_STATUS`. Used in Section C.

### B.5 — Check which source files are present (if skill installed)
```
terminal(command="ls ~/.hermes/skills/social-media/linkedin-api-cli/src/linkedin_api/ 2>/dev/null | sort")
```
Store list. Used in Section C.

### B.6 — Check if curl_cffi is installed
```
terminal(command="pip show curl_cffi 2>/dev/null | grep \"^Version:\" || echo \"NOT_INSTALLED\"")
```

### B.7 — Check if .env file exists
```
terminal(command="ls ~/.hermes/linkedin-auth.env 2>/dev/null && echo \"EXISTS\" || echo \"NOT_FOUND\"")
```
Store result. Used in Section D.

---

## SECTION C — INSTALL OR UPDATE SKILL

**For the AI agent:** Branch based on `SKILL_STATUS` from B.4.

### C.1 — If NOT_INSTALLED: Full install

```
terminal(command="mkdir -p ~/.hermes/skills/social-media/linkedin-api-cli/src/linkedin_api")
```

```
terminal(command="curl -fsSL https://raw.githubusercontent.com/StefanIsMe/linkedin-cli/main/SKILL.md -o ~/.hermes/skills/social-media/linkedin-api-cli/SKILL.md && echo \"DONE\"")
```

```
terminal(command="cd ~/.hermes/skills/social-media/linkedin-api-cli && for f in __init__.py __main__.py client.py cli.py auth.py; do curl -fsSL \"https://raw.githubusercontent.com/StefanIsMe/linkedin-cli/main/src/linkedin_api/$f\" -o \"src/linkedin_api/$f\" && echo \"DONE:$f\"; done")
```

### C.2 — If INSTALLED: Incremental update

```
terminal(command="cd ~/.hermes/skills/social-media/linkedin-api-cli && for f in __init__.py __main__.py client.py cli.py auth.py; do remote_hash=$(curl -fsSL \"https://raw.githubusercontent.com/StefanIsMe/linkedin-cli/main/src/linkedin_api/$f\" | sha256sum | cut -d' ' -f1); local_hash=$(sha256sum \"src/linkedin_api/$f\" 2>/dev/null | cut -d' ' -f1); if [ \"$remote_hash\" != \"$local_hash\" ]; then curl -fsSL \"https://raw.githubusercontent.com/StefanIsMe/linkedin-cli/main/src/linkedin_api/$f\" -o \"src/linkedin_api/$f\" && echo \"UPDATED:$f\"; else echo \"CURRENT:$f\"; fi; done")
```

```
terminal(command="remote_hash=$(curl -fsSL https://raw.githubusercontent.com/StefanIsMe/linkedin-cli/main/SKILL.md | sha256sum | cut -d' ' -f1); local_hash=$(sha256sum ~/.hermes/skills/social-media/linkedin-api-cli/SKILL.md 2>/dev/null | cut -d' ' -f1); if [ \"$remote_hash\" != \"$local_hash\" ]; then curl -fsSL https://raw.githubusercontent.com/StefanIsMe/linkedin-cli/main/SKILL.md -o ~/.hermes/skills/social-media/linkedin-api-cli/SKILL.md && echo \"UPDATED:SKILL.md\"; else echo \"CURRENT:SKILL.md\"; fi")
```

---

## SECTION D — INSTALL DEPENDENCY

**For the AI agent:** Skip if curl_cffi already installed (from B.6).

```
terminal(command="pip show curl_cffi 2>/dev/null | grep -q \"^Version:\" && echo \"SKIPPED:already installed\" || pip install curl_cffi 2>&1 | tail -3")
```

---

## SECTION E — COOKIE SETUP

**For the AI agent:** Present cookie options to the user. Wait for them to complete the manual step and confirm. Do NOT attempt to extract cookies automatically unless the user explicitly requests Option C.

### Present to user:

> **Cookie Setup Required**
>
> To post on your LinkedIn account, you need your session cookies from a browser where you're logged into LinkedIn.
>
> **Option A — Recommended:** Get cookies manually from Chrome/Firefox
> 1. Open linkedin.com in your browser and log in
> 2. Press F12 → Application → Cookies → linkedin.com
> 3. Copy the `li_at` value
> 4. Copy the `JSESSIONID` value (may have `ajax:` prefix — include it)
> 5. Paste both into the file `~/.hermes/linkedin-auth.env` in this format:
>
> ```
> export LINKEDIN_LI_AT="YOUR_LI_AT_VALUE"
> export LINKEDIN_JSESSIONID="YOUR_JSESSIONID_VALUE"
> ```
>
> Then tell Hermes "cookies added" to continue.
>
> **Option B — Hermes auto-extract via browser (NOT recommended):**
> If you want Hermes to try extracting cookies from your current LinkedIn session, say "extract cookies".
> This requires an active Chrome CDP connection and is less secure.
>
> **Do NOT paste raw cookies into chat** — they appear in message history.

### E.1 — After user confirms cookies are in place

```
terminal(command="ls ~/.hermes/linkedin-auth.env 2>/dev/null && echo \"READY\" || echo \"MISSING\"")
```

If MISSING: tell the user the file was not found and ask them to try again.

---

## SECTION F — VERIFY AUTHENTICATION

**For the AI agent:** Execute the auth test and report result to the user.

```
terminal(command="PYTHONPATH=~/.hermes/skills/social-media/linkedin-api-cli/src python3 -m linkedin_api.cli test 2>&1")
```

Parse output:
- If contains "VALID" → report success to user, proceed to Section G
- If contains "INVALID" → report that cookies may be expired and ask user to get fresh ones and update the .env file

---

## SECTION G — POST FIRST UPDATE

**For the AI agent:** Ask user if they want to post a test update now, or skip.

### Present to user:

> **Ready to post!**
>
> Authentication verified. Would you like to post a test update now?
>
> Or say "skip" and post later using:
> ```
> PYTHONPATH=~/.hermes/skills/social-media/linkedin-api-cli/src python3 -m linkedin_api.cli post "Your message"
> ```

### G.1 — If user confirms and provides text

```
terminal(command="PYTHONPATH=~/.hermes/skills/social-media/linkedin-api-cli/src python3 -m linkedin_api.cli post \"USER_PROVIDED_TEXT\" 2>&1")
```

Report the result URL to the user.

---

## SECTION H — DONE

**For the AI agent:** Report completion to the user.

### Present to user:

> **Setup complete.**
>
> Skill installed at: `~/.hermes/skills/social-media/linkedin-api-cli/`
> Auth file: `~/.hermes/linkedin-auth.env`
>
> To post: `PYTHONPATH=~/.hermes/skills/social-media/linkedin-api-cli/src python3 -m linkedin_api.cli post "Your message"`
>
> Cookies typically expire every few weeks. Re-extract fresh cookies from your browser when posting fails.

---

## UNINSTALL

**For the AI agent:** Execute on user request.

```
terminal(command="rm -rf ~/.hermes/skills/social-media/linkedin-api-cli ~/.hermes/linkedin-auth.env && echo \"DONE\"")
```

---

## TROUBLESHOOTING REFERENCE

**For the AI agent:** Use these when the user reports problems.

| Problem | Check | Fix |
|---------|-------|-----|
| "Authentication: INVALID" | Cookies expired? | User re-extracts fresh cookies from browser |
| "TooManyRedirects" | Cookies expired or LinkedIn blocking | Fresh cookies |
| "curl_cffi not found" | Dependency not installed | Re-run Section D |
| File not found on import | Source files missing | Re-run Section C |
| Python version error | Python < 3.9 | User upgrades Python |
