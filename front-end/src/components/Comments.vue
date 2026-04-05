<script setup>
import { toPersianDigits } from '@/utils/toPersianDigits';
import { computed } from 'vue';

const props = defineProps({
  comments: { type: Array, required: true },
});

const filteredComments = computed(() =>
  props.comments.filter((c) => c?.comment !== '')
)
</script>

<template>
  <ul class="comments">
    <li v-for="(c, index) in filteredComments" :key="index" class="comments__comment comment">
      <div class="comment__meta">
        <p>کاربر: <span class="comment__meta-value">{{ c?.username }}</span></p>
        <p class="comment__divider">|</p>
        <p>
          امتیاز: <span class="comment__meta-value">{{ toPersianDigits(`${c?.score} از 5`) }}</span>
        </p>
      </div>
      <p class="comment__text">{{ c?.comment }}</p>
    </li>
  </ul>
</template>

<style lang="scss" scoped>
.comment {
  width: calc(100% - space(12));
  background-color: var(--bg-800);
  border-radius: space(6);
  border-bottom-right-radius: space(0);
  padding: space(6);
  @include flexbox(column, center, start, space(2), nowrap);

  &__meta {
    color: var(--text-700);
    @include flexbox(row, center, center, space(4), wrap);
  }

  &__meta-value {
    color: var(--title-500);
  }

  &__text {
    color: var(--text-900);
  }
}
</style>
