from app.models import ValidationResult, SchemaDefinition


class Validator:
    """Validate compilation output"""
    
    @staticmethod
    def validate(schema: SchemaDefinition) -> ValidationResult:
        """Validate schema"""
        
        errors = []
        warnings = []
        score = 100.0
        
        # Validate tables
        if not schema.tables or len(schema.tables) == 0:
            errors.append("No tables defined in schema")
            score -= 30
        
        # Validate relationships
        table_names = {t.get("name") for t in schema.tables}
        for rel in schema.relationships:
            if rel.get("from") not in table_names:
                warnings.append(f"Relationship source '{rel.get('from')}' not found in tables")
                score -= 5
            if rel.get("to") not in table_names:
                warnings.append(f"Relationship target '{rel.get('to')}' not found in tables")
                score -= 5
        
        # Validate indexes
        if not schema.indexes:
            warnings.append("No indexes defined - may impact query performance")
            score -= 10
        
        # Validate constraints
        if not schema.constraints:
            warnings.append("No constraints defined - data integrity may be at risk")
            score -= 10
        
        # Check primary keys
        has_primary_keys = False
        for table in schema.tables:
            columns = table.get("columns", [])
            if any(c.get("primary_key") for c in columns):
                has_primary_keys = True
                break
        
        if not has_primary_keys:
            errors.append("No primary keys defined in tables")
            score -= 20
        
        score = max(0, min(100, score))
        
        return ValidationResult(
            is_valid=len(errors) == 0,
            errors=errors,
            warnings=warnings,
            score=score / 100.0
        )
