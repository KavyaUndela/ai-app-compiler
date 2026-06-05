"""Canonical schema models for the AI Application Compiler."""

from .api import APISchema, EndpointSchema
from .architecture import (
    ArchitectureLayerSchema,
    ArchitectureSchema,
    ModuleSchema,
    NavigationSchema,
    PageSchema,
    RoleHierarchySchema,
    WorkflowSchema,
)
from .auth import AuthProviderSchema, AuthSchema, AuthSessionSchema
from .database import ColumnSchema, DatabaseSchema, ForeignKeySchema, IndexSchema, TableSchema
from .intent import IntentSchema
from .repair import RepairActionSchema, RepairReport
from .reports import ValidationIssueSchema, ValidationReport
from .simulation import (
    RuntimeCrudPageSchema,
    RuntimeFieldSchema,
    RuntimeFormSchema,
    RuntimeNavigationSchema,
    RuntimePreviewSchema,
    RuntimeSimulationReport,
)
from .types import AuthMode, DatabaseEngine, HttpMethod, IssueSeverity, UIFramework
from .ui import UIComponentSchema, UIPageSchema, UISchema

__all__ = [
    "APISchema",
    "ArchitectureLayerSchema",
    "ArchitectureSchema",
    "AuthMode",
    "AuthProviderSchema",
    "AuthSchema",
    "AuthSessionSchema",
    "ColumnSchema",
    "DatabaseEngine",
    "DatabaseSchema",
    "EndpointSchema",
    "ForeignKeySchema",
    "HttpMethod",
    "IndexSchema",
    "IntentSchema",
    "IssueSeverity",
    "ModuleSchema",
    "NavigationSchema",
    "PageSchema",
    "RepairActionSchema",
    "RepairReport",
    "RoleHierarchySchema",
    "RuntimeCrudPageSchema",
    "RuntimeFieldSchema",
    "RuntimeFormSchema",
    "RuntimeNavigationSchema",
    "RuntimePreviewSchema",
    "RuntimeSimulationReport",
    "TableSchema",
    "UIComponentSchema",
    "UIFramework",
    "UIPageSchema",
    "UISchema",
    "WorkflowSchema",
    "ValidationIssueSchema",
    "ValidationReport",
]