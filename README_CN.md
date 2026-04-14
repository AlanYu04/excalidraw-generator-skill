<div align="center">

# ✏️ Excalidraw Generator

**[English](README.md)** | **[中文](README_CN.md)**

**AI 驱动的 Excalidraw 图表生成器，适用于 Claude Code**

直接生成高质量的流程图、架构图、图表等 — 输出标准 Excalidraw JSON。

[![Python 3.9+](https://img.shields.io/badge/Python-3.9+-3776AB?logo=python&logoColor=white)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Claude Code Skill](https://img.shields.io/badge/Claude_Code-Skill-blueviolet?logo=data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjQiIGhlaWdodD0iMjQiIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cGF0aCBkPSJNMTIgMkw0IDdWMTdMMTIgMjJMMjAgMTdWN0wxMiAyWiIgc3Ryb2tlPSJ3aGl0ZSIgc3Ryb2tlLXdpZHRoPSIyIi8+PC9zdmc+)](https://github.com/AlanYu04/excalidraw-generator-skill)

`39 个内置图标` · `4 种图表类型` · `3 种样式预设` · `CJK 支持` · `零依赖`

</div>

---

## ✨ 功能特性

| | 功能 | 说明 |
|---|------|------|
| 📐 | **元素构建器** | 矩形、椭圆、菱形、箭头、线条、文本 — 支持 `containerId` 绑定 |
| 📊 | **4 种图表** | 柱状图、横向柱状图、折线图、饼图（含甜甜圈模式） |
| 🎨 | **39 个内置图标** | 通用 + ML/AI + 工具类图标集 |
| 🤖 | **AI 图标生成** | 通过 Gemini API 生成自定义图标 |
| 🎭 | **3 种样式预设** | Vivid、Clean、Sketch + 自定义 YAML 样式 |
| 🔄 | **SVG 转换** | SVG 转 Excalidraw，支持贝塞尔曲线和形状分类 |
| 📚 | **图标库** | 持久化存储，支持 TF-IDF 搜索或 OpenAI 向量搜索 |
| 🇨🇳 | **CJK 支持** | 中文、日文、韩文文本渲染 |
| 📏 | **布局助手** | 防止文字与形状重叠 |
| 💾 | **双格式输出** | `.excalidraw`（JSON）或 `.excalidraw.md`（Obsidian） |

> \* AI 图标生成需要 Gemini API 密钥；YAML 样式需要 PyYAML

---

### 🔧 工作原理

![Workflow](docs/images/workflow.png)

### 🖼️ 效果展示

| 架构图 | 图表 | 图标 |
|:---:|:---:|:---:|
| ![Architecture](docs/images/architecture.png) | ![Bar Chart](docs/images/bar-chart.png) | ![Icons](docs/images/icons.png) |
| ![Line Chart](docs/images/line-chart.png) | ![Bar Chart 2](docs/images/bar-chart-2.png) | |

### 🚀 实际案例

| 传感器数据处理 | Decision Transformer | OpenClaw 架构 |
|:---:|:---:|:---:|
| ![Case 1](docs/images/case-sensor.png) | ![Case 2](docs/images/case-decision-transformer.png) | ![Case 3](docs/images/case-openclaw.png) |

---

## 环境准备

### 1. 安装 Obsidian（推荐）

[Obsidian](https://obsidian.md) 是一款免费笔记工具，原生支持 Excalidraw 插件。

1. 下载：https://obsidian.md/download
2. 创建或打开一个 Vault（笔记库）

### 2. 安装 Excalidraw 插件

1. 打开 Obsidian → 设置 → 第三方插件
2. 关闭安全模式（如果还没关）
3. 点击浏览 → 搜索 "Excalidraw"
4. 安装 **Excalidraw**（作者：Zsolt Viczián）
5. 启用插件

### 3. 查看生成的图表

- 将 `.excalidraw` 文件放入 Vault 目录
- 在 Obsidian 中点击即可打开编辑
- 或访问 https://excalidraw.com 在线打开

### 不用 Obsidian？

`.excalidraw` 文件是标准 JSON，也可以用：
- [excalidraw.com](https://excalidraw.com) — 在线编辑器
- VS Code Excalidraw 扩展
- 任何支持 Excalidraw 格式的工具

---

## 快速开始

### 作为 Claude Code Skill

```bash
git clone https://github.com/AlanYu04/excalidraw-generator-skill ~/.claude/skills/excalidraw-generator
```

然后直接对 Claude 说：

> *"画一个 Transformer 架构图 — vivid 风格，hachure 填充，roughness 1"*

### 作为 Python 库

```python
from core.engine import labeled_rect, labeled_ellipse, arrow, bind_arrow, save

# 1. 创建形状
start = labeled_ellipse(200, 20, 100, 50, "开始", fill="#d0f0c0")
step  = labeled_rect(150, 100, 200, 60, "处理数据")
end   = labeled_ellipse(200, 200, 100, 50, "结束", fill="#d0f0c0")

# 2. 用箭头连接
a1 = bind_arrow(arrow(250, 70, 0, 30), start[0], step[0])
a2 = bind_arrow(arrow(250, 160, 0, 40), step[0], end[0])

# 3. 保存
elements = [*start, *step, *end, a1, a2]
save("flow.excalidraw", elements)
```

---

## 图表类型

### 柱状图

```python
from core.charts import bar_chart

elements = bar_chart(
    x=50, y=100,
    data={"React": 85, "Vue": 72, "Angular": 58},
    title="框架流行度",
    bar_color="#a5d8ff",
    show_values=True,
    show_grid=True,
)
```

### 横向柱状图

```python
from core.charts import horizontal_bar_chart

elements = horizontal_bar_chart(
    x=50, y=50,
    data={"训练": 120, "推理": 85, "评估": 45},
    title="耗时分布（分钟）",
)
```

### 折线图（多系列）

```python
from core.charts import line_chart

elements = line_chart(
    x=50, y=50,
    data={"收入": [10, 25, 35, 50, 70], "成本": [8, 15, 20, 30, 35]},
    labels=["Q1", "Q2", "Q3", "Q4", "Q5"],
    title="收入 vs 成本",
    show_points=True, show_legend=True,
)
```

### 饼图（含甜甜圈模式）

```python
from core.charts import pie_chart

elements = pie_chart(
    x=100, y=100,
    data={"移动端": 45, "桌面端": 35, "平板": 20},
    title="流量来源",
    donut=True, donut_radius=50, show_percentages=True,
)
```

---

## 内置图标（39 个）

```python
from core.icons import icon, list_icons

print(list_icons())  # 查看所有图标
elements = icon("database", x=100, y=50, scale=1.0)
```

| 分类 | 图标名称 |
|------|---------|
| **通用（10）** | `database` `user` `cloud` `server` `gear` `document` `shield` `arrow-right` `check` `warning` |
| **ML/AI（12）** | `transformer-block` `attention-head` `embedding-layer` `feedforward` `encoder` `decoder` `loss-function` `optimizer` `gpu` `robot` `brain` `neural-net` |
| **工具（17）** | `cube` `data-pipeline` `matrix` `lock` `wifi` `heart` `star` `lightning` `clock` `magnifier` `fire` `globe` `chat` `api` `terminal` `folder` `key` |

---

## 样式预设

| 预设 | 字体 | 粗糙度 | 填充 | 适用场景 |
|------|------|--------|------|---------|
| **Vivid** | Cascadia (3) | 1 | solid | 丰富多彩、细节丰富 |
| **Clean** | Helvetica (2) | 0 | solid | 简约精确 |
| **Sketch** | Virgil (1) | 2 | hachure | 手绘风格 |

---

## 输出格式

```python
from core.engine import save

save("diagram.excalidraw", elements)      # 纯 JSON
save("diagram.excalidraw.md", elements)   # Obsidian 格式
```

`save()` 根据文件扩展名自动选择格式。

---

## 许可证

[MIT](LICENSE)
