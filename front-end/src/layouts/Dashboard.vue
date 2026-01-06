<script setup>
	const sidebarItems = [
		{ label: 'اطلاعات شخصی', name: 'Profile' },
		{ label: 'تاریخچه نوبت ها', name: 'History' },
		{ label: 'لیست پزشکان', name: 'DoctorsList' },
		{ label: 'اعلان ها و پیام ها', name: 'Home' },
		{ label: 'امور مالی', name: 'Home' },
		// { label: 'ارتباط با مدیریت سیستم', name: 'Home' },
	];
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
			max-width: space(650);
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
