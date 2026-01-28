#!/usr/bin/env python3
"""
Sentry Debug Helper - Fetch and format error data for debugging.

Usage:
    python sentry_debug.py issues [--project PROJECT] [--query QUERY] [--period PERIOD]
    python sentry_debug.py event ISSUE_ID
    python sentry_debug.py stacktrace ISSUE_ID

Environment:
    SENTRY_AUTH_TOKEN - Required API token
    SENTRY_ORG - Organization slug (or pass --org)
    SENTRY_PROJECT - Default project (or pass --project)
"""

import os
import sys
import json
import argparse
from urllib.request import Request, urlopen
from urllib.error import HTTPError

BASE_URL = "https://sentry.io/api/0"

def get_token():
    token = os.environ.get("SENTRY_AUTH_TOKEN")
    if not token:
        print("Error: SENTRY_AUTH_TOKEN environment variable not set", file=sys.stderr)
        sys.exit(1)
    return token

def api_request(endpoint, token):
    """Make authenticated request to Sentry API."""
    url = f"{BASE_URL}{endpoint}"
    req = Request(url, headers={"Authorization": f"Bearer {token}"})
    try:
        with urlopen(req) as response:
            return json.loads(response.read().decode())
    except HTTPError as e:
        print(f"API Error {e.code}: {e.reason}", file=sys.stderr)
        if e.code == 401:
            print("Check your SENTRY_AUTH_TOKEN", file=sys.stderr)
        sys.exit(1)

def list_issues(org, project, query="is:unresolved", period="24h", token=None):
    """List issues for a project."""
    token = token or get_token()
    endpoint = f"/projects/{org}/{project}/issues/?query={query}&statsPeriod={period}"
    issues = api_request(endpoint, token)
    
    print(f"\n{'='*60}")
    print(f"Issues in {org}/{project} ({query}, last {period})")
    print(f"{'='*60}\n")
    
    for issue in issues[:20]:  # Limit to 20
        print(f"[{issue['shortId']}] {issue['title']}")
        print(f"  ID: {issue['id']} | Events: {issue['count']} | Users: {issue['userCount']}")
        print(f"  Last seen: {issue['lastSeen']}")
        print(f"  Culprit: {issue.get('culprit', 'N/A')}")
        print()
    
    return issues

def get_latest_event(issue_id, token=None):
    """Get the latest event for an issue with full details."""
    token = token or get_token()
    endpoint = f"/issues/{issue_id}/events/latest/"
    event = api_request(endpoint, token)
    
    print(f"\n{'='*60}")
    print(f"Latest Event for Issue {issue_id}")
    print(f"{'='*60}\n")
    
    # Basic info
    print(f"Event ID: {event['eventID']}")
    print(f"Timestamp: {event['dateCreated']}")
    print(f"Message: {event.get('message', 'N/A')}")
    
    # User context
    if user := event.get('user'):
        print(f"\nUser: {user.get('email') or user.get('id') or 'Anonymous'}")
    
    # Tags
    if tags := event.get('tags'):
        print("\nTags:")
        for tag in tags[:10]:
            print(f"  {tag['key']}: {tag['value']}")
    
    # Contexts
    if contexts := event.get('contexts'):
        print("\nContexts:")
        for ctx_name, ctx_data in contexts.items():
            if isinstance(ctx_data, dict):
                summary = ', '.join(f"{k}={v}" for k, v in list(ctx_data.items())[:3])
                print(f"  {ctx_name}: {summary}")
    
    # Entries (exception, breadcrumbs, request)
    for entry in event.get('entries', []):
        if entry['type'] == 'exception':
            print("\n--- EXCEPTION ---")
            for exc in entry['data'].get('values', []):
                print(f"Type: {exc.get('type')}")
                print(f"Value: {exc.get('value')}")
        
        elif entry['type'] == 'breadcrumbs':
            print("\n--- BREADCRUMBS (last 10) ---")
            crumbs = entry['data'].get('values', [])[-10:]
            for crumb in crumbs:
                cat = crumb.get('category', 'default')
                msg = crumb.get('message', '')
                ts = crumb.get('timestamp', '')[-8:]  # Just time part
                print(f"  [{ts}] {cat}: {msg}")
        
        elif entry['type'] == 'request':
            req_data = entry['data']
            print(f"\n--- REQUEST ---")
            print(f"  {req_data.get('method', 'GET')} {req_data.get('url', 'N/A')}")
    
    return event

def extract_stacktrace(issue_id, token=None):
    """Extract clean stacktrace with file:line references."""
    token = token or get_token()
    endpoint = f"/issues/{issue_id}/events/latest/"
    event = api_request(endpoint, token)
    
    print(f"\n{'='*60}")
    print(f"Stacktrace for Issue {issue_id}")
    print(f"{'='*60}\n")
    
    for entry in event.get('entries', []):
        if entry['type'] == 'exception':
            for exc in entry['data'].get('values', []):
                print(f"Exception: {exc.get('type')}: {exc.get('value')}\n")
                
                stacktrace = exc.get('stacktrace', {})
                frames = stacktrace.get('frames', [])
                
                # Reverse to show most recent first
                for frame in reversed(frames):
                    filename = frame.get('filename', 'unknown')
                    lineno = frame.get('lineno', '?')
                    func = frame.get('function', 'unknown')
                    in_app = "→" if frame.get('inApp') else " "
                    
                    print(f"{in_app} {filename}:{lineno} in {func}()")
                    
                    if context := frame.get('context_line'):
                        print(f"    {context.strip()}")
                    print()
    
    return event

def main():
    parser = argparse.ArgumentParser(description="Sentry Debug Helper")
    parser.add_argument("--org", default=os.environ.get("SENTRY_ORG"), help="Organization slug")
    parser.add_argument("--project", default=os.environ.get("SENTRY_PROJECT"), help="Project slug")
    
    subparsers = parser.add_subparsers(dest="command", required=True)
    
    # Issues command
    issues_parser = subparsers.add_parser("issues", help="List issues")
    issues_parser.add_argument("--query", default="is:unresolved", help="Search query")
    issues_parser.add_argument("--period", default="24h", help="Time period")
    
    # Event command
    event_parser = subparsers.add_parser("event", help="Get latest event details")
    event_parser.add_argument("issue_id", help="Issue ID")
    
    # Stacktrace command
    stack_parser = subparsers.add_parser("stacktrace", help="Extract stacktrace")
    stack_parser.add_argument("issue_id", help="Issue ID")
    
    args = parser.parse_args()
    
    if args.command == "issues":
        if not args.org or not args.project:
            print("Error: --org and --project required (or set SENTRY_ORG/SENTRY_PROJECT)", file=sys.stderr)
            sys.exit(1)
        list_issues(args.org, args.project, args.query, args.period)
    
    elif args.command == "event":
        get_latest_event(args.issue_id)
    
    elif args.command == "stacktrace":
        extract_stacktrace(args.issue_id)

if __name__ == "__main__":
    main()
