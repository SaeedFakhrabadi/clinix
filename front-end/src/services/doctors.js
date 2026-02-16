import api from '@/services';

export const doctorsList = () => {
	return api.get('/v1/doctors/', {});
};

export const doctorDetails = (did) => {
	return api.get(`/v1/doctors/${did}/`);
};
