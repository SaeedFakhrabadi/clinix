import api from '@/services/index';

export const doctorsList = () => {
	return api.get('/v1/doctors/', {});
};
