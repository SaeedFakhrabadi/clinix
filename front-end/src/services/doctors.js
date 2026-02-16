import api from '@/services/index';

export const doctorsList = () => {
	return api.get('/v1/doctors/', {});
};

export const doctorDetails = async (did) => {
	try {
		const response = await api.get(`/v1/doctors/${did}/`);
		return { data: response.data };
	} catch {
		return { data: getMockDoctorDetails(did) };
	}
};

function getMockDoctorDetails(did) {
	const mockByDid = [
		{
			did: 1,
			name: 'دکتر علی رضایی',
			field: 'قلب و عروق',
			location: 'تهران',
			score: 4.8,
			price: 200_000,
			experience: 15,
			start_working_hour: 8,
			end_working_hour: 21,
			reserved_times: {
				0: [14],
				1: [14, 19],
				2: [],
				3: [],
				4: [14],
				5: [],
				6: [],
				7: [],
				8: [14],
				9: [],
				10: [],
				11: [],
			},
			comments: [
				{
					score: 5,
					username: 'کاربر۱',
					comment: 'پزشک بسیار با تجربه و خوش برخورد.',
				},
				{
					score: 4,
					username: 'علی م',
					comment: 'نوبت به موقع داده شد، راضی بودم.',
				},
				{
					score: 5,
					username: 'سارا ک',
					comment: 'عالی بود، حتماً پیشنهاد می‌کنم.',
				},
			],
		},

		{
			did: 2,
			name: 'دکتر نسرین احمدی',
			field: 'مغز و اعصاب',
			location: 'اصفهان',
			score: 4.2,
			price: 300_000,
			experience: 12,
			start_working_hour: 9,
			end_working_hour: 15,
			reserved_times: {
				0: [10, 12],
				1: [13],
				2: [9, 11],
				3: [14],
				4: [],
				5: [10],
				6: [11],
				7: [12],
				8: [],
				9: [13],
				10: [],
				11: [],
			},
			comments: [
				{ score: 4, username: 'محمد ر', comment: 'تشخیص دقیق و درمان مؤثر.' },
				{
					score: 5,
					username: 'زهرا ن',
					comment: 'خیلی ممنون از رفتار محترمانه.',
				},
			],
		},

		{
			did: 3,
			name: 'دکتر سارا کریمی',
			field: 'پوست و مو',
			location: 'شیراز',
			score: 4.9,
			price: 250_000,
			experience: 8,
			start_working_hour: 8,
			end_working_hour: 14,
			reserved_times: {
				0: [8, 11],
				1: [10],
				2: [9, 12],
				3: [11],
				4: [],
				5: [8, 10],
				6: [9],
				7: [],
				8: [12],
				9: [],
				10: [8],
				11: [],
			},
			comments: [
				{
					score: 5,
					username: 'مریم ح',
					comment: 'بهترین متخصص پوست، نتیجه عالی.',
				},
			],
		},

		{
			did: 4,
			name: 'دکتر مهدی حسینی',
			field: 'اطفال',
			location: 'تبریز',
			score: 3.8,
			price: 180_000,
			experience: 6,
			start_working_hour: 10,
			end_working_hour: 18,
			reserved_times: {
				0: [12, 15],
				1: [16],
				2: [10, 14],
				3: [11, 13],
				4: [12],
				5: [],
				6: [15],
				7: [11],
				8: [14],
				9: [],
				10: [12],
				11: [],
			},
			comments: [
				{
					score: 4,
					username: 'پدر۱',
					comment: 'با بچه‌ها خیلی خوب برخورد می‌کند.',
				},
				{ score: 3, username: 'مادر۲', comment: 'نوبت کمی دیر داده شد.' },
			],
		},
	];

	const doctor = mockByDid.find((item) => item.did === Number(did));
	return doctor;
}
