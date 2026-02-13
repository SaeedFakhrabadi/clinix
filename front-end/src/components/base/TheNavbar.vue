<script setup>
	// Theme
	import { ref, onMounted, watch, computed } from 'vue';

	const savedTheme = sessionStorage.getItem('theme');
	const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
	const theme = ref(savedTheme || (prefersDark ? 'dark' : 'light'));
	const isLightTheme = computed(() => theme.value === 'light');

	const toggleTheme = () => {
		theme.value = theme.value === 'light' ? 'dark' : 'light';
	};

	watch(theme, (newTheme) => {
		document.documentElement.setAttribute('data-theme', newTheme);
		sessionStorage.setItem('theme', newTheme);
	});

	onMounted(() => {
		document.documentElement.setAttribute('data-theme', theme.value);
	});

	// Tabs
	import { useRouter } from 'vue-router';
	import { storeToRefs } from 'pinia';
	import { useActiveTabStore } from '@/stores/activeTab';
	import { useCurrentUserStore } from '@/stores/currentUser';

	const router = useRouter();
	const activeTabStore = useActiveTabStore();
	const currentUserStore = useCurrentUserStore();
	const { currentUser } = storeToRefs(currentUserStore);

	const isActiveTab = (tab) => activeTabStore.activeTab === tab;

	const tabs = [
		{ name: 'Landing', label: 'خانه' },
		{ name: 'DoctorsList', label: 'جستجوی پزشکان' },
		{ name: 'Profile', label: 'پروف' },
		{ name: 'ChangePassword', label: 'تغییر رمز' },
	];

	const logout = () => {
		router.push({ name: 'Login' });
		currentUserStore.removeCurrentUser();
	};
</script>

<template>
	<nav class="navbar">
		<div class="navbar__container">
			<router-link class="navbar__brand brand" :to="{ name: 'Landing' }">
				<h1 class="brand__text">CLINIX</h1>
			</router-link>
			<div class="navbar__burger burger">
				<SvgLoader class="burger__icon" name="burger-menu" />
			</div>
			<ul class="navbar__menu menu">
				<li v-for="(tab, index) in tabs" :key="index" class="menu__item">
					<h4 v-if="index > 0" class="menu__divider">|</h4>
					<router-link
						:to="{ name: tab.name }"
						class="menu__tab"
						:class="{ 'menu__tab--active': isActiveTab(tab.name) }"
					>
						{{ tab.label }}
					</router-link>
				</li>
			</ul>
			<section class="navbar__buttons buttons">
				<SvgLoader
					class="buttons__theme-icon"
					:name="isLightTheme ? 'moon' : 'sun'"
					@click="toggleTheme"
				/>
				<TheButton
					v-if="!currentUser"
					class="buttons__button"
					type="cancel"
					label="ثبت نام"
					@click="router.push({ name: 'Register' })"
				/>
				<TheButton
					v-if="!currentUser"
					class="buttons__button"
					type="submit"
					label="ورود"
					@click="router.push({ name: 'Login' })"
				/>
				<TheButton
					v-if="currentUser"
					class="buttons__button"
					type="cancel"
					label="مشاهده پروفایل"
					@click="router.push({ name: 'Profile' })"
				/>
				<TheButton
					v-if="currentUser"
					class="buttons__button buttons__button-exit"
					type="submit"
					label="خروج"
					@click="logout"
				/>
			</section>
		</div>
	</nav>
</template>

<style lang="scss" scoped>
	.navbar {
		position: fixed;
		top: space(0);
		background-color: var(--bg-900);
		box-shadow: space(0) space(2) space(4) var(--text-100);
		width: 100%;
		height: space(32);
		z-index: 1;
		@include flexbox();

		&__container {
			width: $xl;
			@include flexbox(row, space-between, center, space(0), nowrap);
		}

		.brand {
			background-color: var(--primary-500);
			width: space(100);
			height: space(32);
			transition: all 0.4s ease;
			@include flexbox();

			&:hover {
				background-color: var(--primary-100);
			}

			&__text {
				color: var(--text-900);
			}
		}

		.burger {
			height: space(20);
			margin-left: space(6);

			@media (min-width: $md) {
				display: none;
			}

			&__icon {
				cursor: pointer;
				color: var(--text-900);
			}
		}

		.menu {
			height: space(20);
			@include flexbox(column, center, center, space(5));

			@media (max-width: $md) {
				display: none;
			}

			&__item {
				height: 100%;
				@include flexbox(column, center, center, space(5));
			}

			&__divider {
				color: var(--text-100);
				user-select: none;
			}

			&__tab {
				height: 100%;
				color: var(--title-500);
				transition: all 0.5s ease;
				padding-inline: space(4);
				border-top-left-radius: space(3);
				border-top-right-radius: space(3);
				border-bottom: space(1) solid transparent;
				@include flexbox();

				&:hover {
					background-color: var(--primary-600);
				}

				&--active {
					border-bottom: space(1) solid var(--title-100);
				}
			}
		}

		.buttons {
			@include flexbox(row, space-between, center, space(6), nowrap);

			@media (max-width: $xl) {
				padding-inline: space(6);
			}
			@media (max-width: $md) {
				display: none;
			}

			&__theme-icon {
				color: var(--text-900);
				cursor: pointer;
			}

			&__button {
				width: space(50);
			}

			&__button-exit {
				background-color: var(--red-300);

				&:hover {
					background-color: var(--red-500);
				}
			}
		}
	}
</style>
