"""Tests for image_embed(), bind_arrow(), connect(), arrow abs coords, save(), auto_labeled_rect()."""
import sys, os, tempfile, json
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.engine import (
    image_embed, bind_arrow, arrow, rect, line, connect,
    save_excalidraw, save_obsidian_md, save, text_standalone,
    auto_labeled_rect, estimate_text_width,
)


def test_image_embed_returns_element_and_file_entry():
    tiny_png = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8/5+hHgAHggJ/PchI7wAAAABJRU5ErkJggg=="
    el, file_entry = image_embed(100, 100, 200, 150, tiny_png, mime="image/png")
    assert el["type"] == "image"
    assert el["width"] == 200
    assert el["height"] == 150
    assert el["fileId"] in file_entry
    assert file_entry[el["fileId"]]["mimeType"] == "image/png"


def test_image_embed_position():
    tiny_png = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8/5+hHgAHggJ/PchI7wAAAABJRU5ErkJggg=="
    el, _ = image_embed(50, 75, 200, 150, tiny_png)
    assert el["x"] == 50
    assert el["y"] == 75


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
    assert a["startBinding"] is None
    assert bound["startBinding"] is not None


def test_bind_arrow_custom_gap():
    r1 = rect(0, 0, 100, 50)
    r2 = rect(200, 0, 100, 50)
    a = arrow(100, 25, 100, 0)
    bound = bind_arrow(a, r1, r2, gap=5)
    assert bound["startBinding"]["gap"] == 5
    assert bound["endBinding"]["gap"] == 5


def test_bind_arrow_updates_bound_elements():
    r1 = rect(0, 0, 100, 50)
    r2 = rect(200, 0, 100, 50)
    a = arrow(100, 25, 100, 0)
    bind_arrow(a, r1, r2)
    assert any(b["id"] == a["id"] for b in r1["boundElements"])
    assert any(b["id"] == a["id"] for b in r2["boundElements"])


def test_connect_creates_bound_arrow():
    r1 = rect(0, 0, 100, 50)
    r2 = rect(200, 0, 100, 50)
    a = connect(r1, r2)
    assert a["type"] == "arrow"
    assert a["startBinding"]["elementId"] == r1["id"]
    assert a["endBinding"]["elementId"] == r2["id"]


def test_connect_updates_bound_elements():
    r1 = rect(0, 0, 100, 50)
    r2 = rect(200, 0, 100, 50)
    a = connect(r1, r2)
    assert any(b["id"] == a["id"] for b in r1["boundElements"])
    assert any(b["id"] == a["id"] for b in r2["boundElements"])


def test_connect_arrow_coordinates():
    r1 = rect(0, 0, 100, 50)
    r2 = rect(200, 0, 100, 50)
    a = connect(r1, r2)
    # connect() now uses actual center-to-center direction
    assert a["x"] == 50   # center x of r1
    assert a["y"] == 25   # vertical center of r1
    assert a["points"] == [[0, 0], [200, 0]]  # horizontal direction to r2 center
    assert a["startBinding"]["elementId"] == r1["id"]
    assert a["endBinding"]["elementId"] == r2["id"]


def test_connect_vertical_direction():
    r1 = rect(100, 0, 100, 50)
    r2 = rect(100, 200, 100, 50)
    a = connect(r1, r2)
    # Centers: (150, 25) -> (150, 225), so dx=0, dy=200
    assert a["points"] == [[0, 0], [0, 200]]


def test_connect_diagonal_direction():
    r1 = rect(0, 0, 100, 50)
    r2 = rect(200, 100, 100, 50)
    a = connect(r1, r2)
    # Centers: (50, 25) -> (250, 125), so dx=200, dy=100
    assert a["points"] == [[0, 0], [200, 100]]


def test_connect_same_center_fallback():
    r1 = rect(0, 0, 100, 100)
    r2 = rect(0, 0, 100, 100)
    a = connect(r1, r2)
    # Should not be zero vector -- falls back to dx=1
    assert a["points"][1][0] != 0 or a["points"][1][1] != 0


def test_bind_arrow_clamps_explicit_focus_values():
    r1 = rect(0, 0, 100, 50)
    r2 = rect(200, 0, 100, 50)
    a = arrow(100, 25, 100, 0)
    bound = bind_arrow(a, r1, r2, start_focus=-2, end_focus=3)
    assert bound["startBinding"]["focus"] == -1.0
    assert bound["endBinding"]["focus"] == 1.0


def test_connect_distributes_end_focus_on_wide_target():
    target = rect(200, 200, 600, 40)
    sources = [
        rect(40, 0, 120, 60),
        rect(440, 0, 120, 60),
        rect(840, 0, 120, 60),
    ]
    arrows = [connect(src, target) for src in sources]
    focuses = [round(arw["endBinding"]["focus"], 4) for arw in arrows]
    assert len(set(focuses)) == 3
    assert min(focuses) < 0 < max(focuses)


def test_auto_labeled_rect_sizes_from_text():
    els = auto_labeled_rect(0, 0, "Hello", padding=10, fs=16)
    tw = estimate_text_width("Hello", 16)
    assert els[0]["width"] >= tw + 20  # 2 * padding
    assert els[0]["height"] >= 16 * 1.25 + 20  # text height + 2 * padding


def test_auto_labeled_rect_min_width():
    els = auto_labeled_rect(0, 0, "Hi", padding=4, fs=10, min_width=200)
    assert els[0]["width"] == 200


def test_auto_labeled_rect_min_height():
    els = auto_labeled_rect(0, 0, "Hi", padding=4, fs=10, min_height=60)
    assert els[0]["height"] == 60


def test_auto_labeled_rect_cjk():
    els = auto_labeled_rect(0, 0, "数据处理流程", padding=8, fs=14)
    tw = estimate_text_width("数据处理流程", 14)
    assert els[0]["width"] >= tw + 16  # 2 * padding


def test_arrow_absolute_coords():
    a = arrow(10, 20, x2=110, y2=70)
    assert a["x"] == 10
    assert a["y"] == 20
    assert a["points"] == [[0, 0], [100, 50]]


def test_arrow_relative_unchanged():
    a = arrow(10, 20, 100, 50)
    assert a["points"] == [[0, 0], [100, 50]]


def test_line_absolute_coords():
    l = line(10, 20, x2=110, y2=70)
    assert l["x"] == 10
    assert l["y"] == 20
    assert l["points"] == [[0, 0], [100, 50]]


def test_save_auto_obsidian_md():
    els = [text_standalone(0, 0, "test")]
    with tempfile.NamedTemporaryFile(suffix=".excalidraw.md", delete=False) as f:
        path = f.name
    try:
        save(path, els)
        with open(path) as f:
            content = f.read()
        assert "excalidraw-plugin: raw" in content
        assert "## Drawing" in content
    finally:
        os.unlink(path)


def test_save_obsidian_md_collects_embedded_files():
    tiny_png = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8/5+hHgAHggJ/PchI7wAAAABJRU5ErkJggg=="
    el, files = image_embed(10, 20, 32, 24, tiny_png)
    el["_files"] = files
    with tempfile.NamedTemporaryFile(suffix=".excalidraw.md", delete=False) as f:
        path = f.name
    try:
        save_obsidian_md(path, [el])
        with open(path, encoding="utf-8") as f:
            content = f.read()
        payload = content.split("```json\n", 1)[1].split("\n```", 1)[0]
        data = json.loads(payload)
        assert data["files"]
        assert el["fileId"] in data["files"]
        assert "_files" not in data["elements"][0]
    finally:
        os.unlink(path)


def test_save_auto_excalidraw_json():
    els = [text_standalone(0, 0, "test")]
    with tempfile.NamedTemporaryFile(suffix=".excalidraw", delete=False) as f:
        path = f.name
    try:
        save(path, els)
        with open(path) as f:
            data = json.load(f)
        assert data["type"] == "excalidraw"
        assert len(data["elements"]) == 1
    finally:
        os.unlink(path)
