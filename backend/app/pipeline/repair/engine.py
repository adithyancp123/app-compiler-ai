"""Repair engine applies targeted fixes to failed modules only."""

from __future__ import annotations

from app.models.contracts import (
    AccessRule,
    DBColumn,
    RepairAction,
    ValidationErrorItem,
)


class RepairEngine:
    """Stage 5 targeted repair strategies with module scope."""

    def run(self, generated_schema: dict, validation_errors: list[ValidationErrorItem]) -> tuple[dict, list[RepairAction]]:
        schema = generated_schema
        actions: list[RepairAction] = []

        for error in validation_errors:
            if error.code == "UI_FORM_ROUTE_UNMAPPED":
                actions.extend(self._repair_ui_route_mapping(schema, error))
            elif error.code == "UI_FIELD_NOT_IN_API":
                actions.extend(self._repair_missing_api_field(schema, error))
            elif error.code == "API_FIELD_NOT_IN_DB":
                actions.extend(self._repair_missing_db_field(schema, error))
            elif error.code in {"AUTH_RULE_MISSING", "ADMIN_ANALYTICS_GATE_MISSING"}:
                actions.extend(self._repair_auth_rule(schema, error))
            elif error.code == "AUTH_UNKNOWN_ROLE":
                actions.extend(self._repair_unknown_role(schema, error))

        return schema, actions

    def _repair_ui_route_mapping(self, schema: dict, error: ValidationErrorItem) -> list[RepairAction]:
        _ = error
        actions: list[RepairAction] = []
        api_paths = {route["path"] for route in schema["api"]["routes"]}
        for page in schema["ui"]["pages"]:
            for form in page["forms"]:
                if form["submit_route"] not in api_paths:
                    fallback_route = f"/{page['name']}/create" if f"/{page['name']}/create" in api_paths else "/system/create"
                    form["submit_route"] = fallback_route
                    actions.append(
                        RepairAction(
                            module="ui",
                            action=f"Updated submit route for {form['form_id']} to {fallback_route}",
                            status="repaired",
                            repair_type="schema_alignment",
                        )
                    )
        return actions

    def _repair_missing_api_field(self, schema: dict, error: ValidationErrorItem) -> list[RepairAction]:
        field_name = error.message.split("Field ")[1].split(" not found")[0]
        route_name = error.message.split("API model ")[1]
        actions: list[RepairAction] = []
        inserted = False
        for route in schema["api"]["routes"]:
            if route["name"] == route_name:
                route["request_model"].append({"name": field_name, "type": "string", "required": True})
                route["request_model"] = sorted(route["request_model"], key=lambda item: item["name"])
                inserted = True
                actions.append(
                    RepairAction(
                        module="api",
                        action=f"Inserted missing request field {field_name} into {route_name}",
                        status="repaired",
                        repair_type="field_insertion",
                    )
                )
        if inserted:
            primary_table = schema["db"]["tables"][0]
            existing_columns = {column["name"] for column in primary_table["columns"]}
            if field_name not in existing_columns:
                primary_table["columns"].append(DBColumn(name=field_name, type="TEXT", nullable=False).model_dump())
                primary_table["columns"] = sorted(primary_table["columns"], key=lambda column: column["name"])
                actions.append(
                    RepairAction(
                        module="db",
                        action=f"Added dependent DB column {field_name} for API compatibility",
                        status="repaired",
                        repair_type="dependency_reconciliation",
                    )
                )
        return actions

    def _repair_missing_db_field(self, schema: dict, error: ValidationErrorItem) -> list[RepairAction]:
        field_name = error.message.split("API field ")[1].split(" does not map")[0]
        actions: list[RepairAction] = []
        target_table = schema["db"]["tables"][0]
        existing = {column["name"] for column in target_table["columns"]}
        if field_name not in existing:
            target_table["columns"].append(DBColumn(name=field_name, type="TEXT", nullable=False).model_dump())
            target_table["columns"] = sorted(target_table["columns"], key=lambda column: column["name"])
            actions.append(
                RepairAction(
                    module="db",
                    action=f"Inserted missing DB column {field_name} in table {target_table['name']}",
                    status="repaired",
                    repair_type="dependency_reconciliation",
                )
            )
        return actions

    def _repair_auth_rule(self, schema: dict, error: ValidationErrorItem) -> list[RepairAction]:
        actions: list[RepairAction] = []
        if "protected route" in error.message:
            route = error.message.split("protected route ")[1]
            role_names = sorted(role["name"] for role in schema["auth"]["roles"])
            schema["auth"]["access_rules"].append(AccessRule(route=route, allowed_roles=role_names).model_dump())
            schema["auth"]["access_rules"] = sorted(schema["auth"]["access_rules"], key=lambda rule: rule["route"])
            actions.append(
                RepairAction(
                    module="auth",
                    action=f"Added access rule for {route}",
                    status="repaired",
                    repair_type="schema_alignment",
                )
            )
        return actions

    def _repair_unknown_role(self, schema: dict, error: ValidationErrorItem) -> list[RepairAction]:
        role_name = error.message.split("unknown role ")[1]
        actions: list[RepairAction] = []
        schema["auth"]["roles"].append({"name": role_name, "permissions": ["system:read"]})
        schema["auth"]["roles"] = sorted(schema["auth"]["roles"], key=lambda role: role["name"])
        actions.append(
            RepairAction(
                module="auth",
                action=f"Inserted missing role {role_name}",
                status="repaired",
                repair_type="fallback_assumption",
            )
        )
        return actions
