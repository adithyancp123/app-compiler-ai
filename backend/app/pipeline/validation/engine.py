"""Validation engine for strict schema and consistency checks."""

from __future__ import annotations

from app.models.contracts import (
    APISchema,
    AuthSchema,
    DBSchema,
    GeneratedSchema,
    UISchema,
    ValidationErrorItem,
    ValidationReport,
    ValidationWarningItem,
)


class ValidationEngine:
    """Stage 4 strict validator for schema and cross-layer consistency."""

    def run(self, generated_schema: dict) -> ValidationReport:
        errors: list[ValidationErrorItem] = []
        warnings: list[ValidationWarningItem] = []
        repair_candidates: list[str] = []

        try:
            schema = GeneratedSchema.model_validate(generated_schema)
        except Exception as exc:  # noqa: BLE001
            return ValidationReport(
                valid=False,
                errors=[ValidationErrorItem(module="schema", code="INVALID_JSON_SCHEMA", message=str(exc))],
                warnings=[],
                consistency_score=0,
                repair_candidates=["schema:regenerate-typed-json"],
            )

        self._validate_required_sections(schema, errors, repair_candidates)
        self._validate_entity_lineage(schema.ui, schema.api, schema.db, errors, warnings, repair_candidates)
        self._validate_feature_consistency(schema, errors, warnings, repair_candidates)
        self._validate_navigation_consistency(schema.ui, schema.api, errors, warnings, repair_candidates)
        self._validate_role_consistency(schema.auth, schema.api, errors, warnings, repair_candidates)

        score = max(0, min(100, 100 - (len(errors) * 12) - (len(warnings) * 3)))
        return ValidationReport(
            valid=len(errors) == 0,
            errors=errors,
            warnings=warnings,
            consistency_score=score,
            repair_candidates=sorted(set(repair_candidates)),
        )

    def _validate_required_sections(
        self,
        schema: GeneratedSchema,
        errors: list[ValidationErrorItem],
        repair_candidates: list[str],
    ) -> None:
        if not schema.ui.pages:
            errors.append(ValidationErrorItem(module="ui", code="UI_PAGES_MISSING", message="UI pages are required"))
            repair_candidates.append("ui:add-default-pages")
        if not schema.api.routes:
            errors.append(ValidationErrorItem(module="api", code="API_ROUTES_MISSING", message="API routes are required"))
            repair_candidates.append("api:add-domain-routes")
        if not schema.db.tables:
            errors.append(ValidationErrorItem(module="db", code="DB_TABLES_MISSING", message="DB tables are required"))
            repair_candidates.append("db:add-entity-tables")
        if not schema.auth.roles:
            errors.append(ValidationErrorItem(module="auth", code="AUTH_ROLES_MISSING", message="Auth roles are required"))
            repair_candidates.append("auth:add-default-roles")

    def _validate_entity_lineage(
        self,
        ui: UISchema,
        api: APISchema,
        db: DBSchema,
        errors: list[ValidationErrorItem],
        warnings: list[ValidationWarningItem],
        repair_candidates: list[str],
    ) -> None:
        api_by_path = {route.path: route for route in api.routes}
        db_fields = {column.name for table in db.tables for column in table.columns}
        used_db_fields: set[str] = set()

        for page in ui.pages:
            for form in page.forms:
                route = api_by_path.get(form.submit_route)
                if not route:
                    errors.append(
                        ValidationErrorItem(
                            module="ui",
                            code="UI_FORM_ROUTE_UNMAPPED",
                            message=f"Form route {form.submit_route} is missing in API routes",
                        )
                    )
                    repair_candidates.append("ui:align-form-route")
                    continue

                api_request_fields = {field.name for field in route.request_model}
                for field in form.fields:
                    if field.name not in api_request_fields:
                        errors.append(
                            ValidationErrorItem(
                                module="ui",
                                code="UI_FIELD_NOT_IN_API",
                                message=f"Field {field.name} not found in API model {route.name}",
                            )
                        )
                        repair_candidates.append("api:insert-missing-request-field")
                    elif field.name not in db_fields:
                        errors.append(
                            ValidationErrorItem(
                                module="api",
                                code="API_FIELD_NOT_IN_DB",
                                message=f"API field {field.name} does not map to DB schema",
                            )
                        )
                        repair_candidates.append("db:add-missing-column")
                    else:
                        used_db_fields.add(field.name)

        for route in api.routes:
            for field in route.request_model:
                if field.name not in db_fields and field.name != "id":
                    errors.append(
                        ValidationErrorItem(
                            module="api",
                            code="API_FIELD_NOT_IN_DB",
                            message=f"API field {field.name} does not map to DB schema",
                        )
                    )
                    repair_candidates.append("db:add-missing-column")
                elif field.name != "id":
                    used_db_fields.add(field.name)

        unused_db_fields = sorted(field for field in db_fields if field not in used_db_fields and field not in {"id", "role", "user_id"})
        if unused_db_fields:
            warnings.append(
                ValidationWarningItem(
                    module="db",
                    code="DB_UNUSED_FIELDS",
                    message=f"DB fields never used by UI/API lineage: {', '.join(unused_db_fields)}",
                )
            )

    def _validate_feature_consistency(
        self,
        schema: GeneratedSchema,
        errors: list[ValidationErrorItem],
        warnings: list[ValidationWarningItem],
        repair_candidates: list[str],
    ) -> None:
        route_paths = {route.path for route in schema.api.routes}
        db_table_names = {table.name for table in schema.db.tables}
        permissions = {perm for role in schema.auth.roles for perm in role.permissions}
        page_names = {page.name for page in schema.ui.pages}

        has_billing_routes = any("billing" in route for route in route_paths)
        has_subscription_entity = any("subscription" in table for table in db_table_names)
        if has_billing_routes and not has_subscription_entity:
            warnings.append(
                ValidationWarningItem(
                    module="db",
                    code="PAYMENT_SUBSCRIPTION_ENTITY_MISSING",
                    message="Billing routes exist but subscription entity is absent",
                )
            )
            repair_candidates.append("db:add-subscription-table")

        analytics_pages = {page for page in page_names if "analytics" in page or "reports" in page}
        if analytics_pages and "admin" not in {role.name for role in schema.auth.roles}:
            errors.append(
                ValidationErrorItem(
                    module="auth",
                    code="ANALYTICS_ADMIN_ROLE_MISSING",
                    message="Analytics requires admin role",
                )
            )
            repair_candidates.append("auth:add-admin-role")

        auth_routes = [route for route in route_paths if "auth" in route or "login" in route]
        if not auth_routes and "auth:read" not in permissions:
            warnings.append(
                ValidationWarningItem(
                    module="auth",
                    code="AUTH_FLOW_WEAK",
                    message="Auth permissions are present but explicit auth routes are missing",
                )
            )

    def _validate_navigation_consistency(
        self,
        ui: UISchema,
        api: APISchema,
        errors: list[ValidationErrorItem],
        warnings: list[ValidationWarningItem],
        repair_candidates: list[str],
    ) -> None:
        page_names = {page.name for page in ui.pages}
        if not page_names:
            return

        outgoing = {page: set(destinations) for page, destinations in ui.navigation.items()}
        incoming: dict[str, int] = {page: 0 for page in page_names}
        for source, destinations in outgoing.items():
            if source not in page_names:
                warnings.append(
                    ValidationWarningItem(
                        module="ui",
                        code="NAV_SOURCE_UNKNOWN",
                        message=f"Navigation source {source} has no page definition",
                    )
                )
            for destination in destinations:
                if destination not in page_names:
                    errors.append(
                        ValidationErrorItem(
                            module="ui",
                            code="NAV_BROKEN_LINK",
                            message=f"Navigation target {destination} is missing",
                        )
                    )
                    repair_candidates.append("ui:remove-broken-nav-link")
                else:
                    incoming[destination] += 1

        dead_pages = [page for page in sorted(page_names) if incoming[page] == 0 and page != "home"]
        if dead_pages:
            warnings.append(
                ValidationWarningItem(
                    module="ui",
                    code="NAV_DEAD_PAGES",
                    message=f"Dead pages with no incoming links: {', '.join(dead_pages)}",
                )
            )

        api_paths = {route.path for route in api.routes}
        for page in ui.pages:
            for form in page.forms:
                if form.submit_route not in api_paths:
                    errors.append(
                        ValidationErrorItem(
                            module="ui",
                            code="UI_SUBMIT_ROUTE_MISSING",
                            message=f"Submit route {form.submit_route} missing in API",
                        )
                    )
                    repair_candidates.append("api:add-missing-submit-route")

    def _validate_role_consistency(
        self,
        auth: AuthSchema,
        api: APISchema,
        errors: list[ValidationErrorItem],
        warnings: list[ValidationWarningItem],
        repair_candidates: list[str],
    ) -> None:
        roles = {role.name: set(role.permissions) for role in auth.roles}
        if not roles:
            return

        for role_name, permissions in roles.items():
            if not permissions:
                warnings.append(
                    ValidationWarningItem(
                        module="auth",
                        code="ROLE_WITHOUT_PERMISSIONS",
                        message=f"Role {role_name} has no permissions",
                    )
                )
                repair_candidates.append("auth:assign-default-permissions")

        known_roles = set(roles.keys())
        for rule in auth.access_rules:
            for role in rule.allowed_roles:
                if role not in known_roles:
                    errors.append(
                        ValidationErrorItem(
                            module="auth",
                            code="AUTH_UNKNOWN_ROLE",
                            message=f"Route {rule.route} references unknown role {role}",
                        )
                    )
                    repair_candidates.append("auth:add-missing-role")

        route_map = {route.path: route for route in api.routes}
        for route_path, route in route_map.items():
            if route.auth_required and not any(rule.route == route_path for rule in auth.access_rules):
                errors.append(
                    ValidationErrorItem(
                        module="auth",
                        code="AUTH_RULE_MISSING",
                        message=f"Auth rule missing for protected route {route_path}",
                    )
                )
                repair_candidates.append("auth:add-route-rule")

            if "analytics" in route_path:
                analytics_rule = next((rule for rule in auth.access_rules if rule.route == route_path), None)
                if not analytics_rule or "admin" not in analytics_rule.allowed_roles:
                    errors.append(
                        ValidationErrorItem(
                            module="auth",
                            code="ADMIN_ANALYTICS_GATE_MISSING",
                            message="Analytics routes must include admin access",
                        )
                    )
                    repair_candidates.append("auth:restrict-analytics-admin")
