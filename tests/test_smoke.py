"""Smoke tests: verify existing engine functions work."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.engine import (
    rect, text_standalone, labeled_rect, auto_labeled_rect, arrow,
    ellipse, diamond, line, numbered_circle,
    save_excalidraw, estimate_text_width, is_cjk, uid,
    connect, bind_arrow,
    check_overlaps, check_arrow_bindings, check_spacing, verify_layout,
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


# === Layout Verification Tests ===

def test_check_overlaps_no_overlap():
    a = rect(0, 0, 100, 50)
    b = rect(150, 0, 100, 50)
    results = check_overlaps([a, b])
    assert results == []


def test_check_overlaps_detected():
    a = rect(0, 0, 100, 50)
    b = rect(80, 0, 100, 50)
    results = check_overlaps([a, b])
    assert len(results) == 1
    assert results[0]["overlap_area"] > 0
    assert results[0]["severity"] in ("WARNING", "ERROR")


def test_check_overlaps_skips_container_text():
    pair = labeled_rect(0, 0, 200, 60, "Hello")
    c = rect(150, 0, 100, 50)
    results = check_overlaps([*pair, c])
    # The text inside the rect should not be reported as overlap with its parent
    for r in results:
        assert not (r["a_id"] == pair[1]["id"] and r["b_id"] == pair[0]["id"])
        assert not (r["a_id"] == pair[0]["id"] and r["b_id"] == pair[1]["id"])


def test_check_overlaps_skips_arrows():
    a = rect(0, 0, 100, 50)
    b = rect(150, 0, 100, 50)
    arw = arrow(100, 25, 50, 0)
    results = check_overlaps([a, b, arw])
    assert all(r["a_id"] != arw["id"] and r["b_id"] != arw["id"] for r in results)


def test_check_arrow_bindings_ok():
    a = rect(0, 0, 100, 50)
    b = rect(200, 0, 100, 50)
    arw = connect(a, b)
    issues = check_arrow_bindings([a, b, arw])
    assert issues == []


def test_check_arrow_bindings_missing_binding():
    a = rect(0, 0, 100, 50)
    b = rect(200, 0, 100, 50)
    arw = arrow(100, 25, 100, 0)
    issues = check_arrow_bindings([a, b, arw])
    assert len(issues) >= 2
    issue_types = {i["issue"] for i in issues}
    assert "missing_start_binding" in issue_types
    assert "missing_end_binding" in issue_types


def test_check_arrow_bindings_dead_element():
    a = rect(0, 0, 100, 50)
    b = rect(200, 0, 100, 50)
    arw = arrow(100, 25, 100, 0)
    arw["startBinding"] = {"elementId": "ghost", "focus": 0, "gap": 2, "fixedPoint": None}
    arw["endBinding"] = {"elementId": b["id"], "focus": 0, "gap": 2, "fixedPoint": None}
    issues = check_arrow_bindings([a, b, arw])
    assert any(i["issue"] == "dead_start_element" for i in issues)


def test_check_arrow_bindings_no_collapsed_end_focus_with_auto_focus():
    target = rect(200, 200, 600, 40)
    sources = [
        rect(40, 0, 120, 60),
        rect(440, 0, 120, 60),
        rect(840, 0, 120, 60),
    ]
    arrows = [connect(src, target) for src in sources]
    issues = check_arrow_bindings([target, *sources, *arrows])
    assert not any(i["issue"] == "collapsed_end_focus" for i in issues)


def test_check_arrow_bindings_detects_collapsed_end_focus():
    target = rect(200, 200, 600, 40)
    sources = [
        rect(40, 0, 120, 60),
        rect(300, 0, 120, 60),
        rect(580, 0, 120, 60),
        rect(840, 0, 120, 60),
    ]
    arrows = [connect(src, target, end_focus=0) for src in sources]
    issues = check_arrow_bindings([target, *sources, *arrows])
    collapsed = [i for i in issues if i["issue"] == "collapsed_end_focus"]
    assert len(collapsed) == 1
    assert collapsed[0]["severity"] == "ERROR"


def test_check_spacing_consistent():
    """Only 2 elements — no pair to compare, so no spacing issues."""
    a = rect(0, 0, 100, 50)
    b = rect(150, 0, 100, 50)
    issues = check_spacing([a, b])
    assert issues == []


def test_check_spacing_inconsistent():
    a = rect(0, 0, 100, 50)
    b = rect(150, 0, 100, 50)   # 50px gap
    c = rect(400, 0, 100, 50)   # 150px gap from b
    issues = check_spacing([a, b, c])
    assert len(issues) > 0


def test_verify_layout_pass():
    a = auto_labeled_rect(0, 0, "Box A")
    b = auto_labeled_rect(300, 0, "Box B")
    arw = connect(a[0], b[0])
    elements = [*a, *b, arw]
    report = verify_layout(elements)
    assert report["status"] in ("PASS", "WARN")
    assert report["elements_count"] >= 2
    assert report["arrows_count"] == 1


def test_verify_layout_fail_on_overlap():
    a = rect(0, 0, 200, 100)
    b = rect(50, 0, 200, 100)
    report = verify_layout([a, b])
    assert report["status"] in ("FAIL", "WARN")
    assert report["errors"] > 0 or report["warnings"] > 0


def test_verify_layout_empty():
    report = verify_layout([])
    # Empty diagram gets WARN from richness check (too few elements)
    assert report["status"] in ("PASS", "WARN")
    assert report["elements_count"] == 0
