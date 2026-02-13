<script setup>
	import { useForm, useField } from 'vee-validate';
	import { recoveryPasswordSchema } from '@/schemas';
	import { useRouter } from 'vue-router';
	import { recoveryPassword } from '@/services/auth';
	import { useToast } from 'vue-toastification';

	const router = useRouter();
	const toast = useToast();

	const { handleSubmit } = useForm({
		validationSchema: recoveryPasswordSchema,
		initialValues: {
			email: '',
		},
	});

	const { value: email, errorMessage: emailError } = useField('email');

	const onSubmit = async () => {
		const toastId = toast.info('...در حال بررسی اطلاعات', {
			timeout: false,
			closeOnClick: false,
		});

		try {
			const response = await recoveryPassword(email.value);

			router.push({ name: 'ChangePassword' });

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
		<h3 class="form__title">بازیابی رمز عبور</h3>
		<h5 class="form__text">
			ایمیل خود را وارد کنید تا کد تایید برای شما ارسال شود.
		</h5>
		<TheInput
			label="ایمیل"
			icon-name="email"
			placeholder="ایمیل خود را وارد کنید"
			v-model="email"
			:error-message="emailError"
		/>
		<h5 class="form__text">
			<router-link class="form__link" :to="{ name: 'Login' }">
				بازگشت به صفحه ورود
			</router-link>
		</h5>
		<TheButton type="submit" label="درخواست ارسال کد تایید" />
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

		&__link {
			color: var(--text-500);
			text-decoration: underline;
		}
	}
</style>
