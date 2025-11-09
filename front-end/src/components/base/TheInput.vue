<script setup>
	import { computed, ref, toRefs, watch } from 'vue';
	import { toPersianDigits } from '@/utils/toPersianDigits';

	const props = defineProps({
		label: {
			type: String,
			required: true,
		},
		isMandatory: {
			type: Boolean,
			default: false,
		},
		placeholder: {
			type: String,
			required: true,
		},
		type: {
			type: String,
			default: 'text',
		},
		errorMessage: {
			type: String,
			default: '',
		},
	});

	const emit = defineEmits(['blur', 'focus']);

	const inputValue = defineModel();

	const { type, label, errorMessage } = toRefs(props);

	const isPassword = computed(() => type.value === 'password');

	const eyeIconName = computed(() => (isPasswordVisible.value ? 'eye-slash' : 'eye'));

	const inputType = computed(() => (isPassword.value && isPasswordVisible.value ? 'text' : props.type));

	const isPasswordVisible = ref(false);
	const togglePasswordVisibility = () => {
		isPasswordVisible.value = !isPasswordVisible.value;
	};

	// const isDescription = computed(() => props.label === 'توضیحات');

	// const heightClass = computed(() => (isDescription.value ? 'base-input--description' : 'base-input--default'));

	watch(inputValue, (newVal) => (inputValue.value = toPersianDigits(newVal)));
</script>

<template>
	<div class="the-input">
		<div class="container">
			<!-- <textarea
      v-if="isDescription"
      class="base-input__field"
      placeholder=" "
      v-model="inputValue"
      :style="{ marginTop: '10px' }"
    ></textarea> -->
			<!-- <select
      v-else-if="isActivityType"
      class="base-input__field"
      v-model="inputValue"
    >
      <option
        v-for="activityType in activityTypesStore.activityTypes"
        :key="activityType.id"
        :value="activityType.title"
      >
        {{ activityType.title }}
      </option>
    </select> -->
			<label class="container__label label-box">
				<h5 class="label-box__text">{{ label }}</h5>
				<h5 v-if="isMandatory" class="label-box__mandatory">*</h5>
			</label>
			<div class="container__input-box input-box" :class="{ 'input-box--error': errorMessage }">
				<input
					class="input-box__input"
					v-model="inputValue"
					:placeholder="placeholder"
					:type="inputType"
					@blur="emit('blur', inputValue)"
					@focus="emit('focus', inputValue)"
				/>
				<SvgLoader v-if="isPassword" class="input-box__icon" :name="eyeIconName" @click="togglePasswordVisibility" />
			</div>
			<h6 class="container__error-message">{{ toPersianDigits(errorMessage) }}</h6>
		</div>
	</div>
</template>

<style lang="scss" scoped>
	.the-input {
		width: 100%;
	}

	.container {
		width: 100%;
		@include flexbox(column, start, right, space(0));

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

		.input-box {
			background-image: linear-gradient(90deg, var(--bg-700), var(--bg-900));
			border-right: space(4) solid var(--text-100);
			border-top-left-radius: space(4);
			border-bottom-left-radius: space(4);
			outline: space(0.5) solid var(--text-500);
			@include flexbox(row, center, center, space(0), nowrap);

			&__input {
				background-color: transparent;
				font-size: space(7);
				color: var(--text-900);
				padding-inline: space(2);
				border: none;
				outline: none;
				width: 100%;
				height: space(20);
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

			&__icon {
				color: var(--primary-100);
				margin-inline: space(4);
				cursor: pointer;
			}
		}

		&__error-message {
			user-select: none;
			min-height: space(12);
			color: var(--danger-300);
			@include flexbox();
			@include lineClamp(1);
		}
	}
</style>
