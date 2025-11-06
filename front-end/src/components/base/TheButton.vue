<script setup>
	import { computed } from 'vue';

	const props = defineProps({
		label: { type: String, default: 'ثبت' },
		type: { type: String, default: 'submit' },
		width: { type: Number, default: 60 },
		// iconName: String,
	});

	const TheButtonModifier = computed(() => {
		switch (props.type) {
			case 'submit':
				return 'base-button--submit';
			case 'cancel':
				return 'base-button--cancel';
			case 'hollow':
				return 'base-button--hollow';
			case 'big':
				return 'base-button--big';
		}
	});
</script>

<template>
	<button class="base-button" :class="[TheButtonModifier]" :style="{ width: width + 'px' }">
		<h5>{{ label }}</h5>
		<!-- <SvgIcon v-if="iconName" class="base-button__icon" :name="iconName" /> -->
	</button>
</template>

<style lang="scss" scoped>
	.base-button {
		background-color: transparent;
		border-radius: space(4);
		cursor: pointer;
		height: space(18);
		@include flexbox(row, center, center);
	}

	.base-button--submit {
		background-color: var(--primary-700);
		border: none;
		color: var(--text-900);
	}

	.base-button--submit:hover {
		background-color: var(--primary-400);
	}

	.base-button--cancel {
		border: space(1) solid var(--secondary-400);
		color: var(--secondary-400);
	}

	.base-button--cancel:hover {
		background-color: var(--secondary-400);
		color: var(--text-900);
	}

	.base-button--hollow {
		border: space(1) solid var(--primary-400);
		color: var(--primary-400);
	}

	.base-button--hollow:hover {
		background-color: var(--primary-400);
		color: var(--text-900);
	}

	.base-button--big {
		background-color: var(--primary-700);
		border: none;
		color: var(--text-900);
		height: space(30);
	}

	.base-button--big:hover {
		background-color: var(--primary-900);
	}

	// .base-button__icon {
	//   color: var(--gray-900);
	//   display: flex;
	//   height: 16px;
	//   width: 16px;
	// }
</style>
