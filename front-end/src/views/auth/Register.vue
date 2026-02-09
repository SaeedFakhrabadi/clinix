<script setup>
	import { useForm, useField } from 'vee-validate';
	import { RegisterSchema } from '@/schemas';
	import { useRouter } from 'vue-router';
	import { useCurrentUserStore } from '@/stores/currentUser';
	import { register } from '@/services/auth';
	import { useToast } from 'vue-toastification';

	const router = useRouter();
	const toast = useToast();
	const currentUserStore = useCurrentUserStore();

	const { handleSubmit } = useForm({
		validationSchema: RegisterSchema,
		initialValues: {
			name: '',
			email: '',
			phoneNumber: '',
			password: '',
			confirmPassword: '',
		},
	});

	const { value: name, errorMessage: nameError } = useField('name');
	const { value: email, errorMessage: emailError } = useField('email');
	const { value: phoneNumber, errorMessage: phoneNumberError } =
		useField('phoneNumber');
	const { value: password, errorMessage: passwordError } = useField('password');
	const { value: confirmPassword, errorMessage: confirmPasswordError } =
		useField('confirmPassword');

	const onSubmit = async () => {
		const toastId = toast.info('...در حال ثبت اطلاعات', {
			timeout: false,
			closeOnClick: false,
		});

		try {
			const response = await register(
				name.value,
				email.value,
				phoneNumber.value,
				password.value,
			);

			const userInfo = response?.data;
			currentUserStore?.setCurrentUser(userInfo);

			toast.dismiss(toastId);
			toast.success(response?.data?.message);

			router.push({ name: 'Profile' });
		} catch (error) {
			console.error('Error : ', error?.response?.data || error?.message);

			toast.dismiss(toastId);
			toast.error(error?.response?.data?.message ?? 'خطا در برقراری ارتباط');
		}
	};

	const submitForm = handleSubmit(onSubmit);
</script>

<template>
	<form class="form" @submit.prevent="submitForm">
		<h3 class="form__title">ثبت نام</h3>
		<div class="form__inputs">
			<TheInput
				label="نام"
				iconName="user"
				placeholder="نام خود را وارد کنید"
				v-model="name"
				:error-message="nameError"
			/>
			<TheInput
				label="ایمیل"
				iconName="email"
				placeholder="مانند : example.gmail.com"
				v-model="email"
				:error-message="emailError"
			/>
			<TheInput
				label="شماره تلفن"
				iconName="phone"
				placeholder="مانند : 09123456789"
				v-model="phoneNumber"
				:digits-only="true"
				:error-message="phoneNumberError"
			/>
			<TheInput
				label="رمز عبور"
				iconName="password"
				type="password"
				placeholder="رمز عبور دلخواه خود را وارد کنید"
				v-model="password"
				:error-message="passwordError"
			/>
			<TheInput
				label="تکرار رمز عبور"
				iconName="password"
				type="password"
				placeholder="رمز عبور خود را مجدد وارد کنید"
				v-model="confirmPassword"
				:error-message="confirmPasswordError"
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
