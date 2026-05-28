"""Intent extraction layer converts free text into structured intent."""

from __future__ import annotations

import re

from app.models.contracts import IntentSpec, StageName, StageOutput, StageStatus
from app.pipeline.intent.domain_templates import DOMAIN_TEMPLATES, KEYWORD_TO_TEMPLATE


class IntentExtractor:
    """Stage 1 deterministic prompt intent parser."""

    FEATURE_KEYWORDS = {
        "auth": ["login", "authentication", "signin", "signup", "rbac", "role"],
        "dashboard": ["dashboard", "overview", "analytics"],
        "contacts": ["crm", "contact", "lead", "customer"],
        "billing": ["payment", "billing", "subscription", "invoice", "stripe", "premium"],
        "orders": ["order", "checkout", "cart"],
        "inventory": ["inventory", "stock", "warehouse"],
        "appointments": ["appointment", "schedule", "booking"],
        "reports": ["report", "insights", "metrics", "analytics"],
        "notifications": ["notification", "email", "sms"],
        "analytics": ["analytics", "kpi", "insights"],
    }

    ROLE_KEYWORDS = {
        "admin": ["admin", "owner", "superuser"],
        "manager": ["manager", "staff lead"],
        "member": ["user", "member", "employee", "student", "patient"],
        "viewer": ["viewer", "read-only", "guest"],
        "seller": ["seller", "merchant"],
        "buyer": ["buyer", "shopper"],
        "doctor": ["doctor", "physician"],
        "nurse": ["nurse"],
        "teacher": ["teacher"],
        "student": ["student"],
    }

    ENTITY_KEYWORDS = {
        "user": ["user", "member", "staff", "employee"],
        "contact": ["contact", "lead", "customer"],
        "payment": ["payment", "invoice", "billing", "subscription"],
        "order": ["order", "checkout", "cart"],
        "product": ["product", "catalog", "inventory", "stock"],
        "appointment": ["appointment", "schedule", "booking"],
        "record": ["record", "case", "profile"],
        "patient": ["patient"],
        "doctor": ["doctor", "physician"],
        "prescription": ["prescription"],
        "student": ["student"],
        "classroom": ["class", "classroom"],
        "attendance": ["attendance"],
        "subscription": ["subscription", "plan"],
        "workspace": ["workspace", "tenant"],
        "listing": ["listing"],
        "warehouse": ["warehouse"],
    }

    INTEGRATION_KEYWORDS = {
        "stripe": ["stripe", "payment gateway"],
        "email": ["email", "smtp"],
        "sms": ["sms", "twilio"],
        "sso": ["oauth", "sso", "google login"],
    }

    DEFAULT_PAGES = ["home", "dashboard", "settings"]

    def run(self, prompt: str) -> StageOutput:
        normalized = self._normalize(prompt)
        template_key = self._detect_template(normalized)
        template = DOMAIN_TEMPLATES.get(template_key)

        app_name = self._derive_app_name(prompt)
        app_type = template["app_type"] if template else "general-business-app"

        features = self._extract_terms(normalized, self.FEATURE_KEYWORDS)
        roles = self._extract_terms(normalized, self.ROLE_KEYWORDS)
        entities = self._extract_terms(normalized, self.ENTITY_KEYWORDS)
        integrations = self._extract_terms(normalized, self.INTEGRATION_KEYWORDS)

        assumptions: list[str] = []
        constraints: list[str] = []

        if template:
            features.extend(template["features"])
            roles.extend(template["roles"])
            entities.extend(template["entities"])
            integrations.extend(template["integrations"])
            assumptions.append(f"Applied deterministic template: {template_key}")

        if "auth" not in features:
            features.append("auth")
            assumptions.append("Authentication added as default secure baseline")
        if not roles:
            roles = ["admin", "member"]
            assumptions.append("Default roles inferred: admin/member")
        if "user" not in entities:
            entities.append("user")
        if "dashboard" not in features:
            features.append("dashboard")

        pages = self._derive_pages(features)
        if template:
            pages.extend(template["pages"])
        ambiguities = self._ambiguity_checks(normalized)
        constraints.extend(ambiguities)

        intent = IntentSpec(
            app_name=app_name,
            app_type=app_type,
            features=sorted(set(features)),
            roles=sorted(set(roles)),
            entities=sorted(set(entities)),
            pages=sorted(set(pages)),
            integrations=sorted(set(integrations)),
            constraints=sorted(set(constraints)),
            assumptions=sorted(set(assumptions)),
        )

        notes = ["Deterministic extraction with domain templates"]
        if ambiguities:
            notes.append("Ambiguities detected and captured in constraints")

        return StageOutput(
            stage=StageName.intent_extraction,
            status=StageStatus.warning if ambiguities else StageStatus.success,
            content=intent.model_dump(),
            notes=notes,
        )

    def _normalize(self, prompt: str) -> str:
        return re.sub(r"\s+", " ", prompt.lower().strip())

    def _detect_template(self, normalized: str) -> str | None:
        for keyword, template in KEYWORD_TO_TEMPLATE.items():
            if keyword in normalized:
                return template
        return None

    def _derive_app_name(self, prompt: str) -> str:
        title_tokens = [token for token in re.findall(r"[a-zA-Z0-9]+", prompt)[:4] if token]
        return "-".join(token.lower() for token in title_tokens) or "generated-app"

    def _extract_terms(self, normalized: str, mapping: dict[str, list[str]]) -> list[str]:
        results: list[str] = []
        for key, keywords in mapping.items():
            if any(keyword in normalized for keyword in keywords):
                results.append(key)
        return sorted(results)

    def _derive_pages(self, features: list[str]) -> list[str]:
        pages = list(self.DEFAULT_PAGES)
        if "contacts" in features:
            pages.extend(["contacts", "contact-detail"])
        if "billing" in features:
            pages.extend(["billing", "subscriptions"])
        if "orders" in features:
            pages.extend(["orders", "checkout"])
        if "appointments" in features:
            pages.append("appointments")
        if "reports" in features or "analytics" in features:
            pages.extend(["reports", "analytics"])
        if "inventory" in features:
            pages.append("inventory")
        return sorted(set(pages))

    def _ambiguity_checks(self, normalized: str) -> list[str]:
        messages: list[str] = []
        if "fast" in normalized or "scalable" in normalized:
            messages.append("Non-functional requirements present but not quantified")
        if "maybe" in normalized or " or " in normalized:
            messages.append("Prompt includes potentially conflicting alternatives")
        if len(normalized.split()) < 6:
            messages.append("Prompt is terse; assumptions likely required")
        if "no auth" in normalized and "protected" in normalized:
            messages.append("Conflicting auth requirement detected")
        if "everyone is admin" in normalized and "admins only" in normalized:
            messages.append("Conflicting role visibility requirement detected")
        return sorted(set(messages))
