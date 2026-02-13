import api from '@/services/index';

export const login = (identifier, password) => {
	return api.post('/v1/auth/login/', {
		identifier: identifier,
		password: password,
	});
};

export const register = (name, email, phoneNumber, password) => {
	return api.post('/v1/auth/register/', {
		username: name,
		email: email,
		phonenumber: phoneNumber,
		password: password,
	});
};

export const recoveryPassword = (email) => {
	return api.post('/v1/auth/forgot_password/', {
		identifier: email,
	});
};

export const changePassword = (verificationCode, newPassword) => {
	return api.post('/v1/auth/reset_password/', {
		verificationCode: verificationCode,
		newPassword: newPassword,
	});
};

export const editProfile = (name, email, phoneNumber) => {
	return api.post('/v1/auth/profile/', {
		username: name,
		email: email,
		phonenumber: phoneNumber,
	});
};
