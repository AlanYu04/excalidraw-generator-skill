"""P2 Demo: Generate 3 feature-showcase .excalidraw files for v1.2 features."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.engine import (
    rect, labeled_rect, labeled_diamond, labeled_ellipse,
    arrow, line, text_standalone, group, frame, bind_arrow,
    ellipse, save_excalidraw, save_obsidian_md,
)
from core.svg_converter import svg_to_elements
from core.charts import bar_chart, horizontal_bar_chart

# Obsidian Excalidraw output directory
OBSIDIAN_DIR = os.path.expanduser(
    "~/Library/Mobile Documents/iCloud~md~obsidian/Documents/Excalidraw"
)


def flatten(*args):
    result = []
    for item in args:
        if isinstance(item, list):
            result.extend(flatten(*item))
        else:
            result.append(item)
    return result


def demo_svg_converter():
    """Showcase: SVG-to-Excalidraw conversion."""
    title = text_standalone(400, 30, "SVG-to-Excalidraw Converter", fs=28, color="#1e1e1e")

    # --- Section 1: Simple shapes from SVG ---
    section1 = text_standalone(200, 90, "SVG shapes → Excalidraw elements", fs=14, color="#868e96")

    # Rectangle from SVG
    svg_rect = '<svg viewBox="0 0 100 80"><rect x="10" y="10" width="80" height="60" fill="#a5d8ff" stroke="#1971c2"/></svg>'
    rect_els = svg_to_elements(svg_rect, x=30, y=120, scale=1.0, stroke="#1971c2")
    rect_label = text_standalone(70, 225, "SVG <rect>", fs=12, color="#868e96")

    # Circle from SVG
    svg_circle = '<svg viewBox="0 0 100 100"><circle cx="50" cy="50" r="40" fill="#b2f2bb" stroke="#2f9e44"/></svg>'
    circle_els = svg_to_elements(svg_circle, x=180, y=120, scale=1.0, stroke="#2f9e44")
    circle_label = text_standalone(220, 245, "SVG <circle>", fs=12, color="#868e96")

    # Triangle from SVG path
    svg_tri = '<svg viewBox="0 0 100 100"><path d="M50 10 L90 90 L10 90 Z" fill="#ffd8a8" stroke="#e8590c"/></svg>'
    tri_els = svg_to_elements(svg_tri, x=320, y=120, scale=1.0, stroke="#e8590c")
    tri_label = text_standalone(360, 245, "SVG <path>", fs=12, color="#868e96")

    # --- Section 2: Bezier curves ---
    section2 = text_standalone(200, 250, "Bezier curves → polyline elements", fs=14, color="#868e96")

    svg_curve = '<svg viewBox="0 0 200 100"><path d="M10 50 C 40 10 60 90 100 50 S 160 10 190 50" stroke="#7048e8" fill="none" stroke-width="3"/></svg>'
    curve_els = svg_to_elements(svg_curve, x=50, y=280, scale=1.0, stroke="#7048e8")
    curve_label = text_standalone(150, 400, "Cubic Bezier curve", fs=12, color="#868e96")

    # --- Section 3: Complex path ---
    section3 = text_standalone(430, 250, "Star from SVG path", fs=14, color="#868e96")
    svg_star = '<svg viewBox="0 0 100 100"><path d="M50 5 L61 35 L95 35 L68 57 L79 90 L50 70 L21 90 L32 57 L5 35 L39 35 Z" fill="#ffd43b" stroke="#f08c00"/></svg>'
    star_els = svg_to_elements(svg_star, x=440, y=280, scale=0.8, stroke="#f08c00")
    star_label = text_standalone(470, 380, "Complex polygon", fs=12, color="#868e96")

    elements = flatten(
        title,
        section1, rect_els, rect_label, circle_els, circle_label, tri_els, tri_label,
        section2, curve_els, curve_label,
        section3, star_els, star_label,
    )
    save_excalidraw("examples/svg-converter.excalidraw", elements)
    save_obsidian_md(os.path.join(OBSIDIAN_DIR, "P2-SVG转换器.excalidraw.md"), elements)


def demo_bar_charts():
    """Showcase: Hand-drawn bar charts."""
    title = text_standalone(400, 30, "Hand-drawn Bar Charts", fs=28, color="#1e1e1e")

    # --- Section 1: Vertical bar chart ---
    section1 = text_standalone(130, 80, "bar_chart() — vertical", fs=16, color="#868e96")

    chart1 = bar_chart(
        x=30, y=110,
        data={"React": 85, "Vue": 72, "Angular": 58, "Svelte": 45, "Solid": 38},
        title="Framework Popularity",
        bar_color="#a5d8ff",
        bar_colors={"React": "#a5d8ff", "Vue": "#b2f2bb", "Angular": "#ffd8a8",
                     "Svelte": "#fcc2d7", "Solid": "#d0bfff"},
        bar_width=50,
        max_height=180,
        gap=20,
        fs=13,
        show_values=True,
        show_grid=True,
        roughness=1,
    )

    # --- Section 2: Horizontal bar chart ---
    section2 = text_standalone(530, 80, "horizontal_bar_chart()", fs=16, color="#868e96")

    chart2 = horizontal_bar_chart(
        x=520, y=120,
        data={"Python": 90, "JavaScript": 85, "TypeScript": 75, "Rust": 60, "Go": 55},
        title="Language Usage",
        bar_color="#a5d8ff",
        bar_colors={"Python": "#ffd43b", "JavaScript": "#fcc2d7", "TypeScript": "#74c0fc",
                     "Rust": "#b2f2bb", "Go": "#d0bfff"},
        bar_height=35,
        max_width=220,
        gap=12,
        fs=13,
        roughness=1,
    )

    # --- Section 3: CJK chart ---
    section3 = text_standalone(130, 430, "CJK text support in charts", fs=16, color="#868e96")

    chart3 = bar_chart(
        x=30, y=460,
        data={"数据库": 80, "服务器": 65, "缓存": 90, "消息队列": 55},
        title="系统组件使用率",
        bar_color="#b2f2bb",
        bar_width=60,
        max_height=150,
        gap=25,
        fs=14,
        font_family=3,
        show_values=True,
        roughness=1,
    )

    elements = flatten(
        title,
        section1, chart1,
        section2, chart2,
        section3, chart3,
    )
    save_excalidraw("examples/bar-charts.excalidraw", elements)
    save_obsidian_md(os.path.join(OBSIDIAN_DIR, "P2-手绘柱状图.excalidraw.md"), elements)


def demo_icon_library():
    """Showcase: Icon library + search workflow."""
    title = text_standalone(400, 30, "Icon Library & Search", fs=28, color="#1e1e1e")

    # --- Section 1: Save workflow ---
    section1 = text_standalone(130, 80, "save_icon() — persistent storage", fs=16, color="#868e96")

    f1 = frame(20, 110, 380, 160, "Save Workflow", stroke="#1971c2")
    steps = [
        text_standalone(210, 145, "1. Generate or convert icon elements", fs=13, color="#1971c2"),
        text_standalone(210, 170, "2. save_icon('name', elements, description='...')", fs=13, color="#1971c2"),
        text_standalone(210, 195, "3. Stored at ~/.excalidraw-gen/icons/", fs=13, color="#1971c2"),
        text_standalone(210, 220, "4. index.json holds metadata + embeddings", fs=13, color="#1971c2"),
        text_standalone(210, 245, "5. Optional: OpenAI embeddings for semantic search", fs=13, color="#868e96"),
    ]

    # --- Section 2: Search workflow ---
    section2 = text_standalone(530, 80, "find_icons() — vector search", fs=16, color="#868e96")

    f2 = frame(420, 110, 380, 160, "Search Workflow", stroke="#2f9e44")
    search_steps = [
        text_standalone(610, 145, "1. find_icons('database storage')", fs=13, color="#2f9e44"),
        text_standalone(610, 170, "2. TF-IDF: tokenize → build vectors → cosine sim", fs=13, color="#2f9e44"),
        text_standalone(610, 195, "3. Returns ranked results with scores", fs=13, color="#2f9e44"),
        text_standalone(610, 220, "4. load_icon(name, x, y) to place in diagram", fs=13, color="#2f9e44"),
        text_standalone(610, 245, "5. Zero-dependency — works offline", fs=13, color="#868e96"),
    ]

    # --- Section 3: Demo data flow ---
    section3 = text_standalone(330, 310, "End-to-end workflow", fs=16, color="#868e96")

    # SVG → Convert → Save → Search → Load pipeline
    step_a = labeled_rect(30, 340, 130, 50, "SVG File", fill="#a5d8ff", stroke="#1971c2")
    step_b = labeled_rect(200, 340, 130, 50, "Convert", fill="#b2f2bb", stroke="#2f9e44")
    step_c = labeled_rect(370, 340, 130, 50, "Save to\nLibrary", fill="#ffd8a8", stroke="#e8590c")
    step_d = labeled_rect(540, 340, 130, 50, "Search", fill="#fcc2d7", stroke="#c2255c")
    step_e = labeled_rect(710, 340, 130, 50, "Load &\nPlace", fill="#d0bfff", stroke="#7048e8")

    a1 = arrow(160, 365, 40, 0, stroke="#495057")
    a2 = arrow(330, 365, 40, 0, stroke="#495057")
    a3 = arrow(500, 365, 40, 0, stroke="#495057")
    a4 = arrow(670, 365, 40, 0, stroke="#495057")

    # Code snippet labels
    code_labels = [
        text_standalone(95, 405, "svg_to_elements()", fs=10, color="#868e96"),
        text_standalone(265, 405, "save_icon()", fs=10, color="#868e96"),
        text_standalone(435, 405, "find_icons()", fs=10, color="#868e96"),
        text_standalone(605, 405, "load_icon()", fs=10, color="#868e96"),
        text_standalone(775, 405, "Elements!", fs=10, color="#868e96"),
    ]

    elements = flatten(
        title,
        section1, f1, steps,
        section2, f2, search_steps,
        section3,
        step_a, step_b, step_c, step_d, step_e,
        a1, a2, a3, a4,
        code_labels,
    )
    save_excalidraw("examples/icon-library.excalidraw", elements)
    save_obsidian_md(os.path.join(OBSIDIAN_DIR, "P2-图标库与搜索.excalidraw.md"), elements)


if __name__ == "__main__":
    demo_svg_converter()
    demo_bar_charts()
    demo_icon_library()
    print("\nAll 3 P2 feature-showcase demos generated!")
