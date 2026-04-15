---
title: 样式
---

# 样式

通过预设样式或自定义 YAML 配置控制生成图表的视觉外观。样式定义了颜色、排版、粗糙度、填充模式和布局默认值。

## 预设样式

| 预设 | 字体 | 粗糙度 | 填充风格 | 适用场景 |
|--------|------|-----------|------------|----------|
| **Vivid** | Cascadia (3) | 1 | solid | 丰富、多彩、精细 |
| **Clean** | Helvetica (2) | 0 | solid | 极简、黑白、精确 |
| **Sketch** | Virgil (1) | 2 | hachure | 手绘风格、随意 |

## `load_style`

按名称加载样式。优先检查内置预设，然后回退到 `~/.excalidraw-gen/styles/` 中的自定义 YAML 文件。

```python
from styles import load_style

style = load_style("vivid")
```

| 参数 | 类型 | 默认值 | 说明 |
|-----------|------|---------|-------------|
| `name` | `str` | 必填 | 样式名称（`"vivid"`、`"clean"`、`"sketch"` 或自定义名称） |

返回值：`StyleConfig` 实例。

如果样式名称既不是内置预设也不是自定义 YAML 文件，将抛出 `FileNotFoundError` 异常。

## `list_styles`

```python
from styles import list_styles

names = list_styles()  # ["vivid", "clean", "sketch", ...自定义样式]
```

返回值：`list[str]` -- 所有可用的样式名称（内置 + 自定义）。

## 使用样式属性

```python
from styles import load_style

style = load_style("vivid")

# 语义角色的颜色对
fill, stroke = style.get_color_pair("primary")    # ("#a5d8ff", "#2B5B84")
fill, stroke = style.get_color_pair("danger")     # ("#ffc9c9", "#e03131")
fill, stroke = style.get_color_pair("success")    # ("#b2f2bb", "#2f9e44")

# 排版
font = style.font_family       # 3 (Cascadia)
title_size = style.title_size  # 24

# 布局
roughness = style.roughness       # 1
gap = style.default_gap           # 50
fill_style = style.fill_style     # "solid"
```

## `get_color_pair`

返回语义角色对应的 `(fill, stroke)` 元组。可在任何 `StyleConfig` 实例上使用。

```python
style = load_style("vivid")
fill, stroke = style.get_color_pair("primary")
```

| 角色 | 返回值（Vivid） |
|------|----------------|
| `primary` | `("#a5d8ff", "#2B5B84")` |
| `accent` | `("#ffd8a8", "#E67E22")` |
| `success` | `("#b2f2bb", "#2f9e44")` |
| `warning` | `("#fff3bf", "#f08c00")` |
| `danger` | `("#ffc9c9", "#e03131")` |
| `info` | `("#99e9f2", "#1971c2")` |
| `neutral` | `("#dee2e6", "#999999")` |

## 直接导入预设

为方便使用，可以直接导入预设：

```python
from styles import vivid_style, clean_style, sketch_style

vivid = vivid_style()    # Vivid 预设的 StyleConfig
clean = clean_style()    # Clean 预设的 StyleConfig
sketch = sketch_style()  # Sketch 预设的 StyleConfig
```

## 样式别名

为了向后兼容，`load_style` 会解析以下别名：

| 别名 | 解析为 |
|-------|-------------|
| `"conference"` | `"vivid"` |
| `"journal"` | `"clean"` |
| `"ppt"` | `"sketch"` |

```python
from styles import load_style

style = load_style("conference")  # 等同于 load_style("vivid")
```

## 自定义 YAML 样式

在 `~/.excalidraw-gen/styles/<name>.yaml` 创建 YAML 文件：

```yaml
name: "Dark Mode"
description: "Dark background theme"
colors:
  background: "#1a1a2e"
  primary: "#4A90E2"
  accent: "#E67E22"
  text: "#e0e0e0"
  border: "#555555"
  muted: "#888888"
typography:
  font_family: 3
  title_size: 24
  body_size: 14
  label_size: 11
layout:
  roughness: 1
  border_width: 2
  arrow_width: 2
  default_gap: 50
  border_radius: true
```

然后使用 `load_style("dark-mode")` 加载。

加载器会将 YAML 键映射到 `StyleConfig` 字段。只覆盖你指定的字段，其余保持默认值。

### YAML 结构参考

| 区块 | 键 |
|---------|------|
| `colors` | `background`, `primary`, `accent`, `border`, `muted`, `text` |
| `typography` | `font_family`, `title_size`, `body_size`, `label_size` |
| `layout` | `roughness`, `border_width`, `arrow_width`, `default_gap`, `border_radius` |

## StyleConfig 字段

完整的 `StyleConfig` 数据类暴露以下字段：

**颜色：**
`background`, `primary`, `accent`, `text_color`, `border_color`, `muted`, `success`, `warning`, `danger`, `info`

**填充颜色：**
`primary_fill`, `accent_fill`, `success_fill`, `warning_fill`, `danger_fill`, `info_fill`, `neutral_fill`

**排版：**
`font_family`（1=Virgil, 2=Helvetica, 3=Cascadia）、`title_size`、`subtitle_size`、`body_size`、`label_size`、`caption_size`

**布局：**
`roughness`（0/1/2）、`border_width`、`arrow_width`、`default_gap`、`padding`

**填充/描边：**
`fill_style`（`"solid"` | `"hachure"` | `"cross-hatch"`）、`stroke_style`（`"solid"` | `"dashed"` | `"dotted"`）

**形状：**
`border_radius`、`use_groups`、`compact_layout`

## 完整示例

```python
from styles import load_style
from core.engine import labeled_rect, arrow, bind_arrow, save

style = load_style("vivid")

fill, stroke = style.get_color_pair("primary")
box1 = labeled_rect(100, 50, 200, 60, "Service A",
                    fill=fill, stroke=stroke,
                    roughness=style.roughness, font_family=style.font_family)

fill2, stroke2 = style.get_color_pair("accent")
box2 = labeled_rect(100, 180, 200, 60, "Service B",
                    fill=fill2, stroke=stroke2,
                    roughness=style.roughness, font_family=style.font_family)

a = arrow(200, 110, dx=0, dy=70, stroke=stroke, sw=style.arrow_width,
          roughness=style.roughness)
bound = bind_arrow(a, box1[0], box2[0])

save("styled-diagram.excalidraw", [*box1, *box2, bound])
```
