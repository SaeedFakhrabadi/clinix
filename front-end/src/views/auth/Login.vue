<script setup>
	import { ref } from 'vue';
	import router from '../../routers';

	// داده های فرم
	const email = ref('');
	const phone = ref('');
	const password = ref('');

	// ارورها
	const errors = ref({
		email: '',
		phone: '',
		password: '',
	});

	// اعتبارسنجی ساده هنگام submit
	const validate = () => {
		let valid = true;
		errors.value.email = /\S+@\S+\.\S+/.test(email.value) ? '' : 'ایمیل معتبر نیست';
		errors.value.phone = /^\d{10,15}$/.test(phone.value) ? '' : 'شماره تلفن معتبر نیست';
		errors.value.password = password.value.length >= 6 ? '' : 'رمز عبور باید حداقل 6 کاراکتر باشد';

		Object.values(errors.value).forEach((e) => {
			if (e) valid = false;
		});
		return valid;
	};

	const handleSubmit = () => {
		router.push({ name: 'RecoveryPassword' });
		if (validate()) {
			alert('ثبت‌نام با موفقیت انجام شد!');
			// اینجا میتونی API call بزنی
		}
	};
</script>

<template>
	<form class="form" @submit.prevent="handleSubmit">
		<h3 class="form__title">ورود</h3>
		<TheInput
			label="شماره تلفن / ایمیل"
			:is-mandatory="true"
			placeholder="شماره تلفن یا ایمیل خود را وارد کنید"
			v-model="email"
			:error-message="errors.email"
		/>
		<TheInput
			label="رمز عبور"
			:is-mandatory="true"
			type="password"
			placeholder="رمز عبور"
			v-model="password"
			:error-message="errors.password"
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
