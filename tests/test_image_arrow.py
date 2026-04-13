"""Tests for image_embed(), bind_arrow(), connect(), arrow abs coords, save()."""
import sys, os, tempfile, json
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.engine import (
    image_embed, bind_arrow, arrow, rect, line, connect,
    save_excalidraw, save_obsidian_md, save, text_standalone,
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
    assert a["x"] == 100  # right edge of r1
    assert a["y"] == 25   # vertical center of r1
    assert a["points"] == [[0, 0], [100, 0]]  # dx=200-100=100, dy=0


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
