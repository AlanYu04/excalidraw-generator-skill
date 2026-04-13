# Excalidraw Generator Skill 渐进增强设计文档

**日期：** 2026-04-13
**项目：** AlanYu04/excalidraw-generator-skill
**状态：** 待用户审核

## 背景

本项目是一个 Claude Code Skill，通过 Python 引擎 + builder 函数 + 样式预设来生成 Excalidraw 图表。在同类项目中技术深度最强（对比 ruoningxiong 的纯 SKILL.md 模板方式），但需要在广度和深度上进一步差异化。

### 竞品分析

| 项目 | 关键发现 |
|------|---------|
| ruoningxiong/excalidraw-generator-claude-skill | 纯 SKILL.md 模板教学；仅有矩形/文本/箭头；无可执行代码 |
| zsviczian/excalidraw-mathjax | LaTeX 公式转 SVG 渲染，面向 Obsidian Excalidraw 插件 |
| wictorwilen/fluentui-icons-to-excalidraw | SVG 图标转 Excalidraw 原生元素的流水线（5980+ 图标）；有 Web 展示站 |

### 目标用户

1. **Obsidian + Excalidraw 用户** — 知识工作者、研究者、学生
2. **Claude Code 开发者** — 需要快速生成架构图、流程图等技术图表

## 策略：渐进增强（方案 C）

四个独立可发布的阶段，每阶段交付一个可审核的 `.excalidraw` 演示文件。

---

## 阶段 1：基础补全 + README 重写

**目标：** 补全所有缺失元素类型，新增图标库，重写 README 为专业级别。发布为 v1.1。

### 1.1 新增元素 Builder（`core/engine.py`）

| 函数名 | 元素类型 | 用途 |
|--------|---------|------|
| `diamond()` | 决策节点 | 流程图中的是/否判断分支 |
| `ellipse()` | 终端节点 | 流程图的开始/结束节点 |
| `line()` | 连接线 | 无箭头的直线连接 |
| `group()` | 分组 | 将多个元素编组（统一移动） |
| `frame()` | 画框 | Excalidraw Frame（画布分区） |
| `image_embed()` | 图片 | 嵌入图片元素 |

所有 builder 函数遵循：
- 通过现有 `uid()`/`sd()`/`ts()` 生成唯一 ID/seed/时间戳
- 正确处理 `boundElements`/`containerId` 双向绑定
- 支持 CJK 字体选项（`fontFamily: 5`）
- 返回新 dict（不可变模式，不修改传入参数）

### 1.2 图标库（`core/icons.py`，新建文件）

内置图标集，全部用 Excalidraw 原生元素（线条、椭圆、矩形）绘制，保持手绘风格一致性。

**首批 10 个技术图标：**

| 图标名 | 用途 | 实现方式 |
|--------|------|---------|
| `database` | 数据库圆柱体 | 线条 + 椭圆组合 |
| `user` | 用户人形 | 线条绘制 |
| `cloud` | 云服务 | 椭圆组合 |
| `server` | 服务器 | 矩形 + 装饰线条 |
| `gear` | 设置/引擎 | 线条绘制 |
| `document` | 文档折角 | 矩形 + 折角线条 |
| `shield` | 安全盾牌 | 三角形线条 |
| `arrow-right` | 流程箭头 | 原生箭头 |
| `check` | 完成/成功 | 线条打勾 |
| `warning` | 警告三角 | 三角形线条 |

**使用方式：**
```python
from core.icons import icon
db = icon("database", x=100, y=200, scale=1.5)
```

返回 Excalidraw 元素 dict 列表，可与其他 builder 组合使用。

### 1.3 SKILL.md 更新

- 新增全部 6 种元素的完整 JSON 模板
- 新增决策流程图模式（diamond → 是/否分支）
- 新增垂直布局模式说明
- 更新「常见错误」表格，补充新元素相关陷阱
- 新增图标使用说明章节

### 1.4 README 完全重写

参考 fluentui-icons 的专业风格，结构如下：

```
Badge 墙（Claude Code | Excalidraw | Python | MIT）
一句话标语 + 功能亮点
Demo 展示廊（3 列网格：Vivid | Clean | Sketch）
功能对比表（vs ruoningxiong | vs 手动 JSON | vs Mermaid）
快速开始（安装 → 配置 → 首次使用）
API 参考表（所有 builder 函数）
样式系统（3 种预设 + 自定义 YAML）
贡献指南链接
```

### 1.5 新增示例文件

| 示例文件 | 展示内容 | 使用的新元素 |
|---------|---------|-------------|
| `decision-flow.excalidraw` | 登录决策流程（含分支） | diamond, ellipse |
| `system-arch.excalidraw` | 微服务架构图（含图标） | frame, group, icons |
| `cjk-timeline.excalidraw` | 中文时间线 | 全中文文本 |

### 1.6 阶段 1 审核案例

**演示图：** 一张微服务架构图：
```
[👤 用户图标] → [☁️ 云/负载均衡] → [⚙️ API 网关] → [🗄 数据库图标]
                                                    ↘ [🖥 服务器图标]
```
- 交付一个可在 Excalidraw 编辑器中直接打开的 `.excalidraw` 文件
- 包含图标、菱形决策节点、Frame 分组
- 所有元素可编辑、可移动

---

## 阶段 2：智能布局引擎

**目标：** 用自动布局算法替代手动坐标计算。发布为 v1.2。

### 2.1 新建文件：`core/layout.py`

基于拓扑排序 + 层次化布局的自动布局引擎（类 Dagre 思路）：

**支持的布局方式：**
- 垂直流程（从上到下）
- 水平流程（从左到右）
- 分支/合并流程
- 并行元素网格对齐
- Frame 内感知布局（元素在 Frame 内自动定位）

**使用方式：**
```python
from core.layout import auto_layout

elements = [
    rect("开始", ...),
    diamond("判断", ...),
    rect("是路径", ...),
    rect("否路径", ...),
    rect("结束", ...),
]
connections = [
    ("开始", "判断"),
    ("判断", "是路径", "是"),
    ("判断", "否路径", "否"),
    ("是路径", "结束"),
    ("否路径", "结束"),
]
result = auto_layout(elements, connections, direction="vertical", spacing=80)
```

### 2.2 SKILL.md 更新

- 新增布局触发关键词（用户说"自动布局"、"垂直流程"等）
- 文档化布局 API

### 2.3 阶段 2 审核案例

**演示图：** 用阶段 1 的同一张架构图，以自动布局重新生成。提供并排对比：手动坐标 vs 自动布局。

---

## 阶段 3：LaTeX 数学公式支持

**目标：** 在 Excalidraw 图表中渲染 LaTeX 数学公式。发布为 v1.3。

### 3.1 新建文件：`core/latex.py`

**渲染管线：**
1. LaTeX 字符串 → `latex` + `dvisvgm` → SVG（需要本机安装 LaTeX）
2. SVG → base64 → 嵌入 Excalidraw 的 `files` 字段
3. 生成 `image` 元素引用该 file

**降级方案：** 如果本机未安装 LaTeX，使用 `text_standalone` 以等宽字体显示公式原文。

**使用方式：**
```python
from core.latex import formula

eq1 = formula("E = mc^2", x=200, y=100, font_size=20)
eq2 = formula(r"\int_0^\infty e^{-x^2} dx = \frac{\sqrt{\pi}}{2}", x=200, y=300)
```

### 3.2 阶段 3 审核案例

**演示图：** 一张研究流程图，含公式节点：
```
[输入数据] → [模型: y = β₀ + β₁x + ε] → [损失函数: L = Σ(yᵢ - ŷᵢ)²] → [输出]
```
交付一个 `.excalidraw` 文件，公式以图片形式渲染，可在 Excalidraw 编辑器中查看和移动。

---

## 阶段 4：Web 模板画廊

**目标：** GitHub Pages 展示站，展示模板和示例。发布为 v2.0。

### 4.1 范围

- 纯静态网站（无后端）
- 模板浏览器 + 预览图片
- 一键复制安装命令
- 响应式设计

### 4.2 技术选型

轻量方案：原生 HTML/CSS/JS 或最小化静态生成器。不用 React，无需构建步骤。

### 4.3 阶段 4 审核案例

可访问的 GitHub Pages URL，包含模板画廊页面。

---

## 项目结构变更总览

```
excalidraw-generator/
├── SKILL.md                 # 阶段1: 更新元素模板；阶段2: 新增布局文档
├── README.md                # 阶段1: 完全重写，专业级别
├── core/
│   ├── __init__.py          # 阶段1: 导出新符号
│   ├── engine.py            # 阶段1: 新增 diamond/ellipse/line/group/frame/image_embed
│   ├── layout.py            # 阶段2: 新建 — 自动布局引擎
│   ├── latex.py             # 阶段3: 新建 — LaTeX 公式渲染
│   └── icons.py             # 阶段1: 新建 — 内置图标库
├── styles/                  # 各阶段不变
├── prompts/                 # 阶段1: 更新视觉指南适配新元素
├── examples/                # 阶段1: 3 个新示例；阶段2: 布局演示；阶段3: 公式演示
├── templates/               # 阶段2: 新建 — 预定义图表模板
├── web/                     # 阶段4: 新建 — GitHub Pages 站点
├── assets/                  # 阶段1: 新增 demo 截图
└── docs/                    # 本设计文档
```

## 设计原则

1. **每阶段独立可发布** — 阶段 1 完成不需要阶段 2-4 即可发版
2. **向后兼容** — 新 builder 函数为纯新增，不改现有 API
3. **零运行时依赖**（阶段 3 LaTeX 除外）— 保持纯 Python + Claude Code Skill 的轻量特性
4. **每个功能都有可审核的演示** — 每阶段交付具体 `.excalidraw` 文件
5. **不可变数据模式** — 所有 builder 返回新 dict，不修改传入参数

## 依赖要求

- 阶段 1：无新依赖（纯 Python）
- 阶段 2：无新依赖（纯 Python 数学/图算法）
- 阶段 3：可选系统依赖 — `latex` + `dvisvgm`（未安装时降级为纯文本）
- 阶段 4：静态站点，无服务端依赖
