# 快速开始

## 作为 Claude Code 技能使用

将仓库克隆到你的 Claude Code 技能目录：

```bash
git clone https://github.com/AlanYu04/excalidraw-generator-skill ~/.claude/skills/excalidraw-generator
```

然后直接让 Claude 画图：

> "帮我画一个 Transformer 架构图 — vivid 风格，hachure 填充，roughness 1"

Claude 会生成一个 `.excalidraw` 文件，你可以在 [excalidraw.com](https://excalidraw.com)、VS Code 或 Obsidian 中打开。

## 作为 Python 库使用

### 前置条件

**Obsidian（推荐）** — 用于查看和编辑 Excalidraw 文件：

1. 从 [obsidian.md](https://obsidian.md/download) 下载
2. 创建或打开一个 Vault
3. 安装 **Excalidraw** 社区插件（作者：Zsolt Viczian）

**不使用 Obsidian** — `.excalidraw` 文件是标准 JSON 格式，兼容任何支持 Excalidraw 的工具。

### 安装

```bash
cd ~/.claude/skills/excalidraw-generator
pip install matplotlib numpy
```

可选：`pip install pyyaml` 用于自定义 YAML 样式。

### 创建你的第一个图表

```python
from core.engine import labeled_rect, labeled_ellipse, arrow, bind_arrow, save

# 1. 创建形状
start = labeled_ellipse(200, 20, 100, 50, "Start", fill="#d0f0c0")
step  = labeled_rect(150, 100, 200, 60, "Process")
end   = labeled_ellipse(200, 200, 100, 50, "End", fill="#d0f0c0")

# 2. 用箭头连接
a1 = bind_arrow(arrow(250, 70, 0, 30), start[0], step[0])
a2 = bind_arrow(arrow(250, 160, 0, 40), step[0], end[0])

# 3. 保存
elements = [*start, *step, *end, a1, a2]
save("flow.excalidraw", elements)
```

### 生成图表

```python
from core.charts import bar_chart

elements = bar_chart(
    x=50, y=100,
    data={"React": 85, "Vue": 72, "Angular": 58},
    title="Framework Popularity",
    bar_color="#a5d8ff",
    show_values=True,
    show_grid=True,
)
```

### 添加公式

```python
from core.latex import formula

elements = formula(r"E = mc^2", x=100, y=50, font_size=20)
```

### 放置图标

```python
from core.icons import icon

elements = icon("database", x=100, y=50, scale=1.0, stroke="#1e1e1e", sw=2)
```

## 下一步

- [风格配置](/zh/guide/style-config) — 了解 3 种风格预设和自定义 YAML 样式
- [高级用法](/zh/guide/advanced) — 布局辅助、CJK 支持、图标库等
- [API 参考](/zh/api/) — 所有模块的完整 API 文档
