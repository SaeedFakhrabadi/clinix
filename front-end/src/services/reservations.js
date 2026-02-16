import api from '@/services/index';

export const createReservation = (did, pid, time) => {
	return api.post('/v1/reservations/create', {
		doctor_id: did,
		user_id: pid,
		time: time,
	});
};

// export const getReservations = () => {
// 	return api.post('/v1/reservations', {
// 	});
// };