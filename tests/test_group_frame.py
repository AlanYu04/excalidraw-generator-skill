"""Tests for group() and frame() builders."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.engine import group, frame, rect


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


def test_group_preserves_existing_group_ids():
    r1 = rect(0, 0, 100, 50)
    grouped_once = group([r1])
    grouped_twice = group(grouped_once)
    assert len(grouped_twice[0]["groupIds"]) == 2


def test_frame_returns_dict_with_correct_type():
    f = frame(0, 0, 500, 400, "模块A")
    assert f["type"] == "frame"
    assert f["name"] == "模块A"
    assert f["width"] == 500
    assert f["height"] == 400


def test_frame_default_name():
    f = frame(0, 0, 300, 200)
    assert f["name"] == "Frame"


def test_frame_position():
    f = frame(100, 200, 300, 150, "Test")
    assert f["x"] == 100
    assert f["y"] == 200
