"""
Stage 2: System Design Service
Converts intent into high-level system architecture and design.
"""

import uuid
from typing import List, Dict
from app.models import IntentSchema, SystemDesignSchema, Module, PageSchema

def generate_design(intent: IntentSchema) -> SystemDesignSchema:
    """Generate system design from extracted intent."""
    
    design_id = str(uuid.uuid4())
    
    # Create modules based on features and workflows
    modules = []
    
    # Authentication module
    modules.append(Module(
        name="Authentication",
        pages=[
            PageSchema(
                name="Login",
                component_type="form",
                fields=["email", "password"],
                required_roles=[]
            ),
            PageSchema(
                name="Signup",
                component_type="form",
                fields=["email", "password", "name"],
                required_roles=[]
            ),
            PageSchema(
                name="Profile",
                component_type="detail",
                fields=["email", "name", "avatar", "preferences"],
                required_roles=["User", "Admin"]
            )
        ],
        functions=["login()", "signup()", "logout()", "updateProfile()"]
    ))
    
    # Data Management module
    data_module_pages = [
        PageSchema(
            name="List",
            component_type="list",
            fields=[e.name for e in intent.entities if e.entity_type == "data"],
            required_roles=["User", "Admin"]
        ),
        PageSchema(
            name="Create",
            component_type="form",
            fields=[e.name for e in intent.entities if e.entity_type == "data"],
            required_roles=["User", "Admin"]
        ),
        PageSchema(
            name="Detail",
            component_type="detail",
            fields=[e.name for e in intent.entities if e.entity_type == "data"],
            required_roles=["User", "Admin"]
        ),
        PageSchema(
            name="Edit",
            component_type="form",
            fields=[e.name for e in intent.entities if e.entity_type == "data"],
            required_roles=["User", "Admin"]
        ),
    ]
    
    modules.append(Module(
        name="DataManagement",
        pages=data_module_pages,
        functions=["create()", "read()", "update()", "delete()", "list()"]
    ))
    
    # Dashboard module
    modules.append(Module(
        name="Dashboard",
        pages=[
            PageSchema(
                name="Overview",
                component_type="dashboard",
                fields=["summary", "stats", "charts"],
                required_roles=["User", "Admin"]
            )
        ],
        functions=["getStats()", "getCharts()"]
    ))
    
    # Admin module
    if any(r.name == "Admin" for r in intent.roles):
        modules.append(Module(
            name="AdminPanel",
            pages=[
                PageSchema(
                    name="Users",
                    component_type="list",
                    fields=["id", "email", "role", "status"],
                    required_roles=["Admin"]
                ),
                PageSchema(
                    name="Settings",
                    component_type="form",
                    fields=["app_name", "logo", "theme", "features"],
                    required_roles=["Admin"]
                )
            ],
            functions=["manageUsers()", "updateSettings()"]
        ))
    
    # Build navigation structure
    navigation = {
        "main": ["Dashboard", "DataManagement"],
        "authenticated": ["Profile", "Logout"],
        "admin": ["AdminPanel", "Settings"] if any(r.name == "Admin" for r in intent.roles) else []
    }
    
    # Auth flow description
    auth_flow = "OAuth2 with JWT tokens" if "Premium" in [r.name for r in intent.roles] else "Basic JWT authentication"
    
    # User workflows
    user_workflows = intent.workflows if intent.workflows else ["User Login", "CRUD Operations"]
    
    summary = f"Designed system with {len(modules)} modules, {sum(len(m.pages) for m in modules)} pages, supporting {len(intent.roles)} roles"
    
    return SystemDesignSchema(
        design_id=design_id,
        modules=modules,
        navigation=navigation,
        auth_flow=auth_flow,
        user_workflows=user_workflows,
        summary=summary
    )
