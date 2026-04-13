# P1 基础补全实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**目标：** 补全缺失元素类型、新增图标库、重写 README，发布为 v1.1

**架构：** 在现有 `core/engine.py` 基础上新增 `labeled_diamond`/`labeled_ellipse`/`group`/`frame`/`image_embed`/`bind_arrow` builder 函数，新建 `core/icons.py` 图标库模块。所有新函数遵循现有不可变模式（返回新 dict）。

**技术栈：** Python 3.8+，pytest，无新依赖

---

### Task 1: 搭建测试基础设施

**Files:**
- Create: `tests/__init__.py`
- Create: `tests/test_engine.py`
- Create: `pytest.ini`

- [ ] **Step 1: 创建 pytest 配置**

```ini
# pytest.ini
[pytest]
testpaths = tests
python_files = test_*.py
python_functions = test_*
```

- [ ] **Step 2: 创建测试目录和初始测试文件**

```python
# tests/__init__.py
# (空文件)
```

```python
# tests/test_engine.py
"""测试现有 engine builder 函数的基本行为。"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.engine import rect, labeled_rect, text_standalone, arrow, ellipse, diamond, line, uid, sd, ts


def test_rect_returns_dict_with_correct_type():
    r = rect(0, 0, 100, 50)
    assert r["type"] == "rectangle"
    assert r["width"] == 100
    assert r["height"] == 50


def test_labeled_rect_returns_two_elements():
    els = labeled_rect(0, 0, 100, 50, "Hello")
    assert len(els) == 2
    assert els[0]["type"] == "rectangle"
    assert els[1]["type"] == "text"
    assert els[1]["containerId"] == els[0]["id"]
    assert els[0]["boundElements"][0]["id"] == els[1]["id"]


def test_diamond_returns_dict_with_correct_type():
    d = diamond(0, 0, 80, 80)
    assert d["type"] == "diamond"


def test_ellipse_returns_dict_with_correct_type():
    e = ellipse(0, 0, 60, 60)
    assert e["type"] == "ellipse"


def test_arrow_returns_dict_with_points():
    a = arrow(0, 0, 100, 0)
    assert a["type"] == "arrow"
    assert a["points"] == [[0, 0], [100, 0]]
    assert a["endArrowhead"] == "arrow"


def test_uid_generates_unique_ids():
    id1 = uid()
    id2 = uid()
    assert id1 != id2
```

- [ ] **Step 3: 运行测试确认全部通过**

运行: `cd /Users/alan/.claude/skills/excalidraw-generator && python -m pytest tests/test_engine.py -v`
预期: 6 个测试全部 PASS

---

### Task 2: 新增 `labeled_diamond()` 和 `labeled_ellipse()`

**Files:**
- Modify: `core/engine.py`
- Modify: `core/__init__.py`
- Create: `tests/test_labeled_shapes.py`

- [ ] **Step 1: 写失败测试**

```python
# tests/test_labeled_shapes.py
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.engine import labeled_diamond, labeled_ellipse


def test_labeled_diamond_returns_two_elements():
    els = labeled_diamond(0, 0, 120, 80, "Yes?")
    assert len(els) == 2
    assert els[0]["type"] == "diamond"
    assert els[1]["type"] == "text"
    assert els[1]["containerId"] == els[0]["id"]
    assert els[0]["boundElements"][0]["id"] == els[1]["id"]


def test_labeled_diamond_text_content():
    els = labeled_diamond(0, 0, 120, 80, "条件判断")
    assert els[1]["text"] == "条件判断"
    assert els[1]["originalText"] == "条件判断"


def test_labeled_ellipse_returns_two_elements():
    els = labeled_ellipse(0, 0, 100, 60, "Start")
    assert len(els) == 2
    assert els[0]["type"] == "ellipse"
    assert els[1]["type"] == "text"
    assert els[1]["containerId"] == els[0]["id"]
    assert els[0]["boundElements"][0]["id"] == els[1]["id"]


def test_labeled_ellipse_text_content():
    els = labeled_ellipse(0, 0, 100, 60, "结束")
    assert els[1]["text"] == "结束"
```

- [ ] **Step 2: 运行测试确认失败**

运行: `cd /Users/alan/.claude/skills/excalidraw-generator && python -m pytest tests/test_labeled_shapes.py -v`
预期: FAIL — `ImportError: cannot import name 'labeled_diamond'`

- [ ] **Step 3: 在 `core/engine.py` 中实现**

在 `diamond()` 函数后面添加:

```python
def labeled_diamond(x, y, w, h, label, fill="transparent", stroke="#1e1e1e",
                    sw=2, fs=16, label_color=None, roughness=1, font_family=3,
                    fill_style="solid"):
    if label_color is None: label_color = stroke
    did, tid = uid(), uid()
    d = {
        "id": did, "type": "diamond",
        "x": x, "y": y, "width": w, "height": h,
        "angle": 0, "strokeColor": stroke, "backgroundColor": fill,
        "fillStyle": fill_style, "strokeWidth": sw, "strokeStyle": "solid",
        "roughness": roughness, "opacity": 100, "groupIds": [],
        "roundness": {"type": 2}, "seed": sd(), "version": 1,
        "versionNonce": sd(), "isDeleted": False,
        "boundElements": [{"id": tid, "type": "text"}],
        "updated": ts(), "link": None, "locked": False
    }
    t = {
        "id": tid, "type": "text",
        "x": x + 4, "y": y + 4, "width": w - 8, "height": h - 8,
        "angle": 0, "strokeColor": label_color, "backgroundColor": "transparent",
        "fillStyle": "solid", "strokeWidth": 2, "strokeStyle": "solid",
        "roughness": 0, "opacity": 100, "groupIds": [],
        "roundness": None, "seed": sd(), "version": 1,
        "versionNonce": sd(), "isDeleted": False, "boundElements": [],
        "updated": ts(), "link": None, "locked": False,
        "text": label, "fontSize": fs, "fontFamily": font_family,
        "textAlign": "center", "verticalAlign": "middle",
        "containerId": did, "originalText": label, "lineHeight": 1.25
    }
    return [d, t]
```

在 `ellipse()` 函数后面添加:

```python
def labeled_ellipse(x, y, w, h, label, fill="transparent", stroke="#1e1e1e",
                    sw=2, fs=16, label_color=None, roughness=1, font_family=3,
                    fill_style="solid"):
    if label_color is None: label_color = stroke
    eid, tid = uid(), uid()
    e = {
        "id": eid, "type": "ellipse",
        "x": x, "y": y, "width": w, "height": h,
        "angle": 0, "strokeColor": stroke, "backgroundColor": fill,
        "fillStyle": fill_style, "strokeWidth": sw, "strokeStyle": "solid",
        "roughness": roughness, "opacity": 100, "groupIds": [],
        "roundness": {"type": 2}, "seed": sd(), "version": 1,
        "versionNonce": sd(), "isDeleted": False,
        "boundElements": [{"id": tid, "type": "text"}],
        "updated": ts(), "link": None, "locked": False
    }
    t = {
        "id": tid, "type": "text",
        "x": x + 4, "y": y + 4, "width": w - 8, "height": h - 8,
        "angle": 0, "strokeColor": label_color, "backgroundColor": "transparent",
        "fillStyle": "solid", "strokeWidth": 2, "strokeStyle": "solid",
        "roughness": 0, "opacity": 100, "groupIds": [],
        "roundness": None, "seed": sd(), "version": 1,
        "versionNonce": sd(), "isDeleted": False, "boundElements": [],
        "updated": ts(), "link": None, "locked": False,
        "text": label, "fontSize": fs, "fontFamily": font_family,
        "textAlign": "center", "verticalAlign": "middle",
        "containerId": eid, "originalText": label, "lineHeight": 1.25
    }
    return [e, t]
```

- [ ] **Step 4: 更新 `core/__init__.py` 导出**

在 import 和 `__all__` 中添加 `labeled_diamond` 和 `labeled_ellipse`。

- [ ] **Step 5: 运行测试确认通过**

运行: `cd /Users/alan/.claude/skills/excalidraw-generator && python -m pytest tests/ -v`
预期: 全部 PASS

---

### Task 3: 新增 `group()` 和 `frame()` builder

**Files:**
- Modify: `core/engine.py`
- Modify: `core/__init__.py`
- Create: `tests/test_group_frame.py`

- [ ] **Step 1: 写失败测试**

```python
# tests/test_group_frame.py
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.engine import group, frame, rect, labeled_rect


def test_group_assigns_group_id_to_elements():
    r1 = rect(0, 0, 100, 50)
    r2 = rect(0, 60, 100, 50)
    grouped = group([r1, r2])
    gid = grouped[0]["groupIds"][-1]
    assert len(gid) > 0
    assert grouped[1]["groupIds"][-1] == gid


def test_group_does_not_mutate_originals():
    r1 = rect(0, 0, 100, 50)
    original_groups = list(r1["groupIds"])
    group([r1])
    assert r1["groupIds"] == original_groups


def test_frame_returns_dict_with_correct_type():
    f = frame(0, 0, 500, 400, "模块A")
    assert f["type"] == "frame"
    assert f["name"] == "模块A"
    assert f["width"] == 500
```

- [ ] **Step 2: 运行测试确认失败**

运行: `cd /Users/alan/.claude/skills/excalidraw-generator && python -m pytest tests/test_group_frame.py -v`
预期: FAIL — `ImportError: cannot import name 'group'`

- [ ] **Step 3: 在 `core/engine.py` 中实现**

在文件末尾 `_build_scene` 之前添加:

```python
def group(elements):
    """将元素编组，返回新元素列表（不修改原始元素）。"""
    gid = uid()
    result = []
    for el in elements:
        new_el = dict(el)
        new_el["groupIds"] = list(el.get("groupIds", [])) + [gid]
        result.append(new_el)
    return result


def frame(x, y, w, h, name="Frame", stroke="#1e1e1e", sw=2):
    return {
        "id": uid(), "type": "frame",
        "x": x, "y": y, "width": w, "height": h,
        "angle": 0, "strokeColor": stroke, "backgroundColor": "transparent",
        "fillStyle": "solid", "strokeWidth": sw, "strokeStyle": "solid",
        "roughness": 0, "opacity": 100, "groupIds": [],
        "roundness": None, "seed": sd(), "version": 1,
        "versionNonce": sd(), "isDeleted": False, "boundElements": [],
        "updated": ts(), "link": None, "locked": False,
        "name": name
    }
```

- [ ] **Step 4: 更新 `core/__init__.py` 导出 `group` 和 `frame`**

- [ ] **Step 5: 运行测试确认通过**

运行: `cd /Users/alan/.claude/skills/excalidraw-generator && python -m pytest tests/ -v`
预期: 全部 PASS

---

### Task 4: 新增 `image_embed()` 和 `bind_arrow()`

**Files:**
- Modify: `core/engine.py`
- Modify: `core/__init__.py`
- Create: `tests/test_image_arrow.py`

- [ ] **Step 1: 写失败测试**

```python
# tests/test_image_arrow.py
import sys, os, base64
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.engine import image_embed, bind_arrow, arrow, rect


def test_image_embed_returns_element_and_file_entry():
    # 1x1 白色 PNG 的 base64
    tiny_png = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8/5+hHgAHggJ/PchI7wAAAABJRU5ErkJggg=="
    el, file_entry = image_embed(100, 100, 200, 150, tiny_png, mime="image/png")
    assert el["type"] == "image"
    assert el["width"] == 200
    assert el["height"] == 150
    assert el["fileId"] in file_entry
    assert file_entry[el["fileId"]]["mimeType"] == "image/png"


def test_bind_arrow_sets_bindings():
    r1 = rect(0, 0, 100, 50)
    r2 = rect(200, 0, 100, 50)
    a = arrow(100, 25, 100, 0)
    bound = bind_arrow(a, r1, r2)
    assert bound["startBinding"]["elementId"] == r1["id"]
    assert bound["endBinding"]["elementId"] == r2["id"]


def test_bind_arrow_does_not_mutate_original():
    r1 = rect(0, 0, 100, 50)
    r2 = rect(200, 0, 100, 50)
    a = arrow(100, 25, 100, 0)
    bound = bind_arrow(a, r1, r2)
    assert a["startBinding"] is None  # 原始未变
    assert bound["startBinding"] is not None
```

- [ ] **Step 2: 运行测试确认失败**

运行: `cd /Users/alan/.claude/skills/excalidraw-generator && python -m pytest tests/test_image_arrow.py -v`
预期: FAIL — `ImportError`

- [ ] **Step 3: 在 `core/engine.py` 中实现**

```python
def image_embed(x, y, w, h, base64_data, mime="image/png"):
    """创建图片元素和对应的 files 条目。返回 (element_dict, files_dict)。"""
    file_id = uid()
    el = {
        "id": uid(), "type": "image",
        "x": x, "y": y, "width": w, "height": h,
        "angle": 0, "strokeColor": "transparent", "backgroundColor": "transparent",
        "fillStyle": "solid", "strokeWidth": 0, "strokeStyle": "solid",
        "roughness": 0, "opacity": 100, "groupIds": [],
        "roundness": None, "seed": sd(), "version": 1,
        "versionNonce": sd(), "isDeleted": False, "boundElements": [],
        "updated": ts(), "link": None, "locked": False,
        "fileId": file_id, "status": "saved", "scale": [1, 1]
    }
    file_entry = {
        file_id: {
            "mimeType": mime,
            "id": file_id,
            "dataURL": f"data:{mime};base64,{base64_data}",
            "created": ts()
        }
    }
    return el, file_entry


def bind_arrow(arrow_el, start_el, end_el, gap=2):
    """绑定箭头到起止元素，返回新箭头（不修改原始）。"""
    new_arrow = dict(arrow_el)
    new_arrow["startBinding"] = {
        "elementId": start_el["id"],
        "focus": 0,
        "gap": gap,
        "fixedPoint": None
    }
    new_arrow["endBinding"] = {
        "elementId": end_el["id"],
        "focus": 0,
        "gap": gap,
        "fixedPoint": None
    }
    return new_arrow
```

- [ ] **Step 4: 更新 `core/__init__.py` 导出 `image_embed` 和 `bind_arrow`**

- [ ] **Step 5: 更新 `_build_scene` 支持 files 参数**

修改 `core/engine.py` 中的 `_build_scene`、`save_excalidraw`、`save_obsidian_md`:

```python
def _build_scene(elements, bg="#ffffff", files=None):
    return {
        "type": "excalidraw", "version": 2,
        "source": "https://excalidraw.com",
        "elements": elements,
        "appState": {"viewBackgroundColor": bg, "gridSize": None},
        "files": files or {}
    }

def save_excalidraw(filepath, elements, bg="#ffffff", files=None):
    scene = _build_scene(elements, bg, files)
    # ... 其余不变

def save_obsidian_md(filepath, elements, bg="#ffffff", files=None):
    scene = _build_scene(elements, bg, files)
    # ... 其余不变
```

- [ ] **Step 6: 运行测试确认通过**

运行: `cd /Users/alan/.claude/skills/excalidraw-generator && python -m pytest tests/ -v`
预期: 全部 PASS

---

### Task 5: 创建 `core/icons.py` 图标库

**Files:**
- Create: `core/icons.py`
- Create: `tests/test_icons.py`

- [ ] **Step 1: 写失败测试**

```python
# tests/test_icons.py
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.icons import icon, list_icons


def test_list_icons_returns_all_10():
    names = list_icons()
    assert len(names) >= 10
    assert "database" in names
    assert "user" in names
    assert "cloud" in names


def test_icon_returns_list_of_elements():
    els = icon("database", x=100, y=100)
    assert isinstance(els, list)
    assert len(els) > 0
    for el in els:
        assert "type" in el
        assert "x" in el


def test_icon_respects_position():
    els = icon("database", x=200, y=300)
    # 所有元素的 x 应该 >= 200（基于偏移）
    for el in els:
        assert el["x"] >= 200


def test_icon_respects_scale():
    els_normal = icon("database", x=0, y=0, scale=1.0)
    els_big = icon("database", x=0, y=0, scale=2.0)
    # 放大后的元素尺寸应该更大
    def total_area(els):
        return sum(el.get("width", 0) * el.get("height", 0) for el in els if "width" in el)
    assert total_area(els_big) > total_area(els_normal)


def test_unknown_icon_raises():
    import pytest
    with pytest.raises(ValueError):
        icon("nonexistent_icon", x=0, y=0)
```

- [ ] **Step 2: 运行测试确认失败**

运行: `cd /Users/alan/.claude/skills/excalidraw-generator && python -m pytest tests/test_icons.py -v`
预期: FAIL — `ModuleNotFoundError`

- [ ] **Step 3: 创建 `core/icons.py`**

创建文件 `core/icons.py`，包含:
- `list_icons()` 函数返回所有可用图标名
- `icon(name, x, y, scale=1.0, stroke="#1e1e1e", sw=2, roughness=1)` 函数
- 10 个图标定义函数（`_icon_database`, `_icon_user`, `_icon_cloud` 等）
- 每个图标用 `line()`, `ellipse()`, `rect()` 等原生元素组合绘制
- 所有坐标相对于 (x, y) 偏移，支持 scale 缩放

图标实现要点:
- `database`: 上下两个椭圆 + 两条竖线（圆柱体）
- `user`: 头部圆 + 身体弧线
- `cloud`: 3 个重叠椭圆
- `server`: 矩形 + 3 条水平装饰线
- `gear`: 圆 + 8 条短线（齿轮齿）
- `document`: 矩形 + 右上角折角线
- `shield`: 5 点多边形线条
- `arrow-right`: 原生 arrow 元素
- `check`: 两条线组成勾
- `warning`: 三角形 + 感叹号线

- [ ] **Step 4: 更新 `core/__init__.py`**

添加:
```python
from .icons import icon, list_icons
```

并在 `__all__` 中添加 `"icon"`, `"list_icons"`。

- [ ] **Step 5: 运行测试确认通过**

运行: `cd /Users/alan/.claude/skills/excalidraw-generator && python -m pytest tests/ -v`
预期: 全部 PASS

---

### Task 6: 创建 3 个新示例文件

**Files:**
- Create: `examples/generate_p1_demos.py`
- 输出: `examples/decision-flow.excalidraw`
- 输出: `examples/system-arch.excalidraw`
- 输出: `examples/cjk-timeline.excalidraw`

- [ ] **Step 1: 编写 `examples/generate_p1_demos.py`**

脚本包含 3 个函数:

1. `demo_decision_flow()` — 登录决策流程图:
   - `labeled_ellipse("开始")` → `labeled_rect("输入用户名密码")` → `labeled_diamond("验证通过?")` → 是: `labeled_rect("进入主页")` → `labeled_ellipse("结束")` / 否: `labeled_rect("显示错误")` → 回到输入
   - 使用 `bind_arrow()` 绑定箭头
   - 垂直布局

2. `demo_system_arch()` — 微服务架构图:
   - `frame("前端层")` 包含 `icon("user")` + `labeled_rect("Web App")`
   - `frame("服务层")` 包含 `icon("cloud")` + `icon("gear")` + `labeled_rect("API Gateway")` + `labeled_rect("Auth Service")`
   - `frame("数据层")` 包含 `icon("database")` + `icon("server")`
   - 使用 `group()` 编组相关元素
   - 水平布局

3. `demo_cjk_timeline()` — 中文项目时间线:
   - 水平时间轴线
   - 4 个里程碑: "需求分析" → "系统设计" → "开发实现" → "测试上线"
   - 全中文文本，`fontFamily=5`

- [ ] **Step 2: 运行脚本生成示例文件**

运行: `cd /Users/alan/.claude/skills/excalidraw-generator && python examples/generate_p1_demos.py`
预期: 生成 3 个 `.excalidraw` 文件

- [ ] **Step 3: 验证生成的文件是有效 JSON**

运行: `cd /Users/alan/.claude/skills/excalidraw-generator && python -c "import json; [json.load(open(f'examples/{n}.excalidraw')) for n in ['decision-flow','system-arch','cjk-timeline']]; print('All valid JSON')"` 
预期: "All valid JSON"

---

### Task 7: 更新 SKILL.md

**Files:**
- Modify: `SKILL.md`

- [ ] **Step 1: 在 Step 3 的 builder 函数列表中添加新函数**

添加:
```
labeled_diamond(x, y, w, h, label)              # 带文本的菱形决策节点
labeled_ellipse(x, y, w, h, label)              # 带文本的椭圆/圆
group(elements)                                   # 将元素编组
frame(x, y, w, h, name)                           # 画框分区
image_embed(x, y, w, h, base64_data)             # 嵌入图片
bind_arrow(arrow_el, start_el, end_el)           # 绑定箭头到元素
icon(name, x, y, scale)                           # 内置图标
list_icons()                                       # 列出所有可用图标
```

- [ ] **Step 2: 新增「决策流程图」模式**

在 Step 4 Common Diagram Patterns 中添加决策流程图模式代码示例。

- [ ] **Step 3: 新增「图标使用」章节**

在 SKILL.md 末尾添加图标使用说明和可用图标列表。

---

### Task 8: 重写 README.md

**Files:**
- Modify: `README.md`

- [ ] **Step 1: 重写 README 为专业级别**

结构:
1. Logo + Badge 墙（Claude Code | Excalidraw | Python | MIT | Zero Dependencies）
2. 一句话标语 + 功能亮点列表
3. Demo Gallery（3 列网格截图）
4. 功能对比表（vs ruoningxiong | vs 手动 JSON | vs Mermaid）
5. 快速开始（安装 → 配置 → 首次使用）
6. API 参考表（所有 builder 函数，含新增的）
7. 图标库参考（10 个图标名 + 用途）
8. 样式系统（3 种预设 + 自定义 YAML）
9. 输出格式说明
10. 项目结构（更新后的目录树）
11. License

- [ ] **Step 2: 更新项目结构树**

添加 `core/icons.py`、`tests/` 目录、新示例文件。

---

### Task 9: 最终验证 + 审核交付

**Files:**
- 无新文件

- [ ] **Step 1: 运行全部测试**

运行: `cd /Users/alan/.claude/skills/excalidraw-generator && python -m pytest tests/ -v`
预期: 全部 PASS

- [ ] **Step 2: 运行示例生成脚本**

运行: `cd /Users/alan/.claude/skills/excalidraw-generator && python examples/generate_p1_demos.py`
预期: 3 个 `.excalidraw` 文件生成成功

- [ ] **Step 3: 验证 `.excalidraw` 文件结构**

运行:
```bash
cd /Users/alan/.claude/skills/excalidraw-generator
python -c "
import json
for name in ['decision-flow', 'system-arch', 'cjk-timeline']:
    with open(f'examples/{name}.excalidraw') as f:
        scene = json.load(f)
    print(f'{name}: {len(scene[\"elements\"])} elements, type={scene[\"type\"]}')
    types = set(e['type'] for e in scene['elements'])
    print(f'  element types: {types}')
"
```
预期: 每个文件包含正确的元素类型

- [ ] **Step 4: 交付给用户审核**

交付清单:
- `core/engine.py` — 6 个新 builder 函数
- `core/icons.py` — 10 个内置图标
- `SKILL.md` — 更新模板 + 新模式 + 图标章节
- `README.md` — 完全重写
- `examples/` — 3 个新示例 `.excalidraw` 文件
- `tests/` — 4 个测试文件，覆盖所有新功能

用户需要:
1. 在 Excalidraw 编辑器中打开 3 个示例文件验证效果
2. 确认 README 排版和内容
3. 确认通过后再 git commit
