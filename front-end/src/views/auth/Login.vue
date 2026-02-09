<script setup>
	import { useForm, useField } from 'vee-validate';
	import { loginSchema } from '@/schemas';
	import { useRouter } from 'vue-router';
	import { useCurrentUserStore } from '@/stores/currentUser';
	import { login } from '@/services/auth';
	import { useToast } from 'vue-toastification';

	const router = useRouter();
	const toast = useToast();
	const currentUserStore = useCurrentUserStore();

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

	const onSubmit = async () => {
		const toastId = toast.info('...در حال بررسی اطلاعات', {
			timeout: false,
			closeOnClick: false,
		});

		try {
			const response = await login(identifier.value, password.value);

			const userInfo = response?.data;
			currentUserStore?.setCurrentUser(userInfo);

			toast.dismiss(toastId);
			toast.success(response?.data?.message);

			router.push({ name: 'Profile' });
		} catch (error) {
			console.error('Error : ', error?.response?.data || error?.message);

			toast.dismiss(toastId);
			toast.error(error?.response?.data?.message ?? 'خطا در برقراری ارتباط')
		}
	};

	const submitForm = handleSubmit(onSubmit);
</script>

<template>
	<form class="form" @submit.prevent="submitForm">
		<h3 class="form__title">ورود</h3>
		<div class="form__inputs">
			<TheInput
				label="شماره تلفن یا ایمیل"
				iconName="id-card"
				placeholder="شماره تلفن یا ایمیل خود را وارد کنید"
				v-model="identifier"
				:error-message="identifierError"
			/>
			<TheInput
				label="رمز عبور"
				iconName="password"
				type="password"
				placeholder="رمز عبور خود را وارد کنید"
				v-model="password"
				:error-message="passwordError"
			/>
			<h5 class="form__text">
				رمز عبور خود را فراموش کرده اید ؟
				<router-link class="form__link" :to="{ name: 'RecoveryPassword' }">
					بازیابی رمز عبور
				</router-link>
			</h5>
		</div>
		<TheButton type="submit" label="ورود" />
		<h5 class="form__text">
			حساب کاربری ندارید ؟
			<router-link class="form__link" :to="{ name: 'Register' }">
				ثبت نام
			</router-link>
		</h5>
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
			width: 100%;
			color: var(--text-900);
			text-align: center;
			margin-bottom: space(6);
		}

		&__link {
			color: var(--text-500);
			text-decoration: underline;
		}
	}
</style>
