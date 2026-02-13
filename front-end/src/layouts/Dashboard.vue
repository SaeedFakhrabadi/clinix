<script setup>
	import { computed } from 'vue';
	import { useCurrentUserStore } from '@/stores/currentUser';

	const currentUserStore = useCurrentUserStore();

	const userRole = computed(() => currentUserStore?.currentUser?.role?.value);
	const sidebarItems = computed(() => {
		if (userRole.value === 'PATIENT') {
			return [
				{ label: 'اطلاعات شخصی', name: 'Profile' },
				{ label: 'نوبت ها', name: 'Reservations' },
				{ label: 'تاریخچه تراکنش ها', name: 'Transactions' },
				{ label: 'ارتباط با مدیریت سیستم', name: 'Home' },
			];
		} else if (userRole.value === 'DOCTOR') {
			return [
				{ label: 'اطلاعات شخصی', name: 'Profile' },
				{ label: 'دکترم', name: 'Reservations' },
				{ label: 'دکتر نیستم', name: 'Transactions' },
			];
		}
	});
</script>

<template>
	<div class="dashboard">
		<TheNavbar />
		<main class="dashboard__main-content">
			<TheSidebar :items="sidebarItems" />
			<div class="dashboard__content">
				<router-view />
			</div>
		</main>
	</div>
</template>

<style lang="scss" scoped>
	.dashboard {
		height: 100vh;

		&__main-content {
			height: calc(100% - space(32));
			padding-top: space(32);
			margin: 0 auto;
			max-width: $xl;
			@include flexbox(row, start, start, space(0));
		}

		&__content {
			height: 100%;
			flex: 1;
			@include flexbox(row, start, start, space(0));
			overflow: auto;
		}
	}
</style>
