---
title: LaTeX 公式
---

# LaTeX 公式

将 LaTeX 数学表达式渲染为 Excalidraw 图片元素。使用 matplotlib 进行渲染，支持从 mathtext 到完整 LaTeX 的自动回退。

## `formula`

```python
from core.latex import formula

elements = formula(
    r"E = mc^2",
    x=100, y=50,
    font_size=20,
    stroke="#1e1e1e",
    stroke_width=2,
    roughness=0,
    scale=1.0,
    dpi=300,
    fontset=None,
)
```

| 参数 | 类型 | 默认值 | 说明 |
|-----------|------|---------|-------------|
| `latex_str` | `str` | 必填 | LaTeX 数学表达式（如 `"E = mc^2"`） |
| `x` | `float` | `0` | X 位置 |
| `y` | `float` | `0` | Y 位置 |
| `font_size` | `int` | `20` | 字体大小（磅） |
| `stroke` | `str` | `"#1e1e1e"` | 描边颜色（用于文本回退） |
| `stroke_width` | `int` | `2` | 描边宽度（用于文本回退） |
| `roughness` | `int` | `0` | 粗糙度（用于文本回退） |
| `scale` | `float` | `1.0` | 渲染公式的缩放因子 |
| `dpi` | `int` | `300` | 渲染分辨率（越高越清晰，但文件越大） |
| `fontset` | `str \| None` | `None` | 数学文本字体集，默认为模块级别的 `DEFAULT_FONTSET` |

返回值：`list[dict]` -- 包含单个元素的列表，该元素为嵌入 base64 PNG 数据的 Excalidraw 图片元素。如果渲染失败，则回退为等宽文本元素。

## 渲染策略

公式渲染器使用两阶段方案：

1. **阶段 1：Mathtext**（快速，无外部依赖）-- 处理大多数常见的 LaTeX 数学语法，包括分数、积分、求和、极限、希腊字母、平方根和上下标。

2. **阶段 2：usetex**（完整 LaTeX + amsmath）-- 当 mathtext 遇到不支持的命令时自动激活。需要系统中安装了 LaTeX 发行版（`pdflatex` 和 `amsmath` 宏包）。

3. **最终回退** -- 如果两个阶段都失败，将原始 LaTeX 字符串渲染为等宽文本。

## 字体选项

通过 `fontset` 参数或模块级别默认值控制数学文本字体：

```python
import core.latex

# 全局修改默认值
core.latex.DEFAULT_FONTSET = "stix"

# 或逐个公式指定
elements = formula(r"\alpha + \beta = \gamma", x=100, y=150, fontset="stix")
```

| 字体集 | 名称 | 风格 |
|---------|------|-------|
| `"stix"` | STIX | 专业/学术风格，清晰 |
| `"cm"` | Computer Modern | 经典 LaTeX 外观 |
| `"dejavusans"` | DejaVu Sans | 现代风格，粗体（默认） |
| `"dejavuserif"` | DejaVu Serif | 衬线风格，纤细 |

注意：使用 usetex 模式（阶段 2）时，使用 LaTeX 默认的 Computer Modern 字体，`fontset` 参数将被忽略。

## 支持的语法

**Mathtext（阶段 1）：**
- 分数：`\frac{a}{b}`
- 积分：`\int`, `\iint`, `\iiint`
- 求和与乘积：`\sum`, `\prod`
- 极限：`\lim`, `\min`, `\max`
- 希腊字母：`\alpha`, `\beta`, `\gamma` 等
- 平方根：`\sqrt{x}`, `\sqrt[n]{x}`
- 上下标：`x_i`, `x^2`
- 标准运算符：`\leq`, `\geq`, `\neq`, `\times`, `\div`

**usetex 回退（阶段 2）-- 环境：**
- `\begin{pmatrix}`, `\begin{bmatrix}`, `\begin{vmatrix}`
- `\begin{array}`
- `\begin{cases}`
- `\begin{smallmatrix}`

usetex 模式需要安装 LaTeX（`pdflatex` + `amsmath` 宏包）。

## 示例

### 简单公式

```python
from core.latex import formula
from core.engine import save

el = formula(r"E = mc^2", x=100, y=50, font_size=20)
save("physics.excalidraw", el)
```

### 包含矩阵的复杂公式

```python
from core.latex import formula
from core.engine import save, rect

# 遇到 pmatrix 时自动回退到 usetex
el = formula(
    r"\begin{pmatrix} a & b \\ c & d \end{pmatrix}",
    x=100, y=100,
    font_size=14,
)

save("matrix.excalidraw", el)
```

### 使用不同字体的多个公式

```python
from core.latex import formula
from core.engine import save

stix = formula(r"\alpha + \beta = \gamma", x=100, y=50, fontset="stix")
cm = formula(r"\alpha + \beta = \gamma", x=100, y=120, fontset="cm")
dejavu = formula(r"\alpha + \beta = \gamma", x=100, y=190, fontset="dejavusans")

save("font-comparison.excalidraw", [*stix, *cm, *dejavu])
```

### 修改全局默认值

```python
import core.latex
core.latex.DEFAULT_FONTSET = "stix"

# 之后所有的 formula() 调用都使用 STIX，除非被单独覆盖
from core.latex import formula
el = formula(r"\sum_{i=1}^{n} i = \frac{n(n+1)}{2}", x=50, y=50)
```
