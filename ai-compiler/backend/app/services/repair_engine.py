from app.models import RepairAction, ValidationResult


class RepairEngine:
    """Repair validation issues"""
    
    @staticmethod
    def repair(validation: ValidationResult) -> list:
        """Generate repair actions for validation errors"""
        
        repairs = []
        
        for error in validation.errors:
            if "No tables defined" in error:
                repairs.append(RepairAction(
                    action_type="add_tables",
                    target="schema",
                    description="Add default tables (users, sessions, compilations)",
                    automatic=True
                ))
            elif "No primary keys" in error:
                repairs.append(RepairAction(
                    action_type="add_primary_keys",
                    target="schema.tables",
                    description="Add UUID primary keys to all tables",
                    automatic=True
                ))
        
        for warning in validation.warnings:
            if "No indexes" in warning:
                repairs.append(RepairAction(
                    action_type="add_indexes",
                    target="schema",
                    description="Add indexes on frequently queried columns",
                    automatic=False
                ))
            elif "No constraints" in warning:
                repairs.append(RepairAction(
                    action_type="add_constraints",
                    target="schema",
                    description="Add foreign key and unique constraints",
                    automatic=False
                ))
        
        return repairs
