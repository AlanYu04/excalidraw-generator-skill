"""P1 Demo: Generate 3 feature-showcase .excalidraw files."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.engine import (
    rect, labeled_rect, labeled_diamond, labeled_ellipse,
    arrow, line, text_standalone, group, frame, bind_arrow,
    ellipse, diamond, save_excalidraw,
)
from core.icons import icon, list_icons


def flatten(*args):
    result = []
    for item in args:
        if isinstance(item, list):
            result.extend(flatten(*item))
        else:
            result.append(item)
    return result


def demo_element_types():
    """Showcase: labeled_rect vs labeled_diamond vs labeled_ellipse + bind_arrow."""
    title = text_standalone(400, 30, "Element Builders Showcase", fs=28, color="#1e1e1e")

    # --- Section 1: Three labeled shapes side by side ---
    section1_label = text_standalone(200, 90, "labeled_rect   labeled_diamond   labeled_ellipse", fs=14, color="#868e96")

    lr = labeled_rect(50, 120, 180, 80, "labeled_rect", fill="#a5d8ff", stroke="#1971c2")
    ld = labeled_diamond(290, 110, 200, 120, "labeled_diamond", fill="#b2f2bb", stroke="#2f9e44")
    le = labeled_ellipse(550, 120, 180, 100, "labeled_ellipse", fill="#ffd8a8", stroke="#e8590c")

    # --- Section 2: Plain shapes (no label) ---
    section2_label = text_standalone(200, 270, "Base shapes: rect   ellipse   diamond   line   arrow", fs=14, color="#868e96")

    r = rect(50, 300, 120, 70, stroke="#495057")
    e = ellipse(210, 300, 100, 70, stroke="#495057")
    d = diamond(350, 295, 100, 80, stroke="#495057")
    ln = line(490, 335, 80, 0, stroke="#495057")
    ar = arrow(610, 335, 80, 0, stroke="#495057")

    shape_labels = flatten(
        text_standalone(110, 390, "rect()", fs=12, color="#868e96"),
        text_standalone(260, 390, "ellipse()", fs=12, color="#868e96"),
        text_standalone(400, 390, "diamond()", fs=12, color="#868e96"),
        text_standalone(530, 370, "line()", fs=12, color="#868e96"),
        text_standalone(650, 370, "arrow()", fs=12, color="#868e96"),
    )

    # --- Section 3: bind_arrow vs plain arrow ---
    section3_label = text_standalone(200, 440, "bind_arrow() — arrow snaps to elements when moved", fs=14, color="#868e96")

    # Before: plain arrow
    ba_r1 = labeled_rect(50, 480, 140, 50, "Element A", stroke="#1971c2")
    ba_r2 = labeled_rect(300, 480, 140, 50, "Element B", stroke="#1971c2")
    plain_a = arrow(190, 505, 110, 0, stroke="#adb5bd", sw=2)
    plain_note = text_standalone(250, 550, "plain arrow — no binding", fs=11, color="#adb5bd")

    # After: bound arrow
    bb_r1 = labeled_rect(500, 480, 140, 50, "Element A", stroke="#2f9e44")
    bb_r2 = labeled_rect(750, 480, 140, 50, "Element B", stroke="#2f9e44")
    bound_a = bind_arrow(arrow(640, 505, 110, 0, stroke="#2f9e44", sw=2), bb_r1[0], bb_r2[0])
    bound_note = text_standalone(700, 550, "bind_arrow — bound to elements", fs=11, color="#2f9e44")

    elements = flatten(
        title,
        section1_label, lr, ld, le,
        section2_label, r, e, d, ln, ar, shape_labels,
        section3_label,
        ba_r1, ba_r2, plain_a, plain_note,
        bb_r1, bb_r2, bound_a, bound_note,
    )
    save_excalidraw("examples/element-types.excalidraw", elements)


def demo_icons_frames_groups():
    """Showcase: all 10 icons + frame() + group()."""
    title = text_standalone(400, 30, "Icons · Frames · Groups", fs=28, color="#1e1e1e")

    # --- All 10 icons in a grid ---
    icon_names = list_icons()
    icons_per_row = 5
    x_start, y_start = 40, 80
    x_step, y_step = 150, 110

    icon_elements = []
    for i, name in enumerate(icon_names):
        col = i % icons_per_row
        row = i // icons_per_row
        ix = x_start + col * x_step
        iy = y_start + row * y_step
        ic = icon(name, x=ix + 20, y=iy, stroke="#495057", scale=1.0)
        label = text_standalone(ix + 44, iy + 65, name, fs=12, color="#495057")
        icon_elements.extend(flatten(ic))
        icon_elements.append(label)

    # --- frame() demo ---
    frame_title = text_standalone(130, 330, "frame() — named regions", fs=16, color="#868e96")
    f1 = frame(30, 360, 240, 130, "Region A", stroke="#1971c2")
    f1_inner = labeled_rect(50, 390, 200, 50, "content inside frame", stroke="#1971c2")
    f2 = frame(290, 360, 240, 130, "Region B", stroke="#e8590c")
    f2_inner = labeled_rect(310, 390, 200, 50, "content inside frame", stroke="#e8590c")

    # --- group() demo ---
    group_title = text_standalone(600, 330, "group() — drag together", fs=16, color="#868e96")

    # Ungrouped
    ug_note = text_standalone(570, 360, "Before (separate):", fs=12, color="#adb5bd")
    ug_r1 = rect(560, 385, 50, 40, stroke="#adb5bd", sw=1)
    ug_r2 = rect(620, 385, 50, 40, stroke="#adb5bd", sw=1)
    ug_r3 = rect(680, 385, 50, 40, stroke="#adb5bd", sw=1)

    # Grouped
    g_note = text_standalone(570, 450, "After group() — moves as one:", fs=12, color="#2f9e44")
    g_r1 = rect(560, 475, 50, 40, stroke="#2f9e44", sw=2)
    g_r2 = rect(620, 475, 50, 40, stroke="#2f9e44", sw=2)
    g_r3 = rect(680, 475, 50, 40, stroke="#2f9e44", sw=2)
    grouped = group([g_r1, g_r2, g_r3])

    # Highlight around grouped
    g_box = rect(555, 470, 180, 50, stroke="#2f9e44", sw=1, fill="transparent", stroke_style="dashed")

    elements = flatten(
        title,
        icon_elements,
        frame_title, f1, f1_inner, f2, f2_inner,
        group_title, ug_note, ug_r1, ug_r2, ug_r3,
        g_note, grouped, g_box,
    )
    save_excalidraw("examples/icons-frames-groups.excalidraw", elements)


def demo_features_overview():
    """One overview diagram: all new v1.1 features in frames."""
    # Main title
    title = text_standalone(420, 20, "v1.1 New Features Overview", fs=30, color="#1e1e1e")

    # --- Feature 1: New labeled shapes ---
    f1 = frame(20, 70, 380, 180, "New Labeled Shapes", stroke="#1971c2")
    f1_lr = labeled_rect(40, 120, 100, 50, "labeled_rect", fill="#a5d8ff", stroke="#1971c2", fs=11)
    f1_ld = labeled_diamond(170, 110, 130, 80, "labeled_diamond", fill="#b2f2bb", stroke="#2f9e44", fs=11)
    f1_le = labeled_ellipse(330, 115, 60, 60, "ellipse", fill="#ffd8a8", stroke="#e8590c", fs=11)
    f1_code = text_standalone(210, 215, "containerId binding for auto-centering", fs=11, color="#868e96")

    # --- Feature 2: Arrow binding ---
    f2 = frame(420, 70, 380, 180, "bind_arrow()", stroke="#2f9e44")
    f2_a = labeled_rect(440, 120, 90, 40, "A", stroke="#2f9e44")
    f2_b = labeled_rect(690, 120, 90, 40, "B", stroke="#2f9e44")
    f2_arrow = bind_arrow(arrow(530, 140, 160, 0, stroke="#2f9e44", sw=2), f2_a[0], f2_b[0])
    f2_note = text_standalone(610, 215, "arrow follows element when moved", fs=11, color="#2f9e44")

    # --- Feature 3: Icons ---
    f3 = frame(20, 280, 380, 140, "Icon Library (10 icons)", stroke="#e8590c")
    mini_icons = []
    icon_names_short = ["database", "user", "cloud", "server", "gear",
                        "document", "shield", "check", "warning", "arrow-right"]
    for i, name in enumerate(icon_names_short):
        col = i % 5
        row = i // 5
        ix = 40 + col * 72
        iy = 310 + row * 60
        mini_icons.extend(flatten(icon(name, x=ix, y=iy, stroke="#e8590c", scale=0.6)))

    # --- Feature 4: Frame + Group ---
    f4 = frame(420, 280, 380, 140, "frame() + group()", stroke="#7048e8")
    f4_inner1 = rect(440, 310, 50, 40, stroke="#7048e8", sw=2)
    f4_inner2 = rect(500, 310, 50, 40, stroke="#7048e8", sw=2)
    f4_grouped = group([f4_inner1, f4_inner2])
    f4_note = text_standalone(600, 340, "grouped — drag together", fs=11, color="#7048e8")
    f4_inner3 = labeled_rect(440, 370, 140, 35, "inside frame()", stroke="#7048e8", fs=11)

    # --- Feature 5: image_embed ---
    f5 = frame(20, 450, 380, 100, "image_embed()", stroke="#0c8599")
    f5_note = text_standalone(210, 510, "embed base64 images with files dict", fs=12, color="#0c8599")

    # --- Feature 6: CJK ---
    f6 = frame(420, 450, 380, 100, "CJK Support", stroke="#c2255c")
    f6_cjk = labeled_ellipse(460, 470, 80, 40, "中文文本", fill="#fcc2d7", stroke="#c2255c", fs=13, font_family=5)
    f6_note = text_standalone(600, 510, "font_family=5 for CJK fonts", fs=12, color="#c2255c")

    elements = flatten(
        title,
        f1, f1_lr, f1_ld, f1_le, f1_code,
        f2, f2_a, f2_b, f2_arrow, f2_note,
        f3, mini_icons,
        f4, f4_grouped, f4_note, f4_inner3,
        f5, f5_note,
        f6, f6_cjk, f6_note,
    )
    save_excalidraw("examples/features-overview.excalidraw", elements)


if __name__ == "__main__":
    demo_element_types()
    demo_icons_frames_groups()
    demo_features_overview()
    print("\nAll 3 feature-showcase demos generated!")
