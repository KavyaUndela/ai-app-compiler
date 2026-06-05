from app.models import SystemDesign, IntentExtraction


class Designer:
    """Design system architecture"""
    
    @staticmethod
    def design(intent: IntentExtraction) -> SystemDesign:
        """Design system based on intent"""
        
        # Basic architecture design
        architecture = "Microservices"
        if intent.priority == "low":
            architecture = "Monolithic"
        elif len(intent.sub_intents) > 3:
            architecture = "Event-Driven"
        
        # Components based on intent
        components = [
            "API Gateway",
            "Authentication Service",
            "Data Service",
            "Business Logic Service"
        ]
        
        # Add more components based on features
        if any("search" in str(x).lower() for x in intent.sub_intents):
            components.append("Search Service")
        if any("payment" in str(x).lower() for x in intent.sub_intents):
            components.append("Payment Service")
        if any("notification" in str(x).lower() for x in intent.sub_intents):
            components.append("Notification Service")
        
        # Data flow
        data_flow = "Request → API Gateway → Service Router → Business Logic → Database → Response"
        
        # Tech stack from preferences or defaults
        tech_stack = intent.entities.get("tech_stack", {})
        if not tech_stack:
            tech_stack = {
                "frontend": "Next.js",
                "backend": "FastAPI",
                "database": "PostgreSQL",
                "cache": "Redis",
                "queue": "RabbitMQ"
            }
        
        return SystemDesign(
            architecture=architecture,
            components=components,
            data_flow=data_flow,
            tech_stack=tech_stack,
            scalability_notes="Design supports horizontal scaling with load balancing"
        )
