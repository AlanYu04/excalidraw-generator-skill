"""Tests for image_embed() and bind_arrow()."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.engine import image_embed, bind_arrow, arrow, rect


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
