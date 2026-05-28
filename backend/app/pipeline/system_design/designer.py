"""System design layer derives architecture from extracted intent."""

from __future__ import annotations

from app.models.contracts import (
    EntityRelationship,
    FeatureFlow,
    IntentSpec,
    PermissionRule,
    StageName,
    StageOutput,
    StageStatus,
    SystemDesignSpec,
)


class SystemDesigner:
    """Stage 2 deterministic architecture synthesis."""

    def run(self, intent_output: StageOutput) -> StageOutput:
        intent = IntentSpec.model_validate(intent_output.content)

        modules = self._build_modules(intent)
        feature_flows = self._build_feature_flows(intent)
        relationships = self._build_entity_relationships(intent)
        permissions = self._build_permissions(intent)
        navigation = self._build_navigation(intent)
        api_domains = sorted(set([feature for feature in intent.features if feature != "dashboard"] + ["system"]))

        design = SystemDesignSpec(
            modules=modules,
            feature_flows=feature_flows,
            entity_relationships=relationships,
            permissions=permissions,
            page_navigation=navigation,
            api_domains=api_domains,
        )

        return StageOutput(
            stage=StageName.system_design,
            status=StageStatus.success,
            content=design.model_dump(),
            notes=["Deterministic module map and permission topology generated"],
        )

    def _build_modules(self, intent: IntentSpec) -> list[str]:
        modules = ["prompt-interface", "intent-engine", "schema-compiler", "validation-engine", "runtime-simulator"]
        modules.extend([f"feature-{feature}" for feature in intent.features])
        return sorted(set(modules))

    def _build_feature_flows(self, intent: IntentSpec) -> list[FeatureFlow]:
        primary_role = "admin" if "admin" in intent.roles else intent.roles[0]
        flows: list[FeatureFlow] = []
        for feature in intent.features:
            flows.append(
                FeatureFlow(
                    feature=feature,
                    primary_role=primary_role,
                    steps=[
                        "open_page",
                        f"perform_{feature}_action",
                        "persist_changes",
                    ],
                )
            )
        return sorted(flows, key=lambda flow: flow.feature)

    def _build_entity_relationships(self, intent: IntentSpec) -> list[EntityRelationship]:
        relationships: list[EntityRelationship] = []
        entities = sorted(intent.entities)
        if "user" in entities:
            for entity in entities:
                if entity != "user":
                    relationships.append(EntityRelationship(source="user", target=entity, relation="owns_many"))
        for idx in range(len(entities) - 1):
            relationships.append(
                EntityRelationship(source=entities[idx], target=entities[idx + 1], relation="references")
            )
        return relationships

    def _build_permissions(self, intent: IntentSpec) -> list[PermissionRule]:
        permissions: list[PermissionRule] = []
        feature_permissions = [f"{feature}:read" for feature in intent.features] + [
            f"{feature}:write" for feature in intent.features if feature != "reports"
        ]
        for role in sorted(intent.roles):
            if role == "admin":
                role_permissions = sorted(set(feature_permissions + ["system:manage"]))
            elif role == "viewer":
                role_permissions = sorted(permission for permission in feature_permissions if permission.endswith(":read"))
            else:
                role_permissions = sorted(permission for permission in feature_permissions if "write" not in permission)
            permissions.append(PermissionRule(role=role, permissions=role_permissions))
        return permissions

    def _build_navigation(self, intent: IntentSpec) -> dict[str, list[str]]:
        pages = sorted(set(intent.pages + ["settings"]))
        navigation = {page: [] for page in pages}
        for idx, page in enumerate(pages[:-1]):
            navigation[page].append(pages[idx + 1])
        return navigation
