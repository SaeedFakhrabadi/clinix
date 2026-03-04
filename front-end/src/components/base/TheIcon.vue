<script setup>
	import { computed } from 'vue';

	const props = defineProps({
		name: { type: String, required: true },
		class: { type: String, default: '' },
	});

	const icons = import.meta.glob('@/assets/icons/*.svg', { eager: true });

	const iconComponent = computed(() => {
		const path = `/src/assets/icons/${props.name}.svg`;
		return icons[path]?.default || null;
	});
</script>

<template>
	<component v-if="iconComponent" :is="iconComponent" :class="props.class" />
	<div class="icon-not-found" v-else>
		<h6>Icon not found</h6>
	</div>
</template>

<style lang="scss" scoped>
	.icon-not-found {
		color: var(--danger-100);
	}
</style>
