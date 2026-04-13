"""Tests for bar chart builder."""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.charts import bar_chart, horizontal_bar_chart


def test_bar_chart_empty_data():
    elements = bar_chart(0, 0, {})
    assert elements == []


def test_bar_chart_basic():
    data = {"A": 10, "B": 20, "C": 15}
    elements = bar_chart(50, 100, data, bar_width=60, max_height=200)
    # Should have: 2 axes + 3 bars + 3 labels + 3 value labels = 11
    assert len(elements) >= 11

    # Check types
    types = [el["type"] for el in elements]
    assert "rectangle" in types
    assert "line" in types
    assert "text" in types


def test_bar_chart_proportions():
    data = {"Small": 10, "Big": 100}
    elements = bar_chart(0, 0, data, bar_width=60, max_height=200)
    rects = [el for el in elements if el["type"] == "rectangle"]
    assert len(rects) == 2
    # "Big" bar should be 10x taller than "Small"
    big_bar = max(rects, key=lambda r: r["height"])
    small_bar = min(rects, key=lambda r: r["height"])
    assert big_bar["height"] > small_bar["height"]


def test_bar_chart_title():
    data = {"X": 1}
    elements = bar_chart(0, 0, data, title="Test Chart")
    texts = [el for el in elements if el["type"] == "text"]
    assert any(el["text"] == "Test Chart" for el in texts)


def test_bar_chart_no_values():
    data = {"A": 10, "B": 20}
    elements = bar_chart(0, 0, data, show_values=False)
    texts = [el for el in elements if el["type"] == "text"]
    # Should have labels but no value texts
    texts_content = [el["text"] for el in texts]
    assert "10" not in texts_content
    assert "20" not in texts_content


def test_bar_chart_grid():
    data = {"A": 50, "B": 100}
    elements_no_grid = bar_chart(0, 0, data, show_grid=False)
    elements_with_grid = bar_chart(0, 0, data, show_grid=True, grid_lines=4)
    # Grid should add extra line + text elements
    assert len(elements_with_grid) > len(elements_no_grid)


def test_bar_chart_custom_colors():
    data = {"A": 10, "B": 20}
    colors = {"A": "#ff0000", "B": "#00ff00"}
    elements = bar_chart(0, 0, data, bar_colors=colors)
    rects = [el for el in elements if el["type"] == "rectangle"]
    assert len(rects) == 2
    fills = {el["backgroundColor"] for el in rects}
    assert "#ff0000" in fills
    assert "#00ff00" in fills


def test_bar_chart_cjk_labels():
    data = {"数据库": 80, "服务器": 65}
    elements = bar_chart(0, 0, data)
    texts = [el for el in elements if el["type"] == "text"]
    assert any(el["text"] == "数据库" for el in texts)
    assert any(el["text"] == "服务器" for el in texts)


def test_bar_chart_zero_value():
    data = {"A": 0, "B": 10}
    elements = bar_chart(0, 0, data)
    assert len(elements) >= 5  # Should still render
    rects = [el for el in elements if el["type"] == "rectangle"]
    # A's bar should have zero or minimal height
    a_rect = [r for r in rects if r["height"] < 5]
    assert len(a_rect) >= 1


def test_bar_chart_single_bar():
    data = {"Only": 42}
    elements = bar_chart(0, 0, data)
    assert len(elements) >= 4  # axes + bar + label + value


# ---------------------------------------------------------------------------
# Horizontal Bar Chart
# ---------------------------------------------------------------------------
def test_hbar_empty():
    elements = horizontal_bar_chart(0, 0, {})
    assert elements == []


def test_hbar_basic():
    data = {"A": 10, "B": 20}
    elements = horizontal_bar_chart(0, 0, data)
    assert len(elements) >= 5
    types = [el["type"] for el in elements]
    assert "rectangle" in types
    assert "text" in types


def test_hbar_title():
    data = {"X": 1}
    elements = horizontal_bar_chart(0, 0, data, title="HBar Test")
    texts = [el for el in elements if el["type"] == "text"]
    assert any(el["text"] == "HBar Test" for el in texts)


def test_hbar_custom_colors():
    data = {"A": 10, "B": 20}
    colors = {"A": "#ff0000", "B": "#0000ff"}
    elements = horizontal_bar_chart(0, 0, data, bar_colors=colors)
    rects = [el for el in elements if el["type"] == "rectangle"]
    fills = {el["backgroundColor"] for el in rects}
    assert "#ff0000" in fills
    assert "#0000ff" in fills


def test_hbar_no_values():
    data = {"A": 10, "B": 20}
    elements = horizontal_bar_chart(0, 0, data, show_values=False)
    texts = [el for el in elements if el["type"] == "text"]
    texts_content = [el["text"] for el in texts]
    assert "10" not in texts_content
    assert "20" not in texts_content


# ---------------------------------------------------------------------------
# Line Chart
# ---------------------------------------------------------------------------
def test_line_chart_empty():
    from core.charts import line_chart
    assert line_chart(x=0, y=0, data={}, labels=[]) == []

def test_line_chart_basic():
    from core.charts import line_chart
    data = {"Sales": [10, 30, 20, 50]}
    labels = ["Jan", "Feb", "Mar", "Apr"]
    els = line_chart(x=50, y=50, data=data, labels=labels)
    assert len(els) > 0
    types = {e["type"] for e in els}
    assert "line" in types
    assert "text" in types

def test_line_chart_multi_series():
    from core.charts import line_chart
    data = {"A": [10, 20], "B": [30, 10]}
    labels = ["Q1", "Q2"]
    els = line_chart(x=50, y=50, data=data, labels=labels)
    assert len(els) > 0

def test_line_chart_title():
    from core.charts import line_chart
    data = {"Sales": [10, 20]}
    labels = ["A", "B"]
    els = line_chart(x=50, y=50, data=data, labels=labels, title="Revenue")
    texts = [e for e in els if e["type"] == "text"]
    assert any("Revenue" in e["text"] for e in texts)

def test_line_chart_no_points():
    from core.charts import line_chart
    data = {"Sales": [10, 20]}
    labels = ["A", "B"]
    els_with = line_chart(x=50, y=50, data=data, labels=labels, show_points=True)
    els_without = line_chart(x=50, y=50, data=data, labels=labels, show_points=False)
    ellipses_with = sum(1 for e in els_with if e["type"] == "ellipse")
    ellipses_without = sum(1 for e in els_without if e["type"] == "ellipse")
    assert ellipses_with > ellipses_without

def test_line_chart_grid():
    from core.charts import line_chart
    data = {"A": [10, 20]}
    labels = ["X", "Y"]
    els_no = line_chart(x=50, y=50, data=data, labels=labels, show_grid=False)
    els_yes = line_chart(x=50, y=50, data=data, labels=labels, show_grid=True)
    assert len(els_yes) > len(els_no)

def test_line_chart_custom_colors():
    from core.charts import line_chart
    data = {"A": [10, 20]}
    labels = ["X", "Y"]
    els = line_chart(x=50, y=50, data=data, labels=labels, series_colors={"A": "#ff0000"})
    lines_red = [e for e in els if e["type"] == "line" and e["strokeColor"] == "#ff0000"]
    assert len(lines_red) > 0

def test_line_chart_legend():
    from core.charts import line_chart
    data = {"Series A": [10, 20], "Series B": [30, 10]}
    labels = ["X", "Y"]
    els = line_chart(x=50, y=50, data=data, labels=labels, show_legend=True)
    texts = [e for e in els if e["type"] == "text"]
    assert any("Series A" in e["text"] for e in texts)
    assert any("Series B" in e["text"] for e in texts)
