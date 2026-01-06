<script setup>
	import { useForm, useField } from 'vee-validate';
	import { changePasswordSchema } from '@/schemas';
	import { useRouter } from 'vue-router';

	const router = useRouter();

	const { handleSubmit } = useForm({
		validationSchema: changePasswordSchema,
		initialValues: {
			oldPassword: '',
			newPassword: '',
			confirmNewPassword: '',
		},
	});

	const { value: oldPassword, errorMessage: oldPasswordError } =
		useField('oldPassword');
	const { value: newPassword, errorMessage: newPasswordError } =
		useField('newPassword');
	const { value: confirmNewPassword, errorMessage: confirmNewPasswordError } =
		useField('confirmNewPassword');

	const onSubmit = handleSubmit(() => {
		router.push({ name: 'Profile' });
	});
</script>

<template>
	<form class="form" @submit.prevent="onSubmit">
		<h3 class="form__title">تغییر رمز عبور</h3>
		<div class="form__inputs">
			<TheInput
				label="رمز عبور قبلی"
				type="password"
				placeholder="رمز عبور قبلی خود را وارد کنید"
				v-model="oldPassword"
				:error-message="oldPasswordError"
			/>
			<TheInput
				label="رمز عبور جدید"
				type="password"
				placeholder="رمز عبور جدید خود را وارد کنید"
				v-model="newPassword"
				:error-message="newPasswordError"
			/>
			<TheInput
				label="تکرار رمز عبور جدید"
				type="password"
				placeholder="رمز عبور جدید خود را مجدد وارد کنید"
				v-model="confirmNewPassword"
				:error-message="confirmNewPasswordError"
			/>
		</div>
		<TheButton type="submit" label="تغییر رمز عبور" />
	</form>
</template>

<style lang="scss" scoped>
	.form {
		&__title {
			text-align: center;
			color: var(--text-900);
			border-bottom: space(0.5) solid var(--primary-100);
		}

		&__inputs {
			width: 100%;
		}
	}
</style>
