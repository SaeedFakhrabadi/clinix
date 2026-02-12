<script setup>
	import { computed } from 'vue';

	const props = defineProps({
		label: {
			type: String,
			required: true,
		},
		type: {
			type: String,
			required: true,
		},
		iconName: {
			type: String,
			default: '',
		},
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
	<button class="the-button" :class="[TheButtonModifier]">
		<SvgLoader v-if="iconName" :name="iconName" />
		<h5>{{ label }}</h5>
	</button>
</template>

<style lang="scss" scoped>
	.the-button {
		background-color: transparent;
		width: 100%;
		height: space(20);
		border-radius: space(4);
		user-select: none;
		transition: all 0.4s ease;
		cursor: pointer;
		@include flexbox(row, center, center, space(2), nowrap);

		&--submit {
			background-color: var(--primary-300);
			border: none;
			color: var(--text-900);
		}

		&--submit:hover {
			background-color: var(--primary-500);
		}

		&--cancel {
			border: space(1) solid var(--primary-100);
			color: var(--primary-100);
		}

		&--cancel:hover {
			background-color: var(--primary-700);
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
