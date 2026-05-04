---
name: linkedin-api-cli
description: Unofficial LinkedIn CLI client. Post to LinkedIn feed via Voyager GraphQL API using cookie authentication.
tags: [linkedin, social-media, api, cli, posting]
---

# LinkedIn API CLI

Unofficial LinkedIn client using cookie-based authentication.

## Quick Start

```bash
cd ~/.hermes/skills/social-media/linkedin-api-cli
PYTHONPATH=src python3 -m linkedin_api.cli post "Your post text here"
```

## Commands

### Post to LinkedIn

```bash
# Public post
PYTHONPATH=src python3 -m linkedin_api.cli post "Hello LinkedIn!"

# Connections only
PYTHONPATH=src python3 -m linkedin_api.cli post --visibility CONNECTIONS "Team update"

# JSON output (for scripts)
PYTHONPATH=src python3 -m linkedin_api.cli post --json "Check this out!"
```

### Test Authentication

```bash
PYTHONPATH=src python3 -m linkedin_api.cli test
```

## Authentication Setup

Create `~/.hermes/linkedin-auth.env`:

```
export LINKEDIN_LI_AT="your_li_at_cookie"
export LINKEDIN_JSESSIONID="your_jsessionid_cookie"
```

Get cookies from browser DevTools (F12 → Application → Cookies → linkedin.com).

## Python API

```python
import os
import sys

# Resolve skill src directory portably
skill_dir = os.path.expanduser("~/.hermes/skills/social-media/linkedin-api-cli")
sys.path.insert(0, os.path.join(skill_dir, "src"))

from linkedin_api.client import LinkedInClient, load_auth_from_env

# Uses LINKEDIN_AUTH_ENV env var, or defaults to ~/.hermes/linkedin-auth.env
li_at, jsessionid = load_auth_from_env()
client = LinkedInClient(li_at, jsessionid)
result = client.post("Hello from the Python API!")

if result.success:
    print(f"Posted{': ' + result.share_url if result.share_url else ''}")
else:
    print(f"Failed: {result.error}")
```

## Visibility Options

- `ANYONE` — Public post (default)
- `CONNECTIONS` — Connections only

## Dependencies

- `curl_cffi` (for Chrome impersonation)
- Python 3.9+
