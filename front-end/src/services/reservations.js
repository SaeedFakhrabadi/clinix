import api from '@/services/index';

export const createReservation = (did, pid, time) => {
	return api.post('/v1/reservations/create/', {
		doctor_id: did,
		user_id: pid,
		time: time,
	});
};

export const getReservations = (uid) => {
	return api.get(`/v1/reservations/${uid}/`);
};

export const deleteReservation = (rid) => {
	return api.delete(`/v1/reservations/delete/${rid}/`);
};
