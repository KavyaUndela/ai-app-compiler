from app.models import SchemaDefinition, SystemDesign


class SchemaGenerator:
    """Generate database schema"""
    
    @staticmethod
    def generate(design: SystemDesign) -> SchemaDefinition:
        """Generate schema from design"""
        
        tables = [
            {
                "name": "users",
                "columns": [
                    {"name": "id", "type": "UUID", "primary_key": True},
                    {"name": "username", "type": "VARCHAR(255)", "unique": True},
                    {"name": "email", "type": "VARCHAR(255)", "unique": True},
                    {"name": "password_hash", "type": "VARCHAR(255)"},
                    {"name": "created_at", "type": "TIMESTAMP"}
                ]
            },
            {
                "name": "sessions",
                "columns": [
                    {"name": "id", "type": "UUID", "primary_key": True},
                    {"name": "user_id", "type": "UUID", "foreign_key": "users.id"},
                    {"name": "token", "type": "TEXT"},
                    {"name": "expires_at", "type": "TIMESTAMP"}
                ]
            },
            {
                "name": "compilations",
                "columns": [
                    {"name": "id", "type": "UUID", "primary_key": True},
                    {"name": "user_id", "type": "UUID", "foreign_key": "users.id"},
                    {"name": "title", "type": "VARCHAR(255)"},
                    {"name": "status", "type": "VARCHAR(50)"},
                    {"name": "created_at", "type": "TIMESTAMP"}
                ]
            }
        ]
        
        relationships = [
            {"from": "sessions", "to": "users", "type": "many_to_one"},
            {"from": "compilations", "to": "users", "type": "many_to_one"}
        ]
        
        indexes = [
            "users(username)",
            "users(email)",
            "sessions(user_id)",
            "compilations(user_id)",
            "compilations(created_at)"
        ]
        
        constraints = [
            "UNIQUE(users.username)",
            "UNIQUE(users.email)",
            "FOREIGN KEY(sessions.user_id) REFERENCES users(id)",
            "FOREIGN KEY(compilations.user_id) REFERENCES users(id)"
        ]
        
        return SchemaDefinition(
            tables=tables,
            relationships=relationships,
            indexes=indexes,
            constraints=constraints
        )
