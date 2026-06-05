from fastapi import APIRouter

router = APIRouter(prefix="/api/metrics", tags=["metrics"])


@router.get("/dashboard")
async def get_dashboard():
    """Get metrics dashboard"""
    
    return {
        "compilation_stats": {
            "total_compilations": 42,
            "successful": 38,
            "failed": 2,
            "pending": 2,
            "success_rate": 95.2
        },
        "average_metrics": {
            "compilation_time_ms": 1245,
            "schema_complexity_score": 0.78,
            "validation_score": 0.92
        },
        "recent_compilations": [
            {
                "id": "comp-1",
                "title": "E-commerce Platform",
                "status": "completed",
                "duration_ms": 1250
            },
            {
                "id": "comp-2",
                "title": "Blog System",
                "status": "completed",
                "duration_ms": 890
            }
        ]
    }


@router.get("/performance")
async def get_performance():
    """Get performance metrics"""
    
    return {
        "api_metrics": {
            "avg_response_time_ms": 145,
            "p95_response_time_ms": 320,
            "p99_response_time_ms": 650,
            "requests_per_second": 42
        },
        "database_metrics": {
            "avg_query_time_ms": 25,
            "total_queries": 15420,
            "slow_queries": 8
        }
    }


@router.get("/health")
async def health_check():
    """Health check endpoint"""
    
    return {
        "status": "healthy",
        "version": "1.0.0",
        "timestamp": str(__import__('datetime').datetime.utcnow())
    }
