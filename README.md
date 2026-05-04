# LinkedIn CLI — Hermes Agent Setup

Paste each block below into your Hermes Agent and follow the prompts.

---

## Step 1 — Install the Skill Files

```
terminal(command="mkdir -p ~/.hermes/skills/social-media/linkedin-api-cli/src/linkedin_api && echo \"dirs created\"")
```

---

## Step 2 — Download the Skill

```
terminal(command="curl -fsSL https://raw.githubusercontent.com/StefanIsMe/linkedin-cli/main/SKILL.md -o ~/.hermes/skills/social-media/linkedin-api-cli/SKILL.md && echo \"SKILL.md downloaded\"")
```

---

## Step 3 — Download the Source Code

```
terminal(command="cd ~/.hermes/skills/social-media/linkedin-api-cli && for f in __init__.py __main__.py client.py cli.py auth.py; do curl -fsSL \"https://raw.githubusercontent.com/StefanIsMe/linkedin-cli/main/src/linkedin_api/$f\" -o \"src/linkedin_api/$f\" && echo \"downloaded: $f\"; done")
```

---

## Step 4 — Install curl_cffi Dependency

```
terminal(command="pip install curl_cffi 2>&1 | tail -3")
```

---

## Step 5 — Set Up Your Cookies

See the full guide: https://github.com/StefanIsMe/linkedin-cli/blob/main/SETUP.md

Quick version — create `~/.hermes/linkedin-auth.env` with:

```
export LINKEDIN_LI_AT="YOUR_LI_AT_COOKIE"
export LINKEDIN_JSESSIONID="YOUR_JSESSIONID_COOKIE"
```

Get these from Chrome DevTools: F12 → Application → Cookies → linkedin.com

---

## Step 6 — Verify It Works

```
terminal(command="PYTHONPATH=~/.hermes/skills/social-media/linkedin-api-cli/src /usr/bin/python3 -m linkedin_api.cli test")
```

You should see **"Authentication: VALID"**.

---

## Post Your First Update

```
terminal(command="PYTHONPATH=~/.hermes/skills/social-media/linkedin-api-cli/src /usr/bin/python3 -m linkedin_api.cli post \"Hello from LinkedIn CLI!\"")
```

---

Full documentation: https://github.com/StefanIsMe/linkedin-cli
