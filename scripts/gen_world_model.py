"""Generate: 世界模型物理表征 Architecture Diagram (1150x580, academic style).

Key fix: uses labeled_rect (containerId binding) for ALL text inside boxes,
so Excalidraw auto-centers text at render time instead of relying on
CJK width estimation.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.engine import (
    rect, labeled_rect, text_standalone, arrow, line, frame, save, uid, sd, ts
)

elements = []

# ── Color constants ──
CORE_F, CORE_S = "#a5d8ff", "#2B5B84"
PROBE_F, PROBE_S = "#b2f2bb", "#2f9e44"
LOSS_F, LOSS_S = "#ffc9c9", "#e03131"
EXT_F, EXT_S = "#99e9f2", "#1971c2"
FUT_F, FUT_S = "#ffd8a8", "#E67E22"
AUX_F, AUX_S = "#f8f9fa", "#6c757d"
TXT = "#1e1e1e"

# Common params
R = 0       # roughness: precise
FF = 2      # font family: Helvetica (sans-serif)

# ══════════════════════════════════════════════════════════════
# 3.1 Top-level Pipeline (y=50)
# ══════════════════════════════════════════════════════════════

# 观测输入框
elements += labeled_rect(30, 50, 100, 55, "观测 o_t",
    fill=AUX_F, stroke=AUX_S, sw=1.5, fs=13,
    label_color=TXT, font_family=FF, roughness=R)

# Arrow: 观测 → RSSM
elements.append(arrow(130, 78, dx=40, dy=0, stroke=CORE_S, sw=2, roughness=R))

# RSSM 编码器
elements += labeled_rect(170, 50, 160, 55, "RSSM 编码器\nh_t, z_t",
    fill=CORE_F, stroke=CORE_S, sw=2, fs=12,
    label_color=TXT, font_family=FF, roughness=R)

# Arrow: RSSM → 动态模型
elements.append(arrow(330, 78, dx=40, dy=0, stroke=CORE_S, sw=2, roughness=R))

# 动态模型
elements += labeled_rect(370, 50, 180, 55, "动态模型\nRSSM posterior",
    fill=CORE_F, stroke=CORE_S, sw=2, fs=12,
    label_color=TXT, font_family=FF, roughness=R)

# imagination 标注 (standalone, outside box)
elements.append(text_standalone(460, 28, "imagination 轨迹",
    fs=11, color=CORE_S, font_family=FF, roughness=R))

# imagination 虚线长箭头 (below 动态模型)
elements.append(line(370, 110, dx=250, dy=0,
    stroke=CORE_S, sw=1, roughness=R, stroke_style="dashed"))

# 向右出箭头 (动态模型 → Goal接口方向)
elements.append(arrow(550, 78, dx=120, dy=0, stroke=CORE_S, sw=1.5, roughness=R))

# ══════════════════════════════════════════════════════════════
# 3.2 Probe Heads (y=140)
# ══════════════════════════════════════════════════════════════

# 区域标题 (standalone)
elements.append(text_standalone(250, 130, "Physics Probe Heads (轻量线性层)",
    fs=12, color=CORE_S, font_family=FF, roughness=R))

# Arrow: 动态模型底部 → 探针区
elements.append(arrow(460, 105, dx=0, dy=35, stroke=CORE_S, sw=1.5, roughness=R))

# 四个探针头
probes = [
    (50,  "能量 E"),
    (168, "动量 p"),
    (286, "接触力 F"),
    (404, "速度 v"),
]
for px, plabel in probes:
    elements += labeled_rect(px, 140, 110, 48, plabel,
        fill=PROBE_F, stroke=PROBE_S, sw=2, fs=13,
        label_color=TXT, font_family=FF, roughness=R)

# 四个探针头各自向下红色箭头
for px in [50, 168, 286, 404]:
    elements.append(arrow(px + 55, 188, dx=0, dy=35, stroke=LOSS_S, sw=1.5, roughness=R))

# ══════════════════════════════════════════════════════════════
# 3.3 Physics Loss (y=220)
# ══════════════════════════════════════════════════════════════

elements += labeled_rect(80, 220, 380, 50,
    "物理约束损失\nL_phys = ||E_probe − E_GT||² + ||p_probe − p_GT||²",
    fill=LOSS_F, stroke=LOSS_S, sw=2, fs=11,
    label_color=TXT, font_family=FF, roughness=R)

# ══════════════════════════════════════════════════════════════
# 3.4 Gradient feedback (dashed, bent arrow)
# ══════════════════════════════════════════════════════════════

# Horizontal segment: 损失框右侧 → 右
elements.append(arrow(460, 245, dx=100, dy=0,
    stroke=LOSS_S, sw=1.5, roughness=R, stroke_style="dashed"))
# Vertical segment: 向上回到编码器
elements.append(arrow(560, 245, dx=0, dy=-170,
    stroke=LOSS_S, sw=1.5, roughness=R, stroke_style="dashed"))

# 标注文字 (standalone)
elements.append(text_standalone(600, 140, "梯度反传 →\n迫使 latent 编码物理结构",
    fs=11, color=LOSS_S, font_family=FF, roughness=R, text_align="left"))

# ══════════════════════════════════════════════════════════════
# 3.5 接触事件分段验证器
# ══════════════════════════════════════════════════════════════

elements += labeled_rect(540, 140, 220, 80,
    "接触事件分段验证器\n(VeriPhys 模块)\n5 regime: free-flight / contact\n/ rolling / sliding / resting",
    fill=AUX_F, stroke=AUX_S, sw=1.5, fs=10,
    label_color=TXT, font_family=FF, roughness=R)

# Arrow: 动态模型右侧 → 验证器
elements.append(arrow(550, 78, dx=0, dy=100, stroke=AUX_S, sw=1, roughness=R))

# ══════════════════════════════════════════════════════════════
# 3.6 训练/推理说明
# ══════════════════════════════════════════════════════════════

elements.append(text_standalone(570, 20, "训练时: MuJoCo ground-truth\n推理时: 仅探针，无仿真器",
    fs=11, color=CORE_S, font_family=FF, roughness=R, text_align="left"))

# ══════════════════════════════════════════════════════════════
# 4. Middle connection (x ~810)
# ══════════════════════════════════════════════════════════════

# 粗黑色水平箭头 (imagination → Goal)
elements.append(arrow(670, 78, dx=190, dy=0, stroke=TXT, sw=2.5, roughness=R))

# 标注文字 (standalone)
elements.append(text_standalone(765, 60, "物理一致的\nlatent dynamics",
    fs=11, color=TXT, font_family=FF, roughness=R))

# ══════════════════════════════════════════════════════════════
# 5.1 右侧扩展区 frame
# ══════════════════════════════════════════════════════════════

elements.append(frame(840, 50, 270, 200, name="扩展：结构化 Goal 接口", stroke=EXT_S, sw=2))

# Goal Tokens
elements += labeled_rect(860, 80, 230, 55, "Goal Tokens\n{action, direction, speed, contact}",
    fill=EXT_F, stroke=EXT_S, sw=2, fs=11,
    label_color=TXT, font_family=FF, roughness=R)

# Arrow down
elements.append(arrow(975, 135, dx=0, dy=20, stroke=EXT_S, sw=2, roughness=R))

# Goal-Conditioned Policy
elements += labeled_rect(860, 155, 230, 55, "Goal-Conditioned Policy\n(在物理对齐世界中)",
    fill=EXT_F, stroke=EXT_S, sw=2, fs=11,
    label_color=TXT, font_family=FF, roughness=R)

# 说明文字 (standalone)
elements.append(text_standalone(1100, 168, "有限词表 → 歧义为零\nEvaluation 可控可复现",
    fs=10, color=TXT, font_family=FF, roughness=R, text_align="left"))

# ══════════════════════════════════════════════════════════════
# 5.2 右侧未来区 frame (dashed border)
# ══════════════════════════════════════════════════════════════

# Dashed frame (manual, since frame() doesn't support stroke_style)
fid = uid()
elements.append({
    "id": fid, "type": "frame",
    "x": 840, "y": 270, "width": 270, "height": 240,
    "angle": 0, "strokeColor": FUT_S, "backgroundColor": "transparent",
    "fillStyle": "solid", "strokeWidth": 2, "strokeStyle": "dashed",
    "roughness": 0, "opacity": 100, "groupIds": [],
    "roundness": None, "seed": sd(), "version": 1,
    "versionNonce": sd(), "isDeleted": False, "boundElements": [],
    "updated": ts(), "link": None, "locked": False,
    "name": "未来方向：LLM 语义规划器"
})

# proof-of-concept 标注 (standalone)
elements.append(text_standalone(870, 290, "proof-of-concept，非论文主贡献",
    fs=9, color=FUT_S, font_family=FF, roughness=R, text_align="left"))

# LLM 语义理解
elements += labeled_rect(860, 310, 105, 55, "LLM\n语义理解",
    fill=FUT_F, stroke=FUT_S, sw=2, fs=12,
    label_color=TXT, font_family=FF, roughness=R)

# 翻译框
elements += labeled_rect(985, 310, 105, 55, "翻译\nNL→Goal",
    fill=FUT_F, stroke=FUT_S, sw=2, fs=12,
    label_color=TXT, font_family=FF, roughness=R)

# 向下箭头
elements.append(arrow(912, 365, dx=0, dy=15, stroke=FUT_S, sw=2, roughness=R))
elements.append(arrow(1037, 365, dx=0, dy=15, stroke=FUT_S, sw=1.5, roughness=R))

# 物理反馈框
elements += labeled_rect(860, 380, 230, 65, "物理反馈 → LLM 策略调整\n(如：力不足，需增大力度)",
    fill=FUT_F, stroke=FUT_S, sw=2, fs=11,
    label_color=TXT, font_family=FF, roughness=R)

# LLM 内部循环虚线箭头 (物理反馈 → 翻译框)
elements.append(arrow(1090, 380, dx=0, dy=-25,
    stroke=FUT_S, sw=1, roughness=R, stroke_style="dashed"))

# ══════════════════════════════════════════════════════════════
# 5.3 扩展区 → 未来区 连接
# ══════════════════════════════════════════════════════════════

elements.append(arrow(975, 210, dx=0, dy=60, stroke=FUT_S, sw=1.5, roughness=R))
elements.append(text_standalone(940, 240, "结构化 goal 执行与验证",
    fs=10, color=TXT, font_family=FF, roughness=R, text_align="left"))

# 分隔虚线
elements.append(line(845, 262, dx=260, dy=0,
    stroke=AUX_S, sw=1, roughness=R, stroke_style="dashed"))

# ══════════════════════════════════════════════════════════════
# 6. Legend (y=520)
# ══════════════════════════════════════════════════════════════

elements.append(text_standalone(50, 520, "图例",
    fs=12, color=TXT, font_family=FF, roughness=R, text_align="left"))

legend = [
    (CORE_F,  CORE_S,  "核心组件 (RSSM + 探针)"),
    (PROBE_F, PROBE_S, "物理探针头"),
    (LOSS_F,  LOSS_S,  "物理约束损失"),
    (EXT_F,   EXT_S,   "扩展接口"),
    (FUT_F,   FUT_S,   "未来方向 (LLM)"),
]
lx = 100
for fill, stroke, label in legend:
    elements.append(rect(lx, 514, 14, 14, fill=fill, stroke=stroke, sw=1.5, roughness=R))
    elements.append(text_standalone(lx + 20, 521, label,
        fs=10, color=TXT, font_family=FF, roughness=R, text_align="left"))
    lx += 20 + len(label) * 7 + 20

# ══════════════════════════════════════════════════════════════
# Save
# ══════════════════════════════════════════════════════════════

out = "/Users/alan/Library/Mobile Documents/iCloud~md~obsidian/Documents/世界模型物理表征.excalidraw"
save(out, elements, bg="#ffffff")
print(f"Saved to: {out}")
