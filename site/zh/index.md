---
layout: home

hero:
  name: Excalidraw Generator
  text: 用 Python 生成精美的 Excalidraw 图表
  tagline: AI 驱动的图表生成器，直接输出 Excalidraw JSON 格式。流程图、架构图、数据图表、数学公式，一气呵成。
  actions:
    - theme: brand
      text: 快速开始
      link: /zh/guide/quick-start
    - theme: alt
      text: API 参考
      link: /zh/api/
    - theme: alt
      text: GitHub
      link: https://github.com/AlanYu04/excalidraw-generator-skill
---

<div style="text-align:center">
<div class="hero-badge">Claude Code Skill · MIT License</div>

<div class="install-cmd">claude skill add excalidraw-generator</div>
</div>


---

## 功能特性

<div class="feature-grid feature-grid-3">

<div class="feature-card">
  <img src="/images/bar-charts-demo.png" alt="图表" />
  <div class="card-body">
    <h3>多种图表类型</h3>
    <p>柱状图、折线图、饼图、水平柱状图，支持网格线、图例和中英文标签</p>
  </div>
</div>

<div class="feature-card">
  <img src="/images/icons.png" alt="图标" />
  <div class="card-body">
    <h3>39+ 内置图标</h3>
    <p>技术图标、AI 生成图标、持久化图标库，覆盖常见技术场景</p>
  </div>
</div>

<div class="feature-card">
  <img src="/images/font-comparison.png" alt="LaTeX" />
  <div class="card-body">
    <h3>LaTeX 公式渲染</h3>
    <p>matplotlib mathtext 渲染引擎，4 种字体可选，完美支持中英文</p>
  </div>
</div>

</div>

---

## 作品画廊

<div class="gallery-grid">
  <img src="/images/architecture.png" alt="架构图" />
  <img src="/images/bar-chart.png" alt="柱状图" />
  <img src="/images/bar-chart-2.png" alt="水平柱状图" />
  <img src="/images/line-chart.png" alt="折线图" />
  <img src="/images/icons.png" alt="图标集合" />
  <img src="/images/case-sensor.png" alt="传感器数据管道" />
  <img src="/images/case-decision-transformer.png" alt="Decision Transformer" />
  <img src="/images/case-openclaw.png" alt="OpenClaw 架构" />
  <img src="/images/workflow.png" alt="工作流" />
  <img src="/images/how-it-works.png" alt="原理示意" />
  <img src="/images/demo-gallery.png" alt="演示画廊" />
  <img src="/images/font-comparison.png" alt="字体对比" />
</div>

<style>
/* Force hero into single centered column */
.VPHero .container {
  flex-direction: column !important;
  align-items: center !important;
}
.VPHero .main {
  width: 100% !important;
  max-width: 100% !important;
  order: unset !important;
  display: flex !important;
  flex-direction: column !important;
  align-items: center !important;
}
.VPHero .heading {
  align-items: center !important;
}
.VPHero .name,
.VPHero .text {
  max-width: 900px !important;
  white-space: nowrap !important;
  margin: 0 auto !important;
  text-align: center !important;
}
.VPHero .tagline {
  max-width: 560px !important;
  margin: 12px auto 0 !important;
  text-align: center !important;
  font-size: 1.05rem !important;
  color: #555 !important;
  line-height: 1.75 !important;
}
.VPHero .actions {
  justify-content: center !important;
}
</style>
