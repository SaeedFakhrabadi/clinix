import { computed } from 'vue';
import { useRoute } from 'vue-router';
import { defineStore } from 'pinia';

export const useActiveTabStore = defineStore(
	'activeTab',
	() => {
		const activeTab = ref('LLLL');

		const setActiveTab = (tab) => {
			activeTab.value = tab;
		};

		return {
			activeTab,
			setActiveTab,
		};
	},
	{
		persist: {
			key: 'activeTab',
			storage: sessionStorage,
		},
	},
);
