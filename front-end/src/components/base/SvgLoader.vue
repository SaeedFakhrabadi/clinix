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
	<div v-else class="text-red-500">Icon not found</div>
</template>
