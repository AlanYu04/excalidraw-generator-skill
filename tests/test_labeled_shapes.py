"""Tests for labeled_diamond and labeled_ellipse builders."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.engine import labeled_diamond, labeled_ellipse


def test_labeled_diamond_returns_two_elements():
    els = labeled_diamond(0, 0, 160, 100, "Yes?")
    assert len(els) == 2
    d, t = els
    assert d["type"] == "diamond"
    assert t["type"] == "text"


def test_labeled_diamond_container_binding():
    els = labeled_diamond(0, 0, 160, 100, "OK")
    d, t = els
    assert t["containerId"] == d["id"]
    assert any(b["id"] == t["id"] for b in d["boundElements"])


def test_labeled_diamond_dimensions():
    els = labeled_diamond(10, 20, 160, 100, "X")
    d = els[0]
    assert d["x"] == 10
    assert d["y"] == 20
    assert d["width"] == 160
    assert d["height"] == 100


def test_labeled_ellipse_returns_two_elements():
    els = labeled_ellipse(0, 0, 80, 80, "Start")
    assert len(els) == 2
    e, t = els
    assert e["type"] == "ellipse"
    assert t["type"] == "text"


def test_labeled_ellipse_container_binding():
    els = labeled_ellipse(0, 0, 80, 80, "End")
    e, t = els
    assert t["containerId"] == e["id"]
    assert any(b["id"] == t["id"] for b in e["boundElements"])


def test_labeled_ellipse_accepts_fill_and_stroke():
    els = labeled_ellipse(0, 0, 100, 60, "Go", fill="#a5d8ff", stroke="#1971c2")
    e = els[0]
    assert e["backgroundColor"] == "#a5d8ff"
    assert e["strokeColor"] == "#1971c2"


def test_labeled_diamond_accepts_cjk():
    els = labeled_diamond(0, 0, 160, 100, "通过?", font_family=5)
    t = els[1]
    assert t["text"] == "通过?"
    assert t["fontFamily"] == 5
