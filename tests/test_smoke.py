"""Smoke tests: verify existing engine functions work."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.engine import (
    rect, text_standalone, labeled_rect, arrow,
    ellipse, diamond, line, numbered_circle,
    save_excalidraw, estimate_text_width, is_cjk, uid,
)


def test_uid_increments():
    a = uid()
    b = uid()
    assert a != b
    assert a.startswith("e")


def test_rect_shape():
    r = rect(10, 20, 100, 50)
    assert r["type"] == "rectangle"
    assert r["x"] == 10
    assert r["width"] == 100


def test_ellipse_shape():
    e = ellipse(0, 0, 80, 60)
    assert e["type"] == "ellipse"


def test_diamond_shape():
    d = diamond(0, 0, 120, 80)
    assert d["type"] == "diamond"


def test_labeled_rect_pair():
    els = labeled_rect(0, 0, 200, 60, "Hello")
    assert len(els) == 2
    assert els[0]["type"] == "rectangle"
    assert els[1]["type"] == "text"
    assert els[1]["containerId"] == els[0]["id"]


def test_arrow_points():
    a = arrow(0, 0, 100, 0)
    assert a["type"] == "arrow"
    assert a["points"] == [[0, 0], [100, 0]]


def test_cjk_detection():
    assert is_cjk("中")
    assert not is_cjk("A")


def test_estimate_text_width():
    assert estimate_text_width("AB", 20) > 0
