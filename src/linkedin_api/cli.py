#!/usr/bin/env python3
"""
LinkedIn CLI - Command-line interface for posting to LinkedIn.

Usage:
    python3 -m linkedin_api.cli post "Your post text here"
    python3 -m linkedin_api.cli post --visibility CONNECTIONS "Team update"
    python3 -m linkedin_api.cli test
"""

import argparse
import json
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from linkedin_api.client import LinkedInClient, load_auth_from_env


def cmd_post(args):
    """Create a new LinkedIn post."""
    try:
        li_at, jsessionid = load_auth_from_env(args.auth_file)
    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    client = LinkedInClient(li_at, jsessionid)
    result = client.post(args.text, visibility=args.visibility)

    if args.json:
        output = {
            "success": result.success,
            "post_urn": result.post_urn,
            "share_url": result.share_url,
            "error": result.error
        }
        print(json.dumps(output, indent=2))
    else:
        if result.success:
            print(f"Posted successfully")
            if result.share_url:
                print(f"  URL: {result.share_url}")
            if result.error:
                print(f"  Note: {result.error}")
        else:
            print(f"Failed: {result.error}", file=sys.stderr)

    return 0 if result.success else 1


def cmd_test(args):
    """Test authentication."""
    try:
        li_at, jsessionid = load_auth_from_env(args.auth_file)
    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    print("Auth credentials loaded:")
    print(f"  li_at: {li_at[:20]}...{li_at[-10:]}")
    print(f"  JSESSIONID: {jsessionid[:10]}...")

    client = LinkedInClient(li_at, jsessionid)

    if client.test_auth():
        print("\nAuthentication: VALID")
        print("  Cookies work with LinkedIn API")
        return 0
    else:
        print("\nAuthentication: INVALID", file=sys.stderr)
        print("  Cookies may be expired — re-extract from Chrome DevTools", file=sys.stderr)
        return 1


def main():
    parser = argparse.ArgumentParser(
        description="LinkedIn CLI - Post to LinkedIn from command line",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  Post a simple status:
    python3 -m linkedin_api.cli post "Hello LinkedIn!"

  Post with visibility restriction:
    python3 -m linkedin_api.cli post --visibility CONNECTIONS "Team update"

  Post with JSON output:
    python3 -m linkedin_api.cli post --json "Check this out!"

  Test authentication:
    python3 -m linkedin_api.cli test
"""
    )

    parser.add_argument(
        "--auth-file",
        help="Path to auth.env file (default: ~/.hermes/linkedin-auth.env)"
    )

    sub = parser.add_subparsers(dest="command", help="Command to run")

    post_parser = sub.add_parser("post", help="Create a new post")
    post_parser.add_argument("text", help="Post content text")
    post_parser.add_argument(
        "--visibility",
        choices=["ANYONE", "CONNECTIONS"],
        default="ANYONE",
        help="Post visibility (default: ANYONE/public)"
    )
    post_parser.add_argument(
        "--json", action="store_true", dest="json",
        help="Output as JSON"
    )

    sub.add_parser("test", help="Test authentication")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    commands = {"post": cmd_post, "test": cmd_test}

    handler = commands.get(args.command)
    if handler:
        return handler(args)
    else:
        print(f"Unknown command: {args.command}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
