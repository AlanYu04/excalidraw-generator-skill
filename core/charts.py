"""
Hand-drawn Bar Chart Builder for Excalidraw

Generates bar chart diagrams using existing engine primitives.
Supports CJK text labels, custom colors, value annotations, and grid lines.
"""

from typing import Any, Dict, List, Optional, Tuple, Union

import math

from . import engine
from .svg_converter import svg_to_elements


def bar_chart(
    x: float,
    y: float,
    data: Dict[str, Union[int, float]],
    title: Optional[str] = None,
    bar_color: str = "#a5d8ff",
    bar_colors: Optional[Dict[str, str]] = None,
    axis_color: str = "#495057",
    bar_width: int = 60,
    max_height: int = 200,
    gap: int = 30,
    fs: int = 14,
    label_fs: Optional[int] = None,
    value_fs: Optional[int] = None,
    title_fs: Optional[int] = None,
    roughness: int = 1,
    font_family: int = 3,
    stroke_width: int = 2,
    show_values: bool = True,
    show_grid: bool = False,
    grid_color: str = "#dee2e6",
    grid_lines: int = 5,
    axis_label: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """Generate a hand-drawn bar chart as Excalidraw elements.

    Args:
        x: Top-left X coordinate of the chart area.
        y: Top-left Y coordinate of the chart area.
        data: Dict mapping category labels to numeric values.
        title: Optional chart title displayed above.
        bar_color: Default fill color for bars.
        bar_colors: Optional per-category color overrides {label: color}.
        axis_color: Color for axes and tick marks.
        bar_width: Width of each bar in pixels.
        max_height: Maximum bar height in pixels.
        gap: Horizontal gap between bars.
        fs: Base font size for labels.
        label_fs: Font size for category labels (defaults to fs).
        value_fs: Font size for value labels (defaults to fs - 2).
        title_fs: Font size for title (defaults to fs + 8).
        roughness: Excalidraw roughness level.
        font_family: Excalidraw font family (1=Virgil, 2=Helvetica, 3=Cascadia).
        stroke_width: Stroke width for bars and axes.
        show_values: Show numeric value above each bar.
        show_grid: Show horizontal grid lines.
        grid_color: Color for grid lines.
        grid_lines: Number of grid lines.
        axis_label: Optional Y-axis label text.

    Returns:
        List of Excalidraw element dicts.
    """
    if not data:
        return []

    label_fs = label_fs or fs
    value_fs = value_fs or max(fs - 2, 10)
    title_fs = title_fs or (fs + 8)

    categories = list(data.keys())
    values = list(data.values())
    max_val = max(values) if values else 1
    if max_val == 0:
        max_val = 1

    elements: List[Dict[str, Any]] = []

    # Layout calculations
    n = len(categories)
    chart_width = n * bar_width + (n - 1) * gap
    axis_y = y + max_height
    axis_x_start = x
    axis_x_end = x + chart_width
    left_margin = 40  # Space for Y-axis tick labels
    top_margin = 10

    # Offset everything by left_margin for tick labels
    chart_x = x + left_margin
    axis_x_start = chart_x
    axis_x_end = chart_x + chart_width

    # --- Title ---
    title_y = y - 10
    if title:
        tw = engine.estimate_text_width(title, title_fs)
        title_el = engine.text_standalone(
            chart_x + chart_width / 2, title_y - title_fs,
            title, fs=title_fs, color="#1e1e1e", font_family=font_family,
        )
        elements.append(title_el)

    # --- Grid lines ---
    if show_grid:
        for i in range(1, grid_lines + 1):
            gy = axis_y - (max_height * i / (grid_lines + 1))
            elements.append(
                engine.line(
                    axis_x_start, gy, chart_width, 0,
                    stroke=grid_color, sw=1, roughness=0,
                )
            )
            # Tick value
            tick_val = max_val * i / (grid_lines + 1)
            tick_label = f"{tick_val:.0f}" if tick_val == int(tick_val) else f"{tick_val:.1f}"
            elements.append(
                engine.text_standalone(
                    axis_x_start - 5, gy,
                    tick_label, fs=value_fs, color="#868e96",
                    font_family=font_family,
                )
            )

    # --- Y-axis ---
    elements.append(
        engine.line(
            axis_x_start, y + top_margin, 0, max_height - top_margin,
            stroke=axis_color, sw=stroke_width, roughness=roughness,
        )
    )

    # --- X-axis ---
    elements.append(
        engine.line(
            axis_x_start, axis_y, chart_width, 0,
            stroke=axis_color, sw=stroke_width, roughness=roughness,
        )
    )

    # --- Y-axis label ---
    if axis_label:
        elements.append(
            engine.text_standalone(
                x, y + max_height / 2,
                axis_label, fs=label_fs, color="#868e96",
                font_family=font_family,
            )
        )

    # --- Bars ---
    for i, (cat, val) in enumerate(data.items()):
        bar_x = axis_x_start + i * (bar_width + gap)
        bar_h = (val / max_val) * max_height
        bar_y = axis_y - bar_h

        color = bar_color
        if bar_colors and cat in bar_colors:
            color = bar_colors[cat]

        # Bar rectangle
        elements.append(
            engine.rect(
                bar_x, bar_y, bar_width, bar_h,
                fill=color, stroke=axis_color,
                sw=stroke_width, roughness=roughness,
            )
        )

        # Category label below x-axis
        label_cx = bar_x + bar_width / 2
        label_cy = axis_y + label_fs + 5
        elements.append(
            engine.text_standalone(
                label_cx, label_cy,
                cat, fs=label_fs, color="#495057",
                font_family=font_family,
            )
        )

        # Value label above bar
        if show_values:
            val_text = f"{val:.0f}" if val == int(val) else f"{val:.1f}"
            val_cx = bar_x + bar_width / 2
            val_cy = bar_y - value_fs / 2 - 3
            elements.append(
                engine.text_standalone(
                    val_cx, val_cy,
                    val_text, fs=value_fs, color="#495057",
                    font_family=font_family,
                )
            )

    return elements


def horizontal_bar_chart(
    x: float,
    y: float,
    data: Dict[str, Union[int, float]],
    title: Optional[str] = None,
    bar_color: str = "#a5d8ff",
    bar_colors: Optional[Dict[str, str]] = None,
    axis_color: str = "#495057",
    bar_height: int = 40,
    max_width: int = 250,
    gap: int = 15,
    fs: int = 14,
    label_fs: Optional[int] = None,
    value_fs: Optional[int] = None,
    title_fs: Optional[int] = None,
    roughness: int = 1,
    font_family: int = 3,
    stroke_width: int = 2,
    show_values: bool = True,
) -> List[Dict[str, Any]]:
    """Generate a horizontal bar chart as Excalidraw elements.

    Args:
        x: Top-left X coordinate.
        y: Top-left Y coordinate.
        data: Dict mapping category labels to numeric values.
        title: Optional chart title.
        bar_color: Default fill color.
        bar_colors: Per-category color overrides.
        axis_color: Color for axis lines.
        bar_height: Height of each bar.
        max_width: Maximum bar width.
        gap: Vertical gap between bars.
        fs: Base font size.
        roughness: Excalidraw roughness level.
        font_family: Font family ID.
        stroke_width: Stroke width.
        show_values: Show numeric value at end of each bar.

    Returns:
        List of Excalidraw element dicts.
    """
    if not data:
        return []

    label_fs = label_fs or fs
    value_fs = value_fs or max(fs - 2, 10)
    title_fs = title_fs or (fs + 8)

    categories = list(data.keys())
    values = list(data.values())
    max_val = max(values) if values else 1
    if max_val == 0:
        max_val = 1

    elements: List[Dict[str, Any]] = []
    n = len(categories)
    chart_height = n * bar_height + (n - 1) * gap
    label_margin = 80  # Space for category labels on the left

    # Title
    if title:
        elements.append(
            engine.text_standalone(
                x + label_margin + max_width / 2, y - title_fs,
                title, fs=title_fs, color="#1e1e1e", font_family=font_family,
            )
        )

    # Y-axis
    axis_x = x + label_margin
    elements.append(
        engine.line(
            axis_x, y, 0, chart_height,
            stroke=axis_color, sw=stroke_width, roughness=roughness,
        )
    )

    # Bars
    for i, (cat, val) in enumerate(data.items()):
        bar_y = y + i * (bar_height + gap)
        bar_w = (val / max_val) * max_width

        color = bar_color
        if bar_colors and cat in bar_colors:
            color = bar_colors[cat]

        # Bar
        elements.append(
            engine.rect(
                axis_x, bar_y, bar_w, bar_height,
                fill=color, stroke=axis_color,
                sw=stroke_width, roughness=roughness,
            )
        )

        # Category label on the left
        elements.append(
            engine.text_standalone(
                axis_x - 10, bar_y + bar_height / 2,
                cat, fs=label_fs, color="#495057",
                font_family=font_family,
            )
        )

        # Value at end of bar
        if show_values:
            val_text = f"{val:.0f}" if val == int(val) else f"{val:.1f}"
            elements.append(
                engine.text_standalone(
                    axis_x + bar_w + value_fs, bar_y + bar_height / 2,
                    val_text, fs=value_fs, color="#495057",
                    font_family=font_family,
                )
            )

    return elements


def line_chart(
    x: float,
    y: float,
    data: Dict[str, List[Union[int, float]]],
    labels: List[str],
    title: Optional[str] = None,
    series_colors: Optional[Dict[str, str]] = None,
    default_color: str = "#1971c2",
    axis_color: str = "#495057",
    chart_width: int = 400,
    chart_height: int = 200,
    fs: int = 14,
    label_fs: Optional[int] = None,
    value_fs: Optional[int] = None,
    title_fs: Optional[int] = None,
    roughness: int = 1,
    font_family: int = 3,
    stroke_width: int = 2,
    show_points: bool = True,
    show_values: bool = False,
    show_grid: bool = False,
    grid_color: str = "#dee2e6",
    grid_lines: int = 5,
    show_legend: bool = True,
) -> List[Dict[str, Any]]:
    """Generate a hand-drawn line chart as Excalidraw elements.

    Args:
        x: Top-left X coordinate of the chart area.
        y: Top-left Y coordinate of the chart area.
        data: Dict mapping series names to lists of numeric values.
        labels: List of x-axis labels (one per data point).
        title: Optional chart title displayed above.
        series_colors: Optional per-series color overrides {name: color}.
        default_color: Default line/point color.
        axis_color: Color for axes.
        chart_width: Width of the chart area in pixels.
        chart_height: Height of the chart area in pixels.
        fs: Base font size.
        label_fs: Font size for x-axis labels (defaults to fs).
        value_fs: Font size for value annotations (defaults to max(fs-2, 10)).
        title_fs: Font size for title (defaults to fs + 8).
        roughness: Excalidraw roughness level.
        font_family: Excalidraw font family (1=Virgil, 2=Helvetica, 3=Cascadia).
        stroke_width: Stroke width for lines and axes.
        show_points: Show dot markers at data points.
        show_values: Show numeric value at each point.
        show_grid: Show horizontal grid lines.
        grid_color: Color for grid lines.
        grid_lines: Number of grid lines.
        show_legend: Show series legend below chart.

    Returns:
        List of Excalidraw element dicts.
    """
    if not data:
        return []

    label_fs = label_fs or fs
    value_fs = value_fs or max(fs - 2, 10)
    title_fs = title_fs or (fs + 8)

    # Compute max value across all series, guard against 0
    max_val = max(max(vals) for vals in data.values())
    if max_val == 0:
        max_val = 1

    # X spacing between data points
    step_x = chart_width / max(len(labels) - 1, 1)

    elements: List[Dict[str, Any]] = []

    # Chart origin (bottom-left of plot area)
    origin_x = x
    origin_y = y + chart_height

    # --- Title ---
    if title:
        elements.append(
            engine.text_standalone(
                x + chart_width / 2, y - title_fs,
                title, fs=title_fs, color="#1e1e1e",
                font_family=font_family,
            )
        )

    # --- Grid lines ---
    if show_grid:
        for i in range(1, grid_lines + 1):
            gy = origin_y - (chart_height * i / (grid_lines + 1))
            elements.append(
                engine.line(
                    origin_x, gy, chart_width, 0,
                    stroke=grid_color, sw=1, roughness=0,
                )
            )
            # Tick value
            tick_val = max_val * i / (grid_lines + 1)
            tick_label = f"{tick_val:.0f}" if tick_val == int(tick_val) else f"{tick_val:.1f}"
            elements.append(
                engine.text_standalone(
                    origin_x - 5, gy,
                    tick_label, fs=value_fs, color="#868e96",
                    font_family=font_family,
                )
            )

    # --- Y-axis ---
    elements.append(
        engine.line(
            origin_x, y, 0, chart_height,
            stroke=axis_color, sw=stroke_width, roughness=roughness,
        )
    )

    # --- X-axis ---
    elements.append(
        engine.line(
            origin_x, origin_y, chart_width, 0,
            stroke=axis_color, sw=stroke_width, roughness=roughness,
        )
    )

    # --- Data series ---
    for series_name, values in data.items():
        color = default_color
        if series_colors and series_name in series_colors:
            color = series_colors[series_name]

        # Compute point positions
        points: List[Tuple[float, float]] = []
        for j, val in enumerate(values):
            px = origin_x + j * step_x
            py = origin_y - (val / max_val) * chart_height
            points.append((px, py))

        # Connect points with line segments
        for j in range(len(points) - 1):
            x1, y1 = points[j]
            x2, y2 = points[j + 1]
            elements.append(
                engine.line(
                    x1, y1, x2 - x1, y2 - y1,
                    stroke=color, sw=stroke_width, roughness=roughness,
                )
            )

        # Point markers
        if show_points:
            for px, py in points:
                dot_size = 8
                elements.append(
                    engine.ellipse(
                        px - dot_size / 2, py - dot_size / 2,
                        dot_size, dot_size,
                        fill=color, stroke=color,
                        sw=1, roughness=roughness,
                    )
                )

        # Value annotations
        if show_values:
            for j, val in enumerate(values):
                px, py = points[j]
                val_text = f"{val:.0f}" if val == int(val) else f"{val:.1f}"
                elements.append(
                    engine.text_standalone(
                        px, py - value_fs,
                        val_text, fs=value_fs, color="#495057",
                        font_family=font_family,
                    )
                )

    # --- X-axis labels ---
    for j, label in enumerate(labels):
        lx = origin_x + j * step_x
        ly = origin_y + label_fs + 5
        elements.append(
            engine.text_standalone(
                lx, ly, label,
                fs=label_fs, color="#495057",
                font_family=font_family,
            )
        )

    # --- Legend ---
    if show_legend:
        legend_y = origin_y + label_fs + 30
        legend_x = origin_x
        for series_name in data:
            color = default_color
            if series_colors and series_name in series_colors:
                color = series_colors[series_name]

            # Short colored line segment
            elements.append(
                engine.line(
                    legend_x, legend_y, 20, 0,
                    stroke=color, sw=stroke_width, roughness=roughness,
                )
            )
            # Series name text
            elements.append(
                engine.text_standalone(
                    legend_x + 28, legend_y,
                    series_name, fs=label_fs, color="#495057",
                    font_family=font_family,
                )
            )
            # Move to next legend entry
            name_width = engine.estimate_text_width(series_name, label_fs)
            legend_x += 28 + name_width + 20

    return elements


def _wedge_svg(
    cx: float,
    cy: float,
    r: float,
    start_angle: float,
    end_angle: float,
    fill: str,
    stroke: str = "#495057",
    stroke_width: int = 2,
) -> str:
    """Generate an SVG string for a single pie wedge."""
    x1 = cx + r * math.cos(start_angle)
    y1 = cy + r * math.sin(start_angle)
    x2 = cx + r * math.cos(end_angle)
    y2 = cy + r * math.sin(end_angle)
    large_arc = 1 if (end_angle - start_angle) > math.pi else 0
    d = (
        f"M{cx},{cy} L{x1:.1f},{y1:.1f} "
        f"A{r},{r} 0 {large_arc},1 {x2:.1f},{y2:.1f} Z"
    )
    return (
        f'<svg viewBox="0 0 {2 * r:.0f} {2 * r:.0f}">'
        f'<path d="{d}" fill="{fill}" stroke="{stroke}" '
        f'stroke-width="{stroke_width}"/></svg>'
    )


def pie_chart(
    x: float,
    y: float,
    data: Dict[str, Union[int, float]],
    title: Optional[str] = None,
    slice_colors: Optional[Dict[str, str]] = None,
    default_colors: Optional[List[str]] = None,
    axis_color: str = "#495057",
    radius: int = 100,
    fs: int = 14,
    roughness: int = 1,
    font_family: int = 3,
    stroke_width: int = 2,
    show_labels: bool = True,
    show_percentages: bool = True,
    show_legend: bool = True,
    donut: bool = False,
    donut_radius: int = 50,
) -> List[Dict[str, Any]]:
    """Generate a hand-drawn pie chart as Excalidraw elements.

    Args:
        x: X coordinate of the pie chart top-left corner.
        y: Y coordinate of the pie chart top-left corner.
        data: Dict mapping slice names to numeric values.
        title: Optional chart title displayed above.
        slice_colors: Optional per-slice color overrides {name: color}.
        default_colors: Color palette (cycled through if fewer colors than slices).
        axis_color: Color for wedge strokes.
        radius: Pie radius in pixels.
        fs: Base font size.
        roughness: Excalidraw roughness level.
        font_family: Excalidraw font family (1=Virgil, 2=Helvetica, 3=Cascadia).
        stroke_width: Stroke width for wedge outlines.
        show_labels: Show slice name labels around the pie.
        show_percentages: Show percentage labels around the pie.
        show_legend: Show a color-coded legend below the pie.
        donut: Cut out a centre hole to create a donut chart.
        donut_radius: Radius of the centre hole when donut=True.

    Returns:
        List of Excalidraw element dicts.
    """
    if not data:
        return []

    if default_colors is None:
        default_colors = [
            "#a5d8ff", "#b2f2bb", "#ffd8a8",
            "#fcc2d7", "#d0bfff", "#99e9f2", "#fff3bf",
        ]

    total = sum(data.values())
    if total == 0:
        return []

    elements: List[Dict[str, Any]] = []
    title_fs = fs + 8

    # Centre of the pie in output coordinates
    cx = x + radius
    cy = y + radius

    # --- Title ---
    if title:
        elements.append(
            engine.text_standalone(
                cx, y - title_fs - 10,
                title, fs=title_fs, color="#1e1e1e",
                font_family=font_family,
            )
        )

    # --- Wedges ---
    start_angle = -math.pi / 2  # 12 o'clock
    slice_info: List[Tuple[str, float, float, str]] = []  # (name, start, end, color)

    for i, (name, value) in enumerate(data.items()):
        sweep = (value / total) * 2 * math.pi
        end_angle = start_angle + sweep

        color = slice_colors.get(name, default_colors[i % len(default_colors)]) if slice_colors else default_colors[i % len(default_colors)]

        svg_str = _wedge_svg(
            radius, radius, radius,
            start_angle, end_angle,
            color, axis_color, stroke_width,
        )
        wedge_els = svg_to_elements(
            svg_str, x=x, y=y, scale=1.0,
            stroke=axis_color, stroke_width=stroke_width,
            roughness=roughness,
        )
        elements.extend(wedge_els)
        slice_info.append((name, start_angle, end_angle, color))
        start_angle = end_angle

    # --- Labels & Percentages ---
    for name, sa, ea, _color in slice_info:
        mid = (sa + ea) / 2
        label_r = radius + 20

        if show_labels:
            lx = cx + label_r * math.cos(mid) + 20 * math.cos(mid)
            ly = cy + label_r * math.sin(mid) + 20 * math.sin(mid)
            elements.append(
                engine.text_standalone(
                    lx, ly, name,
                    fs=fs, color="#495057",
                    font_family=font_family,
                )
            )

        if show_percentages:
            pct = ((ea - sa) / (2 * math.pi)) * 100
            pct_text = f"{pct:.1f}%"
            px = cx + (label_r + 10) * math.cos(mid)
            py = cy + (label_r + 10) * math.sin(mid) + fs + 4
            elements.append(
                engine.text_standalone(
                    px, py, pct_text,
                    fs=max(fs - 2, 10), color="#868e96",
                    font_family=font_family,
                )
            )

    # --- Donut hole ---
    if donut:
        elements.append(
            engine.ellipse(
                cx - donut_radius, cy - donut_radius,
                donut_radius * 2, donut_radius * 2,
                fill="#ffffff", stroke="#ffffff",
                sw=0, roughness=0,
            )
        )

    # --- Legend ---
    if show_legend:
        legend_y = y + 2 * radius + 30
        legend_x = x
        for i, (name, _sa, _ea, color) in enumerate(slice_info):
            elements.append(
                engine.rect(
                    legend_x, legend_y, 16, 16,
                    fill=color, stroke=axis_color,
                    sw=1, roughness=roughness,
                )
            )
            elements.append(
                engine.text_standalone(
                    legend_x + 22, legend_y,
                    name, fs=fs, color="#495057",
                    font_family=font_family,
                )
            )
            name_width = engine.estimate_text_width(name, fs)
            legend_x += 22 + name_width + 16

    return elements
