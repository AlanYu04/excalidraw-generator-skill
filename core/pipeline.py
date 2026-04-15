"""Deterministic diagram pipeline: spec -> render -> validate -> repair -> save."""

from __future__ import annotations

import json
import os
from dataclasses import asdict, dataclass, field
from typing import Any

from styles.loader import load_style

from . import engine
from .scene import remap_scene_references


ALLOWED_DIAGRAM_TYPES = {
    "architecture",
    "comparison",
    "concept-map",
    "flowchart",
    "pipeline",
    "system",
}

DIAGRAM_TYPE_ALIASES = {
    "architecture-diagram": "architecture",
    "data-flow": "flowchart",
    "dataflow": "flowchart",
    "flow": "flowchart",
    "flow-diagram": "flowchart",
    "process": "pipeline",
    "system-architecture": "architecture",
}

SHAPE_ALIASES = {
    "box": "rectangle",
    "circle": "ellipse",
    "decision": "diamond",
    "ellipse": "ellipse",
    "rectangle": "rectangle",
    "rect": "rectangle",
    "diamond": "diamond",
}

OUTPUT_FORMAT_ALIASES = {
    ".excalidraw": ".excalidraw",
    ".excalidraw.md": ".excalidraw.md",
    "excalidraw": ".excalidraw",
    "json": ".excalidraw",
    "md": ".excalidraw.md",
    "obsidian": ".excalidraw.md",
    "obsidian-md": ".excalidraw.md",
}


@dataclass
class DiagramCanvas:
    width: int | None = None
    height: int | None = None
    background: str | None = None


@dataclass
class DiagramNode:
    id: str
    label: str
    kind: str = "rectangle"
    x: float | None = None
    y: float | None = None
    width: float | None = None
    height: float | None = None
    role: str = "primary"
    row: int | None = None
    column: int | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class DiagramEdge:
    id: str
    from_id: str
    to_id: str
    label: str = ""
    role: str = "primary"
    arrow_mode: str = "straight"
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class DiagramGroup:
    id: str
    label: str = ""
    member_ids: list[str] = field(default_factory=list)
    role: str = "neutral"


@dataclass
class DiagramAnnotation:
    id: str
    text: str
    target_id: str | None = None
    x: float | None = None
    y: float | None = None
    role: str = "neutral"


@dataclass
class DiagramSpec:
    diagram_type: str
    style: str = "vivid"
    canvas: DiagramCanvas = field(default_factory=DiagramCanvas)
    nodes: list[DiagramNode] = field(default_factory=list)
    edges: list[DiagramEdge] = field(default_factory=list)
    groups: list[DiagramGroup] = field(default_factory=list)
    annotations: list[DiagramAnnotation] = field(default_factory=list)
    layout_rules: dict[str, Any] = field(default_factory=dict)
    style_rules: dict[str, Any] = field(default_factory=dict)
    output_format: str = ".excalidraw"


@dataclass
class ValidationIssue:
    code: str
    message: str
    severity: str = "ERROR"
    repairable: bool = True
    target: str | None = None


@dataclass
class ValidationReport:
    status: str
    issues: list[ValidationIssue] = field(default_factory=list)
    summary: str = "No issues found"

    @property
    def errors(self) -> list[ValidationIssue]:
        return [issue for issue in self.issues if issue.severity == "ERROR"]

    @property
    def warnings(self) -> list[ValidationIssue]:
        return [issue for issue in self.issues if issue.severity == "WARNING"]

    def to_dict(self) -> dict[str, Any]:
        return {
            "status": self.status,
            "summary": self.summary,
            "issues": [asdict(issue) for issue in self.issues],
            "errors": len(self.errors),
            "warnings": len(self.warnings),
        }


@dataclass
class PipelineResult:
    input_spec: dict[str, Any]
    spec: DiagramSpec
    spec_report: ValidationReport
    scene_report: ValidationReport | None = None
    elements: list[dict[str, Any]] = field(default_factory=list)
    repaired: bool = False

    @property
    def final_status(self) -> str:
        if self.spec_report.status == "FAIL":
            return "FAIL"
        if self.scene_report is None:
            return "FAIL"
        return self.scene_report.status

    def to_dict(self) -> dict[str, Any]:
        return {
            "input_spec": self.input_spec,
            "spec": diagram_spec_to_dict(self.spec),
            "spec_report": self.spec_report.to_dict(),
            "scene_report": self.scene_report.to_dict() if self.scene_report else None,
            "repaired": self.repaired,
            "elements_count": len(self.elements),
        }


def _canonical_diagram_type(value: str) -> str:
    key = value.strip().lower()
    return DIAGRAM_TYPE_ALIASES.get(key, key)


def _canonical_shape(value: str) -> str:
    key = value.strip().lower()
    return SHAPE_ALIASES.get(key, key)


def _canonical_output_format(value: str) -> str:
    key = value.strip().lower()
    return OUTPUT_FORMAT_ALIASES.get(key, key)


def _issue_status(issues: list[ValidationIssue]) -> str:
    errors = [issue for issue in issues if issue.severity == "ERROR"]
    if not errors and not issues:
        return "PASS"
    if errors and any(not issue.repairable for issue in errors):
        return "FAIL"
    return "REPAIRABLE"


def _summarize_issues(issues: list[ValidationIssue]) -> str:
    if not issues:
        return "No issues found"
    codes = {}
    for issue in issues:
        codes[issue.code] = codes.get(issue.code, 0) + 1
    return ", ".join(f"{count}x {code}" for code, count in sorted(codes.items()))


def diagram_spec_to_dict(spec: DiagramSpec) -> dict[str, Any]:
    return asdict(spec)


def normalize_diagram_spec(spec_input: DiagramSpec | dict[str, Any]) -> DiagramSpec:
    raw = diagram_spec_to_dict(spec_input) if isinstance(spec_input, DiagramSpec) else dict(spec_input)
    style_name = raw.get("style", "vivid")
    style = load_style(style_name)

    canvas_raw = raw.get("canvas") or {}
    canvas = DiagramCanvas(
        width=canvas_raw.get("width"),
        height=canvas_raw.get("height"),
        background=canvas_raw.get("background") or style.background,
    )

    nodes = []
    for idx, node_raw in enumerate(raw.get("nodes", [])):
        node = DiagramNode(
            id=str(node_raw["id"]),
            label=str(node_raw.get("label", "")).strip(),
            kind=_canonical_shape(str(node_raw.get("kind", "rectangle"))),
            x=node_raw.get("x"),
            y=node_raw.get("y"),
            width=node_raw.get("width"),
            height=node_raw.get("height"),
            role=str(node_raw.get("role", "primary")),
            row=node_raw.get("row"),
            column=node_raw.get("column"),
            metadata=dict(node_raw.get("metadata") or {}),
        )
        node.metadata.setdefault("source_index", idx)
        nodes.append(node)

    edges = [
        DiagramEdge(
            id=str(edge_raw["id"]),
            from_id=str(edge_raw["from_id"]),
            to_id=str(edge_raw["to_id"]),
            label=str(edge_raw.get("label", "")),
            role=str(edge_raw.get("role", "primary")),
            arrow_mode=str(edge_raw.get("arrow_mode", "straight")).lower(),
            metadata={**dict(edge_raw.get("metadata") or {}), "source_index": idx},
        )
        for idx, edge_raw in enumerate(raw.get("edges", []))
    ]

    groups = [
        DiagramGroup(
            id=str(group_raw["id"]),
            label=str(group_raw.get("label", "")),
            member_ids=[str(member_id) for member_id in group_raw.get("member_ids", [])],
            role=str(group_raw.get("role", "neutral")),
        )
        for group_raw in raw.get("groups", [])
    ]

    annotations = [
        DiagramAnnotation(
            id=str(annotation_raw["id"]),
            text=str(annotation_raw.get("text", "")),
            target_id=str(annotation_raw["target_id"]) if annotation_raw.get("target_id") else None,
            x=annotation_raw.get("x"),
            y=annotation_raw.get("y"),
            role=str(annotation_raw.get("role", "neutral")),
        )
        for annotation_raw in raw.get("annotations", [])
    ]

    layout_rules = {
        "direction": "horizontal",
        "gap_x": style.default_gap,
        "gap_y": style.default_gap,
        "origin_x": 100,
        "origin_y": 100,
        "grid_step": style.grid_step,
        "columns": None,
    }
    layout_rules.update(raw.get("layout_rules") or {})

    style_rules = style.to_style_rules()
    style_rules.update(raw.get("style_rules") or {})

    spec = DiagramSpec(
        diagram_type=_canonical_diagram_type(str(raw.get("diagram_type", "flowchart"))),
        style=style.name,
        canvas=canvas,
        nodes=nodes,
        edges=edges,
        groups=groups,
        annotations=annotations,
        layout_rules=layout_rules,
        style_rules=style_rules,
        output_format=_canonical_output_format(str(raw.get("output_format", ".excalidraw"))),
    )

    _apply_node_defaults(spec)
    _apply_layout_defaults(spec)
    return spec


def _apply_node_defaults(spec: DiagramSpec) -> None:
    font_size = spec.style_rules["body_size"]
    padding = spec.style_rules["padding"]

    for node in spec.nodes:
        text_width = engine.estimate_text_width(node.label, font_size)
        text_height = engine.estimate_text_height(node.label, font_size)
        min_width = text_width + padding * 2
        min_height = text_height + padding * 2

        if node.kind == "ellipse":
            min_width += padding * 2
            min_height += padding
        elif node.kind == "diamond":
            min_width += padding * 3
            min_height += padding * 2

        node.width = float(node.width or max(120, round(min_width)))
        node.height = float(node.height or max(56, round(min_height)))


def _snap(value: float, grid_step: int) -> float:
    if not grid_step:
        return float(value)
    return float(round(value / grid_step) * grid_step)


def _apply_layout_defaults(spec: DiagramSpec) -> None:
    if not spec.nodes:
        return

    grid_step = int(spec.layout_rules.get("grid_step") or spec.style_rules.get("grid_step") or 0)
    max_width = max(node.width or 0 for node in spec.nodes)
    max_height = max(node.height or 0 for node in spec.nodes)
    origin_x = float(spec.layout_rules.get("origin_x", 100))
    origin_y = float(spec.layout_rules.get("origin_y", 100))
    gap_x = float(spec.layout_rules.get("gap_x", spec.style_rules["default_gap"]))
    gap_y = float(spec.layout_rules.get("gap_y", spec.style_rules["default_gap"]))
    direction = str(spec.layout_rules.get("direction", "horizontal")).lower()
    columns = spec.layout_rules.get("columns")
    auto_index = 0

    for node in spec.nodes:
        if node.x is not None and node.y is not None:
            node.x = _snap(float(node.x), grid_step)
            node.y = _snap(float(node.y), grid_step)
            auto_index += 1
            continue

        if direction == "vertical":
            row = node.row if node.row is not None else auto_index
            column = node.column if node.column is not None else 0
        elif direction == "grid":
            resolved_columns = max(1, int(columns or 2))
            position = auto_index if node.row is None and node.column is None else None
            row = node.row if node.row is not None else (position // resolved_columns if position is not None else 0)
            column = node.column if node.column is not None else (position % resolved_columns if position is not None else 0)
        else:
            row = node.row if node.row is not None else 0
            column = node.column if node.column is not None else auto_index

        node.x = _snap(origin_x + column * (max_width + gap_x), grid_step)
        node.y = _snap(origin_y + row * (max_height + gap_y), grid_step)
        auto_index += 1


def validate_diagram_spec(spec: DiagramSpec) -> ValidationReport:
    issues: list[ValidationIssue] = []

    if spec.diagram_type not in ALLOWED_DIAGRAM_TYPES:
        issues.append(ValidationIssue(
            code="SPEC-DIAGRAM-TYPE",
            message=f"Unsupported diagram_type '{spec.diagram_type}'",
            repairable=False,
            target="diagram_type",
        ))

    if spec.output_format not in {".excalidraw", ".excalidraw.md"}:
        issues.append(ValidationIssue(
            code="SPEC-OUTPUT-FORMAT",
            message=f"Unsupported output_format '{spec.output_format}'",
            repairable=False,
            target="output_format",
        ))

    if not spec.nodes:
        issues.append(ValidationIssue(
            code="SPEC-NODES",
            message="DiagramSpec must contain at least one node",
            repairable=False,
            target="nodes",
        ))

    node_ids = set()
    for node in spec.nodes:
        if node.id in node_ids:
            issues.append(ValidationIssue(
                code="SPEC-DUPLICATE-NODE",
                message=f"Duplicate node id '{node.id}'",
                repairable=False,
                target=node.id,
            ))
        node_ids.add(node.id)

        if not node.label:
            issues.append(ValidationIssue(
                code="SPEC-NODE-LABEL",
                message=f"Node '{node.id}' is missing a label",
                repairable=False,
                target=node.id,
            ))
        if node.kind not in {"rectangle", "ellipse", "diamond"}:
            issues.append(ValidationIssue(
                code="SPEC-NODE-KIND",
                message=f"Node '{node.id}' uses unsupported kind '{node.kind}'",
                repairable=False,
                target=node.id,
            ))

    edge_ids = set()
    for edge in spec.edges:
        if edge.id in edge_ids:
            issues.append(ValidationIssue(
                code="SPEC-DUPLICATE-EDGE",
                message=f"Duplicate edge id '{edge.id}'",
                repairable=False,
                target=edge.id,
            ))
        edge_ids.add(edge.id)

        if edge.from_id not in node_ids or edge.to_id not in node_ids:
            issues.append(ValidationIssue(
                code="SPEC-EDGE-ENDPOINT",
                message=f"Edge '{edge.id}' references missing node(s)",
                repairable=False,
                target=edge.id,
            ))

        if edge.arrow_mode not in {"straight", "elbowed"}:
            issues.append(ValidationIssue(
                code="SPEC-ARROW-MODE",
                message=f"Edge '{edge.id}' uses unsupported arrow_mode '{edge.arrow_mode}'",
                repairable=False,
                target=edge.id,
            ))

    for group in spec.groups:
        for member_id in group.member_ids:
            if member_id not in node_ids:
                issues.append(ValidationIssue(
                    code="SPEC-GROUP-MEMBER",
                    message=f"Group '{group.id}' references missing node '{member_id}'",
                    repairable=False,
                    target=group.id,
                ))

    for annotation in spec.annotations:
        if annotation.target_id and annotation.target_id not in node_ids:
            issues.append(ValidationIssue(
                code="SPEC-ANNOTATION-TARGET",
                message=f"Annotation '{annotation.id}' references missing node '{annotation.target_id}'",
                repairable=False,
                target=annotation.id,
            ))

    status = "FAIL" if any(issue.severity == "ERROR" for issue in issues) else "PASS"
    return ValidationReport(status=status, issues=issues, summary=_summarize_issues(issues))


def _role_colors(style_rules: dict[str, Any], role: str) -> tuple[str, str]:
    role_colors = style_rules.get("role_colors") or {}
    pair = role_colors.get(role) or role_colors.get("primary") or {"fill": "transparent", "stroke": style_rules["border_color"]}
    return pair["fill"], pair["stroke"]


def render_diagram_spec(spec: DiagramSpec) -> list[dict[str, Any]]:
    elements: list[dict[str, Any]] = []
    stable_ids: dict[str, str] = {}
    shape_by_node: dict[str, dict[str, Any]] = {}

    for node in spec.nodes:
        fill, stroke = _role_colors(spec.style_rules, node.role)
        common_kwargs = {
            "fill": fill,
            "stroke": stroke,
            "sw": spec.style_rules["border_width"],
            "fs": spec.style_rules["body_size"],
            "label_color": spec.style_rules["text_color"],
            "roughness": spec.style_rules["roughness"],
            "font_family": spec.style_rules["font_family"],
            "fill_style": spec.style_rules["fill_style"],
        }

        if node.kind == "ellipse":
            built = engine.labeled_ellipse(
                node.x, node.y, node.width, node.height, node.label, **common_kwargs
            )
        elif node.kind == "diamond":
            built = engine.labeled_diamond(
                node.x, node.y, node.width, node.height, node.label, **common_kwargs
            )
        else:
            built = engine.labeled_rect(
                node.x,
                node.y,
                node.width,
                node.height,
                node.label,
                stroke_style=spec.style_rules["stroke_style"],
                border_radius=spec.style_rules["border_radius"],
                **common_kwargs,
            )

        shape, label = built
        shape.setdefault("customData", {}).update({"specId": node.id, "specRole": "node"})
        label.setdefault("customData", {}).update({"specId": node.id, "specRole": "node-label"})
        stable_ids[shape["id"]] = f"node:{node.id}"
        stable_ids[label["id"]] = f"node:{node.id}:label"
        shape_by_node[node.id] = shape
        elements.extend([shape, label])

    for edge in spec.edges:
        _fill, stroke = _role_colors(spec.style_rules, edge.role)
        arrow = engine.connect(
            shape_by_node[edge.from_id],
            shape_by_node[edge.to_id],
            stroke=stroke,
            sw=spec.style_rules["arrow_width"],
            roughness=spec.style_rules["roughness"],
            elbowed=edge.arrow_mode == "elbowed",
        )
        arrow.setdefault("customData", {}).update({"specId": edge.id, "specRole": "edge"})
        stable_ids[arrow["id"]] = f"edge:{edge.id}"
        elements.append(arrow)

        if edge.label:
            start = shape_by_node[edge.from_id]
            end = shape_by_node[edge.to_id]
            label_x = (start["x"] + start["width"] / 2 + end["x"] + end["width"] / 2) / 2
            label_y = (start["y"] + start["height"] / 2 + end["y"] + end["height"] / 2) / 2
            edge_label = engine.text_standalone(
                label_x,
                label_y,
                edge.label,
                fs=spec.style_rules["caption_size"],
                color=stroke,
                font_family=spec.style_rules["font_family"],
            )
            edge_label.setdefault("customData", {}).update({"specId": edge.id, "specRole": "edge-label"})
            stable_ids[edge_label["id"]] = f"edge:{edge.id}:label"
            elements.append(edge_label)

    for group in spec.groups:
        member_shapes = [shape_by_node[member_id] for member_id in group.member_ids if member_id in shape_by_node]
        if not member_shapes:
            continue
        min_x = min(el["x"] for el in member_shapes) - spec.style_rules["padding"]
        min_y = min(el["y"] for el in member_shapes) - spec.style_rules["padding"]
        max_x = max(el["x"] + el["width"] for el in member_shapes) + spec.style_rules["padding"]
        max_y = max(el["y"] + el["height"] for el in member_shapes) + spec.style_rules["padding"]
        _fill, stroke = _role_colors(spec.style_rules, group.role)
        frame = engine.frame(min_x, min_y, max_x - min_x, max_y - min_y, group.label or group.id, stroke=stroke, sw=spec.style_rules["border_width"])
        frame.setdefault("customData", {}).update({"specId": group.id, "specRole": "group"})
        stable_ids[frame["id"]] = f"group:{group.id}"
        elements.append(frame)

    for annotation in spec.annotations:
        _fill, stroke = _role_colors(spec.style_rules, annotation.role)
        if annotation.x is None or annotation.y is None:
            if annotation.target_id and annotation.target_id in shape_by_node:
                target = shape_by_node[annotation.target_id]
                x = target["x"] + target["width"] / 2
                y = target["y"] - spec.style_rules["default_gap"] / 2
            else:
                x = spec.layout_rules["origin_x"]
                y = spec.layout_rules["origin_y"]
        else:
            x = annotation.x
            y = annotation.y
        note = engine.text_standalone(
            x,
            y,
            annotation.text,
            fs=spec.style_rules["caption_size"],
            color=stroke,
            font_family=spec.style_rules["font_family"],
        )
        note.setdefault("customData", {}).update({"specId": annotation.id, "specRole": "annotation"})
        stable_ids[note["id"]] = f"annotation:{annotation.id}"
        elements.append(note)

    remapped, _ = remap_scene_references(
        elements,
        id_factory=lambda old_id, _element: stable_ids[old_id],
        deterministic=True,
    )
    return remapped


def _check_style_contract(elements: list[dict[str, Any]], spec: DiagramSpec) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    palette = set(spec.style_rules.get("palette") or [])
    font_family = spec.style_rules["font_family"]
    roughness = spec.style_rules["roughness"]
    border_width = spec.style_rules["border_width"]
    arrow_width = spec.style_rules["arrow_width"]
    border_radius = spec.style_rules["border_radius"]
    grid_step = int(spec.style_rules.get("grid_step") or 0)
    allowed_arrow_modes = set(spec.style_rules.get("allowed_arrow_modes") or ["straight"])

    for element in elements:
        el_type = element.get("type")
        el_id = element.get("id")

        if el_type == "text" and element.get("fontFamily") != font_family:
            issues.append(ValidationIssue(
                code="STYLE-FONT-FAMILY",
                message=f"{el_id} uses fontFamily {element.get('fontFamily')} (expected {font_family})",
                target=el_id,
            ))

        if el_type in {"rectangle", "ellipse", "diamond", "arrow", "line"} and element.get("roughness") != roughness:
            issues.append(ValidationIssue(
                code="STYLE-ROUGHNESS",
                message=f"{el_id} uses roughness {element.get('roughness')} (expected {roughness})",
                target=el_id,
            ))

        if el_type in {"rectangle", "ellipse", "diamond", "frame"} and element.get("strokeWidth") != border_width:
            issues.append(ValidationIssue(
                code="STYLE-BORDER-WIDTH",
                message=f"{el_id} uses strokeWidth {element.get('strokeWidth')} (expected {border_width})",
                target=el_id,
            ))

        if el_type in {"arrow", "line"} and element.get("strokeWidth") != arrow_width:
            issues.append(ValidationIssue(
                code="STYLE-ARROW-WIDTH",
                message=f"{el_id} uses strokeWidth {element.get('strokeWidth')} (expected {arrow_width})",
                target=el_id,
            ))

        if el_type == "rectangle":
            has_roundness = element.get("roundness") is not None
            if has_roundness != border_radius:
                issues.append(ValidationIssue(
                    code="STYLE-BORDER-RADIUS",
                    message=f"{el_id} border_radius mismatch",
                    target=el_id,
                ))

        if el_type == "arrow":
            mode = "elbowed" if element.get("elbowed") else "straight"
            if mode not in allowed_arrow_modes:
                issues.append(ValidationIssue(
                    code="STYLE-ARROW-MODE",
                    message=f"{el_id} uses arrow mode '{mode}'",
                    target=el_id,
                ))

        for color_key in ("strokeColor", "backgroundColor"):
            color = element.get(color_key)
            if color and palette and color not in palette:
                issues.append(ValidationIssue(
                    code="STYLE-PALETTE",
                    message=f"{el_id} uses {color_key}={color}, outside style palette",
                    target=el_id,
                ))

        if grid_step and el_type in {"rectangle", "ellipse", "diamond", "frame"}:
            x = float(element.get("x", 0))
            y = float(element.get("y", 0))
            if x % grid_step != 0 or y % grid_step != 0:
                issues.append(ValidationIssue(
                    code="STYLE-GRID",
                    message=f"{el_id} is off the {grid_step}px grid",
                    target=el_id,
                ))

    return issues


def _check_scene_topology(elements: list[dict[str, Any]], spec: DiagramSpec) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    id_to_element = {element.get("id"): element for element in elements}

    for node in spec.nodes:
        if f"node:{node.id}" not in id_to_element:
            issues.append(ValidationIssue(
                code="TOPOLOGY-NODE",
                message=f"Missing rendered node for '{node.id}'",
                repairable=False,
                target=node.id,
            ))

    for edge in spec.edges:
        arrow = id_to_element.get(f"edge:{edge.id}")
        if not arrow:
            issues.append(ValidationIssue(
                code="TOPOLOGY-EDGE",
                message=f"Missing rendered edge for '{edge.id}'",
                repairable=False,
                target=edge.id,
            ))
            continue

        start_binding = arrow.get("startBinding") or {}
        end_binding = arrow.get("endBinding") or {}
        if start_binding.get("elementId") != f"node:{edge.from_id}" or end_binding.get("elementId") != f"node:{edge.to_id}":
            issues.append(ValidationIssue(
                code="TOPOLOGY-BINDING",
                message=f"Edge '{edge.id}' is bound to the wrong nodes",
                target=edge.id,
            ))

        if edge.label and f"edge:{edge.id}:label" not in id_to_element:
            issues.append(ValidationIssue(
                code="TOPOLOGY-EDGE-LABEL",
                message=f"Missing label for edge '{edge.id}'",
                target=edge.id,
            ))

    return issues


def _check_canvas_bounds(elements: list[dict[str, Any]], spec: DiagramSpec) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    if spec.canvas.width is None or spec.canvas.height is None:
        return issues

    for element in elements:
        x = float(element.get("x", 0))
        y = float(element.get("y", 0))
        width = float(element.get("width", 0))
        height = float(element.get("height", 0))
        if x < 0 or y < 0 or x + width > spec.canvas.width or y + height > spec.canvas.height:
            issues.append(ValidationIssue(
                code="LAYOUT-CANVAS-BOUNDS",
                message=f"{element.get('id')} exceeds the configured canvas",
                target=element.get("id"),
            ))

    return issues


def validate_scene_contract(elements: list[dict[str, Any]], spec: DiagramSpec) -> ValidationReport:
    issues: list[ValidationIssue] = []

    layout_report = engine.verify_layout(elements, style_params=spec.style_rules)
    issues.extend(
        ValidationIssue(
            code="LAYOUT-OVERLAP" if issue.get("severity") == "ERROR" else "LAYOUT-WARNING",
            message=f"{issue.get('a_label')} overlaps {issue.get('b_label')}",
            severity=issue.get("severity", "ERROR"),
            target=issue.get("a_id"),
        )
        for issue in layout_report.get("overlaps", [])
    )
    issues.extend(
        ValidationIssue(
            code=f"LAYOUT-{issue.get('issue', 'ARROW').upper()}",
            message=issue.get("detail", "Arrow binding issue"),
            severity=issue.get("severity", "ERROR"),
            target=issue.get("arrow_id"),
        )
        for issue in layout_report.get("arrow_issues", [])
    )
    issues.extend(
        ValidationIssue(
            code="LAYOUT-SPACING",
            message=f"{issue.get('a_id')} to {issue.get('b_id')} gap {issue.get('gap')} deviates from median {issue.get('median_gap')}",
            severity=issue.get("severity", "ERROR"),
            target=issue.get("a_id"),
        )
        for issue in layout_report.get("spacing_issues", [])
    )

    issues.extend(_check_style_contract(elements, spec))
    issues.extend(_check_scene_topology(elements, spec))
    issues.extend(_check_canvas_bounds(elements, spec))

    status = _issue_status(issues)
    return ValidationReport(status=status, issues=issues, summary=_summarize_issues(issues))


def repair_scene(elements: list[dict[str, Any]], spec: DiagramSpec, _report: ValidationReport | None = None) -> list[dict[str, Any]]:
    """Mechanical repairs are handled by deterministic re-render from the spec."""
    return render_diagram_spec(spec)


def generate_diagram(
    spec_input: DiagramSpec | dict[str, Any],
    *,
    auto_repair: bool = True,
    max_repair_attempts: int = 1,
) -> PipelineResult:
    raw_input = diagram_spec_to_dict(spec_input) if isinstance(spec_input, DiagramSpec) else json.loads(json.dumps(spec_input))
    spec = normalize_diagram_spec(spec_input)
    spec_report = validate_diagram_spec(spec)
    result = PipelineResult(input_spec=raw_input, spec=spec, spec_report=spec_report)

    if spec_report.status == "FAIL":
        return result

    elements = render_diagram_spec(spec)
    scene_report = validate_scene_contract(elements, spec)
    repaired = False
    attempts = 0

    while auto_repair and scene_report.status == "REPAIRABLE" and attempts < max_repair_attempts:
        elements = repair_scene(elements, spec, scene_report)
        scene_report = validate_scene_contract(elements, spec)
        repaired = True
        attempts += 1

    result.elements = elements
    result.scene_report = scene_report
    result.repaired = repaired
    return result


def save_generated_diagram(
    filepath: str,
    result: PipelineResult,
    *,
    artifact_dir: str | None = None,
) -> None:
    if result.final_status != "PASS":
        raise ValueError(f"Refusing to save diagram with status {result.final_status}")

    engine.save(filepath, result.elements, bg=result.spec.canvas.background or "#ffffff")

    if artifact_dir:
        os.makedirs(artifact_dir, exist_ok=True)
        with open(os.path.join(artifact_dir, "input_spec.json"), "w", encoding="utf-8") as f:
            json.dump(result.input_spec, f, ensure_ascii=False, indent=2)
        with open(os.path.join(artifact_dir, "diagram_spec.json"), "w", encoding="utf-8") as f:
            json.dump(diagram_spec_to_dict(result.spec), f, ensure_ascii=False, indent=2)
        with open(os.path.join(artifact_dir, "validation_report.json"), "w", encoding="utf-8") as f:
            json.dump(result.to_dict(), f, ensure_ascii=False, indent=2)
