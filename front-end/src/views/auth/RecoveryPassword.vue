<script setup>
	import { useForm, useField } from 'vee-validate';
	import { recoveryPasswordSchema } from '@/schemas';
	import { useRouter } from 'vue-router';

	const router = useRouter();

	const { handleSubmit } = useForm({
		validationSchema: recoveryPasswordSchema,
		initialValues: {
			identifier: '',
		},
	});

	const { value: identifier, errorMessage: identifierError } = useField('identifier');

	const onSubmit = handleSubmit(() => {
		router.push({ name: 'Login' });
	});
</script>

<template>
	<form class="form" @submit.prevent="onSubmit">
		<h3 class="form__title">بازنشانی رمز عبور</h3>
		<h5 class="form__text">
			برای بازنشانی رمز عبور ایمیل یا شماره تلفن خود را وارد کنید تا رمز عبور جدید برای شما ارسال
			شود
		</h5>
		<TheInput
			label="شماره تلفن / ایمیل"
			placeholder="شماره تلفن یا ایمیل خود را وارد کنید"
			v-model="identifier"
			:error-message="identifierError"
		/>
		<TheButton type="submit" label="بازنشانی رمز عبور" />
	</form>
</template>

<style lang="scss" scoped>
	.form {
		&__title {
			text-align: center;
			color: var(--text-900);
			border-bottom: space(0.5) solid var(--primary-100);
		}

		&__text {
			color: var(--text-900);
		}
	}
</style>
