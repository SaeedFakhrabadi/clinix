import api from '@/services';

export const doctorsList = () => {
	return api.get('/v1/doctors/');
};

export const doctorDetails = (did) => {
	return api.get(`/v1/doctors/${did}/`);
};

export const createComment = (uid, did, comment, score) => {
	return api.post('/v1/comments/create/', {
		user_id: uid,
		doctor_id: did,
		comment: comment,
		score: score,
	});
};
