<script setup>
const props = defineProps({
  label: { type: String, required: true },
  hasDivider: { type: Boolean, default: false }
});
</script>

<template>
  <div class="the-title">
    <h2 class="the-title__label" :class="{ 'the-title__label--has-divider': hasDivider }">{{ label }}</h2>
  </div>
</template>

<style lang="scss" scoped>
.the-title {
  width: 100%;

  &__label {
    padding-right: space(3);
    color: var(--text-900);

    &--has-divider {
      border-top: space(0.5) solid var(--text-700);
      padding-top: space(10);
    }
  }
}
</style>
