---
title: 图表
---

# 图表

生成手绘风格的柱状图、水平柱状图、折线图和饼图，输出为原生 Excalidraw 元素。所有图表函数返回一个扁平的 Excalidraw 元素字典列表。

## 柱状图

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

### 参数

| 参数 | 类型 | 默认值 | 说明 |
|-----------|------|---------|-------------|
| `x` | `float` | 必填 | 左上角 X 坐标 |
| `y` | `float` | 必填 | 左上角 Y 坐标 |
| `data` | `dict[str, int\|float]` | 必填 | 类别标签到数值的映射 |
| `title` | `str \| None` | `None` | 显示在图表上方的标题 |
| `bar_color` | `str` | `"#a5d8ff"` | 柱子的默认填充颜色 |
| `bar_colors` | `dict[str, str] \| None` | `None` | 按类别指定颜色覆盖 |
| `axis_color` | `str` | `"#495057"` | 坐标轴和刻度线颜色 |
| `bar_width` | `int` | `60` | 每个柱子的宽度（像素） |
| `max_height` | `int` | `200` | 柱子的最大高度（像素） |
| `gap` | `int` | `30` | 柱子之间的水平间距 |
| `fs` | `int` | `14` | 基础字体大小 |
| `label_fs` | `int \| None` | `None` | 类别标签字体大小（默认为 `fs`） |
| `value_fs` | `int \| None` | `None` | 数值标签字体大小（默认为 `fs - 2`） |
| `title_fs` | `int \| None` | `None` | 标题字体大小（默认为 `fs + 8`） |
| `roughness` | `int` | `1` | Excalidraw 粗糙度级别 |
| `font_family` | `int` | `3` | 字体族（1=Virgil, 2=Helvetica, 3=Cascadia） |
| `stroke_width` | `int` | `2` | 柱子和坐标轴的描边宽度 |
| `show_values` | `bool` | `True` | 在每个柱子上方显示数值 |
| `show_grid` | `bool` | `False` | 显示水平网格线 |
| `grid_color` | `str` | `"#dee2e6"` | 网格线颜色 |
| `grid_lines` | `int` | `5` | 网格线数量 |
| `axis_label` | `str \| None` | `None` | 可选的 Y 轴标签文本 |

### 按类别指定颜色

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

## 水平柱状图

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

### 参数

| 参数 | 类型 | 默认值 | 说明 |
|-----------|------|---------|-------------|
| `x` | `float` | 必填 | 左上角 X 坐标 |
| `y` | `float` | 必填 | 左上角 Y 坐标 |
| `data` | `dict[str, int\|float]` | 必填 | 类别标签到数值的映射 |
| `title` | `str \| None` | `None` | 图表标题 |
| `bar_color` | `str` | `"#a5d8ff"` | 默认填充颜色 |
| `bar_colors` | `dict[str, str] \| None` | `None` | 按类别指定颜色覆盖 |
| `axis_color` | `str` | `"#495057"` | 坐标轴线颜色 |
| `bar_height` | `int` | `40` | 每个柱子的高度 |
| `max_width` | `int` | `250` | 柱子的最大宽度 |
| `gap` | `int` | `15` | 柱子之间的垂直间距 |
| `fs` | `int` | `14` | 基础字体大小 |
| `label_fs` | `int \| None` | `None` | 类别标签字体大小 |
| `value_fs` | `int \| None` | `None` | 数值标签字体大小 |
| `title_fs` | `int \| None` | `None` | 标题字体大小 |
| `roughness` | `int` | `1` | Excalidraw 粗糙度级别 |
| `font_family` | `int` | `3` | 字体族 |
| `stroke_width` | `int` | `2` | 描边宽度 |
| `show_values` | `bool` | `True` | 在每个柱子末端显示数值 |

## 折线图

### `line_chart`

支持多系列绘制，可选图例、数据点标记和网格线。

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

### 参数

| 参数 | 类型 | 默认值 | 说明 |
|-----------|------|---------|-------------|
| `x` | `float` | 必填 | 左上角 X 坐标 |
| `y` | `float` | 必填 | 左上角 Y 坐标 |
| `data` | `dict[str, list[int\|float]]` | 必填 | 系列名称到数值列表的映射 |
| `labels` | `list[str]` | 必填 | X 轴标签（每个数据点一个） |
| `title` | `str \| None` | `None` | 显示在图表上方的标题 |
| `series_colors` | `dict[str, str] \| None` | `None` | 按系列指定颜色覆盖 |
| `default_color` | `str` | `"#1971c2"` | 默认线条/数据点颜色 |
| `axis_color` | `str` | `"#495057"` | 坐标轴颜色 |
| `chart_width` | `int` | `400` | 图表区域的宽度（像素） |
| `chart_height` | `int` | `200` | 图表区域的高度（像素） |
| `fs` | `int` | `14` | 基础字体大小 |
| `label_fs` | `int \| None` | `None` | X 轴标签字体大小 |
| `value_fs` | `int \| None` | `None` | 数值标注字体大小 |
| `title_fs` | `int \| None` | `None` | 标题字体大小 |
| `roughness` | `int` | `1` | Excalidraw 粗糙度级别 |
| `font_family` | `int` | `3` | 字体族 |
| `stroke_width` | `int` | `2` | 线条和坐标轴的描边宽度 |
| `show_points` | `bool` | `True` | 在数据点处显示圆点标记 |
| `show_values` | `bool` | `False` | 在每个数据点处显示数值 |
| `show_grid` | `bool` | `False` | 显示水平网格线 |
| `grid_color` | `str` | `"#dee2e6"` | 网格线颜色 |
| `grid_lines` | `int` | `5` | 网格线数量 |
| `show_legend` | `bool` | `True` | 在图表下方显示系列图例 |

## 饼图

### `pie_chart`

支持标准饼图和环形图模式，带有百分比标签和颜色编码图例。

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

### 参数

| 参数 | 类型 | 默认值 | 说明 |
|-----------|------|---------|-------------|
| `x` | `float` | 必填 | 图表左上角的 X 坐标 |
| `y` | `float` | 必填 | 图表左上角的 Y 坐标 |
| `data` | `dict[str, int\|float]` | 必填 | 扇区名称到数值的映射 |
| `title` | `str \| None` | `None` | 显示在图表上方的标题 |
| `slice_colors` | `dict[str, str] \| None` | `None` | 按扇区指定颜色覆盖 |
| `default_colors` | `list[str] \| None` | `None` | 调色板（少于扇区数量时循环使用） |
| `axis_color` | `str` | `"#495057"` | 扇形描边颜色 |
| `radius` | `int` | `100` | 饼图半径（像素） |
| `fs` | `int` | `14` | 基础字体大小 |
| `roughness` | `int` | `1` | Excalidraw 粗糙度级别 |
| `font_family` | `int` | `3` | 字体族 |
| `stroke_width` | `int` | `2` | 扇形轮廓描边宽度 |
| `show_labels` | `bool` | `True` | 在饼图周围显示扇区名称标签 |
| `show_percentages` | `bool` | `True` | 显示百分比标签 |
| `show_legend` | `bool` | `True` | 在饼图下方显示颜色编码图例 |
| `donut` | `bool` | `False` | 切除中心孔洞 |
| `donut_radius` | `int` | `50` | 当 `donut=True` 时中心孔洞的半径 |

### 标准饼图

```python
from core.charts import pie_chart

elements = pie_chart(
    x=50, y=50,
    data={"Python": 40, "JavaScript": 30, "Go": 20, "Rust": 10},
    title="Language Usage",
    show_percentages=True,
)
```
