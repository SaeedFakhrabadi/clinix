<script setup>
	import { useForm, useField } from 'vee-validate';
	import { loginSchema } from '@/schemas';
	import { useRouter } from 'vue-router';
	import { useCurrentUserStore } from '@/stores/currentUser';
	import { login } from '@/services/auth';

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

	const onSubmit = async () => {
		try {

			const currentUserStore = useCurrentUserStore();
			const response = await login(identifier.value, password.value);
			console.log("response", response);
			
			const userData = {
				identifier: identifier.value,
				password: password.value,
			};
			currentUserStore.setCurrentUser(userData);
			router.push({ name: 'Profile' });
		} catch (error) {
			console.error("Error : ", error.response?.data || error.message);
		}

	};

	// const onSubmit = async () => {
  // const toastId = toast.info("...در حال بررسی اطلاعات", {
  //   timeout: false,
  //   closeOnClick: false,
  // });

  // try {
  //   const response = await loginUser(email.value, password.value);

  //   const token = response.data.data.accessToken;
  //   userInfoStore.setToken(token);

  //   const userInfoResponse = await getUserInfo(token);

  //   userInfoStore.setUserInfo(userInfoResponse.data.data);

  //   toast.dismiss(toastId);
  //   toast.success(".با موفقیت وارد شدید");

  //   router.push({ name: "Home" });
  // } catch (error) {
  //   emailResponseError.value = true;
  //   passwordResponseError.value = true;
  //   console.error("Error : ", error.response?.data || error.message);

  //   const errorMessage = error?.response?.data?.data?.message?.fa;
  //   toast.dismiss(toastId);
  //   if (errorMessage === "ایمیل یا پسورد معتبر نمیباشد!") {
  //     toast.error("!ایمیل یا رمز عبور معتبر نیست");
  //   } else {
  //     toast.error("!خطا در ورود");
  //   }
  // }
// };

const submitForm = handleSubmit(onSubmit);
</script>

<template>
	<form class="form" @submit.prevent="submitForm">
		<h3 class="form__title">ورود</h3>
		<div class="form__inputs">
			<TheInput
				label="شماره تلفن یا ایمیل"
				iconName="user"
				placeholder="شماره تلفن یا ایمیل خود را وارد کنید"
				v-model="identifier"
				:error-message="identifierError"
			/>
			<TheInput
				label="رمز عبور"
				iconName="password"
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
