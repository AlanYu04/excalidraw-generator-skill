<template>
  <div class="style-switcher-section">
    <div class="style-buttons">
      <button
        v-for="style in styles"
        :key="style.id"
        :class="['style-btn', { active: activeStyle === style.id }]"
        @click="switchStyle(style.id)"
      >
        {{ style.label }}
      </button>
    </div>

    <div class="style-viewer">
      <Transition name="fade" mode="out-in">
        <ExcalidrawViewer
          v-if="currentSrc"
          :key="activeStyle"
          :src="currentSrc"
          :height="viewerHeight"
          view-only
        />
      </Transition>
    </div>

    <Transition name="fade" mode="out-in">
      <div :key="activeStyle" class="style-card">
        <h4>{{ currentStyleInfo.font }} &middot; Roughness {{ currentStyleInfo.roughness }}</h4>
        <p>{{ currentStyleInfo.description }}</p>
        <div class="style-meta">
          <span class="meta-tag">Fill: {{ currentStyleInfo.fill }}</span>
          <span class="meta-tag">{{ currentStyleInfo.useCase }}</span>
        </div>
      </div>
    </Transition>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import ExcalidrawViewer from './ExcalidrawViewer.vue'

interface StyleInfo {
  id: string
  label: string
  src: string
  font: string
  roughness: number
  fill: string
  description: string
  useCase: string
}

const styles: StyleInfo[] = [
  {
    id: 'vivid',
    label: 'Vivid',
    src: '/demos/demo-vivid.excalidraw',
    font: 'Cascadia',
    roughness: 1,
    fill: 'Solid',
    description: 'Rich, colorful, detailed diagrams for conference presentations',
    useCase: 'Conference presentations',
  },
  {
    id: 'clean',
    label: 'Clean',
    src: '/demos/demo-clean.excalidraw',
    font: 'Helvetica',
    roughness: 0,
    fill: 'Solid',
    description: 'Minimal, B&W, precise diagrams for journal papers',
    useCase: 'Journal papers',
  },
  {
    id: 'sketch',
    label: 'Sketch',
    src: '/demos/demo-sketch.excalidraw',
    font: 'Virgil',
    roughness: 2,
    fill: 'Hachure',
    description: 'Hand-drawn, casual diagrams for presentations',
    useCase: 'Presentations',
  },
]

const activeStyle = ref<string>('vivid')
const viewerHeight = ref<string>('460px')

const currentSrc = computed(() => {
  return styles.find((s) => s.id === activeStyle.value)?.src || ''
})

const currentStyleInfo = computed(() => {
  return (
    styles.find((s) => s.id === activeStyle.value) || styles[0]
  )
})

function switchStyle(id: string) {
  if (id !== activeStyle.value) {
    activeStyle.value = id
  }
}
</script>

<style scoped>
.style-switcher-section {
  margin: 2rem 0;
}

.style-buttons {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.style-btn {
  padding: 0.5rem 1.5rem;
  border-radius: 20px;
  border: 2px solid var(--vp-c-divider);
  background: var(--vp-c-bg);
  color: var(--vp-c-text-1);
  cursor: pointer;
  font-size: 0.9rem;
  transition: all 0.2s;
}

.style-btn:hover {
  border-color: var(--vp-c-brand-1);
}

.style-btn.active {
  border-color: var(--vp-c-brand-1);
  background: var(--vp-c-brand-soft);
  color: var(--vp-c-brand-1);
}

.style-viewer {
  margin-bottom: 1rem;
}

.style-card {
  padding: 1.25rem;
  border-radius: 8px;
  border: 1px solid var(--vp-c-divider);
  background: var(--vp-c-bg-soft);
}

.style-card h4 {
  margin: 0 0 0.5rem;
  color: var(--vp-c-brand-1);
  font-size: 1rem;
}

.style-card p {
  margin: 0 0 0.75rem;
  color: var(--vp-c-text-2);
  font-size: 0.9rem;
  line-height: 1.5;
}

.style-meta {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.meta-tag {
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  background: var(--vp-c-bg);
  border: 1px solid var(--vp-c-divider);
  font-size: 0.8rem;
  color: var(--vp-c-text-2);
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.25s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
