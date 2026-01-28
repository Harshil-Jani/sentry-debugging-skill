# Sentry API Reference

## Table of Contents
- [Authentication](#authentication)
- [Organizations](#organizations)
- [Projects](#projects)
- [Issues](#issues)
- [Events](#events)
- [Query Parameters](#query-parameters)
- [Response Structures](#response-structures)

## Authentication

All requests require `Authorization: Bearer {token}` header.

Required scopes:
- `project:read` - List projects and their settings
- `event:read` - Read event data
- `issue:read` - Read issue data

## Organizations

### List Organizations
```
GET https://sentry.io/api/0/organizations/
```

### Get Organization Details
```
GET https://sentry.io/api/0/organizations/{org_slug}/
```

## Projects

### List Projects in Organization
```
GET https://sentry.io/api/0/organizations/{org_slug}/projects/
```

### Get Project Details
```
GET https://sentry.io/api/0/projects/{org_slug}/{project_slug}/
```

## Issues

### List Issues
```
GET https://sentry.io/api/0/projects/{org_slug}/{project_slug}/issues/
```

Query parameters:
- `query` - Search query (e.g., `is:unresolved`, `user.email:x@y.com`)
- `statsPeriod` - Time period (`1h`, `24h`, `7d`, `14d`, `30d`)
- `sort` - Sort order (`date`, `freq`, `new`, `priority`)
- `limit` - Number of results (default 25, max 100)
- `cursor` - Pagination cursor

### Get Issue Details
```
GET https://sentry.io/api/0/issues/{issue_id}/
```

### Get Issue Hashes
```
GET https://sentry.io/api/0/issues/{issue_id}/hashes/
```

### Update Issue (resolve, ignore, etc.)
```
PUT https://sentry.io/api/0/issues/{issue_id}/
```
Body: `{"status": "resolved"}` or `{"status": "ignored"}`

## Events

### List Events for Issue
```
GET https://sentry.io/api/0/issues/{issue_id}/events/
```

### Get Latest Event for Issue
```
GET https://sentry.io/api/0/issues/{issue_id}/events/latest/
```

### Get Specific Event
```
GET https://sentry.io/api/0/projects/{org_slug}/{project_slug}/events/{event_id}/
```

## Query Parameters

### Search Query Syntax

| Query | Description |
|-------|-------------|
| `is:unresolved` | Unresolved issues |
| `is:resolved` | Resolved issues |
| `is:ignored` | Ignored issues |
| `is:assigned` | Assigned to someone |
| `is:unassigned` | Not assigned |
| `user.email:x@y.com` | Errors from specific user |
| `user.id:123` | Errors from user ID |
| `release:1.0.0` | Specific release |
| `environment:production` | Specific environment |
| `error.type:TypeError` | Specific error type |
| `http.status_code:500` | HTTP status code |
| `transaction:/api/users` | Specific transaction/route |
| `level:error` | Error level (fatal, error, warning, info) |
| `firstSeen:-24h` | First seen in last 24h |
| `lastSeen:-1h` | Last seen in last hour |

Combine with AND: `is:unresolved environment:production`

### Stats Period
- `1h` - Last hour
- `24h` - Last 24 hours
- `7d` - Last 7 days
- `14d` - Last 14 days
- `30d` - Last 30 days
- `90d` - Last 90 days

### Sort Options
- `date` - Most recent
- `new` - Newest issues first
- `freq` - Most frequent
- `priority` - By issue priority

## Response Structures

### Issue Object
```json
{
  "id": "12345",
  "shortId": "PROJECT-ABC",
  "title": "TypeError: Cannot read property 'x' of undefined",
  "culprit": "app/components/Widget.tsx in render",
  "permalink": "https://sentry.io/...",
  "level": "error",
  "status": "unresolved",
  "count": "142",
  "userCount": 45,
  "firstSeen": "2024-01-15T10:30:00Z",
  "lastSeen": "2024-01-15T14:22:00Z",
  "metadata": {
    "type": "TypeError",
    "value": "Cannot read property 'x' of undefined"
  }
}
```

### Event Object
```json
{
  "eventID": "abc123",
  "dateCreated": "2024-01-15T14:22:00Z",
  "message": "TypeError: Cannot read property 'x' of undefined",
  "user": {
    "id": "user123",
    "email": "user@example.com",
    "username": "johndoe"
  },
  "tags": [
    {"key": "browser", "value": "Chrome 120"},
    {"key": "environment", "value": "production"}
  ],
  "contexts": {
    "browser": {"name": "Chrome", "version": "120"},
    "os": {"name": "macOS", "version": "14.0"},
    "device": {"family": "Desktop"}
  },
  "entries": [
    {
      "type": "exception",
      "data": {
        "values": [{
          "type": "TypeError",
          "value": "Cannot read property 'x' of undefined",
          "stacktrace": {
            "frames": [
              {
                "filename": "app/components/Widget.tsx",
                "function": "render",
                "lineno": 42,
                "colno": 15,
                "context_line": "const value = data.nested.x;"
              }
            ]
          }
        }]
      }
    },
    {
      "type": "breadcrumbs",
      "data": {
        "values": [
          {
            "timestamp": "2024-01-15T14:21:55Z",
            "category": "navigation",
            "message": "Navigated to /dashboard"
          },
          {
            "timestamp": "2024-01-15T14:21:58Z",
            "category": "xhr",
            "message": "GET /api/data",
            "data": {"status_code": 200}
          }
        ]
      }
    },
    {
      "type": "request",
      "data": {
        "url": "https://app.example.com/dashboard",
        "method": "GET",
        "headers": {"User-Agent": "..."}
      }
    }
  ]
}
```

### Stack Frame Object
```json
{
  "filename": "app/components/Widget.tsx",
  "absPath": "/home/app/src/components/Widget.tsx",
  "function": "render",
  "module": "app.components.Widget",
  "lineno": 42,
  "colno": 15,
  "context_line": "const value = data.nested.x;",
  "pre_context": ["const data = props.data;", "if (data) {"],
  "post_context": ["return value;", "}"],
  "inApp": true
}
```

## Rate Limits

- Default: 40 requests per second
- Responses include `X-Sentry-Rate-Limit-*` headers
- Use pagination cursors for large result sets
