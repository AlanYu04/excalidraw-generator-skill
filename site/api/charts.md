---
title: Charts
---

# Charts

Generate hand-drawn bar, horizontal bar, line, and pie charts as native Excalidraw elements. All chart functions return a flat list of Excalidraw element dictionaries.

## Bar Chart

### `bar_chart`

```python
from core.charts import bar_chart

elements = bar_chart(
    x=50, y=100,
    data={"React": 85, "Vue": 72, "Angular": 58},
    title="Framework Popularity",
    bar_color="#a5d8ff",
    show_values=True,
    show_grid=True,
    font_family=3,
)
```

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `x` | `float` | required | Top-left X coordinate |
| `y` | `float` | required | Top-left Y coordinate |
| `data` | `dict[str, int\|float]` | required | Category labels to numeric values |
| `title` | `str \| None` | `None` | Chart title displayed above |
| `bar_color` | `str` | `"#a5d8ff"` | Default fill color for bars |
| `bar_colors` | `dict[str, str] \| None` | `None` | Per-category color overrides |
| `axis_color` | `str` | `"#495057"` | Color for axes and tick marks |
| `bar_width` | `int` | `60` | Width of each bar in pixels |
| `max_height` | `int` | `200` | Maximum bar height in pixels |
| `gap` | `int` | `30` | Horizontal gap between bars |
| `fs` | `int` | `14` | Base font size |
| `label_fs` | `int \| None` | `None` | Font size for category labels (defaults to `fs`) |
| `value_fs` | `int \| None` | `None` | Font size for value labels (defaults to `fs - 2`) |
| `title_fs` | `int \| None` | `None` | Font size for title (defaults to `fs + 8`) |
| `roughness` | `int` | `1` | Excalidraw roughness level |
| `font_family` | `int` | `3` | Font family (1=Virgil, 2=Helvetica, 3=Cascadia) |
| `stroke_width` | `int` | `2` | Stroke width for bars and axes |
| `show_values` | `bool` | `True` | Show numeric value above each bar |
| `show_grid` | `bool` | `False` | Show horizontal grid lines |
| `grid_color` | `str` | `"#dee2e6"` | Color for grid lines |
| `grid_lines` | `int` | `5` | Number of grid lines |
| `axis_label` | `str \| None` | `None` | Optional Y-axis label text |

### Per-Category Colors

```python
from core.charts import bar_chart

elements = bar_chart(
    x=50, y=100,
    data={"Training": 120, "Inference": 85, "Eval": 45},
    title="Time Breakdown (s)",
    bar_colors={
        "Training": "#a5d8ff",
        "Inference": "#b2f2bb",
        "Eval": "#ffd8a8",
    },
    show_values=True,
    show_grid=True,
)
```

## Horizontal Bar Chart

### `horizontal_bar_chart`

```python
from core.charts import horizontal_bar_chart

elements = horizontal_bar_chart(
    x=50, y=50,
    data={"Training": 120, "Inference": 85, "Eval": 45},
    title="Time Breakdown (min)",
    bar_colors={"Training": "#a5d8ff", "Inference": "#b2f2bb", "Eval": "#ffd8a8"},
)
```

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `x` | `float` | required | Top-left X coordinate |
| `y` | `float` | required | Top-left Y coordinate |
| `data` | `dict[str, int\|float]` | required | Category labels to numeric values |
| `title` | `str \| None` | `None` | Chart title |
| `bar_color` | `str` | `"#a5d8ff"` | Default fill color |
| `bar_colors` | `dict[str, str] \| None` | `None` | Per-category color overrides |
| `axis_color` | `str` | `"#495057"` | Color for axis lines |
| `bar_height` | `int` | `40` | Height of each bar |
| `max_width` | `int` | `250` | Maximum bar width |
| `gap` | `int` | `15` | Vertical gap between bars |
| `fs` | `int` | `14` | Base font size |
| `label_fs` | `int \| None` | `None` | Font size for category labels |
| `value_fs` | `int \| None` | `None` | Font size for value labels |
| `title_fs` | `int \| None` | `None` | Font size for title |
| `roughness` | `int` | `1` | Excalidraw roughness level |
| `font_family` | `int` | `3` | Font family |
| `stroke_width` | `int` | `2` | Stroke width |
| `show_values` | `bool` | `True` | Show numeric value at end of each bar |

## Line Chart

### `line_chart`

Supports multi-series plotting with optional legend, point markers, and grid lines.

```python
from core.charts import line_chart

elements = line_chart(
    x=50, y=50,
    data={
        "Revenue": [10, 25, 35, 50, 70],
        "Costs":   [8, 15, 20, 30, 35],
    },
    labels=["Q1", "Q2", "Q3", "Q4", "Q5"],
    title="Revenue vs Costs",
    series_colors={"Revenue": "#1971c2", "Costs": "#e03131"},
    show_points=True,
    show_legend=True,
)
```

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `x` | `float` | required | Top-left X coordinate |
| `y` | `float` | required | Top-left Y coordinate |
| `data` | `dict[str, list[int\|float]]` | required | Series names to value lists |
| `labels` | `list[str]` | required | X-axis labels (one per data point) |
| `title` | `str \| None` | `None` | Chart title displayed above |
| `series_colors` | `dict[str, str] \| None` | `None` | Per-series color overrides |
| `default_color` | `str` | `"#1971c2"` | Default line/point color |
| `axis_color` | `str` | `"#495057"` | Color for axes |
| `chart_width` | `int` | `400` | Width of the chart area in pixels |
| `chart_height` | `int` | `200` | Height of the chart area in pixels |
| `fs` | `int` | `14` | Base font size |
| `label_fs` | `int \| None` | `None` | Font size for x-axis labels |
| `value_fs` | `int \| None` | `None` | Font size for value annotations |
| `title_fs` | `int \| None` | `None` | Font size for title |
| `roughness` | `int` | `1` | Excalidraw roughness level |
| `font_family` | `int` | `3` | Font family |
| `stroke_width` | `int` | `2` | Stroke width for lines and axes |
| `show_points` | `bool` | `True` | Show dot markers at data points |
| `show_values` | `bool` | `False` | Show numeric value at each point |
| `show_grid` | `bool` | `False` | Show horizontal grid lines |
| `grid_color` | `str` | `"#dee2e6"` | Color for grid lines |
| `grid_lines` | `int` | `5` | Number of grid lines |
| `show_legend` | `bool` | `True` | Show series legend below chart |

## Pie Chart

### `pie_chart`

Supports standard pie and donut modes with percentage labels and color-coded legend.

```python
from core.charts import pie_chart

elements = pie_chart(
    x=100, y=100,
    data={"Mobile": 45, "Desktop": 35, "Tablet": 20},
    title="Traffic by Device",
    donut=True,
    donut_radius=50,
    show_percentages=True,
)
```

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `x` | `float` | required | X coordinate of the chart top-left |
| `y` | `float` | required | Y coordinate of the chart top-left |
| `data` | `dict[str, int\|float]` | required | Slice names to numeric values |
| `title` | `str \| None` | `None` | Chart title displayed above |
| `slice_colors` | `dict[str, str] \| None` | `None` | Per-slice color overrides |
| `default_colors` | `list[str] \| None` | `None` | Color palette (cycled if fewer than slices) |
| `axis_color` | `str` | `"#495057"` | Color for wedge strokes |
| `radius` | `int` | `100` | Pie radius in pixels |
| `fs` | `int` | `14` | Base font size |
| `roughness` | `int` | `1` | Excalidraw roughness level |
| `font_family` | `int` | `3` | Font family |
| `stroke_width` | `int` | `2` | Stroke width for wedge outlines |
| `show_labels` | `bool` | `True` | Show slice name labels around the pie |
| `show_percentages` | `bool` | `True` | Show percentage labels |
| `show_legend` | `bool` | `True` | Show color-coded legend below pie |
| `donut` | `bool` | `False` | Cut out a center hole |
| `donut_radius` | `int` | `50` | Radius of center hole when `donut=True` |

### Standard Pie

```python
from core.charts import pie_chart

elements = pie_chart(
    x=50, y=50,
    data={"Python": 40, "JavaScript": 30, "Go": 20, "Rust": 10},
    title="Language Usage",
    show_percentages=True,
)
```
