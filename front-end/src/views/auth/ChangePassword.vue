<script setup>
	import { useForm, useField } from 'vee-validate';
	import { changePasswordSchema } from '@/schemas';
	import { useRouter } from 'vue-router';
	import { useCurrentUserStore } from '@/stores/currentUser';
	import { changePassword } from '@/services/auth';
	import { useToast } from 'vue-toastification';

	const router = useRouter();
	const toast = useToast();
	const currentUserStore = useCurrentUserStore();

	const { handleSubmit } = useForm({
		validationSchema: changePasswordSchema,
		initialValues: {
			verificationCode: '',
			newPassword: '',
			confirmPassword: '',
		},
	});

	const { value: verificationCode, errorMessage: verificationCodeError } =
		useField('verificationCode');
	const { value: newPassword, errorMessage: newPasswordError } =
		useField('newPassword');
	const { value: confirmPassword, errorMessage: confirmPasswordError } =
		useField('confirmPassword');

	const onSubmit = async () => {
		const toastId = toast.info('...در حال بررسی اطلاعات', {
			timeout: false,
			closeOnClick: false,
		});

		try {
			const response = await changePassword(
				verificationCode.value,
				newPassword.value,
			);

			const userInfo = response?.data;
			currentUserStore?.setCurrentUser(userInfo);

			router.push({ name: 'Notifications' });

			toast.dismiss(toastId);
			toast.success(response?.data?.message);
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
		<h3 class="form__title">تغییر رمز عبور</h3>
		<h5 class="form__text">
			کد تایید ارسال شده و رمز عبور جدید خود را وارد کنید.
		</h5>
		<div class="form__inputs">
			<div class="form__input-wrapper">
				<TheInput
					label="کد تایید"
					icon-name="message-check"
					placeholder="مانند : 123456"
					v-model="verificationCode"
					digits-only
					:error-message="verificationCodeError"
				/>
				<TheCountdownTimer class="form__counrdown-timer" />
			</div>
			<TheInput
				label="رمز عبور جدید"
				icon-name="password"
				type="password"
				placeholder="رمز عبور جدید خود را وارد کنید"
				v-model="newPassword"
				:error-message="newPasswordError"
			/>
			<TheInput
				label="تکرار رمز عبور"
				icon-name="password"
				type="password"
				placeholder="رمز عبور خود را مجدد وارد کنید"
				v-model="confirmPassword"
				:error-message="confirmPasswordError"
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

		&__text {
			width: 100%;
			text-align: right;
			color: var(--text-900);
		}

		&__inputs {
			width: 100%;
		}

		&__input-wrapper {
			position: relative;
		}
	}
</style>
