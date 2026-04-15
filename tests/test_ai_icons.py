"""Tests for AI icon generation module (Gemini API)."""
import json
import os
import shutil
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

_TEST_CONFIG_DIR = None


def setup_module():
    global _TEST_CONFIG_DIR
    _TEST_CONFIG_DIR = tempfile.mkdtemp(prefix="excalidraw_test_ai_")
    import core.ai_icons as ai
    ai._config_dir = lambda: _TEST_CONFIG_DIR
    ai._config_path = lambda: os.path.join(_TEST_CONFIG_DIR, "config.json")


def teardown_module():
    if _TEST_CONFIG_DIR and os.path.exists(_TEST_CONFIG_DIR):
        shutil.rmtree(_TEST_CONFIG_DIR)


def test_configure_saves_config():
    from core.ai_icons import configure, _load_config
    configure(
        api_url="https://example.com/v1beta",
        api_key="test-key-123",
        model="gemini-2.0-flash",
    )
    config = _load_config()
    assert config["ai_icon"]["api_url"] == "https://example.com/v1beta"
    assert config["ai_icon"]["api_key"] == "test-key-123"
    assert config["ai_icon"]["default_model"] == "gemini-2.0-flash"


def test_configure_preserves_existing_keys():
    from core.ai_icons import configure, _load_config, _save_config
    _save_config({"other_setting": True})
    configure(api_url="https://example.com", api_key="key")
    config = _load_config()
    assert config.get("other_setting") is True
    assert "ai_icon" in config


def test_generate_icon_svg_no_config_raises():
    from core.ai_icons import generate_icon_svg, _save_config
    _save_config({})
    try:
        generate_icon_svg("a robot")
        assert False, "Should have raised"
    except RuntimeError as e:
        assert "not configured" in str(e).lower()


def test_generate_icon_svg_with_mock(monkeypatch):
    from core.ai_icons import generate_icon_svg, configure

    configure(api_url="https://example.com", api_key="fake-key")

    mock_svg = '<svg viewBox="0 0 48 48"><circle cx="24" cy="24" r="20"/></svg>'

    def mock_call_api(url, payload, api_key):
        return {"candidates": [{"content": {"parts": [{"text": mock_svg}]}}]}

    import core.ai_icons as ai
    monkeypatch.setattr(ai, "_call_gemini_api", mock_call_api)

    result = generate_icon_svg("a circle icon")
    assert "<svg" in result
    assert "circle" in result


def test_generate_icon_returns_elements(monkeypatch):
    from core.ai_icons import generate_icon, configure

    configure(api_url="https://example.com", api_key="fake-key")

    mock_svg = '<svg viewBox="0 0 48 48"><rect x="4" y="4" width="40" height="40"/></svg>'

    def mock_call_api(url, payload, api_key):
        return {"candidates": [{"content": {"parts": [{"text": mock_svg}]}}]}

    import core.ai_icons as ai
    monkeypatch.setattr(ai, "_call_gemini_api", mock_call_api)

    elements = generate_icon("a square", x=100, y=200)
    assert isinstance(elements, list)
    assert len(elements) >= 1


def test_generate_and_save(monkeypatch):
    from core.ai_icons import generate_and_save, configure
    import core.icon_library as il

    test_icon_dir = tempfile.mkdtemp(prefix="excalidraw_test_save_")
    il._icon_dir = lambda: test_icon_dir
    il._index_path = lambda: os.path.join(test_icon_dir, "index.json")

    configure(api_url="https://example.com", api_key="fake-key")

    mock_svg = '<svg viewBox="0 0 48 48"><rect x="0" y="0" width="48" height="48"/></svg>'

    def mock_call_api(url, payload, api_key):
        return {"candidates": [{"content": {"parts": [{"text": mock_svg}]}}]}

    import core.ai_icons as ai
    monkeypatch.setattr(ai, "_call_gemini_api", mock_call_api)

    elements = generate_and_save("test-icon", "a test icon", tags=["test"])
    assert isinstance(elements, list)

    icons = il.list_library_icons()
    assert any(i["name"] == "test-icon" for i in icons)

    shutil.rmtree(test_icon_dir)


def test_generate_icon_png_fallback_attaches_files(monkeypatch):
    from core.ai_icons import generate_icon, configure

    configure(api_url="https://example.com", api_key="fake-key")

    import core.ai_icons as ai

    def fail_svg(*_args, **_kwargs):
        raise ValueError("svg failed")

    def mock_call_api(_url, _payload, _api_key):
        return {
            "candidates": [{
                "content": {
                    "parts": [{
                        "inlineData": {
                            "data": "AAAA",
                            "mimeType": "image/png",
                        }
                    }]
                }
            }]
        }

    monkeypatch.setattr(ai, "generate_icon_svg", fail_svg)
    monkeypatch.setattr(ai, "_call_gemini_api", mock_call_api)

    elements = generate_icon("png fallback")
    assert len(elements) == 1
    assert elements[0]["type"] == "image"
    assert "_files" in elements[0]
    assert elements[0]["fileId"] in elements[0]["_files"]
