"""
Cookie-based authentication helpers for LinkedIn.

Uses li_at cookie and JSESSIONID for CSRF token.
"""
import os
from typing import Tuple


def load_auth(
    li_at: str = None,
    csrf_token: str = None,
    auth_file: str = None,
) -> Tuple[str, str]:
    """
    Load LinkedIn authentication credentials.

    Priority:
    1. Direct parameters
    2. Auth file (.env format)
    3. Environment variables
    4. Default auth file (~/.hermes/linkedin-auth.env)

    Returns:
        Tuple of (li_at, csrf_token)
    """
    if li_at:
        return li_at, csrf_token or ""

    if auth_file and os.path.exists(auth_file):
        return _load_env_file(auth_file)

    env_li_at = os.environ.get("LINKEDIN_LI_AT")
    env_csrf = os.environ.get("LINKEDIN_JSESSIONID")
    if env_li_at:
        return env_li_at, env_csrf or ""

    default_path = os.path.expanduser("~/.hermes/linkedin-auth.env")
    if os.path.exists(default_path):
        return _load_env_file(default_path)

    raise ValueError(
        "No LinkedIn authentication found. "
        "Provide li_at directly, set LINKEDIN_LI_AT env var, "
        "or create ~/.hermes/linkedin-auth.env"
    )


def _load_env_file(filepath: str) -> Tuple[str, str]:
    """Load auth from .env file."""
    li_at = ""
    csrf = ""

    with open(filepath, "r") as f:
        for line in f:
            line = line.strip()
            if line.startswith("export "):
                line = line[7:]
            if "=" in line:
                key, value = line.split("=", 1)
                value = value.strip('"').strip("'")
                if key == "LINKEDIN_LI_AT":
                    li_at = value
                elif key == "LINKEDIN_JSESSIONID":
                    csrf = value

    if not li_at:
        raise ValueError(f"No LINKEDIN_LI_AT found in {filepath}")

    return li_at, csrf


def build_cookie_string(li_at: str, csrf_token: str = "") -> str:
    """Build cookie string for API requests."""
    cookies = [f"li_at={li_at}"]
    if csrf_token:
        # NOTE: JSESSIONID must NOT be quoted —会导致 401
        cookies.append(f"JSESSIONID={csrf_token}")
    return "; ".join(cookies)
