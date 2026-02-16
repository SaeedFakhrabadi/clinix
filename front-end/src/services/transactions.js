import api from '@/services/index';

export const createTransaction = (method, pid, price, type) => {
	return api.post('/v1/transactions/create/', {
		method: method,
		user_id: pid,
		price: price,
		type: type,
	});
};

export const getTransactions = (uid) => {
	return api.get(`/v1/transactions/history/${uid}/`);
};
