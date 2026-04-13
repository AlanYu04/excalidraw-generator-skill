#!/usr/bin/env python3
"""
Generate the "How It Works" flowchart for README using the skill's own engine.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.engine import (
    rect, text_standalone, labeled_rect, labeled_ellipse, arrow, ellipse,
    line, numbered_circle, save_obsidian_md, save_excalidraw
)

OBSIDIAN = "/Users/alan/Library/Mobile Documents/iCloud~md~obsidian/Documents/Excalidraw"
EXAMPLES = os.path.dirname(os.path.abspath(__file__))


def diagram_how_it_works():
    els = []
    cx = 500

    # Colors
    PURPLE_FG, PURPLE_BG = "#6965d5", "#d0bfff"
    BLUE_FG, BLUE_BG = "#1971c2", "#a5d8ff"
    GREEN_FG, GREEN_BG = "#2f9e44", "#b2f2bb"
    ORANGE_FG, ORANGE_BG = "#e8590c", "#ffd8a8"
    TEAL_FG, TEAL_BG = "#0c8599", "#99e9f2"
    GRAY_FG = "#495057"

    # Title
    els.append(text_standalone(cx, 30, "How It Works — Excalidraw Generator", fs=24, color=PURPLE_FG))

    # ---- Step 1: User Input ----
    y1 = 70
    els.extend(labeled_ellipse(cx - 80, y1, 160, 45, "User Request", fill=PURPLE_BG, stroke=PURPLE_FG, sw=2, fs=16, label_color=PURPLE_FG))
    els.append(text_standalone(cx, y1 + 35, '"Draw a pipeline diagram"', fs=11, color=GRAY_FG))

    # Arrow down
    els.append(arrow(cx, y1 + 48, 0, 12, stroke=GRAY_FG, sw=2))

    # ---- Step 2: Config Selection ----
    y2 = y1 + 50
    cfg_w = 140
    cfg_h = 50
    cfg_gap = 20

    configs = [
        ("Style", "Vivid / Clean\n/ Sketch", PURPLE_BG, PURPLE_FG),
        ("Fill", "solid / hachure\n/ cross-hatch", BLUE_BG, BLUE_FG),
        ("Roughness", "0 / 1 / 2", GREEN_BG, GREEN_FG),
        ("Font", "Virgil / Helvetica\n/ Cascadia", ORANGE_BG, ORANGE_FG),
    ]

    cfg_total_w = 4 * cfg_w + 3 * cfg_gap
    cfg_sx = cx - cfg_total_w / 2

    for i, (title, desc, fill, sc) in enumerate(configs):
        x = cfg_sx + i * (cfg_w + cfg_gap)
        els.extend(labeled_rect(x, y2, cfg_w, cfg_h, f"{title}\n{desc}",
                     fill=fill, stroke=sc, sw=2, fs=11))

    # Bracket label
    els.append(text_standalone(cx, y2 - 12, "User selects:", fs=12, color=GRAY_FG))

    # Arrow down
    els.append(arrow(cx, y2 + cfg_h + 3, 0, 20, stroke=GRAY_FG, sw=2))

    # ---- Step 3: Style Loader ----
    y3 = y2 + cfg_h + 45
    loader_w = cfg_total_w
    els.extend(labeled_rect(cfg_sx, y3, loader_w, 40,
        "Style Loader — load_style() → StyleConfig(colors, layout, fill_style, roughness, font)",
        fill="#f8f9fa", stroke=GRAY_FG, sw=2, fs=12))

    # Arrow down
    els.append(arrow(cx, y3 + 40 + 3, 0, 20, stroke=GRAY_FG, sw=2))

    # ---- Step 4: Script Generator ----
    y4 = y3 + 65
    gen_w = loader_w

    # Main generator box
    els.extend(labeled_rect(cfg_sx, y4, gen_w, 30,
        "Python Script Generator", fill=TEAL_BG, stroke=TEAL_FG, sw=2, fs=14))

    # Sub-functions
    funcs = [
        ("labeled_rect()", "auto-center text"),
        ("arrow()", "connect nodes"),
        ("numbered_circle()", "step badges"),
        ("text_standalone()", "CJK-aware text"),
    ]
    func_w = gen_w / 4 - 5
    for i, (fn, desc) in enumerate(funcs):
        x = cfg_sx + i * (func_w + 6) + 3
        els.extend(labeled_rect(x, y4 + 35, func_w, 40,
            f"{fn}\n{desc}", fill="#f8f9fa", stroke=TEAL_FG, sw=1, fs=10, label_color=GRAY_FG))

    # Arrow down
    els.append(arrow(cx, y4 + 78, 0, 20, stroke=GRAY_FG, sw=2))

    # ---- Step 5: Execute ----
    y5 = y4 + 100
    els.extend(labeled_ellipse(cx - 70, y5, 140, 40, "Python Execute", fill="#fff3bf", stroke="#f08c00", sw=2, fs=14, label_color="#f08c00"))

    # Arrow down
    els.append(arrow(cx, y5 + 42, 0, 12, stroke=GRAY_FG, sw=2))

    # ---- Step 6: Output ----
    y6 = y5 + 45
    out_w = 200
    out_h = 45

    # .excalidraw output
    els.extend(labeled_rect(cx - out_w - 20, y6, out_w, out_h,
        ".excalidraw\nPure JSON for any tool",
        fill=BLUE_BG, stroke=BLUE_FG, sw=2, fs=12))

    # .excalidraw.md output
    els.extend(labeled_rect(cx + 20, y6, out_w, out_h,
        ".excalidraw.md\nObsidian plugin format",
        fill=GREEN_BG, stroke=GREEN_FG, sw=2, fs=12))

    # Arrow split
    els.append(arrow(cx - 20, y6 + out_h / 2, -30, 0, stroke=BLUE_FG, sw=2))
    els.append(arrow(cx + 20, y6 + out_h / 2, 0, 0, stroke=GREEN_FG, sw=2))

    save_obsidian_md(os.path.join(OBSIDIAN, "how-it-works.excalidraw.md"), els)
    save_excalidraw(os.path.join(EXAMPLES, "how-it-works.excalidraw"), els)
    print("  How It Works flowchart")


if __name__ == "__main__":
    print("Generating README assets...")
    diagram_how_it_works()
    print("Done")
