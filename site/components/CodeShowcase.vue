<template>
  <div class="code-showcase">
    <div class="code-panel">
      <h4 v-if="title">{{ title }}</h4>
      <slot />
    </div>
    <div class="result-panel">
      <slot name="result" />
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  title?: string
}>()
</script>

<style scoped>
.code-showcase {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
  margin: 1.5rem 0;
}

.code-panel {
  padding: 1rem;
  border-radius: 8px;
  background: var(--vp-c-bg-soft);
  border: 1px solid var(--vp-c-divider);
  overflow-x: auto;
}

.code-panel h4 {
  margin: 0 0 0.75rem;
  font-size: 0.9rem;
  color: var(--vp-c-text-2);
}

.result-panel {
  border-radius: 8px;
  overflow: hidden;
}

@media (max-width: 768px) {
  .code-showcase {
    grid-template-columns: 1fr;
  }
}
</style>
