<script setup>
	import { computed } from 'vue';

	const props = defineProps({
		label: { type: String, required: true },
		type: { type: String, required: true },
		iconName: { type: String, default: '' },
		isDisabled: { type: Boolean, default: false },
	});

	const TheButtonModifier = computed(() => {
		switch (props.type) {
			case 'submit':
				return 'the-button--submit';
			case 'cancel':
				return 'the-button--cancel';
			case 'hollow':
				return 'the-button--hollow';
		}
	});
</script>

<template>
	<button
		class="the-button"
		:class="[TheButtonModifier]"
		:disabled="isDisabled"
	>
		<TheIcon v-if="iconName" :name="iconName" />
		<h4 class="the-button__label">{{ label }}</h4>
	</button>
</template>

<style lang="scss" scoped>
	.the-button {
		background-color: transparent;
		width: 100%;
		height: space(24);
		border-radius: space(6);
		user-select: none;
		box-sizing: border-box;
		transition: all 0.4s ease;
		cursor: pointer;
		@include flexbox(row, center, center, space(2), nowrap);

		&:disabled {
			background-color: var(--bg-600);
			opacity: 0.5;
			cursor: not-allowed;
		}

		&--submit {
			background-color: var(--primary-300);
			border: none;
			color: var(--text-900);
		}

		&--submit:hover {
			background-color: var(--primary-500);
		}

		&--cancel {
			background-color: var(--primary-800);
			border: space(1) solid var(--primary-100);
			color: var(--title-100);
		}

		&--cancel:hover {
			background-color: var(--primary-600);
		}

		&--hollow {
			border: space(1) solid var(--text-900);
			color: var(--text-900);
		}

		&--hollow:hover {
			background-color: var(--text-900);
			color: var(--bg-900);
		}

		&__label {
			@include lineClamp(1);
		}
	}
</style>
