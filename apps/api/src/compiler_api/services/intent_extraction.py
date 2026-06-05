"""Deterministic intent extraction service."""

from __future__ import annotations

import re

from compiler_contracts import IntentSchema

from .intent_patterns import (
    dedupe_preserve_order,
    extract_business_rules,
    extract_entities,
    extract_integrations,
    extract_permissions,
    extract_role_mentions,
    extract_workflows,
    normalize_text,
    split_sentences,
    title_case_phrase,
)


class IntentExtractionService:
    """Convert natural language requirements into a strict IntentSchema.

    The implementation is deterministic and uses rule-based heuristics so the
    same requirement text always yields the same structured intent.
    """

    def extract(self, requirement_text: str) -> IntentSchema:
        normalized_requirement = normalize_text(requirement_text)
        if len(normalized_requirement) < 20:
            raise ValueError("requirement_text must contain at least 20 characters")

        application_name = self._infer_application_name(normalized_requirement)
        problem_statement = self._build_problem_statement(normalized_requirement)
        roles = extract_role_mentions(normalized_requirement)
        entities = extract_entities(normalized_requirement)
        permissions = extract_permissions(normalized_requirement, roles)
        business_rules = extract_business_rules(normalized_requirement)
        workflows = extract_workflows(normalized_requirement)
        integrations = extract_integrations(normalized_requirement)

        return IntentSchema(
            requirement_text=normalized_requirement,
            application_name=application_name,
            problem_statement=problem_statement,
            entities=entities,
            roles=roles,
            permissions=permissions,
            business_rules=business_rules,
            workflows=workflows,
            integrations=integrations,
            primary_objectives=self._extract_primary_objectives(normalized_requirement),
            constraints=self._extract_constraints(normalized_requirement),
            target_users=roles or ["users"],
            success_criteria=self._extract_success_criteria(normalized_requirement),
            assumptions=self._extract_assumptions(normalized_requirement),
            out_of_scope=self._extract_out_of_scope(normalized_requirement),
            compliance_requirements=self._extract_compliance_requirements(normalized_requirement),
        )

    def _infer_application_name(self, requirement_text: str) -> str:
        patterns = (
            r"(?:build|create|develop|design|implement|ship|deliver)\s+(?:an?\s+|the\s+)?([A-Za-z][A-Za-z0-9 _-]{1,60})",
            r"for\s+an?\s+([A-Za-z][A-Za-z0-9 _-]{1,60})",
            r"requirements\s+for\s+an?\s+([A-Za-z][A-Za-z0-9 _-]{1,60})",
        )
        lowered = requirement_text.casefold()
        for pattern in patterns:
            match = re.search(pattern, lowered)
            if match:
                candidate = title_case_phrase(match.group(1))
                if candidate:
                    return candidate[:100]

        first_sentence = split_sentences(requirement_text)[0]
        words = [word for word in re.findall(r"[A-Za-z][A-Za-z0-9_-]*", first_sentence) if len(word) > 2]
        if words:
            return " ".join(word.capitalize() for word in words[:3])[:100]
        return "Generated Application"

    def _build_problem_statement(self, requirement_text: str) -> str:
        sentences = split_sentences(requirement_text)
        if not sentences:
            return requirement_text[:500]
        statement = sentences[0]
        if len(statement) < 20 and len(sentences) > 1:
            statement = f"{statement} {sentences[1]}"
        return statement[:500]

    def _extract_primary_objectives(self, requirement_text: str) -> list[str]:
        clauses = []
        for sentence in split_sentences(requirement_text):
            sentence_lower = sentence.casefold()
            if any(keyword in sentence_lower for keyword in ("build", "create", "manage", "streamline", "automate", "track", "validate")):
                clauses.append(f"Objective: {sentence}")
        return dedupe_preserve_order(clauses or [f"Objective: {requirement_text[:200]}"])

    def _extract_constraints(self, requirement_text: str) -> list[str]:
        constraints = []
        for sentence in split_sentences(requirement_text):
            sentence_lower = sentence.casefold()
            if any(keyword in sentence_lower for keyword in ("must", "cannot", "can't", "never", "only", "deterministic", "strict", "secure")):
                constraints.append(f"Constraint: {sentence}")
        return dedupe_preserve_order(constraints)

    def _extract_success_criteria(self, requirement_text: str) -> list[str]:
        criteria = []
        for sentence in split_sentences(requirement_text):
            sentence_lower = sentence.casefold()
            if any(keyword in sentence_lower for keyword in ("accurate", "reliable", "fast", "deterministic", "validated", "production-grade")):
                criteria.append(f"Success: {sentence}")
        return dedupe_preserve_order(criteria or ["Success: Outputs are deterministic and valid."])

    def _extract_assumptions(self, requirement_text: str) -> list[str]:
        assumptions = []
        if "production" in requirement_text.casefold():
            assumptions.append("Assumption: Production deployment and operational observability are required.")
        if "api" in requirement_text.casefold():
            assumptions.append("Assumption: The system exposes API-driven compiler services.")
        return dedupe_preserve_order(assumptions or ["Assumption: Requirement text is the source of truth."])

    def _extract_out_of_scope(self, requirement_text: str) -> list[str]:
        out_of_scope = []
        if "demo" not in requirement_text.casefold():
            out_of_scope.append("Out of scope: Ad-hoc, non-deterministic generation paths.")
        return dedupe_preserve_order(out_of_scope)

    def _extract_compliance_requirements(self, requirement_text: str) -> list[str]:
        compliance = []
        if "security" in requirement_text.casefold() or "secure" in requirement_text.casefold():
            compliance.append("Compliance: Security controls must be validated explicitly.")
        if "audit" in requirement_text.casefold():
            compliance.append("Compliance: Auditability must be preserved across compiler stages.")
        return dedupe_preserve_order(compliance)