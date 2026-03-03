<script setup>
	import { computed, onMounted } from 'vue';
	import { toPersianDigits } from '@/utils/toPersianDigits';

	const props = defineProps({
		label: { type: String, required: true },
		isMandatory: { type: Boolean, default: false },
		iconName: { type: String, default: '' },
		options: { type: Array, required: true },
		errorMessage: { type: String, default: '' },
		isDisabled: { type: Boolean, default: false },
	});

	const emit = defineEmits(['blur', 'focus', 'change']);

	const selectedValue = defineModel();

	const mappedOptions = () => {
		return props.options.map((opt) => ({
			value: opt.value,
			label: opt.label,
		}));
	};

	const firstOptionValue = computed(() => mappedOptions()[0]?.value);

	const handleChange = (event) => {
		selectedValue.value = event?.target?.value;
		emit('change', selectedValue.value);
	};

	const handleBlur = () => emit('blur', selectedValue.value);
	const handleFocus = () => emit('focus', selectedValue.value);

	onMounted(() => {
		selectedValue.value = firstOptionValue.value;
	});
</script>

<template>
	<div class="the-select">
		<div class="the-select__container">
			<label class="the-select__label label-box">
				<h5 class="label-box__text">{{ label }}</h5>
				<h5 v-if="isMandatory" class="label-box__mandatory">*</h5>
			</label>
			<div
				class="the-select__select-box select-box"
				:class="{ 'input-box--error': errorMessage }"
			>
				<SvgLoader v-if="iconName" class="select-box__icon" :name="iconName" />
				<select
					class="select-box__select"
					:value="selectedValue ?? firstOptionValue"
					:disabled="isDisabled"
					:aria-invalid="!!errorMessage"
					@change="handleChange"
					@blur="handleBlur"
					@focus="handleFocus"
				>
					<option
						class="select-box__option"
						v-for="(opt, index) in mappedOptions()"
						:key="index"
						:value="opt.value"
					>
						{{ toPersianDigits(opt.label) }}
					</option>
				</select>
			</div>
			<h6 v-if="errorMessage" class="the-select__error-message error-message">
				{{ toPersianDigits(errorMessage) }}
			</h6>
			<div v-else class="the-select__error-space"></div>
		</div>
	</div>
</template>

<style lang="scss" scoped>
	.the-select {
		width: 100%;

		&__container {
			width: 100%;
			@include flexbox(column, start, right, space(0));
		}

		.label-box {
			width: 100%;
			user-select: none;
			flex: 1;
			@include flexbox(row, start, right, space(1), nowrap);

			&__text {
				color: var(--text-900);
				padding-right: space(6);
				@include lineClamp(1);
			}

			&__mandatory {
				color: var(--danger-400);
			}
		}

		.select-box {
			background-color: var(--bg-900);
			border-radius: space(6);
			position: relative;
			outline: space(0.5) solid var(--text-500);
			@include flexbox(row, center, center, space(0), nowrap);

			&:focus-within,
			&:hover {
				outline: space(1) solid var(--text-500);
			}

			&--error {
				outline: space(0.5) solid var(--danger-200);
			}

			&--error:focus-within,
			&--error:hover {
				outline: space(1) solid var(--danger-200);
			}

			&__icon {
				position: absolute;
				right: space(0);
				color: var(--primary-100);
				padding: space(4.5);
				padding-left: space(2.5);
			}

			&__select {
				height: space(20);
				cursor: pointer;
				background-color: transparent;
				color: var(--text-900);
				padding: space(2) space(18) space(2) space(6);
				border-radius: space(6);
				border: none;
				outline: none;
				flex: 1;

				&:disabled {
					background-color: var(--bg-700);
					opacity: 0.5;
					cursor: not-allowed;
					z-index: 2;
				}
			}

			&__option {
				background-color: var(--bg-900);
			}
		}

		.error-message {
			user-select: none;
			padding-right: space(6);
			line-height: space(10);
			min-height: space(10);
			color: var(--danger-400);
			@include flexbox();
			@include lineClamp(1);
		}

		&__error-space {
			min-height: space(4);
		}
	}
</style>
