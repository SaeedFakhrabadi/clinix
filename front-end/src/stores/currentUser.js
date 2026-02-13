import { ref } from 'vue';
import { defineStore } from 'pinia';

export const useCurrentUserStore = defineStore(
	'currentUser',
	() => {
		const currentUser = ref(null);

		const mappedRole = (role) => {
			if (role === 'PATIENT') return 'بیمار';
			if (role === 'DOCTOR') return 'پزشک';
		};

		const setCurrentUser = (userInfo) => {
			currentUser.value = {
				id: userInfo?.user?.id,
				name: userInfo?.user?.username,
				email: userInfo?.user?.email,
				phoneNumber: userInfo?.user?.phonenumber,
				role: {
					// label: mappedRole(userInfo?.user?.role),
					// value: userInfo?.user?.role,
					label: 'بیمار',
					value: 'PATIENT',
				},
			};
		};

		const removeCurrentUser = () => {
			currentUser.value = null;
		};

		return {
			currentUser,
			setCurrentUser,
			removeCurrentUser,
		};
	},
	{
		persist: {
			key: 'currentUser',
			storage: sessionStorage,
		},
	},
);
