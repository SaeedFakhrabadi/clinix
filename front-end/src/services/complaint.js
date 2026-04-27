import api from '@/services';

export const createComplaint = (subject, message) => {
	return api.post('/v1/complaint/', {
		subject: subject,
		message: message,
	});
};
