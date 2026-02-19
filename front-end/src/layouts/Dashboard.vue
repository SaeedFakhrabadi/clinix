<script setup>
	import { computed } from 'vue';
	import { useCurrentUserStore } from '@/stores/currentUser';

	const currentUserStore = useCurrentUserStore();

	const userRole = computed(() => currentUserStore?.currentUser?.role?.value);
	const sidebarItems = computed(() => {
		if (userRole.value === 'PATIENT') {
			return [
				{ label: 'اعلان های دریافتی', name: 'Notifications' },
				{ label: 'اطلاعات شخصی', name: 'Profile' },
				{ label: 'نوبت ها', name: 'Reservations' },
				{ label: 'تاریخچه تراکنش ها', name: 'Transactions' },
				{ label: 'ثبت انتقادات و پیشنهادات', name: 'Home' },
			];
		} else if (userRole.value === 'DOCTOR') {
			return [
				{ label: 'اعلان های دریافتی', name: 'Notifications' },
				{ label: 'اطلاعات شخصی', name: 'Profile' },
				{ label: 'مدیریت نوبت ها', name: 'Reservations' },
				{ label: 'ثبت انتقادات و پیشنهادات', name: 'Home' },
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
				<router-view class="dashboard__page" />
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
			overflow: auto;
			@include flexbox(row, start, start, space(0));
		}

		&__page {
			width: 100%;
			padding: space(8) space(6);
			@include flexbox(column, start, start, space(8), nowrap);
		}
	}
</style>
