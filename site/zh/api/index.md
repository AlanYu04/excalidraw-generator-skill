---
title: API 参考
---

# API 参考

Excalidraw Generator 提供了 40 多个公共函数，分布在以下模块中：

| 模块 | 主要函数 | 说明 |
|--------|--------------|-------------|
| `core.engine` | `rect`, `ellipse`, `diamond`, `labeled_*`, `arrow`, `bind_arrow`, `connect` | 元素构建与布局 |
| `core.charts` | `bar_chart`, `horizontal_bar_chart`, `line_chart`, `pie_chart` | 数据可视化 |
| `core.icons` | `icon`, `list_icons` | 39 个内置图标 |
| `core.svg_converter` | `svg_to_elements`, `svg_file_to_elements` | SVG 导入 |
| `core.latex` | `formula` | LaTeX 公式渲染 |
| `core.icon_library` | `save_icon`, `load_icon`, `find_icons` | 持久化图标存储 |
| `core.ai_icons` | `generate_icon`, `generate_and_save` | AI 驱动的图标生成 |
| `styles` | `load_style`, `vivid_style`, `clean_style`, `sketch_style` | 视觉预设样式 |

## 快速导入

```python
# 所有公共 API 均可从 core 导入
from core.engine import *
from core.charts import *
from core.icons import *
from core.latex import formula
from core.svg_converter import svg_to_elements
```

## 进一步阅读

- [元素构建器](./elements) -- 形状、箭头、布局辅助函数和输出
- [图表](./charts) -- 柱状图、水平柱状图、折线图和饼图
- [图标](./icons) -- 内置图标、图标库和 AI 生成
- [SVG 转换](./svg-converter) -- 将 SVG 转换为原生 Excalidraw 元素
- [LaTeX 公式](./latex) -- 将数学表达式渲染为图片
- [样式](./styles) -- 预设样式、自定义 YAML 和颜色对
