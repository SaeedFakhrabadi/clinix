<script setup>
	import { ref } from 'vue';
	import router from '../../routers';

	// داده های فرم
	const name = ref('');
	const email = ref('');
	const phone = ref('');
	const password = ref('');
	const confirmPassword = ref('');

	// ارورها
	const errors = ref({
		name: '',
		email: '',
		phone: '',
		password: '',
		confirmPassword: '',
	});

	// اعتبارسنجی ساده هنگام submit
	const validate = () => {
		let valid = true;
		errors.value.name = name.value.trim() ? '' : 'نام الزامی است';
		errors.value.email = /\S+@\S+\.\S+/.test(email.value) ? '' : 'ایمیل معتبر نیست';
		errors.value.phone = /^\d{10,15}$/.test(phone.value) ? '' : 'شماره تلفن معتبر نیست';
		errors.value.password = password.value.length >= 6 ? '' : 'رمز عبور باید حداقل 6 کاراکتر باشد';
		errors.value.confirmPassword = confirmPassword.value === password.value ? '' : 'تکرار رمز عبور اشتباه است';

		Object.values(errors.value).forEach((e) => {
			if (e) valid = false;
		});
		return valid;
	};

	const handleSubmit = () => {
		router.push({ name: 'SignUp' });
		if (validate()) {
			alert('ثبت‌نام با موفقیت انجام شد!');
			// اینجا میتونی API call بزنی
		}
	};
</script>

<template>
	<form class="form" @submit.prevent="handleSubmit">
		<h3 class="form__title">تغییر رمز</h3>
		<TheInput
      v-model="name"
			label="نام"
			:is-mandatory="true"
			placeholder="نام خود را وارد کنید"
			:error-message="errors.name"
		/>
		<TheInput
			label="ایمیل"
			:is-mandatory="true"
			placeholder="ایمیل خود را وارد کنید"
			v-model="email"
			:error-message="errors.email"
		/>
		<TheInput
			label="شماره تلفن"
			:is-mandatory="true"
			placeholder="شماره تلفن"
			v-model="phone"
			:error-message="errors.phone"
		/>
		<TheInput
			label="رمز عبور"
			:is-mandatory="true"
			type="password"
			placeholder="رمز عبور"
			v-model="password"
			:error-message="errors.password"
		/>
		<TheInput
			label="تکرار رمز عبور"
			:is-mandatory="true"
			type="password"
			placeholder="رمز عبور را دوباره وارد کنید"
			v-model="confirmPassword"
			:error-message="errors.confirmPassword"
		/>
		<TheButton type="submit" label="ثبت نام"></TheButton>
	</form>
</template>

<style lang="scss" scoped>
	.form {
		&__title {
			text-align: center;
			color: var(--text-900);
		}
	}
</style>
