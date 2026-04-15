"""
AI Icon Generation via Gemini API

Generates SVG icons using Gemini, converts to Excalidraw elements.
Falls back to PNG (image_embed) if SVG generation fails.
Config stored at ~/.excalidraw-gen/config.json.
"""

import base64
import json
import os
import re
import urllib.request
import urllib.error
from typing import Any, Dict, List, Optional

from .svg_converter import svg_to_elements
from .icon_library import save_icon
from .engine import image_embed

_DEFAULT_SVG_PROMPT = (
    "Generate a simple, clean SVG icon for: {description}. "
    "Style: minimal line art, single color stroke (#1e1e1e), no fill, "
    "suitable for technical diagrams in academic papers. "
    "ViewBox: 0 0 48 48. Use only path, circle, rect, line elements. "
    "Return ONLY the SVG code, no explanation."
)

_DEFAULT_PNG_PROMPT = (
    "Generate a simple icon image for: {description}. "
    "Style: minimal, black line art on white background, "
    "suitable for technical diagrams in academic papers. "
    "The image should be 256x256 pixels."
)

# PLACEHOLDER_REST


def _config_dir() -> str:
    base = os.path.expanduser("~/.excalidraw-gen")
    os.makedirs(base, exist_ok=True)
    return base


def _config_path() -> str:
    return os.path.join(_config_dir(), "config.json")


def _load_config() -> Dict[str, Any]:
    path = _config_path()
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def _save_config(config: Dict[str, Any]) -> None:
    path = _config_path()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=2)


def configure(
    api_url: str,
    api_key: str,
    model: str = "gemini-2.0-flash",
) -> None:
    """Save Gemini API configuration."""
    config = _load_config()
    config["ai_icon"] = {
        "provider": "gemini",
        "api_url": api_url.rstrip("/"),
        "api_key": api_key,
        "default_model": model,
        "svg_prompt_template": _DEFAULT_SVG_PROMPT,
        "png_prompt_template": _DEFAULT_PNG_PROMPT,
    }
    _save_config(config)


def _get_ai_config() -> Dict[str, Any]:
    config = _load_config()
    ai_config = config.get("ai_icon")
    if not ai_config or not ai_config.get("api_key"):
        raise RuntimeError(
            "AI icon generation not configured. "
            "Call configure(api_url, api_key) first."
        )
    return ai_config


# PLACEHOLDER_API


def _call_gemini_api(
    url: str,
    payload: Dict[str, Any],
    api_key: str,
) -> Dict[str, Any]:
    """Call Gemini REST API using urllib (zero dependencies)."""
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={
            "Content-Type": "application/json",
            "x-goog-api-key": api_key,
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Gemini API error {e.code}: {body}") from e
    except urllib.error.URLError as e:
        raise RuntimeError(f"Network error: {e.reason}") from e


def _extract_svg(text: str) -> Optional[str]:
    """Extract SVG content from API response text."""
    m = re.search(r"```(?:xml|svg)?\s*\n(.*?)```", text, re.DOTALL)
    if m:
        candidate = m.group(1).strip()
        if "<svg" in candidate:
            return candidate
    m = re.search(r"(<svg[^>]*>.*?</svg>)", text, re.DOTALL)
    if m:
        return m.group(1)
    return None


def generate_icon_svg(
    description: str,
    prompt: Optional[str] = None,
    model: Optional[str] = None,
) -> str:
    """Generate an SVG icon string via Gemini API."""
    ai_config = _get_ai_config()
    api_url = ai_config["api_url"]
    api_key = ai_config["api_key"]
    model_name = model or ai_config.get("default_model", "gemini-2.0-flash")

    if prompt is None:
        template = ai_config.get("svg_prompt_template", _DEFAULT_SVG_PROMPT)
        prompt = template.format(description=description)
    elif "{description}" in prompt:
        prompt = prompt.format(description=description)

    url = f"{api_url}/models/{model_name}:generateContent"
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.2, "maxOutputTokens": 4096},
    }

    response = _call_gemini_api(url, payload, api_key)
    candidates = response.get("candidates", [])
    if not candidates:
        raise ValueError("No response from Gemini API")

    parts = candidates[0].get("content", {}).get("parts", [])
    text = ""
    for part in parts:
        if "text" in part:
            text += part["text"]

    svg = _extract_svg(text)
    if svg is None:
        raise ValueError(f"No valid SVG found in response: {text[:200]}")
    return svg


# PLACEHOLDER_GENERATE


def generate_icon(
    description: str,
    x: float = 0,
    y: float = 0,
    scale: float = 1.0,
    stroke: str = "#1e1e1e",
    sw: int = 2,
    roughness: int = 1,
    prompt: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """Generate an icon via Gemini and convert to Excalidraw elements."""
    try:
        svg_str = generate_icon_svg(description, prompt=prompt)
        elements = svg_to_elements(
            svg_str, x=x, y=y, scale=scale,
            stroke=stroke, stroke_width=sw, roughness=roughness,
        )
        if elements:
            return elements
    except (RuntimeError, ValueError, Exception):
        pass

    try:
        ai_config = _get_ai_config()
        api_url = ai_config["api_url"]
        api_key = ai_config["api_key"]
        model_name = ai_config.get("default_model", "gemini-2.0-flash")

        png_template = ai_config.get("png_prompt_template", _DEFAULT_PNG_PROMPT)
        png_prompt = png_template.format(description=description)

        url = f"{api_url}/models/{model_name}:generateContent"
        payload = {
            "contents": [{"parts": [{"text": png_prompt}]}],
            "generationConfig": {"temperature": 0.2},
        }

        response = _call_gemini_api(url, payload, api_key)
        candidates = response.get("candidates", [])
        if candidates:
            parts = candidates[0].get("content", {}).get("parts", [])
            for part in parts:
                inline = part.get("inlineData")
                if inline and inline.get("data"):
                    el, files = image_embed(
                        x, y,
                        int(48 * scale), int(48 * scale),
                        inline["data"],
                        mime=inline.get("mimeType", "image/png"),
                    )
                    el["_files"] = files
                    return [el]
    except Exception:
        pass

    raise RuntimeError(
        f"Failed to generate icon for '{description}'. "
        "Check your API configuration and try again."
    )


def generate_and_save(
    name: str,
    description: str,
    tags: Optional[List[str]] = None,
    **kwargs: Any,
) -> List[Dict[str, Any]]:
    """Generate an icon and save it to the persistent icon library."""
    elements = generate_icon(description, **kwargs)
    save_icon(
        name=name,
        elements=elements,
        description=description,
        tags=tags or [],
        source="ai-generated",
    )
    return elements
