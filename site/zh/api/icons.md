---
title: 图标
---

# 图标

三种图标系统：39 个内置图标、支持搜索的持久化图标库，以及通过 Gemini API 驱动的 AI 图标生成。

## 内置图标

### `icon`

```python
from core.icons import icon, list_icons

# 列出所有可用的图标名称
print(list_icons())

# 在指定位置放置图标
elements = icon("database", x=100, y=50, scale=1.0, stroke="#1e1e1e", sw=2, roughness=1)
```

| 参数 | 类型 | 默认值 | 说明 |
|-----------|------|---------|-------------|
| `name` | `str` | 必填 | 图标名称（使用 `list_icons()` 查看所有图标） |
| `x` | `float` | `0` | 左上角 X 位置 |
| `y` | `float` | `0` | 左上角 Y 位置 |
| `scale` | `float` | `1.0` | 缩放因子（1.0 = 约 48px） |
| `stroke` | `str` | `"#1e1e1e"` | 描边颜色 |
| `sw` | `int` | `2` | 描边宽度 |
| `roughness` | `int` | `1` | Excalidraw 粗糙度（0、1 或 2） |

返回值：`list[dict]` -- 组成图标的 Excalidraw 元素字典列表。

### `list_icons`

```python
from core.icons import list_icons

names = list_icons()  # 返回所有 39 个图标名称的排序列表
```

返回值：`list[str]` -- 所有可用图标名称的排序列表。

## 通用图标（10 个）

| 图标 | 名称 | 说明 |
|------|------|-------------|
| 圆柱体 | `database` | 数据存储 |
| 人物 | `user` | 用户、参与者 |
| 云 | `cloud` | 云服务 |
| 机架 | `server` | 基础设施 |
| 齿轮 | `gear` | 设置、配置 |
| 文件 | `document` | 文件、页面 |
| 盾牌 | `shield` | 安全 |
| 箭头 | `arrow-right` | 方向 |
| 勾选 | `check` | 批准、完成 |
| 三角形 | `warning` | 警告、注意 |

## ML/AI 图标（12 个）

| 图标 | 名称 | 说明 |
|------|------|-------------|
| 方块 | `transformer-block` | 多头注意力 + FFN |
| 箭头组 | `attention-head` | Q、K、V 汇聚 |
| 网格 | `embedding-layer` | 嵌入矩阵 |
| 堆叠 | `feedforward` | 两层 FFN |
| 方块-E | `encoder` | 编码器堆栈 |
| 方块-D | `decoder` | 解码器堆栈 |
| 曲线 | `loss-function` | 下降的损失曲线 |
| 螺旋 | `optimizer` | 梯度下降 |
| 芯片 | `gpu` | GPU / 加速器 |
| 头部 | `robot` | AI 智能体 |
| 大脑 | `brain` | 智能 |
| 节点 | `neural-net` | 三层网络 |

## 工具图标（18 个）

| 图标 | 名称 | 说明 |
|------|------|-------------|
| 3D 方块 | `cube` | 通用对象 |
| 漏斗 | `data-pipeline` | ETL、数据处理 |
| 网格 | `matrix` | 二维矩阵 |
| 挂锁 | `lock` | 安全、认证 |
| 信号 | `wifi` | 连接 |
| 心形 | `heart` | 健康、收藏 |
| 星形 | `star` | 评分、收藏 |
| 闪电 | `lightning` | 速度、能量 |
| 钟面 | `clock` | 时间、调度 |
| 放大镜 | `magnifier` | 搜索、检查 |
| 火焰 | `fire` | 热门、趋势 |
| 地球 | `globe` | 全球、网络 |
| 气泡 | `chat` | 消息 |
| 括号 | `api` | API 端点 |
| 提示符 | `terminal` | CLI、控制台 |
| 文件夹 | `folder` | 目录 |
| 钥匙 | `key` | 认证 |

## 图标库

保存、加载和搜索存储在 `~/.excalidraw-gen/icons/` 中的自定义图标。

### `save_icon`

```python
from core.icon_library import save_icon

save_icon(
    name="my-server",
    elements=server_elements,
    description="Server with LED indicators",
    tags=["server", "hardware"],
    source="custom",
    source_file=None,
)
```

| 参数 | 类型 | 默认值 | 说明 |
|-----------|------|---------|-------------|
| `name` | `str` | 必填 | 唯一图标名称（用作标识符） |
| `elements` | `list[dict]` | 必填 | Excalidraw 元素字典列表 |
| `description` | `str` | `""` | 用于搜索的文本描述 |
| `tags` | `list[str] \| None` | `None` | 可选标签字符串 |
| `source` | `str` | `"custom"` | 来源（如 `'svg-converted'`、`'ai-generated'`） |
| `source_file` | `str \| None` | `None` | 可选的源文件路径 |

### `load_icon`

```python
from core.icon_library import load_icon

elements = load_icon("my-server", x=200, y=100, scale=1.5)
```

如果图标名称未找到，将抛出 `KeyError` 异常。

### `delete_icon`

```python
from core.icon_library import delete_icon

delete_icon("my-server")
```

### `list_library_icons`

```python
from core.icon_library import list_library_icons

icons = list_library_icons()  # 返回元数据字典列表
```

### `find_icons`

```python
from core.icon_library import find_icons

# TF-IDF 搜索（零依赖）
results = find_icons("server infrastructure", limit=5)

# OpenAI 嵌入搜索（需要 openai 包和 OPENAI_API_KEY）
results = find_icons("server infrastructure", use_embeddings=True)
```

| 参数 | 类型 | 默认值 | 说明 |
|-----------|------|---------|-------------|
| `query` | `str` | 必填 | 搜索查询文本 |
| `limit` | `int` | `5` | 最大结果数量 |
| `use_embeddings` | `bool` | `False` | 为 `True` 时使用 OpenAI 嵌入 |

返回值：`list[dict]` -- 每个结果包含 `name`、`score`、`description`、`tags`。

### `import_excalidrawlib`

```python
from core.icon_library import import_excalidrawlib

imported = import_excalidrawlib(
    filepath="my-library.excalidrawlib",
    descriptions={"icon-1": "First icon"},
    tags_map={"icon-1": ["custom", "imported"]},
    prefix="lib-",
)
```

| 参数 | 类型 | 默认值 | 说明 |
|-----------|------|---------|-------------|
| `filepath` | `str` | 必填 | `.excalidrawlib` 文件路径 |
| `descriptions` | `dict \| None` | `None` | 将项目名称/别名映射到描述 |
| `tags_map` | `dict \| None` | `None` | 将项目名称/别名映射到标签列表 |
| `prefix` | `str` | `""` | 所有导入图标名称的前缀 |

返回值：`list[str]` -- 导入的图标名称别名列表。

## AI 图标生成

通过 Gemini API 生成图标，自动进行 SVG 到 Excalidraw 的转换，并提供 PNG 回退方案。

### `configure`

```python
from core.ai_icons import configure

configure(
    api_url="https://generativelanguage.googleapis.com/v1beta",
    api_key="YOUR_KEY",
    model="gemini-2.0-flash",
)
```

将配置保存到 `~/.excalidraw-gen/config.json`。

### `generate_icon`

```python
from core.ai_icons import generate_icon

elements = generate_icon(
    description="kubernetes pod",
    x=100, y=200,
    scale=1.5,
    stroke="#1e1e1e",
    sw=2,
    roughness=1,
)
```

| 参数 | 类型 | 默认值 | 说明 |
|-----------|------|---------|-------------|
| `description` | `str` | 必填 | 要生成的图标描述 |
| `x` | `float` | `0` | X 位置 |
| `y` | `float` | `0` | Y 位置 |
| `scale` | `float` | `1.0` | 缩放因子 |
| `stroke` | `str` | `"#1e1e1e"` | 描边颜色 |
| `sw` | `int` | `2` | 描边宽度 |
| `roughness` | `int` | `1` | 粗糙度级别 |
| `prompt` | `str \| None` | `None` | 自定义提示模板（支持 `{description}` 占位符） |

返回值：`list[dict]` -- Excalidraw 元素字典。

### `generate_icon_svg`

```python
from core.ai_icons import generate_icon_svg

svg_string = generate_icon_svg(
    description="server rack",
    prompt=None,
    model="gemini-2.0-flash",
)
```

返回值：`str` -- 原始 SVG 字符串。适用于需要自行处理 SVG 的场景。

### `generate_and_save`

```python
from core.ai_icons import generate_and_save

elements = generate_and_save(
    name="k8s-pod",
    description="Kubernetes pod icon",
    tags=["k8s", "container"],
    # generate_icon 的所有关键字参数都会被转发
    x=100, y=50, scale=1.5,
)
```

一次调用即可生成图标并保存到持久化图标库。
