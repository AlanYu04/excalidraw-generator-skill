#!/usr/bin/env python3
"""
Style demos v3 — Vivid / Clean / Sketch with proper style application.
Each demo reads its StyleConfig and applies font_family, fill_style, roughness, etc.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.engine import (
    rect, text_standalone, labeled_rect, arrow, ellipse, diamond,
    line, numbered_circle, save_obsidian_md
)
from styles.conference import vivid_style
from styles.journal import clean_style
from styles.ppt import sketch_style

OBSIDIAN = "/Users/alan/Library/Mobile Documents/iCloud~md~obsidian/Documents/Excalidraw"


# ============================================================================
# VIVID: Rich, colorful, detailed — fontFamily=3 (Cascadia), fillStyle=solid
# ============================================================================
def demo_vivid():
    s = vivid_style()
    els = []
    cx = 480
    # Shortcuts from style
    ff = s.font_family       # 3 = Cascadia
    fs_body = s.body_size     # 14
    fs_label = s.label_size   # 11
    fs_title = s.title_size   # 22
    rough = s.roughness       # 1
    fsty = s.fill_style       # "solid"

    els.append(text_standalone(cx, 30, "Vivid Style — Rich & Detailed", fs=fs_title, color=s.primary, font_family=ff))
    els.append(text_standalone(cx, 55, "Cascadia 字体 · solid 填充 · roughness=1 · 丰富配色", fs=12, color=s.accent, font_family=ff))

    # 6-step pipeline with numbered badges
    pipeline = [
        ("Sensors\n传感器", s.primary_fill, s.primary),
        ("Calibration\n校准", s.info_fill, s.info),
        ("Filtering\n滤波", s.success_fill, s.success),
        ("Fusion\n融合", "#d0bfff", "#7048e8"),
        ("State s_t\n状态构建", s.warning_fill, s.warning),
        ("RL Policy\n策略网络", s.accent_fill, s.accent),
    ]

    bw, bh = 120, 65
    gap = 22
    sx = 30
    y1 = 90

    for i, (label, fill, sc) in enumerate(pipeline):
        x = sx + i * (bw + gap)
        els.extend(numbered_circle(x + 15, y1 + 12, i + 1, fill, sc))
        els.extend(labeled_rect(x, y1, bw, bh, label, fill=fill, stroke=sc, sw=2,
                     fs=fs_body, roughness=rough, font_family=ff, fill_style=fsty))
        if i < 5:
            els.append(arrow(x + bw + 2, y1 + bh / 2, gap - 4, 0, stroke=s.muted, sw=2, roughness=rough))

    # Detail sub-cards
    details = [
        "PT100 / NDIR\n电容 / PAR\nFDR / pH",
        "零点漂移\n灵敏度补偿\n线性化校正",
        "Kalman 滤波\n移动平均\n异常值剔除",
        "多传感器冗余\n贝叶斯融合\n置信度加权",
        "归一化 [0,1]\n时间对齐 1Hz\ns_t ∈ R¹¹",
        "SAC / PPO\nπ(a|s; θ)\n连续动作空间",
    ]
    y2 = y1 + bh + 15
    for i, (detail, (_, _, sc)) in enumerate(zip(details, pipeline)):
        x = sx + i * (bw + gap)
        els.extend(labeled_rect(x, y2, bw, 55, detail, fill="#f8f9fa", stroke=sc, sw=1,
                     fs=fs_label, label_color=s.muted, roughness=rough, font_family=ff, fill_style=fsty))

    # 11-dimension grid
    y3 = y2 + 75
    els.append(text_standalone(cx, y3, "11-Dimensional State Vector", fs=16, color=s.primary, font_family=ff))

    dims = [
        ("T_in", s.primary_fill, s.primary), ("RH", s.primary_fill, s.primary),
        ("CO₂", s.primary_fill, s.primary), ("PAR", s.primary_fill, s.primary),
        ("SM", s.success_fill, s.success), ("T_out", s.info_fill, s.info),
        ("RH_out", s.info_fill, s.info), ("WS", s.info_fill, s.info),
        ("Rad", s.info_fill, s.info), ("DoP", s.accent_fill, s.accent),
        ("Yield", s.accent_fill, s.accent),
    ]
    cw, ch = 150, 28
    cgap_x, cgap_y = 12, 5
    y4 = y3 + 22
    for i, (name, fill, sc) in enumerate(dims):
        col, row = i % 4, i // 4
        x = 40 + col * (cw + cgap_x)
        y = y4 + row * (ch + cgap_y)
        els.extend(labeled_rect(x, y, cw, ch, name, fill=fill, stroke=sc, sw=1,
                     fs=fs_body, roughness=rough, font_family=ff, fill_style=fsty))

    # Result highlight
    y5 = y4 + 3 * (ch + cgap_y) + 20
    els.append(rect(30, y5, 930, 45, fill=s.success_fill, stroke=s.success, sw=3,
                roughness=rough, fill_style=fsty))
    els.append(text_standalone(cx, y5 + 14, "Vivid: Cascadia(fontFamily=3) + solid + roughness=1 + 7色", fs=16, color=s.success, font_family=ff))

    save_obsidian_md(os.path.join(OBSIDIAN, "demo-vivid.excalidraw.md"), els)
    print("  Vivid (rich)")


# ============================================================================
# CLEAN: Minimal, black & white — fontFamily=2 (Helvetica), fillStyle=solid, roughness=0
# ============================================================================
def demo_clean():
    s = clean_style()
    els = []
    cx = 400
    ff = s.font_family       # 2 = Helvetica
    rough = s.roughness       # 0
    fsty = s.fill_style       # "solid"

    els.append(text_standalone(cx, 25, "Clean Style — Minimal Data Flow", fs=s.title_size, color="#000000", font_family=ff))

    # 5 nodes, white fill, thin black border
    nodes = {
        "env":     (cx, 90, 140, 40),
        "sensor":  (150, 180, 130, 40),
        "state":   (150, 260, 130, 40),
        "policy":  (650, 260, 130, 40),
        "action":  (650, 180, 130, 40),
    }
    labels = {
        "env": "Environment", "sensor": "Sensors",
        "state": "State s_t", "policy": "Policy π", "action": "Actuator",
    }

    for key, (nx, ny, nw, nh) in nodes.items():
        els.extend(labeled_rect(nx - nw/2, ny - nh/2, nw, nh, labels[key],
                     fill="#ffffff", stroke="#000000", sw=1, fs=s.body_size,
                     roughness=0, font_family=2, fill_style=fsty, label_color="#000000"))

    # Thin black arrows
    e = nodes["env"]; sn = nodes["sensor"]
    els.append(arrow(e[0]-e[2]/2, e[1]+e[3]/2+2,
              sn[0]+sn[2]/2-e[0]+e[2]/2, sn[1]-sn[3]/2-e[1]-e[3]/2-4,
              stroke="#000000", sw=1, roughness=0))
    els.append(arrow(sn[0], sn[1]+sn[3]/2+2, 0,
              nodes["state"][1]-nodes["state"][3]/2-sn[1]-sn[3]/2-4,
              stroke="#000000", sw=1, roughness=0))
    st = nodes["state"]; p = nodes["policy"]
    els.append(arrow(st[0]+st[2]/2+2, st[1],
              p[0]-p[2]/2-st[0]-st[2]/2-4, 0, stroke="#000000", sw=1, roughness=0))
    a = nodes["policy"]
    els.append(arrow(a[0], a[1]-a[3]/2-2, 0,
              e[1]+e[3]/2-a[1]+a[3]/2+4, stroke="#000000", sw=1, roughness=0))

    for lx, ly, lt in [(270,125,"observe"), (120,220,"raw signal"),
                        (400,275,"s_t ∈ R^n"), (680,220,"a_t"), (540,125,"actuate")]:
        els.append(text_standalone(lx, ly, lt, fs=s.caption_size, color="#666666", font_family=2))

    # Compact dimension table
    y_tab = 310
    els.append(text_standalone(cx, y_tab, "State Dimensions", fs=s.body_size, color="#000000", font_family=2))

    dims = ["T_in [°C]", "RH [%]", "CO₂ [ppm]", "PAR [μmol]",
            "SM [m³/m³]", "T_out [°C]", "RH_out [%]", "WS [m/s]",
            "Rad [W/m²]", "DoP [day]", "Yield [kg]"]
    cw, ch = 140, 20
    cgap_x, cgap_y = 10, 3
    tx = cx - (2*cw + 1.5*cgap_x)
    ty = y_tab + 18
    for i, dim in enumerate(dims):
        col, row = i % 4, i // 4
        x = tx + col * (cw + cgap_x)
        y = ty + row * (ch + cgap_y)
        els.extend(labeled_rect(x, y, cw, ch, dim,
                     fill="#ffffff", stroke="#999999", sw=1, fs=s.label_size,
                     roughness=0, font_family=2, fill_style=fsty, label_color="#000000"))

    els.append(text_standalone(cx, ty + 3*(ch+cgap_y) + 15,
        "Clean: Helvetica(fontFamily=2) + B&W + roughness=0 + 无装饰", fs=s.caption_size, color="#666666", font_family=2))

    save_obsidian_md(os.path.join(OBSIDIAN, "demo-clean.excalidraw.md"), els)
    print("  Clean (minimal)")


# ============================================================================
# SKETCH: Hand-drawn, rough, big — fontFamily=1 (Virgil), fillStyle=hachure, roughness=2
# ============================================================================
def demo_sketch():
    s = sketch_style()
    els = []
    cx = 500
    ff = s.font_family       # 1 = Virgil (handwritten)
    rough = s.roughness       # 2
    fsty = s.fill_style       # "hachure"

    els.append(text_standalone(cx, 35, "Sketch Style — Hand-Drawn & Bold", fs=s.title_size, color=s.primary, font_family=ff))
    els.append(text_standalone(cx, 68, "Virgil 手写字体 · hachure 斜线填充 · roughness=2", fs=s.subtitle_size, color=s.muted, font_family=ff))

    # 3 big feature cards
    cards = [
        ("手绘线条", "roughness = 2\n线条自然弯曲\n有人情味", s.primary_fill, s.primary),
        ("手写字体", "Virgil (fontFamily=1)\n不是等宽字体\n而是手写风格", s.success_fill, s.success),
        ("斜线填充", "hachure 填充\n不是纯色块\n而是斜线纹理", s.accent_fill, s.accent),
    ]
    cw, ch = 250, 130
    cgap = 30
    csx = cx - (1.5*cw + cgap)
    cy = 110

    for i, (title, desc, fill, sc) in enumerate(cards):
        x = csx + i * (cw + cgap)
        els.extend(numbered_circle(x+22, cy+18, i+1, fill, sc))
        els.extend(labeled_rect(x, cy, cw, 40, title, fill=fill, stroke=sc, sw=3,
                     fs=s.body_size, roughness=rough, font_family=ff, fill_style=fsty))
        els.extend(labeled_rect(x, cy+48, cw, 82, desc, fill="#f8f9fa", stroke=sc, sw=1,
                     fs=s.label_size, label_color="#495057", roughness=rough, font_family=ff, fill_style=fsty))

    # Big flow
    steps = [
        ("Input", s.primary_fill, s.primary),
        ("Process", s.info_fill, s.info),
        ("Model", "#d0bfff", "#7048e8"),
        ("Output", s.success_fill, s.success),
    ]
    sw, sh = 180, 80
    sgap = 40
    ssx = cx - (2*sw + 1.5*sgap)
    sy = 270
    for i, (label, fill, sc) in enumerate(steps):
        x = ssx + i * (sw + sgap)
        els.extend(labeled_rect(x, sy, sw, sh, label, fill=fill, stroke=sc, sw=3,
                     fs=s.subtitle_size, roughness=rough, font_family=ff, fill_style=fsty))
        if i < 3:
            els.append(arrow(x+sw+3, sy+sh/2, sgap-6, 0, stroke="#495057", sw=3, roughness=rough))

    # Bottom bar
    y_bar = sy + sh + 30
    els.append(rect(60, y_bar, 880, 45, fill="#d0bfff", stroke="#7048e8", sw=3,
                roughness=rough, fill_style=fsty))
    els.append(text_standalone(cx, y_bar + 22,
        "Sketch: Virgil(fontFamily=1) + hachure填充 + roughness=2 + 手绘感",
        fs=s.body_size, color="#7048e8", font_family=ff))

    save_obsidian_md(os.path.join(OBSIDIAN, "demo-sketch.excalidraw.md"), els)
    print("  Sketch (hand-drawn)")


if __name__ == "__main__":
    print("Generating v3 demos with proper style params...")
    print()
    demo_vivid()
    demo_clean()
    demo_sketch()
    print()
    print(f"Saved to: {OBSIDIAN}")
