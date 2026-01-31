<script setup>
	import { computed } from 'vue';

	const props = defineProps({
		label: { type: String, required: true },
		iconName: { type: String, default: '' },
		type: { type: String, required: true },
		width: { type: String, default: '100%' },
		height: { type: String, default: '40px' },
		labelColor: { type: String, default: '' },
		// labelColorHover: { type: String, default: '' },
		bgColor: { type: String, default: '' },
		// bgColorHover: { type: String, default: '' },
		// borderColor: { type: String, default: '' },
	});

	const varify = (variable) => `var(--${variable})`;

	const defaultStyles = computed(() => ({
		width: props.width,
		height: props.height,
		...(props.bgColor ? { backgroundColor: varify(props.bgColor) } : {}),
		...(props.labelColor ? { color: varify(props.labelColor) } : {}),
	}));

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
		:style="defaultStyles"
	>
		<SvgLoader v-if="iconName" :name="iconName" />
		<h5>{{ label }}</h5>
	</button>
</template>

<style lang="scss" scoped>
	.the-button {
		background-color: transparent;
		border-radius: space(4);
		user-select: none;
		transition: all 0.4s ease;
		cursor: pointer;
		@include flexbox(row, center, center, space(2), nowrap);

		&--submit {
			background-color: var(--primary-100);
			border: none;
			color: var(--text-900);
		}

		&--submit:hover {
			background-color: var(--primary-500);
		}

		&--cancel {
			border: space(1) solid var(--primary-500);
			color: var(--primary-500);
		}

		&--cancel:hover {
			background-color: var(--primary-800);
			color: var(--text-900);
		}

		&--hollow {
			border: space(1) solid var(--text-900);
			color: var(--text-900);
		}

		&--hollow:hover {
			background-color: var(--text-900);
			color: var(--text-100);
		}
	}
</style>
