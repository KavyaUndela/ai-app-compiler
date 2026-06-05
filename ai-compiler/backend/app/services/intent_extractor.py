import uuid
from app.models import IntentExtraction, RequirementInput


class IntentExtractor:
    """Extract intent from requirements"""
    
    @staticmethod
    def extract(requirement: RequirementInput) -> IntentExtraction:
        """Extract intent from requirement"""
        
        # Simple intent extraction logic
        main_intent = requirement.title.lower()
        
        # Sub-intents from features
        sub_intents = requirement.features[:3] if requirement.features else []
        
        # Extract entities
        entities = {
            "features": requirement.features,
            "constraints": requirement.constraints or "None",
            "tech_stack": requirement.tech_preferences or {}
        }
        
        # Determine priority
        if requirement.constraints and any(x in requirement.constraints.lower() for x in ["urgent", "critical", "asap"]):
            priority = "high"
        elif len(requirement.features) >= 5:
            priority = "high"
        elif len(requirement.features) >= 2:
            priority = "medium"
        else:
            priority = "low"
        
        return IntentExtraction(
            main_intent=main_intent,
            sub_intents=sub_intents,
            entities=entities,
            priority=priority
        )
