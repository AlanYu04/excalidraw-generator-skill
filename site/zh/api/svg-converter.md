---
title: SVG 转换
---

# SVG 转换

将 SVG 字符串或文件转换为原生 Excalidraw 元素。转换器解析 SVG 路径数据，将贝塞尔曲线和弧线细分为折线，通过 Ramer-Douglas-Peucker 算法进行简化，并将形状分类为椭圆、矩形或自由线条。

## `svg_to_elements`

```python
from core.svg_converter import svg_to_elements

elements = svg_to_elements(
    '<svg viewBox="0 0 100 100"><circle cx="50" cy="50" r="40"/></svg>',
    x=100, y=50,
    scale=1.0,
    stroke="#1e1e1e",
    stroke_width=2,
    roughness=1,
)
```

| 参数 | 类型 | 默认值 | 说明 |
|-----------|------|---------|-------------|
| `svg_string` | `str` | 必填 | SVG 内容字符串 |
| `x` | `float` | `0` | 生成元素的 X 偏移量 |
| `y` | `float` | `0` | 生成元素的 Y 偏移量 |
| `scale` | `float` | `1.0` | 应用于所有坐标的缩放因子 |
| `stroke` | `str` | `"#1e1e1e"` | 默认描边颜色 |
| `stroke_width` | `int` | `2` | 默认描边宽度 |
| `roughness` | `int` | `1` | Excalidraw 粗糙度（0=精确, 1=轻微, 2=粗糙） |

返回值：`list[dict]` -- Excalidraw 元素字典列表。

如果 SVG 具有 `viewBox` 属性，转换器会将输出标准化到约 100px，并在其基础上应用 `scale` 参数。

## `svg_file_to_elements`

```python
from core.svg_converter import svg_file_to_elements

elements = svg_file_to_elements("icon.svg", x=200, y=100, scale=2.0)
```

| 参数 | 类型 | 默认值 | 说明 |
|-----------|------|---------|-------------|
| `filepath` | `str` | 必填 | SVG 文件路径 |
| `x` | `float` | `0` | X 偏移量 |
| `y` | `float` | `0` | Y 偏移量 |
| `scale` | `float` | `1.0` | 缩放因子 |
| `stroke` | `str` | `"#1e1e1e"` | 默认描边颜色 |
| `stroke_width` | `int` | `2` | 默认描边宽度 |
| `roughness` | `int` | `1` | 粗糙度级别 |

返回值：`list[dict]` -- Excalidraw 元素字典列表。

## 支持的 SVG 功能

转换器处理以下 SVG 元素和功能：

**元素：**
- `<path>` 及所有标准命令
- `<rect>`
- `<circle>`
- `<ellipse>`
- `<line>`
- `<polygon>`
- `<polyline>`
- `<defs>` 和 `<use>`（引用解析）

**路径命令：**
- `M`, `m` -- 移动到
- `L`, `l` -- 直线到
- `H`, `h` -- 水平直线到
- `V`, `v` -- 垂直直线到
- `C`, `c` -- 三次贝塞尔曲线
- `S`, `s` -- 简写三次贝塞尔曲线
- `Q`, `q` -- 二次贝塞尔曲线
- `T`, `t` -- 简写二次贝塞尔曲线
- `A`, `a` -- 弧线
- `Z`, `z` -- 闭合路径

**处理流程：**
1. 贝塞尔曲线细分（三次：8 个采样点，二次：6 个采样点，弧线：36 个采样点）
2. 使用自适应 epsilon 的 Ramer-Douglas-Peucker 简化
3. 自动形状分类（椭圆、矩形或自由线条）
4. 从 `<defs>` 解析渐变填充
5. 变换解析（`translate`、`scale`、`rotate`、`matrix`）

## 示例：导入 Logo

```python
from core.svg_converter import svg_file_to_elements
from core.engine import save

elements = svg_file_to_elements(
    "company-logo.svg",
    x=100, y=100,
    scale=3.0,
    stroke="#2B5B84",
    stroke_width=2,
    roughness=1,
)

save("logo.excalidraw", elements)
```

## 示例：内联 SVG

```python
from core.svg_converter import svg_to_elements
from core.engine import save, rect

svg = '''
<svg viewBox="0 0 48 48">
  <circle cx="24" cy="24" r="20" fill="#a5d8ff" stroke="#1e1e1e"/>
  <line x1="10" y1="24" x2="38" y2="24" stroke="#1e1e1e" stroke-width="2"/>
</svg>
'''

background = rect(0, 0, 300, 200, fill="#ffffff")
icon_elements = svg_to_elements(svg, x=50, y=50, scale=4.0)

save("icon-demo.excalidraw", [background, *icon_elements])
```
