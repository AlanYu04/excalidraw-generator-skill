<template>
  <div
    ref="containerRef"
    class="excalidraw-container"
    :style="{ height: height }"
  >
    <div v-if="loading" class="excalidraw-loading">
      <span class="loading-spinner" />
      <span>Loading diagram...</span>
    </div>
    <div v-if="error" class="excalidraw-error">
      <p>Failed to load diagram</p>
      <p class="error-detail">{{ error }}</p>
    </div>
    <div ref="mountRef" :style="{ height: '100%', width: '100%' }" />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, watch } from 'vue'

const props = withDefaults(
  defineProps<{
    src: string
    viewOnly?: boolean
    height?: string
  }>(),
  {
    viewOnly: true,
    height: '500px',
  }
)

const containerRef = ref<HTMLElement | null>(null)
const mountRef = ref<HTMLElement | null>(null)
const loading = ref(false)
const error = ref<string | null>(null)

let root: any = null
let observer: IntersectionObserver | null = null
let mounted = false

async function mountExcalidraw() {
  if (mounted || !mountRef.value) return
  mounted = true
  loading.value = true
  error.value = null

  try {
    const [{ default: ExcalidrawWrapper }, reactModule, { createRoot }] =
      await Promise.all([
        import('./ExcalidrawWrapper.tsx'),
        import('react'),
        import('react-dom/client'),
      ])

    const response = await fetch(props.src)
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`)
    }
    const data = await response.json()

    const elements = data.elements || []
    const appState = data.appState || {}

    if (mountRef.value) {
      root = createRoot(mountRef.value)
      root.render(
        reactModule.createElement(ExcalidrawWrapper, {
          initialData: { elements, appState },
          viewModeEnabled: props.viewOnly,
        })
      )
    }
  } catch (err: unknown) {
    const message = err instanceof Error ? err.message : 'Unknown error'
    error.value = message
  } finally {
    loading.value = false
  }
}

function unmountExcalidraw() {
  if (root) {
    root.unmount()
    root = null
  }
  mounted = false
}

onMounted(() => {
  if (!containerRef.value) return

  observer = new IntersectionObserver(
    (entries) => {
      for (const entry of entries) {
        if (entry.isIntersecting && !mounted) {
          mountExcalidraw()
          observer?.disconnect()
        }
      }
    },
    { rootMargin: '200px' }
  )

  observer.observe(containerRef.value)
})

onUnmounted(() => {
  observer?.disconnect()
  unmountExcalidraw()
})

watch(
  () => props.src,
  () => {
    unmountExcalidraw()
    if (containerRef.value) {
      const rect = containerRef.value.getBoundingClientRect()
      if (rect.top < window.innerHeight && rect.bottom > 0) {
        mountExcalidraw()
      } else {
        observer?.disconnect()
        observer = new IntersectionObserver(
          (entries) => {
            for (const entry of entries) {
              if (entry.isIntersecting && !mounted) {
                mountExcalidraw()
                observer?.disconnect()
              }
            }
          },
          { rootMargin: '200px' }
        )
        observer.observe(containerRef.value)
      }
    }
  }
)
</script>

<style scoped>
.excalidraw-container {
  border: 1px solid var(--vp-c-divider);
  border-radius: 8px;
  overflow: hidden;
  position: relative;
}

.excalidraw-loading {
  position: absolute;
  inset: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 0.75rem;
  color: var(--vp-c-text-2);
  z-index: 1;
}

.loading-spinner {
  width: 32px;
  height: 32px;
  border: 3px solid var(--vp-c-divider);
  border-top-color: var(--vp-c-brand-1);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.excalidraw-error {
  position: absolute;
  inset: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: var(--vp-c-text-2);
}

.error-detail {
  font-size: 0.85rem;
  opacity: 0.7;
}
</style>
