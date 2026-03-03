<script setup>
	import { computed, ref } from 'vue';
	import { toPersianDigits } from '@/utils/toPersianDigits';

	const props = defineProps({
		label: { type: String, required: true },
		isMandatory: { type: Boolean, default: false },
		iconName: { type: String, required: true },
		placeholder: { type: String, default: '' },
		isDisabled: { type: Boolean, default: false },
		type: { type: String, default: 'text' },
		digitsOnly: { type: Boolean, default: false },
		errorMessage: { type: String, default: '' },
	});

	const emit = defineEmits(['blur', 'focus']);

	const inputValue = defineModel();
	const isPasswordVisible = ref(false);

	const isPassword = computed(() => props.type === 'password');
	const eyeIconName = computed(() =>
		isPasswordVisible.value ? 'eye-slash' : 'eye',
	);
	const inputType = computed(() =>
		isPassword.value && isPasswordVisible.value ? 'text' : props.type,
	);

	const togglePasswordVisibility = () =>
		(isPasswordVisible.value = !isPasswordVisible.value);

	const handleInput = (event) => {
		if (props.digitsOnly) {
			let val = event?.target?.value ?? '';
			val = val.replace(/[^\d]/g, '');
			inputValue.value = val;
		}
	};
</script>

<template>
	<div class="the-input">
		<div class="the-input__container">
			<label class="the-input__label label-box">
				<h5 class="label-box__text">{{ label }}</h5>
				<h5 v-if="isMandatory" class="label-box__mandatory">*</h5>
			</label>
			<div
				class="the-input__input-box input-box"
				:class="{ 'input-box--error': errorMessage }"
			>
				<SvgLoader class="input-box__icon" v-if="iconName" :name="iconName" />
				<textarea
					v-if="type === 'textarea'"
					class="input-box__input"
					style="height: 80px; resize: vertical"
					v-model="inputValue"
					:placeholder="placeholder"
					:disabled="isDisabled"
					@input="handleInput"
					@blur="emit('blur', inputValue)"
					@focus="emit('focus', inputValue)"
				/>
				<input
					v-else
					class="input-box__input"
					v-model="inputValue"
					:placeholder="placeholder"
					:disabled="isDisabled"
					:type="inputType"
					@input="handleInput"
					@blur="emit('blur', inputValue)"
					@focus="emit('focus', inputValue)"
				/>
				<SvgLoader
					v-if="isPassword"
					class="input-box__eye-icon"
					:name="eyeIconName"
					@click="togglePasswordVisibility"
				/>
			</div>
			<h6 v-if="errorMessage" class="the-input__error-message error-message">
				{{ toPersianDigits(errorMessage) }}
			</h6>
			<div v-else class="the-input__error-space"></div>
		</div>
	</div>
</template>

<style lang="scss" scoped>
	.the-input {
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

		.input-box {
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

			&__input {
				height: space(16);
				background-color: transparent;
				color: var(--text-900);
				padding: space(2) space(18) space(2) space(6);
				border-radius: space(6);
				border: none;
				outline: none;
				flex: 1;

				&::placeholder {
					color: var(--text-500);
				}

				&:disabled {
					background-color: var(--bg-700);
					opacity: 0.5;
					cursor: not-allowed;
					z-index: 2;
				}
			}

			&__eye-icon {
				position: absolute;
				left: space(0);
				background-color: var(--bg-900);
				color: var(--text-700);
				border-top-left-radius: space(6);
				border-bottom-left-radius: space(6);
				padding: space(4.5);
				padding-right: space(2.5);
				cursor: pointer;
				z-index: 1;
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
