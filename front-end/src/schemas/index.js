import * as yup from 'yup';

const EMAIL_REGEX = /^[A-Za-z][A-Za-z0-9]*@[A-Za-z0-9]+\.[A-Za-z]{2,}$/;
const PHONE_NUMBER_REGEX = /^09\d{9}$/;
const PASSWORD_REGEX = /^(?=.*[A-Za-z])[A-Za-z0-9!@#$%^&*()_\-+={};:'",.<>/?|~`]{8,}$/;

export const signUpSchema = yup.object({
	name: yup.string().trim().required('نام الزامی است'),

	email: yup.string().trim().required('ایمیل الزامی است').matches(EMAIL_REGEX, 'ایمیل معتبر نیست'),

	phoneNumber: yup
		.string()
		.required('شماره تلفن الزامی است')
		.matches(PHONE_NUMBER_REGEX, 'شماره تلفن معتبر نیست'),

	password: yup
		.string()
		.required('رمز عبور الزامی است')
		.matches(PASSWORD_REGEX, 'رمز عبور باید حداقل 8 کاراکتر و شامل حداقل یک حرف انگلیسی باشد'),
});

export const loginSchema = yup.object({
	identifier: yup
		.string()
		.trim()
		.required('ایمیل یا شماره تلفن الزامی است')
		.test('is-email-or-phone', 'ایمیل یا شماره تلفن معتبر نیست', (value) => {
			if (!value) return true;
			return EMAIL_REGEX.test(value) || PHONE_NUMBER_REGEX.test(value);
		}),

	password: yup
		.string()
		.required('رمز عبور الزامی است')
		.matches(PASSWORD_REGEX, 'رمز عبور باید حداقل 8 کاراکتر و شامل حداقل یک حرف انگلیسی باشد'),
});

export const recoveryPasswordSchema = yup.object({
	identifier: yup
		.string()
		.trim()
		.required('ایمیل یا شماره تلفن الزامی است')
		.test('is-email-or-phone', 'ایمیل یا شماره تلفن معتبر نیست', (value) => {
			if (!value) return false;
			return EMAIL_REGEX.test(value) || PHONE_NUMBER_REGEX.test(value);
		}),
});

export const changePasswordSchema = yup.object({
	oldPassword: yup
		.string()
		.required('رمز عبور قبلی الزامی است')
		.matches(PASSWORD_REGEX, 'رمز عبور باید حداقل 8 کاراکتر و شامل حداقل یک حرف انگلیسی باشد'),

	newPassword: yup
		.string()
		.required('رمز عبور فعلی الزامی است')
		.matches(PASSWORD_REGEX, 'رمز عبور باید حداقل 8 کاراکتر و شامل حداقل یک حرف انگلیسی باشد')
		.notOneOf([yup.ref('oldPassword')], 'رمز عبور قبلی و فعلی یکسان هستند'),

	confirmNewPassword: yup
		.string()
		.required('تکرار رمز عبور الزامی است')
		.oneOf([yup.ref('newPassword')], 'تکرار رمز عبور فعلی اشتباه است'),
});
