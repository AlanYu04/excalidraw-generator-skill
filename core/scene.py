"""Scene utilities for rewriting references and collecting embedded assets."""

from __future__ import annotations

import copy
import hashlib
from typing import Any, Callable


def stable_int(token: str, salt: str = "") -> int:
    """Return a deterministic positive integer for scene metadata fields."""
    digest = hashlib.sha1(f"{salt}:{token}".encode("utf-8")).hexdigest()
    return int(digest[:8], 16)


def normalize_scene_files(
    elements: list[dict[str, Any]],
    files: dict[str, Any] | None = None,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    """Return scene-safe elements plus top-level files collected from `_files`."""
    scene_files = copy.deepcopy(files or {})
    clean_elements: list[dict[str, Any]] = []

    for element in elements:
        cloned = copy.deepcopy(element)
        embedded_files = cloned.pop("_files", None)
        if embedded_files:
            scene_files.update(copy.deepcopy(embedded_files))
        clean_elements.append(cloned)

    return clean_elements, scene_files


def remap_scene_references(
    elements: list[dict[str, Any]],
    *,
    id_factory: Callable[[str, dict[str, Any]], str] | None = None,
    group_id_factory: Callable[[str], str] | None = None,
    file_id_factory: Callable[[str], str] | None = None,
    deterministic: bool = False,
) -> tuple[list[dict[str, Any]], dict[str, dict[str, str]]]:
    """Clone elements and rewrite all internal IDs consistently."""
    cloned = copy.deepcopy(elements)

    if id_factory is None:
        id_factory = lambda old_id, _element: old_id
    if group_id_factory is None:
        group_id_factory = lambda old_group_id: old_group_id
    if file_id_factory is None:
        file_id_factory = lambda old_file_id: old_file_id

    id_map: dict[str, str] = {}
    group_map: dict[str, str] = {}
    file_map: dict[str, str] = {}

    for element in cloned:
        old_id = element.get("id")
        if old_id and old_id not in id_map:
            id_map[old_id] = id_factory(old_id, element)

        for group_id in element.get("groupIds", []):
            if group_id not in group_map:
                group_map[group_id] = group_id_factory(group_id)

        file_id = element.get("fileId")
        if file_id and file_id not in file_map:
            file_map[file_id] = file_id_factory(file_id)

        embedded_files = element.get("_files") or {}
        for embedded_file_id in embedded_files:
            if embedded_file_id not in file_map:
                file_map[embedded_file_id] = file_id_factory(embedded_file_id)

    for element in cloned:
        old_id = element.get("id")
        if old_id in id_map:
            element["id"] = id_map[old_id]

        if "groupIds" in element:
            element["groupIds"] = [group_map.get(group_id, group_id) for group_id in element.get("groupIds", [])]

        container_id = element.get("containerId")
        if container_id in id_map:
            element["containerId"] = id_map[container_id]

        for binding_key in ("startBinding", "endBinding"):
            binding = element.get(binding_key)
            if binding and binding.get("elementId") in id_map:
                updated_binding = dict(binding)
                updated_binding["elementId"] = id_map[binding["elementId"]]
                element[binding_key] = updated_binding

        bound_elements = element.get("boundElements")
        if bound_elements is not None:
            rewritten_bound: list[dict[str, Any]] = []
            for bound in bound_elements:
                updated_bound = dict(bound)
                bound_id = updated_bound.get("id")
                if bound_id in id_map:
                    updated_bound["id"] = id_map[bound_id]
                rewritten_bound.append(updated_bound)
            element["boundElements"] = rewritten_bound

        file_id = element.get("fileId")
        if file_id in file_map:
            element["fileId"] = file_map[file_id]

        embedded_files = element.get("_files")
        if embedded_files:
            rewritten_files: dict[str, Any] = {}
            for old_file_id, file_info in embedded_files.items():
                new_file_id = file_map.get(old_file_id, old_file_id)
                new_file_info = copy.deepcopy(file_info)
                new_file_info["id"] = new_file_id
                rewritten_files[new_file_id] = new_file_info
            element["_files"] = rewritten_files

        if deterministic:
            token = element.get("id", "")
            element["seed"] = stable_int(token, "seed")
            element["versionNonce"] = stable_int(token, "nonce")
            element["updated"] = stable_int(token, "updated")

    return cloned, {
        "id_map": id_map,
        "group_map": group_map,
        "file_map": file_map,
    }
