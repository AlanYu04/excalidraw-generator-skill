#!/usr/bin/env python3
"""Generate per-feature demo .excalidraw files for all major features."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.engine import (
    rect, labeled_rect, labeled_diamond, labeled_ellipse,
    arrow, line, text_standalone, group, frame, bind_arrow,
    ellipse, save_excalidraw, connect,
)
from core.charts import bar_chart, horizontal_bar_chart, line_chart, pie_chart
from core.icons import icon, list_icons
from core.svg_converter import svg_to_elements


def flatten(*args):
    """Recursively flatten nested lists into a single list of elements."""
    result = []
    for item in args:
        if isinstance(item, list):
            result.extend(flatten(*item))
        else:
            result.append(item)
    return result


# ---------------------------------------------------------------------------
# 1. Charts Demo
# ---------------------------------------------------------------------------
def demo_charts():
    """4 charts in a 2x2 layout."""
    title = text_standalone(500, 30, "Charts — bar_chart, h_bar, line, pie", fs=26, color="#1e1e1e")

    # --- Top-left: bar_chart ---
    section_tl = text_standalone(200, 80, "bar_chart()", fs=16, color="#868e96")
    chart_tl = bar_chart(
        x=30, y=110,
        data={"React": 85, "Vue": 72, "Angular": 58, "Svelte": 45, "Solid": 38},
        title="Framework Popularity",
        bar_color="#a5d8ff",
        bar_colors={
            "React": "#a5d8ff",
            "Vue": "#b2f2bb",
            "Angular": "#ffd8a8",
            "Svelte": "#fcc2d7",
            "Solid": "#d0bfff",
        },
        bar_width=50,
        max_height=180,
        gap=20,
        fs=13,
        show_values=True,
        show_grid=True,
        roughness=1,
    )

    # --- Top-right: horizontal_bar_chart ---
    section_tr = text_standalone(640, 80, "horizontal_bar_chart()", fs=16, color="#868e96")
    chart_tr = horizontal_bar_chart(
        x=540, y=120,
        data={"Python": 90, "JavaScript": 85, "TypeScript": 75, "Rust": 60, "Go": 55},
        title="Language Usage",
        bar_color="#a5d8ff",
        bar_colors={
            "Python": "#ffd43b",
            "JavaScript": "#fcc2d7",
            "TypeScript": "#74c0fc",
            "Rust": "#b2f2bb",
            "Go": "#d0bfff",
        },
        bar_height=35,
        max_width=220,
        gap=12,
        fs=13,
        show_values=True,
        roughness=1,
    )

    # --- Bottom-left: line_chart ---
    section_bl = text_standalone(240, 450, "line_chart()", fs=16, color="#868e96")
    chart_bl = line_chart(
        x=30, y=490,
        data={
            "Revenue": [30, 45, 42, 60, 55, 80],
            "Cost": [20, 25, 30, 28, 35, 40],
        },
        labels=["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
        title="Revenue vs Cost",
        series_colors={"Revenue": "#1971c2", "Cost": "#e8590c"},
        chart_width=400,
        chart_height=200,
        fs=12,
        show_grid=True,
        show_points=True,
        roughness=1,
    )

    # --- Bottom-right: pie_chart ---
    section_br = text_standalone(740, 450, "pie_chart()", fs=16, color="#868e96")
    chart_br = pie_chart(
        x=580, y=490,
        data={"Direct": 35, "Organic": 30, "Referral": 20, "Social": 15},
        title="Traffic Sources",
        show_percentages=True,
        roughness=1,
    )

    elements = flatten(
        title,
        section_tl, chart_tl,
        section_tr, chart_tr,
        section_bl, chart_bl,
        section_br, chart_br,
    )
    save_excalidraw("examples/demo-charts.excalidraw", elements)


# ---------------------------------------------------------------------------
# 2. Flowchart Demo
# ---------------------------------------------------------------------------
def demo_flowchart():
    """A complete flowchart: Start → Process → Decision → End/Loop."""
    title = text_standalone(400, 30, "Flowchart — Shapes & Arrows", fs=26, color="#1e1e1e")

    # --- Nodes ---
    start = labeled_ellipse(340, 80, 120, 50, "Start",
                            fill="#d0bfff", stroke="#7048e8", fs=18)

    process = labeled_rect(330, 200, 140, 60, "Process Data",
                           fill="#a5d8ff", stroke="#1971c2", fs=16)

    decision = labeled_diamond(310, 330, 180, 120, "Valid?",
                               fill="#ffd8a8", stroke="#e8590c", fs=16)

    save_result = labeled_rect(330, 530, 140, 60, "Save Result",
                               fill="#b2f2bb", stroke="#2f9e44", fs=16)

    end = labeled_ellipse(345, 680, 110, 50, "End",
                          fill="#d0bfff", stroke="#7048e8", fs=18)

    # --- Arrows ---
    # Start → Process
    a1 = arrow(400, 130, 0, 70, stroke="#495057", sw=2)
    lbl1 = text_standalone(430, 155, "", fs=11, color="#868e96")

    # Process → Decision
    a2 = arrow(400, 260, 0, 70, stroke="#495057", sw=2)
    lbl2 = text_standalone(420, 290, "validate", fs=11, color="#868e96")

    # Decision → Save Result (Yes)
    a3 = arrow(400, 450, 0, 80, stroke="#2f9e44", sw=2)
    lbl_yes = text_standalone(420, 470, "Yes", fs=13, color="#2f9e44")

    # Decision → Process Data (No — loop back)
    # Go left from decision, then up to process
    a4_no_right = arrow(310, 390, -140, 0, stroke="#e8590c", sw=2)
    a4_no_up = arrow(170, 390, 0, -130, stroke="#e8590c", sw=2)
    a4_no_right2 = arrow(170, 260, 160, 0, stroke="#e8590c", sw=2)
    lbl_no = text_standalone(220, 370, "No", fs=13, color="#e8590c")

    # Save Result → End
    a5 = arrow(400, 590, 0, 90, stroke="#495057", sw=2)
    lbl5 = text_standalone(420, 630, "done", fs=11, color="#868e96")

    elements = flatten(
        title,
        start, process, decision, save_result, end,
        a1, lbl1,
        a2, lbl2,
        a3, lbl_yes,
        a4_no_right, a4_no_up, a4_no_right2, lbl_no,
        a5, lbl5,
    )
    save_excalidraw("examples/demo-flowchart.excalidraw", elements)


# ---------------------------------------------------------------------------
# 3. Icons Demo
# ---------------------------------------------------------------------------
def demo_icons():
    """Render all built-in icons in a grid."""
    all_names = list_icons()
    title = text_standalone(
        450, 30, f"{len(all_names)} Built-in Icons", fs=26, color="#1e1e1e",
    )

    cols = 5
    icon_scale = 0.8
    icon_size = 48 * icon_scale
    cell_w = 130
    cell_h = 90
    start_x = 40
    start_y = 80

    elements_list = [title]

    for idx, name in enumerate(all_names):
        row = idx // cols
        col = idx % cols
        cx = start_x + col * cell_w
        cy = start_y + row * cell_h

        # Icon at center of cell
        icon_els = icon(name, cx + cell_w / 2 - icon_size / 2, cy,
                        stroke="#495057", scale=icon_scale)
        elements_list.extend(icon_els)

        # Label below icon
        label = text_standalone(
            cx + cell_w / 2, cy + icon_size + 14,
            name, fs=10, color="#868e96",
        )
        elements_list.append(label)

    save_excalidraw("examples/demo-icons.excalidraw", elements_list)


# ---------------------------------------------------------------------------
# 4. SVG Demo
# ---------------------------------------------------------------------------
def demo_svg():
    """Showcase SVG-to-Excalidraw conversion with various shapes."""
    title = text_standalone(400, 30, "SVG-to-Excalidraw Converter", fs=26, color="#1e1e1e")

    # --- Section 1: Simple shapes ---
    section1 = text_standalone(200, 90, "SVG shapes → Excalidraw elements", fs=14, color="#868e96")

    # Rectangle from SVG
    svg_rect = '<svg viewBox="0 0 100 80"><rect x="10" y="10" width="80" height="60" fill="#a5d8ff" stroke="#1971c2"/></svg>'
    rect_els = svg_to_elements(svg_rect, x=30, y=120, scale=1.0, stroke="#1971c2")
    rect_label = text_standalone(70, 230, "SVG <rect>", fs=12, color="#868e96")

    # Circle from SVG
    svg_circle = '<svg viewBox="0 0 100 100"><circle cx="50" cy="50" r="40" fill="#b2f2bb" stroke="#2f9e44"/></svg>'
    circle_els = svg_to_elements(svg_circle, x=180, y=120, scale=1.0, stroke="#2f9e44")
    circle_label = text_standalone(220, 250, "SVG <circle>", fs=12, color="#868e96")

    # Triangle from SVG path
    svg_tri = '<svg viewBox="0 0 100 100"><path d="M50 10 L90 90 L10 90 Z" fill="#ffd8a8" stroke="#e8590c"/></svg>'
    tri_els = svg_to_elements(svg_tri, x=320, y=120, scale=1.0, stroke="#e8590c")
    tri_label = text_standalone(360, 250, "SVG <path>", fs=12, color="#868e96")

    # --- Section 2: Bezier curves ---
    section2 = text_standalone(200, 270, "Bezier curves → polyline elements", fs=14, color="#868e96")

    svg_curve = '<svg viewBox="0 0 200 100"><path d="M10 50 C 40 10 60 90 100 50 S 160 10 190 50" stroke="#7048e8" fill="none" stroke-width="3"/></svg>'
    curve_els = svg_to_elements(svg_curve, x=50, y=300, scale=1.0, stroke="#7048e8")
    curve_label = text_standalone(150, 420, "Cubic Bezier curve", fs=12, color="#868e96")

    # --- Section 3: Star ---
    section3 = text_standalone(470, 270, "Star from SVG path", fs=14, color="#868e96")
    svg_star = '<svg viewBox="0 0 100 100"><path d="M50 5 L61 35 L95 35 L68 57 L79 90 L50 70 L21 90 L32 57 L5 35 L39 35 Z" fill="#ffd43b" stroke="#f08c00"/></svg>'
    star_els = svg_to_elements(svg_star, x=460, y=300, scale=0.8, stroke="#f08c00")
    star_label = text_standalone(490, 400, "Complex polygon", fs=12, color="#868e96")

    elements = flatten(
        title,
        section1, rect_els, rect_label, circle_els, circle_label, tri_els, tri_label,
        section2, curve_els, curve_label,
        section3, star_els, star_label,
    )
    save_excalidraw("examples/demo-svg.excalidraw", elements)


# ---------------------------------------------------------------------------
# 5. Icon Library Demo
# ---------------------------------------------------------------------------
def demo_icon_library():
    """Icon library pipeline: SVG → Convert → Save → Search → Load."""
    title = text_standalone(400, 30, "Icon Library & Search", fs=26, color="#1e1e1e")

    # --- Section 1: Save workflow ---
    section1 = text_standalone(130, 80, "save_icon() — persistent storage", fs=16, color="#868e96")

    f1 = frame(20, 110, 460, 160, "Save Workflow", stroke="#1971c2")
    f1_mw = 420
    steps_save = [
        text_standalone(40, 145, "1. Generate or convert icon elements", fs=13, color="#1971c2", text_align="left", max_width=f1_mw),
        text_standalone(40, 170, "2. save_icon('name', elements, description='...')", fs=13, color="#1971c2", text_align="left", max_width=f1_mw),
        text_standalone(40, 195, "3. Stored at ~/.excalidraw-gen/icons/", fs=13, color="#1971c2", text_align="left", max_width=f1_mw),
        text_standalone(40, 220, "4. index.json holds metadata + embeddings", fs=13, color="#1971c2", text_align="left", max_width=f1_mw),
        text_standalone(40, 245, "5. Optional: OpenAI embeddings for semantic search", fs=13, color="#868e96", text_align="left", max_width=f1_mw),
    ]

    # --- Section 2: Search workflow ---
    section2 = text_standalone(620, 80, "find_icons() — vector search", fs=16, color="#868e96")

    f2 = frame(500, 110, 460, 160, "Search Workflow", stroke="#2f9e44")
    f2_mw = 420
    steps_search = [
        text_standalone(520, 145, "1. find_icons('database storage')", fs=13, color="#2f9e44", text_align="left", max_width=f2_mw),
        text_standalone(520, 170, "2. TF-IDF: tokenize → build vectors → cosine sim", fs=13, color="#2f9e44", text_align="left", max_width=f2_mw),
        text_standalone(520, 195, "3. Returns ranked results with scores", fs=13, color="#2f9e44", text_align="left", max_width=f2_mw),
        text_standalone(520, 220, "4. load_icon(name, x, y) to place in diagram", fs=13, color="#2f9e44", text_align="left", max_width=f2_mw),
        text_standalone(520, 245, "5. Zero-dependency — works offline", fs=13, color="#868e96", text_align="left", max_width=f2_mw),
    ]

    # --- Section 3: End-to-end pipeline ---
    section3 = text_standalone(330, 310, "End-to-end workflow", fs=16, color="#868e96")

    step_a = labeled_rect(30, 340, 130, 50, "SVG File", fill="#a5d8ff", stroke="#1971c2")
    step_b = labeled_rect(200, 340, 130, 50, "Convert", fill="#b2f2bb", stroke="#2f9e44")
    step_c = labeled_rect(370, 340, 130, 50, "Save to\nLibrary", fill="#ffd8a8", stroke="#e8590c")
    step_d = labeled_rect(540, 340, 130, 50, "Search", fill="#fcc2d7", stroke="#c2255c")
    step_e = labeled_rect(710, 340, 130, 50, "Load &\nPlace", fill="#d0bfff", stroke="#7048e8")

    a1 = arrow(160, 365, 40, 0, stroke="#495057")
    a2 = arrow(330, 365, 40, 0, stroke="#495057")
    a3 = arrow(500, 365, 40, 0, stroke="#495057")
    a4 = arrow(670, 365, 40, 0, stroke="#495057")

    code_labels = [
        text_standalone(95, 405, "svg_to_elements()", fs=10, color="#868e96"),
        text_standalone(265, 405, "save_icon()", fs=10, color="#868e96"),
        text_standalone(435, 405, "find_icons()", fs=10, color="#868e96"),
        text_standalone(605, 405, "load_icon()", fs=10, color="#868e96"),
        text_standalone(775, 405, "Elements!", fs=10, color="#868e96"),
    ]

    elements = flatten(
        title,
        section1, f1, steps_save,
        section2, f2, steps_search,
        section3,
        step_a, step_b, step_c, step_d, step_e,
        a1, a2, a3, a4,
        code_labels,
    )
    save_excalidraw("examples/demo-icon-library.excalidraw", elements)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    demo_charts()
    demo_flowchart()
    demo_icons()
    demo_svg()
    demo_icon_library()
    print("\nAll 5 feature demos generated!")
