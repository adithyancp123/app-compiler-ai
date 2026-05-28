"""Runtime simulation validates generated app executability."""

from __future__ import annotations

from app.models.contracts import GeneratedSchema


class RuntimeSimulator:
    """Stage 6 execution-aware deterministic dry-run checks."""

    def run(self, generated_schema: dict) -> dict:
        issues: list[str] = []
        schema = GeneratedSchema.model_validate(generated_schema)

        page_paths = [page.path for page in schema.ui.pages]
        ui_renderable = bool(page_paths and all(path.startswith("/") for path in page_paths))
        if not ui_renderable:
            issues.append("UI pages are missing or have invalid paths")

        api_paths = {route.path for route in schema.api.routes}
        ui_submit_paths = {form.submit_route for page in schema.ui.pages for form in page.forms}
        api_mapped = ui_submit_paths.issubset(api_paths)
        if not api_mapped:
            issues.append("Some UI forms reference unmapped API routes")

        db_tables = {table.name for table in schema.db.tables}
        relation_ok = all(relation.table in db_tables and relation.references_table in db_tables for relation in schema.db.relations)
        db_schema_exists = "users" in db_tables and relation_ok
        if not db_schema_exists:
            issues.append("Database schema or relations are incomplete")

        role_names = {role.name for role in schema.auth.roles}
        auth_rules_valid = True
        for rule in schema.auth.access_rules:
            if not set(rule.allowed_roles).issubset(role_names):
                auth_rules_valid = False
                issues.append(f"Auth rule {rule.route} contains unknown roles")

        route_integrity = all(route.method in {"GET", "POST", "PUT", "PATCH", "DELETE"} for route in schema.api.routes)
        if not route_integrity:
            issues.append("One or more API routes use unsupported HTTP methods")

        has_premium = any("premium" in route.path or "billing" in route.path for route in schema.api.routes)
        has_billing = any("billing" in table.name or "payment" in table.name for table in schema.db.tables)
        if has_premium and not has_billing:
            issues.append("Premium routes exist without billing entities")

        has_analytics = any("analytics" in page.name or "reports" in page.name for page in schema.ui.pages)
        analytics_admin = all(
            "admin" in rule.allowed_roles
            for rule in schema.auth.access_rules
            if "analytics" in rule.route or "reports" in rule.route
        )
        if has_analytics and not analytics_admin:
            issues.append("Analytics exists without admin role protection")

        executable = ui_renderable and api_mapped and db_schema_exists and auth_rules_valid and route_integrity and len(issues) == 0
        confidence_score = max(0, min(100, 100 - len(issues) * 15))

        return {
            "ui_renderable": ui_renderable,
            "api_mapped": api_mapped,
            "db_schema_exists": db_schema_exists,
            "auth_rules_valid": auth_rules_valid,
            "route_integrity": route_integrity,
            "executable": executable,
            "confidence_score": confidence_score,
            "issues": issues,
        }
