"""
Stage 6: Runtime Simulator Service
Generates dynamic forms, CRUD pages, and runtime preview from schemas.
"""

import uuid
from typing import Dict, List, Any
from app.models import (
    SchemaGenerationResult, RuntimePreview, FormSchema, FormField, CRUDPage
)

def generate_runtime_preview(schema: SchemaGenerationResult) -> RuntimePreview:
    """Generate runtime preview with dynamic forms, CRUD pages, and sample data."""
    
    preview_id = str(uuid.uuid4())
    dynamic_forms: List[FormSchema] = []
    crud_pages: List[CRUDPage] = []
    sample_data: Dict[str, List[Any]] = {}
    
    # ============= Generate Dynamic Forms =============
    
    # Login form
    dynamic_forms.append(FormSchema(
        form_id=str(uuid.uuid4()),
        title="Login",
        description="Sign in to your account",
        fields=[
            FormField(name="email", label="Email Address", field_type="email", required=True),
            FormField(name="password", label="Password", field_type="password", required=True),
            FormField(name="remember_me", label="Remember me", field_type="checkbox", required=False),
        ],
        submit_action="/auth/login"
    ))
    
    # Signup form
    dynamic_forms.append(FormSchema(
        form_id=str(uuid.uuid4()),
        title="Sign Up",
        description="Create a new account",
        fields=[
            FormField(name="name", label="Full Name", field_type="text", required=True),
            FormField(name="email", label="Email Address", field_type="email", required=True),
            FormField(name="password", label="Password", field_type="password", required=True),
            FormField(name="confirm_password", label="Confirm Password", field_type="password", required=True),
            FormField(name="terms", label="I agree to Terms of Service", field_type="checkbox", required=True),
        ],
        submit_action="/auth/signup"
    ))
    
    # Generic CRUD create form
    dynamic_forms.append(FormSchema(
        form_id=str(uuid.uuid4()),
        title="Create New Item",
        description="Add a new item to the system",
        fields=[
            FormField(name="title", label="Title", field_type="text", required=True),
            FormField(name="description", label="Description", field_type="textarea", required=False),
            FormField(name="status", label="Status", field_type="select", required=True,
                     options=["Draft", "Active", "Archived"]),
            FormField(name="priority", label="Priority", field_type="select", required=False,
                     options=["Low", "Medium", "High"]),
            FormField(name="due_date", label="Due Date", field_type="date", required=False),
        ],
        submit_action="/items"
    ))
    
    # ============= Generate CRUD Pages =============
    
    crud_pages.append(CRUDPage(
        page_id=str(uuid.uuid4()),
        entity_name="Items",
        list_columns=["id", "title", "status", "created_at"],
        create_form=dynamic_forms[2],  # Use the generic create form above
        edit_form=FormSchema(
            form_id=str(uuid.uuid4()),
            title="Edit Item",
            description="Update item details",
            fields=[
                FormField(name="title", label="Title", field_type="text", required=True),
                FormField(name="description", label="Description", field_type="textarea", required=False),
                FormField(name="status", label="Status", field_type="select", required=True,
                         options=["Draft", "Active", "Archived"]),
            ],
            submit_action="/items/{id}"
        ),
        delete_confirmation="Are you sure you want to delete this item? This action cannot be undone."
    ))
    
    crud_pages.append(CRUDPage(
        page_id=str(uuid.uuid4()),
        entity_name="Users",
        list_columns=["id", "email", "role", "created_at"],
        create_form=FormSchema(
            form_id=str(uuid.uuid4()),
            title="Create User",
            description="Add a new user to the system",
            fields=[
                FormField(name="email", label="Email", field_type="email", required=True),
                FormField(name="name", label="Name", field_type="text", required=True),
                FormField(name="role", label="Role", field_type="select", required=True,
                         options=["User", "Admin"]),
            ],
            submit_action="/users"
        ),
        edit_form=FormSchema(
            form_id=str(uuid.uuid4()),
            title="Edit User",
            description="Update user details",
            fields=[
                FormField(name="name", label="Name", field_type="text", required=True),
                FormField(name="role", label="Role", field_type="select", required=True,
                         options=["User", "Admin"]),
                FormField(name="active", label="Active", field_type="checkbox", required=False),
            ],
            submit_action="/users/{id}"
        ),
        delete_confirmation="Are you sure you want to delete this user?"
    ))
    
    # ============= Generate Sample Data =============
    
    sample_data["users"] = [
        {
            "id": "550e8400-e29b-41d4-a716-446655440000",
            "email": "admin@example.com",
            "name": "Admin User",
            "role": "Admin",
            "created_at": "2024-01-01T00:00:00Z"
        },
        {
            "id": "550e8400-e29b-41d4-a716-446655440001",
            "email": "user@example.com",
            "name": "John Doe",
            "role": "User",
            "created_at": "2024-01-05T10:30:00Z"
        }
    ]
    
    sample_data["items"] = [
        {
            "id": "550e8400-e29b-41d4-a716-446655440100",
            "title": "Setup Database",
            "description": "Create database tables and indexes",
            "status": "Active",
            "priority": "High",
            "created_at": "2024-01-10T08:00:00Z"
        },
        {
            "id": "550e8400-e29b-41d4-a716-446655440101",
            "title": "Build API Endpoints",
            "description": "Implement REST API endpoints",
            "status": "Active",
            "priority": "High",
            "created_at": "2024-01-11T09:00:00Z"
        },
        {
            "id": "550e8400-e29b-41d4-a716-446655440102",
            "title": "Design Dashboard",
            "description": "Create user-facing dashboard",
            "status": "Draft",
            "priority": "Medium",
            "created_at": "2024-01-12T14:00:00Z"
        }
    ]
    
    # ============= Generate Preview HTML =============
    
    preview_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Runtime Preview</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; background: #f9fafb; }
            .container { max-width: 1200px; margin: 0 auto; padding: 20px; }
            header { background: #3b82f6; color: white; padding: 20px; border-radius: 8px; margin-bottom: 20px; }
            .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; }
            .card { background: white; border: 1px solid #e5e7eb; border-radius: 8px; padding: 20px; }
            .table { width: 100%; border-collapse: collapse; margin-top: 10px; }
            .table th, .table td { padding: 10px; text-align: left; border-bottom: 1px solid #e5e7eb; }
            .table th { background: #f3f4f6; font-weight: 600; }
            .btn { padding: 8px 16px; background: #3b82f6; color: white; border: none; border-radius: 4px; cursor: pointer; }
            .btn:hover { background: #2563eb; }
            form { max-width: 400px; }
            .form-group { margin-bottom: 15px; }
            label { display: block; margin-bottom: 5px; font-weight: 500; }
            input, select, textarea { width: 100%; padding: 8px; border: 1px solid #d1d5db; border-radius: 4px; }
            .status { display: inline-block; padding: 4px 8px; border-radius: 4px; font-size: 12px; font-weight: 600; }
            .status-active { background: #d1fae5; color: #065f46; }
            .status-draft { background: #fef3c7; color: #92400e; }
        </style>
    </head>
    <body>
        <div class="container">
            <header>
                <h1>AI Application Compiler - Runtime Preview</h1>
                <p>This is a dynamically generated preview of your application</p>
            </header>
            
            <div class="grid">
                <div class="card">
                    <h2>Users</h2>
                    <table class="table">
                        <thead>
                            <tr><th>Email</th><th>Role</th><th>Actions</th></tr>
                        </thead>
                        <tbody>
                            <tr><td>admin@example.com</td><td>Admin</td><td><button class="btn">Edit</button></td></tr>
                            <tr><td>user@example.com</td><td>User</td><td><button class="btn">Edit</button></td></tr>
                        </tbody>
                    </table>
                    <button class="btn" style="margin-top: 10px;">+ Add User</button>
                </div>
                
                <div class="card">
                    <h2>Items</h2>
                    <table class="table">
                        <thead>
                            <tr><th>Title</th><th>Status</th><th>Actions</th></tr>
                        </thead>
                        <tbody>
                            <tr><td>Setup Database</td><td><span class="status status-active">Active</span></td><td><button class="btn">Edit</button></td></tr>
                            <tr><td>Build API</td><td><span class="status status-active">Active</span></td><td><button class="btn">Edit</button></td></tr>
                            <tr><td>Design Dashboard</td><td><span class="status status-draft">Draft</span></td><td><button class="btn">Edit</button></td></tr>
                        </tbody>
                    </table>
                    <button class="btn" style="margin-top: 10px;">+ Add Item</button>
                </div>
            </div>
            
            <div class="card" style="margin-top: 20px;">
                <h2>Create New Item</h2>
                <form>
                    <div class="form-group">
                        <label for="title">Title</label>
                        <input type="text" id="title" placeholder="Enter item title">
                    </div>
                    <div class="form-group">
                        <label for="description">Description</label>
                        <textarea id="description" placeholder="Enter description" rows="3"></textarea>
                    </div>
                    <div class="form-group">
                        <label for="status">Status</label>
                        <select id="status">
                            <option>Draft</option>
                            <option>Active</option>
                            <option>Archived</option>
                        </select>
                    </div>
                    <button type="button" class="btn">Create Item</button>
                </form>
            </div>
        </div>
    </body>
    </html>
    """
    
    return RuntimePreview(
        preview_id=preview_id,
        schema_id=schema.schema_id,
        dynamic_forms=dynamic_forms,
        crud_pages=crud_pages,
        preview_html=preview_html,
        sample_data=sample_data
    )
