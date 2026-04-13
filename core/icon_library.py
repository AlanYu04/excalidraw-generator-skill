"""
Persistent Icon Library with TF-IDF Vector Search

Saves, loads, searches, and deletes custom Excalidraw icon elements.
Storage at ~/.excalidraw-gen/icons/ with index.json metadata.

Two-tier search:
  - Default: zero-dependency TF-IDF cosine similarity
  - Optional: OpenAI embedding-based semantic search (requires openai package)
"""

import json
import math
import os
import re
import shutil
from collections import Counter
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple

# ---------------------------------------------------------------------------
# Storage Paths
# ---------------------------------------------------------------------------
def _icon_dir() -> str:
    """Return the icon library directory path."""
    base = os.path.expanduser("~/.excalidraw-gen/icons")
    os.makedirs(base, exist_ok=True)
    return base


def _index_path() -> str:
    """Return the path to index.json."""
    return os.path.join(_icon_dir(), "index.json")


# ---------------------------------------------------------------------------
# Index Management
# ---------------------------------------------------------------------------
def _load_index() -> Dict[str, Any]:
    """Load the icon index from disk. Returns empty structure if not found."""
    path = _index_path()
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"version": 1, "icons": {}}


def _save_index(index: Dict[str, Any]) -> None:
    """Write the icon index to disk."""
    path = _index_path()
    with open(path, "w", encoding="utf-8") as f:
        json.dump(index, f, ensure_ascii=False, indent=2)


# ---------------------------------------------------------------------------
# Element Normalization
# ---------------------------------------------------------------------------
def _normalize_elements(elements: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Normalize element coordinates so the bounding box starts at (0, 0).

    Returns a new list; does not modify the input.
    """
    if not elements:
        return []

    min_x = min(el.get("x", 0) for el in elements)
    min_y = min(el.get("y", 0) for el in elements)

    normalized = []
    for el in elements:
        new_el = dict(el)
        new_el["x"] = el.get("x", 0) - min_x
        new_el["y"] = el.get("y", 0) - min_y
        # Deep-copy points array if present
        if "points" in el:
            new_el["points"] = [pt[:] for pt in el["points"]]
        normalized.append(new_el)
    return normalized


def _offset_elements(
    elements: List[Dict[str, Any]],
    x: float,
    y: float,
    scale: float = 1.0,
) -> List[Dict[str, Any]]:
    """Offset and optionally scale elements to a new position.

    Returns a new list; does not modify the input.
    """
    result = []
    for el in elements:
        new_el = dict(el)
        new_el["x"] = el.get("x", 0) * scale + x
        new_el["y"] = el.get("y", 0) * scale + y
        new_el["width"] = el.get("width", 0) * scale
        new_el["height"] = el.get("height", 0) * scale
        if "points" in el:
            new_el["points"] = [
                [pt[0] * scale, pt[1] * scale] for pt in el["points"]
            ]
        # Generate new IDs to avoid collisions
        from . import engine
        new_el["id"] = engine.uid()
        new_el["seed"] = engine.sd()
        new_el["versionNonce"] = engine.sd()
        new_el["updated"] = engine.ts()
        result.append(new_el)
    return result


# ---------------------------------------------------------------------------
# TF-IDF Search (zero-dependency)
# ---------------------------------------------------------------------------
def _tokenize(text: str) -> List[str]:
    """Tokenize text: lowercase, split on non-alphanumeric, filter short tokens."""
    tokens = re.findall(r"[a-zA-Z0-9\u4e00-\u9fff\u3040-\u309f\u30a0-\u30ff]+", text.lower())
    return [t for t in tokens if len(t) >= 2]


def _build_tfidf(documents: List[str]) -> List[Dict[str, float]]:
    """Build TF-IDF sparse vectors for a list of documents.

    Returns a list of dicts mapping token -> tfidf weight.
    """
    n_docs = len(documents)
    if n_docs == 0:
        return []

    # Tokenize all documents
    tokenized = [_tokenize(doc) for doc in documents]

    # Count term frequencies per document
    tf_list = [Counter(tokens) for tokens in tokenized]

    # Document frequency: how many docs contain each term
    df: Counter = Counter()
    for tokens in tokenized:
        unique = set(tokens)
        for t in unique:
            df[t] += 1

    # Build TF-IDF vectors
    vectors: List[Dict[str, float]] = []
    for tf in tf_list:
        vec: Dict[str, float] = {}
        total_terms = sum(tf.values())
        if total_terms == 0:
            vectors.append(vec)
            continue
        for term, count in tf.items():
            term_freq = count / total_terms
            idf = math.log(n_docs / (df[term] + 1)) + 1  # smoothed IDF
            vec[term] = term_freq * idf
        vectors.append(vec)

    return vectors


def _cosine_similarity(
    v1: Dict[str, float],
    v2: Dict[str, float],
) -> float:
    """Compute cosine similarity between two sparse vectors (dicts)."""
    if not v1 or not v2:
        return 0.0

    # Dot product over shared keys
    common_keys = set(v1.keys()) & set(v2.keys())
    dot = sum(v1[k] * v2[k] for k in common_keys)

    # Magnitudes
    mag1 = math.sqrt(sum(v ** 2 for v in v1.values()))
    mag2 = math.sqrt(sum(v ** 2 for v in v2.values()))

    if mag1 == 0 or mag2 == 0:
        return 0.0

    return dot / (mag1 * mag2)


# ---------------------------------------------------------------------------
# Optional OpenAI Embedding Search
# ---------------------------------------------------------------------------
def _get_embedding(text: str) -> Optional[List[float]]:
    """Get embedding for text using OpenAI API. Returns None if unavailable."""
    try:
        import openai
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            return None
        client = openai.OpenAI(api_key=api_key)
        response = client.embeddings.create(
            input=text,
            model="text-embedding-3-small",
        )
        return response.data[0].embedding
    except (ImportError, Exception):
        return None


def _embedding_cosine(a: List[float], b: List[float]) -> float:
    """Cosine similarity between two dense embedding vectors."""
    dot = sum(x * y for x, y in zip(a, b))
    mag_a = math.sqrt(sum(x * x for x in a))
    mag_b = math.sqrt(sum(x * x for x in b))
    if mag_a == 0 or mag_b == 0:
        return 0.0
    return dot / (mag_a * mag_b)


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------
def save_icon(
    name: str,
    elements: List[Dict[str, Any]],
    description: str = "",
    tags: Optional[List[str]] = None,
    source: str = "custom",
    source_file: Optional[str] = None,
) -> None:
    """Save an icon to the persistent library.

    Args:
        name: Unique icon name (used as identifier).
        elements: List of Excalidraw element dicts.
        description: Text description for search.
        tags: Optional list of tag strings.
        source: Origin of the icon (e.g. 'svg-converted', 'ai-generated', 'custom').
        source_file: Optional path to the source SVG file.
    """
    tags = tags or []

    # Normalize elements to origin (0, 0)
    normalized = _normalize_elements(elements)

    # Save element data
    icon_dir = _icon_dir()
    icon_file = f"{name}.json"
    icon_path = os.path.join(icon_dir, icon_file)
    with open(icon_path, "w", encoding="utf-8") as f:
        json.dump(normalized, f, ensure_ascii=False, indent=2)

    # Update index
    index = _load_index()

    # Try to get embedding for the description
    embedding = None
    search_text = f"{description} {' '.join(tags)}"
    if search_text.strip():
        embedding = _get_embedding(search_text)

    index["icons"][name] = {
        "name": name,
        "description": description,
        "tags": tags,
        "source": source,
        "source_file": source_file,
        "element_count": len(normalized),
        "created": datetime.now(timezone.utc).isoformat(),
        "file": icon_file,
        "embedding": embedding,
    }

    _save_index(index)


def load_icon(
    name: str,
    x: float = 0,
    y: float = 0,
    scale: float = 1.0,
) -> List[Dict[str, Any]]:
    """Load an icon from the library, repositioned to (x, y).

    Args:
        name: Icon name to load.
        x: Target X position.
        y: Target Y position.
        scale: Scale factor.

    Returns:
        List of Excalidraw element dicts with fresh IDs.

    Raises:
        KeyError: If the icon name is not found.
    """
    index = _load_index()
    if name not in index["icons"]:
        raise KeyError(f"Icon '{name}' not found in library")

    icon_info = index["icons"][name]
    icon_path = os.path.join(_icon_dir(), icon_info["file"])

    with open(icon_path, "r", encoding="utf-8") as f:
        elements = json.load(f)

    return _offset_elements(elements, x, y, scale)


def delete_icon(name: str) -> None:
    """Delete an icon from the library.

    Args:
        name: Icon name to delete.

    Raises:
        KeyError: If the icon name is not found.
    """
    index = _load_index()
    if name not in index["icons"]:
        raise KeyError(f"Icon '{name}' not found in library")

    icon_info = index["icons"][name]
    icon_path = os.path.join(_icon_dir(), icon_info["file"])

    # Remove the icon file
    if os.path.exists(icon_path):
        os.remove(icon_path)

    # Remove from index
    del index["icons"][name]
    _save_index(index)


def list_library_icons() -> List[Dict[str, Any]]:
    """List all icons in the library.

    Returns:
        List of icon metadata dicts (name, description, tags, etc.).
    """
    index = _load_index()
    return [
        {k: v for k, v in info.items() if k != "embedding"}
        for info in index["icons"].values()
    ]


def find_icons(
    query: str,
    limit: int = 5,
    use_embeddings: bool = False,
) -> List[Dict[str, Any]]:
    """Search for icons by description using TF-IDF or embedding similarity.

    Args:
        query: Search query text.
        limit: Maximum number of results.
        use_embeddings: If True, use OpenAI embeddings (requires API key).

    Returns:
        List of result dicts with 'name', 'score', 'description', 'tags'.
    """
    index = _load_index()
    icons = index["icons"]

    if not icons:
        return []

    query = query.strip()
    if not query:
        return [
            {k: v for k, v in info.items() if k != "embedding"}
            for info in list(icons.values())[:limit]
        ]

    icon_names = list(icons.keys())

    # Build search documents: description + tags
    documents = []
    for name in icon_names:
        info = icons[name]
        doc = f"{info.get('description', '')} {' '.join(info.get('tags', []))}"
        documents.append(doc.strip())

    # --- Embedding-based search ---
    if use_embeddings:
        query_embedding = _get_embedding(query)
        if query_embedding is not None:
            scored: List[Tuple[int, float]] = []
            for i, name in enumerate(icon_names):
                stored_emb = icons[name].get("embedding")
                if stored_emb:
                    sim = _embedding_cosine(query_embedding, stored_emb)
                else:
                    sim = 0.0
                scored.append((i, sim))

            scored.sort(key=lambda x: x[1], reverse=True)
            results = []
            for idx, score in scored[:limit]:
                if score <= 0:
                    continue
                info = icons[icon_names[idx]]
                results.append({
                    "name": info["name"],
                    "score": round(score, 4),
                    "description": info.get("description", ""),
                    "tags": info.get("tags", []),
                })
            if results:
                return results

    # --- TF-IDF fallback ---
    all_docs = documents + [query]
    vectors = _build_tfidf(all_docs)
    query_vec = vectors[-1]
    doc_vecs = vectors[:-1]

    scored_tfidf: List[Tuple[int, float]] = []
    for i, doc_vec in enumerate(doc_vecs):
        sim = _cosine_similarity(query_vec, doc_vec)
        scored_tfidf.append((i, sim))

    scored_tfidf.sort(key=lambda x: x[1], reverse=True)

    results = []
    for idx, score in scored_tfidf[:limit]:
        info = icons[icon_names[idx]]
        results.append({
            "name": info["name"],
            "score": round(score, 4),
            "description": info.get("description", ""),
            "tags": info.get("tags", []),
        })

    return results
