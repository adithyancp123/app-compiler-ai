"""Schema generation layer produces executable app configuration schema."""

from __future__ import annotations

from app.models.contracts import (
    APIField,
    APIRoute,
    APISchema,
    AccessRule,
    AuthRole,
    AuthSchema,
    DBColumn,
    DBRelation,
    DBSchema,
    DBTable,
    GeneratedSchema,
    StageName,
    StageOutput,
    StageStatus,
    SystemDesignSpec,
    UIAction,
    UIComponent,
    UIForm,
    UIFormField,
    UIPage,
    UISchema,
)


class SchemaGenerator:
    """Stage 3 deterministic strict config generator."""

    def run(self, design_output: StageOutput) -> StageOutput:
        design = SystemDesignSpec.model_validate(design_output.content)

        ui = self._build_ui_schema(design)
        api = self._build_api_schema(design)
        db = self._build_db_schema(design)
        auth = self._build_auth_schema(design, api)

        schema = GeneratedSchema(ui=ui, api=api, db=db, auth=auth)
        return StageOutput(
            stage=StageName.schema_generation,
            status=StageStatus.success,
            content=schema.model_dump(),
            notes=["Strict JSON schema generated with stable ordering"],
        )

    def _build_ui_schema(self, design: SystemDesignSpec) -> UISchema:
        pages: list[UIPage] = []
        available_domains = set(design.api_domains)
        for page_name in sorted(design.page_navigation.keys()):
            route_name = f"/{page_name}"
            form_fields = [UIFormField(name="name", type="string", required=True)]
            page_domain = self._page_to_domain(page_name)
            if page_domain not in available_domains:
                if page_domain.endswith("s") and page_domain[:-1] in available_domains:
                    page_domain = page_domain[:-1]
                elif f"{page_domain}s" in available_domains:
                    page_domain = f"{page_domain}s"
                else:
                    page_domain = "system"
            submit_route = f"/{page_domain}/create"
            page = UIPage(
                name=page_name,
                path=route_name,
                layout="app-shell",
                components=[UIComponent(component="header"), UIComponent(component="data-table", bind_entity=self._page_to_entity(page_name))],
                forms=[UIForm(form_id=f"{page_name}_form", submit_route=submit_route, fields=form_fields)],
                actions=[UIAction(id=f"go_{page_name}", type="navigate", target=route_name)],
            )
            pages.append(page)
        return UISchema(pages=pages, navigation=design.page_navigation)

    def _build_api_schema(self, design: SystemDesignSpec) -> APISchema:
        routes: list[APIRoute] = []
        for domain in sorted(design.api_domains):
            request_fields = [APIField(name="name", type="string", required=True)]
            response_fields = [APIField(name="id", type="integer", required=True), APIField(name="name", type="string", required=True)]
            routes.append(
                APIRoute(
                    name=f"create_{domain}",
                    domain=domain,
                    path=f"/{domain}/create",
                    method="POST",
                    auth_required=domain != "system",
                    request_model=request_fields,
                    response_model=response_fields,
                )
            )
            routes.append(
                APIRoute(
                    name=f"list_{domain}",
                    domain=domain,
                    path=f"/{domain}/list",
                    method="GET",
                    auth_required=domain != "system",
                    request_model=[],
                    response_model=response_fields,
                )
            )
        return APISchema(routes=sorted(routes, key=lambda route: route.path))

    def _build_db_schema(self, design: SystemDesignSpec) -> DBSchema:
        tables: list[DBTable] = [
            DBTable(
                name="users",
                columns=[
                    DBColumn(name="id", type="INTEGER", primary_key=True),
                    DBColumn(name="name", type="TEXT"),
                    DBColumn(name="role", type="TEXT"),
                ],
                constraints=["unique(name)"],
            )
        ]
        relations: list[DBRelation] = []
        for relation in design.entity_relationships:
            table_name = f"{relation.target}s"
            if all(table.name != table_name for table in tables):
                tables.append(
                    DBTable(
                        name=table_name,
                        columns=[
                            DBColumn(name="id", type="INTEGER", primary_key=True),
                            DBColumn(name="name", type="TEXT"),
                            DBColumn(name="user_id", type="INTEGER", nullable=False),
                        ],
                        constraints=[],
                    )
                )
            relations.append(
                DBRelation(
                    table=table_name,
                    column="user_id",
                    references_table="users",
                    references_column="id",
                )
            )
        return DBSchema(tables=sorted(tables, key=lambda table: table.name), relations=sorted(relations, key=lambda rel: rel.table))

    def _build_auth_schema(self, design: SystemDesignSpec, api: APISchema) -> AuthSchema:
        roles = [AuthRole(name=rule.role, permissions=rule.permissions) for rule in sorted(design.permissions, key=lambda rule: rule.role)]
        access_rules: list[AccessRule] = []
        role_names = [role.name for role in roles]
        for route in api.routes:
            allowed_roles = role_names if not route.path.startswith("/reports") else [role for role in role_names if role == "admin"]
            access_rules.append(AccessRule(route=route.path, allowed_roles=sorted(allowed_roles)))
        return AuthSchema(roles=roles, access_rules=sorted(access_rules, key=lambda item: item.route))

    def _page_to_domain(self, page_name: str) -> str:
        explicit_map = {
            "home": "system",
            "settings": "system",
            "dashboard": "system",
            "contacts": "contacts",
            "contact-detail": "contacts",
            "billing": "billing",
            "subscriptions": "billing",
            "orders": "orders",
            "checkout": "orders",
            "reports": "reports",
            "appointments": "appointments",
            "analytics": "reports",
            "inventory": "inventory",
            "classes": "reports",
            "catalog": "inventory",
        }
        if page_name in explicit_map:
            return explicit_map[page_name]
        return page_name.replace("-detail", "s")

    def _page_to_entity(self, page_name: str) -> str:
        return "user" if page_name in {"home", "dashboard", "settings"} else page_name.rstrip("s")
