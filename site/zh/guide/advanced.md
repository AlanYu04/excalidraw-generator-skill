# 高级用法

## 布局辅助函数

使用位置工具函数避免元素重叠。这些函数计算坐标，无需手动计算。

```python
from core.engine import below, right_of, above

# 在 y=100 下方放置一个 60px 高的元素，间距 15px
y2 = below(y=100, h=60, gap=15)    # y2 = 175

# 在 x=50 右侧放置一个 200px 宽的元素，间距 10px
x2 = right_of(x=50, w=200, gap=10) # x2 = 260

# 在 y=100 上方放置一个元素，间距 10px
y_above = above(y=100, gap=10)     # y_above = 90
```

这些是纯函数 — 返回计算值，不修改任何状态。

### 构建垂直堆叠

```python
from core.engine import labeled_rect, below, save

elements = []
y = 50
for label in ["Input", "Hidden 1", "Hidden 2", "Output"]:
    block = labeled_rect(100, y, 200, 50, label)
    elements.extend(block)
    y = below(y=y, h=50, gap=20)

save("stack.excalidraw", elements)
```

## 图片嵌入

使用 base64 编码的数据将图片直接嵌入到 Excalidraw 文件中。

```python
from core.engine import image_embed

# 读取图片文件并嵌入
with open("logo.png", "rb") as f:
    data = f.read()

element, files_entry = image_embed(
    x=100, y=50, w=200, h=100,
    base64_data=data,
    mime="image/png",
)
```

`image_embed` 返回一个 `(element_dict, files_dict)` 元组。保存时需要同时传入两者：

```python
from core.engine import save

element, files = image_embed(100, 50, 200, 100, data, "image/png")
save("with-image.excalidraw", [element], files={"embedded_image": files})
```

## CJK 支持

中文、日文和韩文文本会自动处理。所有文本函数都能正确估算 CJK 字符宽度，使标签在容器中居中显示。

```python
from core.engine import labeled_rect, text_standalone

# CJK 文本可用于任何元素
elements = labeled_rect(100, 50, 200, 60, "数据处理流程", font_family=3)

# 多行 CJK 文本
t = text_standalone(300, 100, "第一行\n第二行\n第三行", fs=16, font_family=3)
```

在 Excalidraw 中优化 CJK 渲染，请使用 `font_family=5`。

无需额外配置 — CJK 检测和宽度估算已内置于文本测量函数中。

## 输出格式

### `.excalidraw`

标准 JSON 格式。兼容 [excalidraw.com](https://excalidraw.com)、VS Code Excalidraw 扩展以及任何兼容 Excalidraw 的工具。

### `.excalidraw.md`

用于 [Obsidian Excalidraw 插件](https://github.com/zsviczian/obsidian-excalidraw-plugin) 的 Markdown 包装格式。文件将 Excalidraw JSON 嵌入到 Obsidian 识别的 Markdown 代码块中。

```python
from core.engine import save

save("diagram.excalidraw", elements)        # 纯 JSON
save("diagram.excalidraw.md", elements)     # Obsidian 格式
```

`save()` 函数根据文件扩展名自动检测格式。

## 图标库

持久化图标库将自定义图标存储在 `~/.excalidraw-gen/icons/`，并提供搜索功能。

### 保存和加载

```python
from core.icon_library import save_icon, load_icon, list_library_icons

# 保存自定义图标
save_icon(
    "my-server",
    elements,
    description="带有 LED 指示灯的服务器",
    tags=["server", "hardware"],
)

# 加载并放置
server = load_icon("my-server", x=200, y=100, scale=1.0)

# 列出所有已保存的图标
print(list_library_icons())
```

### 搜索图标

搜索默认使用 TF-IDF（零依赖），如果配置了 OpenAI 则可使用向量检索。

```python
from core.icon_library import find_icons

# TF-IDF 搜索（默认）
results = find_icons("server infrastructure", limit=5)

# OpenAI 向量搜索
results = find_icons("neural network architecture", use_embeddings=True)

# 加载最佳匹配
if results:
    icon = load_icon(results[0]["name"], x=100, y=50)
```

### 从 `.excalidrawlib` 导入

从 Excalidraw 库文件导入图标：

```python
from core.icon_library import import_excalidrawlib

import_excalidrawlib(
    filepath="my-library.excalidrawlib",
    descriptions={"icon-1": "齿轮图标", "icon-2": "云图标"},
    tags_map={"icon-1": ["gear", "settings"], "icon-2": ["cloud"]},
    prefix="custom",
)
```

## AI 图标生成

通过 Gemini API 生成自定义图标，自动进行 SVG 到 Excalidraw 的转换，并提供 PNG 回退。

### 配置

```python
from core.ai_icons import configure

configure(
    api_url="https://generativelanguage.googleapis.com/v1beta",
    api_key="YOUR_GEMINI_API_KEY",
    model="gemini-2.0-flash",
)
```

### 生成图标

```python
from core.ai_icons import generate_icon, generate_and_save

# 生成并放置
elements = generate_icon(
    "kubernetes pod",
    x=100, y=200,
    scale=1.5,
    stroke="#1e1e1e",
    sw=2,
    roughness=1,
)

# 一步生成并保存到图标库
generate_and_save(
    "k8s-pod",
    "Kubernetes pod 图标",
    tags=["k8s", "container"],
)
```

### 原始 SVG 生成

```python
from core.ai_icons import generate_icon_svg

svg_string = generate_icon_svg(
    "neural network node",
    prompt="Simple line art, minimal detail",
    model="gemini-2.0-flash",
)
```

注意：AI 图标生成需要 Gemini API 密钥，并依赖 SVG 转换器进行后处理。

## SVG 转换器

将 SVG 字符串或文件转换为原生 Excalidraw 元素。

```python
from core.svg_converter import svg_to_elements, svg_file_to_elements

# 从 SVG 字符串转换
elements = svg_to_elements(
    '<svg viewBox="0 0 100 100"><circle cx="50" cy="50" r="40"/></svg>',
    x=100, y=50, scale=1.0,
    stroke="#1e1e1e", stroke_width=2, roughness=1,
)

# 从文件转换
elements = svg_file_to_elements("icon.svg", x=200, y=100, scale=2.0)
```

支持的 SVG 功能：`<path>`（所有命令）、`<rect>`、`<circle>`、`<ellipse>`、`<line>`、`<polygon>`、`<polyline>`、`<defs>`、`<use>`、贝塞尔曲线细分、RDP 简化、渐变填充解析和自动形状分类。

## 下一步

- [风格配置](/zh/guide/style-config) — 使用预设和 YAML 自定义视觉外观
- [API 参考](/zh/api/) — 所有模块的完整 API 文档
