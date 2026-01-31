import * as yup from 'yup';

const REGEXES = {
	EMAIL: /^[A-Za-z][A-Za-z0-9._%+-]*@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$/,
	PHONE_NUMBER: /^09\d{9}$/,
	PASSWORD: /^(?=.*[A-Za-z])[A-Za-z0-9!@#$%^&*()_\-+={};:'",.<>/?|~`]{8,}$/,
};

const REQUIRED = {
	NAME: 'نام الزامی است',
	EMAIL: 'ایمیل الزامی است',
	PHONE: 'شماره تلفن الزامی است',
	PASSWORD: 'رمز عبور الزامی است',
	OLD_PASSWORD: 'رمز عبور قبلی الزامی است',
	NEW_PASSWORD: 'رمز عبور فعلی الزامی است',
	CONFIRM_PASSWORD: 'تکرار رمز عبور الزامی است',
	IDENTIFIER: 'شماره تلفن یا ایمیل الزامی است',
};

const INVALID = {
	EMAIL: 'ایمیل معتبر نیست',
	PHONE: 'شماره تلفن معتبر نیست',
	PASSWORD: 'رمز عبور باید حداقل 8 کاراکتر و شامل حداقل یک حرف انگلیسی باشد',
	IDENTIFIER: 'شماره تلفن یا ایمیل معتبر نیست',
	CONFIRM_PASSWORD: 'تکرار رمز عبور فعلی اشتباه است',
	SAME_PASSWORD: 'رمز عبور قبلی و فعلی یکسان هستند',
	MAX_20: 'حداکثر 20 کاراکتر مجاز است',
	MAX_40: 'حداکثر 40 کاراکتر مجاز است',
};

export const RegisterSchema = yup.object({
	name: yup.string().trim().max(20, INVALID.MAX_20).required(REQUIRED.NAME),

	email: yup
		.string()
		.trim()
		.max(40, INVALID.MAX_40)
		.required(REQUIRED.EMAIL)
		.matches(REGEXES.EMAIL, INVALID.EMAIL),

	phoneNumber: yup
		.string()
		.required(REQUIRED.PHONE)
		.matches(REGEXES.PHONE_NUMBER, INVALID.PHONE),

	password: yup
		.string()
		.max(20, INVALID.MAX_20)
		.required(REQUIRED.PASSWORD)
		.matches(REGEXES.PASSWORD, INVALID.PASSWORD),
});

export const loginSchema = yup.object({
	identifier: yup
		.string()
		.trim()
		.max(40, INVALID.MAX_40)
		.required(REQUIRED.IDENTIFIER)
		.test('is-email-or-phone', INVALID.IDENTIFIER, (value) => {
			if (!value) return true;
			return REGEXES.EMAIL.test(value) || REGEXES.PHONE_NUMBER.test(value);
		}),

	password: yup
		.string()
		.max(20, INVALID.MAX_20)
		.required(REQUIRED.PASSWORD)
		.matches(REGEXES.PASSWORD, INVALID.PASSWORD),
});

export const recoveryPasswordSchema = yup.object({
	identifier: yup
		.string()
		.trim()
		.max(40, INVALID.MAX_40)
		.required(REQUIRED.IDENTIFIER)
		.test('is-email-or-phone', INVALID.IDENTIFIER, (value) => {
			if (!value) return false;
			return REGEXES.EMAIL.test(value) || REGEXES.PHONE_NUMBER.test(value);
		}),
});

export const changePasswordSchema = yup.object({
	oldPassword: yup
		.string()
		.max(20, INVALID.MAX_20)
		.required(REQUIRED.OLD_PASSWORD)
		.matches(REGEXES.PASSWORD, INVALID.PASSWORD),

	newPassword: yup
		.string()
		.max(20, INVALID.MAX_20)
		.required(REQUIRED.NEW_PASSWORD)
		.matches(REGEXES.PASSWORD, INVALID.PASSWORD)
		.notOneOf([yup.ref('oldPassword')], INVALID.SAME_PASSWORD),

	confirmNewPassword: yup
		.string()
		.max(20, INVALID.MAX_20)
		.required(REQUIRED.CONFIRM_PASSWORD)
		.oneOf([yup.ref('newPassword')], INVALID.CONFIRM_PASSWORD),
});
