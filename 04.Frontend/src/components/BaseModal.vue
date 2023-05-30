<template>
  <div class="dim-layer" style="display: block">
    <div class="modal-group">
      <div class="dim-bg" @click.self="$emit('close')"></div>
      <div
        id="layer"
        :class="['modal-layer', ...classNames]"
        :style="{ ...styles }"
      >
        <button
          type="button"
          class="modal-close"
          @click="$emit('close')"
        ></button>
        <slot />
      </div>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  styles: { type: Object, required: false },
  classNames: { type: Array },
});
const emits = defineEmits(['close']);
</script>

<style scoped></style>
