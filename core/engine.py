"""
Excalidraw Diagram Generator - Core Engine
Generates Excalidraw scene JSON with CJK-aware text centering.
"""
import json, os, random, time

# ---------------------------------------------------------------------------
# ID / Seed / Timestamp
# ---------------------------------------------------------------------------
_uid_counter = 0
def uid():
    global _uid_counter
    _uid_counter += 1
    return f"e{_uid_counter:06d}"

def sd():
    return random.randint(10000, 999999)

def ts():
    return int(time.time() * 1000)

# ---------------------------------------------------------------------------
# CJK-aware text width estimation
# ---------------------------------------------------------------------------
def is_cjk(ch):
    cp = ord(ch)
    if 0x4E00 <= cp <= 0x9FFF: return True
    if 0x3400 <= cp <= 0x4DBF: return True
    if 0xF900 <= cp <= 0xFAFF: return True
    if 0x3000 <= cp <= 0x303F: return True
    if ch in '↑↓←→∈π≤≥≠×÷±★✓✗': return True
    if ch in '¹²³⁴⁵⁶⁷⁸⁹⁰': return True
    return False

def estimate_text_width(text, fs):
    w = 0.0
    for ch in text:
        if ch == '\n': continue
        if is_cjk(ch):   w += fs * 1.05
        elif ch == ' ':  w += fs * 0.35
        else:            w += fs * 0.62
    return w

def estimate_text_height(text, fs):
    return len(text.split('\n')) * fs * 1.25

# ---------------------------------------------------------------------------
# Element Builders
# ---------------------------------------------------------------------------
def rect(x, y, w, h, fill="transparent", stroke="#1e1e1e", sw=2, roughness=1,
         fill_style="solid", stroke_style="solid"):
    return {
        "id": uid(), "type": "rectangle",
        "x": x, "y": y, "width": w, "height": h,
        "angle": 0, "strokeColor": stroke, "backgroundColor": fill,
        "fillStyle": fill_style, "strokeWidth": sw, "strokeStyle": stroke_style,
        "roughness": roughness, "opacity": 100, "groupIds": [],
        "roundness": {"type": 3}, "seed": sd(), "version": 1,
        "versionNonce": sd(), "isDeleted": False, "boundElements": [],
        "updated": ts(), "link": None, "locked": False
    }

def text_standalone(cx, cy, txt, fs=20, color="#1e1e1e", font_family=3, roughness=0,
                    text_align="center"):
    tw = estimate_text_width(txt, fs)
    th = estimate_text_height(txt, fs)
    # For center: x = cx - tw/2; for left: x = cx; for right: x = cx - tw
    if text_align == "center":
        x = cx - tw / 2
    elif text_align == "right":
        x = cx - tw
    else:  # left
        x = cx
    return {
        "id": uid(), "type": "text",
        "x": x, "y": cy - th/2, "width": tw, "height": th,
        "angle": 0, "strokeColor": color, "backgroundColor": "transparent",
        "fillStyle": "solid", "strokeWidth": 2, "strokeStyle": "solid",
        "roughness": roughness, "opacity": 100, "groupIds": [],
        "roundness": None, "seed": sd(), "version": 1,
        "versionNonce": sd(), "isDeleted": False, "boundElements": [],
        "updated": ts(), "link": None, "locked": False,
        "text": txt, "fontSize": fs, "fontFamily": font_family,
        "textAlign": text_align, "verticalAlign": "middle",
        "containerId": None, "originalText": txt, "lineHeight": 1.25
    }

def labeled_rect(x, y, w, h, label, fill="transparent", stroke="#1e1e1e",
                 sw=2, fs=16, label_color=None, roughness=1, font_family=3,
                 fill_style="solid", stroke_style="solid"):
    if label_color is None: label_color = stroke
    rid, tid = uid(), uid()
    r = {
        "id": rid, "type": "rectangle",
        "x": x, "y": y, "width": w, "height": h,
        "angle": 0, "strokeColor": stroke, "backgroundColor": fill,
        "fillStyle": fill_style, "strokeWidth": sw, "strokeStyle": stroke_style,
        "roughness": roughness, "opacity": 100, "groupIds": [],
        "roundness": {"type": 3}, "seed": sd(), "version": 1,
        "versionNonce": sd(), "isDeleted": False,
        "boundElements": [{"id": tid, "type": "text"}],
        "updated": ts(), "link": None, "locked": False
    }
    # Bound text: align to container inner area, let Excalidraw auto-center
    pad = 4
    t = {
        "id": tid, "type": "text",
        "x": x + pad, "y": y + pad,
        "width": w - pad * 2, "height": h - pad * 2,
        "angle": 0, "strokeColor": label_color, "backgroundColor": "transparent",
        "fillStyle": "solid", "strokeWidth": 2, "strokeStyle": "solid",
        "roughness": 0, "opacity": 100, "groupIds": [],
        "roundness": None, "seed": sd(), "version": 1,
        "versionNonce": sd(), "isDeleted": False, "boundElements": [],
        "updated": ts(), "link": None, "locked": False,
        "text": label, "fontSize": fs, "fontFamily": font_family,
        "textAlign": "center", "verticalAlign": "middle",
        "containerId": rid, "originalText": label, "lineHeight": 1.25
    }
    return [r, t]

def arrow(x, y, dx, dy, stroke="#1e1e1e", sw=2, roughness=1):
    return {
        "id": uid(), "type": "arrow",
        "x": x, "y": y, "width": abs(dx), "height": abs(dy),
        "angle": 0, "strokeColor": stroke, "backgroundColor": "transparent",
        "fillStyle": "solid", "strokeWidth": sw, "strokeStyle": "solid",
        "roughness": roughness, "opacity": 100, "groupIds": [],
        "roundness": {"type": 2}, "seed": sd(), "version": 1,
        "versionNonce": sd(), "isDeleted": False, "boundElements": [],
        "updated": ts(), "link": None, "locked": False,
        "points": [[0,0],[dx,dy]], "startBinding": None, "endBinding": None,
        "startArrowhead": None, "endArrowhead": "arrow", "elbowed": False
    }

def ellipse(x, y, w, h, fill="transparent", stroke="#1e1e1e", sw=2, roughness=1,
            fill_style="solid"):
    return {
        "id": uid(), "type": "ellipse",
        "x": x, "y": y, "width": w, "height": h,
        "angle": 0, "strokeColor": stroke, "backgroundColor": fill,
        "fillStyle": fill_style, "strokeWidth": sw, "strokeStyle": "solid",
        "roughness": roughness, "opacity": 100, "groupIds": [],
        "roundness": {"type": 2}, "seed": sd(), "version": 1,
        "versionNonce": sd(), "isDeleted": False, "boundElements": [],
        "updated": ts(), "link": None, "locked": False
    }

def diamond(x, y, w, h, fill="transparent", stroke="#1e1e1e", sw=2, roughness=1,
            fill_style="solid"):
    return {
        "id": uid(), "type": "diamond",
        "x": x, "y": y, "width": w, "height": h,
        "angle": 0, "strokeColor": stroke, "backgroundColor": fill,
        "fillStyle": fill_style, "strokeWidth": sw, "strokeStyle": "solid",
        "roughness": roughness, "opacity": 100, "groupIds": [],
        "roundness": {"type": 2}, "seed": sd(), "version": 1,
        "versionNonce": sd(), "isDeleted": False, "boundElements": [],
        "updated": ts(), "link": None, "locked": False
    }

def line(x, y, dx, dy, stroke="#1e1e1e", sw=2, roughness=1):
    return {
        "id": uid(), "type": "line",
        "x": x, "y": y, "width": abs(dx), "height": abs(dy),
        "angle": 0, "strokeColor": stroke, "backgroundColor": "transparent",
        "fillStyle": "solid", "strokeWidth": sw, "strokeStyle": "solid",
        "roughness": roughness, "opacity": 100, "groupIds": [],
        "roundness": {"type": 2}, "seed": sd(), "version": 1,
        "versionNonce": sd(), "isDeleted": False, "boundElements": [],
        "updated": ts(), "link": None, "locked": False,
        "points": [[0,0],[dx,dy]], "startBinding": None, "endBinding": None,
        "startArrowhead": None, "endArrowhead": None, "elbowed": False
    }

def labeled_diamond(x, y, w, h, label, fill="transparent", stroke="#1e1e1e",
                    sw=2, fs=16, label_color=None, roughness=1, font_family=3,
                    fill_style="solid"):
    if label_color is None: label_color = stroke
    did, tid = uid(), uid()
    d = {
        "id": did, "type": "diamond",
        "x": x, "y": y, "width": w, "height": h,
        "angle": 0, "strokeColor": stroke, "backgroundColor": fill,
        "fillStyle": fill_style, "strokeWidth": sw, "strokeStyle": "solid",
        "roughness": roughness, "opacity": 100, "groupIds": [],
        "roundness": {"type": 2}, "seed": sd(), "version": 1,
        "versionNonce": sd(), "isDeleted": False,
        "boundElements": [{"id": tid, "type": "text"}],
        "updated": ts(), "link": None, "locked": False
    }
    pad = 4
    t = {
        "id": tid, "type": "text",
        "x": x + pad, "y": y + pad,
        "width": w - pad * 2, "height": h - pad * 2,
        "angle": 0, "strokeColor": label_color, "backgroundColor": "transparent",
        "fillStyle": "solid", "strokeWidth": 2, "strokeStyle": "solid",
        "roughness": 0, "opacity": 100, "groupIds": [],
        "roundness": None, "seed": sd(), "version": 1,
        "versionNonce": sd(), "isDeleted": False, "boundElements": [],
        "updated": ts(), "link": None, "locked": False,
        "text": label, "fontSize": fs, "fontFamily": font_family,
        "textAlign": "center", "verticalAlign": "middle",
        "containerId": did, "originalText": label, "lineHeight": 1.25
    }
    return [d, t]


def labeled_ellipse(x, y, w, h, label, fill="transparent", stroke="#1e1e1e",
                    sw=2, fs=16, label_color=None, roughness=1, font_family=3,
                    fill_style="solid"):
    if label_color is None: label_color = stroke
    eid, tid = uid(), uid()
    e = {
        "id": eid, "type": "ellipse",
        "x": x, "y": y, "width": w, "height": h,
        "angle": 0, "strokeColor": stroke, "backgroundColor": fill,
        "fillStyle": fill_style, "strokeWidth": sw, "strokeStyle": "solid",
        "roughness": roughness, "opacity": 100, "groupIds": [],
        "roundness": {"type": 2}, "seed": sd(), "version": 1,
        "versionNonce": sd(), "isDeleted": False,
        "boundElements": [{"id": tid, "type": "text"}],
        "updated": ts(), "link": None, "locked": False
    }
    pad = 4
    t = {
        "id": tid, "type": "text",
        "x": x + pad, "y": y + pad,
        "width": w - pad * 2, "height": h - pad * 2,
        "angle": 0, "strokeColor": label_color, "backgroundColor": "transparent",
        "fillStyle": "solid", "strokeWidth": 2, "strokeStyle": "solid",
        "roughness": 0, "opacity": 100, "groupIds": [],
        "roundness": None, "seed": sd(), "version": 1,
        "versionNonce": sd(), "isDeleted": False, "boundElements": [],
        "updated": ts(), "link": None, "locked": False,
        "text": label, "fontSize": fs, "fontFamily": font_family,
        "textAlign": "center", "verticalAlign": "middle",
        "containerId": eid, "originalText": label, "lineHeight": 1.25
    }
    return [e, t]


def group(elements):
    """将元素编组，返回新元素列表（不修改原始元素）。"""
    gid = uid()
    result = []
    for el in elements:
        new_el = dict(el)
        new_el["groupIds"] = list(el.get("groupIds", [])) + [gid]
        result.append(new_el)
    return result


def frame(x, y, w, h, name="Frame", stroke="#1e1e1e", sw=2):
    return {
        "id": uid(), "type": "frame",
        "x": x, "y": y, "width": w, "height": h,
        "angle": 0, "strokeColor": stroke, "backgroundColor": "transparent",
        "fillStyle": "solid", "strokeWidth": sw, "strokeStyle": "solid",
        "roughness": 0, "opacity": 100, "groupIds": [],
        "roundness": None, "seed": sd(), "version": 1,
        "versionNonce": sd(), "isDeleted": False, "boundElements": [],
        "updated": ts(), "link": None, "locked": False,
        "name": name
    }


def image_embed(x, y, w, h, base64_data, mime="image/png"):
    """创建图片元素和对应的 files 条目。返回 (element_dict, files_dict)。"""
    file_id = uid()
    el = {
        "id": uid(), "type": "image",
        "x": x, "y": y, "width": w, "height": h,
        "angle": 0, "strokeColor": "transparent", "backgroundColor": "transparent",
        "fillStyle": "solid", "strokeWidth": 0, "strokeStyle": "solid",
        "roughness": 0, "opacity": 100, "groupIds": [],
        "roundness": None, "seed": sd(), "version": 1,
        "versionNonce": sd(), "isDeleted": False, "boundElements": [],
        "updated": ts(), "link": None, "locked": False,
        "fileId": file_id, "status": "saved", "scale": [1, 1]
    }
    file_entry = {
        file_id: {
            "mimeType": mime,
            "id": file_id,
            "dataURL": f"data:{mime};base64,{base64_data}",
            "created": ts()
        }
    }
    return el, file_entry


def bind_arrow(arrow_el, start_el, end_el, gap=2):
    """绑定箭头到起止元素，返回新箭头（不修改原始）。"""
    new_arrow = dict(arrow_el)
    new_arrow["startBinding"] = {
        "elementId": start_el["id"],
        "focus": 0,
        "gap": gap,
        "fixedPoint": None
    }
    new_arrow["endBinding"] = {
        "elementId": end_el["id"],
        "focus": 0,
        "gap": gap,
        "fixedPoint": None
    }
    return new_arrow


# ---------------------------------------------------------------------------
# Layout helpers — prevent text/shape overlap
# ---------------------------------------------------------------------------
def below(y: float, h: float, gap: float = 10) -> float:
    """Safe y-coordinate for placing an element below a shape at (_, y) with height h."""
    return y + h + gap

def right_of(x: float, w: float, gap: float = 10) -> float:
    """Safe x-coordinate for placing an element to the right of a shape at (x, _) with width w."""
    return x + w + gap

def above(y: float, gap: float = 10) -> float:
    """Safe y-coordinate for placing an element above a shape whose top is at y."""
    return y - gap


def numbered_circle(cx, cy, num, fill, stroke):
    r = 16
    return [
        ellipse(cx - r, cy - r, r*2, r*2, fill=fill, stroke=stroke, sw=2),
        text_standalone(cx, cy, str(num), fs=14, color=stroke)
    ]

# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------
def _build_scene(elements, bg="#ffffff", files=None):
    return {
        "type": "excalidraw", "version": 2,
        "source": "https://excalidraw.com",
        "elements": elements,
        "appState": {"viewBackgroundColor": bg, "gridSize": None},
        "files": files or {}
    }

def save_excalidraw(filepath, elements, bg="#ffffff", files=None):
    scene = _build_scene(elements, bg, files)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(scene, f, ensure_ascii=False, indent=2)
    print(f"  ✓ {os.path.basename(filepath)} ({len(elements)} elements)")

def save_obsidian_md(filepath, elements, bg="#ffffff", files=None):
    scene = _build_scene(elements, bg, files)
    text_lines = []
    for e in elements:
        if e["type"] == "text":
            text_lines.append(f'{e["text"]} ^{e["id"]}\n')
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write("---\n\nexcalidraw-plugin: raw\ntags: [excalidraw]\n\n---\n")
        f.write("==⚠  Switch to EXCALIDRAW VIEW in the MORE OPTIONS menu of this document. ⚠==\n\n")
        f.write("# Excalidraw Data\n\n## Text Elements\n")
        for tl in text_lines: f.write(tl)
        f.write("\n\n%%\n## Drawing\n```json\n")
        json.dump(scene, f, ensure_ascii=False)
        f.write("\n```\n%%\n")
    print(f"  ✓ {os.path.basename(filepath)} ({len(elements)} elements)")
