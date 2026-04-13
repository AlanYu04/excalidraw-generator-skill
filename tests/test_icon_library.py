"""Tests for persistent icon library and vector search."""
import json
import os
import shutil
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.icon_library import (
    save_icon,
    load_icon,
    delete_icon,
    list_library_icons,
    find_icons,
    _normalize_elements,
    _offset_elements,
    _tokenize,
    _build_tfidf,
    _cosine_similarity,
    _icon_dir,
    _load_index,
)
from core import engine


# ---------------------------------------------------------------------------
# Use a temp directory for test isolation
# ---------------------------------------------------------------------------
_TEST_DIR = None


def setup_module():
    """Redirect icon library to a temp directory for testing."""
    global _TEST_DIR
    _TEST_DIR = tempfile.mkdtemp(prefix="excalidraw_test_icons_")
    # Patch _icon_dir by monkeypatching the module
    import core.icon_library as il
    il._icon_dir = lambda: _TEST_DIR
    il._index_path = lambda: os.path.join(_TEST_DIR, "index.json")


def teardown_module():
    """Clean up temp directory."""
    if _TEST_DIR and os.path.exists(_TEST_DIR):
        shutil.rmtree(_TEST_DIR)


def _make_elements(x=10, y=20):
    """Create test elements."""
    return [
        engine.rect(x, y, 40, 30, fill="#a5d8ff", stroke="#1971c2"),
        engine.text_standalone(x + 20, y + 15, "test", fs=12),
    ]


# ---------------------------------------------------------------------------
# Save / Load / Delete
# ---------------------------------------------------------------------------
def test_save_and_load():
    elements = _make_elements()
    save_icon("test-icon-1", elements, description="A test icon", tags=["test"])

    loaded = load_icon("test-icon-1", x=100, y=200)
    assert len(loaded) == len(elements)
    # Should be offset to (100, 200) area
    assert all(el["x"] >= 100 for el in loaded)
    assert all(el["y"] >= 200 for el in loaded)


def test_save_creates_files():
    elements = _make_elements()
    save_icon("test-files", elements, description="Files test")

    # Check index exists
    idx = _load_index()
    assert "test-files" in idx["icons"]
    assert idx["icons"]["test-files"]["element_count"] == 2

    # Check icon file exists
    icon_file = os.path.join(_TEST_DIR, idx["icons"]["test-files"]["file"])
    assert os.path.exists(icon_file)


def test_load_nonexistent_raises():
    import pytest
    with pytest.raises(KeyError, match="not-found"):
        load_icon("not-found")


def test_delete_icon():
    elements = _make_elements()
    save_icon("to-delete", elements, description="Will be deleted")
    delete_icon("to-delete")

    import pytest
    with pytest.raises(KeyError):
        load_icon("to-delete")


def test_delete_nonexistent_raises():
    import pytest
    with pytest.raises(KeyError, match="nonexistent"):
        delete_icon("nonexistent")


def test_save_updates_existing():
    elements1 = _make_elements()
    save_icon("updatable", elements1, description="v1")
    elements2 = _make_elements(50, 60)
    save_icon("updatable", elements2, description="v2")

    idx = _load_index()
    assert idx["icons"]["updatable"]["description"] == "v2"


def test_list_library_icons():
    save_icon("list-a", _make_elements(), description="Icon A", tags=["a"])
    save_icon("list-b", _make_elements(), description="Icon B", tags=["b"])

    icons = list_library_icons()
    names = {ic["name"] for ic in icons}
    assert "list-a" in names
    assert "list-b" in names
    # Should not contain embedding data
    for ic in icons:
        assert "embedding" not in ic


# ---------------------------------------------------------------------------
# Normalization & Offset
# ---------------------------------------------------------------------------
def test_normalize_elements():
    elements = [
        {"x": 50, "y": 30, "width": 40, "height": 20},
        {"x": 10, "y": 60, "width": 30, "height": 10},
    ]
    normalized = _normalize_elements(elements)
    assert normalized[0]["x"] == 40  # 50 - min_x(10)
    assert normalized[0]["y"] == 0   # 30 - min_y(30)
    assert normalized[1]["x"] == 0   # 10 - 10
    assert normalized[1]["y"] == 30  # 60 - 30


def test_normalize_does_not_mutate():
    elements = [{"x": 50, "y": 30, "width": 40}]
    _normalize_elements(elements)
    assert elements[0]["x"] == 50


def test_normalize_empty():
    assert _normalize_elements([]) == []


def test_offset_elements():
    elements = [
        {"x": 0, "y": 0, "width": 40, "height": 20},
        {"x": 20, "y": 10, "width": 30, "height": 15},
    ]
    offset = _offset_elements(elements, x=100, y=200, scale=2.0)
    assert offset[0]["x"] == 100
    assert offset[0]["y"] == 200
    assert offset[0]["width"] == 80
    assert offset[1]["x"] == 140  # 20 * 2 + 100
    assert offset[1]["y"] == 220  # 10 * 2 + 200


def test_offset_does_not_mutate():
    elements = [{"x": 5, "y": 10, "width": 20, "height": 10}]
    _offset_elements(elements, x=100, y=100)
    assert elements[0]["x"] == 5


# ---------------------------------------------------------------------------
# TF-IDF Search
# ---------------------------------------------------------------------------
def test_tokenize_basic():
    tokens = _tokenize("Hello World foo-bar")
    assert "hello" in tokens
    assert "world" in tokens
    assert "foo" in tokens
    assert "bar" in tokens


def test_tokenize_cjk():
    tokens = _tokenize("数据库 存储 server")
    assert "数据库" in tokens
    assert "存储" in tokens
    assert "server" in tokens


def test_tokenize_short_filtered():
    tokens = _tokenize("a I x")
    assert len(tokens) == 0  # Single-char tokens filtered


def test_tfidf_basic():
    docs = [
        "database storage system",
        "server infrastructure hosting",
        "user authentication login",
    ]
    vectors = _build_tfidf(docs)
    assert len(vectors) == 3
    # Each vector should have non-zero values for its terms
    assert "database" in vectors[0]
    assert "server" in vectors[1]
    assert "user" in vectors[2]


def test_tfidf_empty():
    assert _build_tfidf([]) == []


def test_cosine_similarity_identical():
    v = {"a": 1.0, "b": 2.0, "c": 3.0}
    sim = _cosine_similarity(v, v)
    assert abs(sim - 1.0) < 0.001


def test_cosine_similarity_orthogonal():
    v1 = {"a": 1.0}
    v2 = {"b": 1.0}
    sim = _cosine_similarity(v1, v2)
    assert sim == 0.0


def test_cosine_similarity_empty():
    assert _cosine_similarity({}, {"a": 1.0}) == 0.0


# ---------------------------------------------------------------------------
# find_icons integration
# ---------------------------------------------------------------------------
def test_find_icons_basic():
    save_icon("search-db", _make_elements(),
              description="database storage system", tags=["database", "storage"])
    save_icon("search-auth", _make_elements(),
              description="user authentication login", tags=["auth", "security"])
    save_icon("search-server", _make_elements(),
              description="server infrastructure hosting", tags=["server", "infra"])

    results = find_icons("database", limit=2)
    assert len(results) >= 1
    assert results[0]["name"] == "search-db"
    assert results[0]["score"] > 0


def test_find_icons_returns_score_and_metadata():
    save_icon("score-test", _make_elements(),
              description="cloud computing service", tags=["cloud"])
    results = find_icons("cloud computing")
    assert len(results) >= 1
    assert "score" in results[0]
    assert "description" in results[0]
    assert "tags" in results[0]


def test_find_icons_empty_library():
    # Clear any test icons
    idx = _load_index()
    idx["icons"] = {}
    import core.icon_library as il
    with open(il._index_path(), "w") as f:
        json.dump(idx, f)

    results = find_icons("anything")
    assert results == []


def test_find_icons_empty_query():
    save_icon("empty-q", _make_elements(), description="something")
    results = find_icons("")
    assert len(results) >= 1
