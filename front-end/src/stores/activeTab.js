import { computed } from 'vue';
import { useRoute } from 'vue-router';
import { defineStore } from 'pinia';

export const useActiveTabStore = defineStore(
	'activeTab',
	() => {
		const route = useRoute();

		const activeTab = computed(() => route.matched[1].name);

		return {
			activeTab,
		};
	},
	{
		persist: {
			key: 'activeTab',
			storage: sessionStorage,
		},
	},
);
