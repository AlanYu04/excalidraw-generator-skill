"""
Hand-drawn Bar Chart Builder for Excalidraw

Generates bar chart diagrams using existing engine primitives.
Supports CJK text labels, custom colors, value annotations, and grid lines.
"""

from typing import Any, Dict, List, Optional, Tuple, Union

from . import engine


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
