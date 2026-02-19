import api from '@/services/index';

export const getNotifications = () => {
	return api.get('/v1/notifications/');
};
