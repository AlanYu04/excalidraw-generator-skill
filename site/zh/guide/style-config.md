# 风格配置

Excalidraw Generator 内置三种风格预设，控制字体、粗糙度、填充方式和颜色。你也可以通过 YAML 定义自定义样式。

## 内置预设

| 预设 | 字体 | 粗糙度 | 填充方式 | 适用场景 |
|------|------|--------|----------|----------|
| **Vivid** | Cascadia (3) | 1 | Solid | 丰富、多彩、精细 — 会议演示 |
| **Clean** | Helvetica (2) | 0 | Solid | 简约、黑白、精确 — 学术论文 |
| **Sketch** | Virgil (1) | 2 | Hachure | 手绘、随意 — 演示和笔记 |

## 加载风格

```python
from styles import load_style

# 按名称加载
style = load_style("vivid")

# 别名也可以
style = load_style("conference")  # 等同于 "vivid"
```

风格别名：`conference` -> `vivid`，`journal` -> `clean`，`ppt` -> `sketch`。

## 颜色对

每种风格通过 `get_color_pair(role)` 提供语义化颜色对。每次调用返回 `(fill, stroke)` 元组。

```python
from styles import load_style

style = load_style("vivid")

fill, stroke = style.get_color_pair("primary")   # ("#a5d8ff", "#2B5B84")
fill, stroke = style.get_color_pair("accent")    # ("#ffd8a8", "#E67E22")
fill, stroke = style.get_color_pair("success")   # ("#b2f2bb", "#2f9e44")
fill, stroke = style.get_color_pair("warning")   # ("#fff3bf", "#f08c00")
fill, stroke = style.get_color_pair("danger")    # ("#ffc9c9", "#e03131")
fill, stroke = style.get_color_pair("info")      # ("#99e9f2", "#1971c2")
fill, stroke = style.get_color_pair("neutral")   # ("#dee2e6", "#999999")
```

支持的角色：`primary`、`accent`、`success`、`warning`、`danger`、`info`、`neutral`。

## 风格配置字段

`StyleConfig` 数据类暴露以下字段：

**颜色**

| 字段 | 默认值 | 说明 |
|------|--------|------|
| `background` | `#ffffff` | 画布背景 |
| `primary` | `#2B5B84` | 主要描边颜色 |
| `accent` | `#E67E22` | 强调描边颜色 |
| `text_color` | `#1e1e1e` | 默认文本颜色 |
| `border_color` | `#333333` | 边框描边颜色 |
| `muted` | `#999999` | 次要/辅助文本 |
| `success` | `#2f9e44` | 成功描边 |
| `warning` | `#f08c00` | 警告描边 |
| `danger` | `#e03131` | 危险描边 |
| `info` | `#1971c2` | 信息描边 |

**排版**

| 字段 | 默认值 | 说明 |
|------|--------|------|
| `font_family` | `3` | 1=Virgil（手写体），2=Helvetica，3=Cascadia |
| `title_size` | `24` | 标题字号 |
| `body_size` | `14` | 正文字号 |
| `label_size` | `11` | 标签字号 |

**布局**

| 字段 | 默认值 | 说明 |
|------|--------|------|
| `roughness` | `1` | 0=精确，1=轻微，2=粗糙 |
| `border_width` | `2` | 默认描边宽度 |
| `fill_style` | `"solid"` | `"solid"`、`"hachure"` 或 `"cross-hatch"` |
| `stroke_style` | `"solid"` | `"solid"`、`"dashed"` 或 `"dotted"` |
| `border_radius` | `True` | 圆角矩形 |

## 自定义 YAML 样式

在 `~/.excalidraw-gen/styles/` 目录下创建 YAML 文件来定义自己的样式。例如 `~/.excalidraw-gen/styles/dark-mode.yaml`：

```yaml
name: "Dark Mode"
description: "暗色背景主题，适合演示"
colors:
  background: "#1a1a2e"
  primary: "#4A90E2"
  accent: "#E67E22"
  text: "#e0e0e0"
  border: "#555555"
typography:
  font_family: 3
  title_size: 24
  body_size: 14
layout:
  roughness: 1
  border_width: 2
  default_gap: 50
```

然后按名称加载：

```python
from styles import load_style

style = load_style("dark-mode")
```

加载器会先检查内置预设，然后回退到自定义 YAML 文件。如果找不到指定样式，会抛出 `FileNotFoundError` 并列出所有可用的样式。

## 实时预览

切换三种预设，查看实际效果：

<ClientOnly>
  <StyleSwitcher />
</ClientOnly>

## 下一步

- [高级用法](/zh/guide/advanced) — 布局辅助、CJK 支持、图标库和输出格式
- [API 参考：Styles](/zh/api/styles) — 完整的 `StyleConfig` API 文档
