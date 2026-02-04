import { ref } from 'vue';
import { defineStore } from 'pinia';

export const useCurrentUserStore = defineStore(
	'currentUser',
	() => {
		const currentUser = ref();

		const setCurrentUser = (userData) => {
			currentUser.value = userData;
		};

		return {
			currentUser,
			setCurrentUser,
		};
	},
	{
		persist: {
			key: 'currentUser',
			storage: sessionStorage,
		},
	},
);
