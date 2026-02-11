<script setup>
	import { computed, onMounted } from 'vue';
	import { toPersianDigits } from '@/utils/toPersianDigits';

	const props = defineProps({
		label: { type: String, required: true },
		isMandatory: { type: Boolean, default: false },
		iconName: { type: String, default: '' },
		options: {
			type: Array,
			required: true,
		},
		errorMessage: { type: String, default: '' },
		disabled: { type: Boolean, default: false },
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
					:disabled="disabled"
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
						{{ opt.label }}
					</option>
				</select>
			</div>
			<h6 class="the-select__error-message">
				{{ toPersianDigits(errorMessage) }}
			</h6>
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
				@include lineClamp(1);
			}

			&__mandatory {
				color: var(--danger-100);
			}
		}

		.select-box {
			background-image: linear-gradient(90deg, var(--bg-800), var(--bg-900));
			border-right: space(4) solid var(--text-100);
			border-top-left-radius: space(4);
			border-bottom-left-radius: space(4);
			transition: all 0.2s ease;
			outline: space(0.5) solid var(--text-500);
			@include flexbox(row, center, center, space(0), nowrap);

			&__icon {
				color: var(--primary-100);
				margin: space(2);
			}

			&__select {
				background-color: transparent;
				color: var(--text-900);
				margin-left: space(5);
				border: none;
				outline: none;
				width: 100%;
				height: space(20);
				cursor: pointer;

				&:disabled {
					opacity: 0.5;
					cursor: not-allowed;
				}
			}

			&:focus-within,
			&:hover {
				border-right: space(2) solid var(--text-100);
			}

			&--error {
				border-right: space(4) solid var(--danger-100);
			}

			&--error:focus-within,
			&--error:hover {
				border-right: space(2) solid var(--danger-100);
			}
		}

		&__error-message {
			user-select: none;
			line-height: space(10);
			min-height: space(10);
			color: var(--danger-600);
			@include flexbox();
			@include lineClamp(1);
		}
	}
</style>
