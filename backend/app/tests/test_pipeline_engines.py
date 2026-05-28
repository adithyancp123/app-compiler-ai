"""Unit tests for validation, repair, and runtime simulation engines."""

from app.pipeline.intent.extractor import IntentExtractor
from app.pipeline.repair.engine import RepairEngine
from app.pipeline.runtime.simulator import RuntimeSimulator
from app.pipeline.schema.generator import SchemaGenerator
from app.pipeline.system_design.designer import SystemDesigner
from app.pipeline.validation.engine import ValidationEngine


def _base_schema(prompt: str = "Build CRM with login and payments") -> dict:
    intent = IntentExtractor().run(prompt)
    design = SystemDesigner().run(intent)
    return SchemaGenerator().run(design).content


def test_validation_cross_layer_detects_missing_api_field() -> None:
    schema = _base_schema()
    schema["ui"]["pages"][0]["forms"][0]["fields"].append({"name": "email", "type": "string", "required": True})

    report = ValidationEngine().run(schema)
    assert report.valid is False
    assert report.consistency_score < 100
    assert any(error.code == "UI_FIELD_NOT_IN_API" for error in report.errors)


def test_repair_engine_repairs_specific_module() -> None:
    schema = _base_schema()
    schema["ui"]["pages"][0]["forms"][0]["fields"].append({"name": "email", "type": "string", "required": True})

    validator = ValidationEngine()
    initial_report = validator.run(schema)
    repaired_schema, actions = RepairEngine().run(schema, initial_report.errors)
    repaired_report = validator.run(repaired_schema)

    assert actions
    assert any(action.module == "api" for action in actions)
    assert repaired_report.valid is True


def test_runtime_simulation_marks_executable() -> None:
    schema = _base_schema()
    result = RuntimeSimulator().run(schema)
    assert result["executable"] is True
    assert result["confidence_score"] == 100
    assert result["issues"] == []


def test_domain_template_inference_for_hospital() -> None:
    schema = _base_schema("Build a hospital management system with doctors, patients, appointments and billing")
    db_tables = {table["name"] for table in schema["db"]["tables"]}
    assert "patients" in db_tables
    assert "appointments" in db_tables


def test_navigation_consistency_detects_broken_link() -> None:
    schema = _base_schema()
    schema["ui"]["navigation"]["home"].append("missing-page")
    report = ValidationEngine().run(schema)
    assert any(error.code == "NAV_BROKEN_LINK" for error in report.errors)
