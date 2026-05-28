"""Deterministic domain templates used during intent extraction."""

from __future__ import annotations

DOMAIN_TEMPLATES: dict[str, dict[str, list[str] | str]] = {
    "crm": {
        "app_type": "crm",
        "features": ["auth", "dashboard", "contacts", "reports", "notifications"],
        "roles": ["admin", "manager", "member"],
        "entities": ["user", "contact", "record"],
        "pages": ["home", "dashboard", "contacts", "contact-detail", "reports", "settings"],
        "integrations": ["email"],
    },
    "ecommerce": {
        "app_type": "ecommerce",
        "features": ["auth", "dashboard", "orders", "inventory", "billing", "notifications"],
        "roles": ["admin", "manager", "member", "viewer"],
        "entities": ["user", "product", "order", "payment"],
        "pages": ["home", "dashboard", "orders", "checkout", "inventory", "billing", "settings"],
        "integrations": ["stripe", "email"],
    },
    "healthcare": {
        "app_type": "healthcare",
        "features": ["auth", "dashboard", "appointments", "billing", "reports"],
        "roles": ["admin", "doctor", "nurse", "member"],
        "entities": ["user", "patient", "appointment", "payment", "prescription"],
        "pages": ["home", "dashboard", "appointments", "billing", "reports", "settings"],
        "integrations": ["email", "sms"],
    },
    "education": {
        "app_type": "education",
        "features": ["auth", "dashboard", "reports", "notifications"],
        "roles": ["admin", "teacher", "student", "member"],
        "entities": ["user", "student", "classroom", "attendance", "record"],
        "pages": ["home", "dashboard", "classes", "reports", "settings"],
        "integrations": ["email"],
    },
    "saas": {
        "app_type": "saas",
        "features": ["auth", "dashboard", "billing", "reports", "notifications"],
        "roles": ["admin", "manager", "member", "viewer"],
        "entities": ["user", "subscription", "payment", "workspace"],
        "pages": ["home", "dashboard", "billing", "subscriptions", "reports", "settings"],
        "integrations": ["stripe", "email", "sso"],
    },
    "marketplace": {
        "app_type": "marketplace",
        "features": ["auth", "dashboard", "orders", "inventory", "billing", "reports"],
        "roles": ["admin", "seller", "buyer", "viewer"],
        "entities": ["user", "product", "order", "payment", "listing"],
        "pages": ["home", "dashboard", "catalog", "orders", "checkout", "billing", "settings"],
        "integrations": ["stripe", "email"],
    },
    "inventory": {
        "app_type": "inventory",
        "features": ["auth", "dashboard", "inventory", "reports", "notifications"],
        "roles": ["admin", "manager", "member"],
        "entities": ["user", "product", "warehouse", "stock-movement"],
        "pages": ["home", "dashboard", "inventory", "reports", "settings"],
        "integrations": ["email"],
    },
}

KEYWORD_TO_TEMPLATE = {
    "crm": "crm",
    "e-commerce": "ecommerce",
    "ecommerce": "ecommerce",
    "hospital": "healthcare",
    "clinic": "healthcare",
    "school": "education",
    "saas": "saas",
    "subscription": "saas",
    "marketplace": "marketplace",
    "inventory": "inventory",
}
