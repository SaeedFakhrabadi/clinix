<script setup>
	import { useForm, useField } from 'vee-validate';
	import { signUpSchema } from '@/schemas';
	import { useRouter } from 'vue-router';

	const router = useRouter();

	const { handleSubmit } = useForm({
		validationSchema: signUpSchema,
		initialValues: {
			name: '',
			email: '',
			phoneNumber: '',
			password: '',
		},
	});

	const { value: name, errorMessage: nameError } = useField('name');
	const { value: email, errorMessage: emailError } = useField('email');
	const { value: phoneNumber, errorMessage: phoneNumberError } = useField('phoneNumber');
	const { value: password, errorMessage: passwordError } = useField('password');

	const onSubmit = handleSubmit(() => {
		router.push({ name: 'Login' });
	});
</script>

<template>
	<form class="form" @submit.prevent="onSubmit">
		<h3 class="form__title">ثبت نام</h3>
		<div class="form__inputs">
			<TheInput
				label="نام"
				placeholder="نام خود را وارد کنید"
				v-model="name"
				:error-message="nameError"
			/>
			<TheInput
				label="ایمیل"
				placeholder="مانند : example.gmail.com"
				v-model="email"
				:error-message="emailError"
			/>
			<TheInput
				label="شماره تلفن"
				placeholder="مانند : 09123456789"
				v-model="phoneNumber"
				:digits-only="true"
				:error-message="phoneNumberError"
			/>
			<TheInput
				label="رمز عبور"
				type="password"
				placeholder="رمز عبور دلخواه خود را وارد کنید"
				v-model="password"
				:error-message="passwordError"
			/>
		</div>
		<TheButton type="submit" label="ثبت نام" />
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
