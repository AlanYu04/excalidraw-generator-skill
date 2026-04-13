"""Tests for core/icons.py icon library."""
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
    for el in els:
        assert el["x"] >= 200


def test_icon_respects_scale():
    els_normal = icon("database", x=0, y=0, scale=1.0)
    els_big = icon("database", x=0, y=0, scale=2.0)
    def total_area(els):
        return sum(el.get("width", 0) * el.get("height", 0) for el in els if "width" in el)
    assert total_area(els_big) > total_area(els_normal)


def test_unknown_icon_raises():
    import pytest
    with pytest.raises(ValueError):
        icon("nonexistent_icon", x=0, y=0)


def test_icon_stroke_color():
    els = icon("user", x=0, y=0, stroke="#ff0000")
    for el in els:
        if "strokeColor" in el:
            assert el["strokeColor"] == "#ff0000"
