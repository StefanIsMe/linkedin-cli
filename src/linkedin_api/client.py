#!/usr/bin/env python3
"""
LinkedIn API Client - Post to LinkedIn via Voyager GraphQL API.

Based on reverse-engineered API from browser network capture.
Uses cookie authentication (li_at + JSESSIONID).
"""

import json
import os
import re
from typing import Optional, Dict, Any
from dataclasses import dataclass

try:
    from curl_cffi import requests
except ImportError:
    print("Error: curl_cffi required. Install with: pip install curl_cffi")
    raise


@dataclass
class PostResult:
    """Result of a LinkedIn post operation."""
    success: bool
    post_urn: Optional[str] = None
    activity_urn: Optional[str] = None
    share_url: Optional[str] = None
    error: Optional[str] = None


class LinkedInClient:
    """LinkedIn API client using cookie authentication."""

    POST_ENDPOINT = "https://www.linkedin.com/voyager/api/graphql"
    QUERY_ID = "voyagerContentcreationDashShares.279996efa5064c01775d5aff003d9377"

    BASE_HEADERS = {
        "accept": "application/vnd.linkedin.normalized+json+2.1",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "en-GB,en;q=0.9",
        "content-type": "application/json; charset=UTF-8",
        "dnt": "1",
        "origin": "https://www.linkedin.com",
        "referer": "https://www.linkedin.com/feed/",
        "sec-ch-prefers-color-scheme": "dark",
        "sec-ch-ua": '"Chromium";v="146", "Not-A.Brand";v="24", "Google Chrome";v="146"',
        "sec-ch-ua-mobile": "?1",
        "sec-ch-ua-platform": '"Android"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "x-li-lang": "en_US",
        "x-li-pem-metadata": "Voyager - Sharing - CreateShare=sharing-create-content",
        "x-restli-protocol-version": "2.0.0",
    }

    def __init__(self, li_at: str, jsessionid: str, timezone: str = "Asia/Bangkok"):
        self.li_at = li_at
        self.jsessionid = jsessionid
        self.timezone = timezone
        self.session = requests.Session(impersonate="chrome133a")

    def _get_headers(self) -> Dict[str, str]:
        """Build headers with auth cookies and CSRF token."""
        headers = self.BASE_HEADERS.copy()
        headers["csrf-token"] = self.jsessionid
        # NOTE: JSESSIONID must NOT be quoted —会导致 401
        headers["cookie"] = f"li_at={self.li_at}; JSESSIONID={self.jsessionid}"

        headers["x-li-track"] = json.dumps({
            "clientVersion": "1.13.42903",
            "mpVersion": "1.13.42903",
            "osName": "web",
            "timezoneOffset": 7,
            "timezone": self.timezone,
            "deviceFormFactor": "DESKTOP",
            "mpName": "voyager-web",
            "displayDensity": 1,
            "displayWidth": 1366,
            "displayHeight": 768
        })

        return headers

    def _build_post_payload(self, text: str, visibility: str = "ANYONE") -> Dict[str, Any]:
        return {
            "queryId": self.QUERY_ID,
            "variables": {
                "post": {
                    "allowedCommentersScope": "ALL",
                    "commentary": {"attributesV2": [], "text": text},
                    "intendedShareLifeCycleState": "PUBLISHED",
                    "origin": "FEED",
                    "visibilityDataUnion": {"visibilityType": visibility}
                }
            }
        }

    def post(self, text: str, visibility: str = "ANYONE") -> PostResult:
        """
        Create a new LinkedIn post.

        Args:
            text: Post content (supports hashtags, mentions via @)
            visibility: ANYONE (public) or CONNECTIONS

        Returns:
            PostResult with success status and post URN
        """
        url = f"{self.POST_ENDPOINT}?action=execute&queryId={self.QUERY_ID}"
        payload = self._build_post_payload(text, visibility)
        headers = self._get_headers()

        try:
            response = self.session.post(url, json=payload, headers=headers, timeout=30)

            if response.status_code == 200:
                data = response.json()

                try:
                    share_data = (data.get("data") or {}).get("data") or {}

                    gql_errors = share_data.get("errors") or []
                    if gql_errors:
                        msg = gql_errors[0].get("message", "Unknown error")
                        status = gql_errors[0].get("extensions", {}).get("status", 0)
                        if status == 409:
                            return PostResult(success=False, error=f"LinkedIn duplicate detection: {msg}")
                        return PostResult(success=False, error=f"LinkedIn API error: {msg}")

                    create_result = share_data.get("createContentcreationDashShares") or {}
                    resource_key = create_result.get("resourceKey", "")

                    if resource_key:
                        match = re.search(r"urn:li:share:(\d+)", resource_key)
                        share_id = match.group(1) if match else None

                        return PostResult(
                            success=True,
                            post_urn=resource_key,
                            share_url=f"https://www.linkedin.com/feed/update/urn:li:activity:{share_id}/" if share_id else None
                        )
                except (KeyError, TypeError) as e:
                    return PostResult(success=True, error=f"Posted but couldn't parse response: {e}")

                return PostResult(success=True)

            elif response.status_code == 401:
                return PostResult(success=False, error="Authentication failed - cookies may be expired")
            elif response.status_code == 429:
                return PostResult(success=False, error="Rate limited - wait before posting again")
            else:
                return PostResult(success=False, error=f"API error: {response.status_code} - {response.text[:200]}")

        except Exception as e:
            return PostResult(success=False, error=f"Request failed: {str(e)}")

    def test_auth(self) -> bool:
        """Test if authentication is working by hitting the /me endpoint."""
        try:
            response = self.session.get(
                "https://www.linkedin.com/voyager/api/me",
                headers=self._get_headers(),
                timeout=15
            )
            return response.status_code == 200
        except Exception:
            return False


def load_auth_from_env(env_path: str = None) -> tuple:
    """
    Load auth cookies from environment file.

    Args:
        env_path: Path to .env file (default: ~/.hermes/linkedin-auth.env)

    Returns:
        Tuple of (li_at, jsessionid)
    """
    if not env_path:
        env_path = os.path.expanduser("~/.hermes/linkedin-auth.env")

    if not os.path.exists(env_path):
        raise FileNotFoundError(
            f"Auth file not found: {env_path}\n"
            "Create it with:\n"
            "  export LINKEDIN_LI_AT='your_li_at_cookie'\n"
            "  export LINKEDIN_JSESSIONID='your_jsessionid_cookie'"
        )

    li_at = None
    jsessionid = None

    with open(env_path, "r") as f:
        for line in f:
            line = line.strip()
            if line.startswith("export LINKEDIN_LI_AT="):
                li_at = line.split("=", 1)[1].strip("'\"")
            elif line.startswith("export LINKEDIN_JSESSIONID="):
                jsessionid = line.split("=", 1)[1].strip("'\"")

    if not li_at or not jsessionid:
        raise ValueError("Auth file missing LINKEDIN_LI_AT or LINKEDIN_JSESSIONID")

    return li_at, jsessionid
