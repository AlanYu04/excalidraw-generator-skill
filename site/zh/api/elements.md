---
title: 元素构建器
---

# 元素构建器

用于以编程方式构建 Excalidraw 图表的核心构建块。所有函数返回普通的 Python 字典（或字典列表），代表 Excalidraw 场景元素。

## 基础形状

### `rect`

```python
from core.engine import rect

el = rect(
    x=100, y=50, w=200, h=80,
    fill="#a5d8ff",       # 默认值: "transparent"
    stroke="#1e1e1e",     # 默认值: "#1e1e1e"
    sw=2,                 # 描边宽度，默认值: 2
    roughness=1,          # 0=精确, 1=默认, 2=粗糙
    fill_style="solid",   # "solid" | "hachure" | "cross-hatch"
    stroke_style="solid", # "solid" | "dashed" | "dotted"
)
```

返回值：`dict` -- 单个 Excalidraw 矩形元素。

### `ellipse`

```python
from core.engine import ellipse

el = ellipse(
    x=100, y=50, w=120, h=60,
    fill="transparent",
    stroke="#1e1e1e",
    sw=2,
    roughness=1,
    fill_style="solid",
)
```

返回值：`dict` -- 单个 Excalidraw 椭圆元素。

### `diamond`

```python
from core.engine import diamond

el = diamond(
    x=100, y=50, w=160, h=100,
    fill="transparent",
    stroke="#1e1e1e",
    sw=2,
    roughness=1,
    fill_style="solid",
)
```

返回值：`dict` -- 单个 Excalidraw 菱形元素。

## 带标签的形状

带标签的形状返回一个 `[shape, text]` 元组，文本通过 `containerId` 绑定到形状上。Excalidraw 会自动将文本居中于形状内部。

### `labeled_rect`

```python
from core.engine import labeled_rect

shape, label = labeled_rect(
    x=100, y=50, w=200, h=60,
    label="Process",
    fill="transparent",
    stroke="#1e1e1e",
    sw=2,
    fs=16,                # 字体大小
    label_color=None,     # 默认使用描边颜色
    roughness=1,
    font_family=3,        # 1=Virgil, 2=Helvetica, 3=Cascadia
    fill_style="solid",
    stroke_style="solid",
)
```

返回值：`list[dict]` -- `[rectangle, bound_text]`。

### `labeled_ellipse`

```python
from core.engine import labeled_ellipse

shape, label = labeled_ellipse(
    x=100, y=50, w=120, h=60,
    label="Start",
    fill="#d0f0c0",
    stroke="#1e1e1e",
    sw=2,
    fs=16,
    label_color=None,
    roughness=1,
    font_family=3,
    fill_style="solid",
)
```

返回值：`list[dict]` -- `[ellipse, bound_text]`。

### `labeled_diamond`

```python
from core.engine import labeled_diamond

shape, label = labeled_diamond(
    x=100, y=50, w=160, h=100,
    label="Decision?",
    fill="transparent",
    stroke="#1e1e1e",
    sw=2,
    fs=16,
    label_color=None,
    roughness=1,
    font_family=3,
    fill_style="solid",
)
```

返回值：`list[dict]` -- `[diamond, bound_text]`。

## 连接器

### `arrow`

```python
from core.engine import arrow

# 相对偏移模式
a1 = arrow(250, 70, dx=0, dy=30, stroke="#1e1e1e", sw=2, roughness=1)

# 绝对坐标模式（仅限关键字参数）
a2 = arrow(100, 50, x2=300, y2=200, stroke="#1e1e1e", sw=2, roughness=1)
```

返回值：`dict` -- 单个 Excalidraw 箭头元素。

### `line`

```python
from core.engine import line

# 相对偏移模式
l1 = line(100, 50, dx=200, dy=0, stroke="#1e1e1e", sw=2, roughness=1)

# 绝对坐标模式
l2 = line(100, 50, x2=300, y2=100, stroke="#1e1e1e", sw=2, roughness=1)
```

返回值：`dict` -- 单个 Excalidraw 线条元素。

### `bind_arrow`

将箭头绑定到起始和结束元素，建立双向引用关系。

```python
from core.engine import arrow, bind_arrow, labeled_rect

step1 = labeled_rect(100, 50, 200, 60, "Step 1")
step2 = labeled_rect(100, 150, 200, 60, "Step 2")

a = arrow(200, 110, dx=0, dy=40)
bound = bind_arrow(a, step1[0], step2[0], gap=2)
```

返回值：`dict` -- 已设置 `startBinding` 和 `endBinding` 的箭头元素。

### `connect`

一次调用即可创建连接两个元素的绑定箭头。箭头从起始元素中心出发，Excalidraw 自动计算正确的边缘交点。

```python
from core.engine import labeled_rect, connect

step1 = labeled_rect(100, 50, 200, 60, "Step 1")
step2 = labeled_rect(100, 150, 200, 60, "Step 2")

a = connect(step1[0], step2[0], stroke="#1e1e1e", sw=2, roughness=1, gap=8)
```

返回值：`dict` -- 一个绑定箭头元素。

## 文本

### `text_standalone`

```python
from core.engine import text_standalone

t = text_standalone(
    cx=300, cy=100,           # 中心位置
    txt="Hello World",
    fs=20,                     # 字体大小，默认值: 20
    color="#1e1e1e",           # 文本颜色
    font_family=3,             # 1=Virgil, 2=Helvetica, 3=Cascadia
    roughness=0,
    text_align="center",       # "center" | "left" | "right"
    max_width=None,            # 文本超出宽度时自动缩小字体
)
```

返回值：`dict` -- 单个 Excalidraw 文本元素。

`text_standalone` 支持 `text_align`（`"center"`、`"left"`、`"right"`）和 `max_width` -- 设置后，字体会自动缩小直到文本符合宽度限制。

## 结构元素

### `numbered_circle`

```python
from core.engine import numbered_circle

circle = numbered_circle(cx=100, cy=50, num=1, fill="#a5d8ff", stroke="#2B5B84")
```

返回值：`list[dict]` -- `[ellipse, text]`，数字居中显示在圆形内部。

### `frame`

```python
from core.engine import frame

f = frame(x=0, y=0, w=500, h=400, name="Architecture", stroke="#1e1e1e", sw=2)
```

返回值：`dict` -- 单个 Excalidraw 框架元素。

### `group`

```python
from core.engine import group, rect, ellipse

elements = [
    rect(0, 0, 100, 50),
    ellipse(10, 10, 30, 30),
]
grouped = group(elements)
```

返回值：`list[dict]` -- 共享相同 `groupIds` 条目的新元素列表。

### `image_embed`

```python
from core.engine import image_embed

el, files = image_embed(
    x=100, y=50, w=200, h=150,
    base64_data="iVBORw0KGgo...",
    mime="image/png",
)
```

返回值：`tuple[dict, dict]` -- 图片元素和用于嵌入场景的 `files` 字典。

## 函数参考

| 函数 | 签名 | 返回值 |
|----------|-----------|---------|
| `rect` | `rect(x, y, w, h, fill, stroke, sw, roughness, fill_style, stroke_style)` | `dict` |
| `ellipse` | `ellipse(x, y, w, h, fill, stroke, sw, roughness, fill_style)` | `dict` |
| `diamond` | `diamond(x, y, w, h, fill, stroke, sw, roughness, fill_style)` | `dict` |
| `labeled_rect` | `labeled_rect(x, y, w, h, label, fill, stroke, sw, fs, label_color, roughness, font_family, fill_style, stroke_style)` | `[rect, text]` |
| `labeled_ellipse` | `labeled_ellipse(x, y, w, h, label, fill, stroke, sw, fs, label_color, roughness, font_family, fill_style)` | `[ellipse, text]` |
| `labeled_diamond` | `labeled_diamond(x, y, w, h, label, fill, stroke, sw, fs, label_color, roughness, font_family, fill_style)` | `[diamond, text]` |
| `text_standalone` | `text_standalone(cx, cy, txt, fs=20, color, font_family=3, roughness=0, text_align="center", max_width=None)` | `dict` |
| `arrow` | `arrow(x, y, dx=0, dy=0, *, x2=None, y2=None, stroke, sw, roughness)` | `dict` |
| `line` | `line(x, y, dx=0, dy=0, *, x2=None, y2=None, stroke, sw, roughness)` | `dict` |
| `numbered_circle` | `numbered_circle(cx, cy, num, fill, stroke)` | `[ellipse, text]` |
| `frame` | `frame(x, y, w, h, name="Frame", stroke, sw)` | `dict` |
| `group` | `group(elements)` | `list[dict]` |
| `bind_arrow` | `bind_arrow(arrow_el, start_el, end_el, gap=2)` | `dict` |
| `connect` | `connect(start_el, end_el, stroke, sw, roughness, gap=8)` | `dict` |
| `image_embed` | `image_embed(x, y, w, h, base64_data, mime="image/png")` | `(element, files)` |
| `bounds` | `bounds(elements)` | `(min_x, min_y, max_x, max_y)` |

## 布局辅助函数

通过位置计算工具防止文本和形状重叠：

```python
from core.engine import below, right_of, above

y2 = below(y=100, h=60, gap=15)     # y2 = 175
x2 = right_of(x=50, w=200, gap=10)  # x2 = 260
y_above = above(y=100, gap=10)      # y_above = 90
```

| 辅助函数 | 签名 | 说明 |
|--------|-----------|-------------|
| `below` | `below(y, h, gap=10)` | 位于形状下方的安全 y 坐标 |
| `right_of` | `right_of(x, w, gap=10)` | 位于形状右侧的安全 x 坐标 |
| `above` | `above(y, gap=10)` | 位于形状上方的安全 y 坐标 |
| `bounds` | `bounds(elements)` | 边界框 `(min_x, min_y, max_x, max_y)` |

## 输出

### `save`

根据文件扩展名自动检测输出格式。

```python
from core.engine import save

save("diagram.excalidraw", elements)        # 标准 JSON
save("diagram.excalidraw.md", elements)     # Obsidian Markdown 包装
```

### `save_excalidraw`

写入与 [excalidraw.com](https://excalidraw.com)、VS Code 扩展及任何 Excalidraw 兼容工具兼容的纯 JSON 文件。

```python
from core.engine import save_excalidraw

save_excalidraw("diagram.excalidraw", elements, bg="#ffffff", files=None)
```

### `save_obsidian_md`

为 [Obsidian Excalidraw 插件](https://github.com/zsviczian/obsidian-excalidraw-plugin) 写入 Markdown 包装文件。

```python
from core.engine import save_obsidian_md

save_obsidian_md("diagram.excalidraw.md", elements, bg="#ffffff", files=None)
```

## 完整示例：流程图

```python
from core.engine import (
    labeled_ellipse, labeled_rect, labeled_diamond,
    arrow, bind_arrow, save,
)

# 1. 创建形状
start   = labeled_ellipse(200, 20, 120, 50, "Start", fill="#d0f0c0")
process = labeled_rect(170, 110, 180, 60, "Process Data")
decision = labeled_diamond(160, 220, 200, 120, "Valid?")
end_yes = labeled_ellipse(140, 400, 120, 50, "Done", fill="#d0f0c0")
end_no  = labeled_ellipse(340, 400, 120, 50, "Retry", fill="#ffc9c9")

# 2. 用箭头连接
a1 = bind_arrow(arrow(260, 70, 0, 40), start[0], process[0])
a2 = bind_arrow(arrow(260, 170, 0, 50), process[0], decision[0])
a3 = bind_arrow(arrow(220, 340, 0, 60), decision[0], end_yes[0])
a4 = bind_arrow(arrow(340, 340, 0, 60), decision[0], end_no[0])

# 3. 收集并保存
elements = [*start, *process, *decision, *end_yes, *end_no, a1, a2, a3, a4]
save("flowchart.excalidraw", elements)
```
