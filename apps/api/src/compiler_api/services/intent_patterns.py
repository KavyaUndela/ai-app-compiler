"""Deterministic text heuristics for intent extraction."""

from __future__ import annotations

from collections.abc import Iterable
import re

ROLE_TERMS = (
    "admin",
    "administrator",
    "analyst",
    "approver",
    "auditor",
    "author",
    "client",
    "customer",
    "developer",
    "editor",
    "employee",
    "end user",
    "manager",
    "member",
    "operator",
    "owner",
    "reader",
    "reviewer",
    "staff",
    "supervisor",
    "support agent",
    "tenant",
    "user",
)

ENTITY_TERMS = (
    "account",
    "api",
    "application",
    "approval",
    "audit log",
    "dashboard",
    "document",
    "entity",
    "invoice",
    "message",
    "notification",
    "order",
    "payment",
    "permission",
    "product",
    "project",
    "record",
    "report",
    "resource",
    "role",
    "session",
    "task",
    "ticket",
    "user",
    "workflow",
)

PERMISSION_TERMS = (
    "approve",
    "archive",
    "assign",
    "create",
    "delete",
    "edit",
    "export",
    "import",
    "manage",
    "publish",
    "read",
    "reject",
    "review",
    "share",
    "submit",
    "update",
    "view",
)

INTEGRATION_TERMS = (
    "active directory",
    "api",
    "aws",
    "azure",
    "datadog",
    "email",
    "github",
    "gitlab",
    "google sheets",
    "ldap",
    "postgresql",
    "redis",
    "s3",
    "salesforce",
    "sendgrid",
    "slack",
    "sso",
    "stripe",
    "saml",
    "twilio",
    "webhook",
)

WORKFLOW_TRIGGERS = (
    "after",
    "before",
    "during",
    "following",
    "on",
    "once",
    "then",
    "when",
)

RULE_TRIGGERS = (
    "at least",
    "cannot",
    "must",
    "never",
    "only",
    "required",
    "should",
    "unless",
    "until",
)

SENTENCE_SPLIT_RE = re.compile(r"(?<=[.!?])\s+|\n+")
WORD_SPLIT_RE = re.compile(r"[^a-z0-9]+")
MULTI_SPACE_RE = re.compile(r"\s+")


def normalize_text(text: str) -> str:
    return MULTI_SPACE_RE.sub(" ", text.strip())


def split_sentences(text: str) -> list[str]:
    sentences = [normalize_text(sentence) for sentence in SENTENCE_SPLIT_RE.split(text) if normalize_text(sentence)]
    return sentences or [normalize_text(text)]


def dedupe_preserve_order(values: Iterable[str]) -> list[str]:
    seen: set[str] = set()
    ordered: list[str] = []
    for value in values:
        normalized = normalize_text(value)
        key = normalized.casefold()
        if normalized and key not in seen:
            seen.add(key)
            ordered.append(normalized)
    return ordered


def title_case_phrase(phrase: str) -> str:
    words = [word for word in WORD_SPLIT_RE.split(phrase.lower()) if word]
    return " ".join(word.capitalize() for word in words)


def extract_keyword_hits(text: str, terms: Iterable[str]) -> list[str]:
    lowered = text.casefold()
    hits: list[str] = []
    for term in terms:
        pattern = rf"(?<![a-z0-9]){re.escape(term.casefold())}(?![a-z0-9])"
        if re.search(pattern, lowered):
            hits.append(title_case_phrase(term))
    return dedupe_preserve_order(hits)


def extract_clause_matches(text: str, triggers: Iterable[str], prefix: str) -> list[str]:
    lowered = text.casefold()
    matches: list[str] = []
    for sentence in split_sentences(text):
        sentence_lower = sentence.casefold()
        for trigger in triggers:
            if trigger in sentence_lower:
                clause = sentence_lower.split(trigger, 1)[1].strip(" :,-")
                if clause:
                    matches.append(f"{prefix}: {normalize_text(clause)}")
                    break
    return dedupe_preserve_order(matches)


def extract_role_mentions(text: str) -> list[str]:
    lowered = text.casefold()
    role_phrases: list[str] = []
    for role in ROLE_TERMS:
        pattern = rf"(?<![a-z0-9]){re.escape(role.casefold())}(?:s)?(?![a-z0-9])"
        if re.search(pattern, lowered):
            role_phrases.append(title_case_phrase(role))
    return dedupe_preserve_order(role_phrases)


def extract_entities(text: str) -> list[str]:
    entities = extract_keyword_hits(text, ENTITY_TERMS)
    capitalized_phrases = re.findall(r"\b(?:[A-Z][A-Za-z0-9]+(?:\s+[A-Z][A-Za-z0-9]+)+)\b", text)
    entities.extend(capitalized_phrases)
    return dedupe_preserve_order(entities)


def extract_permissions(text: str, roles: list[str]) -> list[str]:
    sentences = split_sentences(text)
    permissions: list[str] = []
    for sentence in sentences:
        sentence_lower = sentence.casefold()
        if not any(role.casefold() in sentence_lower for role in roles):
            continue
        for term in PERMISSION_TERMS:
            if re.search(rf"\b{re.escape(term)}\b", sentence_lower):
                permissions.append(f"{title_case_phrase(term)}: {normalize_text(sentence)}")
                break
    if not permissions:
        permissions = [title_case_phrase(term) for term in extract_keyword_hits(text, PERMISSION_TERMS)]
    return dedupe_preserve_order(permissions)


def extract_business_rules(text: str) -> list[str]:
    rules = []
    for sentence in split_sentences(text):
        sentence_lower = sentence.casefold()
        if any(trigger in sentence_lower for trigger in RULE_TRIGGERS):
            rules.append(f"Rule: {normalize_text(sentence)}")
    if not rules:
        rules = [f"Rule: {sentence}" for sentence in split_sentences(text) if len(sentence) > 40]
    return dedupe_preserve_order(rules)


def extract_workflows(text: str) -> list[str]:
    workflows: list[str] = []
    for sentence in split_sentences(text):
        sentence_lower = sentence.casefold()
        if any(trigger in sentence_lower for trigger in WORKFLOW_TRIGGERS) and any(
            keyword in sentence_lower for keyword in ("create", "update", "submit", "approve", "notify", "sync", "generate")
        ):
            workflows.append(f"Workflow: {normalize_text(sentence)}")
    if not workflows:
        workflows = [f"Workflow: {sentence}" for sentence in split_sentences(text) if len(sentence) > 60]
    return dedupe_preserve_order(workflows)


def extract_integrations(text: str) -> list[str]:
    integrations = extract_keyword_hits(text, INTEGRATION_TERMS)
    if "api" in text.casefold() and "Api" not in integrations:
        integrations.append("API")
    return dedupe_preserve_order(integrations)
