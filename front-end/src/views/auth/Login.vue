<script setup>
	import { useForm, useField } from 'vee-validate';
	import { loginSchema } from '@/schemas';
	import { useRouter } from 'vue-router';

	const router = useRouter();

	const { handleSubmit } = useForm({
		validationSchema: loginSchema,
		initialValues: {
			identifier: '',
			password: '',
		},
	});

	const { value: identifier, errorMessage: identifierError } =
		useField('identifier');
	const { value: password, errorMessage: passwordError } = useField('password');

	const onSubmit = handleSubmit(() => {
		router.push({ name: 'Profile' });
	});
</script>

<template>
	<form class="form" @submit.prevent="onSubmit">
		<h3 class="form__title">ورود</h3>
		<div class="form__inputs">
			<TheInput
				label="شماره تلفن / ایمیل"
				placeholder="شماره تلفن یا ایمیل خود را وارد کنید"
				v-model="identifier"
				:error-message="identifierError"
			/>
			<TheInput
				label="رمز عبور"
				type="password"
				placeholder="رمز عبور"
				v-model="password"
				:error-message="passwordError"
			/>
		</div>
		<TheButton type="submit" label="ورود" />
		<div class="form__texts">
			<h5 class="form__text">
				حساب کاربری ندارید ؟
				<router-link class="form__link" :to="{ name: 'Register' }"
					>ثبت نام</router-link
				>
			</h5>
			<h5 class="form__text">
				رمز عبور خود را فراموش کرده اید ؟
				<router-link class="form__link" :to="{ name: 'RecoveryPassword' }">
					بازنشانی رمز عبور
				</router-link>
			</h5>
		</div>
	</form>
</template>

<style lang="scss" scoped>
	.form {
		&__title {
			text-align: center;
			color: var(--text-900);
			border-bottom: space(0.5) solid var(--primary-100);
		}

		&__inputs,
		&__texts {
			width: 100%;
		}

		&__text {
			color: var(--text-900);
			text-align: center;
		}

		&__link {
			color: var(--text-500);
			text-decoration: underline;
		}
	}
</style>
