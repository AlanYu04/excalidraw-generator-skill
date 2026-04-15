"""Tests for the deterministic DiagramSpec pipeline."""
import json
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.pipeline import (
    DiagramSpec,
    generate_diagram,
    normalize_diagram_spec,
    save_generated_diagram,
    validate_scene_contract,
)


def _sample_spec():
    return {
        "diagram_type": "flow",
        "style": "conference",
        "nodes": [
            {"id": "input", "label": "Input", "role": "primary"},
            {"id": "process", "label": "Process", "role": "info"},
            {"id": "output", "label": "Output", "role": "accent"},
        ],
        "edges": [
            {"id": "step-1", "from_id": "input", "to_id": "process", "label": "clean"},
            {"id": "step-2", "from_id": "process", "to_id": "output"},
        ],
    }


def test_normalize_diagram_spec_canonicalizes_aliases():
    spec = normalize_diagram_spec(_sample_spec())
    assert spec.diagram_type == "flowchart"
    assert spec.style == "vivid"
    assert spec.output_format == ".excalidraw"
    assert spec.style_rules["font_family"] == 2
    assert spec.style_rules["border_radius"] is False


def test_generate_diagram_is_stable_across_runs():
    result_1 = generate_diagram(_sample_spec())
    result_2 = generate_diagram(_sample_spec())

    assert result_1.final_status == "PASS"
    assert result_2.final_status == "PASS"
    assert result_1.elements == result_2.elements
    assert result_1.to_dict()["spec"] == result_2.to_dict()["spec"]


def test_validate_scene_contract_catches_style_mismatch():
    result = generate_diagram(_sample_spec())
    assert result.final_status == "PASS"

    broken = json.loads(json.dumps(result.elements))
    for element in broken:
        if element["type"] == "text":
            element["fontFamily"] = 3
            break

    report = validate_scene_contract(broken, result.spec)
    assert report.status == "REPAIRABLE"
    assert any(issue.code == "STYLE-FONT-FAMILY" for issue in report.issues)


def test_save_generated_diagram_writes_artifacts():
    result = generate_diagram(_sample_spec())
    assert result.final_status == "PASS"

    with tempfile.TemporaryDirectory() as tmpdir:
        output_path = os.path.join(tmpdir, "diagram.excalidraw")
        artifacts_dir = os.path.join(tmpdir, "artifacts")
        save_generated_diagram(output_path, result, artifact_dir=artifacts_dir)

        assert os.path.exists(output_path)
        assert os.path.exists(os.path.join(artifacts_dir, "input_spec.json"))
        assert os.path.exists(os.path.join(artifacts_dir, "diagram_spec.json"))
        assert os.path.exists(os.path.join(artifacts_dir, "validation_report.json"))


def test_save_generated_diagram_rejects_invalid_result():
    invalid = DiagramSpec(diagram_type="invalid")
    result = generate_diagram(invalid)
    assert result.final_status == "FAIL"

    with tempfile.TemporaryDirectory() as tmpdir:
        output_path = os.path.join(tmpdir, "diagram.excalidraw")
        try:
            save_generated_diagram(output_path, result)
            assert False, "save_generated_diagram should reject invalid pipeline results"
        except ValueError as exc:
            assert "status FAIL" in str(exc)
