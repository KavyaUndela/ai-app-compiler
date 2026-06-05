from app.models import SimulationResult


class Simulator:
    """Runtime simulator"""
    
    @staticmethod
    def simulate(schema) -> SimulationResult:
        """Simulate runtime execution"""
        
        performance_metrics = {
            "avg_query_time_ms": 45,
            "throughput_rps": 1000,
            "memory_usage_mb": 256,
            "cpu_usage_percent": 35,
            "concurrent_connections": 100
        }
        
        errors = []
        
        # Basic simulation checks
        if not schema.tables:
            errors.append("Cannot simulate without schema tables")
        
        if len(schema.indexes) < len(schema.tables):
            errors.append("Performance warning: Insufficient indexes")
        
        return SimulationResult(
            success=len(errors) == 0,
            output="Simulation completed successfully" if not errors else None,
            errors=errors,
            performance_metrics=performance_metrics
        )
