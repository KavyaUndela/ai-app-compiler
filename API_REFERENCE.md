# API Reference

Complete API documentation for AI Application Compiler.

## Base URL

- **Local:** `http://localhost:8000/api`
- **Production:** `https://api.compiler.example.com`

## Authentication

Currently no authentication. Add JWT tokens in production.

## Response Format

All responses are JSON with consistent structure:

```json
{
  "success": true|false,
  "data": { ... },
  "error": null|"error message",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

---

## Endpoints

### POST /generate

**Description:** Run the complete 6-stage compilation pipeline

**Request:**
```json
{
  "prompt": "Build a CRM with login, contacts, dashboard, and premium plans"
}
```

**Response:** `200 OK`
```json
{
  "compilation_id": "550e8400-e29b-41d4-a716-446655440000",
  "original_prompt": "Build a CRM...",
  "status": "completed",
  "intent": {
    "intent_id": "uuid",
    "entities": ["User", "Contact", "Company"],
    "features": ["Authentication", "CRUD", "Dashboard"],
    "roles": ["Admin", "User"],
    "workflows": ["Create Contact", "View Dashboard"],
    "summary": "..."
  },
  "design": {
    "design_id": "uuid",
    "modules": [
      {
        "name": "Authentication",
        "pages": ["Login", "Signup", "Profile"]
      }
    ],
    "navigation": { "main": [...], "admin": [...] },
    "auth_flow": "OAuth2",
    "workflows": [...],
    "summary": "..."
  },
  "schema": {
    "schema_id": "uuid",
    "database_schema": [
      {
        "table_name": "users",
        "fields": [
          {
            "field_name": "id",
            "field_type": "UUID",
            "is_primary_key": true,
            "is_nullable": false
          }
        ]
      }
    ],
    "api_schema": [
      {
        "path": "/auth/login",
        "method": "POST",
        "description": "User authentication",
        "required_roles": ["Public"]
      }
    ],
    "ui_schema": {
      "theme": "light",
      "colors": { "primary": "#007bff", "secondary": "#6c757d" }
    },
    "auth_schema": {
      "token_type": "JWT",
      "token_expiry": 3600,
      "roles": ["Admin", "User"],
      "permissions": {}
    }
  },
  "validation": {
    "validation_id": "uuid",
    "schema_id": "uuid",
    "issues": [
      {
        "severity": "error",
        "category": "database",
        "message": "Table 'products' missing primary key",
        "suggestion": "Add 'id UUID PRIMARY KEY' field"
      }
    ],
    "is_valid": false,
    "summary": "Found 2 errors, 1 warning"
  },
  "repair": {
    "repair_id": "uuid",
    "validation_id": "uuid",
    "patches": [
      {
        "patch_id": "uuid",
        "affected_component": "products.id",
        "original_value": "missing",
        "fixed_value": "id UUID PRIMARY KEY",
        "explanation": "Added missing primary key",
        "confidence": 0.95
      }
    ],
    "repaired_schema": {...},
    "summary": "Generated 1 patch with avg confidence 0.95"
  },
  "runtime_preview": {
    "preview_id": "uuid",
    "dynamic_forms": [
      {
        "form_id": "login_form",
        "form_name": "Login",
        "fields": [
          {
            "field_name": "email",
            "field_type": "email",
            "required": true,
            "placeholder": "Enter email"
          }
        ]
      }
    ],
    "crud_pages": [
      {
        "page_name": "Products List",
        "entity": "products",
        "operations": ["create", "read", "update", "delete"]
      }
    ],
    "sample_data": {
      "users": [...],
      "products": [...]
    },
    "preview_html": "<html>...</html>"
  },
  "summary": "Compilation successful. Generated 2 modules, 5 tables, 12 endpoints."
}
```

**Error Response:** `400 Bad Request`
```json
{
  "success": false,
  "error": "Prompt cannot be empty"
}
```

---

### GET /compilations

**Description:** List recent compilations

**Query Parameters:**
- `limit` (int, optional): Number of results (default: 10, max: 100)
- `offset` (int, optional): Pagination offset (default: 0)

**Example:**
```
GET /compilations?limit=5&offset=0
```

**Response:** `200 OK`
```json
{
  "compilations": [
    {
      "compilation_id": "uuid",
      "original_prompt": "Build a CRM...",
      "status": "completed",
      "created_at": "2024-01-15T10:30:00Z",
      "summary": {
        "entities": 3,
        "modules": 2,
        "tables": 5,
        "endpoints": 12
      }
    }
  ],
  "total": 42,
  "limit": 5,
  "offset": 0
}
```

---

### GET /compilations/{compilation_id}

**Description:** Retrieve a specific compilation

**Path Parameters:**
- `compilation_id` (string): UUID of the compilation

**Example:**
```
GET /compilations/550e8400-e29b-41d4-a716-446655440000
```

**Response:** `200 OK`
```json
{
  "compilation": {
    "compilation_id": "uuid",
    "original_prompt": "...",
    "status": "completed",
    "intent": {...},
    "design": {...},
    "schema": {...},
    "validation": {...},
    "repair": {...},
    "runtime_preview": {...},
    "summary": "...",
    "created_at": "2024-01-15T10:30:00Z"
  }
}
```

**Error Response:** `404 Not Found`
```json
{
  "success": false,
  "error": "Compilation not found"
}
```

---

### GET /health

**Description:** Health check endpoint

**Response:** `200 OK`
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "compilations_count": 42,
  "uptime": 3600
}
```

---

### POST /validate

**Description:** Standalone validation (without prior compilation)

**Request:**
```json
{
  "database_schema": [...],
  "api_schema": [...],
  "ui_schema": {...},
  "auth_schema": {...}
}
```

**Response:** `200 OK`
```json
{
  "validation_id": "uuid",
  "schema_id": "uuid",
  "issues": [...],
  "is_valid": true|false,
  "summary": "..."
}
```

---

### POST /repair

**Description:** Standalone repair (without prior compilation)

**Request:**
```json
{
  "validation": {
    "validation_id": "uuid",
    "issues": [...]
  },
  "schema": {
    "database_schema": [...],
    "api_schema": [...],
    "ui_schema": {...},
    "auth_schema": {...}
  }
}
```

**Response:** `200 OK`
```json
{
  "repair_id": "uuid",
  "validation_id": "uuid",
  "patches": [...],
  "repaired_schema": {...},
  "summary": "..."
}
```

---

### POST /runtime-preview

**Description:** Standalone runtime preview

**Request:**
```json
{
  "database_schema": [...],
  "api_schema": [...],
  "ui_schema": {...},
  "auth_schema": {...}
}
```

**Response:** `200 OK`
```json
{
  "preview_id": "uuid",
  "dynamic_forms": [...],
  "crud_pages": [...],
  "sample_data": {...},
  "preview_html": "..."
}
```

---

## Data Models

### Intent Schema

```json
{
  "intent_id": "uuid",
  "entities": ["string"],
  "features": ["string"],
  "roles": ["string"],
  "workflows": ["string"],
  "summary": "string"
}
```

### Module Schema

```json
{
  "module_name": "string",
  "description": "string",
  "pages": [
    {
      "page_name": "string",
      "description": "string",
      "components": ["string"]
    }
  ]
}
```

### Database Table

```json
{
  "table_name": "string",
  "description": "string",
  "fields": [
    {
      "field_name": "string",
      "field_type": "UUID|STRING|INTEGER|BOOLEAN|TIMESTAMP",
      "is_primary_key": boolean,
      "is_nullable": boolean,
      "is_unique": boolean,
      "default_value": "string|null"
    }
  ]
}
```

### API Endpoint

```json
{
  "path": "/string",
  "method": "GET|POST|PUT|DELETE|PATCH",
  "description": "string",
  "request_body": {...},
  "response_body": {...},
  "required_roles": ["string"]
}
```

### Validation Issue

```json
{
  "issue_id": "uuid",
  "severity": "error|warning",
  "category": "database|api|auth|ui",
  "message": "string",
  "suggestion": "string",
  "affected_component": "string"
}
```

### Repair Patch

```json
{
  "patch_id": "uuid",
  "affected_component": "string",
  "original_value": "string",
  "fixed_value": "string",
  "explanation": "string",
  "confidence": 0.0..1.0
}
```

---

## Error Codes

| Code | Meaning |
|------|---------|
| 200 | OK - Request succeeded |
| 400 | Bad Request - Invalid input |
| 404 | Not Found - Resource not found |
| 422 | Unprocessable Entity - Validation failed |
| 500 | Internal Server Error - Server error |

---

## Rate Limiting

Not currently implemented. Will add in production.

---

## Pagination

List endpoints support pagination:

```
GET /compilations?limit=10&offset=20
```

- `limit`: Results per page (1-100, default: 10)
- `offset`: Starting position (default: 0)

---

## Versioning

API version in header:
```
X-API-Version: 1.0.0
```

Future versions: `/api/v2/generate`

---

## Examples

### cURL

```bash
# Generate compilation
curl -X POST http://localhost:8000/api/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Build a simple todo app"}'

# List compilations
curl http://localhost:8000/api/compilations?limit=5

# Get specific compilation
curl http://localhost:8000/api/compilations/550e8400-e29b-41d4-a716-446655440000

# Health check
curl http://localhost:8000/api/health
```

### Python (requests)

```python
import requests

api_url = "http://localhost:8000/api"

# Generate
response = requests.post(
    f"{api_url}/generate",
    json={"prompt": "Build a CRM with login and contacts"}
)
result = response.json()
compilation_id = result['compilation_id']

# Retrieve
response = requests.get(f"{api_url}/compilations/{compilation_id}")
compilation = response.json()['compilation']
```

### JavaScript (fetch)

```javascript
const apiUrl = "http://localhost:8000/api";

// Generate
const response = await fetch(`${apiUrl}/generate`, {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    prompt: "Build a CRM with login and contacts"
  })
});
const result = await response.json();
const compilationId = result.compilation_id;

// Retrieve
const response2 = await fetch(
  `${apiUrl}/compilations/${compilationId}`
);
const compilation = await response2.json();
```

---

## Support

For issues or questions:
1. Check logs: `docker compose logs backend`
2. Review backend code in `backend/app/api/routes.py`
3. Check frontend integration in `frontend/src/services/api.ts`
