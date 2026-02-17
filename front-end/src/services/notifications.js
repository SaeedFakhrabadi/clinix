import api from '@/services/index';

export const getNotifications = (user) => {
	if (user?.role?.value === 'DOCTOR') {
		return api.get('/v1/notifications/', {
			params: {
				doctor_id: user?.id,
			},
		});
	}

	if (user?.role?.value === 'PATIENT') {
		return api.get('/v1/notifications/', {
			params: {
				user_id: user?.id,
			},
		});
	}
};
