<script setup>
	// Theme
	import { ref, onMounted, watch, computed } from 'vue';

	const savedTheme = localStorage.getItem('theme');
	const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
	const theme = ref(savedTheme || (prefersDark ? 'dark' : 'light'));
	const isLightTheme = computed(() => theme.value === 'light');

	const toggleTheme = () => {
		theme.value = theme.value === 'light' ? 'dark' : 'light';
	};

	watch(theme, (newTheme) => {
		document.documentElement.setAttribute('data-theme', newTheme);
		localStorage.setItem('theme', newTheme);
	});

	onMounted(() => {
		document.documentElement.setAttribute('data-theme', theme.value);
	});

	// Tabs
	import { useActiveTabStore } from '@/stores/activeTab';
	import { useRouter } from 'vue-router';

	const router = useRouter();
	const activeTabStore = useActiveTabStore();

	const isActiveTab = (tab) => activeTabStore.activeTab === tab;

	const tabs = [
		{ name: 'Landing', label: 'خانه' },
		{ name: 'Profile', label: 'پروفایل' },
		{ name: 'Register', label: 'ثبت نام' },
		{ name: 'Login', label: 'ورود' },
	];
</script>

<template>
	<nav class="navbar">
		<div class="navbar__container">
			<router-link class="navbar__brand brand" :to="{ name: 'Landing' }">
				<h1 class="brand__text">CLINIX</h1>
			</router-link>
			<div class="navbar__bergur bergur"></div>
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
				<TheButton
					@click="toggleTheme"
					type="hollow"
					:label="isLightTheme ? 'تاریک' : 'روشن'"
					iconName="eye"
				/>
				<TheButton
					type="submit"
					label="ورود"
					bgColorHover="danger-700"
					@click="router.push({ name: 'Login' })"
				/>
				<TheButton
					type="cancel"
					label="ثبت نام"
					@click="router.push({ name: 'Register' })"
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
			width: space(650);
			@include flexbox(row, space-between);
		}

		.brand {
			background-color: var(--primary-500);
			width: space(100);
			height: space(32);
			transition: all 0.4s ease;
			@include flexbox();

			&__text {
				color: var(--text-900);
			}
		}

		.brand:hover {
			background-color: var(--primary-100);
		}

		.bergur {
			width: space(20);
			height: space(20);
			background-color: red;
			margin-left: space(6);
			@media (min-width: space(288)) {
				display: none;
			}
		}

		.menu {
			height: space(20);
			@include flexbox(column, center, center, space(5));
			@media (max-width: space(496)) {
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
			padding-inline: space(5);
			width: space(120);
			@include flexbox(row, center, center, space(8), nowrap);
			@media (max-width: space(288)) {
				display: none;
			}
		}
	}
</style>
