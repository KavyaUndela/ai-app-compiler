"""
Stage 1: Intent Extraction Service
Converts natural language requirements into structured intent objects.
"""

import uuid
import re
from typing import List
from app.models import IntentSchema, Entity, Feature, Role

def extract_intent(prompt: str) -> IntentSchema:
    """Extract structured intent from natural language prompt."""
    
    intent_id = str(uuid.uuid4())
    
    # Simple NLP-like extraction (mock LLM behavior)
    prompt_lower = prompt.lower()
    
    # Extract entities (look for common patterns)
    entities = []
    entity_keywords = {
        "user": ["user", "admin", "customer", "profile"],
        "data": ["contact", "form", "data", "record", "item", "product", "order"],
        "system": ["dashboard", "system", "app", "platform"]
    }
    
    for entity_type, keywords in entity_keywords.items():
        for kw in keywords:
            if kw in prompt_lower:
                # Extract entity name (heuristic)
                for word in prompt.split():
                    if kw in word.lower():
                        entities.append(Entity(
                            name=word.strip(".,"),
                            entity_type=entity_type,
                            description=f"Extracted from prompt: {kw}"
                        ))
                        break
    
    # If no entities found, create default ones
    if not entities:
        entities = [
            Entity(name="User", entity_type="user", description="Application user"),
            Entity(name="Data", entity_type="data", description="Data objects")
        ]
    
    # Extract features (look for action words)
    features = []
    action_patterns = {
        "Authentication": ["login", "auth", "authentication", "signin", "signup"],
        "CRUD": ["create", "read", "edit", "delete", "manage", "list", "view"],
        "Dashboard": ["dashboard", "analytics", "overview", "report"],
        "Payment": ["payment", "plan", "premium", "billing", "checkout"],
        "Notifications": ["notification", "alert", "email", "message"],
        "Search": ["search", "filter", "query", "find"],
    }
    
    for feature_name, keywords in action_patterns.items():
        for kw in keywords:
            if kw in prompt_lower:
                features.append(Feature(
                    name=feature_name,
                    description=f"Feature: {feature_name}",
                    related_entities=[e.name for e in entities[:2]]
                ))
                break
    
    # Extract roles/permissions
    roles = []
    role_keywords = {
        "Admin": ["admin", "administrator", "manager"],
        "User": ["user", "customer", "member"],
        "Guest": ["guest", "public", "anonymous"],
        "Premium": ["premium", "paid", "subscriber"]
    }
    
    for role_name, keywords in role_keywords.items():
        for kw in keywords:
            if kw in prompt_lower:
                roles.append(Role(
                    name=role_name,
                    permissions=["read", "write"] if role_name == "Admin" else ["read"],
                    description=f"Role: {role_name}"
                ))
                break
    
    # If no roles, add default
    if not roles:
        roles = [
            Role(name="User", permissions=["read", "write"], description="Standard user"),
            Role(name="Admin", permissions=["read", "write", "delete", "manage"], description="Administrator")
        ]
    
    # Extract workflows
    workflows = []
    workflow_patterns = {
        "User Registration": ["signup", "register", "onboarding"],
        "User Login": ["login", "signin", "authentication"],
        "CRUD Operations": ["create", "read", "update", "delete", "manage"],
        "Payment Flow": ["payment", "checkout", "billing"],
        "Data Management": ["import", "export", "backup", "sync"],
    }
    
    for workflow_name, keywords in workflow_patterns.items():
        for kw in keywords:
            if kw in prompt_lower:
                workflows.append(workflow_name)
                break
    
    summary = f"Extracted intent: {len(entities)} entities, {len(features)} features, {len(roles)} roles, {len(workflows)} workflows"
    
    return IntentSchema(
        intent_id=intent_id,
        entities=entities,
        features=features,
        roles=roles,
        workflows=workflows if workflows else ["User Login", "CRUD Operations"],
        summary=summary
    )
